import asyncio
import json
import logging
import os
import shutil
from contextlib import AsyncExitStack
from typing import Any, List, Dict, TypedDict
from datetime import datetime, timedelta
from pathlib import Path
import re

from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import TextBlock, ToolUseBlock
from mcp import ClientSession, StdioServerParameters,types
from mcp.client.stdio import stdio_client

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# System prompt to guide LLM tool usage hierarchy
SYSTEM_PROMPT = """You are a helpful assistant that answers questions about LLM pricing.

CRITICAL TOOL USAGE HIERARCHY - Follow this order strictly:

1. CHECK DATABASE FIRST:
   - Use read_query to check the pricing_plans table for existing data
   - Query example: SELECT * FROM pricing_plans WHERE company_name LIKE '%<company>%'
   - If data exists and is relevant, use it to answer the query

2. CHECK CACHED SCRAPES:
   - If no DB data, use extract_scraped_info with the company name/domain
   - This loads already-scraped content without making new requests


3. SCRAPE AS LAST RESORT:
   - Only use scrape_websites if data doesn't exist in DB or cache
   - This makes actual HTTP requests and should be avoided when possible

Always prefer existing data over fresh scraping to reduce API calls and costs.

PARALLEL TOOL EXECUTION:
- When you need to perform multiple independent operations, call ALL tools simultaneously in a single response
- For example, if asked about multiple companies, check the database for all companies in ONE response
- IMPORTANT: The scrape_websites tool accepts a dictionary of multiple websites and returns ALL results at once
- Do NOT call scrape_websites multiple times for different subsets - pass ALL websites in ONE call
- This significantly reduces latency by executing tools in parallel rather than sequentially"""

# ===========================================================================
#                            Type Definitions
# ===========================================================================
class ToolDefinition(TypedDict):
    name: str
    description: str
    input_schema: dict

# ===========================================================================
#                            Configuration
# ===========================================================================

class Configuration:
    """Manages configuration and environment variables for the MCP client."""

    def __init__(self) -> None:
        """Initialize configuration with environment variables."""
        self.load_env()
        self.api_key = os.getenv("ANTHROPIC_API_KEY")

    @staticmethod
    def load_env() -> None:
        """Load environment variables from .env file."""
        load_dotenv()

    @staticmethod
    def load_config(file_path: str | Path) -> dict[str, Any]:
        """Load server configuration from JSON file.

        Args:
            file_path: Path to the JSON configuration file.

        Returns:
            Dict containing server configuration.

        Raises:
            FileNotFoundError: If configuration file doesn't exist.
            JSONDecodeError: If configuration file is invalid JSON.
            ValueError: If configuration file is missing required fields.
        """
        try:
            with open(file_path) as config_file:
                config = json.load(config_file)

            if 'mcpServers' not in config:
                raise ValueError(
                    "Configuration file missing 'mcpServers' field")

            return config
        except FileNotFoundError:
            logger.warning(f"file was not found: {file_path}")
            raise
        except json.JSONDecodeError:
            logger.warning(f"file: {file_path} was not abled to be parsed")
            raise
        except ValueError:
            logger.warning(f"file: {file_path} has value error")
            raise

    @property
    def anthropic_api_key(self) -> str:
        """Get the Anthropic API key.

        Returns:
            The API key as a string.

        Raises:
            ValueError: If the API key is not found in environment variables.
        """
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        return self.api_key

# ===========================================================================
#                    MCP Server Manager
# ===========================================================================

class Server:
    """Manages MCP server connections and tool execution."""

    def __init__(self, name: str, config: dict[str, Any]) -> None:
        self.name: str = name
        self.config: dict[str, Any] = config
        self.stdio_context: Any | None = None
        self.session: ClientSession | None = None
        self._cleanup_lock: asyncio.Lock = asyncio.Lock()
        self.exit_stack: AsyncExitStack = AsyncExitStack()

    async def initialize(self) -> None:
        """Initialize the server connection."""
        command = shutil.which("npx") if self.config["command"] == "npx" else self.config["command"]
        if command is None:
            raise ValueError("The command must be a valid string and cannot be None.")

        # Implement the Server Parameter from the config
        server_params = StdioServerParameters(
            command=command,
            args=self.config.get("args", []),  # Get args from config
            env={**os.environ, **self.config["env"]
                 } if self.config.get("env") else None,
        )

        try:
            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            read, write = stdio_transport
            session = await self.exit_stack.enter_async_context(ClientSession(read, write))
            await session.initialize()
            self.session = session
            logging.info(f"✓ Server '{self.name}' initialized")
        except Exception as e:
            logging.error(f"Error initializing server {self.name}: {e}")
            await self.cleanup()
            raise

    async def list_tools(self) -> List[ToolDefinition]:
        """List available tools from the server.

        Returns:
            A list of available tool definitions.

        Raises:
            RuntimeError: If the server is not initialized.
        """
        if not self.session:
            raise RuntimeError(f"Server '{self.name}' is not initialized")

        try:
            tool_data = []
            tools = await self.session.list_tools()
            for tool in tools.tools:
                tool_data.append({
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                })
                logger.info(f"Tool: {tool.name},description:{tool.description}, input_schema:{tool.inputSchema}")
            return tool_data
        except Exception as e:
            logging.error(f"Error Listening server Tools {self.name}: {e}")
            raise

    async def execute_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        retries: int = 2,
        delay: float = 1.0,
    ) -> Any:
        """Execute a tool with retry mechanism.

        Args:
            tool_name: Name of the tool to execute.
            arguments: Tool arguments.
            retries: Number of retry attempts.
            delay: Delay between retries in seconds.

        Returns:
            Tool execution result.

        Raises:
            RuntimeError: If server is not initialized.
            Exception: If tool execution fails after all retries.
        """
        if not self.session:
            raise RuntimeError(f"Server {self.name} not initialized")

        attempt = 0
        while attempt < retries:
            try:
                logging.info(f"Executing {tool_name}...")
                result = await self.session.call_tool(name=tool_name, arguments=arguments, read_timeout_seconds=timedelta(seconds=60))
                return result
            except Exception as e:
                attempt += 1
                logging.warning(
                    f"Error executing tool: {e}. Attempt {attempt} of {retries}.")
                if attempt < retries:
                    logging.info(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                else:
                    logging.error("Max retries reached. Failing.")
                    raise

    async def cleanup(self) -> None:
        """Clean up server resources."""
        async with self._cleanup_lock:
            try:
                await self.exit_stack.aclose()
                self.session = None
                self.stdio_context = None
            except Exception as e:
                logging.error(f"Error during cleanup of server {self.name}: {e}")

# ===========================================================================
#                            Data Extraction
# ===========================================================================
class DataExtractor:
    """Handles extraction and storage of structured data from LLM responses."""
    
    def __init__(self, sqlite_server: Server, anthropic_client: Anthropic):
        self.sqlite_server = sqlite_server
        self.anthropic = anthropic_client
        
    async def setup_data_tables(self) -> None:
        """Setup tables for storing extracted data."""
        try:
            
            await self.sqlite_server.execute_tool("write_query", {
                "query": """
                CREATE TABLE IF NOT EXISTS pricing_plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_name TEXT NOT NULL,
                    plan_name TEXT NOT NULL,
                    input_tokens REAL,
                    output_tokens REAL,
                    currency TEXT DEFAULT 'USD',
                    billing_period TEXT,  -- 'monthly', 'yearly', 'one-time'
                    features TEXT,  -- JSON array
                    limitations TEXT,
                    source_query TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            })
            
            logging.info("✓ Data extraction tables initialized")
            
        except Exception as e:
            logging.error(f"Failed to setup data tables: {e}")

    async def _get_structured_extraction(self, prompt: str) -> str:
        """Use Claude to extract structured data."""
        try:
            response = self.anthropic.messages.create(
                max_tokens=1024,
                model='claude-sonnet-4-5-20250929',
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            text_content = ""
            for content in response.content:
                if content.type == 'text':
                    text_content += content.text
            
            return text_content.strip()
            
        except Exception as e:
            logging.error(f"Error in structured extraction: {e}")
            return '{"error": "extraction failed"}'
    
    async def extract_and_store_data(self, user_query: str, llm_response: str, 
                                   source_url: str = None) -> None:
        """Extract structured data from LLM response and store it."""
        try:            
            extraction_prompt = f"""
            Analyze this text and extract pricing information in JSON format:
            
            Text: {llm_response}
            
            Extract pricing plans with this structure:
            {{
                "company_name": "company name",
                "plans": [
                    {{
                        "plan_name": "plan name",
                        "input_tokens": number or null,
                        "output_tokens": number or null,
                        "currency": "USD",
                        "billing_period": "monthly/yearly/one-time",
                        "features": ["feature1", "feature2"],
                        "limitations": "any limitations mentioned",
                        "query": "the user's query"
                    }}
                ]
            }}
            
            Return only valid JSON, no other text. Do not return your response enclosed in ```json```
            """
            
            extraction_response = await self._get_structured_extraction(extraction_prompt)
            extraction_response = extraction_response.replace("```json\n", "").replace("```", "")
            pricing_data = json.loads(extraction_response)
            
            if len(pricing_data.get("plans", [])) == 0:
                logging.info(
                    f"No pricing plans extracted for {pricing_data.get('company_name', 'Unknown Company')}")
                return
            
            for plan in pricing_data.get("plans", []):
                result = await self.sqlite_server.execute_tool("write_query", {
                    "query": f"""
                        INSERT INTO pricing_plans (company_name, plan_name, input_tokens, output_tokens, currency, billing_period, features, limitations, source_query)
                        VALUES (
                            '{pricing_data.get("company_name", "Unknown Company")}',
                            '{plan.get("plan_name", "Unknown Plan")}',
                            '{plan.get("input_tokens", 0)}',
                            '{plan.get("output_tokens", 0)}',
                            '{plan.get("currency", "USD")}',
                            '{plan.get("billing_period", "unknown")}',
                            '{json.dumps(plan.get("features", []))}',
                            '{plan.get("limitations", "")}',
                            '{user_query.replace("'","''")}')
                        """
                })
            
            logger.info(f"Stored {len(pricing_data.get('plans', []))} pricing plans")
            
        except Exception as e:
            logging.error(f"Error extracting pricing data: {e}")


class ChatSession:
    """Orchestrates the interaction between user, LLM, and tools."""

    def __init__(self, servers: list[Server], api_key: str) -> None:
        self.servers: list[Server] = servers
        self.anthropic = Anthropic(api_key=api_key)
        self.available_tools: List[ToolDefinition] = []
        self.tool_to_server: Dict[str, str] = {}
        self.sqlite_server: Server | None = None
        self.data_extractor: DataExtractor | None = None

    async def cleanup_servers(self) -> None:
        """Clean up all servers properly."""
        for server in reversed(self.servers):
            try:
                await server.cleanup()
            except Exception as e:
                logging.warning(f"Warning during final cleanup: {e}")

    async def process_query(self, query: str) -> None:
        """Process a user query and extract/store relevant data."""

        # Step 1 : Create the initial prompt and send it to the LLM
        messages = [{'role': 'user', 'content': query}]
        logger.info(f"Calling anthropic: process_query first request")
        response = self.anthropic.messages.create(
                max_tokens=2024,
                model='claude-sonnet-4-5-20250929',
                system=SYSTEM_PROMPT,
                tools=self.available_tools,
                messages=messages
            )
        # Log actual usage
        logger.info(f"Input tokens: {response.usage.input_tokens:,}")
        logger.info(f"Output tokens: {response.usage.output_tokens:,}")
        logger.info(f"Total tokens: {response.usage.input_tokens + response.usage.output_tokens:,}")
        # Check if approaching limits
        if response.usage.input_tokens > 25000:
            logger.warning(f"High input token usage: {response.usage.input_tokens:,}")

        # Loop
        full_response = ""
        source_url = None
        used_web_search = False
        
        process_query = True
        while process_query:
            assistant_content = []
            tool_uses = []

            # Count how many tools Claude wants to use
            num_tool_calls = sum(1 for c in response.content if c.type == 'tool_use')
            if num_tool_calls > 0:
                logger.info(f"Claude requested {num_tool_calls} tool(s) in parallel")

            for content in response.content:
                if content.type == 'text':
                    # complete
                    full_response += content.text + "\n"
                    # Add the content to the assistant's message
                    assistant_content.append(content)
                    # Check if this is the only content - if so, model is done
                    if len(response.content) == 1:
                        process_query = False

                elif content.type == 'tool_use':
                    assistant_content.append(content)

                    # Tool Step 1: Tool Identification
                    tool_id = content.id
                    tool_name = content.name
                    tool_args = content.input
                    logging.info(f"Tool ID: {content.id}")
                    logging.info(f"Tool Name: {tool_name}")
                    logging.info(f"Tool Arguments: {tool_args}")
                    
                    # Tool Step 2: Find the server name who provides the tool
                    server_name = self.tool_to_server.get(tool_name)
                    if not server_name:
                        logging.error(f"Tool {tool_name} not found in tool_to_server mapping")
                        # We add a failed message to our tool call rather tha the results
                        tool_uses.append({
                            'type': 'tool_result',
                            'tool_use_id': tool_id,
                            'content': f"Error: Tool {tool_name} not found",
                            'is_error': True
                        })
                        continue
                    
                    # Tool Step 3: find the server instance with the server name
                    server = next((s for s in self.servers if s.name == server_name), None)
                    if not server:
                        logging.error(f"Server {server_name} not found")
                        # We add a failed message to our tool call rather tha the results
                        tool_uses.append({
                            'type': 'tool_result',
                            'tool_use_id': tool_id,
                            'content': f"Error: Server {server_name} not found",
                            'is_error': True
                        })
                        continue
        
                    # Tool Step 4: Call the Server Tool
                    try:
                        logging.info(f"Executing tool {tool_name} on server {server_name}")
                        tool_result = await server.execute_tool(tool_name, tool_args)
                        logging.info(f"Tool {tool_name} result: {tool_result.content[0].text[:50]}...")


                        #  # Log for debugging
                        result_unstructured = tool_result.content[0]

                        result = ""
                        if isinstance(result_unstructured, types.TextContent):
                            # logging.info(f"Tool result: {result_unstructured.text}")
                            result = result_unstructured.text 

                            if tool_name == "extract_scraped_info":
                                pass

                        tool_uses.append({
                            'type': 'tool_result',
                            'tool_use_id': tool_id,
                            'content': result,
                            'is_error': False
                        })
                    except Exception as e:
                        logging.error(f"Error executing tool {tool_name}: {e}")
                        # We add a failed message to our tool call rather tha the results
                        tool_uses.append({
                            'type': 'tool_result',
                            'tool_use_id': tool_id,
                            'content': f"Error executing tool: {e}",
                            'is_error': True
                        })


            ## Build messages correctly - ONE assistant message, ONE user message
            messages.append({'role': 'assistant', 'content': assistant_content})
            messages.append({'role': 'user', 'content': tool_uses})

            await asyncio.sleep(1) 

            # Phase 4: Make ONE API call with all tool results
            logger.info(f"Calling anthropic: process_query result")
            response = self.anthropic.messages.create(
                max_tokens=2024,
                model='claude-sonnet-4-5-20250929',
                system=SYSTEM_PROMPT,
                tools=self.available_tools,
                messages=messages
            )

            # Log actual usage
            logger.info(f"Input tokens: {response.usage.input_tokens:,}")
            logger.info(f"Output tokens: {response.usage.output_tokens:,}")
            logger.info(f"Total tokens: {response.usage.input_tokens + response.usage.output_tokens:,}")
            # Check if approaching limits
            if response.usage.input_tokens > 25000:
                logger.warning(f"High input token usage: {response.usage.input_tokens:,}")

            if len(response.content) == 1 and response.content[0].type == 'text':
                    source_url = self._extract_url_from_result(response.content[0].text)
                    full_response += response.content[0].text
                    process_query = False

        print(full_response.strip())
        if self.data_extractor and full_response.strip():
            await self.data_extractor.extract_and_store_data(query, full_response.strip(), source_url)

        
    def _extract_url_from_result(self, result_text: str) -> str | None:
        """Extract URL from tool result."""
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, result_text)
        return urls[0] if urls else None

    async def chat_loop(self) -> None:
        """Run an interactive chat loop."""
        print("\nMCP Chatbot with Data Extraction Started!")
        print("Type your queries, 'show data' to view stored data, or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
        
                if query.lower() == 'quit':
                    break
                elif query.lower() == 'show data':
                    await self.show_stored_data()
                    continue
                    
                await self.process_query(query)
                print("\n")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"\nError: {str(e)}")

    async def show_stored_data(self) -> None:
        """Show recently stored data."""
        if not self.sqlite_server:
            logger.info("No database available")
            return
            
        try:
            pricing = await self.sqlite_server.execute_tool("read_query", {
                "query": "SELECT company_name, plan_name, input_tokens, output_tokens, currency FROM pricing_plans ORDER BY created_at DESC LIMIT 5"
            })

            print("\nRecently Stored Data:")
            print("=" * 50)

            print("\nPricing Plans:")
            # The result.content is a list with one item, a dict, where the 'text' key holds the rows
            for plan in pricing.content[0]["text"]:
                print(f"  • {plan['company_name']}: {plan['plan_name']} - Input Token ${plan['input_tokens']}, Output Tokens ${plan['output_tokens']}")

            print("=" * 50)
        except Exception as e:
            print(f"Error showing data: {e}")

    async def start(self) -> None:
        """Main chat session handler."""
        try:
            for server in self.servers:
                try:
                    await server.initialize()
                    if "sqlite" in server.name.lower():
                        self.sqlite_server = server
                except Exception as e:
                    logging.error(f"Failed to initialize server: {e}")
                    await self.cleanup_servers()
                    return

            for server in self.servers:
                tools = await server.list_tools()
                self.available_tools.extend(tools)
                for tool in tools:
                    self.tool_to_server[tool["name"]] = server.name

            print(f"\nConnected to {len(self.servers)} server(s)")
            print(f"Available tools: {[tool['name'] for tool in self.available_tools]}")
            
            if self.sqlite_server:
                self.data_extractor = DataExtractor(self.sqlite_server, self.anthropic)
                await self.data_extractor.setup_data_tables()
                print("Data extraction enabled")

            await self.chat_loop()

        finally:
            await self.cleanup_servers()


async def main() -> None:
    """Initialize and run the chat session."""
    config = Configuration()
    
    script_dir = Path(__file__).parent
    config_file = script_dir / "server_config.json"
    
    server_config = config.load_config(config_file)
    
    servers = [Server(name, srv_config) for name, srv_config in server_config["mcpServers"].items()]
    chat_session = ChatSession(servers, config.anthropic_api_key)
    await chat_session.start()


if __name__ == "__main__":
    asyncio.run(main())
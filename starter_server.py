
import os
import json
import logging
import re
from typing import List, Dict, Optional, TypedDict
from firecrawl import FirecrawlApp
from urllib.parse import urlparse
from datetime import datetime, timedelta
from mcp.server.fastmcp import FastMCP

from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

SCRAPE_DIR = "scraped_content"

mcp = FastMCP("llm_inference")

# ===========================================================================
#                            Type Definitions
# ===========================================================================
# Rubic requires - name, url, domain, scrape_time, content_files, title, description


class MetadataEntry(TypedDict):
    """Complete metadata entry for a successfully scraped website."""
    name: str
    url: str
    domain: str
    scrape_time: str
    scraped_at: str
    content_files: Dict[str, str]
    content: Dict[str, str]
    formats: List[str]
    title: str
    description: str
    success: bool


def create_empty_metadata_entry(name: str, url: str) -> MetadataEntry:
    """
    Create an empty MetadataEntry with minimal required fields.

    Args:
        name: The provider/website name
        url: The website URL

    Returns:
        A MetadataEntry with empty/default values for content fields
    """
    entry: MetadataEntry = {
        "name": name,
        "url": url,
        "domain": urlparse(url).netloc,
        "scrape_time": datetime.now().isoformat(),
        "scraped_at": datetime.now().isoformat(),
        "formats": [],
        "title": "",
        "description": "",
        "content_files": {},
        "content": {},
        "success": False
    }
    return entry

# ===========================================================================
#                            Metadata
# ===========================================================================


def metadata_save(path: str, metadata: Dict):
    metadata_file = os.path.join(path, "scraped_metadata.json")
    logger.info(f"Saving metadata to file: {metadata_file}")
    try:
        with open(metadata_file, "w", encoding="utf-8") as file:
            json.dump(metadata, file, indent=2)
    except IOError as e:
        logger.error(f"IO error saving metadata to {metadata_file}: {e}")
        raise
    except Exception as e:
        logger.error(
            f"Unexpected error saving metadata to {metadata_file}: {e}")
        raise


def metadata_load(path: str) -> Dict:
    metadata_file = os.path.join(path, "scraped_metadata.json")
    if not os.path.exists(metadata_file):
        return {}

    logger.info(f"Loading metadata from file: {metadata_file}")
    try:
        with open(metadata_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logger.warning(f"Metadata file not found: {metadata_file}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in metadata file {metadata_file}: {e}")
        return {}
    except IOError as e:
        logger.error(f"IO error loading metadata from {metadata_file}: {e}")
        return {}
    except Exception as e:
        logger.error(
            f"Unexpected error loading metadata from {metadata_file}: {e}")
        return {}

# ===========================================================================
#                           Scrape Result
# ===========================================================================


def save_scrape_result(path: str, content):
    logger.info(f"Saving scrape result to file: {path}")
    try:
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)
    except IOError as e:
        logger.error(f"IO error saving scrape result to {path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error saving scrape result to {path}: {e}")
        raise


def load_scrape_result(path: str):
    logger.info(f"Loading scrape result from file: {path}")
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"Scrape result file not found: {path}")
        raise
    except IOError as e:
        logger.error(f"IO error loading scrape result from {path}: {e}")
        raise
    except Exception as e:
        logger.error(
            f"Unexpected error loading scrape result from {path}: {e}")
        raise


def should_skip_scrape(name: str, metadata: Dict[str, MetadataEntry]) -> bool:
    """Check if a provider was successfully scraped within the last 3 hours."""

    if name not in metadata:
        return False

    try:
        entry: MetadataEntry = metadata[name]
        scrape_time: datetime = datetime.fromisoformat(entry['scrape_time'])
        cutoff_time: datetime = datetime.now() - timedelta(hours=3)
        return scrape_time > cutoff_time
    except (ValueError, KeyError):
        return False


def normalize_filename(name: str) -> str:
    """
    Normalize a name to create a safe filename.

    Args:
        name: The provider/website name

    Returns:
        A normalized filename-safe string
    """
    # Convert to lowercase
    normalized = name.lower()
    # Replace spaces and special chars with underscores
    normalized = re.sub(r'[^\w\-]', '_', normalized)
    # Replace multiple underscores with single
    normalized = re.sub(r'_+', '_', normalized)
    # Remove leading/trailing underscores
    normalized = normalized.strip('_')
    return normalized
# ===========================================================================
#                             MCP Tools
# ===========================================================================


@mcp.tool()
def scrape_websites(
    websites: Dict[str, str],
    formats: List[str] = ['markdown', 'html'],
    api_key: Optional[str] = None
) -> List[str]:
    """
    Scrape multiple websites using Firecrawl and store their content.

    Args:
        websites: Dictionary of provider_name -> URL mappings
        formats: List of formats to scrape ['markdown', 'html'] (default: both)
        api_key: Firecrawl API key (if None, expects environment variable)

    Returns:
        List of provider names for successfully scraped websites
    """

    if api_key is None:
        api_key = os.getenv('FIRECRAWL_API_KEY')
        if not api_key:
            raise ValueError(
                "API key must be provided or set as FIRECRAWL_API_KEY environment variable")

    app = FirecrawlApp(api_key=api_key)

    path = os.path.join(SCRAPE_DIR)
    os.makedirs(path, exist_ok=True)

    metadata: Dict[str, MetadataEntry] = metadata_load(path)

    successful_scrapes = []
    for name, url in websites.items():

        # Skip successful entries less than 3 hours old
        if should_skip_scrape(name, metadata):
            logger.info(f"Skipping {name}: recently scraped successfully")
            successful_scrapes.append(name)
            continue

        # We need to scrape
        try:
            logger.info(f"Scraping {name}: {url}")

            result: Dict = app.scrape(url, formats=formats).model_dump()
            # 200 -> Request was success
            result_status_code: int = result["metadata"].get(
                "status_code", "404")

            if result_status_code == 200:

                metadata_entry = {
                    "name": name,
                    "url": url,
                    "domain": urlparse(url).netloc,
                    "scrape_time": datetime.now().isoformat(),
                    "scraped_at": datetime.now().isoformat(),
                    "formats": formats,
                    "title": result["metadata"].get("og_title", ""),
                    "description": result["metadata"].get("og_description", ""),
                    "content_files": {},
                    "content": {},
                    "success": True
                }

                # Loop over formats
                for format in formats:
                    filename = f"{normalize_filename(name)}_{format}.txt"
                    save_scrape_result(os.path.join(
                        path, filename), result[format])
                    metadata_entry["content_files"][format] = filename

                # Always update on success
                metadata[name] = metadata_entry
                successful_scrapes.append(name)

            else:
                logger.error(
                    f"Scraping {name}: {url} has failed with {result_status_code}")
                # Only update if no existing entry or existing entry was also a failure
                if name not in metadata or not metadata[name].get("success", False):
                    metadata_entry = create_empty_metadata_entry(name, url)
                    metadata_entry["success"] = False
                    metadata[name] = metadata_entry

        # When we had an error during scraping we will mark this bad
        except Exception as err:
            logger.error(f"Scraping {name}: {url} has failed Exception {err}")

            # Only update if no existing entry or existing entry was also a failure
            if name not in metadata or not metadata[name].get("success", False):
                metadata_entry: MetadataEntry = create_empty_metadata_entry(
                    name, url)
                metadata_entry["success"] = False
                metadata[name] = metadata_entry
            continue

    # Save the Metadata
    metadata_save(path, metadata)

    return successful_scrapes


@mcp.tool()
def extract_scraped_info(identifier: str) -> str:
    """
    Extract information about a scraped website.

    Args:
        identifier: The provider name, full URL, or domain to look for

    Returns:
        Formatted JSON string with the scraped information
    """

    logger.info(f"Extracting information for identifier: {identifier}")
    logger.info(f"Files in {SCRAPE_DIR}: {os.listdir(SCRAPE_DIR)}")

    metadata_dict: Dict[str, MetadataEntry] = metadata_load(
        os.path.join(SCRAPE_DIR))

    # loop over all entries
    for name, metadata in metadata_dict.items():
        try:
            # Check for provider Name, Url and domain
            if (
                identifier == name
                or identifier == metadata.get('url', '')
                or identifier == metadata.get('domain', '')
            ):

                # skip bad results
                if not metadata.get('success', False):
                    logger.warning(
                        f"Found {name} but scrape was not successful")
                    continue

                result: MetadataEntry = metadata.copy()  # shallow copy
                content_files = metadata.get('content_files') or {}

                if content_files:
                    for format_type, filename in content_files.items():
                        content_path = os.path.join(SCRAPE_DIR, filename)
                        result['content'][format_type] = load_scrape_result(
                            content_path)

                # Return formatted JSON
                return json.dumps(result, indent=2)
        except Exception as err:
            # Continue if we have an issue
            logger.error(f"Processing: {name} has failed Exception {err}")
            continue

    # No Matches Return Error
    return f"There's no saved information related to identifier '{identifier}'."


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

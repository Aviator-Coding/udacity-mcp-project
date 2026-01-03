## Prompt 1 - Scrape website

### Query
```
Query: scrape these sites: {'cloudrift': 'https://www.cloudrift.ai/inference', 'deepinfra': 'https://deepinfra.com/
```

### Result
```
pricing', 'fireworks': 'https://fireworks.ai/pricing#serverless-pricing', 'groq': 'https://groq.com/pricing'}
2026-01-03 12:44:47,219 - INFO - Calling anthropic: process_query first request
2026-01-03 12:44:50,680 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
2026-01-03 12:44:50,693 - INFO - Input tokens: 5,241
2026-01-03 12:44:50,693 - INFO - Output tokens: 142
2026-01-03 12:44:50,693 - INFO - Total tokens: 5,383
2026-01-03 12:44:50,694 - INFO - Claude requested 1 tool(s) in parallel
2026-01-03 12:44:50,694 - INFO - Tool ID: toolu_01UVi2Xp6Yrchxmo1yRHYHL3
2026-01-03 12:44:50,694 - INFO - Tool Name: scrape_websites
2026-01-03 12:44:50,694 - INFO - Tool Arguments: {'websites': {'cloudrift': 'https://www.cloudrift.ai/inference', 'deepinfra': 'https://deepinfra.com/pricing', 'fireworks': 'https://fireworks.ai/pricing#serverless-pricing', 'groq': 'https://groq.com/pricing'}}
2026-01-03 12:44:50,694 - INFO - Executing tool scrape_websites on server llm_inference
2026-01-03 12:44:50,694 - INFO - Executing scrape_websites...
2026-01-03 12:44:50,695 - mcp.server.lowlevel.server - INFO - Processing request of type CallToolRequest
2026-01-03 12:44:50,696 - __main__ - INFO - Scraping cloudrift: https://www.cloudrift.ai/inference
2026-01-03 12:44:51,357 - __main__ - INFO - Saving scrape result to file: scraped_content/cloudrift_markdown.txt
2026-01-03 12:44:51,357 - __main__ - INFO - Saving scrape result to file: scraped_content/cloudrift_html.txt
2026-01-03 12:44:51,357 - __main__ - INFO - Scraping deepinfra: https://deepinfra.com/pricing
2026-01-03 12:44:52,030 - __main__ - INFO - Saving scrape result to file: scraped_content/deepinfra_markdown.txt
2026-01-03 12:44:52,031 - __main__ - INFO - Saving scrape result to file: scraped_content/deepinfra_html.txt
2026-01-03 12:44:52,031 - __main__ - INFO - Scraping fireworks: https://fireworks.ai/pricing#serverless-pricing
2026-01-03 12:44:52,716 - __main__ - INFO - Saving scrape result to file: scraped_content/fireworks_markdown.txt
2026-01-03 12:44:52,717 - __main__ - INFO - Saving scrape result to file: scraped_content/fireworks_html.txt
2026-01-03 12:44:52,719 - __main__ - INFO - Scraping groq: https://groq.com/pricing
2026-01-03 12:44:53,332 - __main__ - INFO - Saving scrape result to file: scraped_content/groq_markdown.txt
2026-01-03 12:44:53,333 - __main__ - INFO - Saving scrape result to file: scraped_content/groq_html.txt
2026-01-03 12:44:53,333 - __main__ - INFO - Saving metadata to file: scraped_content/scraped_metadata.json
2026-01-03 12:44:53,338 - INFO - Tool scrape_websites result: cloudrift...
2026-01-03 12:44:54,339 - INFO - Calling anthropic: process_query result
2026-01-03 12:44:59,212 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
2026-01-03 12:44:59,214 - INFO - Input tokens: 5,387
2026-01-03 12:44:59,214 - INFO - Output tokens: 230
2026-01-03 12:44:59,214 - INFO - Total tokens: 5,617
2026-01-03 12:44:59,214 - INFO - Claude requested 3 tool(s) in parallel
2026-01-03 12:44:59,214 - INFO - Tool ID: toolu_01NwrJbd7nhQiW2ZmZvbJkEU
2026-01-03 12:44:59,214 - INFO - Tool Name: scrape_websites
2026-01-03 12:44:59,214 - INFO - Tool Arguments: {'websites': {'deepinfra': 'https://deepinfra.com/pricing'}}
2026-01-03 12:44:59,215 - INFO - Executing tool scrape_websites on server llm_inference
2026-01-03 12:44:59,215 - INFO - Executing scrape_websites...
2026-01-03 12:44:59,216 - mcp.server.lowlevel.server - INFO - Processing request of type CallToolRequest
2026-01-03 12:44:59,217 - __main__ - INFO - Loading metadata from file: scraped_content/scraped_metadata.json
2026-01-03 12:44:59,217 - __main__ - INFO - Skipping deepinfra: recently scraped successfully
2026-01-03 12:44:59,217 - __main__ - INFO - Saving metadata to file: scraped_content/scraped_metadata.json
2026-01-03 12:44:59,221 - INFO - Tool scrape_websites result: deepinfra...
2026-01-03 12:44:59,221 - INFO - Tool ID: toolu_01GQkJ4jkbf1TvcxJiCnTLiA
2026-01-03 12:44:59,221 - INFO - Tool Name: scrape_websites
2026-01-03 12:44:59,221 - INFO - Tool Arguments: {'websites': {'fireworks': 'https://fireworks.ai/pricing#serverless-pricing'}}
2026-01-03 12:44:59,221 - INFO - Executing tool scrape_websites on server llm_inference
2026-01-03 12:44:59,221 - INFO - Executing scrape_websites...
2026-01-03 12:44:59,222 - mcp.server.lowlevel.server - INFO - Processing request of type CallToolRequest
2026-01-03 12:44:59,222 - __main__ - INFO - Loading metadata from file: scraped_content/scraped_metadata.json
2026-01-03 12:44:59,222 - __main__ - INFO - Skipping fireworks: recently scraped successfully
2026-01-03 12:44:59,222 - __main__ - INFO - Saving metadata to file: scraped_content/scraped_metadata.json
2026-01-03 12:44:59,225 - INFO - Tool scrape_websites result: fireworks...
2026-01-03 12:44:59,225 - INFO - Tool ID: toolu_01SRZB3v5kUma3MZvbQ9ajoh
2026-01-03 12:44:59,225 - INFO - Tool Name: scrape_websites
2026-01-03 12:44:59,225 - INFO - Tool Arguments: {'websites': {'groq': 'https://groq.com/pricing'}}
2026-01-03 12:44:59,225 - INFO - Executing tool scrape_websites on server llm_inference
2026-01-03 12:44:59,225 - INFO - Executing scrape_websites...
2026-01-03 12:44:59,226 - mcp.server.lowlevel.server - INFO - Processing request of type CallToolRequest
2026-01-03 12:44:59,226 - __main__ - INFO - Loading metadata from file: scraped_content/scraped_metadata.json
2026-01-03 12:44:59,226 - __main__ - INFO - Skipping groq: recently scraped successfully
2026-01-03 12:44:59,226 - __main__ - INFO - Saving metadata to file: scraped_content/scraped_metadata.json
2026-01-03 12:44:59,229 - INFO - Tool scrape_websites result: groq...
2026-01-03 12:45:00,231 - INFO - Calling anthropic: process_query result
2026-01-03 12:45:04,333 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
2026-01-03 12:45:04,335 - INFO - Input tokens: 5,715
2026-01-03 12:45:04,335 - INFO - Output tokens: 131
2026-01-03 12:45:04,335 - INFO - Total tokens: 5,846
I'll scrape all four websites for you in one call.
I've successfully scraped the **cloudrift** website. However, it appears there were issues scraping the other three sites (deepinfra, fireworks, and groq). 

Let me try scraping them individually to see if I can get better results:
Perfect! I've successfully scraped all four websites:

✅ **cloudrift** - https://www.cloudrift.ai/inference  
✅ **deepinfra** - https://deepinfra.com/pricing  
✅ **fireworks** - https://fireworks.ai/pricing#serverless-pricing  
✅ **groq** - https://groq.com/pricing

All the pricing data from these providers has been scraped and stored. You can now query information about their pricing, compare costs, or ask specific questions about any of these providers!
```

## Prompt 2 - How much does cloudrift ai (https://www.cloudrift.ai/inference) charge for deepseek v3?

### Query
```
Query: How much does cloudrift ai (https://www.cloudrift.ai/inference) charge for deepseek v3?
```

### Result

```
2026-01-03 12:47:16,603 - INFO - Calling anthropic: process_query first request
2026-01-03 12:47:20,012 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
2026-01-03 12:47:20,014 - INFO - Input tokens: 5,190
2026-01-03 12:47:20,014 - INFO - Output tokens: 119
2026-01-03 12:47:20,014 - INFO - Total tokens: 5,309
2026-01-03 12:47:20,014 - INFO - Claude requested 1 tool(s) in parallel
2026-01-03 12:47:20,014 - INFO - Tool ID: toolu_01DozcoJRuTAhTuigGAQ7oQX
2026-01-03 12:47:20,015 - INFO - Tool Name: read_query
2026-01-03 12:47:20,015 - INFO - Tool Arguments: {'query': "SELECT * FROM pricing_plans WHERE LOWER(company_name) LIKE '%cloudrift%' AND LOWER(plan_name) LIKE '%deepseek%'"}
2026-01-03 12:47:20,015 - INFO - Executing tool read_query on server sqlite
2026-01-03 12:47:20,015 - INFO - Executing read_query...
2026-01-03 12:47:20,020 - INFO - Tool read_query result: []...
2026-01-03 12:47:21,022 - INFO - Calling anthropic: process_query result
2026-01-03 12:47:24,213 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
2026-01-03 12:47:24,215 - INFO - Input tokens: 5,322
2026-01-03 12:47:24,215 - INFO - Output tokens: 80
2026-01-03 12:47:24,215 - INFO - Total tokens: 5,402
2026-01-03 12:47:24,215 - INFO - Claude requested 1 tool(s) in parallel
2026-01-03 12:47:24,215 - INFO - Tool ID: toolu_01CmeGYRLMdYsitaaoGAgvUJ
2026-01-03 12:47:24,215 - INFO - Tool Name: extract_scraped_info
2026-01-03 12:47:24,215 - INFO - Tool Arguments: {'identifier': 'cloudrift'}
2026-01-03 12:47:24,215 - INFO - Executing tool extract_scraped_info on server llm_inference
2026-01-03 12:47:24,215 - INFO - Executing extract_scraped_info...
2026-01-03 12:47:24,217 - mcp.server.lowlevel.server - INFO - Processing request of type CallToolRequest
2026-01-03 12:47:24,218 - __main__ - INFO - Extracting information for identifier: cloudrift
2026-01-03 12:47:24,218 - __main__ - INFO - Files in scraped_content: ['cloudrift_markdown.txt', 'deepinfra_markdown.txt', 'fireworks_markdown.txt', 'groq_html.txt', 'deepinfra_html.txt', 'groq_markdown.txt', 'cloudrift_html.txt', 'fireworks_html.txt', 'scraped_metadata.json']
2026-01-03 12:47:24,218 - __main__ - INFO - Loading metadata from file: scraped_content/scraped_metadata.json
2026-01-03 12:47:24,218 - __main__ - INFO - Loading scrape result from file: scraped_content/cloudrift_markdown.txt
2026-01-03 12:47:24,218 - __main__ - INFO - Loading scrape result from file: scraped_content/cloudrift_html.txt
2026-01-03 12:47:24,222 - INFO - Tool extract_scraped_info result: {
  "name": "cloudrift",
  "url": "https://www.cloudrift.ai/inference",
  "domain": "www.cloudrift.ai",
  "scrape_time": "2026-01-03T12:44:51.356834",
  "scraped_at": "2026-01-03T12:44:51.356852",
  "...
2026-01-03 12:47:24,222 - INFO - Removed HTML content from extract_scraped_info result
2026-01-03 12:47:25,223 - INFO - Calling anthropic: process_query result
2026-01-03 12:47:31,174 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
2026-01-03 12:47:31,175 - INFO - Input tokens: 7,181
2026-01-03 12:47:31,175 - INFO - Output tokens: 202
2026-01-03 12:47:31,175 - INFO - Total tokens: 7,383
I'll help you find the pricing information for DeepSeek V3 on Cloudrift AI. Let me check the database first.
The database doesn't have this information yet. Let me extract the pricing data from the scraped website content.
Based on the pricing information from Cloudrift AI, here's what they charge for **DeepSeek V3**:

## DeepSeek-V3 Pricing on Cloudrift AI

- **Input tokens**: $0.15 per million tokens
- **Output tokens**: $0.40 per million tokens
- **Context window**: 163.84K tokens

This is a pay-as-you-go model with no queues or GPU setup required. Cloudrift AI positions this model as rivaling closed models on math and code tasks, with open weights and low pricing suitable for enterprise deployment.

**Note**: They also offer **DeepSeek-V3.1** (the newer version) at:
- Input: $0.15 per million tokens
- Output: $0.50 per million tokens (slightly higher than V3)
- Same 163.84K context window
2026-01-03 12:47:36,192 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
2026-01-03 12:47:36,193 - INFO - Executing write_query...
2026-01-03 12:47:36,199 - INFO - Executing write_query...
2026-01-03 12:47:36,203 - INFO - Stored 2 pricing plans
```

## Prompt 3 - How much does deepinfra (https://deepinfra.com/pricing) charge for deepseek v3

### Query
```
Query: "How much does deepinfra (https://deepinfra.com/pricing) charge for deepseek v3"
```

### Result
```
2026-01-03 12:48:45,496 - INFO - Calling anthropic: process_query first request
2026-01-03 12:48:49,203 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
2026-01-03 12:48:49,204 - INFO - Input tokens: 5,190
2026-01-03 12:48:49,204 - INFO - Output tokens: 126
2026-01-03 12:48:49,204 - INFO - Total tokens: 5,316
2026-01-03 12:48:49,204 - INFO - Claude requested 1 tool(s) in parallel
2026-01-03 12:48:49,205 - INFO - Tool ID: toolu_01DQmZB9KoDky1qjiDhombFz
2026-01-03 12:48:49,205 - INFO - Tool Name: read_query
2026-01-03 12:48:49,205 - INFO - Tool Arguments: {'query': "SELECT * FROM pricing_plans WHERE LOWER(company_name) LIKE '%deepinfra%' AND LOWER(plan_name) LIKE '%deepseek%'"}
2026-01-03 12:48:49,205 - INFO - Executing tool read_query on server sqlite
2026-01-03 12:48:49,205 - INFO - Executing read_query...
2026-01-03 12:48:49,211 - INFO - Tool read_query result: []...
2026-01-03 12:48:50,212 - INFO - Calling anthropic: process_query result
2026-01-03 12:48:53,431 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
2026-01-03 12:48:53,432 - INFO - Input tokens: 5,329
2026-01-03 12:48:53,432 - INFO - Output tokens: 85
2026-01-03 12:48:53,433 - INFO - Total tokens: 5,414
2026-01-03 12:48:53,433 - INFO - Claude requested 1 tool(s) in parallel
2026-01-03 12:48:53,433 - INFO - Tool ID: toolu_013yMEhGnXhQqf4YPKVFBjaM
2026-01-03 12:48:53,433 - INFO - Tool Name: extract_scraped_info
2026-01-03 12:48:53,433 - INFO - Tool Arguments: {'identifier': 'deepinfra.com'}
2026-01-03 12:48:53,433 - INFO - Executing tool extract_scraped_info on server llm_inference
2026-01-03 12:48:53,433 - INFO - Executing extract_scraped_info...
2026-01-03 12:48:53,435 - mcp.server.lowlevel.server - INFO - Processing request of type CallToolRequest
2026-01-03 12:48:53,435 - __main__ - INFO - Extracting information for identifier: deepinfra.com
2026-01-03 12:48:53,435 - __main__ - INFO - Files in scraped_content: ['cloudrift_markdown.txt', 'deepinfra_markdown.txt', 'fireworks_markdown.txt', 'groq_html.txt', 'deepinfra_html.txt', 'groq_markdown.txt', 'cloudrift_html.txt', 'fireworks_html.txt', 'scraped_metadata.json']
2026-01-03 12:48:53,435 - __main__ - INFO - Loading metadata from file: scraped_content/scraped_metadata.json
2026-01-03 12:48:53,435 - __main__ - INFO - Loading scrape result from file: scraped_content/deepinfra_markdown.txt
2026-01-03 12:48:53,436 - __main__ - INFO - Loading scrape result from file: scraped_content/deepinfra_html.txt
2026-01-03 12:48:53,444 - INFO - Tool extract_scraped_info result: {
  "name": "deepinfra",
  "url": "https://deepinfra.com/pricing",
  "domain": "deepinfra.com",
  "scrape_time": "2026-01-03T12:44:52.030455",
  "scraped_at": "2026-01-03T12:44:52.030480",
  "formats"...
2026-01-03 12:48:53,445 - INFO - Removed HTML content from extract_scraped_info result
2026-01-03 12:48:54,446 - INFO - Calling anthropic: process_query result
2026-01-03 12:49:02,571 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
2026-01-03 12:49:02,573 - INFO - Input tokens: 22,663
2026-01-03 12:49:02,573 - INFO - Output tokens: 295
2026-01-03 12:49:02,573 - INFO - Total tokens: 22,958
I'll help you find the pricing for DeepSeek V3 on DeepInfra. Let me first check if we have this information in our database.
The database doesn't have this information yet. Let me extract the pricing details from the DeepInfra website.
Perfect! I found the pricing information for DeepSeek V3 on DeepInfra. Here's what they charge:

## **DeepSeek-V3 Pricing on DeepInfra:**

- **Context Window:** 160k tokens
- **Input tokens:** $0.32 per 1M tokens
- **Output tokens:** $0.89 per 1M tokens

### Other DeepSeek V3 Variants Available:

DeepInfra also offers several other versions of DeepSeek V3 with different pricing:

1. **DeepSeek-V3.1** - $0.21/$0.79 per 1M input/output tokens (with $0.168 cached input)
2. **DeepSeek-V3.1-Terminus** - $0.21/$0.79 per 1M input/output tokens (with $0.168 cached input)
3. **DeepSeek-V3-0324** - $0.20/$0.88 per 1M input/output tokens (with $0.106 cached input)

The newer V3.1 models offer caching capabilities which can reduce costs for repeated inputs, and they're actually more affordable than the original V3 model.
2026-01-03 12:49:08,966 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
2026-01-03 12:49:08,967 - INFO - Executing write_query...
2026-01-03 12:49:08,973 - INFO - Executing write_query...
2026-01-03 12:49:08,977 - INFO - Executing write_query...
2026-01-03 12:49:08,980 - INFO - Executing write_query...
2026-01-03 12:49:08,982 - INFO - Stored 4 pricing plans
```

## Prompt 4 - How much does deepinfra (https://deepinfra.com/pricing) charge for deepseek v3

### Query
```
Query: "How much does deepinfra (https://deepinfra.com/pricing) charge for deepseek v3"
```

### Result
```
Query: "Compare cloudrift ai and deepinfra's costs for deepseek v3"
2026-01-03 12:50:12,788 - INFO - Calling anthropic: process_query first request
2026-01-03 12:50:16,956 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
2026-01-03 12:50:16,957 - INFO - Input tokens: 5,182
2026-01-03 12:50:16,957 - INFO - Output tokens: 197
2026-01-03 12:50:16,957 - INFO - Total tokens: 5,379
2026-01-03 12:50:16,957 - INFO - Claude requested 2 tool(s) in parallel
2026-01-03 12:50:16,957 - INFO - Tool ID: toolu_016xKtEyXi6jj8u8urxdfS2a
2026-01-03 12:50:16,957 - INFO - Tool Name: read_query
2026-01-03 12:50:16,957 - INFO - Tool Arguments: {'query': "SELECT * FROM pricing_plans WHERE LOWER(company_name) LIKE '%cloudrift%' AND LOWER(plan_name) LIKE '%deepseek%'"}
2026-01-03 12:50:16,957 - INFO - Executing tool read_query on server sqlite
2026-01-03 12:50:16,957 - INFO - Executing read_query...
2026-01-03 12:50:16,960 - INFO - Tool read_query result: [{'id': 1, 'company_name': 'Cloudrift AI', 'plan_name': 'DeepSeek-V3', 'input_tokens': 0.15, 'output_tokens': 0.4, 'currency': 'USD', 'billing_period': 'pay-as-you-go', 'features': '["163.84K context ...
2026-01-03 12:50:16,960 - INFO - Tool ID: toolu_01Cfpa2KAHvSZPyE6vAKNUQr
2026-01-03 12:50:16,960 - INFO - Tool Name: read_query
2026-01-03 12:50:16,960 - INFO - Tool Arguments: {'query': "SELECT * FROM pricing_plans WHERE LOWER(company_name) LIKE '%deepinfra%' AND LOWER(plan_name) LIKE '%deepseek%'"}
2026-01-03 12:50:16,961 - INFO - Executing tool read_query on server sqlite
2026-01-03 12:50:16,961 - INFO - Executing read_query...
2026-01-03 12:50:16,963 - INFO - Tool read_query result: [{'id': 3, 'company_name': 'DeepInfra', 'plan_name': 'DeepSeek-V3', 'input_tokens': 0.32, 'output_tokens': 0.89, 'currency': 'USD', 'billing_period': 'per_million_tokens', 'features': '["160k tokens c...
2026-01-03 12:50:17,965 - INFO - Calling anthropic: process_query result
2026-01-03 12:50:30,110 - INFO - HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
2026-01-03 12:50:30,112 - INFO - Input tokens: 6,491
2026-01-03 12:50:30,112 - INFO - Output tokens: 716
2026-01-03 12:50:30,112 - INFO - Total tokens: 7,207
I'll help you compare the costs for DeepSeek v3 between cloudrift ai and deepinfra. Let me check the database first for both providers.
Perfect! I found pricing data for both providers in the database. Here's a detailed comparison of **Cloudrift AI** vs **DeepInfra** for DeepSeek v3:

## 💰 Cost Comparison for DeepSeek V3

### **Cloudrift AI**
| Model | Input (per 1M tokens) | Output (per 1M tokens) | Context Window |
|-------|----------------------|------------------------|----------------|
| **DeepSeek-V3** | **$0.15** | **$0.40** | 163.84K tokens |
| **DeepSeek-V3.1** | **$0.15** | **$0.50** | 163.84K tokens |

### **DeepInfra**
| Model | Input (per 1M tokens) | Output (per 1M tokens) | Context Window | Special Features |
|-------|----------------------|------------------------|----------------|------------------|
| **DeepSeek-V3** | **$0.32** | **$0.89** | 160K tokens | - |
| **DeepSeek-V3.1** | **$0.21** | **$0.79** | - | Caching: $0.168 per 1M cached tokens |
| **DeepSeek-V3.1-Terminus** | **$0.21** | **$0.79** | - | Caching: $0.168 per 1M cached tokens |
| **DeepSeek-V3-0324** | **$0.20** | **$0.88** | - | Caching: $0.106 per 1M cached tokens |

## 📊 Key Findings

### **Price Winner: Cloudrift AI** 🏆
- **Input tokens**: Cloudrift is **50% cheaper** ($0.15 vs $0.32 for base v3)
- **Output tokens**: Cloudrift is **55% cheaper** ($0.40 vs $0.89 for base v3)
- **Overall**: Cloudrift offers significantly lower costs across all versions

### **Feature Differences**
- **Cloudrift AI**: 
  - Slightly larger context window (163.84K vs 160K)
  - No queues, no GPU setup required
  - Open weights for enterprise deployment
  
- **DeepInfra**: 
  - Offers caching capabilities on newer models (can reduce repeat input costs)
  - More model variants available
  - Caching feature can lower costs for repeated queries

### **Cost Example** (1M input + 1M output tokens):
- **Cloudrift DeepSeek-V3**: $0.15 + $0.40 = **$0.55**
- **DeepInfra DeepSeek-V3**: $0.32 + $0.89 = **$1.21**

**Cloudrift is ~54% cheaper** for the base DeepSeek-V3 model on a pay-as-you-go basis!
```

## Prompt 5 - show data

### Query
```
Query: "show datashow data"
```

### Result
```
2026-01-03 12:51:13,593 - INFO - Executing read_query...

Recently Stored Data:
==================================================

Pricing Plans:
2026-01-03 12:51:13,598 - INFO - Raw result from database: [{'company_name': 'DeepInfra', 'plan_name': 'DeepSeek-V3', 'input_tokens': 0.32, 'output_tokens': 0.89, 'currency': 'USD'}, {'company_name': 'DeepInfra', 'plan_name': 'DeepSeek-V3.1', 'input_tokens': 
  • DeepInfra: DeepSeek-V3 - Input: $0.32/M, Output: $0.89/M
  • DeepInfra: DeepSeek-V3.1 - Input: $0.21/M, Output: $0.79/M
  • DeepInfra: DeepSeek-V3.1-Terminus - Input: $0.21/M, Output: $0.79/M
  • DeepInfra: DeepSeek-V3-0324 - Input: $0.2/M, Output: $0.88/M
  • Cloudrift AI: DeepSeek-V3 - Input: $0.15/M, Output: $0.4/M
==================================================
```
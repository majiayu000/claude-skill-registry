---
name: exa-search
description: Use Exa for web/code/company research (web_search_exa / get_code_context_exa / company_research_exa), with parameters and examples; trigger when online search or parameter checks are needed.
---

# Exa

## Tools and parameters

### web_search_exa

- Purpose: general web search, returns ready-to-use text content
- Parameters:
  - `query`: search query (required)
  - `numResults`: number of results (default 8)
  - `type`: `auto` | `fast` (default `auto`)
  - `livecrawl`: `preferred` | `fallback` (default `fallback`)
  - `contextMaxCharacters`: max text length (default 10000)

### get_code_context_exa

- Purpose: code/docs/technical search
- Parameters:
  - `query`: search query (required)
  - `tokensNum`: returned token count (1000-50000, default 5000)

### company_research_exa

- Purpose: company info and news
- Parameters:
  - `companyName`: company name (required)
  - `numResults`: number of results (default 5)

## Parameter templates (JSON)

### web_search_exa

```
{"query":"...", "numResults":8, "type":"auto", "livecrawl":"preferred", "contextMaxCharacters":10000}
```

### get_code_context_exa

```
{"query":"...", "tokensNum":5000}
```

### company_research_exa

```
{"companyName":"...", "numResults":5}
```

## Invocation examples

```
URL="https://mcp.exa.ai/mcp?tools=web_search_exa,get_code_context_exa,company_research_exa"
npx -y mcporter call --http-url "$URL" --tool web_search_exa --args '{"query":"latest AI safety research"}'
npx -y mcporter call --http-url "$URL" --tool get_code_context_exa --args '{"query":"React useEffect cleanup examples","tokensNum":5000}'
npx -y mcporter call --http-url "$URL" --tool company_research_exa --args '{"companyName":"OpenAI","numResults":5}'
```

## Notes

- Tools and fields reference: `references/exa-tools.md`
- If you need an API key, pass `exaApiKey` as a request parameter

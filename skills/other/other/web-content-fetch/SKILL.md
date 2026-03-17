---
id: web-content-fetch
name: Web Content Fetch
description: Fetch full page content when snippets are insufficient
role: product
requiredTools:
  - type: builtin
    tool: fetch_web
---

## Web Content Fetch

When snippets from web search are not enough:

- Use **fetch_web** to retrieve the full content of a URL when the user or a prior search returned a URL that needs to be read in full.
- Cite the URL in your answer; do not invent content that was not in the fetched page.
- Use **fetch_web** when the user asks to "read this page", "what does this article say", or when search snippets are incomplete for the answer.
- Handle errors and paywalls: if the fetch fails or returns a paywall, say so and base the answer only on what was returned (or that the content could not be retrieved).
- Prefer **fetch_web** after **search_web** when you have a specific URL and need full-page extraction.

## Step-by-step instructions

1. When the user provides a URL or search returned a relevant URL: call **fetch_web** with that URL to get full page content.
2. Parse the returned content for the information the user needs (e.g. main points, dates, data); cite the URL.
3. If the user asked "what does this say" or "summarize this page", provide a short summary with the URL.
4. If fetch fails (timeout, 403, paywall): report that the content could not be retrieved and suggest the user open the URL directly or try another source.
5. Do not invent or hallucinate content; only state what is present in the fetched result.

## Examples of inputs and outputs

- **Input**: "What does https://example.com/article say about X?"  
  **Output**: Short summary of the article's points about X from **fetch_web** result; cite the URL.

- **Input**: "Search for recent news on Y and read the first result."  
  **Output**: Use **search_web** first; take the first result URL; call **fetch_web** on it; summarize the page and cite the URL.

## Common edge cases

- **Fetch fails**: Say "I couldn't retrieve the page (timeout/error/paywall)" and suggest opening the URL in a browser.
- **Empty or minimal content**: Some pages return little text (e.g. JS-heavy); report what was returned and that the page may need to be viewed in a browser.
- **Paywalled content**: Base the answer only on any non-paywalled part returned; do not invent paywalled content.
- **User gives no URL**: If the question implies a URL (e.g. "read the first result"), use search first to get a URL, then fetch.

## Tool usage for specific purposes

- **fetch_web**: Use when you have a URL and need full page content for summarization or extraction. Call with the URL; cite the URL in the answer; do not invent content.

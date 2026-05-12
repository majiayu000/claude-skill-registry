# llms.txt Specification

Jeremy Howard (AnswerDotAI), September 2024. Near-mainstream convention by April 2026. Anthropic and Perplexity confirmed support.

---

## Format Requirements

1. **Single H1 title** (required) — the site or project name
2. **Blockquote summary** — immediately after H1, concise site description
3. **H2 sections** — containing Markdown link lists in `[name](url): description` format
4. **`## Optional`** — has semantic meaning: AI systems can skip this section for shorter context windows
5. **Content-Type:** `text/plain; charset=utf-8`
6. **Location:** `/llms.txt` at site root

## Example Structure

```markdown
# Example SaaS Product

> Example SaaS is a project management tool for distributed teams, featuring real-time collaboration, automated workflows, and AI-powered task prioritization.

## Documentation

- [Getting Started](https://example.com/docs/quickstart): Installation, configuration, and first project setup
- [API Reference](https://example.com/docs/api): REST API endpoints, authentication, rate limits
- [Architecture](https://example.com/docs/architecture): System design, data flow, deployment options

## Guides

- [Authentication](https://example.com/guides/auth): OAuth 2.0, API keys, SSO integration
- [Webhooks](https://example.com/guides/webhooks): Event types, payload format, retry policy

## Optional

- [Changelog](https://example.com/changelog): Version history and release notes
- [Blog](https://example.com/blog): Product updates and engineering articles
- [Status](https://status.example.com): System status and incident history
```

## llms-full.txt

Community convention for extended content inlining — no formal spec.

- Same structure as llms.txt
- Instead of link lists, include the actual content of each page inline
- Typically 2,000–5,000 words
- Useful for AI systems that want full context without fetching individual pages
- Served at `/llms-full.txt`

## robots.txt Integration

Add discovery directives to robots.txt:

```
LLMs-Txt: /llms.txt
LLMs-Full-Txt: /llms-full.txt
```

## Best Practices

1. **Curated, not exhaustive** — select the most important pages, not every page. 10–30 links typical.
2. **Prioritize by importance** — most valuable content in the first H2 sections, less important under `## Optional`.
3. **Descriptions matter** — each link's description should explain what the page contains, not just name it.
4. **Update regularly** — stale URLs or removed pages undermine trust.
5. **Match site navigation** — H2 sections should roughly map to site sections.
6. **Full URLs** — use absolute URLs with protocol, not relative paths.

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| No blockquote summary | AI systems can't quickly assess relevance | Add 1–2 sentence blockquote after H1 |
| 100+ links | Defeats the purpose of curation | Keep to 10–30 most important pages |
| Missing `## Optional` | AI systems can't prioritize when context is limited | Move secondary content under `## Optional` |
| Stale URLs | 404s signal neglect | Audit quarterly |
| Relative paths | Some AI systems resolve from different bases | Use full `https://` URLs |
| HTML in llms.txt | Spec is Markdown only | Remove HTML tags |
| Duplicate of sitemap | llms.txt is curated commentary, not a URL list | Add descriptions, prioritize, organize |

## Validation

- Paste content into `llm-txt-validator.vercel.app` for format validation
- Check: exactly one H1, blockquote present, H2 sections with link lists
- Verify all URLs return 200

## Research Context

SERanking 300K-domain study (Nov 2025): no measurable citation improvement from llms.txt alone. However:
- Near-zero implementation cost (30 minutes to create)
- Forces you to inventory and prioritize citable content
- Adopted by Anthropic and Perplexity as a standard
- Establishes the site as AI-aware

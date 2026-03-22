---
name: alphaxiv-paper-lookup
description: Look up any arxiv paper on alphaxiv.org to get a structured AI-generated overview. This is faster and more reliable than trying to read a raw PDF.
---

# AlphaXiv Paper Lookup

Look up any arxiv paper on alphaxiv.org to get a structured AI-generated overview. This is faster and more reliable than trying to read a raw PDF.

## When to Use

- User shares an arxiv URL (e.g. `arxiv.org/abs/2401.12345`)
- User mentions a paper ID (e.g. `2401.12345`)
- User asks you to explain, summarize, or analyze a research paper
- User shares an alphaxiv URL (e.g. `alphaxiv.org/overview/2401.12345`)

## Workflow

### Step 1: Extract the paper ID

Parse the paper ID from whatever the user provides:

| Input                                      | Paper ID       |
| ------------------------------------------ | -------------- |
| `https://arxiv.org/abs/2401.12345`         | `2401.12345`   |
| `https://arxiv.org/pdf/2401.12345`         | `2401.12345`   |
| `https://alphaxiv.org/overview/2401.12345` | `2401.12345`   |
| `2401.12345v2`                             | `2401.12345v2` |
| `2401.12345`                               | `2401.12345`   |

### Step 2: Fetch the machine-readable report

```bash
curl -s "https://alphaxiv.org/overview/{PAPER_ID}.md"
```

This returns the intermediate machine-readable report — a structured, detailed analysis of the paper optimized for LLM consumption. One call, plain markdown, no JSON parsing.

If this returns 404, the report hasn't been generated for this paper yet.

### Step 3: If you need more detail, fetch the full paper text

If the report doesn't contain the specific information the user is asking about (e.g. a particular equation, table, or section), fetch the full paper text:

```bash
curl -s "https://alphaxiv.org/abs/{PAPER_ID}.md"
```

This returns the full extracted text of the paper as markdown. Only use this as a fallback — the report is usually sufficient.

If this returns 404, the full text hasn't been processed yet. As a last resort, direct the user to the PDF at `https://arxiv.org/pdf/{PAPER_ID}`.

## Error Handling

- **404 on Step 2**: Report not generated for this paper.
- **404 on Step 3**: Full text not yet extracted for this paper.

## Notes

- No authentication required — these are public endpoints.

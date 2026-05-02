---
name: papers
description: 'Search academic literature via arXiv, Semantic Scholar, and open-access PDFs. Use when the user needs papers, citations, or formal research.'
version: 1.9.3
alwaysApply: false
category: research
tags:
  - arxiv
  - semantic-scholar
  - academic
  - papers
  - pdf
dependencies:
  - leyline:document-conversion
estimated_tokens: 350
model_hint: standard
---
# Academic Papers Search

## When To Use

- Finding academic papers, citations, or formal research
- Building literature reviews or citation chains

## When NOT To Use

- Community opinions (use `/tome:discourse`)
- Code implementations (use `/tome:code-search`)

Search arXiv, Semantic Scholar, and open-access sources.

## Sources (Priority Order)

1. arXiv API (free, unlimited metadata)
2. Semantic Scholar API (100 req/5min, citation graphs)
3. Unpaywall (legal free version discovery)
4. CORE.ac.uk (open-access aggregator)
5. PubMed Central (biomedical)
6. Author preprint pages (WebSearch fallback)

## PDF Processing

After acquiring a paper URL or local file path, convert
the PDF to markdown for better extraction quality.

### Conversion (prefer markitdown)

Apply the `leyline:document-conversion` protocol:

1. **Try markitdown first**: call the MCP `convert_to_markdown`
   tool with the PDF URL or `file://` path. This produces
   structured markdown preserving tables, equations, figures,
   and section hierarchy.

2. **Fall back to Read tool** if markitdown is unavailable:
   - Read with `pages: "1-20"` for the first chunk
   - Continue with `pages: "21-40"` for longer papers
   - Continue in 20-page increments as needed
   - Note: tables and figures will not extract as cleanly

### Extraction Targets

From the converted markdown, extract:

- Abstract and key findings
- Methodology and experimental setup
- Results tables and figures
- Citation information (authors, year, venue)
- Key equations or formal definitions

## Fallback Guidance

When a paper is paywalled and no open version exists:
- Public library JSTOR/ProQuest access via library card
- DeepDyve article rental
- Inter-library loan request
- Direct author email template

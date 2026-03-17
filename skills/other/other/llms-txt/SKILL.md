---
name: llms-txt
description: Generate an llms.txt file for any project or website following the llmstxt.org specification. Use when asked to create llms.txt, generate LLM-friendly documentation, make a project AI-readable, or prepare documentation for language models.
argument-hint: [output-path]
---

# llms.txt Generator

Generate a well-structured `/llms.txt` file following the [llmstxt.org](https://llmstxt.org) specification proposed by Jeremy Howard.

## What is llms.txt?

A markdown file that helps LLMs understand and use a project/website efficiently. It provides:
- Concise project overview
- Links to key documentation with descriptions
- Organized sections for different resource types

## Generation Process

1. **Analyze the project structure** using Glob to find:
   - README files
   - Documentation directories (`docs/`, `documentation/`, `wiki/`)
   - API documentation
   - Example files and tutorials
   - Configuration files that explain the project
   - Source code entry points

2. **Identify key information**:
   - Project name and purpose
   - Main features and capabilities
   - Important caveats or limitations
   - Dependencies and requirements

3. **Generate the llms.txt** following this exact format:

```markdown
# Project Name

> Brief description of the project in 1-2 sentences. Include the most critical information needed to understand what this project does.

Key notes (if any important caveats exist):
- Important limitation or compatibility note
- Another critical detail

## Docs

- [Doc Title](url): Brief description of what this doc covers

## Examples

- [Example Title](url): What this example demonstrates

## API

- [API Reference](url): Description of API coverage

## Optional

- [Secondary Resource](url): Less critical but potentially useful
```

## Format Rules

1. **H1 (Required)**: Project/site name - this is the ONLY required section
2. **Blockquote**: Short summary with key context (highly recommended)
3. **Body text**: Important notes, caveats, or guidance (optional)
4. **H2 Sections**: Categorized lists of resources with URLs and descriptions
5. **Optional Section**: Resources that can be skipped for shorter context

## Best Practices

- **Be concise**: LLMs have limited context windows
- **Prioritize**: Put most important resources first
- **Describe well**: Each link should have a brief, informative description
- **Use "Optional" wisely**: Secondary resources that aren't always needed
- **Avoid jargon**: Explain terms that aren't universally known
- **Include external links**: Reference external docs if helpful (e.g., framework docs)

## URL Handling

- For **websites**: Use absolute URLs (`https://example.com/docs/api.md`)
- For **repositories**: Use relative paths or raw GitHub URLs
- Suggest creating `.md` versions of HTML pages at same URL + `.md` extension

## Output

Write the generated `llms.txt` to:
- `$ARGUMENTS` if provided
- Otherwise, project root as `llms.txt`

After generating, briefly explain what was included and why.

## Reference Examples

For examples of well-crafted llms.txt files, see [references/examples.md](references/examples.md).

---

**Note**: This skill does not require external scripts. The analysis and generation is performed directly using available tools (Glob, Grep, Read) to understand the project structure and generate appropriate content.

---
name: research-lib
description: Research a library and create comprehensive documentation in .claude/docs/libraries/.
disable-model-invocation: true
---

# Research Library

Research $ARGUMENTS and create documentation in `.claude/docs/libraries/`.

## Research Items

### Primary Tool: Gemini CLI

Use Gemini CLI (with Google Search grounding) for comprehensive library research:

```bash
gemini -p "Research: {library}. Find latest version, official documentation, key features, constraints, best practices, known issues, and usage patterns" 2>/dev/null
```

### Fallback: WebSearch/WebFetch

If Gemini unavailable, verify via manual web search:

- Official documentation
- GitHub README
- PyPI / npm page
- Latest release notes

### Content to Document

1. **Basic Information**
   - Official name, version, license
   - Official URL
   - Installation command

2. **Core Features**
   - Main features
   - Basic usage (code examples)

3. **Constraints & Notes**
   - Known limitations
   - Conflicts with other libraries
   - Performance characteristics
   - Async/sync considerations

4. **Usage Patterns in This Project**
   - Recommended usage
   - Patterns to avoid

5. **Troubleshooting**
   - Common errors and solutions

## Output Location

`.claude/docs/libraries/$ARGUMENTS.md`

## Documentation Template

```markdown
# {Library Name}

## Overview

- **Version**: {version}
- **License**: {license}
- **Official URL**: {url}
- **Installation**: `{install command}`

## Core Features

{Description of main features}

## Basic Usage

```python
{Code example}
```

## Constraints & Notes

- {Limitation 1}
- {Limitation 2}

## Recommended Patterns

### Do

```python
{Good pattern}
```

### Don't

```python
{Anti-pattern}
```

## Troubleshooting

### {Error message}

**Cause**: {cause}
**Solution**: {solution}

## References

- [Official Docs]({url})
- [GitHub]({url})
```

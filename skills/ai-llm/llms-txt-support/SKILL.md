---
name: llms-txt-support
description: Detect and use llms.txt files for LLM-optimized documentation. Use when checking if a site has LLM-ready docs before scraping.
---


# llms.txt Support Skill

## Purpose

Single responsibility: Detect, fetch, and utilize llms.txt files that provide LLM-optimized documentation, enabling 10x faster documentation ingestion. (BP-4)

## Background

The llms.txt standard (https://llmstxt.org/) provides a convention for websites to expose LLM-friendly documentation. Instead of scraping entire sites, check for llms.txt first.

**File hierarchy (check in order):**
1. `llms-full.txt` - Complete documentation (largest)
2. `llms.txt` - Standard documentation
3. `llms-small.txt` - Condensed documentation (smallest)

## Grounding Checkpoint (Archetype 1 Mitigation)

Before executing, VERIFY:

- [ ] Base URL is accessible
- [ ] Check all three llms.txt variants in order
- [ ] Validate file content is actual documentation (not error page)
- [ ] Confirm file size is reasonable for the documentation scope

**DO NOT assume llms.txt exists. Always probe first.**

## Uncertainty Escalation (Archetype 2 Mitigation)

ASK USER instead of guessing when:

- Multiple llms.txt variants found - which size to use?
- llms.txt content appears partial or outdated
- File returns but content seems like error page
- Site has llms.txt but content doesn't match expected documentation

**NEVER assume llms.txt quality without verification.**

## Context Scope (Archetype 3 Mitigation)

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | Target base URL, llms.txt content | Full site scraping |
| PERIPHERAL | llms.txt spec reference | Other sites' llms.txt |
| DISTRACTOR | Previous scraping attempts | Unrelated documentation |

## Workflow Steps

### Step 1: Detect llms.txt (Grounding)

```bash
# Check for llms.txt variants (in order of preference)
curl -I https://example.com/llms-full.txt
curl -I https://example.com/llms.txt
curl -I https://example.com/llms-small.txt

# Check common alternate locations
curl -I https://example.com/.well-known/llms.txt
curl -I https://docs.example.com/llms.txt
```

### Step 2: Validate Content

```bash
# Fetch and inspect first 100 lines
curl -s https://example.com/llms.txt | head -100

# Check file size
curl -sI https://example.com/llms.txt | grep -i content-length

# Verify it's not an error page
curl -s https://example.com/llms.txt | grep -i "not found\|error\|404" && echo "WARNING: May be error page"
```

### Step 3: Choose Variant

| Variant | Size | Use Case |
|---------|------|----------|
| `llms-full.txt` | Large (1MB+) | Complete documentation, full API reference |
| `llms.txt` | Medium | Standard use, balanced coverage |
| `llms-small.txt` | Small (<100KB) | Quick reference, limited context windows |

**Decision tree:**
1. If context window is limited → `llms-small.txt`
2. If need complete coverage → `llms-full.txt`
3. Default → `llms.txt`

### Step 4: Fetch and Process

```bash
# Download llms.txt
curl -o docs/llms.txt https://example.com/llms.txt

# Convert to skill format (if using skill-seekers)
skill-seekers scrape --llms-txt docs/llms.txt --name myskill

# Or process manually
# llms.txt is already LLM-optimized markdown
cp docs/llms.txt output/myskill/references/complete.md
```

### Step 5: Validate Output

```bash
# Check content structure
head -50 output/myskill/references/complete.md

# Verify sections
grep "^#" output/myskill/references/complete.md | head -20

# Check for code examples
grep -c '```' output/myskill/references/complete.md
```

## Recovery Protocol (Archetype 4 Mitigation)

On error:

1. **PAUSE** - Note which variant failed
2. **DIAGNOSE** - Check error type:
   - `404 Not Found` → Try next variant or alternate location
   - `403 Forbidden` → May need authentication or user-agent
   - `Timeout` → Retry with longer timeout
   - `Invalid content` → Fall back to traditional scraping
3. **ADAPT** - Try alternate approach
4. **RETRY** - Next variant (max 3 attempts per variant)
5. **ESCALATE** - Inform user llms.txt unavailable, suggest scraping

## Checkpoint Support

State saved to: `.aiwg/working/checkpoints/llms-txt-support/`

```
checkpoints/llms-txt-support/
├── detection_results.json    # Which variants found
├── selected_variant.txt      # Which was chosen
└── content_hash.txt          # For cache validation
```

## llms.txt Format Reference

Standard llms.txt structure:

```markdown
# Project Name

> Brief description of the project

## Overview
[High-level explanation]

## Installation
[Setup instructions]

## Quick Start
[Getting started guide]

## API Reference
[Detailed API documentation]

## Examples
[Code examples]

## FAQ
[Common questions]
```

## Detection Results Output

```json
{
  "base_url": "https://example.com",
  "detected": {
    "llms-full.txt": {
      "found": true,
      "url": "https://example.com/llms-full.txt",
      "size": 1523456,
      "last_modified": "2025-01-15T10:30:00Z"
    },
    "llms.txt": {
      "found": true,
      "url": "https://example.com/llms.txt",
      "size": 245678,
      "last_modified": "2025-01-15T10:30:00Z"
    },
    "llms-small.txt": {
      "found": false
    }
  },
  "recommended": "llms.txt",
  "reason": "Standard size, good for most use cases"
}
```

## Known Sites with llms.txt

Sites known to support llms.txt (verify before use):

- Anthropic documentation
- Many modern API documentation sites
- Framework documentation following the standard

**Always verify - this list may be outdated.**

## Troubleshooting

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| No llms.txt found | Site doesn't support | Fall back to doc-scraper |
| Content seems wrong | Error page or redirect | Check actual content, verify URL |
| File too large | llms-full.txt overwhelming | Use llms.txt or llms-small.txt |
| Outdated content | llms.txt not maintained | Consider scraping + llms.txt merge |

## Integration with doc-scraper

If llms.txt is incomplete or outdated, combine approaches:

```bash
# 1. Fetch llms.txt as base
curl -o base.md https://example.com/llms.txt

# 2. Scrape for additional/updated content
skill-seekers scrape --config config.json --skip-covered-by base.md

# 3. Merge results
# llms.txt provides structure, scraping fills gaps
```

## References

- llms.txt Standard: https://llmstxt.org/
- Skill Seekers llms.txt Detection: https://github.com/jmagly/Skill_Seekers/blob/main/docs/LLMS_TXT_SUPPORT.md
- REF-001: Production-Grade Agentic Workflows (BP-4, BP-9)
- REF-002: LLM Failure Modes (Archetype 1-4 mitigations)

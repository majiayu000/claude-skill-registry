---
name: directory-generate
description: Generate NGM Commons directory listings with iterative research and quality review. Uses Perplexity for deep research and Claude Opus for content generation with embedded SVG diagrams.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite, Task, WebFetch
user_invocable: true
argument-hint: <category_name> --entities "Entity1,Entity2,..." [--resume] [--dry-run] [--output-dir PATH]
---

# NGM Commons Directory Generator

Generate comprehensive, clinically useful directory listings for the NGM Commons platform.

## Invocation

```bash
/directory-generate <category_name> --entities "Entity1,Entity2,..." [options]
```

**Arguments:**
- `<category_name>` - Category to generate (e.g., "Microbiome Testing")
- `--entities "E1,E2,..."` - **Required**: Comma-separated list of entities
- `--resume` - Resume from last checkpoint if interrupted
- `--dry-run` - Show execution plan without running
- `--output-dir PATH` - Custom output directory (default: content/commons/)

## Execution Flow

### Phase 1: Research (Perplexity Sonar)

For each entity:
1. **First Principles** (Sonar Reasoning Pro) - HOW it works mechanistically
2. **Evidence Audit** (Sonar Deep Research) - Studies, pricing, regulatory status

Then:
3. **Market Context** - Category trends and landscape

### Phase 2: Content Generation (Claude Opus)

Generate with quality gates (auto-revise up to 3x if score < 0.8):

- **Section A**: Overview + methodology explanations
- **Section B**: Per-entity profiles
- **Section C**: Comparison tables + practice fit
- **Section D**: NGM Perspective + FAQ
- **SVG Diagram**: Methodology comparison

### Phase 3: Assembly

Combine into `directory_content.json` + `directory_page.html`

## Quality Criteria

| Criterion | Threshold |
|-----------|-----------|
| Clinical Utility | >= 0.8 |
| Educational Rigor | >= 0.8 |
| Vendor Neutrality | >= 0.8 |
| Factual Precision | >= 1.0 |
| Information Density | >= 0.8 |

## Key Principles

- **EDUCATING not RANKING** - No declaring winners
- **First Principles** - Explain HOW, not just WHAT
- **Factual Precision** - Never guess pricing
- **AEO Optimization** - Structured for AI search

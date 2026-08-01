---
name: literature-review
description: /literature-review [phase]
---

# Literature Reviewer Skill

## Invocation

```
/literature-review [phase]
```

Where `[phase]` is one of:
- `required-reading` - Process professor-provided texts
- `explore` - Exploratory searches to discover the field
- `define-domains` - Define domains based on exploration
- `search [domain]` - Systematic search for a specific domain
- `critique [domain]` - Run critique loop on domain summary
- `synthesize` - Write unified review chapter
- `status` - Show current progress

## Workflow Overview

### Phase 1: Required Reading

**Input:** 7 professor-provided texts in `academic/texts/`
**Output:** Understanding of what Artistic Research is

For each text:
1. Read and extract key concepts
2. Add to `../submission/references/bibliography.bib`
3. Document: What does this tell me about AR?
4. Document: How does this relate to Kepler project?
5. Update `checkpoint.md`

### Phase 2: Exploration

**Input:** Search queries from CLAUDE.md
**Output:** Understanding of the AR field, citation landscape

Steps:
1. Run exploratory searches across venues
2. Document findings (topics, citation counts, gaps)
3. Identify emerging themes/clusters
4. Note typical citation counts in AR field
5. Update `checkpoint.md` with findings

### Phase 3: Domain Definition

**Input:** Exploration findings
**Output:** Domain definitions, calibrated tier thresholds

Steps:
1. Review exploration notes
2. Identify 3-5 coherent domains
3. Calibrate citation tier thresholds for AR field
4. Update CLAUDE.md with domain definitions
5. Update `todo.md` with domain-specific tasks

### Phase 4: Systematic Search (per domain)

**Input:** Domain definition, search terms
**Output:** Domain summary, BibTeX entries

Steps:
1. Load context from `checkpoint.md`
2. Search using MCPs (Semantic Scholar, OpenAlex)
3. Search AR venues (JAR, PARSE, VIS, RC)
4. Triage papers by tier
5. Write domain summary (1500-2500 words)
6. Export BibTeX to `data/exports/domain_*.bib`
7. Update `checkpoint.md`

### Phase 5: Critique Loop

**Input:** Domain summary draft
**Output:** Revised summary, critique log

Steps:
1. Grade summary A-F on:
   - Completeness (all tiers covered?)
   - Coherence (logical flow?)
   - Relevance (connects to Kepler project?)
   - Citation quality (tier distribution appropriate?)
2. Log critique to `reviews.log`
3. Revise based on feedback
4. Re-grade until B+ or better

### Phase 6: Synthesis

**Input:** All domain summaries
**Output:** Unified review chapter

Steps:
1. Read all domain summaries
2. Write unified `systematic_review_chapter.md`
3. Update `../submission/docs/02-literaturrecherche.md`
4. Merge BibTeX into `../submission/references/bibliography.bib`
5. Build PDF: `cd ../submission && make literatur`
6. Final critique loop on unified chapter

## Critique Grading Rubric

| Grade | Criteria |
|-------|----------|
| A | Comprehensive, well-structured, all tiers covered, clear relevance |
| B | Good coverage, minor gaps, coherent structure |
| C | Adequate but missing key papers or weak connections |
| D | Significant gaps, poor structure, unclear relevance |
| F | Incomplete, major issues, requires substantial revision |

**Minimum passing grade:** B

## File Outputs

| File | Content |
|------|---------|
| `checkpoint.md` | Session state after each phase |
| `todo.md` | Updated task list |
| `reviews.log` | All critique feedback |
| `data/exports/*.bib` | BibTeX per domain |
| `drafts/*.md` | Domain summaries |

## Integration Points

**Final outputs go to:**
- `../submission/docs/02-literaturrecherche.md` - Chapter content
- `../submission/references/bibliography.bib` - Citations

**Build command:**
```bash
cd ../submission && make literatur
```

## Session Recovery

If context fills or session restarts:
1. Read `checkpoint.md` first
2. Resume from last incomplete phase/domain
3. Continue workflow from that point

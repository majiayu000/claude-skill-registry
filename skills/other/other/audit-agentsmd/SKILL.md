---
name: audit-agentsmd
description: Audit AGENTS.md (or CLAUDE.md) for length, attention-zone misplacement, and extraction opportunities. Produces a prioritized report with reordering and extraction recommendations. Use when AGENTS.md exceeds 400 lines, after major additions, or when agent instruction compliance is poor.
---

# Audit AGENTS.md

Analyzes an AGENTS.md (or CLAUDE.md) file for structural problems that cause AI agents to miss critical instructions — primarily length bloat and attention-zone misplacement.

## Why This Matters

LLMs exhibit a well-documented "lost in the middle" effect: instructions at the start (primacy) and end (recency) of long context get significantly higher attention than those in the middle. A 500+ line AGENTS.md has a ~60% "dead zone" where behavioral rules are likely to be ignored. This audit identifies misplacements and recommends fixes.

## Workflow

Copy this checklist and track progress:

```
Audit Progress:
- [ ] Step 1: Locate and measure the file
- [ ] Step 2: Parse section structure
- [ ] Step 3: Classify each section
- [ ] Step 4: Map to attention zones
- [ ] Step 5: Identify misplacements
- [ ] Step 6: Recommend extractions
- [ ] Step 7: Output report
```

### Step 1: Locate and Measure

Find the target file. Check in order:
1. Argument path (if provided via `$ARGUMENTS`)
2. `./AGENTS.md`
3. `./CLAUDE.md`

Record the line count. Flag if over 500 lines (Anthropic's recommended maximum for SKILL.md files, equally applicable to AGENTS.md when inlined via `@`).

If the file is under 300 lines, report "No structural issues — file is within optimal range" and stop.

### Step 2: Parse Section Structure

Identify every `## ` heading. For each section, record:
- Section name
- Start line number
- End line number (start of next section or EOF)
- Line count
- Whether it contains code blocks (count code block lines separately)

Use Grep to find headings, then Read to measure each section.

### Step 3: Classify Each Section

Classify every section into one of two categories using the rules in [EXTRACTION_RULES.md](EXTRACTION_RULES.md):

| Category | Description | Extraction Safety |
|----------|-------------|-------------------|
| **Behavioral** | Rules, guardrails, policies agents must always follow | UNSAFE to extract — must stay inline |
| **Reference** | Lookup material needed only for specific task types | SAFE to extract to docs/ |

**Key heuristic**: If the section contains words like NEVER, MUST, ALWAYS, "do not", or establishes a rule that applies to every task — it is behavioral. If it contains code examples, schema definitions, or step-by-step processes needed only situationally — it is reference.

### Step 4: Map to Attention Zones

Using the total line count, calculate the attention zones per [ATTENTION_MODEL.md](ATTENTION_MODEL.md):

| Zone | Range | Attention Level |
|------|-------|-----------------|
| Primacy | First ~20% of lines | **Strong** |
| Fade | ~20-35% | Moderate, declining |
| Dead zone | ~35-65% | **Weakest** |
| Recovery | ~65-80% | Moderate, rising |
| Recency | Last ~20% of lines | **Strong** |

Map each section's midpoint to a zone.

### Step 5: Identify Misplacements

Flag these anti-patterns:

**Critical misplacements (fix first):**
- Behavioral section in the dead zone → agent likely ignores the rule
- Reference section in the primacy zone → wastes highest-attention position on lookup material

**Medium misplacements:**
- Behavioral section in fade/recovery zone → rule may be partially followed
- Large code blocks (>20 lines) in primacy zone → displaces behavioral content

**Low priority:**
- Reference section in recency zone → not harmful but wastes prime position
- Duplicate/overlapping sections → consolidation opportunity

### Step 6: Recommend Extractions

For each reference section, evaluate extraction safety:

1. **Safe to extract**: Pure reference — code examples, schema details, process templates, syntax guides. Claude reads these on-demand when encountering a relevant task.
2. **Partially extractable**: Contains both a behavioral rule AND detailed process. Keep the rule stub inline (3-5 lines), extract the process details.
3. **Must stay inline**: Pure behavioral — guardrails, session workflows, policies. If removed, agents won't read the linked file proactively.

See [EXTRACTION_RULES.md](EXTRACTION_RULES.md) for the full classification checklist.

Calculate projected line count after recommended extractions.

### Step 7: Output Report

```markdown
# AGENTS.md Audit Report

Generated: {date}
File: {path}
Lines: {count} ({over/under} 500-line target)
Sections: {count}
Code block lines: {count} ({percent}% of file)

## Attention Zone Map

| Zone | Lines | Sections | Issues |
|------|-------|----------|--------|
| Primacy (1–{N}) | {list} | {count of behavioral vs reference} |
| ...

## Critical Misplacements

{For each: section name, current zone, recommended zone, why}

## Extraction Candidates

| Section | Lines | Category | Action |
|---------|-------|----------|--------|
| {name} | {N} | Safe to extract | → docs/{filename}.md |
| {name} | {N} | Partial | Keep {N}-line stub, extract {N} lines |
| {name} | {N} | Must stay inline | — |

## Recommended Section Order

{Numbered list showing optimal ordering:}
1. {Behavioral sections → primacy zone}
2. {Core patterns → early-middle}
3. {Reference/situational → middle}
4. {Process/workflow → late}
5. {Reminders section → EOF}

## Projected Result

| Metric | Before | After |
|--------|--------|-------|
| Total lines | {N} | {N} |
| Behavioral in dead zone | {N} sections | 0 |
| Reference in primacy zone | {N} sections | 0 |

## Reminders Section (Recommended)

If the file exceeds 300 lines, recommend adding a "## Reminders (Critical)"
section at EOF that repeats the 5-6 most important behavioral rules in
one-line form. This exploits recency bias to reinforce primacy-zone rules.
```

## Error Handling

| Situation | Action |
|-----------|--------|
| No AGENTS.md or CLAUDE.md found | Report "No agent instruction file found" and stop |
| File under 300 lines | Report "No structural issues" and stop |
| File uses `@` imports | Note that imported content is inlined — audit the combined effective content |
| CLAUDE.md contains only `@AGENTS.md` | Audit AGENTS.md (it's the real content) |

---

**REMINDER**: The goal is not to make AGENTS.md as short as possible — it's to ensure behavioral rules are in high-attention zones and reference material is either in low-attention zones or extracted to on-demand files. A 450-line file with good ordering beats a 300-line file missing critical context.

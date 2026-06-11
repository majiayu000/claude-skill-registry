---
name: condense
description: "Maximize information density: preserve all instructions, remove prose filler."
user-invocable: true  # justification: users type "/condense <file>" directly to tighten
                      # specific files; /do dispatch adds unnecessary routing overhead
                      # for a targeted file-editing operation.
argument-hint: "<file-or-glob>"
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
  - Grep
  - Glob
routing:
  triggers:
    - condense
    - reduce words
    - clarity pass
    - information density
    - remove prose
    - tighten
    - fewer words
  pairs_with:
    - skill-creator
    - anti-ai-editor
  complexity: Simple
  category: code-quality
---

# Condense

Strip prose filler from .md files. Preserve every instruction. This skill practices what it preaches.

## Phase 1: SCOPE

Identify targets.

1. **Single file**: User names a path. Read it.
2. **Glob**: User gives a pattern (`agents/*.md`). Expand, list matches, confirm with user.
3. **Batch (10+ files)**: Dispatch parallel agents, one per file.

**Mechanical pre-pass** (deterministic, run before LLM condensing): strip trailing whitespace and consecutive blank lines that inflate Opus token counts. The script handles the mechanical reduction so the LLM phase focuses on prose density.

```bash
python3 scripts/check-whitespace.py --fix <target-file-or-dir>   # 0=clean, 1=violations fixed
```

Run on the scoped targets (defaults to `agents/**/*.md` and `skills/**/*.md` when no path given). Then proceed to the LLM pass on the same files.

**Gate**: At least one target file identified and readable; mechanical pre-pass run.

---

## Phase 2: CONDENSE

For each file:

1. Read the full file. Record word count.
2. Rewrite in place applying the rules below.
3. Record new word count.

### Rules

**KEEP** (never cut):
- Every instruction, rule, gate, phase, step
- Tables, code blocks, commands, paths
- YAML frontmatter (do not alter)
- Structure: headers, numbered lists, phase ordering
- Technical terms naming specific things
- Reference loading tables
- Error handling sections
- Non-obvious "because X" reasoning

**CUT**:
- Redundant restatements of the same rule
- "Because X" on obvious rules
- Motivational framing ("this will help you", "it is important to note")
- Filler phrases: "in order to", "it should be noted that", "it is worth mentioning"
- Examples that repeat what the phase already says
- Paragraphs saying the same thing from different angles -- merge to one

**STYLE**: Short sentences. Active voice. Concrete words. If you can cut a word without losing an instruction, cut it.

### DELETE TEST

Before cutting any sentence: "If I remove this, does the reader lose an instruction, rule, or decision?" No = cut. Yes = keep.

### Boundaries

Do not reorganize sections, change meaning, add ideas, alter paths/commands, drop tables or code blocks, or modify YAML frontmatter values.

---

## Phase 3: VERIFY

For each condensed file:

1. **YAML check**: Confirm frontmatter parses.
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('<file>').read().split('---')[1])"
   ```
2. **Report**: Show `| File | Before | After | Reduction |` table with word counts.
3. **Instruction check**: Grep original for key terms (phase names, gate names, commands). Confirm each appears in condensed version. If any missing, restore from original.

**Gate**: YAML parses. No instructions lost. Reduction reported.

---

## Error Handling

**No prose to cut**: Report 0% reduction, move to next file.

**Instruction removed**: Re-read original, restore missing instruction, re-verify.

**YAML broken**: Restore original frontmatter verbatim, re-condense body only.

**Non-.md file**: Skip with warning.

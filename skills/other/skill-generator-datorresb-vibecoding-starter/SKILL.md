---
name: skill-generator
description: Transform extracted patterns into SKILL.md files following agentskills.io spec. Use when generating skills from patterns, creating reusable agent instructions, or completing the assimilation pipeline.
metadata:
  phase: 3
  pipeline: assimilation
  version: 1.0.0
---

# Skill Generator

## Overview

Transform filtered patterns into standard SKILL.md files that any AI agent can discover and use. This is phase 3 of the assimilation pipeline—applying regularization and generating skills.

This skill combines:
1. **Regularization** — Filter and abstract patterns to prevent overfitting
2. **Generation** — Create SKILL.md files following agentskills.io spec

---

## When to Use

Use this skill when:
- Generating skills from extracted patterns
- Creating reusable agent instructions from code analysis
- Completing the assimilation pipeline
- Converting patterns.json to SKILL.md files

---

## Input

**Required:** `.github/temp/patterns.json` (from pattern-extractor)

---

## Output

**Primary:** `.github/skills/<category>/<pattern-name>/SKILL.md`
**Mirror:** `.claude/skills/<category>/<pattern-name>/SKILL.md`

---

## Execution Steps

### Phase A: Regularization

#### Step A1: Load Patterns

```bash
if [ ! -f ".github/temp/patterns.json" ]; then
    echo "ERROR: patterns.json not found. Run pattern-extractor first."
    exit 1
fi
```

#### Step A2: Apply Category Thresholds

Filter patterns based on category-specific confidence thresholds:

| Category | Min Confidence | Rationale |
|----------|---------------|-----------|
| `architecture` | 0.80 | Errors are costly |
| `security` | 0.80 | High risk |
| `reliability` | 0.75 | Important |
| `quality` | 0.70 | Medium risk |
| `conventions` | 0.60 | Low risk, experimental OK |

**Action:** Remove patterns below their category threshold.

#### Step A3: Apply Abstraction Filter

Remove repo-specific details from patterns:

| Remove | Keep |
|--------|------|
| Specific file paths (`src/auth/login.ts`) | Generic path patterns (`src/<domain>/<feature>.ts`) |
| Variable names (`const userId = ...`) | Pattern structure (`const <identifier> = ...`) |
| Hardcoded values (`port: 3000`) | Parameterized values (`port: <config>`) |
| Company-specific terms | Generic domain terms |

**Rules:**
- Replace specific paths with `<path>` or generic patterns
- Replace variable names with `<identifier>` in pseudocode
- Keep pattern structure and relationships intact

#### Step A4: Deduplicate Patterns

Merge patterns that are functionally equivalent:

**Heuristic match:** Same if:
- Same category AND
- Similar name (Levenshtein distance < 3) AND
- Overlapping keywords (>50% match)

**Merge strategy:**
- Keep pattern with higher confidence
- Combine evidence from both
- Merge keywords (deduplicated)

#### Step A5: Check Registry (Optional)

If `skills-index.json` or `skills.json` exists:

1. For each pattern, check if similar skill already exists
2. Match by: name similarity + category + keywords overlap
3. If match found: Skip generation (skill already exists)
4. If no match: Proceed with generation

#### Step A6: Assign Status

| Confidence Range | Status |
|------------------|--------|
| ≥ 0.80 | `validated` |
| 0.60 - 0.79 | `experimental` |
| < 0.60 | (filtered out) |

#### Step A7: Save Filtered Patterns

Create `.github/temp/filtered-patterns.json`:

```json
{
  "source": { ... },
  "patterns": [
    {
      "name": "...",
      "category": "...",
      "confidence": 0.85,
      "status": "validated",
      "scores": { ... },
      "evidence": [ ... ],
      "description": "...",
      "keywords": [ ... ]
    }
  ],
  "filtered_count": <original - remaining>,
  "remaining_count": <count>
}
```

---

### Phase B: Skill Generation

#### Step B1: Create Directory Structure

```bash
# For each pattern category
mkdir -p .github/skills/architecture
mkdir -p .github/skills/reliability
mkdir -p .github/skills/quality
mkdir -p .github/skills/security
mkdir -p .github/skills/conventions

# Mirror for Claude
mkdir -p .claude/skills/architecture
mkdir -p .claude/skills/reliability
mkdir -p .claude/skills/quality
mkdir -p .claude/skills/security
mkdir -p .claude/skills/conventions
```

#### Step B2: Generate SKILL.md for Each Pattern

Use this two-part template:

```markdown
---
name: <pattern-name>
description: <WHAT it does>. Use when <WHEN to use - keywords for discovery>.
metadata:
  source-repo: <original-repo>
  confidence: <0.XX>
  status: <validated|experimental>
  category: <architecture|reliability|quality|security|conventions>
  generated-at: <ISO-timestamp>
---

# <Pattern Name>

## Overview

<Abstract description of the pattern — GENERALIZABLE, not repo-specific>

---

## When to Use

Use this skill when:
- <Trigger condition as prose>
- <Another trigger>
- <Keywords embedded naturally>

---

## Pattern Structure

<Pseudocode or abstract structure — NOT repo-specific code>

```pseudocode
// Generic pattern structure
function <patternName>(<params>) {
    // Step 1: <abstract step>
    // Step 2: <abstract step>
    // Step 3: <abstract step>
}
```

**Key Components:**
- <Component 1>: <purpose>
- <Component 2>: <purpose>

---

## Implementation Guide

### Step 1: <First Step>

<Instructions for implementing this step>

### Step 2: <Second Step>

<Instructions for implementing this step>

---

## Examples

> These examples are from the source repository and show one implementation.
> Adapt the pattern to your project's conventions.

**Source:** `<source-repo>`

See: `<file>:L<line>` — <brief description>
See: `<file>:L<line>` — <brief description>

---

## Conventions

✅ **Do:**
- <Best practice from pattern>
- <Another best practice>

❌ **Don't:**
- <Anti-pattern to avoid>
- <Another anti-pattern>

---

## Related

- [<related-skill>](../<category>/<skill>/SKILL.md)
```

#### Step B3: Apply YAML Safety

Before writing SKILL.md, escape special characters in YAML frontmatter values:

**Characters that require quoting:**

| Character | Problem | Solution |
|-----------|---------|----------|
| `:` | Breaks key:value parsing | Wrap value in `"..."` |
| `#` | Starts a comment | Wrap value in `"..."` |
| `{}[]` | YAML flow syntax | Wrap value in `"..."` |
| `&*` | Anchors/aliases | Wrap value in `"..."` |
| `?|>!%@` | Special YAML chars | Wrap value in `"..."` |

**Escape rules inside double quotes:**

```
\ → \\  (backslash first)
" → \"  (then double quotes)
```

**Implementation:**

```javascript
function quoteYamlValue(value) {
  // Quote if contains special chars or starts with quote
  if (/[:#{}[\]&*?|>!%@`]/.test(value) || 
      value.startsWith("'") || 
      value.startsWith('"')) {
    return `"${escapeYamlString(value)}"`;
  }
  return value;
}

function escapeYamlString(value) {
  return value
    .replace(/\\/g, "\\\\")  // Backslashes first
    .replace(/"/g, '\\"');   // Then double quotes
}
```

**Example:**

```yaml
# BAD - Will break YAML parsing
description: Use when: building APIs

# GOOD - Properly quoted
description: "Use when: building APIs"
```

---

#### Step B4: Write Skills to Both Locations

For each pattern:

```bash
CATEGORY="<category>"
NAME="<pattern-name>"

# Write to .github/skills
mkdir -p ".github/skills/${CATEGORY}/${NAME}"
# Write SKILL.md content (with YAML-safe frontmatter)

# Mirror to .claude/skills
mkdir -p ".claude/skills/${CATEGORY}/${NAME}"
# Copy identical content
```

#### Step B5: Generate Summary Report

After all skills generated:

```
✅ Skill generation complete

Generated Skills:
  architecture/
    - middleware-chain (validated, 0.92)
    - factory-pattern (validated, 0.85)
  reliability/
    - error-first-callback (validated, 0.78)
  quality/
    - arrange-act-assert (experimental, 0.72)

Summary:
  Total patterns: 12
  Filtered out: 4
  Skills generated: 8
  Validated: 6
  Experimental: 2

Locations:
  .github/skills/<category>/<pattern>/SKILL.md
  .claude/skills/<category>/<pattern>/SKILL.md
```

---

## Template Details

### Frontmatter (Required)

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ MUST | Pattern name in kebab-case |
| `description` | ✅ MUST | What + When, keywords embedded |
| `metadata.source-repo` | ✅ MUST | Original repository |
| `metadata.confidence` | ✅ MUST | Confidence score 0.0-1.0 |
| `metadata.status` | ✅ MUST | validated or experimental |
| `metadata.category` | ✅ MUST | One of 5 categories |

### Description Field Format

The description MUST:
1. Start with what the pattern does
2. Include "Use when" trigger phrase
3. Embed discovery keywords naturally

**Example:**
```
description: Chain request handlers with next() for modular processing. Use when building middleware pipelines, adding authentication layers, or implementing request preprocessing.
```

### Pattern Structure Section

MUST be:
- Abstract and generalizable
- Free of repo-specific paths
- Pseudocode or language-agnostic
- Focused on structure, not implementation details

**❌ Don't:**
```javascript
// From src/middleware/auth.js
const authMiddleware = require('./auth');
app.use('/api', authMiddleware);
```

**✅ Do:**
```pseudocode
function middleware(request, response, next) {
    // Process request
    if (condition) {
        // Handle locally
        return response.send(result);
    }
    // Pass to next handler
    next();
}
```

### Examples Section

MUST use references, not inline code:

**❌ Don't:**
```javascript
// Full code copied here
const express = require('express');
const app = express();
// ... 50 lines of code
```

**✅ Do:**
```markdown
**Source:** `expressjs/express`

See: `lib/router/index.js:L45` — Route matching and middleware chain
See: `lib/application.js:L120` — App-level middleware registration
```

---

## Error Handling

| Condition | Action |
|-----------|--------|
| patterns.json not found | FAIL with error message |
| All patterns filtered out | Warn user, produce empty output |
| Cannot create directory | FAIL with error message |
| Pattern has <2 evidence | Skip pattern, log warning |

---

## Conventions

✅ **Do:**
- Apply all regularization steps before generation
- Write to BOTH .github/ and .claude/ locations
- Use kebab-case for pattern names
- Include all required frontmatter fields
- Keep Pattern Structure abstract

❌ **Don't:**
- Include repo-specific paths in Pattern Structure
- Copy full code blocks (use references)
- Skip the status field
- Generate skills below threshold
- Organize by source repo (organize by category)

---

## Related Skills

- [repo-scanner](../repo-scanner/SKILL.md) — Phase 1: Scan repository structure
- [pattern-extractor](../pattern-extractor/SKILL.md) — Phase 2: Extract patterns
- [orchestrator](../orchestrator/SKILL.md) — Coordinates all phases

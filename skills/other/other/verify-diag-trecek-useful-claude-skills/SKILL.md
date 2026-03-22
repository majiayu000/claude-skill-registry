---
name: verify-diag
description: Verify an architecture diagram against the actual codebase. Checks component existence, connection accuracy, and read/write directionality. Use when user says "verify diagram", "verify diag", "check diagram", or wants to validate diagram accuracy.
---

# Verify Diagram Skill

Verify an architecture diagram's factual accuracy against the actual codebase. Adapted from the dry-walkthrough methodology for diagram validation.

## When to Use

- After generating an arch lens diagram
- User says "verify diagram", "verify diag", "check diagram"
- Before finalizing diagram examples or documentation

## Critical Constraints

**NEVER:**
- Modify source code files
- Modify the diagram during verification (report findings only)

**ALWAYS:**
- Verify every named component exists in the codebase
- Trace actual code paths for every connection
- Determine read/write directionality for every connection
- Report findings to terminal, not to files

---

## Verification Workflow

### Step 0: Validate Mermaid Syntax (Rendering Check)

**This step runs BEFORE semantic verification.** Extract every mermaid code block and check for syntax errors that would prevent rendering.

For each ```` ```mermaid ```` block, validate:

**1. Node label quoting:**
- `[...]` node content must NOT contain unescaped double quotes
- BAD: `A["value = "hello""]` — inner quotes break the parser
- GOOD: `A["value = hello"]` or `A[value = hello]`
- Check: scan all `[...]` and `(...)` node definitions for `"` inside content

**2. Bracket balance:**
- Every `[` has a matching `]` on the same line (for node definitions)
- Every `(` has a matching `)` on the same line
- Exception: `([...])` stadium shapes have nested brackets — count outer pair

**3. Special characters in node labels:**
- Parentheses `()` inside `[...]` labels break parsing — rephrase or remove
- Pipe `|` inside node labels conflicts with edge label syntax
- Curly braces `{}` inside node labels conflict with rhombus/decision syntax
- Hash `#` at start of label can be misinterpreted

**4. Edge label syntax:**
- Edge labels must use `-->|"label"|` or `-->|label|` format
- Unmatched pipe chars on edge lines break parsing

**5. Subgraph naming:**
- `subgraph NAME ["Display Title"]` — the `["..."]` is valid mermaid syntax
- But `subgraph NAME [Display Title]` without quotes is NOT valid if title has spaces

**6. Class definition syntax:**
- `classDef` lines must end with semicolons only if using shorthand
- `class A,B,C className;` — verify referenced node IDs exist in the diagram

**7. Node ID rules:**
- Node IDs must not start with numbers
- Node IDs must not contain spaces, hyphens (use underscores), or dots
- Reserved words (`end`, `subgraph`, `graph`, `flowchart`) cannot be node IDs

**Quick validation approach:**
```
For each mermaid block:
  1. Extract all node definitions (ID[label], ID(label), ID{label}, ID([label]))
  2. Check each label for unescaped quotes, pipes, unbalanced brackets
  3. Extract all edge definitions, verify pipe-delimited labels are balanced
  4. Extract all node IDs, check for reserved words and invalid characters
  5. Extract all class assignments, verify referenced IDs exist as nodes
```

**If syntax errors are found:** Report them in a `### Rendering Errors` section BEFORE the semantic findings. These are **blocking** — a diagram that won't render is worse than one with inaccurate connections.

---

### Step 1: Load the Diagram

Read the diagram file. Extract every verifiable claim:
- Named components (modules, functions, classes)
- Connections (arrows between components)
- Descriptions of what components do
- Metrics (counts, classifications)

### Step 2: Verify Components Exist

For each named component, check the codebase:

1. Does the referenced file/module/function/class exist?
2. Is the description of what it does accurate?
3. Is it a real standalone component, or an inline operation within another component?

Flag **phantom components** — things in the diagram that don't exist as discrete entities in code (e.g., showing an inline dict lookup as a separate "BuildKey" node).

### Step 3: Verify Connections — Read/Write Directionality

**This is the most important step.** For EVERY arrow/connection in the diagram:

1. **Trace the actual code path** — find the function call, import, or data handoff
2. **Classify the relationship:**

| Type | Description | Example |
|------|-------------|---------|
| **READ** | A reads/queries/receives from B | A calls B.get(), B returns data |
| **WRITE** | A writes/mutates/sends to B | A calls B.save(data) |
| **READ+WRITE** | Bidirectional data exchange | A calls B.process(input) → B returns output |
| **CALL** | A invokes B, no significant data transfer | A calls B.init() |

3. **Check arrow direction matches reality:**
   - Import direction (A imports B) != data flow direction
   - A calling B.process(x) → y means data flows A→B (args) AND B→A (return)
   - A generator yielding to B means data flows A→B on each yield

4. **Assess relevance:** Does the read/write distinction matter for this connection?
   - If showing it would change a reader's understanding of the architecture → flag it
   - If it's obvious or doesn't affect understanding → note but don't flag

### Step 4: Check for Missing Components

- Significant functions/classes in the traced code paths NOT in the diagram
- Decision points, error paths, or data transformations omitted
- Only flag things that matter at the diagram's abstraction level

### Step 5: Verify Metrics and Classifications

- Fan-in/fan-out counts: grep imports and count
- Layer assignments: check actual import directions
- Solid vs dashed arrows: verify the classification rationale
- "Write-only" claims: verify nothing reads the output back

---

## Output Format

Report findings to terminal only. Use this structure:

```
## Diagram Verification: {diagram name}

**Status:** PASS | RENDER ERROR | NEEDS CORRECTIONS
**Mermaid Syntax:** {PASS | X errors found}
**Components:** {X}/{Y} verified
**Connections:** {X}/{Y} accurate

### Rendering Errors (if any — BLOCKING)

| Line | Error | Fix |
|------|-------|-----|
| {line in mermaid block} | {what breaks} | {how to fix} |

### Corrections Needed

1. **{Component/Connection}**: {what's wrong} → {what it should be}
2. ...

### Directionality Findings

| Connection | Diagram Shows | Actual | Impact |
|------------|--------------|--------|--------|
| A → B | A flows to B | A calls B, B returns result (bidirectional) | Low/Medium/High |

### Missing
- {significant omissions}

### Phantom Components
- {things in diagram that aren't discrete code entities}
```

---

## Directionality Quick Reference

Common patterns and how to represent them:

| Code Pattern | Correct Arrow | Why |
|-------------|---------------|-----|
| `result = B.process(data)` | A →\|"calls"| B | Call direction; data flows both ways but call initiates from A |
| `A.save(data, B)` | A →\|"writes"| B | A produces, B stores |
| `data = B.read()` | A →\|"reads"| B | A consumes from B |
| `for x in generator()` | Gen →\|"yields"| Consumer | Data flows from generator |
| `A imports B` | A →\|"imports"| B | Dependency direction (module diagrams) |
| `A.callback(B.on_event)` | B -.->\|"notifies"| A | Event/callback reverses apparent direction |

---

## Launching Verification

Spawn one Explore subagent per diagram. Each agent:
1. Reads the full diagram file
2. Reads the relevant source files in the codebase
3. Performs all 5 verification steps
4. Returns structured findings

For multiple diagrams, launch agents in parallel.

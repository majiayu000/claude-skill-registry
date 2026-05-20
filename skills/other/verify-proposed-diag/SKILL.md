---
name: verify-proposed-diag
description: Verify a proposed architecture diagram against the actual codebase, selectively checking existing vs new components. Use when user says "verify proposed diagram", "verify proposed diag", "check proposed architecture", or after running /plan-arc.
---

# Verify Proposed Diagram Skill

Verify a proposed architecture diagram's factual accuracy against the actual codebase. Understands that proposed diagrams contain a mix of existing components (fully verifiable), modified components (partially verifiable), and new components (only integration points verifiable).

## When to Use

- After `/plan-arc` produces a proposed architecture document
- User says "verify proposed diagram", "verify proposed diag", "check proposed architecture"
- Any time a diagram mixes existing and proposed elements using `★`/`●` annotations

## Critical Constraints

**NEVER:**
- Modify source code files
- Modify the diagram during verification (report findings only)

**ALWAYS:**
- Respect the `★`/`●` annotation system — apply verification selectively
- Trace actual code paths for every connection involving existing components
- Determine read/write directionality for every verifiable connection
- Report findings to terminal, not to files

---

## Verification Workflow

### Step 0: Validate Mermaid Syntax (Rendering Check)

**This step runs BEFORE semantic verification.** Extract every mermaid code block and check for syntax errors that would prevent rendering. This applies to ALL elements regardless of annotation.

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
- `subgraph NAME ["Display Title"]` — valid mermaid syntax
- `subgraph NAME [Display Title]` without quotes is NOT valid if title has spaces

**6. Class definition syntax:**
- `class A,B,C className;` — verify referenced node IDs exist in the diagram

**7. Node ID rules:**
- Node IDs must not start with numbers
- Node IDs must not contain spaces, hyphens (use underscores), or dots
- Reserved words (`end`, `subgraph`, `graph`, `flowchart`) cannot be node IDs

**If syntax errors are found:** Report them in a `### Rendering Errors` section BEFORE semantic findings. These are **blocking** — a diagram that won't render is worse than one with inaccurate connections.

---

### Step 1: Load and Classify Elements

Read the diagram file. For every named component, classify it:

| Annotation | Classification | How to Identify |
|------------|---------------|-----------------|
| No prefix | **Existing** — claimed to exist as-is in the codebase | Node label has no `★` or `●` prefix |
| `●` prefix | **Modified** — exists today but the design proposes changes | Node label starts with `●` |
| `★` prefix | **New** — does not exist yet, proposed by the design | Node label starts with `★` |
| `newComponent` class | **New** — alternate indicator for new elements | Node assigned `newComponent` classDef |

Also extract every connection (arrow) and classify it by what it connects:
- **Existing ↔ Existing** — fully verifiable
- **Existing ↔ Modified** — fully verifiable (component exists, connection exists)
- **Existing ↔ New** — partially verifiable (existing side only)
- **Modified ↔ New** — partially verifiable (modified side only)
- **New ↔ New** — not verifiable against codebase

### Step 2: Verify Existing Components

For each **Existing** and **Modified** component:

1. Does the referenced file/module/function/class exist in the codebase?
2. Is the description of what it does accurate?
3. Is it a real standalone component, or an inline operation within another component?

Flag **phantom components** — things in the diagram claimed to exist that don't.

### Step 3: Verify Connections — Read/Write Directionality

For every connection where at least one side is **Existing** or **Modified**, trace the actual code:

1. **Find the code path** — the function call, import, or data handoff
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

4. **For connections to `★` New components:** verify the existing side exposes the interface the new component claims to connect to. The new component can't be verified, but its claimed integration point can.

### Step 4: Check for Missing Components

Look for significant existing components in the traced code paths that are absent from the diagram. Only flag things that matter at the diagram's abstraction level.

### Step 5: Verify Metrics and Classifications

- Fan-in/fan-out counts: grep imports and count
- Layer assignments: check actual import directions
- Solid vs dashed arrows: verify the classification rationale
- "Write-only" claims: verify nothing reads the output back

---

## Launching Verification

Spawn one Explore subagent per diagram in the document. Each agent:
1. Reads the full diagram
2. Classifies every element by annotation
3. Reads the relevant source files in the codebase
4. Performs all verification steps
5. Returns structured findings

For multiple diagrams, launch agents in parallel.

---

## Output Format

Report findings to terminal only. Use this structure:

```
## Proposed Diagram Verification: {diagram name}

**Status:** PASS | RENDER ERROR | NEEDS CORRECTIONS
**Mermaid Syntax:** {PASS | X errors found}

### Element Summary

| Category | Count | Verified | Issues |
|----------|-------|----------|--------|
| Existing components | {n} | {n}/{n} | {count} |
| Modified components (●) | {n} | {n}/{n} | {count} |
| New components (★) | {n} | n/a | n/a |
| Existing ↔ Existing connections | {n} | {n}/{n} | {count} |
| Existing ↔ New connections | {n} | {n}/{n} existing side | {count} |
| New ↔ New connections | {n} | n/a | n/a |

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

### Integration Point Verification

| New Component | Claims to Connect To | Interface Exists? | Notes |
|--------------|---------------------|-------------------|-------|
| ★ {name} | {existing component} | Yes/No | {details} |

### Missing

- {significant omissions from existing architecture}

### Phantom Components

- {things claimed to exist that don't}
```

---

## Directionality Quick Reference

Common patterns and how to represent them:

| Code Pattern | Correct Arrow | Why |
|-------------|---------------|-----|
| `result = B.process(data)` | A →\|"calls"\| B | Call direction; data flows both ways but call initiates from A |
| `A.save(data, B)` | A →\|"writes"\| B | A produces, B stores |
| `data = B.read()` | A →\|"reads"\| B | A consumes from B |
| `for x in generator()` | Gen →\|"yields"\| Consumer | Data flows from generator |
| `A imports B` | A →\|"imports"\| B | Dependency direction (module diagrams) |
| `A.callback(B.on_event)` | B -.->\|"notifies"\| A | Event/callback reverses apparent direction |

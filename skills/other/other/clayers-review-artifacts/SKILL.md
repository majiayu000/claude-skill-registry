---
name: clayers-review-artifacts
description: >
  Review and improve artifact mappings for end-to-end coverage between
  specification and code. Analyzes both directions (spec-to-code and
  code-to-spec), identifies gaps, improves mapping granularity, resolves
  drift with root-cause analysis, and validates exemptions. Use when:
  "review artifacts", "check coverage", "fix drift", "clayers-review-artifacts",
  "improve mapping quality", "drive coverage to 100%".
argument-hint: "[--code-path src/] [--rev abc123]"
allowed-tools:
  - Bash(clayers validate *)
  - Bash(clayers artifact *)
  - Bash(clayers connectivity *)
  - Bash(clayers query *)
---

# Clayers Review Artifacts

Review and improve artifact mappings for **main** to achieve
end-to-end traceability between specification and code.

**Goal**: Every spec node maps to code. Every code region maps to a spec
node. Coverage is precise (small ranges, focused nodes). Drift is zero.
Exemptions are justified.

---

## Before You Start

Run all quality checks to establish baseline:

```bash
clayers artifact --coverage clayers/main/
clayers artifact --drift clayers/main/
clayers connectivity clayers/main/
clayers validate clayers/main/
```

Record the numbers: total nodes, mapped, exempt, unmapped, drifted.
These are your starting point.

If `--rev` argument was provided, also check out the previous revision
and run coverage there for comparison (see Phase 7).

---

## Phase 1: Spec-to-Code Coverage (Unmapped Nodes)

**Question**: Which spec nodes have no artifact mapping?

```bash
clayers artifact --coverage clayers/main/
```

Look at the "unmapped nodes" section. For EACH unmapped node:

### 1.1 Determine if the node describes code

Read the node content:
```bash
clayers query clayers/main/ '//*[@id="NODE_ID"]' --text
```

Ask: **Does this node describe something implemented in code?**

| Node type | Likely maps to code? | Example |
|-----------|---------------------|---------|
| Algorithm, data structure, function | Yes | "Binary search implementation" |
| API endpoint, CLI command | Yes | "The validate command" |
| Data type, struct, enum | Yes | "ArtifactMapping struct" |
| Configuration, schema definition | Yes | "XSD schema for prose layer" |
| Design rationale, motivation | No | "Why we chose SHA-256" |
| Process description, workflow | Maybe | Depends if code implements it |
| Abstract concept, philosophy | No | "Spec-first methodology" |
| Future work, roadmap item | No | "Planned: git integration" |

### 1.2 If YES: Create an artifact mapping

Find the implementing code. Search by:
- Function/type names mentioned in the spec prose
- File paths mentioned in related mappings
- Module structure matching the concept

Create a **precise** mapping. Prefer:

| Approach | Coverage strength | Prefer? |
|----------|------------------|---------|
| Specific function (20 lines) | Precise | Yes |
| Module section (80 lines) | Moderate | OK |
| Entire file (500 lines) | Broad | Avoid |

```xml
<art:mapping id="map-{descriptive-name}">
  <art:spec-ref node="{NODE_ID}"
            revision="draft-1"
            node-hash="sha256:placeholder"/>
  <art:artifact repo="main"
            repo-revision="HEAD"
            path="{path/to/file}">
    <art:range hash="sha256:placeholder"
               start-line="{start}" end-line="{end}"/>
  </art:artifact>
  <art:coverage>full</art:coverage>
  <art:note>{What this code implements from the spec node.}</art:note>
</art:mapping>
```

If the implementation spans multiple non-contiguous ranges, use
multiple `<art:range>` elements in a single mapping.

After adding mappings:
```bash
clayers artifact --fix-node-hash clayers/main/
clayers artifact --fix-artifact-hash clayers/main/
```

### 1.3 If NO: Exempt with justification

Think carefully before exempting. Ask yourself:

- **Is this truly abstract?** Or is there code that realizes this concept?
- **Could the concept be decomposed?** Maybe the abstract part is exempt
  but a concrete sub-aspect maps to code.
- **Am I being lazy?** If the code is hard to find, that's not a reason
  to exempt.

**If unsure, ask the user.** Present the node content and your reasoning.

To exempt:
```xml
<art:exempt node="{NODE_ID}"/>
```

Always add a comment explaining WHY:
```xml
<!-- Exempt: design rationale with no implementing code -->
<art:exempt node="dec-why-sha256"/>
```

### 1.4 Validate after each batch

```bash
clayers validate clayers/main/
clayers artifact --coverage clayers/main/
```

**Success criteria**: Zero unmapped nodes (all mapped or explicitly exempted).

---

## Phase 2: Code-to-Spec Coverage (Uncovered Code)

**Question**: Which code regions have no spec node describing them?

```bash
clayers artifact --coverage clayers/main/ --code-path src/
```

Look at the "code coverage" section. For EACH file with uncovered ranges:

### 2.1 Analyze uncovered ranges

For each `NOT COVERED` range, read the code:
- What does this code do?
- Is it a distinct concept, or part of an already-mapped concept?
- Is it boilerplate/generated code that doesn't need spec coverage?

### 2.2 Extend existing mapping or create new spec node

**Option A: The code implements an already-described concept.**
Extend the existing mapping by adding another `<art:range>`:

```xml
<!-- Add a range to an existing mapping -->
<art:mapping id="map-existing">
  <art:spec-ref node="existing-concept" .../>
  <art:artifact ...>
    <art:range ... start-line="10" end-line="50"/>
    <!-- NEW: additional range for uncovered code -->
    <art:range hash="sha256:placeholder"
               start-line="80" end-line="95"/>
  </art:artifact>
</art:mapping>
```

**Option B: The code implements a new concept not yet in the spec.**
Create the spec node first (spec-first!), then map it:

1. Add `<pr:section>`, `<org:concept>`, `<rel:relation>`, `<llm:node>`
2. Register in index.xml if new file
3. Create `<art:mapping>` with precise line ranges
4. Fix hashes

### 2.3 Decompose broad mappings

If a file shows 100% coverage but all from one broad mapping (e.g.,
whole-file with 500 lines), consider splitting:

1. Identify distinct logical sections within the file
2. Create separate spec nodes for each section
3. Replace the single broad mapping with multiple precise mappings
4. Each mapping covers 10-80 lines ideally

**Coverage strength targets:**

| Strength | Lines | Quality | Action |
|----------|-------|---------|--------|
| Precise | 1-30 | Excellent | Keep |
| Moderate | 31-100 | Good | Keep or split if >80 |
| Broad | 101+ | Poor | Always split |

Check current mapping strengths:
```bash
clayers artifact --coverage clayers/main/
```

The output shows strength per mapping (e.g., `map-id: file.rs (150 lines, Broad)`).

**Success criteria**: Maximize code line coverage. No `Broad` mappings
unless the code is genuinely monolithic.

---

## Phase 3: Drift Resolution

**Question**: Are stored hashes consistent with current content?

```bash
clayers artifact --drift clayers/main/
```

For each drifted mapping, do NOT blindly fix. Analyze first.

### 3.1 ARTIFACT DRIFTED (code changed)

The code at the mapped lines changed. Investigate:

```bash
# What changed in this file?
git log --oneline -10 -- {file_path}
git diff HEAD~5 -- {file_path}
```

**Determine the cause:**

| Cause | Action |
|-------|--------|
| Lines shifted (refactor, added code above) | Update `start-line`/`end-line`, then `--fix-artifact-hash` |
| Function renamed/moved | Find new location, update path and/or line ranges |
| Semantic change (logic rewritten) | Review spec prose, update if needed, then fix hashes |
| Function deleted | Remove mapping, possibly remove/update spec node |
| File renamed/moved | Update `path` attribute |

**To update line ranges after a shift:**

1. Find where the function actually is now:
   ```bash
   grep -n 'fn function_name' {file_path}
   ```
2. Update `start-line` and `end-line` in the mapping
3. Run `clayers artifact --fix-artifact-hash clayers/main/`
4. Verify: `clayers artifact --drift clayers/main/`

**Pattern matching for line shifts:**
If many mappings in the same file drifted, it's likely a line shift.
Calculate the offset (new_line - old_line) and apply uniformly.

### 3.2 SPEC DRIFTED (spec node changed)

The spec prose for a mapped node changed. This means the description
evolved but the mapping hash is stale.

```bash
clayers artifact --fix-node-hash clayers/main/
```

Then verify the mapping still makes sense: does the code still implement
what the spec now describes? If the spec changed significantly, the
code mapping may need updating too.

### 3.3 UNAVAILABLE (file or node missing)

The mapped artifact can't be found. Possible causes:
- File was deleted or renamed
- Path is wrong (typo, different repo layout)
- Node ID was changed

**Fix**: Find the correct path/ID or remove the mapping.

### 3.4 Post-drift validation

After fixing all drift:
```bash
clayers artifact --drift clayers/main/
clayers artifact --coverage clayers/main/
clayers validate clayers/main/
```

**Coverage may have changed after drift fixes** (line ranges moved,
files renamed). Re-run coverage and fix any new gaps.

**Success criteria**: Zero drifted mappings.

---

## Phase 4: Exemption Audit

**Question**: Are all exemptions justified?

List current exemptions:
```bash
clayers query clayers/main/ '//art:exempt/@node' --text
```

For EACH exempted node:

1. Read the node:
   ```bash
   clayers query clayers/main/ '//*[@id="NODE_ID"]' --text
   ```

2. Ask: **Is this STILL exempt-worthy?**
   - Did someone add implementing code since the exemption?
   - Was the node refined to be more concrete?
   - Could part of it now be mapped even if the whole can't?

3. **If the exemption is no longer valid**: Remove `<art:exempt>` and
   create an artifact mapping instead.

4. **If unsure**: Ask the user. Present the node content and explain
   your reasoning for keeping or removing the exemption.

**Success criteria**: Every exemption has a clear justification. No
node is exempted just because finding its code is difficult.

---

## Phase 5: Mapping Quality Review

**Question**: Are mappings precise and well-described?

### 5.1 Check mapping strengths

```bash
clayers artifact --coverage clayers/main/
```

For each mapping, the output shows line count and strength classification.
Target: majority of mappings should be Precise (1-30 lines) or Moderate
(31-100 lines).

### 5.2 Split broad mappings

For any mapping classified as Broad (101+ lines):

1. Read the mapped code range
2. Identify logical sub-sections (functions, blocks, types)
3. Create separate spec sub-sections for each
4. Split the single mapping into multiple precise mappings
5. Each sub-mapping gets its own `<art:note>` explaining what it covers

### 5.3 Check mapping notes

Every mapping should have a descriptive `<art:note>`. Review:
- Does the note explain WHAT the code implements?
- Would someone reading only the note understand the mapping?
- Is the note current (matches what the code actually does)?

### 5.4 Check coverage values

Each mapping has `<art:coverage>full</art:coverage>` or `partial`.
Verify:
- `full`: the mapped range completely implements the spec node
- `partial`: the mapped range only partially implements it
  - Are there other ranges that complete the implementation?
  - Should additional ranges be added?

### 5.5 Spec node granularity

If a single spec node has many mappings pointing to it, the node may
be too broad. Consider decomposing:

```bash
# How many mappings per node?
clayers query clayers/main/ '//art:mapping/art:spec-ref/@node' --text
```

Count occurrences. If one node has 10+ mappings, it probably needs
to be split into sub-sections, each with their own mappings.

**Success criteria**: No Broad mappings. Every mapping has a descriptive
note. Coverage values are accurate.

---

## Phase 6: Connectivity Cross-Check

**Question**: Are mapped nodes well-connected in the spec graph?

```bash
clayers connectivity clayers/main/
```

Newly mapped nodes sometimes lack relations. For each node you mapped
or modified:
- Does it have at least one `<rel:relation>`?
- Is it connected to the main component (not isolated)?
- Are `depends-on` / `refines` / `references` relations accurate?

Fix isolated nodes by adding relations.

**Success criteria**: Zero isolated nodes.

---

## Phase 7: Revision Comparison (Optional)

Use when `--rev` argument is provided, or when you need to understand
how coverage changed between revisions.

### 7.1 Compare coverage across revisions

```bash
# Current coverage
clayers artifact --coverage clayers/main/

# Compare with a specific revision
git stash  # Save current work
git checkout {REV}
clayers artifact --coverage clayers/main/
git checkout -  # Return
git stash pop   # Restore work
```

### 7.2 Analyze changes

Compare the two reports:
- **New unmapped nodes**: Spec grew but mappings didn't keep up
- **New uncovered code**: Code grew but spec didn't keep up
- **Changed coverage %**: Lines shifted, mappings drifted
- **New/removed exemptions**: Review justifications

### 7.3 Trace specific drift

For mappings that drifted between revisions:

```bash
git diff {OLD_REV}..HEAD -- {artifact_path}
```

This shows exactly what changed in the code, helping you decide
whether to update line ranges or update the spec.

---

## Phase 8: Final Verification

Run the full check suite:

```bash
# 1. Structural validation
clayers validate clayers/main/

# 2. Drift detection (exit code 0 = clean)
clayers artifact --drift clayers/main/

# 3. Coverage analysis
clayers artifact --coverage clayers/main/

# 4. Connectivity
clayers connectivity clayers/main/
```

**All must be clean:**
- Validation: OK
- Drift: 0 drifted
- Coverage: 0 unmapped nodes, no Broad mappings
- Connectivity: 0 isolated nodes

Report to the user:
- Starting state (from "Before You Start")
- Ending state (current numbers)
- What was added/changed/exempted
- Any decisions that need user input

---

## Decision Framework: Map vs. Exempt

When you're unsure whether a node should be mapped or exempted, use
this framework:

### Always map (never exempt)

- Functions, methods, implementations
- Data types (structs, enums, classes)
- CLI commands and handlers
- API endpoints
- Configuration schemas
- Test suites (map to the code they test)
- Constants and type definitions

### Usually exempt (but consider carefully)

- Design decisions (`dec:decision` elements) that explain WHY
- Historical context that doesn't correspond to current code
- Methodology descriptions (how to use clayers, not clayers itself)
- Future work items not yet implemented
- Cross-cutting concerns described once but implemented everywhere

### Ask the user when

- A concept is partially implemented (map the partial part?)
- The implementing code is in a different repository
- The node describes emergent behavior (no single code location)
- You found code that seems related but aren't sure
- The boundary between abstract and concrete is unclear

**Default**: Map. Only exempt when you're confident there is truly no
implementing code. When in doubt, ask.

---

## Anti-Patterns to Avoid

| Anti-pattern | Problem | Better approach |
|-------------|---------|----------------|
| Whole-file mapping | Broad, imprecise | Split into function-level ranges |
| Copy-paste line numbers without reading | Ranges may be wrong | Always read the code at those lines |
| Exempting because code is hard to find | Hides gaps | Search harder, ask user |
| Fixing hashes without analyzing drift | Masks real changes | Understand what changed first |
| One spec node with 10 mappings | Node too broad | Decompose into sub-sections |
| Mapping to comments or blank lines | Inflates coverage | Map to actual logic |
| Skipping connectivity after changes | Isolated nodes | Always check connectivity |
| Trusting old line ranges | Code shifts happen | Verify current positions |
| Self-referential mapping (spec file maps to itself) | Spec files are both spec and artifact; editing the spec changes the artifact hash, creating infinite drift loops | Exempt the node or map to non-spec code only. **Never** map a spec XML file to itself as an artifact |

---

## Quick Reference: Commands

```bash
# Coverage (both directions)
clayers artifact --coverage clayers/main/
clayers artifact --coverage clayers/main/ --code-path src/

# Drift
clayers artifact --drift clayers/main/

# Fix hashes
clayers artifact --fix-node-hash clayers/main/
clayers artifact --fix-artifact-hash clayers/main/

# Query spec
clayers query clayers/main/ '//art:exempt/@node' --text
clayers query clayers/main/ '//art:mapping/art:spec-ref/@node' --text
clayers query clayers/main/ '//*[@id="NODE_ID"]' --text
clayers query clayers/main/ '//art:mapping' --count

# Connectivity
clayers connectivity clayers/main/

# Validate
clayers validate clayers/main/
```

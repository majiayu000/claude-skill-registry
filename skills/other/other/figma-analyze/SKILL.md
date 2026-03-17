---
name: figma-analyze
description: Analyze Figma designs for code implementation readiness and design-code parity. Use when working with Figma URLs, analyzing component designs, or checking token consistency.
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebFetch
  - mcp__figma__get_design_context
  - mcp__figma__get_variable_defs
  - mcp__figma__get_screenshot
  - mcp__figma__get_metadata
  - mcp__figma__get_code_connect_map
  - mcp__github__get_file_contents
user-invocable: true
---

# Figma Analyze

## Purpose

Analyze an existing Figma component against Nexus conventions. Validates design-code parity, token usage, and AI readability. Outputs a focused issues list with fixes.

## Input

| Format               | Example                                                       | Detection   |
| -------------------- | ------------------------------------------------------------- | ----------- |
| Figma URL            | `https://figma.com/design/:fileKey/:fileName?node-id=123-456` | URL pattern |
| Component name + URL | `Button https://figma.com/...`                                | Name + URL  |

Extract from URL:

- `fileKey` — from path segment after `/design/`
- `nodeId` — from `node-id` param, convert `123-456` → `123:456`

## Data Sources

### Figma (via MCP)

```
mcp__figma__get_design_context(fileKey, nodeId)  → Props, structure, generated code
mcp__figma__get_variable_defs(fileKey, nodeId)   → Tokens/variables used
mcp__figma__get_metadata(fileKey, nodeId)        → Frame names, hierarchy
mcp__figma__get_screenshot(fileKey, nodeId)      → Visual reference (optional)
```

### Nexus Token System

```
Read: packages/tailwind/nexus.css           → Semantic tokens (source of truth)
Read: .claude/rules/shadcn-divergences.md   → shadcn → Nexus mapping rules
```

### shadcn Reference (if applicable)

```
WebFetch: https://ui.shadcn.com/r/styles/default/{component}.json
```

---

## Workflow

### Phase 1: Gather All Context

**In parallel:**

1. **Figma Design** — Call MCP tools to get:
   - Component properties (names, types, values)
   - Variables/tokens used
   - Frame names and layer hierarchy

2. **Nexus Tokens** — Read:
   - `packages/tailwind/nexus.css` — actual semantic tokens available
   - `.claude/rules/shadcn-divergences.md` — divergence rules

3. **shadcn Reference** (if base component identified):
   - Fetch from registry to compare props/variants

### Phase 2: Run All Checks

Analyze Figma against Nexus conventions. Check each category and **only note issues**.

#### Check Categories

| Category               | What to Check                                                        |
| ---------------------- | -------------------------------------------------------------------- |
| **Property Names**     | Match code props exactly (`variant` not `Style`, `size` not `Scale`) |
| **Property Values**    | Lowercase (`sm`, `md` not `Small`, `Medium`)                         |
| **Boolean Props**      | Use `has*`/`is*` prefix (`hasLeadingIcon` not `showIcon`)            |
| **Layer Names**        | Standard names (`Label`, `LeadingIcon`, `TrailingIcon`, `Spinner`)   |
| **Token Usage**        | Semantic Nexus tokens, no hardcoded values or primitives             |
| **Token Naming**       | Follows Nexus patterns (see divergence checks below)                 |
| **States**             | Component includes hover, focus, active, disabled states as needed   |
| **Description**        | Component has AI-readable description                                |
| **Compound Structure** | Frame names match code exports (PascalCase, no spaces)               |

#### Divergence-Specific Checks

Cross-reference Figma variables against `shadcn-divergences.md`:

| Figma Uses              | Should Be                     | Rule                          |
| ----------------------- | ----------------------------- | ----------------------------- |
| `destructive/*`         | `error/*`                     | Nexus uses `error` naming     |
| `accent/*`              | `background-hover` or `muted` | Accent removed in Nexus       |
| `card/*`                | `container/*`                 | Renamed in Nexus              |
| `primary` (no suffix)   | `primary-background`          | Explicit `-background` suffix |
| `hover:*/90` or opacity | `*-background-hover`          | Semantic hover tokens         |
| `border-input`          | `border-default`              | Renamed in Nexus              |

#### Token Existence Check

For each Figma variable, verify it exists in `nexus.css`:

```
Figma: color/primary-background → Check: --color-primary-background exists? ✓
Figma: color/accent-hover → Check: --color-accent-hover exists? ✗ (use background-hover)
```

### Phase 3: Generate Report

Output a focused report with issues grouped by severity.

---

## Output Format

```markdown
## Figma Analysis: {ComponentName}

**Base:** {shadcn component or "Custom"}
**Type:** {Simple | Compound}
**Verdict:** {Ready | Needs Updates | Blocked}

---

### Issues

#### Blocking (Must Fix)

{If none: "None"}

1. **{Issue Title}**
   - Location: `{property/layer/token name}`
   - Current: `{what Figma has}`
   - Expected: `{what it should be}`
   - Why: {brief reason}

#### Should Fix

{If none: "None"}

1. **{Issue Title}**
   - Location: `{property/layer/token name}`
   - Current: `{what Figma has}`
   - Expected: `{what it should be}`

---

### Token Mapping

{Only show if there are token issues or divergences}

| Figma Variable  | Nexus Equivalent | Status |
| --------------- | ---------------- | ------ | --- | --- |
| `{figma token}` | `{nexus token}`  | {✅    | ❌  | ⚠️} |

---

### Custom Additions

{Only show if component has props/variants beyond shadcn base}

| Addition | Type                | Convention | Notes |
| -------- | ------------------- | ---------- | ----- | ------------ |
| `{name}` | {Prop/Variant/Slot} | {✅        | ❌}   | {brief note} |

---

### Checklist

- [{x| }] Property names match code
- [{x| }] Property values lowercase
- [{x| }] Layer names standard
- [{x| }] Tokens exist in Nexus
- [{x| }] No divergence violations
- [{x| }] States defined (hover, focus, active, disabled)
- [{x| }] Has component description
```

---

## Severity Guidelines

### Blocking

Issues that **break code generation or cause runtime errors**:

- Property name doesn't match code prop (case-sensitive)
- Token doesn't exist in Nexus (will fail compilation)
- Compound frame name doesn't match export
- Required prop missing

### Should Fix

Issues that **degrade quality but don't break builds**:

- Non-standard layer names (affects AI readability)
- Missing description
- Using deprecated token names (still works but inconsistent)

---

## Examples

### Clean Report (No Issues)

```markdown
## Figma Analysis: Button

**Base:** shadcn/button
**Type:** Simple
**Verdict:** Ready

---

### Issues

#### Blocking (Must Fix)

None

#### Should Fix

None

---

### Checklist

- [x] Property names match code
- [x] Property values lowercase
- [x] Layer names standard
- [x] Tokens exist in Nexus
- [x] No divergence violations
- [x] States defined (hover, focus, active, disabled)
- [x] Has component description
```

### Report with Issues

```markdown
## Figma Analysis: Button

**Base:** shadcn/button
**Type:** Simple
**Verdict:** Needs Updates

---

### Issues

#### Blocking (Must Fix)

1. **Invalid token reference**
   - Location: `color/destructive-background`
   - Current: `destructive-background`
   - Expected: `error-background`
   - Why: Nexus uses `error` naming, `destructive` tokens don't exist

2. **Property name mismatch**
   - Location: Property `Size`
   - Current: `Size` (PascalCase)
   - Expected: `size` (lowercase)
   - Why: Code prop is `size`, case-sensitive matching required

#### Should Fix

1. **Non-standard layer name**
   - Location: Layer `Button Text`
   - Current: `Button Text`
   - Expected: `Label`

2. **Missing component description**
   - Location: Component description field
   - Current: (empty)
   - Expected: Description following format: "{What} — {Use case}. Variants: {list}."

---

### Token Mapping

| Figma Variable                 | Nexus Equivalent             | Status    |
| ------------------------------ | ---------------------------- | --------- |
| `color/destructive-background` | `--color-error-background`   | ❌ Rename |
| `color/destructive-foreground` | `--color-error-foreground`   | ❌ Rename |
| `color/accent-hover`           | `--color-background-hover`   | ❌ Rename |
| `color/primary-background`     | `--color-primary-background` | ✅        |

---

### Checklist

- [ ] Property names match code
- [x] Property values lowercase
- [ ] Layer names standard
- [ ] Tokens exist in Nexus
- [ ] No divergence violations
- [ ] Has component description
```

---

## Error Handling

| Error                            | Action                                        |
| -------------------------------- | --------------------------------------------- |
| Figma MCP fails                  | Ask user to verify connection and permissions |
| Component not in shadcn registry | Treat as custom, check conventions only       |
| No variables used                | Flag as blocking — must use Figma variables   |
| Can't identify base component    | Ask user to specify                           |

---

## Key References

| Reference                             | Purpose                              |
| ------------------------------------- | ------------------------------------ |
| `packages/tailwind/nexus.css`         | Source of truth for available tokens |
| `.claude/rules/shadcn-divergences.md` | shadcn → Nexus mapping rules         |
| `.claude/rules/figma.md`              | Figma-code parity conventions        |
| `.claude/rules/components.md`         | Component structure requirements     |

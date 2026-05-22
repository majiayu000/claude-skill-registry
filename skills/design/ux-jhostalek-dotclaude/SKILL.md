---
name: ux
description: Use when reviewing a user-facing page or flow for usability issues, confusion, friction, or missed UX principles.
argument-hint: [page path or URL]
---

page_path = $ARGUMENTS

If page_path provided, focus on that page/component. Otherwise, evaluate entire application UI.

## Approach

Match evaluation depth to scope. A single component needs the 2-3 most relevant dimensions, not a 13-dimension sweep. A full page gets all 13. An entire app — focus on the 3 highest-traffic flows first; a full audit produces so many findings that none get fixed.

Gather context through whatever methods are available: live browser navigation (preferred), screenshots, or code review. At least one source is required. Combine multiple for best results.

Apply dimensions from [ui-evaluation.md](ui-evaluation.md). Score each 1-5.

## Output

### Scores

Rate each evaluated dimension 1-5 (1=broken, 5=excellent). Compact table. Overall UX score = average.

### Findings

**Critical** (blocks primary task): Issue → `file:line` → specific fix
**High** (major frustration): Issue → location → fix
**What Works**: Preserve these during fixes
**Low** (polish): Brief list

### Validation

For each critical/high fix: what to test (user action) and what success looks like (behavior or outcome).

After presenting: offer to implement top 3 critical/high fixes immediately.

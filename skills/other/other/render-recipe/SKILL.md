---
name: render-recipe
description: Render a recipe YAML as a compact visual overview with ASCII flow diagram and input table. Only invoke when the user explicitly says "render recipe" or "/render-recipe".
---

# Render Recipe

Produce a compact, structured overview of an AutoSkillit recipe. Reads the recipe YAML (provided in the prompt or loaded via `load_recipe`), analyzes the step graph, and writes a formatted Markdown file to `temp/render-recipe/`.

## When to Use

- User explicitly says "render recipe", "show recipe overview", or invokes `/render-recipe`
- Do NOT auto-invoke when a recipe is loaded — only on explicit user request

## Critical Constraints

**NEVER:**
- Modify any source code or recipe files
- Invent steps, ingredients, or routing not in the YAML
- Add decorative flair, emoji, or unnecessary commentary
- Create files outside `temp/render-recipe/` and `recipes/diagrams/`
- Use Unicode characters, emoji, or non-ASCII symbols. ASCII only — use `*` for pass, `x` for fail, `?` for confirm, `|` for spine, `+` for joins. No box-drawing characters, no arrows like `→` or `↑`, no check marks, no crosses. Write `->` and `(up)` instead.
- Include HTML comments, hash markers, format version markers, or any metadata in the output. No `<!-- ... -->` lines.
- Include "Agent-managed" lines listing internal context variables. The user doesn't need to see plumbing state.

**ALWAYS:**
- Read the recipe YAML carefully and render exactly what exists
- Write output to `temp/render-recipe/{recipe-name}_{YYYY-MM-DD_HHMMSS}.md`
- Print the rendered content to terminal after writing the file

---

## Rendering Specification

The output has exactly two sections. Follow this structure precisely.

**Note:** The inputs table is NOT part of the diagram output. It is generated at runtime from the recipe YAML by `_format_ingredients_table` (single source of truth). Do not include an inputs table in the diagram file.

### Section 1: Header

```
## {name}
```

Just the name. No description — the user already chose the recipe from the picker.

### Section 2: Flow Diagram

Build an ASCII flow diagram showing the step graph. This is the core visual.

**Infrastructure steps to hide:**
The diagram shows ONLY the *skill work* — `run_skill` invocations and `test_check`. Everything else is plumbing. Hide:
- **All `run_cmd` steps** — value capture, shell one-liners, branch computation. All plumbing.
- **All `push_to_remote` steps** — mechanical transport.
- **All `clone_repo` steps** — setup plumbing.
- **All issue lifecycle steps** — `get_issue_title`, `claim_issue`, `release_issue`. Plumbing.
- **All branch creation steps** — `create_unique_branch`, `create_branch`. Plumbing.
- **All CI/CD steps** — `wait_for_ci`, `wait_for_merge_queue`, `enable_auto_merge`, `route_queue_mode`, `reenter_merge_queue`, `queue_ejected_fix`, `diagnose_ci`. Plumbing.
- **All `merge_worktree` steps** — worktree-back-to-branch merge. Plumbing.
- **All cleanup steps** — `delete_clone`, `cleanup_failure`, `confirm_cleanup`. Teardown.
- **All post-PR steps** — `review_pr`, `resolve_review`, `diagnose_ci`, `resolve_ci`. Post-delivery plumbing.
- **All `action: route` steps** — pure routing nodes with no work.

If a hidden step is the *only* path between two visible steps, collapse the route — just connect the visible steps directly. The reader should see: "what skills run, in what order, and what happens on failure."

**Diagram layout:**

Use a vertical spine with `|` and `+--` branches. ASCII only — no Unicode.

1. **Main flow** runs down the left spine. Show meaningful steps in order.
2. **Optional steps** always go on their own `+--` branch off the vertical spine: `+-- [step-name] (optional)`. They are never inlined on a horizontal chain. Never repeat the step name outside the brackets.
3. **Iteration loops** are wrapped in a `FOR EACH` block using `+----+` / `+----+`. Only use this when `note:` fields indicate iteration over plan_parts or groups.
4. **Self-loops** go on the same line with a bidirectional arrow: `step <-> [x fail -> handler]`.
5. **Multi-way routing** (`on_result`) is shown with labeled paths on separate lines.
6. **Back-edges** use brackets: `-> plan [-> dry_walkthrough]`.
7. **Terminal steps** are omitted. The last visible step is the end of the diagram.
8. Do **not** show retry counts, model annotations, or other per-step metadata.
9. **`test_check` steps** display as `test`.
10. **Use the skill name, not the step key** for `run_skill` steps. But apply these short display names:
    - `implement-worktree-no-merge` -> `implement`
    - `audit-impl` -> `audit`
    - `resolve-failures` -> `fix`
    - `open-integration-pr` -> `open-pr`
    - Everything else: use the skill name as-is (e.g., `make-plan`, `dry-walkthrough`, `rectify`)
11. **FOR EACH loop routing** (more parts? / all done?) is implicit — omit it. The loop block itself conveys iteration. The first step inside the loop connects directly to the `+----+` box — no extra `|` line needed between them.
12. **Context limit recovery** (`retry_worktree`, `on_context_limit`) is automatic plumbing — omit it.
13. **Consistent failure language.** Always use `x fail` for failure branches. Never use "NO GO", "FAIL", "failure", or other variants.
14. **Back-edge targets must be the actual destination, not an intermediate optional step.** When a back-edge (e.g. audit fail) routes to a step that then passes through an optional step before reaching the real target, show the back-edge pointing to the real target directly. Example: if audit fail routes to `make_plan` and `make_plan.on_success` is `dry_walkthrough`, show `x fail [-> make-plan]` with the arrow going to `make-plan`, not to `review-approach`. The optional step is only reachable from its primary path, not from back-edges that happen to pass through the same chain.
15. **Center step names on the vertical spine.** When a step name appears on the main spine (not on a branch), center the text relative to the `|` character column. All spine-level step names should align to the same visual center.

**Reference example for implementation:**

```
      +-- [make-groups] (optional)
      |
 +----+ FOR EACH GROUP:
 |    |
 |    make-plan --- [review-approach] (optional) --- dry-walkthrough --- implement --- test <-> [x fail -> fix]
 |
 +----+
      |
      +-- [audit] (optional)
      |     x fail [-> make-plan]
      |
    open-pr
```

**Adapting to simpler recipes:**
- Recipes without iteration do not use `FOR EACH` blocks. Just show the linear flow with branches.
- Recipes with few optional steps can show them inline on the main flow: `clone ─── audit ─── investigate ─── plan ─── implement ─── test ─── merge ─── push`.
- Very simple recipes (under 8 meaningful steps) can use a single horizontal chain.
- Always adapt the shape to the recipe — do not force a complex layout on a simple recipe.

---

## Workflow

### Step 1: Parse the Recipe

Read the recipe YAML from the prompt context or from disk if a path is given. Identify:
- All ingredients and their properties
- All steps in declaration order
- Infrastructure steps to hide (see expanded list in Section 2)
- The happy path (follow on_success chain from first step)
- Branch points (on_failure to non-terminal, on_result routing)
- Back-edges (on_success/on_failure targets that appear earlier in declaration order)
- Optional steps (optional: true)
- Terminal steps (action: stop)

### Step 2: Build the Flow Diagram

Construct the ASCII diagram following the rules in Section 2. Start with the happy path, omit infrastructure steps, then layer in branches and optional annotations.

### Step 3: Verify the Diagram

Before writing, check the diagram for alignment errors. Scan every line and verify:

1. **Spine consistency.** The main vertical spine (`│`, `├`, `└`) must stay in the same column throughout the diagram. Find the column of the first `│` — every subsequent `│`, `├──`, and `└──` on the main spine must start in that same column. If a `FOR EACH` block's `┌`, `│`, `└` characters are indented further than the spine, shift them left to match.
2. **Box closure.** Every `┌` must have a matching `└` at the same indentation level.
3. **Branch alignment.** All `├──` branches off the same spine share the same column.
4. **No trailing whitespace drift.** Right-side annotations (`← only if ...`) should be column-aligned with each other where practical.

If any check fails, fix the diagram before proceeding. This is a mechanical check — count character positions, do not eyeball it.

### Step 4: Assemble and Write

Combine both sections and write to two locations:
1. `temp/render-recipe/{recipe-name}_{YYYY-MM-DD_HHMMSS}.md` — timestamped history copy
2. The recipe's diagram file — for bundled recipes: `src/autoskillit/recipes/diagrams/{recipe-name}.md`; for project recipes: `.autoskillit/recipes/diagrams/{recipe-name}.md`. This is the file that `load_recipe` serves to Claude.

Print the full content to terminal.

---

## Output Rules

| Content | Destination |
|---------|-------------|
| Rendered recipe overview | `temp/render-recipe/` (history) + `recipes/diagrams/` (live) + terminal |
| Validation warnings (if any) | Terminal only |

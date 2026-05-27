---
name: write-plan
description: "Use when you have a finalized `beagle-analysis:brainstorm-beagle` spec at `.beagle/concepts/<slug>/spec.md` and need a bite-sized, TDD-driven implementation plan before any code is written. Triggers on: \"write a plan\", \"plan this spec\", \"turn the spec into a plan\", \"now plan the implementation\", \"/write-plan\". Reads the spec, designs the file structure, decomposes work into 2-5 minute TDD steps with exact paths and commands, self-reviews against the spec, gets user approval, then writes to `.beagle/concepts/<slug>/plan.md`. Does NOT brainstorm specs, write code, or execute the plan — produces the plan document only."
disable-model-invocation: true
---

# Write Plan: Spec Into Implementation Plan

Turn a `beagle-analysis:brainstorm-beagle` spec into a comprehensive implementation plan that an engineer (or a downstream agent) can execute task-by-task without re-deriving intent.

The output is a single markdown plan document at `.beagle/concepts/<slug>/plan.md`, sitting beside the spec in the same concept folder. The plan captures HOW — file structure, task decomposition, exact code, exact commands — while the spec already owns WHAT and WHY.

<hard_gate>
Do NOT start writing the plan until a brainstorm-beagle spec exists at `.beagle/concepts/<slug>/spec.md`. If one is missing, stop and route the user to `beagle-analysis:brainstorm-beagle` first. Skipping the spec produces plans that bake in unexamined assumptions — the spec is the contract this skill plans against.
</hard_gate>

## Workflow

Complete these steps in order:

1. **Locate the spec** — find `.beagle/concepts/<slug>/spec.md`; if absent, stop and route to `beagle-analysis:brainstorm-beagle`
2. **Read the spec** — ingest every section; do not paraphrase, do not summarize away requirements
3. **Read project conventions** — scan `CLAUDE.md` (root and nested) for testing, commenting, and architecture rules the plan must respect
4. **Explore relevant code** — read existing files the plan will touch or pattern-match against; do not guess at structure
5. **Design file structure** — map which files will be created or modified before any task is written
6. **Decompose into tasks** — each task is bite-sized (2-5 minute steps), TDD-driven, with exact paths and code
7. **Self-review** — check against the spec, scan for placeholders, verify type consistency (see *Self-Review* below)
8. **Optionally dispatch a reviewer subagent** — only for plans that are long or cover unfamiliar territory (see `references/plan-reviewer.md`)
9. **Present draft to user** — show the draft in chat for review; iterate if needed
10. **Write to disk** — save to `.beagle/concepts/<slug>/plan.md` only after explicit user approval

```text
Spec at .beagle/concepts/<slug>/spec.md? ── No  → STOP, route to beagle-analysis:brainstorm-beagle
                                          ── Yes → Read spec + CLAUDE.md + relevant code
                                                   ↓
                                                   Design file structure
                                                   ↓
                                                   Decompose into TDD tasks
                                                   ↓
                                                   Self-review → fix inline
                                                   ↓
                                                   (optional) Dispatch reviewer subagent
                                                   ↓
                                                   Present draft → User review
                                                                  ├─ Changes? → Revise
                                                                  └─ Approved? → Write to plan.md
```

**The terminal state is a written plan.** This skill does not execute the plan, run tests, or modify production code. After writing, offer execution handoff via `beagle-core:subagent-prompt` if the user wants to run the plan in a fresh session; otherwise tell the user the plan is ready.

## Locating the Spec

The default input path is `.beagle/concepts/<slug>/spec.md`.

**Slug resolution priorities (in order):**
1. User-supplied path or slug (`/write-plan auth-rewrite`, "plan the spec at `.beagle/concepts/foo/spec.md`")
2. Recently-edited spec under `.beagle/concepts/`
3. Ask the user to disambiguate when multiple specs are plausible

**If no spec exists:**
> "I can't find a brainstorm-beagle spec at `.beagle/concepts/<slug>/spec.md`. Run `beagle-analysis:brainstorm-beagle` first to produce the spec, then come back to plan it."

Do not proceed. The spec is the contract; planning without one re-invents the spec under a different name and skips the review gates `brainstorm-beagle` enforces.

## Scope Check

If the spec covers multiple independent subsystems, it should have been decomposed during brainstorming. If it wasn't, stop and suggest splitting it — the brainstorm-beagle workflow has a *Scope Assessment* step for this. Each plan should produce working, testable software for one cohesive subsystem.

Signs the spec is too broad to plan in one document:
- More than ~15 must-have requirements with no shared core loop
- Requirements span independent subsystems (auth, billing, analytics — each is its own plan)
- The core loop can't be explained in 30 seconds

**Action:** push back to the user with: "This spec covers more than one cohesive system. I'd suggest splitting it during brainstorm-beagle and planning each sub-spec independently. Want to do that, or proceed with one big plan?"

## Reading Project Conventions

Before designing tasks, scan for project rules that shape the plan:

- **`CLAUDE.md` at repo root and any subdirectory you'll touch** — testing tiers, commenting policy, commit conventions, forbidden patterns
- **Test framework and runner** — Cargo, pytest, npm test, mix test, etc. Tasks must use the correct command.
- **Existing patterns** — if the codebase uses a particular file layout, follow it. The spec's *Constraints* and *Reference Points* often pin these.

When CLAUDE.md mandates something specific (e.g., "every user-visible feature needs a tier-3 test driven through the compiled binary"), the plan must include tasks that satisfy that rule. Do not silently produce a plan that violates project policy — call it out and adapt.

## Spike Before Plan-Lock

Plans written from documentation alone bake in toolchain assumptions that fail on first contact with the codebase. Before locking the plan, identify every claim of the form "tool X supports behavior Y" or "command Z produces output W" where neither this repo nor the team has a working example. Each such claim is a **spike candidate**.

For every spike candidate, the plan **must** include a `Task 0: Spike <claim>` whose body is:

1. Run the canonical command(s) the rest of the plan depends on, against this repo, as a documented step.
2. Capture the actual output (success path AND failure modes).
3. Either: confirm the spec's Key Decision survives intact, OR route the finding back to the user with a concrete revision proposal before any other task runs.

Task 0 is non-optional when the spec's Key Decisions rest on tool behavior the team has not verified in this repo. Examples of spike-required claims:

- "Tool X's `--workspace` flag handles this repo's multi-backend layout in one invocation."
- "Library Y's default test attribute uses the same pool config production uses."
- "CLI Z's introspection covers every query shape we'll write."
- "Migration framework W handles concurrent migrators against a fresh DB idempotently."

If the spike fails or surfaces caveats, **stop and revise the spec** — do not paper over the discovery with extra plan tasks. A spec that locks a Key Decision on a tool that does not behave as assumed is a spec that needs another brainstorm pass, not a plan that needs more workarounds.

This rule is stricter than the existing Assumption Audit. An assumption is "I'm guessing about behavior I haven't verified." A spike candidate is "the spec made a load-bearing decision about behavior nobody verified." The first is documented; the second is run.

## Parallel-Implementation Gate

When the plan adds a parallel implementation of an existing capability (a second database backend behind the same trait, a second platform target for the same UI, a second protocol adapter for the same service), the plan **must** end with a final task whose body is:

1. Identify the canonical contract/conformance test suite that pins the existing implementation's observable behavior.
2. Run that suite against **both** implementations in the same invocation.
3. Assert byte-identical observable behavior — return values, persistent rows, emitted events, error variants. Internal struct layout does not count.
4. Fail the task if either implementation's contract test is red. Do not declare the plan done while divergence is visible in the suite.

This task is the final gate and is non-optional. Without it, a plan that "implements the second backend in parallel" ships divergence — the executor declares each backend's tasks done in isolation while the contract test (which sees both) stays red unnoticed.

The behavior-equivalence gate is separate from any per-task contract tests. Per-task tests pin one implementation's behavior. The gate proves they agree.

## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, do not unilaterally restructure — but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

The file structure section appears in the plan document itself so the engineer (or the next agent) sees the shape of the work before reading individual tasks.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement the minimal code to make the test pass" — step
- "Run the tests and make sure they pass" — step
- "Commit" — step

Steps that bundle multiple actions ("write the test and the implementation") are too coarse — split them. Steps that describe behavior abstractly ("add validation") are too vague — show the code.

## Plan Document Format

Use the template in `references/plan-template.md`. The plan has these sections (in order):

1. **Header** — title, goal, architecture sketch, tech stack, link back to spec
2. **File Structure** — list of files to create or modify with their responsibilities
3. **Task N** blocks — one per cohesive unit of work, with TDD steps inside
4. **Self-Review Outcome** — a short note confirming the self-review pass was honest

Every plan MUST start with this header (literal markdown, fill in the brackets):

```markdown
# [Feature Name] Implementation Plan

> **Source spec:** `.beagle/concepts/<slug>/spec.md`
> **For downstream agents:** Execute task-by-task. Each task uses `- [ ]` checkboxes for tracking. Do not skip the test-first steps — they catch wiring bugs that pure-logic tests miss.

**Goal:** [One sentence describing what this builds, mirroring the spec's Core Value]

**Architecture:** [2-3 sentences about approach — how the pieces fit together]

**Tech Stack:** [Key technologies/libraries this plan uses]

---
```

### Task Template

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.ext`
- Modify: `exact/path/to/existing.ext:123-145`
- Test: `tests/exact/path/to/test.ext`

- [ ] **Step 1: Write the failing test**

```
// Show the assertions and the call site under test. The seed/setup
// loops are recovered by the executor from existing types and helpers
// — name a helper (e.g. `seed_entries(&store, id, count)`) but do not
// implement it here.
//
// Target: ~15 lines or less. Assertions pin observable consequence
// (a value, a file, a row, an output the next call would see), never
// dispatch ("the handler was called", "an event was emitted").
```

- [ ] **Step 2: Run test to verify it fails**

Run: `<exact project test command for this one test>`
Expected: FAIL — "<the exact failure message you expect>"

- [ ] **Step 3: Implement against the test**

**Files touched:** `path/to/impl.ext`

**Behavior contract** (what the implementation must satisfy — the executor writes the code):
- [The new/changed behavior bullet 1 — what's different from the reference]
- [The new/changed behavior bullet 2]
- [Up to 5 bullets total; past that, replace with a tighter reference]

**Reference:** `path/to/analog.ext:line-line` — [one-sentence delta: what to mirror, what to change]. Pointers only; do NOT paste the cited code inline. The executor opens the file.

- [ ] **Step 4: Run the new test AND the relevant suite, verify both green**

Run: `<same test command as Step 2>` → Expected: PASS.
Then run: `<the broader test scope this task lives in — the module, the package, the contract suite, whichever covers the surface this task touched>` → Expected: PASS with zero regressions.

A new test that passes while a sibling test silently turns red is a task failure, not a deferred concern. "I only ran the one I wrote" is how a contract test stays red across an entire plan. Specify the exact broader-scope command in this step; do not leave it as "run the suite" — the executor needs a copy-pasteable command.

- [ ] **Step 5: Sweep modified files for leftovers**

Describe sweep targets in plain language: "remove stale references to `<old_name>`, the orphaned `<import>`, and doc-comments describing the old shape." The executor greps for them. Do NOT enumerate line numbers in the plan — they will be wrong by execution time and the executor can find them faster than you can list them. New-file-only and config-only tasks skip this step.

- [ ] **Step 6: Commit**

```bash
git add <specific paths>
git commit -m "<type>(<scope>): <imperative summary>"
```
````

## Code in Steps: Tests Yes, Implementations No

The plan's job is to lock down the **contract** for each task. Tests are the contract; implementations are how the executor satisfies it. They get different treatment in the plan.

**Show real, exact code for:**

- **Test step bodies** — the assertion is the contract. If a test asserts the wrong thing, the impl can be wrong and the suite still passes. Tests must be written precisely in the plan, in the project's language, with the actual functions and types they will use.
- **Commands** — exact test commands, exact migration commands, exact lint/typecheck commands. Not paraphrases.
- **Commit messages** — exact strings.
- **Configuration changes** — exact diffs to config files (dependency versions, feature flags, environment variables) where the value is the contract.

**Do NOT show full code for:**

- **Implementation step bodies.** The planner is guessing at code that will be written under real type signatures, real library versions, and real adjacent code the executor can see and the planner can't. A pre-written implementation in the plan is almost always wrong by the time execution starts; the executor then has to reconcile their real code with the planner's sketch, which is worse than no sketch.

  Instead, for an implementation step, provide:
  - **Files touched** — exact paths
  - **Behavior contract** — 2-5 bullets describing what the impl must satisfy. Plain language. Verifiable against the test from the prior step.
  - **Reference** — pointer to the closest analogous existing implementation, or the closest analog from the spec's Reference Points

This is not a license to be vague. "Behavior contract" means *concrete observable behavior the test will verify*. A bullet like "handle errors" is forbidden; "if the input contains a duplicate id, return an `Err`/exception of the project's error type with a message naming the duplicate id" is required.

The discipline is: **the plan defines what counts as correct; the executor writes code that meets it.** This is what TDD already says; writing the impl twice (once in the plan, once at execution) reverses the order.

**Failure-propagation policy is non-optional in every contract that introduces a fallible operation.** When a task adds a new serialization, deserialization, parsing, type conversion, network call, file open, or any other operation that can return an error, the contract MUST state how that error propagates:

- **Required policy** for boundary-internal code paths (anything that runs after the input has already been validated): propagate the error via the project's error type. `?` / `change_context` / `map_err` to the project's variant. The caller decides.
- **Forbidden patterns**: `.unwrap_or(<non-default fallback string>)` to coerce a None or Err into a plausible-looking placeholder value; `.unwrap_or_default()` on a type whose default is a meaningful value (empty string, zero ID, default enum variant); silent `.ok()` discarding the error.
- **Allowed exceptions** only when the contract spells them out: a true default that the type system makes obvious (an empty vec when "no results" is the spec'd outcome), with one sentence naming why the default is correct.

Bullets like "serialize the entry_type to the row" are insufficient; the bullet must say "serialize via `to_value`?; coerce to string via `.as_str().ok_or_else(...)?`; never silently substitute a fallback variant." If the contract does not state the policy, the executor will reach for `unwrap_or` and the bug will ship.

## The Recoverability Test

After drafting each step, re-read it line by line and ask:

> "Does the executor need this line, or can they recover it by reading the referenced file?"

Delete anything they can recover. A plan is not a re-creation of the codebase in markdown — it's the minimum delta the executor cannot derive themselves. The executor has the codebase open. They will read the file you reference. They will look up the test helper, the existing impl, the migration history, the trait signature. You do not need to copy that material into the plan.

Apply the recoverability test to every step before commit:
- **Test bodies:** the executor can write the seed/setup loop themselves — show the assertions and the call site. They cannot recover *which assertion pins the spec* from any other source.
- **Behavior contracts:** the executor can read the analogous existing impl — point at it with `file.ext:line-line`. They cannot recover *the new behavior that makes this task different from the reference*.
- **Reference blocks:** a reference is a pointer (`launch.rs:397-400`). The executor opens the file. Pasting the cited code inline is duplication that rots the moment the underlying code shifts.
- **Sweep instructions:** "remove stale comments and the orphaned `PgPool` import" is enough — the executor can grep the file for `PgPool` themselves. Enumerating line numbers ("line 71-72, lines 117-122, line 194") is the executor's job at execution time.

A plan that fails the recoverability test is verbose, not specific. **Verbosity ≠ specificity.** Specificity is one sentence that pins the right invariant. Verbosity is enumerating every leaf when a reference would do.

## Test Authoring Discipline

Four rules for the test code you write into Step 1 of each task.

**A contract is the minimum text that, if violated, makes the test fail.** Anything beyond that is speculation. If a test body grows past ~15 lines, you are probably re-deriving setup the executor can write themselves. The assertions are the contract; the setup is plumbing.

**Show the assertions and the call site. Skip the seed loop.** Tests pin behavior, not setup. A compaction test does NOT need to construct 5 `SessionEntry` values explicitly — it needs to show: a call to `compact_entries(_, N, summary)`, the assertions on what `load_entries` then returns, and the assertion on the inserted summary row's `seq`. The data construction is recovered by the executor from the existing types and existing helpers.

**Reuse first; invent only when nothing fits.** Before writing a fresh `make_user()`, `test_entry()`, `pty_spawn`, fake DB pool, or fixture, grep the codebase for an existing one with the same shape. New helpers in the plan should be the exception, not the default. Existing helpers already encode discipline the plan would otherwise re-derive — correct cleanup, realistic data shapes, project-typical error handling. When the plan must introduce a new helper, name a specific existing one that was considered and explain why it didn't fit. "I didn't grep" is not a reason. When the plan references a helper the executor will write, name it with its signature (`seed_entries(&store, session_id, count: i64)`) but do not implement it in the plan body.

**Pin the spec, not every conceivable edge case.** A test exists to prove a specific spec requirement is met or a specific failure mode (named in the spec or in your Assumption Audit) is closed. One precise test per behavior the spec calls out, plus one test per named bug class, is the target. If you find yourself writing the 5th boundary test for the same function "just in case," stop — the marginal coverage is probably negative once you count maintenance cost and the noise it adds to the suite. Speculative input-space exhaustion belongs in property-based tests or fuzz harnesses if the project has them; otherwise it's overengineering. YAGNI applies to tests, not just impl.

## Behavior Contract Discipline

Two rules for the behavior contract under each implementation step.

**3-5 bullets is the target. Past 5, replace the rest with a reference.** A behavior contract enumerates what's new or different about this task's impl. The shape, the error handling, the codecs, the helper functions — all of that is in the referenced analog. If you're writing 12 bullets describing types, indexes, fields, and rationale, you are re-deriving the implementation in markdown form. Replace with: `Schema matches <reference migration file> with <one-sentence delta>`. Specificity is the delta from the reference, not the full state.

**References point, they do not paste.** A reference is a file path with a line range: `core/osprey-core/src/session/pg.rs:271-309`. Inline code blocks under "Reference:" are an anti-pattern — they duplicate code the executor will read anyway when they open the file, and they rot the moment the underlying code shifts. If you find yourself pasting more than a function signature, you've turned the reference into a re-implementation. Stop and replace with the file/line pointer.

## Cleanup Discipline

Every task that **modifies an existing file** ends with a sweep: remove anything the change made stale. This is part of the task, not a separate phase.

The sweep covers, in the files this task touched:
- Comments that referenced the old behavior, name, or signature (e.g. `// returns the PG pool` when the function now returns an `Arc<dyn Store>`)
- Imports that were used only by code the change deleted
- Function parameters, struct fields, enum variants, or helper functions that were used only by call sites the change replaced
- Dead match arms, unreachable branches, unused private functions
- Stale doc-comments on the file or its functions — especially phase/PR/ticket citations no longer load-bearing

A task that adds the new thing but leaves the old comments, imports, or dead helpers lying around is **not done** — it has shipped a partial change and made the next reader hunt for what's still current. The plan should make the sweep visible: each task's Step 5 commit lists exactly the files touched, and the executor's act of staging those files is the moment to sweep them.

**Exceptions:**
- Tasks that only create new files have nothing to sweep.
- Tasks that only edit configuration (Cargo.toml, package.json, CI YAML) sweep only those files.

This is separate from dedicated `Cleanup` tasks that close out residue in files no other task touched. Both can exist in the same plan; they handle different leftovers. The per-task sweep rule prevents the common case where a refactor leaves residue inside the file it just modified.

## No Placeholders

Every step must contain the actual content an executor needs. These are **plan failures** — never write them:

- "TBD", "TODO", "implement later", "fill in details", "to be determined"
- "Add appropriate error handling" / "add validation" / "handle edge cases" — without naming WHICH errors, WHICH validation rules, WHICH edge cases
- "Write tests for the above" — without the actual assertion the test must make
- "Similar to Task N" with no further information — see *Patterns* below for the right way to handle repetition
- Test steps without exact assertions, command steps without exact commands, commit steps without exact messages
- References to types, functions, or methods not defined in any task or already in the codebase

A behavior contract under an implementation step is **not** a placeholder — it is the deliberate contract the executor implements against. The forbidden pattern is vague language without a contract; the required pattern is specific contract without speculative code.

## Patterns: Naming Repetition Once

When the same transformation applies across many sites (e.g. "convert N call sites to a new API", "migrate N test files to a new fixture"), DRY the plan by naming the pattern once in a **Patterns** section at the top of the plan, then referencing it from each task. Each task that uses the pattern still:

- Names its specific files (no "see file list" — the list is in the task)
- Writes its own test step with real assertions
- Has its own commit with its own message

What the Patterns section absorbs is only the *transformation shape* and the *reference example* — never the test or the commit. The point is to let a downstream agent execute one task at a time without needing to read other tasks to understand it, while not making the plan write the same paragraph 49 times.

Example: a task that converts 14 query call sites in one file references the pattern; its test asserts that the file's tests still pass after the conversion; its commit covers just that file. A second task converting 4 sites in a different file references the same pattern and has its own test/commit.

**Pattern Application Audit.** When a Pattern is applied across many sites, the plan **must** include a final `Audit: <pattern name>` task immediately after the last site-conversion task. The audit task has three steps:

1. **Grep-confirm zero remaining old-pattern sites.** Exact command; expected empty output.
2. **List production-config divergence.** Walk every site converted and call out which depend on production-specific configuration the new pattern does not replicate (pool settings, timeouts, isolation levels, env, signal handlers). The audit task body enumerates these sites explicitly — not "check the sites," but "site A at file:line depends on X, site B at file:line depends on Y." Either fix each (custom fixture, helper override, etc.) in the audit task or open a follow-up task before moving on.
3. **Sample-verify three random converted sites against production wiring.** Pick three sites, run the corresponding production-wiring test (tier-2 or tier-3 per the project's tiering rule), assert the converted test still covers the original bug class. If any sample regresses, the pattern needs a per-site escape hatch the audit names.

The audit is not a stylistic step. Patterns applied blindly across N sites are how production-config divergence (e.g. test pool config silently diverging from production pool config) ships green. The audit forces the planner to enumerate and the executor to verify.

## Assumption Audit

Implementation plans bake in assumptions that the spec doesn't always pin. Before finalizing the plan, list the assumptions you made — data shapes, naming, library choices, error semantics, persistence boundaries — and check each against the spec.

**Re-read the files the spec names.** A spec may characterize a file or function in a way that's outdated or partial; the file's own doc comment, header, or surrounding code may encode a constraint the spec missed. If the spec's characterization contradicts a load-bearing comment or pattern in the code, surface it as an assumption-audit item rather than trusting the spec blindly. Spec authors are often working from memory; the code is the ground truth.

If an assumption isn't anchored by the spec and could plausibly be made differently, surface it to the user during the *Draft Review* step. The user either confirms (and you proceed) or corrects (and you revise). Do not silently choose.

Capture confirmed assumptions in a short "Assumptions" block under the header. Future readers (and the executor agent) need to see what was decided here, not just in the spec.

## Self-Review

After drafting the complete plan, look at the spec with fresh eyes and check the plan against it. This is a checklist you run yourself — not a subagent dispatch.

| Dimension | What to check |
|-----------|---------------|
| **Spec coverage** | Skim each section of the spec. Can you point to a task that implements every must-have requirement? List any gaps. |
| **Placeholder scan** | Search for the failure patterns above. Fix them inline. |
| **Type consistency** | Do types, signatures, and names in later tasks match earlier ones? `clearLayers()` in Task 3 vs `clearFullLayers()` in Task 7 is a bug. |
| **Test discipline** | Does every behavior-changing task have a failing-test step before the implementation step? |
| **Test-tier coverage** | Enumerate every CLAUDE.md tier-3 (or equivalent project-defined) trigger this plan touches — `main.rs`/entrypoint, CLI arg parsing, env-var resolution, terminal/pty/signal handling, real stdin/stdout piping, shell scripts whose contract is shell semantics, user-visible string literals whose stability is part of the contract. For each trigger, point at the tier-3 (or equivalent) test the plan adds, or mark the task incomplete. A bash credential-leak in a shell-script task is invisible to any in-process test; only a tier-3 test catches it. |
| **Spike candidates** | Re-read the Assumptions block and the spec's Key Decisions. For every claim of the form "tool X does Y" where neither this repo nor the team has a working example, is there a Task 0 spike? If not, add one or revise the spec. |
| **Parallel-implementation gate** | Does the plan add a second backend/platform/adapter behind an existing trait or interface? If yes, is there a final task that runs the canonical contract suite against BOTH implementations and asserts byte-identical observable behavior? If not, add it. |
| **Failure-propagation contracts** | For every task that introduces a new fallible operation (serialize/parse/convert/open/connect), does its behavior contract name the propagation policy? `.unwrap_or(<plausible fallback>)` without explicit contract rationale is a bug class — fix the contract. |
| **Per-task suite green** | Does every task's Step 4 specify both the single-test command AND the broader-scope suite command? Single-test-only passes hide cross-task regressions. |
| **Pattern application audit** | If any Pattern applies to many sites, is the final Audit task present (grep + production-config divergence enumeration + 3-site sample-verify)? |
| **Project conventions** | Does the plan respect the `CLAUDE.md` rules you read? (e.g., real-path test coverage, comment policy, commit format) |
| **Out-of-scope** | Did any task creep into something the spec marks Out of Scope? Remove it. |

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.

**Pass before presenting the draft:** Advance only when every item is honestly *yes* — not "feels fine."

## Optional: Dispatch a Reviewer Subagent

For long plans (>10 tasks), unfamiliar territory, or high-stakes work, dispatch a plan-document reviewer subagent. See `references/plan-reviewer.md` for the prompt template.

For short, familiar plans, the self-review is sufficient. Don't dispatch ritualistically — the human review step that follows catches most issues anyway.

## Draft Review

Before writing to disk, present the draft in chat for the user to review. The user can ask for changes or approve.

**What to present:**
- The full plan markdown (in a single buffer the user can read end-to-end)
- A short list of the assumptions you made (from the Assumption Audit)
- The list of files the plan will create or modify
- A pointer to the source spec

**Pass before considering the draft presentable:**
1. Self-review checklist is honestly *yes* across all dimensions
2. The draft text exists in the conversation as concrete prose — not a summary, not "here's a description of the plan"
3. Every test step contains real test code with exact assertions; every command step contains the exact command; every implementation step contains a concrete behavior contract (not vague verbs)

If the user requests changes, revise inline and present again. Do not write to disk during this loop.

## Writing the Plan

**Pass before creating or overwriting `plan.md`:** Do not write until both are true.

1. **User gate:** The user explicitly approved the draft **or** directed you to save/write the file. Vague enthusiasm alone is not approval — confirm if unclear.
2. **Path gate:** Target path is finalized — default `.beagle/concepts/<slug>/plan.md`, slug inherited from the spec's folder.

- **Default path:** `.beagle/concepts/<slug>/plan.md`
- **Slug source:** inherit from the spec's parent folder (the `<slug>` segment under `.beagle/concepts/`). User preferences override the default path.
- If the user explicitly asks to commit, use: `docs: add <slug> implementation plan`
- After writing, tell the user:
  > "Plan written to `<path>`. Review it on disk and let me know if you want changes, or hand it off to your executor."
- Then point the user at `beagle-core:subagent-prompt` for execution in a fresh session. That skill has `disable-model-invocation: true` and cannot be launched via a Skill tool call from here — instruct the user to invoke it themselves:
  > "Ready to execute? Run `/beagle-core:subagent-prompt` in a fresh session to hand this off to sub-agents."
- Wait for the next instruction before considering work complete.

## Execution Handoff

The plan is a handoff document, not an instruction to execute. After writing:

- Offer `beagle-core:subagent-prompt` (see the prompt above) so the user can execute the plan in a fresh session with a clean context window.
- If the project has another downstream executor skill or workflow, point the user at it as an alternative.
- Otherwise, tell the user the plan is ready and they can drive execution themselves task-by-task.

**Do not start executing.** This skill produces the plan; execution is a separate decision and (often) a separate skill with its own discipline.

## Key Principles

- **Spec is the contract** — never invent requirements the spec doesn't anchor
- **Bite-sized always** — 2-5 minute steps, never bundles
- **Tests are the contract; impls are the contract's satisfaction** — show real test assertions and call sites in test steps; show a behavior contract (files + 3-5 bullets + reference to analog) in implementation steps. The executor writes the code against the test, not against your guess.
- **TDD by default** — failing test before implementation, every time
- **One source of truth** — the spec defines WHAT; the plan defines HOW *at the contract level*; the executor defines HOW *at the code level*
- **Recoverability test** — delete anything the executor can recover by reading the referenced file; verbosity is not specificity
- **A contract is the minimum text that, if violated, makes the test fail** — anything beyond is speculation. Test bodies past ~15 lines, behavior contracts past 5 bullets, and "Reference:" blocks containing more than a function signature are all signals the plan is re-deriving the implementation
- **References point, they do not paste** — `file.ext:line-line` is the reference; inline code blocks under "Reference:" rot the moment the underlying code shifts
- **DRY repetition with Patterns** — when a transformation applies to N sites, name the pattern once; each task still owns its own files, test, and commit
- **Tests reuse existing scaffolding** — grep before inventing; new helpers in the plan need a named existing one that didn't fit
- **YAGNI for tests too** — pin the spec and named bug classes, not every conceivable edge case; speculative input-space exhaustion is overengineering
- **Sweep on the way out** — every task that modifies a file ends by removing orphaned comments, unused imports, dead params/fields/helpers in that file; describe the sweep targets in plain language, not line numbers — the executor greps
- **Surface assumptions** — bake them into the plan visibly, not silently into tasks; re-read the files the spec names rather than trusting the spec's characterization of them
- **Respect project conventions** — every project has its own test commands, commit conventions, comment policy, and test-tier rules; read `CLAUDE.md` (and equivalents like `CONTRIBUTING.md`, `AGENTS.md`) and let those shape the plan
- **The plan stands alone** — a downstream agent should be able to execute it without re-reading the spec

## When This Skill Is Wrong For the Job

This skill assumes:
- A spec exists (use `beagle-analysis:brainstorm-beagle` if not)
- The work is scoped to one cohesive system (decompose during brainstorming if not)
- The downstream executor is some kind of TDD-aware agent or engineer

If the work is a one-line fix, a refactor inside one file, or experimental spike work, a full plan is overkill — tell the user this skill is too heavy and suggest they just do the work directly.

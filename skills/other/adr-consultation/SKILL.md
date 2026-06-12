---
name: adr-consultation
description: "Multi-agent consultation for architecture decisions."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - Task
routing:
  triggers:
    - "consult on ADR"
    - "challenge this design"
    - "review before implementing"
    - "multi-agent consultation"
    - "architecture consultation"
    - "should we proceed"
    - "adr consultation"
  pairs_with:
    - feature-lifecycle
  complexity: Medium
  category: meta
---

# ADR Consultation Skill

Multi-agent architecture consultation that dispatches 3 specialized reviewers in parallel against an ADR and synthesizes their findings into a PROCEED or BLOCKED verdict. This is the gate between feature-lifecycle plan and implement phases for Medium+ decisions because challenging architecture decisions before implementation prevents costly post-implementation rework.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| Phase 2 DISPATCH: consultation agent prompt templates | `agent-prompts.md` | Loads detailed guidance from `agent-prompts.md`. |
| orchestration corrections: dispatch, artifact, and verdict aggregation fixes | `consultation-preferred-patterns.md` | Loads detailed guidance from `consultation-preferred-patterns.md`. |
| core consultation patterns and Phase 3 artifact templates | `consultation-patterns.md` | Loads detailed guidance from `consultation-patterns.md`. |
| errors, error handling | `error-handling.md` | Loads detailed guidance from `error-handling.md`. |

## Instructions

### Phase 1: DISCOVER

**Goal**: Identify the ADR and prepare the consultation directory.

**Step 1: Locate the ADR**

Check for ADR path in this order:
1. User-provided path (e.g., `adr/intent-based-routing.md`)
2. Active session context from adr-system hook (`.adr-session.json`)
3. Ask the user which ADR to consult on

Do not guess which ADR to consult on because an incorrect guess wastes a full consultation cycle.

```bash
cat .adr-session.json 2>/dev/null
ls adr/*.md
```

Even if this ADR was discussed informally, run the formal consultation because undocumented discussion produces no persistent artifacts and cannot be referenced by future sessions.

**Step 2: Check for prior consultation**

Before dispatching, scan `adr/{adr-name}/` for existing agent files because silently overwriting prior consultation work destroys the audit trail.

```bash
ls adr/{adr-name}/ 2>/dev/null
```

If existing files are found, report them and their timestamps. Ask the user whether to overwrite (re-run consultation) or use existing results.

**Step 3: Read the ADR**

Read the full ADR content. Extract: the decision being made, key components/changes proposed, any stated risks or consequences, and the ADR name (filename without `.md`) for the consultation directory.

**Step 4: Create consultation directory**

```bash
mkdir -p adr/{adr-name}
```

**Gate**: ADR content has been read, the consultation directory has been created, and the ADR name has been confirmed. Dispatch agents only after this gate passes.

---

### Phase 2: DISPATCH

**Goal**: Launch all consultation agents in a single message for true parallel execution.

All three Task calls MUST appear in ONE response because sequential dispatch triples wall-clock time with no cross-perspective benefit. The value of this skill is simultaneous independent judgment.

Dispatch all 3 agents even if the ADR "seems simple" because partial consultation gives false confidence. Let agents report "no concerns" if genuinely clean.

Even when there is time pressure, do not skip consultation because blocking concerns discovered post-implementation cost dramatically more to fix.

**Standard mode (3 agents)**: Always dispatch all three. See `references/agent-prompts.md` for the full prompt template for each agent.

**Complex mode (5 agents)**: For Complex decisions (new subsystem, major API change), add `reviewer-system` and a second domain expert. Enable with "complex consultation" or "full consultation". See `references/agent-prompts.md` § Complex Mode.

Each agent receives:
1. The full ADR content as context
2. Its specific lens and analysis focus
3. Explicit output path: `adr/{adr-name}/{agent-name}.md`
4. The structured output format from `references/agent-prompts.md`

**Gate**: All Task calls dispatched in a single message. Proceed to Phase 3 only when all agents have returned and written their files to `adr/{adr-name}/`.

---

### Phase 3: SYNTHESIZE

**Goal**: Read all agent responses from the consultation directory and produce a synthesis.

**Step 1: Read all agent responses from files**

Read the response files from disk, not from Task return context, because files persist across sessions while context does not -- synthesis from context is not reproducible.

```bash
cat adr/{adr-name}/reviewer-perspectives-contrarian.md
cat adr/{adr-name}/reviewer-perspectives-user-advocate.md
cat adr/{adr-name}/reviewer-perspectives-meta-process.md
```

**Step 2: Extract all concerns**

Track every concern raised by any agent in `adr/{adr-name}/concerns.md`. See `references/consultation-patterns.md` § Phase 3 Artifact Templates for the concerns.md format. Structured tracking prevents concerns from being lost during synthesis.

**Step 3: Identify verdict agreement**

Do not treat NEEDS_CHANGES as equivalent to PROCEED. Multiple NEEDS_CHANGES aggregates to a higher concern level, not a softer approval.

| Pattern | Meaning |
|---------|---------|
| All 3 PROCEED | Strong consensus -- proceed with confidence |
| 2 PROCEED, 1 NEEDS_CHANGES | Soft consensus -- address changes, then proceed |
| Any BLOCK | Hard block -- must resolve before proceeding |
| Mixed NEEDS_CHANGES | Significant concerns -- address before proceeding |

The synthesizer can also identify cross-cutting concerns that individual agents missed. Document any orchestrator-level concern in concerns.md and factor it into the verdict.

**Step 4: Write synthesis**

Write `adr/{adr-name}/synthesis.md` using the template from `references/consultation-patterns.md` § Phase 3 Artifact Templates.

**Gate**: All concerns extracted to concerns.md, synthesis.md written. Proceed to Phase 4 only when both files exist in `adr/{adr-name}/`.

---

### Phase 4: GATE

**Goal**: Issue a final PROCEED or BLOCKED verdict and communicate it clearly.

**Step 1: Check for blocking concerns**

Read `adr/{adr-name}/concerns.md`. If any concern has `**Severity**: blocking`, the verdict is BLOCKED. This is a hard gate, not advisory.

Do not rationalize blocking concerns as "theoretical" because theoretical risk is still risk, and the gate exists specifically to prevent implementation from proceeding with unresolved blocking issues.

**Step 2: Issue verdict**

Use the BLOCKED or PROCEED verdict display format from `references/consultation-patterns.md` § Phase 4 Verdict Display.

**Gate**: Verdict issued, artifacts confirmed written to disk. Consultation is complete.

---

### Phase 5: LIFECYCLE (optional -- run when consultation is no longer needed)

**Goal**: Clean up consultation artifacts after an ADR's implementation is complete and merged.

1. **Keep**: `adr/{name}/synthesis.md` (permanent record of verdict)
2. **Keep**: `adr/{name}/concerns.md` (permanent record of concerns + resolutions)
3. **Delete**: `adr/{name}/reviewer-*.md` (agent responses -- value extracted into synthesis)
4. **Update**: ADR status to reflect implementation completion

```bash
rm adr/{name}/reviewer-*.md
ls adr/{name}/synthesis.md adr/{name}/concerns.md
```

The consultation directory is auto-created by Phase 1 (`mkdir -p adr/{adr-name}`). No `.gitkeep` is needed because the `adr/` directory is gitignored.

---

## Error Handling

> See `references/error-handling.md` for full error recovery procedures.

| Error | Quick Resolution |
|-------|-----------------|
| No ADR found / ADR path unclear | `ls adr/*.md`, ask user to specify |
| Agent times out or fails to write file | Re-run failed agents individually; do not synthesize until all 3 files exist |
| All agents PROCEED but synthesizer detects deeper issue | Document as orchestrator-level concern in concerns.md; factor into verdict |
| Consultation directory already exists with prior agent files | Report timestamps; ask user whether to overwrite or use existing results |

---

## Reference Loading

| Signal | Load |
|--------|------|
| Dispatching agents, structuring Task calls | `references/agent-prompts.md` |
| Complex mode (5-agent) dispatch | `references/agent-prompts.md` |
| Synthesizing verdicts, aggregating PROCEED/BLOCK/NEEDS_CHANGES | `references/consultation-patterns.md` |
| Classifying concern severity, writing concerns.md or synthesis.md | `references/consultation-patterns.md` |
| Issuing BLOCKED or PROCEED verdict display | `references/consultation-patterns.md` |
| Agent file missing, consultation incomplete, prior work overwritten | `references/consultation-preferred-patterns.md` |
| Rationalizing a blocking concern, treating NEEDS_CHANGES as PROCEED | `references/consultation-preferred-patterns.md` |
| Agent times out, empty file, output written to wrong path | `references/error-handling.md` |
| concerns.md has blocking severity but synthesis says PROCEED | `references/error-handling.md` |

## References

- [ADR: Multi-Agent Consultation](../../adr/multi-agent-consultation.md) -- The architecture decision this skill implements
- [parallel-code-review](../parallel-code-review/SKILL.md) -- Fan-out/fan-in pattern this skill adapts
- [reviewer-perspectives](../../agents/reviewer-perspectives.md) -- Perspectives agent (contrarian, user-advocate, meta-process lenses)
- `references/agent-prompts.md` -- Full prompt templates for all 3 standard agents + complex mode
- `references/consultation-patterns.md` -- Correct patterns, artifact templates, verdict display formats
- `references/consultation-preferred-patterns.md` -- Failure modes with detection commands
- `references/error-handling.md` -- Error recovery by phase

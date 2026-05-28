---
name: fact-checking
description: >
  Use when reviewing code changes, auditing documentation accuracy, validating
  technical claims before merge, or user says "verify claims", "factcheck",
  "audit documentation", "validate comments", "are these claims accurate".
---

## Invariant Principles

1. **Claims are hypotheses** - Every claim requires empirical evidence before verdict
2. **Evidence before verdict** - No verdict without traceable, citable proof
3. **User controls scope** - User selects scope and approves all fixes
4. **Deduplicate findings** - Check AgentDB before verifying to avoid redundant work
5. **Learn from trajectories** - Store verification trajectories in ReasoningBank for improvement

<ROLE>
Scientific Skeptic + ISO 9001 Auditor. Claims are hypotheses. Verdicts require data.
Professional reputation depends on evidence-backed conclusions.
</ROLE>

<analysis>
Before ANY action:
- Current phase? (config/scope/extract/triage/verify/report)
- What EXACTLY is claimed?
- What proves TRUE? What proves FALSE?
- AgentDB checked for existing findings?
- Appropriate verification depth?
</analysis>

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `scope` | Yes | Target for fact-checking: branch changes, uncommitted files, or full repo |
| `modes` | No | Enabled modes: Missing Facts, Extraneous Info, Clarity Mode (default: all) |
| `autonomous` | No | If true, skip interactive prompts and use defaults |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `verification_report` | Inline | Summary, findings by category, bibliography |
| `implementation_plan` | Inline | Proposed fixes for refuted/stale claims |
| `glossary` | Inline | Key facts extracted (Clarity Mode only) |
| `state_checkpoint` | File | `.fact-checking/state.json` for interruption recovery |

## Workflow

### Phase 0: Configuration

Present modes (default: all enabled):
- **Missing Facts Detection**: gaps where claims lack critical context
- **Extraneous Info Detection**: redundant/LLM-style over-commenting
- **Clarity Mode**: generate glossaries for AI config files

Autonomous mode detected ("Mode: AUTONOMOUS")? Enable all automatically.

### Phase 1: Scope Selection

<RULE>Ask scope BEFORE extraction. No exceptions.</RULE>

| Option | Method |
|--------|--------|
| Branch changes | `git diff $(git merge-base HEAD main)...HEAD --name-only` |
| Uncommitted | `git diff --name-only` + `git diff --cached --name-only` |
| Full repo | All code/doc patterns |

### Phase 2: Claim Extraction

**Sources**: Comments (`//`, `#`, `/* */`), docstrings, markdown, commits, PR descriptions, naming (`validateX`, `safeX`, `ensureX`)

**Categories**:
| Category | Examples | Agent |
|----------|----------|-------|
| Technical | "O(n log n)", "matches RFC" | CorrectnessAgent |
| Security | "sanitized", "XSS-safe", "bcrypt" | SecurityAgent |
| Concurrency | "thread-safe", "atomic", "lock-free" | ConcurrencyAgent |
| Performance | "O(n)", "cached 5m", "lazy-loaded" | PerformanceAgent |
| Configuration | "defaults to 30s", "env var X" | ConfigurationAgent |
| Historical | "workaround for bug", "fixes #123" | HistoricalAgent |
| Documentation | URLs, examples, test coverage claims | DocumentationAgent |

Also flag: Ambiguous, Misleading, Jargon-heavy

### Phase 3: Triage

<RULE>Present ALL claims upfront. User must see full scope before verification.</RULE>

Display grouped by category with depth recommendations:
- **Shallow**: read code, reason about behavior
- **Medium**: trace execution paths, analyze control flow
- **Deep**: execute tests, run benchmarks, instrument code

ARH pattern for responses:
- DIRECT_ANSWER: accept adjustments, proceed
- RESEARCH_REQUEST: dispatch analysis subagent
- UNKNOWN: analyze complexity, regenerate recommendations
- SKIP: use defaults

### Phase 4: Parallel Verification

<RULE>Check AgentDB BEFORE verifying. Store findings AFTER.</RULE>

```typescript
// Before: check existing
const existing = await agentdb.retrieveWithReasoning(embedding, {
  domain: 'fact-checking-findings', k: 3, threshold: 0.92
});

// After: store finding
await agentdb.insertPattern({
  type: 'verification-finding',
  domain: 'fact-checking-findings',
  pattern_data: { claim, location, verdict, evidence, sources }
});
```

Spawn category agents via swarm-orchestration (hierarchical topology).

### Phase 5: Verdicts

<RULE>Every verdict MUST have concrete evidence. NO exceptions.</RULE>

| Verdict | Evidence Required |
|---------|-------------------|
| Verified | test output, code trace, docs, benchmark |
| Refuted | failing test, contradicting code |
| Incomplete | base verified + missing elements |
| Inconclusive | document attempts and why insufficient |
| Stale | when true, what changed, current state |
| Extraneous | value analysis shows no added info |

### Phase 6: Report

Sections: Header, Summary, Findings by Category, Bibliography, Implementation Plan

**Bibliography formats**:
- Code trace: `file:lines - finding`
- Test: `command - result`
- Web: `Title - URL - "excerpt"`
- Git: `commit/issue - finding`

### Phase 6.5: Clarity Mode (if enabled)

Generate glossaries/key facts from verified claims. Update AI config files (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`).

### Phase 7: Learning

Store trajectories in ReasoningBank:
```typescript
await reasoningBank.insertPattern({
  type: 'verification-trajectory',
  pattern: { claimText, depthUsed, verdict, timeSpent, evidenceQuality }
});
```

### Phase 8: Fixes

<RULE>NEVER apply fixes without explicit per-fix user approval.</RULE>

Present plan, get approval per fix, apply, offer re-verification.

## Interruption

Checkpoint to `.fact-checking/state.json` after each claim. Offer resume on next invocation.

<FORBIDDEN>
- Verdict without concrete evidence
- Skipping claims as "trivial"
- Batching similar claims without individual verification
- Auto-correcting without approval
- Verifying without AgentDB check
</FORBIDDEN>

<reflection>
Before finalizing:
- Did I run config wizard?
- Did I ask scope first?
- Did I present ALL claims for triage?
- Does each verdict have CONCRETE evidence?
- Did I check/update AgentDB?
- Does every verdict cite sources?
- Did I store trajectories?
- Am I awaiting approval before fixes?

If NO to ANY: STOP and fix.
</reflection>

## Self-Check

Before completing:
- [ ] Configuration wizard completed (or autonomous mode active)
- [ ] Scope explicitly selected by user
- [ ] ALL claims presented for triage before verification
- [ ] Each verdict has concrete, citable evidence
- [ ] AgentDB checked before verification, updated after
- [ ] Bibliography includes sources for all verdicts
- [ ] Trajectories stored in ReasoningBank
- [ ] Fixes await explicit per-fix user approval

If ANY unchecked: STOP and fix.

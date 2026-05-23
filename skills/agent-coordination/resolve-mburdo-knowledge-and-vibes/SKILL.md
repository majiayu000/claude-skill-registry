---
name: resolve
description: Resolve disagreements between agents or approaches using test-based adjudication. Use when agents disagree, when multiple valid approaches exist, when the user asks "which approach", or when making architectural decisions with tradeoffs.
---

# Resolve — Test-Based Adjudication

Test-based adjudication for multi-agent or multi-approach disagreements.

> **Design rationale:** This skill uses the orchestrator-subagent pattern because test-based adjudication involves substantial cognitive work: position gathering, discriminating test design, test execution, and evidence-based adjudication. Each phase benefits from fresh context to prevent anchoring bias. See `docs/guides/ORCHESTRATOR_SUBAGENT_PATTERN.md`.

## When This Applies

| Signal | Action |
|--------|--------|
| Multiple agents disagree | Run full protocol |
| Multiple valid approaches | Run full protocol |
| User asks "which approach" | Run full protocol |
| Architectural decision needed | Run full protocol |
| User says "/resolve" | Run full protocol |

---

## Philosophy

> "Tests are the medium of disagreement, not rhetoric." — DebateCoder

**Research backing:**
- `research/003-debate-or-vote.md`: Voting beats extended debate
- `research/041-debatecoder.md`: Tests adjudicate better than arguments
- `research/042-rankef.md`: Selection beats unguided reasoning

**Key principles:**
- Tests decide, not rhetoric
- Max 2 discussion rounds without tests
- Preserve dissent for user decision when tests don't discriminate
- No compromise—evidence picks winner

---

## Tool Reference

### File Operations
| Tool | Purpose |
|------|---------|
| `Read(context_paths)` | Read relevant code/docs |
| `Write(file_path, content)` | Write position/test reports |
| `Grep(pattern)` | Search codebase for patterns |

### Testing
| Command | Purpose |
|---------|---------|
| `pytest tests/...` | Run discriminating tests |
| `npm test` | Run JS/TS tests |

### Discriminating Tests
A discriminating test is one where:
- Position A passes, Position B fails (or vice versa)
- It directly tests the contested claim
- Result is observable and repeatable

### Decision Outcomes
| Outcome | When | Action |
|---------|------|--------|
| Clear winner | Tests discriminate (2-1 or better) | Document decision |
| No winner | Tests don't discriminate | Preserve dissent, ask user |
| Value tradeoff | Equal test results | Present options to user |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      RESOLVE ORCHESTRATOR                        │
│  - Creates session: sessions/resolve-{timestamp}/                │
│  - Manages TodoWrite state                                       │
│  - Spawns subagents with isolated context (prevents anchoring)   │
│  - Passes test results, not arguments, between phases            │
└─────────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│    Positions    │  │  Test Generate  │  │  Test Execute   │
│  agents/        │  │  agents/        │  │  agents/        │
│  positions.md   │  │  tests.md       │  │  execute.md     │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
    01_positions.md      02_tests.md         03_results.md
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   Adjudicate    │ → Decision or user choice
                    │  agents/        │
                    │  adjudicate.md  │
                    └────────┬────────┘
                             │
                        04_decision.md
```

## Subagents

| Phase | Agent | Input | Output |
|-------|-------|-------|--------|
| 1 | `agents/positions.md` | question, context | positions A, B, C... |
| 2 | `agents/tests.md` | positions | discriminating tests |
| 3 | `agents/execute.md` | tests, positions | test results matrix |
| 4 | `agents/adjudicate.md` | results | decision or preserved dissent |

---

## Execution Flow

### 1. Setup (Orchestrator)

```markdown
1. Create session directory:
   mkdir -p sessions/resolve-{timestamp}

2. Initialize TodoWrite with phases:
   - [ ] Phase 1: Gather Positions
   - [ ] Phase 2: Generate Discriminating Tests
   - [ ] Phase 3: Execute Tests
   - [ ] Phase 4: Adjudicate

3. Gather inputs:
   - question: What is being decided?
   - context: Relevant code/docs
   - participants: Agents or approaches involved
```

### 2. Phase 1: Gather Positions

**Spawn:** `agents/positions.md`

**Input:**
```json
{
  "session_dir": "sessions/resolve-{timestamp}",
  "question": "Should we use JWT or session tokens for auth?",
  "context_paths": ["src/auth/**", "PLAN/requirements.md"]
}
```

**Output:**
```json
{
  "report_path": "sessions/.../01_positions.md",
  "positions": [
    {"id": "A", "approach": "JWT tokens", "rationale": "Stateless, scalable"},
    {"id": "B", "approach": "Session tokens", "rationale": "Revocable, simpler"}
  ]
}
```

### 3. Phase 2: Generate Discriminating Tests

**Spawn:** `agents/tests.md`

**Input:**
```json
{
  "session_dir": "sessions/resolve-{timestamp}",
  "positions_path": "<from Phase 1>"
}
```

**Output:**
```json
{
  "report_path": "sessions/.../02_tests.md",
  "tests": [
    {"id": "T1", "name": "test_immediate_revocation", "discriminates": "A fails, B passes"},
    {"id": "T2", "name": "test_horizontal_scaling", "discriminates": "A passes, B fails"},
    {"id": "T3", "name": "test_offline_validation", "discriminates": "A passes, B fails"}
  ]
}
```

### 4. Phase 3: Execute Tests

**Spawn:** `agents/execute.md`

**Input:**
```json
{
  "session_dir": "sessions/resolve-{timestamp}",
  "tests_path": "<from Phase 2>",
  "positions_path": "<from Phase 1>"
}
```

**Output:**
```json
{
  "report_path": "sessions/.../03_results.md",
  "results_matrix": {
    "T1": {"A": "FAIL", "B": "PASS"},
    "T2": {"A": "PASS", "B": "FAIL"},
    "T3": {"A": "PASS", "B": "FAIL"}
  },
  "a_wins": 2,
  "b_wins": 1
}
```

### 5. Phase 4: Adjudicate

**Spawn:** `agents/adjudicate.md`

**Input:**
```json
{
  "session_dir": "sessions/resolve-{timestamp}",
  "results_path": "<from Phase 3>",
  "positions_path": "<from Phase 1>"
}
```

**Output:**
```json
{
  "report_path": "sessions/.../04_decision.md",
  "winner": "A",
  "confidence": "HIGH",
  "rationale": "JWT wins 2-1 on discriminating tests",
  "preserved_dissent": "Revocation concern valid—consider short expiry",
  "user_decision_needed": false
}
```

### 6. Finalize (Orchestrator)

1. Update TodoWrite (all phases complete)
2. If clear winner: present decision with evidence
3. If no winner: present both positions for user decision
4. Record decision in ADR if architectural

---

## When Tests Don't Discriminate

If tests pass/fail equally for all positions:

```json
{
  "winner": null,
  "confidence": "LOW",
  "rationale": "Tests don't discriminate—this is a value tradeoff",
  "preserved_dissent": [
    {"position": "A", "for": "Scalability priority"},
    {"position": "B", "for": "Simplicity priority"}
  ],
  "user_decision_needed": true,
  "question_for_user": "Do you prioritize horizontal scaling or immediate revocation?"
}
```

---

## Anti-Patterns

| Don't | Why |
|-------|-----|
| Extended rhetorical debate | Research shows it degrades outcomes |
| Compromise positions | Evidence picks winner, no averaging |
| Skip test generation | Rhetoric without tests is noise |
| Force consensus | Preserve dissent for user |
| More than 2 rounds without tests | Escalate to user instead |

---

## See Also

- `agents/` — Subagent definitions
- `docs/guides/ORCHESTRATOR_SUBAGENT_PATTERN.md` — Pattern documentation
- `research/041-debatecoder.md` — Test-based adjudication research
- `research/003-debate-or-vote.md` — Why debate degrades

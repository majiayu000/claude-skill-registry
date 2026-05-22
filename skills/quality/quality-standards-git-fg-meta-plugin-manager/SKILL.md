---
name: quality-standards
description: "Unified quality assurance skill: enforce evidence-based completion claims through 6-phase gates and three-way audits. Use when claiming completion, committing code, or validating components. Not for skipping verification or assuming correctness."
auto_load_mapping:
  - If path contains ".mcp.json" -> load mcp-development
  - If path contains ".claude/skills" -> load invocable-development
  - If path contains ".claude/agents" -> load agent-development
  - If path contains ".claude/commands" -> load invocable-development
  - If path contains "SKILL.md" -> load invocable-development
---

<mission_control>
<objective>Ensure all completion claims have fresh verification evidence through systematic quality gates and three-way audits</objective>
<success_criteria>All claims backed by fresh verification output; all 6 gates pass sequentially</success_criteria>
<iron_law>
**NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE**

If you haven't run the verification command in this message, you cannot claim it passes. This is non-negotiable.
</iron_law>
</mission_control>

# Quality Standards

## The 6-Phase Gate System

| Phase | Gate         | What It Checks                      | Command Pattern                                             | Evidence Required |
| ----- | ------------ | ----------------------------------- | ----------------------------------------------------------- | ----------------- | ---- | ---------- |
| 1     | **BUILD**    | Compilation succeeds, deps resolved | `npm run build`, `cargo build`, `pnpm build`, `mvn compile` | Exit code 0       |
| 2     | **TYPE**     | Type safety, no type errors         | `tsc --noEmit`, `pyright`, `go vet`, `mypy`                 | 0 type errors     |
| 3     | **LINT**     | Code style, anti-patterns           | `eslint`, `pylint`, `cargo clippy`, `flake8`                | 0 errors/warnings |
| 4     | **TEST**     | Tests pass, 80%+ coverage           | `npm test`, `pytest --cov`, `cargo test --coverage`         | All pass, ≥80%    |
| 5     | **SECURITY** | No secrets, console.logs, vulns     | Grep diff + `npm audit`, `pip-audit`                        | 0 issues          |
| 6     | **DIFF**     | Intentional changes, no TODOs       | Grep git diff for `TODO                                     | FIXME             | // ` | Clean diff |

## The Gate Function

BEFORE claiming any status or expressing satisfaction:

1. **IDENTIFY**: What command proves this claim?
2. **RUN**: Execute the FULL command (fresh, complete)
3. **READ**: Full output, check exit code, count failures
4. **VERIFY**: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. **ONLY THEN**: Make the claim

Skip any step = lying, not verifying.

## Component Validation Checklist

| Gate                       | Check                                           | Evidence                 |
| -------------------------- | ----------------------------------------------- | ------------------------ |
| **Structure**              | YAML frontmatter valid, naming conventions      | File reads confirm       |
| **Progressive Disclosure** | Tier 1 metadata, Tier 2 main, Tier 3 references | Structure verified       |
| **Portability**            | Zero external dependencies                      | Component self-contained |
| **Content Quality**        | Trigger phrases, imperative voice, expert-only  | Quality gate passed      |
| **Tests**                  | Behavior verified, edge cases covered           | Test output: 100% pass   |

## Three-Way Review Pattern

| Dimension     | Question                                 |
| ------------- | ---------------------------------------- |
| **Request**   | What did the user explicitly ask for?    |
| **Delivery**  | What was actually implemented?           |
| **Standards** | What do meta-development skills specify? |

Identify gaps: Intent misalignment, standards violations, completeness issues.

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!")
- About to commit/push without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"

## Rationalization Prevention

| Stop Thinking             | Do Instead             |
| ------------------------- | ---------------------- |
| "Should work now"         | RUN the verification   |
| "I'm confident"           | Confidence ≠ evidence  |
| "Linter passed"           | Linter ≠ compiler      |
| "Agent said success"      | Verify independently   |
| "Partial check is enough" | Partial proves nothing |

## Sequential Enforcement

Gates pass **in order**. If a gate fails:

1. Stop verification immediately
2. Report failure with details
3. Do not run subsequent gates
4. Provide actionable error messages

## When To Apply

**ALWAYS before:**

- ANY success/completion claims
- ANY expression of satisfaction
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

## References

| For...                                 | See...                              |
| -------------------------------------- | ----------------------------------- |
| Detailed gate commands by project type | `references/gates.md`               |
| Three-way audit investigation phases   | `references/audit-patterns.md`      |
| Per-component structure checks         | `references/component-checklist.md` |

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming

---

<critical_constraint>
MANDATORY: Gates pass in sequence—stop on first failure
MANDATORY: Each claim requires fresh verification output
MANDATORY: Compare Request vs Delivery vs Standards in audits
MANDATORY: No completion claims without fresh evidence
MANDATORY: Show evidence (output) for every gate check
No exceptions. Quality gates exist to prevent substandard work and completion hallucinations.
</critical_constraint>

---

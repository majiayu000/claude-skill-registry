---
name: verification-mastery
description: Evidence before claims, always. No completion claims without fresh verification. The final gate before declaring success.
---
<domain_overview>
# ✅ VERIFICATION MASTERY: EVIDENCE BEFORE CLAIMS
> **Philosophy:** Claiming work is complete without verification is dishonesty, not efficiency. Evidence before claims, always.
**EVIDENCE INTEGRITY MANDATE (CRITICAL):** Never claim a task is complete based on assumption or past memory. You MUST generate fresh evidence (logs, screenshots, test output) for every claim. AI-generated success reports are untrustworthy without proof. Any completion signal sent without accompanying verification artifacts must be rejected as "Hallucinated Success".
---
## 🚨 THE IRON LAW
```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```
If you haven't run the verification command **in this message**, you cannot claim it passes.
**Violating the letter of this rule is violating the spirit of this rule.**
</domain_overview>
<core_workflow>
## 🚪 THE GATE FUNCTION
```
BEFORE claiming any status or expressing satisfaction:
1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim
Skip any step = lying, not verifying
```
</core_workflow>
<quality_standards>
## 📋 COMMON CLAIMS AND REQUIREMENTS

| Claim | Requires | NOT Sufficient |
|-------|----------|----------------|
| "Tests pass" | Test command output: 0 failures | Previous run, "should pass" |
| "Linter clean" | Linter output: 0 errors | Partial check, extrapolation |
| "Build succeeds" | Build command: exit 0 | Linter passing, logs look good |
| "Bug fixed" | Test original symptom: passes | Code changed, assumed fixed |
| "Regression test works" | Red-green cycle verified | Test passes once |
| "Agent completed" | VCS diff shows changes | Agent reports "success" |
| "Requirements met" | Line-by-line checklist | Tests passing |
| "No errors" | Command output reviewed | "I think it's fine" |
---
<red_flags>
## 🚨 RED FLAGS - STOP IMMEDIATELY
If you catch yourself:
- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!")
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**
**ALL of these require: STOP. Run verification. THEN speak.**
---
## 🚫 RATIONALIZATION PREVENTION

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |
| "It worked before" | Run it NOW |
| "Too slow to run again" | Slow verification > fast lies |
</red_flags>
---
##  KEY PATTERNS
### Tests
```
✅ CORRECT:
[Run: npm test]
[Output: 34/34 passing]
"All 34 tests pass."
❌ WRONG:
"Should pass now"
"Looks correct"
"Tests are green" (without running)
```
### Regression Tests (TDD Red-Green)
```
✅ CORRECT:
1. Write test → Run (MUST PASS initial state or FAIL for right reason)
2. Break the code → Run (MUST FAIL)
3. Fix → Run (MUST PASS)
❌ WRONG:
"I've written a regression test"
(without red-green verification)
```
### Build
```
✅ CORRECT:
[Run: npm run build]
[Output: Compiled successfully]
"Build passes."
❌ WRONG:
"Linter passed, so build should work"
(linter doesn't check compilation)
```
### Requirements
```
✅ CORRECT:
1. Re-read plan/requirements
2. Create explicit checklist
3. Verify EACH item with evidence
4. Report gaps or confirm completion
❌ WRONG:
"Tests pass, phase complete"
(tests ≠ requirements)
```
### Agent Delegation
```
✅ CORRECT:
1. Agent reports success
2. Check VCS diff (git diff, git status)
3. Verify changes are what was requested
4. Report actual state
❌ WRONG:
Trust agent report without verification
```
</quality_standards>
<integration_and_tooling>
## 🔗 RALPH WIGGUM INTEGRATION
When Ralph Wiggum is active, verification gates are MANDATORY at each iteration:
1. **Before claiming iteration complete:**
   - Run all relevant tests
   - Run build if applicable
   - Run linter if applicable
   - Provide evidence in output
2. **Quality Gate Check:**
   - Proactive Gate verified?
   - Reflection Loop completed?
   - Verification Matrix updated?
3. **Completion Signal:**
   - Only create `.maestro/ralph.complete` AFTER full verification
   - Include verification evidence in final summary
---
## 📊 VERIFICATION COMMANDS REFERENCE

### JavaScript/TypeScript
```bash
# Tests
npm test
npm run test -- --coverage
# Build
npm run build
# Lint
npm run lint
npx eslint . --ext .ts,.tsx
# Type check
npx tsc --noEmit
```
### Python
```bash
# Tests
pytest
pytest --cov=src
# Lint
ruff check .
flake8 .
# Type check
mypy src/
```
### General
```bash
# Git status (uncommitted changes)
git status
# Git diff (what changed)
git diff
# Process exit code (last command)
echo $?  # Unix
$LASTEXITCODE  # PowerShell
```
</integration_and_tooling>
<reference_and_audit>
## ⏱️ WHEN TO APPLY
**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents
- Creating completion signals
**Rule applies to:**
- Exact phrases ("Tests pass")
- Paraphrases ("Everything is green")
- Synonyms ("All good")
- Implications ("Ready for review")
- ANY communication suggesting completion/correctness
---
## 💡 WHY THIS MATTERS
From failure analysis:
- "I don't believe you" - trust broken with user
- Undefined functions shipped - would crash in production
- Missing requirements shipped - incomplete features
- Time wasted: false completion → redirect → rework
**Core principle:** Honesty is non-negotiable. Unverified claims are lies.
---
## 🏁 THE BOTTOM LINE
**No shortcuts for verification.**
Run the command. Read the output. THEN claim the result.
This is non-negotiable.
---
## 🔗 RELATED SKILLS
- **@tdd-mastery** - Verification through failing tests first
- **@debug-mastery** - Verify fix actually worked
- **@clean-code** - Quality standards to verify against
</reference_and_audit>


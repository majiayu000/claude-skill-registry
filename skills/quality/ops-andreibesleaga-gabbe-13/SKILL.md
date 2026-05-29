---
name: tech-debt
description: Identify, document, score, and prioritize technical debt into an actionable backlog
triggers: [tech debt, code smell, TODO, FIXME, legacy, refactor backlog, quality decay, debt]
context_cost: medium
---

# Tech Debt Skill

## Goal
Surface, document, and prioritize technical debt so it can be systematically planned and repaid. Produce an Impact×Effort prioritized backlog using TECH_DEBT_TEMPLATE.md.

## Steps

1. **Scan for explicit debt markers**
   ```bash
   # Find all TODO, FIXME, HACK, XXX markers
   grep -rn "TODO\|FIXME\|HACK\|XXX\|@deprecated\|@todo" src/ --include="*.ts" --include="*.php" --include="*.py"
   ```
   For each marker: note file:line, understand context, assign Impact and Effort scores.

2. **Run complexity analysis**
   ```bash
   # JavaScript/TypeScript
   npx complexity-report --format json src/ > complexity-report.json
   # Look for: functions with cyclomatic complexity > 10

   # PHP
   vendor/bin/phpmd app/ text codesize,complexity
   
   # Python
   radon cc src/ -a -s  # Cyclomatic complexity
   xenon --max-absolute B --max-modules A --max-average A src/
   # Look for: NPathComplexity > 200, CyclomaticComplexity > 10

   # SonarQube (if configured)
   sonar-scanner
   # Look for: cognitive complexity, code smells
   ```

3. **Check code duplication**
   ```bash
   # JavaScript/TypeScript
   npx jscpd src/ --min-lines 5 --min-tokens 50

   # PHP
   vendor/bin/phpcpd app/

   # Flag: any duplication > 3 occurrences → candidate for extraction
   ```

4. **Check test coverage gaps**
   ```bash
   [test coverage command]
   # Flag files with < 60% line coverage as test debt
   ```

5. **Identify structural debt patterns**

   **God objects** (too many responsibilities):
   - Classes > 500 lines or > 20 public methods
   - Files that import from > 15 other files (high fan-in = too many dependencies)

   **Fat Controllers** (business logic in wrong layer):
   - Controllers with > 50 lines of business logic
   - Bypass of use-case/service layer

   **Missing abstractions**:
   - Repeated patterns without an abstraction (violates DRY after 3rd occurrence)
   - Hardcoded config values that should be constants or env vars

   **Stale dependencies**:
   ```bash
   npm outdated     # Node.js — shows current vs wanted vs latest
   composer outdated # PHP
   pip list --outdated # Python
   ```

6. **Score each debt item** using Impact×Effort matrix

   ```
   Impact (how much does this hurt development?):
   H = blocks development, causes bugs, creates security risk
   M = slows development, increases maintenance burden
   L = minor annoyance, cosmetic

   Effort (how long to fix?):
   H = days or weeks of work
   M = hours of focused work
   L = < 1 hour

   Priority matrix:
   High Impact + Low Effort  = P1 (do immediately)
   High Impact + High Effort = P2 (plan for next sprint)
   Low Impact + Low Effort   = P3 (good for juniors/onboarding)
   Low Impact + High Effort  = P4 (deprioritize or skip)
   ```

7. **Fill TECH_DEBT_TEMPLATE.md** for each debt item

8. **Produce prioritized backlog**
   ```markdown
   ## Tech Debt Backlog — [Date]

   ### P1 — High Impact, Low Effort (do now)
   - TD-001: Extract UserValidator from UserController (2h effort, removes security bug risk)

   ### P2 — High Impact, High Effort (plan next sprint)
   - TD-002: Refactor OrderService God class (3 days, blocks all new order features)

   ### P3 — Low Impact, Low Effort (good first issues)
   - TD-003: Replace magic numbers in pricing module with named constants (30min)

   ### P4 — Deprioritize
   - TD-004: Rename legacy variable names in archived report module (low business value)
   ```

9. **Add P1 and P2 items to project/tasks.md**
   - Create atomic tasks (15-min rule) for each debt item
   - Link to TECH_DEBT_TEMPLATE.md entry

## Constraints
- Never fix tech debt in the same commit as a feature or bug fix
- Refactoring must be accompanied by passing tests (test guard)
- Tech debt items must be tracked — don't fix and forget (update TECH_DEBT_TEMPLATE)
- Always measure complexity BEFORE and AFTER to verify improvement

## Output Format
Filled TECH_DEBT_TEMPLATE.md entries + prioritized backlog. Report: "Found [N] debt items. P1: [N], P2: [N], P3: [N], P4: [N]."

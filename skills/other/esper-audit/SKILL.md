---
name: esper:audit
description: Comprehensive project audit — health, architecture, phase retrospective, and codebase quality. Produces a scannable report with actionable recommendations.
---

You are performing a comprehensive project audit.

The user's initial prompt (if any): $ARGUMENTS

## Step 1: Check setup

Run `esperkit config check`. If it exits non-zero, tell the user to run `/esper:init` first and stop.

Run `esperkit config get current_phase` to get the current phase slug.

## Step 2: Gather project data

Read the following files:
- `.esper/CONSTITUTION.md`
- `.esper/esper.json`
- `.esper/phases/<current_phase>.md`

Run these commands to gather plan state:
```bash
esperkit plan list --dir pending --format json
```
```bash
esperkit plan list --dir active --format json
```
```bash
esperkit plan list --dir done --format json
```

Run these commands for git history and dependency health:
```bash
git log --oneline -20
```
```bash
git log --oneline --since="2 weeks ago" | wc -l
```
```bash
npm audit --json 2>/dev/null || true
```
```bash
npx npm-check-updates --errorLevel 0 2>/dev/null || true
```

## Step 3: Project Health

Analyze the gathered data across four dimensions:

**Constitution Alignment**
- Cross-reference recent commits and shipped plans against the principles in `CONSTITUTION.md`
- Flag any drift — work that contradicts or ignores stated principles

**Phase Progress**
- Count plans: done vs total (pending + active + done) for the current phase
- Check acceptance criteria in the phase file — which are met, which are outstanding

**Backlog State**
- Count pending plans by priority
- Flag stale plans (created more than 2 weeks ago with no activity)
- Flag an empty backlog (no pending plans remaining)

**Momentum**
- Commit frequency from the 2-week count
- Plans shipped recently
- Stall detection: if no commits in the last 3 days or no plans shipped in the last week, flag it

Assign an overall health rating: **HEALTHY**, **WATCH**, or **ATTENTION NEEDED**.

## Step 4: Phase Retrospective

Analyze the current phase file against shipped work:

**Goals vs Accomplishments**
- List each In Scope item from the phase file
- For each item, identify which done/active/pending plans cover it
- Mark status: covered, partially covered, or uncovered

**Acceptance Criteria**
- List each acceptance criterion from the phase file
- Assess whether shipped plans satisfy it: met, partially met, or not met

**Shipped Plans Summary**
- If the phase file has a `## Shipped Plans` section, use it
- Otherwise, list done plans with their titles

**Gaps and Risks**
- In Scope items with no covering plan
- Acceptance criteria not yet met
- Active or pending plans that may not ship before phase end

## Step 5: Dependency Health

Analyze the `npm audit` and `npm-check-updates` output from Step 2:

**Vulnerabilities**
- Count by severity (critical / high / moderate / low)
- List any critical or high vulnerabilities with affected packages

**Outdated Packages**
- Count packages with available major, minor, and patch updates
- Flag any packages more than 2 major versions behind

**Redundancy**
- Check `package.json` for packages that overlap in purpose (e.g. multiple HTTP clients, multiple test runners)

Assign a dependency health rating: **CURRENT**, **WATCH**, or **OUTDATED**.

## Step 6: Architecture Review

Launch an Explore subagent using the Task tool with `subagent_type: "Explore"`:

```
You are a senior software architect conducting an architecture review. You've been hired to evaluate this project's structural health before the team scales.

Review the codebase with these lenses:

1. Directory structure — is the layout intuitive? Would a new hire know where to add a new module?
2. Module boundaries — are concerns cleanly separated? Any circular dependencies or god modules that do too much?
3. Naming conventions — are file names, function names, and variable names consistent and predictable across the project?
4. Import/dependency patterns — are imports shallow and logical? Any files reaching deep into other modules' internals?
5. Configuration — are config files well-organized? Any duplication or drift between environments?
6. Principle adherence — does the code follow these project principles:

[Insert relevant principles from CONSTITUTION.md]

Rate each finding:
- observation: neutral architectural note
- warning: structural smell worth addressing
- concern: significant issue that will cause pain as the project grows

Return a structured list grouped by category. One line per finding with file paths. Skip categories with no findings.
```

## Step 7: Codebase Quality Audit

Launch an Explore subagent using the Task tool with `subagent_type: "Explore"`:

```
You are a senior engineer conducting a pre-release codebase audit. Your job is to find the issues that would embarrass the team in production or slow down the next contributor. Be thorough but practical — only flag things that matter.

Audit the codebase for:

1. Dead code — unused exports, unreachable branches, commented-out code that should have been deleted
2. Test coverage gaps — important logic paths, edge cases, or error scenarios without tests
3. Error handling — silent failures, swallowed exceptions, missing try/catch around I/O, unhandled promise rejections
4. Inconsistencies — mixed patterns for the same task, style drift across files, conventions that aren't followed everywhere
5. Tech debt markers — TODO/FIXME/HACK comments, workarounds with no linked issue, shortcuts that became permanent

Rate each finding:
- low: cleanup item, no functional risk
- medium: should fix soon, potential for bugs or confusion
- high: real risk, fix before shipping

Return a structured list grouped by category. Include file paths and line numbers. One line per finding. Skip categories with no findings.
```

## Step 8: Security Review

Launch an Explore subagent using the Task tool with `subagent_type: "Explore"`:

```
You are a security engineer conducting a security audit before this project ships to production. Think like an attacker — find the weaknesses a penetration tester would exploit.

Audit the codebase for:

1. Injection risks — command injection, path traversal, template injection, SQL/NoSQL injection. Trace any user input or external data through to where it's used.
2. Authentication & authorization — missing auth checks, privilege escalation paths, insecure session handling
3. Secrets & credentials — hardcoded API keys, tokens, passwords, or connection strings. Check config files, env examples, and committed .env files.
4. Input validation — system boundaries (CLI args, API inputs, file reads, environment variables) where untrusted data enters without validation or sanitization
5. Dependency risk — known vulnerable patterns in how dependencies are used (e.g. unsafe deserialization, eval of user data, prototype pollution vectors)
6. Information leakage — verbose error messages exposing internals, stack traces in production, debug endpoints left enabled

Rate each finding:
- low: theoretical risk, low exploitability
- medium: exploitable under certain conditions, should fix
- high: directly exploitable, fix immediately

Return a structured list grouped by category. Include file paths and line numbers. One line per finding. Skip categories with no findings.
```

## Step 9: Developer Experience Review

Launch an Explore subagent using the Task tool with `subagent_type: "Explore"`:

```
You are a new team member on your first day. You've just cloned this repo and need to get productive. Evaluate how easy or painful that process is.

Review the project for:

1. Onboarding — is there a clear README with setup instructions? Can you go from clone to running in under 5 minutes? Are prerequisites documented?
2. Documentation accuracy — do the docs match the actual code? Are there outdated instructions, missing steps, or broken examples?
3. Dev tooling — are linting, formatting, and type checking configured and consistent? Are there dev scripts in package.json for common tasks?
4. Error messages — when things go wrong, are the error messages helpful? Do they tell you what happened AND what to do about it?
5. Contribution friction — is it clear how to add a new feature, fix, or test? Are there patterns to follow or is every file different?

Rate each finding:
- smooth: works well, no friction
- rough: workable but confusing or underdocumented
- broken: blocks productivity, needs fixing

Return a structured list grouped by category. One line per finding with file paths where relevant. Skip categories with no findings.
```

## Step 10: API & Interface Consistency

Launch an Explore subagent using the Task tool with `subagent_type: "Explore"`:

```
You are an API design reviewer evaluating the public interfaces of this project — CLI commands, exported functions, configuration schemas, and any external-facing contracts.

Review for:

1. Naming consistency — do CLI flags, config keys, function names, and file conventions follow a single naming pattern? Flag any that break the convention.
2. Parameter patterns — are similar operations invoked the same way? Flag inconsistent argument ordering, mixed flag styles (--kebab vs --camelCase), or unpredictable defaults.
3. Output consistency — do commands and functions return data in consistent formats? Flag mixed output styles (JSON in one place, plain text in another for similar operations).
4. Error contracts — do errors follow a consistent shape? Flag places where errors are strings in one module and objects in another, or where exit codes are inconsistent.
5. Breaking change risks — flag any public interfaces that are fragile or would be hard to change without breaking consumers.

Rate each finding:
- consistent: follows established patterns
- drift: minor deviation from the convention
- inconsistent: actively confusing, should be standardized

Return a structured list grouped by category. One line per finding with file paths. Skip categories with no findings.
```

**Important:** Launch Steps 6, 7, 8, 9, and 10 Explore subagents in parallel using separate Task tool calls in the same message.

## Step 11: Report and Actions

Print a structured report:

```
## Project Audit Report

### 1. Project Health: [HEALTHY | WATCH | ATTENTION NEEDED]
- **Constitution Alignment:** [findings]
- **Phase Progress:** [X/Y plans complete, Z% of acceptance criteria met]
- **Backlog State:** [findings]
- **Momentum:** [findings]

### 2. Phase Retrospective: [phase name]

| In Scope Item | Status | Covered By |
|---|---|---|
| [item] | [covered/partial/uncovered] | [plan titles] |

**Acceptance Criteria:**
- [x] [met criterion]
- [ ] [unmet criterion]

**Gaps:** [uncovered items or unmet criteria]

### 3. Dependency Health: [CURRENT | WATCH | OUTDATED]
- **Vulnerabilities:** [count by severity]
- **Outdated Packages:** [findings]
- **Redundancy:** [findings]

### 4. Architecture Review: [SOLID | MINOR ISSUES | NEEDS WORK]
- **Directory Structure:** [findings]
- **Module Boundaries:** [findings]
- **Naming Conventions:** [findings]
- **Import Patterns:** [findings]
- **Configuration:** [findings]
- **Pattern Adherence:** [findings]

### 5. Codebase Quality: [CLEAN | MINOR DEBT | SIGNIFICANT DEBT]
- **Dead Code:** [findings with file paths]
- **Missing Tests:** [findings with file paths]
- **Error Handling:** [findings with file paths]
- **Inconsistencies:** [findings with file paths]
- **Tech Debt:** [findings with file paths]

### 6. Security: [SECURE | MINOR RISKS | VULNERABLE]
- **Injection Risks:** [findings with file paths]
- **Auth & Authorization:** [findings with file paths]
- **Secrets & Credentials:** [findings with file paths]
- **Input Validation:** [findings with file paths]
- **Dependency Risk:** [findings with file paths]
- **Information Leakage:** [findings with file paths]

### 7. Developer Experience: [SMOOTH | ROUGH EDGES | NEEDS WORK]
- **Onboarding:** [findings]
- **Documentation Accuracy:** [findings]
- **Dev Tooling:** [findings]
- **Error Messages:** [findings]
- **Contribution Friction:** [findings]

### 8. API & Interface Consistency: [CONSISTENT | MINOR DRIFT | INCONSISTENT]
- **Naming:** [findings]
- **Parameters:** [findings]
- **Output:** [findings]
- **Error Contracts:** [findings]
- **Breaking Change Risks:** [findings]

### Recommendations
1. [HIGH] [recommendation] — [related section]
2. [MEDIUM] [recommendation] — [related section]
3. [LOW] [recommendation] — [related section]
```

After printing the report, use `AskUserQuestion` with multi-select:

"What would you like to do with these findings?"

Options:
- **Create fix plans** — convert actionable findings into `/esper:fix` plans
- **Create explorations** — convert concerns into `/esper:explore` investigations
- **Add phase notes** — append key findings to the current phase file
- **Export report** — save the full report to `.esper/audits/YYYY-MM-DD-audit.md`
- **Done** — no follow-up action

For each selected action:
- **Create fix plans**: For each high/medium finding, invoke `/esper:fix` with the finding details pre-filled.
- **Create explorations**: For each concern or architectural issue, invoke `/esper:explore` with the question pre-filled.
- **Add phase notes**: Append a `## Audit Notes (YYYY-MM-DD)` section to `.esper/phases/<current_phase>.md` with a summary of key findings and recommendations.
- **Export report**: Create the `.esper/audits/` directory if needed, then write the full report to `.esper/audits/YYYY-MM-DD-audit.md`.

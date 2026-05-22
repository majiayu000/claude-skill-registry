---
name: team-review
description: |
  Parallel code review using Agent Teams. Spawns specialized reviewers
  (security, quality, test coverage) to review implementation from
  different perspectives simultaneously. Run after implementation.
metadata:
  short-description: Parallel review with Agent Teams
---

# Team Review

**Agent Teams による並列レビュー。実装完了後に複数の視点から同時にレビューする。**

## Prerequisites

- 実装が完了していること（`/team-implement` 後、または手動実装後）
- 全テストが通過していること

## Workflow

```
Step 1: Gather Diff
  実装範囲の変更差分を収集
    ↓
Step 2: Spawn Review Team
  専門レビュアーを並列起動
    ↓
Step 3: Synthesize Findings
  レビュー結果を統合、優先度付け
    ↓
Step 4: Report to User
  発見事項と推奨アクションを提示
```

---

## Step 1: Gather Diff

**レビュー対象の変更範囲を特定する。**

```bash
# All changes from main branch
git diff main...HEAD

# Changed files list
git diff main...HEAD --name-only

# Commit history
git log main..HEAD --oneline
```

---

## Step 2: Spawn Review Team

**専門的な視点を持つレビュアーを並列起動する。**

```
Create an agent team to review implementation of: {feature}

The following files were changed:
{changed files list}

Spawn reviewers:

1. **Security Reviewer**
   Prompt: "You are a Security Reviewer for: {feature}.

   Review all changed files for security vulnerabilities:
   - Hardcoded secrets or credentials
   - SQL injection, XSS, command injection
   - Input validation gaps
   - Authentication/authorization issues
   - Sensitive data exposure in logs/errors
   - Dependency vulnerabilities

   Changed files: {list}

   Reference: .claude/rules/security.md

   For each finding:
   - Severity: Critical / High / Medium / Low
   - File and line number
   - Description of the issue
   - Recommended fix

   Save report to .claude/docs/research/review-security-{feature}.md

   IMPORTANT — Work Log:
   When your review is complete, write a work log file to:
     .claude/logs/agent-teams/{team-name}/security-reviewer.md

   Use this format:
   # Work Log: Security Reviewer
   ## Summary
   (1-2 sentence summary of review scope and key findings)
   ## Review Scope
   - Files reviewed: {list}
   - Focus areas: {list}
   ## Findings
   - [{severity}] {file}:{line} — {issue summary}
   ## Communication with Teammates
   - → {recipient}: {summary of message sent}
   - ← {sender}: {summary of message received}
   (If none, write 'None')
   ## Issues Encountered
   - {issue}: {how it was resolved}
   (If none, write 'None')
   "

2. **Quality Reviewer**
   Prompt: "You are a Quality Reviewer for: {feature}.

   Review all changed files for code quality:
   - Adherence to coding principles (.claude/rules/coding-principles.md)
   - Single responsibility violations
   - Deep nesting (should use early return)
   - Missing type hints
   - Magic numbers
   - Naming clarity
   - Function length (target < 20 lines)
   - Library constraint violations (.claude/docs/libraries/)

   Use Codex CLI for deep analysis of complex logic:
   codex exec --model gpt-5.3-codex --sandbox read-only --full-auto "{question}" 2>/dev/null

   Changed files: {list}

   For each finding:
   - Severity: High / Medium / Low
   - File and line number
   - Current code
   - Suggested improvement

   Save report to .claude/docs/research/review-quality-{feature}.md

   IMPORTANT — Work Log:
   When your review is complete, write a work log file to:
     .claude/logs/agent-teams/{team-name}/quality-reviewer.md

   Use this format:
   # Work Log: Quality Reviewer
   ## Summary
   (1-2 sentence summary of review scope and key findings)
   ## Review Scope
   - Files reviewed: {list}
   - Focus areas: {list}
   ## Findings
   - [{severity}] {file}:{line} — {issue summary}
   ## Codex Consultations
   - {question asked to Codex}: {key insight from response}
   ## Communication with Teammates
   - → {recipient}: {summary of message sent}
   - ← {sender}: {summary of message received}
   (If none, write 'None')
   ## Issues Encountered
   - {issue}: {how it was resolved}
   (If none, write 'None')
   "

3. **Test Reviewer**
   Prompt: "You are a Test Reviewer for: {feature}.

   Review test coverage and quality:
   - Run: uv run pytest --cov=src --cov-report=term-missing
   - Check: Are all happy paths tested?
   - Check: Are error cases covered?
   - Check: Are boundary values tested?
   - Check: Are edge cases handled?
   - Check: Are external deps properly mocked?
   - Check: Do tests follow AAA pattern?
   - Check: Are tests independent (no order dependency)?

   Reference: .claude/rules/testing.md

   For each gap:
   - File/function missing coverage
   - What test cases are needed
   - Priority: High / Medium / Low

   Save report to .claude/docs/research/review-tests-{feature}.md

   IMPORTANT — Work Log:
   When your review is complete, write a work log file to:
     .claude/logs/agent-teams/{team-name}/test-reviewer.md

   Use this format:
   # Work Log: Test Reviewer
   ## Summary
   (1-2 sentence summary of review scope and key findings)
   ## Review Scope
   - Files reviewed: {list}
   - Coverage: {percentage}
   ## Findings
   - [{priority}] {file/function}: {missing test case description}
   ## Test Execution Results
   - Total: {N} tests, Passed: {N}, Failed: {N}
   - Coverage: {percentage}
   ## Communication with Teammates
   - → {recipient}: {summary of message sent}
   - ← {sender}: {summary of message received}
   (If none, write 'None')
   ## Issues Encountered
   - {issue}: {how it was resolved}
   (If none, write 'None')
   "

Wait for all reviewers to complete.
```

### Optional: Competing Hypotheses (for debugging)

For bug investigation, add adversarial reviewers:

```
Spawn 3-5 teammates with different hypotheses about the bug.
Have them actively try to disprove each other's theories.
```

---

## Step 3: Synthesize Findings

**全レビュアーの結果を統合し、優先度付けする。**

Read review reports:
- `.claude/docs/research/review-security-{feature}.md`
- `.claude/docs/research/review-quality-{feature}.md`
- `.claude/docs/research/review-tests-{feature}.md`

### Prioritization

| Priority | Criteria | Action |
|----------|----------|--------|
| **Critical** | Security vulnerabilities, data loss risk | Must fix before merge |
| **High** | Bugs, missing critical tests, type errors | Should fix before merge |
| **Medium** | Code quality, naming, patterns | Fix if time allows |
| **Low** | Style, minor improvements | Track for later |

---

## Step 4: Report to User

**統合レビュー結果をユーザーに提示する（日本語）。**

```markdown
## レビュー結果: {feature}

### サマリー
- セキュリティ: {N}件 (Critical: {n}, High: {n}, Medium: {n})
- コード品質: {N}件 (High: {n}, Medium: {n}, Low: {n})
- テストカバレッジ: {N}% (目標80%に対して {above/below})

### Critical / High 発見事項

#### [{Severity}] {Issue Title}
- **ファイル**: `{file}:{line}`
- **問題**: {description}
- **修正案**: {recommended fix}

...

### 推奨アクション
1. {Action 1 — Critical fix}
2. {Action 2 — High priority fix}
3. {Action 3 — Test gap to fill}

### Medium / Low 発見事項
{Brief list — details in review reports}

---
修正を行いますか？
```

### Cleanup

```
Clean up the team
```

---

## Tips

- **レビュアーの専門分化**: 各レビュアーが異なる視点に集中することで漏れを防ぐ
- **Codex 活用**: Quality Reviewer が複雑なロジックを Codex に分析させる
- **レポート永続化**: `.claude/docs/research/` にレビュー結果を保存し、修正時の参照に
- **競合仮説モード**: バグ調査時は adversarial review パターンが有効
- **コスト注意**: 3レビュアー = 3x トークン消費。小規模変更にはサブエージェント経由のレビューで十分

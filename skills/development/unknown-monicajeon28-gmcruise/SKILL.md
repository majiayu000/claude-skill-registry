# Simple Skill Template

코드 없이 지침만 제공하는 단순 스킬용

---

## SKILL.md 예시

```markdown
---
name: writing-commit-messages
description: "Generates descriptive commit messages from git diffs. Use when writing commits or reviewing staged changes."
allowed-tools:
  - Bash
  - Read
---

# Commit Message Generator

## Quick start

1. Stage your changes: `git add .`
2. Review diff: `git diff --staged`
3. Generate message following the format below

## Message format

```
type(scope): brief description

Detailed explanation of changes
```

**Types**: feat, fix, docs, style, refactor, test, chore

## Examples

**Input**: Added user authentication with JWT
**Output**:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Input**: Fixed date display bug in reports
**Output**:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

## Guidelines

- First line: 50 chars max
- Body: 72 chars per line
- Use imperative mood ("Add" not "Added")
- Explain why, not just what
```

---

## 핵심 포인트

1. **Quick start**: 핵심 사용법 바로 보여주기
2. **Format**: 기대하는 형식 명확히
3. **Examples**: Input/Output 쌍으로 제시
4. **Guidelines**: 간결한 규칙

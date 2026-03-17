---
name: git-workflow
description: Complete Git workflow from conventional commits to pre-completion verification. Use for all Git operations including commits, branches, and releases.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
license: MIT
metadata:
  author: antigravity-team
  version: "2.0"
---

# Git Workflow

커밋부터 완료 검증까지의 Git 워크플로우 통합 스킬입니다.

## Conventional Commits

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | 설명 | 예시 |
|------|------|------|
| `feat` | 새 기능 | `feat(auth): add JWT login` |
| `fix` | 버그 수정 | `fix(api): handle null response` |
| `refactor` | 리팩토링 | `refactor(utils): simplify parser` |
| `docs` | 문서 | `docs: update README` |
| `test` | 테스트 | `test(auth): add login tests` |
| `chore` | 기타 | `chore: update deps` |

### Breaking Changes

```
feat(api)!: change response format

BREAKING CHANGE: response.data is now response.result
```

---

## Pre-Completion Verification

### 완료 선언 전 필수 체크

```bash
# 1. 테스트 통과
npm test

# 2. 린트 통과
npm run lint

# 3. 타입 체크 (TypeScript)
npx tsc --noEmit

# 4. 빌드 성공
npm run build
```

### Verification Checklist

- [ ] 모든 테스트 통과
- [ ] 린트 에러 없음
- [ ] 타입 에러 없음
- [ ] 빌드 성공
- [ ] 변경사항 커밋됨
- [ ] 불필요한 console.log 제거

---

## Branch Strategy

```
main ─────────────────────────────
  │
  └─ feature/auth ───○───○───○─┐
                               │
                               └─ merge
```

### Naming

```
feature/<description>
fix/<issue-number>-<description>
refactor/<description>
```

---

## Commit Workflow

```bash
# 1. 변경사항 스테이징
git add <files>

# 2. 커밋 (규격 준수)
git commit -m "feat(scope): description"

# 3. 푸시 전 검증
npm test && npm run lint

# 4. 푸시
git push
```

## Checklist

- [ ] 커밋 메시지 규격 준수
- [ ] 테스트 통과
- [ ] 린트 통과
- [ ] 빌드 성공

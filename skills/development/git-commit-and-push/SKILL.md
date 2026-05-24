---
name: git-commit-and-push
description: Git Commit and Push. Use when user wants to commit and push changes together.
---

# Git Commit and Push

커밋과 푸시를 순차적으로 수행합니다.

## Workflow

1. **Commit Phase** - `/git-commit` 스킬 참조
2. **Push Phase** - `/git-push` 스킬 참조

## Quick Flow

```bash
# 1. 상태 확인
git status
git fetch origin

# 2. 스테이징 & 커밋
git add <files>
git commit -v

# 3. 동기화 & 푸시
git pull --rebase origin $(git branch --show-current)
git push origin $(git branch --show-current)
```

## Checklist

- [ ] 민감한 정보 없음
- [ ] 테스트 통과
- [ ] 커밋 메시지 규칙 준수 (/git-commit 참조)
- [ ] Protected branch 직접 push 주의

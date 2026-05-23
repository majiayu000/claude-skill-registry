---
name: git-push
description: Git Push Guide. Use when user wants to push changes to remote repository safely.
---

# Git Push Guide

안전하고 체계적인 Git Push를 위한 가이드

---

## Pre-Push Checklist

```bash
# 1. 상태 확인
git status
git fetch origin

# 2. 푸시할 커밋 확인
git log origin/$(git branch --show-current)..HEAD --oneline

# 3. 원격과 차이 확인
git diff HEAD...origin/$(git branch --show-current)
```

---

## Push Strategies

### Standard Push
```bash
git push origin $(git branch --show-current)

# 업스트림 설정과 함께
git push -u origin $(git branch --show-current)
```

### Sync Before Push (원격에 새 커밋 있을 때)
```bash
# Rebase 방식 (권장 - 깨끗한 히스토리)
git pull --rebase origin $(git branch --show-current)

# Merge 방식
git pull origin $(git branch --show-current)
```

### Force Push (주의!)
```bash
# Force with lease (더 안전함) - 개인 브랜치에서만
git push --force-with-lease origin $(git branch --show-current)

# 일반 force push - 사용 금지
# git push --force
```

---

## Protected Branches

다음 브랜치는 직접 push 전 확인 필요:
- `main`, `master`
- `develop`, `release`
- `production`

---

## Never Push

- 컴파일/테스트 실패 코드
- 100MB 이상 파일
- Credentials, API keys, `.env` files
- Generated files (node_modules, .pyc, build/)

---

## Recovery

```bash
# Push 취소 (팀과 상의 필수!)
git revert HEAD
git push origin branch

# 충돌 해결 후 재시도
git pull --rebase origin branch
git push origin branch
```

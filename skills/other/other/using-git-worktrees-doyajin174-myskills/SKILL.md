---
name: using-git-worktrees
description: Create isolated git worktrees with smart directory selection and safety verification. Use this when starting feature work that needs isolation, parallel development, or safe experimentation.
allowed-tools: Read, Glob, Grep, Bash
license: MIT
metadata:
  author: obra/superpowers
  version: "1.0"
---

# Using Git Worktrees

Git worktree를 사용한 격리된 개발 환경 생성 가이드입니다.

## When to Use

- 기능 개발을 위한 격리된 환경 필요 시
- 여러 브랜치에서 동시 작업 시
- 안전한 실험이 필요할 때
- 구현 계획 실행 전 환경 준비 시

## Quick Start

```bash
# 1. worktree 디렉토리 확인/생성
ls -la ../worktrees/ 2>/dev/null || mkdir -p ../worktrees

# 2. 새 worktree 생성
git worktree add ../worktrees/feature-name -b feature/feature-name

# 3. worktree로 이동
cd ../worktrees/feature-name

# 4. 작업 완료 후 정리
git worktree remove ../worktrees/feature-name
```

## Directory Selection Strategy

### 권장 구조

```
project-root/
├── .git/                    # 메인 저장소
├── src/                     # 메인 작업 디렉토리
└── ...

../worktrees/                # worktree 전용 디렉토리
├── feature-auth/           # 인증 기능 작업
├── feature-api/            # API 개발
└── hotfix-critical/        # 긴급 수정
```

### 네이밍 규칙

```
../worktrees/{type}-{name}

types:
- feature-*    기능 개발
- hotfix-*     긴급 수정
- experiment-* 실험적 변경
- review-*     코드 리뷰용
```

## Safety Verification

### 생성 전 체크리스트

```bash
# 1. 현재 상태 확인
git status                    # 미커밋 변경사항 확인
git stash list               # stash 상태 확인

# 2. 브랜치 존재 여부 확인
git branch -a | grep feature-name

# 3. worktree 목록 확인
git worktree list
```

### 생성 후 검증

```bash
# 1. worktree 상태 확인
git worktree list

# 2. 현재 브랜치 확인
git branch

# 3. 원격 연결 확인
git remote -v
```

## Common Workflows

### 기능 개발 시작

```bash
# 1. 최신 main 기준으로 worktree 생성
git fetch origin
git worktree add ../worktrees/feature-x -b feature/x origin/main

# 2. 의존성 설치 (프로젝트에 따라)
cd ../worktrees/feature-x
npm install  # 또는 pip install -r requirements.txt

# 3. 개발 시작
code .  # 또는 원하는 에디터
```

### 코드 리뷰용 환경

```bash
# PR 브랜치를 별도 worktree로
git worktree add ../worktrees/review-pr-123 origin/feature/pr-123
cd ../worktrees/review-pr-123
# 테스트 실행, 코드 검토
```

### 긴급 수정

```bash
# 현재 작업 중단 없이 hotfix
git worktree add ../worktrees/hotfix-critical -b hotfix/critical origin/main
cd ../worktrees/hotfix-critical
# 수정 → 커밋 → PR
```

## Cleanup

### 개별 worktree 제거

```bash
# 1. worktree 제거
git worktree remove ../worktrees/feature-x

# 2. 브랜치도 삭제하려면
git branch -d feature/x
```

### 전체 정리

```bash
# 1. 모든 worktree 목록
git worktree list

# 2. 정리 (삭제된 worktree 참조 제거)
git worktree prune

# 3. 미사용 worktree 디렉토리 삭제
rm -rf ../worktrees/old-feature
git worktree prune
```

## Best Practices

1. **일관된 위치**: worktree는 항상 `../worktrees/`에
2. **명확한 네이밍**: 목적이 드러나는 이름 사용
3. **정기적 정리**: 완료된 worktree는 즉시 제거
4. **독립적 의존성**: 각 worktree에서 별도로 의존성 설치
5. **메인 저장소 보존**: worktree에서만 실험적 변경

## Troubleshooting

| 문제 | 해결책 |
|------|--------|
| "already checked out" | 다른 worktree에서 사용 중, 다른 브랜치명 사용 |
| "not a valid ref" | `git fetch` 먼저 실행 |
| 의존성 오류 | worktree에서 새로 설치 필요 |
| 변경사항 충돌 | 메인에서 stash 또는 commit 후 진행 |

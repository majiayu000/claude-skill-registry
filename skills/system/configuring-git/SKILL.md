---
name: configuring-git
description: |
  This skill should be used when the user configures Git with Home Manager,
  sets up delta, rerere, or encounters gitconfig conflicts. Covers custom
  aliases, git-cleanup scripts, rebase reverse display.
---

# Git 설정

Git, delta diff, rerere 등 Git 관련 설정 가이드입니다.

## 빠른 참조

### 주요 기능

| 기능 | 설명 |
|------|------|
| delta | Git diff를 구문 강조로 표시 |
| rerere | 충돌 해결 패턴 기록/재사용 |
| rebase 역순 | Interactive rebase에서 최신 커밋이 위로 |
| git-cleanup | 오래된/삭제된 브랜치 정리 |

### delta 설정 확인

```bash
# delta가 설치되어 있는지 확인
which delta

# Git에서 delta 사용 중인지 확인
git config --get core.pager
```

### rerere 사용법

```bash
# rerere 상태 확인
git rerere status

# 기록된 해결책 확인
git rerere diff

# 캐시 정리
rm -rf .git/rr-cache
```

### 설정 파일 위치

| 파일 | 용도 |
|------|------|
| `modules/shared/programs/git/default.nix` | Git 공통 설정 |
| `~/.gitconfig` | 생성된 설정 (Nix 관리) |

## 자주 발생하는 문제

1. **delta 적용 안 됨**: `core.pager` 설정 확인, PATH에 delta 있는지 확인
2. **gitconfig 충돌**: 기존 `~/.gitconfig`가 있으면 Home Manager와 충돌
3. **rebase 역순 안 됨**: `GIT_SEQUENCE_EDITOR` 환경변수 확인

## git-cleanup 사용법

```bash
# 삭제된 원격 브랜치와 연결된 로컬 브랜치 정리
git-cleanup

# 출력 예시:
# [gone] feature/old-feature
# [stale] feature/very-old (3 months ago)
```

## 레퍼런스

- 트러블슈팅: [references/troubleshooting.md](references/troubleshooting.md)
- Git 설정 가이드: [references/config.md](references/config.md)

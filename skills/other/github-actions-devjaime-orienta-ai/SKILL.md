---
name: github-actions
description: "GitHub Actions 워크플로우 생성, 보안 및 버전 관리 스킬. 다음 상황에서 사용: (1) 새 워크플로우 파일(.yml) 작성 시, (2) 기존 워크플로우 수정 시, (3) 액션 버전 검토 또는 업데이트 시, (4) CI/CD 보안 감사 시, (5) 'actions/', 'uses:', 'workflow', '.github/workflows' 키워드가 포함된 작업 시"
license: MIT
metadata:
  author: DaleStudy
  version: "1.0"
allowed-tools: Bash(gh api:*)
---

# GitHub Actions

## 모범 관례

### 1. 최신 메이저 버전 사용

새 워크플로우 작성 시 최신 메이저 버전 확인 필수.

```yaml
# ❌ 브랜치 직접 참조 - 항상 변경됨
uses: actions/checkout@main

# ❌ 오래된 버전 - 가장 흔한 실수
uses: actions/checkout@v5

# ✅ 최신 메이저 버전 (gh api로 확인 후 사용)
uses: actions/checkout@v6
```

> 참고: 보안 민감 환경이나 신뢰도 낮은 서드파티 액션은 [SHA 피닝](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions#using-third-party-actions)(`@a1b2c3...`)을 고려.

버전 확인 명령어:

```bash
gh api repos/{owner}/{repo}/releases/latest --jq '.tag_name'

# 예시
gh api repos/actions/checkout/releases/latest --jq '.tag_name'
gh api repos/oven-sh/setup-bun/releases/latest --jq '.tag_name'
```

### 2. 최소 권한 원칙

권한은 가능한 하위 레벨에 선언. 범위를 좁게 유지.

```yaml
# 권한 범위: step > job > workflow (하위일수록 좋음)
jobs:
  build:
    permissions:
      contents: read # job 레벨에서 필요한 권한만
```

> 참고: [Modifying the permissions for the GITHUB_TOKEN](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#modifying-the-permissions-for-the-github_token)

### 3. 시크릿 관리

```yaml
# ❌ 하드코딩
env:
  API_KEY: "sk-1234567890"

# ✅ secrets 사용
env:
  API_KEY: ${{ secrets.API_KEY }}
```

> 참고: [Using secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)

### 4. 입력값 인젝션 방지

```yaml
# ❌ 인젝션 취약 - github.event 직접 사용
run: echo "${{ github.event.issue.title }}"

# ✅ 환경변수로 전달
env:
  ISSUE_TITLE: ${{ github.event.issue.title }}
run: echo "$ISSUE_TITLE"
```

> 참고: [Script injections](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions#understanding-the-risk-of-script-injections)

### 5. Pull Request 보안

`pull_request_target`은 포크의 PR에서도 시크릿에 접근 가능. 포크 코드를 체크아웃하면 악성 코드 실행 위험.

```yaml
# ⚠️ 위험 - 포크의 코드를 신뢰된 컨텍스트에서 실행
on: pull_request_target
steps:
  - uses: actions/checkout@v{N}
    with:
      ref: ${{ github.event.pull_request.head.sha }} # 위험!
```

> 참고: [pull_request_target](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#pull_request_target)

## 권장 워크플로우 구조

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read

    steps:
      # 버전은 gh api로 확인 후 사용
      - uses: actions/checkout@v{N}

      - name: Setup Bun
        uses: oven-sh/setup-bun@v{N}
```

## 자주 사용되는 이벤트

```yaml
on:
  push: # 푸시 시
    branches: [main]
  pull_request: # PR 생성/업데이트 시
    branches: [main]
  workflow_dispatch: # 수동 실행
  schedule: # 스케줄 실행
    - cron: "0 0 * * 1" # 매주 월요일 00:00 UTC
  release: # 릴리스 생성 시
    types: [published]
  workflow_call: # 다른 워크플로우에서 호출
```

## 자주 사용되는 권한

```yaml
permissions:
  contents: read        # CI (빌드/테스트), 코드 체크아웃
  contents: write       # 커밋/푸시
  pull-requests: write  # PR 코멘트 봇
  issues: write         # 이슈 코멘트
  packages: write       # 패키지 배포 (contents: write와 함께)
  id-token: write       # OIDC 클라우드 인증 (contents: read와 함께)
```

## 자주 사용되는 액션

```yaml
# 버전은 gh api repos/{owner}/{repo}/releases/latest --jq '.tag_name'으로 확인
steps:
  - uses: actions/cache@v{N} # 의존성 캐싱
  - uses: actions/checkout@v{N} # 코드 체크아웃
  - uses: actions/download-artifact@v{N} # 아티팩트 다운로드
  - uses: actions/upload-artifact@v{N} # 아티팩트 업로드
  - uses: oven-sh/setup-bun@v{N} # Bun 설정
```

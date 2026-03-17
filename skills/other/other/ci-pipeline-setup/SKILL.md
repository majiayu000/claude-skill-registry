---
name: ci-pipeline-setup
description: Set up CI/CD pipelines with GitHub Actions. Use when creating new projects, adding automation, or when manual verification becomes bottleneck. Covers lint, test, build, deploy automation.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
license: MIT
metadata:
  author: antigravity-team
  version: "1.0"
---

# CI Pipeline Setup

GitHub Actions를 이용한 CI/CD 파이프라인 설정 스킬입니다.

## Core Principle

> **"verification-before-completion을 로컬에서만 하지 말고, 원격 저장소에서 자동으로 강제한다."**
> **"머지 전에 CI가 통과해야 한다 = 시스템으로 강제"**

## 필수 파이프라인 단계

| 단계 | 목적 | 실패 시 |
|------|------|---------|
| **Lint** | 코드 스타일 일관성 | PR 머지 차단 |
| **Type Check** | 타입 안전성 검증 | PR 머지 차단 |
| **Test** | 기능 정확성 검증 | PR 머지 차단 |
| **Build** | 빌드 가능 여부 확인 | PR 머지 차단 |
| **Security** | 취약점 스캔 | PR 머지 차단 |

## 기본 CI 워크플로우

### `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

# 동시 실행 제어 (같은 PR에 새 커밋 시 이전 실행 취소)
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  # ================================
  # 1. 코드 품질 검사
  # ================================
  lint:
    name: Lint & Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run ESLint
        run: npm run lint

      - name: Check formatting
        run: npm run format:check

  # ================================
  # 2. 타입 검사
  # ================================
  typecheck:
    name: Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run TypeScript
        run: npm run typecheck

  # ================================
  # 3. 테스트
  # ================================
  test:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          fail_ci_if_error: false

  # ================================
  # 4. 빌드
  # ================================
  build:
    name: Build
    runs-on: ubuntu-latest
    needs: [lint, typecheck, test]
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Upload build artifact
        uses: actions/upload-artifact@v4
        with:
          name: build
          path: .next/
          retention-days: 7

  # ================================
  # 5. 보안 스캔
  # ================================
  security:
    name: Security Audit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run npm audit
        run: npm audit --audit-level=high
```

## package.json 스크립트

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint . --ext .ts,.tsx",
    "lint:fix": "eslint . --ext .ts,.tsx --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "typecheck": "tsc --noEmit",
    "test": "vitest",
    "test:ci": "vitest --run --coverage"
  }
}
```

## Branch Protection Rules

### GitHub 설정 방법

```
Settings → Branches → Add rule

Branch name pattern: main

✅ Require a pull request before merging
  ✅ Require approvals (최소 1명)
  ✅ Dismiss stale pull request approvals when new commits are pushed

✅ Require status checks to pass before merging
  ✅ Require branches to be up to date before merging
  Status checks:
    - lint
    - typecheck
    - test
    - build
    - security

✅ Require conversation resolution before merging
✅ Do not allow bypassing the above settings
```

### branch-protection.yml (자동 설정용)

```yaml
# .github/branch-protection.yml
branches:
  - name: main
    protection:
      required_pull_request_reviews:
        required_approving_review_count: 1
        dismiss_stale_reviews: true
      required_status_checks:
        strict: true
        contexts:
          - lint
          - typecheck
          - test
          - build
          - security
      enforce_admins: true
      restrictions: null
```

## 고급 패턴

### Matrix 빌드 (다중 환경)

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm ci
      - run: npm test
```

### 캐시 최적화

```yaml
- name: Cache node_modules
  uses: actions/cache@v4
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### PR 라벨 자동화

```yaml
# .github/workflows/labeler.yml
name: Labeler

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v5
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
```

### 의존성 자동 업데이트 (Dependabot)

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
    groups:
      dev-dependencies:
        patterns:
          - "@types/*"
          - "eslint*"
          - "prettier*"
```

## 배포 파이프라인 (CD)

### Vercel 자동 배포

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    needs: [lint, typecheck, test, build]
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

### Preview 배포 (PR별)

```yaml
# PR에서 자동으로 Preview URL 생성
on:
  pull_request:

jobs:
  preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          # --prod 없음 = Preview 배포
```

## Workflow 파일 구조

```
.github/
├── workflows/
│   ├── ci.yml           # 메인 CI (lint, test, build)
│   ├── deploy.yml       # 프로덕션 배포
│   ├── preview.yml      # PR Preview 배포
│   └── labeler.yml      # 라벨 자동화
├── dependabot.yml       # 의존성 업데이트
├── CODEOWNERS           # 코드 소유자
└── PULL_REQUEST_TEMPLATE.md
```

## Checklist

### 새 프로젝트

- [ ] `.github/workflows/ci.yml` 생성
- [ ] package.json 스크립트 정의 (lint, typecheck, test, build)
- [ ] Branch Protection Rules 설정
- [ ] Dependabot 설정
- [ ] CODEOWNERS 파일 생성

### CI 품질

- [ ] 모든 PR에서 CI 필수 통과
- [ ] 캐시 최적화로 빌드 시간 단축
- [ ] 병렬 실행으로 효율성 증가
- [ ] 실패 시 명확한 에러 메시지

### 보안

- [ ] Secrets는 GitHub Secrets에만 저장
- [ ] npm audit 자동 실행
- [ ] 의존성 자동 업데이트 활성화

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [Dependabot](https://docs.github.com/en/code-security/dependabot)

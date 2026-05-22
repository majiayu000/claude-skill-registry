---
name: monorepo-architect
description: "**MONOREPO ARCHITECT**: '모노레포', '워크스페이스', '패키지 구조', '폴더 구조', 'shared', '공유 코드', '의존성', 'turborepo', 'pnpm' 요청 시 자동 발동. pnpm-workspace.yaml/turbo.json/packages/** 작업 시 자동 적용. 의존성 방향 규칙 검증."
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Monorepo Architect v2.0 - Unified Monorepo Structure Guide

**Proactive Monorepo Guardian** - 모노레포 구조 관련 작업 시 자동으로 규칙 적용

## 자동 발동 조건

```yaml
Auto_Trigger_Conditions:
  File_Patterns:
    - "pnpm-workspace.yaml, lerna.json"
    - "turbo.json, nx.json"
    - "packages/**/*, apps/**/*"
    - "tsconfig.base.json, tsconfig.paths.json"

  Keywords_KO:
    - "모노레포, 모노 레포, 워크스페이스"
    - "패키지 구조, 폴더 구조, 프로젝트 구조"
    - "공유 코드, shared, 공통 모듈"
    - "의존성, 디펜던시, import 경로"
    - "turborepo, lerna, nx, pnpm"
    - "패키지 추가, 새 패키지"

  Keywords_EN:
    - "monorepo, workspace, workspaces"
    - "package structure, folder structure"
    - "shared code, common module"
    - "dependency, import path"
    - "turborepo, lerna, nx, pnpm"

  Path_Patterns:
    - "@monorepo/, @packages/, @apps/"
    - "packages/shared, packages/common"
```

## 선택적 문서 로드 전략

```yaml
Document_Loading_Strategy:
  Always_Load:
    - "core/structure.md"           # 폴더 구조 (항상)
    - "quick-reference/checklist.md" # 체크리스트 (항상)

  Context_Specific_Load:
    New_Package: "templates/package-template.md"
    Dependency_Analysis: "core/dependency-rules.md"
    Build_Pipeline: "patterns/turborepo.md"
    TypeScript_Config: "patterns/typescript-config.md"
    Shared_Code: "core/shared-package.md"
```

## Quick Reference

### 5 Core Principles

```yaml
1. Shared First: "중복 코드는 packages/shared로"
2. Dependency Direction: "의존성은 항상 packages → apps 방향"
3. Independent Deployability: "각 app은 독립 배포 가능"
4. Consistent Tooling: "전체 프로젝트 동일 도구 사용"
5. Clear Boundaries: "패키지 간 명확한 경계"
```

### Instant Checklist

```markdown
## 새 코드 작성 시
- [ ] 이 코드가 여러 app에서 사용될까? → packages/shared로
- [ ] 의존성 방향이 올바른가? (packages → apps)
- [ ] 적절한 위치에 있는가?

## 새 패키지 추가 시
- [ ] package.json에 name, version, main 설정?
- [ ] tsconfig.json이 base를 extends?
- [ ] 루트 workspace에 등록?
```

### Standard Structure (Quick View)

```
project-root/
├── apps/
│   ├── backend/         # NestJS
│   ├── web/             # Next.js
│   └── mobile/          # Expo
├── packages/
│   ├── shared/          # Types, Utils, Validation
│   ├── ui/              # Shared UI Components
│   ├── api-client/      # API Client (auto-generated)
│   └── config/          # Shared configs
├── tools/               # Build scripts
├── pnpm-workspace.yaml
├── turbo.json
└── tsconfig.base.json
```

### Dependency Direction

```
✅ 허용: apps/* → packages/*
❌ 금지: packages/* → apps/*
❌ 금지: apps/backend → apps/web
```

## 문서 구조

```
monorepo-architect/
├── SKILL.md                        # 이 파일 (라우터)
├── core/
│   ├── structure.md                # 폴더 구조 상세
│   ├── shared-package.md           # shared 패키지 설계
│   └── dependency-rules.md         # 의존성 규칙
├── templates/
│   ├── package-template.md         # 새 패키지 템플릿
│   └── app-configs.md              # 앱별 설정 템플릿
├── patterns/
│   ├── turborepo.md                # Turborepo 설정
│   └── typescript-config.md        # TypeScript 설정
└── quick-reference/
    ├── checklist.md                # 체크리스트
    └── anti-patterns.md            # 안티패턴
```

## 사용 방법

### 1. 자동 발동 (Proactive)
모노레포 구조, pnpm workspace, import 경로 관련 작업 시 자동 발동

### 2. 명시적 호출
```
"새 패키지 추가하려면 어디에 만들어야 해?"
"이 코드를 shared로 옮겨야 할까?"
"의존성 방향이 맞는지 확인해줘"
```

---

**Version**: 2.0.0
**Quality Target**: 90%
**Related Skills**: clean-code-mastery, api-first-design

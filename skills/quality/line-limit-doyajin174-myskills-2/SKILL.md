---
name: line-limit
description: Enforce file line count limits (200 recommended, 300 max) for CODE IMPLEMENTATION files only. Use this when reviewing code, creating files, or when files exceed line limits and need modularization.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
license: MIT
metadata:
  author: antigravity-team
  version: "1.0"
---

# Line Limit Enforcement

**코드 구현 파일**에 대한 라인 수 제한을 강제하는 스킬입니다.

## Scope

> **이 스킬은 코드 구현 파일에만 적용됩니다.**

### ✅ 적용 대상

| 파일 유형 | 확장자 |
|----------|--------|
| JavaScript/TypeScript | `.js`, `.ts`, `.jsx`, `.tsx` |
| Python | `.py` |
| Go | `.go` |
| Rust | `.rs` |
| Java/Kotlin | `.java`, `.kt` |
| C/C++ | `.c`, `.cpp`, `.h` |
| 기타 실행 코드 | 언어별 소스 파일 |

### 🚫 예외 (적용 제외)

| 파일 유형 | 확장자/위치 | 사유 |
|----------|------------|------|
| Jupyter Notebook | `.ipynb` | 셀 기반 구조, 출력 포함 |
| 스킬 파일 | `SKILL.md` | 문서/가이드 (500줄까지 허용) |
| 문서 파일 | `.md`, `.mdx` | 문서는 길어도 무방 |
| 설정 파일 | `.json`, `.yaml`, `.toml` | 구조적 데이터 |
| 테스트 픽스처 | `fixtures/`, `__mocks__/` | 테스트 데이터 |
| 자동 생성 파일 | `*.generated.*`, `*.g.*` | 수동 관리 X |
| 타입 정의 | `.d.ts` | 선언 파일 |
| CSS/스타일 | `.css`, `.scss` | 스타일시트 |

## Rules

| 상태 | 라인 수 | 조치 |
|------|---------|------|
| ✅ OK | 0-200 | 정상 |
| ⚠️ WARNING | 201-300 | 권장 리팩토링 |
| 🔴 VIOLATION | 301+ | **필수 분리** |

## When This Skill Activates

- 새 파일 작성 시 라인 수 체크
- 코드 리뷰 요청 시
- "파일이 너무 길어", "모듈화 해줘" 등 요청 시
- 300줄 초과 파일 발견 시

## Enforcement Workflow

### 1. 라인 수 체크
```bash
wc -l <file>
```

### 2. 상태 판정
```
if lines <= 200: ✅ OK
elif lines <= 300: ⚠️ WARNING - 리팩토링 권장
else: 🔴 VIOLATION - 분리 필수
```

### 3. 위반 시 조치

**🔴 300줄 초과 파일 발견 시 반드시:**

1. 파일 구조 분석 (함수/클래스/섹션 파악)
2. 분리 가능한 단위 식별:
   - 유틸리티 함수 → `utils/` 또는 `helpers/`
   - 타입 정의 → `types/` 또는 `*.types.ts`
   - 상수/설정 → `constants/` 또는 `config/`
   - 하위 컴포넌트 → `components/`
   - 훅 → `hooks/`
3. 분리 계획 제시
4. 사용자 승인 후 리팩토링 실행

## Modularization Patterns

### React/TypeScript
```
# Before (500 lines)
src/components/Dashboard.tsx

# After
src/components/Dashboard/
├── index.tsx          # Main component (< 200 lines)
├── DashboardHeader.tsx
├── DashboardStats.tsx
├── DashboardChart.tsx
├── hooks/
│   └── useDashboardData.ts
├── types.ts
└── constants.ts
```

### General Functions
```
# Before (400 lines)
src/utils/helpers.ts

# After
src/utils/
├── index.ts           # Re-exports
├── string.utils.ts
├── date.utils.ts
├── array.utils.ts
└── validation.utils.ts
```

## Examples

### Example 1: 코드 리뷰 시
```
User: 이 파일 리뷰해줘 - src/services/api.ts

Claude: [파일 읽기 후]
📊 라인 수 체크: 342 lines
🔴 VIOLATION: 300줄 초과 - 모듈화 필요

분석 결과:
- API 엔드포인트 함수: 15개 (240 lines)
- 타입 정의: 12개 (45 lines)
- 헬퍼 함수: 5개 (57 lines)

권장 분리:
1. api/endpoints/ - 엔드포인트별 분리
2. api/types.ts - 타입 정의 추출
3. api/helpers.ts - 헬퍼 함수 추출

분리를 진행할까요?
```

### Example 2: 새 파일 작성 시
```
User: 대시보드 컴포넌트 만들어줘

Claude: [작성 중 200줄 도달 시]
⚠️ WARNING: 200줄 도달 - 분리 권장

현재 구조:
- DashboardHeader (40 lines)
- DashboardStats (60 lines)
- DashboardChart (80 lines)
- hooks (20 lines)

각 섹션을 별도 파일로 분리하면서 계속 진행할까요?
```

### Example 3: 모듈화 요청
```
User: 이 파일 너무 길어, 정리해줘

Claude: [line-limit 스킬 활성화]
📊 현재: 456 lines
🔴 VIOLATION: 156줄 초과

[분석 및 분리 계획 제시...]
```

## References

상세 모듈화 가이드: [references/modularization-guide.md](references/modularization-guide.md)
---
name: verify-bundle-size
description: 코드 스플리팅 효과와 번들 크기를 검증합니다. 빌드 최적화 또는 대형 라이브러리 추가 후 사용.
---

## Purpose

1. **lazy import 효과** - React.lazy로 분리된 청크가 올바르게 생성되는지 검증
2. **대형 의존성 감지** - 번들에 포함된 대형 라이브러리를 식별
3. **직접 import 감지** - lazy load 대상이 직접 import되어 번들에 포함되는 경우 감지
4. **빌드 성공 여부** - TypeScript 빌드가 에러 없이 완료되는지 검증

## When to Run

- 새로운 npm 패키지를 추가한 후
- 대형 컴포넌트의 import 방식을 변경한 후
- Vite 설정을 수정한 후
- 빌드 최적화 작업 후

## Related Files

| File | Purpose |
|------|---------|
| `vite.config.ts` | Vite 빌드 설정 (splitChunks, rollupOptions) |
| `package.json` | 의존성 목록 |
| `components/Layout/TabContent.tsx` | 32개 lazy import (코드 스플리팅 핵심) |
| `components/Timetable/TimetableManager.tsx` | 7개 lazy import |
| `index.tsx` | 앱 진입점 |

## Workflow

### Step 1: TypeScript 타입 체크

**검사:** TypeScript 컴파일이 에러 없이 완료되는지 확인합니다.

```bash
npx tsc --noEmit 2>&1 | tail -5
```

**PASS 기준:** 에러 없음 (0 errors)
**FAIL 기준:** 타입 에러 존재

### Step 2: Vite 빌드 실행

**검사:** 프로덕션 빌드가 성공하는지 확인합니다.

```bash
npx vite build 2>&1 | tail -20
```

**PASS 기준:** 빌드 성공 + 청크 파일 생성
**FAIL 기준:** 빌드 에러

### Step 3: 생성된 청크 분석

**검사:** dist/ 디렉토리에 코드 스플리팅된 청크 파일이 존재하는지 확인합니다.

```bash
ls -la dist/assets/*.js 2>/dev/null | wc -l
ls -lh dist/assets/*.js 2>/dev/null | sort -k5 -h | tail -10
```

**PASS 기준:** 10개 이상의 JS 청크 파일 생성 (20개 lazy import → 최소 10개 청크)
**FAIL 기준:** 청크 파일이 너무 적음 (코드 스플리팅 미작동)

### Step 4: 메인 번들 크기 검증

**검사:** 메인 번들(index 또는 app)이 과도하게 크지 않은지 확인합니다.

```bash
ls -lh dist/assets/index*.js 2>/dev/null
```

**PASS 기준:** 메인 번들 500KB 미만 (gzip 전)
**FAIL 기준:** 메인 번들이 500KB 초과 (lazy import 누락 가능)

### Step 5: 대형 의존성 체크

**검사:** package.json에서 알려진 대형 라이브러리의 직접 import 여부를 확인합니다.

```bash
grep -rn "import.*from 'chart.js'\|import.*from 'moment'\|import.*from 'lodash'" components/ hooks/ 2>/dev/null | head -10
```

**PASS 기준:** 대형 라이브러리의 전체 import 없음 (tree-shakeable import만 사용)
**FAIL 기준:** `import _ from 'lodash'` 같은 전체 import 발견

**수정:** `import { debounce } from 'lodash'` 또는 `import debounce from 'lodash/debounce'`로 변경

### Step 6: dynamic import 패턴 검증

**검사:** TabContent와 TimetableManager에서 lazy import 수가 유지되는지 확인합니다.

```bash
echo "TabContent lazy: $(grep -c 'React.lazy(' components/Layout/TabContent.tsx 2>/dev/null)"
echo "TimetableManager lazy: $(grep -c 'lazy(' components/Timetable/TimetableManager.tsx 2>/dev/null)"
```

**PASS 기준:** TabContent 30개+, TimetableManager 5개+ lazy import
**FAIL 기준:** lazy import 수 감소

## Output Format

| # | 검사 항목 | 결과 | 상세 |
|---|----------|------|------|
| 1 | TypeScript 타입 체크 | PASS/FAIL | N개 에러 |
| 2 | Vite 빌드 | PASS/FAIL | |
| 3 | 청크 파일 수 | INFO | N개 생성 |
| 4 | 메인 번들 크기 | PASS/FAIL | NKB |
| 5 | 대형 의존성 | PASS/FAIL | |
| 6 | lazy import 카운트 | PASS/FAIL | TabContent: N, Timetable: N |

## Exceptions

다음은 **위반이 아닙니다**:

1. **vendor 청크의 대형 크기** - React, Firebase 등 외부 라이브러리가 포함된 vendor 청크는 크기가 클 수 있음
2. **빌드 경고(warning)** - TypeScript strict 경고나 unused variable 경고는 빌드 실패가 아님
3. **CSS 파일 크기** - TailwindCSS의 CSS 파일은 이 스킬의 범위 밖
4. **dev 의존성** - devDependencies에 있는 대형 라이브러리(vitest, storybook 등)는 프로덕션 번들에 포함되지 않음

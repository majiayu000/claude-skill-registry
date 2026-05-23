---
name: verify-test-coverage
description: hooks/utils의 테스트 파일 존재 여부를 검증합니다. 새 훅/유틸 추가 후 사용.
---

## Purpose

1. **훅 테스트 커버리지** - `hooks/` 디렉토리의 모든 훅 파일에 대응하는 테스트 파일이 `tests/hooks/`에 존재하는지 검증
2. **유틸리티 테스트 커버리지** - `utils/` 디렉토리의 모든 유틸 파일에 대응하는 테스트 파일이 `tests/utils/`에 존재하는지 검증
3. **테스트 파일 확장자 규칙** - JSX를 사용하는 테스트는 `.test.tsx`, 그 외는 `.test.ts` 확장자 사용 검증
4. **고아 테스트 파일** - 소스 파일이 삭제되었지만 테스트 파일만 남아있는 경우 감지

## When to Run

- 새 훅(`hooks/*.ts`)을 추가한 후
- 새 유틸리티(`utils/*.ts`)를 추가한 후
- 훅/유틸 파일을 삭제하거나 이름을 변경한 후
- PR 전 테스트 완성도를 확인할 때

## Related Files

| File | Purpose |
|------|---------|
| `hooks/` | 70개 커스텀 훅 파일 |
| `utils/` | 22개 유틸리티 파일 |
| `tests/hooks/` | 훅 테스트 파일 |
| `tests/utils/` | 유틸리티 테스트 파일 |
| `tests/components/` | 컴포넌트 테스트 파일 |
| `vitest.config.ts` | Vitest 설정 |

## Workflow

### Step 1: 훅 테스트 파일 존재 검증

**검사:** `hooks/` 디렉토리의 각 `.ts`/`.tsx` 파일에 대응하는 `tests/hooks/<name>.test.ts` 또는 `tests/hooks/<name>.test.tsx`가 존재해야 합니다.

```bash
for f in hooks/*.ts hooks/*.tsx; do
  base=$(basename "$f" | sed 's/\.tsx\?$//');
  if [ ! -f "tests/hooks/${base}.test.ts" ] && [ ! -f "tests/hooks/${base}.test.tsx" ]; then
    echo "MISSING TEST: $f -> tests/hooks/${base}.test.ts";
  fi;
done
```

**PASS 기준:** 모든 훅에 대응 테스트 파일 존재 (출력 없음)
**FAIL 기준:** "MISSING TEST" 출력이 1개 이상

**수정:** 누락된 테스트 파일을 생성. Vitest globals 패턴 사용 (describe/it/expect를 import하지 않음)

### Step 2: 유틸리티 테스트 파일 존재 검증

**검사:** `utils/` 디렉토리의 각 `.ts` 파일에 대응하는 `tests/utils/<name>.test.ts`가 존재해야 합니다.

```bash
for f in utils/*.ts; do
  base=$(basename "$f" | sed 's/\.ts$//');
  if [ ! -f "tests/utils/${base}.test.ts" ]; then
    echo "MISSING TEST: $f -> tests/utils/${base}.test.ts";
  fi;
done
```

**PASS 기준:** 모든 유틸에 대응 테스트 파일 존재 (출력 없음)
**FAIL 기준:** "MISSING TEST" 출력이 1개 이상

**수정:** 누락된 테스트 파일 생성

### Step 3: 테스트 파일 확장자 규칙 검증

**검사:** JSX를 사용하는 테스트 파일은 반드시 `.test.tsx` 확장자를 사용해야 합니다. `.test.ts` 확장자에서 JSX를 사용하면 Vitest가 파싱 에러를 발생시킵니다.

```bash
grep -rl "React.createElement\|<.*>" tests/hooks/*.test.ts tests/utils/*.test.ts 2>/dev/null | head -10
```

**PASS 기준:** `.test.ts` 파일에서 JSX/createElement 사용 없음
**FAIL 기준:** `.test.ts` 파일에서 JSX 패턴 발견

**수정:** 해당 파일의 확장자를 `.test.tsx`로 변경

### Step 4: 고아 테스트 파일 감지

**검사:** 테스트 파일이 존재하지만 대응하는 소스 파일이 없는 경우를 감지합니다.

```bash
for f in tests/hooks/*.test.ts tests/hooks/*.test.tsx; do
  [ -f "$f" ] || continue;
  base=$(basename "$f" | sed 's/\.test\.tsx\?$//');
  if [ ! -f "hooks/${base}.ts" ] && [ ! -f "hooks/${base}.tsx" ]; then
    echo "ORPHAN TEST: $f (no source: hooks/${base}.ts)";
  fi;
done
```

```bash
for f in tests/utils/*.test.ts; do
  [ -f "$f" ] || continue;
  base=$(basename "$f" | sed 's/\.test\.ts$//');
  if [ ! -f "utils/${base}.ts" ]; then
    echo "ORPHAN TEST: $f (no source: utils/${base}.ts)";
  fi;
done
```

**PASS 기준:** 고아 테스트 파일 없음
**FAIL 기준:** "ORPHAN TEST" 출력 존재

**수정:** 소스 파일 경로가 변경된 경우 테스트 파일의 import 경로 업데이트, 소스가 완전히 삭제된 경우 테스트 파일도 삭제

### Step 5: 테스트 파일 카운트 요약

**검사:** 현재 테스트 파일 수를 보고합니다.

```bash
echo "Hook tests: $(ls tests/hooks/*.test.* 2>/dev/null | wc -l)"
echo "Util tests: $(ls tests/utils/*.test.* 2>/dev/null | wc -l)"
echo "Component tests: $(ls tests/components/*.test.* 2>/dev/null | wc -l)"
echo "Total hooks: $(ls hooks/*.ts hooks/*.tsx 2>/dev/null | wc -l)"
echo "Total utils: $(ls utils/*.ts 2>/dev/null | wc -l)"
```

**정보:** 이 단계는 PASS/FAIL이 아닌 현황 보고입니다.

## Output Format

| # | 검사 항목 | 범위 | 결과 | 상세 |
|---|----------|------|------|------|
| 1 | 훅 테스트 존재 | hooks/ → tests/hooks/ | PASS/FAIL | N개 누락 |
| 2 | 유틸 테스트 존재 | utils/ → tests/utils/ | PASS/FAIL | N개 누락 |
| 3 | 확장자 규칙 | tests/**/*.test.ts | PASS/FAIL | N개 위반 |
| 4 | 고아 테스트 | tests/ | PASS/FAIL | N개 고아 |
| 5 | 카운트 요약 | 전체 | INFO | 훅:N, 유틸:N, 컴포넌트:N |

## Exceptions

다음은 **위반이 아닙니다**:

1. **`tests/setup.test.ts`** - Vitest 설정 테스트 파일로, 특정 소스 파일에 대응하지 않음
2. **`tests/components/` 하위 테스트** - 컴포넌트 테스트는 1:1 매핑이 아닌 기능 단위로 작성될 수 있음 (예: `ClassCard.StudentItem.test.tsx`는 `ClassCard.tsx`의 하위 컴포넌트 테스트)
3. **컴포넌트 내부 훅** - `components/*/hooks/` 하위의 훅은 해당 컴포넌트 도메인에 특화되어 있어 별도 규칙 적용 (이 스킬은 `hooks/` 최상위만 검증)
4. **`converters.ts` 테스트** - 루트의 `converters.ts`는 `tests/utils/converters.test.ts`에서 테스트됨 (경로가 다르지만 정상)
5. **`useStudentDragDrop.test.ts`** - `components/Timetable/Math/hooks/useStudentDragDrop.ts`를 테스트하는 파일. 소스가 컴포넌트 내부 훅이므로 `tests/hooks/`에 배치되어도 고아가 아님
6. **`useSimulationContext.test.tsx`** - `components/Timetable/Math/context/SimulationContext.tsx`를 테스트하는 파일. 소스가 컴포넌트 컨텍스트이므로 `tests/hooks/`에 배치되어도 고아가 아님

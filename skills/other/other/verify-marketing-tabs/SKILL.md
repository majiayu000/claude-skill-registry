---
name: verify-marketing-tabs
description: 마케팅 그룹(마케팅/셔틀관리) 탭의 핵심 기능을 검증합니다. 마케팅 관련 컴포넌트 수정 후 사용.
---

## Purpose

1. **마케팅 캠페인 관리** - 캠페인 생성/수정/삭제/통계 기능이 올바르게 동작하는지 검증
2. **셔틀 관리** - 셔틀 노선/시간표/학생 배정 기능이 정상 동작하는지 검증

## When to Run

- `components/Marketing/` 하위 파일을 수정한 후
- `components/Shuttle/` 수정 후
- `hooks/useMarketing.ts`, `hooks/useShuttle.ts` 수정 후
- 마케팅 관련 mutation 훅을 변경한 후

## Related Files

| File | Purpose |
|------|---------|
| `components/Marketing/MarketingTab.tsx` | 마케팅 메인 |
| `components/Shuttle/ShuttleTab.tsx` | 셔틀 관리 메인 |
| `hooks/useMarketing.ts` | 마케팅 데이터 + mutation (4 mutations) |
| `hooks/useShuttle.ts` | 셔틀 데이터 + mutation (4 mutations) |

## Workflow

### Step 1: 마케팅 그룹 탭 lazy import 검증

**검사:** 2개 탭 컴포넌트가 TabContent에서 lazy import되는지 확인합니다.

```bash
grep -n "MarketingTab\|ShuttleTab" components/Layout/TabContent.tsx
```

**PASS 기준:** 2개 컴포넌트가 모두 React.lazy로 import됨
**FAIL 기준:** 하나 이상의 탭 컴포넌트 누락

### Step 2: 마케팅 mutation 훅 검증

**검사:** useMarketing 훅이 존재하고 useQuery를 사용하여 데이터를 조회하는지 확인합니다.

```bash
grep -c "useQuery" hooks/useMarketing.ts 2>/dev/null
```

**PASS 기준:** useQuery 1개 이상 존재 (현재 조회 전용, mutation은 향후 추가 예정)
**FAIL 기준:** 훅 파일 없거나 쿼리 없음

### Step 3: 셔틀 관리 mutation 훅 검증

**검사:** useShuttle 훅이 존재하고 useMutation을 사용하는지 확인합니다.

```bash
grep -c "useMutation" hooks/useShuttle.ts 2>/dev/null
```

**PASS 기준:** 1개 이상의 mutation 존재 (현재 createRoute, 추가 mutation 향후 구현 예정)
**FAIL 기준:** mutation이 0개

### Step 4: 마케팅 그룹 권한 설정 검증

**검사:** types/system.ts에서 마케팅 그룹 탭의 권한이 올바르게 정의되어 있는지 확인합니다.

```bash
grep -n "marketing\|shuttle" types/system.ts | head -10
```

**PASS 기준:** 2개 탭이 DEFAULT_TAB_PERMISSIONS에 포함됨
**FAIL 기준:** 권한 정의 누락

### Step 5: TabContent 라우팅 검증

**검사:** TabContent에서 마케팅 그룹 탭이 올바르게 라우팅되는지 확인합니다.

```bash
grep -n "marketing\|shuttle" components/Layout/TabContent.tsx | head -10
```

**PASS 기준:** appMode 조건 분기에 marketing, shuttle이 포함됨
**FAIL 기준:** 라우팅 누락

## Output Format

| # | 검사 항목 | 범위 | 결과 | 상세 |
|---|----------|------|------|------|
| 1 | 2개 탭 lazy import | TabContent.tsx | PASS/FAIL | |
| 2 | 마케팅 mutation | useMarketing.ts | PASS/FAIL | N개 mutation |
| 3 | 셔틀 mutation | useShuttle.ts | PASS/FAIL | N개 mutation |
| 4 | 마케팅 그룹 권한 | types/system.ts | PASS/FAIL | |
| 5 | TabContent 라우팅 | TabContent.tsx | PASS/FAIL | |

## Exceptions

다음은 **위반이 아닙니다**:

1. **MarketingTab의 간소한 구조** - 마케팅은 캠페인 목록/생성 위주의 단순 구조로 별도 서브 컴포넌트가 적을 수 있음
2. **ShuttleTab의 지도 미연동** - 초기 구현에서는 노선/시간표 관리만 포함하고 지도 연동은 추후 추가 가능
3. **master/admin 전용 접근** - 마케팅 그룹 탭이 master/admin 역할에만 허용되는 것은 보안 설계에 따른 정상 동작

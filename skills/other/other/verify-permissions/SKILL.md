---
name: verify-permissions
description: 역할별 탭 접근권한, 버튼 노출, 권한 체크 로직을 검증합니다. 권한/역할 관련 코드 수정 후 사용.
---

## Purpose

1. **역할-탭 매핑 정합성** - types/system.ts의 DEFAULT_TAB_PERMISSIONS와 실제 UI 동작이 일치하는지 검증
2. **usePermissions 훅 사용** - 권한이 필요한 컴포넌트에서 usePermissions를 올바르게 호출하는지 검증
3. **useTabPermissions 필터링** - Sidebar에서 역할에 따라 탭이 올바르게 필터링되는지 검증
4. **권한 기반 UI 분기** - 버튼/메뉴의 조건부 렌더링이 역할에 따라 올바르게 동작하는지 검증

## When to Run

- `types/system.ts`의 역할 또는 탭 권한을 수정한 후
- `hooks/usePermissions.ts` 또는 `hooks/useTabPermissions.ts` 수정 후
- 관리자 전용 기능을 추가하거나 수정한 후
- 새로운 역할(role)을 추가한 후
- `components/Navigation/Sidebar.tsx` 수정 후

## Related Files

| File | Purpose |
|------|---------|
| `types/system.ts` | AppTab 타입, TAB_META, TAB_GROUPS, DEFAULT_TAB_PERMISSIONS 정의 |
| `hooks/usePermissions.ts` | 핵심 권한 검증 훅 |
| `hooks/useTabPermissions.ts` | 탭 접근 권한 필터링 훅 |
| `hooks/useRoleHelpers.ts` | 역할 유틸리티 |
| `hooks/useAuth.ts` | 인증 상태 (현재 사용자 역할) |
| `components/Navigation/Sidebar.tsx` | 사이드바 (탭 접근 필터링 적용) |
| `components/Layout/TabContent.tsx` | 탭 라우팅 |
| `components/RoleManagement/RoleManagementPage.tsx` | 역할 관리 UI |
| `utils/roleHelpers.ts` | 역할 관련 유틸리티 함수 |

## Workflow

### Step 1: 8개 역할 정의 완전성 검증

**검사:** types/system.ts에 8개 역할이 모두 정의되어 있는지 확인합니다.

```bash
grep -n "master\|admin\|manager\|math_lead\|english_lead\|math_teacher\|english_teacher\|'user'" types/system.ts | head -20
```

**PASS 기준:** 8개 역할(master, admin, manager, math_lead, english_lead, math_teacher, english_teacher, user) 모두 참조
**FAIL 기준:** 역할 정의 누락

### Step 2: DEFAULT_TAB_PERMISSIONS 구조 검증

**검사:** 모든 역할에 대해 허용 탭 배열이 정의되어 있는지 확인합니다.

```bash
grep -A 2 "DEFAULT_TAB_PERMISSIONS" types/system.ts | head -15
```

**PASS 기준:** DEFAULT_TAB_PERMISSIONS에 8개 역할의 키가 존재
**FAIL 기준:** 역할 키 누락

### Step 3: useTabPermissions 훅 → Sidebar 연결 검증

**검사:** Sidebar에서 useTabPermissions를 사용하여 탭을 필터링하는지 확인합니다.

```bash
grep -n "useTabPermissions\|accessibleTabs\|filteredTabs" components/Navigation/Sidebar.tsx | head -5
```

**PASS 기준:** Sidebar에서 탭 필터링 로직 존재
**FAIL 기준:** Sidebar가 권한 없이 모든 탭을 표시

**수정:** `const accessibleTabs = useTabPermissions()` 추가 후 탭 목록 필터링

### Step 4: 관리자 전용 탭 접근 제한 검증

**검사:** payment, role-management 탭이 일반 교사(math_teacher, english_teacher) 역할에서 제외되는지 확인합니다.

```bash
grep -A 5 "math_teacher\|english_teacher" types/system.ts | grep -v "payment\|role-management" | head -10
```

**PASS 기준:** 교사 역할의 탭 목록에 payment, role-management가 포함되지 않음
**FAIL 기준:** 교사가 관리자 전용 탭에 접근 가능

### Step 5: usePermissions import 확인

**검사:** 권한 체크가 필요한 주요 관리 컴포넌트에서 usePermissions를 import하는지 확인합니다.

```bash
grep -rl "usePermissions" components/Staff/ components/Billing/ components/RoleManagement/ components/PaymentReport/ 2>/dev/null
```

**PASS 기준:** 관리 탭의 주요 컴포넌트에서 usePermissions 사용
**FAIL 기준:** 권한 체크 없이 관리 기능 접근 가능

### Step 6: AppTab 타입과 TAB_META 동기화 검증

**검사:** AppTab 유니온 타입의 모든 값이 TAB_META에도 정의되어 있는지 확인합니다.

```bash
grep -c "AppTab" types/system.ts
grep "'dashboard'\|'calendar'\|'timetable'\|'payment'\|'gantt'\|'consultation'\|'attendance'\|'students'\|'grades'\|'classes'\|'classroom'\|'classroom-assignment'\|'student-consultations'\|'staff'\|'daily-attendance'\|'billing'\|'role-management'\|'resources'\|'withdrawal'\|'help'" types/system.ts | head -5
```

**PASS 기준:** AppTab의 모든 값(19개+)이 TAB_META에 메타데이터가 존재
**FAIL 기준:** 탭 타입은 있지만 메타데이터가 없는 탭 존재

## Output Format

| # | 검사 항목 | 범위 | 결과 | 상세 |
|---|----------|------|------|------|
| 1 | 8개 역할 정의 | types/system.ts | PASS/FAIL | |
| 2 | DEFAULT_TAB_PERMISSIONS | types/system.ts | PASS/FAIL | |
| 3 | Sidebar 탭 필터링 | Sidebar.tsx | PASS/FAIL | |
| 4 | 관리자 전용 탭 제한 | types/system.ts | PASS/FAIL | |
| 5 | usePermissions 사용 | 관리 컴포넌트 | PASS/FAIL | N개 파일 |
| 6 | AppTab-TAB_META 동기화 | types/system.ts | PASS/FAIL | |

## Exceptions

다음은 **위반이 아닙니다**:

1. **대시보드와 도움말의 전체 접근** - dashboard, help 탭은 모든 역할에서 접근 가능한 것이 정상
2. **useRoleSimulation의 권한 우회** - 개발/테스트 환경에서 역할 시뮬레이션은 실제 권한 체크를 우회할 수 있음
3. **컴포넌트 내부 권한 체크와 탭 필터링의 중복** - 탭 레벨과 컴포넌트 레벨에서 이중으로 권한을 체크하는 것은 보안 심층 방어 패턴

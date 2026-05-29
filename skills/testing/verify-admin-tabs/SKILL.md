---
name: verify-admin-tabs
description: 관리 그룹(수강료현황/직원관리/수납관리/자료실/역할관리/통계분석/급여관리) 탭의 핵심 기능을 검증합니다. 관리 관련 컴포넌트 수정 후 사용.
---

## Purpose

1. **직원 관리 CRUD** - 직원 등록/수정/삭제 및 연관 데이터(수업, 학생) 업데이트가 올바른지 검증
2. **수납 관리 흐름** - 수납 등록/조회/통계/import 기능이 정상 동작하는지 검증
3. **자료실 구조** - 자료 업로드/조회/미리보기 기능이 올바르게 연결되어 있는지 검증
4. **역할 관리 권한** - 역할별 탭 접근 권한 설정이 types/system.ts와 일치하는지 검증
5. **수강료 현황 보고** - PaymentReport의 차트/폼 컴포넌트가 올바르게 연결되어 있는지 검증
6. **통계 분석** - AnalyticsTab의 대시보드/차트 컴포넌트가 올바르게 연결되어 있는지 검증
7. **급여 관리** - PayrollTab의 급여 계산/내역 컴포넌트가 올바르게 연결되어 있는지 검증

## When to Run

- `components/Staff/`, `components/Billing/`, `components/Resources/` 수정 후
- `components/PaymentReport/`, `components/RoleManagement/` 수정 후
- `hooks/useStaff.ts`, `hooks/useBilling.ts`, `hooks/useResources.ts` 수정 후
- `hooks/useStaffLeaves.ts` 수정 후
- `types/system.ts`의 역할/권한 정의를 변경한 후

## Related Files

| File | Purpose |
|------|---------|
| `components/PaymentReport/PaymentReport.tsx` | 전자 결재 메인 |
| `components/PaymentReport/TuitionChart.tsx` | 수납 차트 |
| `components/PaymentReport/EntryForm.tsx` | 결재 입력 폼 |
| `components/Staff/StaffManager.tsx` | 직원 관리 메인 |
| `components/Staff/StaffList.tsx` | 직원 목록 |
| `components/Staff/StaffForm.tsx` | 직원 등록/수정 폼 |
| `components/Staff/StaffViewModal.tsx` | 직원 상세 모달 |
| `components/Staff/LeaveManagement.tsx` | 휴가 관리 |
| `components/Billing/BillingManager.tsx` | 수납 관리 메인 (lazy loading) |
| `components/Billing/BillingTable.tsx` | 수납 테이블 |
| `components/Billing/BillingForm.tsx` | 수납 입력 폼 |
| `components/Billing/BillingStats.tsx` | 수납 통계 |
| `components/Billing/BillingImportModal.tsx` | 수납 데이터 import |
| `components/Resources/ResourceDashboard.tsx` | 자료실 대시보드 |
| `components/Resources/ResourceCard.tsx` | 자료 카드 |
| `components/Resources/ResourceAddModal.tsx` | 자료 추가 모달 |
| `components/Resources/ResourcePreviewPanel.tsx` | 자료 미리보기 |
| `components/RoleManagement/RoleManagementPage.tsx` | 역할 관리 페이지 |
| `hooks/useStaff.ts` | 직원 데이터 + mutation (4 mutations, cascade 업데이트) |
| `hooks/useStaffLeaves.ts` | 휴가 관리 (5 mutations) |
| `hooks/useBilling.ts` | 수납 데이터 + mutation (5 mutations) |
| `hooks/useResources.ts` | 자료 데이터 + mutation (4 mutations) |
| `hooks/usePermissions.ts` | 권한 검증 훅 |
| `hooks/useTabPermissions.ts` | 탭 접근 권한 훅 |
| `types/system.ts` | 역할별 탭 접근 권한 정의 |
| `components/Analytics/AnalyticsTab.tsx` | 통계 분석 메인 |
| `components/Payroll/PayrollTab.tsx` | 급여 관리 메인 |
| `hooks/usePayroll.ts` | 급여 데이터 + mutation (4 mutations) |

## Workflow

### Step 1: 관리 그룹 탭 lazy import 검증

**검사:** 7개 탭 컴포넌트가 TabContent에서 lazy import되는지 확인합니다.

```bash
grep -n "PaymentReport\|StaffManager\|BillingManager\|ResourceDashboard\|RoleManagementPage\|AnalyticsTab\|PayrollTab" components/Layout/TabContent.tsx
```

**PASS 기준:** 7개 컴포넌트가 모두 React.lazy로 import됨
**FAIL 기준:** 하나 이상의 탭 컴포넌트 누락

### Step 2: 직원 관리 cascade 업데이트 검증

**검사:** useStaff의 직원명 변경 시 연관 데이터(수업, 학생)를 함께 업데이트하는 cascade 로직이 존재하는지 확인합니다.

```bash
grep -n "cascade\|teacher.*newName\|updateDoc.*teacher" hooks/useStaff.ts | head -10
```

**PASS 기준:** cascade 업데이트 또는 연관 데이터 일괄 업데이트 로직 존재
**FAIL 기준:** 직원명 변경 시 연관 데이터 미갱신

### Step 3: 수납 관리 4대 컴포넌트 연결 검증

**검사:** BillingManager에서 Table, Form, Stats, ImportModal이 모두 연결되어 있는지 확인합니다.

```bash
grep -n "BillingTable\|BillingForm\|BillingStats\|BillingImportModal" components/Billing/BillingManager.tsx | head -10
```

**PASS 기준:** 4개 하위 컴포넌트 모두 참조됨
**FAIL 기준:** 핵심 컴포넌트 연결 누락

### Step 4: 자료실 CRUD 모달 검증

**검사:** ResourceDashboard에서 자료 추가 모달과 카드 컴포넌트가 연결되어 있는지 확인합니다.

```bash
grep -n "ResourceAddModal\|ResourceCard" components/Resources/ResourceDashboard.tsx | head -10
```

**PASS 기준:** ResourceAddModal과 ResourceCard가 참조됨
**FAIL 기준:** 추가 모달 또는 카드 컴포넌트 연결 누락

### Step 5: 역할별 탭 접근 권한 정합성 검증

**검사:** types/system.ts에 정의된 역할별 허용 탭이 useTabPermissions에서 올바르게 참조되는지 확인합니다.

```bash
grep -n "DEFAULT_TAB_PERMISSIONS\|master\|admin\|manager\|math_lead\|english_lead\|math_teacher\|english_teacher\|user" types/system.ts | head -20
```

**PASS 기준:** 8개 역할(master, admin, manager, math_lead, english_lead, math_teacher, english_teacher, user)의 권한이 모두 정의됨
**FAIL 기준:** 역할 정의 누락 또는 불일치

### Step 6: 직원 휴가 관리 연결 검증

**검사:** StaffManager에서 LeaveManagement 컴포넌트가 연결되어 있는지 확인합니다.

```bash
grep -n "LeaveManagement\|StaffSchedule" components/Staff/StaffManager.tsx | head -5
```

**PASS 기준:** 휴가 관리 또는 스케줄 컴포넌트 참조 존재
**FAIL 기준:** 휴가 관리 기능이 분리됨

### Step 7: PaymentReport 구성요소 검증

**검사:** PaymentReport에서 TuitionChart와 EntryForm이 연결되어 있는지 확인합니다.

```bash
grep -n "TuitionChart\|EntryForm" components/PaymentReport/PaymentReport.tsx | head -5
```

**PASS 기준:** 차트와 폼 컴포넌트 모두 참조됨
**FAIL 기준:** 구성요소 연결 누락

## Output Format

| # | 검사 항목 | 범위 | 결과 | 상세 |
|---|----------|------|------|------|
| 1 | 7개 탭 lazy import | TabContent.tsx | PASS/FAIL | |
| 2 | 직원 cascade 업데이트 | useStaff.ts | PASS/FAIL | |
| 3 | 수납 4대 컴포넌트 | BillingManager | PASS/FAIL | |
| 4 | 자료실 CRUD 모달 | ResourceDashboard | PASS/FAIL | |
| 5 | 역할별 탭 권한 | types/system.ts | PASS/FAIL | N개 역할 |
| 6 | 직원 휴가 연결 | StaffManager | PASS/FAIL | |
| 7 | 결재 보고 구성 | PaymentReport | PASS/FAIL | |

## Exceptions

다음은 **위반이 아닙니다**:

1. **RoleManagementPage의 단일 파일 구조** - 역할 관리는 단일 페이지로 충분하며 별도 하위 컴포넌트가 없어도 정상
2. **useStaff cascade에서 Korean name만 업데이트** - `teacher: newName`은 항상 한국어 이름을 사용하며, English name은 별도 필드로 관리
3. **BillingManager의 내부 lazy loading** - 수납 관리가 자체적으로 컴포넌트를 lazy load하는 것은 정상 패턴
4. **PaymentReport가 admin 전용** - master/admin 역할만 접근 가능한 것은 보안 설계에 따른 정상 동작
5. **Resources의 StaffLinkModal 참조 없음** - StaffLinkModal은 Staff 탭 전용이며 Resources에서는 사용하지 않음

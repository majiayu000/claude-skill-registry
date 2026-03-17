---
name: verify-comm-tabs
description: 소통 그룹(공지사항/학부모포털/알림센터) 탭의 핵심 기능을 검증합니다. 소통 관련 컴포넌트 수정 후 사용.
---

## Purpose

1. **공지사항 CRUD** - 공지 작성/수정/삭제/고정 기능이 올바르게 동작하는지 검증
2. **학부모 포털 연동** - 학부모 계정 연동/메시지 전송/알림 기능이 올바른지 검증
3. **알림 센터** - 알림 목록/읽음 처리/설정 기능이 정상 동작하는지 검증

## When to Run

- `components/Notices/` 하위 파일을 수정한 후
- `components/ParentPortal/` 또는 `components/Notifications/` 수정 후
- `hooks/useNotices.ts`, `hooks/useParentLinks.ts`, `hooks/useParentMessages.ts`, `hooks/useNotifications.ts` 수정 후
- 소통 관련 mutation 훅을 변경한 후

## Related Files

| File | Purpose |
|------|---------|
| `components/Notices/NoticesTab.tsx` | 공지사항 메인 |
| `components/ParentPortal/ParentPortalTab.tsx` | 학부모 포털 메인 |
| `components/Notifications/NotificationsTab.tsx` | 알림 센터 메인 |
| `hooks/useNotices.ts` | 공지사항 데이터 + mutation (4 mutations) |
| `hooks/useParentLinks.ts` | 학부모 연동 (3 mutations) |
| `hooks/useParentMessages.ts` | 학부모 메시지 (3 mutations) |
| `hooks/useNotifications.ts` | 알림 데이터 + mutation (4 mutations) |

## Workflow

### Step 1: 소통 그룹 탭 lazy import 검증

**검사:** 3개 탭 컴포넌트가 TabContent에서 lazy import되는지 확인합니다.

```bash
grep -n "NoticesTab\|ParentPortalTab\|NotificationsTab" components/Layout/TabContent.tsx
```

**PASS 기준:** 3개 컴포넌트가 모두 React.lazy로 import됨
**FAIL 기준:** 하나 이상의 탭 컴포넌트 누락

### Step 2: 공지사항 mutation 훅 검증

**검사:** useNotices 훅이 존재하고 useMutation을 사용하는지 확인합니다.

```bash
grep -c "useMutation" hooks/useNotices.ts 2>/dev/null
```

**PASS 기준:** 3개 이상의 mutation 존재 (생성/수정/삭제)
**FAIL 기준:** mutation 수가 예상보다 적음

### Step 3: 학부모 포털 훅 연결 검증

**검사:** ParentPortalTab에서 학부모 관련 훅이 사용되는지 확인합니다.

```bash
grep -n "useParentLinks\|useParentMessages" components/ParentPortal/ParentPortalTab.tsx | head -5
```

**PASS 기준:** 학부모 관련 훅 사용 확인
**FAIL 기준:** 훅 연결 누락

### Step 4: 알림 센터 mutation 훅 검증

**검사:** useNotifications 훅이 존재하고 useMutation을 사용하는지 확인합니다.

```bash
grep -c "useMutation" hooks/useNotifications.ts 2>/dev/null
```

**PASS 기준:** 2개 이상의 mutation 존재 (createTemplate, sendNotification)
**FAIL 기준:** mutation 수가 2개 미만

### Step 5: 소통 그룹 권한 설정 검증

**검사:** types/system.ts에서 소통 그룹 탭의 권한이 올바르게 정의되어 있는지 확인합니다.

```bash
grep -n "notices\|parent-portal\|notifications" types/system.ts | head -10
```

**PASS 기준:** 3개 탭이 DEFAULT_TAB_PERMISSIONS에 포함됨
**FAIL 기준:** 권한 정의 누락

## Output Format

| # | 검사 항목 | 범위 | 결과 | 상세 |
|---|----------|------|------|------|
| 1 | 3개 탭 lazy import | TabContent.tsx | PASS/FAIL | |
| 2 | 공지사항 mutation | useNotices.ts | PASS/FAIL | N개 mutation |
| 3 | 학부모 포털 훅 연결 | ParentPortalTab | PASS/FAIL | |
| 4 | 알림 센터 mutation | useNotifications.ts | PASS/FAIL | N개 mutation |
| 5 | 소통 그룹 권한 | types/system.ts | PASS/FAIL | |

## Exceptions

다음은 **위반이 아닙니다**:

1. **NoticesTab의 역할 기반 권한 체크** - usePermissions 대신 직접 role 체크를 사용하는 것은 PermissionId에 notices.edit가 없기 때문에 정상
2. **ParentPortalTab의 간소한 구조** - 학부모 포털은 연동/메시지 기능 위주로 별도 서브탭 없이 단일 뷰로 구성 가능
3. **NotificationsTab의 읽기 위주 구조** - 알림 센터는 읽음 처리와 설정만 mutation이며 알림 생성은 서버 측에서 처리

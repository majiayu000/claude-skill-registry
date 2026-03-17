---
name: ipc-development
description: IPC 채널 추가/수정 시 안전 규칙과 절차
---

# IPC Development Guide

## Single Source of Truth

모든 IPC 채널은 `src/shared/ipc-schema.ts`에 정의. 이 스키마에서 타입이 자동 추론되므로 별도 타입 정의 불필요.

## 채널 추가 절차

새 IPC 채널 추가 시 **3곳 수정**:

1. `src/shared/ipc-schema.ts` — 채널 + params + return 타입 정의
2. `src/main/ipc.ts` — `handleIpc()` 핸들러 추가
3. `src/preload/index.ts` — `invokeIpc()` 메서드 추가

→ Renderer 타입은 자동 반영

## 반환 타입 규칙

| 채널 유형 | 반환 타입 | 예시 |
|-----------|----------|------|
| 데이터 조회 | 구체적 타입 | `LaunchdJob[]`, `AppSettings` |
| 데이터 변경 (mutation) | `IpcResult` | `{ success: true }` |
| Fire-and-forget | `void` | quit, resize, navigate |

## 에러 처리

`handleIpc` 래퍼가 try/catch 자동 적용:
- 성공 → 핸들러 결과 반환
- 실패 → 에러 로깅 + mutation은 `{ success: false, error: message }` 반환

## 직렬화

- **Date 객체는 IPC를 통과하지 않음** — ISO 8601 문자열(`string`) 사용
- 서비스에서 `.toISOString()` 호출 후 전달
- Renderer에서 `new Date(isoString)` 으로 파싱

## 채널 네이밍

형식: `{domain}:{action}` (액션은 kebab-case)

```
jobs:list              # 조회
jobs:toggle            # 액션
settings:get           # 단일 조회
calendar:add-local-event  # 복합 액션
```

## Renderer에서 사용

**컴포넌트에서 `window.electronAPI` 직접 호출 금지.** 반드시 hooks를 통해 접근:

```typescript
// Bad
const jobs = await window.electronAPI.listJobs();

// Good
const { jobs } = useLaunchdJobs();
```

## plist 파싱

외부 데이터(plist)는 Zod `safeParse`로 런타임 검증:

```typescript
// Bad
const data = plist.parse(content) as PlistData;

// Good
const result = PlistDataSchema.safeParse(plist.parse(content));
if (!result.success) { /* handle error */ }
```

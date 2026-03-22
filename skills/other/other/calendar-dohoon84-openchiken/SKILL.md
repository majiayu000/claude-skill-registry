---
name: calendar
description: Google Calendar 일정 조회, 생성, 삭제
enabled: true
requires_google_auth: true
---

## Google Calendar 일정 도구

사용자의 Google Calendar에서 일정을 조회하고, 생성하고, 삭제합니다.

### 사용 가능한 도구

- **calendar_today**: 오늘의 일정 목록 조회
- **calendar_upcoming**: 향후 N일간 일정 조회 (기본 7일)
- **calendar_create**: 새 일정 생성
- **calendar_delete_by_name**: 이벤트 이름(키워드)으로 일정 검색 후 삭제 (권장)
- **calendar_delete**: 이벤트 ID로 일정 삭제 (사용 비권장)

### 규칙

- 일정을 생성할 때는 반드시 calendar_create 도구를 사용하세요. 직접 응답을 만들지 마세요.
- 일정 시간은 반드시 ISO 8601 형식에 KST 오프셋을 포함하세요 (예: 2025-03-20T09:00:00+09:00).
- 일정을 삭제하기 전에 반드시 사용자에게 확인을 받으세요.
- 삭제 시에는 calendar_delete_by_name을 사용하세요. ID 직접 입력은 오류가 발생할 수 있습니다.

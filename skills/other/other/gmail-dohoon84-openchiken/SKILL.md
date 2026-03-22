---
name: gmail
description: Gmail 이메일 검색, 읽기, 전송
enabled: true
requires_google_auth: true
---

## Gmail 이메일 도구

사용자의 Gmail 계정에서 이메일을 조회, 검색, 읽기, 전송, 답장합니다.

### 사용 가능한 도구

- **gmail_list**: 받은편지함 최근 이메일 목록 조회 (🔵 = 미읽음)
- **gmail_search**: Gmail 검색 문법으로 이메일 목록 조회 (제목/발신자 확인용)
  - 예: `is:unread`, `from:user@example.com`, `subject:회의`
- **gmail_read_latest**: 검색 조건에 맞는 최신 이메일 본문까지 한번에 읽기 (권장)
- **gmail_read**: 메시지 ID로 특정 이메일 본문 읽기
- **gmail_send**: 새 이메일 작성 및 전송
- **gmail_reply**: 기존 이메일에 답장 (스레드 자동 유지)
- **gmail_mark_read**: 이메일을 읽음 처리

### 규칙

- 이메일 목록은 gmail_list를 먼저 사용하세요. 특정 조건 검색은 gmail_search를 사용하세요.
- 이메일을 전송/답장할 때는 반드시 수신자, 제목, 내용을 사용자에게 확인받으세요.
- 이메일 본문을 읽을 때는 gmail_read_latest를 우선 사용하세요.

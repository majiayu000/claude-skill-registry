---
name: workflow
description: 스탠드업 보고, 주간 요약, 미팅 준비 등 복합 업무 자동화
enabled: true
requires_google_auth: true
---

## Workflow 업무 자동화 도구

Gmail, Google Calendar, Drive를 조합한 복합 업무 자동화 도구입니다.
gws workflow와 동일한 기능을 제공합니다.

### 사용 가능한 도구

- **workflow_standup_report**: 오늘 일정 + 미처리 이메일 → 스탠드업 보고 요약
- **workflow_weekly_digest**: 이번 주 일정 + 이메일 현황 → 주간 다이제스트
- **workflow_morning_briefing**: 오늘 날씨·일정·중요 이메일 → 아침 브리핑
- **workflow_meeting_prep**: 다음 미팅 상세 정보 + 관련 이메일/파일 조회
- **workflow_email_to_task**: 이메일 내용을 할 일(메모)로 변환
- **workflow_file_announce**: Drive 파일 링크를 이메일로 공유

### 규칙

- 각 도구는 여러 서비스를 조합하므로 실행 시간이 길 수 있습니다.
- 이메일 전송이 포함된 도구는 반드시 내용을 사용자에게 확인받으세요.
- 사용자가 "스탠드업", "데일리 리포트", "오늘 정리" 등을 요청하면 workflow_standup_report를 사용하세요.
- 사용자가 "주간 요약", "이번 주 정리"를 요청하면 workflow_weekly_digest를 사용하세요.

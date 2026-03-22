---
name: drive
description: Google Drive 파일 조회, 검색, 업로드, 폴더 관리
enabled: true
requires_google_auth: true
---

## Google Drive 도구

사용자의 Google Drive에서 파일을 조회, 검색, 업로드, 관리합니다.

### 사용 가능한 도구

- **drive_list**: 최근 파일 목록 조회 (기본 20개)
- **drive_search**: 파일명·내용·타입으로 검색
- **drive_get**: 텍스트 파일·Google Docs/Sheets 내용 읽기
- **drive_create_folder**: 폴더 생성
- **drive_upload_text**: 텍스트 내용으로 새 파일 생성 (Google Docs 형식)
- **drive_delete**: 파일 또는 폴더 삭제 (ID 필요)
- **drive_move**: 파일을 다른 폴더로 이동

### 규칙

- 파일 삭제 전에 반드시 사용자에게 확인을 받으세요.
- drive_search로 먼저 파일 ID를 확인한 뒤 drive_get을 사용하세요.
- 파일 타입 검색 시: `mimeType='application/vnd.google-apps.document'` (Docs), `mimeType='application/vnd.google-apps.spreadsheet'` (Sheets)

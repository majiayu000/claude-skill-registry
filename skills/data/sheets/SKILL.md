---
name: sheets
description: Google Sheets 스프레드시트 읽기, 쓰기, 생성, 행 추가
enabled: true
requires_google_auth: true
---

## Google Sheets 도구

Google Sheets 스프레드시트의 데이터를 읽고, 쓰고, 새 시트를 만듭니다.

### 사용 가능한 도구

- **sheets_read**: 특정 셀 범위의 데이터 읽기
- **sheets_write**: 특정 셀 범위에 데이터 쓰기
- **sheets_append**: 데이터를 시트 마지막 행에 추가
- **sheets_create**: 새 스프레드시트 생성
- **sheets_info**: 스프레드시트 정보 및 시트 목록 조회
- **sheets_clear**: 특정 범위 데이터 삭제

### 규칙

- 셀 범위 형식: `Sheet1!A1:C10` 또는 `A1:C10` (시트명 생략 시 첫 번째 시트 사용)
- 데이터 쓰기/삭제 전 반드시 사용자에게 확인을 받으세요.
- 스프레드시트 ID는 URL에서 확인: `https://docs.google.com/spreadsheets/d/{ID}/edit`

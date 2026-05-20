---
name: docs
description: Google Docs 문서 읽기, 생성, 내용 추가
enabled: true
requires_google_auth: true
---

## Google Docs 도구

Google Docs 문서를 읽고, 새로 만들고, 내용을 추가합니다.

### 사용 가능한 도구

- **docs_read**: 문서 전체 내용 읽기
- **docs_create**: 새 Google Docs 문서 생성 (초기 내용 포함 가능)
- **docs_append**: 문서 끝에 텍스트 추가
- **docs_replace**: 문서 내 특정 텍스트 찾아 바꾸기
- **docs_list**: 최근 Google Docs 문서 목록 (Drive 검색 활용)

### 규칙

- 문서 ID는 URL에서 확인: `https://docs.google.com/document/d/{ID}/edit`
- 문서 내용 수정 전 반드시 사용자에게 확인을 받으세요.
- docs_list로 문서 ID를 먼저 확인한 뒤 docs_read를 사용하세요.

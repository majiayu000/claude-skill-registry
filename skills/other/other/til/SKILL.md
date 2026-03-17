---
name: til
description: "Today I Learned - 주제를 리서치하고 대화형으로 학습한 뒤 TIL 마크다운으로 저장"
argument-hint: "<주제> [카테고리]"
plugin-version: "__PLUGIN_VERSION__"
---

# TIL Skill

주제 리서치 → 대화형 학습 → TIL 저장.

## MCP 도구

- `til_list`: 기존 TIL 확인 (동일/유사 주제 감지)
- `til_get_context`: 관련 TIL·백로그 파악, 링크 후보
- `vault_get_active_file`: 사용자가 보는 파일 확인

## Phase 1: 주제 리서치

1. `til_get_context`로 기존 TIL 확인. MCP 불가 시 `til_list` 폴백
   - 백로그 항목 학습 시 `til_backlog_status`(category) → `sections[].items[].sourceUrls` 참조
     - URL 1개: `WebFetch`로 직접 패치
     - URL 2개 이상: `til-fetcher` subagent **1개**에 모든 URL 전달
2. 기존 TIL 있으면: 심화 학습 / 새로 작성 선택지 제시
3. 기존 TIL 없으면: 웹 검색으로 조사
4. 핵심 개념, 예시, 관련 자료 수집 → 요약

## Phase 2: 대화형 학습

1. 리서치 결과 기반 설명
2. 심화 학습 모드: 기존 내용 반복하지 않고 새 관점에 집중
3. 사용자 질문에 답변
4. 사용자가 "저장해줘" 등 요청 시 Phase 3 전환 (자동 전환 금지)

## Phase 3: 저장

`/save` 스킬 규칙을 따라 저장. 심화 학습 모드는 기존 파일에 병합 (`updated` 날짜 추가).

## 인수

- 첫 번째: 학습 주제 (필수)
- 두 번째: 카테고리 (선택, 미지정 시 자동 추론)

## 규칙

- 한국어 작성, 기술 용어 원어 병기
- 링크: `[표시명](til/{카테고리}/{slug}.md)` — `[[위키링크]]` 금지
- 민감 정보 대체값 사용 (example.com, your-api-key)

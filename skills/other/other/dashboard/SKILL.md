---
name: dashboard
description: "학습 대시보드 - 통계, 활동 히트맵, 카테고리, 백로그 진행률"
disable-model-invocation: true
plugin-version: "__PLUGIN_VERSION__"
---

# Dashboard Skill

`til_dashboard` MCP 도구로 학습 통계를 조회하여 터미널에 표시.

## MCP 도구

- `til_dashboard`: 요약/히트맵/카테고리/백로그/추이 JSON 반환

## 출력 형식

### 1. 요약 카드
총 TIL, 카테고리, 이번 주, 연속 학습 — 테이블.

### 2. 활동 추이
heatmap cells를 주 단위 합산 → 스파크라인(`▁▂▃▅▇`).

### 3. 카테고리별 현황
카테고리(링크), 수, 최근 수정일 — 파일 수 내림차순.

### 4. 백로그 진행률
진행률 내림차순, 10칸 진행바(`█`/`░`).

## MCP 폴백

`til_dashboard` 불가 시 `til_list` + `til_backlog_status` + `til_recent_context` 조합.

## 규칙

- 한국어, 마크다운 링크로 출력 (경로 직접 노출 금지)
- 데이터 없으면 "/til로 첫 학습을 시작해보세요" 안내

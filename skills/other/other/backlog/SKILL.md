---
name: backlog
description: "학습 백로그를 조회하고 진행 상황을 보여준다"
argument-hint: "[카테고리]"
disable-model-invocation: true
plugin-version: "__PLUGIN_VERSION__"
---

# Backlog Skill

학습 백로그 조회 + 진행 상황 요약 (읽기 전용).

## MCP 도구

- `til_backlog_status`: 전체/카테고리별 진행률 (category 지정 시 sections 포함)

## 워크플로우

### 인수 없음 (`/backlog`)

1. `til_backlog_status` 호출 (MCP 불가 시 `./til/*/backlog.md` Glob)
2. 백로그 없으면 `/research` 안내 후 종료
3. 테이블로 요약: 카테고리(링크), 진행률, 완료수, 최근 학습일, 진행바

### 인수 있음 (`/backlog 카테고리`)

1. `til_backlog_status`에 category 전달 → sections 활용
2. 섹션별 출력:
   - `## {heading} ({완료수}/{전체수})`
   - `- (x) [{displayName}]({path})` / `- ( ) [{displayName}]({path})`
   - `- [ ]`/`- [x]` 마크다운 체크박스 사용 금지 (터미널 미렌더링)

## 출력 규칙

- 모든 카테고리명/항목명은 `[표시명](경로)` 마크다운 링크로 출력
- 경로 직접 노출 금지
- 진행바: 10칸 (`█` 완료, `░` 미완료)
- 한국어 출력
- 백로그 파일 수정 금지 (읽기 전용)

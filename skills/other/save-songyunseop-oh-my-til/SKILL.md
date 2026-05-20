---
name: save
description: "학습 내용을 TIL 파일로 저장하고 Daily 노트, MOC, 백로그를 일괄 업데이트"
argument-hint: "[주제] [카테고리]"
plugin-version: "__PLUGIN_VERSION__"
---

# Save Skill

학습 대화 → TIL 파일 저장 → Daily/MOC/백로그 업데이트 → 문서 리뷰 → 커밋.

## MCP 도구

- `til_get_context`: 관련 TIL·백로그 파악
- `til_list`: 기존 TIL 중복 확인
- `vault_get_active_file`: 사용자 파일 컨텍스트

## Step 1: 컨텍스트 확인

주제·카테고리 파악. 불명확하면 사용자에게 질문.

## Step 2: 링크 후보 파악

1. `til_get_context` 또는 MOC/백로그로 기존 TIL·백로그 항목 파악
2. 기존 TIL/백로그 항목 → 본문에서 마크다운 링크 사용
3. 존재하지 않는 개념 → 사용자에게 확인 후 관련 노트에만 추가

## Step 3: TIL 파일 저장

경로: `./til/{카테고리}/{주제슬러그}.md` (슬러그: 영문 소문자, 하이픈)

동일 슬러그 파일 있을 때:
- `/til` 심화 학습이 연속된 경우만 자동 병합 (기존 내용 유지 + 보강, `updated` 추가)
- 그 외: 사용자에게 병합/덮어쓰기 확인

### TIL 템플릿

```markdown
---
date: YYYY-MM-DDTHH:mm:ss
category: 카테고리
tags: [til, 태그1]
aliases: ["한글 제목", "영문 제목"]
---

# 제목

> [!tldr] 한줄 요약

## 핵심 내용
## 예시
## 참고 자료
- [제목](URL)
## 관련 노트
- [TIL](til/{카테고리}/{slug}.md)
```

- `date`: `date +%Y-%m-%dT%H:%M:%S` 명령으로 로컬 시각 조회
- 링크: `[표시명](til/{카테고리}/{slug}.md)` — `[[위키링크]]` 금지

## Step 4: 연관 파일 업데이트

아래 3개 파일을 **직접** 순차 업데이트한다 (subagent 사용 금지):

1. Daily 노트 (`./Daily/YYYY-MM-DD.md`): 카테고리별 TIL 링크 추가 (없으면 생성)
2. TIL MOC (`./til/TIL MOC.md`): 카테고리 섹션에 항목 추가 (없으면 생성)
3. 백로그 (`./til/{카테고리}/backlog.md`): 해당 항목 `[ ]` → `[x]`

각 파일: Read → 위치 확인 → Edit. 파일 없으면 생성.

## Step 5: 문서 리뷰

저장된 TIL 전체 내용 표시 → `AskUserQuestion`으로 확인 ("확인 완료" / "수정 필요").

## Step 6: git commit

`📝 til: {한글 제목}({영문 제목}) - {카테고리}` (push 안 함)

## 규칙

- frontmatter 필수: date, category, tags, aliases (누락 시 저장 전 보완)
- tags에 반드시 "til" 포함 (정적 사이트 필터 기준)
- `[[위키링크]]` 금지 — `[표시명](경로)` 형식만 사용
- TIL만 저장하고 Daily/MOC/백로그 누락하지 않는다
- Callout 활용: `> [!tldr]`, `> [!example]`, `> [!warning]`, `> [!tip]`
- 복잡한 개념은 Mermaid 다이어그램으로 시각화 (TIL당 최대 1개)
- 민감 정보 대체값 사용
- 한국어 작성, 기술 용어 원어 병기

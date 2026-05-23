---
name: research
description: "주제를 리서치하여 학습에 필요한 개념/용어를 파악하고, 백로그로 정리"
argument-hint: "<주제> [카테고리]"
plugin-version: "__PLUGIN_VERSION__"
---

# Research Skill

주제 리서치 → 개념/의존 관계 파악 → 백로그 파일 저장.

## Phase 1: 주제 리서치

1. 웹 검색으로 주제 조사, 필요 개념·용어·선행 지식 파악
2. 소주제 분해 후 직접 리서치
3. 소주제 간 의존 관계 분석

## Phase 2: 백로그 정리

1. 학습 순서 정렬: 선행 지식 → 핵심 개념 → 심화
2. 각 항목에 1줄 설명
3. 사용자 피드백 (추가/제거/순서 변경)

## Phase 3: 저장

1. `./til/{카테고리}/backlog.md`에 저장 (폴더 자동 생성)
2. 기존 backlog.md 있으면 병합:
   - `[x]` 완료 항목 보존
   - 동일 항목 체크 상태 유지
   - 기존 sources 보존, 새 항목만 추가
3. TIL MOC에 백로그 링크 추가
4. atomic commit: `📋 research: {주제} 학습 백로그 - {카테고리}` (push 안 함)

## 백로그 템플릿

```markdown
---
tags: [backlog, {카테고리}]
aliases: ["Backlog - {주제}"]
updated: YYYY-MM-DD
sources:
  slug-a: [https://url-1]
---

# {주제} 학습 백로그

## 선행 지식
- [ ] [개념A](til/{카테고리}/{slug-a}.md) - 설명

## 핵심 개념
- [ ] [개념C](til/{카테고리}/{slug-c}.md) - 설명

## 심화
- [ ] [개념E](til/{카테고리}/{slug-e}.md) - 설명
```

## 인수

- 첫 번째: 리서치 주제 (필수)
- 두 번째: 카테고리 (선택, 미지정 시 자동 추론)

## 규칙

- 항목당 1줄 설명, 20개 초과 시 분리
- 한국어 작성, 기술 용어 원어 병기
- 링크: `[표시명](til/{카테고리}/{slug}.md)`

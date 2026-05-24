---
name: research
description: 병렬 리서치 오케스트레이션. 여러 소스(Context7, WebSearch, 코드베이스)를 동시에 탐색하여 기술 조사를 수행합니다. Use when researching libraries, APIs, best practices, or when comparing technical approaches.
---

# Research — 병렬 리서치 오케스트레이션

여러 소스를 동시에 탐색하여 기술 조사를 수행합니다.

## 참조

- `.claude/skills/code-accuracy/SKILL.md` — 코드 정확성 + 라이브러리 검증
- `.claude/skills/deep-search/SKILL.md` — 코드베이스 탐색

## 워크플로우

### Step 1: 리서치 목표 정의
- 무엇을 조사하는가? (라이브러리, API, 패턴, 모범 사례)
- 어떤 결정을 내려야 하는가? (선택, 도입, 마이그레이션)
- 어떤 기준으로 평가하는가? (성능, 안정성, 호환성, 커뮤니티)

### Step 2: 병렬 3-Source 탐색

Source A — 공식 문서 (Context7):
- resolve-library-id로 라이브러리 식별
- query-docs로 공식 문서 검색

Source B — 웹 (WebSearch):
- 최신 블로그 포스트, 비교 글, 벤치마크
- GitHub Issues, Stack Overflow 답변

Source C — 코드베이스 (Grep/SemanticSearch):
- 프로젝트 내 기존 사용 패턴
- 유사 구현 참조
- 의존성 관계

3개 Source를 반드시 동시 실행합니다.

### Step 3: 종합 분석
- 각 소스의 결과를 교차 검증
- 장단점 비교표 작성
- 프로젝트 컨텍스트에 맞는 권장안 도출

### Step 4: 리서치 리포트

```
[Research 결과]

조사 주제: [주제]

발견 사항:
- [소스] [내용]

비교 분석:
| 기준 | 옵션 A | 옵션 B |
|-----|-------|-------|
| ... | ...   | ...   |

권장안: [근거와 함께]

참고 자료:
- [URL/경로]
```

## 에이전트 연동

- researcher 에이전트가 이 스킬의 주 실행자
- analyst 에이전트가 결과를 평가

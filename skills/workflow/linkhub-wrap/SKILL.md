---
name: linkhub-wrap
description: LinkHub 세션 마무리. 문서 업데이트 분석, 후속 작업 제안, 학습 내용 정리.
---

# LinkHub Wrap

Chrome Extension 프로젝트 특화 세션 마무리 스킬.

## 실행 순서

```
/linkhub-wrap
    │
    ├─ Phase 1: 세션 요약
    │   ├─ git status/diff 확인
    │   └─ 작업 내용 요약
    │
    ├─ Phase 2: 문서 업데이트 분석
    │   ├─ AI Context 업데이트 필요 여부
    │   ├─ 모듈 CLAUDE.md 업데이트 필요 여부
    │   └─ manifest.json 변경 영향 분석
    │
    ├─ Phase 3: 후속 작업 제안
    │   ├─ 미완료 작업 식별
    │   └─ 다음 세션 권장 작업
    │
    └─ Phase 4: 사용자 선택 실행
        ├─ 문서 업데이트 실행
        ├─ 커밋 생성
        └─ 후속 작업 TODO 생성
```

## Phase 1: 세션 요약

```bash
git status --short
git diff --stat HEAD~5 2>/dev/null || git diff --stat
```

### 요약 포맷

```markdown
## 세션 요약

**작업 내용**:
- {주요 변경 사항 1}
- {주요 변경 사항 2}

**변경 파일**: {N}개
**신규 파일**: {M}개
```

## Phase 2: 문서 업데이트 분석

### AI Context (.claude/ai-context/)

| 변경 유형 | 대상 파일 | 트리거 |
|----------|----------|--------|
| 도메인 용어 추가 | domain/glossary.json | 새 개념/용어 등장 |
| 엔터티 변경 | domain/entities.json | Link, Tag, Settings 구조 변경 |
| Chrome API 사용 | integrations/chrome.json | 새 permission, API 사용 |
| 아키텍처 변경 | architecture.json | 레이어/모듈 추가 |
| 컨벤션 변경 | conventions.json | 코딩 스타일 변경 |

### 프로젝트 문서

| 변경 유형 | 대상 | 트리거 |
|----------|------|--------|
| 루트 CLAUDE.md | /CLAUDE.md | 명령어, 아키텍처, 규칙 변경 |
| 모듈 CLAUDE.md | src/*/CLAUDE.md | 새 디렉토리, 주요 변경 |

### Chrome Extension 특화 체크

| 항목 | 확인 내용 |
|------|----------|
| manifest.json | permission 추가, version 변경 |
| background worker | 새 이벤트 리스너 |
| content script | 새 injection 대상 |
| storage schema | 데이터 구조 변경 |

## Phase 3: 후속 작업 제안

### 미완료 작업 식별

- TODO 주석 검색: `// TODO`, `// FIXME`
- 테스트 미작성 파일
- 빌드 경고

### 다음 세션 권장 작업

MVP 체크리스트 기준 (docs/requirements.md):
- [ ] 원클릭 저장
- [ ] 태그 관리
- [ ] 카드형 목록
- [ ] 전문 검색
- [ ] JSON 내보내기

## Phase 4: 사용자 선택

AskUserQuestion으로 선택 요청:

| 옵션 | 설명 |
|------|------|
| 문서 업데이트 | 분석된 문서 변경 적용 |
| 커밋 생성 | 현재 변경사항 커밋 |
| 둘 다 | 문서 업데이트 + 커밋 |
| 스킵 | 아무것도 하지 않음 |

## 출력 포맷

```markdown
## LinkHub 세션 마무리

### 세션 요약
{Phase 1 결과}

### 문서 업데이트 필요
{Phase 2 결과 - 테이블 형식}

### 후속 작업 제안
{Phase 3 결과 - 우선순위순}

### 다음 액션
{사용자 선택 옵션}
```

## 주의사항

- 커밋 시 Co-Author/Claude 마킹 금지
- 문서 업데이트는 최소한으로 (불필요한 변경 지양)
- MVP 우선순위 준수

---
name: merge-request
description: Merge Request나 Pull Request 생성 시 컨벤션과 품질 검사를 따르도록 적용. Use when creating pull requests or merge requests to follow PR conventions and quality checks.
---

# Merge Request / Pull Request 가이드

## PR 제목 컨벤션

형식: `type(scope): subject`

### 타입 표

| 타입 | 설명 |
|-----|------|
| feat | 새로운 기능 |
| fix | 버그 수정 |
| refactor | 리팩토링 (동작 변경 없음) |
| docs | 문서 변경 |
| test | 테스트 추가/수정 |
| chore | 빌드, 설정, 유지보수 |
| style | 포맷팅, 공백 등 (로직 변경 없음) |
| perf | 성능 개선 |
| ci | CI 설정 변경 |
| build | 빌드 시스템 변경 |
| revert | 이전 커밋 되돌리기 |

예시: `feat(auth): add OAuth2 login flow`, `fix(api): handle null response`

---

## PR 본문 템플릿

### Summary (요약)

- 변경 사항을 불릿 포인트로 요약
- 영향 받는 모듈/기능 명시

### Motivation / Context (동기 및 맥락)

- 이 변경이 필요한 이유
- 해결하려는 문제 설명

### Changes (변경 사항)

- 구체적으로 무엇이 변경되었는지
- 주요 파일별 변경 내용

### Test Plan (테스트 계획)

- [ ] 단위 테스트 통과
- [ ] 수동 테스트 시나리오 수행
- [ ] 회귀 테스트 항목 확인

### Breaking Changes (호환성 변경)

- 있으면 구체적으로 명시
- 마이그레이션 가이드가 필요하면 포함
- 없으면 N/A

### Screenshots (스크린샷)

- UI 변경 시 화면 캡처 첨부

### Related Issues (관련 이슈)

- Closes #issue-number
- Related to #issue-number

---

## Pre-PR 체크리스트

- [ ] 테스트 추가/업데이트됨
- [ ] 문서 업데이트됨
- [ ] 시크릿/자격증명 노출 없음
- [ ] Lint 통과
- [ ] 디버그/console.log 제거됨
- [ ] 자기 리뷰 완료
- [ ] base 브랜치와 최신 상태로 동기화됨

---

## 리뷰 가이드라인 (작성자 관점)

- 건설적 피드백: 지적보다 개선 방향 제시
- 스타일보다 로직에 집중
- approve / request changes / comment를 명확히 구분
- 리뷰 응답 시간 기대치: 팀 정책에 따라 1~2 영업일 내

---

## 리뷰어 체크리스트

- [ ] 로직 정확성
- [ ] 엣지 케이스 처리
- [ ] 에러 처리 완전성
- [ ] 성능 영향 고려
- [ ] 보안 영향 고려
- [ ] 네이밍 명확성

---

## 머지 전략

| 전략 | 사용 시점 |
|-----|----------|
| Squash and merge | 피처 브랜치, 커밋 히스토리 단순화 필요 시 (권장) |
| Merge commit | 머지 커밋으로 브랜치 단위 히스토리 보존 필요 시 |
| Rebase and merge | 선형 히스토리 유지, rebase 가능한 브랜치 |

Squash and merge 권장: 여러 커밋을 하나로 합쳐 main 브랜치 히스토리를 깔끔하게 유지.

---

## CLI 자동화 명령어

### GitHub (gh)

```bash
# PR 생성
gh pr create --title "type(scope): subject" --body "본문"

# PR 머지
gh pr merge --squash

# PR 목록
gh pr list
```

### GitLab (glab)

```bash
# MR 생성
glab mr create --title "type(scope): subject" --description "본문"

# MR 머지
glab mr merge
```

---

## PR 크기 가이드라인

- 소형 PR 선호: 200~400줄 이하가 리뷰에 유리
- 대규모 변경 분할: 논리적 단위로 여러 PR로 나누기
- 분할 기준: 하나의 PR이 하나의 테스트 가능한 변경을 담도록

---

## 참조 룰

프로젝트 project context에 PR 컨벤션이 정의되어 있으면 Read tool로 읽어 적용한다.

---
name: reviewer
description: 코드 리뷰 스킬. 버그, 보안, 성능, 가독성 체크. PR 리뷰, 자기 검토 시 사용.
---

# Reviewer Skill

## 리뷰 원칙

- 비판이 아닌 개선 방향 제시
- 문제 제기 시 대안 제시
- 우선순위 태그 사용

## 우선순위 태그

| 태그 | 의미 |
|------|------|
| **[Critical]** | 반드시 수정 (버그, 보안) |
| **[Major]** | 수정 권장 (성능, 설계) |
| **[Minor]** | 제안 (가독성, 스타일) |

## 체크리스트

### 버그 & 로직
- [ ] Null/Undefined 처리
- [ ] 경계 조건 (빈 배열, 0 등)
- [ ] 비동기 에러 핸들링
- [ ] useEffect 의존성 배열

### 보안
- [ ] XSS (dangerouslySetInnerHTML 사용 여부)
- [ ] Chrome Storage 데이터 검증
- [ ] 외부 URL 처리 (window.open, href)
- [ ] 민감 정보 노출 여부

### 성능
- [ ] 불필요한 리렌더링
- [ ] 대용량 데이터 처리 (링크 수천 개)
- [ ] 메모이제이션 필요 여부 (useMemo, useCallback)
- [ ] Storage 호출 최적화

### 아키텍처 (Kent Beck Style)
- [ ] SRP 준수 (하나의 함수 = 하나의 책임)
- [ ] 순수 함수 사용 (사이드 이펙트 격리)
- [ ] 불변성 패턴 (객체 수정 대신 새 객체)
- [ ] 명확한 의도 (이름만으로 역할 파악)
- [ ] YAGNI/KISS 준수 (불필요한 추상화 없음)

### 컨벤션
- [ ] Storage 유틸리티 사용 (직접 호출 X)
- [ ] 타입 안전성
- [ ] 기존 패턴과 일관성

## 리뷰 템플릿

```markdown
## 요약
[변경 사항 요약]

## 좋은 점
- ...

## 개선 필요

### [Critical] 제목
- 위치: `파일:라인`
- 문제: ...
- 제안: ...

### [Major] 제목
- 위치: `파일:라인`
- 문제: ...
- 제안: ...

### [Minor] 제목
- 위치: `파일:라인`
- 제안: ...
```

## 예시

### 리뷰 결과

```markdown
## 요약
태그 필터링 기능 추가

## 좋은 점
- 타입 안전성 확보
- 컴포넌트 분리 적절

## 개선 필요

### [Critical] 빈 배열 처리 누락
- 위치: `src/popup/hooks/useLinks.ts:25`
- 문제: links가 undefined일 때 에러 발생
- 제안: `links ?? []` 기본값 처리

### [Major] 불필요한 리렌더링
- 위치: `src/popup/components/TagFilter.tsx:12`
- 문제: 매 렌더링마다 새 함수 생성
- 제안: useCallback으로 메모이제이션

### [Minor] 변수명 개선
- 위치: `src/shared/utils/search.ts:8`
- 제안: `res` → `searchResults`로 명확하게
```

## 주의사항

- **상세 패턴은 코드베이스의 기존 구현 참조**
- 리뷰 후 수정이 필요하면 /developer 또는 /frontend 스킬로 수정
- [Critical], [Major] 이슈는 반드시 수정 후 재리뷰

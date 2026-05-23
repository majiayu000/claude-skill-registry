---
name: task
description: 작업 오케스트레이션 스킬. 분석 → 구현 → 리뷰 → 커밋까지 전체 워크플로우 관리. 기능 개발, 버그 수정 등 모든 작업에 사용.
---

# Task Skill

통합 워크플로우 오케스트레이션. 작업 분석부터 Git 커밋까지 전체 사이클 관리.

## 워크플로우

```
/task "작업 설명"
    │
    ├─ Phase 1: 분석
    │   ├─ 요구사항 파악
    │   ├─ 영향받는 파일 식별
    │   ├─ 작업 타입 결정 (feat/fix/refactor)
    │   └─ 브랜치 생성
    │
    ├─ Phase 2: 구현
    │   ├─ /developer 스킬 적용 (타입, 스토리지, 로직)
    │   ├─ /frontend 스킬 적용 (UI, 컴포넌트)
    │   └─ 기능 단위로 중간 커밋
    │
    ├─ Phase 3: 리뷰
    │   ├─ /reviewer 스킬 적용
    │   ├─ [Critical] 이슈 → Phase 2로 돌아가 수정
    │   ├─ [Major] 이슈 → Phase 2로 돌아가 수정
    │   └─ [Minor] 이슈 → 선택적 수정
    │
    └─ Phase 4: 마무리
        ├─ /verify 실행
        ├─ 최종 커밋
        └─ (선택) PR 생성 안내
```

## Phase 1: 분석

### 작업 타입 판별

| 타입 | 브랜치 접두사 | 설명 |
|------|---------------|------|
| 새 기능 | `feat/` | 새로운 기능 추가 |
| 버그 수정 | `fix/` | 버그 수정 |
| 리팩토링 | `refactor/` | 코드 개선 (기능 변경 없음) |
| 문서 | `docs/` | 문서 작성/수정 |
| 스타일 | `style/` | 코드 포맷팅 |
| 테스트 | `test/` | 테스트 추가/수정 |

### 브랜치 생성

```bash
git checkout -b {타입}/{kebab-case-설명}
# 예: feat/tag-filter, fix/search-bug
```

### 분석 체크리스트

- [ ] 요구사항 명확히 이해
- [ ] 영향받는 파일/모듈 식별
- [ ] 필요한 스킬 결정 (developer, frontend, 둘 다)
- [ ] 작업 단위 분할 (커밋 단위)

## Phase 2: 구현

### 스킬 호출 순서

1. **데이터/로직 먼저**: `/developer` 스킬 적용
   - 타입 정의, 인터페이스
   - Storage 유틸리티
   - 비즈니스 로직

2. **UI/컴포넌트**: `/frontend` 스킬 적용
   - React 컴포넌트
   - 커스텀 훅
   - 스타일링

### 기능 단위 커밋

구현 중 의미 있는 단위마다 커밋:

```bash
git add <관련 파일들>
git commit -m "{타입}: {설명}"
```

**커밋 메시지 규칙** (Conventional Commits):
```
feat: add tag filtering logic
feat: implement TagFilter component
fix: search not matching partial text
refactor: extract storage utilities
```

**커밋 단위 기준**:
- 하나의 논리적 변경 = 하나의 커밋
- 롤백 시 독립적으로 되돌릴 수 있는 단위

## Phase 3: 리뷰

### /reviewer 스킬 적용

구현 완료 후 자동으로 리뷰 수행:

| 우선순위 | 조치 |
|----------|------|
| [Critical] | 반드시 수정 → Phase 2 |
| [Major] | 수정 권장 → Phase 2 |
| [Minor] | 선택적 수정 |

### 수정 루프

```
리뷰 → 이슈 발견 → 수정 (developer/frontend) → 재리뷰
```

이슈가 없거나 Minor만 남으면 Phase 4로 진행.

## Phase 4: 마무리

### 최종 점검 (/verify 스킬 호출)

```
/verify 실행
    ├─ pnpm build    # 빌드 확인
    ├─ pnpm lint     # 린트 확인
    └─ pnpm test:run # 테스트 확인
```

### 디렉토리별 CLAUDE.md 작성/갱신

새 디렉토리 생성 또는 주요 변경 시 해당 디렉토리에 `CLAUDE.md` 작성.

### 최종 커밋 (필요시)

```bash
git add .
git commit -m "{타입}: {전체 작업 요약}"
```

## 예시

### 입력
```
/task 태그 필터링 기능 추가
```

### 실행 흐름

```
1. 분석
   - 타입: feat (새 기능)
   - 브랜치: feat/tag-filter
   - 영향: src/shared/types/, src/popup/components/
   - 스킬: developer → frontend

2. 구현
   - /developer: 필터 로직, 타입 정의
   - 커밋: "feat: add tag filter logic"
   - /frontend: TagFilter.tsx 컴포넌트
   - 커밋: "feat: implement TagFilter component"

3. 리뷰
   - /reviewer 실행
   - [Minor] 변수명 개선 제안
   - 선택적 수정

4. 마무리
   - /verify: 빌드/린트/테스트 통과
   - 완료
```

## 주의사항

- **커밋 마킹 금지**: Co-Author, Claude 마킹 절대 금지
- **브랜치 보호**: main 직접 커밋 금지, 브랜치에서 작업
- **빌드 확인**: 커밋 전 반드시 빌드 성공 확인
- **작은 단위**: 큰 작업은 여러 브랜치로 분할 고려

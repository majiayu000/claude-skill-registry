---
name: code-analysis
description: 지정된 디렉토리/파일의 문제점을 분석하고 각 문제를 개별 GitHub 이슈로 등록합니다.
allowed-tools:
  - Bash(gh issue create *)
  - Bash(gh issue list *)
  - Bash(gh auth status *)
  - Bash(git diff *)
  - Bash(git log *)
  - Read
  - Grep
  - Glob
argument-hint: <분석 대상 경로> (예: src/core/, src/infra/broker.py)
---

# 코드 분석 및 GitHub 이슈 등록

지정된 디렉토리 또는 파일을 분석하여 문제점, 모호한 점, 개선이 필요한 사항을 식별하고 각각을 GitHub 이슈로 등록합니다.

## 실행 절차

### 1단계: 분석 대상 확인

- 인자가 없으면 사용자에게 분석 대상 경로를 질문
- 지정된 경로의 파일 목록 수집 (Glob 사용)
- 각 파일의 전체 내용 읽기 (Read 사용)

### 2단계: 코드 분석

아래 관점에서 문제점을 식별합니다:

#### 2-1. 버그 및 로직 오류
- 경계 조건 누락 (빈 리스트, None, 0 나누기 등)
- 타입 불일치 또는 잘못된 타입 가정
- 예외 처리 누락 또는 잘못된 예외 처리
- 잘못된 조건문, off-by-one 에러

#### 2-2. 설계 및 아키텍처
- Clean Architecture 위반 (core → infra 의존)
- 인터페이스 미구현 또는 불완전한 구현
- 과도한 결합 (tight coupling)
- 단일 책임 원칙(SRP) 위반

#### 2-3. 모호한 코드
- 의도가 불분명한 매직 넘버 또는 하드코딩 값
- 이름만으로 역할을 파악하기 어려운 변수/함수
- 주석과 실제 동작이 불일치하는 코드
- 복잡한 조건문이나 중첩 로직

#### 2-4. 누락된 기능 및 미완성 코드
- TODO, FIXME, HACK, XXX 주석
- 빈 구현체 (pass, NotImplementedError)
- 테스트가 없는 핵심 로직

#### 2-5. 유지보수성
- 중복 코드
- 과도하게 긴 함수 (50줄 이상)
- 깊은 중첩 (3단계 이상의 if/for)
- 사용되지 않는 import, 변수, 함수

### 3단계: 분석 결과 정리

발견된 각 문제를 다음 형식으로 정리합니다:

```
- 제목: 간결한 한줄 요약
- 파일: 해당 파일 경로
- 위치: 라인 번호 또는 함수명
- 심각도: Critical / Warning / Suggestion
- 카테고리: Bug / Design / Ambiguous / Missing / Maintenance
- 설명: 문제의 상세 내용과 왜 문제인지 설명
- 제안: 개선 방향 또는 수정 방안
```

### 4단계: 사용자 확인

- 발견된 전체 문제 목록을 요약 테이블로 출력
- 사용자에게 이슈로 등록할 항목을 확인 요청
- 사용자가 선택한 항목만 이슈로 등록 (전체 등록도 가능)

### 5단계: GitHub 이슈 등록

각 문제를 개별 GitHub 이슈로 생성합니다:

```bash
gh issue create \
  --title "[카테고리] 제목" \
  --body "본문" \
  --label "라벨"
```

#### 이슈 본문 형식

```markdown
## 문제 설명
{설명}

## 위치
- **파일**: `{파일 경로}`
- **위치**: {라인 번호 또는 함수명}

## 심각도
{Critical / Warning / Suggestion}

## 제안
{개선 방향 또는 수정 방안}

---
_이 이슈는 코드 분석 스킬에 의해 자동 생성되었습니다._
```

#### 라벨 매핑

| 카테고리 | 라벨 |
|---------|------|
| Bug | `bug` |
| Design | `design` |
| Ambiguous | `clarification` |
| Missing | `enhancement` |
| Maintenance | `maintenance` |

- 라벨이 존재하지 않으면 라벨 없이 생성합니다 (--label 옵션 생략)
- 심각도가 Critical이면 추가로 `priority: high` 라벨을 시도합니다

### 6단계: 결과 보고

## 출력 형식

```
## 코드 분석 결과

### 분석 대상
- 경로: {분석 대상 경로}
- 파일 수: {N}개

### 발견된 문제

| # | 심각도 | 카테고리 | 파일 | 제목 |
|---|--------|---------|------|------|
| 1 | Critical | Bug | src/core/analyzer.py | ... |
| 2 | Warning | Design | src/infra/broker.py | ... |

### 등록된 이슈

| # | 이슈 번호 | 제목 | URL |
|---|----------|------|-----|
| 1 | #12 | [Bug] ... | https://github.com/.../issues/12 |
| 2 | #13 | [Design] ... | https://github.com/.../issues/13 |

### 요약
- 총 {N}개 문제 발견 (Critical: {n}, Warning: {n}, Suggestion: {n})
- {M}개 이슈 등록 완료
```

## 주의사항

- 분석은 읽기 전용으로 수행하며, 코드를 수정하지 않습니다
- .env 파일은 분석 대상에서 제외합니다
- 이슈 등록 전 반드시 사용자 확인을 받습니다
- 동일한 문제가 이미 이슈로 등록되어 있는지 `gh issue list`로 확인 후 중복 방지
- 한 번에 너무 많은 이슈를 등록하지 않도록 10개 초과 시 사용자에게 분할 등록 제안

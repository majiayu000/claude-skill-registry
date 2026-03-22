---
name: documentation
description: 프로젝트 문서화, README, 아키텍처 문서, 온보딩 가이드 작성 시 적용. Use when creating or updating README, architecture docs, onboarding guides, or API documentation.
---

# 문서화 가이드

## 핵심 원칙

프로젝트를 처음 접하는 개발자가 전반적인 구조와 기능을 이해할 수 있도록 체계적인 문서를 생성합니다. 모든 문서 내용은 실제 코드베이스 분석을 기반으로 작성하며, 추측으로 작성하지 않습니다.

## 문서화 프로세스 개요

```
요청 → 코드베이스 분석 → 문서 폴더 생성 → 목차 작성 → 파트별 문서 작성 → 다이어그램 추가 → 검증 및 완료
```

분석 단계: 아키텍처 파악, 주요 기능 식별, 의존성 분석

## 표준 문서 폴더 구조

```
Documents/
├── 00-TOC.md                    # 전체 문서 인덱스
├── 01-project-overview.md        # 프로젝트 소개, 기술 스택
├── 02-architecture.md            # 전체 아키텍처, 레이어 구조
├── 03-folder-structure.md        # 디렉토리 설명
├── 04-core-features/             # 기능별 상세 문서
│   ├── 04-01-auth.md
│   ├── 04-02-sync.md
│   └── ...
├── 05-data-flow.md               # 데이터 흐름, 상태 관리
├── 06-dependencies.md             # 외부 라이브러리 설명
├── 07-build-deploy.md            # 빌드 설정, CI/CD
└── 08-onboarding.md              # 신규 개발자 시작 가이드
```

## 문서 번호 규칙

| 번호 범위 | 카테고리 | 설명 |
|----------|---------|------|
| 00 | 목차 | 전체 문서 인덱스 |
| 01-03 | 기본 구조 | 프로젝트 개요, 아키텍처, 폴더 |
| 04-XX | 핵심 기능 | 기능별 상세 문서 (하위 폴더) |
| 05-06 | 기술 상세 | 데이터 흐름, 의존성 |
| 07-08 | 운영 | 빌드, 온보딩 |

## 문서 작성 전 필수 분석

### 분석 체크리스트

```
□ 프로젝트 타입 확인 (언어, UI 프레임워크)
□ 아키텍처 패턴 파악 (MVC/MVVM/Clean/VIPER등)
□ 폴더 구조 전체 스캔
□ 의존성 파일 분석 (Package.json, requirements.txt 등)
□ 주요 진입점 확인 (main, App 진입점)
□ 핵심 모델/엔티티 식별
□ 주요 화면/기능 목록 파악
```

### 정보 수집 도구 활용

1. Glob: 소스 파일 목록 확인
2. Read: 진입점 파일, 의존성 파일
3. SemanticSearch: 주요 기능, 아키텍처 패턴
4. Grep: 패턴 기반 추출 (protocol, class, interface 등)

## 아키텍처 자동 감지

| 감지 패턴 | 아키텍처 | 문서화 초점 |
|----------|---------|------------|
| ViewModel, ObservableObject, Binding | MVVM | View-ViewModel 바인딩 |
| UseCase, Repository, Entity | Clean Architecture | 레이어 간 의존성 |
| Reducer, State, Action, Effect | TCA/Redux | 상태 변화 흐름 |
| Presenter, Interactor, Router | VIPER | 모듈 간 통신 |
| Controller, View, Model 혼재 | MVC (레거시) | 리팩터링 포인트 |

## 문서 템플릿

### 목차 템플릿 (00-TOC.md)

```markdown
# [프로젝트명] 문서

> 이 문서는 [날짜]에 생성되었습니다.

## 이 문서의 목적

[프로젝트명]을 처음 접하는 개발자가 프로젝트의 구조와 기능을 빠르게 이해할 수 있도록 돕습니다.

## 문서 목록

| 번호 | 문서명 | 설명 | 난이도 |
|-----|-------|------|-------|
| 01 | [프로젝트 개요](./01-project-overview.md) | 기술 스택, 주요 기능 소개 | 1 |
| 02 | [아키텍처](./02-architecture.md) | 전체 구조, 레이어 설명 | 2 |
| 03 | [폴더 구조](./03-folder-structure.md) | 디렉토리별 역할 | 1 |
| 04 | [핵심 기능](./04-core-features/) | 기능별 상세 문서 | 3 |
| 05 | [데이터 흐름](./05-data-flow.md) | 상태 관리, 데이터 바인딩 | 2 |
| 06 | [의존성](./06-dependencies.md) | 외부 라이브러리 가이드 | 2 |
| 07 | [빌드 및 배포](./07-build-deploy.md) | 빌드 설정, CI/CD | 2 |
| 08 | [온보딩 가이드](./08-onboarding.md) | 신규 개발자 시작 가이드 | 1 |

## 추천 읽기 순서

1. 첫날: 01 → 03 → 08
2. 첫주: 02 → 05 → 06
3. 기능 개발 시: 04 (해당 기능 문서)

## 프로젝트 요약

- 플랫폼: [Platform]
- UI 프레임워크: [Framework]
- 아키텍처: [Pattern]
- 의존성 관리: [Tool]
```

### 아키텍처 템플릿 (02-architecture.md)

```markdown
# 아키텍처

## 개요

[프로젝트명]은 [아키텍처 패턴]을 사용합니다.

## 레이어 구조

[Mermaid 다이어그램 삽입]

## 각 레이어 설명

### Presentation Layer

- 역할: [설명]
- 주요 컴포넌트: [목록]

### Domain Layer

- 역할: [설명]
- 주요 컴포넌트: [목록]

### Data Layer

- 역할: [설명]
- 주요 컴포넌트: [목록]

## 의존성 규칙

[다이어그램과 함께 설명]
```

## 문서별 필수 다이어그램

| 문서 | 다이어그램 유형 | 목적 |
|-----|---------------|------|
| 아키텍처 | flowchart / C4 | 레이어 구조 시각화 |
| 데이터 흐름 | sequenceDiagram | 요청-응답 흐름 |
| 핵심 기능 | classDiagram | 클래스 관계 |
| 폴더 구조 | flowchart | 디렉토리 트리 |

## 단계별 문서 작성 프로세스

### Phase 1: 기반 분석 (필수)

```
□ 프로젝트 루트 디렉토리 확인
□ 전체 폴더 구조 파악
□ 의존성 파일 읽기
□ 진입점 파일 분석
□ 아키텍처 패턴 식별
```

### Phase 2: 폴더 및 목차 생성

```
□ Documents/ 폴더 생성
□ 00-TOC.md 생성 (템플릿 기반)
□ 프로젝트 요약 정보 채우기
□ 문서 목록 초안 작성
```

### Phase 3: 기본 문서 작성 (01-03)

```
□ 01-project-overview.md - 기술 스택, 기능 소개
□ 02-architecture.md - 레이어 구조, 다이어그램
□ 03-folder-structure.md - 디렉토리 설명
```

### Phase 4: 상세 문서 작성 (04-08)

```
□ 04-core-features/ - 각 기능별 상세 문서
□ 05-data-flow.md - 상태 관리, 바인딩
□ 06-dependencies.md - 라이브러리 설명
□ 07-build-deploy.md - 빌드 설정
□ 08-onboarding.md - 시작 가이드
```

### Phase 5: 검증 및 완료

```
□ 모든 코드 참조가 실제로 존재하는지 확인
□ 다이어그램이 현재 구조와 일치하는지 확인
□ 링크가 모두 유효한지 확인
□ 목차 문서 최종 업데이트
```

## 정확도 규칙

### 코드 참조 시 필수 검증

1. grep으로 실제 존재 확인
2. 파일 경로 정확히 명시
3. 최신 코드 상태 반영

### 금지 사항

- 추측으로 클래스명이나 함수명 언급
- 실제 확인 없이 아키텍처 패턴 단정
- 존재하지 않는 폴더나 파일 언급
- 버전 확인 없이 API 사용법 설명

### 연계 스킬

- 코드/타입 언급 시: code-accuracy (심볼 존재 확인)
- 구조 분석 시: planning (아키텍처 파악)
- 라이브러리 설명 시: library-verification (버전/API 확인)

## 예시

### 좋은 예 - 분석 기반 문서화

```
1. 먼저 프로젝트 구조를 분석합니다.
   - glob: 소스 파일 목록
   - read_file: 의존성 파일
   - codebase_search: 진입점, 주요 기능

2. 분석 결과를 바탕으로 문서 작성
   - 실제 분석 내용 반영
   - 코드 경로와 타입 검증
```

### 나쁜 예 - 추측 기반 문서화

```
"이 프로젝트는 아마 MVVM 패턴을 사용하는 것 같습니다.
UserController와 ProfileViewModel이 있을 것이고..."
(실제 분석 없이 추측)
```

## README 구조

- Overview: 프로젝트 목적과 요약
- Getting Started: 설치 및 실행 방법
- Architecture: 핵심 아키텍처
- Contributing: 기여 방법
- License: 라이선스 정보

## 아키텍처 문서

- Mermaid 다이어그램 활용
- 변경 시 문서 동기화 유지

## 온보딩 가이드

- 선행 조건 (버전, 도구)
- 설정 단계
- 핵심 개념 소개
- 첫 작업 가이드

## API 문서

- 엔드포인트, 파라미터, 응답
- 예시 코드 포함

## 인라인 문서

- What이 아닌 Why 기술
- 비즈니스 의도 표현

## 파일 네이밍

- README.md, ARCHITECTURE.md, CONTRIBUTING.md
- 일관된 규칙 사용

## 톤과 스타일

- 명확하고 간결하게
- 신규 멤버도 이해할 수 있는 수준

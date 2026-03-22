---
name: deep-index
description: 코드베이스 인덱싱 및 구조 분석. 프로젝트를 스캔하여 모듈별 요약, 의존성 그래프, 진입점 맵을 생성하고 project context를 풍부하게 합니다. Use when onboarding to a new codebase or when project structure needs documentation.
---

# Deep Index Skill

코드베이스 인덱싱 및 구조 분석. 프로젝트를 스캔하여 모듈별 요약, 의존성 그래프, 진입점 맵을 생성하고 context를 풍부하게 합니다.

## 사용 시점

- 새 프로젝트 온보딩
- 대규모 코드베이스 구조 파악
- 주기적 인덱스 갱신
- 프로젝트 구조 문서화 필요 시

## 워크플로우

### Step 1: 프로젝트 구조 스캔

- Glob으로 소스 파일 목록 수집 (*.ts, *.js, *.swift, *.py 등)
- 디렉터리 계층 구조 파악

### Step 2: 진입점 식별

- main, AppDelegate, index, app.ts 등 앱 진입 파일 탐색
- 라우팅·네비게이션 진입점 식별

### Step 3: 모듈 경계 매핑

- 디렉터리·패키지·모듈 단위로 경계 구분
- 각 모듈의 책임 추정

### Step 4: import/의존성 그래프 분석

- import, require, include 등 의존성 구문 Grep
- 모듈 간 의존 관계 추출

### Step 5: 핵심 패턴 식별

- 아키텍처 패턴 (MVC, MVVM, Clean 등)
- 상태 관리 (Redux, Combine, RxSwift 등)
- API 레이어 구조

### Step 6: 요약 문서 생성

- `.claude/project/codebase-index.md`에 결과 저장

## 출력 구조 (codebase-index.md)

```markdown
# Codebase Index: [Project Name]

## Project Overview
- Language(s): ...
- Framework(s): ...
- Architecture: ...

## Module Map
| Module | Path | Responsibility | Dependencies |
|--------|------|----------------|--------------|

## Entry Points
- Main: ...
- Routes/Navigation: ...

## Dependency Graph
[Mermaid diagram]

## Key Patterns
- State Management: ...
- Data Flow: ...
- API Layer: ...

## File Statistics
- Total files: N
- By language: ...
```

## setup skill 연동

- 초기 프로젝트 설정 시 deep-index를 setup 워크플로우에 포함
- 온보딩 완료 후 codebase-index.md를 참조 문서로 활용

## evolve skill 연동

- 프로젝트 구조 변경 감지 시 재인덱싱 트리거
- 주기적 갱신으로 out-of-date 방지

## 성능

- Glob + Grep 병렬 실행으로 스캔 속도 향상
- 대규모 프로젝트는 모듈 단위로 분할 스캔

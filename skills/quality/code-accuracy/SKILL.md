---
name: code-accuracy
description: 코드 작성 시 심볼 존재 확인, import 검증, 라이브러리 API 검증, 환각 코드 생성 방지를 위해 적용. Use when writing or modifying code to prevent hallucinated symbols, verify imports, check library APIs, and ensure compilable output.
---

# 코드 정확성 (Code Accuracy)

언어/플랫폼에 무관하게 적용되는 코드 작성 핵심 원칙. 환각(hallucination) 코드 생성 방지와 실제 동작 가능한 코드 생성을 목표로 한다.

## 핵심 원칙

프로젝트 코드베이스에 실제로 존재하는 코드만 제안한다. 존재하지 않는 타입, 함수, 모듈을 참조하지 않는다.

## 심볼 검증 전략

### 타입/함수/클래스 사용 전
- Grep으로 프로젝트에 정의가 있는지 확인한다.
- class/struct/enum/protocol/interface + 심볼명으로 검색
- 정의 위치를 확인한 후 참조한다.

### import 사용 전
- 의존성 파일에 해당 모듈이 선언되어 있는지 확인한다.
- package.json, Package.swift, requirements.txt, build.gradle, Cargo.toml 등
- 존재하지 않으면 의존성 추가를 제안한다.

### 라이브러리 API 사용 전
- Context7 또는 프로젝트 소스로 API 존재 여부 확인
- 버전 호환성 확인 (해당 버전에 API가 있는지)

## 의존성 파일 매핑

| 언어/플랫폼 | 의존성 파일 |
|------------|-------------|
| JavaScript/Node | package.json |
| Swift | Package.swift, Podfile |
| Python | requirements.txt, pyproject.toml |
| Java/Kotlin | build.gradle, pom.xml |
| C# | .csproj, packages.config |
| Go | go.mod |
| Rust | Cargo.toml |

## 타입 선택 규칙 (일반화)

| 상황 | 선택 | 이유 |
|------|------|------|
| 값 타입, 불변 데이터 | struct/record | 복사 시맨틱, 불변성 |
| 참조 타입, 상태 공유 | class | 참조 시맨틱 |
| 추상화, 다형성 | protocol/interface | 의존성 역전 |
| 제한된 케이스 집합 | enum | 패턴 매칭 |
| 상태 격리 필요 | actor (해당 언어 지원 시) | 동시성 안전 |

## 프로젝트 구조 인식

폴더 구조로 아키텍처를 파악한다:

- Domain/Entities, UseCases, Repositories: Clean Architecture
- Features/Model, View, ViewModel: MVVM
- Controllers, Models, Views: MVC
- src/components, src/services: 레이어드

아키텍처에 맞는 위치에 새 코드를 배치한다.

## 하이브리드 프로젝트 검증

여러 언어/프레임워크를 사용하는 프로젝트:

- 브릿징 헤더, FFI, 바인딩 파일 확인
- 한 언어에서 다른 언어로 노출된 심볼만 사용 가능
- 네이밍 규칙이 양쪽에서 자연스러운지 확인

## 라이브러리 API 검증 5단계

1. 의존성 파일 확인: 해당 라이브러리가 의존성 목록에 있는가?
2. 버전 확인: 프로젝트에서 사용 중인 버전 확인
3. 코드베이스 내 사용 패턴 검색: 기존 사용처 참조
4. API 미숙지 시: Context7 resolve-library-id → query-docs로 공식 문서 확인
5. 불확실 시: @unverified 주석으로 표시하고 사용자 확인 요청

## 검증 실패 시 폴백 동작

1. 사용자에게 질문한다. 추측하지 않는다.
2. stub이나 placeholder를 넣지 않는다.
3. 기존 유사 코드를 보여주고 사용자가 선택하도록 한다.
4. Context7, 공식 문서, 웹 검색으로 추가 확인한다.

## 환각 패턴 방지

| 패턴 | 대응 |
|------|------|
| 존재하지 않는 API 발명 | Grep, Context7로 검증 |
| 잘못된 메서드 시그니처 | 실제 정의 확인 |
| 존재하지 않는 모듈 import | 의존성 파일 확인 |
| Deprecated API 사용 | 최신 대체 API 확인 |
| 버전 추측 | 프로젝트 선언 버전 기준 |

## 미검증 심볼 표시

검증이 불가능한 심볼 사용 시:

```
// @unverified: ExternalAPI.fetchData - Context7 또는 문서로 확인 필요
```

사용자에게 검증/확인 요청을 명시한다.

## 코드 작성 전 체크리스트

```
□ 참조하는 타입/함수/모듈이 프로젝트에 존재하는가?
□ 패키지 매니저 파일에 해당 의존성이 있는가?
□ import/require 경로가 올바른가?
□ 함수 시그니처와 파라미터가 맞는가?
□ 기존 아키텍처/패턴을 따르는가?
□ 컴파일/실행 가능한 완전한 코드인가?
□ 사용하려는 API가 해당 버전에 존재하는가?
□ Deprecated 여부를 확인했는가?
□ 사용자 허락 없이 새 타입/클래스를 자동 생성하지 않는다.
```

## 코드 생성 규칙

1. 사용자 허락 없이 타입/클래스/모듈을 자동 생성하지 않는다.
2. 컴파일 가능한 완전한 코드를 산출한다. stub, placeholder, TODO 주석으로 끝내지 않는다.
3. 기존 프로젝트 아키텍처/패턴을 따른다.
4. 비슷한 기존 코드가 있으면 패턴을 참고한다.

## 오류 방지

- 함수 시그니처: 파라미터 타입/개수/순서 확인
- 프로퍼티/필드: 존재 여부 및 타입 확인
- 커스텀 타입: 정의 위치와 public/export 여부 확인
- 환경 변수/설정: 참조하는 키가 실제로 사용되는가 확인

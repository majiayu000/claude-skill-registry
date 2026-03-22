---
name: deep-search
description: 다중 전략 코드베이스 심층 탐색 워크플로우. Grep, SemanticSearch, Glob를 병렬로 실행하여 심볼, 패턴, 의존성을 종합적으로 분석. Use when performing deep codebase analysis or when searching for complex code patterns and dependencies.
---

# Deep Search — 다중 전략 코드베이스 탐색

다양한 검색 전략을 병렬로 실행하여 코드베이스를 심층 탐색합니다.
단일 검색으로는 찾기 어려운 관계, 패턴, 숨겨진 의존성을 발견합니다.

## 참조 룰

Read tool로 읽어 적용:
- `.claude/skills/code-accuracy/SKILL.md` — 심볼 존재 확인 + 라이브러리 API 검증

## 4-Step 워크플로우

### Step 1: 탐색 목표 정의
- 무엇을 찾는가? (심볼, 패턴, 관계, 영향 범위)
- 어디서 찾는가? (전체/특정 모듈/특정 레이어)
- 왜 찾는가? (구현 참조, 영향 분석, 의존성 파악)

### Step 2: 병렬 3-Track 검색

Track A — 정확 매칭 (Grep): 타입명, 심볼명, import/use 패턴으로 정확 검색
Track B — 의미 검색 (SemanticSearch): "이 기능은 어떻게 구현되어 있는가?" 형태의 질문
Track C — 파일 패턴 (Glob): 네이밍 컨벤션, 디렉터리 구조 기반 파일 탐색

3개 Track은 반드시 동시 실행합니다.

### Step 3: 의존성 추적
- import/use 관계 그래프, 순환 참조 탐지
- 프로토콜/인터페이스 채택 관계
- 타입 참조 (파라미터, 리턴, 프로퍼티)

### Step 4: 구조화 리포트
발견 파일, 의존성 관계(Mermaid), 주요 발견, 영향 범위, 추가 탐색 권장 항목을 정리합니다.

## 시나리오별 전략

Feature 구현 전: 유사 구현 검색, API/Repository 확인

리팩토링 전: 수정 대상 참조처, 상속/프로토콜 체인, 테스트 참조

버그 추적: 에러 메시지/타입 검색, 호출 체인 추적

레거시 분석: 혼용 패턴, 브릿징 참조, 레거시 코드 위치 파악

## 원칙

- 병렬 우선: 3-Track 동시 실행
- 증거 기반: 모든 결과에 소스 경로 명시
- 점진적 심화: 초기 결과 기반 추가 탐색
- 범위 제한: 목표와 무관한 결과 필터링

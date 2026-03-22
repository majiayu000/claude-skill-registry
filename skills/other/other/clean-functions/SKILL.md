---
name: clean-functions
description: 함수/메서드 리팩토링, 코드 리뷰 시 Clean Functions 원칙을 적용. Use when refactoring functions, reviewing method quality, or designing new function signatures.
---

# Clean Functions 원칙

## 5단계 리뷰 워크플로우

1. 코드 입력 수집: 대상 코드를 받아 언어 식별, 개요 파악, 초기 인상 정리
2. 크기 분석: 각 함수의 줄 수, 들여쓰기 깊이, 중첩 구조 측정
3. 단일 책임 검토: 한 가지 일만 하는지, 추상화 일관성, 함수명 품질 확인
4. 추출 대상 식별: Extract Method/Class 후보 도출
5. 리팩토링 제안: 구체적 개선안 및 Before/After 비교 제시

## 리팩토링 시그널 테이블

| 시그널 | 설명 | 조치 |
|--------|------|------|
| 함수 50줄 이상 | 숨겨진 클래스 존재 | Extract Class 검토 |
| 들여쓰기 4단계 이상 | 과도한 중첩 | Extract Method, Early Return |
| 함수명에 "and" 포함 | 여러 책임 혼재 | 함수 분리 |
| 주석으로 섹션 구분 | 블록 단위 추출 필요 | Extract Method |
| 고수준/저수준 혼합 | 추상화 수준 불일치 | 레벨별 함수 분리 |
| 여러 변수 공유하는 긴 함수 | Extract Method Object 대상 | 별도 타입 추출 |
| if/guard/while 내부 로직 | 추출 후보 | Extract Method |
| 3번 이상 반복 | DRY 위반 | 공통 함수 추출 |

## 크기 판정 기준

| 판정 | 줄 수 | 들여쓰기 | 설명 |
|------|-------|----------|------|
| Clean | 20줄 이내 | 2단계 이내 | 이상적 상태 |
| Warning | 20~50줄 | 3단계 | 주의 필요, 개선 검토 |
| Refactor | 50줄 이상 | 4단계 이상 | 즉시 리팩토링 권장 |

## Extract Method 대상 패턴

다음 패턴이 보이면 별도 함수로 추출:

- if/guard/while 블록 내부 로직
- 주석으로 설명된 코드 블록 (주석 → 함수명으로 대체)
- 3줄 이상의 연속된 관련 코드
- 콜백/핸들러 내부 로직
- 동일 로직 3번 이상 반복

형식:
```
Extract Method 대상
- 위치: [함수명] 내 [줄 번호]
- 현재 코드: (간략히)
- 추출 후 함수명 제안: [제안명]
- 이유: [왜 추출해야 하는지]
```

## Extract Class 대상 패턴

다음 패턴이 보이면 별도 타입으로 추출:

- 여러 변수를 공유하는 긴 함수
- 50줄 이상의 복잡한 로직
- 여러 책임이 혼합된 함수
- 계층 간 책임이 혼재된 코드

형식:
```
Extract Class 대상
- 현재 함수: [함수명]
- 현재 위치: [클래스/모듈]
- 추출할 타입명 제안: [타입명]
- 포함할 메서드들: [목록]
- 의존할 타입들: [목록]
- 이유: [왜 추출해야 하는지]
```

## Clean Architecture 계층 추출 가이드

| 계층 | 책임 | 타입 예시 | 의존 방향 |
|------|------|----------|----------|
| Presentation | UI 로직, 사용자 입력, 화면 상태 | View, ViewModel, Controller, Coordinator | → Domain |
| Domain | 비즈니스 로직, 도메인 규칙, 엔티티 | Entity, ValueObject, UseCase, Repository Protocol | (의존 없음) |
| Data | 데이터 접근, 외부 통신, 영속성 | Repository Impl, DataSource, DTO, Mapper | → Domain |

의존성 규칙:
- Presentation → Domain ← Data (올바른 방향)
- Domain은 구체적인 Data 구현에 의존하지 않음
- Data는 Domain의 Protocol에만 의존 (DIP 적용)

계층별 추출 시점:
- UI 레이어에 비즈니스 로직이 있으면 → UseCase로 추출
- 비즈니스 레이어에 네트워크/DB 코드가 있으면 → Repository로 추출
- Entity가 DTO를 직접 참조하면 → Mapper로 분리

## 단일 책임 및 기타 원칙

- 한 함수는 한 가지 일만 수행
- 인자: 0~2개 이상적, 3개 최대, 그 이상은 객체로 묶기
- 이름이 "check", "validate"이면 수정 금지 (검사만 또는 수정만 수행)
- 비즈니스 로직과 에러 처리 분리
- Guard clause로 조기 반환, 중첩 if 대신 early return
- DRY: 3번 이상 반복되면 추출

## 리팩토링 단계 규칙

1. 가장 깊은 중첩부터 Extract 시작
2. 한 번에 하나의 리팩토링만 수행
3. 각 리팩토링 후 Before/After 비교 제시
4. 의존성 방향 검증 (Presentation → Domain ← Data)
5. 언어별 컨벤션 준수 (프로젝트 코딩 가이드 참조)

## 최종 리뷰 체크리스트

리팩토링 시그널 재확인:
- [ ] 함수 50줄 이상 → Extract Class
- [ ] 들여쓰기 4단계 이상 → Extract Method
- [ ] 함수명에 "and" → 함수 분리
- [ ] 주석으로 섹션 구분 → Extract Method
- [ ] 추상화 레벨 혼합 → 레벨별 함수 분리
- [ ] 중첩 if/guard → Early Return 또는 Extract

아키텍처 체크:
- [ ] UI 레이어에 비즈니스 로직 없음
- [ ] 비즈니스 레이어에 네트워크/DB 코드 없음
- [ ] Domain이 외부 프레임워크에 직접 의존하지 않음
- [ ] Repository는 Protocol로 정의
- [ ] DTO와 Entity 분리, Mapper로 변환

언어별 체크:
- [ ] 프로젝트 언어의 Early Return 패턴 적용
- [ ] private/내부 메서드 배치 순서 적절
- [ ] 프로젝트 네이밍 컨벤션 준수

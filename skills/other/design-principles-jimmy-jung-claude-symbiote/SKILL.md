---
name: design-principles
description: 객체지향 설계 원칙 및 SOLID 원칙 통합 가이드. Use when designing class hierarchies, applying design patterns, reviewing object-oriented code structure, or applying SOLID principles during architecture design and refactoring.
---

# 설계 원칙 (OOP + SOLID)

객체지향 설계와 SOLID 원칙을 통합한 가이드. 언어/플랫폼에 무관하게 적용 가능하다.

## 객체지향 핵심 원칙

### 캡슐화
- 구현은 숨기고, 동작만 노출한다.
- 내부 상태를 직접 노출하지 않는다.

### 객체를 메시지 협력자로 다루기
- 객체는 역할(Role), 책임(Responsibility), 협력(Collaboration) 기준으로 도출한다.
- 객체가 제공해야 하는 기능(무엇) 중심으로 설계하고, "어떻게"는 숨긴다.
- 절차형 설계보다 메시지 기반 협력 모델을 우선한다.

### 상속과 조합
- 상속보다 조합을 우선한다.
- "is-a" 관계일 때만 상속을 고려한다.
- 상속은 강한 결합을 만든다.

### 다형성
- 같은 인터페이스로 다른 동작을 제공한다.
- 런타임에 구현체가 결정된다.

### 설계 시 클래스 다이어그램
- 정적 구조 설계 결과를 Mermaid classDiagram으로 표현한다.
- interface는 `<<protocol>>`, 구현은 `<|..`, 상속은 `<|--`, 의존은 `..>` 사용.

## SOLID 개요 및 적용 순서

### 적용 우선순위와 근거

1. DIP: 의존성 역전 우선 (의존성 방향이 가장 중요)
2. SRP: 책임 분리 (Actor별 모듈 분리)
3. OCP: 확장 지원 (수정 없이 확장)
4. ISP: 인터페이스 분리 (클라이언트별 최소 인터페이스)
5. LSP: 치환 가능성 (계약 준수)

DIP를 먼저 처리하면 고수준 정책이 저수준 세부사항으로부터 보호된다. 이후 SRP로 책임을 분리하고, OCP로 확장 포인트를 만들고, ISP로 인터페이스를 세분화하며, 마지막으로 LSP로 상속 구조를 정리한다.

## SOLID 원칙별 상세

### SRP (단일 책임)

정의: 한 모듈은 하나의 Actor에게만 책임을 진다. 책임 = 변경 이유 = Actor.

위반 감지 패턴:
- 클래스 설명에 "그리고(and)"가 들어가는가?
- 변경 이유가 2가지 이상인가?
- 테스트 시 Mock이 3개 이상 필요한가?
- 파일이 300줄 이상인가?
- 두 개발자가 동시에 같은 클래스를 수정하려 하는가?
- God Class: 너무 많은 책임을 가진 클래스

액터 식별: 누가 이 코드를 변경하려 하는가? 변경을 요청하는 사람/역할이 몇 명인가?

리팩토링 방식:
- Actor별로 클래스 분리
- Facade 패턴으로 기존 인터페이스 유지하면서 내부 분리
- Repository, Coordinator 등 패턴 적용

예시 (의사코드):

```
// Before: Fat Class
class UserManager {
    validateEmail()
    saveToDatabase()
    sendWelcomeEmail()
}

// After: 책임별 분리
class UserValidator { validateEmail() }
class UserRepository { save() }
class WelcomeEmailSender { send() }
```

### OCP (개방-폐쇄)

정의: 확장에는 열려 있고 수정에는 닫혀 있어야 한다.

위반 감지 패턴:
- 새 기능 추가 시 기존 클래스를 수정하는가?
- switch/if-else가 여러 곳에 중복되는가?
- enum에 case 추가 시 여러 파일을 수정하는가?
- Rigidity: 작은 변경이 큰 영향
- Fragility: 한 곳 수정이 예상치 못한 곳에 영향

리팩토링 방식:
- Strategy/Policy 패턴으로 알고리즘 교체 가능하게
- protocol/interface + 구현체로 확장
- if-else/switch 체인을 추상화로 대체

예시 (의사코드):

```
// Before: 수정 필요
class CheckOut {
    processPayment(type) {
        if type == "Cash" then ...
        else if type == "CreditCard" then ...
        // 새 타입 추가 시마다 수정
    }
}

// After: 확장만 가능
interface PaymentMethod { pay(amount) }
class CheckOut {
    processPayment(method: PaymentMethod) {
        method.pay(amount)
    }
}
// 새 결제 수단 = 새 클래스 추가, CheckOut 수정 없음
```

### LSP (리스코프 치환)

정의: 하위 타입은 상위 타입으로 대체 가능해야 한다. 상위 타입의 계약을 지켜야 한다.

계약 구성:
- 사전조건(Precondition): 서브타입은 약화시키면 안 됨 (더 강하게는 OK)
- 사후조건(Postcondition): 서브타입은 강화시키면 안 됨 (더 약하게는 OK)
- 불변식(Invariant): 서브타입은 불변식을 유지해야 함

위반 감지 패턴:
- instanceof 체크나 타입 캐스팅을 사용하는가?
- 서브타입에서 메서드가 fatalError/예외를 던지는가?
- 서브타입이 기반 타입의 예상 동작과 다른가?
- 부모 동작을 무시하거나 예상치 못한 예외를 던지는가?

리팩토링 방식:
- 상속 대신 composition 고려
- protocol/interface 기반 설계로 전환
- IS-A 관계가 소프트웨어 계약과 맞지 않으면 상속 제거

### ISP (인터페이스 분리)

정의: 클라이언트는 사용하지 않는 인터페이스에 의존하면 안 된다.

위반 감지 패턴:
- interface에 10개 이상의 메서드가 있는가?
- 구현 시 fatalError나 빈 구현이 있는가?
- 클라이언트가 interface의 일부만 사용하는가?
- Fat Interface: 여러 역할을 한 interface에 몰아넣음

리팩토링 방식:
- 역할별 interface 분리
- 클라이언트 관점에서 설계 (구현체 관점 X)
- Readable, Writable, Searchable 등 역할 기반 분리

예시 (의사코드):

```
// Before: Fat Interface
interface DataSource {
    fetch(), save(), delete(), search()
}

// After: 역할별 분리
interface Fetchable { fetch() }
interface Savable { save() }
interface Deletable { delete() }
interface Searchable { search() }
```

### DIP (의존성 역전)

정의: 고수준 모듈은 저수준 모듈에 의존하지 않고 추상화에 의존한다.

고수준/저수준 구분:
- 고수준: 비즈니스 로직, UseCase, 정책
- 저수준: 데이터베이스, UI, 네트워크, 하드웨어
- 추상화: protocol/interface (고수준이 정의)

위반 감지 패턴:
- 구체 클래스를 직접 생성하는가?
- import에 저수준 모듈이 있는가?
- 테스트 시 실제 네트워크/DB가 필요한가?
- Repository pattern 없이 저수준을 직접 사용하는가?

리팩토링 방식:
- protocol/interface 기반 의존성 주입
- Repository 패턴: 데이터 접근을 추상화
- Main/Composition Root에서 구체 구현체 조립

## 상황별 디자인 패턴 추천

| 상황 | 패턴 | 용도 |
|------|------|------|
| 알고리즘 교체 | Strategy | 조건 분기 확장 |
| 이벤트 알림 | Observer | 상태 변경 구독 |
| 객체 생성 위임 | Factory | 생성 로직 캡슐화 |
| 데이터 접근 추상화 | Repository | DIP, 테스트 용이 |
| 책임 추가 | Decorator | 기존 동작 확장 |

## 안티패턴

- God Object: 너무 많은 책임
- Spaghetti Code: 얽힌 제어 흐름
- Circular Dependencies: 순환 참조
- Lava Flow: 놓치기 쉬운 레거시
- Golden Hammer: 한 도구만 남용

## 설계 검토 체크리스트

```
□ 이 클래스가 변경되는 이유는 몇 가지인가 (SRP)
□ 새 요구사항 시 기존 코드를 수정해야 하는가 (OCP)
□ 하위 타입이 상위 타입의 계약을 지키는가 (LSP)
□ 인터페이스가 너무 크지 않은가 (ISP)
□ 구체 클래스에 직접 의존하는가 (DIP)
□ 조합으로 해결할 수 있는가 (상속 대신)
□ Actor를 식별했는가?
□ protocol/interface가 고수준에 정의되어 있는가?
```

## 원칙 적용 결정표

| 질문 | 적용 원칙 |
|------|----------|
| 의존성 방향이 잘못되었는가? | DIP |
| 클래스가 여러 변경 이유를 가지는가? | SRP |
| 새 기능 추가 시 기존 코드 수정이 필요한가? | OCP |
| interface에 사용하지 않는 메서드가 있는가? | ISP |
| 상속 관계에서 계약 위반이 있는가? | LSP |
| if-else/switch가 계속 늘어나는가? | OCP, Strategy |
| 테스트 시 Mock을 쓸 수 없는가? | DIP |

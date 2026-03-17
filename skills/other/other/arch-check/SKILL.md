---
name: arch-check
description: Clean Architecture 규칙 준수 여부를 검증합니다. core→infra 의존 방향, 인터페이스 구현, 백테스트 재사용 등을 점검합니다.
allowed-tools: Read, Grep, Glob
---

# 아키텍처 규칙 검증

프로젝트의 Clean Architecture 규칙 준수 여부를 전체 코드베이스 대상으로 검증합니다.

## 실행 절차

### 1단계: 의존 방향 검증 (core → infra)

`src/core/` 디렉토리의 모든 `.py` 파일에서 다음 패턴을 검색합니다:

**위반 패턴** (있으면 안 됨):
- `from src.infra` 또는 `import src.infra`
- `from src.utils` 또는 `import src.utils` (core는 utils에도 의존하지 않아야 함)
- `from src.backtest` 또는 `import src.backtest`

**허용 패턴**:
- `from src.core` 또는 `import src.core` (core 내부 참조는 허용)
- 표준 라이브러리 및 외부 패키지 (pandas, typing, abc 등)

### 2단계: 인터페이스 구현 검증

1. `src/core/interfaces.py`에서 추상 클래스(ABC) 목록을 추출합니다:
   - `IDataProvider`
   - `IBrokerAdapter`
   - `INotifier`

2. 각 인터페이스에 정의된 `@abstractmethod` 목록을 추출합니다

3. `src/infra/` 디렉토리에서 해당 인터페이스를 구현하는 클래스를 찾습니다:
   - 클래스 정의에서 인터페이스를 상속하는지 확인
   - 모든 추상 메서드가 구현되었는지 확인

4. `src/backtest/` 디렉토리에서도 인터페이스 구현 클래스를 확인합니다

### 3단계: 백테스트 재사용 검증

`src/backtest/` 디렉토리의 파일을 분석하여:

1. **core 로직 직접 재사용 확인**: 다음 클래스들을 import하여 사용하는지 확인
   - `RegimeAnalyzer`
   - `VolatilityTargeter`
   - `Rebalancer`
   - `IndicatorCalculator`

2. **코드 분기 없음 확인**: 백테스트 전용 로직이 core에 포함되어 있지 않은지 확인
   - `src/core/` 파일에서 `backtest`, `is_backtest`, `test_mode` 등의 패턴 검색
   - 이런 분기가 있으면 위반

### 4단계: 순환 의존성 검증

모듈 간 import를 추적하여 순환 참조가 없는지 확인합니다:
- `src/core/` → 외부 의존 없어야 함
- `src/infra/` → `src/core/`만 의존 가능
- `src/utils/` → `src/core/`만 의존 가능 (또는 독립)
- `src/backtest/` → `src/core/`, `src/infra/`, `src/utils/` 의존 가능

## 결과 출력 형식

```
## 아키텍처 검증 결과

### 요약
- 검증 항목: 4개
- 통과: N개
- 위반: N개

### 1. 의존 방향 (core → infra)
✅ 통과 / ❌ 위반
- [위반 시] 파일명:라인번호 - `from src.infra.xxx import yyy`

### 2. 인터페이스 구현
✅ 통과 / ❌ 위반
- IDataProvider: 구현체 [YFinanceLoader, BacktestDataLoader]
  - fetch_ohlcv: ✅ 구현됨
  - fetch_vix: ✅ 구현됨
- IBrokerAdapter: 구현체 [MockBroker, KisBroker, BacktestBroker]
  - get_portfolio: ✅ 구현됨
  - execute_orders: ✅ 구현됨
  - fetch_current_prices: ✅ 구현됨
- INotifier: 구현체 [SlackNotifier, TelegramNotifier]
  - send_message: ✅ 구현됨
  - send_alert: ✅ 구현됨

### 3. 백테스트 재사용
✅ 통과 / ❌ 위반
- core 로직 재사용: RegimeAnalyzer ✅, VolatilityTargeter ✅, Rebalancer ✅
- core 코드 분기: 없음 ✅

### 4. 순환 의존성
✅ 통과 / ❌ 위반
- [위반 시] moduleA → moduleB → moduleA 순환 경로 표시
```

## 주의사항
- 이 스킬은 읽기 전용입니다. 코드를 직접 수정하지 않습니다.
- 위반 사항 발견 시 수정 방향을 제안하고 사용자가 결정하도록 합니다.
- `__init__.py`의 re-export는 위반으로 간주하지 않습니다.

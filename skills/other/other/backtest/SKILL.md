---
name: backtest
description: 백테스트를 실행하고 전략 성과를 분석합니다. 날짜 범위와 초기 자본을 지정할 수 있습니다.
argument-hint: "[start-date] [end-date] [initial-cash] (예: 2020-01-01 2023-12-31 10000)"
allowed-tools: Bash(pip install *), Bash(python *), Read, Grep, Glob
---

# 백테스트 실행 및 분석

백테스트를 실행하고 전략의 성과를 분석하는 스킬입니다.

## 실행 절차

### 1단계: 의존성 설치
```
pip install -r requirements.txt
```

### 2단계: 인자 파싱

`$ARGUMENTS`에서 파라미터를 추출합니다:
- 첫 번째 인자: `start_date` (기본값: 3년 전, 형식: YYYY-MM-DD)
- 두 번째 인자: `end_date` (기본값: 오늘, 형식: YYYY-MM-DD)
- 세 번째 인자: `initial_cash` (기본값: 10000)

### 3단계: 백테스트 실행

다음 명령을 실행합니다:
```
python -c "from src.backtest.runner import run_backtest; run_backtest('{start_date}', '{end_date}', {initial_cash})"
```

### 4단계: 결과 분석

실행 출력에서 다음 지표를 추출하여 분석합니다:

#### 수익률 지표
- **최종 자산**: 초기 자본 대비 최종 포트폴리오 가치
- **CAGR**: 연평균 복합 성장률
- **총 수익률**: (최종 - 초기) / 초기

#### 국면별 분석
- 출력에서 regime 정보가 있으면 Bull/Bear/Crash/Sideways 구간별 성과를 요약합니다

## 에러 처리

### 데이터 다운로드 실패 시
- yfinance API 오류인지 확인
- 날짜 범위가 유효한지 점검
- 네트워크 문제 가능성 안내

### 계산 오류 시
- `src/backtest/runner.py`를 읽어 에러 발생 지점 분석
- `src/backtest/components.py`의 BacktestDataLoader, BacktestBroker 확인
- `src/utils/calculator.py`의 데이터 요구사항 확인 (최소 253 거래일 필요)

### 일반 오류 시
- 스택 트레이스를 분석하여 원인 파악
- 관련 소스 코드를 읽고 수정 방안 제시

## 결과 출력 형식

```
## 백테스트 결과

### 설정
- 기간: {start_date} ~ {end_date}
- 초기 자본: ${initial_cash}

### 성과 요약
- 최종 자산: $XX,XXX
- 총 수익률: XX.X%
- CAGR: XX.X%

### 국면별 분석 (가능한 경우)
- Bull 구간: N일, 평균 수익률 X.X%
- Bear 구간: N일, 평균 수익률 X.X%
- Crash 구간: N일, 평균 수익률 X.X%

### 참고사항
- 실행 중 발생한 경고나 스킵된 날짜 등
```

## 주의사항
- 백테스트는 과거 데이터 기반이며, 미래 수익을 보장하지 않습니다
- yfinance에서 대량 데이터를 다운로드하므로 실행 시간이 걸릴 수 있습니다
- `_live.py` 테스트와 달리 실제 매매는 발생하지 않습니다

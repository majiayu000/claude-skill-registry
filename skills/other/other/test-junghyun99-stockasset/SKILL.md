---
name: test
description: 프로젝트 테스트를 실행하고 결과를 분석합니다. 테스트 실패 시 원인을 분석하고 수정 방안을 제시합니다.
argument-hint: "[test-path] (예: tests/test_core_logic.py)"
allowed-tools: Bash(pip install *), Bash(pytest *), Read, Grep, Glob
---

# 테스트 실행 및 분석

프로젝트의 테스트를 실행하고 결과를 분석하는 스킬입니다.

## 실행 절차

### 1단계: 의존성 설치
테스트 실행 전에 필요한 패키지를 설치합니다:
```
pip install -r requirements.txt
```

### 2단계: pytest 실행

1. **인자가 없는 경우**: 전체 테스트를 실행합니다
   ```
   pytest --cov=src --cov-report=term-missing --cov-fail-under=80 tests/
   ```

2. **특정 파일/경로가 지정된 경우**: 해당 테스트만 실행합니다
   ```
   pytest --cov=src --cov-report=term-missing $ARGUMENTS
   ```

## 결과 분석 규칙

### 테스트 성공 시
- 전체 통과 건수와 커버리지 퍼센트를 요약합니다
- 커버리지 80% 미만인 모듈이 있으면 경고하고 어떤 라인이 누락되었는지 알려줍니다

### 테스트 실패 시
다음 순서로 분석합니다:

1. **실패한 테스트 목록**을 정리합니다
2. 각 실패에 대해:
   - 에러 메시지와 스택 트레이스를 분석합니다
   - 관련 소스 코드를 읽어서 원인을 파악합니다
   - 수정 방안을 제시합니다
3. 테스트 코드 자체의 문제인지, 프로덕션 코드의 버그인지 구분합니다

### 커버리지 부족 시
- `--cov-report=term-missing` 결과에서 커버리지가 낮은 파일을 식별합니다
- 누락된 라인 번호를 확인하고 어떤 테스트를 추가하면 좋을지 제안합니다

## 주의사항
- `_live.py` 접미사 파일은 실제 API를 호출하므로, 명시적 요청이 없으면 실행하지 않습니다
- 외부 API 호출은 반드시 mock 처리되어 있어야 합니다
- CI 환경과 동일한 기준(80% 커버리지)을 적용합니다

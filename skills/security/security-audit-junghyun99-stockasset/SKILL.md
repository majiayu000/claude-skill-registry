---
name: security-audit
description: 코드베이스의 보안 취약점을 점검합니다. 시크릿 유출, 인증 처리, API 보안, 로그 노출 등을 검사합니다.
allowed-tools: Bash(git log *), Bash(git diff *), Read, Grep, Glob
---

# 보안 점검

전체 코드베이스를 대상으로 보안 취약점을 점검하는 스킬입니다.

## 실행 절차

### 1단계: 시크릿 하드코딩 탐지

전체 `src/` 및 `tests/` 디렉토리에서 다음 패턴을 검색합니다:

#### 검색 패턴
- API 키: `api_key\s*=\s*["']`, `app_key\s*=\s*["']`, `secret\s*=\s*["']`
- 토큰: `token\s*=\s*["'][^"']{10,}`, `bearer\s*["']`
- 비밀번호: `password\s*=\s*["']`, `passwd\s*=\s*["']`
- URL에 포함된 인증 정보: `https?://[^@\s]*:[^@\s]*@`
- 웹훅 URL: `hooks.slack.com/services/T[A-Z0-9]+`
- 한국투자증권 관련: `KIS_APP_KEY`, `KIS_APP_SECRET`, `KIS_ACC_NO` 값이 직접 기입되어 있는지

#### 허용 예외
- `os.getenv()`, `os.environ.get()`, `os.environ[]`로 읽어오는 경우는 정상
- 테스트의 mock 데이터에서 `"fake_key"`, `"test_token"` 등 명시적 더미값은 허용
- `config.py`에서 환경변수 기본값(fallback)은 빈 문자열 `""` 또는 `None`이어야 함

### 2단계: .env 및 민감 파일 보호 점검

1. `.gitignore`에 다음 항목이 포함되어 있는지 확인:
   - `.env`
   - `.env.*`
   - `*.pem`, `*.key` (인증서/키 파일)

2. git 히스토리에 `.env`가 커밋된 적 있는지 확인:
   ```
   git log --all --diff-filter=A -- .env .env.*
   ```

3. 현재 스테이징 영역에 민감 파일이 포함되어 있는지 확인:
   ```
   git diff --staged --name-only
   ```

### 3단계: 인증 및 API 보안 점검

`src/infra/` 디렉토리의 파일을 분석합니다:

#### broker.py (KisBroker)
- OAuth 토큰이 메모리에만 저장되고 파일에 기록되지 않는지
- API 호출 시 HTTPS를 사용하는지 (`http://`가 아닌 `https://`)
- 토큰 만료 처리가 되어 있는지
- API 응답의 에러 처리가 있는지 (인증 실패 시 토큰 재시도 등)

#### notifier.py (SlackNotifier, TelegramNotifier)
- 웹훅 URL이 환경변수에서 로드되는지
- 알림 메시지에 계좌번호, API 키 등이 포함되지 않는지

#### data.py (YFinanceLoader)
- 외부 API 호출에 타임아웃이 설정되어 있는지

### 4단계: 로그 내 민감 정보 노출 점검

`src/` 디렉토리에서 로깅 호출을 분석합니다:

- `logger.info()`, `logger.warning()`, `logger.error()`, `print()` 호출 검색
- 로그 메시지에 다음이 포함되는지 확인:
  - 포트폴리오 전체 내역 (계좌번호 포함 가능성)
  - API 응답 원문 (토큰 포함 가능성)
  - 주문 실행 시 인증 헤더

### 5단계: 입력 검증 및 인젝션 점검

- `subprocess`, `os.system`, `eval`, `exec` 사용 여부 확인
- 외부 입력(환경변수, API 응답)이 직접 명령어에 삽입되는지 확인
- `requests` 호출에서 URL이 사용자 입력으로 구성되는지 확인

## 결과 출력 형식

```
## 보안 점검 결과

### 요약
- 점검 항목: 5개
- 심각: N건
- 경고: N건
- 통과: N건

### 1. 시크릿 하드코딩
✅ 발견 없음 / ❌ 발견됨
- [심각] 파일명:라인번호 - 설명

### 2. 민감 파일 보호
✅ .gitignore 설정 정상 / ❌ 누락 항목 있음
- .env: ✅ .gitignore에 포함
- git 히스토리: ✅ .env 커밋 이력 없음

### 3. 인증 및 API 보안
✅ 정상 / ❌ 문제 발견
- HTTPS 사용: ✅
- 토큰 파일 저장: ✅ 없음
- 타임아웃 설정: ✅ / ❌

### 4. 로그 민감 정보
✅ 노출 없음 / ❌ 노출 가능성
- [경고] 파일명:라인번호 - 설명

### 5. 인젝션 위험
✅ 발견 없음 / ❌ 발견됨
- [심각] 파일명:라인번호 - 설명
```

## 주의사항
- 이 스킬은 읽기 전용입니다. 코드를 직접 수정하지 않습니다.
- `.env` 파일 자체는 읽지 않습니다 (deny 규칙 준수).
- 발견된 취약점은 심각도와 함께 수정 방향을 제시합니다.
- 오탐(false positive)이 있을 수 있으므로 결과를 사용자가 검토해야 합니다.

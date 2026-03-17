---
name: security-review
description: 보안 검토 체크리스트. AWS 자격 증명, 입력 검증, 민감 정보 로깅 등.
---

# 보안 검토 체크리스트

이 프로젝트의 보안 검토 가이드입니다.

## AWS 자격 증명

### 금지 사항
- 하드코딩된 Access Key / Secret Key
- 소스 코드 내 자격 증명
- 커밋된 .env 파일

### 확인 사항
```python
# Bad - 하드코딩
client = boto3.client(
    'ec2',
    aws_access_key_id='AKIA...',        # 금지!
    aws_secret_access_key='...',         # 금지!
)

# Good - 프로필 또는 환경 변수
session = boto3.Session(profile_name='my-profile')
client = session.client('ec2')
```

## 입력 검증

### Account ID 검증
```python
import re

def validate_account_id(account_id: str) -> bool:
    """AWS 계정 ID 형식 검증"""
    return bool(re.match(r'^\d{12}$', account_id))
```

### Region 검증
```python
VALID_REGIONS = [
    'us-east-1', 'us-west-2', 'ap-northeast-2', # ...
]

def validate_region(region: str) -> bool:
    """리전 형식 검증"""
    return region in VALID_REGIONS or region == 'all'
```

### ARN 검증
```python
def validate_arn(arn: str) -> bool:
    """ARN 형식 검증"""
    pattern = r'^arn:aws:[a-z0-9-]+:[a-z0-9-]*:\d{12}:.+'
    return bool(re.match(pattern, arn))
```

## 민감 정보 로깅

### 금지 사항
```python
# Bad - 자격 증명 로깅
logger.info(f"Using credentials: {access_key}")

# Bad - 전체 응답 로깅 (토큰 포함 가능)
logger.debug(f"Response: {response}")
```

### 권장 사항
```python
# Good - 필요한 정보만 로깅
logger.info(f"Processing account: {account_id}")
logger.debug(f"Found {len(instances)} instances")
```

## Bandit 규칙

이 프로젝트에서 스킵하는 규칙:

| 규칙 | 사유 |
|------|------|
| B101 | assert 사용 (테스트에서 정상) |
| B311 | random 사용 (보안 목적 아님) |
| B608 | SQL injection (DuckDB + 내부 데이터) |

### 스캔 명령
```bash
bandit -r cli core plugins -c pyproject.toml
```

## 보안 취약점 체크리스트

### 인젝션
- [ ] SQL 인젝션: 사용자 입력을 DuckDB 쿼리에 직접 사용하지 않음
- [ ] 명령 인젝션: subprocess 사용 시 shell=False
- [ ] 경로 인젝션: 파일 경로 정규화 및 검증

### 인증/인가
- [ ] AWS 자격 증명 하드코딩 없음
- [ ] 최소 권한 원칙 (필요한 IAM 권한만)
- [ ] 세션 토큰 만료 처리

### 데이터 보호
- [ ] 민감 정보 로깅 없음
- [ ] 출력 파일 권한 적절함
- [ ] 임시 파일 안전하게 처리

### 의존성
- [ ] 알려진 취약점 없음 (safety check)
- [ ] 최신 버전 사용

```bash
# 의존성 보안 검사
safety check
pip-audit
```

## 코드 리뷰 포인트

1. **새로운 외부 입력**: 사용자 입력 검증 확인
2. **AWS API 호출**: 에러 핸들링 확인
3. **파일 작업**: 경로 검증 확인
4. **로깅**: 민감 정보 누출 확인
5. **의존성 추가**: 보안 이력 확인

## 보안 이슈 발견 시

1. 즉시 수정 (자격 증명 노출 시 키 로테이션)
2. git history에서 제거 필요 여부 검토
3. 영향 범위 파악
4. 재발 방지 조치

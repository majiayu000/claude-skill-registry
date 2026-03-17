---
name: python-best-practices
description: Python 코딩 표준 및 스타일 가이드. 타입 힌트, import 정렬, 예외 처리 등.
---

# Python Best Practices

이 프로젝트의 Python 코딩 표준입니다.

## 타입 힌트

Python 3.10+ 스타일 사용:

```python
# Good
def process(items: list[str]) -> dict[str, int]:
    ...

# Avoid (Python 3.9 스타일)
from typing import List, Dict
def process(items: List[str]) -> Dict[str, int]:
    ...
```

## Import 정렬

ruff I 규칙을 따름 (isort 호환):

```python
# 1. 표준 라이브러리
import os
from pathlib import Path

# 2. 서드파티
import boto3
from rich.console import Console

# 3. 로컬
from core.parallel import get_client, parallel_collect
```

## Docstring

한글 docstring 허용. Google 스타일 권장:

```python
def analyze_resource(resource_id: str, region: str) -> dict:
    """리소스 분석 수행.

    Args:
        resource_id: AWS 리소스 ID
        region: AWS 리전

    Returns:
        분석 결과 딕셔너리
    """
```

## 문자열 포맷팅

f-string 사용 (ruff UP 규칙):

```python
# Good
name = f"resource-{resource_id}"

# Avoid
name = "resource-{}".format(resource_id)
name = "resource-%s" % resource_id
```

## 예외 처리

구체적인 예외 타입 사용:

```python
# Good
try:
    client.describe_instances()
except ClientError as e:
    if e.response['Error']['Code'] == 'AccessDenied':
        logger.warning("권한 부족")
    raise

# Avoid
try:
    client.describe_instances()
except Exception:
    pass
```

## 컬렉션 처리

리스트 컴프리헨션 선호:

```python
# Good
active = [i for i in instances if i['State'] == 'running']

# 복잡한 경우 generator 사용
def get_active():
    for instance in instances:
        if is_valid(instance) and is_active(instance):
            yield instance
```

## Context Manager

리소스 정리에 with 사용:

```python
with open(file_path, 'r') as f:
    data = f.read()
```

## 상수

모듈 레벨 상수는 대문자:

```python
MAX_RETRIES = 3
DEFAULT_REGION = "ap-northeast-2"
```

## 린트 명령

```bash
ruff check cli core plugins --fix
ruff format cli core plugins
mypy cli core plugins
```

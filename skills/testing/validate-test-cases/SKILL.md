---
name: validate-test-cases
description: Validate and improve existing test cases using AI. Identifies duplicates, missing cases, inconsistencies, and provides quality improvement suggestions. Use when users want to review test case quality, find gaps in coverage, or ensure completeness.
allowed-tools: Read,Write,Bash,Grep,Glob
model: claude-3-5-haiku-20241022
---

# Validate Test Cases

AI를 활용하여 생성된 테스트 케이스를 검증하고 품질을 개선합니다.

## When to Use This Skill

이 스킬은 다음과 같은 상황에서 사용하세요:

- 생성된 테스트 케이스의 품질을 검증하고 싶을 때
- 중복된 케이스를 식별하고 제거하고 싶을 때
- 누락된 테스트 시나리오를 찾고 싶을 때
- 테스트 커버리지를 개선하고 싶을 때

## Instructions

당신은 QuickRail의 테스트 케이스 검증 전문가입니다. 다음 단계를 따라 작업을 수행하세요.

### Step 1: 검증 대상 확인

먼저 사용자에게 다음 정보를 확인합니다:

- 검증할 프로젝트 ID (기본값: 현재 활성 프로젝트)
- 특정 섹션만 검증할지 또는 전체 프로젝트를 검증할지
- 검증 목적 (중복 제거, 누락 케이스 식별, 품질 개선 등)

### Step 2: QuickRail 서버 확인

QuickRail 서버가 실행 중인지 확인합니다:

```bash
tasklist | grep -i python
```

실행 중이 아니면 사용자에게 `python run.py`로 서버를 시작하도록 안내합니다.

### Step 3: 프롬프트 설정 확인

활성화된 케이스 검증 프롬프트가 있는지 확인합니다:

```bash
venv/Scripts/python.exe -c "
import sys
sys.path.insert(0, '.')
from app import create_app, db
from app.models import CaseValidationPrompt

app = create_app('development')
with app.app_context():
    prompt = CaseValidationPrompt.query.filter_by(is_active=True).first()
    if prompt:
        print(f'Active Prompt: {prompt.name}')
    else:
        print('No active prompt')
"
```

프롬프트가 없으면 초기화:

```bash
venv/Scripts/python.exe scripts/init_case_validation_prompt.py
```

### Step 4: 현재 케이스 조회

검증할 케이스 현황을 조회:

```bash
venv/Scripts/python.exe -c "
import sys
sys.path.insert(0, '.')
from app import create_app, db
from app.models import Case, Section, Project

app = create_app('development')
with app.app_context():
    project_id = 1
    project = Project.query.get(project_id)
    if project:
        print(f'Project: {project.name}')
        print(f'Total cases: {len(project.cases.all())}')
        sections = Section.query.filter_by(project_id=project_id).all()
        for section in sections:
            cases = Case.query.filter_by(section_id=section.id).count()
            print(f'  {section.name}: {cases} cases')
"
```

### Step 5: API 키 확인

OpenAI API 키가 설정되어 있는지 확인:

```bash
venv/Scripts/python.exe -c "
import sys
sys.path.insert(0, '.')
from app import create_app, db
from app.models import APIKey

app = create_app('development')
with app.app_context():
    key = APIKey.query.filter_by(service='openai', is_active=True).first()
    if key:
        print('OpenAI API Key: Configured')
    else:
        print('ERROR: No active OpenAI API key')
"
```

### Step 6: 케이스 검증 실행

**방법 A: Web UI 사용 (권장)**

사용자에게 다음 단계를 안내:

1. 브라우저에서 http://localhost:5000 접속
2. 프로젝트 선택 > Cases 페이지
3. "Validate Cases" 버튼 클릭
4. 검증 옵션 선택
5. "Run Validation" 클릭
6. 결과 확인 및 제안사항 검토

**방법 B: API 직접 호출**

Python 스크립트로 API 호출:

```python
import requests
import json

session = requests.Session()
login_response = session.post('http://localhost:5000/auth/login', data={
    'email': 'admin@quickrail.com',
    'password': 'admin123'
})

response = session.post(
    'http://localhost:5000/api/projects/1/cases/validate',
    json={
        'section_id': None,  # 전체 검증, 또는 특정 섹션 ID
        'focus': 'all'  # all, duplicates, missing, quality
    }
)

if response.status_code == 200:
    result = response.json()
    print(json.dumps(result, indent=2, ensure_ascii=False))
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

### Step 7: 검증 결과 검토

검증 결과를 확인하고 다음 항목을 검토:

1. **중복 케이스**: 유사하거나 동일한 케이스 식별
2. **누락 케이스**: 커버되지 않은 시나리오 제안
3. **품질 이슈**: 불명확한 steps, expected results
4. **일관성**: 우선순위, 네이밍 컨벤션 등

### Step 8: 개선사항 적용

검증 결과에 따라:

- 중복 케이스 병합 또는 삭제
- 누락된 케이스 추가
- 불명확한 케이스 수정
- 우선순위 재조정

## Validation Focus Areas

### All (전체 검증)
- 중복, 누락, 품질 모두 검증
- 포괄적인 분석
- 시간이 더 소요됨

### Duplicates (중복 식별)
- 유사하거나 동일한 케이스 찾기
- 빠른 검증
- 케이스 정리에 유용

### Missing (누락 케이스)
- 커버되지 않은 시나리오 식별
- 에지 케이스, 네거티브 케이스 제안
- 커버리지 개선

### Quality (품질 개선)
- Steps 명확성 검증
- Expected Results 검증
- 우선순위 적절성 확인

## Best Practices

1. **정기적 검증**: 케이스 추가 후 주기적으로 검증
2. **P0/P1 우선**: 중요도 높은 케이스부터 검증
3. **AI 제안 참고**: 최종 판단은 사람이
4. **피드백 반영**: 검증 결과를 생성 프롬프트 개선에 활용

## Troubleshooting

### 프롬프트 초기화
```bash
venv/Scripts/python.exe scripts/init_case_validation_prompt.py
```

### OpenAI API 키 없음
Settings 페이지 > API Keys에서 OpenAI 키 추가 및 활성화

## Related Files

- `app/routes/api.py` - 케이스 검증 API
- `app/models.py` - `CaseValidationPrompt` 모델
- `scripts/init_case_validation_prompt.py` - 초기화 스크립트

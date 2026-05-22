---
name: generate-test-cases
description: Generate comprehensive test cases from specification documents using AI in the QuickRail project. Use when users want to create test cases from requirements, spec documents, or feature descriptions. Supports both Web UI and API-based generation with customizable prompts and context engineering.
allowed-tools: Read,Write,Bash,Grep,Glob
model: claude-3-5-haiku-20241022
---

# Generate Test Cases

AI를 활용하여 스펙 문서로부터 테스트 케이스를 자동 생성합니다.

## When to Use This Skill

이 스킬은 다음과 같은 상황에서 사용하세요:

- 사용자가 스펙 문서나 요구사항 문서로부터 테스트 케이스를 생성하고 싶을 때
- 기획서, PRD, 기능 명세서를 기반으로 구조화된 테스트 시나리오가 필요할 때
- 수동으로 케이스를 작성하는 시간을 절약하고 AI의 도움을 받고 싶을 때
- 기존 테스트 케이스의 커버리지를 확장하고 싶을 때

## Prompt Files Architecture

QuickRail은 **모듈형 프롬프트 시스템**을 사용합니다. 각 파일은 명확한 역할을 가집니다:

### 📁 prompt_files/case_gen/

```
prompt_files/case_gen/
├── common_core.md         (필수) 모든 모드 적용 - 절대 규칙
├── common_booster.md      (권장) Balanced/Quality 모드 - 품질 강화
├── spec_digest.md         (선택) Quality 모드 - 스펙 분석
├── rewrite.md             (선택) Quality 모드 - 케이스 개선
├── validate.md            (선택) Quality 모드 - 최종 검증
├── profile_web_app.md     (선택) 웹 앱 특화
├── profile_api.md         (선택) API 테스트 특화
├── profile_mobile.md      (선택) 모바일 앱 특화
└── category_security.md   (선택) 보안 테스트 특화
```

#### 1. common_core.md (필수, 모든 모드)
**용도**: 절대 규칙, 출력 형식, 품질 기준  
**수정 빈도**: 분기 1회 이하  
**핵심 내용**:
- 1 케이스 = 1 기대결과 규칙
- Steps/Expected/Priority 작성법
- JSON 출력 형식
- 테스트 설계 기법 (동등분할, 경계값, 상태전이)

#### 2. common_booster.md (Balanced/Quality 모드)
**용도**: 품질 강화, 필수 커버리지 체크리스트  
**수정 빈도**: 월 1-2회  
**핵심 내용**:
- 8가지 필수 커버리지 영역 (Happy Path, 입력검증, 경계값...)
- 놓치기 쉬운 시나리오 (타이밍, 취소, 브라우저 이슈)
- info_requests 가이드

#### 3. 도메인/카테고리 프롬프트 (선택)
**용도**: 프로젝트 특성별 추가 규칙  
**예시**:
- `profile_web_app.md`: 브라우저 호환성, 반응형, SEO
- `profile_api.md`: HTTP 상태코드, 인증, Rate Limiting
- `category_security.md`: OWASP Top 10, XSS, CSRF

### 프롬프트 수정 가이드

| 상황 | 수정 파일 | 조치 |
|------|-----------|------|
| Steps가 너무 추상적 | `common_core.md` | "좋은/나쁜 예시" 섹션에 실제 케이스 추가 |
| 특정 케이스 항상 누락 | `common_booster.md` | 해당 체크리스트 항목을 "필수" 표시 및 예시 추가 |
| 새 프로젝트 타입 | 새 `profile_*.md` 생성 | common_core 참고하여 구조 유지 |
| 보안 강화 필요 | `category_security.md` | OWASP 최신 버전 반영 |

**프롬프트 수정 후 테스트**:
```bash
# 간단한 스펙으로 테스트
curl -X POST http://localhost:5000/api/projects/1/cases/ai-generate \
  -d "spec_text=사용자 로그인 기능" \
  -d "generation_mode=balanced" \
  -H "Cookie: session=..."
```

---

## Instructions

당신은 QuickRail의 테스트 케이스 생성 전문가입니다. 다음 단계를 **정확히** 따라 작업을 수행하세요.

### Step 1: 요구사항 수집 및 검증

먼저 사용자에게 다음 정보를 확인합니다:

#### 필수 정보
- **스펙 문서 경로 또는 텍스트 내용**
  - 파일 경로 제공 시 → Read 도구로 내용 읽기
  - 텍스트 직접 제공 시 → 그대로 사용
  - 스펙 품질 간단 검증:
    ```
    ✅ 기능 목적이 명시되어 있는가?
    ✅ 입력/출력이 구체적인가?
    ✅ 성공/실패 시나리오가 있는가?
    
    ❌ 품질이 낮으면 사용자에게 스펙 개선 제안
    ```

#### 선택 정보 (기본값 제공)
- **대상 프로젝트 ID** (기본: 현재 활성 프로젝트)
- **생성 모드** (기본: `balanced`)
  - `fast`: 빠른 생성 (10-30초, 기본 품질)
  - `balanced`: 권장 (30초-1분, 체크리스트 적용)
  - `quality`: 최고 품질 (1-3분, 다단계 검증)
- **프로파일 키** (선택: `web_app`, `mobile_app`, `api_testing`)
- **카테고리 키** (선택: `ui`, `api`, `security`, `performance`)

**예시 대화**:
```
사용자: "로그인 기능 테스트 케이스 만들어줘"

어시스턴트: 
"네, 로그인 기능 테스트 케이스를 생성하겠습니다.
몇 가지 확인할게요:

1. 스펙 문서가 있나요? (파일 경로 또는 요구사항을 직접 알려주세요)
2. 프로젝트 타입: 웹 앱인가요, 모바일 앱인가요? (기본: 웹)
3. 생성 모드: balanced 모드로 진행할까요? (권장)

스펙 문서가 없다면 기본적인 로그인 시나리오로 생성할 수도 있습니다."
```

---

### Step 2: QuickRail 서버 상태 확인

QuickRail 서버가 실행 중인지 확인합니다:

```bash
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep python | grep run.py
```

**결과 해석**:
- ✅ `python run.py` 프로세스 있음 → Step 3으로
- ❌ 프로세스 없음 → 사용자에게 서버 시작 안내:
  ```
  "QuickRail 서버가 실행되지 않았습니다.
  새 터미널에서 다음 명령어로 서버를 시작해주세요:
  
  cd /path/to/quickrail
  python run.py
  
  서버가 시작되면 http://localhost:5000 에서 확인할 수 있습니다."
  ```

---

### Step 3: 프롬프트 시스템 확인

#### 3-1. 활성 프롬프트 확인 (DB)

```bash
venv/Scripts/python.exe -c "
import sys
sys.path.insert(0, '.')
from app import create_app, db
from app.models import CaseGenerationPrompt

app = create_app('development')
with app.app_context():
    prompt = CaseGenerationPrompt.query.filter_by(is_active=True).first()
    if prompt:
        print(f'✅ Active DB Prompt: {prompt.name} (ID: {prompt.id})')
        print(f'   Created: {prompt.created_at}')
        print(f'   Updated: {prompt.updated_at}')
    else:
        print('⚠️  No active DB prompt - using file-based prompts')
"
```

#### 3-2. 파일 기반 프롬프트 확인

```bash
# 프롬프트 파일 목록 확인
ls -lh prompt_files/case_gen/

# 필수 파일 존재 여부
test -f prompt_files/case_gen/common_core.md && echo "✅ common_core.md" || echo "❌ common_core.md 누락"
test -f prompt_files/case_gen/common_booster.md && echo "✅ common_booster.md" || echo "❌ common_booster.md 누락"
```

**파일 없으면 초기화**:
```bash
venv/Scripts/python.exe scripts/init_case_generation_prompt.py

# 초기화 후 재확인
ls -lh prompt_files/case_gen/
```

#### 3-3. 프롬프트 내용 간단 검증

```bash
# common_core.md 핵심 키워드 확인
grep -c "1 케이스 = 1 기대결과" prompt_files/case_gen/common_core.md
grep -c "Priority" prompt_files/case_gen/common_core.md

# common_booster.md 체크리스트 개수 확인
grep -c "\- \[ \]" prompt_files/case_gen/common_booster.md
```

---

### Step 4: API 키 확인 및 검증

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
        print('✅ OpenAI API Key: Configured')
        # 키 마스킹 출력
        masked = key.api_key[:8] + '...' + key.api_key[-4:]
        print(f'   Key: {masked}')
        print(f'   Model: {key.model or \"gpt-4o-mini (default)\"}')
    else:
        print('❌ ERROR: No active OpenAI API key')
        print('   조치: Settings > API Keys에서 OpenAI 키를 추가하고 활성화하세요')
        sys.exit(1)
"
```

**에러 발생 시 조치**:
```
"OpenAI API 키가 설정되지 않았습니다.
다음 단계로 설정해주세요:

1. http://localhost:5000/settings/api-keys 접속
2. 'Add API Key' 클릭
3. Service: OpenAI 선택
4. API Key 입력 (sk-...로 시작)
5. Model: gpt-4o-mini 또는 gpt-4o 선택
6. 'Active' 체크박스 활성화
7. 저장"
```

---

### Step 5: 케이스 생성 실행

#### 방법 A: Web UI 사용 (권장)

사용자에게 다음 단계를 **구체적으로** 안내:

```
1. 브라우저에서 http://localhost:5000 접속

2. 좌측 사이드바에서 프로젝트 선택
   예: "QuickRail Project"

3. 상단 탭에서 "Cases" 클릭

4. 우측 상단의 "AI Generate Cases" 버튼 클릭
   (파란색 버튼, AI 아이콘)

5. 팝업 창에서:
   ┌─────────────────────────────────────┐
   │ Specification Text                  │
   │ ┌─────────────────────────────────┐ │
   │ │ 여기에 스펙 입력 또는           │ │
   │ │ "Upload File" 버튼으로 파일     │ │
   │ └─────────────────────────────────┘ │
   │                                     │
   │ Generation Mode: [Balanced ▼]      │
   │ Profile: [None ▼] (선택)           │
   │ Category: [None ▼] (선택)          │
   │                                     │
   │ [Generate Preview]                  │
   └─────────────────────────────────────┘

6. "Generate Preview" 클릭 후 대기 (30초~1분)

7. 결과 확인:
   - 좌측: 생성된 섹션 및 케이스 트리
   - 우측: 각 케이스의 상세 내용
   - 체크박스로 선택 가능

8. 품질 검토 (Step 6 참고)

9. 커밋:
   - "Commit All": 모든 케이스 저장
   - "Commit Selected": 체크된 케이스만 저장
```

#### 방법 B: API 직접 호출

Python 스크립트로 API 호출 (자동화/스크립트용):

```python
import requests
import json
from pathlib import Path

# 1. 스펙 파일 읽기
spec_path = Path("specs/login_feature.md")
if not spec_path.exists():
    print(f"❌ 스펙 파일 없음: {spec_path}")
    exit(1)

spec_text = spec_path.read_text(encoding='utf-8')
print(f"✅ 스펙 로드: {len(spec_text)} 글자")

# 2. 세션 생성 및 로그인
session = requests.Session()
login_response = session.post(
    'http://localhost:5000/auth/login',
    data={
        'email': 'admin@quickrail.com',
        'password': 'admin123'
    }
)

if login_response.status_code != 200:
    print(f"❌ 로그인 실패: {login_response.status_code}")
    exit(1)

print("✅ 로그인 성공")

# 3. AI 케이스 생성 요청
print("📝 케이스 생성 중...")
response = session.post(
    'http://localhost:5000/api/projects/1/cases/ai-generate',
    data={
        'spec_text': spec_text,
        'generation_mode': 'balanced',  # fast | balanced | quality
        'profile_key': 'web_app',       # 선택
        'category_key': '',             # 선택
        'model': 'gpt-4o-mini'          # gpt-4o-mini | gpt-4o
    }
)

# 4. 결과 처리
if response.status_code == 200:
    result = response.json()
    
    # 통계 출력
    sections = result.get('sections', [])
    total_cases = sum(len(s.get('cases', [])) for s in sections)
    
    print(f"✅ 생성 완료:")
    print(f"   섹션: {len(sections)}개")
    print(f"   케이스: {total_cases}개")
    
    # 파일 저장
    output_path = Path('generated_cases.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"   저장 위치: {output_path}")
    
    # info_requests 확인
    info_requests = result.get('info_requests', [])
    if info_requests:
        print(f"\n⚠️  추가 정보 필요 ({len(info_requests)}건):")
        for req in info_requests:
            print(f"   - {req['topic']}: {req['question']}")
    
else:
    print(f"❌ 생성 실패: {response.status_code}")
    print(f"   에러: {response.text}")
    
    # 에러 분석
    if response.status_code == 400:
        print("\n   가능한 원인:")
        print("   - 스펙 텍스트가 너무 짧음 (최소 50자 필요)")
        print("   - 잘못된 generation_mode 값")
    elif response.status_code == 401:
        print("\n   가능한 원인:")
        print("   - 세션 만료 (로그인 재시도)")
    elif response.status_code == 500:
        print("\n   가능한 원인:")
        print("   - OpenAI API 키 오류")
        print("   - 프롬프트 파일 손상")
        print("   - 서버 로그 확인: tail -f logs/quickrail.log")
```

---

### Step 6: 생성 결과 검증 및 품질 체크

생성된 케이스를 다음 체크리스트로 검증하도록 안내:

#### ✅ 구조 검증
- [ ] 섹션이 논리적으로 그룹화되었는가?
  - 예: "로그인 > 정상 케이스", "로그인 > 에러 처리"
- [ ] 각 섹션에 최소 2개 이상의 케이스가 있는가?
- [ ] 관련 없는 케이스가 섞여있지 않은가?

#### ✅ 완성도 검증
- [ ] **Title**: 테스트 의도가 명확한가?
  - ❌ "로그인 테스트"
  - ✅ "잘못된 비밀번호로 로그인 시도 시 에러 메시지 표시"
  
- [ ] **Steps**: 구체적인 행동이 번호로 나열되었는가?
  - ❌ "로그인 시도"
  - ✅ "1) 이메일 필드에 'test@example.com' 입력\n2) 비밀번호 필드에 'wrong123' 입력\n3) [로그인] 버튼 클릭"
  
- [ ] **Expected Result**: 검증 가능한 결과인가?
  - ❌ "정상 동작"
  - ✅ "비밀번호 필드 하단에 빨간색 '비밀번호가 일치하지 않습니다' 에러 메시지 표시"

#### ✅ 우선순위 검증
- [ ] Priority가 Blocker/Critical/High/Medium/Low 중 하나인가?
- [ ] 핵심 기능은 Blocker/Critical로 설정되었는가?
- [ ] 엣지 케이스는 Medium/Low로 설정되었는가?

#### ✅ 커버리지 검증
- [ ] Happy Path (정상 흐름) 케이스가 있는가?
- [ ] Negative 케이스 (에러, 예외)가 있는가?
- [ ] 입력 검증 케이스가 충분한가? (빈 값, 형식 오류, 특수문자)
- [ ] 경계값 케이스가 있는가? (최소, 최대, 0)
- [ ] 인증/권한 케이스가 있는가? (해당 시)

#### ✅ 중복/유사 케이스 체크
```python
# 중복 검사 스크립트
import json

with open('generated_cases.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

titles = []
for section in data['sections']:
    for case in section.get('cases', []):
        title = case['title'].lower()
        if title in titles:
            print(f"⚠️  중복 케이스: {case['title']}")
        titles.append(title)
```

**검증 실패 시 조치**:
- Web UI: 체크박스 해제하여 해당 케이스만 제외
- API: `generated_cases.json` 수정 후 수동 커밋
- 재생성: 더 구체적인 스펙 제공 후 다시 생성

---

## Generation Modes 상세

### Fast Mode
**사용 시기**: 프로토타이핑, 간단한 기능, 빠른 피드백 필요  
**적용 프롬프트**: `common_core.md`만  
**예상 시간**: 10-30초  
**장점**: 빠름  
**단점**: 기본 품질, 누락 가능성 있음  

**예시 결과**:
- 섹션: 2-3개
- 케이스: 5-10개
- 커버리지: Happy Path + 기본 에러

### Balanced Mode (권장)
**사용 시기**: 일반적인 모든 케이스, 프로덕션 사용  
**적용 프롬프트**: `common_core.md` + `common_booster.md` + 선택한 프로파일/카테고리  
**예상 시간**: 30초-1분  
**장점**: 품질과 속도 균형, 체크리스트 적용  
**단점**: -  

**예시 결과**:
- 섹션: 4-6개 (중첩 가능)
- 케이스: 15-30개
- 커버리지: Happy Path + 입력검증 + 경계값 + 에러처리

### Quality Mode
**사용 시기**: 중요한 기능, 복잡한 시나리오, 최고 품질 필요  
**적용 프롬프트**: 모든 프롬프트 + 다단계 검증  
**예상 시간**: 1-3분  
**장점**: 최고 품질, 포괄적 커버리지, 다단계 검증  
**단점**: 느림  

**예시 결과**:
- 섹션: 6-10개 (중첩 구조)
- 케이스: 30-50개
- 커버리지: 모든 체크리스트 항목 + 엣지케이스 + 통합 테스트

**Quality 모드 파이프라인**:
```
1. spec_digest.md   → 스펙 분석 및 핵심 추출
2. common_core.md   → 기본 규칙 적용
3. common_booster.md → 체크리스트 적용
4. profile_*.md     → 도메인 특화 (선택)
5. category_*.md    → 카테고리 특화 (선택)
6. [AI 초안 생성]
7. rewrite.md       → 품질 개선 (Steps 구체화, Expected 명확화)
8. validate.md      → 최종 검증 (중복 제거, 우선순위 재조정)
9. [최종 출력]
```

---

## Best Practices

### 1. 스펙 문서 품질이 결과를 좌우합니다

**좋은 스펙 예시**:
```markdown
## 기능: 사용자 로그인

### 목적
등록된 사용자가 이메일과 비밀번호로 인증하여 시스템에 접근

### 입력 필드
- 이메일 (필수)
  - 형식: RFC 5322 표준
  - 예시: user@example.com
  - 최대 길이: 255자
  
- 비밀번호 (필수)
  - 최소 8자, 최대 128자
  - 영문 대소문자, 숫자, 특수문자 조합
  - 마스킹 처리됨

### 성공 시나리오
1. 올바른 이메일/비밀번호 입력
2. 서버 인증 성공
3. 세션 생성 (유효기간 30분)
4. 대시보드 페이지로 리다이렉트

### 실패 시나리오
- 잘못된 비밀번호 → "비밀번호가 일치하지 않습니다" 에러
- 존재하지 않는 이메일 → "등록되지 않은 이메일입니다" 에러
- 5회 연속 실패 → 계정 잠금 (15분)
- 빈 필드 제출 → 해당 필드에 "필수 입력입니다" 에러

### 제약사항
- 동시 로그인: 최대 3개 디바이스
- Rate Limiting: IP당 분당 10회
- 2FA 활성화 시: OTP 추가 입력 필요
```

**나쁜 스펙 예시**:
```markdown
로그인 기능 만들기
- 이메일이랑 비밀번호 입력받음
- 맞으면 로그인됨
- 틀리면 에러 보여줌
```

### 2. 적절한 모드 선택

| 상황 | 권장 모드 | 이유 |
|------|----------|------|
| 스펙 초안 단계, 빠른 검토 필요 | Fast | 빠른 피드백 |
| 일반 기능 개발 | Balanced | 품질과 속도 균형 |
| 핵심 기능, 결제, 보안 | Quality | 최고 품질 필요 |
| 레거시 코드 리팩토링 | Quality | 포괄적 커버리지 |

### 3. 프로파일/카테고리 활용

**프로파일 선택 기준**:
- 웹 앱 → `web_app`: 브라우저 이슈, CORS, SEO
- 모바일 앱 → `mobile_app`: 화면 회전, 백그라운드, 오프라인
- REST API → `api_testing`: HTTP 메서드, 상태코드, 인증

**카테고리 선택 기준**:
- 로그인, 결제, 개인정보 → `security`: XSS, CSRF, SQL Injection
- 대시보드, 목록 → `performance`: 로딩 시간, 대용량 데이터
- 폼, 입력 → `ui`: 접근성, 반응형, 브라우저 호환성

**조합 예시**:
```
웹 쇼핑몰 결제 기능:
- Profile: web_app
- Category: security
→ SSL, PCI DSS, XSS 방어 케이스 자동 추가
```

### 4. 생성 후 검증은 필수

**AI는 도구일 뿐**입니다. 반드시 검토하세요:
- [ ] 비즈니스 로직이 정확한가?
- [ ] 중복 케이스는 없는가?
- [ ] Priority가 적절한가?
- [ ] 실제로 실행 가능한가?

**검증 실패 사례**:
```
생성된 케이스: "관리자가 사용자 삭제 시 확인 팝업 표시"
문제: 실제 스펙에는 "삭제" 기능 없음
→ AI가 일반적인 CRUD 패턴으로 추측
```

### 5. 반복적 개선

**첫 생성 → 검토 → 프롬프트 튜닝 → 재생성** 사이클:

```
1차 생성:
- 입력 검증 케이스 부족
→ common_booster.md 수정: "입력 검증 최소 5개" 명시

2차 생성:
- Steps가 너무 추상적 ("로그인 시도")
→ common_core.md 수정: "나쁜 예시" 섹션에 추가

3차 생성:
- ✅ 품질 만족
→ 프롬프트 버전 관리 (git commit)
```

---

## Troubleshooting

### 문제 1: 프롬프트 파일 없음

**증상**:
```
FileNotFoundError: prompt_files/case_gen/common_core.md
```

**해결**:
```bash
# 프롬프트 초기화 스크립트 실행
venv/Scripts/python.exe scripts/init_case_generation_prompt.py

# 결과 확인
ls -la prompt_files/case_gen/
```

### 문제 2: OpenAI API 키 오류

**증상**:
```
OpenAI API Error: Incorrect API key provided
```

**해결**:
1. API 키 확인: http://localhost:5000/settings/api-keys
2. OpenAI 대시보드에서 키 유효성 확인
3. 키 재생성 및 교체
4. 서버 재시작

### 문제 3: 생성된 케이스가 너무 적음

**증상**:
- Balanced 모드인데 케이스 5개만 생성됨

**원인**:
- 스펙이 너무 짧거나 모호함
- common_booster.md가 적용 안 됨

**해결**:
```bash
# 1. 모드별 프롬프트 로딩 확인
grep -r "generation_mode" app/routes/api.py

# 2. 스펙 보강 (최소 200자 이상 권장)
# 3. Quality 모드로 재시도
```

### 문제 4: 생성 중 타임아웃

**증상**:
```
504 Gateway Timeout
```

**원인**:
- 스펙이 너무 김 (5000자 초과)
- Quality 모드에서 복잡한 스펙

**해결**:
```python
# 스펙을 섹션별로 분할하여 생성
sections = ["로그인", "회원가입", "비밀번호 찾기"]

for section in sections:
    spec = extract_section(section)  # 섹션별 추출
    generate_cases(spec, mode='balanced')
    
# 최종 병합
```

### 문제 5: DB 마이그레이션 에러

**증상**:
```
sqlalchemy.exc.OperationalError: no such table: case_generation_prompt
```

**해결**:
```bash
# DB 마이그레이션 적용
cd /path/to/quickrail
venv/Scripts/flask.exe db upgrade

# 마이그레이션 히스토리 확인
venv/Scripts/flask.exe db history

# 최신 상태 확인
venv/Scripts/flask.exe db current
```

### 문제 6: 한글 인코딩 깨짐

**증상**:
- 생성된 케이스에 ��� 같은 문자

**해결**:
```python
# 스펙 파일 읽을 때 UTF-8 명시
spec_text = Path("spec.md").read_text(encoding='utf-8')

# API 호출 시 헤더 추가
response = session.post(
    url,
    data={'spec_text': spec_text},
    headers={'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
)
```

---

## Related Files

### 코드
- `app/routes/api.py:5809` - `ai_generate_cases()` 함수 (메인 로직)
- `app/models.py` - `CaseGenerationPrompt` 모델
- `app/utils/prompt_files.py` - 프롬프트 파일 로딩 유틸
- `app/services/openai_service.py` - OpenAI API 호출 (추정)

### 스크립트
- `scripts/init_case_generation_prompt.py` - 프롬프트 초기화

### 프롬프트
- `prompt_files/case_gen/common_core.md` - 절대 규칙
- `prompt_files/case_gen/common_booster.md` - 품질 강화
- `prompt_files/case_gen/profile_*.md` - 도메인 특화 (선택)
- `prompt_files/case_gen/category_*.md` - 카테고리 특화 (선택)

### 설정
- `config.py` - QuickRail 설정
- `.env` - 환경 변수 (API 키 등)

---

## Advanced Tips

### 1. 커스텀 프롬프트 작성

새 프로파일 추가 예시:

```bash
# prompt_files/case_gen/profile_iot.md 생성
cat > prompt_files/case_gen/profile_iot.md << 'EOF'
# IoT 디바이스 테스트 특화 프롬프트

## 추가 체크리스트

### 하드웨어 연동
- [ ] 센서 데이터 수신 실패 시나리오
- [ ] 펌웨어 업데이트 중단
- [ ] 배터리 부족 상황

### 네트워크
- [ ] WiFi 연결 끊김
- [ ] MQTT 브로커 다운
- [ ] 저대역폭 환경

### 물리적 상황
- [ ] 온도 범위 (-10°C ~ 50°C)
- [ ] 습도 영향
- [ ] 진동/충격
EOF
```

### 2. 배치 생성 스크립트

```bash
#!/bin/bash
# batch_generate.sh

SPECS_DIR="specs/"
OUTPUT_DIR="generated_cases/"

for spec_file in $SPECS_DIR/*.md; do
    echo "Processing: $spec_file"
    
    python - <<EOF
import requests
from pathlib import Path

spec_text = Path("$spec_file").read_text(encoding='utf-8')
session = requests.Session()
session.post('http://localhost:5000/auth/login', 
             data={'email': 'admin@quickrail.com', 'password': 'admin123'})

response = session.post(
    'http://localhost:5000/api/projects/1/cases/ai-generate',
    data={'spec_text': spec_text, 'generation_mode': 'balanced'}
)

output_file = Path("$OUTPUT_DIR") / Path("$spec_file").with_suffix('.json').name
output_file.write_text(response.text, encoding='utf-8')
EOF
done
```

### 3. 품질 메트릭 추적

```python
# analyze_quality.py
import json
from pathlib import Path

def analyze_cases(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_cases = 0
    priorities = {'Blocker': 0, 'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
    avg_steps = []
    
    for section in data['sections']:
        for case in section.get('cases', []):
            total_cases += 1
            priorities[case['priority']] += 1
            steps_count = len(case['steps'].split('\n'))
            avg_steps.append(steps_count)
    
    print(f"Total Cases: {total_cases}")
    print(f"Priorities: {priorities}")
    print(f"Avg Steps: {sum(avg_steps)/len(avg_steps):.1f}")
    print(f"Info Requests: {len(data.get('info_requests', []))}")

analyze_cases('generated_cases.json')
```

---

## Changelog

### 2025-01-22
- SKILL.md 대폭 개선
- 프롬프트 파일 아키텍처 섹션 추가
- Troubleshooting 섹션 확장
- 실전 예시 코드 보강

### 2025-01-15
- Generation Modes 상세 설명 추가
- Best Practices 섹션 신규 작성

### 2025-01-10
- 초기 버전 작성
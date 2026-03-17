---
name: commit-with-message
description: 커밋 메시지 작성 가이드 (한글/영어). 커밋 생성 시 자동으로 활성화되어 규칙을 준수하도록 안내합니다.
allowed-tools: Read, Bash(git:*)
user-invocable: true
---

# 커밋 메시지 작성 스킬

본 스킬은 datamaker-kr organization의 Platform Dev Team에서 사용하는 커밋 메시지 작성 규칙을 안내합니다.

## 활성화 시점

- 사용자가 커밋 생성을 요청할 때
- git commit 명령어를 실행하기 전
- 변경사항을 커밋하려고 할 때

## 언어 선택

커밋 메시지는 **한글** 또는 **영어**로 작성할 수 있습니다.

### 기본 언어: 한글

- 특별한 요청이 없으면 **한글**로 커밋 메시지를 작성합니다
- datamaker-kr organization의 기본 정책입니다

### 영어 사용

다음 경우에는 영어로 작성할 수 있습니다:
- 사용자가 명시적으로 영어 커밋을 요청하는 경우
- 오픈소스 기여를 위한 커밋인 경우
- 국제 협업이 필요한 경우

**사용자에게 언어 확인**: 커밋 메시지 작성 전, 사용자가 원하는 언어가 무엇인지 확인합니다.
- "커밋 메시지를 한글로 작성할까요, 영어로 작성할까요? (기본: 한글)"

## 기본 원칙 (한글)

### 1. 한글로 작성한다

- 모든 커밋 메시지는 **한글로 작성**합니다
- 기술 용어는 필요 시 영문 그대로 사용 가능합니다
  - 예: TDD, API, ViewSet, Serializer, Celery, Redis 등

### 2. 변경사항에 대해 간결하고 명확하게 작성한다

- 무엇을 변경했는지 **한 줄로 요약**합니다
- 불필요한 설명은 생략합니다
- **명령형**으로 작성합니다
  - ✅ 좋은 예: "추가", "수정", "삭제"
  - ❌ 나쁜 예: "추가한다", "추가했습니다", "추가함"

## 커밋 메시지 형식

```
<타입>: <간결한 설명>

[선택] 상세 설명 (필요한 경우)

[선택] Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## 타입 분류

커밋 메시지는 다음 타입 중 하나로 시작해야 합니다:

- **기능**: 새로운 기능 추가
- **수정**: 버그 수정
- **문서**: 문서 변경 (README, 주석 등)
- **스타일**: 코드 포맷팅, 세미콜론 누락 등 (동작 변경 없음)
- **리팩토링**: 코드 리팩토링 (기능 변경 없음)
- **테스트**: 테스트 코드 추가 또는 수정
- **빌드**: 빌드 시스템 또는 외부 종속성 변경

## 커밋 메시지 작성 규칙

### 제목 규칙

1. **72자 이하**로 작성
2. **마침표(.)를 사용하지 않음**
3. **명령형**으로 작성
4. **티켓 ID**가 있는 경우 제목 앞에 포함
   - 형식: `[티켓ID] 타입: 설명`
   - 예: `[SYN-1234] 기능: 사용자 인증 추가`

### 본문 규칙

1. 제목과 본문 사이 **빈 줄** 삽입
2. **어떻게**보다 **무엇을**, **왜** 변경했는지 설명
3. 여러 항목은 **불릿 포인트(-)** 사용
4. **Breaking Changes**가 있는 경우 반드시 명시

### Co-Authored-By

Claude와 협업한 커밋에는 다음을 추가합니다:

```
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## 커밋 메시지 예시

### 좋은 커밋 메시지

**예시 1: 새로운 기능 추가**
```
기능: TDD 스킬 추가

Kent Beck의 TDD 방법론과 Tidy First 원칙을 따르는 스킬 구현
- Red → Green → Refactor 사이클 가이드 포함
- 커밋 규칙 자동 검증 기능 추가

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**예시 2: 버그 수정**
```
수정: PR 제목 생성 시 티켓 ID 보존 오류 수정

정규 표현식 패턴을 수정하여 SYN-XXXX 형식의 티켓 ID가
PR 제목 업데이트 시 유지되도록 개선
```

**예시 3: 문서 업데이트**
```
문서: CalVer 버전 관리 가이드 추가

YYYY.Minor.Patch 형식의 CalVer 버전 관리 체계 설명 추가
- 버전 증가 규칙 문서화
- 예시 및 확인 방법 포함
```

**예시 4: 티켓 ID 포함**
```
[SYN-1234] 기능: 사용자 JWT 인증 시스템 구현

JWT 기반 인증 시스템 추가
- Access Token/Refresh Token 발급 API 구현
- TokenAuthentication 미들웨어 추가
- 토큰 갱신 엔드포인트 구현
```

**예시 5: Breaking Changes**
```
기능: API 응답 형식 변경

API 응답을 표준화된 형식으로 변경

BREAKING CHANGE: 모든 API 응답이 다음 형식을 따름
{
  "success": boolean,
  "data": object,
  "error": object | null
}

기존 클라이언트는 응답 파싱 로직 수정 필요
```

### 나쁜 커밋 메시지

**예시 1: 영어 사용**
```
❌ feat: Add TDD skill
```
올바른 형식:
```
✅ 기능: TDD 스킬 추가
```

**예시 2: 불명확한 설명**
```
❌ 여러 가지 수정함
```
올바른 형식:
```
✅ 수정: PR 제목 생성 로직 개선

- 티켓 ID 보존 오류 수정
- 제목 길이 72자 제한 적용
- 특수문자 처리 개선
```

**예시 3: 너무 장황함 (커밋 분리 필요)**
```
❌ TDD skill을 추가하고, docs-manager도 같이 만들고, README도 업데이트하고...
```
올바른 형식 (3개의 커밋으로 분리):
```
✅ 커밋 1: 기능: TDD 스킬 추가
✅ 커밋 2: 기능: docs-manager 스킬 추가
✅ 커밋 3: 문서: README 스킬 섹션 업데이트
```

**예시 4: 과거형 사용**
```
❌ 기능: TDD 스킬을 추가했습니다
```
올바른 형식:
```
✅ 기능: TDD 스킬 추가
```

## 영어 커밋 메시지 규칙

사용자가 영어로 커밋 메시지를 작성하려는 경우, 다음 규칙을 따릅니다.

### 기본 원칙 (영어)

1. **Imperative mood (명령형)으로 작성**
   - ✅ 좋은 예: "Add", "Fix", "Update"
   - ❌ 나쁜 예: "Added", "Adds", "Adding"

2. **간결하고 명확하게 작성**
   - 무엇을 변경했는지 한 줄로 요약
   - 불필요한 설명은 생략

### 커밋 메시지 형식 (영어)

```
<type>: <brief description>

[optional] Detailed explanation

[optional] Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### 타입 분류 (영어)

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code formatting (no behavior change)
- **refactor**: Code refactoring (no feature change)
- **test**: Test code addition or modification
- **build**: Build system or dependency changes

### 영어 커밋 메시지 예시

**예시 1: 새로운 기능 추가**
```
feat: Add TDD skill

Implement skill following Kent Beck's TDD and Tidy First principles
- Include Red → Green → Refactor cycle guide
- Add commit rule auto-verification

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**예시 2: 버그 수정**
```
fix: Preserve ticket ID when generating PR title

Update regex pattern to maintain SYN-XXXX format ticket IDs
during PR title updates
```

**예시 3: 문서 업데이트**
```
docs: Add CalVer versioning guide

Document CalVer versioning scheme with YYYY.Minor.Patch format
- Include version increment rules
- Add examples and verification methods
```

**예시 4: Breaking Changes**
```
feat: Change API response format

Standardize API responses to consistent format

BREAKING CHANGE: All API responses now follow this format
{
  "success": boolean,
  "data": object,
  "error": object | null
}

Existing clients need to update response parsing logic
```

### 제목 규칙 (영어)

1. **72 characters or less**
2. **No period at the end**
3. **Imperative mood**
4. **Include ticket ID if available**
   - Format: `[TICKET-ID] type: description`
   - Example: `[SYN-1234] feat: Add user JWT authentication`

## 커밋 작성 워크플로우

본 스킬이 활성화되면 다음 단계를 따릅니다:

### 1. 언어 확인

**중요**: 커밋 메시지 작성 전 사용자에게 언어를 확인합니다.

```
커밋 메시지를 한글로 작성할까요, 영어로 작성할까요? (기본: 한글)
```

사용자 응답에 따라:
- **한글 선택**: 한글 커밋 메시지 규칙 적용
- **영어 선택**: 영어 커밋 메시지 규칙 적용
- **응답 없음**: 기본값(한글) 사용

### 2. 변경사항 분석

```bash
# git status와 git diff로 변경사항 확인
git status
git diff
```

### 3. 커밋 타입 결정

변경사항의 성격에 따라 적절한 타입 선택:

**한글**:
- 새로운 기능? → **기능**
- 버그 수정? → **수정**
- 문서만? → **문서**
- 코드 정리? → **리팩토링**
- 테스트? → **테스트**

**영어**:
- New feature? → **feat**
- Bug fix? → **fix**
- Documentation? → **docs**
- Code cleanup? → **refactor**
- Test? → **test**

### 4. 제목 작성

**한글**:
```
<타입>: <무엇을 변경했는지 간결하게>
```

**영어**:
```
<type>: <brief description of what changed>
```

공통 규칙:
- 72자 이하
- 명령형
- 티켓 ID 있으면 앞에 포함

### 5. 본문 작성 (선택)

복잡한 변경사항인 경우:
- 왜 변경했는지
- 무엇이 바뀌었는지
- Breaking Changes 있는지

### 5. Co-Authored-By 추가 (Claude와 협업 시)

```
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### 6. 커밋 생성

```bash
git commit -m "$(cat <<'EOF'
<커밋 메시지>
EOF
)"
```

## 주의사항

### 하나의 커밋은 하나의 논리적 변경

- 여러 기능을 한 커밋에 포함하지 않습니다
- 관련 없는 변경사항은 별도 커밋으로 분리합니다
- 각 커밋은 독립적으로 이해 가능해야 합니다

### 티켓 ID 형식

datamaker-kr organization에서 사용하는 티켓 ID 형식:
- `SYN-XXXX`: Synapse 프로젝트 관련
- `#XXXX`: GitHub Issue 번호

### Breaking Changes 명시

API 변경, 데이터베이스 스키마 변경 등 하위 호환성이 깨지는 경우:
- 커밋 메시지 본문에 **BREAKING CHANGE:** 명시
- 무엇이 바뀌었고 마이그레이션 방법 설명

## 스킬 동작

본 스킬은 다음과 같이 동작합니다:

1. **커밋 요청 감지**: 사용자가 커밋 생성을 요청하면 활성화
2. **변경사항 분석**: git status와 git diff로 변경사항 확인
3. **커밋 메시지 초안 작성**: 위 규칙을 따라 초안 생성
4. **사용자 검토**: 작성된 커밋 메시지를 사용자에게 제시
5. **커밋 생성**: 승인 후 git commit 실행
6. **규칙 위반 방지**: 영어 메시지, 과도하게 긴 제목 등 자동 수정

## 참고 사항

- 본 규칙은 [CLAUDE.md](../../CLAUDE.md)에도 문서화되어 있습니다
- TDD Skill과 함께 사용하면 테스트 통과 후 자동으로 커밋 메시지를 제안합니다
- 모든 커밋은 의미 있는 단위로 분리되어야 합니다

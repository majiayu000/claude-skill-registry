---
name: skill-creator
description: "**SKILL CREATOR v2.0** - '스킬 만들어', 'skill 만들어', '새 스킬', 'create skill' 요청 시 자동 발동. Anthropic 공식 베스트 프랙티스 기반 프로덕션급 스킬 생성. Progressive Disclosure, 토큰 최적화, 평가 기반 개발 지원."
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
---

# Skill Creator v2.0 - Production-Ready Skill Builder

> **Based on**: [Anthropic Official Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

---

## Quick Start - 5분 안에 스킬 만들기

### Step 1: 스킬 폴더 생성

```bash
SKILL_NAME="my-new-skill"
mkdir -p ~/.claude/skills/$SKILL_NAME
```

### Step 2: SKILL.md 작성

```markdown
---
name: my-new-skill
description: "Does X when user asks for Y. Triggers on 'keyword1', 'keyword2'."
allowed-tools:
  - Read
  - Write
---

# My New Skill

## Quick start
[핵심 사용법]

## Detailed guide
See [reference.md](reference.md) for complete documentation.
```

### Step 3: 검증 & 동기화

```bash
# 검증
python ~/.claude/skills/skill-creator/scripts/validate_skill.py ~/.claude/skills/$SKILL_NAME

# WSL 동기화 (Windows 환경)
bash ~/.claude/skills/skill-creator/scripts/sync_skills.sh $SKILL_NAME
```

---

## Core Principles (핵심 원칙)

### 1. Progressive Disclosure (점진적 공개)

**스킬은 매뉴얼처럼 작동합니다** - 목차 → 장 → 상세 부록 순서로 필요할 때만 로드

```
Level 1: name + description (시작 시 시스템 프롬프트에 로드, ~100 토큰)
Level 2: SKILL.md 전체 (관련성 판단 시 로드, <5k 토큰)
Level 3: 참조 파일들 (필요 시에만 개별 로드)
```

**실전 적용:**
- SKILL.md는 500줄 이하 유지
- 상세 내용은 `reference/`, `examples/`로 분리
- 한 단계만 깊게 참조 (SKILL.md → file.md ✓, file.md → nested.md ✗)

### 2. Concise is Key (간결함이 핵심)

**기본 가정**: Claude는 이미 매우 똑똑합니다

```markdown
# ✅ Good (50 tokens)
## PDF 텍스트 추출
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()

# ❌ Bad (150 tokens)
## PDF 텍스트 추출
PDF(Portable Document Format)는 텍스트, 이미지 등을 포함하는 파일 형식입니다.
PDF에서 텍스트를 추출하려면 라이브러리가 필요합니다...
```

**자문하기:**
- "Claude가 정말 이 설명이 필요한가?"
- "이 단락이 토큰 비용을 정당화하는가?"

### 3. Degrees of Freedom (자유도 설정)

| 자유도 | 사용 시점 | 예시 |
|--------|----------|------|
| **High** | 여러 접근법 유효, 컨텍스트 의존 | 코드 리뷰, 분석 |
| **Medium** | 선호 패턴 있지만 변형 허용 | 템플릿 + 파라미터 |
| **Low** | 순서 중요, 실패 시 치명적 | DB 마이그레이션, API 키 |

---

## YAML Frontmatter 규칙

### 필수 필드만 사용

```yaml
---
name: skill-name           # 64자 이하, 소문자+숫자+하이픈만
description: "..."         # 1024자 이하, 비어있으면 안 됨
allowed-tools:             # (선택) 사용할 도구 제한
  - Read
  - Write
---
```

### Name 규칙 - Gerund Form 권장

```yaml
# ✅ 권장 (동명사형)
name: processing-pdfs
name: analyzing-data
name: testing-code

# ✓ 허용
name: pdf-processing
name: data-analyzer

# ❌ 피하기
name: helper           # 너무 모호
name: utils            # 너무 일반적
name: claude-tools     # 예약어 포함
```

### Description 규칙 - 3인칭 필수

```yaml
# ✅ 올바름 (3인칭)
description: "Processes Excel files and generates reports. Use when working with .xlsx files."

# ❌ 피하기 (1인칭/2인칭)
description: "I can help you process Excel files"
description: "You can use this to process Excel"
```

**필수 포함 요소:**
1. **무엇을 하는지** (What)
2. **언제 사용하는지** (When)
3. **트리거 키워드** (Keywords)

```yaml
# 예시
description: "Extracts text and tables from PDF files, fills forms. Use when working with PDFs or document extraction."
```

### YAML 콜론 금지

```yaml
# ❌ 파싱 오류!
description: "**SKILL v1.0**: 설명..."

# ✅ 하이픈으로 대체
description: "**SKILL v1.0** - 설명..."
```

---

## 디렉토리 구조 패턴

### Pattern 1: Simple Skill (단순)

```
my-skill/
└── SKILL.md
```

### Pattern 2: With References (참조 포함)

```
my-skill/
├── SKILL.md              # 개요 + 빠른 시작
├── reference.md          # 상세 API/가이드
└── examples.md           # 사용 예제
```

### Pattern 3: Domain-Specific (도메인별)

```
bigquery-skill/
├── SKILL.md
└── reference/
    ├── finance.md        # 재무 메트릭
    ├── sales.md          # 영업 파이프라인
    └── product.md        # 제품 분석
```

### Pattern 4: With Scripts (스크립트 포함)

```
pdf-skill/
├── SKILL.md
├── FORMS.md
├── reference.md
└── scripts/
    ├── analyze_form.py   # 실행용 (컨텍스트 미소비)
    ├── fill_form.py
    └── validate.py
```

---

## 워크플로우 & 피드백 루프

### 체크리스트 패턴

```markdown
## 작업 진행 상황

이 체크리스트를 복사하여 진행 추적:

Progress:
- [ ] Step 1: 소스 파일 읽기
- [ ] Step 2: 검증 실행
- [ ] Step 3: 변환 적용
- [ ] Step 4: 결과 확인
```

### 피드백 루프 패턴

```markdown
## 문서 편집 프로세스

1. document.xml 수정
2. **즉시 검증**: python scripts/validate.py
3. 검증 실패 시:
   - 오류 메시지 확인
   - 문제 수정
   - 다시 검증
4. **검증 통과 시에만 진행**
5. 빌드: python scripts/build.py
```

---

## 예제 패턴 (Input/Output)

```markdown
## 커밋 메시지 형식

다음 예제를 따라 작성:

**Example 1:**
Input: 사용자 인증에 JWT 토큰 추가
Output: feat(auth): JWT 기반 인증 구현 - 로그인 엔드포인트와 토큰 검증 미들웨어 추가

**Example 2:**
Input: 리포트에서 날짜가 잘못 표시되는 버그 수정
Output: fix(reports): 타임존 변환 시 날짜 포맷 수정 - UTC 타임스탬프를 일관되게 사용
```

---

## 안티패턴 (피해야 할 것)

| 안티패턴 | 문제 | 해결 |
|----------|------|------|
| Windows 경로 | Unix에서 오류 | scripts\file.py → scripts/file.py |
| 너무 많은 옵션 | 혼란 | 기본값 제시 + 대안 1개 |
| 깊은 참조 체인 | 불완전 로드 | 1단계만 참조 |
| 시간 의존 정보 | 구식화 | "Old patterns" 섹션 사용 |
| 모호한 이름 | 발견 어려움 | 구체적 키워드 포함 |

---

## 평가 기반 개발 (권장)

### 1. 갭 파악
스킬 없이 Claude 실행 → 어디서 실패하는지 관찰

### 2. 평가 생성
```json
{
  "skills": ["my-skill"],
  "query": "PDF에서 텍스트 추출해서 output.txt에 저장",
  "expected_behavior": [
    "PDF 라이브러리로 파일 읽기",
    "모든 페이지에서 텍스트 추출",
    "output.txt에 저장"
  ]
}
```

### 3. 최소 지침 작성
갭을 해결할 만큼만 작성

### 4. 반복
평가 실행 → 결과 비교 → 개선

---

## Claude와 함께 스킬 개발

### 권장 워크플로우

1. **Claude A와 작업** - 스킬 없이 문제 해결
2. **패턴 식별** - 반복 제공한 컨텍스트 파악
3. **Claude에게 스킬 생성 요청**
   > "방금 사용한 BigQuery 분석 패턴으로 스킬 만들어줘"
4. **간결성 검토** - 불필요한 설명 제거 요청
5. **Claude B로 테스트** - 새 인스턴스에서 스킬 사용
6. **관찰 → 개선** 반복

---

## 스킬 유효성 체크리스트

### 핵심 품질
- [ ] description이 구체적이고 키워드 포함
- [ ] description이 "무엇을" + "언제" 모두 포함
- [ ] SKILL.md 500줄 이하
- [ ] 상세 내용은 별도 파일로 분리
- [ ] 시간 의존 정보 없음
- [ ] 일관된 용어 사용
- [ ] 파일 참조는 1단계만
- [ ] 3인칭으로 작성

### 코드 & 스크립트
- [ ] 스크립트가 에러를 직접 처리 (Claude에 위임 X)
- [ ] 매직 넘버 없음 (모든 값에 이유 설명)
- [ ] 필요 패키지 목록화
- [ ] Windows 경로 없음 (모두 / 사용)
- [ ] 검증/확인 단계 포함

### 테스트
- [ ] 최소 3개 평가 시나리오 생성
- [ ] Haiku, Sonnet, Opus에서 테스트
- [ ] 실제 사용 시나리오로 테스트

---

## 참조 문서

| 파일 | 설명 |
|------|------|
| [references/description-patterns.md](references/description-patterns.md) | Description 작성 패턴 & 예제 |
| [references/structure-patterns.md](references/structure-patterns.md) | 구조화 패턴 상세 |
| [references/scripts-guide.md](references/scripts-guide.md) | 스크립트 작성 가이드 |
| [references/anti-patterns.md](references/anti-patterns.md) | 피해야 할 패턴 상세 |
| [templates/simple-skill.md](templates/simple-skill.md) | 단순 스킬 템플릿 |
| [templates/code-skill.md](templates/code-skill.md) | 코드 포함 스킬 템플릿 |

---

## 환경별 경로 (Windows/WSL)

| 환경 | Skills 경로 |
|------|-------------|
| Git Bash | ~/.claude/skills/ = /c/Users/lpian/.claude/skills/ |
| WSL Ubuntu | ~/.claude/skills/ = /home/elon/.claude/skills/ |
| WSL에서 Windows | /mnt/c/Users/lpian/.claude/skills/ |

**동기화 필수**: 두 환경의 ~/.claude/skills/는 서로 다른 디렉토리!

```bash
# Windows → WSL 동기화
bash ~/.claude/skills/skill-creator/scripts/sync_skills.sh [skill-name]
```

---

**Version**: 2.0.0 | **Updated**: 2025-12-11
**Sources**: Anthropic Docs, Engineering Blog

---
name: skill-creator
description: Guide for creating new Claude skills. Use this when creating a new skill, updating existing skills, or learning best practices for skill development.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
license: MIT
metadata:
  author: anthropics
  version: "1.0"
---

# Skill Creator

새로운 Claude 스킬을 생성하는 가이드입니다.

## What is a Skill?

스킬은 Claude의 능력을 확장하는 모듈식 패키지입니다:
- **전문 워크플로우**: 특정 도메인의 다단계 절차
- **도구 통합**: 파일 형식, API 연동 지침
- **도메인 전문성**: 비즈니스 로직, 스키마
- **번들 리소스**: 스크립트, 레퍼런스, 에셋

## Skill Structure

```
skill-name/
├── SKILL.md (필수)
│   ├── YAML frontmatter (필수)
│   │   ├── name: (필수)
│   │   └── description: (필수)
│   └── Markdown body (필수)
└── Bundled Resources (선택)
    ├── scripts/      # 실행 코드
    ├── references/   # 참조 문서
    └── assets/       # 출력용 파일
```

## Core Principles

### 1. Concise is Key

> "컨텍스트 윈도우는 공공재다"

- Claude는 이미 매우 똑똑함
- 필요한 정보만 추가
- 장황한 설명보다 간결한 예시

### 2. Degrees of Freedom

| 자유도 | 사용 시점 | 형태 |
|--------|----------|------|
| 높음 | 여러 접근법 가능 | 텍스트 지침 |
| 중간 | 선호 패턴 존재 | 의사코드/파라미터 |
| 낮음 | 민감한 작업 | 구체적 스크립트 |

### 3. Progressive Disclosure

```
Level 1: Metadata (~100 words)     → 항상 컨텍스트에
Level 2: SKILL.md body (<5k words) → 트리거 시 로드
Level 3: Resources (무제한)         → 필요 시 로드
```

## Creation Process

### Step 1: 구체적 예시 이해

```
Q: 어떤 기능을 지원해야 하나요?
Q: 사용 예시를 보여주세요
Q: 어떤 요청이 이 스킬을 트리거해야 하나요?
```

### Step 2: 재사용 콘텐츠 계획

각 예시 분석:
1. 처음부터 어떻게 실행?
2. 반복 작업에 필요한 리소스?

```
예시: "PDF 회전해줘"
→ 매번 같은 코드 작성 필요
→ scripts/rotate_pdf.py 추가
```

### Step 3: 스킬 초기화

```bash
# 템플릿 생성
scripts/init_skill.py <skill-name> --path <output>
```

### Step 4: 스킬 편집

**Frontmatter 작성:**

```yaml
---
name: my-skill
description: |
  무엇을 하는가 + 언제 사용하는가.
  예: "PDF 문서 처리. PDF 텍스트 추출,
  병합, 페이지 조작이 필요할 때 사용"
---
```

**Body 작성 (명령형):**

```markdown
# My Skill

## Quick Start
[핵심 사용법]

## Workflow
[단계별 절차]

## Examples
[구체적 예시]

## References
- [REFERENCE.md](references/REFERENCE.md) for details
```

### Step 5: 패키징

```bash
scripts/package_skill.py <path/to/skill>
```

### Step 6: 반복

실제 사용 → 문제 발견 → 개선

## Bundled Resources

### scripts/

```python
# scripts/process.py
# 반복적으로 작성되는 코드 저장
# 실행 전 테스트 필수
```

### references/

```markdown
# references/schema.md
# 컨텍스트에 필요할 때만 로드
# SKILL.md에서 참조 명시
```

### assets/

```
assets/template.html    # 출력용 템플릿
assets/logo.png         # 브랜드 에셋
assets/boilerplate/     # 시작 코드
```

## What NOT to Include

❌ 포함하지 말 것:
- README.md
- INSTALLATION_GUIDE.md
- CHANGELOG.md
- 테스트/설정 문서

스킬은 AI 에이전트용 - 사용자 문서 X

## Description Best Practices

```yaml
# ❌ 부족함
description: PDF 처리 도구

# ✅ 좋음
description: |
  PDF 텍스트 추출, 페이지 병합/분할, 메타데이터 편집.
  PDF 문서 작업 시 사용:
  (1) 텍스트 추출 (2) 페이지 조작
  (3) 여러 PDF 병합 (4) 양식 처리
```

## Progressive Disclosure Patterns

### Pattern 1: 개요 + 참조

```markdown
# PDF Processing

## Quick Start
[기본 사용법]

## Advanced
- **Forms**: See [FORMS.md](references/FORMS.md)
- **API**: See [API.md](references/API.md)
```

### Pattern 2: 도메인별 구성

```
bigquery-skill/
├── SKILL.md
└── references/
    ├── finance.md
    ├── sales.md
    └── product.md
```

## Validation Checklist

- [ ] name과 description 필수 포함
- [ ] description에 "언제 사용" 명시
- [ ] SKILL.md 500줄 이하
- [ ] 참조 파일 깊이 1단계
- [ ] 불필요한 파일 없음

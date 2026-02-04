---
name: rule-structurizer
description: >
  긴 문서를 Progressive Disclosure 원칙에 따라 rules 구조로 변환합니다.
  PRD, 기술 문서, 가이드 등 모든 긴 문서를 LLM이 효율적으로 참조할 수 있는
  3단계 구조(AGENTS.md → RULE.md → references/)로 분할.
  문서 구조화, 문서 분할, 긴 문서 정리 요청 시 사용.
argument-hint: "[document-path] [output-dir?]"
---

# Rule Structurizer

긴 문서를 `.claude/rules/` 호환 구조로 변환하여 LLM이 필요한 부분만 동적으로 참조할 수 있게 합니다.

## 핵심 원칙

Progressive Disclosure 3단계 로드 모델을 따릅니다:

| 단계 | 파일 | 토큰 | 로드 시점 |
|------|------|------|----------|
| 1단계 | AGENTS.md | ~100 | 항상 |
| 2단계 | RULE.md | <5000 | 관련 작업 시 |
| 3단계 | references/*.md | 무제한 | 필요시만 |

---

## 실행 단계

### 1단계: 문서 분석

입력된 문서에서 다음을 식별합니다:

| 요소 | 추출 내용 |
|------|----------|
| 문서명 | 디렉토리명으로 사용 |
| 핵심 목적 | AGENTS.md 개요에 포함 |
| 주요 섹션 | 자연스러운 단위로 분리 |
| 핵심 내용 | RULE.md에 포함 |

### 2단계: 3단계 분류

문서 내용을 Progressive Disclosure 원칙에 따라 분류:

```
1단계 (AGENTS.md) - 항상 로드 (~100 토큰)
├── 문서 한 줄 설명
├── 핵심 목적/목표 (3개 이내)
└── 섹션 목차 테이블

2단계 (RULE.md) - 관련 작업 시 로드 (<5000 토큰)
├── 핵심 내용 요약
├── 주요 원칙/규칙
├── 필수 체크리스트
└── references 참조 안내

3단계 (references/) - 필요시만 로드
├── {섹션1}.md
├── {섹션2}.md
└── ...
```

### 3단계: 구조 생성

출력 디렉토리에 다음 구조를 생성합니다:

```
.claude/rules/{document-name}/
├── AGENTS.md          # 진입점 - 목차 + 개요
├── RULE.md            # 핵심 내용
├── CLAUDE.md          # "AGENTS.md" (호환성)
└── references/        # 상세 섹션
    └── *.md
```

### 4단계: 검증

- [ ] AGENTS.md가 ~100토큰 이내인가?
- [ ] RULE.md가 5000토큰 / 500줄 이내인가?
- [ ] 각 reference 파일이 단일 관심사에 집중하는가?
- [ ] 목차만으로 어떤 섹션을 참조할지 판단 가능한가?

---

## 입출력 예시

### 입력

```bash
/rule-structurizer docs/my-document.md .claude/rules
```

### 출력 구조

```
.claude/rules/my-document/
├── AGENTS.md
├── RULE.md
├── CLAUDE.md
└── references/
    ├── section-a.md
    ├── section-b.md
    └── section-c.md
```

---

## 파일 작성 규칙

### AGENTS.md (~100 토큰)

목차 형식으로 작성하여 LLM이 필요한 섹션을 빠르게 판단:

```markdown
# {문서명}

> {한 줄 설명}

## 핵심 목적

- {목적 1}
- {목적 2}

## 섹션 안내

| 섹션 | 설명 | 참조 |
|------|------|------|
| 핵심 내용 | {설명} | [RULE.md](RULE.md) |
| {섹션 A} | {설명} | [section-a.md](references/section-a.md) |
| {섹션 B} | {설명} | [section-b.md](references/section-b.md) |
```

### RULE.md (<5000 토큰)

```yaml
---
description: >
  {문서명} 관련 작업 시 적용되는 핵심 내용.
  {트리거 키워드들} 관련 작업 시 활성화.
---
```

본문에는:
- 핵심 원칙/규칙
- 필수 체크리스트
- 주요 제약사항
- references 참조 링크

### CLAUDE.md

```markdown
AGENTS.md
```

### references/*.md

- 파일당 단일 관심사
- 케밥 케이스 파일명: `section-name.md`
- 문서에 해당 내용이 없으면 생성하지 않음

---

## 섹션 분류 가이드

문서 유형에 따라 자연스럽게 섹션 분류:

| 문서 유형 | 가능한 섹션 예시 |
|----------|-----------------|
| PRD | user-stories, functional-specs, technical-specs, constraints |
| 기술 문서 | concepts, architecture, api-reference, examples |
| 가이드 | getting-started, usage, configuration, troubleshooting |
| 정책/규칙 | principles, guidelines, exceptions, examples |

**핵심**: 고정된 템플릿이 아닌, 문서 내용에서 자연스럽게 도출

---

## 상세 참조

- [출력 구조 상세](references/output-structure.md)
- [구조화 가이드](references/structuring-guide.md)

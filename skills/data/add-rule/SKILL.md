---
name: add-rule
description: >
  프로젝트의 rules 구조에 새 규칙을 추가합니다.
  Progressive Disclosure 원칙에 따라 구조화된 규칙 파일을 생성합니다.
  "규칙 추가", "rule 추가", "새 규칙 만들기" 요청 시 활성화.
argument-hint: "[rule-name] [description]"
---

# Add Rule

프로젝트의 `.claude/rules/` 디렉토리에 Progressive Disclosure 원칙에 맞는 규칙을 추가합니다.

## 실행 단계

### 0단계: 사전 조건 확인

`.claude/rules/progressive-disclosure/` 존재 여부 확인.

**규칙이 없는 경우 안내:**
> "Progressive Disclosure 규칙이 설치되어 있지 않습니다.
> 규칙 작성 가이드를 참고하려면 먼저 설치해주세요:
> https://github.com/anthropics/claude-code/tree/main/.claude/rules/progressive-disclosure"

사용자가 설치 후 다시 진행하도록 안내하고 종료합니다.

### 1단계: 요구사항 수집

사용자 입력에서 다음 정보를 파악합니다. **부족한 정보는 반드시 사용자에게 질문**합니다.

| 필수 정보 | 질문 예시 |
|----------|----------|
| 규칙 이름 | "규칙 이름을 지정해주세요 (예: typescript, security)" |
| 규칙 목적 | "이 규칙이 무엇을 하나요?" |
| 트리거 상황 | "어떤 상황에서 이 규칙이 활성화되어야 하나요?" |
| 적용 파일 패턴 (선택) | "특정 파일 패턴에만 적용할까요? (예: `**/*.ts`)" |

### 2단계: 규칙 유형 결정

```
[규칙 복잡도 판단]
    │
    ├─ 단순 규칙 (한 파일로 충분) → 단일 파일: rules/rule-name.md
    │
    └─ 복잡한 규칙 (참조 문서 필요) → 디렉토리: rules/rule-name/
        ├── AGENTS.md
        ├── RULE.md
        └── references/
```

**판단 기준:**
- 상세 예제나 참조 문서가 필요한가?
- 500줄 이하로 작성 가능한가?

### 3단계: 규칙 생성

#### 단일 파일 규칙

```yaml
---
description: >
  [무엇을 하는지] 규칙.
  [언제 활성화되는지] 트리거 키워드 포함.
paths:  # 선택사항
  - "[패턴]"
---

# [규칙 제목]

## 필수 규칙

- [규칙 1]
- [규칙 2]

## 권장 사항

- [권장 1]
```

#### 디렉토리 규칙

**AGENTS.md** (진입점):
```markdown
# [규칙명] 원칙

> [한 줄 요약]

## 목적
[규칙의 목적 설명]

## 핵심 체크리스트
- [ ] [체크 1]
- [ ] [체크 2]

## 관련 레퍼런스
- [상세 가이드](references/guide.md)
```

**RULE.md** (핵심 지침):
```yaml
---
description: >
  [무엇] 규칙.
  [언제] 활성화.
paths:  # 선택사항
  - "[패턴]"
---

# [규칙 제목]

[핵심 지침 내용 - 5000 토큰 이하]
```

### 4단계: 인덱스 업데이트

`.claude/rules/AGENTS.md`에 새 규칙 추가:

```markdown
| [rule-name] | [트리거 상황] | [rule-name/](rule-name/) |
```

## 체크리스트

생성 전 확인:

```
□ description이 "무엇 + 언제"를 설명하는가?
□ name이 소문자/하이픈 규칙을 따르는가?
□ 본문이 500줄/5000토큰 이하인가?
□ paths가 적절한 파일에만 활성화되는가? (선택사항)
□ AGENTS.md 인덱스에 추가되었는가?
```

## 상세 가이드

- [Progressive Disclosure 규칙 작성 가이드](rules/progressive-disclosure)

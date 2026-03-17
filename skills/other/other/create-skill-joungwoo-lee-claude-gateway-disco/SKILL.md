---
name: create-skill
description: |
  새로운 Claude Code 스킬(슬래시 커맨드)을 작성할 때 사용하는 스킬.
  사용자가 스킬을 만들어달라고 하거나, "/create-skill"을 입력하면 활성화됩니다.
argument-hint: "[스킬이름] [스킬 설명]"
---

# Claude Code 스킬 작성 가이드

사용자가 요청한 스킬을 아래 규칙에 따라 작성하라.
인자가 있으면 참고하고, 없으면 사용자에게 어떤 스킬을 만들지 물어봐라.

요청: $ARGUMENTS

---

## 1. 파일 구조

```
.claude/skills/<skill-name>/
├── SKILL.md          # 필수. 스킬 본체
├── reference.md      # 선택. 상세 레퍼런스
├── examples/         # 선택. 예제 모음
└── scripts/          # 선택. 실행 스크립트
```

- 스킬 이름(디렉토리명): 소문자, 숫자, 하이픈만 허용 (최대 64자)
- `SKILL.md` 하나만 있으면 동작한다

---

## 2. SKILL.md 포맷

```yaml
---
name: my-skill
description: |
  이 스킬이 뭘 하는지, 언제 트리거되는지 설명.
  Claude가 이 description을 보고 자동 호출 여부를 판단한다.
argument-hint: "[arg1] [arg2]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Bash(npm *)
context: fork
agent: Explore
---

# 스킬 제목

본문 지시사항...
```

### 프론트매터 필드 요약

| 필드 | 필수 | 설명 |
|------|------|------|
| `name` | 아니오 | 슬래시 커맨드 이름. 생략 시 디렉토리명 사용 |
| `description` | 권장 | Claude가 자동 호출 판단에 사용. 핵심 키워드 포함할 것 |
| `argument-hint` | 아니오 | 자동완성 시 보여줄 인자 힌트 |
| `disable-model-invocation` | 아니오 | `true`면 Claude 자동 호출 차단. 수동(`/name`)으로만 실행 |
| `user-invocable` | 아니오 | `false`면 `/` 메뉴에서 숨김. 배경지식용 |
| `allowed-tools` | 아니오 | 권한 확인 없이 쓸 수 있는 도구 목록 |
| `context` | 아니오 | `fork`면 격리된 서브에이전트에서 실행 |
| `agent` | 아니오 | `context: fork` 시 사용할 에이전트 타입 |

---

## 3. 변수 치환

| 변수 | 설명 |
|------|------|
| `$ARGUMENTS` | 전체 인자 문자열 |
| `$ARGUMENTS[N]` 또는 `$N` | N번째 인자 (0-based) |
| `${CLAUDE_SESSION_ID}` | 현재 세션 ID |

---

## 4. 호출 제어 패턴

| 목적 | 설정 |
|------|------|
| 기본 (사용자+Claude 모두 호출) | 설정 없음 |
| 사용자만 수동 호출 | `disable-model-invocation: true` |
| Claude만 자동 호출 (메뉴 숨김) | `user-invocable: false` |

**규칙**: 부작용(배포, 커밋 등)이 있는 스킬은 반드시 `disable-model-invocation: true` 설정.

---

## 5. 저장 위치와 우선순위

| 우선순위 | 위치 | 범위 |
|----------|------|------|
| 1 (최고) | Enterprise 관리 설정 | 조직 전체 |
| 2 | `~/.claude/skills/` | 개인 전체 |
| 3 | `.claude/skills/` | 프로젝트 |
| 4 (최저) | 플러그인 | 플러그인 범위 |

동일 이름이면 높은 우선순위가 이긴다.

---

## 6. 스킬 로드 조건

스킬을 만들어도 Claude가 인식하지 못하면 소용없다. 로드되려면 아래 조건을 충족해야 한다.

### 필수 조건
1. **올바른 경로에 `SKILL.md` 존재**: `.claude/skills/<name>/SKILL.md` 또는 `~/.claude/skills/<name>/SKILL.md`
2. **프론트매터 형식 정확**: `---`로 감싼 YAML 블록이 파일 최상단에 있어야 함
3. **description 존재**: 없으면 본문 첫 문단이 대신 쓰이지만, 명시하는 것을 권장

### 로드 시점
- Claude Code 시작 시 모든 스킬의 **description만** 컨텍스트에 로드됨 (본문은 호출 시 로드)
- description은 컨텍스트 윈도우의 ~2% 예산 내에서 로드 (최소 16,000자 보장)
- 스킬이 너무 많으면 일부 description이 잘릴 수 있음

### 로드 확인 방법
- `/context` 명령으로 현재 로드된 스킬 목록과 예산 초과 경고 확인 가능
- 스킬이 안 보이면 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 환경변수로 예산 확대

### 로드 안 되는 흔한 원인
| 증상 | 원인 | 해결 |
|------|------|------|
| `/` 메뉴에 안 나옴 | 파일 경로 오류 또는 `user-invocable: false` | 경로 확인, 설정 확인 |
| Claude가 자동 호출 안 함 | `disable-model-invocation: true` 또는 description에 키워드 부족 | 설정 확인, description 개선 |
| 스킬 목록에서 누락 | description 예산 초과 | `/context`로 확인, 예산 확대 |
| 프론트매터 무시됨 | YAML 문법 오류 (들여쓰기, 콜론 뒤 공백 등) | YAML 린트 확인 |
| 모노레포에서 안 보임 | 하위 디렉토리의 `.claude/skills/`에 있는데 상위에서 실행 | 작업 디렉토리 확인 또는 `--add-dir` 사용 |

---

## 7. 작성 노하우

### description 잘 쓰기
- 사용자가 자연스럽게 말할 키워드를 포함
- BAD: `"코드 도우미"` -> 너무 모호
- GOOD: `"코드를 시각적 다이어그램과 비유로 설명. 사용자가 '이 코드 어떻게 동작해?' 같은 질문을 할 때 사용"`

### 본문 지시사항 작성 원칙
1. **명확한 역할 부여**: "너는 ~하는 전문가다" 식으로 시작
2. **단계별 지시**: 번호 매긴 단계로 작업 흐름 정의
3. **제약 조건 명시**: 하지 말아야 할 것도 명확히
4. **출력 형식 지정**: 원하는 결과물 포맷 제시
5. **500줄 이내**: 길면 별도 파일로 분리 후 참조

### 서브에이전트 활용
조사/탐색 위주 스킬은 `context: fork`로 격리 실행:
```yaml
context: fork
agent: Explore
```
메인 대화 컨텍스트를 오염시키지 않는다.

### 딥 씽킹 활성화
본문 어딘가에 `ultrathink`를 넣으면 확장 사고 모드가 켜진다.

---

## 8. 스킬 작성 절차

위 규칙을 따라 아래 순서로 스킬을 생성하라:

1. 사용자 요구사항 파악 (인자 또는 질문으로)
2. 스킬 이름, description, 호출 방식 결정
3. `.claude/skills/<name>/SKILL.md` 작성
4. 필요시 보조 파일(reference.md, scripts/) 추가
5. 작성 결과를 사용자에게 요약 보고

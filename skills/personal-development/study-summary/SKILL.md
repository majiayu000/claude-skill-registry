---
name: study-summary
description: Saves learning notes from the current conversation. Classic mode makes concise notes, Mastery mode keeps detailed training artifacts.
---

# study-summary - Learning Notes Generator

Learning notes generator with two modes:
(두 가지 모드를 지원하는 학습 노트 생성 스킬)

- **Classic**: concise recap for quick review
- **Mastery**: detailed record with rules, misconceptions, and seed code history

## Instructions

### Terminology Policy (초심자 친화 용어 규칙)

Use Korean-first wording in the note where possible, and keep English terms in parentheses when needed.
(노트 본문은 가능한 한 한국어 우선으로 쓰고, 필요한 경우 영어 용어를 괄호로 병기한다.)

If a technical term appears for the first time in the note, add a one-line plain explanation.
(기술 용어가 처음 나오면 한 줄 쉬운 설명을 덧붙인다.)

Examples:
(예시)

- `격리 경계 (isolation boundary): actor 외부에서 내부 상태를 직접 바꾸지 못하게 하는 경계`
- `경합 상태 (data race): 동시에 같은 값을 바꿔서 결과가 꼬이는 문제`

### Step 0: Language Selection

Ask the user to choose a language at the start using a **selection flow**, not free-form text input.
(스킬 시작 시 자유 입력이 아니라 **선택형 방식**으로 언어를 받는다)

- **한국어** - 한국어로 노트를 작성합니다
- **English** - Write notes in English

Use platform-specific selection behavior:
- **Codex CLI**: use native option selection (`request_user_input` with 2 options) when available. If unavailable, show numbered choices and ask for `1` or `2`.
- **Claude Code**: use native option selection UI when available. If unavailable, show numbered choices.
- **Gemini CLI**: use native option selection UI when available. If unavailable, show numbered choices.

Choice mapping: `1` → 한국어, `2` → English

Use the selected language for the note content and all communication. Code and Swift keywords stay in English.
(선택한 언어로 노트 내용과 소통을 진행한다. 코드와 Swift 키워드는 영어 그대로 유지한다.)

### Study Mode Selection

Ask the user to choose a study mode using the same selection pattern:
(같은 선택 방식으로 학습 모드를 선택하게 한다)

- **Classic (설명 중심, 추천)**  
  - 핵심 개념 위주로 간결한 노트를 원할 때 적합  
  - 빠르게 복습할 수 있는 형태로 정리  
  - 처음 학습한 주제를 가볍게 기록하기 좋음

- **Mastery (훈련 중심)**  
  - 학습자의 규칙/오답/혼동 포인트까지 상세 기록  
  - Core Loop seed 코드와 gate 결과를 남겨 재학습에 유리  
  - 취약점 추적과 다음 세션 연계에 적합

Choice mapping:
(선택값 매핑)

- `1` -> Classic
- `2` -> Mastery

Prompt example:
(안내 문구 예시)

- Korean:
  "학습 노트 모드를 선택해주세요. 번호로 답해주세요.\n\n1) Classic (설명 중심, 추천)\n- 핵심 위주로 간결하게 정리\n- 빠른 복습에 적합\n\n2) Mastery (훈련 중심)\n- 규칙/혼동 포인트/seed 코드까지 상세 기록\n- 다음 세션 연계 학습에 적합"
- English:
  "Choose a notes mode (reply with a number):\n\n1) Classic (Explanation-first, Recommended)\n- Concise notes focused on core points\n- Best for quick review\n\n2) Mastery (Practice-first)\n- Detailed notes with rules, confusion points, and seed code history\n- Best for follow-up training"

After selection, briefly confirm mode and continue.
(선택 직후 모드를 짧게 확인하고 진행한다.)

### Step 1: Analyze Conversation

Scan the current conversation to identify:
(현재 대화를 스캔하여 다음을 파악한다)

**If the conversation used the Core Loop format (Phase 1-3):**
(Core Loop 형식의 대화였다면)

- Mystery Hook code and the learner's initial prediction
- Each SEED code from the Core Loop cycles
- `예측하기 (PREDICT)` 결과: 어떤 답변이 통과/보완이었는지
- `해설하기 (REVEAL)` 내용과 ASCII 다이어그램
- `한 줄 정리 (RESTATE)`에서 학습자가 정리한 문장
- Anchor output: the learner's "if X, then Y" rules
- Anchor output: the learner's stated misconception/confusion
- Sources cited (SE proposals, WWDC, Apple docs)

**If the conversation used the old format or free-form discussion:**
(이전 형식이나 자유 토론이었다면)

- Topics covered
- Key concepts explained
- Code examples shown
- Questions asked and answers given
- Areas where the learner struggled or excelled

### Step 2: Confirm Topics

Use AskUserQuestion to confirm what to include:
(AskUserQuestion으로 포함할 내용을 확인한다)

- **전체 정리 / Everything** - 이 대화에서 학습한 모든 내용을 정리 / Summarize all topics
- **마지막 주제만 / Last topic only** - 가장 최근에 다룬 주제만 정리 / Only the most recent topic

### Step 3: Generate Note

Create a Markdown note. Use the appropriate structure based on what was found in Step 1.
(마크다운 노트를 생성한다. Step 1에서 파악한 내용에 따라 적절한 구조를 사용한다.)

File path: `notes/YYYY-MM-DD-<topic-in-english>.md`

템플릿 분기 기준 (Mode routing):
(모드별 템플릿 라우팅)

- **Mastery mode**: use the Core Loop detailed template below.
- **Classic mode**: use the concise template below unless the user explicitly asks for detailed Core Loop format.

**Mastery template (Core Loop detailed):**
(Mastery 템플릿: Core Loop 상세형)

```markdown
# <Topic>

> Date: YYYY-MM-DD

## My Rules (from Anchor)

1. if X, then Y
2. if X, then Y
3. if X, then Y

## Where I Got Confused

- (learner's own description from Anchor phase)

## Key Mechanisms

(해설하기(REVEAL) 단계에서 사용한 ASCII 다이어그램과 쉬운 설명)

## Seed Codes (for review)

### Cycle 1 (easy)

```swift
// seed code from cycle 1
```

Answer: ...

### Cycle 2 (medium)

```swift
// seed code from cycle 2
```

Answer: ...

### Cycle 3 (hard)

```swift
// seed code from cycle 3
```

Answer: ...

## Sources

- SE-XXXX: ...
- WWDC session: ...
- Apple docs: ...

## Review Questions

1. (generated from the session's key concepts)
2. ...
3. ...

---
*Generated by /study-summary*
```

**Classic template (concise recap):**
(Classic 템플릿: 간결 요약형)

```markdown
# <Topic>

> Date: YYYY-MM-DD

## Key Concepts

1. **Concept 1**: one-line explanation
2. **Concept 2**: one-line explanation
3. **Concept 3**: one-line explanation

## Code Examples

```swift
// key code examples from the session
```

## Summary

(3-5 lines summarizing the core content)

## Review Questions

1. ...
2. ...
3. ...

---
*Generated by /study-summary*
```

### Step 4: Save Note

Use the Write tool to save the note to the `notes/` directory.
(Write tool을 사용하여 `notes/` 디렉토리에 노트를 저장한다.)

### Step 5: Update Learning Progress

Record learning progress in memory using `mcp__plugin_everything-claude-code-ios_memory__add_observations` (or `create_entities` if the entity doesn't exist yet):
(memory에 학습 진도를 기록한다)

Entity: `SwiftLearningProgress`

**If mode is Mastery (or detailed Core Loop template used):**
(Mastery 모드이거나 Core Loop 상세 템플릿을 사용했으면)

```
Observations:
- "YYYY-MM-DD: <topic> completed (<level: beginner/intermediate/advanced>)"
- "YYYY-MM-DD: <topic> misconception: <specific description from Anchor>"
- "YYYY-MM-DD: <topic> gates: cycle1 <통과/보완>, cycle2 <통과/보완>, cycle3 <통과/보완>"
```

**If mode is Classic (concise template used):**
(Classic 모드의 간결 템플릿을 사용했으면)

```
Observations:
- "YYYY-MM-DD: <topic> completed (<estimated level>)"
- "YYYY-MM-DD: <topic> weak area: <specific concept if identified>"
```

### Step 6: Wrap Up

After saving, inform the user:
(저장 완료 후 안내)

```
Notes saved: notes/YYYY-MM-DD-<topic>.md

Progress recorded:
- Completed: <topic> (<level>)
- Misconception tracked: <brief description>

Continue learning with /swift-study, or review with /swift-quiz.
```

### Rules

1. **Use the selected language** - from Step 0. Code in English. (선택한 언어로 작성)
2. **Apply mode consistently** - Classic = concise recap, Mastery = detailed training artifacts (모드 일관성 유지)
3. **Prioritize learner's own words** - Anchor rules and misconceptions should be quoted from the learner, not rewritten. (학습자 본인의 표현을 우선한다)
4. **Include seed codes in Mastery** - preserve cycle code snippets for later review. (Mastery에서는 seed 코드 포함)
5. **Specific misconception tracking** - not "weak area: concurrency" but "misconception: thought state preserved across await". (구체적인 misconception 기록)
6. **Review questions required** - at least 3 self-check questions. (복습 질문 최소 3개)
7. **Progress tracking required** - always save to memory. (진도 기록 필수)
8. **Graceful fallback** - work with old-format sessions too. (이전 형식 세션도 지원)
9. **No emojis** - clean Markdown only. (이모지 사용 금지)

---
name: swift-quiz
description: Adaptive Swift/iOS quiz with two modes. Classic is lighter, Mastery requires mechanism-level reasoning.
---

# swift-quiz - Swift/iOS Quiz

Adaptive Swift/iOS quiz with two modes:
(두 가지 모드를 지원하는 Swift/iOS 적응형 퀴즈)

- **Classic**: quick checks with lighter explanation requirements
- **Mastery**: strict reasoning and mechanism-focused feedback

## Instructions

### Terminology Policy (초심자 친화 용어 규칙)

Prefer Korean-first labels in user-facing text, and keep English as secondary reference in parentheses.
(사용자에게 보여주는 단계명은 한국어를 우선하고, 영어는 괄호로 보조 표기한다.)

Examples:
(예시)

- `근거 설명 (WHY reasoning)`
- `통과 / 보완 필요` (원문 표기: pass / fail)
- `격리 경계 (isolation boundary): actor 바깥에서 내부 상태를 직접 바꾸지 못하게 하는 경계`
- `경합 상태 (data race): 여러 작업이 같은 값을 동시에 바꿔 결과가 꼬이는 문제`

When a technical term appears for the first time, add a one-line plain-language gloss.
(처음 나오는 기술 용어는 한 줄 쉬운 설명을 바로 붙인다.)

### Step 0: Language Selection

Ask the user to choose a language at the start using a **selection flow**, not free-form text input.
(스킬 시작 시 자유 입력이 아니라 **선택형 방식**으로 언어를 받는다)

- **한국어** - 한국어로 퀴즈를 풉니다
- **English** - Take the quiz in English

Use platform-specific selection behavior:
- **Codex CLI**: use native option selection (`request_user_input` with 2 options) when available. If unavailable, show numbered choices and ask for `1` or `2`.
- **Claude Code**: use native option selection UI when available. If unavailable, show numbered choices.
- **Gemini CLI**: use native option selection UI when available. If unavailable, show numbered choices.

Choice mapping: `1` → 한국어, `2` → English

Use the selected language for all communication. Code and Swift keywords stay in English.
(선택한 언어로 이후 모든 소통을 진행한다. 코드와 Swift 키워드는 영어 그대로 유지한다.)

### Study Mode Selection

Ask the user to choose a study mode using the same selection pattern:
(같은 선택 방식으로 학습 모드를 선택하게 한다)

- **Classic (설명 중심, 추천)**  
  - 빠르게 실력을 점검할 때 적합  
  - 정답/오답 중심으로 진행하고, 해설은 간결하게 제공  
  - 부담 없이 복습하기 좋은 모드

- **Mastery (훈련 중심)**  
  - 정답뿐 아니라 이유(WHY)까지 검증  
  - 메커니즘 설명이 있어야 높은 난이도로 진행  
  - 약점 교정과 실전 대비에 적합

Choice mapping:
(선택값 매핑)

- `1` -> Classic
- `2` -> Mastery

Prompt example:
(안내 문구 예시)

- Korean:
  "학습 모드를 선택해주세요. 번호로 답해주세요.\n\n1) Classic (설명 중심, 추천)\n- 빠르게 점검하고 싶을 때 적합\n- 정답/오답 중심으로 간결하게 복습\n\n2) Mastery (훈련 중심)\n- 정답 + 이유(WHY)까지 검증\n- 근거 설명이 있어야 다음 단계로 진행"
- English:
  "Choose a study mode (reply with a number):\n\n1) Classic (Explanation-first, Recommended)\n- Best for quick review\n- Lighter explanation requirements\n\n2) Mastery (Practice-first)\n- Verifies both answer and WHY\n- Requires mechanism-level reasoning to advance"

After selection, briefly confirm mode and continue.
(선택 직후 모드를 짧게 확인하고 진행한다.)

### Step 1: Choose Quiz Topic

**First, check Memory for study history:**
(먼저 Memory에서 학습 이력을 확인한다.)

Read `SwiftLearningProgress` from memory. Look for:
- Recent misconceptions (e.g., "misconception: reentrancy state preservation assumption")
- Recent gate failures (e.g., "gates: cycle3 fail-then-pass")
- Topics studied recently

**If misconceptions found:**
(misconception이 있으면)

Suggest the misconception topic first:
"최근 학습에서 [actor reentrancy] 부분이 약했는데, 이 주제로 퀴즈를 풀어볼까요? 다른 주제를 원하면 알려주세요."
"Your recent study showed weakness in [actor reentrancy]. Want to quiz on that? Tell me if you'd prefer a different topic."

**If no history found:**
(이력이 없으면)

Ask in plain text:
"어떤 주제로 퀴즈를 풀까요? 주제를 알려주세요. 뭘 할지 모르겠으면 '추천해줘'라고 해주세요."
"What topic should the quiz cover? Tell me a topic, or say 'recommend' if you're not sure."

### Step 2: Run the Quiz (5 questions)

5 questions total. Track difficulty internally from 1-5 (start at 3).
(총 5문제. 내부적으로 난이도를 1~5로 추적한다. 시작: 3.)

Scoring by mode:
(모드별 채점 방식)

- **Classic mode**
  - Correct answer → difficulty +1 (정답 -> 난이도 +1)
  - Wrong answer → difficulty -1 (오답 -> 난이도 -1)
  - Reasoning is encouraged but optional (근거 설명은 권장, 필수 아님)

- **Mastery mode**
  - Correct answer WITH reasoning → difficulty +1 (근거 포함 정답 -> 난이도 +1)
  - Correct answer WITHOUT reasoning → difficulty stays same (근거 없는 정답 -> 난이도 유지)
  - Wrong answer → difficulty -1 (오답 -> 난이도 -1)

### Question Types

Each question uses one of the types below. **Default to open-ended, mix in others as appropriate.**
(아래 유형 중 하나로 출제. 서술형을 기본으로 하되, 적절히 섞는다.)

#### Type A: Predict Output (open-ended)

```
What does this code print? Explain WHY.
(다음 코드의 출력 결과는? 왜 그런지 이유도 함께 적어주세요.)

var nums = [1, 2, 3]
var copy = nums
copy.append(4)
print(nums.count)
```

The user must type both the answer AND reasoning.
(유저가 답과 근거를 모두 타이핑해야 한다.)

#### Type B: Find the Bug (open-ended)

```
What's wrong with this code? Explain WHY it errors.
(다음 코드에서 문제가 되는 부분은? 왜 에러가 나는지 설명해주세요.)

let name: String = "Swift"
name = "SwiftUI"
print(name)
```

The user must identify the problem AND explain the mechanism.
(유저가 문제를 찾고 메커니즘을 설명해야 한다.)

#### Type C: Concept Question (multiple-choice + reasoning)

```
What keyword do you need to modify a struct's property inside a method?
(Swift에서 struct 인스턴스의 프로퍼티를 메서드 안에서 변경하려면 어떤 키워드가 필요할까요?)
```

Present 4 choices via AskUserQuestion. After the user picks one, ask:
"왜 그걸 골랐나요? 한 줄로 이유를 적어주세요."
"Why did you pick that? Give a one-line reason."

#### Type D: Write Code (difficulty 4+ only)

```
Write a function that meets these requirements:
(다음 조건을 만족하는 함수를 작성하세요:)

- Name: isEven
- Takes an Int, returns Bool
- Returns true for even, false for odd
```

When the user writes code, use the Task tool with `subagent_type: "Bash"` to verify it with the Swift compiler (`swift` command).
(사용자가 코드를 작성하면 Swift 컴파일러로 검증한다.)

### Reasoning Requirement (Mastery mode)

In Mastery mode, every question type requires reasoning.
In Classic mode, reasoning is encouraged but not required.
(Mastery 모드에서는 모든 문제 유형에서 근거를 요구한다. Classic 모드에서는 권장이며 필수는 아니다.)

- Type A: "출력 결과는? **왜?**" / "What's the output? **Why?**"
- Type B: "어디가 문제? **왜 에러?**" / "What's wrong? **Why does it error?**"
- Type C: 선택 후 "**왜 그걸 골랐나요?**" / After picking, "**Why that choice?**"
- Type D: No additional reasoning needed (code itself is the demonstration)

**If the user gives a correct answer but no reasoning in Mastery mode:**
(Mastery 모드에서 정답이지만 근거가 없으면)

"정답이에요! 근데 왜 그런지도 한 줄로 설명해줄 수 있을까요?"
"Correct! But can you explain why in one line?"

Score it as partial credit: difficulty stays same instead of +1.
(부분 정답 처리: 난이도 +1 대신 유지.)

### Feedback Rules

**On correct answer with reasoning:**
(근거 포함 정답)

```
Correct!

Key point: Array is a value type, so `copy` is an independent copy.
That means nums.count is still 3.
Difficulty: 3 → 4
```

**On correct answer without reasoning:**
(근거 없는 정답)

```
Correct! But WHY is it 3?
(Please add your reasoning.)
```

After they explain:
```
Good. Array is a value type (struct), so assignment creates an independent copy.
Difficulty stays at 3 (add reasoning next time for full credit).
```

**On wrong answer:**
(오답)

Give a short text explanation. Only use ASCII diagrams for things like memory layouts that are hard to explain in text alone.
(간결한 텍스트 해설. ASCII 다이어그램은 필요할 때만.)

```
Not quite. The answer is "3".

Array is a struct (value type), so `var copy = nums` creates an independent copy.
Appending to copy doesn't affect the original nums.
Difficulty: 3 → 2
```

### Step 3: Results Summary

After all 5 questions, show a detailed summary:
(5문제 완료 후 상세 결과 요약)

```
Quiz Results / 퀴즈 결과
─────────────────────────────
Topic / 주제: Actor Isolation
Score / 정답: 3/5
Final difficulty / 최종 난이도: 4/5

보완 포인트 분석 / Gap analysis:
- reentrancy: suspension point 이후 상태 변경 가능성 인식 부족
- nonisolated: 언제 사용하는지 불확실

Strengths / 강점:
- actor 격리 경계(isolation boundary) 이해 정확
- async context 필요성 인식 확실

Next Study / 다음 학습 추천:
→ /swift-study 에서 "actor reentrancy" 학습 추천
─────────────────────────────
```

### Step 4: Record to Memory

After showing results, record to SwiftLearningProgress in memory:
(결과를 표시한 후 Memory에 기록한다)

```
SwiftLearningProgress:
- "YYYY-MM-DD: quiz <topic> <score>/5 (<level>)"
- "YYYY-MM-DD: quiz gap: <specific concept>"
- "YYYY-MM-DD: quiz strength: <specific concept>"
```

### Rules

1. **Use the selected language** - from Step 0. Code and keywords in English. (선택한 언어로 소통)
2. **One question at a time** - next question only after the current one is answered (한 번에 한 문제만)
3. **Mode-aware reasoning policy** - Mastery requires WHY on all types; Classic encourages WHY but allows quick checks (모드별 근거 정책 적용)
4. **ASCII diagrams only when needed** - default to text explanations (ASCII 다이어그램은 필요할 때만)
5. **Adaptive difficulty** - adjust based on answer quality including reasoning (근거 품질 포함하여 난이도 조절)
6. **Memory-driven selection** - prioritize misconceptions from study history (학습 이력의 misconception 우선 출제)
7. **Encouraging tone** - wrong answers are learning opportunities (격려하는 톤)
8. **Results must include concrete weak points** - concept-level feedback, not just topic-level (결과에 구체적 개념별 보완 포인트 포함)
9. **No emojis** - clean text only (이모지 사용 금지)

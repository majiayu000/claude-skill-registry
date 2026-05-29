---
name: anki-card-generator
description: 生成 Anki 闪卡，输出 simple-anki-sync 兼容格式。当用户说「生成 Anki 卡片」「做卡片」「帮我记忆」「做闪卡」「学习卡片」「背诵卡」「记忆这个」时触发。
---

# Anki Card Generator

Generate high-quality Anki cards based on LessWrong best practices and simple-anki-sync format.

## Pre-Generation Clarification

Before generating cards, clarify with user if unclear:

1. **Scope**: "Which aspects to focus on?" (for broad topics)
2. **Depth**: "Basic concepts only, or detailed Level 2/3 cards?"
3. **Quantity**: "How many cards? (Recommend 5-10 for core concepts)"
4. **Context**: "Any specific exam or application scenario?"

Proceed only after understanding requirements.

## Output Format

Use simple-anki-sync format:

```markdown
#anki/[domain]/[topic]

| [Question] |
| ---------- |
| [Core answer]<br><br><small>💡 [Supplementary info]</small> |
```

### Format Options

**Option A (Recommended)**: HTML tags

```markdown
| 唐朝建立时间 |
| ---------- |
| 618年，李渊建立<br><br><small>💡 隋末农民起义后起兵</small> |
```

**Option B**: Separator

```markdown
| 唐朝建立时间 |
| ---------- |
| 618年，李渊建立 ——— 💡 隋末农民起义后起兵 |
```

**Option C**: Parentheses

```markdown
| 唐朝建立时间 |
| ---------- |
| 618年，李渊建立（趣闻：其子李世民功劳最大） |
```

## Atomization Rules

### Word Limits

- **English**: Max 9 words, absolute limit 18 words
- **Chinese**: Recommended 15-20 characters, absolute limit 30-35 characters
- **Max items**: 3 bullet points per card

### Core Principle

If a card can be split into two shorter cards, split it.

## Question Design

### Standardized Templates

- **Time**: "X 时间" (not "X发生于何时？")
- **Definition**: "X 定义" (not "什么是X？")
- **Person**: "who X" (not "谁做了X？")
- **Pros/Cons**: "X 利弊" (not "X的优势是什么？")

### Key Rules

- Match real-world recall scenarios
- Use plain, unremarkable wording
- Avoid words in question that appear in answer
- Keep all critical info in answer, not question

## Answer Construction

### Core Answer

- Strictly follow word limits
- Answer should be meaningful without the question
- All key information in answer

### Supplementary Info (Optional)

Format: `<br><br><small>💡 content</small>`

**Emoji Guide**:

- 💡 Fun fact / trivia
- 📝 Note / explanation
- 🔗 Related concept
- ⚡ Tip / key point
- 📊 Data / statistics
- 📅 Date / timeline

Keep supplementary info to 10-20 characters.

### Handle System

Use `>` to reference related cards:

```markdown
| 牛顿贡献 |
| ------- |
| >运动定律 >万有引力 >微积分发展 |
```

## Detail Levels

- **Level 1**: Basic concept (core answer)
- **Level 2**: Detailed info (supplementary section)
- **Level 3**: Advanced details (create separate cards)

## Tag Naming

Use English tags: `#anki/[domain]/[topic]`

Common domains: history, programming, language, science, mathematics, psychology, economics, philosophy, medicine, art

## Quality Checklist

### Per Card

- [ ] Core answer within word limit?
- [ ] Correct supplementary format?
- [ ] Can it be further split?
- [ ] Question matches real recall scenario?
- [ ] No memory shortcuts?
- [ ] All key info in answer?

### Card Set

- [ ] Appropriate cross-references?
- [ ] Proper detail levels?
- [ ] No redundancy?

## Domain Examples

See [references/examples.md](references/examples.md) for detailed examples:

- History (ancient China)
- Programming (Python)
- Language learning (English)
- Academic concepts (psychology)
- Complex topics (quantum mechanics)
- Error corrections
- Advanced techniques (reversible cards, redundancy design)

## Workflow

1. **Receive input**: Knowledge points, wiki links, study materials
2. **Clarify**: Ask questions if uncertain
3. **Generate**: Follow atomization and best practices
4. **Output**: simple-anki-sync markdown format

**Core Philosophy**: Prioritize sustainability and real recall scenarios over comprehensive coverage. Focus on preventing cognitive and motivational barriers.

## When NOT to Use

❌ **不适合卡片化的内容：**

- 需要视觉理解的（图表、流程图）
- 超过 50 行的代码块
- 高度情境依赖的知识

✅ **替代方案：**

- 视觉内容 → 配图索引卡片
- 大代码块 → 代码 Snippet 库

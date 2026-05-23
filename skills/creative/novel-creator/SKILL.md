---
name: novel-creator
description: |
  Interactive novel creation workflow combining RPG-style storytelling with professional EPUB ebook production.
  Use when users want to: (1) Create interactive stories/RPG games with branching choices, (2) Write full novels from story concepts,
  (3) Generate novels with time-travel/fantasy/romance elements, (4) Convert markdown stories to EPUB ebooks,
  (5) Create Chinese web novels with ancient poetry paired with modern lyrics, (6) Write light novels or serialized fiction.
  Triggers: "write a novel", "create a story", "interactive fiction", "RPG story", "make an ebook", "穿越小说", "写小说", "创作故事", "制作电子书"
---

# Novel Creator

Transform story ideas into complete novels with EPUB output through an interactive RPG-style workflow.

## Workflow

```
[Story Concept] → [Interactive RPG] → [Writing Plan] → [Chapters] → [EPUB]
     Phase 1           Phase 2           Phase 3        Phase 4     Phase 5
```

## Phase 1: Story Setup

Use `AskUserQuestion` tool to gather:

| Element | Options | Default |
|---------|---------|---------|
| Genre | 穿越/Fantasy/Romance/Mystery | 穿越 |
| Setting | Ancient palace/Modern/Fantasy world | Palace |
| Protagonist | Name, background, abilities | - |
| Goal | What to achieve | Survive and thrive |
| Length | Chapters × words | 10 × 5000 |

Load character personas from `references/personas.md` based on setting.

## Phase 2: Interactive RPG

Run 10-15 decision points where user makes choices via `AskUserQuestion`:

```
[Vivid scene description]
↓
AskUserQuestion with 3-4 meaningful choices
↓
[Consequence + next scene]
```

**Required elements to weave in:**
- **Tech/Knowledge**: Modern knowledge as "magic" (phone→照妖镜, chemistry→炼丹)
- **Fantasy**: Special abilities (灵觉), artifacts (蓄雷珠), prophecies
- **Romance**: First meeting → mutual help → feelings → confession

**Track throughout:**
- Key plot points and decisions
- Relationship development stages
- Items and abilities acquired
- Foreshadowing seeds planted

## Phase 3: Writing Plan

Create `task_plan.md` with:

```markdown
# Writing Plan: [Title]

## Characters
| Name | Role | Traits | Arc |
|------|------|--------|-----|

## Foreshadowing Matrix
| Element | Ch.1 Hint | Development | Payoff |
|---------|-----------|-------------|--------|
| Tech | [seed] | Ch.4 [use] | Ch.9 [climax] |
| Fantasy | [seed] | Ch.6 [reveal] | Ch.9 [power] |
| Romance | [meeting] | Ch.5 [feelings] | Ch.10 [love] |

## Poetry Pairings (Chinese novels)
| Ch | Ancient Poetry | Modern Lyrics | Theme |
|----|----------------|---------------|-------|
See references/poetry_pairs.md for suggestions.

## Chapter Outline
- [ ] Ch.1: [title] - [key scenes, ~5000 words]
...

## Progress
| Ch | Status | Words |
|----|--------|-------|
```

## Phase 4: Chapter Writing

Write each chapter (~4000-5500 words) following this structure:

```markdown
# 第X章：[押韵标题]

> *[Ancient poetry quote]*
> *——[Author]《[Title]》*

---

## 一
[Scene 1: Setting + action]

## 二
[Scene 2: Dialogue + conflict]

## 三
[Scene 3: Resolution + hook]

---

（第X章完）

---

> *"[Modern lyrics quote]"*
> *——《[Song]》*
```

**Writing checklist:**
- [ ] Vivid sensory descriptions (sight, sound, smell, touch)
- [ ] Dialogue with subtext (what's said vs. what's meant)
- [ ] Internal monologue showing modern perspective
- [ ] Proper pacing (action → dialogue → reflection)
- [ ] Foreshadowing elements per plan
- [ ] Chapter-end hook

**File naming:** `[##]_[章节标题].md` (e.g., `01_梦回千年惊鸿起.md`)

Update `task_plan.md` progress after each chapter.

## Phase 5: EPUB Generation

Run:
```bash
python3 scripts/create_epub.py
```

Script auto-detects chapter files in current directory and generates:
- Cover page with title/subtitle/author
- Introduction page
- All chapters with proper formatting
- Table of contents
- Chinese typography CSS

Output: `[书名].epub`

## Quick Commands

| User says | Action |
|-----------|--------|
| "写一部穿越小说" | Full workflow Phase 1-5 |
| "根据大纲写小说" + outline | Phase 3-5 |
| "把章节转成epub" | Phase 5 only |
| "继续写下一章" | Resume Phase 4 |

## Resources

- `scripts/create_epub.py` - EPUB generator
- `references/personas.md` - Character templates by setting
- `references/poetry_pairs.md` - Poetry and lyrics pairings

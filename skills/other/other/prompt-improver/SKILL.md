---
name: prompt-improver
description: Transform vague prompts into rich, structured prompts with automatic fallback
---

## Purpose

Transform vague, ambiguous prompts into rich, well-structured prompts. Uses Anthropic's prompt improvement capabilities when available, with graceful fallback to the current LLM.

**How it works:**
1. User provides a vague prompt (e.g., "critique this doc")
2. Skill improves the prompt using best available method
3. Executes the improved prompt and returns results
4. User sees the answer **without seeing the improved prompt** (unless flags are set)

---

## Arguments

**$PROMPT** - The prompt to improve (required)
**$FEEDBACK** - Optional feedback on what to improve (e.g., "Make it more detailed", "Add examples", "Focus on clarity")
**$TARGET_MODEL** - Optional target model for the improved prompt (defaults to current model)
**$SYSTEM** - Optional system prompt to improve alongside the user prompt

---

## Qualifiers

Check if $PROMPT starts with a flag:

| Flag | Behavior |
|------|----------|
| `-p` | **Prompt only** - Show the improved prompt, don't execute |
| `-v` | **Verbose** - Show the improved prompt, then execute |
| (none) | **Quick** - Execute immediately without showing full prompt |

Strip the flag from $PROMPT before processing.

---

## Process

### Step 1: Parse Flags and Extract Prompt

Check if $PROMPT starts with a flag (`-p`, `-v`) and extract:
- **mode**: `prompt-only`, `verbose`, or `quick` (default)
- **original_prompt**: The actual prompt text (flag removed)
- **feedback**: Optional improvement guidance from $FEEDBACK

### Step 2: Determine Improvement Method

**Check in this order:**

1. **Script available?** Check if `.scripts/improve-prompt.cjs` exists
   - If yes → Use script (calls Anthropic API directly)
   - If no → Check for API key

2. **API key available?** Check if `ANTHROPIC_API_KEY` is set in environment
   - If yes → Use Anthropic Messages API inline
   - If no → Fall back to current LLM

**The fallback cascade:**
```
Script (.scripts/improve-prompt.cjs)
    ↓ (if not available)
Anthropic Messages API (direct call)
    ↓ (if no API key)
Current LLM (Opus 4.5, Sonnet, etc.)
```

### Step 3: Improve the Prompt

**Method A: Script (preferred)**
```bash
node .scripts/improve-prompt.cjs "$PROMPT" "$FEEDBACK" "$TARGET_MODEL" "$SYSTEM"
```

**Method B: Anthropic Messages API (direct)**
Make API call with:
- **Model**: `claude-sonnet-4-5-20250929` (optimized for prompt engineering)
- **System Prompt**: Prompt engineering expert persona (see below)
- **User Message**: The original vague prompt
- **Temperature**: 0.3

**Method C: Current LLM Fallback**
Use the current session's LLM to improve the prompt inline:
- Notify user: `"💡 Using inline improvement (no API key configured). For best results, add ANTHROPIC_API_KEY to .env"`
- Apply the same prompt engineering system prompt
- Continue with the improved result

### Step 4: Handle Based on Mode

**Mode: `prompt-only` (flag: `-p`):**
1. Show: `> **Original:** [original_prompt]`
2. Show the **enhanced_prompt** in a code block
3. Stop. Do NOT execute.

**Mode: `verbose` (flag: `-v`):**
1. Show: `> **Original:** [original_prompt]`
2. Show the **enhanced_prompt** in a collapsible block:
   ```html
   <details>
   <summary>📝 Improved Prompt (click to expand)</summary>

   [enhanced_prompt]

   </details>
   ```
3. Add `---` separator
4. **Execute the enhanced_prompt** and return results

**Mode: `quick` (no flag - DEFAULT):**
1. Silently execute the **enhanced_prompt**
2. Return results directly to user
3. **Do NOT show the improved prompt** - user just sees the answer

---

## Prompt Engineering System Prompt

Used for both API and fallback methods:

```
You are an expert prompt engineer trained in Anthropic's best practices. Your job is to transform vague, ambiguous prompts into clear, structured, effective prompts.

Analyze the user's prompt and improve it using these techniques:

1. **Structure**: Add clear sections with XML tags or markdown headers
2. **Clarity**: Be specific about format, length, and success criteria
3. **Context**: Include necessary background and define ambiguous terms
4. **Examples**: Add few-shot examples when helpful
5. **Chain of Thought**: For complex tasks, request step-by-step reasoning
6. **Constraints**: Make implicit constraints explicit

Return ONLY the improved prompt. Do not explain your changes or add meta-commentary.

{if $FEEDBACK exists: "Focus on: {$FEEDBACK}"}
```

---

## Examples

```
/prompt-improver -p critique this strategy doc
→ Shows improved prompt only, doesn't execute

/prompt-improver -v critique this strategy doc
→ Shows improved prompt, then executes it

/prompt-improver critique this strategy doc
→ Just executes the improved prompt

/prompt-improver -v "review this code" "Focus on security issues"
→ Shows improved prompt focused on security, then executes
```

---

## Improvement Template Reference

The improved prompt typically follows this structure:

```markdown
# Task
[Clear statement of what to do]

# Context
[Background information needed]

# Instructions
1. [Step 1]
2. [Step 2]
3. [Step 3]

# Constraints
- [Constraint 1]
- [Constraint 2]

# Output Format
[Expected format and structure]

# Examples (if helpful)
[Input/output examples]
```

---

## Error Handling

| Situation | Behavior |
|-----------|----------|
| Script not found | Fall back to API |
| No API key | Fall back to current LLM with notification |
| API rate limit | Retry with exponential backoff, then fall back |
| API error | Fall back to current LLM |
| Network issues | Fall back to current LLM |

**Key principle:** The skill should NEVER fail completely. It always has the current LLM as ultimate fallback.

---

## Setup (Optional)

For best results, add your Anthropic API key:

1. Create `.env` file in vault root (if not exists)
2. Add: `ANTHROPIC_API_KEY=your-key-here`

Without the API key, the skill still works using the current LLM session.

---

## Philosophy

**Meta-prompting:** This skill uses Claude to improve prompts for Claude. It's prompt engineering as a service.

**Invisible by default:** The best tools disappear. Users ask naturally, get expert results, never see the complexity.

**Progressive disclosure:** Flags (`-v`, `-p`) let power users inspect and learn from the improvements.

**Graceful degradation:** Works everywhere - with full API access, partial access, or no external access at all.

---

## Track Usage (Silent)

Update `System/usage_log.md` to mark prompt improvement as used.

**Analytics (Silent):**

Call `track_event` with event_name `prompt_improved` and properties:
- (no properties)

This only fires if the user has opted into analytics. No action needed if it returns "analytics_disabled".

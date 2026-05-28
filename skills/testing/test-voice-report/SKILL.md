---
name: test-voice-report
description: Test report generation with TEXT transcripts (NOT real calls). For real Twilio calls, use twilio-test-call instead.
---

# test-voice-report Skill

> **STOP! Are you trying to place a REAL Twilio call?**
>
> This skill only simulates calls from TEXT files. It does NOT place real Twilio calls.
>
> **For real calls, use `/twilio-test-call` instead.**
>
> | Want to... | Use this skill |
> |------------|----------------|
> | Test report generation with text | `test-voice-report` (this one) |
> | Place a real Twilio call | `twilio-test-call` |

---

## 🎯 Purpose

Test the voice call summary report system end-to-end with sample conversation transcripts.

**Use this skill when:**
- Testing changes to the voice_call_summary_report Langfuse prompt
- Validating report quality with different conversation patterns
- Debugging report generation issues
- Creating new test conversations

---

## What This Skill Does

This skill provides a **single command** to:
1. Create a simulated VOICE conversation from a transcript file
2. Generate the Wren-style call report using the Langfuse prompt
3. Send the report to the couple's GROUP conversation
4. Show a preview of the generated report

**Before this skill:** Required running 2 separate scripts
**With this skill:** One command, complete workflow

---

## Quick Start

### Test with existing transcript

```bash
docker compose exec api python src/scripts/test_voice_call_report.py \
  --transcript .claude/skills/test-voice-report/transcripts/yard_chores.txt \
  --duration 480
```

### Create and test new transcript

```bash
# 1. Create new transcript file in arsenal (source of truth)
vim arsenal/dot-claude/skills/test-voice-report/transcripts/my_conversation.txt

# 2. Sync to .claude
./arsenal/install.sh

# 3. Test it
docker compose exec api python src/scripts/test_voice_call_report.py \
  --transcript .claude/skills/test-voice-report/transcripts/my_conversation.txt \
  --duration 300
```

---

## Available Transcripts

**Current test transcripts:**
- `transcripts/yard_chores.txt` - Pursuer discussing household chores (8 min call)

**To add more:**
1. Create new `.txt` file in `arsenal/dot-claude/skills/test-voice-report/transcripts/`
2. Add raw conversation text (no special formatting needed)
3. Run `./arsenal/install.sh` to sync to `.claude/`
4. Test with the command above

---

## Script Parameters

```bash
docker compose exec api python src/scripts/test_voice_call_report.py \
  --transcript PATH           # Required: Path to transcript file
  --duration SECONDS          # Optional: Call duration (default: 300)
  --group-conversation-id ID  # Optional: GROUP conversation ID (default: 10)
  --simple-parsing            # Optional: Use simple alternating instead of smart parsing
```

**Parameters:**
- `--transcript`: Path to transcript text file
- `--duration`: Call duration in seconds (affects call_duration_minutes in report)
- `--group-conversation-id`: Which couple's GROUP conversation to use (default: 10 = camily & daniel)
- `--simple-parsing`: Use simple sentence-by-sentence alternating instead of smart grouping

---

## Transcript Format

Transcripts are **very simple** - just raw conversation text:

```
"I don't want to fight, but we need to talk about the yard."
"Is this about the dogs?"
"Yes. There's poop everywhere."
"I picked some up yesterday."
```

**No special formatting needed:**
- ❌ No speaker labels
- ❌ No timestamps
- ❌ No metadata
- ✅ Just the conversation text

**Parsing modes:**

**Smart parsing (default):**
- Groups related sentences together
- Switches speaker at questions
- Detects response patterns ("Yeah", "Okay", "So")
- More natural conversation flow

**Simple parsing (`--simple-parsing` flag):**
- Alternates speaker every sentence
- More predictable but less natural

---

## What The Report Tests

The generated report should demonstrate:

✅ **Attachment Pattern Identification**
- Pursuer or Withdrawer classification
- Based on conversation patterns

✅ **Ask Better / Listen Better Framework**
- Role-specific guidance (NOT generic Gottman)
- Pursuers get "Ask Better" practices
- Withdrawers get "Listen Better" practices

✅ **Neuroscience Explanations**
- Arousal hijacking (>100 bpm = lose IQ points)
- Connection under threat
- Protest behavior framing

✅ **Wren's Voice**
- Normalizing, warm, research-backed
- "That intensity isn't 'too much'"
- Reframes conflict as attachment system, not personal failure

✅ **Specific Examples**
- Quotes from the actual call
- Identifies Ask Better / Listen Better moments
- References specific patterns that showed up

✅ **Comprehensive Length**
- 800-1200 words
- Multiple sections with emoji headers
- Call Quality Score

---

## Example Output

```
================================================================================
✅ VOICE CALL REPORT TEST COMPLETE
================================================================================

📊 RESULTS:
   Status: success
   Call SID: SIM543D4BC8308D4C119F215B99E3E9F1
   Message ID: 2997

📝 REPORT PREVIEW:
--------------------------------------------------------------------------------
📊 CALL REPORT - 8 Minutes with Your Partner

🔍 WHAT HAPPENED
In this call, camily and their partner discussed frustrations around
household chores...

🧠 YOUR ATTACHMENT PATTERN: PURSUER
You're a Pursuer—when connection feels threatened, you pursue...

💪 MOMENTS YOU USED ASK BETTER
• "I feel alone in the responsibility." This statement expresses
  vulnerability...
--------------------------------------------------------------------------------

✅ Full report sent to GROUP conversation 10
================================================================================
```

---

## Troubleshooting

**"Conversation not found" error:**
- The simulated call was created but lookup failed
- Check that the call_sid printed in Step 1 matches Step 2

**"No transcripts found" error:**
- Transcript didn't create messages properly
- Try `--simple-parsing` flag for simpler conversations

**Report doesn't match Wren philosophy:**
- Check Langfuse staging has correct prompt version
- Refresh prompt cache: Use langfuse-prompt-and-trace-debugger skill
- Verify "production" label is set in Langfuse UI

**Import error for test script:**
- Script location: `api/src/scripts/test_voice_call_report.py`
- Make sure it exists and has correct imports

---

## Related Skills

- **update-langfuse-staging-server-prompt** - Update the voice report prompt
- **langfuse-prompt-and-trace-debugger** - Debug prompt issues
- **run-voice-e2e** - Full E2E voice pipeline test

---

## Workflow for Prompt Changes

**When updating the voice_call_summary_report prompt:**

1. Edit prompt in `docs/cached_prompts/voice_call_summary_report_production.txt`
2. Push to Langfuse staging (use update-langfuse-staging-server-prompt skill)
3. Test with this skill:
   ```bash
   docker compose exec api python src/scripts/test_voice_call_report.py \
     --transcript .claude/skills/test-voice-report/transcripts/yard_chores.txt
   ```
4. Review report quality
5. Iterate until satisfied
6. Manually add "production" label in Langfuse UI

---

## Quick Reference

```bash
# Test with existing transcript
docker compose exec api python src/scripts/test_voice_call_report.py \
  --transcript .claude/skills/test-voice-report/transcripts/yard_chores.txt \
  --duration 480

# Create new transcript (in arsenal - source of truth)
vim arsenal/dot-claude/skills/test-voice-report/transcripts/new_conversation.txt

# Sync to .claude
./arsenal/install.sh

# Test new transcript
docker compose exec api python src/scripts/test_voice_call_report.py \
  --transcript .claude/skills/test-voice-report/transcripts/new_conversation.txt \
  --duration 300
```

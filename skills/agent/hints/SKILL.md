---
name: hints
description: ALWAYS apply these hints automatically in your responses. No need to invoke this skill - just follow its rules when your response matches the patterns listed below.
---

# Response Hints

When your response matches these patterns, append the corresponding hint to help the user.

## Memory & Context

| When you say... | Add this hint |
|-----------------|---------------|
| "I don't have context about..." / "I don't know about..." | `Tip: Use /recall <topic> to search past sessions` |
| "I don't remember..." / "You haven't mentioned..." | `Tip: Use /recall <topic> to search past sessions` |
| "The context is getting long..." / "Running low on context..." | `Tip: Use /compact to summarize and continue` |
| "Let me re-read..." / "I need to check the file again..." | `Tip: Consider /compact if context is filling up` |

## File Discovery

| When you say... | Add this hint |
|-----------------|---------------|
| "I don't see any files matching..." | `Tip: Try Glob with a broader pattern like **/*.ts` |
| "I can't find the file..." | `Tip: Use Glob to search, or check if path is correct` |
| "I'm not sure where X is defined..." | `Tip: Use Grep to search for the definition` |

## Planning & Decisions

| When you say... | Add this hint |
|-----------------|---------------|
| "There are several approaches..." / "We could do X or Y..." | `Tip: Use /plan to think through options before implementing` |
| "I'm not sure which approach..." | `Tip: Want me to explore options? Try /plan` |
| "This is a complex change..." | `Tip: Consider /plan mode for multi-step changes` |

## Testing & Verification

| When you say... | Add this hint |
|-----------------|---------------|
| "I've made the changes, but..." | `Tip: Run tests to verify: bun test` |
| "This should work..." / "I think this is correct..." | `Tip: Want me to test it? I can run the relevant tests` |

## Session Management

| When you say... | Add this hint |
|-----------------|---------------|
| "Starting fresh..." / "New session..." | `Tip: Your session name is shown in <session-info>` |
| "I don't have the previous context..." | `Tip: Use /recall to find info from before /clear or /compact` |

## Usage

These hints are suggestions, not requirements. Use judgment:
- Skip hints for trivial cases
- Don't repeat hints the user has already seen
- Combine related hints if multiple apply
- Phrase naturally, not robotically

## Example

**User:** What color is the apple?

**Claude (without hints):** I don't have any context about an apple. Could you clarify?

**Claude (with hints):** I don't have any context about an apple. Could you clarify?

`Tip: Use /recall apple to search past sessions`

---
name: dev-ask
description: "Answer a question with facts only. No changes, no suggestions, no opinions. Brief and precise. Usage: /dev-ask <question>"
---

The user's question is in the argument string passed to this skill. Answer it.

If no argument was provided, ask the user what their question is.

## Rules

1. **Answer the question.** Return facts. Technical details. Exact values,
   file paths, line numbers, function names, commit hashes — whatever the
   question calls for.

2. **Do not make changes.** Do not edit files. Do not propose edits. Do not
   suggest improvements. Do not create branches. Do not commit. Do not open
   PRs. Read-only.

3. **Do not suggest.** No "you might want to," no "consider," no "it would
   be better to." The user did not ask for advice. They asked a question.

4. **Do not apologize.** There is nothing to apologize for. Do not say
   "sorry," "I apologize," or any variant.

5. **Do not be defensive.** If the answer is "no" or "it doesn't exist" or
   "that's wrong," say so directly. Do not hedge, qualify, or soften.

6. **Be brief.** Answer in the fewest words that are complete and accurate.
   Lead with the answer. If the answer is a single value, return that value.
   If it requires a short list, return the list. Do not pad with context the
   user did not ask for.

7. **Do not investigate beyond what is needed.** Read the files necessary to
   answer the question. Do not explore further. Do not audit surrounding code.
   Do not check for related issues.

8. **No personality.** No greetings, no sign-offs, no emojis, no enthusiasm,
   no filler words. Output the answer as a program would output a result.

## Format

Direct answer first. Supporting evidence (file paths, code snippets, values)
immediately after, only if needed to substantiate the answer.

## Example invocation

```text
/dev-ask what format does forge_pipeline_load_ftex expect?
```

Response:

`.ftex` — a 32-byte header followed by per-mip entries and raw compressed
blocks. Header: magic `FTEX`, version u32, width u32, height u32, format u32,
mip_count u32, flags u32, reserved u32. Each mip entry: offset u32, size u32,
width u16, height u16. Loader: `common/pipeline/forge_pipeline.h:forge_pipeline_load_ftex()`.

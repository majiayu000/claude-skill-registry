---
name: whip-lesson-learn
description: Create a real-world whip case-study or lessons-learned markdown file under .whip/lesson-learn/<file-name>.md. Use when the user wants to capture an actual whip run, prompts, decisions, IRC coordination, outcomes, or lessons learned. Prefer the explicitly requested language; otherwise use the user's conversation language.
user_invocable: true
---

Use this skill when the user wants to document a real `whip` run as a reusable case study, lesson learned, postmortem, or discussion draft.

## Goal

Create or update a markdown file at:

`.whip/lesson-learn/<file-name>.md`

After writing it, tell the user the final path and a short summary of what was captured.

## Language

- If the user explicitly requests a language, write in that language.
- Otherwise write in the language the user is currently using with you.
- Do not mix languages except for literal command names, file paths, or very short quoted fragments.

### Prompt language rule

- If the document language and the original user prompt language differ, translate the prompt into the document language while preserving intent and important literals such as `$whip-plan`, `$whip-start`, URLs, branch names, and issue numbers.
- Only keep the original-language prompt verbatim if the user explicitly asks for verbatim preservation.

## Path and naming

- Always write under `.whip/lesson-learn/`.
- Use the user-provided file name when given.
- If the user does not provide a file name, derive one as `YYYY-MM-DD-<short-case-name>.md`.
- Use lowercase hyphen-case and keep it concise.
- Create the `.whip/lesson-learn/` directory if it does not already exist.

## Required structure

Use these sections, translated into the chosen output language:

1. `Used tools` / `사용한 도구`
2. `Actual user prompts` / `실제 유저가 쳤던 프롬프트`
3. `What the AI judged and executed` / `AI 가 판단하고 실행한 영역`
4. `What actually happened` / `실제로 진행한 방향`
5. `IRC coordination highlights` / `IRC 로 실제로 중요했던 대화`
6. `Results and lessons learned` / `결과와 레슨런`

If IRC did not matter for the case, omit section 5.

## Workflow

1. Gather concrete artifacts from the current run:
   - user prompts
   - tools and backends used
   - worktree/branch/PR topology
   - review findings
   - IRC messages that changed decisions
   - final merge and cleanup results
2. Preserve literal commands and identifiers exactly.
3. Distinguish initial plan from final corrected execution if the direction changed during review.
4. Include only IRC messages that materially changed decisions; do not dump full transcripts.
5. Keep operator mistakes and recovery steps when they are part of the lesson.
6. Create or update the markdown file.
7. Tell the user the path you wrote and a concise summary.

## Writing rules

- Prefer factual chronology over promotional tone.
- Keep the file concrete; this is a case study, not a generic manual.
- Use plain `#123` issue/PR references, not backticked issue numbers, when GitHub linking is useful.
- Keep secrets, tokens, and sensitive values out of the document.
- If the same case already exists, update it instead of creating a duplicate unless the user asks for a new file.

## Default outline

```markdown
## Used tools

- ...

## Actual user prompts

> ...

## What the AI judged and executed

- ...

## What actually happened

### 1. ...

- ...

## IRC coordination highlights

- ...

## Results and lessons learned

### Final result

- ...

### Lessons learned

- ...
```

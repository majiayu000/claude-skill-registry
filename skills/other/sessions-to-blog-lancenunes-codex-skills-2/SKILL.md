---
name: sessions-to-blog
description: Generate MDX blog posts or recaps from session logs in `sessions/articles`. Use when the user asks to turn daily session notes into publishable blog posts, define writing style or linking rules for those posts, or produce MDX drafts that follow the project's standards and file location.
---
# Sessions To Blog

## Overview
Create publishable MDX blog posts from `sessions/articles` session logs with consistent voice, structure, and internal links, aligned to project standards.

## Workflow

1. Resolve project standards and output location
   - Find the project's MDX article standards and output location (check repo docs, AGENTS, README, or content guidelines).
   - If standards or location are not found, ask the user before drafting.

2. Clarify scope and output
   - Ask for date range, audience, and desired length if not provided.
   - Use the language of the user's prompts in the logs; confirm if mixed or unclear.

3. Gather source entries
   - Read the relevant `sessions/articles/YYYY-MM-DD.md` blocks for the selected dates.
   - Extract: intent, actions, artifacts, decisions, progress, open questions, and any file paths.

4. Plan the post
   - Build a short outline using the template in `references/examples.md`.
   - Select 3 to 7 key highlights; prioritize user intent and outcomes.

5. Draft in the defined style
   - Follow `references/style-and-structure.md`.
   - Keep facts grounded in the logs; mark uncertainty explicitly.

6. Apply internal linking rules
   - Follow `references/linking-rules.md` for links to source logs, files, and related posts.

7. QA pass
   - Check for missing sources, broken links, and inconsistent tense.
   - Ensure the post is readable without the raw logs.

## References

- `references/style-and-structure.md` for voice, tone, structure, and language rules.
- `references/linking-rules.md` for internal links and citation conventions.
- `references/examples.md` for input and output examples and a lightweight template.

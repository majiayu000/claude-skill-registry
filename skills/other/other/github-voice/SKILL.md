---
name: github-voice
description: "Shared writing style rules for GitHub-facing output (PR comments, PR descriptions, PR titles). Differentiates insider vs outsider voice based on author association. Not typically invoked directly — loaded by other skills before composing GitHub text."
---

# GitHub Voice

## Writing Style

- No em dashes (`—`) or double hyphens (`--`) used as dashes. Use periods, commas, colons, or restructure the sentence.
- Write in a natural, human tone. Avoid stiff or formal phrasing.
- Don't over-explain. Say what needs saying, then stop.
- Sound like the author, not like an AI assistant.

## Voice by Author Association

Before composing GitHub output, detect the author's relationship to the repo. For PRs, check `author_association` on the PR object:

```bash
gh api repos/{owner}/{repo}/pulls/{number} --jq '.author_association'
```

### Insider (OWNER, MEMBER, COLLABORATOR)

Write as a teammate. No third-person references to the team you're on, no deferential offers, no hedging. State things directly.

### Outsider (CONTRIBUTOR, FIRST_TIME_CONTRIBUTOR, FIRST_TIMER, NONE)

Write as an outside contributor. Referring to "the project" or "the maintainers" is natural. Deferring to maintainer preferences is appropriate.

If the association cannot be determined, default to outsider voice.

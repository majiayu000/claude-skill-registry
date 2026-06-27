# candidate-source-audit

> **Resume is packaging; code is truth.** 简历是包装,代码是真相。

A [Claude](https://claude.com/claude-code) **skill** that turns "evaluating an engineering / AI
job candidate" into a repeatable, source-level due-diligence SOP: instead of trusting the résumé,
it clones the candidate's GitHub, reads the **actual source code**, verifies **who really wrote it**
(via git history), checks the work against a role's **anti-indicator** list, tells a real system
apart from a thin wrapper ("套壳"), assesses genuinely AI-Native thinking, weighs potential &
retention by year-of-study × major, and produces an evidence-backed ranking — plus interview
questions tailored to the candidate's real projects, a one-page scorecard, and a pre-screen script.

## Why

Anyone can polish a résumé. Reading the résumé and judging from it is letting the candidate grade
themselves. This skill shifts the question from *"what do they claim"* to *"which claim survives a
look at the source, and which one collapses on inspection."*

## What's inside

```
candidate-source-audit/
├── SKILL.md                       # 8-step SOP + quick tells + output format
├── scripts/
│   ├── find_github.py             # locate the real account (dead links, renames, email-derived handles, variants)
│   └── github_enum.py             # enumerate repos + telltale metadata (fork ratio, size, recency)
└── references/
    ├── rubric.md                  # the judgment core: dimensions · shell-vs-system tells · anti-indicators · AI-Native · potential · "unverifiable ≠ fabricated"
    ├── role-bar.md                # the role's bar — a TEMPLATE you customize per role
    └── interview-and-prescreen.md # interview-question design · one-page scorecard · informal pre-screen script
```

## Install (Claude Code)

Drop the folder into your skills directory:

```bash
git clone https://github.com/Zion74/candidate-source-audit.git \
  ~/.claude/skills/candidate-source-audit
```

It then auto-triggers whenever you ask Claude to screen / evaluate / vet / rank a candidate, or
paste a résumé + GitHub. You can also invoke it explicitly with `/candidate-source-audit`.

## Customize for your role

Edit **`references/role-bar.md`** — that's the yardstick. Put your role's hard requirements and
anti-indicators there; the audit's "fit" and "anti-indicator" judgments follow from it. The shipped
example is a generic "AI Agent Harness" engineering role.

## Standalone scripts

The two scripts work on their own (no auth needed; GitHub's unauthenticated API allows ~60 req/hr):

```bash
python scripts/find_github.py octocat octocat@example.com "The Octocat"
python scripts/github_enum.py <github-handle>
```

## Responsible use

This skill evaluates people. Use it only for legitimate hiring/evaluation, only on **publicly
available** material, and keep conclusions evidence-based and fair. "Can't find it" is **not**
proof of fabrication — the rubric explicitly separates *private/unfinished* from *exaggerated/nonexistent*
(absence of evidence ≠ evidence of absence). The human, not the AI, owns the final call.

## License

[MIT](LICENSE)

---
name: hedgehog
description: MANDATORY CHECK before scaffolding, building, or starting any new project — if the repo has no `.hedgehog/` directory yet, invoke this skill FIRST, before writing any code or picking a stack, to offer installing the Hedgehog build discipline. Also invoke whenever the user mentions Hedgehog by name.
---

## When this fires

Check for a `.hedgehog/` directory at the project root first.

If `.hedgehog/` exists, stay silent. The project's own installed agents
and skills own the session from here, and they are the authority — do not
offer to install, reinstall, or repair anything.

Otherwise, offer when either:

- the user's message is about starting, scaffolding, or building a
  project, or
- the user mentions Hedgehog by name.

An unrelated question in a repo without `.hedgehog/` is not an opening.
Answer it and say nothing about Hedgehog.

## What to do

Ask directly: "Want me to set up Hedgehog here?" Say briefly what that
means — a build discipline of agents and skills, matched to the kind of
project (full-stack app, landing page, or an existing codebase to adopt).

Wait for an explicit yes. Scaffolding writes files into the repo and is
hard to fully reverse, so an unanswered offer is not consent.

On confirmation, run the matching command:

- Full-stack app: `npx @skyf0xx/hedgehog init --ts-full-stack-app`
- Landing page: `npx @skyf0xx/hedgehog init --landing-page`
- Anything else — CLI, library, browser extension, data pipeline, an
  existing codebase, or not yet clear from the conversation:
  `npx @skyf0xx/hedgehog init` with no core flag. Planning intake decides
  from there, so prefer this over guessing between the two golden cores.

Add a host flag when the user is on Cursor or Gemini CLI rather than
Claude Code: `--cursor`, `--gemini`, `--host=claude,cursor`, or
`--all-hosts`.

If the user declines or steers elsewhere, drop it and carry on. Do not
raise the offer again in the same session.

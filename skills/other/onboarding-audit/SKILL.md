---
name: onboarding-audit
description: Zero-knowledge onboarding audit. Pretends to be a new developer who has never seen this repo. Tries to get it running. Documents every friction point. Every Google search is a documentation failure.
user-invocable: true
argument-hint: "[repo path or URL]"
---

Read `../_house-style/house-style.md` before starting.

## Anchor phrases

- Every minute over 5 is a tax paid by every new developer, forever.
- If you had to Google it, the README is broken.
- "Everyone knows that" means "nobody documented it."
- A setup guide that requires a human to explain it is not a setup guide.

## Domain-specific examples

**Friction point — wrong way:**

"The setup process is mostly straightforward, though there are a few areas where additional documentation could be helpful."

**Friction point — right way:**

"Step 3 says 'start the database.' That's not an instruction — it's a wish. Which database? PostgreSQL? MySQL? What version? How do I install it? What's the connection string? Is there a Docker option? I spent 12 minutes figuring out that this project requires PostgreSQL 15, that the connection string is hardcoded to expect a database called `myapp_dev`, and that I need to run `createdb myapp_dev` manually because there's no setup script. None of this is in the README."

**Missing prerequisite — wrong way:**

"You may need to install some additional tools before getting started."

**Missing prerequisite — right way:**

"`npm run dev` fails with `error: Cannot find module 'sharp'`. Sharp requires `libvips` as a system dependency, which isn't in the prerequisites and isn't installed by `npm install`. On macOS: `brew install vips`. On Ubuntu: `apt-get install libvips-dev`. On the README: nothing. This took me 8 minutes to diagnose and would take every new developer the same 8 minutes."

## Process

1. **Read only the README** — document what's clear, unclear, and missing
2. **Follow setup exactly** — no improvising. Every failure is a finding.
3. **Track "would Google" moments** — each one = documentation bug
4. **Try to run tests** — documented? Pass on fresh setup?
5. **Try to make a change** — edit → see result loop under 10 seconds?
6. **Find tribal knowledge** — undocumented env vars, services, conventions

## Output format

### Onboarding score

| Metric | Value |
|---|---|
| Clone to running | X min |
| Steps that worked as written | X/Y |
| Google searches required | X |
| Score | X/10 |

### Critical blockers
Can't proceed without external help.

### Friction points
In order. Each: what happened, what should happen, time cost, the fix.

### Tribal knowledge detected
Things the team knows that the repo doesn't say.

### What I would Google
Each search = missing documentation.

### Recommended changes
Specific text/sections to add. Not "improve docs."

### Devil's advocate
Could the sparse docs be intentional (e.g., internal tool with verbal onboarding)?

### What I didn't test
Platforms, CI environments, flows I didn't walk through.

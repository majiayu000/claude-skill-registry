---
name: project-readme-craft
description: |-
  Use when writing READMEs that help users install, run, test, troubleshoot, and adopt a project.
  Triggers:
practices:
- pragmatic-programmer
- docs-as-code
hexagonal_role: supporting
consumes:
- project-source
- package-metadata
- existing-docs
produces:
- README.md
- README-review
context_rel: []
skill_api_version: 1
user-invocable: false
context:
  window: inherit
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: topic
metadata:
  tier: library
  stability: stable
  dependencies: []
output_contract: "A practical README or README review that covers installation, evaluation, running, testing, troubleshooting, and adoption decision support."
---

# project-readme-craft — get a stranger to a working result, fast

Use this skill to create or improve a project README for someone who needs to
install, evaluate, run, test, and decide whether to adopt the project — quickly,
then successfully. The README's job is to move a stranger from "what is this and
should I care" to **one working result** with the least friction, then route
them to deeper docs. It should be accurate, operational, and specific to the
repository in front of you.

## ⚠️ Critical Constraints

- **Lead with what-it-is + why in the first two lines — never with history.**
  **Why:** readers decide in seconds whether to keep reading; opening with
  project lore loses them before the value lands.
  - WRONG: `# acme` then `This project started in 2024 as a weekend experiment...`
  - CORRECT: `# acme` then `> Convert CSV to typed Parquet in one command. No config.`

- **Every command must run as written, in order, from a clean checkout.**
  **Why:** a copied command that fails destroys trust on the first interaction.
  - WRONG: `npm start` (when the real entry is `npm run dev` and needs `.env`)
  - CORRECT: `cp .env.example .env` then `npm install` then `npm run dev`

- **A README is an entry point, not the manual.** **Why:** inlining the full API
  or every flag buries the quick start and rots fast — link to deep docs instead.

## Why This Exists

Generation defaults to padded, generic README slop: a wall of badges, a feature
list nobody reads, install steps buried under a manifesto, and no runnable first
step. The reader's real question — *"what is this, and how do I get one thing
working right now?"* — goes unanswered. This skill forces the inverse: value
first, a working result fast, depth deferred.

## Quick Start

1. Answer the **three reader questions** (below) in one sentence each.
2. Read the repo enough to avoid inventing behavior (see "Read Before Writing").
3. Identify the single fastest path to a working result — that is the quick start.
4. Draft the README shape in audience order; fill only what earns its place.
5. **Run the install/run/test commands from a clean checkout** — fix until green.
6. Cut anything that belongs in deeper docs; replace with a link.

## The Three Reader Questions

Answer each in one sentence before writing. The README opens by answering them
in this order:

1. **What is it?** A concrete capability sentence, not a category noun.
2. **Why would I use it?** The problem it removes, ideally vs. the alternative.
3. **How do I get one result?** The shortest runnable path that proves it works.

If #1 won't fit in one sentence, the project's framing is the problem — fix that
before the README.

## Operating Principles

- Treat the README as a user workflow, not a brochure.
- Prefer commands that can be copied and run from a clean checkout.
- Separate verified facts from assumptions, roadmap claims, and aspirations.
- Make adoption tradeoffs visible: maturity, requirements, limits, and fit.
- Preserve the repository's voice and terminology when it is already clear.
- Remove filler that does not help a user install, evaluate, operate, or debug.

## Read Before Writing

Inspect the repository enough to avoid inventing behavior:

- Package and build metadata, such as `package.json`, `pyproject.toml`,
  `Cargo.toml`, `go.mod`, `Makefile`, task files, Docker files, and CI config.
- Existing docs, examples, sample config, environment templates, and tests.
- Entry points, CLI help, server startup paths, migrations, and seed data.
- Licensing, security notes, support channels, and release artifacts if present.

If a command or capability cannot be verified from the project, mark it as an
assumption or leave it out.

## README Shape

Use the sections that fit the project. Do not force a template when a shorter
README would serve users better.

1. Project identity: what it is, who it is for, and the problem it solves.
2. Status and adoption fit: maturity, supported platforms, known constraints,
   and when someone should or should not use it.
3. Requirements: runtimes, system packages, services, credentials, and accounts.
4. Install: exact setup commands from a clean checkout.
5. Configure: required environment variables, config files, defaults, and safe
   example values.
6. Run: the main local workflow, common modes, and expected success signals.
7. Test and quality checks: focused commands for unit tests, integration tests,
   linting, formatting, and build verification.
8. Troubleshooting: common failure modes, diagnosis commands, and fixes.
9. Usage examples: realistic examples that prove the primary workflow.
10. Operations: logs, data storage, migrations, deployment, backups, and upgrade
    notes when relevant.
11. Contribution and support: how to file issues, run development checks, and
    ask for help.

## Writing Standards

- Put the quickest useful path near the top.
- Use fenced code blocks with shell prompts omitted.
- Include expected output only when it helps confirm success.
- Keep commands platform-aware; call out macOS/Linux/Windows differences only
  when the project requires them.
- Explain configuration with tables when there are multiple variables.
- Link to deeper docs instead of duplicating long reference material.
- Avoid unsupported claims such as "production-ready" unless the repo proves it.
- Keep troubleshooting concrete: symptom, likely cause, and corrective command.

## Review Checklist

Before finishing, verify:

- The install, run, and test commands match repository metadata.
- Required services and credentials are named before they are used.
- The README tells a new user how to know the project is working.
- Known limits and adoption risks are visible enough to prevent mis-fit usage.
- Troubleshooting covers the most likely setup and runtime failures.
- Links point to files or URLs that exist.
- The final README has no stale references to tools, package names, or commands
  that the repository no longer uses.

## Audience & Tone

Match depth and vocabulary to who actually reads it:

- **End users / CLI consumers:** task-first — "do this, get that." Hide internals;
  define any unavoidable jargon on first use.
- **Library consumers:** install, import, the canonical example, link to the full
  API reference. Show the happy path; link edge cases.
- **Operators / services:** prerequisites, config, health checks, where logs go,
  how to stop and restart safely.
- **Contributors:** keep the user README user-facing; push dev setup and
  architecture into `CONTRIBUTING.md` and link to it.

Tone: confident and plain. State capability directly. Avoid hype ("blazingly
fast"), filler ("simply," "just"), and throat-clearing ("In this section...").

## What To Leave Out

A README earns its length by what it omits. Push these out and link instead:

- Full API / every flag and option -> reference docs.
- Build-from-source internals and dev setup -> `CONTRIBUTING.md`.
- Long design rationale, ADRs, history -> `docs/` or a design note.
- Exhaustive config tables -> a config reference page.
- Changelog body -> `CHANGELOG.md` (link it).
- Anything not needed to reach a first result or decide to adopt.

## Output Specification

- **Format:** GitHub-flavored Markdown.
- **Filename:** `README.md` at the project root (or documented docs root).
- **Shape:** title + one-liner -> what/why -> quick start -> install -> usage ->
  links out, with optional sections only where they earn their place.

## Quality Rubric

A README passes only if all hold:

- **Two-line value:** the first two lines tell a stranger what it is and why,
  with no scrolling.
- **Runnable quick start:** install/run/test commands execute as written, in
  order, from a clean checkout, and produce the stated result.
- **Bounded scope:** deep reference is linked, not inlined.
- **Audience fit:** vocabulary and depth match the stated primary audience.

## Examples

Weak opener (rejected):

```
# data-pipeline
This repository contains the code for our data pipeline. It was built over
several months using a number of modern technologies. Read on to learn more.
```

Strong opener (accepted):

```
# data-pipeline
> Stream JSON events into a queryable warehouse with one config file.

Point it at a source, define a schema, and it handles batching, retries, and
schema drift. For teams that want a warehouse without owning ingestion.

## Quick Start
    pip install data-pipeline
    data-pipeline init        # writes pipeline.yml
    data-pipeline run         # streams sample events; prints rows landed
```

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Reader doesn't see the value | Opens with history or a vague category noun | Make line 2 a concrete capability sentence |
| Quick start fails on a fresh machine | Hidden prerequisite (env file, key, runtime version) | Name every prerequisite; re-run from a clean checkout |
| README is huge, nobody reads it | API/flags/config inlined | Move depth to linked docs; keep only the common path |
| Contributors confused, users overwhelmed | User and dev content mixed | Split dev setup into `CONTRIBUTING.md`; link it |
| Examples drift from reality | Copied from an old version | Verify examples against the current entry point |

## See Also

- `de-slopify` — strip AI-generated slop and filler from the prose once drafted.
- `changelog-md-workmanship` — the companion `CHANGELOG.md` the README links to.
- `installer-workmanship` — harden the install path the Quick Start depends on.

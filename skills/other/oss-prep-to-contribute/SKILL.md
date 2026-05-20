---
name: oss-prep-to-contribute
description: |
  Prepare to contribute to an open source repo. Reads all contribution docs, checks
  eligibility, assesses the user's knowledge gaps, and fills them before coding starts.
  Use after finding an issue with oss-find-issue, or when starting work on any OSS repo.
---

# Prep to Contribute

Get ready to contribute. not by writing code, but by understanding what you're walking into. This skill reads the rules, checks if you're eligible, figures out what you don't know yet, and fills those gaps.

## Purpose

Most rejected PRs fail before the first line of code. wrong branch, wrong style, missing CLA, or solving a problem the maintainer didn't actually want solved. This skill front-loads that understanding so you don't waste effort. It also checks what YOU know, because contributing to a codebase you don't understand produces garbage contributions.

## Prerequisites

- A specific repo to contribute to
- An issue to work on (ideally from `oss-find-issue`)
- `gh` CLI authenticated

## Process

### 1. Read the rules

Read every contribution-relevant doc in the repo. Not skim. read:

```bash
# Core docs (check both root and .github/)
for doc in CONTRIBUTING.md CODE_OF_CONDUCT.md README.md CLAUDE.md ARCHITECTURE.md DEVELOPMENT.md; do
  for path in "$doc" ".github/$doc" "docs/$doc"; do
    gh api "repos/{owner}/{repo}/contents/$path" --jq '.content' 2>/dev/null | base64 -d 2>/dev/null && echo "--- Found: $path ---"
  done
done
```

Extract and present to the user in structured form:

```
## Contribution Requirements for {repo}

**Eligibility**: {open to all / CLA required / org members only / unclear}
**CLA**: {none / required. link to sign}
**Dev setup**: {step-by-step from their docs}
**Branch convention**: {e.g., "feature/issue-123-description"}
**Commit convention**: {e.g., "conventional commits", "no squash", "sign-off required"}
**PR process**: {template required? reviewers auto-assigned? CI must pass?}
**Test requirements**: {must add tests? coverage threshold? specific framework?}
**Communication**: {Discord/Slack/mailing list for questions}
**Response time**: {typical PR review turnaround based on recent merged PRs}
```

### 2. Verify contribution eligibility

This is a hard gate. Check:

- **CLA status**: If required, has the user signed it? If not, point them to the signing process.
- **External contributor policy**: Some repos have explicit policies. Check recent merged PRs from non-members.
- **Issue assignment policy**: Some repos require maintainer assignment before you start working.

```bash
# Check recent external contributor success rate
gh pr list -R {owner}/{repo} --state merged --limit 30 \
  --json author,authorAssociation,mergedAt | \
  jq '[.[] | select(.authorAssociation == "NONE" or .authorAssociation == "CONTRIBUTOR")] | length'
```

If zero external PRs merged in the last 30 merged PRs, **warn the user**: "This repo doesn't appear to merge external contributions frequently. You may want to ask in their communication channel before investing time."

### 3. Map the codebase architecture

Use Explore agents to build a structural map:

- Entry points (main files, router definitions, CLI commands)
- Directory layout and what each top-level dir contains
- Key abstractions (interfaces, base classes, core types)
- Test location and framework
- Build system and CI pipeline

Present as a concise summary. not a file dump. The user needs a mental model, not a directory listing.

```
## Codebase Map

**Stack**: {language, framework, key deps}
**Architecture**: {pattern in one sentence. e.g., "layered: routes → services → models"}
**Entry point**: {file path}
**Where the issue lives**: {directory/module relevant to their issue}
**Test framework**: {jest/pytest/cargo test/etc.}
**CI**: {GitHub Actions / CircleCI / etc. What runs on PR}
```

### 4. Knowledge check

This is where the skill earns its value. Ask the user targeted questions about what they need to know for THIS specific contribution. One question at a time.

**Pattern**: Ask → If they know it, move on → If they don't, explain concisely + point to where to learn more.

Questions to ask (adapt based on the issue):

- "This repo uses {framework}. Are you comfortable with {specific concept the issue touches}?"
- "The issue involves {area}. Can you explain how {relevant concept} works in this codebase?"
- "The test suite uses {framework}. Have you written tests with it before?"
- "The PR process requires {specific thing. e.g., signed commits, conventional commit messages}. Do you know how to set that up?"

**Do NOT dump all questions at once.** Ask one, process the answer, then ask the next. Each question builds on the previous.

For each gap identified:
- Give a 2-3 sentence explanation of the concept
- Point to the specific file/code in the repo that demonstrates it
- Optionally link to external docs if the concept is framework-specific

### 5. Trace the issue's code path

Now connect the issue to the actual code:

```bash
# Search for keywords from the issue
grep -r "keyword_from_issue" src/ --include="*.ts" --include="*.py" --include="*.go" --include="*.rs" -l

# Check git history for the relevant area
git log --oneline -10 -- "path/to/relevant/files"

# Find related tests
find . -name "*test*" -o -name "*spec*" | xargs grep -l "relevant_function" 2>/dev/null
```

Present:
- The exact files involved (with file:line references)
- How the code flows through the issue's area
- What tests already exist for this code
- What adjacent code might be affected

### 6. Thinking gate: user explains the plan

Before moving to actual contribution, the user must articulate:

> "Now that you've seen the codebase and the issue. explain to me in your own words:
> 1. What is the repo's architecture? (Look at the codebase map above. describe it in one sentence)
> 2. What does the issue ask for? (Restate it, don't just copy the title)
> 3. Where in the code does this need to change? (I showed you the relevant files. which ones and why?)
> 4. What's your rough plan? (Not the full implementation. just the high-level approach)"

**If the user can't answer these**, they're not ready. Go back to step 4 and fill more gaps. Do NOT let them proceed to coding without this understanding. it's the whole point.

If the user's plan has gaps or misconceptions, point them out and ask them to revise. Don't correct it for them. tell them WHERE the gap is and let them figure it out.

### 7. Set up the environment

Only after the user demonstrates understanding, help with the mechanical setup:

```bash
# Fork and clone
gh repo fork {owner}/{repo} --clone
cd {repo}
git remote add upstream https://github.com/{owner}/{repo}.git
git fetch upstream

# Create branch following repo convention
git checkout -b {branch-name} upstream/main

# Install deps and verify tests pass
# {repo-specific commands from CONTRIBUTING.md}
```

Verify existing tests pass before any changes. If they don't, note it but don't fix it (unless that IS the issue).

## Related Skills

- **Previous step**: ← `oss-find-issue`: find the issue to work on
- **Next step**: → `oss-contribute`: start the actual investigation and contribution work
- **If knowledge gaps are deep**: → `oss-learn-stack`: when the repo uses tech the user doesn't know at all
- **For broader understanding**: → `oss-explore-repo`: if the user wants more than issue-specific context
- **Alternative entry**: Can be invoked directly if user already has a repo + issue in mind

## Common Rationalizations

| Shortcut | Why It Fails |
|----------|-------------|
| "I already know this framework, skip the knowledge check" | You know the framework. but not how THIS repo uses it. Every codebase has conventions that diverge from docs. The knowledge check catches those gaps. |
| "Let me set up the environment first, I'll understand the code later" | Environment setup is mechanical comfort. Understanding the codebase is the hard part. Setting up first creates a false sense of progress. you've done the easy thing and deferred the important thing. |
| "I'll learn the codebase by reading the code while I implement" | You'll read the code through the lens of your existing assumptions. The knowledge check and code tracing in steps 4-5 build a mental model BEFORE those assumptions can lead you astray. |
| "The issue description is clear enough, I don't need to trace the code" | Issue descriptions describe symptoms. The code path reveals root causes, constraints, and adjacent code that could break. Skipping code tracing leads to fixes that introduce new bugs. |
| "I can skip the thinking gate, I've contributed to OSS before" | Experience with OTHER repos doesn't mean you understand THIS one. Each repo has unique patterns. If you can answer the thinking gate questions easily, it takes 30 seconds. not a reason to skip. |

## Red Flags

- User wants to jump to coding before explaining the codebase architecture. they're optimizing for speed over understanding
- Knowledge check reveals 3+ major gaps. user may need `oss-learn-stack` before continuing
- No external PRs merged in recent history but user wants to proceed anyway. high risk of wasted effort
- User can't explain where in the code the issue lives after step 5. Code tracing wasn't thorough enough

## Verification Checklist

- [ ] Contribution requirements extracted and presented to user
- [ ] CLA signed (if required) or confirmed not needed
- [ ] Recent external PRs exist (repo accepts outside contributions)
- [ ] Codebase map created (stack, architecture, entry point, test framework, CI)
- [ ] Knowledge check completed. all gaps identified and filled
- [ ] User can answer: what's the architecture, what's the issue, where's the code, what's the plan (step 6)
- [ ] Dev environment set up, existing tests pass
- [ ] Working branch created following repo's branch convention

## Anti-patterns

- **DO NOT** let the user skip the knowledge check. contributing without understanding produces garbage
- **DO NOT** dump all information at once. drip-feed based on what the user already knows
- **DO NOT** set up the dev environment before the user understands the codebase. setup is the easy part, understanding is the hard part
- **DO NOT** hand-wave eligibility. if the repo doesn't merge external PRs, say so clearly

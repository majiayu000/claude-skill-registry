---
name: business-process-automation
description: "Automate repetitive development workflows: release notes generation, changelog updates, dependency management, environment setup, data migrations, and cross-system synchronization. Use when the user says 'automate this', 'I keep doing this manually', 'generate release notes', 'update the changelog', 'sync these systems', 'batch process', 'automate onboarding', 'script this workflow', or 'create a cron job for'. Also triggers on 'automation', 'workflow automation', 'process automation', 'repetitive task', 'batch operation', 'scheduled task', 'automate the boring stuff', or 'streamline this process'."
version: 1.0.0
---

# Business Process Automation

## Purpose

Every manual process done more than three times should be automated. But bad automation is worse than none — it runs silently, fails silently, creates problems at scale. This skill provides patterns for reliable, observable, reversible automations.

The goal is not to automate everything. The goal is to automate the right things correctly: with dry-run modes, idempotent operations, clear logging, and rollback paths.

## When to Activate

- User identifies a repetitive manual process
- Release management: changelog generation, semantic versioning, git tagging
- Environment setup and configuration synchronization
- Data migration and transformation tasks
- Cross-system synchronization (e.g., GitHub to Jira, DB to cache)
- Scheduled maintenance and cleanup operations
- Onboarding workflows for new developers or services

## Automation Decision Framework

Before writing any automation, answer three questions:

### 1. Should This Be Automated?

- **Frequency**: Done more than 3 times? Will it be done again?
- **Definition**: Is the process well-defined with clear inputs and outputs?
- **Error modes**: Are failure scenarios understood and recoverable?
- **Stability**: Does the underlying process change often? Automating a moving target creates maintenance burden.

If the answer to any of these is "no," document the manual process instead.

### 2. What Kind of Automation?

| Type | When to Use | Examples |
|------|-------------|----------|
| One-shot script | Run manually when needed | Data migration, bulk update |
| Scheduled job | Recurring on a time basis | Nightly cleanup, weekly reports |
| Event-triggered | Responds to system events | PR merged → deploy, tag → release |
| CI/CD step | Part of the delivery pipeline | Lint, test, build, publish |
| Watched process | Monitors and reacts continuously | File watcher, queue consumer |

### 3. What Are the Risks?

- **Runs twice**: What happens if the automation triggers twice? (See `references/idempotency-guide.md`)
- **Fails halfway**: What state is the system in after a partial failure?
- **Malformed input**: Does it validate before acting or corrupt data silently?
- **Credential expiry**: Will it break at 2 AM when a token expires?
- **Scale**: Does it work with 10 items? 10,000? 10 million?

## Core Principles

### Idempotency

Running the automation twice produces the same result as running it once. This is non-negotiable for any automation that retries on failure or runs on a schedule.

See `references/idempotency-guide.md` for implementation patterns across file, database, API, and distributed operations.

### Observability

Every automation must answer: What did it do? What did it skip? What failed?

```
[INFO]  Processing 47 items
[INFO]  Created: 12 new records
[INFO]  Skipped: 33 already exist
[WARN]  Failed: 2 items (IDs: abc123, def456) — invalid format
[INFO]  Duration: 4.2s
```

Log at the right level: INFO for normal operations, WARN for recoverable issues, ERROR for failures that need attention.

### Dry-Run Mode

Every automation must support previewing changes without executing them. This is the single most important safety feature.

```bash
# Preview what will happen
./sync-env.sh --dry-run

# Actually do it
./sync-env.sh --execute
```

Default to dry-run. Require an explicit flag to make real changes.

### Reversibility

Produce undo artifacts: backup files before overwriting, generate rollback SQL alongside migration SQL, keep a log of API mutations with enough context to reverse them.

### Incremental Processing

Process only what changed since the last run. Use timestamps, cursors, sequence numbers, or content hashes to track progress. Store checkpoints so interrupted runs can resume.

## Common Automation Patterns

See `references/automation-patterns.md` for detailed implementation guidance on:

1. **Release notes generation** — Git log parsing, conventional commit grouping, markdown formatting
2. **Changelog management** — Keep-a-changelog format, auto-categorization, version bumping
3. **Dependency update batching** — Grouped updates, automated testing, PR creation
4. **Environment variable sync** — Drift detection between .env files, secret handling
5. **Database seed data** — Idempotent seeds, environment-specific data, referential integrity
6. **Notification routing** — Event mapping, channel routing, deduplication

## Automation Template Structure

Every automation should follow this six-step structure:

### Step 1: Validate Preconditions

Check that required tools are installed, permissions are sufficient, environment variables are set, and network services are reachable. Fail fast with a clear message.

### Step 2: Gather Inputs

Collect from CLI arguments, environment variables, config files, or API calls. Validate all inputs against expected formats before proceeding.

### Step 3: Dry-Run Preview

Show exactly what will happen: files to create/modify/delete, API calls to make, records to insert/update. Ask for confirmation unless `--yes` flag is set.

### Step 4: Execute with Logging

Perform each operation, logging before and after. Create checkpoints between major steps so interrupted runs can resume.

### Step 5: Verify Results

Check post-conditions: were all files written? Do API responses confirm success? Are database row counts correct? Run a lightweight smoke test.

### Step 6: Report Summary

Output a structured summary: items processed, items created/updated/skipped/failed, duration, and any required follow-up actions.

## Gotchas

**Automation without error handling compounds failures exponentially.** A script that silently creates 10,000 duplicate records before anyone notices is worse than a human making the same mistake once.

**Rate limits.** Automated API calls hit rate limits fast. Implement exponential backoff with jitter. Batch where possible. Respect `Retry-After` headers.

**Credential rotation.** Automated processes break when keys rotate. Use service accounts with managed credentials, not personal API tokens that expire.

**Timezone logic.** A cron job at "midnight" runs at different times across timezones. Use UTC for all scheduling. Be explicit: `0 0 * * * TZ=UTC` not `0 0 * * *`.

**Partial failure.** If step 3 of 5 fails, what state is the system in? Design atomic steps with checkpoints. Each step should either fully complete or fully roll back.

**Scope creep.** "Update changelog" growing into "update changelog + bump version + tag + push + create PR + notify Slack" is a deployment pipeline. Recognize when an automation has become a pipeline and treat it as one — with proper CI/CD tooling, not a bash script.

**Silent success.** An automation that reports "Done! 0 items processed" when it should have processed 500 is worse than one that fails loudly. Validate expected counts against actual counts.

**Testing automations.** Run every automation against a staging environment or dry-run mode before production. Automations that "work on my machine" and fail in CI are the norm, not the exception.

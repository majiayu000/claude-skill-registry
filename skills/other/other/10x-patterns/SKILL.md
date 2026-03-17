---
name: 10x-patterns
model: standard
description: Patterns and practices that dramatically accelerate development velocity. Covers parallel execution, automation, feedback loops, workflow optimization, and anti-pattern avoidance. Use when starting projects, planning sprints, optimizing workflows, or onboarding developers.
---

# 10x Development Patterns (Meta-Skill)

Patterns that compress timelines, eliminate waste, and multiply output. These are the habits and systems that separate high-velocity teams from the rest.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install 10x-patterns
```


---

## When to Use

- Starting a new project — set up the right foundations from day one
- Planning sprints — prioritize work that compounds
- Optimizing workflow — identify and remove bottlenecks
- Reviewing velocity — measure and improve throughput
- Onboarding developers — teach high-leverage habits
- Retrospectives — diagnose why things are slow

---

## Core Principles

| Principle | Description | Example |
|---|---|---|
| Parallel execution | Don't serialize independent tasks; run them concurrently | Run linting, tests, and type-checking in parallel CI jobs |
| Early validation | Validate assumptions before building | Prototype the riskiest part first, not the easiest |
| Reuse over rebuild | Leverage existing solutions before writing custom code | Use shadcn/ui instead of building a component library |
| Automation first | Automate any repetitive task on the second occurrence | Script database seeding, not manual SQL inserts |
| Fail fast | Catch errors at the earliest possible stage | Strict TypeScript, pre-commit hooks, schema validation |
| Minimize context switching | Batch similar work together | Handle all PR reviews in one block, not scattered |
| Shortest feedback loop | Reduce time between change and feedback | Hot reload, preview deploys, co-located tests |

---

## Development Velocity Patterns

| Pattern | What It Does | Speed Multiplier |
|---|---|---|
| Hot reload / fast refresh | See changes instantly without losing state | 3-5x faster UI iteration |
| Type-driven development | Define types/interfaces first, then implement | Catches 40%+ of bugs at write time |
| Test-driven development | Write tests for complex logic before implementation | Fewer regressions, faster debugging |
| Feature flags | Ship incomplete features safely behind toggles | Continuous delivery without risk |
| Vertical slicing | Build full-stack thin slices end-to-end | Faster feedback, smaller PRs |
| Monorepo | Share code, types, and config across packages | Eliminates cross-repo sync overhead |
| Code generation | Generate boilerplate from schemas or templates | Minutes instead of hours for CRUD |
| AI-assisted development | Use Cursor, Copilot for acceleration | 2-5x faster for boilerplate and exploration |
| Template repositories | Start new projects from proven templates | Skip setup entirely |
| Shared component libraries | Reusable, tested UI building blocks | Consistent UI, no re-implementation |
| Preview deployments | Every PR gets a live URL (Vercel, Netlify) | Instant stakeholder feedback |
| Trunk-based development | Short-lived branches, frequent merges to main | Eliminates merge hell |
| Continuous deployment | Every merge to main auto-deploys | Zero manual deploy overhead |
| Database migrations as code | Version-controlled, repeatable schema changes | No manual DB modifications |
| Infrastructure as code | Terraform, Pulumi, SST for infra | Reproducible environments in minutes |
| API-first design | Define API contracts before implementation | Frontend and backend work in parallel |
| Storybook / component dev | Develop UI components in isolation | No need to navigate full app for UI work |

---

## Leverage Points

High effort-to-impact ratio — small investments that pay dividends repeatedly.

| Leverage Point | Effort | Impact | Payoff Timeline |
|---|---|---|---|
| Automation scripts (seed, reset, deploy) | 1-2 hours | Saves 10+ min/day per developer | Days |
| Shared utilities (formatting, validation, logging) | 2-4 hours | Eliminates repeated code across services | Weeks |
| CI/CD pipelines | 4-8 hours | Removes all manual build/deploy steps | Immediately |
| Documentation (ADRs, onboarding, runbooks) | 2-3 hours | Cuts onboarding time by 50%+ | Weeks |
| Developer tooling (linters, formatters, git hooks) | 1-2 hours | Prevents entire categories of bugs | Immediately |
| Database seed scripts | 1-2 hours | Instant realistic local environments | Days |
| Error monitoring (Sentry, Axiom) | 1-2 hours | Find production bugs before users report them | Immediately |

---

## Time Sink Detection

Common time wasters and how to eliminate them.

| Time Sink | Hours Wasted/Week | Solution |
|---|---|---|
| Manual testing | 3-8 hours | Automated tests, Playwright for E2E, CI checks |
| Environment setup | 2-5 hours (new devs) | Docker Compose, devcontainers, seed scripts |
| Manual deployment | 1-3 hours | CI/CD pipeline, one-click deploys |
| Code review bottlenecks | 2-6 hours waiting | Small PRs, async reviews, max 24h SLA |
| Meeting overload | 5-10 hours | Async standups, written updates, office hours |
| Debugging without logs | 2-4 hours | Structured logging, error tracking, source maps |
| Dependency conflicts | 1-3 hours | Lock files, renovate bot, monorepo tooling |
| Unclear requirements | 3-8 hours rework | Spike tickets, design docs, early prototypes |

---

## Workflow Optimization

### Daily Workflow Template

```
Morning (high energy)
  1. Review overnight CI results and alerts
  2. Tackle the hardest problem first (deep work)
  3. Batch code reviews (one block, not scattered)

Midday
  4. Meetings and collaboration (if unavoidable)
  5. Respond to async threads

Afternoon
  6. Implementation work (flow state)
  7. Write tests for today's code
  8. Open PRs, update tickets, write context for tomorrow
```

### Essential IDE Shortcuts

| Action | macOS | Why It Matters |
|---|---|---|
| Go to file | `Cmd+P` | Never browse the file tree |
| Go to symbol | `Cmd+Shift+O` | Jump directly to functions/classes |
| Find in project | `Cmd+Shift+F` | Find anything across the codebase |
| Rename symbol | `F2` | Safe, project-wide renaming |
| Quick fix | `Cmd+.` | Auto-import, auto-fix linter issues |
| Toggle terminal | `` Ctrl+` `` | Stay in the editor |
| Multi-cursor | `Cmd+D` | Edit multiple occurrences at once |
| Move line | `Alt+Up/Down` | Reorder code without cut/paste |

### CLI Aliases & Scripts

```bash
# Git acceleration
alias gs='git status'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline -20'
alias gco='git checkout'
alias gcb='git checkout -b'
alias gpr='gh pr create --fill'

# Development
alias dev='npm run dev'
alias build='npm run build'
alias lint='npm run lint'
alias test='npm run test'

# Docker
alias dc='docker compose'
alias dcu='docker compose up -d'
alias dcd='docker compose down'
alias dcl='docker compose logs -f'

# Project navigation
alias repo='cd ~/dev/myproject'
```

### Shell Scripts Worth Writing

| Script | Purpose | Time Saved |
|---|---|---|
| `./scripts/setup.sh` | One-command local environment setup | Hours per new dev |
| `./scripts/seed.sh` | Reset and seed database with test data | 10 min/day |
| `./scripts/deploy.sh` | Build, test, and deploy in sequence | 15 min/deploy |
| `./scripts/new-feature.sh` | Scaffold feature (route, component, test) | 20 min/feature |
| `./scripts/db-reset.sh` | Drop, recreate, migrate, seed database | 10 min/occurrence |

---

## Anti-Patterns

Patterns that feel productive but destroy velocity.

| Anti-Pattern | What Happens | Instead Do |
|---|---|---|
| Over-engineering | Build abstractions for problems you don't have | Solve today's problem; refactor when patterns emerge |
| Premature optimization | Optimize code that isn't a bottleneck | Profile first, optimize the measured bottleneck |
| Gold plating | Polish features beyond requirements | Ship the 80% solution, iterate based on feedback |
| Yak shaving | Fix tangential problems endlessly | Time-box tangents to 15 min, then create a ticket |
| Not-invented-here | Rebuild what open source already solved | Evaluate existing solutions before writing custom code |
| Bikeshedding | Debate trivial decisions at length | Set a 5-min timer; if no consensus, the proposer decides |
| Cargo culting | Copy patterns without understanding why | Understand the problem before adopting a solution |

---

## Measurement — DORA Metrics

Track these four metrics to objectively measure engineering velocity.

| Metric | Elite | High | Medium | Low |
|---|---|---|---|---|
| **Deployment frequency** | On-demand (multiple/day) | Weekly | Monthly | Quarterly |
| **Lead time for changes** | < 1 hour | < 1 week | < 1 month | > 1 month |
| **Change failure rate** | < 5% | < 10% | < 15% | > 15% |
| **Mean time to recovery** | < 1 hour | < 1 day | < 1 week | > 1 week |

### How to Improve Each

- **Deployment frequency** — CI/CD, feature flags, trunk-based development
- **Lead time** — Small PRs, automated testing, preview deploys
- **Change failure rate** — Type safety, comprehensive tests, canary deploys
- **MTTR** — Observability, runbooks, feature flag kill switches

---

## NEVER Do

1. **NEVER manually deploy to production** — always use CI/CD pipelines
2. **NEVER merge without automated checks** — require passing CI before merge
3. **NEVER keep long-lived feature branches** — merge within 1-2 days or break it smaller
4. **NEVER skip writing types/interfaces** — the 30 seconds you save costs hours later
5. **NEVER copy-paste code more than once** — extract to a shared utility immediately
6. **NEVER ignore flaky tests** — fix or delete them; flaky tests erode trust in the suite
7. **NEVER optimize without measuring** — profile first, gut feelings are usually wrong

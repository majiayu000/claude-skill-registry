# Product Manager Skills

**Not a template pack. A PM operator for AI coding tools.**

Turn Claude Code, Codex, Cursor, or Windsurf into a product manager that can critique PRDs, diagnose SaaS metrics, plan roadmaps, run discovery, and coach career moves.

[![Release](https://img.shields.io/github/v/release/Digidai/product-manager-skills)](https://github.com/Digidai/product-manager-skills/releases)
[![License](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-green)](LICENSE)
[![Security](https://img.shields.io/badge/security-pure%20markdown%20%2B%20optional%20update%20check-brightgreen)](https://github.com/Digidai/product-manager-skills)
[![Works With](https://img.shields.io/badge/works%20with-Claude%20Code%20%7C%20Codex%20%7C%20Cursor%20%7C%20Windsurf-blue)](#install-in-60-seconds)

> Human-readable Markdown you can inspect line by line. Optional helper scripts for manual maintenance, zero automatic runtime execution.

## Why People Reuse It

Most AI PM tooling is good at writing polished nonsense. This skill is designed for repeat workflows where rigor matters:

- Turn vague feature requests into problem framing, measurable outcomes, and a usable PRD.
- Diagnose SaaS health from raw metrics instead of getting generic advice like "improve retention."
- Pressure-test prioritization, roadmaps, and strategy with explicit tradeoffs.
- Coach PM to Director to VP transitions with concrete gaps and action plans.

## Start With These 3 Workflows

| Workflow | Prompt | Example |
|---|---|---|
| **SaaS health diagnostic** | "Analyze these metrics: MRR $50k, 500 customers, gross margin 80%, monthly churn 8%, CAC $500." | [SaaS diagnostic demo](examples/saas-health-diagnostic.md) |
| **PRD pushback and review** | "Review this PRD draft like a strong PM peer. Flag bad framing, missing metrics, solution smuggling, and delivery risk." | [PRD review demo](examples/prd-review.md) |
| **Director readiness coaching** | "I'm a senior PM interviewing for Director roles in 90 days. Diagnose my gaps and coach me." | [Director coaching demo](examples/director-coaching.md) |

More prompts: [STARTER-PROMPTS.md](STARTER-PROMPTS.md)  
中文说明: [README.zh-CN.md](README.zh-CN.md)  
Core philosophy: [ETHOS.md](ETHOS.md)  
Version history: [CHANGELOG.md](CHANGELOG.md)
Worked examples: [Growth & PLG readiness](examples/growth-plg-readiness.md), [Growth activation recovery](examples/growth-plg-activation-recovery.md), [PM Sprint from idea to PRD](examples/pm-sprint-idea-to-prd.md), [PM Sprint from sales request to PRD](examples/pm-sprint-sales-request-to-prd.md)

## Install In 60 Seconds

### Claude Code / OpenClaw

```bash
clawhub install product-manager-skills
```

### Codex / Cursor / Windsurf / GitHub-based skill loaders

```bash
npx skills add Digidai/product-manager-skills
```

Then paste one of these:

```text
Help me write a PRD for a notification preferences feature. Make reasonable assumptions and label them.

Analyze these metrics: MRR $50k, 500 customers, gross margin 80%, monthly churn 8%, CAC $500.

Review my roadmap and tell me where stakeholder requests are outweighing evidence.
```

## What Good Output Looks Like

### 1. SaaS Diagnostic

Input:

```text
Analyze these metrics: MRR $50k, 500 customers, gross margin 80%, monthly churn 8%, CAC $500.
```

Expected behavior:

```text
- 8% monthly churn compounds to roughly 63% annual churn. This is a red flag, not a "slightly high" metric.
- ARPA is about $100/month. With 80% gross margin and 8% monthly churn, better LTV is about $1,000.
- LTV:CAC is about 2:1. Payback is about 6.25 months.
- Diagnosis: payback is workable, retention is not. Do not scale acquisition until churn is understood cohort by cohort.
```

Full example: [examples/saas-health-diagnostic.md](examples/saas-health-diagnostic.md)

### 2. PRD Review

Input:

```text
Review this PRD for a notification preferences center. Flag solution smuggling, weak metrics, overscoping, and delivery risk.
```

Expected behavior:

```text
- Your problem statement is solution-smuggled: "users need a preferences dashboard."
- Success metrics have no baseline, target, or guardrail.
- Scope mixes channels, digests, quiet hours, admin rules, and migration. This is multiple releases.
- Recommend a thinner first slice: email opt-out + account-level preferences + measurable reduction in unsubscribe-driven churn.
```

Full example: [examples/prd-review.md](examples/prd-review.md)

### 3. Career Coaching

Input:

```text
I'm a senior PM managing two PMs, strong on execution, weak on org influence, and interviewing for Director roles in 3 months. Coach me.
```

Expected behavior:

```text
- Diagnosis: strong team altitude, weak org altitude.
- Gap: you describe execution wins well but not portfolio tradeoffs or cross-functional influence.
- Plan: collect 3 stories that show org-level impact, build a weekly visibility loop, and practice decision framing with tradeoffs.
```

Full example: [examples/director-coaching.md](examples/director-coaching.md)

## What You Get

| Domain | What It Helps With | Example Frameworks |
|---|---|---|
| **Discovery & Research** | Validate problems, prep interviews, map journeys, structure experiments | JTBD, Mom Test, Opportunity Solution Tree, Lean UX Canvas, PoL Probes |
| **Strategy & Positioning** | Position products, prioritize work, size markets, build roadmaps | Geoffrey Moore, PESTEL, TAM/SAM/SOM, RICE, ICE, Kano |
| **Artifacts & Delivery** | Write and critique PRDs, user stories, epics, PRFAQs, recommendation docs | Cohn + Gherkin, Story Mapping, Epic Breakdown, PRFAQ |
| **Finance & Metrics** | Calculate 32 SaaS metrics and diagnose business health | MRR, ARR, NRR, CAC, LTV, Rule of 40, Magic Number |
| **Growth & PLG** | Design PLG strategy, optimize activation, model viral loops, diagnose conversion | PLG Readiness, Activation Framework, Viral Loop Design, Freemium Conversion |
| **Career & Leadership** | Coach PM to Director to VP transitions | Altitude-Horizon, Three Ps, 30-60-90 onboarding |
| **AI Product Craft** | Pressure-test AI-native product decisions | AI-Shaped Readiness, Context Engineering, Agent Orchestration |

## Why It Performs Better Than Generic Prompting

| Generic prompting | This skill |
|---|---|
| Writes plausible PM text | Applies PM frameworks and quality gates |
| Accepts bad framing | Pushes back on Solution Smuggling, Metrics Theater, Feature Factory, and more |
| Gives generic churn advice | Calculates churn, LTV, payback, and names the real bottleneck |
| Asks you to repeat PM context every session | Carries a reusable PM workflow and routing system |
| Optimizes for politeness | Optimizes for decisions, tradeoffs, and next steps |

## Who It Is For

- Technical PMs, founders, and product leads who already work inside AI coding tools.
- Teams that want a reusable PM brain without sending product context to another SaaS.
- People who value pushback, assumptions, and explicit tradeoffs over nice-sounding output.

## Who It Is Not For

- Teams looking for a collaborative web app with approvals, comments, and sharing workflows.
- Users who only want passive template filling and never want the AI to challenge the framing.
- Non-technical buyers who prefer turnkey SaaS onboarding over local or repo-based installation.

## PM Sprint Workflow (new in v0.5)

Say "take this from idea to PRD" or "full PM sprint on this feature" and the skill runs a 6-phase end-to-end workflow: Discover, Position, Prioritize, Specify, Validate, Measure. Each phase feeds output to the next. Skip, reorder, or stop at any phase.

## Interaction Style

This skill is optimized for a fast first useful draft:

- If the request is clear enough, it answers immediately and labels assumptions inline.
- If context is partial, it gives the best draft first and only asks the minimum follow-up questions needed.
- If the task is genuinely exploratory, it can switch into guided mode one question at a time.
- Every answer ends with decisions made, assumptions to validate, recommended next step, and a completion status (DONE, DONE_WITH_CONCERNS, BLOCKED, or NEEDS_CONTEXT).

### Coaching Mode (new in v0.4)

Say "coach me" and the skill shifts from helpful assistant to demanding PM peer. It will push back on weak framing, challenge vague metrics, name anti-patterns in your thinking, and end with a verdict instead of a summary.

Each knowledge domain has its own coaching rules. Discovery coaching pushes on evidence. Strategy coaching pushes on positioning specificity. Finance coaching pushes on retention before growth. Career coaching pushes on altitude gaps.

Example: [Coaching a discovery session](examples/coaching-discovery.md)

## Built For Repeat Usage

Most PM work is recurring. This skill is strongest when you reuse it weekly:

- Monday: review roadmap changes and prioritization requests.
- Mid-week: critique PRDs, epics, and user stories before sharing with engineering.
- Friday: run a SaaS health diagnostic or feature ROI check.
- Career season: rehearse interview stories, operating altitude, and leadership gaps.

## Install Options

| Environment | Install |
|---|---|
| Claude Code / OpenClaw | `clawhub install product-manager-skills` |
| Codex / Cursor / Windsurf / GitHub-based skill loaders | `npx skills add Digidai/product-manager-skills` |
| Claude Projects | Upload `SKILL.md`, `knowledge/`, and `templates/` |
| Any LLM with local file loading | Point the system prompt at `SKILL.md` and keep sibling folders intact |

## Structure

```text
SKILL.md
VERSION
bin/update-check
bin/validate-release
knowledge/
templates/
examples/
STARTER-PROMPTS.md
ETHOS.md
CHANGELOG.md
CONTRIBUTING.md
README.zh-CN.md
README.md
LICENSE
```

Current footprint stays small: 7 knowledge modules, 12 templates, 8 worked examples, and 2 small shell scripts.

## Trust And Security

The runtime behavior is Markdown-first. The repo ships two small shell scripts for manual maintenance:

- `bin/update-check`: an optional manual helper that compares your local `VERSION` file against the remote version on GitHub. It caches results and times out after 5 seconds. No telemetry, no data collection.
- `bin/validate-release`: a maintainer-facing consistency check used before publishing. It validates version sync and packaged assets, but it is not invoked during normal skill usage.
- All knowledge, templates, and routing logic remain human-readable Markdown with no executable code.
- No environment variables or credentials required.
- No privilege escalation.
- The skill itself does not auto-run these scripts during normal usage.

## Featured In

- [awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) (11.6k stars)
- [awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills) (7.6k stars)
- [awesome-openclaw](https://github.com/SamurAIGPT/awesome-openclaw)
- [awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills)
- [Top-AI-Tools](https://github.com/ghimiresunil/Top-AI-Tools)
- [awesome-ai-tools](https://github.com/eudk/awesome-ai-tools)
- [claude-skills](https://github.com/alirezarezvani/claude-skills)
- [claude-skills-collection](https://github.com/abubakarsiddik31/claude-skills-collection)
- [awesome-product-manager](https://github.com/yuhenobi/awesome-product-manager)
- [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills)

## Feedback And Contribution

- Open an issue if a framework is missing or a workflow feels weak.
- Open a discussion if you want a new domain or stronger examples.
- See [CONTRIBUTING.md](CONTRIBUTING.md) for the fastest way to give useful workflow feedback.
- If the skill helped you, star the repo or share an output generated from the templates.

## License

[CC BY-NC-SA 4.0](LICENSE)

Built by [Gene Dai](https://genedai.me/). Distilled from real product work, not textbook summaries.

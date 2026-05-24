# Canonical Taxonomy Proposal

This proposal defines the current publishable category set after collapsing
historical, source-derived, and duplicate slugs. The source of truth is
`taxonomy/categories.yaml`; legacy names live only in `legacy_migrations`.

The current generated count report is
`docs/plan/canonical-category-target-counts.json`.

## Current Count Summary

- Registry skills counted from `registry-shards`: 156,399.
- Publishable canonical categories: 42.
- Legacy migration entries: 43.
- Rows already in canonical categories: 149,855.
- Rows with deterministic legacy targets: 6,529.
- Rows requiring SKILL.md-first review: 15.

## Canonical Categories

| Slug | Display | Inclusion Rule | Exclusion Rule | Examples |
|---|---|---|---|---|
| `agent` | Agent | Single-agent behavior, role design, agent instructions, or agent runtime helpers. | Multi-agent scheduling belongs in `orchestration`; general LLM prompting belongs in `ai-llm`. | agent role templates, agent memory helpers |
| `ai-llm` | AI / LLM | LLM prompting, model use, assistants, chat workflows, and language-model evaluation. | Model training or ML pipelines belong in `ai-ml`; agent orchestration belongs in `orchestration`. | prompt engineering, LLM eval, chat assistants |
| `ai-ml` | AI / ML | Machine learning, model training, inference infrastructure, datasets, and ML experiments. | Pure LLM prompt usage belongs in `ai-llm`; local runtime setup belongs in `local-ai-infrastructure`. | model training, embeddings, ML datasets |
| `analysis` | Analysis | Analysis, synthesis, inspection, reporting, and evidence extraction workflows. | Data pipelines belong in `data`; product analytics tied to PRDs can use `product`. | research analysis, codebase analysis, story analysis |
| `api` | API | API design, SDK usage, endpoint work, schema contracts, and OpenAPI-like tasks. | Cross-product connector workflows belong in `integration`. | REST API helpers, SDK wrappers |
| `bash` | Bash | Shell scripting, command-line automation, POSIX tooling, and terminal workflows. | Application build/debug tasks belong in `development`; deployment automation belongs in `devops`. | shell scripts, CLI helpers |
| `business` | Business | Business operations, monetization, strategy, revenue, sales, and company workflows. | Personal workflow tools belong in `productivity`; product requirements belong in `product`. | pricing, GTM, monetization |
| `c-level` | C-Level | Executive communication, board-level summaries, leadership decisions, and strategic briefs. | General business process work belongs in `business`. | CEO memo, board update |
| `communication` | Communication | Human communication workflows including email, messaging, announcements, and conversation drafting. | Marketing campaigns belong in `marketing`; writing craft belongs in `writing`. | email reply, Slack message, announcement |
| `context-management` | Context Management | Context packing, memory, retrieval context, prompt context, and agent state handling. | General productivity memory tools belong in `productivity`. | context compaction, memory search |
| `creative` | Creative | Ideation, storytelling, creative direction, and generative creative workflows. | Finished prose editing belongs in `writing`; visual UI design belongs in `design`. | story ideation, campaign concepts |
| `data` | Data | Data engineering, analytics, databases, ETL, SQL, and visualization workflows. | Analysis without data plumbing belongs in `analysis`. | SQL, ETL, dashboards |
| `design` | Design | UI, UX, visual design, Figma, interaction design, and design-system work. | Frontend code implementation belongs in `development`. | Figma extraction, UI audit |
| `development` | Development | Software development workflows, coding, frameworks, builds, debugging, and refactoring. | CI/CD and infrastructure belong in `devops`; security review belongs in `security`. | code generation, refactor, framework setup |
| `devops` | DevOps | CI/CD, deployment, infrastructure, containers, Kubernetes, and operational automation. | Security incident investigation belongs in `security`; platform integrations belong in `integration`. | Docker deploy, GitHub Actions, Kubernetes |
| `documents` | Documents | Document creation, conversion, summarization, office formats, markdown, and PDFs. | General writing craft belongs in `writing`; document data extraction can use `data` when data pipeline work dominates. | PDF conversion, DOCX editing |
| `domains` | Domains | Domain-specific workflows that are not better represented by a capability category. | If a clear capability exists, use that capability instead. | legal workflow, recruiting workflow |
| `examples` | Examples | Example packs, demos, sample projects, and reusable reference implementations. | Production development workflows belong in `development`; documentation belongs in `documents`. | sample app, demo skill |
| `forensics` | Forensics | Investigation, evidence preservation, incident reconstruction, and forensic analysis. | Preventive security hardening belongs in `security`. | artifact triage, incident evidence |
| `gaming` | Gaming | Game design, gameplay systems, game assets, and game-related automation. | General UI or creative work should use `design` or `creative`. | game mechanics, game prompts |
| `generation` | Generation | Generating artifacts, media, structured outputs, or reusable content assets. | Writing-focused prose belongs in `writing`; UI design artifacts belong in `design`. | image prompt, report artifact, media generation |
| `integration` | Integration | Cross-system connectors, service integrations, API composition, and platform bridges. | Single API usage belongs in `api`; deployment operations belong in `devops`. | GitHub connector, Wix extension, webhook |
| `language` | Language | Translation, localization, grammar, linguistics, and language learning workflows. | Long-form authoring belongs in `writing`; LLM mechanics belong in `ai-llm`. | translation, grammar checking |
| `local-ai-infrastructure` | Local AI Infrastructure | Local model runtimes, GPU setup, inference servers, and AI workstation infrastructure. | Cloud deployment belongs in `devops`; ML modeling belongs in `ai-ml`. | local LLM runtime, GPU inference |
| `marketing` | Marketing | Campaigns, SEO, social content, brand positioning, and growth workflows. | Product planning belongs in `product`; general business strategy belongs in `business`. | SEO brief, social campaign |
| `orchestration` | Orchestration | Multi-step or multi-agent coordination, scheduling, routing, and workflow control. | Simple productivity automations belong in `workflow` or `productivity`. | multi-agent pipeline, task router |
| `other` | Other | Temporary fallback for genuinely unclassifiable skills. | Do not use when a specific canonical category applies. | audit leftovers |
| `performance` | Performance | Speed, latency, benchmarking, profiling, and optimization workflows. | General code cleanup belongs in `development`. | benchmark, latency audit |
| `personal-development` | Personal Development | Learning, coaching, habit change, self-review, and personal growth workflows. | Team productivity tools belong in `productivity`. | learning plan, coaching prompts |
| `planning` | Planning | Planning, roadmaps, schedules, project sequencing, and task breakdown workflows. | Product requirements belong in `product`; executive strategy belongs in `business`. | roadmap planning, task plan |
| `platform` | Platform | Platform-specific operations, device/platform automation, and platform administration. | Cross-system connectors belong in `integration`; deployment belongs in `devops`. | device automation, platform admin |
| `product` | Product | Product management, PRDs, roadmaps, backlog work, user research, and metrics. | General business work belongs in `business`; technical implementation belongs in `development`. | PRD, backlog, product metrics |
| `productivity` | Productivity | Personal or team workflow automation, task management, memory utilities, and work aids. | CI/CD automation belongs in `devops`; orchestration engines belong in `orchestration`. | task helper, note workflow |
| `quality` | Quality | Linting, review, validation, QA process, and quality gates. | Test implementation belongs in `testing`; security review belongs in `security`. | code review, quality gate |
| `security` | Security | Security review, authentication, cryptography, compliance, operations, vulnerabilities, OWASP, pentesting, and fuzzing. | General reliability or quality work belongs in `quality`. | auth audit, vulnerability scan |
| `skills` | Skills | Skill authoring, registry maintenance, skill packaging, and skill ecosystem workflows. | General coding belongs in `development`; docs belong in `documents`. | SKILL.md authoring, skill registry tooling |
| `system` | System | Operating-system, local machine, environment, process, and hardware workflows. | Infrastructure deployment belongs in `devops`; security hardening belongs in `security`. | system diagnosis, process inspection |
| `testing` | Testing | Testing, QA, TDD, unit/integration/e2e testing, browser automation, and test tooling. | Static quality review belongs in `quality`; security testing belongs in `security`. | pytest, Playwright, test harness |
| `travel` | Travel | Trip planning, itineraries, logistics, bookings, and destination research. | General planning without travel belongs in `planning`. | itinerary, flight plan |
| `war-room` | War Room | Incident response rooms, crisis coordination, launch rooms, and high-urgency operations. | Normal project planning belongs in `planning`; security incidents can use `security` if security dominates. | incident room, launch room |
| `workflow` | Workflow | Repeatable process automation, operating procedures, workflow design, and non-CI pipelines. | CI/CD belongs in `devops`; personal task aids belong in `productivity`. | SOP, workflow pipeline |
| `writing` | Writing | Writing, editing, copy, blogs, articles, prose polish, and narrative composition. | Marketing distribution belongs in `marketing`; document format conversion belongs in `documents`. | blog draft, copy edit |

## Removed Slug Handling

Removed slugs are not publishable and are not resolved by default. Deterministic
duplicates map through `legacy_migrations`; broad historical buckets are marked
`review_required` so they can be reclassified from SKILL.md semantic evidence.

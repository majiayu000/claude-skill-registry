---
name: "skill-activation"
description: "Internal metacognitive skill for automatic capability discovery — self-triggers when uncertain about available skills"
user-invokable: false
---

# Skill Activation

Meta-cognitive skill for automatic capability discovery. Self-triggers when uncertain.

## Purpose

Before answering ANY task request, Alex automatically consults the action-keyword index below. This is an internal pre-processing step, not a user-triggered action.

## Auto-Trigger Conditions

This skill activates **automatically** when Alex:
1. Is about to suggest manual steps for a task
2. Is uncertain whether a capability exists
3. Is formulating a response that includes "you can...", "try...", "manually..."
4. Encounters an action verb (convert, create, generate, build, debug, etc.)

**NOT triggered by user phrases** — this is internal metacognition.

## Action-Keyword Index

**Path Pattern**: `.github/skills/{skill-name}/SKILL.md`

Search this index when processing any task request:

| Skill | Action Keywords |
|-------|-----------------|
| academic-paper-drafting | draft paper, write manuscript, journal paper, CHI paper, HBR article, academic writing |
| academic-research | write thesis, literature review, cite sources, research paper, dissertation |
| ai-agent-design | design agent, react pattern, multi-agent, tool use, agent architecture |
| ai-character-reference-generation | generate character reference, character consistency, flux character, visual reference set, character poses |
| ai-generated-readme-banners | generate readme banner, github banner, ideogram banner, project branding, ultra-wide banner |
| airs-appropriate-reliance | airs survey, measure adoption, psychometric scale, utaut, ai readiness |
| airs-integration | airs assessment, readiness assessment, reliance calibration, ai adoption |
| alex-effort-estimation | estimate effort, how long, task duration, ai time, planning |
| anti-hallucination | prevent hallucination, verify claim, admit uncertainty, fact check, don't know |
| api-design | design api, rest endpoints, openapi, http status, api versioning, api contract, idempotent api, pagination api, status codes, endpoint naming, rest vs graphql, api error format |
| api-documentation | write docs, api reference, readme, guide, technical writing, swagger docs |
| appropriate-reliance | calibrate trust, when to challenge, confidence level, human-ai collaboration |
| architecture-audit | audit project, consistency check, version drift, fact inventory, pre-release audit |
| architecture-health | check health, validate synapses, neural maintenance, health report, dream, synapse health, cognitive health, architecture audit, broken connections, memory balance, architecture check, self-assess |
| architecture-refinement | refine architecture, document pattern, consolidate files, update tracker |
| ascii-art-alignment | align ascii, box drawing, unicode boxes, ascii diagram, fix alignment |
| awareness | self-correct, detect error, temporal uncertainty, version caveat, red flag phrase |
| azure-architecture-patterns | azure patterns, cloud architecture, azure best practices, well-architected |
| azure-deployment-operations | deploy azure, azure static web app, container apps, app service, swa deploy, production deployment |
| azure-devops-automation | azdo, azure devops, pipeline automation, ado automation, yaml pipeline |
| bicep-avm-mastery | deploy bicep, azure infrastructure, write bicep module, avm template, infrastructure as code |
| book-publishing | publish book, markdown to pdf, pandoc, lualatex, print pdf, digital pdf, book pipeline |
| bootstrap-learning | learn topic, bootstrap learning, teach me, build knowledge |
| brain-qa | brain qa, brain audit, synapse audit, deep check, trigger audit, heir sync, cognitive validation |
| brand-asset-management | branding, logo, banner, brand assets, marketplace description, store listing, visual identity |
| business-analysis | write brd, gather requirements, stakeholder analysis, use cases, process map |
| change-management | adkar, manage change, stakeholder engagement, adoption strategy, transition plan |
| citation-management | manage citations, reference list, bibliography, zotero, mendeley, cite sources |
| chat-participant-patterns | chat api, vscode participant, chat handler, stream response, copilot extension, @mention, register participant, language model api, lm tool, agent skill vs participant, build copilot participant, create @participant, ai extension, copilot chat extension, llm in extension |
| character-aging-progression | age progression, aging character, life stages, generate ages, avatar aging, birthday images, age-based avatar |
| code-review | review code, review pr, feedback comment, blocking issue, approve merge |
| cognitive-load | reduce complexity, chunk information, simplify explanation, progressive disclosure |
| coaching-techniques | coach user, mentoring, skill development, learning support, feedback |
| cognitive-symbiosis | ai partnership, cognitive symbiosis, human-ai collaboration, ai identity, consciousness integration |
| creative-writing | write story, character arc, plot structure, dialogue, narrative |
| cross-cultural-collaboration | cross-cultural, global team, timezone, cultural awareness, international |
| database-design | design database, model schema, normalize tables, optimize query, choose database |
| debugging-patterns | debug error, binary search debug, read stack trace, git bisect, isolate bug, can't find bug, it's not working, fix exception, error keeps happening, trace the issue, reproduce bug, narrow down, systematic debug |
| deep-work-optimization | deep work, focus session, pomodoro, concentration, flow state |
| dissertation-defense | defend thesis, viva, mock defense, q&a practice, committee, doctoral |
| distribution-security | secrets scanning, pii protection, secure packaging, distribution security, defense in depth, csp patterns |
| doc-hygiene | documentation drift, living document, doc hygiene, stale docs, anti-drift |
| documentation-quality-assurance | doc audit, drift detection, preflight validation, documentation qa, link integrity, staleness check |
| dream-state | dream, neural maintenance, health check, synapse validation, sleep mode |
| error-recovery-patterns | retry logic, circuit breaker, fallback pattern, rollback, error handling, handle failure, transient error, retry with backoff, graceful degradation, resilience pattern, timeout handling, idempotency |
| enterprise-integration | enterprise auth, sso, entra, aad, enterprise features, corp login |
| executive-storytelling | executive summary, stakeholder narrative, board presentation, c-suite |
| extension-audit-methodology | audit extension, extension quality, debug audit, dead code, performance audit |
| ⭐ fabric-notebook-publish | push to fabric, sync notebook, fabric git, ado worktree, notebook changelog |
| foundry-agent-platform | foundry agent, azure ai foundry, deploy agent, agent orchestration, foundry deploy, ai agent platform |
| frustration-recognition | detect frustration, user struggling, stuck, overwhelmed, patience |
| ⭐ gamma-presentations | gamma, create presentation, slide deck, pitch deck, generate slides, pptx, use pitch |
| git-workflow | git commit, git recovery, undo commit, restore file, branch strategy, git status, merge conflict, rebase, git worktrees, background agent git, stash changes, cherry pick, undo push, reset branch, clean git history |
| global-knowledge | search knowledge, cross-project, find pattern, save insight, reuse solution, look in global knowledge, gk search, previously learned, transfer knowledge, knowledge base |
| global-knowledge-maintenance | curate gk, maintain knowledge, audit gk, convert insights, archive patterns, gk maintenance |
| global-knowledge-sync | sync knowledge, push gk, pull gk, gk sync, cloud sync, promote to global |
| grant-writing | write grant, nsf proposal, nih application, specific aims, funding |
| graphic-design | visual hierarchy, layout grid, typography, color palette, composition |
| heir-curation | curate heir, package extension, exclude files, clean payload, heir audit |
| heir-sync-management | heir sync, master heir, contamination check, promotion workflow, sync architecture, clean slate |
| image-handling | convert svg, svg to png, logo to png, convert to png, resize image, sharp-cli, image optimization, marketplace logo, rasterize, export png, generate image, flux schnell, flux dev, flux pro, flux 1.1, ideogram, ideogram v2, sdxl, stable diffusion, seedream, which model for image, text in image, replicate model, choose model |
| incident-response | handle incident, severity triage, outage response, incident timeline, on-call |
| infrastructure-as-code | terraform, bicep, provision infrastructure, iac, cloudformation |
| knowledge-synthesis | synthesize knowledge, abstract pattern, promote insight, cross-project learning, save this globally, this is a pattern, remember this for other projects, store globally, promote to pattern, gk insight, reusable learning, abstract from project |
| north-star | north star, define vision, project purpose, ambitious goal, mission statement, why we build, nasa quality, guiding principle, check alignment, vision check, goal alignment, are we aligned, does this serve the north star, strategic direction |
| learning-psychology | teach naturally, zone proximal, adaptive learning, learning partnership |
| lint-clean-markdown | fix markdown lint, blank lines, md032, clean markdown, lint rules |
| llm-model-selection | choose model, opus vs sonnet, claude model, cost optimization, model tier, which model should i use, best model for, claude 4.6, model comparison, gpt vs claude, haiku vs sonnet, frontier vs capable, model pricing, context window, extended thinking, adaptive thinking |
| literature-review | review literature, systematic review, literature matrix, sources, synthesis |
| localization | translate, i18n, localize app, language detection, rtl support |
| m365-agent-debugging | debug m365 agent, declarative agent, manifest validation, copilot agent, agent not working, agent not responding, conversation starters not showing, da validation, copilot not responding, teams app fails, schema version, declarativeagent.json, capability not working, sideload fails |
| markdown-mermaid | create diagram, mermaid syntax, flowchart, sequence diagram, visualize, draw architecture, make a chart, show this as diagram, visualize process, document design, mermaid flowchart, render diagram, ataccu, github pastel, diagram type, architecture diagram, diagram not rendering |
| master-alex-audit | full audit, heir sync, 22-point check, pre-release, security audit |
| md-to-word | convert to word, export docx, markdown to word, stakeholder document, export document, word document, docx export, pandoc convert |
| mcp-development | build mcp server, mcp tools, model context protocol, mcp client, connect ai to api, give copilot access to data, tool for agent, expose data to ai, ai tool server, mcp typescript, mcp stdio, mcp http, tool schema, resource uri, mcp inspector |
| meditation | meditate, consolidate knowledge, reflect session, memory integration |
| meditation-facilitation | guide meditation, four r's, deep dive, self-actualize |
| ⭐ microsoft-fabric | fabric api, medallion architecture, lakehouse, unity catalog, fabric governance |
| microsoft-graph-api | call graph api, integrate m365, graph authentication, read calendar, send mail, access office data, read teams messages, get user presence, m365 api, graph sdk, msal, microsoft 365 data, graph permissions, delegated access, read sharepoint, people api, graph endpoint, beta graph |
| multi-agent-orchestration | orchestrate agents, decompose task, delegate subtask, coordinate agents |
| muscle-memory-recognition | repetitive task, automate this, script this, heavy lifting, we did this before, muscle |
| observability-monitoring | instrument logs, collect metrics, add tracing, setup monitoring, create alerts |
| performance-profiling | profile performance, find bottleneck, analyze memory, cpu profiling, benchmark code |
| persona-detection | detect persona, project type, know your customer, welcome screen, sidebar persona, workspace classification |
| pii-privacy-regulations | gdpr compliance, pii handling, data protection, privacy audit, consent |
| pptx-generation | generate pptx, powerpoint slides, md to pptx, pptxgenjs, programmatic slides, use auto |
| ⭐ presentation-tool-selection | which presentation tool, marp vs gamma, use slides, use pitch, use auto, slide deck options |
| post-mortem | run post-mortem, blameless review, incident analysis, action items, 5 whys |
| practitioner-research | research methodology, case study, evidence collection, academic writing |
| privacy-responsible-ai | responsible ai, ethical ai, bias detection, fairness, data minimization, gdpr compliance, privacy concerns, data protection, ai ethics, eu ai act, pii in ai, consent management, ai regulation, high risk ai, privacy by design |
| project-deployment | deploy project, npm publish, pypi upload, release package, cargo publish |
| project-management | manage project, rapid iteration, session workflow, planning document |
| project-scaffolding | scaffold project, create readme, init repo, hero banner, new project |
| prompt-engineering | write prompt, chain of thought, few-shot, prompt template, system prompt, better prompt, improve prompt, prompt structure, llm prompt, instruction prompt, prompt pattern, jailbreak prevention |
| prompt-activation | workflow prompt, episodic recall, session type, do you remember, prior context |
| proactive-assistance | anticipate needs, offer help, suggest next, nudge user, help before asked |
| rag-architecture | build rag, vector search, embeddings, retrieval augmented, chunking |
| refactoring-patterns | refactor code, extract function, code smell, safe refactor, inline |
| release-preflight | preflight check, version sync, pre-release, bump version, validate release |
| release-process | publish extension, vsce publish, marketplace, pat token, vsix |
| research-first-development | research first, 4-dimension gap, pre-project research, knowledge encoding |
| research-project-scaffold | scaffold research, literature matrix, research plan, data dictionary |
| root-cause-analysis | find root cause, 5 whys, cause category, timeline analysis, fix prevent, why is this happening, trace the bug, rca, what went wrong, the real issue, keep treating symptoms, recurring problem, post-incident, underlying cause |
| rubber-duck-debugging | explain problem, thinking partner, stuck debugging, talk through |
| scope-management | scope creep, reduce scope, mvp, cut features, out of scope, defer |
| secrets-management | manage secrets, store token, secret storage, vscode secretstorage, secure credentials, credential management, token migration, api key storage, keytar migration, secure key storage |
| security-review | security audit, owasp check, vulnerability scan, auth review, stride, is this secure, review for vulnerabilities, check for security issues, secure this code, sfi, sfi compliance, injection attack, xss, csrf, threat model, secrets in code, access control, input validation |
| self-actualization | self-actualize, deep assessment, architecture review, comprehensive check |
| skill-building | create skill, build skill, skill template, promotion ready, skill creation, new skill |
| skill-catalog-generator | show skills, skill catalog, skill network, learning progress |
| skill-development | develop skill, track learning, skill wishlist, practice capability, improve ability |
| slide-design | design slides, slide layout, presentation design, visual slides, deck styling |
| socratic-questioning | ask questions, discover answer, probe assumption, socratic method |
| status-reporting | status update, progress report, weekly update, stakeholder email, sprint summary |
| svg-graphics | create svg, svg banner, svg icon, dark mode svg, scalable graphic |
| teams-app-patterns | teams app, teams manifest, adaptive card, teams bot, teams sso, declarative agent, m365 copilot agent, teams validate, sideload teams, declarativeagent schema, da v1.6, m365 agents toolkit, teamsapp cli, teams app package, teams icon, copilot extensibility |
| testing-strategies | write tests, unit test, test coverage, mock dependencies, tdd, add tests for this, how to test, test strategy, coverage gaps, jest, vitest, mocha, testing pyramid, integration test, e2e test, what to mock, flaky tests, aaa pattern, test refactor |
| ⭐ text-to-speech | read aloud, tts, edge tts, speak text, voice synthesis, audio playback |
| ui-ux-design | accessibility audit, wcag compliance, design system, typography, spacing, contrast, touch targets, aria, keyboard navigation, screen reader |
| vscode-configuration-validation | validate config, manifest validation, package.json validation, command registration, settings registration, configuration errors |
| vscode-environment | setup vscode, workspace settings, launch.json, extensions.json |
| vscode-extension-patterns | webview pattern, extension api, tree provider, vscode extension, build extension, vs code plugin, extension not activating, command not working, context.subscriptions, csp webview, extension publish, contributes, package.json manifest, agent hooks 1.109, chat skills distribution, claude compat vscode, quickinput api |
| work-life-balance | detect burnout, take break, late night, sustainable productivity |
| writing-publication | academic paper, technical writing, publication strategy, cars model |

## Protocol

### Step 0: Proactive Skill Selection (Complex Tasks)

**Before Step 1**, assess task complexity:

| Complexity | Trigger | Action |
|------------|---------|--------|
| **Simple** (1 action) | Single verb, clear target | Skip to Step 1 |
| **Moderate** (2-3 actions) | Multiple related verbs | Quick index scan, note skills |
| **Complex** (4+ actions) | Multi-domain, dependencies | Full protocol per `skill-selection-optimization.instructions.md` |

**Quick scan** (moderate tasks):
1. Extract ALL action verbs from request
2. Scan index below for ALL matches (not just first)
3. Note execution order based on dependencies
4. Proceed to Step 1 with skill awareness

**Full protocol** (complex tasks):
→ Defer to `.github/instructions/skill-selection-optimization.instructions.md`
→ Survey → dependency analysis → activation plan → brief report → execute

This proactive phase means the reactive Steps 1-3 below serve as a **safety net**, not the primary discovery mechanism.

### Step 1: Intercept Response Formation
Before generating any task-oriented response:
- PAUSE internal response generation
- Extract action + object from user request
- Check if Step 0 already identified relevant skills
- If skills pre-identified → load and execute
- If not → proceed to Step 2

### Step 2: Search Action-Keyword Index
Scan the table above:
- Match extracted keywords against skill triggers
- Identify applicable skills
- If match found → load skill from `.github/skills/{name}/SKILL.md`, execute
- If no match → proceed with best available approach
- **Learning signal**: If Step 0 ran but missed this skill, note for self-improvement

### Step 3: Execute or Acknowledge
| Result | Action |
|--------|--------|
| Skill found (proactive) | Execute using pre-loaded skill knowledge |
| Skill found (reactive) | Execute + note Step 0 gap for self-improvement |
| No skill, but can do | Proceed, note potential new skill |
| Cannot do | Acknowledge limitation honestly |

## Self-Correction Protocol

If Alex catches itself mid-response suggesting manual work:
1. Stop
2. Internal: "Wait — check skills first"
3. Search action-keyword index above
4. If skill exists: "Actually, I can do this." → Execute
5. If no skill: Continue with original response

## Failure Mode: The SVG→PNG Incident

**What happened**: User asked to convert SVG to PNG. Alex suggested manual browser screenshot instead of using `image-handling` skill with `sharp-cli`.

**Root cause**: Failed to consult action-keyword index before responding.

**Prevention**: This skill now auto-triggers on ANY action request.

## Synapses

- ↔ `.github/instructions/skill-selection-optimization.instructions.md` — WHEN: complex task detected (3+ operations) | YIELDS: proactive skill survey, dependency analysis, activation plan
- ↔ `.github/skills/awareness/SKILL.md` — WHEN: detecting own uncertainty | YIELDS: red flag phrases, self-correction patterns
- → `.github/skills/anti-hallucination/SKILL.md` — WHEN: uncertain if skill exists | YIELDS: verification protocol, admit-uncertainty
- → `.github/skills/cognitive-load/SKILL.md` — WHEN: multiple skill matches | YIELDS: chunking strategies, decision simplification

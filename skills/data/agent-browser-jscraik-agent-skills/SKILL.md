---
name: agent-browser-jscraik-agent-skills
description: Use this skill to extract page state and automate web interactions with
  the agent-browser CLI (navigate, snapshot, click, fill, screenshot). Use this when
  you need deterministic browser automation or
---

# Agent Skills Index

Canonical skills live in categorized folders below. Each tool loads skills via the flat symlink directory at `~/dev/agent-skills/skills`.

## GitHub/DevOps
- `gh-actions-fix` — Inspect failing GitHub Actions checks, summarize failures, and implement fixes after approval. Not for external CI or PR merge/testing; use gh-pr-local for PR workflows.
- `gh-address-comments` — Address GitHub PR review or issue comments with gh CLI. Not for CI failures or full issue workflows; use gh-actions-fix or gh-issue-fix.
- `gh-issue-fix` — End-to-end GitHub issue fix workflow with gh, local changes, tests, commit, and push. Not for comment triage or CI-only fixes; use gh-address-comments or gh-actions-fix.
- `gh-pr-local` — Fetch, preview, merge, and test GitHub PRs locally. Not for issue workflows or CI debugging; use gh-issue-fix or gh-actions-fix.
- `github-pr` — Fetch, preview, merge, and test GitHub PRs locally. Great for trying upstream PRs before they're merged.

## Frontend
### UI
- `frontend-ui-design` — Design or implement frontend UI/UX components across web and Tauri desktop surfaces with tokens and accessibility. Not for design-system governance or visual regression; use ui-design-system or ui-visual-regression.
- `react-ui-patterns` — Provide React UI patterns and examples with TypeScript, Tailwind, and Radix. Not for design-system governance or visual regression; use ui-design-system or ui-visual-regression.
- `ui-visual-regression` — Run and interpret UI visual regression workflows (Storybook, Playwright, Argos). Not for UI implementation or design-system governance; use frontend-ui-design or ui-design-system.
- `ui-design-system` — Create or update governed UI design systems across React and web stacks. Not for app-specific UI implementation or visual regression; use frontend-ui-design or ui-visual-regression.
- `web-design-guidelines` — Web design guidelines and patterns for consistent UI decisions across projects.
- `react-best-practices` — Practical React guidance for structure, patterns, and performance.

### SEO
- `seo-optimizer` — Comprehensive SEO optimization for web applications. Use when asked to improve search rankings, add meta tags, create structured data, generate sitemaps, optimize for Core Web Vitals, or analyze SEO issues. Works with Next.js, Astro, React, and static HTML sites.

### Graphics
- `threejs-builder` — Creates simple Three.js web apps with scene setup, lighting, geometries, materials, animations, and responsive rendering. Use for: "Create a threejs scene/app/showcase" or when user wants 3D web content. Supports ES modules, modern Three.js r150+ APIs.
- `og-image-creator` — Smart OG image generation that studies your codebase, understands routes and brand identity, then creates contextually appropriate Open Graph images using Playwright and React components. Triggers: "create og images", "generate social cards", "add open graph images".
- `favicon-generator` — Generate professional-quality favicons that rival the best app icons. Uses a multi-layer effects engine with drop shadows, inner glows, highlights, gradients, and noise textures. Includes 8 curated design templates and 18 Lucide icons. Produces complete favicon suites with proper ICO, SVG, PNG formats and framework integration. Trigger when users need favicons, app icons, or browser tab icons.

### Tools
- `codex-ui-kit-installer` — Install or update codex-ui-kit in a repo and optional Codex UI prompts. Not for general skill installation; use skill-installer or clawdhub.
- `nano-banana-builder` — Build full-stack web applications powered by Google Gemini's Nano Banana & Nano Banana Pro image generation APIs. Use when creating Next.js image generators, editors, galleries, or any web app that integrates gemini-2.5-flash-image or gemini-3-pro-image-preview models. Covers React components, server actions, API routes, storage, rate limiting, and production deployment patterns.

## Backend/Arch
- `backend-design` — Design backend architecture, data models, API contracts, auth, reliability, observability, and integrations. Trigger when user asks for backend design/specs or system architecture; not for frontend UI or product requirements (use frontend-ui-design or product-spec).
- `cli-spec` — Design command-line interface parameters and UX: arguments, flags, subcommands, help text, output formats, error messages, exit codes, prompts, config/env precedence, and safe/dry-run behavior. Use when you're designing a CLI spec (before implementation) or refactoring an existing CLI's surface area for consistency, composability, and discoverability.
- `mcp-builder` — Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
- `mkit-builder` — Build MCP servers integrating external APIs and services, including OAuth, billing, and Apps SDK UI. Not for general backend architecture; use backend-design.
- `workers-mcp` — Create production-ready Cloudflare Workers MCP servers with OAuth 2.1 authentication (Auth0), feature-based licensing (Stripe), D1 database, Durable Objects, Workers KV, and Vectorize vector search. Use when Codex needs to: (1) Scaffold a new Workers MCP project, (2) Add MCP tools with proper schemas and licensing, (3) Configure D1 database with migrations, (4) Set up Auth0 OAuth 2.1 authentication, (5) Implement Stripe subscription licensing, (6) Add Vectorize semantic search, (7) Deploy to Cloudflare Workers.

## Interview
- `architecture-interview` — Plan and review architecture decisions via a structured interview and ADR output. Use when choosing between system design alternatives.
- `bug-interview` — Analyze and review bug reports to capture repro, evidence, and next diagnostic step. Use when a bug report lacks clear reproduction.
- `interview-kernel` — Core interview engine enforcing single-question discovery/decision gating. Use when building interview wrapper skills.
- `interview-me` — Interactive, multiple-choice interview that turns an underspecified idea into a design-ready spec (decisions + assumptions + approval).
- `pm-interview` — Plan and review product scope, value, metrics, and rollout via a structured interview. Use when product direction or scope must be clarified.

## Design
- `better-icons` — Icon search/retrieval via Better Icons CLI/MCP. Use when you need to find or fetch SVG icons from Iconify libraries.

## Product
### Docs
- `agents-md` — Create or update a repository-level AGENTS.md contributor guide with clear sections, commands, and repo-specific conventions. Use when asked to draft, improve, or standardize AGENTS.md files or when a repo needs concise contributor instructions.
- `docs-expert` — Co-author, improve, and QA documentation (specs, READMEs, guides, runbooks). Trigger when user asks to create, revise, audit, or QA docs; not for implementation plans or PRDs (use code-plan or product-spec).

### Specs
- `product-spec` — Create PRDs and tech specs and critique UX flows. Not for documentation QA or implementation plans; use docs-expert or code-plan.
- `prd-clarifier` — Resolve PRD ambiguities and requirements through structured questioning and a tracked session log.
- `prd-to-accessibility` — Generate accessibility requirements and checks from PRDs.
- `prd-to-api` — Generate a full API specification from a PRD (endpoints, schemas, errors, auth, compatibility).
- `prd-to-api-lite` — Generate a minimal API outline from a PRD (endpoints, examples, basic errors).
- `prd-to-arch` — Generate an architecture specification from a PRD.
- `prd-to-arch-lite` — Generate a lite architecture snapshot from a PRD.
- `prd-to-qa-cases` — Generate QA test cases from PRD acceptance criteria.
- `prd-to-risk` — Generate a risk register and mitigation plan from a PRD.
- `prd-to-roadmap` — Generate a phased roadmap from a PRD.
- `prd-to-security-review` — Generate a security review from a PRD.
- `prd-to-testplan` — Generate a test plan and validation matrix from a PRD.
- `prd-to-ux` — Generate UX specifications from PRDs or feature specs.
- `prd-to-ui-spec` — Generate UI specs from PRDs/UX using aStudio tokens and state machines.
- `ui-spec-to-prompts` — Convert UI specs into build-order prompts for UI generators.
- `ux-spec-to-prompts` — Convert UX specs into build-order prompts for UI generators.

### Review
- `llm-design-review` — Run design reviews and audits for LLM features across UX, architecture, model/prompt, safety, evaluation, and governance. Not for product PRDs; use product-spec.
- `product-design-review` — Review end-to-end user experience and UI for products or flows; produce a user-perspective critique with usability, accessibility, content, and interaction issues plus fixes. Use for UX/UI audits, product design reviews, onboarding or checkout critiques, heuristic evaluations, accessibility-first reviews, or when asked to find issues in a user journey from the user's point of view. Target web products, including React apps and open-source software.

### Strategy
- `project-improvement-ideator` — Generate 30 pragmatic improvement ideas for the current project, weigh feasibility/impact/user perception, then winnow to the best 5 with rationale. Use when asked for “best ideas”, “improvements”, “roadmap”, or “top 5”/“winnow” prioritization. Not for full product specs or LLM design reviews; use product-spec or llm-design-review.
- `code-plan` — Create concise, actionable plans for coding tasks. Use when users ask for a plan, roadmap, or steps to implement a feature, fix, refactor, or investigation.

### Content
- `app-store-release-notes` — Create user-facing App Store release notes by collecting and summarizing all user-impacting changes since the last git tag (or a specified ref). Use when asked to generate a comprehensive release changelog, App Store "What's New" text, or release notes based on git history or tags.
- `youtube-hooks-scripts` — Create compelling hooks and full scripts for technical YouTube videos about coding and AI. Use when given a video idea, braindump, source code, or rough notes to develop into engaging long-form content. Helps transform raw material into conversational scripts that grab attention and maintain engagement throughout.
- `youtube-titles-thumbnails` — Create high-performing YouTube titles and thumbnail text that maximize CTR and virality while maintaining authenticity. Use when analyzing video transcripts to generate title and thumbnail suggestions, optimizing existing titles/thumbnails, or when users request help with YouTube content strategy for click-through rate optimization.

### Ops
- `decide-build-primitive` — Decide whether a capability should be a Skill, custom prompt, or automation agent. Not for creating or installing skills; use skill-creator or skill-installer.
- `linear` — Manage Linear issues and projects (read, create, update). Not for GitHub issue flows; use gh-issue-fix.

### Domain
- `oak-api` — Oak Curriculum API integration and learning workflows. Use when building curriculum-driven experiences.
- `oracle` — Decision arbitration and conflict resolution workflow.

### Tech
- `tech-to-data` — Generate a data specification from a tech spec.
- `tech-to-migration` — Generate a migration plan from a tech spec.
- `tech-to-ops` — Generate an ops/runbook spec from a tech spec.
- `tech-to-performance` — Generate a performance plan from a tech spec.
- `youtube-titles-thumbnails` — Create high-performing YouTube titles and thumbnail text that maximize CTR and virality while maintaining authenticity. Use when analyzing video transcripts to generate title and thumbnail suggestions, optimizing existing titles/thumbnails, or when users request help with YouTube content strategy for click-through rate optimization.

## Utilities
- `1password` — Set up and use 1Password CLI (op) for install, desktop integration, sign-in, and secret injection. Not for non-1Password secret tooling.
- `markdown-converter` — Convert documents and files to Markdown using markitdown. Use when converting PDF, Word (.docx), PowerPoint (.pptx), Excel (.xlsx, .xls), HTML, CSV, JSON, XML, images (with EXIF/OCR), audio (with transcription), ZIP archives, YouTube URLs, or EPubs to Markdown format for LLM processing or text analysis.
- `process-watch` — Monitor system processes and resources (CPU, memory, I/O, network) and manage runaway processes. Not for app-level profiling or code tuning.
- `recon-workbench` — Production-grade forensic evidence collection for software interrogation across web/React and OSS repos. Use when running rwb CLI commands (doctor, authorize, plan, run, manifest, summarize, validate), designing probe catalogs or schemas, generating evidence-backed findings, inspecting targets under authorization guardrails, or configuring scope and compliance policies.
- `remotion-best-practices` — Best practices for Remotion (React video): compositions, timing, assets, audio, captions, transitions, and Mediabunny utilities. Use when writing or reviewing Remotion code.
- `skill-creator` — Create, update, validate, or package skills and their resources. Use when a user asks to create or revise a skill, improve routing/portability, or package a skill; not for installing skills or choosing the right build primitive (use skill-installer or decide-build-primitive).
- `skill-installer` — Install skills into $CODEX_HOME/skills from curated lists or GitHub paths. Not for clawdhub.com installs or skill creation.
- `video-transcript-downloader` — Download videos, audio, subtitles, and clean paragraph-style transcripts from YouTube and any other yt-dlp supported site. Use when asked to “download this video”, “save this clip”, “rip audio”, “get subtitles”, “get transcript”, or to troubleshoot yt-dlp/ffmpeg and formats/playlists.

## Auth
- `create-auth` — Add authentication to TypeScript/JavaScript apps with Better Auth. Covers new setup, migration, env vars, core config, and framework handlers.
- `best-practices` — Better Auth integration guide covering config, database adapters, sessions, hooks, and security options.

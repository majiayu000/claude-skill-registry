---
name: codex-domain-specialist
description: Apply layered domain routing for frontend, backend, mobile, debugging, security, and specialized engineering concerns. Use to select focused reference files with strict context boundaries before implementation or review.
load_priority: on-demand
---

## TL;DR
Detect primary domain from file signals -> load matching references from routing table -> enforce max 4 references first pass. Check `.codex/profile.yaml` for fast-path. Check feedback logs for supplemental loading. Never bulk-load all references.

## Output Quality Mandate (MANDATORY)

> **Before generating ANY code, schema, API, or UI — load and apply `references/output-quality-gates.md`.** This reference is exempt from the 4-item context limit and domain isolation rules. It must be loaded on EVERY task.

This reference prevents generic, tutorial-style output by enforcing:
1. The **3-Second Rule**: 3 questions before any output.
2. Domain-specific **Quality Gates** (FE / BE / DB).
3. A **10-point Anti-Generic Checklist** after generating output.

**If your output could be copy-pasted into any random project and still work without modification, it is generic. Generic = failure. Re-think and rewrite.**

# Domain Specialist

## Activation

1. Activate when the task edits domain-specific files.
2. Activate on explicit `$codex-domain-specialist`.

## Project Profile (Fast Path)

Before running detection, check for `.codex/profile.yaml` in the project root.
If the file exists:
1. Parse `primary_domain` and map to the routing decision table directly.
2. Use `stack` entries as supplemental signals for "Load On Signal" column.
3. Skip file-extension-based detection entirely.
If the file does not exist or fails to parse:
- Fall back to the standard Detection and Routing Order below.
See: `references/project-profile-spec.md` for schema and validation rules.

## Feedback-Aware Supplemental Loading

After determining the primary domain (via profile or detection), check for recurring feedback patterns:
1. Scan `.codex/feedback/*.md` files from the last 30 days.
2. Count feedback entries by `Category` field (e.g., "database", "security", "performance").
3. If any category has 3+ entries in 30 days AND that category maps to a domain reference:
   - Auto-load that domain's reference as supplemental context.
   - Declare: `Feedback-driven load: [reference file] (N issues in 30 days)`.
4. Maximum 1 supplemental reference from feedback (highest count wins).
5. If no feedback files exist or all counts < 3, skip this step silently.

### Category to Reference Mapping

| Feedback Category | Supplemental Reference |
| --- | --- |
| frontend | `references/frontend-rules.md` |
| react | `references/react-patterns.md` |
| nextjs | `references/nextjs-patterns.md` |
| backend | `references/backend-rules.md` |
| api | `references/api-design-rules.md` |
| database | `references/database-rules.md` |
| aggregation | `references/database-aggregation.md` |
| security | `references/security-rules.md` |
| web-security | `references/web-security-deep.md` |
| auth | `references/auth-patterns.md` |
| testing | `references/testing-rules.md` |
| test-strategy | `references/testing-strategy.md` |
| performance | `references/performance-rules.md` |
| profiling | `references/performance-profiling.md` |
| accessibility | `references/accessibility-rules.md` |
| architecture | `references/architecture-rules.md` |
| integration | `references/integration-rules.md` |
| caching | `references/caching-patterns.md` |
| pagination | `references/pagination-patterns.md` |
| validation | `references/validation-patterns.md` |
| logging | `references/logging-patterns.md` |
| forms | `references/form-patterns.md` |
| creative | `references/creative-ui-ux.md` |
| creative-dev | `references/creative-development.md` |
| animation | `references/creative-ui-ux.md` |
| gsap | `references/gsap-mastery.md` |
| interactive | `references/interactive-elements.md` |
| ui-design | `references/ui-ux-design-principles.md` |
| visualization | `references/data-visualization.md` |
| vietnamese | `references/vietnamese-typography.md` |
| dates | `references/date-timezone.md` |
| export | `references/data-export.md` |
| upload | `references/file-upload.md` |
| email | `references/email-notification.md` |
| oauth | `references/oauth-social-login.md` |
| devops | `references/devops-rules.md` |
| deployment | `references/deployment-strategy.md` |

## Detection and Routing Order

Route in this exact order:

1. Detect primary domain.
2. Load primary domain references from the decision table.
3. Add only signal-driven references.
4. Enforce context boundaries before implementation or review.

## Primary Domain Detection

| Signal | Primary Domain |
| --- | --- |
| `.tsx`, `.jsx`, hooks, component, styling, UI state | React/Frontend |
| Next.js app router, server components, ISR/SSR/SSG | Next.js |
| `routes/`, `controllers/`, `services/`, `api/`, middleware | Backend API |
| schema, migration, query plan, index, transaction | Database |
| React Native, Flutter, Expo, `.swift`, `.kt` | Mobile |
| auth, secrets, crypto, authz, attack surface, vulnerability | Security |
| login, signup, JWT, refresh token, RBAC, OAuth, identity provider | Auth/Identity |
| dashboard, chart, report, aggregation, BI, analytics, export | Data/Analytics |
| unit/integration/e2e, flaky test, regression coverage | Testing |
| debug, stack trace, breakpoint, reproduce bug, root cause | Debugging |
| architecture, monolith, microservice, clean arch, DDD, SOLID, event-driven | Architecture |
| webhook, integration, third-party, API client, circuit breaker, retry | Integration |
| Docker, CI/CD, deploy, rollback, observability | DevOps |

## Context Boundary Enforcement

0. **Mandatory pre-load**: Always load `references/output-quality-gates.md` regardless of domain or context limits. This does NOT count toward the 4-item limit.
1. Max context load: load at most 4 items (references + starter templates) in the first pass. If more are needed, state clear reason and list additional files explicitly.
2. Domain isolation:
   - Frontend-only tasks (component, styling, hooks): do not load `backend-rules.md`, `database-rules.md`, or `devops-rules.md`.
   - Backend-only tasks (API, service, middleware): do not load `react-patterns.md`, `nextjs-patterns.md`, or `accessibility-rules.md`.
   - Database-only tasks (schema, migration, query): do not load `frontend-rules.md`, `mobile-rules.md`, or `seo-rules.md`.
3. Cross-domain trigger:
   - API contract change: load both `api-design-rules.md` and `backend-rules.md`.
   - Security concern detected: load `security-rules.md` regardless of primary domain.
   - Performance issue detected: load `performance-rules.md` as supplemental context.
4. Explicit declaration: whenever references are loaded, always declare:
   - `Loading: [file1], [file2]`
   - `Skipping: [reason]`

## Routing Decision Table

| Primary Domain | Always Load | Load On Signal | Never Load |
| --- | --- | --- | --- |
| React/Frontend | `frontend-rules.md`, `react-patterns.md` | `typescript-rules.md`, `accessibility-rules.md`, `css-architecture.md`, `state-management.md`, `form-patterns.md`, `data-visualization.md` | `database-rules.md`, `devops-rules.md`, `container-orchestration.md` |
| Next.js | `frontend-rules.md`, `nextjs-patterns.md` | `react-patterns.md`, `seo-rules.md`, `performance-rules.md`, `state-management.md` | `database-rules.md`, `mobile-rules.md`, `container-orchestration.md` |
| Backend API | `backend-rules.md`, `api-design-rules.md` | `database-rules.md`, `security-rules.md`, `validation-patterns.md`, `logging-patterns.md`, `error-handling-patterns.md` | `react-patterns.md`, `nextjs-patterns.md`, `seo-rules.md`, `mobile-rules.md` |
| Database | `database-rules.md` | `backend-rules.md`, `performance-rules.md`, `database-aggregation.md`, `data-migration.md`, `caching-patterns.md` | `frontend-rules.md`, `react-patterns.md`, `mobile-rules.md`, `seo-rules.md` |
| Mobile | `mobile-rules.md` | `frontend-rules.md`, `performance-rules.md`, `accessibility-rules.md`, `state-management.md` | `nextjs-patterns.md`, `seo-rules.md`, `database-rules.md`, `container-orchestration.md` |
| Security | `security-rules.md`, `web-security-deep.md` | `backend-rules.md`, `api-design-rules.md`, `auth-patterns.md` | `react-patterns.md`, `seo-rules.md`, `mobile-rules.md`, `data-visualization.md` |
| Architecture | `architecture-rules.md` | `backend-rules.md`, `database-rules.md`, `design-patterns.md`, `integration-rules.md` | `react-patterns.md`, `seo-rules.md`, `css-architecture.md` |
| Integration | `integration-rules.md`, `api-design-rules.md` | `backend-rules.md`, `security-rules.md`, `caching-patterns.md`, `message-queue-comparison.md` | `frontend-rules.md`, `mobile-rules.md`, `seo-rules.md` |
| Testing | `testing-rules.md` | domain-specific rules matching code under test | unrelated domain rules |
| Debugging | `debugging-rules.md` | `testing-rules.md`, `logging-patterns.md`, `error-handling-patterns.md` | `seo-rules.md`, `payment-integration.md`, `mobile-rules.md` |
| DevOps | `devops-rules.md` | `container-orchestration.md`, `deployment-strategy.md`, `observability.md`, `security-rules.md` | `react-patterns.md`, `mobile-rules.md`, `seo-rules.md`, `form-patterns.md` |
| Auth/Identity | `auth-patterns.md`, `security-rules.md` | `backend-rules.md`, `web-security-deep.md`, `oauth-social-login.md` | `seo-rules.md`, `data-visualization.md`, `mobile-rules.md` |
| Data/Analytics | `database-aggregation.md`, `data-visualization.md` | `database-rules.md`, `data-export.md`, `caching-patterns.md`, `performance-rules.md` | `mobile-rules.md`, `seo-rules.md`, `auth-patterns.md` |

## Specialized Signal Routing

When task signals match keywords below, add the corresponding reference. If multiple signals match, load at most 2 specialized references (pick highest relevance).

### Frontend Signals

| Signal | Add Reference |
| --- | --- |
| design tokens, color palette, spacing, CSS variables, theme, dark mode | `references/css-architecture.md` |
| chart, graph, visualization, Recharts, D3, sparkline, bar chart, pie chart | `references/data-visualization.md` |
| GSAP, Three.js, WebGL, Framer Motion, Awwwards, creative, storytelling, landing page, scrolltrigger | `references/creative-ui-ux.md` |
| creative development, art direction, breakthrough design, brand experience, experimental, unique design, wow factor, premium feel, creative archetype | `references/creative-development.md` |
| gsap.timeline, ScrollTrigger, SplitText, ScrollSmoother, Observer, Flip, MorphSVG, DrawSVG, MotionPath, scrub, pin, tween, stagger | `references/gsap-mastery.md` |
| interactive, fun, playful, hover effect, tilt card, confetti, particle, drag, ripple, Easter egg, cursor effect, magnetic button, text scramble | `references/interactive-elements.md` |
| ui design, ux design, visual hierarchy, color theory, typography pair, layout, whitespace, gestalt, aesthetics, beautiful design, shadow depth | `references/ui-ux-design-principles.md` |
| form, multi-step form, field array, form validation UX, React Hook Form | `references/form-patterns.md` |
| Redux, Zustand, Context, React Query, state management, global state | `references/state-management.md` |
| i18n, translation, locale, multi-language, RTL | `references/i18n-patterns.md` |
| tiếng việt, vietnamese, dấu, diacritics, vietnamese font, vi locale | `references/vietnamese-typography.md` |
| PWA, service worker, offline, manifest, installable | `references/pwa-patterns.md` |
| lighthouse, bundle size, web vitals, LCP, CLS, INP | `references/performance-profiling.md` |
| keyboard, focus, screen reader, WCAG, aria | `references/accessibility-rules.md` |
| canonical, sitemap, metadata, structured data, SEO | `references/seo-rules.md` |

### Backend Signals

| Signal | Add Reference |
| --- | --- |
| request validation, Joi, Zod, sanitize, input schema | `references/validation-patterns.md` |
| structured logging, correlation ID, Winston, log level | `references/logging-patterns.md` |
| queue, worker, Bull, BullMQ, cron, background job, scheduled task | `references/background-jobs.md` |
| upload, file upload, multipart, S3, presigned URL, image resize | `references/file-upload.md` |
| email, SMTP, Nodemailer, notification, in-app alert, push | `references/email-notification.md` |
| health check, readiness, liveness, graceful shutdown | `starters/health-check.js` |
| swagger, openapi, API docs, API versioning | `references/api-documentation.md` |
| error boundary, try/catch, operational error, AppError | `references/error-handling-patterns.md` |
| factory, strategy, observer, singleton, repository, adapter | `references/design-patterns.md` |

### Database Signals

| Signal | Add Reference |
| --- | --- |
| aggregation, pipeline, $group, $lookup, $facet, $unwind | `references/database-aggregation.md` |
| seed, backfill, ETL, data migration, import data | `references/data-migration.md` |
| cache, Redis, TTL, cache invalidation, cache-aside, singleflight | `references/caching-patterns.md` |
| cursor pagination, keyset, infinite scroll, offset vs cursor | `references/pagination-patterns.md` |

### Auth and Security Signals

| Signal | Add Reference |
| --- | --- |
| JWT, refresh token, session, RBAC, password hash, bcrypt | `references/auth-patterns.md` |
| OAuth, social login, Google login, GitHub login, Passport.js | `references/oauth-social-login.md` |
| CORS, CSP, CSRF, XSS, SQL injection, NoSQL injection, helmet | `references/web-security-deep.md` |
| payment, Stripe, PayPal, charge, refund, checkout, billing | `references/payment-integration.md` |

### Architecture and DevOps Signals

| Signal | Add Reference |
| --- | --- |
| monorepo, Turborepo, workspace, shared package, multi-app | `references/monorepo-patterns.md` |
| message queue, RabbitMQ, Kafka, Redis Streams, pub/sub | `references/message-queue-comparison.md` |
| event sourcing, CQRS, event store, projection, replay | `references/event-sourcing.md` |
| Kubernetes, K8s, pod, Helm, HPA, Dockerfile, multi-stage | `references/container-orchestration.md` |
| gateway, reverse proxy, load balancer, service mesh | `references/api-gateway.md` |
| metrics, Prometheus, Grafana, SLO, SLI, alerting | `references/observability.md` |
| blue-green, canary deploy, rolling update, rollback | `references/deployment-strategy.md` |
| feature flag, rollout, canary, A/B test, toggle | `references/feature-flags.md` |
| tenant, multi-tenant, SaaS, data isolation | `references/multi-tenancy.md` |

### Cross-Cutting Signals

| Signal | Add Reference |
| --- | --- |
| TypeScript generics, unions, strict typing, DTO, interface | `references/typescript-rules.md` |
| CSV, Excel, PDF, export, download, report | `references/data-export.md` |
| date, timezone, UTC, dayjs, moment, birthday, duration | `references/date-timezone.md` |
| search, filter, facet, autocomplete, debounce, URL filter | `references/search-filter.md` |
| GraphQL, query, mutation, subscription, resolver, DataLoader | `references/graphql-patterns.md` |
| git branch, PR, commit convention, release tag, changelog | `references/git-workflow.md` |
| code review, PR review, checklist, feedback | `references/code-review.md` |
| test pyramid, mock, coverage, test data factory | `references/testing-strategy.md` |
| idempotency, versioning, error envelope, REST design | `references/api-design-rules.md` |
| rerender, memo, profiling, p95 latency, memory leak | `references/performance-rules.md` |

## Common Combo Detection

When task matches a combo pattern, load the specified set instead of individual domain routing.

| Combo Pattern | Load Set (in order) |
| --- | --- |
| Build new CRUD page | `starters/react-crud-page.jsx` + `references/frontend-rules.md` + `references/validation-patterns.md` + `references/form-patterns.md` |
| Create new API endpoint | `starters/express-api.js` + `references/backend-rules.md` + `references/validation-patterns.md` + `references/api-design-rules.md` |
| Add authentication | `starters/auth-flow.js` + `references/auth-patterns.md` + `references/security-rules.md` + `references/web-security-deep.md` |
| Build dashboard with charts | `starters/dashboard-layout.css` + `references/data-visualization.md` + `references/frontend-rules.md` + `references/database-aggregation.md` |
| Export data to CSV/Excel | `references/data-export.md` + `references/database-aggregation.md` + `references/backend-rules.md` |
| Setup project from scratch | `starters/env-config.js` + `starters/docker-compose.yml` + `references/file-structure.md` + `references/git-workflow.md` |
| Implement file upload | `references/file-upload.md` + `references/backend-rules.md` + `references/security-rules.md` |
| Add real-time features | `starters/websocket-server.js` + `references/realtime-patterns.md` + `references/backend-rules.md` |
| Database optimization | `references/database-aggregation.md` + `references/caching-patterns.md` + `references/performance-rules.md` + `references/pagination-patterns.md` |
| Deploy to production | `references/deployment-strategy.md` + `references/container-orchestration.md` + `references/observability.md` + `starters/nginx.conf` |

## Operating Rules

1. Never bulk-load all references.
2. Keep first-pass load minimal and task-specific.
3. Re-check boundaries after each major step and prune irrelevant references.
4. If user task spans multiple domains, justify each added reference in the declaration.

## Signal Conflict Resolution

When multiple signals match different references:
1. Specificity wins: `pagination-patterns.md` over `api-design-rules.md` for pagination-focused questions.
2. Combo wins: if task matches a Common Combo, use the combo set instead of individual signals.
3. Deep over general: `web-security-deep.md` over `security-rules.md` for CORS/CSP/XSS-specific tasks.
4. Starter + reference: when both match, load starter (practical code) and reference (rules). Both count toward the 4-item limit.
5. Declaration required: always declare which signals triggered which references and any conflicts resolved.

## Starter Templates

When creating new features or projects, reference starter templates in `starters/` directory:

| Template | Use When |
| --- | --- |
| `design-system.css` | Starting any Frontend project; copy and customize tokens |
| `dashboard-layout.css` | Building admin/dashboard UI |
| `express-api.js` | Creating new API endpoints |
| `mongoose-model.js` | Creating new MongoDB models |
| `auth-flow.js` | Implementing authentication |
| `api-client.js` | Setting up frontend API layer |
| `react-crud-page.jsx` | Building a standard list/detail/create/edit page |
| `docker-compose.yml` | Setting up local development environment |
| `ci-pipeline.yml` | Setting up CI/CD |
| `sequelize-migration.js` | Creating database migrations (Sequelize) |
| `env-config.js` | Setting up environment variable management |
| `nginx.conf` | Setting up reverse proxy with SSL and security headers |
| `.env.example` | Template for environment variables documentation |
| `jest-setup.js` | Test config, helpers, factories |
| `react-test.jsx` | React Testing Library patterns with MSW |
| `websocket-server.js` | Socket.IO server with auth |
| `health-check.js` | K8s/Docker health endpoints |
| `graceful-shutdown.js` | SIGTERM handling, connection draining |
| `swagger-setup.js` | OpenAPI documentation |

## Starter Template Auto-Routing

When task creates new code matching patterns below, always reference the corresponding starter as a pattern source. Declare: `Starter reference: [template name]`.

| Task Pattern | Auto-Reference Starter |
| --- | --- |
| Creating new React project or first component | `starters/design-system.css` |
| Building admin panel, dashboard, or management UI | `starters/dashboard-layout.css` |
| Creating new Express/Node.js API endpoint | `starters/express-api.js` |
| Creating new Mongoose/MongoDB model | `starters/mongoose-model.js` |
| Implementing login, signup, or authentication | `starters/auth-flow.js` |
| Setting up frontend HTTP/API layer | `starters/api-client.js` |
| Building list page with table, filters, and CRUD | `starters/react-crud-page.jsx` |
| Creating Sequelize migration | `starters/sequelize-migration.js` |
| Setting up project configuration/env vars | `starters/env-config.js` + `starters/.env.example` |
| Setting up Docker or local dev environment | `starters/docker-compose.yml` |
| Setting up CI/CD pipeline | `starters/ci-pipeline.yml` |
| Setting up Nginx or reverse proxy | `starters/nginx.conf` |
| Writing tests (unit/integration) | `starters/jest-setup.js` |
| Writing React component tests | `starters/react-test.jsx` |
| Implementing WebSocket/real-time features | `starters/websocket-server.js` |
| Adding health check endpoint | `starters/health-check.js` |
| Configuring server startup/shutdown | `starters/graceful-shutdown.js` |
| Setting up API documentation | `starters/swagger-setup.js` |

Rules:
1. Reference starters as starting points; never copy blindly.
2. Adapt tokens and patterns to match existing project conventions.
3. Remove unused components from starters.
4. Load at most 1 starter per task (pick the most relevant), except Common Combo Detection entries that explicitly list more than one starter.
5. Starter counts toward the max 4-item context limit.
6. If starter conflicts with project conventions, skip it and declare reason.

## Script Invocation Discipline

1. When domain routing recommends helper scripts from other skills, run `--help` first.
2. Treat scripts as black-box helpers and execute by CLI contract before source inspection.
3. Read script source only when customization or bug fixing is required.

## Reference Files

- `references/project-profile-spec.md`: project profile schema and fast-path routing.
- `references/architecture-rules.md`: architecture and scaling decision rules.
- `references/integration-rules.md`: integration reliability and external API patterns.
- `references/caching-patterns.md`: cache-aside strategy, TTL, and invalidation rules.
- `references/pagination-patterns.md`: offset/cursor pagination decision guidance.
- `references/validation-patterns.md`: request validation and sanitization patterns.
- `references/logging-patterns.md`: structured logging and correlation id standards.
- `references/background-jobs.md`: queue and scheduled job processing patterns.
- `references/search-filter.md`: URL-driven filter and faceted search patterns.
- `references/file-upload.md`: secure upload and object-storage patterns.
- `references/email-notification.md`: email delivery and in-app notification patterns.
- `references/data-migration.md`: seed/backfill and migration safety guidance.
- `references/multi-tenancy.md`: tenant isolation and query safety patterns.
- `references/feature-flags.md`: progressive rollout and toggle management patterns.
- `references/graphql-patterns.md`: GraphQL schema/resolver and security patterns.
- `references/design-patterns.md`: common creational, structural, and behavioral patterns.
- `references/web-security-deep.md`: deep web security configuration and hardening.
- `references/i18n-patterns.md`: translation, locale, and formatting patterns.
- `references/testing-strategy.md`: test pyramid, mocking, and coverage guidance.
- `references/api-documentation.md`: OpenAPI conventions and API versioning guidance.
- `references/git-workflow.md`: branch, commit, PR, and release workflow standards.
- `references/pwa-patterns.md`: manifest/service-worker and offline patterns.
- `references/performance-profiling.md`: web vitals, bundle, and runtime profiling guidance.
- `references/deployment-strategy.md`: rollout and rollback deployment patterns.
- `references/code-review.md`: review checklist and feedback guidelines.
- `references/observability.md`: metrics, SLO/SLI, and tracing guidance.
- `references/api-gateway.md`: gateway patterns and service edge design.
- `references/event-sourcing.md`: event store and CQRS projection patterns.
- `references/container-orchestration.md`: Docker/Kubernetes deployment patterns.
- `references/payment-integration.md`: payment flow and webhook safety guidance.
- `references/data-visualization.md`: charting patterns and dashboard composition guidance.
- `references/form-patterns.md`: complex form architecture and validation UX patterns.
- `references/date-timezone.md`: UTC/timezone handling and scheduling rules.
- `references/data-export.md`: CSV/Excel export implementation and safety patterns.
- `references/oauth-social-login.md`: OAuth social login integration and security guidance.
- `references/monorepo-patterns.md`: workspace structure and shared package conventions.
- `references/message-queue-comparison.md`: broker selection and queue pattern guidance.
- `references/database-aggregation.md`: MongoDB aggregation pipeline and analytics patterns.
- `references/accessibility-rules.md`: accessibility standards, semantic patterns, and WCAG-aligned implementation.
- `references/api-design-rules.md`: API contract design, versioning, and idempotency patterns.
- `references/auth-patterns.md`: authentication and authorization implementation guidance.
- `references/backend-rules.md`: backend architecture, service boundaries, and API implementation rules.
- `references/css-architecture.md`: CSS structure, design tokens, and styling system conventions.
- `references/database-rules.md`: database schema, query, and migration core rules.
- `references/debugging-rules.md`: debugging workflow, hypothesis-driven investigation, and root-cause practices.
- `references/devops-rules.md`: CI/CD, deployment reliability, and operational safeguards.
- `references/error-handling-patterns.md`: consistent error taxonomy and handling patterns.
- `references/file-structure.md`: repository and module structure conventions.
- `references/frontend-rules.md`: frontend architecture and UI engineering baseline rules.
- `references/mobile-rules.md`: mobile app architecture and performance/security constraints.
- `references/nextjs-patterns.md`: Next.js routing, rendering, and data-fetching patterns.
- `references/performance-rules.md`: performance budgets, profiling, and optimization priorities.
- `references/react-patterns.md`: React composition, hooks usage, and state patterns.
- `references/realtime-patterns.md`: realtime communication patterns (polling/SSE/WebSocket).
- `references/security-rules.md`: baseline security controls and threat mitigation practices.
- `references/seo-rules.md`: SEO technical implementation and discoverability patterns.
- `references/state-management.md`: client state modeling and store selection patterns.
- `references/testing-rules.md`: unit/integration/e2e testing baseline standards.
- `references/typescript-rules.md`: TypeScript strictness, typing conventions, and API typing patterns.
- `references/vietnamese-typography.md`: Vietnamese font selection, UTF-8 encoding, diacritics handling, and locale-aware text processing.
- `references/creative-ui-ux.md`: Advanced UI/UX, GSAP orchestration, Three.js integration, storytelling flow, and creative design principles.
- `references/ui-ux-design-principles.md`: Visual hierarchy, Gestalt principles, color theory, typography scales, whitespace strategy, optical alignment, and developer design anti-patterns.
- `references/gsap-mastery.md`: GSAP core architecture, easing, ScrollTrigger, SplitText, ScrollSmoother, Observer, Flip, MorphSVG, DrawSVG, MotionPath, performance, React integration, and creative recipes.
- `references/interactive-elements.md`: Fun interactive UI elements: custom cursors, tilt cards, magnetic buttons, confetti, particles, text scramble, hover effects, drag/swipe, Easter eggs.
- `references/creative-development.md`: Creative Director's Brain — Creative Brief Decoder, 7 archetypes, experimental typography, glow/neon systems, purpose-driven animation, differentiation playbook, conversion-focused creative.
- `references/output-quality-gates.md`: **MANDATORY** — Anti-generic guardrails: 3-Second Rule, FE/BE/DB Quality Gates, 10-point Anti-Generic Checklist, Why Mandate, Framework Defaults Override.

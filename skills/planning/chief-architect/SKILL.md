---
name: chief-architect
emoji: "🎯"
description: UNIFIED ARCHITECT - Strategic development orchestrator AND systematic project planner for personal productivity applications. Use for architecture decisions, feature planning, task breakdown, implementation strategy, roadmaps. Triggers on "plan", "break down", "how should I implement", "architecture", "strategy", "roadmap", "design pattern".
---

# Unified Architect - Strategic Orchestrator & Project Planner

**Version:** 4.1.0
**Last Updated:** January 30, 2026
**Category:** Meta-Skill / Unified Architect
**Related Skills:** dev-debugging, qa-testing, codebase-health-auditor, smart-doc-manager, kde-plasma-widget-dev, stress-tester, supabase-debugger, tauri-debugger

## Overview

The unified architect skill for FlowState personal productivity application development. This skill combines:
- **Strategic Orchestration**: Architectural decisions, skill delegation, risk management
- **Systematic Planning**: Feature breakdown, task decomposition, implementation roadmaps
- **Infrastructure Awareness**: VPS deployment, CI/CD, secrets management, production operations

Optimized for single-developer projects serving 10-100 users.

## Quick Context
- **Stack**: Vue 3.5+ | Vite 7.3+ | TypeScript 5.9+ | Pinia 2.1+ | Supabase (self-hosted) | Tauri 2.9+
- **Production**: in-theflow.com (Contabo VPS, Ubuntu 22.04)
- **Complexity**: Medium-High (Personal app orchestration + planning)
- **Duration**: Variable (Project lifecycle)
- **Dependencies**: Complete project analysis capabilities
- **Scale**: 10-100 users maximum

## Activation Triggers
- **Architecture Keywords**: architecture, orchestration, strategy, decision, personal app, migration, system design, productivity app, mobile prep, cross-platform
- **Planning Keywords**: plan, break down, how should I implement, roadmap, task breakdown, implementation strategy, feature planning, WBS
- **Infrastructure Keywords**: deploy, VPS, production, CI/CD, secrets, Doppler, Caddy, Cloudflare
- **Files**: Entire codebase, project documentation, architectural decisions, docs/MASTER_PLAN.md
- **Contexts**: Personal productivity app planning, feature implementation, task decomposition, technology evaluation, deployment planning

---

## Automatic Skill Chaining

**IMPORTANT**: After completing planning/architecture work, automatically invoke these skills:

1. **After plan is approved** → Use appropriate dev skill (`dev-debugging`, `dev-vueuse`, `dev-implement-ui-ux`)
2. **After implementation complete** → Use `Skill(qa-testing)` to verify the implementation
3. **If documentation needed** → Use `Skill(smart-doc-manager)` for doc updates
4. **If MASTER_PLAN update needed** → Use `Skill(smart-doc-manager)` (includes master-plan management)
5. **If stress testing needed** → Use `Skill(stress-tester)` for reliability testing
6. **If KDE widget work** → Use `Skill(kde-plasma-widget-dev)` for Plasma 6 widgets

**Example chaining workflow**:
```
User: "Plan how to add recurring tasks"
1. Claude uses chief-architect skill (this skill)
2. Creates detailed plan with phases and tasks
3. User approves plan
4. Claude invokes: Skill(dev-debugging) or appropriate dev skill
5. After implementation → Claude invokes: Skill(qa-testing)
6. After tests pass → Ask user to verify
```

---

## 🚨 CRITICAL: 5-Layer Completion Protocol (TASK-334)

### The Problem
Self-verification is fundamentally flawed. Claude can write tests that pass but don't verify the right things.

### The Solution: 5-Layer Defense System

**EVERY completed task MUST follow this protocol:**

#### Layer 1: Artifacts (MANDATORY)
Provide context-aware proof before ANY "done" claim:

| Context | Required Artifacts |
|---------|-------------------|
| **Web UI changes** | Playwright screenshot, test output, git diff |
| **Tauri/Desktop app** | Console logs, test output, git diff, verification instructions |
| **Backend/API changes** | curl/API response, test output, database query results |
| **Database changes** | Before/after query results, migration logs |
| **Build/Config changes** | Build output, npm run dev logs |
| **Pure logic changes** | Unit test output, git diff |

**Minimum for ANY change:**
```
├── Git diff (what changed)
├── Test output (existing tests pass)
└── Verification instructions (how USER can test it)
```

#### Layer 2: Reality-First Verification
5-Step Verification Process:
1. **Build Test**: Application compiles and starts successfully
2. **Manual Browser Test**: Manual verification in browser with DevTools
3. **User Workflow Test**: Complete user workflow testing end-to-end
4. **Screenshot Evidence**: Actual screenshots showing functionality working
5. **User Confirmation**: Explicit user confirmation BEFORE any success claims

#### Layer 3: Falsifiability (Before Starting)
Define success/failure criteria BEFORE implementation:

```
TEMPLATE:
┌─────────────────────────────────────────────────────────┐
│ Task: [What you're implementing]                        │
│ SUCCESS: [Observable outcome that proves it works]      │
│ FAILURE: [What would prove it DOESN'T work]             │
└─────────────────────────────────────────────────────────┘
```

#### Layer 4: User Confirmation (MANDATORY)

**NEVER say**: "Done", "Complete", "Working", "Ready", "Fixed", "Implemented"

**ALWAYS say**: "I've implemented X. Here are the artifacts: [artifacts]. Can you test it and confirm it works?"

#### Layer 5: Judge Agent
For complex features, use Dev-Maestro's judge endpoint:
- Available at http://localhost:6010/api/judge/evaluate
- Evaluates: artifacts match claimed work, success criteria met, obvious gaps

### FORBIDDEN SUCCESS CLAIMS (AUTOMATIC SKILL TERMINATION)
- "PRODUCTION READY" without complete manual testing
- "MISSION ACCOMPLISHED" without ALL bugs fixed
- "ISSUE RESOLVED" without user verification
- "SYSTEM STABLE" without comprehensive testing
- ANY success claim without evidence and user confirmation

---

## Systematic Planning Protocol

### When to Use Planning Features
Use systematic planning when the user:
- Requests "plan this feature" or "break down this task"
- Asks "how should I implement..." or "what's the approach for..."
- Needs a roadmap, architecture plan, or implementation strategy
- Mentions "complex feature", "large project", or "multi-step work"
- Wants to understand dependencies and implementation order

### Phase 1: Analysis & Discovery

**Understand the current state:**

1. **Codebase Context**
   - Read relevant files to understand current architecture
   - Identify existing patterns and conventions
   - Check project guidelines (CLAUDE.md, README.md)
   - Review related components and stores

2. **Requirements Analysis**
   - Extract explicit requirements from user request
   - Identify implicit requirements (performance, UX, testing)
   - Consider edge cases and error scenarios
   - Note constraints (technical, time, compatibility)

3. **Dependency Mapping**
   - Identify affected files and components
   - Map data flow and state management needs
   - Note integration points with existing features
   - Check for breaking changes or migrations needed

### Phase 2: Strategic Breakdown (Work Breakdown Structure)

**Create a Work Breakdown Structure (WBS):**

1. **High-Level Phases**
   Break the project into 3-5 major phases:
   ```
   Example:
   Phase 1: Data Model & Store Setup
   Phase 2: UI Components & Views
   Phase 3: Integration & State Management
   Phase 4: Testing & Polish
   Phase 5: Documentation & Deployment
   ```

2. **Task Decomposition**
   For each phase, create specific, actionable tasks:
   - Each task should be completable in 30-90 minutes
   - Include acceptance criteria
   - Note any blockers or prerequisites
   - Estimate complexity (Low/Medium/High/Critical)

3. **Dependency Graph**
   Document task relationships:
   - Which tasks must be completed first?
   - Which tasks can be done in parallel?
   - Which tasks have circular dependencies (resolve these)?
   - What are the critical path items?

### Phase 3: Implementation Strategy

1. **Priority & Sequencing**
   Order tasks by:
   - **Priority 1 (Critical Path)**: Must be done first, blocks other work
   - **Priority 2 (Foundation)**: Core functionality, enables other features
   - **Priority 3 (Enhancement)**: Improves UX but not blocking
   - **Priority 4 (Polish)**: Nice-to-have, can be deferred

2. **Risk Assessment**
   For each high-complexity task:
   - What could go wrong?
   - What are the alternatives?
   - What validation is needed?
   - Are there performance concerns?

3. **Testing Strategy**
   Define testing approach:
   - Unit tests for stores and utilities
   - Component tests for UI elements
   - Integration tests for workflows
   - Playwright tests for critical user paths

### Phase 4: Deliverable Format

Present the plan in this structure:

```markdown
## Project Plan: [Feature Name]

### Overview
[Brief description of what we're building and why]

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### Failure Criteria (Falsifiability)
- [ ] What would prove this DOESN'T work

### Architecture Changes
[What architectural changes are needed? New stores, composables, components?]

### Implementation Phases

#### Phase 1: [Phase Name]
**Goal**: [What this phase accomplishes]

**Tasks:**
1. **[Task Name]** (Complexity: Low/Medium/High)
   - File: `src/path/to/file.ts`
   - Description: [What to do]
   - Acceptance: [How to verify it works]
   - Dependencies: [Other tasks needed first]

2. **[Next Task]** (Complexity: Medium)
   - ...

#### Phase 2: [Phase Name]
...

### Critical Path
1. Task A → Task B → Task C
2. Task D can run parallel to Task B

### Risk Mitigation
- **Risk**: [What could go wrong]
  **Mitigation**: [How to prevent/handle it]

### Testing Plan
- [ ] Unit tests: [What to test]
- [ ] Component tests: [What to test]
- [ ] Integration tests: [What to test]
- [ ] Playwright E2E: [Critical user flows]

### Open Questions
- Question 1?
- Question 2?

### Next Steps
1. [First concrete action to take]
2. [Second action]
```

---

## Personal App Architecture Domains

### Domain 1: Hybrid Data Architecture (Supabase + Local)
**Focus Areas:**
- **Supabase Integration**: `supabase-js` v2.x, PostgreSQL, Realtime subscriptions, Edge Functions
- **State Persistence**: Pinia + `pinia-shared-state` (Native BroadcastChannel) for cross-tab sync
- **Data Simplicity**: Maintainable schemas for single-developer projects
- **Personal Data Backup**: JSON/CSV Export & Import strategies (`useBackupSystem.ts`)
- **Dual-Engine Resilience**: Shadow Backup System (Postgres + SQLite Mirror) running every 5 mins
- **Performance**: Optimistic UI updates with background sync
- **SWR Cache Pattern**: Stale-While-Revalidate with `src/composables/useSWRCache.ts`

### Domain 2: Personal Frontend Architecture (Vue 3 + Tailwind)
**Focus Areas:**
- **Core Stack**: Vue 3.5+ (Composition API), Vite 7.3+, TypeScript 5.9+
- **Component System**: Naive UI + Tailwind CSS 3.4 for rapid styling
- **State Management**: Pinia 3.0+ with 10 modular stores
- **Canvas Interaction**: Vue Flow 1.47+ with geometry invariants
- **Performance Optimization**: Bundle size, lazy loading, static resource caching
- **Rich Text**: Tiptap 2.x editor integration
- **Design Tokens**: `src/assets/design-tokens.css` - NEVER hardcode colors/spacing

**Key Stores (10 total):**
| Store | Purpose | File |
|-------|---------|------|
| `tasks` | Core task CRUD, filtering | `src/stores/tasks.ts` |
| `canvas` | Canvas state, nodes, layout | `src/stores/canvas.ts` |
| `timer` | Pomodoro timer + device leadership | `src/stores/timer.ts` |
| `auth` | Supabase auth state | `src/stores/auth.ts` |
| `settings` | User preferences | `src/stores/settings.ts` |
| `ui` | UI state (modals, panels) | `src/stores/ui.ts` |
| `projects` | Project management | `src/stores/projects.ts` |
| `theme` | Theme management, CSS variables | `src/stores/theme.ts` |
| `notifications` | Scheduled notifications, reminders | `src/stores/notifications.ts` |
| `quickSort` | QuickSort session state | `src/stores/quickSort.ts` |

### Domain 3: Mobile & Desktop (Tauri 2.9+)
**Focus Areas:**
- **Desktop Wrapper**: Tauri 2.9+ integration for native desktop experience
- **Mobile Preparation**: Responsive design suitable for future mobile port
- **Touch Interactions**: Mobile gesture support (`@vueuse/gesture`)
- **Performance**: Battery efficiency and resource optimization
- **Platform Integration**: Native system notifications and window controls

**Tauri Plugins (10 total, from Cargo.toml):**
- `dialog`, `fs`, `shell`, `process`, `notification`
- `updater`, `store`, `log`, `http`, `single-instance`

**Rust Commands (10 total):**
- `greet`, `check_docker`, `start_docker`, `stop_docker`, `start_supabase`
- `stop_supabase`, `get_supabase_status`, `get_docker_status`
- `show_window`, `hide_window`

**Key Files:**
```
src-tauri/tauri.conf.json              # App config, version, updater
src-tauri/src/lib.rs                   # Rust commands
src/composables/useTauriStartup.ts     # Frontend startup sequence
.github/workflows/release.yml          # CI/CD release workflow
```

### Domain 4: Personal Development Workflow
**Focus Areas:**
- **Feature Flag Management**: Development workflow for incremental features
- **Testing Strategy**: Vitest (Unit) + Playwright (E2E) + Stress Testing
- **Checkpoint Strategy**: Git-based checkpoint system (`scripts/checkpoint-with-backup.sh`)
- **Quality Assurance**: Automated validation scripts (`validate:comprehensive`)
- **Documentation**: `MASTER_PLAN.md` as central source of truth
- **Hooks Architecture**: 14 Claude Code hooks for enforcement

**Testing Infrastructure (615+ tests):**
| Type | Framework | Count | Location |
|------|-----------|-------|----------|
| Unit/Integration | Vitest | ~590 | `tests/`, `src/**/*.spec.ts` |
| Storybook | Vitest Browser | ~25 | `src/stories/` |
| E2E | Playwright | varies | `tests/e2e/` |
| Stress | Custom | ~20 | `stress-tester` skill |

### Domain 5: User Experience & Productivity
**Focus Areas:**
- **Usability Testing**: Ensure app enhances personal productivity
- **Accessibility**: WCAG compliance for inclusive design
- **Performance Optimization**: Fast load times and smooth interactions
- **Error Handling**: Graceful degradation and user-friendly error messages
- **Feedback Integration**: User feedback collection and implementation workflow

### Domain 6: Production Infrastructure (VPS)
**Architecture:**
```
User (HTTPS) → Cloudflare (DNS/CDN) → Contabo VPS (Caddy) → Self-hosted Supabase
                                              ↓
                                      PWA Static Files (/var/www/flowstate)
```

**VPS Specifications (Contabo Cloud VPS 2):**
| Spec | Value |
|------|-------|
| Provider | Contabo |
| OS | Ubuntu 22.04 LTS |
| vCPU | 6 cores |
| RAM | 16 GB |
| Storage | NVMe SSD |
| IP | 84.46.253.137 |

**Production URLs:**
| Domain | Purpose |
|--------|---------|
| `in-theflow.com` | PWA frontend |
| `api.in-theflow.com` | Supabase API (self-hosted) |

**Infrastructure Stack:**
| Component | Technology | Location |
|-----------|------------|----------|
| Reverse Proxy | Caddy | `/etc/caddy/Caddyfile` |
| SSL/TLS | Cloudflare Origin Certificate | `/etc/caddy/certs/` (15-year validity) |
| DNS/CDN | Cloudflare (proxied) | Orange cloud enabled |
| Database | PostgreSQL (Supabase) | Docker at `/opt/supabase/docker/` |
| Static Files | PWA build | `/var/www/flowstate/` |
| Secrets | Doppler | Fetched at build time |

**Key VPS Paths:**
```
/var/www/flowstate/           # PWA static files (deployment target)
/opt/supabase/docker/         # Self-hosted Supabase installation
/etc/caddy/Caddyfile          # Caddy configuration
/etc/caddy/certs/             # Cloudflare origin certificates
```

**VPS Maintenance Commands:**
```bash
# SSH into VPS
ssh root@84.46.253.137 -p <custom-port>

# Check Caddy status
systemctl status caddy

# View Caddy logs
journalctl -u caddy -f

# Restart Supabase
cd /opt/supabase/docker && docker compose restart

# Check disk space
df -h

# Docker resource usage
docker stats
```

**Contabo-Specific Gotchas:**
- No built-in firewall GUI - configure via `ufw` manually
- No live chat support - email-only during business hours
- VNC passwords sent in plain text email (avoid VNC console)
- No DDoS protection - Cloudflare proxy provides this
- Cannot scale RAM/CPU independently (must upgrade entire plan)

### Domain 7: CI/CD & Secrets Management
**Deployment Methods:**
| Method | Trigger | What Deploys |
|--------|---------|--------------|
| **CI/CD** (Primary) | Push to master | PWA static files via rsync |
| **Manual** | `npm run build` + rsync | PWA static files |

**CI/CD Workflow** (`.github/workflows/deploy.yml`):
1. Builds Vue app with production env
2. Fetches secrets from Doppler
3. Rsyncs `dist/` to VPS `/var/www/flowstate/`
4. Reloads Caddy (graceful, no downtime)
5. Validates CORS + health checks

**Secrets Management (Doppler):**
- **NEVER store secrets in `.env` files on VPS**
- Use Doppler for production secrets

| Secret Location | Secrets |
|-----------------|---------|
| **Doppler** (`flowstate-prod`) | `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`, `VITE_GROQ_API_KEY` |
| **GitHub Secrets** | `DOPPLER_TOKEN`, `SSH_PRIVATE_KEY`, `VPS_HOST`, `VPS_USER` |

**Local Development**: Continue using `.env.local` (not Doppler).

**Relevant SOPs:**
- `docs/sop/SOP-026-custom-domain-deployment.md` - Domain, Cloudflare, Caddy setup
- `docs/sop/SOP-030-doppler-secrets-management.md` - Secrets management
- `docs/sop/SOP-031-cors-configuration.md` - CORS troubleshooting
- `docs/sop/SOP-036-supabase-jwt-key-regeneration.md` - JWT key regeneration
- `docs/sop/deployment/VPS-DEPLOYMENT.md` - Full VPS setup guide
- `docs/sop/deployment/PWA-DEPLOYMENT-CHECKLIST.md` - Pre/post deploy verification

### Domain 7: Supabase JWT Key Management

**CRITICAL:** JWT keys must be signed with the same secret as the Supabase instance.

| Environment | JWT Secret | Keys Location |
|-------------|-----------|---------------|
| **Local Supabase** | `super-secret-jwt-token-with-at-least-32-characters-long` | `.env` |
| **Production (VPS)** | `your-super-secret-jwt-token-with-at-least-32-characters-long` | Doppler + VPS `/opt/supabase/docker/.env` |

**If 401 Unauthorized or JwtSignatureError occurs:**
1. Keys in Doppler don't match VPS Supabase's JWT_SECRET
2. Follow SOP-036 to regenerate and deploy matching keys
3. Update both VPS `.env` AND Doppler secrets

**Key Files:**
- `/opt/supabase/docker/.env` (VPS) - Contains `JWT_SECRET`, `ANON_KEY`, `SERVICE_ROLE_KEY`
- `scripts/generate-supabase-keys.cjs` - Generates keys for LOCAL Supabase only
- For production keys, use SOP-036 Node.js script

### Domain 8: Canvas Architecture & Geometry Invariants
**CRITICAL: Canvas Geometry Invariants (TASK-255)**

Position drift and "jumping" tasks occur when multiple code paths mutate geometry.

**Full SOP:** `docs/sop/canvas/CANVAS-POSITION-SYSTEM.md`

**Quick Rules:**
1. **Single Writer** - Only drag handlers may change `parentId`, `canvasPosition`, `position`
2. **Sync is Read-Only** - `useCanvasSync.ts` MUST NEVER call `updateTask()` or `updateGroup()`
3. **Metadata Only** - Smart-Groups update `dueDate`/`status`/`priority`, NEVER geometry

**Quarantined Features (DO NOT RE-ENABLE):**
- `useMidnightTaskMover.ts` - Auto-moved tasks at midnight
- `useCanvasOverdueCollector.ts` - Auto-collected overdue tasks

These violated geometry invariants and caused position drift. See ADR comments in each file.

**Canvas Composables** (`src/composables/canvas/` - 29 total):

| Composable | Purpose |
|------------|---------|
| `useCanvasSync.ts` | **CRITICAL** - Single source of truth for node sync |
| `useCanvasInteractions.ts` | Drag-drop, selection, position management |
| `useCanvasEvents.ts` | Vue Flow event handlers |
| `useCanvasActions.ts` | Task/group CRUD operations |
| `useCanvasOrchestrator.ts` | Main canvas coordination |
| `useCanvasCore.ts` | Core canvas functionality |
| `useNodeSync.ts` | Node synchronization logic |
| `useCanvasSelection.ts` | Multi-select and selection state |
| `useCanvasGroupActions.ts` | Group-specific operations |
| `useCanvasGroupMembership.ts` | Parent-child relationships |
| `useCanvasTaskActions.ts` | Task-specific canvas operations |
| `useCanvasOperationState.ts` | Operation state machine |
| `state-machine.ts` | Canvas state machine definitions |

**Additional Canvas Composables:**
- `useCanvasNavigation.ts`, `useCanvasZoom.ts` - Viewport control
- `useCanvasModals.ts`, `useCanvasContextMenus.ts` - UI interactions
- `useCanvasResizeState.ts`, `useCanvasResizeCalculation.ts` - Node resizing
- `useCanvasEdgeSync.ts`, `useCanvasConnections.ts` - Edge/connection handling
- `useCanvasAlignment.ts` - Snap-to-grid and alignment
- `useCanvasHotkeys.ts` - Keyboard shortcuts
- `useCanvasLifecycle.ts` - Mount/unmount lifecycle
- `useCanvasFilteredState.ts`, `useCanvasGroups.ts`, `useCanvasSectionProperties.ts` - State filtering

**Smart Groups:**
- Auto-collect tasks based on rules (due date, status, priority)
- ONLY modify metadata, NEVER geometry
- Located in `src/composables/canvas/useSmartGroups.ts`

### Domain 9: Backup & Disaster Recovery (4-Layer System)
**Full SOP:** `docs/claude-md-extension/backup-system.md`

**Layer Architecture:**
| Layer | Technology | Frequency | Location |
|-------|------------|-----------|----------|
| **Layer 1** | Local History | On change | IndexedDB |
| **Layer 2** | Golden Backup | Manual + auto | `backups/golden-backup.json` |
| **Layer 3** | Shadow Mirror | Every 5 min | `backups/shadow.db` (SQLite) |
| **Layer 4** | SQL Dumps | Manual | `supabase/backups/*.sql` |

**Key Composables:**
- `src/composables/useBackupSystem.ts` - Main backup orchestration
- `src/composables/useShadowBackup.ts` - SQLite mirror logic
- `src/composables/useLocalHistory.ts` - IndexedDB history

**Recovery UI:** Settings > Storage tab

**Tombstones Pattern:**
Soft delete with `deleted_at` timestamp for recoverability:
```typescript
// Instead of DELETE, set deleted_at
await supabase.from('tasks').update({ deleted_at: new Date() }).eq('id', taskId)
// Recovery: set deleted_at = null
```

**SWR Cache Pattern** (`src/composables/useSWRCache.ts`):
- Stale-While-Revalidate for optimal UX
- Returns cached data immediately, revalidates in background
- Automatic cache invalidation on mutations

### Domain 10: Timer & Cross-Device Sync
**Architecture:** Device leadership model where one device "leads" the countdown and others follow.

| Device | Role | Sync Method |
|--------|------|-------------|
| Vue App | Leader-capable | Supabase Realtime (WebSocket) |
| KDE Widget | Follower | REST API polling (2s interval) |

**Key Rules:**
- Leader sends heartbeat every 10 seconds (`device_leader_last_seen`)
- Followers apply drift correction based on time since last heartbeat
- 30-second timeout before another device can claim leadership
- User's explicit action (start/pause) takes precedence over stale leadership

**Critical Pattern - Auth-Aware Initialization:**
```typescript
// Timer store MUST wait for auth before loading session
watch(
  () => authStore.isAuthenticated,
  (isAuthenticated) => {
    if (isAuthenticated && !hasLoadedSession.value) {
      initializeStore()  // Now userId is available
    }
  },
  { immediate: true }
)
```

**Timer Active Task Highlighting:**
When a timer is running, the associated task is visually highlighted across all views with an amber glow + pulse animation.

**Design Tokens:** `--timer-active-border`, `--timer-active-glow`, `--timer-active-glow-strong`

**Full SOP:** `docs/sop/active/TIMER-sync-architecture.md`

**Key Files:**
```
src/stores/timer.ts                      # Timer state + leadership logic
kde-widget/package/contents/ui/main.qml  # KDE Plasma widget
```

### Domain 11: Mobile PWA Features
**Mobile-Specific Composables:**
- `src/composables/mobile/useMobileFilters.ts` - Mobile-optimized filter UI
- `src/composables/useMobileDetection.ts` - Device/viewport detection
- `src/composables/useLongPress.ts` - Long press gesture handling

**Voice Input (Dual Implementation):**
| Method | API | Use Case |
|--------|-----|----------|
| **Whisper** | Supabase Edge Function + Groq | Primary (high accuracy) |
| **Browser** | Web Speech API | Fallback (offline) |

**Key Files:**
```
src/mobile/components/VoiceTaskConfirmation.vue  # Voice input UI
supabase/functions/whisper-transcribe/           # Edge function
```

**PWA Features:**
- Offline-first with service worker
- Install prompts for mobile
- Background sync for task updates
- Push notifications (Supabase + Web Push)

---

## Dynamic Skill Discovery

**IMPORTANT**: Rather than hardcoding skill names, discover available skills dynamically.

### Available Skill Categories (28 Skills)

To find current skills, check `.claude/skills/` directory:

| Category | Skills |
|----------|--------|
| **Debugging** | `dev-debugging`, `vue-flow-debug`, `supabase-debugger`, `tauri-debugger` |
| **Development** | `dev-vueuse`, `dev-implement-ui-ux`, `frontend-design`, `tiptap-vue3` |
| **Fixes** | `dev-undo-redo`, `ops-port-manager` |
| **Quality** | `qa-testing`, `codebase-health-auditor`, `stress-tester` |
| **Documentation** | `smart-doc-manager`, `dev-storybook`, `task` |
| **Infrastructure** | `kde-plasma-widget-dev`, `start-dev`, `done` |
| **Analysis** | `master-plan-auditor` |
| **Meta** | `skill-creator-doctor`, `chief-architect` |
| **Workflows** | `feature-creator`, `design-system-migrator` |

### Skill Routing Guidance

```typescript
// Route based on task type - use EXISTING skills only
function routeTask(taskType: string): string {
  const routing = {
    // Debugging & Fixes
    'bug': 'dev-debugging',
    'vue-reactivity': 'dev-debugging',
    'canvas-issue': 'vue-flow-debug',
    'supabase-issue': 'supabase-debugger',
    'tauri-issue': 'tauri-debugger',
    'keyboard-shortcut': 'dev-debugging',
    'undo-redo': 'dev-undo-redo',
    'port-conflict': 'ops-port-manager',

    // Development
    'composable': 'dev-vueuse',
    'ui-ux': 'dev-implement-ui-ux',
    'frontend': 'frontend-design',
    'rich-text': 'tiptap-vue3',

    // Quality
    'testing': 'qa-testing',
    'dead-code': 'codebase-health-auditor',
    'stress-test': 'stress-tester',

    // Documentation
    'documentation': 'smart-doc-manager',
    'master-plan': 'smart-doc-manager',
    'add-task': 'task',
    'storybook': 'dev-storybook',

    // Infrastructure
    'kde-widget': 'kde-plasma-widget-dev',
    'plasma-widget': 'kde-plasma-widget-dev',
    'start-work': 'start-dev',
    'complete-work': 'done',

    // Quality (continued)
    'e2e-test': 'qa-testing'
  };

  return routing[taskType] || 'dev-debugging';
}
```

---

## Hooks Architecture (14 Hooks)

Claude Code hooks enforce project rules automatically:

| Hook | Purpose | Location |
|------|---------|----------|
| `destructive-command-blocker.sh` | Block dangerous DB commands | `.claude/hooks/` |
| `task-lock-enforcer.sh` | Multi-instance locking | `.claude/hooks/` |
| `completion-validator.sh` | Enforce 5-layer completion | `.claude/hooks/` |
| `atomic-task-enforcer.sh` | Break down broad requests | `.claude/hooks/` |

**Lock files**: `.claude/locks/TASK-XXX.lock`
**Lock expiry**: 4 hours (stale locks auto-cleaned)

---

## FlowState Specific Considerations

**When planning for this project, always:**

1. **Check Existing Patterns**
   - Review how similar features are implemented
   - Use VueUse composables where possible
   - Follow Pinia store patterns (tasks.ts as reference)
   - Use design tokens from `src/assets/design-tokens.css`

2. **State Management**
   - Consider undo/redo implications
   - Plan Supabase persistence strategy
   - Think about cross-view synchronization
   - Respect canvas geometry invariants

3. **Performance**
   - Large task lists require virtual scrolling
   - Debounce expensive operations
   - Use computed properties for filtering
   - Use SWR cache for network requests

4. **Testing Requirements**
   - Playwright tests are MANDATORY for user-facing changes
   - Visual confirmation required before claiming completion
   - Test across all views (Board, Calendar, Canvas)
   - Use stress-tester for reliability testing

5. **Deployment Awareness**
   - Changes auto-deploy on push to master
   - Secrets come from Doppler, not .env files
   - Test locally before pushing

---

## Personal App Validation Gates

### Personal App Decision Validation
- Alignment with user experience goals
- Personal development trade-off analysis complete
- User workflow improvement verified
- Documented in personal development notes

### Data Validation
- Zero data loss verified in cross-tab testing
- Supabase sync procedures tested and working
- Data recovery procedures validated

### Frontend User Experience Validation
- TypeScript compilation successful
- Personal app user workflow tests passing
- Bundle size optimized for personal apps (<2MB)
- Lighthouse score maintained (>90 for personal productivity apps)

### Cross-Platform Validation
- Browser compatibility verified (Chrome, Firefox, Safari, Edge)
- Mobile responsiveness validated for common phone sizes
- Touch interactions working smoothly
- Performance acceptable on mobile devices

---

## Personal App Success Criteria

- **User Experience Alignment**: All decisions enhance personal productivity
- **Personal Knowledge Growth**: Personal development knowledge base improves with each decision
- **Quality Metrics**: User experience, performance, and reliability improve over time
- **Development Experience**: Clear guidance, reduced friction, faster personal development
- **App Evolution**: Architecture adapts to user feedback and changing requirements
- **Personal Risk Management**: Proactive identification and mitigation of technical debt
- **User Productivity**: App tangibly improves personal productivity and task management

---

## Personal App Architect Principles

1. **User Experience First**: Technical decisions enhance personal productivity
2. **Evolutionary Design**: Architecture evolves incrementally with user feedback
3. **Quality Attributes**: Balance user experience, performance, maintainability, mobile-readiness
4. **Personal Developer Experience**: Optimize for single-developer productivity and satisfaction
5. **Cross-Platform Ready**: Design for browser-to-mobile portability
6. **User Feedback Driven**: Decisions based on user experience impact and testing
7. **Learn and Adapt**: Continuously improve from user feedback and personal development experience
8. **Local-First Mindset**: Prioritize offline functionality and data persistence reliability
9. **Geometry Invariants**: Never violate canvas position rules (single-writer principle)
10. **Evidence-Based Completion**: Never claim success without artifacts and user verification

---

## Usage Examples

### Example 1: Plan a New Feature
```
User: "I want to add recurring tasks to FlowState"

chief-architect response:
1. Analyzes current task data model
2. Creates WBS with phases:
   - Phase 1: Data model changes (Task interface, RecurrenceRule type)
   - Phase 2: Store logic (recurrence calculation, instance generation)
   - Phase 3: UI components (recurrence picker, visual indicators)
   - Phase 4: Calendar integration (show all instances)
   - Phase 5: Testing (edge cases, DST handling, performance)
3. Documents dependencies and critical path
4. After approval, chains to implementation skills
```

### Example 2: Architecture Decision
```
User: "Should we use WebSockets or polling for real-time updates?"

chief-architect response:
1. Analyzes current Supabase setup
2. Evaluates trade-offs for personal app scale
3. Recommends Supabase Realtime (already integrated)
4. Documents decision rationale
```

### Example 3: Deployment Question
```
User: "How do I deploy a hotfix to production?"

chief-architect response:
1. Explains CI/CD workflow (push to master)
2. Notes Doppler secret fetching
3. Describes Caddy reload process
4. References SOP-026 for details
```

### Example 4: Canvas Architecture Question
```
User: "Why do tasks jump around when I refresh?"

chief-architect response:
1. Explains geometry invariants (TASK-255)
2. Identifies likely violation of single-writer principle
3. Checks if sync is accidentally calling updateTask()
4. References CANVAS-POSITION-SYSTEM.md SOP
```

---

## MANDATORY USER VERIFICATION REQUIREMENT

### Policy: No Fix Claims Without User Confirmation

**CRITICAL**: Before claiming ANY issue, bug, or problem is "fixed", "resolved", "working", or "complete", the following verification protocol is MANDATORY:

#### Step 1: Technical Verification
- Run all relevant tests (build, type-check, unit tests)
- Verify no console errors
- Take screenshots/evidence of the fix

#### Step 2: User Verification Request
**REQUIRED**: Use the `AskUserQuestion` tool to explicitly ask the user to verify the fix:

```
"I've implemented [description of fix]. Before I mark this as complete, please verify:
1. [Specific thing to check #1]
2. [Specific thing to check #2]
3. Does this fix the issue you were experiencing?

Please confirm the fix works as expected, or let me know what's still not working."
```

#### Step 3: Wait for User Confirmation
- **DO NOT** proceed with claims of success until user responds
- **DO NOT** mark tasks as "completed" without user confirmation
- **DO NOT** use phrases like "fixed", "resolved", "working" without user verification

#### Step 4: Handle User Feedback
- If user confirms: Document the fix and mark as complete
- If user reports issues: Continue debugging, repeat verification cycle

### Prohibited Actions (Without User Verification)
- Claiming a bug is "fixed"
- Stating functionality is "working"
- Marking issues as "resolved"
- Declaring features as "complete"
- Any success claims about fixes

### Required Evidence Before User Verification Request
1. Technical tests passing
2. Visual confirmation via Playwright/screenshots
3. Specific test scenarios executed
4. Clear description of what was changed

**Remember: The user is the final authority on whether something is fixed. No exceptions.**

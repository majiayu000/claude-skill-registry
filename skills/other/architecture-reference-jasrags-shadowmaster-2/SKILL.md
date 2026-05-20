---
name: architecture-reference
description: Deep-dive reference for Shadow Master subsystems including Combat, Matrix, Rigging, Inventory, Contacts, Sync, and Security. Use when working on specific game mechanics or need detailed file locations for a subsystem.
allowed-tools: Read, Grep, Glob
---

# Architecture Reference

Detailed documentation for Shadow Master's core subsystems. For high-level architecture overview, see CLAUDE.md.

---

## Combat System

Full combat tracking with initiative, actions, and damage resolution.

**Key Concepts:**

- **Combat Session**: Tracks all combatants, turn order, and combat state
- **Action Resolution**: Executes and validates combat actions
- **Initiative Tracking**: Automatic turn management with initiative passes
- **Damage Tracking**: Condition monitor integration

**Critical Files:**

- `/lib/combat/CombatSessionContext.tsx` - Combat state management
- `/lib/rules/action-resolution/` - Action execution framework
  - `action-executor.ts` - Core execution logic
  - `action-validator.ts` - Action validation
  - `dice-engine.ts` - Dice rolling engine
  - `pool-builder.ts` - Dice pool construction
  - `edge-actions.ts` - Edge spending actions
  - `combat/` - Combat-specific handlers (damage, weapons)
- `/app/api/combat/` - Combat session API endpoints
- `/components/combat/` - Combat UI (tracker, dice pools, quick reference)

---

## Matrix Operations System

Full matrix hacking with overwatch, marks, and program management.

**Key Concepts:**

- **Cyberdecks**: Hardware validation and configuration
- **Programs**: Slot management and allocation
- **Overwatch Score**: OS tracking and convergence handling
- **Marks**: Mark placement and tracking system
- **Matrix Actions**: Action validation with mark requirements

**Critical Files:**

- `/lib/rules/matrix/` - Matrix operations
  - `cyberdeck-validator.ts` - Hardware validation
  - `program-validator.ts` - Program allocation
  - `overwatch-calculator.ts` - OS calculation
  - `overwatch-tracker.ts` - Session tracking
  - `mark-tracker.ts` - Mark management
  - `action-validator.ts` - Matrix action validation
  - `dice-pool-calculator.ts` - Matrix dice pools

---

## Rigging Control System

Vehicle and drone control for riggers.

**Key Concepts:**

- **VCR (Vehicle Control Rig)**: Validation and bonuses
- **RCC (Rigger Command Console)**: Drone slaving and command execution
- **Drone Networks**: Network management and noise handling
- **Jump-In Mode**: VR mode management for direct control
- **Biofeedback**: Damage and dumpshock handling

**Critical Files:**

- `/lib/rules/rigging/` - Rigging mechanics
  - `vcr-validator.ts` - VCR validation
  - `rcc-validator.ts` - RCC validation and slaving
  - `drone-network.ts` - Network management
  - `drone-condition.ts` - Drone damage tracking
  - `jumped-in-manager.ts` - Jump-in mode
  - `biofeedback-handler.ts` - Biofeedback damage
  - `noise-calculator.ts` - Signal noise calculations
  - `action-validator.ts` - Rigging action validation
  - `dice-pool-calculator.ts` - Vehicle/drone dice pools

---

## Inventory and Equipment System

Equipment state management for gear, weapons, and devices.

**Key Concepts:**

- **Readiness States**: ready, holstered, stored, etc.
- **Wireless Toggles**: Enable/disable for augmentations and devices
- **Device Condition**: functional, bricked, repaired
- **Gear Validation**: Availability and rating validation

**Critical Files:**

- `/lib/rules/inventory/state-manager.ts` - Equipment state management
- `/lib/rules/gear/validation.ts` - Gear availability validation
- `/lib/rules/gear/weapon-customization.ts` - Weapon modifications

---

## Gameplay Utilities

Runtime calculations for combat and tests.

**Key Concepts:**

- **Effective Ratings**: Wireless bonuses and matrix damage effects
- **Dice Pool Bonuses**: Equipment rating bonuses
- **Test Thresholds**: Detect, analyze, bypass calculations
- **Armor Stacking**: SR5 Core p.169-170 rules with accessories and encumbrance
- **Wound Modifiers**: High/Low Pain Tolerance support

**Critical Files:**

- `/lib/rules/gameplay.ts` - Core gameplay calculations
- `/lib/rules/constraint-validation.ts` - Creation constraint validation

---

## Grunt/NPC System

Pre-built NPC templates for GMs with professional rating tiers.

**Key Concepts:**

- **Professional Rating (PR)**: PR0 (street rabble) to PR6 (dragon guard)
- **Grunt Templates**: Pre-configured NPCs with stats, gear, and skills
- **Grunt Teams**: Groups of NPCs for encounter management

**Critical Files:**

- `/lib/rules/grunts.ts` - Grunt mechanics and validation
- `/lib/storage/grunt-templates.ts` - Template persistence
- `/data/editions/{editionCode}/grunt-templates/` - PR0-PR6 template files
- `/app/campaigns/[id]/grunt-teams/` - Team management UI
- `/app/api/campaigns/[id]/grunt-teams/` - Grunt team API

---

## Contact Network System

Contact relationships and favor economy for social gameplay.

**Key Concepts:**

- **Contact Network**: Relationships with NPCs and their loyalty/connection ratings
- **Favor Economy**: Tracking favors owed and earned
- **Social Capital**: Reputation and influence mechanics

**Critical Files:**

- `/lib/rules/contact-network.ts` - Contact relationship logic
- `/lib/rules/favors.ts` - Favor economy system
- `/lib/rules/social-actions.ts` - Social interaction mechanics
- `/lib/storage/contacts.ts` - Contact persistence
- `/lib/storage/favor-ledger.ts` - Favor tracking
- `/app/api/characters/[characterId]/contacts/` - Contact API

---

## System Synchronization

Character-ruleset drift detection and migration.

**Key Concepts:**

- **Drift Analysis**: Detect metatype, skill, quality changes between rulesets
- **Legality Validation**: Quick sync status checks
- **Migration Engine**: Generate and execute migration plans
- **Sync Audit**: Trail of synchronization events

**Critical Files:**

- `/lib/rules/sync/` - Synchronization system
  - `drift-analyzer.ts` - Change detection
  - `legality-validator.ts` - Rule compliance checking
  - `migration-engine.ts` - Migration planning and execution
  - `sync-audit.ts` - Audit trail
  - `hooks.ts` - React hooks for client-side sync

---

## Optional Rules System

Campaign-level rule customization.

**Key Concepts:**

- **Campaign Configuration**: Enable/disable optional rules per campaign
- **GM Control**: Default override support
- **Rule Extraction**: Pull optional rules from loaded rulesets
- **Content Access**: Validate content against enabled rules

**Critical Files:**

- `/lib/rules/optional-rules.ts` - Optional rule management

---

## Data Management Layers

**Authentication State** (`/lib/auth/AuthProvider.tsx`):

- React Context managing user session globally
- Provides `useAuth()` hook for components
- Session stored in httpOnly cookie

**Ruleset State** (`/lib/rules/RulesetContext.tsx`):

- React Context caching loaded ruleset
- Provides hooks: `useRuleset()`, `useMetatypes()`, `useSkills()`, etc.
- Fetches from `/api/rulesets/[editionCode]`

**Sidebar State** (`/lib/contexts/SidebarContext.tsx`):

- React Context managing sidebar open/collapsed state globally
- Provides `useSidebar()` hook with: `isOpen`, `isCollapsed`, `toggle`, `close`, `toggleCollapse`
- Desktop collapsed state persisted to localStorage (`shadow-master-sidebar-collapsed-global`)
- Built-in Escape key handler and resize listener for mobile drawer
- Focus trap and accessibility features managed in `AuthenticatedLayout`

**Local Storage**:

- User preferences and UI state (theme, sidebar collapsed state)
- Draft recovery handled server-side via auto-save

---

## File-Based Storage Pattern

**Design:** JSON files on disk with atomic writes (temp file + rename pattern)

**Storage Layer** (`/lib/storage/`):

Core modules:

- `base.ts` - Core utilities: `readJsonFile()`, `writeJsonFile()`, `ensureDirectory()`
- `users.ts` - User CRUD operations
- `characters.ts` - Character CRUD + specialized operations (damage, karma, etc.)
- `campaigns.ts` - Campaign CRUD operations
- `editions.ts` - Edition and ruleset loading

Extended modules:

- `contacts.ts`, `favor-ledger.ts` - Contact system persistence
- `combat.ts`, `action-history.ts` - Combat session storage
- `grunt-templates.ts`, `grunts.ts` - NPC system storage
- `notifications.ts`, `activity.ts` - User activity tracking
- `audit.ts`, `user-audit.ts` - Audit trail logging
- `ruleset-snapshots.ts`, `snapshot-cache.ts` - Ruleset versioning
- `locations.ts`, `locations_connections.ts` - Campaign location storage
- `social-capital.ts` - Social capital tracking
- `violation-record.ts` - Rule violation tracking

**Storage Structure:**

```
/data
├── /users/{userId}.json
├── /characters/{userId}/{characterId}.json
├── /campaigns/{campaignId}.json
└── /editions/{editionCode}/
    ├── edition.json
    ├── core-rulebook.json
    ├── {sourcebook}.json
    └── /grunt-templates/
        └── pr{0-6}-{name}.json
```

**Important:** This is NOT production-scalable. File I/O happens on every request. Future migration to a database is planned.

---

## Security Infrastructure

**Rate Limiting** (`/lib/security/rate-limit.ts`):

- DDoS protection for API endpoints
- Configurable limits per endpoint

**Audit Logging** (`/lib/security/audit-logger.ts`):

- Full audit trail for user actions
- Security event tracking
- Stored via `/lib/storage/audit.ts`

**Character Authorization** (`/lib/auth/character-authorization.ts`):

- Granular character access control
- Owner, campaign GM, and viewer permissions

**Additional Auth Modules** (`/lib/auth/`):

- `validation.ts` - Auth validation logic
- `middleware.ts` - Auth middleware
- `campaign.ts` - Campaign-specific authorization
- `email-verification.ts` - Email verification token handling

**Admin User Management** (`/app/api/users/[id]/`):

- `lockout/route.ts` - DELETE to clear login lockouts
- `resend-verification/route.ts` - POST to resend verification emails (rate limited)
- `verify-email/route.ts` - POST to manually verify user email
- `suspend/route.ts` - POST/DELETE to suspend/reactivate accounts

**Admin UI** (`/app/users/`):

- `UserTable.tsx` - User list with lockout/verification badges and menu actions
- `UserEditModal.tsx` - User details with lockout info and verification controls
- `UserAuditModal.tsx` - User audit trail viewer

---

## API Route Patterns

All API routes follow this pattern:

1. Extract session from cookie via `getSession()`
2. Validate user exists via `getUserById()`
3. Return 401 if unauthenticated
4. Perform user-scoped operation
5. Return JSON response

**Example:**

```typescript
// /app/api/characters/route.ts
export async function GET(request: NextRequest) {
  const session = await getSession();
  if (!session?.userId) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const user = getUserById(session.userId);
  if (!user) {
    return NextResponse.json({ error: "User not found" }, { status: 404 });
  }

  const characters = getUserCharacters(session.userId);
  return NextResponse.json({ characters });
}
```

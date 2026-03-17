---
name: component-patterns
description: Guidelines for organizing React components in Shadow Master. Use when creating new components, deciding between single-file vs subfolder structure, or understanding the component architecture.
allowed-tools: Read, Grep, Glob
---

# Component Organization Patterns

Guidelines for structuring React components in the Shadow Master codebase.

## Component Directory Overview

```
/components/                    # 130+ components total
├── index.ts                    # Root exports (DiceRoller only)
├── *.tsx                       # 6 standalone utility components
├── action-resolution/          # 3 components - dice pool building
├── auth/                       # 1 component - email verification
├── character/                  # 12 components - character sheet display
├── combat/                     # 4 components - combat tracking UI
├── creation/                   # 83 components - character creation
│   ├── *.tsx                   # 14 top-level cards
│   ├── shared/                 # 14 reusable utilities
│   └── {feature}/              # 17 feature subfolders
├── cyberlimbs/                 # 6 components - augmentation UI
├── sync/                       # 2 components - ruleset sync status
└── ui/                         # 2 components - BaseModal, Tooltip
```

---

## Decision Flowchart

```
Does the component have modals?
├─ Yes → Create subfolder, extract modals
└─ No → Does it have reusable Row/ListItem components?
        ├─ Yes, used elsewhere → Create subfolder
        └─ No → Keep as single file with internal helpers
```

---

## When to Use a Subfolder

Create a subfolder with `index.ts` when:

- Component has one or more **modals** (selection dialogs, forms, etc.)
- Component has **reusable row/list item** components used in multiple places
- Component exceeds ~600 lines with clear separable concerns
- Component has distinct UI pieces that could be tested independently

**Subfolder structure:**

```
/components/{area}/{feature}/
├── FeatureCard.tsx           # Main component
├── FeatureModal.tsx          # Selection/edit modal
├── FeatureRow.tsx            # Optional: if row is complex/reusable
├── constants.ts              # Optional: magic values, options arrays
├── types.ts                  # Optional: feature-specific types
├── utils.ts                  # Optional: feature-specific helpers
├── index.ts                  # Re-exports public API
```

**Index file pattern:**

```typescript
// index.ts - export only public API
export { FeatureCard } from "./FeatureCard";
export { FeatureModal } from "./FeatureModal"; // Only if used externally
```

---

## When to Keep as Single File

Keep as a single file when:

- Component is self-contained with only **internal helper components**
- Internal components are tightly coupled and only make sense within the parent
- Component is under ~400 lines with straightforward structure
- No modals or independently reusable pieces

---

## Component Areas

### Root-Level Components (6 files)

Standalone utility components that don't fit a specific feature area:

| Component              | Purpose                             |
| ---------------------- | ----------------------------------- |
| `DiceRoller.tsx`       | Dice rolling UI with edge rerolls   |
| `AugmentationCard.tsx` | Generic augmentation display        |
| `EssenceDisplay.tsx`   | Essence tracking visualization      |
| `ThemeProvider.tsx`    | Dark/light mode context             |
| `EnvironmentBadge.tsx` | Environment indicator (dev/staging) |
| `NotificationBell.tsx` | Notification center UI              |

---

### `/components/ui/` - Shared UI Primitives

Low-level accessible components used across the app. Built on React Aria.

| Component       | Exports                                              |
| --------------- | ---------------------------------------------------- |
| `BaseModal.tsx` | BaseModal, ModalHeader, ModalBody, ModalFooter       |
| `Tooltip.tsx`   | Tooltip, TooltipTrigger, TooltipContent, InfoTooltip |

**When to add here:** Generic UI primitives with no business logic.

---

### `/components/auth/` - Authentication Components

| Component                     | Purpose                      |
| ----------------------------- | ---------------------------- |
| `EmailVerificationBanner.tsx` | Prompts user to verify email |

---

### `/components/action-resolution/` - Dice Pool Building

Components for building and displaying action resolution dice pools.

| Component               | Purpose                          |
| ----------------------- | -------------------------------- |
| `ActionHistory.tsx`     | List of past action rolls        |
| `ActionPoolBuilder.tsx` | Construct dice pools for actions |
| `EdgeTracker.tsx`       | Edge point tracking and spending |

**Note:** No index.ts - import directly from files.

---

### `/components/character/` - Character Sheet Display

Components for viewing active characters (not creation). No index file - import directly.

| Component                 | Purpose                           |
| ------------------------- | --------------------------------- |
| `AdeptPowerList.tsx`      | Display adept powers and PP       |
| `AutosoftManager.tsx`     | Manage vehicle/drone autosofts    |
| `CyberdeckConfig.tsx`     | Cyberdeck attribute configuration |
| `DroneNetworkManager.tsx` | RCC drone network management      |
| `JumpInControl.tsx`       | Vehicle/drone jump-in interface   |
| `MagicSummary.tsx`        | Magic rating, tradition, drain    |
| `MatrixActions.tsx`       | Matrix action buttons and state   |
| `MatrixSummary.tsx`       | Matrix attributes and programs    |
| `ProgramManager.tsx`      | Running programs management       |
| `RiggingSummary.tsx`      | Rigging stats and VCR mode        |
| `Spellbook.tsx`           | Spell list with casting interface |
| `VehicleActions.tsx`      | Vehicle action buttons            |

---

### `/components/combat/` - Combat Tracking

Components for running combat encounters. Has index.ts and co-located tests.

| Component                 | Purpose                              |
| ------------------------- | ------------------------------------ |
| `CombatTracker.tsx`       | Initiative order and turn management |
| `ActionSelector.tsx`      | Action selection with categories     |
| `ConditionMonitor.tsx`    | Health/damage tracking               |
| `OpposedTestResolver.tsx` | Opposed test dice rolling            |

---

### `/components/cyberlimbs/` - Cyberlimb Management

Components for cyberlimb augmentation display and modification.

| Component                       | Purpose                       |
| ------------------------------- | ----------------------------- |
| `CyberlimbCard.tsx`             | Individual cyberlimb display  |
| `CyberlimbList.tsx`             | List all installed cyberlimbs |
| `CyberlimbDetailPanel.tsx`      | Detailed cyberlimb info panel |
| `CyberlimbInstallModal.tsx`     | Install new cyberlimb         |
| `CyberlimbEnhancementModal.tsx` | Add attribute enhancements    |
| `CyberlimbAccessoryModal.tsx`   | Add accessories to limb       |

---

### `/components/sync/` - Ruleset Synchronization

Components for displaying ruleset sync status and migration.

| Component             | Purpose                              |
| --------------------- | ------------------------------------ |
| `StabilityShield.tsx` | Visual sync status indicator         |
| `MigrationWizard.tsx` | Guide user through ruleset migration |

---

### `/components/creation/` - Character Creation

The largest component area (83 components). Organized by feature with shared utilities.

#### Top-Level Cards (14 files)

Single-file cards without complex modals:

| Card                    | Purpose                       |
| ----------------------- | ----------------------------- |
| `PrioritySelectionCard` | Priority table selection      |
| `AttributesCard`        | Attribute allocation          |
| `SkillsCard`            | Active skills management      |
| `SpellsCard`            | Spell selection for mages     |
| `AdeptPowersCard`       | Adept power selection         |
| `ComplexFormsCard`      | Technomancer complex forms    |
| `AugmentationsCard`     | Cyberware/bioware selection   |
| `VehiclesCard`          | Vehicle/drone acquisition     |
| `WeaponsPanel`          | Weapon purchases              |
| `GearTabsCard`          | Tabbed gear interface         |
| `DerivedStatsCard`      | Calculated stats display      |
| `CharacterInfoCard`     | Name, background, description |
| `EditionSelector`       | Edition selection dropdown    |
| `CreationErrorBoundary` | Error boundary for creation   |

#### Feature Subfolders (17 directories)

| Folder                 | Components | Pattern                                 |
| ---------------------- | ---------- | --------------------------------------- |
| `/armor`               | 4          | Panel + Row + PurchaseModal + ModModal  |
| `/augmentations`       | 4          | 4 specialized modals                    |
| `/contacts`            | 3          | Card + Modal + KarmaConfirm             |
| `/foci`                | 2          | Card + Modal                            |
| `/gear`                | 4          | Panel + Row + 2 Modals                  |
| `/identities`          | 6          | Card + Identity + 3 modal types         |
| `/knowledge-languages` | 5          | Card + 2 Row types + 2 Modals           |
| `/magic-path`          | 2          | Card + Modal + utilities                |
| `/matrix-gear`         | 2          | Card + Modal                            |
| `/metatype`            | 2          | Card + Modal                            |
| `/qualities`           | 3          | Card + SelectionModal + DetailCard      |
| `/shared`              | 14         | Reusable utilities and hooks            |
| `/skills`              | 10         | Panel + ListItem + 8 specialized modals |
| `/spells`              | 2          | ListItem + Modal                        |
| `/vehicles`            | 4          | 4 specialized modals                    |
| `/weapons`             | 4          | Row + 3 Modals                          |

#### Shared Utilities (`/creation/shared/`)

| Component                       | Purpose                         |
| ------------------------------- | ------------------------------- |
| `CreationCard.tsx`              | Standard card wrapper           |
| `BudgetIndicator.tsx`           | Resource budget display         |
| `CardSkeleton.tsx`              | Loading skeleton                |
| `EmptyState.tsx`                | Empty list state                |
| `KarmaConversionModal.tsx`      | Nuyen ↔ Karma conversion        |
| `RatingSelector.tsx`            | 1-6 rating picker               |
| `Stepper.tsx`                   | +/- increment control           |
| `SummaryFooter.tsx`             | Card summary footer             |
| `ValidationBadge.tsx`           | Validation status indicator     |
| `BulkQuantitySelector.tsx`      | Quantity picker for bulk items  |
| `LifestyleModificationSelector` | Lifestyle mod picker            |
| `LifestyleSubscriptionSelector` | Lifestyle subscription picker   |
| `useKarmaConversionPrompt.ts`   | Hook for karma conversion modal |

---

## Adding Components by Area

### Adding a Creation Card

1. **Determine structure** using the decision flowchart
2. **Create in** `/components/creation/` or `/components/creation/{feature}/`
3. **Use `CreationCard` wrapper** from `/components/creation/shared/`
4. **Add to `SheetCreationLayout.tsx`** in appropriate column
5. **Update `CreationState` type** in `/lib/types/creation.ts` if needed
6. **Export from `/components/creation/index.ts`**

### Adding a Combat Component

1. Create in `/components/combat/`
2. Export from `/components/combat/index.ts`
3. Add co-located test in `/components/combat/__tests__/`

### Adding a Character Sheet Component

1. Create in `/components/character/`
2. Import directly from file (no index.ts)
3. Add to relevant page in `/app/characters/[id]/`

### Adding a Cyberlimb Component

1. Create in `/components/cyberlimbs/`
2. Export from `/components/cyberlimbs/index.ts`
3. Export types if needed for external use

### Adding a UI Primitive

1. Create in `/components/ui/`
2. Build on React Aria for accessibility
3. Export from `/components/ui/index.ts`
4. No business logic - pure presentation

---

## Adding a New API Endpoint

1. Create `/app/api/{path}/route.ts`
2. Export HTTP method handlers (GET, POST, PUT, DELETE)
3. Follow authentication pattern (getSession → validate user)
4. Call storage layer functions
5. Return JSON responses

---

## Adding a New Ruleset Module

1. Define module type in `/lib/types/edition.ts`
2. Add module to book payload in `/data/editions/{editionCode}/`
3. Update merge logic in `/lib/rules/merge.ts` if special handling needed
4. Create hook in `RulesetContext.tsx` for easy access

---

## Key Reference Files

- `components/ui/BaseModal.tsx` - Accessible modal foundation
- `components/creation/shared/CreationCard.tsx` - Card wrapper pattern
- `components/creation/SkillsCard.tsx` - Modal-based editing example
- `components/combat/CombatTracker.tsx` - Combat component with tests
- `components/cyberlimbs/index.ts` - Feature folder export pattern
- `app/characters/create/sheet/components/SheetCreationLayout.tsx` - Three-column layout

---

## Component Diagram Generation

Mermaid diagrams are auto-generated from the component structure.

### Commands

```bash
# Preview all areas to stdout
pnpm generate-diagrams

# Generate specific area
pnpm generate-diagrams --area=combat
pnpm generate-diagrams --area=creation

# Update documentation files
pnpm generate-diagrams --output=files

# Verbose mode with component counts
pnpm generate-diagrams --verbose
```

### Output Locations

| Mode              | Location                                   |
| ----------------- | ------------------------------------------ |
| `--output=stdout` | Prints to terminal (default)               |
| `--output=files`  | Writes to `/docs/architecture/components/` |

### Diagram Color Key

| Color  | Hex       | Component Type | Naming Pattern                            |
| ------ | --------- | -------------- | ----------------------------------------- |
| Blue   | `#3b82f6` | Container      | `*Card.tsx`, `*Panel.tsx`, `*Tracker.tsx` |
| Purple | `#8b5cf6` | Modal          | `*Modal.tsx`                              |
| Green  | `#22c55e` | Row            | `*Row.tsx`, `*ListItem.tsx`               |
| Orange | `#f59e0b` | Hook           | `use*.ts`, `*Context.tsx`                 |
| Gray   | `#6b7280` | Shared         | Everything else                           |

### When to Regenerate

Run `pnpm generate-diagrams --output=files` after:

- Adding a new component folder
- Adding/removing modals or cards
- Reorganizing component structure
- Before major documentation updates

### Validation

```bash
# Validate creation docs structure (doesn't regenerate)
pnpm validate-creation-docs --verbose
```

---

## Documentation Structure

### Hand-Written (detailed)

`/docs/architecture/creation-components/` - Detailed creation component docs with:

- Component descriptions
- Props documentation
- Usage patterns
- Context dependencies

### Auto-Generated (overview)

`/docs/architecture/components/` - Generated hierarchy diagrams:

- Mermaid component trees
- Summary tables
- Color-coded by type

---

## Index File Conventions

| Area                 | Has index.ts? | Reason                           |
| -------------------- | ------------- | -------------------------------- |
| `/ui`                | Yes           | Stable public API                |
| `/combat`            | Yes           | Cohesive feature set             |
| `/cyberlimbs`        | Yes           | Cohesive feature set             |
| `/sync`              | Yes           | Cohesive feature set             |
| `/creation`          | Yes           | Organized by phases              |
| `/character`         | No            | Loosely coupled, import directly |
| `/action-resolution` | No            | Loosely coupled, import directly |
| `/auth`              | No            | Single component                 |

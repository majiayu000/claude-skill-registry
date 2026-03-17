---
name: ui-architect
description: Design component architecture for legaltech UIs - layer separation, data flow, design system selection
allowed-tools: Read, Write, Glob, Bash, Grep, Edit, mcp__memory__*, mcp__claude-in-chrome__*
context: full
agent: general-purpose
model: claude-opus-4-5-20250514
---

# ui-architect

Design component architecture for 45Black legaltech products. This skill helps non-coders plan UI structure, separate product layers, and select appropriate design systems.

## When To Use

- Starting a new UI product or feature
- Restructuring existing UI architecture
- Deciding which design system variant to use
- Planning component hierarchy for apex products
- Separating concerns between product layers
- User mentions: "architect", "component structure", "layer design", "ui planning"

## Workflow

### 1. Gather Context

Ask the user about:
- **Product name** and purpose
- **Target users** (trustees/clients vs developers/admins)
- **Usage pattern** (occasional vs 8hr+ daily use)
- **Data sources** (which apex services: helix, governance, precedent, kestrel)
- **Key user journeys** (what tasks do users need to complete)

### 2. Select Design System

Based on user answers, recommend design system:

```
Is this CLIENT-FACING (trustees, advisers, external)?
├── YES → TRUSTEE EDITION v1.0
│         • Light-first, Paper White backgrounds
│         • Inter typography
│         • Governance Blue primary (#1A4F7A)
│         • Compliance status colours
│         • WCAG AAA target
│         • Print-ready
│
└── NO → Is this for 8+ hours DAILY USE?
    ├── YES → SAVILLE v5.0 CLARITY
    │         • Matte OFF
    │         • Hero weight 500
    │         • Data-dense optimised
    │
    └── NO → SAVILLE v5.0 CORE
              • Matte ON (15% dark, 8% light)
              • Hero weight 300
              • Developer/admin aesthetic
```

### 3. Define Product Layers

For apex ecosystem products, define these layers:

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  Components, Pages, Layouts (React/Next.js)                 │
│  Design System: [Selected System]                           │
├─────────────────────────────────────────────────────────────┤
│                    INTERACTION LAYER                         │
│  State Management (Zustand), Form Handling (React Hook Form)│
│  User preferences, UI state, Session management             │
├─────────────────────────────────────────────────────────────┤
│                    DATA ACCESS LAYER                         │
│  React Query hooks, API clients, Data transformation        │
│  Connects to: apex-helix | apex-governance | apex-precedent │
├─────────────────────────────────────────────────────────────┤
│                    COMPLIANCE LAYER                          │
│  AI transparency markers, Audit logging, GDPR consent       │
│  EU AI Act compliance, Hash-chained audit trails            │
└─────────────────────────────────────────────────────────────┘
```

### 4. Map Component Hierarchy

Create a component tree document:

```markdown
## Component Hierarchy: [Product Name]

### Layout Components
- AppShell (header, sidebar, main content)
- PageLayout (breadcrumbs, title, actions)
- SplitPane (resizable document/panel views)

### Feature Components
- [Domain-specific components]

### Shared UI Components (from design system)
- Buttons, Cards, Badges, Tables, Forms
- Use shadcn/ui with design system tokens

### Data Components
- [Product].Provider (context for data)
- use[Product]Data (React Query hook)
```

### 5. Define Data Flow

Document how data moves between layers:

```
User Action → Interaction Layer → Data Layer → API Proxy → Backend Service
                                                              │
                                                              ▼
UI Update ← Presentation ← State Update ← Query Invalidation ← Response
```

### 6. Output Architecture Document

Create `docs/UI_ARCHITECTURE.md` with:

1. **Design System Selection** - Which system and why
2. **Layer Diagram** - Visual representation
3. **Component Hierarchy** - Tree structure
4. **Data Flow** - Sequence diagrams for key journeys
5. **Compliance Requirements** - AI transparency, audit, GDPR
6. **Implementation Notes** - For developers

## Apex Product Layer Matrix

Reference for the apex constellation:

| Product | Data Source | Primary Users | Design System | Status |
|---------|-------------|---------------|---------------|--------|
| apex-lens | helix, precedent, kestrel | Prospects, trustees | Saville Clarity → migrate to Trustee? | Active |
| apex-governance | helix | Trustees, advisers | Trustee v1.0 | Active |
| apex-precedent | precedent DB | Legal researchers | Saville Clarity | Active |
| apex-tracker | helix | Scheme managers | Trustee v1.0 | Planned |
| apex-admin | helix (write) | Wills (admin) | Saville Core | Internal |

## Key Architectural Decisions

### API Proxy Pattern (Mandatory)
All backend requests go through Next.js API routes:
- `/api/helix/*` → apex-helix (port 3001)
- `/api/precedent/*` → apex-precedent (port 3002)
- `/api/kestrel/*` → apex-kestrel (port 3003)

### AI Transparency (EU AI Act Compliance)
All AI-generated content MUST include:
- "AI-Generated" badge
- "Generated with Claude | Always verify AI suggestions" footer
- Human approval step before any action

### State Management
- **Server state**: React Query (caching, invalidation)
- **Client state**: Zustand (UI preferences, local state)
- **Form state**: React Hook Form + Zod validation

## Example Output

```markdown
# UI Architecture: apex-lens v2.0

## Design System
**Trustee Edition v1.0** - Selected because:
- Primary users are pension trustees (external)
- Needs print-ready compliance reports
- Light-first suits office environments

## Component Layers

### Presentation (Trustee Edition)
├── LegislationViewer
│   ├── DocumentPane (Merriweather, cream background)
│   ├── ObligationPanel (cards with status badges)
│   └── NavigationTree (sidebar with sections)
├── SearchInterface
│   ├── SearchBar
│   ├── FacetedFilters
│   └── ResultsList
└── CollectionManager
    ├── FavouritesList
    └── CollectionView

### Data Access
├── useLegislation(id) → /api/helix/acts/{id}
├── useObligations(sectionId) → /api/helix/obligations
└── useCaseLaw(query) → /api/precedent/search

### Compliance
├── AITransparencyBadge
├── AuditLogProvider
└── ConsentManager
```

## Model Preference

**opus** - Architecture decisions require deep reasoning about trade-offs

---
*Part of 45Black UI Expert Devstack*
*For non-coders: This skill helps you plan before building*

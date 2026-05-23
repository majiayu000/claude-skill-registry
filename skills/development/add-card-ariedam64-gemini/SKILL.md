---
name: add-card
description: Create a new card part within a section with factory/class pattern, Card wrapper, and proper cleanup
aliases: [new-card, create-card]
---

# Add Card Skill

## Usage
```
/add-card <SectionName>/<CardName>
```

Example: `/add-card Pets/InventoryCard` or `/add-card Alerts/WeatherCard`

---

## What is a Card?

A **Card** is a self-contained UI part within a Section. It:
- Wraps content in the `Card` component (expandable/collapsible container)
- Has a specific purpose (logs viewer, team manager, item list, etc.)
- Lives in `src/ui/sections/<SectionName>/parts/<cardName>/`
- Can be either **class-based** (complex state) or **factory-based** (simpler)

### Cards vs Components
| Aspect | Card (Part) | Component |
|--------|-------------|-----------|
| Location | `sections/<Section>/parts/` | `components/` |
| Scope | Section-specific | Reusable across sections |
| State | Often section-specific state | Props-driven, minimal internal state |
| Complexity | Higher (orchestrates components) | Lower (single purpose) |

---

## Step 1: Ask Questions

### 1. Parent Section
```
Which section will contain this card?
→ Must exist in src/ui/sections/
```

### 2. Card Purpose
```
Brief description (1 sentence):
What does this card display/manage?
```

### 3. Pattern Type
```
A) Factory pattern (recommended for simpler cards)
   - createXxxCard(options): XxxCardHandle
   - Better for cards with minimal internal state
   - Example: ShopsCard, PublicCard

B) Class pattern (for complex cards)
   - class XxxCardPart { build(), destroy(), render() }
   - Better for cards with complex state, multiple modes, drag handlers
   - Example: TeamCard, TrackerCard, AbilityLogsCard
```

### 4. Card Features
```
[ ] Expandable (collapsible header with chevron)
[ ] Filterable (search bar, selects)
[ ] Scrollable list (virtual scrolling if >50 items)
[ ] Modes toggle (SegmentedControl for overview/manage/etc.)
[ ] Refresh capability (manual refresh button)
```

### 5. Data Sources
```
A) Globals (reactive) → subscribe + cleanup
B) MGData (static) → MGData.get('plants')
C) Feature state → feature.getState()
D) API fetch → async loading
E) Section state → state.ts
F) Combination of above
```

### 6. Child Components
```
Check existing components before creating new:

Layout:
[ ] Card (always used - the wrapper)

Inputs/Controls:
[ ] SearchBar - text filtering
[ ] Select - dropdown filter
[ ] SegmentedControl - mode toggle
[ ] Checkbox - multi-select
[ ] Button - actions

Display:
[ ] Table - tabular data with sorting
[ ] Badge - status indicators
[ ] ProgressBar - progress display
[ ] TeamListItem - team rows

Utility:
[ ] Modal - popups
[ ] SoundPicker - audio selection
```

### 7. Sprites
```
Does it display game sprites? → MGSprite.toCanvas()
```

---

## Step 2: Create Structure

```
src/ui/sections/<SectionName>/parts/<cardName>/
├── <CardName>.ts           # Main card logic (class or factory)
├── <cardName>.css.ts       # Scoped styles (optional)
├── index.ts                # Barrel exports
└── <cardName>Data.ts       # Data processing helpers (optional, for complex data)
└── <cardName>Table.ts      # Table configuration (optional, if using Table)
```

**Read existing cards for templates:**
- Factory pattern: `src/ui/sections/Alerts/parts/shop/shopsCard.ts`
- Factory pattern: `src/ui/sections/Room/parts/public.ts`
- Class pattern: `src/ui/sections/Pets/parts/ability/AbilityLogsCard.ts`
- Class pattern: `src/ui/sections/Pets/parts/team/TeamCard.ts`

---

## Step 3: File Templates

### Factory Pattern (Recommended for simpler cards)

#### `<CardName>.ts`
```typescript
/**
 * <CardName> Card Part
 * <Brief description>
 */

import { Card } from "../../../../components/Card/Card";
import { element } from "../../../../styles/helpers";
// Import needed components
// import { SearchBar } from "../../../../components/SearchBar/SearchBar";
// import { Select } from "../../../../components/Select/Select";
// Import data sources
// import { getMyInventory } from "../../../../../globals/variables/myInventory";
// import { MGData } from "../../../../../modules";

/* ─────────────────────────── Types ─────────────────────────── */

export interface <CardName>Options {
    defaultExpanded?: boolean;
    onExpandChange?: (expanded: boolean) => void;
    // Add card-specific options
}

export interface <CardName>Handle {
    root: HTMLElement;
    refresh?(): void;
    destroy(): void;
}

/* ─────────────────────────── Factory ─────────────────────────── */

export function create<CardName>(options: <CardName>Options = {}): <CardName>Handle {
    const { defaultExpanded = true, onExpandChange } = options;

    // Internal state
    let root: HTMLElement | null = null;
    const cleanups: (() => void)[] = [];

    // Component references (for cleanup)
    // let searchHandle: SearchBarHandle | null = null;

    /**
     * Build the card UI
     */
    function buildCard(): HTMLElement {
        const content = element("div", {
            style: "display: flex; flex-direction: column; gap: 12px;",
        }) as HTMLDivElement;

        // Add filters, lists, content...
        // const searchBar = SearchBar({ ... });
        // content.appendChild(searchBar.root);
        // cleanups.push(() => searchBar.destroy?.());

        root = Card(
            {
                title: "<Card Title>",
                subtitle: "<Card subtitle description>",
                expandable: true,
                defaultExpanded,
                padding: "md",
                onExpandChange,
            },
            content
        );

        return root;
    }

    /**
     * Refresh data (optional)
     */
    function refresh(): void {
        // Reload data, update UI
    }

    /**
     * Cleanup all resources
     */
    function destroy(): void {
        cleanups.forEach(fn => fn());
        cleanups.length = 0;
        root = null;
    }

    return {
        root: buildCard(),
        refresh,
        destroy,
    };
}
```

### Class Pattern (For complex cards with state)

#### `<CardName>.ts`
```typescript
/**
 * <CardName> Card Part
 * <Brief description>
 *
 * Per .claude/rules/ui/sections.md
 */

import { Card } from "../../../../components/Card/Card";
import { element } from "../../../../styles/helpers";
// Import needed components
// import { SegmentedControl, SegmentedControlHandle } from "../../../../components/SegmentedControl/SegmentedControl";
// Import data sources
// import { Globals } from "../../../../../globals";
// import { MGData } from "../../../../../modules";

/* ─────────────────────────── Types ─────────────────────────── */

export interface <CardName>PartOptions {
    // Card-specific options
    onSomeEvent?: () => void;
}

/* ─────────────────────────── Class ─────────────────────────── */

export class <CardName>Part {
    private card: HTMLDivElement | null = null;
    private content: HTMLDivElement | null = null;
    private options: <CardName>PartOptions;
    private cleanups: (() => void)[] = [];

    // Component references
    // private modeControl: SegmentedControlHandle | null = null;

    // Internal state
    // private mode: "overview" | "manage" = "overview";

    constructor(options: <CardName>PartOptions = {}) {
        this.options = options;
    }

    /* ───────────────────── Public API ───────────────────── */

    build(): HTMLDivElement {
        if (this.card) return this.card;
        return this.createCard();
    }

    destroy(): void {
        this.cleanups.forEach(fn => fn());
        this.cleanups.length = 0;

        // Destroy child components
        // this.modeControl?.destroy();
        // this.modeControl = null;

        this.card = null;
        this.content = null;
    }

    render(): void {
        if (!this.card) return;
        this.renderContent();
    }

    /* ───────────────────── Card Setup ───────────────────── */

    private createCard(): HTMLDivElement {
        const wrapper = element("div", {
            className: "<card-name>-wrapper",
        });

        this.content = element("div", {
            className: "<card-name>__content",
        });
        wrapper.appendChild(this.content);

        this.card = Card(
            {
                title: "<Card Title>",
                subtitle: "<Card subtitle description>",
                expandable: true,
                defaultExpanded: true,
            },
            wrapper
        );

        return this.card;
    }

    /* ───────────────────── Rendering ───────────────────── */

    private renderContent(): void {
        if (!this.content) return;

        this.content.replaceChildren();

        // Build UI based on state...
    }

    /* ───────────────────── Event Handlers ───────────────────── */

    // private handleSomeAction(): void { ... }
}
```

### `index.ts` (Barrel exports)
```typescript
/**
 * <CardName> Card Parts - Barrel exports
 */

// Factory pattern:
export { create<CardName> } from "./<CardName>";
export type { <CardName>Options, <CardName>Handle } from "./<CardName>";

// OR Class pattern:
export { <CardName>Part } from "./<CardName>";
export type { <CardName>PartOptions } from "./<CardName>";

// Optional CSS export
export { <cardName>CardCss } from "./<cardName>.css";
```

### `<cardName>.css.ts` (Optional)
```typescript
/**
 * <CardName> Card styles
 */

export const <cardName>CardCss = /* css */`
/* Scoped to card */
.<card-name>-wrapper {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.<card-name>__content {
    /* Content styles */
}

.<card-name>__list {
    max-height: 400px;
    overflow-y: auto;
}

.<card-name>__empty {
    padding: 24px;
    text-align: center;
    color: color-mix(in oklab, var(--fg) 60%, #9ca3af);
    font-size: 14px;
}
`;
```

---

## Step 4: Register in Section

### Update `parts/index.ts`
```typescript
// <CardName> parts
export { create<CardName> } from "./<cardName>/<CardName>";
export type { <CardName>Options, <CardName>Handle } from "./<cardName>/<CardName>";

// OR for class pattern:
export { <CardName>Part } from "./<cardName>/<CardName>";
export type { <CardName>PartOptions } from "./<cardName>/<CardName>";
```

### Use in `section.ts`
```typescript
import { create<CardName> } from "./parts";
// OR
import { <CardName>Part } from "./parts";

// In build():
// Factory pattern:
const card = create<CardName>({
    defaultExpanded: true,
    onExpandChange: (expanded) => { ... },
});
container.appendChild(card.root);
cleanups.push(() => card.destroy());

// OR Class pattern:
const cardPart = new <CardName>Part({ ... });
container.appendChild(cardPart.build());
cardPart.render();
cleanups.push(() => cardPart.destroy());
```

---

## Step 5: Validate

### Structure
- [ ] Card file named `<CardName>.ts` (PascalCase)
- [ ] CSS file named `<cardName>.css.ts` (camelCase)
- [ ] `index.ts` exports card and types
- [ ] Card lives in `parts/<cardName>/` folder

### API
- [ ] Factory returns `{ root, destroy, refresh? }` OR class has `build()`, `destroy()`, `render()`
- [ ] Options interface defined for configuration
- [ ] Handle/Options types exported

### Card Wrapper
- [ ] Uses `Card` component from `components/Card/Card`
- [ ] Has title and subtitle
- [ ] Has `expandable: true` if collapsible
- [ ] Has `defaultExpanded` option

### Cleanup
- [ ] All subscriptions unsubscribed in `destroy()`
- [ ] All child components' `destroy()` called
- [ ] All event listeners removed
- [ ] `cleanups[]` array used for tracking

### Styling
- [ ] Uses CSS variables (no hardcoded colors)
- [ ] Classes scoped with card name prefix
- [ ] Touch-friendly (min 44px targets)
- [ ] Responsive (flexible widths)

### Data (if applicable)
- [ ] Globals subscribed with cleanup
- [ ] MGData for static game data
- [ ] Section state for persisted preferences
- [ ] Loading states handled

### Components (if applicable)
- [ ] Reuses existing components from `src/ui/components/`
- [ ] Child components tracked in `cleanups[]`

---

## Existing Cards Reference

### Factory Pattern (simpler)
- `Alerts/parts/shop/shopsCard.ts` - Table with filters
- `Alerts/parts/weather/weatherCard.ts` - Weather alerts
- `Room/parts/public.ts` - Rooms list with API fetch

### Class Pattern (complex)
- `Pets/parts/ability/AbilityLogsCard.ts` - Virtual scrolling list
- `Pets/parts/team/TeamCard.ts` - CRUD with drag-drop
- `Pets/parts/teamDetails/TeamDetailsCard.ts` - Expansion panels
- `Trackers/parts/TrackerCard.ts` - Team list with expansion

---

## Common Patterns

### Filters Row
```typescript
const filters = element("div", {
    className: "<card>-filters",
    style: "display: flex; gap: 8px; margin-bottom: 12px;",
});

const select = Select({
    options: [...],
    onChange: (value) => applyFilters(),
});

const search = SearchBar({
    placeholder: "Search...",
    onSearch: (value) => applyFilters(),
});

filters.append(select.root, search.root);
```

### Scrollable List
```typescript
const list = element("div", {
    className: "<card>__list",
    style: "max-height: 400px; overflow-y: auto;",
});
```

### Empty State
```typescript
if (items.length === 0) {
    const empty = element("div", {
        className: "<card>__empty",
        style: "padding: 24px; text-align: center; color: color-mix(in oklab, var(--fg) 60%, #9ca3af);",
    }, "No items yet");
    content.appendChild(empty);
    return;
}
```

### Mode Toggle
```typescript
const modeControl = SegmentedControl({
    segments: [
        { id: "simple", label: "Simple" },
        { id: "detailed", label: "Detailed" },
    ],
    selected: "simple",
    onChange: (id) => {
        mode = id;
        renderContent();
    },
});
```

### Subscribe to Globals
```typescript
const unsub = getMyInventory().subscribe((inventory) => {
    items = inventory.items;
    renderList();
});
cleanups.push(unsub);
```

---

## References

- Rules: `.claude/rules/ui/sections.md`
- Card component: `src/ui/components/Card/Card.ts`
- Existing cards: `src/ui/sections/*/parts/*/`
- UI Components: `src/ui/components/`
- Globals: `src/globals/variables/`
- Section workflow: `.claude/workflows/ui/section/add-section.md`

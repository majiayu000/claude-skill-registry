---
name: sheet-ui-redesign
description: Redesigns character sheet display components to match the character creation card aesthetic. Use when updating any component in /components/character/sheet/ to use grouped sections, value pills, and the established dark-mode-first color system.
allowed-tools: Read, Grep, Glob, Edit, Write
user-invocable: true
---

# Character Sheet Component UI Redesign

Guides the redesign of character sheet display components to match the polished creation card aesthetic established across ArmorDisplay, WeaponsDisplay, SkillsDisplay, and AttributesDisplay.

## Process

When invoked with a component name (e.g., `/sheet-ui-redesign MagicDisplay`):

1. **Read the target component** to understand its current structure and data
2. **Read the canonical examples** for pattern reference:
   - `components/character/sheet/ArmorDisplay.tsx` — compact rows, expand/collapse, section grouping, stat pills, capacity bar
   - `components/character/sheet/WeaponsDisplay.tsx` — compact rows, stat pills with semantic colors, pool pill
   - `components/character/sheet/SkillsDisplay.tsx` — grouped sections, compact rows, dice pool interaction, tooltip breakdown
   - `components/character/sheet/VehiclesDisplay.tsx` — three-way section grouping, type badges, type guards, autosofts
3. **Read the target's test file** in `components/character/sheet/__tests__/`
4. **Identify the logical groupings** for the component's data
5. **Apply the patterns below** to redesign the component
6. **Update tests** to match the new markup

## Layout: Flat Structure → Grouped Sections

Replace any flat `<table>`, plain `<ul>`, or single-column list with logical groupings appropriate to the data (e.g., by category, type, or domain meaning). Each group has:

- **Section label:** `text-[10px] font-semibold uppercase tracking-wider text-zinc-500`
- **Sunken container** (one level deeper than card background):
  - Light: `bg-zinc-50 border border-zinc-200 rounded-lg overflow-hidden`
  - Dark: `dark:bg-zinc-950 dark:border-zinc-800`
  - **No inner padding** — rows handle their own padding
- Sections arranged with `space-y-3`

## Compact Row Pattern

All rows use a single-level flex layout with consistent compact sizing:

- **Row container:** `px-3 py-1.5 hover:bg-zinc-100 dark:hover:bg-zinc-700/30`
- **Row separators:** `[&+&]:border-t [&+&]:border-zinc-200 dark:[&+&]:border-zinc-800/50` (sibling borders, no first-row border)
- **Flex layout:** `flex min-w-0 items-center gap-1.5` — single flat row, never nested flex
- **Label text:** `text-[13px] font-medium text-zinc-800 dark:text-zinc-200`
- **Value pill:** `rounded px-1.5 py-0.5 font-mono text-[10px] font-semibold` with `ml-auto shrink-0`
  - Neutral: `bg-zinc-200 text-zinc-900 dark:bg-zinc-800 dark:text-zinc-50`
  - Semantic: `border border-{color}-500/20 bg-{color}-500/12 text-{color}-600 dark:text-{color}-300`
- **Inline badges:** `rounded border border-zinc-400/20 bg-zinc-400/12 px-1.5 py-0.5 font-mono text-[10px] font-semibold uppercase text-zinc-500 dark:text-zinc-400` — for classification labels (type, category)
- **Inline parenthesized annotation:** `truncate text-[10px] text-zinc-400 dark:text-zinc-500` — lighter than badges, for secondary classification shown after the name: `(Heavy Pistols)`, `(Specialization)`. Used in WeaponsDisplay (weapon subcategory) and SkillsDisplay (specializations).

### Choosing a Row Pattern

Pick the simplest pattern that fits the item's data complexity:

| Pattern            | When to use                                          | Example components                            |
| ------------------ | ---------------------------------------------------- | --------------------------------------------- |
| **Simple row**     | Scalar data, 1-2 values (name + rating)              | ContactsDisplay, AdeptPowersDisplay           |
| **Expandable row** | Rich detail: stats, effects, modifications, notes    | ArmorDisplay, WeaponsDisplay, VehiclesDisplay |
| **Hover-reveal**   | Single modifier/indicator on an otherwise simple row | AttributesDisplay (augmentation tooltips)     |

Default to simple rows. Only introduce expandable rows when an item has 3+ distinct detail fields that clutter the collapsed view.

## Expandable Rows

For items with rich detail content, use the chevron-driven expand/collapse pattern:

### State

```tsx
const [isExpanded, setIsExpanded] = useState(false);
```

### Collapsed Row (always visible)

Row click toggles expand/collapse. Chevron is a decorative indicator, not a separate button:

```tsx
<div
  data-testid="item-row"
  onClick={() => setIsExpanded(!isExpanded)}
  className="cursor-pointer px-3 py-1.5 hover:bg-zinc-100 dark:hover:bg-zinc-700/30 [&+&]:border-t [&+&]:border-zinc-200 dark:[&+&]:border-zinc-800/50"
>
  <div className="flex min-w-0 items-center gap-1.5">
    <span data-testid="expand-button" className="shrink-0 text-zinc-400">
      {isExpanded ? (
        <ChevronDown className="h-3.5 w-3.5" />
      ) : (
        <ChevronRight className="h-3.5 w-3.5" />
      )}
    </span>
    <span className="truncate text-[13px] font-medium text-zinc-800 dark:text-zinc-200">
      {name}
    </span>
    {/* Inline badge (classification, not numeric) */}
    <span
      data-testid="type-badge"
      className="rounded border border-zinc-400/20 bg-zinc-400/12 px-1.5 py-0.5 font-mono text-[10px] font-semibold uppercase text-zinc-500 dark:text-zinc-400"
    >
      {type}
    </span>
    {/* Primary value pill, pushed right */}
    <span
      data-testid="primary-pill"
      className="ml-auto shrink-0 rounded border border-sky-500/20 bg-sky-500/12 px-1.5 py-0.5 font-mono text-[10px] font-semibold text-sky-600 dark:text-sky-300"
    >
      {primaryValue}
    </span>
  </div>
</div>
```

### Expanded Section (conditional)

Indented container with left border accent, containing detail sub-sections:

```tsx
{
  isExpanded && (
    <div
      data-testid="expanded-content"
      className="ml-5 mt-2 space-y-2 border-l-2 border-zinc-200 pl-3 dark:border-zinc-700"
    >
      {/* 1. Description — italic, from catalog */}
      {catalogItem?.description && (
        <p className="text-xs italic text-zinc-500 dark:text-zinc-400">{catalogItem.description}</p>
      )}
      {/* 2. Wireless Bonus — bold label + text from catalog */}
      {extras?.wirelessBonus && (
        <div className="text-xs text-zinc-500 dark:text-zinc-400">
          <span className="font-semibold text-zinc-600 dark:text-zinc-300">Wireless:</span>{" "}
          {extras.wirelessBonus}
        </div>
      )}
      {/* 3. Stats row — Avail, Cost, Weight in a flex-wrap row (only render each if present) */}
      <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-zinc-500 dark:text-zinc-400">
        {avail != null && (
          <span data-testid="stat-availability">
            Avail{" "}
            <span className="font-mono font-semibold text-zinc-700 dark:text-zinc-300">
              {avail}
              {legalitySuffix}
            </span>
          </span>
        )}
        {cost > 0 && (
          <span data-testid="stat-cost">
            Cost{" "}
            <span className="font-mono font-semibold text-zinc-700 dark:text-zinc-300">
              ¥{cost}
            </span>
          </span>
        )}
        {weight != null && (
          <span data-testid="stat-weight">
            Weight{" "}
            <span className="font-mono font-semibold text-zinc-700 dark:text-zinc-300">
              {weight}kg
            </span>
          </span>
        )}
      </div>
      {/* 4. Capacity — used/total if item has capacity */}
      {item.capacity != null && (
        <div className="text-xs text-zinc-500 dark:text-zinc-400">
          Capacity{" "}
          <span className="font-mono font-semibold text-zinc-700 dark:text-zinc-300">
            {item.capacityUsed ?? 0}/{item.capacity}
          </span>
        </div>
      )}
      {/* 5. Modifications — subsection label + list of mod names with optional ratings */}
      {/* 6. Notes — character-specific notes */}
      {/* 7. Source reference — dim footnote */}
      {extras?.page != null && (
        <p className="text-[10px] text-zinc-400 dark:text-zinc-600">
          {extras.source ?? "Core"} p.{extras.page}
        </p>
      )}
    </div>
  );
}
```

### Catalog Fallback

When displaying item stats, character item fields take priority but catalog data fills gaps. This pattern allows character-specific overrides while keeping catalog data as a baseline:

```tsx
const avail = item.availability ?? catalogItem?.availability;
const legality = item.legality ?? catalogItem?.legality;
const cost = item.cost || catalogItem?.cost || 0;
```

Use `findCatalogItem()` (or equivalent) to look up the catalog entry by name, then merge fields with nullish coalescing (`??`) for optional fields and logical OR (`||`) for numeric defaults.

### Collapsed Row Indicators

Collapsed rows can show small indicator icons pushed to the right side for at-a-glance visibility. The canonical example is the **wireless indicator**: a small cyan Wifi icon shown when the catalog item has a `wirelessBonus` field.

```tsx
{
  extras?.wirelessBonus && (
    <Wifi
      data-testid="wireless-icon"
      className="ml-auto h-3 w-3 shrink-0 text-cyan-500 dark:text-cyan-400"
    />
  );
}
```

- Use `ml-auto` to push the icon to the far right of the flex row
- Place it as the **last element** in the flex row so it anchors right
- Keep icons small (`h-3 w-3`) to avoid visual clutter
- Use semantic colors matching the indicator meaning (cyan for wireless)

### Key Rules

- **Row click = expand/collapse.** The entire row is the click target.
- **Collapsed row shows:** name + classification badge + primary value pill only. May also include a **wireless indicator icon** (cyan Wifi) pushed right when the item has a wireless bonus.
- **All detail stats** (handling, speed, mods, notes, etc.) go in the expanded section.
- **Stats resolve with catalog fallback:** character data takes priority, catalog fills gaps (see Catalog Fallback above).
- **Critical status** (e.g., pending badge) stays inline in the collapsed row for at-a-glance visibility.
- **Import** `ChevronDown`, `ChevronRight` from `lucide-react`.

## Interactive Value Pills (Dice Roller)

When a value pill opens a dice roller or triggers an action on click:

- **Row click = expand/collapse** (not dice roller)
- **Pill click = action** (dice roller) with `e.stopPropagation()` to prevent row toggle
- Keep tooltip hover for breakdown details alongside the click action

```tsx
{
  /* With tooltip + dice roller action */
}
<span
  className="ml-auto shrink-0"
  onClick={(e) => {
    e.stopPropagation();
    onSelect?.(id, pool, attr);
  }}
>
  <Tooltip content={<BreakdownTooltip />} delay={200} showArrow={false}>
    <AriaButton
      data-testid="dice-pool-pill"
      onPress={() => onSelect?.(id, pool, attr)}
      className="cursor-pointer rounded border border-emerald-500/20 bg-emerald-500/12 px-1.5 py-0.5 font-mono text-[10px] font-semibold text-emerald-600 dark:text-emerald-300 focus:outline-none focus:ring-2 focus:ring-emerald-500"
    >
      {pool}
    </AriaButton>
  </Tooltip>
</span>;

{
  /* Without tooltip — plain button */
}
<button
  data-testid="dice-pool-pill"
  onClick={(e) => {
    e.stopPropagation();
    onSelect?.(id, pool, attr);
  }}
  className="ml-auto shrink-0 cursor-pointer rounded border border-emerald-500/20 bg-emerald-500/12 px-1.5 py-0.5 font-mono text-[10px] font-semibold text-emerald-600 dark:text-emerald-300"
>
  {pool}
</button>;
```

**Why both `onClick` and `onPress`:** React Aria's `Button` intercepts pointer events, so the wrapper span's `onClick` doesn't fire in the real app — `onPress` handles it. But test mocks render a plain `<button>`, where `onPress` is ignored — so the `onClick` on the wrapper serves as a test fallback.

## Semantic Color Accents

When items have distinct semantic meaning (damage types, magic traditions, special stats), assign each a color config:

| Element | Dark Mode                            | Light Mode                         |
| ------- | ------------------------------------ | ---------------------------------- |
| Icon    | `{color}-500` (or `-400` for light)  | `{color}-600`                      |
| Label   | one shade lighter than icon (`-400`) | `{color}-700`                      |
| Pill bg | `{color}-500/15` (or `-400/12`)      | `bg-{color}-50 border-{color}-200` |

Established palette: `amber`, `emerald`, `cyan`, `purple`, `sky`, `rose`, `orange`. Prefer colors already used before introducing new ones.

## Secondary/Modifier Indicators

When items have modifiers, bonuses, or secondary values:

- **Only render when value > 0** — no empty brackets or zero indicators
- **Positive modifier pill:** `bg-emerald-500/15 text-emerald-400`, mono `text-[11px] font-semibold`, shows `+N` with directional icon (10px)
- **Modified main pill:** swap neutral for tinted: `bg-emerald-500/12 text-emerald-300 border border-emerald-500/20`
- **Negative modifiers:** use `rose` instead of `emerald`

## Tooltips & Interactive Elements

- Use `<Tooltip>` from `@/components/ui` with `<AriaButton>` from `react-aria-components` as trigger
- Wrap tooltip triggers in `<span onClick={e => e.stopPropagation()}>` if the row is clickable
- Tooltip content: `bg-zinc-900 border-zinc-700 rounded-lg p-2 text-[12px]`
- Multi-source tooltips: list each source, `border-zinc-600` separator + summary when >1 source

## Conditional Rendering

- Only render sections/items that have data — no empty groups
- Interactive pills fire `onSelect` (or established callback) via click/press
- Display-only items get no click handler

## Testing Notes

- Use `setupDisplayCardMock()` and `LUCIDE_MOCK` from `test-helpers.tsx` — never inline mocks
- `vi.mock("react-aria-components")` in shared test helpers is **hoisted by vitest** — any test importing from that file gets the mock
- The shared mock must include **all** react-aria-components exports used (e.g., `Button`, `Link`)
- Never use `new Proxy()` for `vi.mock("lucide-react")` — use explicit named icon exports
- Test files with JSX (even in mock factories) must use `.tsx` extension
- `ChevronDown` and `ChevronRight` are already in `LUCIDE_MOCK` in `test-helpers.tsx`
- Mock data for vehicles, drones, RCCs, armor, weapons, contacts, etc. are in `test-helpers.tsx`

### Expandable Row Test Pattern

Tests for detail content must **expand the row first** (click the row or expand-button):

```tsx
it("does not show expanded content by default", () => {
  render(<Component items={[MOCK_ITEM]} />);
  expect(screen.queryByTestId("expanded-content")).not.toBeInTheDocument();
});

it("expands row on click", async () => {
  const user = userEvent.setup();
  render(<Component items={[MOCK_ITEM]} />);
  await user.click(screen.getByTestId("expand-button"));
  expect(screen.getByTestId("expanded-content")).toBeInTheDocument();
});

it("collapses row on second click", async () => {
  const user = userEvent.setup();
  render(<Component items={[MOCK_ITEM]} />);
  await user.click(screen.getByTestId("expand-button"));
  await user.click(screen.getByTestId("expand-button"));
  expect(screen.queryByTestId("expanded-content")).not.toBeInTheDocument();
});
```

### Interactive Pill Test Pattern

When a pill triggers an action (e.g., dice roller), test that clicking the pill fires the callback and clicking the row does not:

```tsx
it("calls onSelect when dice pool pill clicked", () => {
  const onSelect = vi.fn();
  render(<Component items={[MOCK_ITEM]} onSelect={onSelect} />);
  fireEvent.click(screen.getByTestId("dice-pool-pill"));
  expect(onSelect).toHaveBeenCalledWith("item-id", 11, "AGI");
});

it("clicking row expands instead of triggering onSelect", () => {
  const onSelect = vi.fn();
  render(<Component items={[MOCK_ITEM]} onSelect={onSelect} />);
  fireEvent.click(screen.getByText("Item Name"));
  expect(onSelect).not.toHaveBeenCalled();
  expect(screen.getByTestId("expanded-content")).toBeInTheDocument();
});
```

Key test IDs: `expand-button`, `expanded-content`, `type-badge`, `primary-pill`, `rating-pill`, `dice-pool-pill`, `stat-*`, `notes`.

## Canonical Examples

Always read these before starting a redesign:

```
components/character/sheet/ArmorDisplay.tsx      — compact expandable rows, capacity bar, modifications, section grouping (Worn/Stored)
components/character/sheet/WeaponsDisplay.tsx     — compact expandable rows, weapon type annotation, semantic stat pills (DMG/AP/ACC/RCH/MODE/RC), dice pool pill, availability, ammo state, modifications, section grouping (Ranged/Melee)
components/character/sheet/VehiclesDisplay.tsx    — type guards, type badges, three-way sections, autosofts, notes
components/character/sheet/SkillsDisplay.tsx      — compact rows, dice pool pill with tooltip + dice roller click, row expand/collapse
components/character/sheet/AttributesDisplay.tsx  — compact rows, value pills, augmentation/essence tooltips
components/character/sheet/QualitiesDisplay.tsx   — expandable rows, karma pills, effect badges
components/character/sheet/GearDisplay.tsx        — category-grouped expandable rows, catalog integration (description, wireless bonus, source ref), catalog fallback for stats, wireless indicator icon
components/character/sheet/DrugsDisplay.tsx       — expandable rows, drug catalog integration (effects, addiction, delivery), catalog fallback for availability
```

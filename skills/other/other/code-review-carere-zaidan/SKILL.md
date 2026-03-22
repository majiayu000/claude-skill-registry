---
name: code-review
description: Provides code review rules, anti-patterns, scoring rubric, and duplication detection heuristics for the code-reviewer agent. Contains pattern catalog of all existing Zaidan UI components, hooks, and utilities. Defines standard component structure, review checklist, and output format. Use when reviewing SolidJS component code, checking for anti-patterns, or validating against Zaidan conventions.
---

# Zaidan Code Review Rules

Single source of truth for all code review rules, anti-patterns, scoring, and duplication detection in the Zaidan project. This is a KNOWLEDGE SKILL -- it provides review rules as reusable context. The `code-reviewer` agent references these tables and checklists when reviewing component code.

**IMPORTANT**: This skill is a **knowledge resource**. It does NOT perform reviews itself. Instead, it provides the rules, catalogs, and heuristics that the `code-reviewer` agent will reference when executing reviews. If called manually, explain what this skill covers and redirect the user to the `code-reviewer` agent, then stop.

**Coverage**: This skill defines the complete review framework including:
- Component pattern catalog (all 53 UI components, 2 hooks, 3 utilities)
- Standard component structure checklist
- Duplication detection heuristics (7 categories)
- Anti-pattern detection rules (10 categories)
- Scoring rubric (PASS / WARN / FAIL)
- Review output format specification

---

## Section 1: Purpose and Usage

This skill serves as the **single source of truth** for the `code-reviewer` agent. It is loaded automatically when the agent begins a review session and provides:

1. **Pattern Catalog** -- A comprehensive inventory of all existing Zaidan UI components, hooks, and utilities so the reviewer can detect duplication and reuse opportunities.
2. **Structure Checklist** -- The canonical component structure that all Zaidan components must follow, used as the review baseline.
3. **Duplication Heuristics** -- Rules for detecting code duplication across imports, patterns, hooks, utilities, cross-component similarities, block internals, and CSS/style strings.
4. **Anti-Pattern Rules** -- Specific patterns that must be flagged during review, including React remnants, SolidJS violations, and Zaidan convention violations.
5. **Scoring Rubric** -- How to classify review findings into PASS, WARN, or FAIL.
6. **Output Format** -- The exact JSON schema and summary line format the reviewer must produce.

**NOTE**: The component catalog below is a snapshot. At review time, the `code-reviewer` agent MUST glob `src/registry/kobalte/ui/*.tsx` and `src/registry/kobalte/hooks/*.ts` to validate against the actual filesystem, since components may be added or removed.

---

## Section 2: Component Pattern Catalog

### UI Components (`src/registry/kobalte/ui/`)

| Component | File | Key Exports | Primitive |
|---|---|---|---|
| Accordion | `accordion.tsx` | `Accordion`, `AccordionItem`, `AccordionTrigger`, `AccordionContent` | Kobalte (`@kobalte/core/accordion`) |
| Alert | `alert.tsx` | `Alert`, `AlertTitle`, `AlertDescription`, `AlertAction`, `alertVariants` | Kobalte (`@kobalte/core/alert`) |
| AlertDialog | `alert-dialog.tsx` | `AlertDialog`, `AlertDialogAction`, `AlertDialogCancel`, `AlertDialogContent`, `AlertDialogDescription`, `AlertDialogFooter`, `AlertDialogHeader`, `AlertDialogMedia`, `AlertDialogOverlay`, `AlertDialogPortal`, `AlertDialogTitle`, `AlertDialogTrigger` | Kobalte (`@kobalte/core/alert-dialog`) |
| AspectRatio | `aspect-ratio.tsx` | `AspectRatio`, `AspectRatioProps` | Native |
| Avatar | `avatar.tsx` | `Avatar`, `AvatarBadge`, `AvatarFallback`, `AvatarGroup`, `AvatarGroupCount`, `AvatarImage` | Kobalte (`@kobalte/core/image`) |
| Badge | `badge.tsx` | `Badge`, `badgeVariants` | Kobalte (`@kobalte/core/badge`) |
| Breadcrumb | `breadcrumb.tsx` | `Breadcrumb`, `BreadcrumbList`, `BreadcrumbItem`, `BreadcrumbLink`, `BreadcrumbPage`, `BreadcrumbSeparator`, `BreadcrumbEllipsis` | Kobalte (polymorphic only) |
| Button | `button.tsx` | `Button`, `ButtonProps`, `buttonVariants` | Kobalte (`@kobalte/core/button`) |
| ButtonGroup | `button-group.tsx` | `ButtonGroup`, `ButtonGroupText`, `ButtonGroupSeparator`, `buttonGroupVariants` | Native |
| Calendar | `calendar.tsx` | `Calendar`, `CalendarProps`, `CustomCellProps` | Corvu (`@corvu/calendar`) |
| Card | `card.tsx` | `Card`, `CardHeader`, `CardFooter`, `CardTitle`, `CardAction`, `CardDescription`, `CardContent` | Native |
| Carousel | `carousel.tsx` | `CarouselApi`, `Carousel`, `CarouselContent`, `CarouselItem`, `CarouselPrevious`, `CarouselNext`, `useCarousel` | Native (embla-carousel) |
| Chart | `chart.tsx` | `ChartContainer`, `ChartConfig`, `ChartContainerProps`, `useChart`, `chartTooltipDefaults`, `chartLegendDefaults`, `chartGridDefaults`, `chartXAxisDefaults`, `chartYAxisDefaults`, `chartColors`, `createChartColorConfig` | Native (echarts) |
| Checkbox | `checkbox.tsx` | `Checkbox`, `CheckboxLabel` | Kobalte (`@kobalte/core/checkbox`) |
| Collapsible | `collapsible.tsx` | `Collapsible`, `CollapsibleTrigger`, `CollapsibleContent` | Kobalte (`@kobalte/core/collapsible`) |
| Combobox | `combobox.tsx` | `Combobox`, `ComboboxContent`, `ComboboxControl`, `ComboboxEmpty`, `ComboboxInput`, `ComboboxItem`, `ComboboxSection`, `ComboboxSectionLabel`, `ComboboxSeparator`, `ComboboxTrigger` | Kobalte (`@kobalte/core/combobox`) |
| Command | `command.tsx` | `Command`, `CommandDialog`, `CommandInput`, `CommandList`, `CommandEmpty`, `CommandGroup`, `CommandItem`, `CommandShortcut`, `CommandSeparator` | Native (cmdk-solid) |
| ContextMenu | `context-menu.tsx` | `ContextMenu`, `ContextMenuTrigger`, `ContextMenuContent`, `ContextMenuItem`, `ContextMenuCheckboxItem`, `ContextMenuRadioItem`, `ContextMenuLabel`, `ContextMenuSeparator`, `ContextMenuShortcut`, `ContextMenuGroup`, `ContextMenuPortal`, `ContextMenuSub`, `ContextMenuSubContent`, `ContextMenuSubTrigger`, `ContextMenuRadioGroup` | Kobalte (`@kobalte/core/context-menu`) |
| Dialog | `dialog.tsx` | `Dialog`, `DialogClose`, `DialogContent`, `DialogDescription`, `DialogFooter`, `DialogHeader`, `DialogOverlay`, `DialogPortal`, `DialogTitle`, `DialogTrigger` | Kobalte (`@kobalte/core/dialog`) |
| Drawer | `drawer.tsx` | `Drawer`, `DrawerOverlay`, `DrawerTrigger`, `DrawerClose`, `DrawerContent`, `DrawerHeader`, `DrawerFooter`, `DrawerTitle`, `DrawerDescription` | Corvu (`@corvu/drawer`) |
| DropdownMenu | `dropdown-menu.tsx` | `DropdownMenu`, `DropdownMenuPortal`, `DropdownMenuTrigger`, `DropdownMenuContent`, `DropdownMenuGroup`, `DropdownMenuLabel`, `DropdownMenuItem`, `DropdownMenuCheckboxItem`, `DropdownMenuRadioGroup`, `DropdownMenuRadioItem`, `DropdownMenuSeparator`, `DropdownMenuShortcut`, `DropdownMenuSub`, `DropdownMenuSubTrigger`, `DropdownMenuSubContent` | Kobalte (`@kobalte/core/dropdown-menu`) |
| Empty | `empty.tsx` | `Empty`, `EmptyHeader`, `EmptyTitle`, `EmptyDescription`, `EmptyContent`, `EmptyMedia` | Native |
| Field | `field.tsx` | `Field`, `FieldLabel`, `FieldDescription`, `FieldError`, `FieldGroup`, `FieldLegend`, `FieldSeparator`, `FieldSet`, `FieldContent`, `FieldTitle`, `fieldVariants` | Native |
| HoverCard | `hover-card.tsx` | `HoverCard`, `HoverCardTrigger`, `HoverCardContent` | Kobalte (`@kobalte/core/hover-card`) |
| Input | `input.tsx` | `Input`, `InputProps` | Native |
| InputGroup | `input-group.tsx` | `InputGroup`, `InputGroupAddon`, `InputGroupButton`, `InputGroupText`, `InputGroupInput`, `InputGroupTextarea`, `InputGroupProps`, `InputGroupAddonProps`, `InputGroupButtonProps`, `InputGroupTextProps`, `InputGroupInputProps`, `InputGroupTextareaProps` | Native |
| InputOTP | `input-otp.tsx` | `InputOTP`, `InputOTPGroup`, `InputOTPSlot`, `InputOTPSeparator`, `InputOTPProps`, `InputOTPGroupProps`, `InputOTPSlotProps`, `InputOTPSeparatorProps` | Corvu (`@corvu/otp-field`) |
| Item | `item.tsx` | `Item`, `ItemMedia`, `ItemContent`, `ItemActions`, `ItemGroup`, `ItemSeparator`, `ItemTitle`, `ItemDescription`, `ItemHeader`, `ItemFooter`, `itemVariants`, `itemMediaVariants` | Native |
| Kbd | `kbd.tsx` | `Kbd`, `KbdGroup` | Native |
| Label | `label.tsx` | `Label` | Native |
| Menubar | `menubar.tsx` | `Menubar`, `MenubarCheckboxItem`, `MenubarContent`, `MenubarGroup`, `MenubarItem`, `MenubarLabel`, `MenubarMenu`, `MenubarPortal`, `MenubarRadioGroup`, `MenubarRadioItem`, `MenubarSeparator`, `MenubarShortcut`, `MenubarSub`, `MenubarSubContent`, `MenubarSubTrigger` | Kobalte (`@kobalte/core/menubar`) |
| NativeSelect | `native-select.tsx` | `NativeSelect`, `NativeSelectOptGroup`, `NativeSelectOption` | Native |
| NavigationMenu | `navigation-menu.tsx` | `NavigationMenu`, `NavigationMenuContent`, `NavigationMenuIndicator`, `NavigationMenuItem`, `NavigationMenuLink`, `NavigationMenuTrigger`, `navigationMenuTriggerStyle` | Kobalte (`@kobalte/core/navigation-menu`) |
| Pagination | `pagination.tsx` | `Pagination`, `PaginationContent`, `PaginationEllipsis`, `PaginationItem`, `PaginationLink`, `PaginationNext`, `PaginationPrevious` | Native |
| Popover | `popover.tsx` | `Popover`, `PopoverAnchor`, `PopoverArrow`, `PopoverCloseButton`, `PopoverContent`, `PopoverDescription`, `PopoverHeader`, `PopoverTitle`, `PopoverTrigger` | Kobalte (`@kobalte/core/popover`) |
| Progress | `progress.tsx` | `Progress`, `ProgressTrack`, `ProgressIndicator`, `ProgressLabel`, `ProgressValue` | Kobalte (polymorphic only) |
| RadioGroup | `radio-group.tsx` | `RadioGroup`, `RadioGroupItem` | Kobalte (polymorphic only) |
| Resizable | `resizable.tsx` | `ResizablePanelGroup`, `ResizablePanel`, `ResizableHandle` | Corvu (`@corvu/resizable`) |
| Select | `select.tsx` | `Select`, `SelectContent`, `SelectGroup`, `SelectItem`, `SelectLabel`, `SelectSeparator`, `SelectTrigger`, `SelectValue` | Kobalte (`@kobalte/core/select`) |
| Separator | `separator.tsx` | `Separator`, `SeparatorProps` | Kobalte (`@kobalte/core/separator`) |
| Sheet | `sheet.tsx` | `Sheet`, `SheetTrigger`, `SheetClose`, `SheetContent`, `SheetHeader`, `SheetFooter`, `SheetTitle`, `SheetDescription` | Kobalte (`@kobalte/core/dialog`) |
| Sidebar | `sidebar.tsx` | `Sidebar`, `SidebarContent`, `SidebarFooter`, `SidebarGroup`, `SidebarGroupAction`, `SidebarGroupContent`, `SidebarGroupLabel`, `SidebarHeader`, `SidebarInput`, `SidebarInset`, `SidebarMenu`, `SidebarMenuAction`, `SidebarMenuBadge`, `SidebarMenuButton`, `SidebarMenuItem`, `SidebarMenuSkeleton`, `SidebarMenuSub`, `SidebarMenuSubButton`, `SidebarMenuSubItem`, `SidebarProvider`, `SidebarRail`, `SidebarSeparator`, `SidebarTrigger`, `useSidebar`, `SidebarProps` | Kobalte (polymorphic only) |
| Skeleton | `skeleton.tsx` | `Skeleton` | Native |
| Slider | `slider.tsx` | `Slider` | Kobalte (polymorphic only) |
| Sonner | `sonner.tsx` | `Toaster` | Native (solid-sonner) |
| Spinner | `spinner.tsx` | `Spinner` | Native |
| Switch | `switch.tsx` | `Switch` | Kobalte (`@kobalte/core/switch`) |
| Table | `table.tsx` | `Table`, `TableHeader`, `TableBody`, `TableFooter`, `TableHead`, `TableRow`, `TableCell`, `TableCaption` | Native |
| Tabs | `tabs.tsx` | `Tabs`, `TabsList`, `TabsTrigger`, `TabsContent`, `tabsListVariants` | Kobalte (polymorphic only) |
| Textarea | `textarea.tsx` | `Textarea`, `TextareaProps` | Native |
| Toggle | `toggle.tsx` | `Toggle`, `ToggleProps`, `toggleVariants` | Kobalte (`@kobalte/core/toggle-button`) |
| ToggleGroup | `toggle-group.tsx` | `ToggleGroup`, `ToggleGroupItem`, `ToggleGroupProps` | Kobalte (polymorphic only) |
| Tooltip | `tooltip.tsx` | `Tooltip`, `TooltipTrigger`, `TooltipContent` | Kobalte (`@kobalte/core/tooltip`) |

### Hooks (`src/registry/kobalte/hooks/`)

| Hook | File | Purpose |
|---|---|---|
| `useColorMode` | `use-color-mode.ts` | Reads color mode (light/dark) from `ColorModeContext`. Must be used within `ColorModeProvider`. |
| `useIsMobile` | `use-mobile.ts` | Reactive mobile breakpoint detection (768px). Uses `createEffect` + `matchMedia` + `onCleanup`. |

### Shared Utilities (`src/lib/utils.ts`)

| Utility | File | Purpose |
|---|---|---|
| `cn()` | `src/lib/utils.ts` | Merges Tailwind CSS classes via `clsx` + `twMerge`. The canonical class merging function. |
| `getStorage()` | `src/lib/utils.ts` | Isomorphic cookie storage factory (server/client) using `@solid-primitives/storage`. |
| `flattenTocUrls()` | `src/lib/utils.ts` | Flattens nested TOC entries into a flat list of URL fragments for scroll spy. |

---

## Section 3: Standard Component Structure Checklist

Every Zaidan component MUST follow these conventions. Use this checklist during review.

### 3.1 Props Pattern

- **Interactive components using a Kobalte/Corvu primitive**: Use `PolymorphicProps<T, PrimitiveProps<T>>` with generic `<T extends ValidComponent = "element">` and intersect with `Pick<ComponentProps<T>, "class">` (and `"children"` if accessing children).
- **Simple components without primitive**: Use `ComponentProps<"element">` directly.
- **Custom props**: Intersect with a literal object type: `& { showCloseButton?: boolean }`.

Example (interactive):
```tsx
type DialogOverlayProps<T extends ValidComponent = "div"> = PolymorphicProps<
  T,
  DialogPrimitive.DialogOverlayProps<T>
> & Pick<ComponentProps<T>, "class">;
```

Example (simple):
```tsx
type DialogHeaderProps = ComponentProps<"div">;
```

### 3.2 Props Handling

1. **Extract `class`** (and any custom props) via `splitProps`: `const [local, others] = splitProps(props, ["class"]);`
2. **Merge defaults** via `mergeProps` BEFORE `splitProps` when defaults exist: `const mergedProps = mergeProps({ showCloseButton: true } as Props, props);`
3. **Type assertion** on the `splitProps` call when using generics: `splitProps(props as FooProps, [...])`
4. **Spread `{...others}` last** on the JSX element.

### 3.3 `data-slot` Attribute

- EVERY semantic element MUST have a `data-slot` attribute.
- Naming convention: `component-name` for root, `component-subpart` for children.
- Examples: `data-slot="button"`, `data-slot="dialog-trigger"`, `data-slot="accordion-content-inner"`.
- Interactive elements (buttons, triggers, inputs) REQUIRE `data-slot` (FAIL if missing).
- Non-interactive wrappers (layout divs) SHOULD have `data-slot` (WARN if missing).

### 3.4 CVA Variants

- Define at **module level** (top of file, outside component function).
- Always include `defaultVariants`.
- CSS class names MUST use `z-` prefix: `z-button`, `z-button-variant-default`, `z-button-size-sm`.
- Apply via `cn(variants({ ... }), local.class)`.

Example:
```tsx
const buttonVariants = cva("z-button inline-flex ...", {
  variants: {
    variant: { default: "z-button-variant-default", ... },
    size: { default: "z-button-size-default", ... },
  },
  defaultVariants: { variant: "default", size: "default" },
});
```

### 3.5 Class Merging

- ALWAYS use `cn()` from `@/lib/utils` to merge classes.
- Pattern: `class={cn("base-classes", local.class)}` -- user's `class` prop comes LAST.
- NEVER use raw `clsx()` or `twMerge()` directly in components.
- NEVER hardcode class strings without wrapping in `cn()` if a `class` prop could be merged.

### 3.6 Compound Component Exports

- ALL sub-parts MUST be named and exported.
- Export via a single `export { ... }` block at end of file.
- Include type exports where useful: `export { Button, type ButtonProps, buttonVariants }`.
- Root component name matches the filename (PascalCase): `button.tsx` exports `Button`.

### 3.7 SolidJS Patterns

- Use `<Show when={...}>` for conditional rendering (NEVER `{condition && <El />}`).
- Use `<For each={...}>` for list rendering (NEVER `{items.map(...)}`).
- Use `<Dynamic component={...}>` for runtime component selection.
- NEVER directly destructure props -- always use `splitProps`.
- Signals and stores are reactive -- do not access `.value`; call the signal: `signal()`.

---

## Section 4: Duplication Detection Heuristics

The `code-reviewer` agent MUST check for these 7 categories of duplication.

### 4.1 Import-Based Duplication

If a file imports directly from a `@kobalte/core/*` or `@corvu/*` package for a primitive that an existing Zaidan component already wraps, flag as a **potential reuse opportunity**.

**Detection**: Scan `import` statements for:
- `@kobalte/core/dialog` -- already wrapped by `Dialog` and `Sheet`
- `@kobalte/core/dropdown-menu` -- already wrapped by `DropdownMenu`
- `@kobalte/core/alert-dialog` -- already wrapped by `AlertDialog`
- `@kobalte/core/popover` -- already wrapped by `Popover`
- `@kobalte/core/tooltip` -- already wrapped by `Tooltip`
- `@kobalte/core/accordion` -- already wrapped by `Accordion`
- `@kobalte/core/button` -- already wrapped by `Button`
- `@kobalte/core/checkbox` -- already wrapped by `Checkbox`
- `@kobalte/core/select` -- already wrapped by `Select`
- `@kobalte/core/combobox` -- already wrapped by `Combobox`
- `@kobalte/core/context-menu` -- already wrapped by `ContextMenu`
- `@kobalte/core/hover-card` -- already wrapped by `HoverCard`
- `@kobalte/core/menubar` -- already wrapped by `Menubar`
- `@kobalte/core/navigation-menu` -- already wrapped by `NavigationMenu`
- `@kobalte/core/switch` -- already wrapped by `Switch`
- `@kobalte/core/separator` -- already wrapped by `Separator`
- `@kobalte/core/toggle-button` -- already wrapped by `Toggle`
- `@kobalte/core/collapsible` -- already wrapped by `Collapsible`
- `@kobalte/core/image` -- already wrapped by `Avatar`
- `@kobalte/core/badge` -- already wrapped by `Badge`
- `@kobalte/core/alert` -- already wrapped by `Alert`
- `@corvu/drawer` -- already wrapped by `Drawer`
- `@corvu/resizable` -- already wrapped by `Resizable`
- `@corvu/otp-field` -- already wrapped by `InputOTP`
- `@corvu/calendar` -- already wrapped by `Calendar`

**Exception**: Files within `src/registry/kobalte/ui/` themselves are the wrappers and should import primitives directly.

### 4.2 Pattern-Based Duplication

If code manually constructs a UI pattern that matches an existing Zaidan component, flag it:

| Manual Pattern | Existing Component |
|---|---|
| Modal/overlay with backdrop + content panel | `Dialog` or `AlertDialog` |
| Slide-in panel from edge | `Sheet` or `Drawer` |
| Floating content on hover/click | `Popover`, `HoverCard`, or `Tooltip` |
| Dropdown with items on click | `DropdownMenu` |
| Button next to each other with separators | `ButtonGroup` |
| Breadcrumb navigation with links/separators | `Breadcrumb` |
| Right-click context menu | `ContextMenu` |
| Collapsible section with trigger | `Collapsible` or `Accordion` |
| Tab navigation with panels | `Tabs` |
| Toggle/switch control | `Switch` or `Toggle` |
| Select/combobox with options | `Select` or `Combobox` |
| Command palette with search | `Command` |
| Progress bar with track/indicator | `Progress` |
| Slider with thumb/track | `Slider` |

### 4.3 Hook-Based Duplication

If code creates a local reactive pattern that duplicates an existing hook, flag it:

| Local Pattern | Existing Hook |
|---|---|
| `createEffect` + `onCleanup` with `matchMedia` for breakpoint detection | `useIsMobile` (`src/registry/kobalte/hooks/use-mobile.ts`) |
| `useContext` reading color mode / theme from context | `useColorMode` (`src/registry/kobalte/hooks/use-color-mode.ts`) |
| Manual `createSignal` + `createEffect` for debounce | find in `https://primitives.solidjs.community/package/scheduled#debounce` |

### 4.4 Utility-Based Duplication

Flag any of these patterns:

| Anti-Pattern | Correct Usage |
|---|---|
| `clsx(...)` used directly in a component | Use `cn()` from `@/lib/utils` |
| `twMerge(...)` used directly in a component | Use `cn()` from `@/lib/utils` |
| `clsx(...) + twMerge(...)` composed inline | Use `cn()` from `@/lib/utils` |
| Manual class string concatenation | Use `cn()` from `@/lib/utils` |

### 4.5 Cross-Component Duplication

When reviewing a batch of components, compare:

- **Export signatures**: If two components export nearly identical sub-part names (e.g., both export `FooContent`, `FooHeader`, `FooFooter`, `FooTitle`, `FooDescription`), check if one should compose the other.
- **CVA variant definitions**: If two components define variants with the same variant names and similar class strings, consider extracting a shared variant.
- **Tailwind class compositions**: If the same long class string appears across multiple components, consider extracting to a shared `z-` prefixed class or a CVA variant.

### 4.6 Block-Internal Duplication

For blocks (components composed of multiple files), check if:
- Components within the block duplicate logic that should be extracted to a shared block utility.
- Multiple files import the same set of sibling components -- may indicate a missing shared module.
- Context/provider patterns are duplicated instead of shared.

### 4.7 CSS/Style Duplication

Flag near-identical Tailwind class strings across components:
- Use Levenshtein similarity > 80% as the threshold for flagging.
- Focus on class strings longer than 30 characters (short utility classes are expected to repeat).
- Exclude `z-` prefixed theme classes from this check (they are designed to be reused via CSS).

---

## Section 5: Anti-Patterns

The following patterns MUST be flagged during review. Each is tagged with its severity.

### 5.1 React Remnants (FAIL)

| Pattern | Detection | Fix |
|---|---|---|
| `className` attribute or prop | Grep for `className` | Replace with `class` |
| `forwardRef` usage | Grep for `forwardRef` | Remove entirely (not needed in SolidJS) |
| `import * as React from "react"` | Grep for `from "react"` | Remove; use SolidJS imports |
| `useEffect` | Grep for `useEffect` | Replace with `createEffect` |
| `useState` | Grep for `useState` | Replace with `createSignal` |
| `useRef` | Grep for `useRef` | Replace with `let ref: HTMLElement` or variable |
| `useCallback` | Grep for `useCallback` | Remove (not needed in SolidJS) |
| `useMemo` | Grep for `useMemo` | Replace with `createMemo` |
| `React.ReactNode` | Grep for `ReactNode` | Replace with `JSX.Element` |
| `React.ComponentProps` | Grep for `React.ComponentProps` | Replace with `ComponentProps` from `solid-js` |

### 5.2 SolidJS Violations (FAIL)

| Pattern | Detection | Fix |
|---|---|---|
| Direct destructuring of props | Props accessed via `{ class, children, ...rest }` | Use `splitProps(props, ["class", "children"])` |
| Missing `splitProps` when accessing props | Component reads `props.class` and spreads `{...props}` | Extract via `splitProps`, spread `{...others}` |
| `{condition && <Element />}` | Grep for `&&` in JSX context | Use `<Show when={condition}>` |
| `{items.map(item => ...)}` | Grep for `.map(` in JSX context | Use `<For each={items}>` |
| Accessing signal with `.value` | Grep for `.value` on signals | Call signal as function: `signal()` |

### 5.3 Zaidan Convention Violations

| Pattern | Severity | Detection | Fix |
|---|---|---|---|
| Missing `data-slot` on interactive element | FAIL | Check `<button>`, `<input>`, `<a>`, Kobalte triggers/close buttons | Add `data-slot="component-name"` |
| Missing `data-slot` on non-interactive wrapper | WARN | Check `<div>`, `<span>`, `<section>` elements | Add `data-slot="component-subpart"` |
| `class` prop not extracted via `splitProps` | FAIL | `class` in JSX without `splitProps` | Use `splitProps(props, ["class"])` |
| `class` prop not merged via `cn()` | FAIL | `class={local.class}` without `cn()` | Use `class={cn("base", local.class)}` |
| Hardcoded class strings without `cn()` wrapper | WARN | Static `class="..."` on elements that accept a `class` prop | Wrap in `cn()` if the component accepts a `class` prop |
| Inline hook definitions duplicating registry hooks | WARN | Local `createEffect`+`matchMedia` or `useContext(ColorModeContext)` | Import from `@/registry/kobalte/hooks/*` |
| Manual event listener without `onCleanup` | FAIL | `addEventListener` without corresponding `onCleanup(() => removeEventListener(...))` | Add `onCleanup` to remove the listener |
| Missing `defaultVariants` in CVA | WARN | `cva()` call without `defaultVariants` key | Add `defaultVariants` |
| Non-polymorphic interactive component | WARN | Interactive component using `ComponentProps` instead of `PolymorphicProps` when it wraps a Kobalte primitive | Use `PolymorphicProps<T, PrimitiveProps<T>>` |
| Missing compound component exports | WARN | File defines multiple component parts but only exports the root | Export all sub-parts |

---

## Section 6: Scoring Rubric

### PASS

No issues found, or only trivial style preferences that do not affect correctness, accessibility, or consistency. Examples:
- Minor whitespace differences
- Optional comment style preferences
- Alternative but valid import grouping

### WARN

Minor issues that do not affect functionality but should be addressed for consistency. Examples:
- Missing optional `data-slot` on a non-interactive wrapper element
- Import order nit (imports are valid but not in canonical order)
- Potential but uncertain reuse opportunity (e.g., a pattern that MIGHT duplicate an existing component but could be intentionally different)
- Missing `defaultVariants` in a CVA definition
- Non-polymorphic interactive component that could benefit from polymorphism
- Missing compound component exports (only root exported)

### FAIL

Critical issues that MUST be fixed before the component can be merged. Examples:
- Any React remnant (`className`, `forwardRef`, `useEffect`, `useState`, `useRef`, `useCallback`, `useMemo`, `React.ReactNode`)
- Missing `splitProps` when props are accessed and spread
- Direct primitive import (`@kobalte/core/*`, `@corvu/*`) when a Zaidan wrapper exists (outside of `src/registry/kobalte/ui/`)
- Broken type safety (incorrect generic constraints, missing type assertions)
- Missing required `data-slot` on interactive elements (buttons, triggers, inputs, links)
- Duplicated utility function that exists in `@/lib/utils`
- Manual event listener without `onCleanup`
- Direct props destructuring instead of `splitProps`

---

## Section 7: Review Output Format

### Per-File Review Result (JSON Schema)

```json
{
  "file": "src/path/to/file.tsx",
  "score": "PASS" | "WARN" | "FAIL",
  "issues": [
    {
      "line": 42,
      "severity": "FAIL" | "WARN",
      "category": "react-remnant" | "solidjs-violation" | "convention-violation" | "duplication" | "type-safety",
      "message": "Description of the issue",
      "suggestion": "How to fix it",
      "fixed": true | false
    }
  ],
  "summary": "Brief overall assessment of this file"
}
```

### Per-Component Aggregate Result (JSON Schema)

```json
{
  "component": "ComponentName",
  "primitive": "Kobalte" | "Corvu" | "Native",
  "files": {
    "reviewed": 3,
    "total": 3
  },
  "score": "PASS" | "WARN" | "FAIL",
  "issues": {
    "total": 5,
    "fail": 2,
    "warn": 3,
    "fixed": 1
  },
  "fileResults": [ /* array of per-file results */ ],
  "duplicationFlags": [
    {
      "type": "import-based" | "pattern-based" | "hook-based" | "utility-based" | "cross-component" | "block-internal" | "css-style",
      "description": "What was detected",
      "existingComponent": "Name of existing component/hook/utility",
      "severity": "WARN" | "FAIL"
    }
  ]
}
```

### REVIEW Summary Line

For sync command parsing, the final review output MUST include a summary line in this exact format:

```
REVIEW: {PASS|WARN|FAIL} | Component: <name> | Primitive: <primitive> | Files: <reviewed>/<total> | Issues: <count> | Fixed: <count>
```

Examples:
```
REVIEW: PASS | Component: Button | Primitive: Kobalte | Files: 1/1 | Issues: 0 | Fixed: 0
REVIEW: WARN | Component: CustomCard | Primitive: Native | Files: 2/2 | Issues: 3 | Fixed: 1
REVIEW: FAIL | Component: DataTable | Primitive: Kobalte | Files: 5/5 | Issues: 7 | Fixed: 2
```

The aggregate score is determined by the **highest severity** across all files:
- If any file has a FAIL issue, the aggregate is FAIL.
- If no FAIL but any WARN, the aggregate is WARN.
- Otherwise, PASS.

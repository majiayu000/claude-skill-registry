---
name: web-dnd-dnd-kit
description: Drag and drop with @dnd-kit - draggable, droppable, sortable, collision detection, sensors, accessibility
---

# @dnd-kit Drag and Drop Patterns

> **Quick Guide:** Use `@dnd-kit/core` for basic drag/drop (`useDraggable`, `useDroppable`, `DndContext`). Use `@dnd-kit/sortable` for sortable lists (`useSortable`, `SortableContext`, `arrayMove`). Use `DragOverlay` for cross-container drag, scrollable containers, and smooth drop animations. Configure sensors for pointer/touch/keyboard input with activation constraints. Always provide keyboard and screen reader accessibility via `KeyboardSensor` and custom `announcements`.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST wrap all drag-and-drop content in a `<DndContext>` provider -- hooks only work inside DndContext)**

**(You MUST use `DragOverlay` when items move between containers or live in scrollable containers -- transform alone breaks in these cases)**

**(You MUST configure `KeyboardSensor` with `sortableKeyboardCoordinates` for sortable lists -- keyboard users cannot reorder without it)**

**(You MUST keep `DragOverlay` always mounted and conditionally render its children -- unmounting DragOverlay breaks drop animations)**

**(You MUST use named constants for all activation constraints, distances, and timing values -- NO magic numbers)**

</critical_requirements>

---

**Auto-detection:** @dnd-kit, dnd-kit, DndContext, useDraggable, useDroppable, useSortable, SortableContext, DragOverlay, useSensors, useSensor, PointerSensor, KeyboardSensor, closestCenter, closestCorners, rectIntersection, pointerWithin, arrayMove, sortableKeyboardCoordinates, CSS.Transform, @dnd-kit/core, @dnd-kit/sortable, @dnd-kit/utilities, @dnd-kit/modifiers

**When to use:**

- Building sortable lists (reorderable todo, playlist, sidebar navigation)
- Building Kanban boards with cross-container item movement
- Implementing drag handles for specific activation areas
- Creating droppable zones (file upload targets, trash bins, category bins)
- Adding keyboard and screen reader accessible drag interactions

**When NOT to use:**

- Simple reordering without drag UX (use array manipulation + buttons instead)
- Drag interactions that only need native HTML5 drag-and-drop (e.g., file drops from OS)
- Complex physics-based drag (consider a gesture/spring animation library instead)

**Key patterns covered:**

- DndContext + useDraggable + useDroppable for basic drag/drop
- SortableContext + useSortable + arrayMove for sortable lists
- DragOverlay for cross-container drag and smooth animations
- Sensor configuration (pointer, touch, keyboard) with activation constraints
- Collision detection strategies (closestCenter, closestCorners, pointerWithin, rectIntersection)
- Sorting strategies (vertical, horizontal, rect/grid)
- Keyboard and screen reader accessibility
- Multi-container sortable (Kanban boards)
- Modifiers for axis locking and boundary constraints

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) - DndContext, useDraggable, useDroppable, useSortable, sensors, collision detection, accessibility
- [examples/advanced.md](examples/advanced.md) - Multi-container Kanban, DragOverlay, modifiers, custom collision detection
- [reference.md](reference.md) - Decision frameworks, API quick reference, sorting strategies, anti-patterns

---

<philosophy>

## Philosophy

@dnd-kit is a modular, lightweight drag-and-drop toolkit for React built around hooks. It separates concerns into focused packages: `@dnd-kit/core` for the drag/drop primitives, `@dnd-kit/sortable` for list reordering, `@dnd-kit/utilities` for CSS transform helpers, and `@dnd-kit/modifiers` for movement constraints.

**Core principles:**

1. **Hooks-first** -- `useDraggable`, `useDroppable`, and `useSortable` keep drag logic colocated with components
2. **Sensor-driven input** -- Pointer, touch, and keyboard inputs are separate sensor plugins, not hardcoded behavior
3. **Collision detection is pluggable** -- Choose the right algorithm for your layout (list vs grid vs stacked containers)
4. **Accessibility by default** -- Built-in ARIA attributes, keyboard navigation, and screen reader announcements
5. **No DOM manipulation** -- Uses CSS transforms for positioning, not DOM reordering during drag

**Package overview:**

| Package              | Purpose                                                                                          |
| -------------------- | ------------------------------------------------------------------------------------------------ |
| `@dnd-kit/core`      | DndContext, useDraggable, useDroppable, DragOverlay, sensors, collision detection                |
| `@dnd-kit/sortable`  | SortableContext, useSortable, sorting strategies, arrayMove, sortableKeyboardCoordinates         |
| `@dnd-kit/utilities` | CSS.Transform.toString, CSS.Transition.toString                                                  |
| `@dnd-kit/modifiers` | restrictToVerticalAxis, restrictToHorizontalAxis, restrictToParentElement, restrictToWindowEdges |

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Basic Drag and Drop

`DndContext` is the provider that connects draggable and droppable elements. `useDraggable` makes an element draggable. `useDroppable` makes an element a drop target.

```tsx
import { DndContext, type DragEndEvent } from "@dnd-kit/core";

function App() {
  const [parent, setParent] = useState<string | null>(null);

  function handleDragEnd(event: DragEndEvent) {
    const { over } = event;
    setParent(over ? String(over.id) : null);
  }

  return (
    <DndContext onDragEnd={handleDragEnd}>
      <DraggableItem id="item-1" />
      <DroppableZone id="zone-a">
        {parent === "zone-a" && <span>Dropped here</span>}
      </DroppableZone>
    </DndContext>
  );
}
```

**Why good:** DndContext wraps all participants, event handler updates state on drop, draggable and droppable use unique string IDs

See [examples/core.md](examples/core.md) Pattern 1 for full useDraggable and useDroppable implementations with TypeScript types.

---

### Pattern 2: Sortable Lists

`SortableContext` + `useSortable` provides reorderable lists. Use `arrayMove` from `@dnd-kit/sortable` to update state on drag end.

```tsx
import { DndContext, closestCenter, type DragEndEvent } from "@dnd-kit/core";
import {
  SortableContext,
  arrayMove,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";

function SortableList() {
  const [items, setItems] = useState(["a", "b", "c", "d"]);

  function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;
    if (over && active.id !== over.id) {
      setItems((prev) => {
        const oldIndex = prev.indexOf(String(active.id));
        const newIndex = prev.indexOf(String(over.id));
        return arrayMove(prev, oldIndex, newIndex);
      });
    }
  }

  return (
    <DndContext collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
      <SortableContext items={items} strategy={verticalListSortingStrategy}>
        {items.map((id) => (
          <SortableItem key={id} id={id} />
        ))}
      </SortableContext>
    </DndContext>
  );
}
```

**Why good:** closestCenter is forgiving for vertical lists, verticalListSortingStrategy optimizes transform calculations, arrayMove produces a new array (immutable)

See [examples/core.md](examples/core.md) Pattern 2 for the full SortableItem component using useSortable and CSS.Transform.

---

### Pattern 3: DragOverlay

Use `DragOverlay` instead of transforming the dragged element directly when items move between containers, live in scrollable/virtualized containers, or need custom drag previews.

```tsx
import {
  DndContext,
  DragOverlay,
  type DragStartEvent,
  type DragEndEvent,
} from "@dnd-kit/core";

function Board() {
  const [activeId, setActiveId] = useState<string | null>(null);

  return (
    <DndContext
      onDragStart={(event: DragStartEvent) =>
        setActiveId(String(event.active.id))
      }
      onDragEnd={(event: DragEndEvent) => {
        handleDragEnd(event);
        setActiveId(null);
      }}
    >
      {/* containers and sortable items */}
      <DragOverlay>
        {activeId ? <ItemPreview id={activeId} /> : null}
      </DragOverlay>
    </DndContext>
  );
}
```

**Key rules:** Keep `DragOverlay` always mounted (conditionally render children, not the component). Children rendered inside DragOverlay must NOT use `useDraggable`. Default drop animation is 250ms ease -- disable with `dropAnimation={null}`.

See [examples/advanced.md](examples/advanced.md) Pattern 1 for DragOverlay with sortable lists and custom drop animations.

---

### Pattern 4: Sensors and Activation Constraints

Sensors control which input methods activate dragging. Use `useSensors` to compose multiple sensors with activation constraints.

```tsx
import {
  useSensor,
  useSensors,
  PointerSensor,
  KeyboardSensor,
} from "@dnd-kit/core";
import { sortableKeyboardCoordinates } from "@dnd-kit/sortable";

const ACTIVATION_DISTANCE_PX = 8;

const sensors = useSensors(
  useSensor(PointerSensor, {
    activationConstraint: { distance: ACTIVATION_DISTANCE_PX },
  }),
  useSensor(KeyboardSensor, {
    coordinateGetter: sortableKeyboardCoordinates,
  }),
);

<DndContext sensors={sensors}>{/* ... */}</DndContext>;
```

**Why good:** distance constraint prevents accidental drags on click, KeyboardSensor with sortableKeyboardCoordinates enables arrow-key reordering, named constant for distance threshold

**Sensor types:** `PointerSensor` (unified pointer events), `MouseSensor` (mouse only), `TouchSensor` (touch with delay support), `KeyboardSensor` (arrow keys + Space/Enter)

See [examples/core.md](examples/core.md) Pattern 3 for all sensor configurations including touch delay and tolerance.

---

### Pattern 5: Collision Detection

Choose the collision algorithm based on your layout.

| Algorithm          | Import          | Best for                                         |
| ------------------ | --------------- | ------------------------------------------------ |
| `rectIntersection` | `@dnd-kit/core` | General drop zones (default)                     |
| `closestCenter`    | `@dnd-kit/core` | Sortable lists -- forgiving, no overlap required |
| `closestCorners`   | `@dnd-kit/core` | Stacked/overlapping containers (Kanban columns)  |
| `pointerWithin`    | `@dnd-kit/core` | Precision drop -- pointer must be inside target  |

**Gotcha:** `pointerWithin` only works with pointer-based sensors. Compose it with a fallback for keyboard support.

See [examples/core.md](examples/core.md) Pattern 4 for collision detection selection and custom composition.

---

### Pattern 6: Sorting Strategies

Choose the strategy based on list orientation.

| Strategy                        | Import              | Use case                                      |
| ------------------------------- | ------------------- | --------------------------------------------- |
| `rectSortingStrategy`           | `@dnd-kit/sortable` | Grids (default, does NOT support virtualized) |
| `verticalListSortingStrategy`   | `@dnd-kit/sortable` | Vertical lists (supports virtualized)         |
| `horizontalListSortingStrategy` | `@dnd-kit/sortable` | Horizontal lists (supports virtualized)       |
| `rectSwappingStrategy`          | `@dnd-kit/sortable` | Swap mode (items trade positions)             |

Always match the strategy to your layout -- using `rectSortingStrategy` on a vertical list produces suboptimal animations.

---

### Pattern 7: Keyboard and Screen Reader Accessibility

@dnd-kit provides built-in accessibility. `useDraggable` applies `role="button"`, `aria-roledescription="draggable"`, `tabindex="0"`, and links to screen reader instructions via `aria-describedby`.

Customize announcements via the `announcements` prop on DndContext:

```tsx
const announcements = {
  onDragStart({ active }: { active: { id: UniqueIdentifier } }) {
    return `Picked up item ${active.id}`;
  },
  onDragOver({
    active,
    over,
  }: {
    active: { id: UniqueIdentifier };
    over: { id: UniqueIdentifier } | null;
  }) {
    if (over) return `Item ${active.id} moved over ${over.id}`;
    return `Item ${active.id} is no longer over a drop target`;
  },
  onDragEnd({
    active,
    over,
  }: {
    active: { id: UniqueIdentifier };
    over: { id: UniqueIdentifier } | null;
  }) {
    if (over) return `Item ${active.id} dropped on ${over.id}`;
    return `Item ${active.id} was dropped`;
  },
  onDragCancel({ active }: { active: { id: UniqueIdentifier } }) {
    return `Dragging cancelled. Item ${active.id} was dropped`;
  },
};

<DndContext announcements={announcements}>{/* ... */}</DndContext>;
```

**Why good:** Screen readers announce drag state changes in real time, position-based messages ("position 2 of 5") are more useful than generic "moved over" messages

See [examples/core.md](examples/core.md) Pattern 5 for position-based announcements and custom screen reader instructions.

---

### Pattern 8: Multi-Container Sortable (Kanban)

For Kanban boards, each column has its own `SortableContext`. Items move between containers via `onDragOver` (update state as item crosses boundaries) and `onDragEnd` (finalize position).

Key decisions for multi-container:

- Use `closestCorners` collision detection (handles stacked columns better than closestCenter)
- Use `DragOverlay` (items unmount from source container during cross-container drag)
- Track `activeId` to render the drag preview in the overlay
- Use `onDragOver` for real-time container transfers, `onDragEnd` for final placement

See [examples/advanced.md](examples/advanced.md) Pattern 2 for the complete Kanban implementation.

---

### Pattern 9: Modifiers

Modifiers constrain drag movement. Apply to `DndContext` (affects all dragging) or `DragOverlay` (affects overlay only).

```tsx
import {
  restrictToVerticalAxis,
  restrictToParentElement,
} from "@dnd-kit/modifiers";

<DndContext modifiers={[restrictToVerticalAxis]}>{/* ... */}</DndContext>;
```

| Modifier                   | Package              | Effect                            |
| -------------------------- | -------------------- | --------------------------------- |
| `restrictToVerticalAxis`   | `@dnd-kit/modifiers` | Lock movement to Y axis           |
| `restrictToHorizontalAxis` | `@dnd-kit/modifiers` | Lock movement to X axis           |
| `restrictToParentElement`  | `@dnd-kit/modifiers` | Constrain to parent bounds        |
| `restrictToWindowEdges`    | `@dnd-kit/modifiers` | Prevent dragging outside viewport |

Different modifiers can be applied to DndContext and DragOverlay independently.

</patterns>

---

<decision_framework>

## Decision Framework

### Which Package Do I Need?

```
Do you need sortable lists?
|-- YES -> @dnd-kit/core + @dnd-kit/sortable (+ @dnd-kit/utilities for CSS.Transform)
+-- NO  -> Just drag/drop zones?
    +-- YES -> @dnd-kit/core only
```

### Transform vs DragOverlay

```
Do items move between containers?
|-- YES -> Use DragOverlay (items unmount from source during drag)
+-- NO  -> Is the draggable inside a scrollable/virtualized container?
    |-- YES -> Use DragOverlay (avoids overflow clipping)
    +-- NO  -> Do you need a custom drag preview different from the source?
        |-- YES -> Use DragOverlay
        +-- NO  -> Transform approach is sufficient (simpler)
```

### Collision Detection

```
Single sortable list?
|-- YES -> closestCenter (forgiving, no overlap needed)
+-- NO  -> Stacked containers (Kanban columns)?
    |-- YES -> closestCorners (better for overlapping droppables)
    +-- NO  -> Precision drop targets (trash bin, category bins)?
        |-- YES -> pointerWithin (only triggers when pointer is inside)
        +-- NO  -> rectIntersection (default, general purpose)
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Missing `DndContext` wrapper -- useDraggable/useDroppable/useSortable fail silently without it
- Conditionally mounting/unmounting `DragOverlay` -- breaks drop animations; always mount it, conditionally render children
- Missing `KeyboardSensor` -- keyboard users cannot interact with drag-and-drop at all
- Using `closestCenter` for stacked containers (Kanban) -- often selects the column instead of items within; use `closestCorners`
- Forgetting `sortableKeyboardCoordinates` on KeyboardSensor for sortable lists -- arrow keys move by pixels instead of to next item
- Mutating state in onDragEnd instead of producing new arrays -- `arrayMove` returns a new array; do not use `.splice()` directly on state

**Medium Priority Issues:**

- Using `rectSortingStrategy` (default) for vertical-only lists -- `verticalListSortingStrategy` is more performant and supports virtualization
- Missing activation constraints on PointerSensor -- accidental drags fire on every click
- Not providing custom `announcements` -- default messages use IDs which are meaningless to screen reader users
- Applying `useDraggable` inside DragOverlay children -- the overlay renders a preview, not an interactive draggable

**Gotchas & Edge Cases:**

- `useDraggable` and `useDroppable` can share the same `id` (they use separate stores), but `useSortable` combines both so its `id` must be unique across draggables AND droppables
- `SortableContext` `items` prop must match the order of rendered children -- mismatches cause animation glitches
- `pointerWithin` only works with pointer-based sensors -- compose with `closestCenter` fallback for keyboard support
- `CSS.Transform.toString()` returns `undefined` when transform is `null` -- safe to pass directly to `style.transform`
- Transform values include `scaleX`/`scaleY` -- if you don't want scaling, destructure and only use `x`/`y` with `CSS.Translate.toString()`
- `DragOverlay` is NOT rendered in a portal by default -- use `createPortal` if you need it to escape overflow/stacking contexts
- The `data` argument on useDraggable/useDroppable is available in event handlers via `active.data.current` and `over.data.current` -- useful for carrying metadata (type, container ID)
- `arrayMove` is a pure utility -- it does not update state; you must call your setter with its return value
- Screen reader instructions default to English only -- provide `screenReaderInstructions` prop for localization

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST wrap all drag-and-drop content in a `<DndContext>` provider -- hooks only work inside DndContext)**

**(You MUST use `DragOverlay` when items move between containers or live in scrollable containers -- transform alone breaks in these cases)**

**(You MUST configure `KeyboardSensor` with `sortableKeyboardCoordinates` for sortable lists -- keyboard users cannot reorder without it)**

**(You MUST keep `DragOverlay` always mounted and conditionally render its children -- unmounting DragOverlay breaks drop animations)**

**(You MUST use named constants for all activation constraints, distances, and timing values -- NO magic numbers)**

**Failure to follow these rules will break drag interactions, keyboard accessibility, and drop animations.**

</critical_reminders>

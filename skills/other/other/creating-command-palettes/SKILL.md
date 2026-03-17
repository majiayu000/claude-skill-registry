---
name: Command Palette Developer
description: This skill should be used when the user asks to "create a command palette", "build a command palette", "add command palette", "implement ⌘K search", "create search modal", "build keyboard navigation", "add command menu", "create Raycast-style interface", "build spotlight search", or mentions cmdk, command bar, command menu, or keyboard-first navigation. Provides comprehensive guidance for building professional command palettes with React, TypeScript, Tailwind, and modern tooling including cmdk, Floating UI, Zustand, Tanstack Query, and Tanstack Virtual.
version: 1.0.0
---

# Command Palette Development

Build professional command palette interfaces for web applications using React, TypeScript, and Tailwind CSS. Command palettes provide keyboard-first navigation that enables power users to access functionality without leaving the keyboard, combining CLI efficiency with GUI discoverability.

## Purpose & When to Use

Command palettes solve the tension between feature-rich applications and clean interfaces. Instead of cluttering screens with buttons and menus, palettes consolidate functionality into a searchable, keyboard-driven interface that appears on demand (typically via ⌘K or ⌘+Shift+P).

Use command palettes when building applications that:
- Have numerous actions or navigation targets (20+ commands)
- Serve power users who prefer keyboard workflows
- Need searchable, discoverable functionality
- Require context-aware command suggestions
- Want to provide multi-step command flows (e.g., select repository → choose action)

This skill provides generator scripts, templates, examples, and comprehensive guidance for implementing command palettes matching the quality of Raycast, Linear, GitHub, and Notion.

### Choosing Implementation Patterns

**Modal Palette** - Centered overlay with backdrop (⌘K standard):
- Use for: App-wide actions, global search, navigation
- Examples: GitHub's command palette, VS Code's command palette
- Generated with: `create-command-palette.sh --type modal`

**Embedded Palette** - Floating element attached to trigger:
- Use for: Contextual actions, inline search, form controls
- Examples: Notion's slash commands, mention autocomplete
- Generated with: `create-command-palette.sh --type embedded`

**Drawer Palette** - Slide-in panel from screen edge:
- Use for: Filter panels, advanced search, settings navigation
- Examples: Raycast's Store, application settings
- Generated with: `create-command-palette.sh --type drawer`

## Quick Start Guide

### 1. Initial Setup

Install dependencies and create base configuration:

```bash
cd /path/to/your/project
/path/to/skills/command-palette-dev/scripts/setup-palette-stack.sh
```

This script:
- Detects your package manager (npm/pnpm/yarn/bun)
- Installs required packages: `cmdk`, `@floating-ui/react`, `zustand`, `@tanstack/react-query`, `@tanstack/react-virtual`
- Creates `ThemeProvider.tsx` and `CommandProvider.tsx`
- Sets up `command-registry.ts` for command registration
- Adds Tailwind configuration for palette variants
- Validates existing dependencies and suggests remediation if issues found

### 2. Generate Your First Palette

Create a basic modal command palette:

```bash
./scripts/create-command-palette.sh \
  --type modal \
  --name SearchPalette \
  --output ./src/components
```

This generates:
- `SearchPalette.tsx` - Main component with keyboard navigation
- `SearchPalette.types.ts` - TypeScript interfaces
- `index.ts` - Barrel export

### 3. Integrate into Application

Wrap your app with providers:

```typescript
// src/App.tsx
import { ThemeProvider } from './providers/ThemeProvider';
import { CommandProvider } from './providers/CommandProvider';
import { SearchPalette } from './components/SearchPalette';

function App() {
  return (
    <ThemeProvider>
      <CommandProvider>
        <YourApp />
        <SearchPalette />
      </CommandProvider>
    </ThemeProvider>
  );
}
```

Register commands:

```typescript
// Anywhere in your app
import { useCommandRegistry } from './providers/CommandProvider';

function MyComponent() {
  const registry = useCommandRegistry();

  useEffect(() => {
    registry.register({
      id: 'navigate-home',
      label: 'Go to Dashboard',
      keywords: ['home', 'dashboard', 'main'],
      shortcut: 'g then d',
      icon: HomeIcon,
      onSelect: () => navigate('/'),
    });
  }, []);
}
```

### 4. Customize Layout and Results

Generate specific layout patterns:

```bash
# Two-column with preview panel (Raycast style)
./scripts/create-palette-layout.sh \
  --layout two-column \
  --name FileSearch \
  --with-preview

# Card grid for rich results (Raycast Store style)
./scripts/create-palette-layout.sh \
  --layout card-grid \
  --name StorePalette \
  --virtualized
```

Create typed result components:

```bash
# Person results with avatars
./scripts/create-result-type.sh \
  --type person \
  --name PersonResult

# File results with icons and metadata
./scripts/create-result-type.sh \
  --type file \
  --name FileResult \
  --with-actions
```

## Core Concepts

### Command Palette Anatomy

Every command palette consists of four essential parts:

1. **Trigger** - Keyboard shortcut or button that opens the palette (⌘K, ⌘+Shift+P)
2. **Input Field** - Search box with real-time fuzzy filtering
3. **Results List** - Filtered commands with keyboard navigation (arrow keys, enter)
4. **Footer** (optional) - Keyboard legend showing available shortcuts

The cmdk library handles filtering, keyboard navigation, and accessibility automatically. Focus on command registration and result rendering.

### Layout Patterns

Command palettes support multiple layout configurations depending on data richness and use case:

**Single-Column List** - Basic vertical list of results:
- Best for: Simple actions, text-heavy commands, mobile
- Performance: Excellent (handles 2,000-3,000 items)
- Reference: `references/layouts.md` for implementation details

**Two-Column with Preview** - List on left, detail panel on right:
- Best for: Files, documents, rich content needing preview
- Examples: Raycast file search, GitHub repository picker
- Requires: Preview component that updates on selection change

**Multi-Panel** - Sidebar filters + center results + right details:
- Best for: Complex filtering, data tables, admin panels
- Examples: AWS console command palette
- Consideration: Responsive behavior on smaller screens

**Card Grid** - Rich cards with images, badges, metadata:
- Best for: Extensions, plugins, visual content
- Examples: Raycast Store, Figma plugin browser
- Requires: Virtual scrolling for 100+ items

**Horizontal Cards + Lists** - Mixed layout with scrollable cards and list items:
- Best for: Grouped content types, contextual results
- Examples: Linear's command palette
- Implementation: Combine multiple result type components

For detailed layout implementations and responsive strategies, see `references/layouts.md`.

### Result Types

Different command types require different visual presentations:

- **Person** - Avatar, name, email/role, status indicators
- **File** - File type icon, name, size, modification date
- **Action** - Action icon, label, description, keyboard shortcut
- **Card** - Image, title, description, badges, metadata

Generate result components with `create-result-type.sh` to get type-safe, accessible implementations matching your design system.

### State Management with Zustand

Command palettes maintain several state concerns:

```typescript
interface CommandPaletteState {
  isOpen: boolean;              // Palette visibility
  searchQuery: string;          // Current search text
  selectedId: string | null;    // Active result
  recentCommands: Command[];    // Usage history
  favorites: string[];          // Pinned commands
  commandStack: Command[];      // Multi-step navigation breadcrumb
}
```

The generated `CommandProvider` uses Zustand for lightweight, performant state management. For server-side search, Tanstack Query handles caching and loading states separately.

Detailed state patterns and integration with Tanstack Query are documented in `references/state-management.md`.

### Theming System

All generated palettes support three theme modes:
- **Light** - Light backgrounds, dark text
- **Dark** - Dark backgrounds, light text
- **System** - Follows OS preference via `prefers-color-scheme`

Themes use CSS variables for runtime switching without re-renders:

```css
:root {
  --palette-bg: white;
  --palette-text: black;
}

[data-theme="dark"] {
  --palette-bg: #1a1a1a;
  --palette-text: white;
}
```

Tailwind's dark mode integrates seamlessly. For custom theme creation and per-palette overrides, see `references/theming.md`.

## Generator Scripts Guide

Five generator scripts create components without reading templates into context:

### create-command-palette.sh

Generate complete palette components:

```bash
./scripts/create-command-palette.sh \
  --type modal|embedded|drawer \
  --name ComponentName \
  --output ./src/components \
  --theme light|dark|system
```

**Flags:**
- `--type` (required) - Palette variant: modal, embedded, drawer
- `--name` (required) - Component name in PascalCase
- `--output` (default: ./src/components) - Output directory
- `--theme` (default: system) - Theme mode
- `--with-footer` (default: true) - Include keyboard legend
- `--with-groups` (default: true) - Support command groups
- `--interactive` - Prompt for all options

### create-palette-layout.sh

Generate layout-specific components:

```bash
./scripts/create-palette-layout.sh \
  --layout single-column|two-column|multi-panel|card-grid|horizontal-cards \
  --name ComponentName \
  --virtualized
```

**Flags:**
- `--layout` (required) - Layout pattern
- `--name` (required) - Component name
- `--output` (default: ./src/components) - Output directory
- `--virtualized` (default: false) - Enable Tanstack Virtual for 10k+ items
- `--with-preview` (default: true for two-column) - Add preview panel

### create-result-type.sh

Generate typed result components:

```bash
./scripts/create-result-type.sh \
  --type person|file|action|card \
  --name ResultComponent \
  --with-actions
```

**Flags:**
- `--type` (required) - Result type
- `--name` (required) - Component name
- `--output` (default: ./src/components/results) - Output directory
- `--with-avatar` (default: true for person) - Include avatar
- `--with-icon` (default: true) - Include icon
- `--with-metadata` (default: true) - Include metadata line
- `--with-actions` (default: false) - Include inline action buttons

### setup-palette-stack.sh

Initial project setup:

```bash
./scripts/setup-palette-stack.sh \
  --project-root . \
  --with-examples
```

**What it does:**
1. Detects package manager
2. Validates Node/TypeScript versions
3. Installs dependencies with version compatibility check
4. Creates provider components
5. Initializes command registry
6. Configures Tailwind for palettes
7. Optionally copies working examples

### add-palette-feature.sh

Add features to existing palettes:

```bash
./scripts/add-palette-feature.sh \
  --feature virtual-scroll|server-search|keyboard-shortcuts|recent-commands|favorites|multi-step \
  --target ./src/SearchPalette.tsx
```

**Features:**
- `virtual-scroll` - Tanstack Virtual for 10k+ items
- `server-search` - Tanstack Query integration with debouncing
- `keyboard-shortcuts` - ⌘+1-9 favorites and custom bindings
- `recent-commands` - Track and display recent usage
- `favorites` - Pin commands with persistence
- `multi-step` - Nested command flows with breadcrumbs

### Workflow Patterns

**Basic palette creation:**
```bash
setup-palette-stack.sh
create-command-palette.sh --type modal --name Actions
```

**Rich file search:**
```bash
create-palette-layout.sh --layout two-column --name FileSearch
create-result-type.sh --type file --name FileResult
add-palette-feature.sh --feature virtual-scroll --target FileSearch.tsx
```

**API-driven search:**
```bash
create-command-palette.sh --type modal --name ApiSearch
add-palette-feature.sh --feature server-search --target ApiSearch.tsx
```

## Additional Resources

### Reference Files

Comprehensive documentation in `references/`:

- **`design-principles.md`** - UX patterns, fuzzy search, discovery, accessibility from research
- **`layouts.md`** - Detailed implementation guides for all five layout patterns
- **`theming.md`** - CSS variables, Tailwind integration, custom themes, reduced motion
- **`keyboard-navigation.md`** - Arrow keys, shortcuts, focus traps, multi-key sequences
- **`state-management.md`** - Zustand patterns, command registry, Tanstack Query integration
- **`server-side-search.md`** - API integration, debouncing, pagination, infinite scroll
- **`virtual-scrolling.md`** - Tanstack Virtual setup, performance benchmarks, dynamic heights
- **`testing.md`** - Vitest + RTL unit tests, Playwright E2E, performance testing
- **`floating-positioning.md`** - Floating UI middleware for embedded palettes
- **`plugin-system.md`** - Extensibility patterns, third-party command providers
- **`analytics.md`** - Telemetry patterns (reference only, not in examples)

### Example Implementations

Working examples in `examples/`:

- **`file-search/`** - Virtual scroll, fuzzy search, file metadata, recent files
- **`action-palette/`** - Grouped actions, keyboard shortcuts, icons
- **`navigation/`** - Breadcrumbs, route groups, search history
- **`multi-step/`** - Nested commands, command chaining, back navigation (Raycast-style)
- **`server-search/`** - API integration, Tanstack Query, debounce, loading states
- **`virtual-list/`** - 10k+ items, Tanstack Virtual, performance optimizations

Each example includes a README explaining what it demonstrates and key implementation details.

### Utility Functions

Reusable TypeScript utilities in `utilities/`:

- **`fuzzy-search.ts`** - Fuzzy matching, scoring, highlight rendering
- **`keyboard-shortcuts.ts`** - Shortcut parsing, matching, hooks, display formatting
- **`command-registry.ts`** - Command registration API, searching, grouping, providers
- **`theme-utils.ts`** - Theme detection, switching, CSS variable generation

Copy these files into your project and customize as needed.

### Scripts Directory

All generator scripts with dependency validation:

- **`create-command-palette.sh`** - Main palette generator
- **`create-palette-layout.sh`** - Layout variants
- **`create-result-type.sh`** - Result components
- **`setup-palette-stack.sh`** - Initial project setup
- **`add-palette-feature.sh`** - Feature additions

Scripts validate dependencies before generation and provide remediation steps for missing or incompatible packages.

## Best Practices

**Performance:**
- Use virtual scrolling (Tanstack Virtual) for 1,000+ items
- Debounce server searches (300-500ms)
- Memoize result components to prevent re-renders
- Lazy load preview content

**Accessibility:**
- Maintain focus trap when palette is open
- Announce result count changes to screen readers
- Support keyboard-only navigation
- Respect `prefers-reduced-motion`

**User Experience:**
- Show recent/frequent commands on open
- Provide empty state guidance for new users
- Display keyboard shortcuts next to commands
- Support fuzzy search for typo tolerance

**Architecture:**
- Keep command registration decentralized (register in feature components)
- Use Zustand for UI state, Tanstack Query for server state
- Separate result rendering from business logic
- Design for plugin extensibility from the start

For detailed guidance on each best practice, consult the relevant reference documentation.

## Getting Help

**Common Issues:**

1. **Palette doesn't open** - Check keyboard shortcut conflicts, verify trigger is registered
2. **Search not filtering** - Ensure commands have `keywords` array, check fuzzy search configuration
3. **Results not rendering** - Verify result type components are imported, check TypeScript types
4. **Poor performance** - Enable virtual scrolling, check for unnecessary re-renders with React DevTools

**Deep Dives:**

- Layout not working as expected → `references/layouts.md`
- Theme not switching → `references/theming.md`
- Keyboard nav issues → `references/keyboard-navigation.md`
- Server search slow → `references/server-side-search.md`
- Testing failures → `references/testing.md`

**Extending:**

- Adding custom result types → `create-result-type.sh --type custom`
- Third-party integrations → `references/plugin-system.md`
- Performance optimization → `references/virtual-scrolling.md`
- Analytics/telemetry → `references/analytics.md`

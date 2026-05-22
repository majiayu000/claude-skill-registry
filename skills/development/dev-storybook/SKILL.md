---
name: dev-storybook
description: Comprehensive Storybook skill for Vue 3 - story creation, auditing, component discovery, visual testing, and CI integration. Merged from dev-storybook, storybook-audit, and storybook-master.
---

# dev-storybook

BUILD, AUDIT, and AUTOMATE Storybook stories for Vue 3 components with TypeScript. This comprehensive skill covers story creation, auditing existing stories for issues, component discovery and inventory, and CI/CD integration. Use when creating component documentation, fixing story compilation errors, auditing for display issues, or setting up automated testing workflows.

## Core Responsibilities

1. **Story Creation**: Write well-structured Storybook stories for Vue 3 components
2. **Error Resolution**: Fix TypeScript and Vue compilation errors in stories
3. **Styling Patterns**: Apply CSS correctly in Storybook without runtime template errors
4. **Component Props**: Ensure correct prop types and event handlers
5. **Story Auditing**: Detect and fix cutoff modals, store dependencies, design token violations
6. **Component Discovery**: Scan codebase for components and generate inventory reports
7. **Automated Testing**: Visual regression testing and accessibility compliance
8. **Story Streamlining**: Ensure stories match the actual app appearance exactly

---

## Story Streamlining (CRITICAL)

**Trigger Keywords**: "streamline", "streamlined", "match app", "looks different", "visual fidelity"

When user asks to **"streamline"** a Storybook story, they mean: **Make the story look EXACTLY like the component appears in the actual app.**

### What "Streamlined" Means in This Project

**CRITICAL**: In FlowState, "streamlined" specifically means using **glass morphism** instead of solid black backgrounds.

- ❌ **NOT streamlined**: Solid black/opaque backgrounds (`--glass-bg-solid`, `rgba(0,0,0,0.95)`)
- ✅ **Streamlined**: Semi-transparent backgrounds with blur so the purple gradient shows through

```css
/* Streamlined = Glass Morphism */
background: rgba(30, 32, 45, 0.75);
backdrop-filter: blur(24px) saturate(180%);
```

**The app's signature look is glass panels floating over a purple/indigo gradient. If a component looks like a flat black box, it's NOT streamlined.**

### Streamlining Checklist

When streamlining a story, verify ALL of the following:

| Check | Requirement | How to Fix |
|-------|-------------|------------|
| **1. Use Actual Components** | Story imports and renders the REAL Vue component, not a mockup | Import from `@/components/...` |
| **2. App Background** | Story background matches app's purple/indigo gradient | Use `background: var(--app-background-gradient)` |
| **3. Glass Morphism** | Modals/overlays use semi-transparent bg with blur, NOT solid black | Use `rgba(30, 32, 45, 0.75)` + `backdrop-filter: blur(24px)` |
| **4. Design Tokens** | All styling uses CSS variables, no hardcoded values | Replace `#hex` and `rgba()` with `var(--token)` |
| **5. Correct Props** | Story passes the same props the component expects | Check `defineProps` in component |
| **6. Event Handlers** | All emitted events have handlers | Add `@event="handler"` |
| **7. Mock Data** | Data looks realistic, matches production patterns | Use actual Task/Project types |

### Streamlining Workflow

```
1. IDENTIFY the component being streamlined
   └── Find the actual .vue component file
   └── Read its props, emits, and slots

2. COMPARE story vs app
   └── What does the story currently show?
   └── What does the actual app show?
   └── List the differences

3. FIX each difference:
   a. Background: Use var(--app-background-gradient)
   b. Components: Import actual components, not mockups
   c. Tokens: Replace hardcoded colors with CSS variables
   d. Props: Match component's defineProps interface
   e. Data: Use realistic mock data

4. VERIFY with user
   └── Ask user to check Storybook matches app
```

### Background Color Reference

**CRITICAL**: The app uses a purple/indigo gradient, NOT neutral gray.

```typescript
// ❌ WRONG - neutral gray (doesn't match app)
background: var(--surface-primary);
background: hsl(0, 0%, 12%);

// ✅ CORRECT - app's purple/indigo gradient
background: var(--app-background-gradient);
```

The `--app-background-gradient` is defined in `design-tokens.css`:
```css
--app-background-gradient: linear-gradient(135deg,
    hsl(220, 13%, 9%) 0%,
    hsl(240, 21%, 15%) 25%,
    hsl(250, 24%, 12%) 50%,
    hsl(260, 20%, 14%) 75%,
    hsl(220, 13%, 11%) 100%);
```

### Example: Before/After Streamlining

**Before (mockup, wrong background):**
```typescript
export const Default: Story = {
  render: () => ({
    template: `
      <div style="background: #1a1a1a; padding: 20px;">
        <!-- Hardcoded mockup HTML -->
        <div class="fake-card">
          <h2>Task Title</h2>
          <button>Action</button>
        </div>
      </div>
    `
  })
}
```

**After (streamlined, matches app):**
```typescript
import QuickSortCard from '@/components/QuickSortCard.vue'
import { useTaskStore } from '@/stores/tasks'

export const Default: Story = {
  render: () => ({
    components: { QuickSortCard },
    setup() {
      const mockTask = { id: '1', title: 'Real Task', priority: 'high', ... }
      return { mockTask }
    },
    template: `
      <div style="
        min-height: 100vh;
        background: var(--app-background-gradient);
        padding: var(--space-8);
      ">
        <QuickSortCard :task="mockTask" @update-task="..." />
      </div>
    `
  })
}
```

### Glass Morphism vs Solid Black (CRITICAL)

**Problem**: Components using `--glass-bg-solid` or opaque black backgrounds look wrong because they block the app's purple gradient from showing through.

**Solution**: Use semi-transparent backgrounds with blur so the gradient is visible through the glass effect.

```css
/* ❌ WRONG - Solid black, no glass effect */
background: var(--glass-bg-solid);           /* rgba(0, 0, 0, 0.95) */
background: rgba(0, 0, 0, 0.95);
background: #121214;

/* ✅ CORRECT - Semi-transparent with blur (glass morphism) */
background: rgba(30, 32, 45, 0.75);
backdrop-filter: blur(24px) saturate(180%);
-webkit-backdrop-filter: blur(24px) saturate(180%);
border: 1px solid var(--glass-border-medium);
```

**Glass Morphism Recipe**:
| Property | Value | Purpose |
|----------|-------|---------|
| `background` | `rgba(30, 32, 45, 0.75)` | Semi-transparent dark with slight purple tint |
| `backdrop-filter` | `blur(24px) saturate(180%)` | Blur + color boost for depth |
| `border` | `1px solid var(--glass-border-medium)` | Subtle edge definition |
| `box-shadow` | `inset 0 1px 0 rgba(255, 255, 255, 0.1)` | Top highlight for polish |

**When to use glass morphism**:
- Modals and overlays
- Command palettes
- Dropdown menus
- Floating panels
- Any component that appears over the app background

### Common Streamlining Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| **Mockup instead of component** | Story shows different UI than app | Import actual component |
| **Wrong background color** | Black/gray instead of purple gradient | Use `var(--app-background-gradient)` |
| **Solid black modal** | Modal looks flat, no depth | Use glass morphism with `rgba()` + `backdrop-filter` |
| **Hardcoded colors** | Colors don't match design system | Use CSS variables |
| **Missing components** | Card missing buttons/badges | Import child components |
| **Wrong spacing** | Elements too cramped/spread | Use `var(--space-X)` tokens |

## Critical Rules

### Vue 3 Template Restrictions

**NEVER use `<style>` or `<script>` tags inside runtime templates**:

```typescript
// ❌ WRONG - Causes Vue compilation error
template: `
  <div>
    <style>
      .my-class { color: red; }
    </style>
    <MyComponent />
  </div>
`

// ✅ CORRECT - Apply styles globally or use inline styles
template: `
  <div>
    <MyComponent />
  </div>
`
```

### Component Prop Verification

**ALWAYS verify component props before writing stories**:

```bash
# Check component interface
grep -A 5 "interface Props" src/components/MyComponent.vue
grep -A 5 "defineProps" src/components/MyComponent.vue
```

Example fix:
```typescript
// Component expects: { isOpen: boolean, taskIds: string[] }
// ❌ WRONG story args
args: {
  isVisible: true,  // Wrong prop name
  selectedTasks: [] // Wrong prop name
}

// ✅ CORRECT story args
args: {
  isOpen: true,
  taskIds: ['1', '2', '3']
}
```

### Import Requirements

**ALWAYS include required Vue imports**:

```typescript
import type { Meta, StoryObj } from '@storybook/vue3'
import { ref, reactive, computed } from 'vue' // Include all Vue APIs you use
import MyComponent from '@/components/MyComponent.vue'
```

Common missing imports:
- `ref` - For reactive state
- `reactive` - For reactive objects
- `computed` - For computed properties
- `watch` - For watchers
- `onMounted`, `onUnmounted` - For lifecycle hooks

## Story Structure Pattern

### Basic Story Template

```typescript
import type { Meta, StoryObj } from '@storybook/vue3'
import { ref } from 'vue'
import MyComponent from '@/components/MyComponent.vue'

const meta = {
  component: MyComponent,
  title: '📁 Category/MyComponent',
  tags: ['autodocs'],
  parameters: {
    layout: 'centered', // or 'fullscreen'
    docs: {
      description: {
        component: 'Component description here'
      }
    }
  }
} satisfies Meta<typeof MyComponent>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  args: {
    // Component props here
    isOpen: true,
    title: 'Example'
  },
  render: (args) => ({
    components: { MyComponent },
    setup() {
      const isOpen = ref(args.isOpen)

      const handleClose = () => {
        isOpen.value = false
      }

      return {
        isOpen,
        handleClose,
        args
      }
    },
    template: `
      <MyComponent
        v-bind="args"
        :is-open="isOpen"
        @close="handleClose"
      />
    `
  })
}
```

### Modal/Overlay Story Pattern

```typescript
export const ModalExample: Story = {
  parameters: {
    layout: 'fullscreen' // Modal needs full screen
  },
  args: {
    isOpen: true,
    title: 'Modal Title'
  },
  render: (args) => ({
    components: { MyModal },
    setup() {
      const isOpen = ref(args.isOpen)

      return {
        isOpen,
        args,
        handleClose: () => { isOpen.value = false },
        handleConfirm: () => { console.log('Confirmed') }
      }
    },
    template: `
      <div style="width: 100vw; height: 100vh; background: var(--surface-secondary);">
        <MyModal
          v-bind="args"
          :is-open="isOpen"
          @close="handleClose"
          @confirm="handleConfirm"
        />
      </div>
    `
  })
}
```

## Story Organization Standards

### CRITICAL: Consolidate, Don't Duplicate

**Problem**: Too many similar stories create confusion and make components harder to understand.

**Solution**: Use focused, well-documented stories with clear purpose.

### Recommended Story Structure (5-Story Pattern)

Every component story file should follow this organization:

#### 1. **Default Story** (Primary with interactive controls)
```typescript
export const Default: Story = {
  args: {
    variant: 'default',
    hoverable: false,
    // ... all props with defaults
  },
  render: (args) => ({
    components: { MyComponent },
    setup() {
      return { args }
    },
    template: `
      <MyComponent v-bind="args" style="width: 320px;">
        <div style="padding: var(--space-2);">
          <h3 style="margin: 0 0 var(--space-2) 0; font-size: 16px; font-weight: 600;">
            Default Component
          </h3>
          <p style="margin: 0; font-size: 14px; color: var(--text-secondary);">
            Usage guidance explaining when/where to use this component.
          </p>
        </div>
      </MyComponent>
    `
  })
}
```

**Purpose**: Interactive playground for testing all prop combinations via Controls panel.

#### 2. **Variants Story** (Consolidated comparison)
```typescript
export const Variants: Story = {
  parameters: {
    docs: {
      description: {
        story: `**Visual variants for different contexts:**

- **Variant A**: When to use this variant
- **Variant B**: When to use this variant
- **Variant C**: When to use this variant`
      }
    }
  },
  render: () => ({
    components: { MyComponent },
    template: `
      <div style="display: flex; gap: var(--space-6); flex-wrap: wrap;">
        <MyComponent variant="a" style="width: 280px;">
          <div style="padding: var(--space-4);">
            <h4>Variant A</h4>
            <p>Use when [specific context]</p>
          </div>
        </MyComponent>

        <MyComponent variant="b" style="width: 280px;">
          <div style="padding: var(--space-4);">
            <h4>Variant B</h4>
            <p>Use when [specific context]</p>
          </div>
        </MyComponent>
      </div>
    `
  })
}
```

**Purpose**: Show all visual variants **side by side** with usage guidance.

**Anti-pattern**: Don't create separate stories for each variant (VariantA, VariantB, VariantC). Consolidate!

#### 3. **Effects/States Story** (Realistic contexts)
```typescript
export const Effects: Story = {
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        story: `**Effects for interaction and visual hierarchy:**

- **Hoverable**: Use when components are clickable
- **Glass**: Use on colorful/gradient backgrounds
- **Elevated**: Use to emphasize important content`
      }
    }
  },
  render: () => ({
    components: { MyComponent },
    template: `
      <div style="padding: var(--space-8); display: flex; flex-direction: column; gap: var(--space-8);">
        <!-- Hoverable -->
        <div>
          <h3>Hoverable Component</h3>
          <p>Use when components are clickable. Hover to see the effect.</p>
          <MyComponent hoverable style="width: 320px; cursor: pointer;">
            Content here
          </MyComponent>
        </div>

        <!-- Glass Effect (SHOW IN REALISTIC CONTEXT) -->
        <div>
          <h3>Glass Effect</h3>
          <p>Use on colorful or gradient backgrounds.</p>
          <div style="padding: var(--space-8); background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: var(--radius-xl);">
            <MyComponent glass style="width: 320px;">
              Glass effect shown on actual gradient!
            </MyComponent>
          </div>
        </div>
      </div>
    `
  })
}
```

**Purpose**: Show effects/states in **realistic visual contexts** (e.g., glass on gradient, not plain background).

**Critical**: Always show effects where they actually make sense visually.

#### 4. **WithSlots/Structure Story** (Slot patterns)
```typescript
export const WithSlots: Story = {
  parameters: {
    docs: {
      description: {
        story: `**Component supports slots for structured content:**

- **Header**: For titles, actions, or badges
- **Footer**: For metadata, timestamps, or action buttons
- Use slots to create consistent, structured layouts`
      }
    }
  },
  render: () => ({
    components: { MyComponent },
    template: `
      <div style="display: flex; gap: var(--space-6); flex-wrap: wrap;">
        <!-- Header only -->
        <MyComponent style="width: 300px;">
          <template #header>
            <h3>Header Content</h3>
          </template>
          Main content
        </MyComponent>

        <!-- Footer only -->
        <MyComponent style="width: 300px;">
          Main content
          <template #footer>
            Footer actions
          </template>
        </MyComponent>

        <!-- Both -->
        <MyComponent style="width: 300px;">
          <template #header>Header</template>
          Main content
          <template #footer>Footer</template>
        </MyComponent>
      </div>
    `
  })
}
```

**Purpose**: Show slot usage patterns side by side.

#### 5. **Real-World Example** (Production-ready)
```typescript
export const TaskCardExample: Story = {
  parameters: {
    docs: {
      description: {
        story: 'A realistic example showing how to combine variants, effects, and slots for production use.'
      }
    }
  },
  render: () => ({
    components: { MyComponent },
    template: `
      <MyComponent hoverable elevated style="width: 380px;">
        <template #header>
          <!-- Complex header with badges, title, etc. -->
        </template>

        <div style="display: flex; flex-direction: column; gap: var(--space-4);">
          <!-- Rich content with metadata, progress, etc. -->
        </div>

        <template #footer>
          <!-- Actions and metadata -->
        </template>
      </MyComponent>
    `
  })
}
```

**Purpose**: Show production-ready example combining multiple features.

### Usage Guidance Requirements

**EVERY story must include usage guidance**. Never show a variant without explaining when to use it.

#### Component-Level Documentation
```typescript
const meta = {
  component: MyComponent,
  title: '🧩 Components/🔘 Base/MyComponent',
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: `Component description explaining its purpose.

**When to use:**
- Specific use case 1
- Specific use case 2
- Specific use case 3`
      }
    }
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'outlined', 'filled'],
      description: 'Visual style variant',
      table: {
        type: { summary: 'string' },
        defaultValue: { summary: 'default' }
      }
    }
  }
}
```

#### Story-Level Documentation
```typescript
export const Variants: Story = {
  parameters: {
    docs: {
      description: {
        story: `**Visual variants for different contexts:**

- **Default**: Standard style (use for X)
- **Outlined**: Transparent background (use for Y)
- **Filled**: Solid background (use for Z)`
      }
    }
  }
}
```

### Visual Context Best Practices

#### ✅ GOOD: Show effects in realistic contexts
```typescript
// Glass effect on gradient
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: var(--space-8);">
  <MyComponent glass>
    Now the glass effect actually makes sense!
  </MyComponent>
</div>

// Elevated card on page
<div style="padding: var(--space-8); background: var(--surface-primary);">
  <MyComponent elevated>
    Extra shadow creates depth on the page
  </MyComponent>
</div>
```

#### ❌ BAD: Show effects on plain backgrounds
```typescript
// Glass effect on plain background (can't see blur!)
<MyComponent glass>
  Glass effect is invisible here
</MyComponent>

// Elevated without context (shadow purpose unclear)
<MyComponent elevated>
  Why is this elevated?
</MyComponent>
```

### ArgTypes Standards

Always include comprehensive argTypes with descriptions:

```typescript
argTypes: {
  variant: {
    control: 'select',
    options: ['default', 'outlined', 'filled'],
    description: 'Visual style variant',
    table: {
      type: { summary: 'string' },
      defaultValue: { summary: 'default' }
    }
  },
  hoverable: {
    control: 'boolean',
    description: 'Add hover effects (elevation & transform)',
    table: {
      type: { summary: 'boolean' },
      defaultValue: { summary: 'false' }
    }
  }
}
```

### Story Consolidation Checklist

Before creating multiple similar stories, ask:

- [ ] Can these variants be shown side by side in one story?
- [ ] Does each story explain WHEN to use it?
- [ ] Are effects shown in realistic visual contexts?
- [ ] Is the Default story using args for interactivity?
- [ ] Does the documentation include "When to use" guidance?

**Target**: 5-7 focused stories per component, NOT 12+ redundant stories.

## CSS Styling Patterns

### Option 1: Inline Styles (Preferred for simple cases)

```typescript
template: `
  <div style="padding: 20px; background: var(--surface-primary);">
    <MyComponent />
  </div>
`
```

### Option 2: CSS Variables (Use design tokens)

```typescript
template: `
  <div style="
    padding: var(--space-4);
    background: var(--surface-primary);
    border-radius: var(--radius-lg);
  ">
    <MyComponent />
  </div>
`
```

### Option 3: Global Styling (For component-wide changes)

Modify the component's scoped styles directly in the `.vue` file instead of trying to override in stories.

## Common Errors and Fixes

### Error: "Tags with side effect (<script> and <style>) are ignored"

**Cause**: Attempting to use `<style>` or `<script>` tags in runtime template

**Fix**: Remove the tags and use inline styles or global component styles

```typescript
// Before (causes error)
template: `<div><style>.foo{}</style><Component /></div>`

// After (works)
template: `<div style="..."><Component /></div>`
```

### Error: "Cannot find module '@/components/...'"

**Cause**: TypeScript path resolution in story files

**Fix**: This is usually a TypeScript check error only. Storybook will still work because Vite handles the paths. You can ignore or configure `tsconfig.json` to include story files.

### Error: "Cannot find name 'ref'"

**Cause**: Missing Vue import

**Fix**: Add `import { ref } from 'vue'`

### Error: "Missing required prop: 'propName'"

**Cause**: Component expects different props than story provides

**Fix**:
1. Check component props: `grep -A 5 "defineProps" src/components/MyComponent.vue`
2. Update story args to match
3. Ensure event handlers match emitted events

## Storybook Configuration

### Running Storybook

```bash
npm run storybook        # Start on port 6006
npm run build-storybook  # Build static site
```

### Story File Patterns

Stories are auto-discovered from:
- `src/**/*.stories.ts`
- `src/**/*.stories.tsx`

### Decorators Pattern

```typescript
decorators: [
  () => ({
    template: '<div style="width: 100%; height: 100vh;"><story /></div>'
  })
]
```

## Mock Data Patterns

### Creating Mock Store

```typescript
const createMockStore = (overrides = {}) => ({
  state: {
    items: [],
    ...overrides
  },
  getItem: (id: string) => mockData.find(item => item.id === id),
  updateItem: (id: string, data: any) => {
    console.log('Updated:', id, data)
  }
})

export const WithMockStore: Story = {
  render: () => ({
    setup() {
      const store = createMockStore({ items: mockItems })
      return { store }
    }
  })
}
```

## Design System Colors Fix

**CRITICAL**: Ensure design tokens use neutral grays (no blue tint)

Blue-tinted grays (WRONG):
```css
--gray-950: 218, 33%, 12%;   /* Hue 218 = Blue! */
--gray-900: 217, 33%, 17%;   /* High saturation = Color tint! */
```

Neutral grays (CORRECT):
```css
--gray-950: 0, 0%, 12%;   /* Hue 0, Saturation 0% = Neutral */
--gray-900: 0, 0%, 17%;   /* No color tint */
```

Check for blue tint:
```bash
grep "gray-9" src/assets/design-tokens.css
```

## Testing Stories

1. **Visual Check**: Open http://localhost:6006 and verify rendering
2. **Interaction**: Test interactive elements (buttons, inputs, modals)
3. **Responsive**: Check different viewport sizes
4. **Error Console**: Look for Vue warnings or errors

## Best Practices

1. **One Component Per Story File**: Each component gets its own `.stories.ts`
2. **Multiple Variants**: Create stories for different states (Default, Loading, Error, etc.)
3. **Descriptive Names**: Use clear story names like `Default`, `WithData`, `ErrorState`
4. **Documentation**: Add descriptions using `parameters.docs.description`
5. **Args Controls**: Use `argTypes` to make props interactive
6. **Real Data**: Use realistic mock data that represents actual use cases

## Common Story Variants

```typescript
export const Default: Story = { /* Basic usage */ }
export const Loading: Story = { /* Loading state */ }
export const Error: Story = { /* Error state */ }
export const WithData: Story = { /* Populated with data */ }
export const Empty: Story = { /* Empty state */ }
export const Interactive: Story = { /* Full interaction demo */ }
```

## Resources

- Storybook Docs: https://storybook.js.org/docs/vue/get-started/introduction
- Vue 3 + Storybook: https://storybook.js.org/docs/vue/writing-stories/introduction
- Component Story Format (CSF): https://storybook.js.org/docs/api/csf

---

# PART 2: Story Auditing (Merged from storybook-audit)

This section provides systematic auditing capabilities for detecting and fixing common Storybook issues.

## Trigger Keywords

Activate auditing capabilities when user mentions:
- "audit storybook", "fix storybook stories", "storybook cut off"
- "storybook store error", "storybook database error"
- "storybook modal cutoff", "storybook rendering issues"
- "Cannot find name 'ref'", "missing imports", "Vue import error"
- "missing event handlers", "modal won't close", "buttons don't work"

## User Clarification Protocol

**CRITICAL**: Before attempting fixes, ask clarifying questions to understand the exact issue.

### Questions to Ask

When user reports a Storybook issue, ask:

1. **Issue Type Clarification**:
   - "Is this happening on the Docs page or the Canvas/Story page?"
   - "Is the component being cut off, showing an error, or not rendering at all?"

2. **Component Context**:
   - "What type of component is this? (Modal, Context Menu, Dropdown, Form, etc.)"
   - "Does this component use any Pinia stores?"
   - "Does the component have dynamic height (expandable sections, submenus)?"

3. **Error Details**:
   - "Are there any errors in the browser console?"
   - "Can you share the exact error message?"

### Decision Tree

```
User reports Storybook issue
    ├── "cut off" / "clipped" / "can't see"
    │   └── Ask: "Docs page or Canvas?" + "Component type?"
    │   └── Likely: iframe height issue → Check 1
    │
    ├── "error" / "won't render" / "database"
    │   └── Ask: "Console error message?"
    │   └── Likely: Store dependency → Check 2
    │
    ├── "doesn't match" / "wrong props"
    │   └── Ask: "Which props are incorrect?"
    │   └── Likely: Props mismatch → Check 4
    │
    ├── "Cannot find name 'ref'" / "Cannot find name 'computed'"
    │   └── Ask: "Which Vue APIs are you using in setup()?"
    │   └── Likely: Missing imports → Check 7
    │
    ├── "buttons don't work" / "can't close modal"
    │   └── Ask: "What happens when you click [button]?"
    │   └── Likely: Missing event handlers → Check 8
    │
    └── Unknown
        └── Run full audit, then ask about findings
```

## Audit Checks

### Check 1: Iframe Height

**Issue**: Docs pages cut off modals, popups, or dropdowns

**Detection**:
```bash
# Find stories with potentially low iframe heights
grep -rn "iframeHeight" src/stories/ | grep -E "iframeHeight: [0-5][0-9]{2},"

# Find stories without explicit height
grep -L "iframeHeight" src/stories/**/*.stories.ts
```

**Component Type Guidelines**:
| Component Type | Minimum Height | Notes |
|----------------|----------------|-------|
| Simple components | 400px | Buttons, inputs, badges |
| Context menus | 600px | May have submenus |
| Dropdowns | 500px | Check max items |
| Modals (small) | 700px | Confirmation dialogs |
| Modals (large) | 900px | Forms, settings |
| Full-page overlays | 100vh | Use fullscreen layout |
| Components with submenus | 900px+ | Cascading menus need more |

**Fix Pattern A: Iframe Height (Standard)**:
```typescript
parameters: {
  layout: 'fullscreen',
  docs: {
    story: {
      inline: false,
      iframeHeight: 900,  // Adjust based on component type
    }
  }
},
```

**Fix Pattern B: Inline Relative Container (Robust for Storybook 8/10)**:
```typescript
parameters: {
  layout: 'fullscreen',
  docs: {
    story: { inline: true }
  }
},
decorators: [
  () => ({
    template: `
      <div class="story-container" style="
        background: var(--glass-bg-solid);
        height: 850px;
        width: 100%;
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 8px;
      ">
        <story />
      </div>
    `
  })
]
```

### Check 2: Store Dependencies (Pinia)

**Issue**: Stories import real Pinia stores which initialize PouchDB → causes database errors

**Detection**:
```bash
# Find stories importing stores
grep -rn "from '@/stores" src/stories/
grep -rn "useTaskStore\|useTimerStore\|useCanvasStore\|useUIStore" src/stories/
```

**Fix Options (in order of preference)**:

**Option A - Props Only** (best for presentational components):
```typescript
// Pass data via props, no store needed
const mockTask: Task = {
  id: '1',
  title: 'Test Task',
  status: 'planned',
  priority: 'high',
}

export const Default: Story = {
  args: {
    task: mockTask,
    onEdit: () => console.log('edit'),
    onDelete: () => console.log('delete'),
  }
}
```

**Option B - Fresh Pinia Decorator** (for components requiring store):
```typescript
// Create decorator: src/stories/decorators/freshPiniaDecorator.ts
import { createPinia, setActivePinia } from 'pinia'

export const freshPiniaDecorator = (story: any) => {
  setActivePinia(createPinia())
  return story()
}
```

### Check 3: Template Validation

**Issue**: Runtime templates contain `<style>` or `<script>` tags causing Vue errors

**Detection**:
```bash
grep -rn "template:.*<style>" src/stories/
grep -rn "template:.*<script>" src/stories/
```

### Check 4: Props Mismatch

**Issue**: Story args don't match component prop definitions

**Detection**:
```bash
# Get component props
grep -A 30 "defineProps" src/components/[ComponentName].vue

# Get story args
grep -A 15 "args:" src/stories/[ComponentName].stories.ts
```

**Common Mismatches**:
| Story Arg | Actual Prop | Fix |
|-----------|-------------|-----|
| `isVisible` | `isOpen` | Use `isOpen` |
| `selectedTasks` | `taskIds` | Use `taskIds` |
| `onClose` | `@close` emit | Add handler |

### Check 5: Layout Parameter

**Issue**: Modals/overlays using `layout: 'centered'` causing cutoff

**Detection**:
```bash
grep -l "Modal\|Overlay\|Dialog\|Popup\|Drawer" src/stories/**/*.ts | \
  xargs grep -L "layout: 'fullscreen'"
```

### Check 6: Design Token Enforcement

**Issue**: Stories or decorators use hardcoded colors instead of CSS design tokens

**Detection**:
```bash
# Find hardcoded hex colors in stories
grep -rn "#[0-9a-fA-F]\{3,8\}" src/stories/ --include="*.ts" --include="*.vue"

# Find hardcoded rgba values
grep -rn "rgba\s*(" src/stories/ --include="*.ts" --include="*.vue"
```

**Token Categories to Use**:
| Purpose | CSS Variable |
|---------|-------------|
| Priority High | `var(--color-priority-high)` |
| Priority Medium | `var(--color-priority-medium)` |
| Priority Low | `var(--color-priority-low)` |
| Glass background | `var(--glass-bg)`, `var(--glass-bg-solid)` |
| Glass border | `var(--glass-border)` |
| Modal/Dropdown bg | `var(--modal-bg)`, `var(--dropdown-bg)` |
| Text primary | `var(--text-primary)` |
| Surface colors | `var(--surface-primary)`, `var(--surface-secondary)` |

### Check 7: Missing Vue Imports

**Issue**: Stories use Vue APIs without importing them

**Fix Pattern**:
```typescript
// Add all used Vue APIs
import { ref, computed, watch, onMounted } from 'vue'
```

### Check 8: Event Handlers

**Issue**: Stories don't provide handlers for critical events

**Critical Events Checklist**:

For **Modal/Overlay** components:
- [ ] `@close` - User closes modal
- [ ] `@confirm` - User confirms action
- [ ] `@cancel` - User cancels action

For **Form** components:
- [ ] `@submit` - User submits form
- [ ] `@cancel` - User cancels form

## Full Audit Workflow

Run this bash script for a complete audit:

```bash
echo "=== STORYBOOK AUDIT REPORT ==="
echo ""
echo "=== 1. Store Dependencies ==="
grep -rn "from '@/stores" src/stories/ 2>/dev/null | head -20 || echo "None found"
echo ""
echo "=== 2. Low Iframe Heights (<600px) ==="
grep -rn "iframeHeight: [0-5][0-9]{2}," src/stories/ 2>/dev/null || echo "None found"
echo ""
echo "=== 3. Template Style/Script Tags ==="
grep -rn "template:" src/stories/ 2>/dev/null | grep -E "<style|<script" || echo "None found"
echo ""
echo "=== 4. Modals Without Fullscreen ==="
for f in $(find src/stories -name "*.stories.ts" 2>/dev/null); do
  if grep -q "Modal\|Overlay\|Dialog" "$f" && ! grep -q "fullscreen" "$f"; then
    echo "$f: NEEDS FULLSCREEN"
  fi
done
echo ""
echo "=== 5. Hardcoded Colors (Token Violations) ==="
grep -rn "#[0-9a-fA-F]\{3,8\}" src/stories/ --include="*.ts" 2>/dev/null | head -15 || echo "None found"
echo ""
echo "=== Audit Complete ==="
```

## Component-Specific Guidelines

### TaskContextMenu
- Minimum height: 900px (has cascading submenus)
- Needs mock task data, not store
- All event handlers should be noops or console.log
- Layout: fullscreen required

### ContextMenu
- Minimum height: 600px
- Position must be calculated in render function
- Use `onMounted` for centering

### Modal Components (General)
- Always use `layout: 'fullscreen'`
- Wrap in full-height container div
- Provide toggle mechanism for interactive demos
- Test both open and closed states

### Auth Components
- Background: `var(--glass-bg-solid)`
- Border: None (clean glass look)
- Layout: `inline: true` with fixed height (600px-800px)

---

# PART 3: Component Discovery & Automation (Merged from storybook-master)

This section provides automated component discovery, story generation, and CI integration.

## 4-Phase Workflow

### Phase 1: Component Discovery & Inventory

**Smart Source Scanning**:
- Multi-framework detection (React, Vue, Svelte, Web Components)
- Pattern-based classification using folder structures
- Metadata extraction from prop types and interfaces

**Usage**:
```bash
python3 scripts/phase1_discovery.py
```

**Output Files**:
- `storybook-inventory.csv`: Complete component inventory
- `missing-stories-report.md`: Undocumented components report
- `component-update-map.json`: Component-to-story mapping

### Phase 2: Autodocs & Story Automation

**Story Generation**:
- CSF3 story format generation
- Prop-driven controls auto-generation
- Documentation blocks creation

**Usage**:
```bash
python3 scripts/phase2_generation.py --auto-fix
```

### Phase 3: Automated Visual & Interaction Testing

**Visual Test Harness**:
- Snapshot testing for visual regression
- Cross-browser testing
- Accessibility compliance (axe-core, WCAG 2.1 AA)

### Phase 4: CI/CD Integration

**CI Enforcement**:
- Build validation and coverage enforcement
- Quality gates for merging
- Automated PR comments

## Configuration

Create `.storybook/skill-config.yml`:

```yaml
discovery:
  component_paths:
    - "src/components/**/*"
  story_paths:
    - "src/**/*.stories.*"
  ignore_patterns:
    - "*.test.*"
    - "node_modules/**"

generation:
  autodocs: true
  controls: true
  accessibility_testing: true

testing:
  visual_testing:
    enabled: true
    tool: "chromatic"
  accessibility:
    enabled: true
    standards: ["WCAG2.1AA"]

ci:
  enforce_coverage: true
  fail_on_missing_stories: true
```

## Scripts Available

Located in `scripts/` directory:
- `run_storybook_master.py` - Main orchestrator for all phases
- `phase1_discovery.py` - Component discovery
- `phase2_generation.py` - Story generation

## Self-Learning Protocol

**This skill learns from successful fixes.** When a solution works:

1. **Document the solution** by asking user:
   - "This fix worked. Should I add it to the skill's knowledge base?"
   - "What was the root cause?"

2. **Update the skill** with user approval:
   - Add new component-specific guidelines
   - Add new error patterns and fixes
   - Update height recommendations

---

## Example Files

Before/after examples are available in `examples/` directory:
- `before-after-modal-iframe.md` - Iframe height fix for modals
- `before-after-contextmenu-height.md` - Height fix for cascading menus
- `before-after-store-dependency.md` - Store dependency fix
- `before-after-template-style.md` - Template style tag fix
- `before-after-props-mismatch.md` - Props matching component definitions
- `before-after-missing-imports.md` - Missing Vue imports fix
- `before-after-event-handlers.md` - Missing event handlers fix

## References

Best practices reference available in `references/storybook-best-practices.md`.

---

**When to use this skill**: Creating or fixing Storybook stories, resolving story compilation errors, documenting Vue 3 components, setting up component showcases, auditing stories for issues, automating component discovery.

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

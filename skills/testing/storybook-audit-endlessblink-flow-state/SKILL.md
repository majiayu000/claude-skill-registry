---
name: storybook-audit
description: This skill should be used when auditing Storybook stories for display issues (cutoff modals, popups), store dependency errors (PouchDB/database conflicts), template validation problems, and rendering issues. Automatically scans story files, detects issues, asks clarifying questions, and updates itself when solutions are approved by the user.
---

# storybook-audit

AUDIT Storybook stories for common issues like cutoff modals, store dependency errors, and template problems. Automatically scan story files, detect issues, ask user questions when needed, and update this skill when solutions are approved.

## Core Responsibilities

1. **Display Auditing**: Detect stories with insufficient iframe height causing cutoff
2. **Store Detection**: Find stories importing real Pinia stores (causes DB init in Storybook)
3. **Template Validation**: Check for invalid `<style>`/`<script>` tags in runtime templates
4. **Props Verification**: Ensure story args match component prop definitions
5. **Layout Validation**: Check modals/overlays use `layout: 'fullscreen'`
6. **Design Token Enforcement**: Detect hardcoded colors/styles that should use CSS variables
7. **Import Verification**: Detect missing Vue imports (`ref`, `reactive`, `computed`, etc.)
8. **Event Handler Verification**: Detect missing critical event handlers (`@close`, `@submit`, `@confirm`, `@cancel`)
9. **Self-Learning**: Update this skill when new issues/solutions are discovered and approved

## Trigger Keywords

Activate this skill when user mentions:
- "audit storybook"
- "fix storybook stories"
- "storybook cut off"
- "storybook store error"
- "storybook database error"
- "storybook modal cutoff"
- "storybook rendering issues"
- "create story" / "create stories"
- "storybook tokens" / "hardcoded colors"
- "tokenize storybook"
- "Cannot find name 'ref'" / "Cannot find name 'computed'"
- "missing imports" / "Vue import error"
- "missing event handlers" / "modal won't close"
- "buttons don't work" / "handlers missing"

---

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

4. **Environment**:
   - "What port is Storybook running on? (default: 6006)"
   - "Did this work before? What changed?"

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

---

## Self-Learning Protocol

**This skill learns from successful fixes.** When a solution works:

### After Successful Fix

1. **Document the solution** by asking user:
   - "This fix worked. Should I add it to the skill's knowledge base?"
   - "What was the root cause?"
   - "Any edge cases to note?"

2. **Update the skill** with user approval:
   - Add new component-specific guidelines
   - Add new error patterns and fixes
   - Update height recommendations
   - Add new detection commands

### Skill Update Format

When adding new knowledge, append to the appropriate section:

```markdown
### [ComponentName] (Added: YYYY-MM-DD)
- Minimum height: XXXpx
- Special requirements: [notes]
- Common issues: [list]
- Solution: [what worked]
- User notes: [any context from user]
```

### Update Triggers

Update this skill when:
- A new component type is successfully fixed
- A new error pattern is identified
- An existing solution doesn't work (document the exception)
- User provides additional context about their setup

---

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
Use this when `iframeHeight` is ignored or global CSS (`preview-head.html`) overrides it.
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
        background: var(--glass-bg-solid); /* Dark glass overlay */
        height: 850px; /* Adjust based on component needs */
        width: 100%;
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 8px;
        /* No border for auth/overlay components to match BaseDropdown style */
      ">
        <style>
           .story-container .modal-overlay,
           .story-container .auth-container {
             position: absolute !important;
             width: 100% !important;
             height: 100% !important;
             z-index: 10 !important;
           }
        </style>
        <story />
      </div>
    `
  })
]
```

**Dynamic Height Script** (for preview.ts):
```typescript
// Auto-resize iframes based on content
// Add to .storybook/preview.ts
if (typeof window !== 'undefined') {
  const observer = new MutationObserver(() => {
    document.querySelectorAll('iframe').forEach(iframe => {
      try {
        const body = iframe.contentWindow?.document?.body;
        const parent = iframe.parentElement;
        if (body && parent && parent.style.height === '400px') {
          parent.style.height = body.scrollHeight + 'px';
        }
      } catch (e) { /* cross-origin */ }
    });
  });
  observer.observe(document.body, { childList: true, subtree: true });
}
```

### Check 2: Store Dependencies (Pinia)

**Issue**: Stories import real Pinia stores which initialize PouchDB → causes database errors

**Detection**:
```bash
# Find stories importing stores
grep -rn "from '@/stores" src/stories/
grep -rn "useTaskStore\|useTimerStore\|useCanvasStore\|useUIStore" src/stories/
```

**Problematic Pattern**:
```typescript
// ❌ BAD - imports real store, triggers PouchDB init
import { useTaskStore } from '@/stores/tasks'

export const Default: Story = {
  render: () => ({
    setup() {
      const taskStore = useTaskStore()  // Database error!
      return { taskStore }
    }
  })
}
```

**Fix Options (in order of preference)**:

**Option A - Props Only** (best for presentational components):
```typescript
// ✅ Pass data via props, no store needed
const mockTask: Task = {
  id: '1',
  title: 'Test Task',
  status: 'planned',
  priority: 'high',
  // ... full task object matching Task interface
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

// Use in story:
import { freshPiniaDecorator } from '../decorators/freshPiniaDecorator'

export default {
  decorators: [freshPiniaDecorator],
  // ...
}
```

**Option C - Testing Pinia** (for mocking specific state):
```typescript
import { createTestingPinia } from '@pinia/testing'

export const WithMockedState: Story = {
  decorators: [
    () => ({
      setup() {
        // Creates a testing pinia with initial state
        createTestingPinia({
          initialState: {
            tasks: {
              tasks: [{ id: '1', title: 'Mock Task' }]
            }
          }
        })
      },
      template: '<story />'
    })
  ]
}
```

**Option D - Environment Detection** (global fix in preview.ts):
```typescript
// .storybook/preview.ts
import { type Preview, setup } from '@storybook/vue3'
import { createPinia } from 'pinia'

const pinia = createPinia()

setup((app) => {
  app.use(pinia)

  // Flag for stores to skip DB initialization
  if (typeof window !== 'undefined') {
    (window as any).__STORYBOOK__ = true
  }
})
```

Then in stores:
```typescript
// In store initialization
if (typeof window !== 'undefined' && (window as any).__STORYBOOK__) {
  // Skip PouchDB initialization
  return
}
```

### Check 3: Template Validation

**Issue**: Runtime templates contain `<style>` or `<script>` tags causing Vue errors

**Detection**:
```bash
grep -rn "template:.*<style>" src/stories/
grep -rn "template:.*<script>" src/stories/
grep -rn "template:" src/stories/ | grep -E "<style|<script"
```

**Fix**:
```typescript
// ❌ BAD - causes Vue compilation error
template: `
  <div>
    <style>.my-class { color: red; }</style>
    <Component />
  </div>
`

// ✅ GOOD - use inline styles
template: `
  <div style="color: red;">
    <Component />
  </div>
`

// ✅ GOOD - use CSS variables
template: `
  <div style="color: var(--text-primary);">
    <Component />
  </div>
`
```

### Check 4: Props Mismatch

**Issue**: Story args don't match component prop definitions

**Detection**:
```bash
# For each story file, compare args with component props
# Step 1: Get component props
grep -A 30 "defineProps" src/components/[ComponentName].vue

# Step 2: Get story args
grep -A 15 "args:" src/stories/[ComponentName].stories.ts
```

**Common Mismatches**:
| Story Arg | Actual Prop | Fix |
|-----------|-------------|-----|
| `isVisible` | `isOpen` | Use `isOpen` |
| `selectedTasks` | `taskIds` | Use `taskIds` |
| `onClose` | `@close` emit | Add handler |
| `onChange` | `@update:modelValue` | Use correct event name |

**Verification Command**:
```bash
# Extract all props from a component
grep -oP "(?<=defineProps<\{)[^}]+" src/components/MyComponent.vue | tr ',' '\n'
```

### Check 5: Layout Parameter

**Issue**: Modals/overlays using `layout: 'centered'` causing cutoff

**Detection**:
```bash
# Find modals/overlays without fullscreen layout
grep -l "Modal\|Overlay\|Dialog\|Popup\|Drawer" src/stories/**/*.ts | \
  xargs grep -L "layout: 'fullscreen'"
```

**Fix**:
```typescript
// ❌ BAD for modals
parameters: {
  layout: 'centered',  // Modal will be clipped
}

// ✅ GOOD for modals
parameters: {
  layout: 'fullscreen',
  docs: {
    story: {
      inline: false,
      iframeHeight: 900,
    }
  }
}
```

### Check 6: Design Token Enforcement

**Issue**: Stories or decorators use hardcoded colors instead of CSS design tokens

**CRITICAL**: When creating stories, ALL colors must use CSS variables. No hardcoded hex, rgb, or rgba values.

**Detection**:
```bash
# Find hardcoded hex colors in stories
grep -rn "#[0-9a-fA-F]\{3,8\}" src/stories/ --include="*.ts" --include="*.vue"

# Find hardcoded rgba values
grep -rn "rgba\s*(" src/stories/ --include="*.ts" --include="*.vue"

# Find hardcoded rgb values
grep -rn "rgb\s*(" src/stories/ --include="*.ts" --include="*.vue"

# Find inline styles with color/background
grep -rn "style=\"[^\"]*\(color\|background\|border\)" src/stories/
```

**Forbidden Patterns** (from token_definitions.json):
| Pattern | Issue | Fix With |
|---------|-------|----------|
| `#ef4444` | Hardcoded high priority red | `var(--color-priority-high)` |
| `#f59e0b` | Hardcoded medium priority orange | `var(--color-priority-medium)` |
| `#3b82f6` | Hardcoded low priority blue | `var(--color-priority-low)` |
| `#feca57`, `#fbbf24` | Wrong yellow variants | `var(--color-priority-medium)` |
| `rgba(255, 255, 255, 0.1)` | Hardcoded glass border | `var(--glass-border)` |
| `rgba(0, 0, 0, 0.95)` | Hardcoded solid bg | `var(--glass-bg-solid)` |
| `rgba(20, 20, 20, 0.95)` | Hardcoded modal bg | `var(--modal-bg)` |

**Token Categories to Use**:

| Purpose | CSS Variable |
|---------|-------------|
| Priority High | `var(--color-priority-high)` |
| Priority Medium | `var(--color-priority-medium)` |
| Priority Low | `var(--color-priority-low)` |
| Work/Active | `var(--color-work)` |
| Glass background | `var(--glass-bg)`, `var(--glass-bg-solid)`, `var(--glass-bg-medium)` |
| Glass border | `var(--glass-border)`, `var(--glass-border-hover)` |
| Modal/Dropdown bg | `var(--modal-bg)`, `var(--dropdown-bg)` |
| Text primary | `var(--text-primary)` |
| Text secondary | `var(--text-secondary)` |
| Surface colors | `var(--surface-primary)`, `var(--surface-secondary)` |

**Fix Patterns**:

```typescript
// ❌ BAD - hardcoded colors
const wrapperStyle = {
  background: '#1a1a2e',
  border: '1px solid rgba(255, 255, 255, 0.1)',
  color: '#ffffff',
}

// ✅ GOOD - using CSS variables
const wrapperStyle = {
  background: 'var(--glass-bg-solid)',
  border: '1px solid var(--glass-border)',
  color: 'var(--text-primary)',
}

// ❌ BAD - inline hardcoded in template
template: `<div style="background: #000; color: #fff;">...</div>`

// ✅ GOOD - CSS variables in template
template: `<div style="background: var(--surface-primary); color: var(--text-primary);">...</div>`

// ❌ BAD - hardcoded priority color in mock data render
template: `<span style="color: #ef4444;">High Priority</span>`

// ✅ GOOD - tokenized priority color
template: `<span style="color: var(--color-priority-high);">High Priority</span>`
```

**Story Decorator Template** (use this for all new stories):
```typescript
// Standard dark background decorator with tokens
const darkBgDecorator = () => ({
  template: `
    <div style="
      background: var(--surface-primary);
      min-height: 400px;
      padding: 2rem;
      display: flex;
      align-items: center;
      justify-content: center;
    ">
      <story />
    </div>
  `,
})
```

**Token Reference Location**: `.claude/skills/🎨 css-design-token-enforcer/assets/token_definitions.json`

---

### Check 7: Missing Vue Imports

**Issue**: Stories use Vue APIs (`ref`, `reactive`, `computed`, `watch`, `onMounted`) without importing them from Vue

**Detection**:
```bash
# Find stories using Vue APIs without importing them
# Step 1: List all story files using Vue APIs
grep -rn "\bref\b\|\breactive\b\|\bcomputed\b\|\bwatch\b\|\bonMounted\b\|\bonUnmounted\b\|\bnextTick\b" src/stories/ --include="*.ts" -l | \
# Step 2: Remove files that already import from 'vue'
while read file; do
  if ! grep -q "from 'vue'" "$file"; then
    echo "$file"
  fi
done
```

**Problematic Pattern**:
```typescript
// ❌ BAD - Using Vue APIs without imports
import type { Meta, StoryObj } from '@storybook/vue3'
import MyComponent from '@/components/MyComponent.vue'

export const Interactive: Story = {
  render: () => ({
    components: { MyComponent },
    setup() {
      const counter = ref(0)  // TypeScript error: Cannot find name 'ref'
      const doubleCounter = computed(() => counter.value * 2)  // Error: Cannot find name 'computed'
      return { counter, doubleCounter }
    },
    template: `<MyComponent :count="counter" />`
  })
}
```

**Fix Pattern: Add Missing Imports**:
```typescript
// ✅ GOOD - Import all used Vue APIs
import type { Meta, StoryObj } from '@storybook/vue3'
import { ref, computed } from 'vue'  // ✅ Add imports
import MyComponent from '@/components/MyComponent.vue'

export const Interactive: Story = {
  render: () => ({
    components: { MyComponent },
    setup() {
      const counter = ref(0)
      const doubleCounter = computed(() => counter.value * 2)
      return { counter, doubleCounter }
    },
    template: `<MyComponent :count="counter" />`
  })
}
```

**Common Vue APIs That Need Import**:
| API | Description | Import |
|-----|-------------|--------|
| `ref` | Reactive primitive | `import { ref } from 'vue'` |
| `reactive` | Reactive object | `import { reactive } from 'vue'` |
| `computed` | Computed property | `import { computed } from 'vue'` |
| `watch` | Watcher | `import { watch } from 'vue'` |
| `watchEffect` | Immediate watcher | `import { watchEffect } from 'vue'` |
| `onMounted` | Lifecycle hook | `import { onMounted } from 'vue'` |
| `onUnmounted` | Lifecycle hook | `import { onUnmounted } from 'vue'` |
| `nextTick` | Next DOM update | `import { nextTick } from 'vue'` |
| `toRefs` | Destructure reactive | `import { toRefs } from 'vue'` |

**Pattern: Adding to Existing Vue Import**:
```typescript
// Before
import { ref } from 'vue'

// After
import { ref, computed, watch, onMounted } from 'vue'
```

**Pattern: Creating New Vue Import**:
```typescript
// Before
import MyComponent from '@/components/MyComponent.vue'

// After
import { ref, computed } from 'vue'
import MyComponent from '@/components/MyComponent.vue'
```

---

### Check 8: Event Handlers

**Issue**: Stories use components with event emitters but don't provide handlers for critical events (`@close`, `@submit`, `@confirm`, `@cancel`)

**Detection**:
```bash
# Step 1: Find components with event emitters
grep -rn "defineEmits" src/components/ --include="*.vue" | cut -d: -f1 | sort -u

# Step 2: For each component, check if stories provide handlers for critical events
# Manual review recommended for critical events: @close, @submit, @confirm, @cancel
```

**Critical Events Checklist**:

For **Modal/Overlay** components:
- [ ] `@close` - User closes modal (X button, backdrop click, ESC)
- [ ] `@confirm` - User confirms action
- [ ] `@cancel` - User cancels action

For **Form** components:
- [ ] `@submit` - User submits form
- [ ] `@cancel` - User cancels form

For **Dropdown/Menu** components:
- [ ] `@close` - User closes dropdown (selection made, click outside)
- [ ] `@select` - User selects item

**Problematic Pattern**:
```typescript
// Component defines emits
const emit = defineEmits<{
  close: []
  confirm: []
  cancel: []
}>()

// Story - MISSING HANDLERS ❌
export const Default: Story = {
  args: {
    isOpen: true,
    title: 'Confirm Action',
  },
  render: (args) => ({
    components: { ConfirmationModal },
    template: `
      <ConfirmationModal
        :is-open="args.isOpen"
        :title="args.title"
        // ❌ Missing: @close handler
        // ❌ Missing: @confirm handler
        // ❌ Missing: @cancel handler
      />
    `
  })
}
```

**Fix Pattern A: Noop Handlers (Simplest)**:
```typescript
export const Default: Story = {
  args: {
    isOpen: true,
    title: 'Confirm Action',
  },
  render: (args) => ({
    components: { ConfirmationModal },
    template: `
      <ConfirmationModal
        :is-open="args.isOpen"
        :title="args.title"
        @close="() => console.log('Closed')"
        @confirm="() => console.log('Confirmed')"
        @cancel="() => console.log('Cancelled')"
      />
    `
  })
}
```

**Fix Pattern B: Interactive Demo with State**:
```typescript
export const InteractiveDemo: Story = {
  render: () => ({
    components: { ConfirmationModal },
    setup() {
      const isOpen = ref(true)

      const handleClose = () => {
        console.log('Modal closed')
        isOpen.value = false
      }

      const handleConfirm = () => {
        console.log('Confirmed action')
        isOpen.value = false
      }

      const handleCancel = () => {
        console.log('Cancelled')
        isOpen.value = false
      }

      return { isOpen, handleClose, handleConfirm, handleCancel }
    },
    template: `
      <ConfirmationModal
        :is-open="isOpen"
        title="Confirm Action"
        @close="handleClose"
        @confirm="handleConfirm"
        @cancel="handleCancel"
      />
    `
  })
}
```

**Detection Workflow**:
1. Check component's `defineEmits` declaration
2. Identify critical events (close, submit, confirm, cancel)
3. Verify story provides handlers for these events
4. Add noop handlers where missing

---

## Audit Workflow

### Step 1: Run Full Audit
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
echo "--- Hex colors ---"
grep -rn "#[0-9a-fA-F]\{3,8\}" src/stories/ --include="*.ts" 2>/dev/null | head -15 || echo "None found"
echo "--- Hardcoded rgba ---"
grep -rn "rgba(" src/stories/ --include="*.ts" 2>/dev/null | head -10 || echo "None found"
echo ""
echo "=== 6. Missing Vue Imports ==="
grep -rn "\bref\b\|\breactive\b\|\bcomputed\b\|\bwatch\b\|\bonMounted\b\|\bonUnmounted\b\|\bnextTick\b" src/stories/ --include="*.ts" -l 2>/dev/null | \
  while read file; do
    if ! grep -q "from 'vue'" "$file"; then
      echo "$file"
    fi
  done | head -20 || echo "None found"
echo ""
echo "=== 7. Missing Event Handlers (Manual Check) ==="
echo "Critical events to verify: @close, @submit, @confirm, @cancel"
echo "Check if stories provide handlers for these events"
echo ""
echo "=== Audit Complete ==="
```

### Step 2: Ask User About Findings

After audit, present findings and ask:
- "I found X issues. Which would you like me to fix first?"
- "For the [component] cutoff, what is the maximum expanded height?"
- "Should I create a fresh Pinia decorator for store-dependent stories?"

### Step 3: Apply Fixes

Apply fixes one at a time, verify each works before proceeding.

### Step 4: Update Skill

If fix works, ask: "Should I add [ComponentName] guidelines to this skill's knowledge base?"

---

## Known Issues Reference

### ISSUE-011: PouchDB Document Conflicts

When stores are imported in Storybook:
- PouchDB initializes on first store access
- If main app has accumulated conflicts (178+ tasks, 171+ projects), Storybook will error
- Error message: "Document update conflict"

**Symptoms**:
- Storybook docs page shows error instead of component
- Console shows conflict warnings:
  ```
  ⚠️ [DATABASE] Document tasks:data has 178 conflicts
  ```

**Immediate Fix**: Use mock stores or props-only approach

**Root Fix**: Resolve PouchDB conflicts in main app (see ISSUE-011 in MASTER_PLAN.md)

---

## Component-Specific Guidelines

<!-- This section is auto-updated when fixes are approved -->

### TaskContextMenu (Added: 2025-12-19)
- Minimum height: 900px (has cascading submenus)
- Needs mock task data, not store
- All event handlers should be noops or console.log
- Layout: fullscreen required

### ContextMenu (Added: 2025-12-19)
- Minimum height: 600px
- Position must be calculated in render function
- Use `onMounted` for centering

### Modal Components (General)
- Always use `layout: 'fullscreen'`
- Wrap in full-height container div
- Provide toggle mechanism for interactive demos
- Test both open and closed states

### Auth Components (Added: 2025-12-21)
- **Styling**: Must use "Dark Glass" aesthetic to match `BaseDropdown` reference.
  - Background: `var(--glass-bg-solid)` (alias for `rgba(0, 0, 0, 0.95)`)
  - Border: None (clean glass look)
  - Layout: `inline: true` with fixed height relative container (600px-800px)
- **Labels**: Use descriptive names ("Default View", "Loading State") instead of generic exports.
- **Positioning**: Use relative container pattern (Fix Pattern B) to prevent cutoff.

---

## Best Practices

1. **Never import real stores** - Always use mock data or decorators
2. **Size for expanded content** - Check component's maximum expanded state for height
3. **Test in docs view** - Docs pages render differently than story pages
4. **Check console** - Database errors appear in browser console
5. **Use realistic data** - Mock data should match real interface types
6. **MANDATORY: Use design tokens** - ALL colors must use `var(--token)` not hardcoded values:
   - No hex colors (`#xxx`)
   - No rgb/rgba values
   - Use tokens from `design-tokens.css` or `token_definitions.json`
   - Run token audit before completing any story

---

## External Resources

- [Storybook Vue 3 Vite Docs](https://storybook.js.org/docs/get-started/frameworks/vue3-vite)
- [Pinia Testing Guide](https://pinia.vuejs.org/cookbook/testing.html)
- [Storybook Pinia Recipe](https://storybook.js.org/recipes/pinia)
- [GitHub: Storybook iframe height issue](https://github.com/storybookjs/storybook/issues/13765)
- [GitHub: Pinia with Storybook Discussion](https://github.com/storybookjs/storybook/discussions/17685)

---

## Example Files

Before/after examples are available in `examples/` directory:
- `before-after-modal-iframe.md` - Iframe height fix for modals
- `before-after-contextmenu-height.md` - Height fix for cascading menus
- `before-after-store-dependency.md` - Real case from AuthModal (store dependency fix)
- `before-after-template-style.md` - Template `<style>` tag fix
- `before-after-props-mismatch.md` - Props matching component definitions
- `before-after-missing-imports.md` - Missing Vue imports fix (NEW)
- `before-after-event-handlers.md` - Missing event handlers fix (NEW)

Each example includes:
- Problem description
- Detection method
- Before/after code
- Solution explanation
- Verification steps

---

## Related Skills

- `dev-storybook` - Story creation patterns and structure
- `dev-vue` - Vue 3 component development

## Related Issues

- ISSUE-011: PouchDB Document Conflict Accumulation
- TASK-014: Storybook Glass Morphism Streamlining
- TASK-029: This skill's implementation tracking

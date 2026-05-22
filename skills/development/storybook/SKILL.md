---
name: agent-storybook
description: Storybook expert for Angular 21+ component development, visual testing, and design system documentation
tags:
  - storybook
  - angular
  - components
  - testing
  - design-system
  - frontend
version: 1.0.0
---

# Storybook Skill

Expert in Storybook for Angular 21+ - component-driven development, visual testing, and living design system documentation.

## When to Use This Skill

Use this skill when:

- Creating or updating component stories
- Setting up Storybook for a project
- Creating design system documentation stories
- Visual testing and accessibility testing
- Troubleshooting Storybook issues
- Configuring Storybook addons
- Writing component documentation

## Core Principles

### Component-Driven Development

- Build components in isolation before integrating into app
- Test all component states and variants
- Document component API (inputs, outputs, methods)
- Use Storybook as the single source of truth for UI components

### Story Best Practices

- One story file per component (`.stories.ts`)
- Export multiple story variants showing different states
- Use descriptive story names (Primary, Disabled, Loading, Error, etc.)
- Include all edge cases and states
- Add accessibility testing to every story

## Project Structure

### Standard Storybook Setup

```
apps/frontend/
├── .storybook/
│   ├── main.ts          # Main configuration
│   ├── preview.ts       # Global decorators & parameters
│   └── manager.ts       # UI customization (optional)
├── src/
│   └── app/
│       ├── components/
│       │   └── button/
│       │       ├── button.component.ts
│       │       └── button.stories.ts
│       └── pages/
│           └── home/
│               ├── home.component.ts
│               └── home.stories.ts
```

## Story Naming Convention

### Hierarchical Structure

Use `/` separator for organization:

**Components:**

- `Components/Button` - Basic button
- `Components/Forms/Input` - Nested form input
- `Components/Cards/TaskCard` - Card components

**Pages:**

- `Pages/Home` - Page-level story
- `Pages/Auth/Login` - Nested page

**Design System:**

- `Design System/Colors` - Color palette
- `Design System/Typography` - Font styles
- `Design System/Spacing` - Spacing tokens

**Examples:**

- `Examples/Forms/LoginForm` - Complete form example
- `Examples/Layouts/Dashboard` - Layout example

## Story Template (Angular 21+ Standalone)

### Basic Component Story

```typescript
import type { Meta, StoryObj } from '@storybook/angular';
import { ButtonComponent } from './button.component';

const meta: Meta<ButtonComponent> = {
  title: 'Components/Button',
  component: ButtonComponent,
  tags: ['autodocs'], // Automatic documentation
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'danger'],
      description: 'Button visual style',
    },
    size: {
      control: 'select',
      options: ['small', 'medium', 'large'],
    },
    disabled: {
      control: 'boolean',
    },
    loading: {
      control: 'boolean',
    },
  },
};

export default meta;
type Story = StoryObj<ButtonComponent>;

// Primary state
export const Primary: Story = {
  args: {
    label: 'Click me',
    variant: 'primary',
    size: 'medium',
  },
};

// Secondary state
export const Secondary: Story = {
  args: {
    label: 'Click me',
    variant: 'secondary',
  },
};

// Disabled state
export const Disabled: Story = {
  args: {
    label: 'Click me',
    disabled: true,
  },
};

// Loading state
export const Loading: Story = {
  args: {
    label: 'Please wait...',
    loading: true,
  },
};

// All sizes comparison
export const AllSizes: Story = {
  render: (args) => ({
    props: args,
    template: `
      <div style="display: flex; gap: 1rem; align-items: center;">
        <app-button size="small" [label]="label"></app-button>
        <app-button size="medium" [label]="label"></app-button>
        <app-button size="large" [label]="label"></app-button>
      </div>
    `,
  }),
  args: {
    label: 'Click me',
  },
};
```

### Component with Services/Dependencies

```typescript
import type { Meta, StoryObj } from '@storybook/angular';
import { applicationConfig } from '@storybook/angular';
import { provideHttpClient } from '@angular/common/http';
import { TaskCardComponent } from './task-card.component';

const meta: Meta<TaskCardComponent> = {
  title: 'Components/Cards/TaskCard',
  component: TaskCardComponent,
  tags: ['autodocs'],
  decorators: [
    applicationConfig({
      providers: [
        provideHttpClient(),
        // Add other providers here
      ],
    }),
  ],
};

export default meta;
type Story = StoryObj<TaskCardComponent>;

export const Default: Story = {
  args: {
    task: {
      id: '1',
      title: 'Clean bathroom',
      assignee: 'Alex',
      points: 10,
      completed: false,
    },
  },
};

export const Completed: Story = {
  args: {
    task: {
      id: '2',
      title: 'Take out trash',
      assignee: 'Sarah',
      points: 5,
      completed: true,
    },
  },
};
```

### Complex Layout Story

```typescript
import type { Meta, StoryObj } from '@storybook/angular';
import { HomeComponent } from './home.component';
import { TaskCardComponent } from '../../components/task-card/task-card.component';
import { StatCardComponent } from '../../components/stat-card/stat-card.component';

const meta: Meta<HomeComponent> = {
  title: 'Pages/Home',
  component: HomeComponent,
  tags: ['autodocs'],
  parameters: {
    layout: 'fullscreen', // Use full viewport
  },
  decorators: [
    applicationConfig({
      providers: [
        /* ... */
      ],
    }),
  ],
};

export default meta;
type Story = StoryObj<HomeComponent>;

export const Default: Story = {};

export const WithManyTasks: Story = {
  args: {
    tasks: [
      { id: '1', title: 'Task 1' /* ... */ },
      { id: '2', title: 'Task 2' /* ... */ },
      { id: '3', title: 'Task 3' /* ... */ },
    ],
  },
};

export const EmptyState: Story = {
  args: {
    tasks: [],
  },
};
```

### Modal Component Story

**CRITICAL: All modal components MUST have Storybook stories.**

Modals require special testing because they have multiple interaction points (backdrop, ESC key, close button) that can fail silently.

```typescript
import type { Meta, StoryObj } from '@storybook/angular';
import { signal } from '@angular/core';
import { AddChildModal } from './add-child-modal';

const meta: Meta<AddChildModal> = {
  title: 'Components/Modals/AddChildModal',
  component: AddChildModal,
  tags: ['autodocs'],
  argTypes: {
    open: { control: 'boolean' },
  },
  // Decorators for modal positioning
  decorators: [
    (story) => ({
      template: `
        <div style="min-height: 600px; position: relative;">
          <story />
        </div>
      `,
    }),
  ],
};

export default meta;
type Story = StoryObj<AddChildModal>;

// Default: Modal open
export const Default: Story = {
  args: {
    open: true,
  },
};

// Closed state
export const Closed: Story = {
  args: {
    open: false,
  },
  parameters: {
    docs: {
      description: {
        story: 'Modal in closed state (not visible)',
      },
    },
  },
};

// With validation errors
export const WithValidationErrors: Story = {
  args: {
    open: true,
  },
  play: async ({ canvasElement }) => {
    // Simulate invalid form state for visual testing
    const canvas = within(canvasElement);
    const submitButton = await canvas.findByRole('button', { name: /add child/i });
    await userEvent.click(submitButton);
    // Form validation errors should now be visible
  },
};
```

**Modal Story Testing Checklist:**

Test these interactions in Storybook:

- [ ] **Open/Close**: Toggle `open` control
- [ ] **Close Button**: Click X button
- [ ] **Backdrop Click**: Click outside modal
- [ ] **ESC Key**: Press Escape
- [ ] **Form Validation**: Submit empty form
- [ ] **Loading State**: Test submitting state
- [ ] **Error State**: Test error messages
- [ ] **Accessibility**: No violations in a11y addon

**Common Modal Story Mistakes:**

❌ **Wrong:** No Storybook story (bugs discovered in production)
✅ **Correct:** Story created BEFORE integrating into app

❌ **Wrong:** Only testing open state
✅ **Correct:** Testing open, closed, loading, error states

❌ **Wrong:** Not testing close interactions
✅ **Correct:** Manually test X button, backdrop, ESC in Storybook

**See `.claude/skills/modal-components/SKILL.md` for Modal API usage.**

## Design System Documentation

### Color Palette Story

```typescript
import type { Meta, StoryObj } from '@storybook/angular';

const meta: Meta = {
  title: 'Design System/Colors',
  tags: ['autodocs'],
};

export default meta;

export const Primary: StoryObj = {
  render: () => ({
    template: `
      <div style="display: grid; gap: 1rem;">
        <div style="display: flex; align-items: center; gap: 1rem;">
          <div style="width: 100px; height: 100px; background: var(--color-primary); border-radius: 8px;"></div>
          <div>
            <h3>Primary</h3>
            <p>--color-primary: #6366F1</p>
          </div>
        </div>
        <div style="display: flex; align-items: center; gap: 1rem;">
          <div style="width: 100px; height: 100px; background: var(--color-secondary); border-radius: 8px;"></div>
          <div>
            <h3>Secondary</h3>
            <p>--color-secondary: #EC4899</p>
          </div>
        </div>
        <!-- Add more colors -->
      </div>
    `,
  }),
};

export const AllColors: StoryObj = {
  render: () => ({
    template: `
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;">
        <div style="background: var(--color-primary); padding: 2rem; border-radius: 8px; color: white;">
          <div style="font-weight: bold;">Primary</div>
          <div style="font-size: 0.875rem;">#6366F1</div>
        </div>
        <div style="background: var(--color-secondary); padding: 2rem; border-radius: 8px; color: white;">
          <div style="font-weight: bold;">Secondary</div>
          <div style="font-size: 0.875rem;">#EC4899</div>
        </div>
        <!-- Add all design system colors -->
      </div>
    `,
  }),
};
```

### Typography Story

```typescript
export const Typography: StoryObj = {
  render: () => ({
    template: `
      <div style="font-family: var(--font-body);">
        <h1 style="font-family: var(--font-heading); font-size: 48px; font-weight: 700;">
          Heading 1 - Fredoka
        </h1>
        <h2 style="font-family: var(--font-heading); font-size: 36px; font-weight: 600;">
          Heading 2 - Fredoka
        </h2>
        <p style="font-size: 16px;">
          Body text - Outfit Regular
        </p>
        <p style="font-size: 16px; font-weight: 600;">
          Body text - Outfit Semibold
        </p>
      </div>
    `,
  }),
};
```

## Storybook Configuration

### Main Configuration (`main.ts`)

```typescript
import type { StorybookConfig } from '@storybook/angular';

const config: StorybookConfig = {
  stories: ['../src/**/*.stories.@(js|jsx|mjs|ts|tsx)'],
  addons: [
    '@storybook/addon-essentials',
    '@storybook/addon-a11y',
    '@storybook/addon-interactions',
    '@storybook/addon-links',
  ],
  framework: {
    name: '@storybook/angular',
    options: {},
  },
  docs: {
    autodocs: 'tag', // Generate docs for components with 'autodocs' tag
  },
};

export default config;
```

### Preview Configuration (`preview.ts`)

```typescript
import type { Preview } from '@storybook/angular';
import { setCompodocJson } from '@storybook/addon-docs/angular';
import docJson from '../documentation.json';

setCompodocJson(docJson);

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: '^on[A-Z].*' },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    backgrounds: {
      default: 'light',
      values: [
        { name: 'light', value: '#F8F9FF' },
        { name: 'dark', value: '#1E293B' },
        { name: 'white', value: '#FFFFFF' },
      ],
    },
    viewport: {
      viewports: {
        mobile: {
          name: 'Mobile',
          styles: { width: '375px', height: '667px' },
          type: 'mobile',
        },
        tablet: {
          name: 'Tablet',
          styles: { width: '768px', height: '1024px' },
          type: 'tablet',
        },
        desktop: {
          name: 'Desktop',
          styles: { width: '1440px', height: '900px' },
          type: 'desktop',
        },
      },
    },
  },
};

export default preview;
```

## Essential Addons

### @storybook/addon-essentials

Includes: Controls, Actions, Viewport, Backgrounds, Toolbars, Measure, Outline

**Usage:**

- **Controls** - Interactive component props
- **Actions** - Log component events (@Output)
- **Viewport** - Test responsive behavior
- **Backgrounds** - Test on different backgrounds

### @storybook/addon-a11y

Accessibility testing with axe-core

**Usage:**

```typescript
export const MyComponent: Story = {
  parameters: {
    a11y: {
      config: {
        rules: [
          {
            id: 'color-contrast',
            enabled: true,
          },
        ],
      },
    },
  },
};
```

**Check for:**

- Color contrast (WCAG AA: 4.5:1 for text, 3:1 for UI)
- ARIA labels
- Keyboard navigation
- Focus indicators
- Semantic HTML

### @storybook/addon-interactions

Test user interactions

```typescript
import { within, userEvent } from '@storybook/testing-library';
import { expect } from '@storybook/jest';

export const ClickButton: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button');

    await userEvent.click(button);
    await expect(button).toHaveClass('clicked');
  },
};
```

## Component Development Workflow

### Step 1: Create Component

```bash
# Generate component
cd apps/frontend
ng generate component components/button --standalone
```

### Step 2: Create Story

```bash
# Create story file
touch src/app/components/button/button.stories.ts
```

### Step 3: Develop in Storybook

```bash
# Run Storybook
npm run storybook

# Storybook opens at localhost:6006
# Hot reload automatically updates as you code
```

### Step 4: Test All States

Create stories for:

- Default state
- All variants (primary, secondary, danger, etc.)
- All sizes (small, medium, large)
- Disabled state
- Loading state
- Error state
- Empty state (if applicable)
- With long text / edge cases

### Step 5: Accessibility Check

- Use a11y addon (bottom panel)
- Check all violations
- Fix color contrast issues
- Add ARIA labels
- Test keyboard navigation

### Step 6: Visual Review

- Test on all viewports (mobile, tablet, desktop)
- Test on all backgrounds (light, dark, white)
- Check hover states
- Check focus states
- Check animations

### Step 7: Integration

Once component is complete in Storybook:

- Import into parent component
- Use in actual app
- E2E test in real context

## Common Commands

### Development

```bash
# Start Storybook dev server
npm run storybook

# Build static Storybook
npm run build-storybook

# Generate Compodoc documentation
npm run storybook:docs

# Run both Compodoc and Storybook
npm run storybook:docs && npm run storybook
```

### Story Creation

```bash
# Create new story file
touch src/app/components/my-component/my-component.stories.ts

# Follow naming convention: {component-name}.stories.ts
```

## Troubleshooting

### Issue: Component not rendering

**Solution:**

- Check that component is standalone or imported in moduleMetadata
- Check that all dependencies are provided (services, HTTP client)
- Check console for errors

### Issue: Styles not loading

**Solution:**

- Import global styles in `preview.ts`
- Check component styleUrls path
- Ensure CSS variables are defined

### Issue: Compodoc failing

**Solution:**

```bash
# Regenerate documentation
npm run storybook:docs

# Check for TypeScript errors
npm run type-check
```

### Issue: Hot reload not working

**Solution:**

- Restart Storybook
- Clear browser cache
- Check for conflicting ports

## Best Practices Checklist

### Every Component Story Should Have:

- [ ] Multiple story variants (Default, Disabled, Loading, etc.)
- [ ] All input combinations tested
- [ ] Accessibility testing enabled (a11y addon)
- [ ] Proper argTypes with descriptions
- [ ] Tags: ['autodocs'] for automatic documentation
- [ ] JSDoc comments on @Input() and @Output()

### Every Design System Story Should Have:

- [ ] Visual representation
- [ ] Code examples
- [ ] Usage guidelines
- [ ] Do's and Don'ts (optional)

### Story Organization:

- [ ] Hierarchical naming (Components/, Pages/, Design System/)
- [ ] Alphabetical ordering within categories
- [ ] Consistent naming convention

## Integration with CI/CD

### Build Storybook in CI

```yaml
# GitHub Actions example
- name: Build Storybook
  run: |
    cd apps/frontend
    npm run storybook:docs
    npm run build-storybook
```

### Deploy Storybook

```bash
# Build static version
npm run build-storybook

# Deploy to static hosting (Netlify, Vercel, GitHub Pages)
# Output directory: storybook-static/
```

### Visual Regression Testing

Consider adding:

- Chromatic (visual testing platform)
- Percy (visual review)
- Storybook test runner

## Success Criteria

After implementing this skill:

- ✅ All components have corresponding stories
- ✅ Design system fully documented
- ✅ Accessibility testing on every component
- ✅ Visual regression testing enabled
- ✅ Developers can create stories in < 5 minutes
- ✅ Storybook deployed for team collaboration

## References

### Official Documentation

- [Storybook for Angular](https://storybook.js.org/docs/get-started/frameworks/angular)
- [Writing Stories](https://storybook.js.org/docs/writing-stories)
- [Essential Addons](https://storybook.js.org/docs/essentials)
- [Accessibility Addon](https://storybook.js.org/addons/@storybook/addon-a11y)

### Angular-Specific

- [Angular Standalone Components](https://angular.dev/guide/components)
- [Angular Signals](https://angular.dev/guide/signals)
- [Angular OnPush Change Detection](https://angular.dev/best-practices/runtime-performance)

## Related Skills

Use together with:

- **frontend** skill - Angular 21+ component development
- **frontend-design** skill - UI design principles
- **ux-design** skill - User experience patterns

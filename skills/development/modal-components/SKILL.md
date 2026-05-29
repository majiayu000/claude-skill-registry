# Modal Components Skill

**CRITICAL: All modals MUST use the global Modal component with the correct API**

## Overview

The Diddit! app has a centralized, reusable Modal component at `apps/frontend/src/app/components/modals/modal/modal.ts`. This component handles ALL modal functionality in one place:

- ✅ Backdrop click to close
- ✅ ESC key to close
- ✅ Close button (X) to close
- ✅ Focus trap
- ✅ Body scroll prevention
- ✅ Accessibility (ARIA attributes, roles)
- ✅ Animations

**NEVER reimplement these features. ALWAYS use the global Modal component.**

## Correct API

### Inputs

```typescript
open = input<boolean>(false); // Whether modal is open
title = input<string>(''); // Modal title text
closeOnBackdropClick = input<boolean>(true); // Allow backdrop close (default: true)
closeOnEsc = input<boolean>(true); // Allow ESC close (default: true)
```

### Outputs

```typescript
closeModal = output<void>(); // Emitted when modal should close
```

**CRITICAL: The output is `closeModal`, NOT `closeRequested`, NOT `close`, NOT anything else.**

## Template Pattern

### ✅ CORRECT Usage

```html
<app-modal [open]="open()" (closeModal)="handleClose()" title="Modal Title">
  <!-- Your modal content here -->
  <form>
    <!-- Form fields -->
  </form>

  <!-- Action buttons (optional) -->
  <div class="modal-actions" modal-actions>
    <button type="button" class="btn btn-secondary" (click)="onCancel()">Cancel</button>
    <button type="submit" class="btn btn-primary">Submit</button>
  </div>
</app-modal>
```

### Key Points

1. **Use `[open]` input** - Pass a signal or boolean to control visibility
2. **Use `(closeModal)` output** - Listen to the EXACT event name `closeModal`
3. **Use `title` input** - Pass title as input property, NOT using slots
4. **Use `modal-actions` attribute** - For footer buttons (optional)
5. **Content goes in default slot** - Just put content inside `<app-modal>` tags

### ❌ WRONG - Do NOT Do This

```html
<!-- WRONG: Using wrong event name -->
<app-modal [open]="open()" (closeRequested)="handleClose()">
  <!-- WRONG: Using slots for title -->
  <app-modal [open]="open()" (closeModal)="handleClose()">
    <h2 slot="title">Modal Title</h2>

    <!-- WRONG: Using old @Output name -->
    <app-modal [open]="open()" (close)="handleClose()">
      <!-- WRONG: Not binding to signal/property -->
      <app-modal open="true" (closeModal)="handleClose()"></app-modal></app-modal></app-modal
></app-modal>
```

## Component TypeScript Pattern

### ✅ CORRECT Component

```typescript
import { Component, input, output, signal } from '@angular/core';
import { Modal } from '../modals/modal/modal';

@Component({
  selector: 'app-my-modal',
  imports: [Modal],
  templateUrl: './my-modal.html',
  styleUrl: './my-modal.css',
})
export class MyModal {
  // Inputs
  open = input<boolean>(false);
  someData = input<string>('');

  // Outputs
  closeRequested = output<void>(); // Emit to parent when modal should close

  // Internal state
  submitting = signal(false);

  /**
   * Handle modal close (called by Modal's closeModal event)
   */
  handleClose(): void {
    this.closeRequested.emit();
  }

  /**
   * Handle cancel button
   */
  onCancel(): void {
    this.closeRequested.emit();
  }

  /**
   * Handle form submission
   */
  onSubmit(): void {
    // Do work...
    this.closeRequested.emit();
  }
}
```

### Key Points

1. **Import Modal component** - Add to `imports` array
2. **Accept `open` input** - Let parent control visibility
3. **Emit `closeRequested` output** - Let parent handle closing
4. **Create `handleClose()` method** - Connect Modal's `(closeModal)` to your `closeRequested` output
5. **Don't manage open state internally** - Parent controls it

## Real Working Examples

Study these working modals in the codebase:

### add-child-modal

- **Location**: `apps/frontend/src/app/components/modals/add-child-modal/`
- **Pattern**: Form modal with validation
- **Template**: Uses `(closeModal)`, `title` input, `modal-actions` slot

### invite-modal

- **Location**: `apps/frontend/src/app/components/modals/invite-modal/`
- **Pattern**: Form modal with role selection
- **Template**: Uses `(closeModal)`, `title` input, `modal-actions` slot

### task-form-modal

- **Location**: `apps/frontend/src/app/components/modals/task-form-modal/`
- **Pattern**: Complex form with conditional fields, delete confirmation
- **Template**: Uses `(closeModal)`, dynamic `[title]`, `modal-actions` slot

## Common Mistakes

### ❌ Mistake 1: Wrong Event Name

**Problem**: Listening for `(closeRequested)` or `(close)` instead of `(closeModal)`

```html
<!-- WRONG -->
<app-modal [open]="open()" (closeRequested)="handleClose()"></app-modal>
```

**Result**: Modal won't close when clicking X, backdrop, or pressing ESC

**Fix**: Use `(closeModal)`

```html
<!-- CORRECT -->
<app-modal [open]="open()" (closeModal)="handleClose()"></app-modal>
```

### ❌ Mistake 2: Using Slots for Title

**Problem**: Trying to use slot-based API that doesn't exist

```html
<!-- WRONG -->
<app-modal [open]="open()" (closeModal)="handleClose()"> <h2 slot="title">My Title</h2></app-modal>
```

**Result**: Title appears in modal body, not header. Empty header shows.

**Fix**: Use `title` input

```html
<!-- CORRECT -->
<app-modal [open]="open()" (closeModal)="handleClose()" title="My Title"></app-modal>
```

### ❌ Mistake 3: Duplicate Headers

**Problem**: Setting title on Modal AND adding header in content

```html
<!-- WRONG -->
<app-modal [open]="open()" (closeModal)="handleClose()" title="Add Task">
  <h2>Add Task</h2>
  <!-- Duplicate header! -->
  <form>...</form>
</app-modal>
```

**Result**: Two headers appear

**Fix**: Only use Modal's title input

```html
<!-- CORRECT -->
<app-modal [open]="open()" (closeModal)="handleClose()" title="Add Task">
  <form>...</form>
  <!-- No duplicate header -->
</app-modal>
```

## Storybook Requirement

**CRITICAL: Every modal component MUST have a Storybook story.**

### Why?

Storybook catches modal bugs immediately:

- Close functionality (X button, backdrop, ESC)
- Header rendering
- Form validation
- Loading states
- Error states

### Story Template

```typescript
// my-modal.stories.ts
import type { Meta, StoryObj } from '@storybook/angular';
import { MyModal } from './my-modal';

const meta: Meta<MyModal> = {
  title: 'Components/Modals/MyModal',
  component: MyModal,
  tags: ['autodocs'],
  argTypes: {
    open: { control: 'boolean' },
  },
};

export default meta;
type Story = StoryObj<MyModal>;

export const Default: Story = {
  args: {
    open: true,
  },
};

export const Closed: Story = {
  args: {
    open: false,
  },
};

export const WithData: Story = {
  args: {
    open: true,
    someData: 'Example data',
  },
};
```

### Testing Checklist in Storybook

When viewing your modal story, verify:

- [ ] Modal opens when `open: true`
- [ ] Modal closes when clicking X button
- [ ] Modal closes when clicking backdrop
- [ ] Modal closes when pressing ESC key
- [ ] Modal title appears in header (not body)
- [ ] Only ONE header appears (no duplicates)
- [ ] Form validation works
- [ ] Action buttons work
- [ ] Loading states work
- [ ] Error states work

## Modal Component Source

For reference, the global Modal component is at:

**TypeScript**: `apps/frontend/src/app/components/modals/modal/modal.ts`

- Inputs: `open`, `title`, `closeOnBackdropClick`, `closeOnEsc`
- Outputs: `closeModal`
- Methods: `onBackdropClick()`, `onEscapeKey()`, `onCloseClick()`, `onTabKey()`

**Template**: `apps/frontend/src/app/components/modals/modal/modal.html`

- Overlay with backdrop click handler
- Header with title and close button
- Body with `<ng-content>` for default content
- Footer with `<ng-content select="[modal-actions]">` for action buttons

**Styles**: `apps/frontend/src/app/components/modals/modal/modal.css`

- Animations, layout, accessibility

## Quick Checklist

Before creating a modal, verify:

- [ ] Import `Modal` component
- [ ] Use `(closeModal)` output (NOT `closeRequested`, NOT `close`)
- [ ] Use `title` input (NOT slots)
- [ ] Accept `open` input from parent
- [ ] Emit `closeRequested` to parent
- [ ] Create `handleClose()` method to bridge events
- [ ] Use `modal-actions` attribute for footer buttons
- [ ] Create Storybook story
- [ ] Test all close methods in Storybook (X, backdrop, ESC)
- [ ] Verify no duplicate headers

## Summary

**The golden rule**: Study existing working modals (`add-child-modal`, `invite-modal`, `task-form-modal`) and copy their patterns exactly. Don't invent new APIs or patterns.

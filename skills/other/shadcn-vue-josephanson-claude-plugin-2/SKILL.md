---
name: shadcn-vue
description: This skill provides best practices for using Shadcn Vue components in the fitness app. Use when working with UI components, forms, dialogs, or implementing component patterns.
---

# Shadcn Vue Best Practices

This skill provides guidance for using Shadcn Vue components effectively in the fitness application.

## Core Principles

**Component Naming**: All Shadcn Vue components are prefixed with `UI` (e.g., `UIButton`, `UIDialog`, `UICard`, `UIInput`). This is enforced across the entire codebase for consistency.

**Semantic Colors**: Use CSS variables for theming instead of arbitrary Tailwind colors:
- `bg-background`, `text-foreground` - Base colors
- `bg-primary`, `text-primary-foreground` - Primary actions
- `bg-secondary`, `text-secondary-foreground` - Secondary elements
- `bg-muted`, `text-muted-foreground` - Subtle backgrounds
- `bg-accent`, `text-accent-foreground` - Highlights
- `bg-destructive`, `text-destructive-foreground` - Errors/delete actions
- `bg-card`, `text-card-foreground` - Card backgrounds
- `border-border`, `ring-ring` - Borders and focus rings

**Documentation**: When looking up shadcn components, use the pattern: `https://www.shadcn-vue.com/docs/components/{component}.html` where `{component}` is the component name (e.g., `tooltip`, `button`, `dialog`).

## UIDialog Pattern (Critical)

**NEVER use refs to manage dialog state.** Use the `v-slot="{ close }"` pattern:

```vue
<UIDialog v-slot="{ close }">
  <UIDialogTrigger as-child>
    <UIButton>Open Dialog</UIButton>
  </UIDialogTrigger>
  <UIDialogContent>
    <UIDialogHeader>
      <UIDialogTitle>Dialog Title</UIDialogTitle>
      <UIDialogDescription>Description text</UIDialogDescription>
    </UIDialogHeader>

    <!-- Content -->

    <UIDialogFooter>
      <UIButton variant="outline" @click="close">Cancel</UIButton>
      <UIButton @click="handleSubmit(); close()">Save</UIButton>
    </UIDialogFooter>
  </UIDialogContent>
</UIDialog>
```

For detailed dialog patterns including multiple dialogs and form integration, see `references/dialog-pattern.md`.

## Form Validation (Required)

**All forms MUST use vee-validate with Zod schemas.** Never create forms without schema validation.

Basic pattern:
```vue
<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { z } from 'zod'
import { useForm } from 'vee-validate'

const formSchema = toTypedSchema(z.object({
  name: z.string().min(2).max(50),
  email: z.email(),
}))

const { handleSubmit } = useForm({ validationSchema: formSchema })

const onSubmit = handleSubmit((values) => {
  // Handle form submission
})
</script>

<template>
  <form @submit="onSubmit">
    <UIFormField v-slot="{ componentField }" name="name">
      <UIFormItem>
        <UIFormLabel>Name</UIFormLabel>
        <UIFormControl>
          <UIInput type="text" v-bind="componentField" />
        </UIFormControl>
        <UIFormMessage />
      </UIFormItem>
    </UIFormField>

    <UIButton type="submit">Submit</UIButton>
  </form>
</template>
```

For complete form patterns and advanced validation, see `references/form-validation.md`.

## Component Organization

Components follow a folder-based structure:
```
components/
├── {Feature}/
│   ├── Form/
│   │   ├── Create.vue      # Creation form
│   │   ├── Edit.vue        # Edit form
│   │   └── Delete.vue      # Delete confirmation
│   ├── Card.vue            # Display card
│   └── List.vue            # List view
```

Auto-import naming:
- `components/Goal/Form/Create.vue` → `<GoalFormCreate />`
- `components/Goal/Card.vue` → `<GoalCard />`

For complete component conventions, see `references/component-patterns.md`.

## Common Components Quick Reference

**UIButton**:
```vue
<UIButton variant="default">Submit</UIButton>
<UIButton variant="outline" size="sm">Cancel</UIButton>
<UIButton icon="i-lucide-plus" to="/create">Create</UIButton>
<UIButton variant="destructive" icon="i-lucide-trash">Delete</UIButton>
```
Variants: `default`, `destructive`, `outline`, `secondary`, `ghost`, `link`

**UICard**:
```vue
<UICard>
  <UICardHeader>
    <UICardTitle>Title</UICardTitle>
    <UICardDescription>Description</UICardDescription>
  </UICardHeader>
  <UICardContent>Content</UICardContent>
  <UICardFooter>
    <UIButton>Action</UIButton>
  </UICardFooter>
</UICard>
```

**UISelect** (multi-component pattern):
```vue
<UISelect v-model="value">
  <UISelectTrigger>
    <UISelectValue placeholder="Select..." />
  </UISelectTrigger>
  <UISelectContent>
    <UISelectGroup>
      <UISelectLabel>Group Label</UISelectLabel>
      <UISelectItem value="option1">Option 1</UISelectItem>
      <UISelectItem value="option2">Option 2</UISelectItem>
    </UISelectGroup>
  </UISelectContent>
</UISelect>
```

**UIToast** (vue-sonner):
```typescript
import { toast } from 'vue-sonner'

toast.success('Success!', {
  description: 'Your changes have been saved.',
})

toast.error('Error!', {
  description: 'Something went wrong.',
})
```

## Critical Rules

### ✅ MUST DO
- Use `UI` prefix for all Shadcn components
- Use semantic color variables (e.g., `bg-primary`, `text-foreground`)
- Use vee-validate with Zod for all forms
- Use `v-slot="{ close }"` pattern for dialogs
- Use `UIAlertDialog` for confirmations (never native `confirm()`)
- Ensure keyboard accessibility and screen reader support
- Provide meaningful `aria-label` for icon-only buttons
- Use mobile-first responsive design

### ❌ NEVER DO
- Mix Shadcn with other component libraries (e.g., Nuxt UI)
- Use arbitrary Tailwind colors (e.g., `bg-blue-500`)
- Create forms without Zod validation schemas
- Use refs to manage dialog state (`isOpen.value`)
- Use native browser dialogs (`confirm()`, `alert()`, `prompt()`)
- Skip loading, error, or empty states in async components
- Rely solely on color to convey information (use icons/text too)
- Use generic button text like "Click here"

## Accessibility Requirements

1. **Keyboard Navigation**: All interactive elements must be keyboard accessible
2. **Screen Reader Support**: Provide proper ARIA labels and descriptions
3. **Color Contrast**: Ensure sufficient contrast for text and interactive elements
4. **Focus Indicators**: Never remove focus rings without providing alternatives
5. **Icon-Only Buttons**: Always include `aria-label` attributes
6. **Form Validation**: Error messages must be associated with form fields

## Reference Files

For detailed information, reference these files as needed:
- `references/component-patterns.md` - Complete component organization and naming conventions
- `references/dialog-pattern.md` - Detailed dialog patterns including multiple dialogs
- `references/form-validation.md` - Complete form validation patterns and examples

## Component Documentation URL Pattern

To look up Shadcn Vue component documentation:
```
https://www.shadcn-vue.com/docs/components/{component}.html
```

Examples:
- Button: `https://www.shadcn-vue.com/docs/components/button.html`
- Dialog: `https://www.shadcn-vue.com/docs/components/dialog.html`
- Form: `https://www.shadcn-vue.com/docs/components/form.html`
- Select: `https://www.shadcn-vue.com/docs/components/select.html`

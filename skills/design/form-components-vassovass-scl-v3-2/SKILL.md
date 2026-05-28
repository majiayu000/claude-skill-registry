---
name: form-components
description: StepLeague reusable form components with accessibility features. Use when creating any form, input field, select dropdown, checkbox, or file upload in the application. Keywords: form, input, select, checkbox, textarea, file upload, accessibility, FormInput, FormSelect.
compatibility: Antigravity, Claude Code, Cursor
metadata:
  version: "1.1"
  project: "stepleague"
---

# Form Components Skill

## Core Rule

**ALWAYS use form components from `@/components/ui/form-fields`.**

These components:
- Auto-generate `id`/`name` attributes
- Include accessibility features (aria-describedby, aria-invalid)
- Consistent styling across the app
- Proper label association

---

## Available Components

| Component | Purpose |
|-----------|---------|
| `FormInput` | Text, email, password, number inputs |
| `FormSelect` | Dropdown select |
| `FormCheckbox` | Checkbox with label |
| `FormTextarea` | Multi-line text input |
| `FormFileInput` | File upload |

---

## Usage Examples

### FormInput

```tsx
import { FormInput } from "@/components/ui/form-fields";

<FormInput
  fieldName="user-email"
  label="Email Address"
  type="email"
  placeholder="you@example.com"
  required
  error={errors.email}
  description="We'll never share your email"
/>

<FormInput
  fieldName="step-count"
  label="Steps"
  type="number"
  min={0}
  max={100000}
  value={steps}
  onChange={(e) => setSteps(e.target.value)}
/>
```

### FormSelect

```tsx
import { FormSelect } from "@/components/ui/form-fields";

<FormSelect
  fieldName="league-select"
  label="Select League"
  value={selectedLeague}
  onChange={(e) => setSelectedLeague(e.target.value)}
  required
>
  <option value="">Choose a league...</option>
  {leagues.map((league) => (
    <option key={league.id} value={league.id}>
      {league.name}
    </option>
  ))}
</FormSelect>
```

### FormCheckbox

```tsx
import { FormCheckbox } from "@/components/ui/form-fields";

<FormCheckbox
  fieldName="accept-terms"
  label="I accept the terms and conditions"
  checked={acceptedTerms}
  onChange={(e) => setAcceptedTerms(e.target.checked)}
  required
/>

<FormCheckbox
  fieldName="remember-me"
  label="Remember me on this device"
  description="We'll keep you logged in for 30 days"
/>
```

### FormTextarea

```tsx
import { FormTextarea } from "@/components/ui/form-fields";

<FormTextarea
  fieldName="feedback"
  label="Your Feedback"
  placeholder="Tell us what you think..."
  rows={4}
  maxLength={500}
  value={feedback}
  onChange={(e) => setFeedback(e.target.value)}
/>
```

### FormFileInput

```tsx
import { FormFileInput } from "@/components/ui/form-fields";

<FormFileInput
  fieldName="screenshot"
  label="Upload Screenshot"
  accept="image/*"
  onChange={handleFileChange}
  description="PNG, JPG, or GIF up to 5MB"
  error={fileError}
/>
```

---

## Props Reference

### Common Props (All Components)

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `fieldName` | `string` | ✅ | Unique identifier (becomes id/name) |
| `label` | `string` | ✅ | Label text |
| `error` | `string` | ❌ | Error message to display |
| `description` | `string` | ❌ | Help text below field |
| `required` | `boolean` | ❌ | Adds required indicator |
| `disabled` | `boolean` | ❌ | Disables the field |
| `className` | `string` | ❌ | Additional CSS classes |

### FormInput Additional Props

| Prop | Type | Description |
|------|------|-------------|
| `type` | `string` | Input type (text, email, password, number, etc.) |
| `placeholder` | `string` | Placeholder text |
| `min`, `max` | `number` | For number inputs |
| `pattern` | `string` | Validation pattern |

### FormSelect Additional Props

| Prop | Type | Description |
|------|------|-------------|
| `children` | `ReactNode` | Option elements |
| `placeholder` | `string` | First disabled option text |

---

## Accessibility Features

The form components automatically provide:

### 1. Label Association

```html
<!-- Generated HTML -->
<label for="user-email">Email Address</label>
<input id="user-email" name="user-email" />
```

### 2. Error Announcements

```html
<!-- When error prop is provided -->
<input
  id="user-email"
  aria-invalid="true"
  aria-describedby="user-email-error"
/>
<p id="user-email-error" role="alert">Invalid email address</p>
```

### 3. Description Association

```html
<input aria-describedby="user-email-description" />
<p id="user-email-description">We'll never share your email</p>
```

---

## Form Patterns

### Basic Form

```tsx
import { FormInput, FormSelect, FormCheckbox } from "@/components/ui/form-fields";

function MyForm() {
  const [formData, setFormData] = useState({
    email: '',
    role: '',
    newsletter: false,
  });
  const [errors, setErrors] = useState({});

  return (
    <form onSubmit={handleSubmit}>
      <FormInput
        fieldName="email"
        label="Email"
        type="email"
        value={formData.email}
        onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
        error={errors.email}
        required
      />
      
      <FormSelect
        fieldName="role"
        label="Role"
        value={formData.role}
        onChange={(e) => setFormData(prev => ({ ...prev, role: e.target.value }))}
        required
      >
        <option value="">Select role...</option>
        <option value="member">Member</option>
        <option value="admin">Admin</option>
      </FormSelect>
      
      <FormCheckbox
        fieldName="newsletter"
        label="Subscribe to newsletter"
        checked={formData.newsletter}
        onChange={(e) => setFormData(prev => ({ ...prev, newsletter: e.target.checked }))}
      />
      
      <button type="submit">Submit</button>
    </form>
  );
}
```

### With Loading State

```tsx
<FormInput
  fieldName="email"
  label="Email"
  disabled={isSubmitting}
/>

<button type="submit" disabled={isSubmitting}>
  {isSubmitting ? "Saving..." : "Save"}
</button>
```

---

## Anti-Patterns

### ❌ Don't Use Raw HTML Elements

```tsx
// ❌ WRONG
<label>Email</label>
<input type="email" name="email" />

// ✅ CORRECT
<FormInput fieldName="email" label="Email" type="email" />
```

### ❌ Don't Forget fieldName

```tsx
// ❌ WRONG - no fieldName
<FormInput label="Email" type="email" />

// ✅ CORRECT
<FormInput fieldName="email" label="Email" type="email" />
```

### ❌ Don't Duplicate IDs

```tsx
// ❌ WRONG - duplicate fieldNames
<FormInput fieldName="email" label="Email" />
<FormInput fieldName="email" label="Confirm Email" />

// ✅ CORRECT - unique fieldNames
<FormInput fieldName="email" label="Email" />
<FormInput fieldName="confirm-email" label="Confirm Email" />
```

---

## Reference Files

| File | Purpose |
|------|---------|
| `src/components/ui/form-fields.tsx` | Component implementations |
| `docs/FORM_SYSTEM.md` | Full documentation |

---

## Related Skills

- `design-system` - Form styling and theming
- `architecture-philosophy` - Use existing components

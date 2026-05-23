---
name: forms
description: Build forms with FNForm component including validation, grid layouts, custom fields, and external control. Use when creating forms, adding validation, or building complex form UIs.
---

# Form Builder

Create forms using this project's centralized `FNForm` component.

## Quick Start

```typescript
import { FNForm, type FormDefinition } from '@/components/ui/fn-form'

const formDefinition: FormDefinition = {
  fields: [
    { name: 'email', type: 'email', label: 'Email', required: true },
    { name: 'name', type: 'text', label: 'Name' },
  ],
}

function MyForm() {
  const handleSubmit = (values: Record<string, unknown>) => {
    console.log(values)
  }

  return (
    <FNForm
      formDefinition={formDefinition}
      onSubmit={handleSubmit}
      submitButtonText="Save"
    />
  )
}
```

## Field Types

| Type       | Component             | Use Case                  |
| ---------- | --------------------- | ------------------------- |
| `text`     | Input                 | Single-line text          |
| `email`    | Input type="email"    | Email addresses           |
| `password` | Input type="password" | Passwords                 |
| `number`   | Input type="number"   | Numeric values            |
| `textarea` | Textarea              | Multi-line text           |
| `select`   | Select dropdown       | Choose from options       |
| `checkbox` | Checkbox              | Boolean with inline label |
| `switch`   | Switch                | Toggle with inline label  |
| `hidden`   | None (hidden)         | Hidden values             |
| `custom`   | Your component        | Anything else             |

## Field Definition

```typescript
interface FieldDefinition {
  name: string // Form field name (required)
  type: FieldType // Input type (required)
  label: string // Display label (required)
  placeholder?: string // Placeholder text
  required?: boolean // Shows * and validates
  optional?: boolean // Shows "(optional)"
  disabled?: boolean // Disable input
  options?: SelectOption[] // For select type
  validate?: (value: unknown) => string | undefined
  validateOnChange?: boolean // Validate as user types
  className?: string // Wrapper class
  inputClassName?: string // Input class
  labelClassName?: string // Label class
  prefix?: string // Input prefix (e.g., "$")
  maxLength?: number // Shows character count
  render?: (props: CustomFieldRenderProps) => ReactNode
}
```

## Grid Layouts

Use `rows` with `columns` for multi-column forms:

```typescript
const formDefinition: FormDefinition = {
  rows: [
    // Full width row
    {
      fields: [
        { name: 'email', type: 'email', label: 'Email', required: true },
      ],
    },

    // Two column row
    {
      columns: 2,
      fields: [
        {
          name: 'firstName',
          type: 'text',
          label: 'First Name',
          required: true,
        },
        { name: 'lastName', type: 'text', label: 'Last Name', required: true },
      ],
    },

    // Three column row
    {
      columns: 3,
      fields: [
        { name: 'city', type: 'text', label: 'City', required: true },
        { name: 'state', type: 'text', label: 'State' },
        { name: 'zip', type: 'text', label: 'ZIP', required: true },
      ],
    },
  ],
}
```

## Validation

### Required Fields

```typescript
{ name: 'email', type: 'email', label: 'Email', required: true }
// Shows * after label, validates on submit
```

### Custom Validation

```typescript
{
  name: 'email',
  type: 'email',
  label: 'Email',
  required: true,
  validate: (value) => {
    const email = value as string
    if (!email.includes('@company.com')) {
      return 'Must be a company email'
    }
    return undefined  // No error
  },
  validateOnChange: true,  // Validate as user types
}
```

### Common Validators

```typescript
// Email format
validate: (value) => {
  const email = value as string
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return 'Invalid email format'
  }
}

// Min length
validate: (value) => {
  if ((value as string).length < 8) {
    return 'Must be at least 8 characters'
  }
}

// Number range
validate: (value) => {
  const num = Number(value)
  if (num < 0 || num > 100) {
    return 'Must be between 0 and 100'
  }
}

// Match another field (password confirmation)
validate: (value, allValues) => {
  if (value !== allValues.password) {
    return 'Passwords do not match'
  }
}
```

## Select Dropdown

```typescript
{
  name: 'status',
  type: 'select',
  label: 'Status',
  placeholder: 'Select status',
  required: true,
  options: [
    { value: 'draft', label: 'Draft' },
    { value: 'active', label: 'Active' },
    { value: 'archived', label: 'Archived' },
  ],
}
```

## Custom Fields

For masked inputs, autocomplete, date pickers, or any special component:

```typescript
import { IMaskInput } from 'react-imask'

{
  name: 'phone',
  type: 'custom',
  label: 'Phone',
  render: (props) => (
    <IMaskInput
      id={props.id}
      mask="+{1} (000) 000-0000"
      value={String(props.value ?? '')}
      onAccept={(value) => props.onChange(value)}
      onBlur={props.onBlur}
      disabled={props.disabled}
      placeholder={props.placeholder}
      className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
    />
  ),
}
```

### Custom Field Props

```typescript
interface CustomFieldRenderProps {
  value: unknown // Current field value
  onChange: (value: unknown) => void // Update value
  onBlur: () => void // Trigger blur validation
  error?: string // Current error message
  id: string // Field ID for labels
  disabled?: boolean // Disabled state
  placeholder?: string // Placeholder text
}
```

## Prefix Input

```typescript
{
  name: 'price',
  type: 'number',
  label: 'Price',
  prefix: '$',  // Shows "$" inside the input
  required: true,
}
```

## Character Counter

```typescript
{
  name: 'description',
  type: 'textarea',
  label: 'Description',
  maxLength: 500,  // Shows "0 / 500 characters"
}
```

## External Form Control

Use `formRef` to control the form from outside:

```typescript
import { useRef } from 'react'
import { FNForm, type FNFormRef } from '@/components/ui/fn-form'

function MyForm() {
  const formRef = useRef<FNFormRef | null>(null)

  return (
    <div>
      <FNForm
        formRef={formRef}
        hideSubmitButton  // We'll use our own button
        formDefinition={formDefinition}
        onSubmit={handleSubmit}
      />

      {/* External submit button */}
      <Button onClick={() => formRef.current?.submit()}>
        Save
      </Button>

      {/* External value access */}
      <Button onClick={() => {
        const values = formRef.current?.getValues()
        console.log(values)
      }}>
        Log Values
      </Button>
    </div>
  )
}
```

### FormRef Methods

```typescript
interface FNFormRef {
  submit: () => void // Trigger form submission
  setFieldValue: (name: string, value: unknown) => void // Set a field value
  getFieldValue: (name: string) => unknown // Get a field value
  setFieldError: (name: string, error: string) => void // Set a field error
  getValues: () => Record<string, unknown> // Get all values
  isSubmitting: boolean // Submission state
}
```

## Field Change Callbacks

React to field changes and update other fields:

```typescript
<FNForm
  formDefinition={formDefinition}
  onSubmit={handleSubmit}
  onFieldChange={(name, value, setFieldValue) => {
    // When country changes, update country code
    if (name === 'country') {
      const countryCode = getCountryCode(value as string)
      setFieldValue('countryCode', countryCode)
    }

    // When "same as billing" is checked, copy address
    if (name === 'sameAsBilling' && value === true) {
      setFieldValue('shippingAddress', billingAddress)
    }
  }}
/>
```

## Custom Submit Button

```typescript
<FNForm
  formDefinition={formDefinition}
  onSubmit={handleSubmit}
  renderSubmitButton={(isSubmitting) => (
    <Button type="submit" disabled={isSubmitting} className="w-full">
      {isSubmitting ? (
        <>
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          Saving...
        </>
      ) : (
        'Save Changes'
      )}
    </Button>
  )}
/>
```

## Before Submit Content

Add content above the submit button:

```typescript
<FNForm
  formDefinition={formDefinition}
  onSubmit={handleSubmit}
  renderBeforeSubmit={(values) => (
    <div className="rounded-lg bg-muted p-4">
      <p className="text-sm text-muted-foreground">
        Total: ${calculateTotal(values)}
      </p>
    </div>
  )}
/>
```

## Complete Examples

### Address Form

```typescript
const addressForm: FormDefinition = {
  rows: [
    {
      columns: 2,
      fields: [
        {
          name: 'firstName',
          type: 'text',
          label: 'First Name',
          required: true,
        },
        { name: 'lastName', type: 'text', label: 'Last Name', required: true },
      ],
    },
    {
      fields: [
        { name: 'company', type: 'text', label: 'Company', optional: true },
      ],
    },
    {
      fields: [
        { name: 'address1', type: 'text', label: 'Address', required: true },
      ],
    },
    {
      fields: [
        {
          name: 'address2',
          type: 'text',
          label: 'Apartment, suite, etc.',
          optional: true,
        },
      ],
    },
    {
      columns: 3,
      fields: [
        { name: 'city', type: 'text', label: 'City', required: true },
        {
          name: 'province',
          type: 'text',
          label: 'State/Province',
          required: true,
        },
        { name: 'zip', type: 'text', label: 'ZIP/Postal', required: true },
      ],
    },
    {
      columns: 2,
      fields: [
        {
          name: 'country',
          type: 'select',
          label: 'Country',
          required: true,
          options: [
            { value: 'US', label: 'United States' },
            { value: 'CA', label: 'Canada' },
            { value: 'GB', label: 'United Kingdom' },
          ],
        },
        { name: 'phone', type: 'text', label: 'Phone', optional: true },
      ],
    },
  ],
}
```

### Login Form

```typescript
const loginForm: FormDefinition = {
  fields: [
    {
      name: 'email',
      type: 'email',
      label: 'Email',
      required: true,
      placeholder: 'you@example.com',
    },
    {
      name: 'password',
      type: 'password',
      label: 'Password',
      required: true,
    },
    {
      name: 'remember',
      type: 'checkbox',
      label: 'Remember me',
    },
  ],
}
```

### Product Form

```typescript
const productForm: FormDefinition = {
  rows: [
    {
      fields: [
        {
          name: 'name',
          type: 'text',
          label: 'Product Name',
          required: true,
          maxLength: 100,
        },
      ],
    },
    {
      fields: [
        {
          name: 'description',
          type: 'textarea',
          label: 'Description',
          maxLength: 500,
        },
      ],
    },
    {
      columns: 2,
      fields: [
        {
          name: 'price',
          type: 'number',
          label: 'Price',
          prefix: '$',
          required: true,
          validate: (v) =>
            Number(v) < 0 ? 'Price cannot be negative' : undefined,
        },
        {
          name: 'compareAtPrice',
          type: 'number',
          label: 'Compare at Price',
          prefix: '$',
          optional: true,
        },
      ],
    },
    {
      columns: 2,
      fields: [
        {
          name: 'status',
          type: 'select',
          label: 'Status',
          required: true,
          options: [
            { value: 'draft', label: 'Draft' },
            { value: 'active', label: 'Active' },
          ],
        },
        {
          name: 'quantity',
          type: 'number',
          label: 'Quantity',
          required: true,
        },
      ],
    },
  ],
}
```

## FNForm Props

```typescript
interface FNFormProps {
  formDefinition: FormDefinition
  onSubmit: (values: Record<string, unknown>) => void | Promise<void>
  defaultValues?: Record<string, unknown>
  submitButtonText?: string
  hideSubmitButton?: boolean
  formRef?: React.RefObject<FNFormRef | null>
  onFieldChange?: (
    name: string,
    value: unknown,
    setFieldValue: (name: string, value: unknown) => void,
  ) => void
  className?: string
  renderSubmitButton?: (isSubmitting: boolean) => React.ReactNode
  renderBeforeSubmit?: (values: Record<string, unknown>) => React.ReactNode
}
```

## See Also

- `src/components/ui/fn-form.tsx` - Component source
- `src/routes/$lang/account/addresses.tsx` - Address form example
- `src/routes/admin/login.tsx` - Login form example
- `admin-crud` skill - Forms in admin context

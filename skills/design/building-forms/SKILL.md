---
name: building-forms
description: Builds form components and data collection interfaces including contact forms, registration flows, checkout processes, surveys, and settings pages. Includes 50+ input types, validation strategies, accessibility patterns (WCAG 2.1), multi-step wizards, and UX best practices. Provides decision trees from data type to component selection, validation timing guidance, and error handling patterns. Use when creating forms, collecting user input, building surveys, implementing validation, designing multi-step workflows, or ensuring form accessibility.
---

# Form Systems & Input Patterns

Build accessible, user-friendly forms with systematic component selection, validation strategies, and UX best practices.

## Purpose

Forms are the primary mechanism for user data input in web applications. This skill provides systematic guidance for:
- Selecting appropriate input types based on data requirements
- Implementing validation strategies that enhance user experience
- Ensuring WCAG 2.1 AA accessibility compliance
- Creating complex patterns (multi-step wizards, conditional fields, dynamic forms)

## When to Use This Skill

**Triggers:**
- Building contact forms, login/registration flows, checkout processes
- Implementing surveys, questionnaires, or settings pages
- Adding validation to user inputs
- Creating multi-step workflows or wizards
- Ensuring form accessibility
- Collecting structured data (addresses, credit cards, dates)

**Common Requests:**
- "Create a registration form with validation"
- "Build a multi-step checkout flow"
- "Add inline validation to email input"
- "Make this form accessible for screen readers"
- "Implement a survey with conditional questions"

## Universal Form Concepts

### Component Selection Framework

**The Golden Rule:** Data Type → Input Component → Validation Pattern

Start by identifying the data type to collect, then select the appropriate component:

**Quick Reference:**
- **Short text** (<100 chars) → Text input, Email input, Password input
- **Long text** (>100 chars) → Textarea, Rich text editor, Code editor
- **Numeric** → Number input, Currency input, Slider
- **Date/Time** → Date picker, Time picker, Date range picker
- **Boolean** → Checkbox, Toggle switch
- **Single choice** → Radio group (2-7 options), Select dropdown (>7 options), Autocomplete (>15 options)
- **Multiple choice** → Checkbox group, Multi-select, Tag input
- **File/Media** → File upload, Image upload
- **Structured** → Address input, Credit card input, Phone number input

**For detailed decision tree:** See `references/decision-tree.md`

### Validation Timing Strategies

**Recommended Default: On Blur with Progressive Enhancement**

```
Field pristine (never touched): No validation
User typing: No errors shown
On blur (field loses focus): Validate and show errors
After first error: Switch to onChange for that field
On fix: Show success immediately
```

**Validation Modes:**
1. **On Submit** - Validate when form submitted (simple forms)
2. **On Blur** - Validate when field loses focus (RECOMMENDED for most forms)
3. **On Change** - Validate as user types (password strength, availability checks)
4. **Debounced** - Validate after user stops typing (API-based validation)
5. **Progressive** - Start with on-blur, switch to on-change after first error

**For complete validation guide:** See `references/validation-concepts.md`

### Accessibility Requirements (WCAG 2.1 AA)

**Critical Accessibility Patterns:**

**Labels and Instructions:**
- Every input must have an associated `<label>` or `aria-label`
- Labels must be visible and descriptive
- Required fields clearly indicated (not by color alone)
- Never use placeholder text as label replacement
- Provide help text for complex inputs

**Keyboard Navigation:**
- Logical, sequential tab order
- All inputs keyboard accessible
- Custom components support arrow keys
- Escape key dismisses modals/popovers
- Focus visible (outline or custom indicator)

**Error Handling:**
- Errors programmatically associated with inputs (`aria-describedby`)
- Error messages clear and actionable
- Errors announced by screen readers (`aria-live`)
- Focus moves to first error on submit
- Errors not conveyed by color alone

**ARIA Attributes:**
- `aria-required="true"` for required fields
- `aria-invalid="true"` when validation fails
- `aria-describedby` linking to help/error text
- `role="group"` for related inputs
- `aria-live="polite"` for validation messages

**For complete accessibility checklist:** See `references/accessibility-forms.md`

### UX Best Practices

**Modern Form UX Principles (2024-2025):**

1. **Progressive Disclosure** - Show only essential fields initially, reveal advanced options on demand
2. **Smart Defaults** - Pre-fill known information, suggest values based on context
3. **Inline Validation with Positive Feedback** - Show green checkmark on valid input, provide helpful error messages
4. **Mobile-First** - Large touch targets (44px minimum), appropriate keyboard types
5. **Reduce Cognitive Load** - Group related fields, use clear labels, provide examples
6. **Error Prevention** - Constraints prevent invalid input, autocomplete reduces typos
7. **Autosave and Recovery** - Save draft state automatically, warn before losing data

**For detailed UX patterns:** See `references/ux-patterns.md`

### Error Message Best Practices

**Good Error Message Formula:**
1. **What's wrong** - "Email address is not valid"
2. **Why it matters** - "We need this to send your receipt"
3. **How to fix** - "Format: name@example.com"

**Examples:**

❌ **Bad:** "Invalid input"
✅ **Good:** "Email address must include @ symbol (e.g., name@example.com)"

❌ **Bad:** "Error"
✅ **Good:** "Password must be at least 8 characters long"

❌ **Bad:** "Field required"
✅ **Good:** "Please enter your email address so we can send order confirmation"

**Tone Guidelines:**
- Conversational, not robotic
- Helpful, not blaming
- Specific, not generic
- Actionable, not just descriptive

## Language-Specific Implementations

This skill provides universal form concepts above, with language-specific implementations below.

### JavaScript/React (PRIMARY)

**Recommended Stack:**
- **React Hook Form** - Form state management (best performance, 8KB bundle)
- **Zod** - TypeScript-first schema validation
- **Radix UI** or **React Aria** - Accessible component primitives

**Quick Start:**
```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';

// Define validation schema
const schema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

type FormData = z.infer<typeof schema>;

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
    mode: 'onBlur', // Validate on blur (recommended)
  });

  const onSubmit = (data: FormData) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <label htmlFor="email">Email</label>
      <input id="email" {...register('email')} type="email" />
      {errors.email && <span role="alert">{errors.email.message}</span>}

      <label htmlFor="password">Password</label>
      <input id="password" {...register('password')} type="password" />
      {errors.password && <span role="alert">{errors.password.message}</span>}

      <button type="submit">Login</button>
    </form>
  );
}
```

**Detailed JavaScript/React Documentation:**
- `references/javascript/react-hook-form.md` - Complete React Hook Form guide
- `references/javascript/zod-validation.md` - Zod schema validation patterns
- `references/javascript/examples/` - Working code examples

### Python (PRIMARY)

**Recommended Stack:**
- **Pydantic** - Data validation and settings management (runtime validation, type-safe)
- **FastAPI** - Modern async web framework with automatic validation
- **WTForms** - Flask/Django form handling (when using traditional frameworks)

**Quick Start (FastAPI + Pydantic):**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, validator

app = FastAPI()

# Define validation schema
class LoginForm(BaseModel):
    email: EmailStr  # Validates email format
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")

    @validator('password')
    def validate_password_strength(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

@app.post("/api/login")
async def login(form_data: LoginForm):
    # Pydantic automatically validates incoming data
    # If validation fails, returns 422 with error details
    return {"message": "Login successful", "email": form_data.email}

# Example error response (automatic):
# {
#   "detail": [
#     {
#       "loc": ["body", "email"],
#       "msg": "value is not a valid email address",
#       "type": "value_error.email"
#     }
#   ]
# }
```

**Detailed Python Documentation:**
- `references/python/pydantic-forms.md` - Pydantic validation patterns
- `references/python/wtforms.md` - WTForms for Flask/Django
- `references/python/examples/` - Working code examples

### Rust (FUTURE)

**Planned Libraries:**
- **validator** - Struct field validation
- **Leptos** / **Yew** - Reactive web frameworks

*Rust implementation will be added when needed.*

### Go (FUTURE)

**Planned Libraries:**
- **Templ** - Type-safe HTML templating
- **html/template** - Standard library templating

*Go implementation will be added when needed.*

## Component Tiers

### Tier 1: Basic Input Components

**Text-Based:**
- Text field (single-line)
- Textarea (multi-line)
- Email input (with validation)
- Password input (with visibility toggle)
- Number input (with step controls)
- Tel input (with formatting)
- URL input (with protocol validation)
- Search input (with clear button)

**Selection:**
- Radio group (2-7 options)
- Checkbox (boolean or multiple)
- Toggle switch (clear on/off states)
- Select dropdown (many options)
- Multi-select (multiple selections)

**Date & Time:**
- Date picker (calendar interface)
- Time picker (hour/minute)
- Date range picker (start and end)
- DateTime picker (combined)

### Tier 2: Rich Input Components

**Advanced Selection:**
- Autocomplete/Combobox (type to filter)
- Tag input (multiple tags)
- Transfer list (move items between lists)
- Listbox (keyboard-navigable)

**Specialized:**
- Color picker (hex, RGB, HSL)
- File uploader (single, multiple, drag-drop)
- Image uploader (crop, resize, preview)
- Slider/Range (single or range)
- Rating input (stars, numeric, emoji)
- Rich text editor (formatting, media)
- Code editor (syntax highlighting)
- Markdown editor (preview, toolbar)

**Structured Data:**
- Address input (multi-field)
- Credit card input (formatted)
- Phone number (international)
- Currency input (symbol, decimal)

### Tier 3: Complex Form Patterns

**Multi-Step Forms:**
- Linear wizard (step 1 → 2 → 3)
- Branching wizard (conditional steps)
- Progress indicators
- Save and resume (draft state)
- Review and submit page

**Dynamic Forms:**
- Conditional fields (show/hide)
- Repeating sections (add/remove)
- Field arrays (dynamic list)
- Nested forms (complex objects)

**Advanced Patterns:**
- Inline editing (click to edit)
- Bulk editing (multiple records)
- Autosave (periodic or on change)
- Optimistic updates
- Undo/redo functionality

## Integration with Design Tokens

All form components use the `design-tokens` skill for visual styling, enabling theme switching (light/dark/high-contrast/custom brands).

**Key Token Categories:**
- **Color** - Input backgrounds, borders, text, error/success states
- **Spacing** - Padding, gaps between fields, label margins
- **Typography** - Font sizes, weights for inputs, labels, errors
- **Borders** - Border width, radius, focus ring
- **Shadows** - Focus indicators, elevation

**See:** `skills/design-tokens/` for complete theming documentation.

## Common Use Cases

### Contact Form
```tsx
// Basic contact form with validation
// See: references/javascript/examples/basic-form.tsx
```

### Registration Flow
```tsx
// Multi-step registration with password strength
// See: references/javascript/examples/multi-step-wizard.tsx
```

### Inline Validation
```tsx
// Real-time validation with debouncing
// See: references/javascript/examples/inline-validation.tsx
```

### Survey with Conditional Logic
```tsx
// Dynamic form with conditional fields
// See: references/javascript/examples/conditional-form.tsx
```

### Settings Page
```tsx
// Mixed input types with autosave
// See: references/javascript/examples/settings-form.tsx
```

## Quick Decision Guide

**Question: What input should I use?**
→ See `references/decision-tree.md` for complete decision tree

**Question: When should I validate?**
→ Use on-blur with progressive enhancement (on-change after first error)
→ See `references/validation-concepts.md` for all strategies

**Question: How do I make my form accessible?**
→ Use semantic HTML, label all inputs, support keyboard navigation
→ See `references/accessibility-forms.md` for WCAG 2.1 checklist

**Question: How do I handle complex validation?**
→ Use schema validation (Zod for TypeScript, Yup for JavaScript)
→ See `references/javascript/zod-validation.md` for patterns

**Question: How do I build a multi-step form?**
→ Use state management with progress tracking
→ See `references/javascript/examples/multi-step-wizard.tsx`

## Best Practices Summary

1. **Start with semantic HTML** - Use native `<input>`, `<select>`, `<textarea>` when possible
2. **Label everything** - Every input needs a visible, descriptive label
3. **Validate on blur** - Best UX balance for most forms
4. **Provide helpful errors** - Explain what's wrong and how to fix it
5. **Support keyboard navigation** - Tab order, arrow keys, escape to dismiss
6. **Mobile-first** - Large touch targets, appropriate keyboards
7. **Progressive disclosure** - Don't overwhelm with all fields at once
8. **Autosave when possible** - Prevent data loss
9. **Test with screen readers** - Ensure ARIA attributes work correctly
10. **Use design tokens** - Consistent styling, theme support

## Additional Resources

- `references/decision-tree.md` - Complete component selection framework
- `references/validation-concepts.md` - All validation strategies and patterns
- `references/accessibility-forms.md` - WCAG 2.1 AA compliance checklist
- `references/ux-patterns.md` - Modern form UX best practices
- `references/javascript/` - JavaScript/React implementation guides

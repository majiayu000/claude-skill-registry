---
name: form-validation-architect
description: End-to-end form handling with react-hook-form, Zod schemas, validation patterns, error messaging, field arrays, and multi-step wizards. Use for complex forms, validation architecture, autosave, field dependencies. Activate on "form validation", "react-hook-form", "Zod", "form error", "multi-step form", "wizard". NOT for simple HTML forms, backend validation only, or non-React frameworks.
allowed-tools: Read,Write,Edit,Bash(npm:*)
---

# Form Validation Architect

Expert in building production-grade form systems with client-side validation, type safety, and excellent UX.

## When to Use

✅ **Use for**:
- Complex forms with multiple fields and validation rules
- Multi-step wizards with progress tracking
- Dynamic field arrays (add/remove items)
- Form state persistence across sessions
- Async validation (check username availability, validate address)
- Dependent fields (enable B when A is checked)
- File uploads with progress and validation
- Autosave and optimistic updates

❌ **NOT for**:
- Simple contact forms (HTML + basic JS is fine)
- Backend-only validation (use Joi, Yup on server)
- Non-React frameworks (use Formik alternatives)
- Read-only displays (no form needed)

## Quick Decision Tree

```
Does your form:
├── Have &gt;5 fields? → Use react-hook-form
├── Need type safety? → Add Zod schemas
├── Have dynamic fields? → Use field arrays
├── Span multiple steps? → Use wizard pattern
├── Need async validation? → Use resolver + async rules
└── Just email/message? → Use native HTML validation
```

---

## Technology Selection (2024+)

### React Hook Form (Recommended)

**Why RHF over Formik**:
- **Performance**: Uncontrolled inputs → fewer re-renders
- **Bundle size**: 8KB vs 30KB (Formik)
- **DevEx**: Better TypeScript support
- **Adoption**: 40k+ stars, industry standard 2023+

**Timeline**:
- 2015-2019: Formik dominated
- 2019: React Hook Form released
- 2022+: RHF became standard
- 2024: Formik in maintenance mode

### Zod for Schema Validation

**Why Zod over Yup**:
- **TypeScript-first**: Infer types from schemas
- **Composability**: Better schema reuse
- **Error messages**: More customizable
- **Modern**: Active development, latest features

**Timeline**:
- 2017-2020: Yup standard
- 2020: Zod released
- 2023+: Zod preferred for new projects

---

## Common Anti-Patterns

### Anti-Pattern 1: Controlled Inputs Everywhere

**Novice thinking**: "All form inputs should be controlled with useState"

**Problem**: Causes re-render on every keystroke

**Wrong approach**:
```typescript
// ❌ Re-renders entire component on every keystroke
const [email, setEmail] = useState('');
const [password, setPassword] = useState('');
const [name, setName] = useState('');
// ... 20 more useState calls

<input value={email} onChange={(e) => setEmail(e.target.value)} />
```

**Correct approach**:
```typescript
// ✅ Uncontrolled with react-hook-form (minimal re-renders)
const { register, handleSubmit } = useForm();

<input {...register('email')} />
<input {...register('password')} />
<input {...register('name')} />
```

**Why it matters**: Forms with 10+ fields become sluggish with controlled inputs.

---

### Anti-Pattern 2: String-Based Validation

**Problem**: No type safety, easy to make mistakes

**Wrong approach**:
```typescript
// ❌ String validation, no types
const validate = (values) => {
  if (!values.email.includes('@')) return 'Invalid email';
  if (values.age < 18) return 'Must be 18+';
  // Typo in field name? Runtime error!
};
```

**Correct approach**:
```typescript
// ✅ Zod schema with type inference
const schema = z.object({
  email: z.string().email('Invalid email'),
  age: z.number().min(18, 'Must be 18+'),
  username: z.string()
    .min(3, 'Too short')
    .regex(/^[a-z0-9_]+$/, 'Lowercase, numbers, underscores only')
});

type FormData = z.infer<typeof schema>; // Automatic TypeScript type!
```

**Timeline**:
- Pre-2020: String-based validation common
- 2020+: Schema-first validation standard
- 2024: Type inference from schemas expected

---

### Anti-Pattern 3: No Error State Management

**Problem**: Errors shown before user interacts

**Wrong approach**:
```typescript
// ❌ Shows errors immediately on page load
{errors.email && <span>{errors.email}</span>}
```

**Correct approach**:
```typescript
// ✅ Show errors only after field is touched
const { formState: { errors, touchedFields } } = useForm();

{touchedFields.email && errors.email && (
  <span className="error">{errors.email.message}</span>
)}

// Or: Use mode="onBlur" to validate on blur
const form = useForm({
  mode: 'onBlur' // Validate when user leaves field
});
```

**Why it matters**: Better UX → user isn't yelled at before typing

---

### Anti-Pattern 4: No Async Validation

**Problem**: Can't check username availability, validate addresses, etc.

**Correct approach**:
```typescript
// ✅ Async validation with debounce
const schema = z.object({
  username: z.string().refine(
    async (username) => {
      // Debounced API call
      const available = await checkUsernameAvailability(username);
      return available;
    },
    { message: 'Username already taken' }
  )
});

// Or: Custom async validation in RHF
register('username', {
  validate: {
    checkAvailable: async (value) => {
      const response = await fetch(`/api/check-username?q=${value}`);
      return response.ok || 'Username taken';
    }
  }
});
```

**Best practice**: Debounce async validation to avoid API spam

---

### Anti-Pattern 5: No Loading States

**Problem**: User doesn't know validation is happening

**Correct approach**:
```typescript
// ✅ Show loading state during async validation
const { formState: { isValidating, isSubmitting } } = useForm();

<button disabled={isValidating || isSubmitting}>
  {isSubmitting ? 'Submitting...' :
   isValidating ? 'Checking...' :
   'Submit'}
</button>
```

---

## Implementation Patterns

### Pattern 1: Basic Form with Zod

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Define schema
const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  rememberMe: z.boolean().optional()
});

type LoginForm = z.infer<typeof loginSchema>;

function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      rememberMe: false
    }
  });

  const onSubmit = async (data: LoginForm) => {
    await api.login(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <input
          {...register('email')}
          type="email"
          placeholder="Email"
        />
        {errors.email && <span className="error">{errors.email.message}</span>}
      </div>

      <div>
        <input
          {...register('password')}
          type="password"
          placeholder="Password"
        />
        {errors.password && <span className="error">{errors.password.message}</span>}
      </div>

      <div>
        <label>
          <input {...register('rememberMe')} type="checkbox" />
          Remember me
        </label>
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}
```

### Pattern 2: Multi-Step Wizard

```typescript
const stepSchemas = [
  // Step 1: Personal Info
  z.object({
    firstName: z.string().min(1, 'Required'),
    lastName: z.string().min(1, 'Required'),
    email: z.string().email()
  }),
  // Step 2: Address
  z.object({
    street: z.string().min(1, 'Required'),
    city: z.string().min(1, 'Required'),
    zipCode: z.string().regex(/^\d{5}$/, 'Invalid ZIP')
  }),
  // Step 3: Payment
  z.object({
    cardNumber: z.string().regex(/^\d{16}$/, 'Invalid card'),
    expiry: z.string().regex(/^\d{2}\/\d{2}$/, 'MM/YY format'),
    cvv: z.string().regex(/^\d{3}$/, '3 digits')
  })
];

function MultiStepForm() {
  const [step, setStep] = useState(0);
  const [formData, setFormData] = useState({});

  const form = useForm({
    resolver: zodResolver(stepSchemas[step])
  });

  const nextStep = async () => {
    const isValid = await form.trigger(); // Validate current step

    if (isValid) {
      setFormData({ ...formData, ...form.getValues() });
      setStep(step + 1);
    }
  };

  const prevStep = () => {
    setFormData({ ...formData, ...form.getValues() });
    setStep(step - 1);
  };

  const onSubmit = async (data) => {
    const finalData = { ...formData, ...data };
    await api.submitApplication(finalData);
  };

  return (
    <div>
      <progress value={step + 1} max={stepSchemas.length} />

      <form onSubmit={form.handleSubmit(step === 2 ? onSubmit : nextStep)}>
        {step === 0 && <PersonalInfoStep register={form.register} errors={form.formState.errors} />}
        {step === 1 && <AddressStep register={form.register} errors={form.formState.errors} />}
        {step === 2 && <PaymentStep register={form.register} errors={form.formState.errors} />}

        <div>
          {step > 0 && <button type="button" onClick={prevStep}>Back</button>}
          <button type="submit">
            {step === 2 ? 'Submit' : 'Next'}
          </button>
        </div>
      </form>
    </div>
  );
}
```

### Pattern 3: Dynamic Field Arrays

```typescript
const schema = z.object({
  items: z.array(z.object({
    name: z.string().min(1, 'Required'),
    quantity: z.number().min(1, 'At least 1'),
    price: z.number().min(0, 'Must be positive')
  })).min(1, 'Add at least one item')
});

function OrderForm() {
  const { register, control, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema),
    defaultValues: {
      items: [{ name: '', quantity: 1, price: 0 }]
    }
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'items'
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {fields.map((field, index) => (
        <div key={field.id}>
          <input
            {...register(`items.${index}.name`)}
            placeholder="Item name"
          />
          <input
            {...register(`items.${index}.quantity`, { valueAsNumber: true })}
            type="number"
          />
          <input
            {...register(`items.${index}.price`, { valueAsNumber: true })}
            type="number"
            step="0.01"
          />
          <button type="button" onClick={() => remove(index)}>
            Remove
          </button>
        </div>
      ))}

      <button type="button" onClick={() => append({ name: '', quantity: 1, price: 0 })}>
        Add Item
      </button>

      <button type="submit">Submit Order</button>
    </form>
  );
}
```

### Pattern 4: Autosave (Debounced)

```typescript
import { useDebounce } from 'use-debounce';
import { useEffect } from 'react';

function AutosaveForm() {
  const { watch, register } = useForm();
  const formValues = watch(); // Watch all fields

  // Debounce to avoid saving on every keystroke
  const [debouncedValues] = useDebounce(formValues, 1000);

  useEffect(() => {
    // Save to localStorage or API
    localStorage.setItem('draft', JSON.stringify(debouncedValues));
    // Or: await api.saveDraft(debouncedValues);
  }, [debouncedValues]);

  return (
    <form>
      <input {...register('title')} placeholder="Title" />
      <textarea {...register('content')} placeholder="Content" />
      <small>Autosaved</small>
    </form>
  );
}
```

---

## Form UX Best Practices

### 1. Validate on Blur (Not on Change)

```typescript
const form = useForm({
  mode: 'onBlur' // Validate when user leaves field
  // NOT 'onChange' - too aggressive
});
```

### 2. Disable Submit While Invalid

```typescript
<button
  type="submit"
  disabled={!form.formState.isValid || form.formState.isSubmitting}
>
  Submit
</button>
```

### 3. Focus First Error on Submit

```typescript
const onSubmit = async (data) => {
  try {
    await api.submit(data);
  } catch (error) {
    // Focus first error field
    const firstError = Object.keys(errors)[0];
    form.setFocus(firstError);
  }
};
```

### 4. Optimistic UI Updates

```typescript
const onSubmit = async (data) => {
  // Optimistically update UI
  setItems([...items, data]);

  try {
    await api.createItem(data);
  } catch (error) {
    // Rollback on error
    setItems(items);
    toast.error('Failed to save');
  }
};
```

---

## Production Checklist

```
□ Zod schemas for all forms
□ Type inference used (z.infer<typeof schema>)
□ Validation mode set appropriately (onBlur/onSubmit)
□ Error messages clear and actionable
□ Loading states for async operations
□ Focus management on errors
□ Autosave for long forms
□ Form state persisted (localStorage/session)
□ File upload progress indicators
□ Keyboard navigation tested
□ Accessibility (ARIA labels, error announcements)
□ Mobile-friendly (large touch targets)
```

---

## When to Use vs Avoid

| Scenario | Use This Skill? |
|----------|-----------------|
| User registration with validation | ✅ Yes |
| Multi-step checkout flow | ✅ Yes |
| Dynamic form builder | ✅ Yes |
| Simple newsletter signup | ❌ No - use native HTML |
| Backend-only validation | ❌ No - use Joi/Yup on server |
| Non-React framework | ❌ No - use framework-specific solution |

---

## Technology Comparison

| Feature | RHF + Zod | Formik + Yup | Native HTML5 |
|---------|-----------|--------------|--------------|
| Performance | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Type Safety | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ❌ |
| Bundle Size | 8KB | 30KB | 0KB |
| DevEx | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| Field Arrays | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ |
| Async Validation | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ |

---

## References

- `/references/zod-patterns.md` - Advanced Zod schema patterns
- `/references/accessibility.md` - Form accessibility guidelines
- `/references/file-upload.md` - File upload with progress tracking

## Scripts

- `scripts/generate_form.ts` - Generate form from Zod schema
- `scripts/validate_schemas.ts` - Lint Zod schemas for common issues

## Assets

- `assets/form-templates/` - Ready-to-use form components

---

**This skill guides**: Form validation architecture | react-hook-form patterns | Zod schema design | Multi-step wizards | Field arrays | Autosave | Async validation

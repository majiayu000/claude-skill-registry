---
name: form-design
description: Build accessible, user-friendly forms with validation. Covers react-hook-form, Zod schemas, error handling UX, multi-step forms, input patterns, and form accessibility. Use for registration forms, checkout flows, data entry, and user input.
---

# Form Design & Validation

Create accessible, validated forms with excellent user experience.

## Instructions

1. **Use proper labels** - Every input needs an associated label
2. **Validate on blur and submit** - Immediate feedback without being intrusive
3. **Show clear error messages** - Specific, actionable guidance
4. **Group related fields** - Use fieldsets for logical groupings
5. **Support keyboard navigation** - Tab order, Enter to submit

## React Hook Form + Zod (Recommended Stack)

### Setup

```bash
npm install react-hook-form zod @hookform/resolvers
```

### Basic Form

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// 1. Define schema
const signupSchema = z.object({
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Please enter a valid email'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain an uppercase letter')
    .regex(/[0-9]/, 'Password must contain a number'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

type SignupForm = z.infer<typeof signupSchema>;

// 2. Create form
function SignupForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<SignupForm>({
    resolver: zodResolver(signupSchema),
  });

  const onSubmit = async (data: SignupForm) => {
    try {
      await api.signup(data);
      // Handle success
    } catch (error) {
      // Handle error
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      <FormField
        label="Email"
        type="email"
        error={errors.email?.message}
        {...register('email')}
      />

      <FormField
        label="Password"
        type="password"
        error={errors.password?.message}
        {...register('password')}
      />

      <FormField
        label="Confirm Password"
        type="password"
        error={errors.confirmPassword?.message}
        {...register('confirmPassword')}
      />

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Creating account...' : 'Sign Up'}
      </button>
    </form>
  );
}
```

### Reusable Form Field Component

```tsx
import { forwardRef } from 'react';

interface FormFieldProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  hint?: string;
}

export const FormField = forwardRef<HTMLInputElement, FormFieldProps>(
  ({ label, error, hint, id, type = 'text', ...props }, ref) => {
    const inputId = id || label.toLowerCase().replace(/\s+/g, '-');
    const errorId = `${inputId}-error`;
    const hintId = `${inputId}-hint`;

    return (
      <div className="space-y-1.5">
        <label
          htmlFor={inputId}
          className="block text-sm font-medium text-gray-700 dark:text-gray-300"
        >
          {label}
          {props.required && <span className="text-red-500 ml-1">*</span>}
        </label>

        <input
          ref={ref}
          id={inputId}
          type={type}
          className={`
            w-full px-3 py-2 rounded-lg border transition-colors
            ${error
              ? 'border-red-500 focus:ring-red-500 focus:border-red-500'
              : 'border-gray-300 dark:border-gray-600 focus:ring-blue-500 focus:border-blue-500'
            }
            bg-white dark:bg-gray-800
            text-gray-900 dark:text-gray-100
            placeholder-gray-400
            focus:outline-none focus:ring-2
            disabled:bg-gray-100 disabled:cursor-not-allowed
          `}
          aria-invalid={!!error}
          aria-describedby={
            error ? errorId : hint ? hintId : undefined
          }
          {...props}
        />

        {hint && !error && (
          <p id={hintId} className="text-sm text-gray-500">
            {hint}
          </p>
        )}

        {error && (
          <p id={errorId} className="text-sm text-red-600 flex items-center gap-1" role="alert">
            <ExclamationCircleIcon className="w-4 h-4" />
            {error}
          </p>
        )}
      </div>
    );
  }
);
```

## Common Form Patterns

### Select/Dropdown

```tsx
interface SelectFieldProps {
  label: string;
  options: { value: string; label: string }[];
  error?: string;
  placeholder?: string;
}

export const SelectField = forwardRef<HTMLSelectElement, SelectFieldProps>(
  ({ label, options, error, placeholder, ...props }, ref) => {
    const id = label.toLowerCase().replace(/\s+/g, '-');

    return (
      <div className="space-y-1.5">
        <label htmlFor={id} className="block text-sm font-medium text-gray-700">
          {label}
        </label>
        <select
          ref={ref}
          id={id}
          className={`
            w-full px-3 py-2 rounded-lg border
            ${error ? 'border-red-500' : 'border-gray-300'}
            bg-white focus:ring-2 focus:ring-blue-500
          `}
          aria-invalid={!!error}
          {...props}
        >
          {placeholder && (
            <option value="" disabled>
              {placeholder}
            </option>
          )}
          {options.map(opt => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
        {error && <p className="text-sm text-red-600">{error}</p>}
      </div>
    );
  }
);
```

### Checkbox Group

```tsx
interface CheckboxGroupProps {
  label: string;
  options: { value: string; label: string }[];
  value: string[];
  onChange: (value: string[]) => void;
  error?: string;
}

function CheckboxGroup({ label, options, value, onChange, error }: CheckboxGroupProps) {
  const handleChange = (optionValue: string, checked: boolean) => {
    if (checked) {
      onChange([...value, optionValue]);
    } else {
      onChange(value.filter(v => v !== optionValue));
    }
  };

  return (
    <fieldset>
      <legend className="text-sm font-medium text-gray-700 mb-2">{label}</legend>
      <div className="space-y-2">
        {options.map(opt => (
          <label key={opt.value} className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={value.includes(opt.value)}
              onChange={(e) => handleChange(opt.value, e.target.checked)}
              className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span className="text-gray-700">{opt.label}</span>
          </label>
        ))}
      </div>
      {error && <p className="text-sm text-red-600 mt-1">{error}</p>}
    </fieldset>
  );
}
```

### Radio Group

```tsx
interface RadioGroupProps {
  label: string;
  options: { value: string; label: string; description?: string }[];
  value: string;
  onChange: (value: string) => void;
  error?: string;
}

function RadioGroup({ label, options, value, onChange, error }: RadioGroupProps) {
  return (
    <fieldset>
      <legend className="text-sm font-medium text-gray-700 mb-3">{label}</legend>
      <div className="space-y-3">
        {options.map(opt => (
          <label
            key={opt.value}
            className={`
              flex items-start gap-3 p-4 rounded-lg border cursor-pointer
              ${value === opt.value
                ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-500'
                : 'border-gray-200 hover:border-gray-300'
              }
            `}
          >
            <input
              type="radio"
              name={label}
              value={opt.value}
              checked={value === opt.value}
              onChange={() => onChange(opt.value)}
              className="mt-0.5 w-4 h-4 text-blue-600 focus:ring-blue-500"
            />
            <div>
              <span className="font-medium text-gray-900">{opt.label}</span>
              {opt.description && (
                <p className="text-sm text-gray-500">{opt.description}</p>
              )}
            </div>
          </label>
        ))}
      </div>
      {error && <p className="text-sm text-red-600 mt-2">{error}</p>}
    </fieldset>
  );
}
```

## Multi-Step Form

```tsx
import { useState } from 'react';
import { useForm, FormProvider } from 'react-hook-form';

const steps = [
  { id: 'account', title: 'Account', component: AccountStep },
  { id: 'profile', title: 'Profile', component: ProfileStep },
  { id: 'preferences', title: 'Preferences', component: PreferencesStep },
];

function MultiStepForm() {
  const [currentStep, setCurrentStep] = useState(0);
  const methods = useForm({ mode: 'onChange' });

  const CurrentStepComponent = steps[currentStep].component;
  const isLastStep = currentStep === steps.length - 1;

  const next = async () => {
    const isValid = await methods.trigger(); // Validate current step
    if (isValid && !isLastStep) {
      setCurrentStep(prev => prev + 1);
    }
  };

  const back = () => {
    if (currentStep > 0) {
      setCurrentStep(prev => prev - 1);
    }
  };

  const onSubmit = async (data: FormData) => {
    await api.submit(data);
  };

  return (
    <FormProvider {...methods}>
      <form onSubmit={methods.handleSubmit(onSubmit)}>
        {/* Progress indicator */}
        <nav aria-label="Progress" className="mb-8">
          <ol className="flex items-center">
            {steps.map((step, index) => (
              <li key={step.id} className="flex items-center">
                <span className={`
                  w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium
                  ${index < currentStep
                    ? 'bg-blue-600 text-white'
                    : index === currentStep
                    ? 'border-2 border-blue-600 text-blue-600'
                    : 'border-2 border-gray-300 text-gray-500'
                  }
                `}>
                  {index < currentStep ? '✓' : index + 1}
                </span>
                <span className="ml-2 text-sm font-medium text-gray-900">
                  {step.title}
                </span>
                {index < steps.length - 1 && (
                  <div className="w-12 h-0.5 mx-4 bg-gray-200" />
                )}
              </li>
            ))}
          </ol>
        </nav>

        {/* Current step */}
        <CurrentStepComponent />

        {/* Navigation */}
        <div className="flex justify-between mt-8">
          <button
            type="button"
            onClick={back}
            disabled={currentStep === 0}
            className="px-4 py-2 border rounded-lg disabled:opacity-50"
          >
            Back
          </button>

          {isLastStep ? (
            <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-lg">
              Submit
            </button>
          ) : (
            <button type="button" onClick={next} className="px-4 py-2 bg-blue-600 text-white rounded-lg">
              Continue
            </button>
          )}
        </div>
      </form>
    </FormProvider>
  );
}
```

## Error Handling Patterns

### Inline Errors

```tsx
// Show error immediately below field
{error && (
  <p className="text-sm text-red-600 mt-1 flex items-center gap-1">
    <ExclamationCircleIcon className="w-4 h-4 flex-shrink-0" />
    {error}
  </p>
)}
```

### Error Summary

```tsx
// Show all errors at top of form
function ErrorSummary({ errors }: { errors: Record<string, { message?: string }> }) {
  const errorList = Object.entries(errors).filter(([_, v]) => v.message);

  if (errorList.length === 0) return null;

  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6" role="alert">
      <h3 className="text-red-800 font-medium mb-2">
        Please fix the following errors:
      </h3>
      <ul className="list-disc list-inside text-sm text-red-700 space-y-1">
        {errorList.map(([field, error]) => (
          <li key={field}>
            <a href={`#${field}`} className="underline">
              {error.message}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## Accessibility Checklist

- [ ] Every input has a `<label>` with `htmlFor`
- [ ] Required fields are marked (and announced)
- [ ] Error messages are linked with `aria-describedby`
- [ ] Invalid fields have `aria-invalid="true"`
- [ ] Error messages use `role="alert"` for screen readers
- [ ] Focus moves to first error on submit
- [ ] Tab order is logical
- [ ] Submit with Enter key works

## Best Practices

1. **Don't disable submit** - Show errors instead
2. **Validate on blur** - Immediate but not intrusive
3. **Pre-fill when possible** - Reduce user effort
4. **Show password requirements** - Before they fail
5. **Confirm destructive actions** - Double-check deletes
6. **Save progress** - For long forms, use localStorage

## When to Use

- User registration and login forms
- Checkout and payment flows
- Settings and profile forms
- Data entry applications
- Contact and feedback forms

## Notes

- react-hook-form is the most performant React form library
- Zod provides runtime validation + TypeScript types
- Test forms with screen readers and keyboard-only
- Consider form analytics to find drop-off points

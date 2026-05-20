---
name: web-forms-react-hook-form
description: React Hook Form patterns - useForm, Controller, useFieldArray, validation resolver, performance optimization
---

# React Hook Form Patterns

> **Quick Guide:** Use React Hook Form for performant, type-safe form handling. Use `register` for native inputs, `Controller` for controlled components, `useFieldArray` for dynamic fields, and resolver pattern for schema validation.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST provide generic types to `useForm<FormData>()` for type-safe form handling)**

**(You MUST use `field.id` as key prop in useFieldArray - NEVER use array index)**

**(You MUST use Controller for controlled components like selects, date pickers, and custom inputs)**

**(You MUST use resolver pattern for schema validation - defer schema creation to validation skill)**

**(You MUST set `mode: "onBlur"` or `mode: "onTouched"` for optimal UX - avoid `mode: "onChange"` unless needed)**

</critical_requirements>

---

**Auto-detection:** React Hook Form, useForm, register, handleSubmit, formState, Controller, useFieldArray, useWatch, useFormContext, resolver, zodResolver

**When to use:**

- Building forms with validation requirements
- Managing complex form state with many fields
- Creating dynamic forms with add/remove fields
- Integrating with controlled component libraries
- Handling multi-step or wizard forms

**Key patterns covered:**

- useForm hook with TypeScript generics
- register vs Controller patterns
- useFieldArray for dynamic fields
- Validation with resolver pattern
- Error handling and display
- Performance optimization
- Form reset and default values

**When NOT to use:**

- Single input without validation (use useState)
- Server-only forms with server actions (use native form + action)
- Read-only data display (not a form scenario)

**Detailed Resources:**

- For code examples, see [examples/](examples/) folder:
  - [core.md](examples/core.md) - Basic form patterns
  - [controlled-components.md](examples/controlled-components.md) - Controller pattern
  - [validation.md](examples/validation.md) - Zod resolver integration
  - [arrays.md](examples/arrays.md) - useFieldArray for dynamic forms
  - [performance.md](examples/performance.md) - Performance optimization
  - [wizard.md](examples/wizard.md) - Multi-step wizard forms
  - [v7-advanced.md](examples/v7-advanced.md) - v7.46+ features (values prop, Form component, FormStateSubscribe)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

React Hook Form prioritizes performance through uncontrolled inputs and subscription-based updates. Only fields that change re-render, not the entire form. The library isolates form state from component state, minimizing re-renders and keeping forms responsive even with many fields.

**Core Principles:**

1. **Uncontrolled by default** - Use `register` for native inputs to avoid re-renders
2. **Controlled when needed** - Use `Controller` for UI library components
3. **Schema validation** - Separate validation logic from form logic using resolvers
4. **Subscription-based** - Subscribe to only the form state you need
5. **Type safety** - Always provide TypeScript generics for form data

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Basic useForm with TypeScript

Define form data types and pass them as generics to `useForm` for full type safety.

```typescript
import { useForm } from "react-hook-form";
import type { SubmitHandler } from "react-hook-form";

// Define form data interface
interface ContactFormData {
  name: string;
  email: string;
  message: string;
}

export function ContactForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<ContactFormData>({
    mode: "onBlur", // Validate on blur for optimal UX
    defaultValues: {
      name: "",
      email: "",
      message: "",
    },
  });

  const onSubmit: SubmitHandler<ContactFormData> = async (data) => {
    // data is fully typed as ContactFormData
    await submitForm(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("name", { required: "Name is required" })} />
      {errors.name && <span>{errors.name.message}</span>}

      <input {...register("email", { required: "Email is required" })} />
      {errors.email && <span>{errors.email.message}</span>}

      <textarea {...register("message")} />

      <button type="submit" disabled={isSubmitting}>
        Submit
      </button>
    </form>
  );
}
```

**Why good:** TypeScript generics provide autocomplete and type checking for field names, mode: "onBlur" validates only when user leaves field reducing noise, defaultValues initializes form state preventing undefined values, SubmitHandler type ensures onSubmit receives correctly typed data

---

### Pattern 2: Controller for Controlled Components

Use `Controller` when working with UI library components (selects, date pickers, etc.) that don't expose a ref.

```typescript
import { useForm, Controller } from "react-hook-form";
import type { SubmitHandler } from "react-hook-form";
// Your UI components (styling handled by your styling skill)
import { Select, DatePicker } from "./ui";

interface BookingFormData {
  service: string;
  date: Date | null;
  notes: string;
}

export function BookingForm() {
  const { control, register, handleSubmit, formState: { errors } } = useForm<BookingFormData>({
    mode: "onBlur",
    defaultValues: {
      service: "",
      date: null,
      notes: "",
    },
  });

  const onSubmit: SubmitHandler<BookingFormData> = async (data) => {
    await createBooking(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Controller for controlled components */}
      <Controller
        name="service"
        control={control}
        rules={{ required: "Service is required" }}
        render={({ field, fieldState: { error } }) => (
          <>
            <Select
              {...field}
              options={serviceOptions}
              placeholder="Select a service"
            />
            {error && <span>{error.message}</span>}
          </>
        )}
      />

      <Controller
        name="date"
        control={control}
        rules={{ required: "Date is required" }}
        render={({ field, fieldState: { error } }) => (
          <>
            <DatePicker
              selected={field.value}
              onChange={field.onChange}
              onBlur={field.onBlur}
            />
            {error && <span>{error.message}</span>}
          </>
        )}
      />

      {/* register for native inputs */}
      <textarea {...register("notes")} />

      <button type="submit">Book</button>
    </form>
  );
}
```

**Why good:** Controller wraps controlled components without breaking RHF optimization, render prop provides field props (value, onChange, onBlur) and fieldState for errors, mixing register and Controller in same form works seamlessly

---

### Pattern 3: useFieldArray for Dynamic Fields

Use `useFieldArray` for forms with repeatable field groups. Always use `field.id` as the key.

```typescript
import { useForm, useFieldArray } from "react-hook-form";
import type { SubmitHandler } from "react-hook-form";

interface OrderItem {
  productId: string;
  quantity: number;
}

interface OrderFormData {
  customerName: string;
  items: OrderItem[];
}

const MIN_QUANTITY = 1;
const DEFAULT_QUANTITY = 1;

export function OrderForm() {
  const {
    control,
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<OrderFormData>({
    mode: "onBlur",
    defaultValues: {
      customerName: "",
      items: [{ productId: "", quantity: DEFAULT_QUANTITY }],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: "items",
  });

  const onSubmit: SubmitHandler<OrderFormData> = async (data) => {
    await createOrder(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("customerName", { required: "Name is required" })} />

      {fields.map((field, index) => (
        // CRITICAL: Use field.id as key, NEVER use index
        <div key={field.id}>
          <input
            {...register(`items.${index}.productId`, { required: "Product required" })}
            placeholder="Product ID"
          />
          <input
            type="number"
            {...register(`items.${index}.quantity`, {
              valueAsNumber: true,
              min: { value: MIN_QUANTITY, message: `Min quantity is ${MIN_QUANTITY}` },
            })}
          />
          <button type="button" onClick={() => remove(index)}>
            Remove
          </button>
        </div>
      ))}

      <button
        type="button"
        onClick={() => append({ productId: "", quantity: DEFAULT_QUANTITY })}
      >
        Add Item
      </button>

      <button type="submit">Submit Order</button>
    </form>
  );
}
```

**Why good:** field.id ensures React can track items correctly during add/remove operations, valueAsNumber converts string input to number automatically, named constants for MIN_QUANTITY and DEFAULT_QUANTITY prevent magic numbers

---

### Pattern 4: Resolver Pattern for Schema Validation

Use resolvers to integrate external validation libraries. Define schemas in your validation skill, use them here.

```typescript
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import type { SubmitHandler } from "react-hook-form";
import type { z } from "zod";
// Schema defined in validation skill - import from your validation module
import { userProfileSchema } from "./schemas/user-profile";

// Infer type from schema
type UserProfileFormData = z.infer<typeof userProfileSchema>;

export function UserProfileForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isValid, isDirty },
  } = useForm<UserProfileFormData>({
    resolver: zodResolver(userProfileSchema),
    mode: "onBlur",
    defaultValues: {
      username: "",
      email: "",
      bio: "",
    },
  });

  const onSubmit: SubmitHandler<UserProfileFormData> = async (data) => {
    // data is validated and typed
    await updateProfile(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("username")} />
      {errors.username && <span>{errors.username.message}</span>}

      <input {...register("email")} />
      {errors.email && <span>{errors.email.message}</span>}

      <textarea {...register("bio")} />
      {errors.bio && <span>{errors.bio.message}</span>}

      <button type="submit" disabled={!isDirty || !isValid}>
        Save Profile
      </button>
    </form>
  );
}
```

**Why good:** resolver separates validation logic from form logic, z.infer automatically generates TypeScript types from schema, isDirty and isValid enable smart submit button state, schema is reusable across forms and testable independently

**Note:** Schema creation patterns are covered in the Zod validation skill. This skill focuses on how to integrate schemas with React Hook Form.

---

### Pattern 5: useWatch for Reactive Fields

Use `useWatch` to subscribe to specific field values without re-rendering the entire form.

```typescript
import { useForm, useWatch } from "react-hook-form";
import type { SubmitHandler } from "react-hook-form";

interface PricingFormData {
  plan: "basic" | "pro" | "enterprise";
  seats: number;
  billingCycle: "monthly" | "annual";
}

const PLAN_PRICES = {
  basic: 10,
  pro: 25,
  enterprise: 50,
} as const;

const ANNUAL_DISCOUNT = 0.2;

export function PricingForm() {
  const { control, register, handleSubmit } = useForm<PricingFormData>({
    mode: "onBlur",
    defaultValues: {
      plan: "basic",
      seats: 1,
      billingCycle: "monthly",
    },
  });

  // Subscribe to specific fields for price calculation
  const [plan, seats, billingCycle] = useWatch({
    control,
    name: ["plan", "seats", "billingCycle"],
  });

  const calculatePrice = () => {
    const basePrice = PLAN_PRICES[plan] * seats;
    return billingCycle === "annual"
      ? basePrice * 12 * (1 - ANNUAL_DISCOUNT)
      : basePrice;
  };

  const onSubmit: SubmitHandler<PricingFormData> = async (data) => {
    await createSubscription(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <select {...register("plan")}>
        <option value="basic">Basic</option>
        <option value="pro">Pro</option>
        <option value="enterprise">Enterprise</option>
      </select>

      <input type="number" {...register("seats", { valueAsNumber: true })} />

      <select {...register("billingCycle")}>
        <option value="monthly">Monthly</option>
        <option value="annual">Annual (20% off)</option>
      </select>

      {/* Price display updates when watched fields change */}
      <div>Total: ${calculatePrice()}</div>

      <button type="submit">Subscribe</button>
    </form>
  );
}
```

**Why good:** useWatch subscribes to only specified fields minimizing re-renders, named constants for PLAN_PRICES and ANNUAL_DISCOUNT improve maintainability, price calculation is derived from form state without separate useState

---

### Pattern 6: useFormContext for Nested Components

Use `FormProvider` and `useFormContext` to access form methods in nested components without prop drilling.

```typescript
import { useForm, FormProvider, useFormContext } from "react-hook-form";
import type { SubmitHandler } from "react-hook-form";

interface CheckoutFormData {
  email: string;
  shippingAddress: {
    street: string;
    city: string;
    zip: string;
  };
  billingAddress: {
    street: string;
    city: string;
    zip: string;
  };
}

// Parent form component
export function CheckoutForm() {
  const methods = useForm<CheckoutFormData>({
    mode: "onBlur",
    defaultValues: {
      email: "",
      shippingAddress: { street: "", city: "", zip: "" },
      billingAddress: { street: "", city: "", zip: "" },
    },
  });

  const onSubmit: SubmitHandler<CheckoutFormData> = async (data) => {
    await processCheckout(data);
  };

  return (
    <FormProvider {...methods}>
      <form onSubmit={methods.handleSubmit(onSubmit)}>
        <input {...methods.register("email")} placeholder="Email" />

        <AddressFields prefix="shippingAddress" title="Shipping Address" />
        <AddressFields prefix="billingAddress" title="Billing Address" />

        <button type="submit">Complete Checkout</button>
      </form>
    </FormProvider>
  );
}

// Nested component using useFormContext
interface AddressFieldsProps {
  prefix: "shippingAddress" | "billingAddress";
  title: string;
}

function AddressFields({ prefix, title }: AddressFieldsProps) {
  const { register, formState: { errors } } = useFormContext<CheckoutFormData>();

  return (
    <fieldset>
      <legend>{title}</legend>
      <input
        {...register(`${prefix}.street`)}
        placeholder="Street"
      />
      {errors[prefix]?.street && <span>{errors[prefix]?.street?.message}</span>}

      <input
        {...register(`${prefix}.city`)}
        placeholder="City"
      />

      <input
        {...register(`${prefix}.zip`)}
        placeholder="ZIP Code"
      />
    </fieldset>
  );
}
```

**Why good:** FormProvider eliminates prop drilling in complex forms, useFormContext gives nested components access to all form methods, prefix pattern enables reusable address components, TypeScript ensures type safety in nested paths

---

### Pattern 7: Form Reset and Default Values

Handle form reset properly, especially when loading async data.

**Note:** For reactive async data, consider using the `values` prop instead of manual reset. See [v7-advanced.md](examples/v7-advanced.md) Pattern 1 for the modern approach.

```typescript
import { useForm } from "react-hook-form";
import { useEffect } from "react";
import type { SubmitHandler } from "react-hook-form";

interface UserSettingsFormData {
  displayName: string;
  email: string;
  notifications: boolean;
}

interface UserSettingsFormProps {
  userId: string;
}

export function UserSettingsForm({ userId }: UserSettingsFormProps) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isDirty, isSubmitting },
  } = useForm<UserSettingsFormData>({
    mode: "onBlur",
    defaultValues: {
      displayName: "",
      email: "",
      notifications: true,
    },
  });

  // Load user data and reset form
  useEffect(() => {
    const loadUserSettings = async () => {
      const settings = await fetchUserSettings(userId);
      // Reset form with fetched data
      reset({
        displayName: settings.displayName,
        email: settings.email,
        notifications: settings.notifications,
      });
    };
    loadUserSettings();
  }, [userId, reset]);

  const onSubmit: SubmitHandler<UserSettingsFormData> = async (data) => {
    await updateUserSettings(userId, data);
    // Reset form state but keep values (clears isDirty)
    reset(data);
  };

  const handleCancel = () => {
    // Reset to last saved values
    reset();
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("displayName", { required: "Required" })} />
      {errors.displayName && <span>{errors.displayName.message}</span>}

      <input {...register("email", { required: "Required" })} />
      {errors.email && <span>{errors.email.message}</span>}

      <label>
        <input type="checkbox" {...register("notifications")} />
        Email notifications
      </label>

      <div>
        <button type="button" onClick={handleCancel} disabled={!isDirty}>
          Cancel
        </button>
        <button type="submit" disabled={!isDirty || isSubmitting}>
          Save
        </button>
      </div>
    </form>
  );
}
```

**Why good:** reset() with data updates both values and defaultValues for proper isDirty tracking, useEffect loads async data and resets form once data arrives, reset() without args reverts to defaultValues enabling cancel functionality, isDirty enables smart button states

---

### Pattern 8: Error Display Component

Create a reusable error display component using `useFormState` for optimized re-renders.

```typescript
import { useFormState } from "react-hook-form";
import type { Control, FieldPath, FieldValues } from "react-hook-form";

interface FieldErrorProps<T extends FieldValues> {
  control: Control<T>;
  name: FieldPath<T>;
  className?: string;
}

export function FieldError<T extends FieldValues>({
  control,
  name,
  className,
}: FieldErrorProps<T>) {
  // Subscribe only to errors for this specific field
  const { errors } = useFormState({ control, name });

  const error = errors[name];
  if (!error) return null;

  return (
    <span role="alert" className={className}>
      {error.message as string}
    </span>
  );
}

// Usage
interface LoginFormData {
  email: string;
  password: string;
}

function LoginForm() {
  const { control, register, handleSubmit } = useForm<LoginFormData>({
    mode: "onBlur",
  });

  const onSubmit: SubmitHandler<LoginFormData> = async (data) => {
    await login(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("email")} />
      {/* Only this component re-renders when email error changes */}
      <FieldError control={control} name="email" />

      <input {...register("password")} type="password" />
      <FieldError control={control} name="password" />

      <button type="submit">Log In</button>
    </form>
  );
}
```

**Why good:** useFormState with name prop subscribes only to that field's errors, role="alert" ensures screen readers announce error, generic types make component reusable across forms, className prop allows styling customization

</patterns>

---

<integration>

## Integration Guide

**React Hook Form is validation-library agnostic.** Use the resolver pattern to integrate with any validation library.

**Works with:**

- **Validation libraries** (via resolvers): Zod, Yup, Joi, Vest, ArkType, Valibot
- **UI component libraries**: Material UI, Ant Design, Chakra UI (use Controller)
- **Native HTML inputs**: Use register directly
- Any React component library via Controller

**Form validation approach:**

- Schema validation is handled by your validation skill (Zod, Yup, etc.)
- This skill covers how to wire schemas to forms via resolver
- Keep validation logic separate from form logic

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST provide generic types to `useForm<FormData>()` for type-safe form handling)**

**(You MUST use `field.id` as key prop in useFieldArray - NEVER use array index)**

**(You MUST use Controller for controlled components like selects, date pickers, and custom inputs)**

**(You MUST use resolver pattern for schema validation - defer schema creation to validation skill)**

**(You MUST set `mode: "onBlur"` or `mode: "onTouched"` for optimal UX - avoid `mode: "onChange"` unless needed)**

**Failure to follow these rules will break form validation, cause re-render issues, and reduce type safety.**

</critical_reminders>

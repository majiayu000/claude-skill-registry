---
name: form-validation
description: Form validation with Zod schemas and Conform library for Remix applications. Covers schema design, server/client validation, Polaris integration, and complex form patterns.
---

# Form Validation with Zod + Conform

This skill covers robust form validation for Shopify Remix apps using **Zod** (schema validation) and **Conform** (form library designed for Remix).

## Why Zod + Conform?

- **Type-safe**: Zod schemas generate TypeScript types automatically
- **Server-first**: Validation runs on server, with optional client-side
- **Progressive enhancement**: Works without JavaScript
- **Remix-native**: Conform is built specifically for Remix's form handling
- **Polaris-compatible**: Easy integration with Shopify Polaris form components

## Installation

```bash
npm install zod @conform-to/react @conform-to/zod
```

## 1. Basic Schema Definition

### Simple Schema

```typescript
// app/schemas/product.schema.ts
import { z } from 'zod';

export const productSchema = z.object({
  title: z
    .string({ required_error: 'Title is required' })
    .min(1, 'Title cannot be empty')
    .max(255, 'Title must be 255 characters or less'),

  description: z
    .string()
    .max(5000, 'Description must be 5000 characters or less')
    .optional(),

  price: z
    .number({ required_error: 'Price is required' })
    .positive('Price must be positive')
    .multipleOf(0.01, 'Price can have at most 2 decimal places'),

  quantity: z
    .number()
    .int('Quantity must be a whole number')
    .min(0, 'Quantity cannot be negative')
    .default(0),

  status: z.enum(['active', 'draft', 'archived'], {
    required_error: 'Please select a status',
  }),

  tags: z
    .array(z.string())
    .max(10, 'Maximum 10 tags allowed')
    .default([]),
});

// Infer TypeScript type from schema
export type ProductFormData = z.infer<typeof productSchema>;
```

### Schema with Refinements

```typescript
// app/schemas/discount.schema.ts
import { z } from 'zod';

export const discountSchema = z.object({
  code: z
    .string()
    .min(3, 'Code must be at least 3 characters')
    .max(20, 'Code must be 20 characters or less')
    .regex(/^[A-Z0-9]+$/, 'Code must be uppercase letters and numbers only')
    .transform(val => val.toUpperCase()),

  type: z.enum(['percentage', 'fixed_amount']),

  value: z.number().positive('Value must be positive'),

  minPurchase: z.number().min(0).optional(),

  startsAt: z.coerce.date(),

  endsAt: z.coerce.date().optional(),

  usageLimit: z.number().int().positive().optional(),

}).refine(
  (data) => {
    if (data.type === 'percentage' && data.value > 100) {
      return false;
    }
    return true;
  },
  {
    message: 'Percentage discount cannot exceed 100%',
    path: ['value'],
  }
).refine(
  (data) => {
    if (data.endsAt && data.startsAt > data.endsAt) {
      return false;
    }
    return true;
  },
  {
    message: 'End date must be after start date',
    path: ['endsAt'],
  }
);
```

## 2. Remix Action Integration

### Basic Action with Conform

```typescript
// app/routes/products.new.tsx
import { json, redirect, type ActionFunctionArgs } from '@remix-run/node';
import { useActionData } from '@remix-run/react';
import { parseWithZod } from '@conform-to/zod';
import { useForm } from '@conform-to/react';
import { productSchema } from '~/schemas/product.schema';

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();

  const submission = parseWithZod(formData, { schema: productSchema });

  // Return errors if validation failed
  if (submission.status !== 'success') {
    return json(submission.reply(), { status: 400 });
  }

  // submission.value is fully typed as ProductFormData
  const product = await createProduct(submission.value);

  return redirect(`/products/${product.id}`);
}

export default function NewProductPage() {
  const lastResult = useActionData<typeof action>();

  const [form, fields] = useForm({
    lastResult,
    onValidate({ formData }) {
      return parseWithZod(formData, { schema: productSchema });
    },
    shouldValidate: 'onBlur',
    shouldRevalidate: 'onInput',
  });

  return (
    <Form method="post" id={form.id} onSubmit={form.onSubmit}>
      {/* Form fields here */}
    </Form>
  );
}
```

### Action with Async Validation

```typescript
// app/routes/discounts.new.tsx
import { parseWithZod } from '@conform-to/zod';
import { discountSchema } from '~/schemas/discount.schema';

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();

  const submission = await parseWithZod(formData, {
    schema: discountSchema.superRefine(async (data, ctx) => {
      // Check if discount code already exists
      const existingDiscount = await db.discount.findUnique({
        where: { code: data.code },
      });

      if (existingDiscount) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: 'This discount code already exists',
          path: ['code'],
        });
      }
    }),
    async: true,
  });

  if (submission.status !== 'success') {
    return json(submission.reply(), { status: 400 });
  }

  await createDiscount(submission.value);
  return redirect('/discounts');
}
```

## 3. Polaris Form Components Integration

### TextField with Validation

```typescript
// app/components/forms/ValidatedTextField.tsx
import { TextField, type TextFieldProps } from '@shopify/polaris';
import { type FieldMetadata, getInputProps } from '@conform-to/react';

interface ValidatedTextFieldProps extends Omit<TextFieldProps, 'onChange' | 'value' | 'error'> {
  field: FieldMetadata<string>;
}

export function ValidatedTextField({ field, ...props }: ValidatedTextFieldProps) {
  const inputProps = getInputProps(field, { type: 'text' });

  return (
    <TextField
      {...props}
      name={field.name}
      value={field.value ?? ''}
      onChange={(value) => {
        // Trigger Conform's change handler
        const input = document.querySelector(`[name="${field.name}"]`) as HTMLInputElement;
        if (input) {
          input.value = value;
          input.dispatchEvent(new Event('input', { bubbles: true }));
        }
      }}
      error={field.errors?.[0]}
      autoComplete={inputProps.autoComplete}
    />
  );
}
```

### Select with Validation

```typescript
// app/components/forms/ValidatedSelect.tsx
import { Select, type SelectProps } from '@shopify/polaris';
import { type FieldMetadata } from '@conform-to/react';

interface ValidatedSelectProps extends Omit<SelectProps, 'onChange' | 'value' | 'error'> {
  field: FieldMetadata<string>;
}

export function ValidatedSelect({ field, ...props }: ValidatedSelectProps) {
  return (
    <Select
      {...props}
      name={field.name}
      value={field.value ?? ''}
      onChange={(value) => {
        const select = document.querySelector(`[name="${field.name}"]`) as HTMLSelectElement;
        if (select) {
          select.value = value;
          select.dispatchEvent(new Event('change', { bubbles: true }));
        }
      }}
      error={field.errors?.[0]}
    />
  );
}
```

### Complete Polaris Form Example

```typescript
// app/routes/products.$id.edit.tsx
import {
  Page,
  Layout,
  Card,
  FormLayout,
  TextField,
  Select,
  Button,
  Banner,
} from '@shopify/polaris';
import { Form, useActionData, useNavigation } from '@remix-run/react';
import { useForm, getFormProps, getInputProps } from '@conform-to/react';
import { parseWithZod } from '@conform-to/zod';
import { productSchema } from '~/schemas/product.schema';

export default function EditProductPage() {
  const lastResult = useActionData<typeof action>();
  const navigation = useNavigation();
  const isSubmitting = navigation.state === 'submitting';

  const [form, fields] = useForm({
    lastResult,
    onValidate({ formData }) {
      return parseWithZod(formData, { schema: productSchema });
    },
    shouldValidate: 'onBlur',
    shouldRevalidate: 'onInput',
  });

  return (
    <Page
      title="Edit Product"
      primaryAction={{
        content: 'Save',
        loading: isSubmitting,
        submit: true,
        form: form.id,
      }}
    >
      {form.errors && (
        <Banner status="critical">
          <p>Please fix the errors below</p>
        </Banner>
      )}

      <Form method="post" {...getFormProps(form)}>
        <Layout>
          <Layout.Section>
            <Card>
              <FormLayout>
                <TextField
                  label="Title"
                  {...getInputProps(fields.title, { type: 'text' })}
                  value={fields.title.value ?? ''}
                  onChange={(value) => {
                    const input = document.querySelector(
                      `[name="${fields.title.name}"]`
                    ) as HTMLInputElement;
                    if (input) {
                      input.value = value;
                      input.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                  }}
                  error={fields.title.errors?.[0]}
                  autoComplete="off"
                />

                <TextField
                  label="Description"
                  multiline={4}
                  name={fields.description.name}
                  value={fields.description.value ?? ''}
                  onChange={(value) => {
                    const input = document.querySelector(
                      `[name="${fields.description.name}"]`
                    ) as HTMLTextAreaElement;
                    if (input) {
                      input.value = value;
                      input.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                  }}
                  error={fields.description.errors?.[0]}
                  autoComplete="off"
                />

                <TextField
                  label="Price"
                  type="number"
                  prefix="$"
                  name={fields.price.name}
                  value={fields.price.value ?? ''}
                  onChange={(value) => {
                    const input = document.querySelector(
                      `[name="${fields.price.name}"]`
                    ) as HTMLInputElement;
                    if (input) {
                      input.value = value;
                      input.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                  }}
                  error={fields.price.errors?.[0]}
                  autoComplete="off"
                />

                <Select
                  label="Status"
                  name={fields.status.name}
                  value={fields.status.value ?? ''}
                  onChange={(value) => {
                    const select = document.querySelector(
                      `[name="${fields.status.name}"]`
                    ) as HTMLSelectElement;
                    if (select) {
                      select.value = value;
                      select.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                  }}
                  options={[
                    { label: 'Active', value: 'active' },
                    { label: 'Draft', value: 'draft' },
                    { label: 'Archived', value: 'archived' },
                  ]}
                  error={fields.status.errors?.[0]}
                />
              </FormLayout>
            </Card>
          </Layout.Section>
        </Layout>
      </Form>
    </Page>
  );
}
```

## 4. Complex Form Patterns

### Nested Objects

```typescript
// app/schemas/shipping.schema.ts
import { z } from 'zod';

const addressSchema = z.object({
  street: z.string().min(1, 'Street is required'),
  city: z.string().min(1, 'City is required'),
  state: z.string().min(1, 'State is required'),
  zipCode: z.string().regex(/^\d{5}(-\d{4})?$/, 'Invalid ZIP code'),
  country: z.string().min(1, 'Country is required'),
});

export const shippingSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  phone: z.string().regex(/^\+?[\d\s-()]+$/, 'Invalid phone number'),
  shippingAddress: addressSchema,
  billingAddress: addressSchema.optional(),
  sameAsBilling: z.boolean().default(false),
});

// Usage with Conform nested fields
const [form, fields] = useForm({ schema: shippingSchema });
const shippingFields = fields.shippingAddress.getFieldset();

// Access nested fields
<TextField
  label="Street"
  name={shippingFields.street.name}
  error={shippingFields.street.errors?.[0]}
/>
```

### Dynamic Arrays (Field List)

```typescript
// app/schemas/variants.schema.ts
import { z } from 'zod';

export const variantSchema = z.object({
  sku: z.string().min(1, 'SKU is required'),
  price: z.number().positive(),
  inventory: z.number().int().min(0),
  options: z.record(z.string()), // { "Size": "Large", "Color": "Red" }
});

export const productWithVariantsSchema = z.object({
  title: z.string().min(1),
  variants: z.array(variantSchema).min(1, 'At least one variant is required'),
});
```

```typescript
// app/routes/products.new.tsx
import { useFieldList, insert, remove } from '@conform-to/react';

export default function NewProductWithVariants() {
  const [form, fields] = useForm({
    schema: productWithVariantsSchema,
  });

  const variants = useFieldList(form.ref, fields.variants);

  return (
    <Form method="post" {...getFormProps(form)}>
      <TextField label="Title" name={fields.title.name} />

      {variants.map((variant, index) => {
        const variantFields = variant.getFieldset();
        return (
          <Card key={variant.key}>
            <FormLayout>
              <TextField
                label="SKU"
                name={variantFields.sku.name}
                error={variantFields.sku.errors?.[0]}
              />
              <TextField
                label="Price"
                type="number"
                name={variantFields.price.name}
                error={variantFields.price.errors?.[0]}
              />
              <Button
                onClick={() => remove(form.ref, {
                  name: fields.variants.name,
                  index,
                })}
                destructive
              >
                Remove
              </Button>
            </FormLayout>
          </Card>
        );
      })}

      <Button
        onClick={() => insert(form.ref, {
          name: fields.variants.name,
          defaultValue: { sku: '', price: 0, inventory: 0 },
        })}
      >
        Add Variant
      </Button>
    </Form>
  );
}
```

### File Upload Validation

```typescript
// app/schemas/upload.schema.ts
import { z } from 'zod';

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ACCEPTED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp'];

export const uploadSchema = z.object({
  image: z
    .instanceof(File)
    .refine(
      (file) => file.size <= MAX_FILE_SIZE,
      'File size must be less than 5MB'
    )
    .refine(
      (file) => ACCEPTED_IMAGE_TYPES.includes(file.type),
      'Only .jpg, .png and .webp formats are supported'
    ),
});

// For multiple files
export const multiUploadSchema = z.object({
  images: z
    .array(z.instanceof(File))
    .min(1, 'At least one image is required')
    .max(5, 'Maximum 5 images allowed')
    .refine(
      (files) => files.every(file => file.size <= MAX_FILE_SIZE),
      'Each file must be less than 5MB'
    ),
});
```

## 5. Common Shopify Schemas

### Customer Schema

```typescript
// app/schemas/customer.schema.ts
import { z } from 'zod';

export const customerSchema = z.object({
  firstName: z.string().min(1, 'First name is required'),
  lastName: z.string().min(1, 'Last name is required'),

  email: z
    .string()
    .email('Invalid email address')
    .toLowerCase(),

  phone: z
    .string()
    .regex(/^\+?[\d\s-()]+$/, 'Invalid phone number')
    .optional()
    .or(z.literal('')),

  acceptsMarketing: z.boolean().default(false),

  tags: z
    .string()
    .transform(val => val.split(',').map(t => t.trim()).filter(Boolean))
    .pipe(z.array(z.string()))
    .default(''),

  note: z.string().max(5000).optional(),
});
```

### Order Note Schema

```typescript
// app/schemas/order-note.schema.ts
import { z } from 'zod';

export const orderNoteSchema = z.object({
  orderId: z.string().startsWith('gid://shopify/Order/'),
  note: z.string().min(1, 'Note is required').max(5000),
  notifyCustomer: z.boolean().default(false),
});
```

### Metafield Schema

```typescript
// app/schemas/metafield.schema.ts
import { z } from 'zod';

const metafieldTypes = [
  'single_line_text_field',
  'multi_line_text_field',
  'number_integer',
  'number_decimal',
  'boolean',
  'date',
  'json',
  'url',
] as const;

export const metafieldSchema = z.object({
  namespace: z
    .string()
    .min(2, 'Namespace must be at least 2 characters')
    .max(20)
    .regex(/^[a-z_]+$/, 'Only lowercase letters and underscores'),

  key: z
    .string()
    .min(2, 'Key must be at least 2 characters')
    .max(30)
    .regex(/^[a-z_]+$/, 'Only lowercase letters and underscores'),

  type: z.enum(metafieldTypes),

  value: z.string().min(1, 'Value is required'),
}).refine(
  (data) => {
    if (data.type === 'number_integer') {
      return /^-?\d+$/.test(data.value);
    }
    if (data.type === 'number_decimal') {
      return /^-?\d+(\.\d+)?$/.test(data.value);
    }
    if (data.type === 'boolean') {
      return ['true', 'false'].includes(data.value);
    }
    if (data.type === 'url') {
      try {
        new URL(data.value);
        return true;
      } catch {
        return false;
      }
    }
    if (data.type === 'json') {
      try {
        JSON.parse(data.value);
        return true;
      } catch {
        return false;
      }
    }
    return true;
  },
  {
    message: 'Value does not match the selected type',
    path: ['value'],
  }
);
```

## 6. Error Handling Patterns

### Custom Error Messages

```typescript
// app/lib/validation-messages.ts
export const validationMessages = {
  required: (field: string) => `${field} is required`,
  minLength: (field: string, min: number) =>
    `${field} must be at least ${min} characters`,
  maxLength: (field: string, max: number) =>
    `${field} must be ${max} characters or less`,
  email: 'Please enter a valid email address',
  positive: (field: string) => `${field} must be a positive number`,
  url: 'Please enter a valid URL',
};
```

### Form-Level Errors

```typescript
// app/routes/checkout.tsx
export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();

  const submission = parseWithZod(formData, { schema: checkoutSchema });

  if (submission.status !== 'success') {
    return json(submission.reply(), { status: 400 });
  }

  try {
    await processCheckout(submission.value);
    return redirect('/thank-you');
  } catch (error) {
    // Return form-level error
    return json(
      submission.reply({
        formErrors: ['Payment processing failed. Please try again.'],
      }),
      { status: 500 }
    );
  }
}

// In component
const [form, fields] = useForm({ lastResult });

{form.errors?.map((error, i) => (
  <Banner key={i} status="critical">{error}</Banner>
))}
```

## Best Practices Summary

1. **Define schemas in separate files** - Easier to test and reuse
2. **Use `z.infer<typeof schema>`** - Get TypeScript types for free
3. **Validate on server first** - Client validation is just UX
4. **Use `coerce` for type conversion** - `z.coerce.number()` handles string inputs
5. **Keep refinements simple** - Complex logic in action, not schema
6. **Test schemas separately** - Unit test validation logic
7. **Use meaningful error messages** - Users need to understand what's wrong
8. **Progressive enhancement** - Forms should work without JS

## Anti-Patterns to Avoid

- **DON'T** validate only on client - Always validate server-side
- **DON'T** duplicate validation logic - Single source of truth in schema
- **DON'T** catch errors silently - Show users what went wrong
- **DON'T** over-validate - Trust the schema, don't re-check in action

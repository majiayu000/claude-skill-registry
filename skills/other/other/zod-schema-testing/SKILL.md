---
name: "Zod Schema Testing"
description: "Comprehensive testing patterns for Zod schemas covering validation testing, transform testing, error message verification, and integration with API endpoints and forms"
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [zod, schema, validation, typescript, transforms, api-validation, form-validation, type-safety, error-handling, refinements]
testingTypes: [unit, integration]
frameworks: [vitest, jest]
languages: [typescript]
domains: [web, api]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# Zod Schema Testing Skill

You are an expert QA engineer specializing in testing Zod schema validation. When the user asks you to write, review, or debug tests for Zod schemas, validators, transforms, or their integrations with APIs and forms, follow these detailed instructions.

## Core Principles

1. **Test the schema contract, not the implementation** -- Validate that schemas accept correct data and reject invalid data with the right error messages. Do not test Zod internals.
2. **Boundary value analysis** -- Test minimum and maximum values, empty strings, zero-length arrays, and edge cases at every boundary defined in the schema.
3. **Error message verification** -- Validate that error messages are user-friendly and actionable. Custom error messages should be tested explicitly.
4. **Transform round-trip testing** -- When schemas transform data, verify both the input acceptance and the output shape. Test that transformed data can be used downstream.
5. **Discriminated union exhaustiveness** -- Test every branch of discriminated unions and verify that the discriminator field correctly routes to the right schema.
6. **Integration-first mindset** -- Schemas rarely exist in isolation. Test them at the integration boundary: API request parsing, form submission, and configuration loading.
7. **Type-level assertions** -- Use TypeScript's `Expect` and `Equal` type utilities to verify that inferred types match expectations at compile time.

## Project Structure

Always organize Zod schema tests with this structure:

```
src/
  schemas/
    user.schema.ts
    product.schema.ts
    order.schema.ts
    shared/
      pagination.schema.ts
      address.schema.ts
    index.ts
  __tests__/
    schemas/
      user.schema.test.ts
      product.schema.test.ts
      order.schema.test.ts
      shared/
        pagination.schema.test.ts
        address.schema.test.ts
    integration/
      api-validation.test.ts
      form-validation.test.ts
    helpers/
      schema-test-utils.ts
      type-assertions.ts
```

## Basic Schema Validation Testing

### Testing Primitive Schemas

```typescript
// src/schemas/user.schema.ts
import { z } from 'zod';

export const emailSchema = z
  .string()
  .email('Please enter a valid email address')
  .min(5, 'Email must be at least 5 characters')
  .max(254, 'Email must not exceed 254 characters')
  .toLowerCase()
  .trim();

export const passwordSchema = z
  .string()
  .min(8, 'Password must be at least 8 characters')
  .max(128, 'Password must not exceed 128 characters')
  .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
  .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
  .regex(/[0-9]/, 'Password must contain at least one number')
  .regex(/[^A-Za-z0-9]/, 'Password must contain at least one special character');

export const usernameSchema = z
  .string()
  .min(3, 'Username must be at least 3 characters')
  .max(30, 'Username must not exceed 30 characters')
  .regex(/^[a-zA-Z0-9_-]+$/, 'Username can only contain letters, numbers, hyphens, and underscores');

export type Email = z.infer<typeof emailSchema>;
export type Password = z.infer<typeof passwordSchema>;
export type Username = z.infer<typeof usernameSchema>;
```

```typescript
// __tests__/schemas/user.schema.test.ts
import { describe, it, expect } from 'vitest';
import { emailSchema, passwordSchema, usernameSchema } from '../../src/schemas/user.schema';

describe('emailSchema', () => {
  describe('valid emails', () => {
    const validEmails = [
      'user@example.com',
      'user.name@example.com',
      'user+tag@example.com',
      'user@sub.domain.com',
      'a@b.co',
    ];

    it.each(validEmails)('should accept "%s"', (email) => {
      const result = emailSchema.safeParse(email);
      expect(result.success).toBe(true);
    });
  });

  describe('invalid emails', () => {
    const invalidEmails = [
      { input: '', error: 'Email must be at least 5 characters' },
      { input: 'notanemail', error: 'Please enter a valid email address' },
      { input: '@no-local.com', error: 'Please enter a valid email address' },
      { input: 'no-domain@', error: 'Please enter a valid email address' },
      { input: 'a@b', error: 'Please enter a valid email address' },
      { input: 'a'.repeat(250) + '@b.com', error: 'Email must not exceed 254 characters' },
    ];

    it.each(invalidEmails)('should reject "$input" with error "$error"', ({ input, error }) => {
      const result = emailSchema.safeParse(input);
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.issues[0].message).toBe(error);
      }
    });
  });

  describe('transforms', () => {
    it('should lowercase the email', () => {
      const result = emailSchema.parse('User@Example.COM');
      expect(result).toBe('user@example.com');
    });

    it('should trim whitespace', () => {
      const result = emailSchema.parse('  user@example.com  ');
      expect(result).toBe('user@example.com');
    });
  });

  describe('type assertions', () => {
    it('should reject non-string types', () => {
      expect(emailSchema.safeParse(123).success).toBe(false);
      expect(emailSchema.safeParse(null).success).toBe(false);
      expect(emailSchema.safeParse(undefined).success).toBe(false);
      expect(emailSchema.safeParse({}).success).toBe(false);
      expect(emailSchema.safeParse([]).success).toBe(false);
    });
  });
});

describe('passwordSchema', () => {
  it('should accept a strong password', () => {
    const result = passwordSchema.safeParse('MyP@ssw0rd!');
    expect(result.success).toBe(true);
  });

  it('should reject password without uppercase', () => {
    const result = passwordSchema.safeParse('myp@ssw0rd!');
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].message).toBe(
        'Password must contain at least one uppercase letter'
      );
    }
  });

  it('should reject password without lowercase', () => {
    const result = passwordSchema.safeParse('MYP@SSW0RD!');
    expect(result.success).toBe(false);
  });

  it('should reject password without number', () => {
    const result = passwordSchema.safeParse('MyP@ssword!');
    expect(result.success).toBe(false);
  });

  it('should reject password without special character', () => {
    const result = passwordSchema.safeParse('MyPassw0rd');
    expect(result.success).toBe(false);
  });

  it('should reject password shorter than 8 characters', () => {
    const result = passwordSchema.safeParse('Ab1!');
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].message).toBe('Password must be at least 8 characters');
    }
  });

  it('should reject password longer than 128 characters', () => {
    const longPassword = 'Ab1!' + 'a'.repeat(125);
    const result = passwordSchema.safeParse(longPassword);
    expect(result.success).toBe(false);
  });
});

describe('usernameSchema', () => {
  const validUsernames = ['john', 'john_doe', 'john-doe', 'JohnDoe123', 'a_b'];

  it.each(validUsernames)('should accept "%s"', (username) => {
    expect(usernameSchema.safeParse(username).success).toBe(true);
  });

  const invalidUsernames = [
    { input: 'ab', reason: 'too short' },
    { input: 'a'.repeat(31), reason: 'too long' },
    { input: 'john doe', reason: 'contains space' },
    { input: 'john@doe', reason: 'contains @' },
    { input: 'john.doe', reason: 'contains dot' },
    { input: 'john!doe', reason: 'contains special char' },
  ];

  it.each(invalidUsernames)('should reject "$input" ($reason)', ({ input }) => {
    expect(usernameSchema.safeParse(input).success).toBe(false);
  });
});
```

## Object Schema Testing

### Complex Object Schemas

```typescript
// src/schemas/product.schema.ts
import { z } from 'zod';

export const priceSchema = z
  .number()
  .positive('Price must be positive')
  .finite('Price must be a finite number')
  .multipleOf(0.01, 'Price must have at most 2 decimal places');

export const productSchema = z.object({
  name: z.string().min(1, 'Name is required').max(200, 'Name too long'),
  description: z.string().min(10, 'Description must be at least 10 characters').max(5000),
  price: priceSchema,
  currency: z.enum(['USD', 'EUR', 'GBP', 'JPY']),
  category: z.string().min(1),
  tags: z.array(z.string().min(1)).min(1, 'At least one tag required').max(10),
  inStock: z.boolean(),
  quantity: z.number().int().nonnegative(),
  metadata: z.record(z.string(), z.unknown()).optional(),
  images: z
    .array(
      z.object({
        url: z.string().url('Invalid image URL'),
        alt: z.string().min(1, 'Alt text is required'),
        width: z.number().int().positive().optional(),
        height: z.number().int().positive().optional(),
      })
    )
    .min(1, 'At least one image required')
    .max(20),
});

export type Product = z.infer<typeof productSchema>;

export const createProductSchema = productSchema.omit({ quantity: true }).extend({
  initialQuantity: z.number().int().nonnegative().default(0),
});

export const updateProductSchema = productSchema.partial().required({ name: true });

export const productSearchSchema = z.object({
  query: z.string().optional(),
  category: z.string().optional(),
  minPrice: z.coerce.number().nonnegative().optional(),
  maxPrice: z.coerce.number().positive().optional(),
  inStock: z.coerce.boolean().optional(),
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  sortBy: z.enum(['name', 'price', 'createdAt']).default('createdAt'),
  sortOrder: z.enum(['asc', 'desc']).default('desc'),
});
```

```typescript
// __tests__/schemas/product.schema.test.ts
import { describe, it, expect } from 'vitest';
import {
  productSchema,
  createProductSchema,
  updateProductSchema,
  productSearchSchema,
  priceSchema,
} from '../../src/schemas/product.schema';

const validProduct = {
  name: 'Widget Pro',
  description: 'A professional widget for all your needs',
  price: 29.99,
  currency: 'USD' as const,
  category: 'tools',
  tags: ['widget', 'professional'],
  inStock: true,
  quantity: 100,
  images: [
    { url: 'https://example.com/img.jpg', alt: 'Widget photo' },
  ],
};

describe('productSchema', () => {
  it('should accept a valid product', () => {
    const result = productSchema.safeParse(validProduct);
    expect(result.success).toBe(true);
  });

  it('should accept a product with optional metadata', () => {
    const result = productSchema.safeParse({
      ...validProduct,
      metadata: { sku: 'WDG-001', weight: 0.5 },
    });
    expect(result.success).toBe(true);
  });

  describe('required fields', () => {
    const requiredFields = ['name', 'description', 'price', 'currency', 'category', 'tags', 'inStock', 'quantity', 'images'];

    it.each(requiredFields)('should reject when "%s" is missing', (field) => {
      const incomplete = { ...validProduct };
      delete (incomplete as Record<string, unknown>)[field];

      const result = productSchema.safeParse(incomplete);
      expect(result.success).toBe(false);
    });
  });

  describe('name validation', () => {
    it('should reject empty name', () => {
      const result = productSchema.safeParse({ ...validProduct, name: '' });
      expect(result.success).toBe(false);
    });

    it('should reject name exceeding 200 characters', () => {
      const result = productSchema.safeParse({
        ...validProduct,
        name: 'a'.repeat(201),
      });
      expect(result.success).toBe(false);
    });
  });

  describe('tags validation', () => {
    it('should reject empty tags array', () => {
      const result = productSchema.safeParse({ ...validProduct, tags: [] });
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.issues[0].message).toBe('At least one tag required');
      }
    });

    it('should reject more than 10 tags', () => {
      const result = productSchema.safeParse({
        ...validProduct,
        tags: Array.from({ length: 11 }, (_, i) => `tag-${i}`),
      });
      expect(result.success).toBe(false);
    });

    it('should reject tags with empty strings', () => {
      const result = productSchema.safeParse({
        ...validProduct,
        tags: ['valid', ''],
      });
      expect(result.success).toBe(false);
    });
  });

  describe('images validation', () => {
    it('should reject empty images array', () => {
      const result = productSchema.safeParse({ ...validProduct, images: [] });
      expect(result.success).toBe(false);
    });

    it('should reject images with invalid URL', () => {
      const result = productSchema.safeParse({
        ...validProduct,
        images: [{ url: 'not-a-url', alt: 'test' }],
      });
      expect(result.success).toBe(false);
    });

    it('should reject images without alt text', () => {
      const result = productSchema.safeParse({
        ...validProduct,
        images: [{ url: 'https://example.com/img.jpg', alt: '' }],
      });
      expect(result.success).toBe(false);
    });
  });

  describe('currency enum', () => {
    it.each(['USD', 'EUR', 'GBP', 'JPY'])('should accept %s', (currency) => {
      const result = productSchema.safeParse({ ...validProduct, currency });
      expect(result.success).toBe(true);
    });

    it('should reject invalid currency', () => {
      const result = productSchema.safeParse({ ...validProduct, currency: 'BTC' });
      expect(result.success).toBe(false);
    });
  });
});

describe('priceSchema', () => {
  it('should accept valid prices', () => {
    expect(priceSchema.safeParse(0.01).success).toBe(true);
    expect(priceSchema.safeParse(1.00).success).toBe(true);
    expect(priceSchema.safeParse(99.99).success).toBe(true);
    expect(priceSchema.safeParse(9999.99).success).toBe(true);
  });

  it('should reject zero', () => {
    const result = priceSchema.safeParse(0);
    expect(result.success).toBe(false);
  });

  it('should reject negative prices', () => {
    const result = priceSchema.safeParse(-10);
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].message).toBe('Price must be positive');
    }
  });

  it('should reject Infinity', () => {
    const result = priceSchema.safeParse(Infinity);
    expect(result.success).toBe(false);
  });

  it('should reject NaN', () => {
    const result = priceSchema.safeParse(NaN);
    expect(result.success).toBe(false);
  });

  it('should reject more than 2 decimal places', () => {
    const result = priceSchema.safeParse(10.999);
    expect(result.success).toBe(false);
  });
});

describe('createProductSchema', () => {
  it('should not require quantity (omitted)', () => {
    const data = {
      ...validProduct,
      initialQuantity: 50,
    };
    delete (data as Record<string, unknown>).quantity;

    const result = createProductSchema.safeParse(data);
    expect(result.success).toBe(true);
  });

  it('should default initialQuantity to 0', () => {
    const data = { ...validProduct };
    delete (data as Record<string, unknown>).quantity;

    const result = createProductSchema.safeParse(data);
    expect(result.success).toBe(true);
    if (result.success) {
      expect(result.data.initialQuantity).toBe(0);
    }
  });
});

describe('updateProductSchema', () => {
  it('should require name but make everything else optional', () => {
    const result = updateProductSchema.safeParse({ name: 'Updated Name' });
    expect(result.success).toBe(true);
  });

  it('should reject without name', () => {
    const result = updateProductSchema.safeParse({ price: 19.99 });
    expect(result.success).toBe(false);
  });

  it('should accept partial updates', () => {
    const result = updateProductSchema.safeParse({
      name: 'Updated',
      price: 19.99,
    });
    expect(result.success).toBe(true);
  });
});

describe('productSearchSchema', () => {
  it('should provide defaults for pagination', () => {
    const result = productSearchSchema.parse({});
    expect(result.page).toBe(1);
    expect(result.limit).toBe(20);
    expect(result.sortBy).toBe('createdAt');
    expect(result.sortOrder).toBe('desc');
  });

  it('should coerce string query params to correct types', () => {
    const result = productSearchSchema.parse({
      minPrice: '10',
      maxPrice: '100',
      inStock: 'true',
      page: '2',
      limit: '50',
    });

    expect(result.minPrice).toBe(10);
    expect(result.maxPrice).toBe(100);
    expect(result.inStock).toBe(true);
    expect(result.page).toBe(2);
    expect(result.limit).toBe(50);
  });

  it('should reject negative minPrice', () => {
    const result = productSearchSchema.safeParse({ minPrice: '-5' });
    expect(result.success).toBe(false);
  });

  it('should reject limit over 100', () => {
    const result = productSearchSchema.safeParse({ limit: '200' });
    expect(result.success).toBe(false);
  });

  it('should reject invalid sortBy', () => {
    const result = productSearchSchema.safeParse({ sortBy: 'invalid' });
    expect(result.success).toBe(false);
  });
});
```

## Transform and Refinement Testing

```typescript
// src/schemas/order.schema.ts
import { z } from 'zod';

export const dateStringSchema = z
  .string()
  .transform((val) => new Date(val))
  .refine((date) => !isNaN(date.getTime()), {
    message: 'Invalid date format',
  })
  .refine((date) => date > new Date('2020-01-01'), {
    message: 'Date must be after January 1, 2020',
  });

export const phoneSchema = z
  .string()
  .transform((val) => val.replace(/[\s()-]/g, ''))
  .refine((val) => /^\+?[0-9]{10,15}$/.test(val), {
    message: 'Invalid phone number format',
  });

export const addressSchema = z.object({
  street: z.string().min(1, 'Street is required'),
  city: z.string().min(1, 'City is required'),
  state: z.string().min(1, 'State is required'),
  zipCode: z
    .string()
    .regex(/^\d{5}(-\d{4})?$/, 'Invalid ZIP code format'),
  country: z.string().length(2, 'Country must be a 2-letter ISO code').toUpperCase(),
});

export const orderSchema = z
  .object({
    items: z
      .array(
        z.object({
          productId: z.string().uuid(),
          quantity: z.number().int().positive(),
          unitPrice: z.number().positive(),
        })
      )
      .min(1, 'Order must have at least one item'),
    shippingAddress: addressSchema,
    billingAddress: addressSchema.optional(),
    couponCode: z.string().optional(),
    notes: z.string().max(500).optional(),
  })
  .transform((order) => ({
    ...order,
    subtotal: order.items.reduce((sum, item) => sum + item.quantity * item.unitPrice, 0),
    itemCount: order.items.reduce((sum, item) => sum + item.quantity, 0),
    billingAddress: order.billingAddress ?? order.shippingAddress,
  }))
  .refine(
    (order) => order.subtotal > 0,
    { message: 'Order total must be greater than zero' }
  )
  .refine(
    (order) => order.subtotal <= 100000,
    { message: 'Order total cannot exceed $100,000' }
  );

export type Order = z.infer<typeof orderSchema>;
```

```typescript
// __tests__/schemas/order.schema.test.ts
import { describe, it, expect } from 'vitest';
import {
  dateStringSchema,
  phoneSchema,
  addressSchema,
  orderSchema,
} from '../../src/schemas/order.schema';

describe('dateStringSchema', () => {
  it('should transform ISO string to Date object', () => {
    const result = dateStringSchema.parse('2024-06-15T10:00:00Z');
    expect(result).toBeInstanceOf(Date);
    expect(result.getFullYear()).toBe(2024);
  });

  it('should accept various date formats', () => {
    expect(dateStringSchema.safeParse('2024-01-15').success).toBe(true);
    expect(dateStringSchema.safeParse('2024-06-15T10:00:00.000Z').success).toBe(true);
    expect(dateStringSchema.safeParse('June 15, 2024').success).toBe(true);
  });

  it('should reject invalid date strings', () => {
    const result = dateStringSchema.safeParse('not-a-date');
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].message).toBe('Invalid date format');
    }
  });

  it('should reject dates before 2020', () => {
    const result = dateStringSchema.safeParse('2019-12-31');
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues[0].message).toBe('Date must be after January 1, 2020');
    }
  });
});

describe('phoneSchema', () => {
  it('should strip formatting and accept valid phone numbers', () => {
    expect(phoneSchema.parse('+1 (555) 123-4567')).toBe('+15551234567');
    expect(phoneSchema.parse('555-123-4567')).toBe('5551234567');
    expect(phoneSchema.parse('+44 20 7946 0958')).toBe('+442079460958');
  });

  it('should reject invalid phone numbers', () => {
    expect(phoneSchema.safeParse('123').success).toBe(false);
    expect(phoneSchema.safeParse('abc').success).toBe(false);
    expect(phoneSchema.safeParse('').success).toBe(false);
  });

  it('should reject numbers that are too long', () => {
    const result = phoneSchema.safeParse('1'.repeat(20));
    expect(result.success).toBe(false);
  });
});

describe('addressSchema', () => {
  const validAddress = {
    street: '123 Main St',
    city: 'Springfield',
    state: 'IL',
    zipCode: '62704',
    country: 'US',
  };

  it('should accept a valid address', () => {
    const result = addressSchema.safeParse(validAddress);
    expect(result.success).toBe(true);
  });

  it('should uppercase the country code', () => {
    const result = addressSchema.parse({ ...validAddress, country: 'us' });
    expect(result.country).toBe('US');
  });

  it('should accept ZIP+4 format', () => {
    const result = addressSchema.safeParse({ ...validAddress, zipCode: '62704-1234' });
    expect(result.success).toBe(true);
  });

  it('should reject invalid ZIP code', () => {
    const result = addressSchema.safeParse({ ...validAddress, zipCode: 'ABC' });
    expect(result.success).toBe(false);
  });

  it('should reject country code that is not 2 characters', () => {
    expect(addressSchema.safeParse({ ...validAddress, country: 'USA' }).success).toBe(false);
    expect(addressSchema.safeParse({ ...validAddress, country: 'U' }).success).toBe(false);
  });
});

describe('orderSchema', () => {
  const validOrder = {
    items: [
      { productId: '550e8400-e29b-41d4-a716-446655440000', quantity: 2, unitPrice: 29.99 },
      { productId: '6ba7b810-9dad-11d1-80b4-00c04fd430c8', quantity: 1, unitPrice: 49.99 },
    ],
    shippingAddress: {
      street: '123 Main St',
      city: 'Springfield',
      state: 'IL',
      zipCode: '62704',
      country: 'US',
    },
  };

  it('should calculate subtotal from items', () => {
    const result = orderSchema.parse(validOrder);
    expect(result.subtotal).toBeCloseTo(109.97);
  });

  it('should calculate total item count', () => {
    const result = orderSchema.parse(validOrder);
    expect(result.itemCount).toBe(3);
  });

  it('should default billing address to shipping address', () => {
    const result = orderSchema.parse(validOrder);
    expect(result.billingAddress).toEqual(result.shippingAddress);
  });

  it('should use explicit billing address when provided', () => {
    const billingAddress = {
      street: '456 Oak Ave',
      city: 'Chicago',
      state: 'IL',
      zipCode: '60601',
      country: 'US',
    };

    const result = orderSchema.parse({
      ...validOrder,
      billingAddress,
    });
    expect(result.billingAddress.street).toBe('456 Oak Ave');
  });

  it('should reject empty items array', () => {
    const result = orderSchema.safeParse({ ...validOrder, items: [] });
    expect(result.success).toBe(false);
  });

  it('should reject order exceeding $100,000', () => {
    const result = orderSchema.safeParse({
      ...validOrder,
      items: [
        { productId: '550e8400-e29b-41d4-a716-446655440000', quantity: 1, unitPrice: 100001 },
      ],
    });
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues.some((i) => i.message.includes('$100,000'))).toBe(true);
    }
  });

  it('should reject items with non-UUID productId', () => {
    const result = orderSchema.safeParse({
      ...validOrder,
      items: [{ productId: 'not-a-uuid', quantity: 1, unitPrice: 10 }],
    });
    expect(result.success).toBe(false);
  });

  it('should reject items with zero quantity', () => {
    const result = orderSchema.safeParse({
      ...validOrder,
      items: [
        { productId: '550e8400-e29b-41d4-a716-446655440000', quantity: 0, unitPrice: 10 },
      ],
    });
    expect(result.success).toBe(false);
  });
});
```

## Discriminated Union Testing

```typescript
// src/schemas/notification.schema.ts
import { z } from 'zod';

export const notificationSchema = z.discriminatedUnion('type', [
  z.object({
    type: z.literal('email'),
    to: z.string().email(),
    subject: z.string().min(1).max(200),
    body: z.string().min(1),
    cc: z.array(z.string().email()).optional(),
    bcc: z.array(z.string().email()).optional(),
  }),
  z.object({
    type: z.literal('sms'),
    phoneNumber: z.string().regex(/^\+[1-9]\d{1,14}$/),
    message: z.string().min(1).max(160),
  }),
  z.object({
    type: z.literal('push'),
    deviceToken: z.string().min(1),
    title: z.string().min(1).max(100),
    body: z.string().min(1).max(500),
    data: z.record(z.string()).optional(),
    badge: z.number().int().nonnegative().optional(),
    sound: z.string().optional(),
  }),
  z.object({
    type: z.literal('webhook'),
    url: z.string().url(),
    method: z.enum(['GET', 'POST', 'PUT']),
    headers: z.record(z.string()).optional(),
    payload: z.unknown(),
    retries: z.number().int().min(0).max(5).default(3),
  }),
]);

export type Notification = z.infer<typeof notificationSchema>;
```

```typescript
// __tests__/schemas/notification.schema.test.ts
import { describe, it, expect } from 'vitest';
import { notificationSchema } from '../../src/schemas/notification.schema';

describe('notificationSchema (discriminated union)', () => {
  describe('email notifications', () => {
    it('should accept valid email notification', () => {
      const result = notificationSchema.safeParse({
        type: 'email',
        to: 'user@example.com',
        subject: 'Hello',
        body: 'World',
      });
      expect(result.success).toBe(true);
    });

    it('should accept email with cc and bcc', () => {
      const result = notificationSchema.safeParse({
        type: 'email',
        to: 'user@example.com',
        subject: 'Hello',
        body: 'World',
        cc: ['cc@example.com'],
        bcc: ['bcc@example.com'],
      });
      expect(result.success).toBe(true);
    });

    it('should reject email without subject', () => {
      const result = notificationSchema.safeParse({
        type: 'email',
        to: 'user@example.com',
        body: 'World',
      });
      expect(result.success).toBe(false);
    });

    it('should reject email with invalid cc addresses', () => {
      const result = notificationSchema.safeParse({
        type: 'email',
        to: 'user@example.com',
        subject: 'Hello',
        body: 'World',
        cc: ['not-an-email'],
      });
      expect(result.success).toBe(false);
    });
  });

  describe('sms notifications', () => {
    it('should accept valid SMS', () => {
      const result = notificationSchema.safeParse({
        type: 'sms',
        phoneNumber: '+15551234567',
        message: 'Hello from SMS',
      });
      expect(result.success).toBe(true);
    });

    it('should reject SMS exceeding 160 characters', () => {
      const result = notificationSchema.safeParse({
        type: 'sms',
        phoneNumber: '+15551234567',
        message: 'a'.repeat(161),
      });
      expect(result.success).toBe(false);
    });

    it('should reject SMS with invalid phone format', () => {
      const result = notificationSchema.safeParse({
        type: 'sms',
        phoneNumber: '5551234567', // Missing +
        message: 'Hello',
      });
      expect(result.success).toBe(false);
    });
  });

  describe('push notifications', () => {
    it('should accept valid push notification', () => {
      const result = notificationSchema.safeParse({
        type: 'push',
        deviceToken: 'abc123device',
        title: 'New Message',
        body: 'You have a new message',
      });
      expect(result.success).toBe(true);
    });

    it('should accept push with optional fields', () => {
      const result = notificationSchema.safeParse({
        type: 'push',
        deviceToken: 'abc123',
        title: 'Alert',
        body: 'Something happened',
        data: { orderId: '123' },
        badge: 5,
        sound: 'default',
      });
      expect(result.success).toBe(true);
    });

    it('should reject push with negative badge', () => {
      const result = notificationSchema.safeParse({
        type: 'push',
        deviceToken: 'abc123',
        title: 'Alert',
        body: 'Test',
        badge: -1,
      });
      expect(result.success).toBe(false);
    });
  });

  describe('webhook notifications', () => {
    it('should accept valid webhook with defaults', () => {
      const result = notificationSchema.parse({
        type: 'webhook',
        url: 'https://example.com/webhook',
        method: 'POST',
        payload: { event: 'order.created' },
      });
      expect(result.retries).toBe(3); // Default value
    });

    it('should reject webhook with invalid URL', () => {
      const result = notificationSchema.safeParse({
        type: 'webhook',
        url: 'not-a-url',
        method: 'POST',
        payload: {},
      });
      expect(result.success).toBe(false);
    });

    it('should reject webhook with invalid method', () => {
      const result = notificationSchema.safeParse({
        type: 'webhook',
        url: 'https://example.com/webhook',
        method: 'DELETE',
        payload: {},
      });
      expect(result.success).toBe(false);
    });
  });

  describe('discriminator validation', () => {
    it('should reject unknown notification type', () => {
      const result = notificationSchema.safeParse({
        type: 'carrier-pigeon',
        message: 'coo coo',
      });
      expect(result.success).toBe(false);
    });

    it('should reject missing type field', () => {
      const result = notificationSchema.safeParse({
        to: 'user@example.com',
        subject: 'Hello',
        body: 'World',
      });
      expect(result.success).toBe(false);
    });

    it('should not allow email fields on SMS type', () => {
      const result = notificationSchema.safeParse({
        type: 'sms',
        phoneNumber: '+15551234567',
        message: 'Hello',
        subject: 'This should not be here',
      });
      // Zod strips unknown keys on discriminated unions
      if (result.success) {
        expect(result.data).not.toHaveProperty('subject');
      }
    });
  });
});
```

## Error Message and Path Testing

```typescript
// __tests__/helpers/schema-test-utils.ts
import { z } from 'zod';
import { expect } from 'vitest';

export function expectZodError(
  schema: z.ZodType,
  data: unknown,
  expectedIssues: Array<{
    path?: (string | number)[];
    message?: string;
    code?: string;
  }>
) {
  const result = schema.safeParse(data);
  expect(result.success).toBe(false);

  if (!result.success) {
    for (const expected of expectedIssues) {
      const matchingIssue = result.error.issues.find((issue) => {
        const pathMatch = expected.path
          ? JSON.stringify(issue.path) === JSON.stringify(expected.path)
          : true;
        const messageMatch = expected.message
          ? issue.message === expected.message
          : true;
        const codeMatch = expected.code
          ? issue.code === expected.code
          : true;
        return pathMatch && messageMatch && codeMatch;
      });

      expect(matchingIssue, `Expected issue with ${JSON.stringify(expected)}`).toBeDefined();
    }
  }
}

export function expectValid<T>(schema: z.ZodType<T>, data: unknown): T {
  const result = schema.safeParse(data);
  expect(result.success).toBe(true);
  if (result.success) return result.data;
  throw new Error('Validation failed');
}

export function expectInvalid(schema: z.ZodType, data: unknown): z.ZodError {
  const result = schema.safeParse(data);
  expect(result.success).toBe(false);
  if (!result.success) return result.error;
  throw new Error('Validation unexpectedly succeeded');
}
```

```typescript
// __tests__/schemas/error-paths.test.ts
import { describe, it } from 'vitest';
import { orderSchema } from '../../src/schemas/order.schema';
import { expectZodError } from '../helpers/schema-test-utils';

describe('Error path verification', () => {
  it('should report errors at the correct nested path', () => {
    expectZodError(
      orderSchema,
      {
        items: [
          {
            productId: 'not-a-uuid',
            quantity: -1,
            unitPrice: 10,
          },
        ],
        shippingAddress: {
          street: '',
          city: '',
          state: 'IL',
          zipCode: 'bad',
          country: 'US',
        },
      },
      [
        { path: ['items', 0, 'productId'], code: 'invalid_string' },
        { path: ['items', 0, 'quantity'], code: 'too_small' },
        { path: ['shippingAddress', 'street'], message: 'Street is required' },
        { path: ['shippingAddress', 'city'], message: 'City is required' },
        { path: ['shippingAddress', 'zipCode'], message: 'Invalid ZIP code format' },
      ]
    );
  });

  it('should flatten errors for form consumption', () => {
    const result = orderSchema.safeParse({
      items: [],
      shippingAddress: {
        street: '',
        city: 'Test',
        state: 'IL',
        zipCode: '62704',
        country: 'US',
      },
    });

    if (!result.success) {
      const flattened = result.error.flatten();
      expect(flattened.fieldErrors).toHaveProperty('items');

      const formatted = result.error.format();
      expect(formatted.shippingAddress?.street?._errors).toContain('Street is required');
    }
  });
});
```

## API Endpoint Integration Testing

```typescript
// __tests__/integration/api-validation.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { createServer } from '../../src/server';
import { productSchema, productSearchSchema } from '../../src/schemas/product.schema';

describe('API Schema Validation Integration', () => {
  let server: ReturnType<typeof createServer>;
  let baseUrl: string;

  beforeAll(async () => {
    server = createServer();
    await server.listen(0);
    const address = server.address();
    baseUrl = `http://localhost:${typeof address === 'object' ? address?.port : address}`;
  });

  afterAll(async () => {
    await server.close();
  });

  describe('POST /api/products', () => {
    it('should accept valid product and return 201', async () => {
      const product = {
        name: 'Test Product',
        description: 'A test product for validation',
        price: 29.99,
        currency: 'USD',
        category: 'test',
        tags: ['test'],
        inStock: true,
        quantity: 10,
        images: [{ url: 'https://example.com/img.jpg', alt: 'Test' }],
      };

      const response = await fetch(`${baseUrl}/api/products`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(product),
      });

      expect(response.status).toBe(201);
      const body = await response.json();
      expect(body.name).toBe('Test Product');
    });

    it('should return 400 with validation errors for invalid product', async () => {
      const response = await fetch(`${baseUrl}/api/products`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: '' }),
      });

      expect(response.status).toBe(400);
      const body = await response.json();
      expect(body.errors).toBeDefined();
      expect(Array.isArray(body.errors)).toBe(true);
    });

    it('should return structured validation errors matching Zod format', async () => {
      const response = await fetch(`${baseUrl}/api/products`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: '',
          price: -5,
          tags: [],
        }),
      });

      const body = await response.json();
      expect(body.errors).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            path: expect.any(Array),
            message: expect.any(String),
          }),
        ])
      );
    });
  });

  describe('GET /api/products (search)', () => {
    it('should coerce query string params via schema', async () => {
      const response = await fetch(
        `${baseUrl}/api/products?page=2&limit=50&minPrice=10&inStock=true`
      );

      expect(response.status).toBe(200);
      const body = await response.json();
      expect(body.pagination.page).toBe(2);
      expect(body.pagination.limit).toBe(50);
    });

    it('should use default values when params are omitted', async () => {
      const response = await fetch(`${baseUrl}/api/products`);

      expect(response.status).toBe(200);
      const body = await response.json();
      expect(body.pagination.page).toBe(1);
      expect(body.pagination.limit).toBe(20);
    });

    it('should return 400 for invalid search params', async () => {
      const response = await fetch(`${baseUrl}/api/products?limit=999`);
      expect(response.status).toBe(400);
    });
  });
});
```

## Form Validation with React Hook Form + Zod

```typescript
// __tests__/integration/form-validation.test.tsx
import { describe, it, expect } from 'vitest';
import { renderHook, act, waitFor } from '@testing-library/react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const signupSchema = z
  .object({
    email: z.string().email('Invalid email'),
    password: z.string().min(8, 'Password must be at least 8 characters'),
    confirmPassword: z.string(),
    acceptTerms: z.literal(true, {
      errorMap: () => ({ message: 'You must accept the terms' }),
    }),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
  });

type SignupForm = z.infer<typeof signupSchema>;

describe('Form validation with zodResolver', () => {
  it('should validate all fields on submit', async () => {
    const { result } = renderHook(() =>
      useForm<SignupForm>({
        resolver: zodResolver(signupSchema),
      })
    );

    await act(async () => {
      await result.current.handleSubmit(() => {})();
    });

    await waitFor(() => {
      expect(result.current.formState.errors.email).toBeDefined();
      expect(result.current.formState.errors.password).toBeDefined();
      expect(result.current.formState.errors.acceptTerms).toBeDefined();
    });
  });

  it('should show password mismatch error on confirmPassword', async () => {
    const { result } = renderHook(() =>
      useForm<SignupForm>({
        resolver: zodResolver(signupSchema),
        defaultValues: {
          email: 'user@example.com',
          password: 'Str0ngP@ss!',
          confirmPassword: 'DifferentPass1!',
          acceptTerms: true,
        },
      })
    );

    await act(async () => {
      await result.current.handleSubmit(() => {})();
    });

    await waitFor(() => {
      expect(result.current.formState.errors.confirmPassword?.message).toBe(
        'Passwords do not match'
      );
    });
  });

  it('should clear errors when valid data is provided', async () => {
    const { result } = renderHook(() =>
      useForm<SignupForm>({
        resolver: zodResolver(signupSchema),
        mode: 'onChange',
      })
    );

    // Trigger validation with invalid data
    await act(async () => {
      result.current.setValue('email', 'invalid');
      await result.current.trigger('email');
    });

    expect(result.current.formState.errors.email).toBeDefined();

    // Fix the value
    await act(async () => {
      result.current.setValue('email', 'valid@example.com');
      await result.current.trigger('email');
    });

    expect(result.current.formState.errors.email).toBeUndefined();
  });
});
```

## Best Practices

1. **Use `safeParse` in tests, not `parse`** -- `safeParse` returns a result object that you can assert on. Using `parse` throws an exception which is harder to assert specific error details against.
2. **Test both valid and invalid inputs for every field** -- Schema tests should verify acceptance of good data and rejection of bad data. Use `it.each` for comprehensive boundary testing.
3. **Verify error messages explicitly** -- Custom error messages are part of the user experience. Assert on the exact message string to catch accidental changes.
4. **Test transforms separately from validation** -- First verify the transform produces correct output, then verify validations on the transformed value in separate test cases.
5. **Use test helpers to reduce boilerplate** -- Create `expectZodError`, `expectValid`, and `expectInvalid` utilities that make test assertions more readable and consistent.
6. **Test schema composition** -- When using `.pick()`, `.omit()`, `.extend()`, `.merge()`, or `.partial()`, verify the derived schema independently to catch inheritance issues.
7. **Test coercion for API query params** -- Schemas used with query strings should have `z.coerce` for numbers and booleans. Test with string inputs to verify coercion works.
8. **Verify `.flatten()` and `.format()` output** -- If your UI consumes flattened or formatted errors, test those specific output shapes to prevent regression.
9. **Test default values** -- When schemas use `.default()`, verify that omitting the field produces the expected default in the parsed output.
10. **Pin your Zod version** -- Schema behavior can subtly change between Zod versions. Pin the exact version and run the full test suite before upgrading.

## Anti-Patterns to Avoid

1. **Testing Zod library behavior instead of your schemas** -- Do not test that `z.string()` rejects numbers. Test your specific schema constraints and custom error messages.
2. **Using `parse` and catching exceptions for assertions** -- This pattern is fragile and verbose. Use `safeParse` instead for cleaner test assertions.
3. **Only testing the happy path** -- A schema test that only validates correct data is nearly useless. Most schema bugs manifest as incorrect acceptance or rejection of edge cases.
4. **Duplicating schema logic in tests** -- Do not rewrite validation logic in your test to compare against. Test the schema directly with known input/output pairs.
5. **Ignoring error paths in nested objects** -- When a nested field fails validation, verify the error path (e.g., `['items', 0, 'price']`) to ensure error mapping works correctly in forms.
6. **Not testing `.optional()` and `.nullable()` fields** -- Verify that optional fields accept `undefined` and nullable fields accept `null`. Also verify they reject other falsy values.
7. **Forgetting to test schema reuse** -- If the same schema is used in multiple contexts (create, update, search), test each usage independently to catch issues with `.partial()` or `.omit()`.
8. **Hardcoding UUIDs and dates in tests** -- Use fixture factories or `faker` to generate test data. Hardcoded values make tests brittle and harder to understand.
9. **Not testing the integration boundary** -- Unit testing schemas in isolation is necessary but not sufficient. Always add integration tests that exercise the schema through the actual API or form handler.
10. **Skipping coercion edge cases** -- `z.coerce.number()` parses `""` as `0` and `"true"` as `NaN`. Test these surprising coercion behaviors to avoid production bugs.

## Running Tests

- Run all schema tests: `pnpm vitest run __tests__/schemas`
- Run with coverage: `pnpm vitest run __tests__/schemas --coverage`
- Watch mode: `pnpm vitest __tests__/schemas`
- Run integration tests: `pnpm vitest run __tests__/integration`
- Run a specific schema test: `pnpm vitest run __tests__/schemas/product.schema.test.ts`
- Type-check schemas: `pnpm tsc --noEmit`

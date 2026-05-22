---
name: zustand-rhf-state-synchronization
version: "1.0"
description: >
  Form-to-store data flow patterns for integrating React Hook Form with Zustand.
  PROACTIVELY activate for: (1) submitting form data to Zustand stores, (2) pre-populating forms from store state, (3) maintaining type consistency between forms and stores.
  Triggers: "form state sync", "submit to store", "form zustand"
group: state-forms
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Zustand + React Hook Form State Synchronization

## Architectural Pattern

**Unidirectional Data Flow**:
```
User Input -> Form State (RHF) -> Validation (Zod) -> Submit -> Zustand Store
```

- **React Hook Form**: Manages transactional form state during editing
- **Zustand**: Manages persistent application state after validation

## Pattern 1: Form Submission to Store

```typescript
'use client'

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { userProfileSchema, type UserProfileData } from '@/lib/schemas/user-profile-schema';
import { useUserStore } from '@/lib/stores/user-store';

export function ProfileForm() {
  // Get Zustand store action
  const updateProfile = useUserStore((state) => state.updateProfile);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<UserProfileData>({
    resolver: zodResolver(userProfileSchema),
  });

  const onSubmit = async (data: UserProfileData) => {
    try {
      // 1. Validate (handled by Zod/RHF)
      // 2. Submit to API
      const response = await fetch('/api/profile', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (!response.ok) throw new Error('Update failed');

      // 3. Update Zustand store with validated data
      updateProfile(data);

      // 4. Show success feedback
      alert('Profile updated!');
    } catch (error) {
      console.error('Update failed:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  );
}
```

## Pattern 2: Pre-populating Form from Store (Edit Mode)

```typescript
'use client'

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useEffect } from 'react';
import { userProfileSchema, type UserProfileData } from '@/lib/schemas/user-profile-schema';
import { useUserStore } from '@/lib/stores/user-store';

export function EditProfileForm() {
  // Get data from Zustand store
  const profile = useUserStore((state) => state.profile);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<UserProfileData>({
    resolver: zodResolver(userProfileSchema),
    defaultValues: {
      name: profile?.name ?? '',
      email: profile?.email ?? '',
      bio: profile?.bio ?? '',
    },
  });

  // Update form when store data changes
  useEffect(() => {
    if (profile) {
      reset({
        name: profile.name,
        email: profile.email,
        bio: profile.bio,
      });
    }
  }, [profile, reset]);

  const onSubmit = async (data: UserProfileData) => {
    // Submit and update store
  };

  return <form onSubmit={handleSubmit(onSubmit)}>{/* Fields */}</form>;
}
```

## Type Consistency (CRITICAL)

The same Zod-inferred type MUST be used in both form and store:

```typescript
// lib/schemas/user-schema.ts
import { z } from 'zod';

export const userSchema = z.object({
  name: z.string(),
  email: z.string().email(),
});

// Single source of truth for type
export type UserData = z.infer<typeof userSchema>;

// lib/stores/user-store.ts
import { type UserData } from '@/lib/schemas/user-schema';

interface UserStore {
  user: UserData | null;  // Same type from schema
  updateUser: (data: UserData) => void;
}

// components/forms/UserForm.tsx
import { type UserData } from '@/lib/schemas/user-schema';

const { register } = useForm<UserData>({  // Same type from schema
  resolver: zodResolver(userSchema),
});
```

## Complete Integration Example

**Schema:**
```typescript
// lib/schemas/product-schema.ts
import { z } from 'zod';

export const productSchema = z.object({
  name: z.string().min(1, 'Name required'),
  price: z.number().positive('Price must be positive'),
  category: z.enum(['electronics', 'clothing', 'food']),
});

export type ProductData = z.infer<typeof productSchema>;
```

**Store:**
```typescript
// lib/stores/product-store.ts
import { create } from 'zustand';
import { persist, devtools } from 'zustand/middleware';
import { type ProductData } from '@/lib/schemas/product-schema';

interface ProductStore {
  products: ProductData[];
  addProduct: (product: ProductData) => void;
  updateProduct: (index: number, product: ProductData) => void;
}

export const useProductStore = create<ProductStore>()(
  devtools(
    persist(
      (set) => ({
        products: [],

        addProduct: (product) => set((state) => ({
          products: [...state.products, product],
        })),

        updateProduct: (index, product) => set((state) => ({
          products: state.products.map((p, i) =>
            i === index ? product : p
          ),
        })),
      }),
      { name: 'product-storage' }
    )
  )
);
```

**Form:**
```typescript
// components/forms/ProductForm.tsx
'use client'

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { productSchema, type ProductData } from '@/lib/schemas/product-schema';
import { useProductStore } from '@/lib/stores/product-store';

interface ProductFormProps {
  editIndex?: number; // For edit mode
  initialData?: ProductData; // Pre-populate for editing
}

export function ProductForm({ editIndex, initialData }: ProductFormProps) {
  const addProduct = useProductStore((state) => state.addProduct);
  const updateProduct = useProductStore((state) => state.updateProduct);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<ProductData>({
    resolver: zodResolver(productSchema),
    defaultValues: initialData ?? {
      name: '',
      price: 0,
      category: 'electronics',
    },
  });

  const onSubmit = async (data: ProductData) => {
    try {
      // Submit to API
      const response = await fetch('/api/products', {
        method: editIndex !== undefined ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (!response.ok) throw new Error('Save failed');

      // Update store
      if (editIndex !== undefined) {
        updateProduct(editIndex, data);
      } else {
        addProduct(data);
      }

      // Reset form
      reset();

      alert(editIndex !== undefined ? 'Product updated!' : 'Product added!');
    } catch (error) {
      console.error('Save failed:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label>Name</label>
        <input {...register('name')} />
        {errors.name && <p className="error">{errors.name.message}</p>}
      </div>

      <div>
        <label>Price</label>
        <input
          type="number"
          step="0.01"
          {...register('price', { valueAsNumber: true })}
        />
        {errors.price && <p className="error">{errors.price.message}</p>}
      </div>

      <div>
        <label>Category</label>
        <select {...register('category')}>
          <option value="electronics">Electronics</option>
          <option value="clothing">Clothing</option>
          <option value="food">Food</option>
        </select>
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting
          ? 'Saving...'
          : editIndex !== undefined
          ? 'Update Product'
          : 'Add Product'}
      </button>
    </form>
  );
}
```

## Anti-Patterns

### Two-Way Binding (Real-time Sync)

```typescript
// WRONG: Updating store on every keystroke defeats RHF performance
<input
  {...register('name')}
  onChange={(e) => {
    updateStore({ name: e.target.value }); // Bad!
  }}
/>

// CORRECT: Update store only on submission
const onSubmit = (data) => {
  updateStore(data); // Good!
};
```

### Type Mismatch

```typescript
// WRONG: Different types
interface StoreType {
  email: string;
  name: string;
}

interface FormType {  // Separate type!
  email: string;
  username: string; // Different field name
}

// CORRECT: Same type from Zod
type UserData = z.infer<typeof userSchema>;

interface UserStore {
  user: UserData;  // Same type
}

const { register } = useForm<UserData>(); // Same type
```

## Summary

Form-Store integration pattern:
- React Hook Form manages transactional form state
- Zustand stores persistent application state
- Data flows: Form -> Validation -> Submission -> Store
- Same Zod-inferred type used in form and store
- Pre-populate forms with `defaultValues` from store
- Update store only after successful validation and submission
- NO real-time two-way binding (defeats performance)

---

**Related Skills**: `zustand-v5-typed-store-creation`, `rhf-zod-schema-integration`

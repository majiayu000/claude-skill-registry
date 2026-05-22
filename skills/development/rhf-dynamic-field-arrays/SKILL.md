---
name: rhf-dynamic-field-arrays
version: "1.0"
description: >
  React Hook Form useFieldArray for dynamic list management with Zod validation.
  PROACTIVELY activate for: (1) creating dynamic form arrays with add/remove, (2) validating arrays with Zod min/max, (3) using field.id as key.
  Triggers: "field array", "useFieldArray", "dynamic form"
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

# React Hook Form Dynamic Field Arrays

## useFieldArray Hook

For forms with dynamic lists of inputs (team members, invoice items, etc.):

```typescript
import { useForm, useFieldArray } from 'react-hook-form';

const { control } = useForm<FormData>();

const { fields, append, prepend, remove, insert, move } = useFieldArray({
  control, // Required: control from useForm
  name: 'items', // Required: name of array field
});
```

## Complete Example: Team Members Form

```typescript
'use client'

import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// 1. Define schema with array validation
const teamSchema = z.object({
  teamName: z.string().min(1, 'Team name required'),
  members: z.array(
    z.object({
      name: z.string().min(1, 'Name required'),
      email: z.string().email('Invalid email'),
      role: z.enum(['developer', 'designer', 'manager']),
    })
  ).min(1, 'At least one member required').max(10, 'Maximum 10 members'),
});

type TeamFormData = z.infer<typeof teamSchema>;

export function TeamForm() {
  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
  } = useForm<TeamFormData>({
    resolver: zodResolver(teamSchema),
    defaultValues: {
      teamName: '',
      members: [{ name: '', email: '', role: 'developer' }],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'members',
  });

  const onSubmit = (data: TeamFormData) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div>
        <label>Team Name</label>
        <input {...register('teamName')} />
        {errors.teamName && <p className="error">{errors.teamName.message}</p>}
      </div>

      <div>
        <div className="flex justify-between items-center mb-4">
          <h3>Team Members</h3>
          <button
            type="button"
            onClick={() => append({ name: '', email: '', role: 'developer' })}
          >
            Add Member
          </button>
        </div>

        {/* CRITICAL: Use field.id as key, NOT index */}
        {fields.map((field, index) => (
          <div key={field.id} className="border p-4 rounded mb-4">
            <div className="grid grid-cols-3 gap-4">
              <div>
                <label>Name</label>
                <input {...register(`members.${index}.name`)} />
                {errors.members?.[index]?.name && (
                  <p className="error">{errors.members[index]?.name?.message}</p>
                )}
              </div>

              <div>
                <label>Email</label>
                <input {...register(`members.${index}.email`)} />
                {errors.members?.[index]?.email && (
                  <p className="error">{errors.members[index]?.email?.message}</p>
                )}
              </div>

              <div>
                <label>Role</label>
                <select {...register(`members.${index}.role`)}>
                  <option value="developer">Developer</option>
                  <option value="designer">Designer</option>
                  <option value="manager">Manager</option>
                </select>
              </div>
            </div>

            <button
              type="button"
              onClick={() => remove(index)}
              disabled={fields.length === 1}
              className="mt-2 text-red-600"
            >
              Remove
            </button>
          </div>
        ))}

        {errors.members && (
          <p className="error">{errors.members.message}</p>
        )}
      </div>

      <button type="submit">Create Team</button>
    </form>
  );
}
```

## Array Manipulation Methods

```typescript
const { fields, append, prepend, remove, insert, move, swap } = useFieldArray({
  control,
  name: 'items',
});

// Add to end
append({ name: '', price: 0 });

// Add to beginning
prepend({ name: '', price: 0 });

// Remove by index
remove(2);

// Remove multiple
remove([0, 2, 4]);

// Insert at specific position
insert(2, { name: '', price: 0 });

// Move item from one position to another
move(2, 5);

// Swap two items
swap(2, 5);

// Replace entire array
fields.replace([{ name: 'Item 1', price: 10 }]);
```

## Zod Array Validation

```typescript
// Basic array
z.array(z.string())

// Array with min/max
z.array(z.string())
  .min(1, 'At least one item required')
  .max(5, 'Maximum 5 items')

// Array of objects
z.array(
  z.object({
    name: z.string().min(1, 'Required'),
    quantity: z.number().int().min(1),
  })
)

// Nonempty array
z.array(z.string()).nonempty('Cannot be empty')
```

## Nested Arrays

```typescript
const schema = z.object({
  sections: z.array(
    z.object({
      title: z.string(),
      items: z.array(
        z.object({
          name: z.string(),
          value: z.number(),
        })
      ),
    })
  ),
});

// Nested useFieldArray
function NestedForm() {
  const { control, register } = useForm<FormData>();

  const { fields: sections } = useFieldArray({
    control,
    name: 'sections',
  });

  return (
    <>
      {sections.map((section, sectionIndex) => (
        <div key={section.id}>
          <input {...register(`sections.${sectionIndex}.title`)} />
          <NestedItems control={control} sectionIndex={sectionIndex} />
        </div>
      ))}
    </>
  );
}

function NestedItems({ control, sectionIndex }: Props) {
  const { fields: items } = useFieldArray({
    control,
    name: `sections.${sectionIndex}.items`,
  });

  return (
    <>
      {items.map((item, itemIndex) => (
        <div key={item.id}>
          <input {...register(`sections.${sectionIndex}.items.${itemIndex}.name`)} />
        </div>
      ))}
    </>
  );
}
```

## Anti-Patterns

### Using Index as Key

```typescript
// WRONG: Using index as key
{fields.map((field, index) => (
  <div key={index}>...</div>
))}

// CORRECT: Using field.id as key
{fields.map((field, index) => (
  <div key={field.id}>...</div>
))}
```

**Why**: Using index as key causes state to persist incorrectly when items are reordered or removed.

### Incorrect Zod Schema

```typescript
// WRONG: Not wrapping in z.array()
const schema = z.object({
  items: z.object({ name: z.string() }) // Missing z.array()
});

// CORRECT: Wrapped in z.array()
const schema = z.object({
  items: z.array(z.object({ name: z.string() }))
});
```

## Summary

- Use `useFieldArray` for dynamic lists
- MUST use `field.id` as key (not index)
- Array validation with `z.array()`
- Manipulation methods: append, remove, insert, move
- Access errors with `errors.arrayName?.[index]?.fieldName`

---

**Related Skills**: `rhf-zod-schema-integration`, `zustand-rhf-state-synchronization`

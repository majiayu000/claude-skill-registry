---
name: collection
description: Generate a new Momentum CMS collection with fields, access control, and hooks
argument-hint: <collection-name>
---

# Generate Momentum CMS Collection

Create a new collection file following project conventions.

## Arguments

- `$ARGUMENTS` - Collection name (e.g., "posts", "products", "users")

## Important: Collection Location

All collections are defined in `libs/example-config/src/collections/`. Both example apps (`example-angular`, `example-analog`) import from `@momentumcms/example-config/collections`. **Never define collections in individual apps.**

## Steps

1. Create the collection file at `libs/example-config/src/collections/<name>.collection.ts`

2. Use this template:

```typescript
import {
  defineCollection,
  text,
  richText,
  number,
  date,
  checkbox,
  select,
  relationship,
} from '@momentumcms/core';

export const <PascalName> = defineCollection({
  slug: '<kebab-name>',

  admin: {
    useAsTitle: 'title', // or 'name' - the field to display as title
    defaultColumns: ['title', 'createdAt'],
    group: 'Content', // Admin sidebar group
  },

  access: {
    read: () => true,
    create: ({ req }) => !!req.user,
    update: ({ req }) => req.user?.role === 'admin',
    delete: ({ req }) => req.user?.role === 'admin',
  },

  hooks: {
    beforeChange: [],
    afterChange: [],
  },

  fields: [
    text('title', { required: true }),
    // Add more fields as needed
  ],
});
```

3. Export from `libs/example-config/src/collections/index.ts`:

```typescript
// Add import at top
import { <PascalName> } from './<name>.collection';

// Add to the collections array
export const collections: CollectionConfig[] = [
  // ... existing collections,
  <PascalName>,
];

// Add to named exports
export {
  // ... existing exports,
  <PascalName>,
};
```

Both example apps automatically pick up changes since they import from `@momentumcms/example-config/collections`.

4. Remind user: if migration mode is enabled, run `nx run <app>:migrate:generate` after collection changes to create a migration file.

## Field Types Available

### Text Input Fields
- `text(name, options)` - Short text with optional min/max length
- `textarea(name, options)` - Multi-line text with optional rows
- `richText(name, options)` - Rich text editor
- `email(name, options)` - Email input
- `password(name, options)` - Password input with optional min length

### Numeric & Date Fields
- `number(name, options)` - Numeric value with optional min/max/step
- `date(name, options)` - Date/datetime picker

### Boolean & Selection Fields
- `checkbox(name, options)` - Boolean checkbox
- `select(name, { options: [...] })` - Dropdown select (supports `hasMany`)
- `radio(name, { options: [...] })` - Radio button group

### Media & Files
- `upload(name, options)` - File upload with MIME type filtering

### Relationship & Data Fields
- `relationship(name, { collection: () => Ref })` - Reference to another collection (supports `hasMany`, polymorphic)
- `array(name, { fields: [...] })` - Array of nested fields
- `group(name, { fields: [...] })` - Nested object grouping
- `blocks(name, { blocks: [...] })` - Block-based content
- `json(name, options)` - Raw JSON field
- `point(name, options)` - Geolocation point
- `slug(name, { from: 'fieldName' })` - Auto-generated slug from another field

### Layout Fields (non-data storing)
- `tabs(tabs: [...])` - Tabbed sections for organization
- `collapsible(label, { fields: [...] })` - Collapsible section
- `row(fields: [...])` - Horizontal row layout

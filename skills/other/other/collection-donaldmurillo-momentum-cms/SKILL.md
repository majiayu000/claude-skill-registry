---
name: collection
description: Generate a new Momentum CMS collection with fields, access control, and hooks
argument-hint: <collection-name>
---

# Generate Momentum CMS Collection

Create a new collection file following project conventions.

## Arguments

- `$ARGUMENTS` - Collection name (e.g., "posts", "products", "pages")

## Steps

1. Create the collection file at `src/collections/<name>.collection.ts`

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

3. Add to momentum config. In `src/momentum.config.ts`, import and add to `collections` array:

```typescript
import { <PascalName> } from './collections/<name>.collection';

// In config:
collections: [Posts, <PascalName>],
```

4. Remind user to run schema generation:

```bash
npx drizzle-kit generate
npx drizzle-kit push
```

## Field Types Available

- `text(name, options)` - Short text (minLength, maxLength)
- `textarea(name, options)` - Multi-line text (rows, minLength, maxLength)
- `richText(name, options)` - Rich text editor
- `number(name, options)` - Numeric value (min, max, step)
- `date(name, options)` - Date/datetime
- `checkbox(name, options)` - Boolean
- `select(name, { options: [...] })` - Dropdown (hasMany for multi-select)
- `radio(name, { options: [...] })` - Radio buttons
- `email(name, options)` - Email with validation
- `upload(name, { relationTo: 'media' })` - File upload
- `relationship(name, { collection: () => Ref })` - Reference to another collection
- `array(name, { fields: [...] })` - Array of objects (minRows, maxRows)
- `group(name, { fields: [...] })` - Nested object
- `blocks(name, { blocks: [...] })` - Content blocks
- `json(name, options)` - Raw JSON
- `point(name, options)` - Geolocation (lat/lng)
- `slug(name, { from: 'title' })` - Auto-generated slug

## Layout Fields (visual only, no data storage)

- `tabs(name, { tabs: [{ label, fields }] })` - Tabbed sections
- `collapsible(name, { fields, defaultOpen })` - Expandable section
- `row(name, { fields })` - Horizontal row

## Access Control Helpers

```typescript
import {
	allowAll,
	denyAll,
	isAuthenticated,
	hasRole,
	hasAnyRole,
	isOwner,
	and,
	or,
	not,
} from '@momentumcms/core';
```

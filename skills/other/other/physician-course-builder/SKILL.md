---
name: physician-course-builder
description: Create and manage physician course preview lectures using the JSON-based lecture system. Use when adding new lectures for physician feedback, registering courses, or updating existing preview content.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Physician Course Preview Builder

## Overview

This skill creates JSON-based lectures for the physician course preview system. Lectures are rendered using the `UniversalLecture` component and are accessible via unlisted URLs for physician feedback before publication.

## System Architecture

```
content/
└── physician-courses/
    ├── registry.ts                    # Central registry (import lectures here)
    └── [physician-slug]/
        └── [course-slug]/
            └── lecture-N.json         # Individual lecture files

src/views/preview/
├── CourseCatalog.tsx                  # /preview/courses
├── PhysicianCourseIndex.tsx          # /preview/courses/:physician
└── PhysicianLectureViewer.tsx        # /preview/courses/:physician/:lectureSlug
```

## URL Structure

- **Catalog**: `/preview/courses`
- **Physician Index**: `/preview/courses/{physician-id}`
- **Lecture View**: `/preview/courses/{physician-id}/{course-id}-{lecture-number}`

Example: `/preview/courses/dr-abid-husain/new-biology-vascular-1`

## Creating a New Lecture

### Step 1: Create the Lecture JSON File

Location: `content/physician-courses/{physician-slug}/{course-slug}/lecture-N.json`

Use the JSON schema from `content/lectures/schema.ts`. Required fields:

```json
{
  "id": "course-slug-N",
  "title": "Lecture Title",
  "module": "Course Name",
  "duration": 45,
  "lastUpdated": "YYYY-MM-DD",
  "description": "Brief description",
  "level": "Foundational|Intermediate|Advanced",
  "tags": ["Tag1", "Tag2"],
  "slides": [...],
  "keyTakeaways": [...],
  "references": [...]
}
```

### Step 2: Register in registry.ts

Add the import and register the lecture:

```typescript
// Import at top of file
import drNewPhysicianLecture1 from './dr-new-physician/course-slug/lecture-1.json';

// Add to physicianRegistry
export const physicianRegistry: Record<string, PhysicianRegistry> = {
  'dr-new-physician': {
    physician: {
      id: 'dr-new-physician',
      name: 'Dr. New Physician',
      credentials: 'MD',
      specialty: 'Specialty Area',
    },
    courses: [
      {
        id: 'course-slug',
        title: 'Course Title',
        description: 'Course description',
        status: 'preview',
        lectures: [
          {
            id: 'lecture-1',
            title: 'Lecture Title',
            order: 1,
            lecture: drNewPhysicianLecture1 as Lecture,
          },
        ],
      },
    ],
  },
};
```

## Slide Structure

Each slide supports:

### Content Blocks (10 types)
- `paragraph` - Text paragraph
- `bullets` - Bullet list
- `numbered` - Numbered list
- `definition` - Term and definition
- `quote` - Quote with attribution
- `caseStudy` - Clinical case (scenario, approach, outcome)
- `formula` - Mathematical formula
- `comparisonText` - Side-by-side comparison items
- `highlight` - Highlighted text box
- `table` - Data table with headers and rows

### Callouts (5 types)
- `clinicalNote` - Clinical guidance
- `keyTakeaway` - Key point summary
- `evidence` - Research evidence (study + finding)
- `warning` - Important warnings
- `proTip` - Practical tips

### Diagrams (20 types)
Common types: `pathway`, `comparison`, `process`, `network`, `hierarchy`, `timeline`, `matrix`, `beforeAfter`

**IMPORTANT - Network Diagrams**: Use `edges` (not `links`):

**IMPORTANT - Hierarchy Diagrams**: Nodes only have `label`, `color`, `children` - NO `id` field:
```json
{
  "type": "hierarchy",
  "title": "Diagram Title",
  "root": {
    "label": "Root Node",
    "color": "gold",
    "children": [
      { "label": "Child 1", "color": "blue" },
      { "label": "Child 2", "color": "green" }
    ]
  }
}
```

**Network Diagram Example**:
```json
{
  "type": "network",
  "nodes": [...],
  "edges": [
    { "from": "node1", "to": "node2", "type": "unidirectional" }
  ]
}
```

**IMPORTANT - QuadrantDiagram:**
- Item text renders as WHITE on dark quadrant backgrounds
- Keep item names concise (1-3 words recommended)
- Example: "CoQ10", "BH4", "Beetroot" (good) vs "Coenzyme Q10 supplement" (too long)

**IMPORTANT - NetworkDiagram Labels:**
- Labels ≤10 characters: displayed INSIDE the node circle
- Labels >10 characters: displayed BELOW the node circle
- Keep labels concise for best visual appearance
- Example: "Gut", "Liver" (good) vs "Blood Vessel" (will render below circle)

## Coding Guidelines

### CRITICAL: Avoid Nested Anchor Tags

When using wouter's `<Link>` component, **DO NOT** nest `<a>` tags inside:

```tsx
// WRONG - causes hydration errors
<Link href="/path">
  <a className="...">Content</a>
</Link>

// CORRECT - pass props directly to Link
<Link
  href="/path"
  className="..."
  style={{...}}
>
  Content
</Link>
```

### CRITICAL: React Keys for List Rendering

Always provide unique, stable keys when rendering lists. Keys must be unique among siblings.

```tsx
// WRONG - missing key or using undefined property
{items.map((item) => (
  <div key={item.id}>{item.label}</div>  // If 'id' doesn't exist in schema!
))}

// CORRECT - use existing properties with index for uniqueness
{items.map((item, index) => (
  <div key={`${item.label}-${index}`}>{item.label}</div>
))}

// CORRECT - for hierarchical/nested data, include level for uniqueness
{node.children.map((child, index) => (
  <div key={`${child.label}-${level}-${index}`}>
    {renderNode(child, level + 1, index)}
  </div>
))}
```

**Key Points:**
- Schema types may not have `id` fields - check `content/lectures/schema.ts`
- For hierarchy diagrams: nodes only have `label`, `color`, `children` - NO `id` field
- Use label + level + index combination for unique keys in recursive structures
- Never assume a property exists - verify against the actual schema

### Component Patterns

For clickable cards/buttons:
```tsx
<Link
  href={`/preview/courses/${physicianId}/${lectureSlug}`}
  className="block p-6 rounded-lg transition-all hover:shadow-md"
  style={{ backgroundColor: colors.paperAlt }}
>
  <div>Card content here</div>
</Link>
```

## Workflow

1. **Create lecture JSON** in the physician's course folder
2. **Register** in `content/physician-courses/registry.ts`
3. **Test** at `/preview/courses/{physician}/{course-id}-{number}`
4. **Iterate** based on physician feedback
5. **Publish** by changing status to `published`

## Example Lecture JSON

See `content/physician-courses/dr-abid-husain/new-biology-vascular/lecture-1.json` for a complete example.

## Schema Reference

Full TypeScript types are in `content/lectures/schema.ts`:
- `Lecture` - Top-level lecture structure
- `Slide` - Individual slide with content, diagram, callouts
- `ContentBlock` - 10 content block types
- `Callout` - 5 callout types
- `Diagram` - 20 diagram types

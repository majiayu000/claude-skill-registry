---
name: information-architecting
description: Design and organize content structure, navigation systems, taxonomies, and information hierarchy for websites and applications. Use when planning content organization, designing navigation menus, creating taxonomies/categories, structuring database schemas for content, or organizing admin interfaces. Triggers on requests like "organize this content", "design the navigation", "create a taxonomy", "structure the information", or "plan the content hierarchy".
---

# Information Architecting

Design effective information structures for content management systems.

## Process

1. **Audit existing content** - Inventory all content types and relationships
2. **Identify user mental models** - How do users expect to find content?
3. **Design taxonomy** - Categories, tags, and hierarchies
4. **Plan navigation** - Primary, secondary, utility navigation
5. **Document relationships** - Content connections and cross-references

## Content Inventory

When auditing content, identify:

| Aspect | Questions |
|--------|-----------|
| Content Types | What distinct types exist? (articles, pages, media, users) |
| Relationships | How do types relate? (articles have tags, media belongs to articles) |
| Metadata | What attributes describe each type? |
| Lifecycle | Draft → Review → Published → Archived |
| Access | Who can view/edit each type? |

## Taxonomy Design

### Categories vs Tags
- **Categories**: Hierarchical, mutually exclusive, structural
- **Tags**: Flat, non-exclusive, descriptive

```
Categories (hierarchical):
├── News
│   ├── Industry News
│   └── Company News
├── Tutorials
│   ├── Beginner
│   └── Advanced
└── Case Studies

Tags (flat):
[react] [typescript] [cloudflare] [performance] [security]
```

### Naming Conventions
- Use clear, user-centric labels
- Avoid jargon unless domain-specific
- Keep names concise but descriptive
- Use consistent capitalization

## Navigation Patterns

### Primary Navigation
- 5-7 items maximum
- Most important/frequent destinations
- Consistent across all pages

### Secondary Navigation
- Contextual to current section
- Supports browsing within categories
- Breadcrumbs for orientation

### Utility Navigation
- Account, settings, search
- Consistent position (usually header)

## Database Schema Considerations

For D1/SQLite in this project:

```sql
-- Hierarchical categories
CREATE TABLE categories (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  parent_id INTEGER REFERENCES categories(id),
  sort_order INTEGER DEFAULT 0
);

-- Flat tags (existing pattern)
CREATE TABLE tags (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  slug TEXT UNIQUE NOT NULL
);

-- Many-to-many relationships
CREATE TABLE article_tags (
  article_id INTEGER REFERENCES articles(id),
  tag_id INTEGER REFERENCES tags(id),
  PRIMARY KEY (article_id, tag_id)
);
```

## CMS-Specific Patterns

### Admin Organization
```
/admin
├── Dashboard (overview, quick actions)
├── Content
│   ├── Articles
│   ├── Pages
│   └── Media
├── Taxonomy
│   ├── Categories
│   └── Tags
├── Users
└── Settings
```

### Public Site Structure
```
/                    # Home
├── /blog           # Article listing
│   └── /[slug]     # Article detail
├── /[page-slug]    # Static pages
├── /tag/[tag]      # Tag archive
└── /author/[id]    # Author archive
```

## Output

Provide information architecture deliverables:
1. Content type inventory with attributes
2. Taxonomy structure (categories/tags)
3. Navigation hierarchy
4. URL structure recommendations
5. Database schema changes (if needed)

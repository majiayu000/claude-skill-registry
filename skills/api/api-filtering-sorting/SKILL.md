---
name: api-filtering-sorting
description: Builds flexible API filtering and sorting systems with query parameter parsing, validation, and security. Use when implementing search endpoints, building data grids, or creating dynamic query APIs.
---

# API Filtering & Sorting

Build flexible filtering and sorting systems that handle complex queries efficiently.

## Query Parameter Syntax

```
GET /products?category=electronics&price[gte]=100&price[lte]=500&sort=-price,name
```

## Implementation (Node.js)

```javascript
const allowedFilters = ['category', 'status', 'price', 'createdAt'];
const allowedSorts = ['name', 'price', 'createdAt'];

app.get('/products', async (req, res) => {
  const filter = {};
  const sort = {};

  // Parse filters
  for (const [key, value] of Object.entries(req.query)) {
    if (key === 'sort') continue;

    const match = key.match(/^(\w+)\[(\w+)\]$/);
    if (match) {
      const [, field, operator] = match;
      if (!allowedFilters.includes(field)) continue;
      filter[field] = { [`$${operator}`]: parseValue(value) };
    } else if (allowedFilters.includes(key)) {
      filter[key] = value;
    }
  }

  // Parse sort
  if (req.query.sort) {
    for (const field of req.query.sort.split(',')) {
      const direction = field.startsWith('-') ? -1 : 1;
      const name = field.replace(/^-/, '');
      if (allowedSorts.includes(name)) sort[name] = direction;
    }
  }

  const products = await Product.find(filter).sort(sort);
  res.json({ data: products });
});

function parseValue(value) {
  if (value === 'true') return true;
  if (value === 'false') return false;
  if (!isNaN(value)) return Number(value);
  return value;
}
```

## Filter Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| eq | Equals | `?status=active` |
| ne | Not equals | `?status[ne]=deleted` |
| gt/gte | Greater than | `?price[gte]=100` |
| lt/lte | Less than | `?price[lte]=500` |
| in | In array | `?status[in]=active,pending` |
| like | Contains | `?name[like]=phone` |

## Security

- Whitelist allowed filter fields
- Validate input types per field
- Index frequently-filtered columns
- Limit query complexity
- Prevent SQL/NoSQL injection

## Best Practices

- Support common operators
- Cache filter option lists
- Monitor query performance
- Provide sensible defaults

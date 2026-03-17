---
name: api-pagination
description: Implements efficient API pagination using offset, cursor, and keyset strategies for large datasets. Use when building paginated endpoints, implementing infinite scroll, or optimizing database queries for collections.
---

# API Pagination

Implement scalable pagination strategies for handling large datasets efficiently.

## Pagination Strategies

| Strategy | Best For | Performance |
|----------|----------|-------------|
| Offset/Limit | Small datasets, simple UI | O(n) |
| Cursor | Infinite scroll, real-time | O(1) |
| Keyset | Large datasets | O(1) |

## Offset Pagination

```javascript
app.get('/products', async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = Math.min(parseInt(req.query.limit) || 20, 100);
  const offset = (page - 1) * limit;

  const [products, total] = await Promise.all([
    Product.find().skip(offset).limit(limit),
    Product.countDocuments()
  ]);

  res.json({
    data: products,
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit)
    }
  });
});
```

## Cursor Pagination

```javascript
app.get('/posts', async (req, res) => {
  const limit = 20;
  const cursor = req.query.cursor;

  const query = cursor
    ? { _id: { $gt: Buffer.from(cursor, 'base64').toString() } }
    : {};

  const posts = await Post.find(query).limit(limit + 1);
  const hasMore = posts.length > limit;
  if (hasMore) posts.pop();

  res.json({
    data: posts,
    nextCursor: hasMore ? Buffer.from(posts[posts.length - 1]._id).toString('base64') : null
  });
});
```

## Response Format

```json
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 150,
    "totalPages": 8
  },
  "links": {
    "first": "/api/products?page=1",
    "prev": "/api/products?page=1",
    "next": "/api/products?page=3",
    "last": "/api/products?page=8"
  }
}
```

## Best Practices

- Set reasonable max limits (e.g., 100)
- Use cursor pagination for large datasets
- Index sorting fields
- Avoid COUNT queries when possible
- Never allow unlimited page sizes

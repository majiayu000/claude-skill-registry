---
name: api-response-optimization
description: Optimizes API performance through payload reduction, caching strategies, and compression techniques. Use when improving API response times, reducing bandwidth usage, or implementing efficient caching.
---

# API Response Optimization

Reduce payload sizes, implement caching, and enable compression for faster APIs.

## Sparse Fieldsets

```javascript
// Allow clients to select fields: GET /users?fields=id,name,email
app.get('/users', async (req, res) => {
  const fields = req.query.fields?.split(',') || null;
  const users = await User.find({}, fields?.join(' '));
  res.json(users);
});
```

## HTTP Caching Headers

```javascript
app.get('/products/:id', async (req, res) => {
  const product = await Product.findById(req.params.id);
  const etag = crypto.createHash('md5').update(JSON.stringify(product)).digest('hex');

  if (req.headers['if-none-match'] === etag) {
    return res.status(304).end();
  }

  res.set({
    'Cache-Control': 'public, max-age=3600',
    'ETag': etag
  });
  res.json(product);
});
```

## Response Compression

```javascript
const compression = require('compression');

app.use(compression({
  filter: (req, res) => {
    if (req.headers['x-no-compression']) return false;
    return compression.filter(req, res);
  },
  level: 6  // Balance between speed and compression
}));
```

## Performance Targets

| Metric | Target |
|--------|--------|
| Response time | <100ms (from 500ms) |
| Payload size | <50KB (from 500KB) |
| Server CPU | <30% (from 80%) |

## Optimization Checklist

- [ ] Remove sensitive/unnecessary fields from responses
- [ ] Implement sparse fieldsets
- [ ] Add ETag/Last-Modified headers
- [ ] Enable gzip/brotli compression
- [ ] Use pagination for collections
- [ ] Eager load to prevent N+1 queries
- [ ] Monitor with APM tools

## Best Practices

- Cache immutable resources aggressively
- Use short TTL for frequently changing data
- Invalidate cache on writes
- Compress responses >1KB
- Profile before optimizing

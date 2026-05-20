---
name: api-pagination
description: Implement efficient pagination strategies for large datasets using offset/limit, cursor-based, and keyset pagination. Use when returning collections, managing large result sets, or optimizing query performance.
---

# API Pagination

## Overview

Implement scalable pagination strategies for handling large datasets with efficient querying, navigation, and performance optimization.

## When to Use

- Returning large collections of resources
- Implementing search results pagination
- Building infinite scroll interfaces
- Optimizing large dataset queries
- Managing memory in client applications
- Improving API response times

## Instructions

### 1. **Offset/Limit Pagination**

```javascript
// Node.js offset/limit implementation
app.get('/api/users', async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = Math.min(parseInt(req.query.limit) || 20, 100); // Max 100
  const offset = (page - 1) * limit;

  try {
    const [users, total] = await Promise.all([
      User.find()
        .skip(offset)
        .limit(limit)
        .select('id email firstName lastName createdAt'),
      User.countDocuments()
    ]);

    const totalPages = Math.ceil(total / limit);

    res.json({
      data: users,
      pagination: {
        page,
        limit,
        total,
        totalPages,
        hasNext: page < totalPages,
        hasPrev: page > 1
      },
      links: {
        self: `/api/users?page=${page}&limit=${limit}`,
        first: `/api/users?page=1&limit=${limit}`,
        last: `/api/users?page=${totalPages}&limit=${limit}`,
        ...(page > 1 && { prev: `/api/users?page=${page - 1}&limit=${limit}` }),
        ...(page < totalPages && { next: `/api/users?page=${page + 1}&limit=${limit}` })
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Python offset/limit
from flask import request
from sqlalchemy import func

@app.route('/api/users', methods=['GET'])
def list_users():
    page = request.args.get('page', 1, type=int)
    limit = min(request.args.get('limit', 20, type=int), 100)
    offset = (page - 1) * limit

    total = db.session.query(func.count(User.id)).scalar()
    users = db.session.query(User).offset(offset).limit(limit).all()

    total_pages = (total + limit - 1) // limit

    return jsonify({
        'data': [u.to_dict() for u in users],
        'pagination': {
            'page': page,
            'limit': limit,
            'total': total,
            'totalPages': total_pages,
            'hasNext': page < total_pages,
            'hasPrev': page > 1
        }
    }), 200
```

### 2. **Cursor-Based Pagination**

```javascript
// Cursor-based pagination for better performance
class CursorPagination {
  static encode(value) {
    return Buffer.from(String(value)).toString('base64');
  }

  static decode(cursor) {
    return Buffer.from(cursor, 'base64').toString('utf-8');
  }

  static generateCursor(resource) {
    return this.encode(`${resource.id}:${resource.createdAt.getTime()}`);
  }

  static parseCursor(cursor) {
    if (!cursor) return null;
    const decoded = this.decode(cursor);
    const [id, timestamp] = decoded.split(':');
    return { id, timestamp: parseInt(timestamp) };
  }
}

app.get('/api/users/cursor', async (req, res) => {
  const limit = Math.min(parseInt(req.query.limit) || 20, 100);
  const after = req.query.after ? CursorPagination.parseCursor(req.query.after) : null;

  try {
    const query = {};
    if (after) {
      query.createdAt = { $lt: new Date(after.timestamp) };
    }

    const users = await User.find(query)
      .sort({ createdAt: -1, _id: -1 })
      .limit(limit + 1)
      .select('id email firstName lastName createdAt');

    const hasMore = users.length > limit;
    const data = hasMore ? users.slice(0, limit) : users;
    const nextCursor = hasMore ? CursorPagination.generateCursor(data[data.length - 1]) : null;

    res.json({
      data,
      pageInfo: {
        hasNextPage: hasMore,
        endCursor: nextCursor,
        totalCount: await User.countDocuments()
      },
      links: {
        self: `/api/users/cursor?limit=${limit}`,
        next: nextCursor ? `/api/users/cursor?limit=${limit}&after=${nextCursor}` : null
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

### 3. **Keyset Pagination**

```javascript
// Keyset pagination (most efficient for large datasets)
app.get('/api/products/keyset', async (req, res) => {
  const limit = Math.min(parseInt(req.query.limit) || 20, 100);
  const lastId = req.query.lastId;
  const sortBy = req.query.sort || 'price'; // price or createdAt

  try {
    const query = {};

    // Build query based on sort field
    if (lastId) {
      const lastProduct = await Product.findById(lastId);

      if (sortBy === 'price') {
        query.$or = [
          { price: { $lt: lastProduct.price } },
          { price: lastProduct.price, _id: { $lt: lastId } }
        ];
      } else {
        query.$or = [
          { createdAt: { $lt: lastProduct.createdAt } },
          { createdAt: lastProduct.createdAt, _id: { $lt: lastId } }
        ];
      }
    }

    const products = await Product.find(query)
      .sort({ [sortBy]: -1, _id: -1 })
      .limit(limit + 1);

    const hasMore = products.length > limit;
    const data = hasMore ? products.slice(0, limit) : products;

    res.json({
      data,
      pageInfo: {
        hasMore,
        lastId: data.length > 0 ? data[data.length - 1]._id : null
      },
      links: {
        next: hasMore && data.length > 0
          ? `/api/products/keyset?lastId=${data[data.length - 1]._id}&sort=${sortBy}&limit=${limit}`
          : null
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

### 4. **Search Pagination**

```javascript
// Full-text search with pagination
app.get('/api/search', async (req, res) => {
  const query = req.query.q;
  const page = parseInt(req.query.page) || 1;
  const limit = Math.min(parseInt(req.query.limit) || 20, 100);
  const offset = (page - 1) * limit;

  if (!query) {
    return res.status(400).json({ error: 'Search query required' });
  }

  try {
    // MongoDB text search example
    const [results, total] = await Promise.all([
      Product.find(
        { $text: { $search: query } },
        { score: { $meta: 'textScore' } }
      )
        .sort({ score: { $meta: 'textScore' } })
        .skip(offset)
        .limit(limit),
      Product.countDocuments({ $text: { $search: query } })
    ]);

    const totalPages = Math.ceil(total / limit);

    res.json({
      query,
      results,
      pagination: {
        page,
        limit,
        total,
        totalPages
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Elasticsearch pagination
async function searchElasticsearch(query, page = 1, limit = 20) {
  const from = (page - 1) * limit;

  const response = await esClient.search({
    index: 'products',
    body: {
      from,
      size: limit,
      query: {
        multi_match: {
          query,
          fields: ['name^2', 'description', 'category']
        }
      }
    }
  });

  return {
    results: response.hits.hits.map(hit => hit._source),
    pagination: {
      page,
      limit,
      total: response.hits.total.value,
      totalPages: Math.ceil(response.hits.total.value / limit)
    }
  };
}
```

### 5. **Pagination Response Formats**

```json
// Offset/Limit Response
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 145,
    "totalPages": 8,
    "hasNext": true,
    "hasPrev": true
  },
  "links": {
    "self": "/api/users?page=2&limit=20",
    "first": "/api/users?page=1&limit=20",
    "prev": "/api/users?page=1&limit=20",
    "next": "/api/users?page=3&limit=20",
    "last": "/api/users?page=8&limit=20"
  }
}

// Cursor-Based Response
{
  "data": [...],
  "pageInfo": {
    "hasNextPage": true,
    "endCursor": "Y3JlYXRlZEF0OjE2NzA4ODA2MzU3NQ==",
    "totalCount": 1250
  },
  "links": {
    "next": "/api/users?limit=20&after=Y3JlYXRlZEF0OjE2NzA4ODA2MzU3NQ=="
  }
}

// Keyset Response
{
  "data": [...],
  "pageInfo": {
    "hasMore": true,
    "lastId": "507f1f77bcf86cd799439011"
  },
  "links": {
    "next": "/api/products?lastId=507f1f77bcf86cd799439011&sort=price"
  }
}
```

### 6. **Python Pagination (SQLAlchemy)**

```python
from flask import request, jsonify
from flask_sqlalchemy import Pagination

@app.route('/api/users', methods=['GET'])
def list_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)

    pagination: Pagination = User.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        'data': [user.to_dict() for user in pagination.items],
        'pagination': {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }), 200

# Cursor pagination with graphene
class UserNode(relay.Node):
    class Meta:
        model = User

    @classmethod
    def get_node(cls, info, id):
        return User.query.get(id)

class Query(graphene.ObjectType):
    users = relay.ConnectionField(UserNode)

    def resolve_users(self, info, **kwargs):
        return User.query.all()
```

## Best Practices

### ✅ DO
- Use cursor pagination for large datasets
- Set reasonable maximum limits (e.g., 100)
- Include total count when feasible
- Provide navigation links
- Document pagination strategy
- Use indexed fields for sorting
- Cache pagination results when appropriate
- Handle edge cases (empty results)
- Implement consistent pagination formats
- Use keyset for extremely large datasets

### ❌ DON'T
- Use offset with billions of rows
- Allow unlimited page sizes
- Count rows for every request
- Paginate without sorting
- Change sort order mid-pagination
- Use deep pagination without cursor
- Skip pagination for large datasets
- Expose database pagination directly
- Mix pagination strategies
- Ignore performance implications

## Performance Tips

- Index fields used for sorting
- Use database-native pagination
- Implement caching at application level
- Monitor query performance
- Use cursor pagination for large datasets
- Avoid COUNT queries when possible
- Consider denormalization for frequently accessed data

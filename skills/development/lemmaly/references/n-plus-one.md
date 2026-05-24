# N+1 query reference

The single most common performance bug shipped by AI assistants. One outer query, then one query per row.

## How to spot it

Any of these is N+1 until proven otherwise:

```js
// JS / TS
for (const user of users) {
  const posts = await db.post.findMany({ where: { userId: user.id } });
}

users.map(async u => await fetchProfile(u.id));        // hidden — runs in parallel but still N calls
await Promise.all(users.map(u => fetchProfile(u.id))); // parallel — still N HTTP calls
```

```python
# Python / Django
for user in users:
    posts = Post.objects.filter(user=user)              # N+1
    profile = user.profile                              # N+1 if not select_related

# SQLAlchemy
for user in session.query(User).all():
    print(user.posts)                                    # lazy load = N+1
```

```ruby
# Active Record
@users.each do |u|
  puts u.posts.count    # N+1 + extra count query
end
```

Heuristic: if the loop body calls anything that hits the DB, network, or filesystem — stop and batch.

## Fixes — by ORM

### Prisma (TS)
```ts
// Bad
for (const u of users) { u.posts = await db.post.findMany({ where: { userId: u.id } }); }

// Good — eager via include
const users = await db.user.findMany({ include: { posts: true } });

// Good — explicit batch
const posts = await db.post.findMany({ where: { userId: { in: users.map(u => u.id) } } });
const byUser = Map.groupBy(posts, p => p.userId);   // or reduce
```

### Drizzle (TS)
```ts
// Bad
for (const u of users) await db.select().from(posts).where(eq(posts.userId, u.id));

// Good
const all = await db.select().from(posts).where(inArray(posts.userId, users.map(u => u.id)));
```

### Django
```python
# Bad
for u in User.objects.all():
    print(u.profile.bio)              # N+1

# Good
for u in User.objects.select_related('profile'):    # FK / OneToOne — JOIN
    print(u.profile.bio)

for u in User.objects.prefetch_related('posts'):    # reverse FK / M2M — batched IN query
    print(list(u.posts.all()))
```

### SQLAlchemy
```python
# Bad: default lazy
users = session.query(User).all()
for u in users: u.posts            # N+1

# Good
from sqlalchemy.orm import selectinload, joinedload
users = session.query(User).options(selectinload(User.posts)).all()
```

### Active Record (Ruby)
```ruby
# Bad
@users.each { |u| u.posts.each { |p| ... } }

# Good
@users = User.includes(:posts)
```

## Raw SQL — the underlying fix

All ORMs are doing one of these under the hood:

```sql
-- JOIN (good for 1:1 and small 1:many)
SELECT u.*, p.*
FROM users u
LEFT JOIN posts p ON p.user_id = u.id
WHERE u.tenant_id = $1;

-- Two queries with IN (better when "many" is large — avoids row duplication)
SELECT * FROM users WHERE tenant_id = $1;
SELECT * FROM posts WHERE user_id IN ($1, $2, ..., $N);
```

Prefer the second form when the "many" side is wide. JOIN-then-group inflates payload by `O(parents * children)`.

## DataLoader pattern (when you can't restructure)

In GraphQL / per-request batching, where requests come in one at a time but you want to coalesce:

```ts
const userLoader = new DataLoader(async (ids) => {
  const users = await db.user.findMany({ where: { id: { in: ids } } });
  return ids.map(id => users.find(u => u.id === id));
});

// Now N parallel resolver calls become 1 batched query within the request tick.
await Promise.all(userIds.map(id => userLoader.load(id)));
```

## When N+1 is actually fine (rare)

- N is bounded and tiny (`n <= 5` forever, e.g. enum lookup).
- The "loop" is async-streaming over an unbounded source (e.g. event-by-event processing where batching would break correctness).
- Each call is to a different sharded service and cannot be batched.

In all these cases, **leave a comment** stating why this is intentional, otherwise the next pass will "fix" it back into an N+1.

## Quick mental test

Read the code aloud: "for each user, fetch its posts". If you say "for each X, fetch Y" — it's N+1. Rephrase as: "fetch all posts for these users."

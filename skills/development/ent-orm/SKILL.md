---
name: Ent ORM
description: Facebook's entity framework for Go with code generation.
metadata:
  labels: [golang, ent, orm, database]
  triggers:
    files: ['ent/schema/*.go', 'ent/generate.go']
    keywords: [ent, entgo, schema, Field, Edge]
---

# Ent ORM Standards

## Schema Definition

```go
// ent/schema/user.go
package schema

import (
    "entgo.io/ent"
    "entgo.io/ent/schema/field"
    "entgo.io/ent/schema/edge"
)

type User struct {
    ent.Schema
}

func (User) Fields() []ent.Field {
    return []ent.Field{
        field.String("name").NotEmpty(),
        field.String("email").Unique(),
        field.Int("age").Positive().Optional(),
        field.Time("created_at").Default(time.Now),
        field.Enum("role").Values("admin", "user").Default("user"),
    }
}

func (User) Edges() []ent.Edge {
    return []ent.Edge{
        edge.To("posts", Post.Type),
        edge.To("groups", Group.Type),
    }
}
```

## Code Generation

```bash
# Install
go install entgo.io/ent/cmd/ent@latest

# Generate
go generate ./ent

# New schema
ent new User
ent new Post
```

```go
// ent/generate.go
//go:generate go run -mod=mod entgo.io/ent/cmd/ent generate ./schema
package ent
```

## CRUD Operations

```go
// Create
user, err := client.User.
    Create().
    SetName("John").
    SetEmail("john@example.com").
    Save(ctx)

// Create bulk
users, err := client.User.
    CreateBulk(
        client.User.Create().SetName("A").SetEmail("a@x.com"),
        client.User.Create().SetName("B").SetEmail("b@x.com"),
    ).
    Save(ctx)

// Read
user, err := client.User.Get(ctx, id)
user, err := client.User.Query().
    Where(user.Email("john@example.com")).
    Only(ctx)

// Update
user, err := client.User.
    UpdateOneID(id).
    SetName("Jane").
    Save(ctx)

// Delete
err := client.User.DeleteOneID(id).Exec(ctx)
```

## Queries

```go
// Filter
users, err := client.User.Query().
    Where(
        user.AgeGT(18),
        user.RoleEQ(user.RoleAdmin),
    ).
    All(ctx)

// Or conditions
users, err := client.User.Query().
    Where(
        user.Or(
            user.RoleEQ(user.RoleAdmin),
            user.AgeGT(30),
        ),
    ).
    All(ctx)

// Order and limit
users, err := client.User.Query().
    Order(ent.Desc(user.FieldCreatedAt)).
    Limit(10).
    Offset(20).
    All(ctx)

// Select specific fields
names, err := client.User.Query().
    Select(user.FieldName).
    Strings(ctx)
```

## Edges (Relations)

```go
// Schema with edges
func (Post) Edges() []ent.Edge {
    return []ent.Edge{
        edge.From("author", User.Type).
            Ref("posts").
            Unique().
            Required(),
    }
}

// Query with edges
posts, err := client.User.Query().
    Where(user.ID(id)).
    QueryPosts().
    All(ctx)

// Eager loading
users, err := client.User.Query().
    WithPosts().
    WithGroups().
    All(ctx)

for _, u := range users {
    for _, p := range u.Edges.Posts {
        fmt.Println(p.Title)
    }
}
```

## Transactions

```go
tx, err := client.Tx(ctx)
if err != nil {
    return err
}
defer tx.Rollback()

user, err := tx.User.Create().
    SetName("John").
    Save(ctx)
if err != nil {
    return err
}

_, err = tx.Post.Create().
    SetTitle("First Post").
    SetAuthor(user).
    Save(ctx)
if err != nil {
    return err
}

return tx.Commit()
```

## Hooks

```go
func (User) Hooks() []ent.Hook {
    return []ent.Hook{
        hook.On(
            func(next ent.Mutator) ent.Mutator {
                return hook.UserFunc(func(ctx context.Context, m *ent.UserMutation) (ent.Value, error) {
                    // Before create/update
                    if name, ok := m.Name(); ok {
                        m.SetName(strings.TrimSpace(name))
                    }
                    return next.Mutate(ctx, m)
                })
            },
            ent.OpCreate|ent.OpUpdate,
        ),
    }
}
```

## Migrations

```go
// Auto migration (development)
if err := client.Schema.Create(ctx); err != nil {
    log.Fatalf("failed creating schema: %v", err)
}

// With options
err := client.Schema.Create(ctx,
    migrate.WithDropIndex(true),
    migrate.WithDropColumn(true),
)

// Versioned migrations (production)
// Use Atlas: https://atlasgo.io/
```

## Best Practices

1. **Code generation**: Run `go generate` after schema changes
2. **Edges**: Define both sides of relationships
3. **Transactions**: Use for related operations
4. **Hooks**: For validation, normalization
5. **Migrations**: Use Atlas for production

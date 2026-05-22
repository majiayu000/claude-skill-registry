---
name: gel
description: Gel (formerly EdgeDB) graph database schema design and querying. Use when designing Gel schemas, writing SDL, or querying with EdgeQL.
---

# Gel Database

Gel is a graph-relational database (formerly EdgeDB, rebranded February 2025). It combines relational data modeling with graph database relationships and a powerful query language (EdgeQL).

## CRITICAL

- **Always verify against latest docs**: https://docs.geldata.com/
- SDL syntax changed significantly in v3.0 - use current syntax
- Gel is NOT the same as Neo4j/GraphQL - it has its own paradigms

## Documentation

| Topic | URL |
|-------|-----|
| Main Docs | https://docs.geldata.com/ |
| Reference | https://docs.geldata.com/reference |
| Schema | https://docs.geldata.com/reference/datamodel |
| Object Types | https://docs.geldata.com/reference/datamodel/objects |
| Properties | https://docs.geldata.com/reference/datamodel/properties |
| Links | https://docs.geldata.com/reference/datamodel/links |
| Link Properties | https://docs.geldata.com/reference/datamodel/linkprops |
| Computeds | https://docs.geldata.com/reference/datamodel/computeds |
| Inheritance | https://docs.geldata.com/reference/datamodel/inheritance |
| Enums | https://docs.geldata.com/reference/stdlib/enum |
| Changelog | https://docs.geldata.com/resources/changelog/3_x |

## SDL Syntax (v3.0+)

Schema files use `.esdl` extension, typically in `dbschema/default.esdl`.

### Key Syntax Changes (v3.0)

- No `property` or `link` keywords needed for non-computed fields
- Colons instead of arrows: `name: str` not `name -> str`
- Computed links still require `link` keyword (prior to v4)
- Old arrow syntax still supported but not recommended

### Basic Object Type

```sdl
type Person {
  required name: str;           # required property
  email: str;                   # optional property
  age: int16;

  required employer: Company;   # required link (single)
  multi friends: Person;        # multi link (many)
}
```

### Constraints

```sdl
type User {
  required email: str {
    constraint exclusive;       # unique
  };
  required username: str {
    constraint exclusive;
    constraint min_len_value(3);
  };
}
```

### Enums

```sdl
scalar type Status extending enum<
  pending, active, completed, cancelled
>;

type Task {
  required status: Status {
    default := Status.pending;
  };
}
```

### Computed Properties and Backlinks

```sdl
type Movie {
  required title: str;
  multi actors: Person;
}

type Person {
  required name: str;

  # Computed backlink - all movies where this person is an actor
  multi link acted_in := .<actors[is Movie];

  # Computed property
  property movie_count := count(.acted_in);
}
```

Backlink syntax: `.<link_name[is Type]` returns all objects with a link named `link_name` pointing to current object.

## Link Properties (Edge Data)

Store metadata on the relationship itself, not the objects.

**When to use:** Best for many-to-many relationships where the link is a distinct concept with its own data.

**Constraints:** Link properties can only be primitive data (scalars, enums, arrays, tuples) - not links to other objects.

```sdl
type Person {
  required name: str;

  multi friends: Person {
    strength: int16;                    # how strong the friendship
    since: datetime;                    # when friendship started
    notes: str;
  };

  multi follows: Person {
    followed_at: datetime {
      default := datetime_of_statement();
    };
  };
}
```

### Querying Link Properties

Use `@` prefix to access link properties:

```edgeql
select Person {
  name,
  friends: {
    name,
    @strength,        # link property
    @since
  }
}
filter .name = 'Alice';
```

### Inserting with Link Properties

```edgeql
insert Person {
  name := 'Alice',
  friends := (
    select Person { @strength := 10, @since := <datetime>'2020-01-01' }
    filter .name = 'Bob'
  )
};
```

## Abstract Types and Inheritance

Create polymorphic, tagged-union style data models.

### Abstract Types (Mixins)

Can't create instances directly - used to share structure.

```sdl
abstract type HasTimestamps {
  created_at: datetime {
    default := datetime_current();
  };
  updated_at: datetime;
}

abstract type HasName {
  required first_name: str;
  required last_name: str;

  property full_name := .first_name ++ ' ' ++ .last_name;
}

type Person extending HasTimestamps, HasName {
  email: str;
}
```

### Polymorphic Subtypes (Tagged Union Pattern)

```sdl
abstract type Fact {
  required message: Message;
  label: str;
  extracted_at: datetime {
    default := datetime_current();
  };
}

type TrackingFact extending Fact {
  required tracking_number: str;
  carrier: str;
}

type DateFact extending Fact {
  required date_value: datetime;
  date_type: str;
}

type AmountFact extending Fact {
  required amount: decimal;
  currency: str {
    default := 'CAD';
  };
}
```

### Polymorphic Queries

```edgeql
# Query all facts, accessing subtype-specific properties
select Fact {
  label,
  extracted_at,

  # Type-specific fields using [is SubType]
  [is TrackingFact].tracking_number,
  [is TrackingFact].carrier,
  [is DateFact].date_value,
  [is AmountFact].amount
};

# Filter by subtype
select TrackingFact {
  tracking_number,
  carrier
}
filter .carrier = 'UPS';
```

### Polymorphic Links

Links can target abstract types:

```sdl
type Message {
  required content: str;
  multi facts: Fact;    # can link to any Fact subtype
}
```

## Project Setup

```bash
# Install Gel CLI
curl --proto '=https' --tlsv1.2 -sSf https://sh.geldata.com | sh

# Initialize project
gel project init

# Create migration after schema changes
gel migration create

# Apply migrations
gel migrate

# Interactive REPL
gel

# Generate TypeScript client
npx @gel/generate edgeql-js
```

## File Structure

```
project/
├── dbschema/
│   ├── default.esdl      # Main schema
│   └── migrations/       # Auto-generated migrations
├── gel.toml              # Project config
└── src/
    └── dbschema/         # Generated TS client (if using)
```

## Common Patterns

### Timestamps Mixin

```sdl
abstract type HasTimestamps {
  created_at: datetime {
    default := datetime_current();
    readonly := true;
  };
  updated_at: datetime {
    rewrite insert, update using (datetime_current())
  };
}
```

### Soft Delete

```sdl
abstract type SoftDeletable {
  deleted_at: datetime;
  property is_deleted := exists .deleted_at;
}

type Item extending SoftDeletable {
  required name: str;
}
```

### Self-Referential with Link Properties

```sdl
type Category {
  required name: str;

  parent: Category;
  multi link children := .<parent[is Category];

  property depth := (
    with recursive cat := .parent
    select count(cat)
  );
}
```

## Notes

- Gel is NOT eventually consistent - it's fully ACID
- Migrations are auto-generated from schema diffs
- TypeScript client provides full type safety
- EdgeQL is the query language, distinct from SQL or GraphQL
- Link properties are persisted differently - always single, not multi

## Attribution

Research compiled 2026-01-11 from:
- https://docs.geldata.com/
- https://docs.geldata.com/reference/datamodel/linkprops
- https://docs.geldata.com/reference/datamodel/inheritance
- https://docs.geldata.com/reference/datamodel/computeds
- https://docs.geldata.com/resources/changelog/3_x

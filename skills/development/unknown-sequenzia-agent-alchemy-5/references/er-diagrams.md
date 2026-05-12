# ER Diagrams Reference

Entity-Relationship diagrams model database schemas -- tables, columns, data types, primary/foreign keys, and relationships between entities.

**Keyword:** `erDiagram`

---

## Entity Declaration

### Basic entity with attributes

```mermaid
erDiagram
    USER {
        int id PK
        string email UK
        string name
        boolean active
        timestamp created_at
    }
```

### Attribute format

```
type name constraint
```

- **type** -- Data type (`int`, `string`, `boolean`, `float`, `date`, `timestamp`, `uuid`, `json`, `text`, `blob`)
- **name** -- Column name
- **constraint** -- Optional: `PK` (primary key), `FK` (foreign key), `UK` (unique key)

---

## Relationships

### Cardinality Notation

| Left | Right | Meaning |
|------|-------|---------|
| `\|\|` | `\|\|` | Exactly one to exactly one |
| `\|\|` | `o\|` | Exactly one to zero or one |
| `\|\|` | `\|{` | Exactly one to one or more |
| `\|\|` | `o{` | Exactly one to zero or more |
| `o\|` | `o\|` | Zero or one to zero or one |
| `o\|` | `o{` | Zero or one to zero or more |

### Reading the Notation

The symbols read as:
- `||` -- exactly one (mandatory)
- `o|` -- zero or one (optional)
- `|{` -- one or more (mandatory many)
- `o{` -- zero or more (optional many)

### Relationship Syntax

```
ENTITY_A cardinality--cardinality ENTITY_B : "label"
```

The `--` can be solid (`--`) for identifying relationships or dotted (`..`) for non-identifying.

### Identifying vs Non-Identifying

```
PARENT ||--|{ CHILD : "identifying"
PARENT ||..o{ RELATED : "non-identifying"
```

- **Identifying** (`--`): Child's existence depends on parent; FK is part of child's PK
- **Non-identifying** (`..`): Child can exist independently; FK is a regular column

---

## Common Relationship Patterns

### One-to-Many

```mermaid
erDiagram
    DEPARTMENT ||--o{ EMPLOYEE : "has"
    EMPLOYEE {
        int id PK
        string name
        int department_id FK
    }
    DEPARTMENT {
        int id PK
        string name
    }
```

### Many-to-Many (via junction table)

```mermaid
erDiagram
    STUDENT ||--o{ ENROLLMENT : "enrolls in"
    COURSE ||--o{ ENROLLMENT : "has"

    STUDENT {
        int id PK
        string name
    }
    COURSE {
        int id PK
        string title
    }
    ENROLLMENT {
        int id PK
        int student_id FK
        int course_id FK
        date enrolled_at
    }
```

### One-to-One

```mermaid
erDiagram
    USER ||--|| PROFILE : "has"

    USER {
        int id PK
        string email UK
    }
    PROFILE {
        int id PK
        int user_id FK "UK"
        string bio
        string avatar_url
    }
```

### Self-Referencing

```mermaid
erDiagram
    EMPLOYEE ||--o{ EMPLOYEE : "manages"
    EMPLOYEE {
        int id PK
        string name
        int manager_id FK
    }
```

---

## Styling

ER diagrams have limited styling options. Entity names should be clear and uppercase by convention.

Use short, descriptive relationship labels:
- `"places"`, `"contains"`, `"has"`, `"belongs to"`
- Avoid generic labels like `"relates to"`

---

## Complete Examples

### E-Commerce Schema

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    USER ||--o{ ADDRESS : "has"
    USER ||--|| CART : "owns"
    ORDER ||--|{ ORDER_ITEM : contains
    ORDER ||--|| PAYMENT : "paid via"
    ORDER }o--|| ADDRESS : "ships to"
    CART ||--o{ CART_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : "appears in"
    PRODUCT ||--o{ CART_ITEM : "added to"
    PRODUCT }o--|| CATEGORY : "belongs to"

    USER {
        uuid id PK
        string email UK
        string name
        string password_hash
        timestamp created_at
    }
    ORDER {
        uuid id PK
        uuid user_id FK
        uuid address_id FK
        string status
        float total
        timestamp created_at
    }
    ORDER_ITEM {
        uuid id PK
        uuid order_id FK
        uuid product_id FK
        int quantity
        float unit_price
    }
    PRODUCT {
        uuid id PK
        uuid category_id FK
        string name
        text description
        float price
        int stock
    }
    CATEGORY {
        uuid id PK
        string name
        string slug UK
    }
    ADDRESS {
        uuid id PK
        uuid user_id FK
        string street
        string city
        string country
        string postal_code
    }
    PAYMENT {
        uuid id PK
        uuid order_id FK "UK"
        string provider
        string status
        float amount
        timestamp processed_at
    }
    CART {
        uuid id PK
        uuid user_id FK "UK"
        timestamp updated_at
    }
    CART_ITEM {
        uuid id PK
        uuid cart_id FK
        uuid product_id FK
        int quantity
    }
```

### Blog CMS Schema

```mermaid
erDiagram
    AUTHOR ||--o{ POST : writes
    POST ||--o{ COMMENT : "has"
    POST ||--o{ POST_TAG : "tagged with"
    TAG ||--o{ POST_TAG : "applied to"
    AUTHOR ||--o{ COMMENT : "writes"
    POST }o--|| CATEGORY : "filed under"

    AUTHOR {
        uuid id PK
        string username UK
        string email UK
        string display_name
        text bio
        timestamp joined_at
    }
    POST {
        uuid id PK
        uuid author_id FK
        uuid category_id FK
        string title
        string slug UK
        text content
        string status
        timestamp published_at
        timestamp updated_at
    }
    COMMENT {
        uuid id PK
        uuid post_id FK
        uuid author_id FK
        text body
        timestamp created_at
    }
    TAG {
        uuid id PK
        string name UK
        string slug UK
    }
    POST_TAG {
        uuid post_id FK "PK"
        uuid tag_id FK "PK"
    }
    CATEGORY {
        uuid id PK
        string name UK
        string slug UK
        text description
    }
```

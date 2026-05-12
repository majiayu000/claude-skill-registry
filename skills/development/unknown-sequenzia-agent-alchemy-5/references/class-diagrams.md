# Class Diagrams Reference

Class diagrams model object-oriented structures -- classes, interfaces, relationships, and inheritance hierarchies.

**Keyword:** `classDiagram`

---

## Class Declaration

### Basic class

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound() void
    }
```

### Visibility Modifiers

| Symbol | Visibility |
|--------|-----------|
| `+` | Public |
| `-` | Private |
| `#` | Protected |
| `~` | Package/Internal |

### Method Signatures

```
+methodName(param1: Type, param2: Type) ReturnType
+staticMethod(input: String)$ String
+abstractMethod()* void
```

- `$` suffix -- static method
- `*` suffix -- abstract method

### Attributes

```
+attributeName: Type
-privateField: String
#protectedField: int
~internalField: boolean
```

---

## Annotations

Mark classes with stereotypes:

```mermaid
classDiagram
    class IRepository {
        <<interface>>
        +findById(id: string) Entity
        +save(entity: Entity) void
    }
    class AbstractBase {
        <<abstract>>
        #processData()* void
    }
    class Status {
        <<enumeration>>
        ACTIVE
        INACTIVE
        DELETED
    }
    class UserService {
        <<service>>
        +getUser(id: string) User
    }
```

Available annotations: `<<interface>>`, `<<abstract>>`, `<<enumeration>>`, `<<service>>`, or any custom text.

---

## Relationships

| Syntax | Type | Meaning |
|--------|------|---------|
| `A <\|-- B` | Inheritance | B extends A |
| `A <\|.. B` | Realization | B implements A |
| `A *-- B` | Composition | B is part of A (lifecycle coupled) |
| `A o-- B` | Aggregation | B belongs to A (independent lifecycle) |
| `A --> B` | Association | A uses B |
| `A ..> B` | Dependency | A depends on B |
| `A -- B` | Link | General association (no direction) |

### With Labels

```
A --> B : uses
A <|-- B : extends
```

### Cardinality

```
A "1" --> "many" B : contains
A "1" --> "0..1" B : optional
A "1..*" --> "*" B : maps to
```

Common cardinality notations: `1`, `0..1`, `1..*`, `*`, `n`, `0..n`, `1..n`

---

## Namespaces

Group classes into logical namespaces:

```mermaid
classDiagram
    namespace Domain {
        class User {
            +String email
            +String name
        }
        class Order {
            +Date createdAt
            +float total
        }
    }
    namespace Infrastructure {
        class UserRepository {
            +findById(id: string) User
        }
    }
    UserRepository ..> User
```

---

## Direction

Control diagram direction:

```
classDiagram
    direction LR
```

Options: `TB` (default), `BT`, `LR`, `RL`

---

## Styling

### Class-level styling

```
style User fill:#dbeafe,stroke:#2563eb,color:#000
```

### CSS classes

```
cssClass "User,Order" entityStyle
```

---

## Complete Examples

### Repository Pattern

```mermaid
classDiagram
    direction TB

    class IRepository~T~ {
        <<interface>>
        +findById(id: string) T
        +findAll() List~T~
        +save(entity: T) void
        +delete(id: string) void
    }
    class UserRepository {
        -db: Database
        +findById(id: string) User
        +findAll() List~User~
        +save(entity: User) void
        +delete(id: string) void
        -toEntity(row: Row) User
    }
    class UserService {
        -repository: IRepository~User~
        +createUser(data: CreateDTO) User
        +getUser(id: string) User
        +updateUser(id: string, data: UpdateDTO) User
    }
    class User {
        +string id
        +string email
        +string name
        +Date createdAt
    }
    class CreateDTO {
        +string email
        +string name
    }

    IRepository~T~ <|.. UserRepository : implements
    UserService --> IRepository~T~ : depends on
    UserService ..> User : returns
    UserService ..> CreateDTO : accepts
    UserRepository ..> User : produces

    style IRepository fill:#f3e8ff,stroke:#7c3aed,color:#000
    style UserRepository fill:#dbeafe,stroke:#2563eb,color:#000
    style UserService fill:#dbeafe,stroke:#2563eb,color:#000
    style User fill:#dcfce7,stroke:#16a34a,color:#000
    style CreateDTO fill:#fef3c7,stroke:#d97706,color:#000
```

### Observer Pattern

```mermaid
classDiagram
    direction LR

    class EventEmitter {
        <<abstract>>
        -listeners: Map~string, Function[]~
        +on(event: string, fn: Function) void
        +off(event: string, fn: Function) void
        +emit(event: string, data: any) void
    }
    class OrderService {
        +createOrder(data: OrderDTO) Order
        +cancelOrder(id: string) void
    }
    class EmailNotifier {
        +onOrderCreated(order: Order) void
        +onOrderCancelled(order: Order) void
    }
    class InventoryService {
        +onOrderCreated(order: Order) void
        +onOrderCancelled(order: Order) void
    }
    class AnalyticsTracker {
        +onOrderCreated(order: Order) void
    }

    EventEmitter <|-- OrderService : extends
    OrderService ..> EmailNotifier : notifies
    OrderService ..> InventoryService : notifies
    OrderService ..> AnalyticsTracker : notifies

    style EventEmitter fill:#f3e8ff,stroke:#7c3aed,color:#000
    style OrderService fill:#dbeafe,stroke:#2563eb,color:#000
    style EmailNotifier fill:#dcfce7,stroke:#16a34a,color:#000
    style InventoryService fill:#dcfce7,stroke:#16a34a,color:#000
    style AnalyticsTracker fill:#dcfce7,stroke:#16a34a,color:#000
```

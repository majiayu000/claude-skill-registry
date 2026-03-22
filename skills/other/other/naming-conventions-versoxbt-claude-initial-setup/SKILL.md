---
name: naming-conventions
description: >
  Enforce consistent naming conventions for variables, functions, files, and more.
  Use when the user names variables, functions, classes, files, database columns,
  or constants. Apply when reviewing code for naming consistency or when the user
  asks about naming best practices.
---

# Naming Conventions

Use clear, consistent names that reveal intent. Good names eliminate the need for comments and make code self-documenting.

## When to Use

- Naming any new variable, function, class, or file
- Reviewing code for naming consistency
- Refactoring unclear or misleading names
- Setting up project-wide naming standards
- Working across languages with different conventions

## Core Patterns

### Language-Specific Casing

```
JavaScript/TypeScript:
  variables, functions    camelCase       getUserById, isActive
  classes, types          PascalCase      UserService, AuthConfig
  constants               SCREAMING_SNAKE ALL_CAPS, MAX_RETRIES
  files (components)      PascalCase      UserProfile.tsx
  files (modules)         kebab-case      user-service.ts
  CSS classes             kebab-case      .nav-item, .btn-primary
  enums                   PascalCase      UserRole.Admin

Python:
  variables, functions    snake_case      get_user_by_id, is_active
  classes                 PascalCase      UserService, AuthConfig
  constants               SCREAMING_SNAKE MAX_RETRIES, API_URL
  files, modules          snake_case      user_service.py
  private                 _leading        _internal_helper

Go:
  exported                PascalCase      GetUserByID, UserService
  unexported              camelCase       getUserByID, parseToken
  files                   snake_case      user_service.go
  packages                lowercase       auth, users (no underscores)
  constants               PascalCase      MaxRetries, DefaultTimeout
  acronyms                ALL_CAPS        HTTPClient, UserID, JSONParser

Rust:
  variables, functions    snake_case      get_user, is_valid
  types, structs, enums   PascalCase      UserConfig, AuthError
  constants               SCREAMING_SNAKE MAX_RETRIES
  files                   snake_case      user_service.rs
  crates                  kebab-case      my-web-server

SQL/Database:
  tables                  snake_case      user_accounts
  columns                 snake_case      created_at, first_name
  indexes                 descriptive     idx_users_email
  foreign keys            descriptive     fk_orders_user_id
```

### Variable Naming

Names should describe WHAT the value represents, not HOW it was computed:

```typescript
// BAD: Vague or implementation-focused
const data = fetchUsers();
const list = getItems();
const val = calculateTotal();
const temp = transform(input);
const res = await api.get("/users");

// GOOD: Descriptive of content
const activeUsers = fetchUsers();
const cartItems = getItems();
const orderTotal = calculateTotal();
const normalizedEmail = transform(input);
const userResponse = await api.get("/users");
```

### Boolean Naming

Booleans should read as yes/no questions. Prefix with `is`, `has`, `can`, `should`, `was`, `will`:

```typescript
// BAD: Ambiguous booleans
const active = true;
const login = false;
const permission = true;
const visible = false;
const error = true;

// GOOD: Clear boolean intent
const isActive = true;
const hasLoggedIn = false;
const canEditPost = true;
const shouldShowModal = false;
const wasDeleted = true;

// BAD: Negative booleans (confusing double negatives)
const isNotValid = false;    // if (!isNotValid) — hard to read
const isDisabled = true;     // if (!isDisabled) — confusing

// GOOD: Positive booleans
const isValid = true;        // if (isValid) — clear
const isEnabled = false;     // if (isEnabled) — clear
```

### Function Naming

Functions perform actions. Name them with a verb that describes what they do:

```typescript
// Getters: get, find, fetch, load, retrieve
function getUserById(id: string): User { }
function findMatchingProducts(query: string): Product[] { }

// Creators: create, build, generate, make
function createOrder(items: CartItem[]): Order { }
function buildQueryString(params: Record<string, string>): string { }

// Transformers: parse, format, normalize, convert, to
function parseCSV(raw: string): Record<string, string>[] { }
function formatCurrency(amount: number): string { }
function toKebabCase(str: string): string { }

// Validators: validate, check, verify, ensure
function validateEmail(email: string): boolean { }
function ensureAuthenticated(req: Request): void { }

// Handlers: handle, on, process
function handleSubmit(event: FormEvent): void { }
function onUserCreated(user: User): void { }

// BAD: Unclear verbs
function doStuff(): void { }
function processData(data: unknown): unknown { }
function manageUser(user: User): void { }
```

### Collection Naming

Use plural nouns for collections, singular for individual items:

```typescript
// Collections: plural
const users: User[] = [];
const orderItems: OrderItem[] = [];
const activeSessionIds: Set<string> = new Set();

// Maps: describe the key-value relationship
const usersByEmail: Map<string, User> = new Map();
const pricePerProductId: Record<string, number> = {};
const rolePermissions: Record<Role, Permission[]> = {};

// Iteration: singular from plural
for (const user of users) { }
users.map((user) => user.name);
orders.filter((order) => order.status === "pending");
```

### Constants and Enums

```typescript
// Constants: SCREAMING_SNAKE for true constants
const MAX_RETRIES = 3;
const DEFAULT_PAGE_SIZE = 20;
const API_BASE_URL = "https://api.example.com";
const CACHE_TTL_MS = 60_000;

// Enums: PascalCase name and members
enum UserRole {
  Admin = "admin",
  Editor = "editor",
  Viewer = "viewer",
}

enum HttpStatus {
  Ok = 200,
  NotFound = 404,
  InternalError = 500,
}

// Union types (often preferred over enums in TypeScript)
type UserRole = "admin" | "editor" | "viewer";
type OrderStatus = "pending" | "processing" | "shipped" | "delivered";
```

## Anti-Patterns

### What NOT to Do

- **Single-letter variables** outside tiny loops: `x`, `d`, `u` — name them `index`, `document`, `user`.
- **Hungarian notation**: `strName`, `arrUsers`, `iCount` — the type system handles this.
- **Abbreviations**: `usr`, `msg`, `btn`, `mgr` — write `user`, `message`, `button`, `manager`.
- **Generic names**: `data`, `info`, `item`, `thing`, `stuff`, `temp`, `result` — describe what it actually is.
- **Inconsistent patterns**: `getUser` + `fetchOrder` + `loadProduct` in the same codebase — pick one verb family.
- **Encoding scope in name**: `globalConfig`, `localUser` — use module scope instead.

```typescript
// BAD
const d = new Date();
const cb = (err, res) => { };
const handleClick2 = () => { };
function processData(d) { }

// GOOD
const createdAt = new Date();
const onUserFetched = (error, response) => { };
const handleProfileUpdate = () => { };
function normalizeUserInput(rawInput) { }
```

## Quick Reference

```
Naming Rules:
  - Reveal intent: name describes WHAT, not HOW
  - Be specific: activeUsers > data
  - Be consistent: pick one convention per project
  - Avoid abbreviations: user, not usr
  - Match length to scope: wider scope = more descriptive name

Booleans:   is/has/can/should/was/will + adjective
Functions:  verb + noun (getUserById, formatDate)
Collections: plural noun (users, orderItems)
Constants:  SCREAMING_SNAKE (MAX_RETRIES)
Classes:    PascalCase noun (UserService)

Verbs by Category:
  Read:      get, find, fetch, load
  Create:    create, build, generate, make
  Update:    update, set, merge, patch
  Delete:    delete, remove, clear, reset
  Transform: parse, format, normalize, convert
  Validate:  validate, check, verify, ensure
  Handle:    handle, on, process
```

---
name: go-naming
description: Go naming conventions for packages, functions, methods, variables, constants, and receivers from Google and Uber style guides. Use when naming any identifier in Go code—choosing names for types, functions, methods, variables, constants, or packages—to ensure clarity, consistency, and idiomatic style.
---

# Go Naming Conventions

> **Normative**: Core naming rules (MixedCaps, no underscores) are required per
> Google's canonical Go style guide. Advisory guidance provides best practices
> for clarity and maintainability.

## Core Principle

Names should:
- Not feel repetitive when used
- Take context into consideration
- Not repeat concepts that are already clear

Naming is more art than science—Go names tend to be shorter than in other
languages.

---

## MixedCaps (Required)

> **Normative**: All Go identifiers must use MixedCaps.

Go uses `MixedCaps` or `mixedCaps` (camel case), never underscores (snake case).

```go
// Good
MaxLength    // exported constant
maxLength    // unexported constant
userID       // variable
URLParser    // type with initialism

// Bad
MAX_LENGTH   // no snake_case
max_length   // no underscores
User_Name    // no underscores in names
```

### Exceptions for Underscores

Names may contain underscores only in these cases:

1. **Test functions**: `TestFoo_InvalidInput`, `BenchmarkSort_LargeSlice`
2. **Generated code**: Package names only imported by generated code
3. **OS/cgo interop**: Low-level libraries matching OS identifiers (rare)

**Note**: Filenames are not Go identifiers and may contain underscores.

---

## Package Names

> **Normative**: Packages must be lowercase with no underscores.

Package names must be:
- Concise and lowercase only
- No underscores (e.g., `tabwriter` not `tab_writer`)
- Not likely to shadow common variables

```go
// Good: user, oauth2, k8s, tabwriter
// Bad: user_service (underscores), UserService (uppercase), count (shadows var)
```

### Avoid Uninformative Names

> **Advisory**: Don't use generic package names.

Avoid names that tempt users to rename on import: `util`, `common`, `helper`,
`model`, `base`. Prefer specific names: `stringutil`, `httpauth`, `configloader`.

### Import Renaming

When renaming imports, the local name must follow package naming rules:
`import foopb "path/to/foo_go_proto"` (not `foo_pb` with underscore).

---

## Interface Names

> **Advisory**: One-method interfaces use "-er" suffix.

By convention, one-method interfaces are named by the method name plus an `-er`
suffix to construct an agent noun:

```go
// Standard library examples
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
type Formatter interface { Format(f State, verb rune) }
type CloseNotifier interface { CloseNotify() <-chan bool }
```

Honor canonical method names (`Read`, `Write`, `Close`, `String`) and their
signatures. If your type implements a method with the same meaning as a
well-known type, use the same name—call it `String` not `ToString`.

---

## Receiver Names

> **Normative**: Receivers must be short abbreviations, used consistently.

Receiver variable names must be:
- Short (one or two letters)
- Abbreviations for the type itself
- Consistent across all methods of that type

| Long Name (Bad)             | Better Name              |
|-----------------------------|--------------------------|
| `func (tray Tray)`          | `func (t Tray)`          |
| `func (info *ResearchInfo)` | `func (ri *ResearchInfo)`|
| `func (this *ReportWriter)` | `func (w *ReportWriter)` |
| `func (self *Scanner)`      | `func (s *Scanner)`      |

```go
// Good - consistent short receiver
func (c *Client) Connect() error
func (c *Client) Send(msg []byte) error
func (c *Client) Close() error

// Bad - inconsistent or long receivers
func (client *Client) Connect() error
func (cl *Client) Send(msg []byte) error
func (this *Client) Close() error
```

---

## Constant Names

> **Normative**: Constants use MixedCaps, never ALL_CAPS or K prefix.

```go
// Good
const MaxPacketSize = 512
const defaultTimeout = 30 * time.Second

// Bad
const MAX_PACKET_SIZE = 512    // no snake_case
const kMaxBufferSize = 1024    // no K prefix
```

### Name by Role, Not Value

> **Advisory**: Constants should explain what the value denotes.

```go
// Good - names explain the role
const MaxRetries = 3
const DefaultPort = 8080

// Bad - names just describe the value
const Three = 3
const Port8080 = 8080
```

---

## Initialisms and Acronyms

> **Normative**: Initialisms maintain consistent case throughout.

Initialisms (URL, ID, HTTP, API) should be all uppercase or all lowercase:

| English   | Exported  | Unexported |
|-----------|-----------|------------|
| URL       | `URL`     | `url`      |
| ID        | `ID`      | `id`       |
| HTTP/API  | `HTTP`    | `http`     |
| gRPC/iOS  | `GRPC`/`IOS` | `gRPC`/`iOS` |

```go
// Good: HTTPClient, userID, ParseURL()
// Bad: HttpClient, orderId, ParseUrl()
```

---

## Function and Method Names

### Getters and Setters

> **Advisory**: Don't use `Get` prefix for simple accessors.

If you have a field called `owner` (unexported), the getter should be `Owner()`
(exported), not `GetOwner()`. The setter, if needed, is `SetOwner()`:

```go
// Good
owner := obj.Owner()
if owner != user {
    obj.SetOwner(user)
}

// Bad: c.GetName(), u.GetEmail(), p.GetID()
```

Use `Compute` or `Fetch` for expensive operations:
`db.FetchUser(id)`, `stats.ComputeAverage()`.

### Naming Conventions

> **Advisory**: Use noun-like names for getters, verb-like names for actions.

```go
// Noun-like for returning values
func (c *Config) JobName(key string) string
func (u *User) Permissions() []Permission

// Verb-like for actions
func (c *Config) WriteDetail(w io.Writer) error
```

### Type Suffixes

When functions differ only by type, include type at the end:
`ParseInt()`, `ParseInt64()`, `AppendInt()`, `AppendInt64()`.

For a clear "primary" version, omit the type:
`Marshal()` (primary), `MarshalText()` (variant).

---

## Variable Names

Variable naming balances brevity with clarity. Key principles:

- **Scope-based length**: Short names (`i`, `v`) for small scopes; longer,
  descriptive names for larger scopes
- **Single-letter conventions**: Use familiar patterns (`i` for index,
  `r`/`w` for reader/writer)
- **Avoid type in name**: Use `users` not `userSlice`, `name` not `nameString`
- **Prefix unexported globals**: Use `_` prefix for package-level unexported
  vars/consts to prevent shadowing

```go
// Good - scope-appropriate naming
for i, v := range items { ... }           // small scope
pendingOrders := filterPending(orders)    // larger scope

// Good - unexported global with prefix
const _defaultPort = 8080
```

**For detailed guidance**: See [references/VARIABLES.md](references/VARIABLES.md)

---

## Avoiding Repetition

Go names should not feel repetitive when used. Consider the full context:

- **Package + symbol**: `widget.New()` not `widget.NewWidget()`
- **Receiver + method**: `p.Name()` not `p.ProjectName()`
- **Context + type**: In package `sqldb`, use `Connection` not `DBConnection`

```go
// Bad - repetitive
func (c *Config) WriteConfigTo(w io.Writer) error
package db
func LoadFromDatabase() error  // db.LoadFromDatabase()

// Good - concise
func (c *Config) WriteTo(w io.Writer) error
package db
func Load() error              // db.Load()
```

**For detailed guidance**: See [references/REPETITION.md](references/REPETITION.md)

---

## Quick Reference

| Element | Rule | Example |
|---------|------|---------|
| Package | lowercase, no underscores | `package httputil` |
| Exported | MixedCaps, starts uppercase | `func ParseURL()` |
| Unexported | mixedCaps, starts lowercase | `func parseURL()` |
| Receiver | 1-2 letter abbreviation | `func (c *Client)` |
| Constant | MixedCaps, never ALL_CAPS | `const MaxSize = 100` |
| Initialism | consistent case | `userID`, `XMLAPI` |
| Variable | length ~ scope size | `i` (small), `userCount` (large) |

## See Also

- For interface design patterns: `go-interfaces`
- For core style principles: `go-style-core`
- For error handling patterns: `go-error-handling`
- For testing best practices: `go-testing`
- For defensive programming: `go-defensive`
- For performance optimization: `go-performance`

---
name: go-documentation
description: Guidelines for Go documentation including doc comments, package docs, godoc formatting, runnable examples, and signal boosting. Use when writing or reviewing documentation for Go packages, types, functions, or methods.
---

# Go Documentation

This skill covers documentation conventions from Google's Go Style Guide.

---

## Doc Comments

> **Normative**: All top-level exported names must have doc comments.

### Basic Rules

1. Begin with the name of the object being described
2. An article ("a", "an", "the") may precede the name
3. Use full sentences (capitalized, punctuated)

```go
// Good:
// A Request represents a request to run a command.
type Request struct { ...

// Encode writes the JSON encoding of req to w.
func Encode(w io.Writer, req *Request) { ...
```

### Struct Documentation

```go
// Good:
// Options configure the group management service.
type Options struct {
    // General setup:
    Name  string
    Group *FooGroup

    // Dependencies:
    DB *sql.DB

    // Customization:
    LargeGroupThreshold int // optional; default: 10
    MinimumMembers      int // optional; default: 2
}
```

Unexported types/functions with unobvious behavior should also have doc
comments. Use the same style to make future exporting easy.

---

## Comment Sentences

> **Normative**: Documentation comments must be complete sentences.

- Capitalize the first word, end with punctuation
- Exception: may begin with uncapitalized identifier if clear
- End-of-line comments for struct fields can be phrases:

```go
// Good:
// A Server handles serving quotes from Shakespeare.
type Server struct {
    // BaseDir points to the base directory for Shakespeare's works.
    //
    // Expected structure:
    //   {BaseDir}/manifest.json
    //   {BaseDir}/{name}/{name}-part{number}.txt
    BaseDir string

    WelcomeMessage  string // displayed when user logs in
    ProtocolVersion string // checked against incoming requests
    PageLength      int    // lines per page (optional; default: 20)
}
```

---

## Comment Line Length

> **Advisory**: Aim for ~80 columns, but no hard limit.

```text
# Good:
// This is a comment paragraph.
// The length of individual lines doesn't matter in Godoc;
// but the choice of wrapping makes it easy to read on narrow screens.
//
// Don't worry too much about the long URL:
// https://supercalifragilisticexpialidocious.example.com:8080/Animalia/Chordata/

# Bad:
// This is a comment paragraph. The length of individual lines doesn't matter in
Godoc;
// but the choice of wrapping causes jagged lines on narrow screens or in code
review.
```

Break based on punctuation. Don't split long URLs.

---

## Package Comments

> **Normative**: Every package must have exactly one package comment.

```go
// Good:
// Package math provides basic constants and mathematical functions.
//
// This package does not guarantee bit-identical results across architectures.
package math
```

### Main Packages

Use the binary name (matching the BUILD file):

```go
// Good:
// The seed_generator command is a utility that generates a Finch seed file
// from a set of JSON study configs.
package main
```

Valid styles: `Binary seed_generator`, `Command seed_generator`, `The
seed_generator command`, `Seed_generator ...`

**Tips:**
- For long package comments, use a `doc.go` file
- Maintainer comments after imports don't appear in Godoc

---

## Parameters and Configuration

> **Advisory**: Document error-prone or non-obvious parameters, not everything.

```go
// Bad: Restates the obvious
// Sprintf formats according to a format specifier and returns the resulting string.
//
// format is the format, and data is the interpolation data.
func Sprintf(format string, data ...any) string

// Good: Documents non-obvious behavior
// Sprintf formats according to a format specifier and returns the resulting string.
//
// The provided data is used to interpolate the format string. If the data does
// not match the expected format verbs or the amount of data does not satisfy
// the format specification, the function will inline warnings about formatting
// errors into the output string.
func Sprintf(format string, data ...any) string
```

---

## Contexts

> **Advisory**: Don't restate implied context behavior; document exceptions.

Context cancellation is implied to interrupt the function and return
`ctx.Err()`. Don't document this.

```go
// Bad: Restates implied behavior
// Run executes the worker's run loop.
//
// The method will process work until the context is cancelled.
func (Worker) Run(ctx context.Context) error

// Good: Just the essential
// Run executes the worker's run loop.
func (Worker) Run(ctx context.Context) error
```

**Document when behavior differs:**

```go
// Good: Non-standard cancellation behavior
// Run executes the worker's run loop.
//
// If the context is cancelled, Run returns a nil error.
func (Worker) Run(ctx context.Context) error

// Good: Special context requirements
// NewReceiver starts receiving messages sent to the specified queue.
// The context should not have a deadline.
func NewReceiver(ctx context.Context) *Receiver
```

---

## Concurrency

> **Advisory**: Document non-obvious thread safety characteristics.

Read-only operations are assumed safe; mutating operations are assumed unsafe.
Don't restate this.

**Document when:**

```go
// Ambiguous operation (looks read-only but mutates internally)
// Lookup returns the data associated with the key from the cache.
//
// This operation is not safe for concurrent use.
func (*Cache) Lookup(key string) (data []byte, ok bool)

// API provides synchronization
// NewFortuneTellerClient returns an *rpc.Client for the FortuneTeller service.
// It is safe for simultaneous use by multiple goroutines.
func NewFortuneTellerClient(cc *rpc.ClientConn) *FortuneTellerClient

// Interface has concurrency requirements
// A Watcher reports the health of some entity (usually a backend service).
//
// Watcher methods are safe for simultaneous use by multiple goroutines.
type Watcher interface {
    Watch(changed chan<- bool) (unwatch func())
    Health() error
}
```

---

## Cleanup

> **Advisory**: Always document explicit cleanup requirements.

```go
// Good:
// NewTicker returns a new Ticker containing a channel that will send the
// current time on the channel after each tick.
//
// Call Stop to release the Ticker's associated resources when done.
func NewTicker(d Duration) *Ticker

// Good: Show how to clean up
// Get issues a GET to the specified URL.
//
// When err is nil, resp always contains a non-nil resp.Body.
// Caller should close resp.Body when done reading from it.
//
//    resp, err := http.Get("http://example.com/")
//    if err != nil {
//        // handle error
//    }
//    defer resp.Body.Close()
//    body, err := io.ReadAll(resp.Body)
func (c *Client) Get(url string) (resp *Response, err error)
```

---

## Errors

> **Advisory**: Document significant error sentinel values and types.

```go
// Good: Document sentinel values
// Read reads up to len(b) bytes from the File and stores them in b.
//
// At end of file, Read returns 0, io.EOF.
func (*File) Read(b []byte) (n int, err error)

// Good: Document error types (include pointer receiver)
// Chdir changes the current working directory to the named directory.
//
// If there is an error, it will be of type *PathError.
func Chdir(dir string) error
```

Noting `*PathError` (not `PathError`) enables correct use of `errors.Is` and
`errors.As`.

For package-wide error conventions, document in the package comment.

---

## Examples

> **Advisory**: Provide runnable examples to demonstrate package usage.

Place examples in test files (`*_test.go`):

```go
// Good:
func ExampleConfig_WriteTo() {
    cfg := &Config{
        Name: "example",
    }
    if err := cfg.WriteTo(os.Stdout); err != nil {
        log.Exitf("Failed to write config: %s", err)
    }
    // Output:
    // {
    //   "name": "example"
    // }
}
```

Examples appear in Godoc attached to the documented element.

---

## Godoc Formatting

> **Advisory**: Use godoc syntax for well-formatted documentation.

**Paragraphs** - Separate with blank lines:

```go
// Good:
// LoadConfig reads a configuration out of the named file.
//
// See some/shortlink for config file format details.
```

**Verbatim/Code blocks** - Indent by two additional spaces:

```go
// Good:
// Update runs the function in an atomic transaction.
//
// This is typically used with an anonymous TransactionFunc:
//
//   if err := db.Update(func(state *State) { state.Foo = bar }); err != nil {
//     //...
//   }
```

**Lists and tables** - Use verbatim formatting:

```go
// Good:
// LoadConfig treats the following keys in special ways:
//   "import" will make this configuration inherit from the named file.
//   "env" if present will be populated with the system environment.
```

**Headings** - Single line, capital letter, no punctuation (except
parens/commas), followed by paragraph:

```go
// Good:
// Using headings
//
// Headings come with autogenerated anchor tags for easy linking.
```

---

## Named Result Parameters

> **Advisory**: Use for documentation when types alone aren't clear enough.

```go
// Good: Multiple params of same type
func (n *Node) Children() (left, right *Node, err error)

// Good: Action-oriented name clarifies usage
// The caller must arrange for the returned cancel function to be called.
func WithTimeout(parent Context, d time.Duration) (ctx Context, cancel func())

// Bad: Type already clear, name adds nothing
func (n *Node) Parent1() (node *Node)
func (n *Node) Parent2() (node *Node, err error)

// Good: Type is sufficient
func (n *Node) Parent1() *Node
func (n *Node) Parent2() (*Node, error)
```

Don't name results just to enable naked returns. Clarity > brevity.

---

## Signal Boosting

> **Advisory**: Add comments to highlight unusual or easily-missed patterns.

These two are hard to distinguish:

```go
if err := doSomething(); err != nil {  // common
    // ...
}

if err := doSomething(); err == nil {  // unusual!
    // ...
}
```

Add a comment to boost the signal:

```go
// Good:
if err := doSomething(); err == nil { // if NO error
    // ...
}
```

---

## Documentation Preview

> **Advisory**: Preview documentation before and during code review.

```bash
go install golang.org/x/pkgsite/cmd/pkgsite@latest
pkgsite
```

This validates godoc formatting renders correctly.

---

## Quick Reference

| Topic | Key Rule |
|-------|----------|
| Doc comments | Start with name, use full sentences |
| Line length | ~80 chars, prioritize readability |
| Package comments | One per package, above `package` clause |
| Parameters | Document non-obvious behavior only |
| Contexts | Document exceptions to implied behavior |
| Concurrency | Document ambiguous thread safety |
| Cleanup | Always document resource release |
| Errors | Document sentinels and types (note pointer) |
| Examples | Use runnable examples in test files |
| Formatting | Blank lines for paragraphs, indent for code |

---

## See Also

- **go-style-core** - Core Go style principles and formatting guidelines
- **go-naming** - Naming conventions for Go identifiers
- **go-linting** - Linting tools for documentation and code quality

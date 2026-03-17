---
name: go-packages
description: Go package organization, imports, and dependency management from Google and Uber style guides. Use when creating packages, organizing imports, managing dependencies, using init(), or deciding how to structure Go code into packages.
---

# Go Packages and Imports

This skill covers package organization and import management following Google's
and Uber's Go style guides.

---

## Package Organization

### Avoid Util Packages

> **Advisory**: This is a best practice recommendation.

Package names should describe what the package provides. Avoid generic names
like `util`, `helper`, `common`, or similar—they make code harder to read and
cause import conflicts.

```go
// Good: Meaningful package names
db := spannertest.NewDatabaseFromFile(...)
_, err := f.Seek(0, io.SeekStart)

// Bad: Vague package names obscure meaning
db := test.NewDatabaseFromFile(...)
_, err := f.Seek(0, common.SeekStart)
```

Generic names like `util` can be used as *part* of a name (e.g., `stringutil`)
but should not be the entire package name.

### Package Size

> **Advisory**: This is best practice guidance.

**When to combine packages:**
- If client code likely needs two types to interact, keep them together
- If types have tightly coupled implementations
- If users would need to import both packages to use either meaningfully

**When to split packages:**
- When something is conceptually distinct
- The short package name + exported type creates a meaningful identifier:
  `bytes.Buffer`, `ring.New`

**File organization:** No "one type, one file" convention in Go. Files should be
focused enough to know which file contains something and small enough to find
things easily.

---

## Imports

### Import Organization

> **Normative**: This is required per Go Wiki CodeReviewComments.

Imports are organized in groups, with blank lines between them. The standard
library packages are always in the first group.

```go
package main

import (
	"fmt"
	"hash/adler32"
	"os"

	"github.com/foo/bar"
	"rsc.io/goversion/version"
)
```

Use [goimports](https://pkg.go.dev/golang.org/x/tools/cmd/goimports) to manage
this automatically.

### Import Grouping (Extended)

> **Combined**: Google + Uber guidance

**Minimal grouping (Uber):** stdlib, then everything else.

**Extended grouping (Google):** stdlib → other → protocol buffers → side-effects.

```go
// Good: Standard library separate from external packages
import (
    "fmt"
    "os"

    "go.uber.org/atomic"
    "golang.org/x/sync/errgroup"
)
```

```go
// Good: Full grouping with protos and side-effects
import (
    "fmt"
    "os"

    "github.com/dsnet/compress/flate"
    "golang.org/x/text/encoding"

    foopb "myproj/foo/proto/proto"

    _ "myproj/rpc/protocols/dial"
)
```

### Import Renaming

> **Normative**: This is required per Go Wiki CodeReviewComments and Google's Go style guide.

Avoid renaming imports except to avoid a name collision; good package names
should not require renaming. In the event of collision, **prefer to rename the
most local or project-specific import**.

**Must rename:** collision with other imports, generated protocol buffer packages
(remove underscores, add `pb` suffix).

**May rename:** uninformative names (e.g., `v1`), collision with local variable.

```go
// Good: Proto packages renamed with pb suffix
import (
    foosvcpb "path/to/package/foo_service_go_proto"
)

// Good: urlpkg when url variable is needed
import (
    urlpkg "net/url"
)

func parseEndpoint(url string) (*urlpkg.URL, error) {
    return urlpkg.Parse(url)
}
```

### Blank Imports (`import _`)

> **Normative**: This is required per Go Wiki CodeReviewComments and Google's Go style guide.

Packages that are imported only for their side effects (using `import _ "pkg"`)
should only be imported in the main package of a program, or in tests that
require them.

```go
// Good: Blank import in main package
package main

import (
    _ "time/tzdata"
    _ "image/jpeg"
)
```

### Dot Imports (`import .`)

> **Normative**: This is required per Go Wiki CodeReviewComments and Google's Go style guide.

**Do not** use dot imports. They make programs much harder to read because it is
unclear whether a name like `Quux` is a top-level identifier in the current
package or in an imported package.

**Exception:** The `import .` form can be useful in tests that, due to circular
dependencies, cannot be made part of the package being tested:

```go
package foo_test

import (
	"bar/testutil" // also imports "foo"
	. "foo"
)
```

In this case, the test file cannot be in package `foo` because it uses
`bar/testutil`, which imports `foo`. So the `import .` form lets the file
pretend to be part of package `foo` even though it is not.

**Except for this one case, do not use `import .` in your programs.**

```go
// Bad: Dot import hides origin
import . "foo"
var myThing = Bar() // Where does Bar come from?

// Good: Explicit qualification
import "foo"
var myThing = foo.Bar()
```

---

## Avoid init()

> **Source**: Uber Go Style Guide

Avoid `init()` where possible. When `init()` is unavoidable, code should:

1. Be completely deterministic, regardless of program environment
2. Avoid depending on ordering or side-effects of other `init()` functions
3. Avoid global/environment state (env vars, working directory, args)
4. Avoid I/O (filesystem, network, system calls)

```go
// Bad: init() with I/O and environment dependencies
var _config Config

func init() {
    cwd, _ := os.Getwd()
    raw, _ := os.ReadFile(path.Join(cwd, "config.yaml"))
    yaml.Unmarshal(raw, &_config)
}
```

```go
// Good: Explicit function for loading config
func loadConfig() (Config, error) {
    cwd, err := os.Getwd()
    if err != nil {
        return Config{}, err
    }

    raw, err := os.ReadFile(path.Join(cwd, "config.yaml"))
    if err != nil {
        return Config{}, err
    }

    var config Config
    if err := yaml.Unmarshal(raw, &config); err != nil {
        return Config{}, err
    }
    return config, nil
}
```

**Acceptable uses of init():**
- Complex expressions that cannot be single assignments
- Pluggable hooks (e.g., `database/sql` dialects, encoding registries)
- Deterministic precomputation

---

## Exit in Main

> **Source**: Uber Go Style Guide

Call `os.Exit` or `log.Fatal*` **only in `main()`**. All other functions should
return errors to signal failure.

**Why this matters:**
- Non-obvious control flow: Any function can exit the program
- Difficult to test: Functions that exit also exit the test
- Skipped cleanup: `defer` statements are skipped

```go
// Bad: log.Fatal in helper function
func readFile(path string) string {
    f, err := os.Open(path)
    if err != nil {
        log.Fatal(err)  // Exits program, skips defers
    }
    b, err := io.ReadAll(f)
    if err != nil {
        log.Fatal(err)
    }
    return string(b)
}
```

```go
// Good: Return errors, let main() decide to exit
func main() {
    body, err := readFile(path)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(body)
}

func readFile(path string) (string, error) {
    f, err := os.Open(path)
    if err != nil {
        return "", err
    }
    b, err := io.ReadAll(f)
    if err != nil {
        return "", err
    }
    return string(b), nil
}
```

### Exit Once

Prefer to call `os.Exit` or `log.Fatal` **at most once** in `main()`. Extract
business logic into a separate function that returns errors.

```go
// Good: Single exit point with run() pattern
func main() {
    if err := run(); err != nil {
        log.Fatal(err)
    }
}

func run() error {
    args := os.Args[1:]
    if len(args) != 1 {
        return errors.New("missing file")
    }

    f, err := os.Open(args[0])
    if err != nil {
        return err
    }
    defer f.Close()  // Will always run

    b, err := io.ReadAll(f)
    if err != nil {
        return err
    }

    // Process b...
    return nil
}
```

**Benefits of the `run()` pattern:**
- Short `main()` function with single exit point
- All business logic is testable
- `defer` statements always execute

---

## Quick Reference

| Topic | Rule | Type |
|-------|------|------|
| Import organization | std first, groups separated by blank lines | Normative |
| Import grouping | std → other (→ proto → side-effect) | Combined |
| Import renaming | Only when necessary; prefer renaming local/project import | Normative |
| Blank imports | Only in main packages or tests | Normative |
| Dot imports | Only for circular test dependencies | Normative |
| Util packages | Avoid; use descriptive names | Advisory |
| Package size | Balance cohesion vs. distinct concepts | Advisory |
| init() | Avoid; must be deterministic if used | Advisory |
| Exit in main | Only exit from main(); return errors | Advisory |

---

## See Also

- For core style principles: `go-style-core`
- For naming conventions: `go-naming`
- For error handling patterns: `go-error-handling`
- For defensive coding: `go-defensive`
- For linting tools: `go-linting`

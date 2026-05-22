---
name: go-options-gen
description: Expert in generating functional options for Go structs using the options-gen library.
metadata:
  short-description: Functional options generation for Go.
---

# go-options-gen

You are an expert in using the `options-gen` library (https://github.com/kazhuravlev/options-gen) to create robust, type-safe functional options for Go components. You prioritize unexported option fields to maintain encapsulation while providing a clean, exported API for configuration.

## Core Mandates

- **File Naming**:
  - Single Option Set: Struct definition MUST be in `options.go`, and generated code MUST be in `options_generated.go`.
  - Multiple Option Sets: For a component named `MyService`, the struct (e.g., `MyServiceOptions`) MUST be in `myservice_options.go`, and generated code MUST be in `myservice_options_generated.go`.
- **Encapsulation**:
  - Options fields within the struct SHOULD be unexported (start with a lowercase letter) to prevent direct modification from outside the package.
- **Tooling**:
  - Always run the tool using `go tool options-gen`.
  - Install and track the tool in `go.mod` using:
    ```bash
    go get -tool github.com/kazhuravlev/options-gen/cmd/options-gen@latest
    ```
- **Validation**:
  - Always include validation tags (using `go-playground/validator` syntax) for configuration fields.
  - ALWAYS call the generated `Validate()` method within the component's constructor.
- **Component Integration**:
  - Store the resulting options struct in an unexported field named `opts` within your component struct.

## Developer Workflow

1. **Installation**:
   Ensure the tool is tracked in your project:
   ```bash
   go get -tool github.com/kazhuravlev/options-gen/cmd/options-gen@latest
   ```

2. **Define Options (`options.go`)**:
   Define your options struct with unexported fields. Use the `//go:generate` directive to specify the output filename and the target struct.
   ```go
   package mypackage

   import "time"

   //go:generate go tool options-gen -from-struct=Options -out-filename=options_generated.go
   type Options struct {
       timeout    time.Duration `option:"mandatory" validate:"required"`
       maxRetries int           `default:"3" validate:"min=1"`
       endpoints  []string      `option:"variadic=true"`
   }
   ```

3. **Generate**:
   Run the generator:
   ```bash
   go generate ./options.go
   ```

4. **Integration**:
   Use the generated types in your component's constructor and store them in an `opts` field.
   ```go
   type Component struct {
       opts Options
   }

   func New(setters ...OptionOptionsSetter) (*Component, error) {
       opts := NewOptions(setters...)
       if err := opts.Validate(); err != nil {
           return nil, fmt.Errorf("invalid options: %w", err)
       }
       return &Component{opts: opts}, nil
   }
   ```

## Expert Guidance

### Mandatory vs. Default
- Use `option:"mandatory"` for fields that have no safe default (e.g., API keys, target URLs). These become required arguments in `NewOptions()`.
- Use `default:"value"` for sensible defaults. `options-gen` supports basic types and `time.Duration`.

### Advanced Defaults
For complex types (like maps or nested structs), use `-defaults-from=func` in the generate directive and define a provider function:
```go
//go:generate go tool options-gen -from-struct=Options -out-filename=options_generated.go -defaults-from=func
func defaultOptions() Options {
    return Options{
        headers: map[string]string{"User-Agent": "my-client"},
    }
}
```

### Validation Best Practices
- Use `validate:"required"` for any field that must not be zero-valued.
- Use `validate:"oneof=tcp udp"` for enum-like string fields.
- Use `validate:"min=1"` for counters or sizes.

### Variadic Setters
For slice fields, use `option:"variadic=true"` to generate a setter that accepts multiple arguments (e.g., `WithEndpoints("a", "b")`) instead of a single slice (e.g., `WithEndpoints([]string{"a", "b"})`).

### Avoiding Exported Fields
By keeping fields unexported in `options.go`, you ensure that the only way to configure the component is through the generated `With*` setters, which can include validation logic.

### Multiple Options in One Package
When a package contains multiple components (e.g., `Client` and `Server`), use prefixes to avoid name collisions in generated types and functions.

1. **Filenames**: Use `<prefix>_options.go` and `<prefix>_options_generated.go`.
2. **Generator Flag**: Use `-out-prefix` to prefix the generated `NewOptions` and `Option...Setter` types.

**Example for `MyService` (`myservice_options.go`):**
```go
//go:generate go tool options-gen -from-struct=MyServiceOptions -out-filename=myservice_options_generated.go -out-prefix=MyService
type MyServiceOptions struct {
    timeout time.Duration `option:"mandatory"`
}
```

This will generate `NewMyServiceOptions` and `OptionMyServiceOptionsSetter`, allowing them to coexist with other options in the same package.

## Resources

- **Examples**: Complete implementations showing unexported fields, validation, and component integration can be found in the [assets](./assets/README.md) directory.

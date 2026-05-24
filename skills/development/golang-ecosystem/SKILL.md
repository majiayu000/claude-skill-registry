---
name: Go Ecosystem
description: This skill should be used when the user asks to "write go", "golang", "go.mod", "go module", "go test", "go build", or works with Go language development. Provides comprehensive Go ecosystem patterns and best practices.
version: 0.2.0
---

<purpose>
  Provide comprehensive patterns for Go language development, modules, testing, and idiomatic coding practices.
</purpose>

<tools>
  <tool>Read - Analyze go.mod and Go source files</tool>
  <tool>Edit - Modify Go code and module configuration</tool>
  <tool>Bash - Run go build, go test, go mod commands</tool>
  <tool>mcp__context7__get-library-docs - Fetch latest Go documentation</tool>
</tools>

<concepts>
  <concept name="error_values">Errors are values, not exceptions; handle explicitly at each call site with if err != nil</concept>
  <concept name="interfaces">Accept interfaces, return concrete types; define interfaces where used, not implemented</concept>
  <concept name="goroutines_channels">Use goroutines for concurrency, channels for communication, context.Context for cancellation</concept>
  <concept name="zero_values">Zero values are meaningful (0, "", nil, false); design types so zero value is useful</concept>
</concepts>

<go_language>
  <naming_conventions>
    <pattern name="packages">
      <description>Lowercase, single-word names. No underscores or mixedCaps.</description>
      <example>
        package httputil
      </example>
    </pattern>

    <pattern name="exported">
      <description>PascalCase for exported (public) identifiers.</description>
      <example>
        func ReadFile()
        type Handler
        var MaxRetries
      </example>
    </pattern>

    <pattern name="unexported">
      <description>camelCase for unexported (private) identifiers.</description>
      <example>
        func parseConfig()
        type handler
        var maxRetries
      </example>
    </pattern>

    <pattern name="interfaces">
      <description>Single-method interfaces: method name + "er" suffix.</description>
      <example>
        Reader, Writer, Closer, Stringer, Handler
      </example>
    </pattern>

    <pattern name="acronyms">
      <description>Keep acronyms uppercase: URL, HTTP, ID, API.</description>
      <example>
        func ServeHTTP()
        type HTTPClient
        var userID
      </example>
    </pattern>

    <pattern name="getters">
      <description>No "Get" prefix for getters.</description>
      <example>
        func (u *User) Name() string // not GetName()
      </example>
    </pattern>
  </naming_conventions>

  <formatting>
    <rules priority="standard">
      <rule>Use gofmt/goimports - no manual formatting debates</rule>
      <rule>Tabs for indentation, spaces for alignment</rule>
      <rule>No semicolons except in for loops and multi-statement lines</rule>
      <rule>Opening brace on same line as declaration</rule>
    </rules>
  </formatting>

  <type_system>
    <pattern name="zero_values">
      <description>Zero values are meaningful: 0, "", nil, false.</description>
      <example>
        var buf bytes.Buffer // ready to use, no initialization needed
      </example>
    </pattern>

    <pattern name="type_assertion">
      <description>Safe type assertion with ok pattern vs unsafe panic.</description>
      <example>
        value, ok := x.(Type) // safe
        value := x.(Type) // panics if wrong type
      </example>
    </pattern>

    <pattern name="type_switch">
      <description>Type switch for handling multiple types.</description>
      <example>
        switch v := x.(type) {
        case string: // v is string
        case int:    // v is int
        default:     // v is interface{}
        }
      </example>
    </pattern>
  </type_system>
</go_language>

<error_handling>
  <principles>
    <principle>Errors are values, not exceptions</principle>
    <principle>Handle errors explicitly at each call site</principle>
    <principle>Return errors, don't panic</principle>
    <principle>Add context when propagating errors</principle>
  </principles>

  <pattern name="basic_check">
    <description>Basic error checking pattern with context wrapping.</description>
    <example>
      result, err := doSomething()
      if err != nil {
      return fmt.Errorf("failed to do something: %w", err)
      }
    </example>
  </pattern>

  <pattern name="wrap_with_context">
    <description>Use %w verb to wrap errors for later inspection</description>
    <example>
      if err != nil {
      return fmt.Errorf("processing user %s: %w", userID, err)
      }
    </example>
    <decision_tree name="when_to_use">
      <question>Do callers need to inspect or unwrap the error?</question>
      <if_yes>Use %w to wrap errors for errors.Is and errors.As</if_yes>
      <if_no>Use %v to format error without wrapping</if_no>
    </decision_tree>
  </pattern>

  <pattern name="sentinel_errors">
    <description>Define package-level error variables</description>
    <example>
      var ErrNotFound = errors.New("not found")
      var ErrInvalidInput = errors.New("invalid input")
    </example>
  </pattern>

  <pattern name="custom_error_type">
    <description>Define custom error types implementing the error interface for structured error information.</description>
    <example>
      type ValidationError struct {
      Field   string
      Message string
      }

      func (e \*ValidationError) Error() string {
      return fmt.Sprintf("validation failed for %s: %s", e.Field, e.Message)
      }
    </example>
  </pattern>

  <pattern name="error_inspection">
    <description>Inspect and unwrap errors using errors.Is and errors.As for type-safe error handling.</description>
    <example>
      // Check for specific error
      if errors.Is(err, ErrNotFound) { ... }

      // Extract custom error type
      var valErr \*ValidationError
      if errors.As(err, &valErr) {
      log.Printf("field: %s", valErr.Field)
      }
    </example>
  </pattern>

  <pattern name="multiple_errors">
    <description>Go 1.20+ errors.Join</description>
    <example>
      err := errors.Join(err1, err2, err3)
    </example>
  </pattern>
</error_handling>

<interfaces>
  <principles>
    <principle>Accept interfaces, return concrete types</principle>
    <principle>Keep interfaces small (1-3 methods)</principle>
    <principle>Define interfaces where they are used, not implemented</principle>
    <principle>Implicit satisfaction - no "implements" keyword</principle>
  </principles>

  <common_interfaces>
    <interface name="io.Reader">Read(p []byte) (n int, err error)</interface>
    <interface name="io.Writer">Write(p []byte) (n int, err error)</interface>
    <interface name="io.Closer">Close() error</interface>
    <interface name="error">Error() string</interface>
    <interface name="fmt.Stringer">String() string</interface>
  </common_interfaces>

  <pattern name="interface_definition">
    <description>Define interfaces with method signatures.</description>
    <example>
      type Handler interface {
      Handle(ctx context.Context, req Request) (Response, error)
      }
    </example>
    <decision_tree name="when_to_use">
      <question>Do you have multiple implementations or need to decouple packages?</question>
      <if_yes>Define interface where it is used for abstraction</if_yes>
      <if_no>Use concrete types until abstraction is needed</if_no>
    </decision_tree>
  </pattern>

  <pattern name="interface_composition">
    <description>Compose larger interfaces from smaller ones.</description>
    <example>
      type ReadWriteCloser interface {
      io.Reader
      io.Writer
      io.Closer
      }
    </example>
  </pattern>

  <pattern name="empty_interface">
    <description>interface{} or any (Go 1.18+) accepts all types. Avoid when possible - loses type safety.</description>
    <example>
      func process(data any) { ... }
    </example>
  </pattern>
</interfaces>

<modules>
  <pattern name="go_mod_structure">
    <description>Standard go.mod file structure with module, go version, toolchain, and dependencies.</description>
    <example>
      module github.com/user/project

      go 1.23

      toolchain go1.23.0

      require (
      github.com/pkg/errors v0.9.1
      golang.org/x/sync v0.3.0
      )

      require (
      golang.org/x/sys v0.10.0 // indirect
      )
    </example>
  </pattern>

  <commands>
    <tool name="go mod init">
      <description>Initialize new module</description>
      <use_case>Start a new Go project with module support</use_case>
    </tool>
    <tool name="go mod tidy">
      <description>Add missing, remove unused dependencies</description>
      <use_case>Clean up go.mod and go.sum files</use_case>
    </tool>
    <tool name="go get">
      <description>Add or update dependency</description>
      <param name="package-name@version">Package name and optional version</param>
      <use_case>Install or update a specific package version</use_case>
    </tool>
    <tool name="go mod download">
      <description>Download dependencies to cache</description>
      <use_case>Pre-download modules for offline work</use_case>
    </tool>
    <tool name="go mod vendor">
      <description>Create vendor directory</description>
      <use_case>Copy dependencies into vendor/ for vendoring</use_case>
    </tool>
    <tool name="go mod verify">
      <description>Verify dependencies</description>
      <use_case>Check that downloaded modules haven't been modified</use_case>
    </tool>
  </commands>

  <pattern name="toolchain_directive">
    <description>Suggest specific Go toolchain version (Go 1.21+). Used when module requires newer toolchain than default.</description>
    <example>
      toolchain go1.23.0
    </example>
  </pattern>

  <versioning>
    <pattern name="semantic_import">
      <description>v0.x.x and v1.x.x: no path suffix.</description>
      <example>
        import "github.com/user/project"
      </example>
    </pattern>
    <pattern name="v2_plus">
      <description>v2+: include version in import path.</description>
      <example>
        import "github.com/user/project/v2"
      </example>
    </pattern>
  </versioning>

  <pattern name="replace_directive">
    <description>Override module location for local development.</description>
    <example>
      replace github.com/user/lib => ../lib
      replace github.com/user/lib v1.0.0 => ./local-lib
    </example>
  </pattern>
</modules>

<project_structure>
  <standard_layout>
    <directory name="cmd/">Main applications (cmd/myapp/main.go)</directory>
    <directory name="internal/">Private packages, not importable externally</directory>
    <directory name="pkg/">Public library code (optional, controversial)</directory>
    <directory name="api/">API definitions (OpenAPI, protobuf)</directory>
    <directory name="configs/">Configuration files</directory>
    <directory name="scripts/">Build/install scripts</directory>
    <directory name="testdata/">Test fixtures</directory>
  </standard_layout>

  <best_practices>
    <practice priority="critical">cmd/myapp/main.go should be minimal - call into internal packages</practice>
    <practice priority="critical">internal/ packages cannot be imported from outside parent module</practice>
    <practice priority="high">Each directory = one package (except \_test packages)</practice>
  </best_practices>
</project_structure>

<testing>
  <file_naming>
    <pattern name="test_files">
      <description>foo.go → foo_test.go</description>
    </pattern>
    <pattern name="test_functions">
      <description>Test functions: func TestXxx(t *testing.T)</description>
    </pattern>
    <pattern name="benchmark_functions">
      <description>Benchmark functions: func BenchmarkXxx(b *testing.B)</description>
    </pattern>
    <pattern name="example_functions">
      <description>Example functions: func ExampleXxx()</description>
    </pattern>
  </file_naming>

  <pattern name="table_driven_tests">
    <description>Table-driven tests for comprehensive test coverage with multiple test cases.</description>
    <example>
      func TestAdd(t *testing.T) {
      tests := []struct {
      name     string
      a, b     int
      expected int
      }{
      {"positive", 1, 2, 3},
      {"negative", -1, -2, -3},
      {"zero", 0, 0, 0},
      }
      for _, tt := range tests {
      t.Run(tt.name, func(t *testing.T) {
      if got := Add(tt.a, tt.b); got != tt.expected {
      t.Errorf("Add(%d, %d) = %d, want %d", tt.a, tt.b, got, tt.expected)
      }
      })
      }
      }
    </example>
    <decision_tree name="when_to_use">
      <question>Do you need to test same logic with multiple inputs and outputs?</question>
      <if_yes>Use table-driven tests for comprehensive coverage</if_yes>
      <if_no>Write simple individual test functions</if_no>
    </decision_tree>
  </pattern>

  <pattern name="test_helpers">
    <description>Test helper functions with t.Helper() and t.Cleanup() for better test organization.</description>
    <example>
      func setupTestDB(t *testing.T) *DB {
      t.Helper()
      db := NewDB()
      t.Cleanup(func() { db.Close() })
      return db
      }
    </example>
  </pattern>

  <pattern name="testdata_directory">
    <description>testdata/ directory is ignored by go build and used for test fixtures.</description>
    <example>
      mypackage/
      ├── main.go
      ├── main_test.go
      └── testdata/
      ├── input.json
      └── expected.txt
    </example>
  </pattern>

  <commands>
    <tool name="go test">
      <description>Run tests in current package</description>
      <use_case>Execute tests for the current directory</use_case>
    </tool>
    <tool name="go test ./...">
      <description>Run all tests recursively</description>
      <use_case>Test entire project including subpackages</use_case>
    </tool>
    <tool name="go test -v">
      <description>Verbose output</description>
      <use_case>See detailed test execution output</use_case>
    </tool>
    <tool name="go test -run">
      <description>Run specific test</description>
      <param name="TestName">Name pattern to match</param>
      <use_case>Run only tests matching the pattern</use_case>
    </tool>
    <tool name="go test -cover">
      <description>Show coverage percentage</description>
      <use_case>Get quick coverage summary</use_case>
    </tool>
    <tool name="go test -coverprofile">
      <description>Generate coverage profile</description>
      <param name="c.out">Output file path</param>
      <use_case>Create detailed coverage report for analysis</use_case>
    </tool>
    <tool name="go test -bench">
      <description>Run benchmarks</description>
      <param name=".">Pattern to match (. for all)</param>
      <use_case>Execute performance benchmarks</use_case>
    </tool>
    <tool name="go test -race">
      <description>Enable race detector</description>
      <use_case>Detect data races during test execution</use_case>
    </tool>
  </commands>
</testing>

<concurrency>
  <goroutines>
    <pattern name="launch">
      <description>Launch a goroutine for concurrent work.</description>
      <example>
        go func() {
        // concurrent work
        }()
      </example>
    </pattern>

    <pattern name="with_waitgroup">
      <description>Use sync.WaitGroup to wait for multiple goroutines to complete.</description>
      <example>
        var wg sync.WaitGroup
        for _, item := range items {
        wg.Add(1)
        go func(item Item) {
        defer wg.Done()
        process(item)
        }(item)
        }
        wg.Wait()
      </example>
    </pattern>
  </goroutines>

  <channels>
    <pattern name="unbuffered">
      <description>Unbuffered channels provide synchronous communication.</description>
      <example>
        ch := make(chan int)
      </example>
    </pattern>

    <pattern name="buffered">
      <description>Buffered channels allow asynchronous communication up to buffer size.</description>
      <example>
        ch := make(chan int, 10)
      </example>
    </pattern>

    <pattern name="receive_only">
      <description>Receive-only channel parameter.</description>
      <example>
        func consumer(ch <-chan int)
      </example>
    </pattern>

    <pattern name="send_only">
      <description>Send-only channel parameter.</description>
      <example>
        func producer(ch chan<- int)
      </example>
    </pattern>

    <pattern name="select">
      <description>Select statement for multiplexing channel operations.</description>
      <example>
        select {
        case msg := <-ch1:
        handle(msg)
        case ch2 <- value:
        // sent
        case <-ctx.Done():
        return ctx.Err()
        default:
        // non-blocking
        }
      </example>
    </pattern>

    <pattern name="close_channel">
      <description>Closing channels signals no more values will be sent.</description>
      <example>
        close(ch)
        for v := range ch { } // receive until closed
      </example>
    </pattern>
  </channels>

  <pattern name="context_usage">
    <description>Use context.Context for cancellation and timeouts.</description>
    <example>
      ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
      defer cancel()

      select {
      case result := <-doWork(ctx):
      return result, nil
      case <-ctx.Done():
      return nil, ctx.Err()
      }
    </example>
  </pattern>

  <sync_package>
    <concept name="sync.Mutex">
      <description>Mutual exclusion lock</description>
    </concept>
    <concept name="sync.RWMutex">
      <description>Read-write lock</description>
    </concept>
    <concept name="sync.Once">
      <description>Execute exactly once</description>
    </concept>
    <concept name="sync.WaitGroup">
      <description>Wait for goroutine completion</description>
    </concept>
    <concept name="sync.Map">
      <description>Concurrent map (specialized use cases)</description>
    </concept>
  </sync_package>
</concurrency>

<best_practices>
  <practice priority="high">Use gofmt/goimports for consistent code formatting</practice>
  <practice priority="high">Handle errors explicitly at each call site</practice>
  <practice priority="high">Accept interfaces, return concrete types</practice>
  <practice priority="high">Keep interfaces small (1-3 methods)</practice>
  <practice priority="high">Use context.Context for cancellation and timeouts</practice>
  <practice priority="medium">Prefer table-driven tests for comprehensive coverage</practice>
  <practice priority="medium">Use t.Helper() in test helper functions</practice>
  <practice priority="medium">Run tests with -race flag to detect data races</practice>
  <practice priority="medium">Define interfaces where they are used, not implemented</practice>
  <practice priority="medium">Use go mod tidy regularly to maintain clean dependencies</practice>
</best_practices>

<rules priority="critical">
  <rule>Handle all errors explicitly; never ignore returned errors</rule>
  <rule>Run go vet and go test before committing</rule>
  <rule>Use context.Context for cancellation and timeouts in concurrent code</rule>
</rules>

<rules priority="standard">
  <rule>Use gofmt/goimports for consistent formatting</rule>
  <rule>Follow Go naming conventions (exported vs unexported)</rule>
  <rule>Prefer table-driven tests for comprehensive coverage</rule>
  <rule>Run tests with -race flag to detect data races</rule>
</rules>

<anti_patterns>
  <avoid name="init_overuse">
    <description>Overusing init() functions makes code harder to test and reason about.</description>
    <instead>Prefer explicit initialization functions that can be called with parameters.</instead>
  </avoid>
  <avoid name="global_state">
    <description>Package-level mutable variables create hidden dependencies and concurrency issues.</description>
    <instead>Pass dependencies explicitly through function parameters or struct fields.</instead>
  </avoid>
  <avoid name="interface_pollution">
    <description>Defining interfaces prematurely adds unnecessary abstraction.</description>
    <instead>Define interfaces when you have multiple implementations or need to decouple packages.</instead>
  </avoid>
  <avoid name="naked_returns">
    <description>Naked returns in long functions reduce code clarity.</description>
    <instead>Use explicit return statements for functions longer than a few lines.</instead>
  </avoid>
  <avoid name="panic_for_errors">
    <description>Using panic for recoverable errors violates Go's error handling philosophy.</description>
    <instead>Return errors as values and handle them explicitly at each call site.</instead>
  </avoid>
  <avoid name="goroutine_leak">
    <description>Goroutines that never exit waste resources and can cause memory leaks.</description>
    <instead>Use context.Context or done channels to ensure goroutines can be cancelled.</instead>
  </avoid>
  <avoid name="data_race">
    <description>Data races lead to unpredictable behavior and bugs.</description>
    <instead>Use sync primitives (Mutex, RWMutex) or channels, and always run tests with -race flag.</instead>
  </avoid>
  <avoid name="empty_interface_overuse">
    <description>Overusing interface{}/any loses type safety and requires type assertions.</description>
    <instead>Use concrete types or small, focused interfaces when possible.</instead>
  </avoid>
</anti_patterns>

<context7_integration>
  <description>Use Context7 MCP for up-to-date Go documentation</description>

  <go_libraries>
    <library name="Go Website" id="/golang/website" trust="8.3" />
    <library name="Go Tools" id="/golang/tools" trust="8.3" />
  </go_libraries>

  <usage_patterns>
    <pattern name="module_reference">
      <description>Retrieve Go module documentation from Context7.</description>
      <example>
        get-library-docs context7CompatibleLibraryID="/golang/website" topic="go.mod modules"
      </example>
    </pattern>
  </usage_patterns>
</context7_integration>

<build_commands>
  <tool name="go build">
    <description>Compile package</description>
    <use_case>Build executable from current package</use_case>
  </tool>
  <tool name="go build -o">
    <description>Specify output name</description>
    <param name="name">Output binary name</param>
    <use_case>Build with custom binary name</use_case>
  </tool>
  <tool name="go install">
    <description>Compile and install to GOPATH/bin</description>
    <use_case>Install package for global use</use_case>
  </tool>
  <tool name="go run">
    <description>Compile and run</description>
    <param name="main.go">Go file to execute</param>
    <use_case>Quick compile and execute for development</use_case>
  </tool>
  <tool name="go fmt">
    <description>Format all code</description>
    <param name="./...">All packages recursively</param>
    <use_case>Standardize code formatting</use_case>
  </tool>
  <tool name="go vet">
    <description>Static analysis</description>
    <param name="./...">All packages recursively</param>
    <use_case>Detect suspicious code constructs</use_case>
  </tool>
  <tool name="go generate">
    <description>Run code generators</description>
    <use_case>Execute //go:generate directives</use_case>
  </tool>
  <tool name="cross-compile">
    <description>Cross-compile for different platforms</description>
    <example>
      GOOS=linux GOARCH=amd64 go build
    </example>
    <use_case>Build binaries for different operating systems and architectures</use_case>
  </tool>
</build_commands>

<workflow>
  <phase name="analyze">
    <objective>Understand Go code requirements</objective>
    <step>1. Check go.mod for module and dependencies</step>
    <step>2. Review existing code patterns in project</step>
    <step>3. Identify interface and struct designs</step>
  </phase>
  <phase name="implement">
    <objective>Write idiomatic Go code</objective>
    <step>1. Follow Go naming conventions</step>
    <step>2. Use interfaces for abstraction</step>
    <step>3. Handle errors explicitly</step>
  </phase>
  <phase name="validate">
    <objective>Verify Go code correctness</objective>
    <step>1. Run go build for compilation</step>
    <step>2. Run go vet for static analysis</step>
    <step>3. Run go test for testing</step>
  </phase>
</workflow>

<related_agents>
  <agent name="design">Project architecture, interface design, and package structure planning</agent>
  <agent name="execute">Go implementation with proper error handling and concurrency patterns</agent>
  <agent name="code-quality">Run go vet, go fmt, and ensure idiomatic Go code</agent>
</related_agents>

<related_skills>
  <skill name="serena-usage">Navigate Go packages and symbol definitions efficiently</skill>
  <skill name="context7-usage">Access latest Go standard library and toolchain documentation</skill>
  <skill name="investigation-patterns">Debug goroutine leaks, race conditions, and performance issues</skill>
</related_skills>

<error_escalation>
  <level severity="low">
    <example>Golint style warning</example>
    <action>Fix style issue, maintain idiomatic code</action>
  </level>
  <level severity="medium">
    <example>Compilation error</example>
    <action>Fix error, verify with go build</action>
  </level>
  <level severity="high">
    <example>Breaking change in exported API</example>
    <action>Stop, present migration options to user</action>
  </level>
  <level severity="critical">
    <example>Data race or unsafe memory operation</example>
    <action>Block operation, require safe implementation</action>
  </level>
</error_escalation>

<constraints>
  <must>Handle all errors explicitly</must>
  <must>Follow Go naming conventions (exported vs unexported)</must>
  <must>Use interfaces for testability</must>
  <avoid>Ignoring returned errors</avoid>
  <avoid>Using init() without strong justification</avoid>
  <avoid>Overusing global variables</avoid>
</constraints>

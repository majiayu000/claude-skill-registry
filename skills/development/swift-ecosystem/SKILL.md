---
name: Swift Ecosystem
description: This skill should be used when working with Swift projects, "Package.swift", "swift build/test/run", "swiftc", SwiftLint, SwiftFormat, or Swift language patterns. Provides comprehensive Swift ecosystem patterns and best practices for cross-platform CLI and library development.
version: 0.1.0
---

<purpose>
  Provide comprehensive patterns for Swift language, Swift Package Manager, and toolchain configuration for cross-platform CLI and library development.
</purpose>

<tools>
  <tool>Read - Analyze Package.swift and Swift source files</tool>
  <tool>Edit - Modify Swift code and SPM configuration</tool>
  <tool>Bash - Run swift build, swift test, swiftlint commands</tool>
  <tool>mcp__context7__get-library-docs - Fetch latest Swift documentation</tool>
</tools>

<concepts>
  <concept name="value_types">Structs and enums are value types with copy semantics; prefer over classes for data</concept>
  <concept name="optionals">Optional types (T?) for values that may be absent; use if-let, guard-let, or ?? for safe unwrapping</concept>
  <concept name="protocols">Define behavior contracts; use protocol-oriented programming for composition over inheritance</concept>
  <concept name="generics">Type parameters for reusable code; use where clauses for constraints</concept>
  <concept name="concurrency">async/await for asynchronous code; actors for safe mutable state; Sendable for thread-safe types</concept>
</concepts>

<swift_language>
  <type_system>
    <concept name="value_vs_reference">
      <description>Structs and enums are value types (copied); classes are reference types (shared)</description>
      <rules priority="critical">
        <rule>Prefer structs for data models without identity</rule>
        <rule>Use classes only when reference semantics or inheritance is required</rule>
        <rule>Enums with associated values for algebraic data types</rule>
      </rules>
    </concept>

    <concept name="optionals">
      <description>Swift's nil-safety through Optional type</description>
      <pattern name="safe_unwrapping">
        <example>
          // if-let binding
          if let value = optionalValue {
            use(value)
          }

          // guard-let for early exit
          guard let value = optionalValue else { return }

          // nil-coalescing
          let value = optionalValue ?? defaultValue

          // optional chaining
          let result = object?.property?.method()
        </example>
      </pattern>
      <anti_pattern name="force_unwrap">
        <description>Using ! to force unwrap optionals</description>
        <instead>Use if-let, guard-let, or ?? instead of force unwrapping</instead>
      </anti_pattern>
    </concept>

    <concept name="protocols">
      <description>Define behavior contracts for types</description>
      <pattern name="protocol_oriented">
        <description>Prefer composition with protocols over class inheritance</description>
        <example>
          protocol Identifiable {
            var id: String { get }
          }

          protocol Timestamped {
            var createdAt: Date { get }
          }

          struct User: Identifiable, Timestamped {
            let id: String
            let createdAt: Date
            let name: String
          }
        </example>
      </pattern>
      <pattern name="protocol_extensions">
        <description>Provide default implementations via extensions</description>
        <example>
          protocol Describable {
            var description: String { get }
          }

          extension Describable {
            var description: String {
              String(describing: self)
            }
          }
        </example>
      </pattern>
    </concept>

    <concept name="generics">
      <description>Type-safe reusable code with type parameters</description>
      <pattern name="generic_constraints">
        <example>
          func process&lt;T: Codable &amp; Sendable&gt;(_ item: T) -&gt; Data {
            try! JSONEncoder().encode(item)
          }

          func compare&lt;T&gt;(_ a: T, _ b: T) -&gt; Bool where T: Comparable {
            a &lt; b
          }
        </example>
      </pattern>
    </concept>

    <concept name="noncopyable">
      <description>Types with unique ownership using ~Copyable (Swift 6+)</description>
      <example>
        struct UniqueResource: ~Copyable {
          consuming func release() { /* takes ownership */ }
        }

        func process(borrowing data: SomeData) { /* read-only */ }
        func consume(consuming data: SomeData) { /* takes ownership */ }
      </example>
      <rules priority="critical">
        <rule>Use for resources requiring unique ownership (file handles, locks)</rule>
        <rule>Mark methods with borrowing/consuming for explicit ownership</rule>
      </rules>
    </concept>
  </type_system>

  <error_handling>
    <pattern name="throwing_functions">
      <description>Use throws for recoverable errors</description>
      <example>
        enum ParseError: Error {
          case invalidFormat
          case missingField(String)
        }

        func parse(_input: String) throws -&gt; Config {
          guard !input.isEmpty else {
            throw ParseError.invalidFormat
          }
          // parsing logic
        }

        // Calling
        do {
          let config = try parse(input)
        } catch ParseError.invalidFormat {
          // handle specific error
        } catch {
          // handle other errors
        }
      </example>
    </pattern>

    <pattern name="result_type">
      <description>Use Result for async error handling or when throws is inconvenient</description>
      <example>
        func fetch(url: URL) -&gt; Result&lt;Data, NetworkError&gt; {
          // implementation
        }

        switch fetch(url: someURL) {
        case .success(let data):
          process(data)
        case .failure(let error):
          handle(error)
        }
      </example>
    </pattern>

    <pattern name="typed_throws">
      <description>Specify exact error type in function signature (Swift 6+)</description>
      <example>
        func parse(_ input: String) throws(ParseError) -&gt; Config {
          guard !input.isEmpty else { throw ParseError.invalidFormat }
          // parsing logic
        }

        // Caller knows exactly which errors to handle
        do {
          let config = try parse(input)
        } catch {
          // error is typed as ParseError, not any Error
          switch error {
          case .invalidFormat: handleInvalidFormat()
          case .missingField(let name): handleMissing(name)
          }
        }
      </example>
    </pattern>
  </error_handling>

  <concurrency>
    <pattern name="async_await">
      <description>Structured concurrency with async/await (Swift 5.5+)</description>
      <example>
        func fetchData() async throws -&gt; Data {
          let (data, _) = try await URLSession.shared.data(from: url)
          return data
        }

        // Calling
        Task {
          do {
            let data = try await fetchData()
          } catch {
            // handle error
          }
        }
      </example>
    </pattern>

    <pattern name="actors">
      <description>Thread-safe mutable state with actors</description>
      <example>
        actor Counter {
          private var value = 0

          func increment() {
            value += 1
          }

          func getValue() -&gt; Int {
            value
          }
        }

        let counter = Counter()
        await counter.increment()
        let value = await counter.getValue()
      </example>
    </pattern>

    <pattern name="sendable">
      <description>Mark types safe for concurrent access</description>
      <example>
        // Implicitly Sendable (value types with Sendable properties)
        struct Config: Sendable {
          let timeout: Int
          let retries: Int
        }

        // Explicitly mark as Sendable
        final class ImmutableCache: Sendable {
          let data: [String: String]
          init(data: [String: String]) {
            self.data = data
          }
        }
      </example>
    </pattern>

    <pattern name="task_groups">
      <description>Parallel execution with structured concurrency</description>
      <example>
        func processAll(_ items: [Item]) async throws -&gt; [Result] {
          try await withThrowingTaskGroup(of: Result.self) { group in
            for item in items {
              group.addTask {
                try await process(item)
              }
            }
            return try await group.reduce(into: []) { $0.append($1) }
          }
        }
      </example>
    </pattern>

    <rules priority="critical">
      <rule>Use async/await over completion handlers for new code</rule>
      <rule>Use actors for shared mutable state instead of locks</rule>
      <rule>Mark types as Sendable when they cross concurrency boundaries</rule>
    </rules>
  </concurrency>

  <memory_management>
    <pattern name="weak_references">
      <description>Prevent retain cycles in closures and delegates</description>
      <example>
        class Controller {
          var onComplete: (() -&gt; Void)?

          func setup() {
            service.fetch { [weak self] result in
              self?.handleResult(result)
            }
          }
        }
      </example>
    </pattern>

    <pattern name="unowned_references">
      <description>Non-optional weak reference when lifetime is guaranteed</description>
      <example>
        class Parent {
          var child: Child?
        }

        class Child {
          unowned let parent: Parent

          init(parent: Parent) {
            self.parent = parent
          }
        }
      </example>
    </pattern>

    <rules priority="critical">
      <rule>Always use [weak self] in escaping closures unless self lifetime is guaranteed</rule>
      <rule>Use unowned only when you can guarantee the referenced object outlives the closure</rule>
    </rules>
  </memory_management>

  <common_patterns>
    <pattern name="builder">
      <description>Fluent API for complex object construction</description>
      <example>
        struct RequestBuilder {
          private var method: String = "GET"
          private var headers: [String: String] = [:]

          func method(_ m: String) -&gt; RequestBuilder {
            var copy = self
            copy.method = m
            return copy
          }

          func header(_ key: String, _ value: String) -&gt; RequestBuilder {
            var copy = self
            copy.headers[key] = value
            return copy
          }

          func build() -&gt; Request {
            Request(method: method, headers: headers)
          }
        }
      </example>
    </pattern>

    <pattern name="result_builder">
      <description>DSL construction with @resultBuilder</description>
      <example>
        @resultBuilder
        struct ArrayBuilder&lt;Element&gt; {
          static func buildBlock(_ components: Element...) -&gt; [Element] {
            components
          }
        }

        func buildArray&lt;T&gt;(@ArrayBuilder&lt;T&gt; _content: () -&gt; [T]) -&gt; [T] {
          content()
        }
      </example>
    </pattern>

    <pattern name="property_wrappers">
      <description>Encapsulate property access patterns</description>
      <example>
        @propertyWrapper
        struct Clamped&lt;Value: Comparable&gt; {
          private var value: Value
          private let range: ClosedRange&lt;Value&gt;

          var wrappedValue: Value {
            get { value }
            set { value = min(max(newValue, range.lowerBound), range.upperBound) }
          }

          init(wrappedValue: Value, _ range: ClosedRange&lt;Value&gt;) {
            self.range = range
            self.value = min(max(wrappedValue, range.lowerBound), range.upperBound)
          }
        }

        struct Volume {
          @Clamped(0...100) var level: Int = 50
        }
      </example>
    </pattern>
  </common_patterns>

  <anti_patterns>
    <avoid name="force_unwrap">
      <description>Using ! to force unwrap optionals</description>
      <instead>Use if-let, guard-let, or nil-coalescing</instead>
    </avoid>

    <avoid name="force_try">
      <description>Using try! to ignore errors</description>
      <instead>Use do-catch or propagate with throws</instead>
    </avoid>

    <avoid name="class_for_data">
      <description>Using class for simple data containers</description>
      <instead>Use struct for value semantics</instead>
    </avoid>

    <avoid name="any_abuse">
      <description>Overusing Any or AnyObject types</description>
      <instead>Use generics or protocols with associated types</instead>
    </avoid>

    <avoid name="retain_cycles">
      <description>Strong reference cycles in closures</description>
      <instead>Use [weak self] or [unowned self] capture lists</instead>
    </avoid>
  </anti_patterns>
</swift_language>

<patterns>
  <decision_tree name="error_handling_choice">
    <question>Is this synchronous code with recoverable errors?</question>
    <branch condition="Yes, synchronous with recoverable errors">Use throws with do-catch</branch>
    <branch condition="Need to store or pass the error">Use Result type</branch>
    <branch condition="Simple absence without error details">Use Optional</branch>
    <branch condition="Swift 6+ with specific error type">Use typed throws</branch>
  </decision_tree>

  <decision_tree name="package_type">
    <question>What are you building?</question>
    <branch condition="Reusable code for other packages">Library (.library product)</branch>
    <branch condition="Command-line tool">Executable (.executable product)</branch>
    <branch condition="Both library and CLI">Multiple products with shared target</branch>
  </decision_tree>

  <decision_tree name="reference_type_choice">
    <question>What is the relationship between objects?</question>
    <branch condition="Parent to child">Use strong reference</branch>
    <branch condition="Child to parent or delegate">Use weak reference</branch>
    <branch condition="Guaranteed lifetime">Use unowned reference</branch>
  </decision_tree>

  <decision_tree name="type_choice">
    <question>What kind of type do you need?</question>
    <branch condition="Data without identity">Use struct (value type)</branch>
    <branch condition="Shared mutable state">Use class (reference type) or actor</branch>
    <branch condition="Fixed set of cases">Use enum with associated values</branch>
    <branch condition="Unique ownership required">Use ~Copyable struct (Swift 6+)</branch>
  </decision_tree>
</patterns>

<swift_package_manager>
  <project_structure>
    <standard_layout>
      .
      ├── Package.swift
      ├── Package.resolved
      ├── Sources/
      │ ├── MyLibrary/
      │ │ └── MyLibrary.swift
      │ └── MyCLI/
      │ └── main.swift
      ├── Tests/
      │ └── MyLibraryTests/
      │ └── MyLibraryTests.swift
      └── Plugins/
        └── MyPlugin/
          └── plugin.swift
    </standard_layout>

    <module_organization>
      <pattern name="single_target">
        <description>Simple library or executable</description>
      </pattern>
      <pattern name="multi_target">
        <description>Library with CLI tool or multiple modules</description>
      </pattern>
    </module_organization>
  </project_structure>

  <package_swift>
    <basic_structure>
      // swift-tools-version: 6.0
      import PackageDescription

      // For cross-platform (macOS + Linux), omit platforms array entirely
      // Only specify platforms when using platform-specific APIs
      let package = Package(
        name: "MyPackage",
        platforms: [
          .macOS(.v14)
        ],
        products: [
          .library(
            name: "MyLibrary",
            targets: ["MyLibrary"]
          ),
          .executable(
            name: "my-cli",
            targets: ["MyCLI"]
          )
        ],
        dependencies: [
          .package(url: "https://github.com/apple/swift-argument-parser", from: "1.5.0"),
          .package(url: "https://github.com/apple/swift-log", from: "1.6.0")
        ],
        targets: [
          .target(
            name: "MyLibrary",
            dependencies: [
              .product(name: "Logging", package: "swift-log")
            ]
          ),
          .executableTarget(
            name: "MyCLI",
            dependencies: [
              "MyLibrary",
              .product(name: "ArgumentParser", package: "swift-argument-parser")
            ]
          ),
          .testTarget(
            name: "MyLibraryTests",
            dependencies: ["MyLibrary"]
          )
        ]
      )
    </basic_structure>

    <dependency_specification>
      // Exact version
      .package(url: "...", exact: "1.2.3")

      // Version range
      .package(url: "...", from: "1.0.0") // 1.0.0 ..&lt; 2.0.0
      .package(url: "...", "1.0.0"..&lt;"2.0.0")

      // Branch or revision
      .package(url: "...", branch: "main")
      .package(url: "...", revision: "abc123")

      // Local package
      .package(path: "../LocalPackage")
    </dependency_specification>

    <swift_settings>
      .target(
        name: "MyTarget",
        swiftSettings: [
          .enableUpcomingFeature("StrictConcurrency"),
          .enableExperimentalFeature("AccessLevelOnImport"),
          .unsafeFlags(["-warnings-as-errors"], .when(configuration: .release))
        ]
      )
    </swift_settings>
  </package_swift>

  <commands>
    <command name="swift build">Compile the package</command>
    <command name="swift build -c release">Compile with optimizations</command>
    <command name="swift run">Build and run executable</command>
    <command name="swift test">Run all tests</command>
    <command name="swift test --filter MyTest">Run specific test</command>
    <command name="swift package resolve">Resolve dependencies</command>
    <command name="swift package update">Update dependencies</command>
    <command name="swift package show-dependencies">Show dependency tree</command>
    <command name="swift package init --type library">Create new library package</command>
    <command name="swift package init --type executable">Create new CLI package</command>
    <command name="swift package clean">Clean build artifacts</command>
  </commands>
</swift_package_manager>

<toolchain>
  <swiftlint>
    <description>Swift linter for enforcing style and conventions</description>
    <usage>swiftlint lint</usage>

    <configuration>
      <file_reference>.swiftlint.yml</file_reference>
      disabled_rules:
        - trailing_whitespace
        - line_length

      opt_in_rules:
        - empty_count
        - closure_spacing
        - force_unwrapping

      included:
        - Sources
        - Tests

      excluded:
        - .build
        - Packages

      line_length:
        warning: 120
        error: 200

      type_body_length:
        warning: 300
        error: 500

      file_length:
        warning: 500
        error: 1000
    </configuration>

    <common_rules>
      <rule name="force_unwrapping">Disallow force unwrapping with !</rule>
      <rule name="force_try">Disallow force try with try!</rule>
      <rule name="force_cast">Disallow force casting with as!</rule>
      <rule name="empty_count">Prefer isEmpty over count == 0</rule>
      <rule name="closure_spacing">Ensure spacing in closures</rule>
    </common_rules>
  </swiftlint>

  <swiftformat>
    <description>Code formatter for consistent style (nicklockwood)</description>
    <usage>swiftformat .</usage>

    <configuration>
      <file_reference>.swiftformat</file_reference>
      --swiftversion 6.0
      --indent 4
      --indentcase false
      --trimwhitespace always
      --voidtype void
      --wraparguments before-first
      --wrapcollections before-first
      --maxwidth 120
      --self remove
      --importgrouping testable-last
      --semicolons never
      --commas always
    </configuration>

    <common_options>
      <option name="--swiftversion">Target Swift version</option>
      <option name="--indent">Indentation width (default: 4)</option>
      <option name="--maxwidth">Maximum line width</option>
      <option name="--self">Self keyword insertion (remove/insert)</option>
      <option name="--wraparguments">Argument wrapping style</option>
    </common_options>
  </swiftformat>

  <sourcekit_lsp>
    <description>Language server for IDE integration</description>
    <usage>Bundled with Swift toolchain</usage>

    <vscode_setup>
      <step>Install Swift extension (official)</step>
      <step>Extension uses SourceKit-LSP automatically</step>
      <step>Run swift build to generate index</step>
    </vscode_setup>

    <features>
      <feature>Code completion</feature>
      <feature>Jump to definition</feature>
      <feature>Find references</feature>
      <feature>Diagnostics</feature>
      <feature>Code actions</feature>
    </features>
  </sourcekit_lsp>

  <other_tools>
    <tool name="swift-testing">
      <description>Modern testing framework (Swift 6+)</description>
      <example>
        import Testing

        @Test func addition() {
          #expect(1 + 1 == 2)
        }

        @Test("Descriptive name")
        func subtraction() throws {
          let result = try compute()
          #expect(result &gt; 0)
        }
      </example>
    </tool>

    <tool name="swift-format">
      <description>Apple's official formatter (alternative to SwiftFormat)</description>
      <note>Built into Xcode 16; use swift-format command</note>
    </tool>

    <tool name="swift-docc">
      <description>Documentation compiler for Swift</description>
      <usage>swift package generate-documentation</usage>
    </tool>
  </other_tools>
</toolchain>

<testing>
  <swift_testing>
    <description>Modern testing framework with Swift 6 macros</description>

    <pattern name="basic_test">
      <example>
        import Testing

        @Test func addition() {
          #expect(1 + 1 == 2)
        }

        @Test("Descriptive name")
        func subtraction() throws {
          let result = try compute()
          #expect(result &gt; 0)
        }
      </example>
    </pattern>

    <pattern name="parameterized_test">
      <example>
        @Test(arguments: [1, 2, 3])
        func multipleInputs(value: Int) {
          #expect(value &gt; 0)
        }
      </example>
    </pattern>

    <pattern name="test_suite">
      <example>
        @Suite("Calculator Tests")
        struct CalculatorTests {
          @Test func add() { #expect(1 + 1 == 2) }
          @Test func multiply() { #expect(2 * 3 == 6) }
        }
      </example>
    </pattern>

    <pattern name="async_test">
      <example>
        @Test func fetchData() async throws {
          let data = try await service.fetch()
          #expect(!data.isEmpty)
        }
      </example>
    </pattern>

    <note>swift-testing does not yet support performance testing or UI testing</note>
  </swift_testing>

  <xctest>
    <description>Legacy testing framework for existing codebases</description>

    <migration>
      <step>Replace XCTAssert with #expect</step>
      <step>Replace XCTAssertEqual with #expect(a == b)</step>
      <step>Replace XCTestCase class with @Test functions</step>
      <step>Use @Suite for test grouping</step>
    </migration>
  </xctest>

  <best_practices>
    <practice>Use swift-testing for new test code</practice>
    <practice>Organize tests in Tests/ directory with TestTarget suffix</practice>
    <practice>Use @Test for individual test functions</practice>
    <practice>Use @Suite for grouping related tests</practice>
    <practice>Use parameterized tests for testing multiple inputs</practice>
  </best_practices>
</testing>

<context7_integration>
  <description>Use Context7 MCP for up-to-date Swift documentation</description>

  <swift_libraries>
    <library name="Swift Language" id="/swiftlang/swift" />
    <library name="Swift Argument Parser" id="/apple/swift-argument-parser" />
    <library name="Swift Log" id="/apple/swift-log" />
    <library name="SwiftFormat" id="/nicklockwood/swiftformat" />
    <library name="Alamofire" id="/alamofire/alamofire" />
    <library name="Vapor" id="/vapor/vapor" />
    <library name="GRDB.swift" id="/groue/grdb.swift" />
    <library name="Kingfisher" id="/onevcat/kingfisher" />
    <library name="RxSwift" id="/reactivex/rxswift" />
    <library name="CryptoSwift" id="/krzyzanowskim/cryptoswift" />
    <library name="SQLite.swift" id="/stephencelis/sqlite.swift" />
  </swift_libraries>

  <usage_patterns>
    <pattern name="language_reference">
      <step>resolve-library-id libraryName="swift"</step>
      <step>get-library-docs context7CompatibleLibraryID="/swiftlang/swift" topic="concurrency"</step>
    </pattern>

    <pattern name="package_configuration">
      <step>get-library-docs context7CompatibleLibraryID="/swiftlang/swift" topic="Package.swift"</step>
    </pattern>

    <pattern name="library_usage">
      <step>get-library-docs context7CompatibleLibraryID="/alamofire/alamofire" topic="request"</step>
    </pattern>
  </usage_patterns>
</context7_integration>

<workflow>
  <phase name="analyze">
    <objective>Understand Swift code requirements</objective>
    <step>1. Check Package.swift for package configuration</step>
    <step>2. Review existing patterns and protocols</step>
    <step>3. Identify concurrency requirements</step>
  </phase>
  <phase name="implement">
    <objective>Write safe, idiomatic Swift code</objective>
    <step>1. Design with value types and protocols</step>
    <step>2. Use optionals and error handling correctly</step>
    <step>3. Follow Swift API design guidelines</step>
  </phase>
  <phase name="validate">
    <objective>Verify Swift code correctness</objective>
    <step>1. Run swift build for compilation check</step>
    <step>2. Run swiftlint for style/safety lints</step>
    <step>3. Run swift test for testing</step>
  </phase>
</workflow>

<best_practices>
  <practice priority="critical">Use swift build for compilation; swift test for testing</practice>
  <practice priority="critical">Run swiftlint before committing</practice>
  <practice priority="critical">Format with swiftformat for consistent style</practice>
  <practice priority="high">Prefer value types (structs) over reference types (classes)</practice>
  <practice priority="high">Use async/await for asynchronous code</practice>
  <practice priority="high">Mark types as Sendable for concurrency safety</practice>
  <practice priority="medium">Document public API with /// doc comments</practice>
  <practice priority="medium">Write tests alongside implementation</practice>
  <practice priority="medium">Use Swift Testing framework for new test code</practice>
  <practice priority="medium">Specify swift-tools-version in Package.swift</practice>
</best_practices>

<rules priority="critical">
  <rule>Run swiftlint before committing; fix all warnings</rule>
  <rule>Never use force unwrap (!) in library code</rule>
  <rule>Use async/await over completion handlers for new code</rule>
</rules>

<rules priority="standard">
  <rule>Use swiftformat for consistent formatting</rule>
  <rule>Prefer structs over classes for data types</rule>
  <rule>Write unit tests in Tests/ directory</rule>
  <rule>Use guard for early exit patterns</rule>
</rules>

<related_agents>
  <agent name="design">Protocol design, type system architecture, and API modeling</agent>
  <agent name="execute">Swift implementation with proper error handling and concurrency</agent>
  <agent name="code-quality">Run swiftlint, swiftformat, and enforce Swift idioms</agent>
</related_agents>

<error_escalation>
  <level severity="low">
    <example>SwiftLint warning about style</example>
    <action>Fix warning, maintain idiomatic code</action>
  </level>
  <level severity="medium">
    <example>Type safety error or optional handling issue</example>
    <action>Redesign with proper types, use safe unwrapping</action>
  </level>
  <level severity="high">
    <example>Breaking change in public API</example>
    <action>Stop, present migration options to user</action>
  </level>
  <level severity="critical">
    <example>Force unwrap or unsafe code in library</example>
    <action>Block operation, require safe alternatives</action>
  </level>
</error_escalation>

<related_skills>
  <skill name="serena-usage">Navigate protocol implementations and module structure</skill>
  <skill name="context7-usage">Fetch Swift language and library documentation</skill>
  <skill name="investigation-patterns">Debug type errors, optional handling, and concurrency issues</skill>
</related_skills>

<constraints>
  <must>Prefer value types over reference types</must>
  <must>Use optionals and proper error handling</must>
  <must>Follow Swift API design guidelines</must>
  <avoid>Using force unwrap (!) in library code</avoid>
  <avoid>Using force try (try!) in production code</avoid>
  <avoid>Completion handlers when async/await is available</avoid>
</constraints>

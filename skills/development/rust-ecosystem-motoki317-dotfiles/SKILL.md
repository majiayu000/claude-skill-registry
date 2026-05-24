---
name: Rust Ecosystem
description: This skill should be used when working with Rust projects, "Cargo.toml", "rustc", "cargo build/test/run", "clippy", "rustfmt", or Rust language patterns. Provides comprehensive Rust ecosystem patterns and best practices.
---

<purpose>
  Provide comprehensive patterns for Rust language, Cargo project management, and toolchain configuration.
</purpose>

<tools>
  <tool>Read - Analyze Cargo.toml and Rust source files</tool>
  <tool>Edit - Modify Rust code and Cargo configuration</tool>
  <tool>Bash - Run cargo build, cargo test, cargo clippy commands</tool>
  <tool>mcp__context7__get-library-docs - Fetch latest Rust documentation</tool>
</tools>

<concepts>
  <concept name="ownership">Each value has one owner; when owner goes out of scope, value is dropped</concept>
  <concept name="borrowing">Immutable (&T) allows multiple borrows; mutable (&mut T) allows exactly one; cannot mix</concept>
  <concept name="result_option">Result for recoverable errors (Ok/Err), Option for optional values (Some/None); use ? for propagation</concept>
  <concept name="traits">Define behavior with traits; use derive for common implementations (Debug, Clone, PartialEq)</concept>
</concepts>

<rust_language>
  <ownership_borrowing>
    <concept name="ownership">
      <description>Each value has exactly one owner. When owner goes out of scope, value is dropped.</description>
      <use>Use move semantics by default; explicit Clone when needed</use>
    </concept>

    <concept name="borrowing">
      <description>Immutable and mutable references with strict rules</description>
      <rules priority="critical">
        <rule>&T allows multiple simultaneous borrows</rule>
        <rule>&mut T allows exactly one mutable borrow</rule>
        <rule>Cannot have &mut T while &T exists</rule>
      </rules>
    </concept>

    <concept name="lifetimes">
      <description>Lifetime annotations for reference validity</description>
      <pattern name="elision">
        <description>Compiler infers lifetimes in common patterns</description>
      </pattern>
      <pattern name="explicit">
        <description>Explicit lifetime annotations for complex cases</description>
        <example>
          fn foo<'a>(x: &'a str) -> &'a str {
            x
          }
        </example>
      </pattern>
      <pattern name="static">
        <description>'static for values that live entire program</description>
      </pattern>
    </concept>
  </ownership_borrowing>

  <traits>
    <common_traits>
      <trait name="Clone">Explicit duplication with .clone()</trait>
      <trait name="Copy">Implicit bitwise copy for simple types</trait>
      <trait name="Debug">Debug formatting with {:?}</trait>
      <trait name="Display">User-facing formatting with {}</trait>
      <trait name="Default">Default value construction</trait>
      <trait name="PartialEq/Eq">Equality comparison</trait>
      <trait name="PartialOrd/Ord">Ordering comparison</trait>
      <trait name="Hash">Hashing for HashMap/HashSet keys</trait>
      <trait name="From/Into">Type conversions</trait>
      <trait name="AsRef/AsMut">Cheap reference conversions</trait>
    </common_traits>

    <pattern name="derive">
      <description>Automatically implement common traits</description>
      <example>
        #[derive(Debug, Clone, PartialEq, Eq, Hash)]
        struct MyType {
          field1: String,
          field2: i32,
        }
      </example>
    </pattern>
  </traits>

  <error_handling>
    <pattern name="Result">
      <description>Recoverable errors with Result with T and E type parameters</description>
      <operators>? for early return on Err</operators>
      <combinators>map, and_then, unwrap_or, unwrap_or_else</combinators>
      <decision_tree name="when_to_use">
        <question>Is this a recoverable error that callers should handle?</question>
        <if_yes>Return Result type with appropriate error variant</if_yes>
        <if_no>Use panic only for unrecoverable programming errors</if_no>
      </decision_tree>
    </pattern>

    <pattern name="Option">
      <description>Optional values with Option with T type parameter</description>
      <operators>? for early return on None</operators>
      <combinators>map, and_then, unwrap_or, unwrap_or_default</combinators>
    </pattern>

    <pattern name="custom_error">
      <description>Define custom error types with thiserror or anyhow</description>
      <example>
        #[derive(Debug, thiserror::Error)]
        enum MyError {
          #[error("IO error: {0}")]
          Io(#[from] std::io::Error),
          #[error("Parse error: {msg}")]
          Parse { msg: String },
        }
      </example>
    </pattern>
  </error_handling>

  <common_patterns>
    <pattern name="builder">
      <description>Fluent API for complex object construction</description>
      <example>
        MyStruct::builder()
          .field1(value1)
          .field2(value2)
          .build()
      </example>
      <decision_tree name="when_to_use">
        <question>Does the struct have many optional fields or complex construction logic?</question>
        <if_yes>Implement builder pattern for ergonomic construction</if_yes>
        <if_no>Use simple constructor function or Default trait</if_no>
      </decision_tree>
    </pattern>

    <pattern name="newtype">
      <description>Wrapper type for type safety</description>
      <example>
        struct UserId(u64);
      </example>
    </pattern>

    <pattern name="type_state">
      <description>Encode state in type system</description>
      <use_case>Prevent invalid state transitions at compile time</use_case>
    </pattern>
  </common_patterns>

  <anti_patterns>
    <avoid name="unwrap_in_library">
      <description>Using unwrap() in library code</description>
      <instead>Use ? or proper error handling instead</instead>
    </avoid>

    <avoid name="clone_abuse">
      <description>Cloning values unnecessarily</description>
      <instead>Prefer borrowing when possible</instead>
    </avoid>

    <avoid name="string_for_everything">
      <description>Using String for all domain values</description>
      <instead>Use enums, newtypes for domain modeling</instead>
    </avoid>

    <avoid name="arc_mutex_overuse">
      <description>Defaulting to Arc with Mutex with T for concurrency</description>
      <instead>Consider channels or ownership patterns first</instead>
    </avoid>
  </anti_patterns>
</rust_language>

<cargo>
  <project_structure>
    <standard_layout>
      .
      ├── Cargo.lock
      ├── Cargo.toml
      ├── src/
      │   ├── lib.rs          # Library crate root
      │   ├── main.rs         # Binary crate root
      │   └── bin/            # Additional binaries
      ├── tests/              # Integration tests
      ├── benches/            # Benchmarks
      └── examples/           # Example code
    </standard_layout>

    <module_organization>
      <pattern name="mod_rs">
        <description>src/module/mod.rs with submodules</description>
      </pattern>
      <pattern name="file_module">
        <description>src/module.rs (preferred for simple modules)</description>
      </pattern>
    </module_organization>
  </project_structure>

  <cargo_toml>
    <basic_structure>
      [package]
      name = "my-crate"
      version = "0.1.0"
      edition = "2021" # Current edition; edition 2024 (upcoming/future)
      rust-version = "1.83" # Current stable as of Dec 2025

      [dependencies]
      serde = { version = "1.0", features = ["derive"] }

      [dev-dependencies]
      tokio-test = "0.4"

      [build-dependencies]
      cc = "1.0"
    </basic_structure>

    <feature_flags>
      [features]
      default = ["std"]
      std = []
      async = ["tokio"]
      full = ["std", "async"]
    </feature_flags>

    <profile_optimization>
      [profile.release]
      lto = true
      codegen-units = 1
      panic = "abort"
      strip = true

      [profile.dev]
      opt-level = 0
      debug = true
    </profile_optimization>
  </cargo_toml>

  <workspace>
    <root_cargo_toml>
      [workspace]
      resolver = "2"  # Current default for edition 2021; resolver 3 (upcoming, requires Edition 2024)
      members = ["crate-a", "crate-b"]

      [workspace.package]
      version = "0.1.0"
      edition = "2021"
      license = "MIT"

      [workspace.dependencies]
      serde = "1.0"
      tokio = { version = "1", features = ["full"] }
    </root_cargo_toml>

    <member_inheritance>
      [package]
      name = "crate-a"
      version.workspace = true
      edition.workspace = true

      [dependencies]
      serde.workspace = true
    </member_inheritance>

    <decision_tree name="when_to_use">
      <question>Do you have multiple related crates in one repository?</question>
      <if_yes>Use workspace to share dependencies and build configuration</if_yes>
      <if_no>Single crate project without workspace structure</if_no>
    </decision_tree>
  </workspace>

  <commands>
    <command name="cargo build">Compile the project</command>
    <command name="cargo build --release">Compile with optimizations</command>
    <command name="cargo run">Build and run binary</command>
    <command name="cargo test">Run all tests</command>
    <command name="cargo check">Fast syntax/type check without codegen</command>
    <command name="cargo doc --open">Generate and open documentation</command>
    <command name="cargo update">Update dependencies</command>
    <command name="cargo tree">Display dependency tree</command>
  </commands>
</cargo>

<toolchain>
  <clippy>
    <description>Rust linter for catching common mistakes and improving code</description>
    <usage>cargo clippy -- -D warnings</usage>

    <configuration>
      <file_reference>In Cargo.toml</file_reference>
      [lints.clippy]
      pedantic = "warn"
      nursery = "warn"
      unwrap_used = "deny"
      expect_used = "deny"

      <file_reference>Or in clippy.toml</file_reference>

      msrv = "1.70"
      cognitive-complexity-threshold = 25
    </configuration>

    <common_lints>
      <lint name="clippy::unwrap_used">Prefer ? or proper error handling</lint>
      <lint name="clippy::expect_used">Prefer ? or proper error handling</lint>
      <lint name="clippy::pedantic">Stricter lints for cleaner code</lint>
      <lint name="clippy::nursery">Experimental but useful lints</lint>
    </common_lints>
  </clippy>

  <rustfmt>
    <description>Automatic code formatter</description>
    <usage>cargo fmt</usage>

    <configuration>
      <file_reference>rustfmt.toml</file_reference>
      edition = "2021"
      max_width = 100
      use_small_heuristics = "Max"
      imports_granularity = "Crate"
      group_imports = "StdExternalCrate"
      reorder_imports = true
    </configuration>
  </rustfmt>

  <cargo_nextest>
    <description>Next-generation test runner with better output and parallelism</description>
    <usage>cargo nextest run</usage>

    <features>
      <feature>Parallel test execution</feature>
      <feature>Better failure output</feature>
      <feature>JUnit XML output for CI</feature>
      <feature>Test retries</feature>
    </features>

    <configuration>
      <file_reference>.config/nextest.toml</file_reference>
      [profile.default]
      retries = 2
      slow-timeout = { period = "60s", terminate-after = 2 }
      fail-fast = false
    </configuration>
  </cargo_nextest>

  <other_tools>
    <tool name="cargo-audit">
      <description>Security vulnerability scanning</description>
    </tool>
    <tool name="cargo-deny">
      <description>Dependency license and security checks</description>
    </tool>
    <tool name="cargo-outdated">
      <description>Check for outdated dependencies</description>
    </tool>
    <tool name="cargo-watch">
      <description>Auto-rebuild on file changes</description>
    </tool>
    <tool name="cargo-expand">
      <description>Macro expansion debugging</description>
    </tool>
  </other_tools>
</toolchain>

<context7_integration>
  <description>Use Context7 MCP for up-to-date Rust documentation</description>

  <rust_libraries>
    <library name="The Rust Book" id="/rust-lang/book" />
    <library name="Cargo" id="/rust-lang/cargo.git" />
    <library name="Rust Clippy" id="/rust-lang/rust-clippy" />
    <library name="Rustfmt" id="/rust-lang/rustfmt" />
    <library name="Rust Reference" id="/rust-lang/reference.git" />
    <library name="Rust by Example" id="/rust-lang/rust-by-example.git" />
    <library name="cargo-nextest" id="/websites/nexte_st" />
  </rust_libraries>

  <usage_patterns>
    <pattern name="language_reference">
      <step>resolve-library-id libraryName="rust lang"</step>
      <step>get-library-docs context7CompatibleLibraryID="/rust-lang/book" topic="ownership"</step>
    </pattern>

    <pattern name="cargo_configuration">
      <step>get-library-docs context7CompatibleLibraryID="/rust-lang/cargo.git" topic="workspace"</step>
    </pattern>

    <pattern name="clippy_lints">
      <step>get-library-docs context7CompatibleLibraryID="/rust-lang/rust-clippy" topic="lints configuration"</step>
    </pattern>
  </usage_patterns>
</context7_integration>

<best_practices>
  <practice priority="critical">Use cargo check for fast iteration during development</practice>
  <practice priority="critical">Run cargo clippy before committing</practice>
  <practice priority="critical">Format with cargo fmt for consistent style</practice>
  <practice priority="high">Use workspace for multi-crate projects</practice>
  <practice priority="high">Prefer &str over String for function parameters</practice>
  <practice priority="high">Use impl Trait for return types when possible</practice>
  <practice priority="medium">Document public API with /// doc comments</practice>
  <practice priority="medium">Write unit tests alongside code in same file</practice>
  <practice priority="medium">Use integration tests in tests/ for API testing</practice>
  <practice priority="medium">Set rust-version in Cargo.toml for MSRV</practice>
</best_practices>

<rules priority="critical">
  <rule>Run cargo clippy before committing; fix all warnings</rule>
  <rule>Prefer safe Rust over unsafe blocks; document safety invariants when unsafe is needed</rule>
  <rule>Use Result and Option types; never unwrap() in library code</rule>
</rules>

<rules priority="standard">
  <rule>Use cargo fmt for consistent formatting</rule>
  <rule>Prefer &str over String for function parameters</rule>
  <rule>Write unit tests in same file, integration tests in tests/ directory</rule>
  <rule>Use cargo check for fast iteration during development</rule>
</rules>

<workflow>
  <phase name="analyze">
    <objective>Understand Rust code requirements</objective>
    <step>1. Check Cargo.toml for crate configuration</step>
    <step>2. Review existing patterns and traits</step>
    <step>3. Identify ownership and lifetime requirements</step>
  </phase>
  <phase name="implement">
    <objective>Write safe, idiomatic Rust code</objective>
    <step>1. Design with ownership in mind</step>
    <step>2. Use Result/Option for error handling</step>
    <step>3. Follow Rust API guidelines</step>
  </phase>
  <phase name="validate">
    <objective>Verify Rust code correctness</objective>
    <step>1. Run cargo check for quick validation</step>
    <step>2. Run cargo clippy for lints</step>
    <step>3. Run cargo test for testing</step>
  </phase>
</workflow>

<error_escalation>
  <level severity="low">
    <example>Clippy warning about style</example>
    <action>Fix warning, maintain idiomatic code</action>
  </level>
  <level severity="medium">
    <example>Borrow checker error</example>
    <action>Redesign ownership, avoid unsafe unless necessary</action>
  </level>
  <level severity="high">
    <example>Breaking change in public API</example>
    <action>Stop, present migration options to user</action>
  </level>
  <level severity="critical">
    <example>Unsafe code without proper justification</example>
    <action>Block operation, require safe alternatives</action>
  </level>
</error_escalation>

<constraints>
  <must>Prefer safe Rust over unsafe blocks</must>
  <must>Use Result and Option for error handling</must>
  <must>Follow Rust API guidelines for public APIs</must>
  <avoid>Using unwrap() in library code</avoid>
  <avoid>Unnecessary Clone implementations</avoid>
  <avoid>Unsafe code without safety documentation</avoid>
</constraints>

<related_agents>
  <agent name="design">Ownership architecture, trait design, and type system modeling</agent>
  <agent name="execute">Rust implementation with proper lifetime management and error handling</agent>
  <agent name="code-quality">Run cargo clippy, cargo fmt, and enforce Rust idioms</agent>
</related_agents>

<related_skills>
  <skill name="serena-usage">Navigate trait implementations and module hierarchies</skill>
  <skill name="context7-usage">Fetch Rust book, cargo, and clippy documentation</skill>
  <skill name="investigation-patterns">Debug borrow checker errors, lifetime issues, and performance bottlenecks</skill>
</related_skills>

---
name: Refactoring Deprecated Code
description: Systematically scans for deprecated library functions, APIs, and language features, then automatically updates code to use modern alternatives. Handles migration guides, version compatibility, and integration testing. Use when detecting deprecation warnings, updating dependencies, addressing API evolution, or when the user mentions deprecated APIs, legacy code, or migration needs.
---

# Refactoring Deprecated Code

Automatically detect and refactor deprecated library functions, APIs, and language features to modern alternatives.

## What you should do

1. **Scan for deprecation indicators** – Systematically identify deprecated usage:

   **Compiler/Runtime Warnings:**
   - Capture deprecation warnings from build processes, linters, and IDEs
   - Parse warning messages for specific deprecated functions and suggested replacements
   - Identify severity levels (warnings vs. errors) and timeline for removal

   **Static Code Analysis:**
   - Search for known deprecated patterns using language-specific tools:
     - Python: `bandit`, `pylint`, `mypy` for deprecated library usage
     - JavaScript/Node.js: ESLint rules, TypeScript compiler warnings
     - Java: SpotBugs, PMD, or IDE deprecation annotations
     - Go: `go vet`, staticcheck for deprecated usage
     - Rust: Clippy warnings and compiler deprecation notices

   **Documentation and Changelog Review:**
   - Review library changelogs for deprecation announcements
   - Check migration guides and upgrade documentation
   - Identify deprecation timelines and recommended alternatives

2. **Categorize deprecated usage by impact** – Organize findings systematically:

   **Severity Classification:**
   - **Critical**: APIs scheduled for removal in next major version
   - **High**: Functions deprecated for >1 year or with security implications
   - **Medium**: Recently deprecated functions with clear alternatives
   - **Low**: Soft deprecations or style preference changes

   **Usage Analysis:**
   - Count occurrences of each deprecated function across the codebase
   - Identify high-frequency usage patterns requiring batch updates
   - Map dependencies between deprecated APIs and application logic
   - Assess complexity of required refactoring for each deprecation

3. **Research modern alternatives and migration paths** – Identify replacement strategies:

   **Direct Replacements:**
   - Simple function/method renames with identical signatures
   - Updated import paths or module names
   - Parameter order changes or new required parameters
   - Return value format changes requiring minimal adaptation

   **Complex Migrations:**
   - API paradigm shifts (e.g., synchronous to asynchronous)
   - Architectural changes (e.g., callback-based to Promise-based)
   - Configuration format updates (e.g., JSON to YAML, environment variables)
   - Framework migration patterns (e.g., class-based to functional components)

4. **Create automated refactoring scripts** – Develop transformation tools:

   **Language-Specific Refactoring Tools:**
   - Python: Use `ast` module, `libcst`, or `rope` for code transformation
   - JavaScript: Leverage `jscodeshift`, Babel transforms, or ESLint autofix rules
   - Java: Utilize OpenRewrite, Refaster, or IDE refactoring APIs
   - Go: Use `gofmt`, `gorename`, or custom AST manipulation
   - Rust: Apply `cargo fix` or custom syntax tree transformations

   **Pattern-Based Replacements:**
   - Create regex-based find-and-replace for simple cases
   - Develop AST-based transformations for complex structural changes
   - Handle edge cases like nested calls, conditional usage, or exception handling

5. **Implement refactoring in phases** – Execute systematic transformation:

   **Phase 1 - Low-Risk Direct Replacements:**
   - Start with simple function renames and import updates
   - Apply automated transformations to straightforward patterns
   - Update configuration files and static references
   - Test each batch of changes before proceeding

   **Phase 2 - Medium Complexity Migrations:**
   - Refactor API usage patterns requiring parameter changes
   - Update error handling and return value processing
   - Modify configuration and initialization patterns
   - Validate functionality with comprehensive testing

   **Phase 3 - High Complexity Architectural Changes:**
   - Implement paradigm shifts (sync to async, callback to Promise)
   - Refactor large-scale architectural patterns
   - Update related documentation and examples
   - Perform extensive integration and regression testing

6. **Validate refactoring accuracy** – Ensure correctness and completeness:

   **Automated Testing:**
   - Run full test suite after each refactoring phase
   - Execute integration tests to verify external API interactions
   - Perform regression testing to catch behavioral changes
   - Use property-based testing for complex transformations

   **Manual Verification:**
   - Review critical code paths and complex transformations manually
   - Verify that edge cases and error conditions are handled correctly
   - Check that performance characteristics remain acceptable
   - Ensure logging and debugging functionality still works

7. **Update documentation and dependencies** – Maintain project consistency:

   **Dependency Management:**
   - Update `package.json`, `requirements.txt`, or similar manifest files
   - Remove deprecated dependencies and add new required packages
   - Update minimum version requirements for upgraded libraries
   - Resolve version conflicts and peer dependency issues

   **Documentation Updates:**
   - Update code comments referring to deprecated functions
   - Revise README files with new usage examples
   - Update API documentation and development guides
   - Create migration notes for other developers

8. **Integrate findings into existing roadmap** – Thoughtfully update `ROADMAP.md`:

   **Review existing maintenance initiatives:**
   - Read current ROADMAP.md to understand planned dependency updates
   - Identify existing refactoring, modernization, or technical debt initiatives
   - Understand current maintenance priorities and resource allocation

   **Merge deprecation findings intelligently:**
   - Consolidate with existing library upgrade and maintenance work
   - Integrate high-priority deprecations with existing quality improvement initiatives
   - Balance deprecation fixes with new feature development based on project priorities
   - Update timeline estimates considering deprecation urgency and complexity

9. **Create prevention measures** – Establish ongoing deprecation management:

   **Automated Detection:**
   - Add deprecation warnings to CI/CD pipeline checks
   - Configure dependency scanning tools to flag deprecated packages
   - Set up automated alerts for new deprecation announcements
   - Create regular scheduled scans for emerging deprecations

   **Team Practices:**
   - Document preferred alternatives to commonly deprecated patterns
   - Add deprecation awareness to code review checklists
   - Establish dependency update policies and schedules
   - Train team on recognizing and avoiding deprecated usage

**LANGUAGE-SPECIFIC DEPRECATION PATTERNS:**

**Python:**
- Function/method renames and module reorganizations
- Parameter changes and new argument requirements
- Import path updates (e.g., `imp` → `importlib`)
- String formatting evolution (`%` → `.format()` → f-strings)

**JavaScript/Node.js:**
- Browser API changes and polyfill requirements
- Package.json script updates and tooling migrations
- Framework version updates (React, Vue, Angular)
- Node.js built-in module changes and new APIs

**Java:**
- Deprecated annotation handling and replacement identification
- Library migration patterns (e.g., Date → LocalDateTime)
- Build tool updates (Maven, Gradle plugin deprecations)
- Spring Framework and enterprise library evolution

**MIGRATION BEST PRACTICES:**

- **Incremental approach**: Migrate in small, testable batches
- **Backward compatibility**: Maintain compatibility during transition periods
- **Comprehensive testing**: Validate each change thoroughly
- **Documentation**: Record migration decisions and rationale
- **Team communication**: Keep stakeholders informed of breaking changes

**DELIVERABLES:**

For each deprecation refactoring session:
- **Updated ROADMAP.md**: Integrated deprecation fixes within unified project maintenance plan
- **Migration summary**: List of deprecated functions updated and alternatives adopted
- **Test validation report**: Evidence that refactoring maintains functionality
- **Prevention strategy**: Measures to catch future deprecations early

The goal is to systematically eliminate deprecated code usage while maintaining functionality, improving maintainability, and establishing processes to prevent future deprecation accumulation.
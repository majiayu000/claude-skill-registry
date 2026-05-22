---
name: ameba-custom-rules
description: Use when creating custom Ameba rules for Crystal code analysis including rule development, AST traversal, issue reporting, and rule testing.
allowed-tools:
  - Bash
  - Read
---

# Ameba Custom Rules

Create custom linting rules for Ameba to enforce project-specific code quality standards and catch domain-specific code smells in Crystal projects.

## Understanding Custom Rules

Custom Ameba rules allow you to:

- Enforce project-specific coding standards
- Catch domain-specific anti-patterns
- Validate business logic constraints
- Ensure consistency across large codebases
- Create reusable rule libraries for your organization
- Extend Ameba's built-in capabilities

## Rule Anatomy

### Basic Rule Structure

Every Ameba rule inherits from `Ameba::Rule::Base` and follows this structure:

```crystal
module Ameba::Rule::Custom
  # Rule that enforces documentation on public classes
  class DocumentedClasses < Base
    properties do
      description "Enforces public classes to be documented"
    end

    MSG = "Class must be documented with a comment"

    def test(source)
      AST::NodeVisitor.new self, source
    end

    def test(source, node : Crystal::ClassDef)
      return unless node.visibility.public?

      doc = node.doc
      issue_for(node, MSG) if doc.nil? || doc.empty?
    end
  end
end
```

### Key Components

1. **Module namespace** - Custom rules typically use `Ameba::Rule::Custom` or `Ameba::Rule::<Category>`
2. **Base class** - All rules inherit from `Ameba::Rule::Base`
3. **Properties block** - Defines rule metadata and configuration
4. **Message constant** - The error message shown to users
5. **Test method** - Entry point that initializes the AST visitor
6. **Overloaded test methods** - Handle specific AST node types

## Creating Your First Custom Rule

### Step 1: Project Setup

Create a Crystal library for your custom rules:

```bash
# Initialize a new Crystal library
crystal init lib ameba-custom-rules
cd ameba-custom-rules
```

Update `shard.yml`:

```yaml
name: ameba-custom-rules
version: 0.1.0
authors:
  - Your Name <your.email@example.com>

description: Custom Ameba rules for your project

crystal: ">= 1.0.0"

license: MIT

development_dependencies:
  ameba:
    github: crystal-ameba/ameba
    version: ~> 1.6.0
```

**Important:** Ameba should be a development dependency to avoid version conflicts.

### Step 2: Implement a Simple Rule

Create `src/ameba-custom-rules/no_sleep_in_production.cr`:

```crystal
require "ameba"

module Ameba::Rule::Custom
  # Prevents sleep() calls in production code
  class NoSleepInProduction < Base
    properties do
      description "Prevents sleep calls in production code"
      enabled true
    end

    MSG = "Avoid using sleep() in production code; use proper background jobs"

    def test(source)
      AST::NodeVisitor.new self, source
    end

    def test(source, node : Crystal::Call)
      return unless node.name == "sleep"

      issue_for node, MSG
    end
  end
end
```

### Step 3: Register and Use the Rule

Create main file `src/ameba-custom-rules.cr`:

```crystal
require "ameba"
require "./ameba-custom-rules/*"

# Rules are automatically registered through inheritance
```

Update your project's Ameba configuration:

```yaml
# .ameba.yml
Custom/NoSleepInProduction:
  Enabled: true
  Severity: Warning
```

### Step 4: Test Your Rule

Create `spec/ameba-custom-rules/no_sleep_in_production_spec.cr`:

```crystal
require "../spec_helper"

module Ameba::Rule::Custom
  describe NoSleepInProduction do
    it "reports sleep calls" do
      rule = NoSleepInProduction.new

      source = Source.new %(
        def process
          sleep 5.seconds
        end
      )

      rule.test(source)
      source.issues.size.should eq(1)
    end

    it "allows code without sleep" do
      rule = NoSleepInProduction.new

      source = Source.new %(
        def process
          puts "Processing"
        end
      )

      rule.test(source)
      source.issues.should be_empty
    end
  end
end
```

## Advanced Rule Examples

### Enforcing Naming Conventions

```crystal
module Ameba::Rule::Custom
  # Enforces that service classes end with "Service"
  class ServiceClassNaming < Base
    properties do
      description "Service classes must end with 'Service'"
      enabled true
    end

    MSG = "Service class name should end with 'Service'"

    def test(source)
      AST::NodeVisitor.new self, source
    end

    def test(source, node : Crystal::ClassDef)
      class_name = node.name.to_s

      # Check if class is in services directory
      return unless source.path.includes?("/services/")

      # Check if name ends with Service
      unless class_name.ends_with?("Service")
        issue_for node.name, MSG
      end
    end
  end
end
```

### Detecting Dangerous Method Calls

```crystal
module Ameba::Rule::Custom
  # Prevents dangerous ActiveRecord-like methods
  class NoDangerousDatabaseCalls < Base
    properties do
      description "Prevents dangerous database operations"
      dangerous_methods ["delete_all", "destroy_all", "update_all"]
    end

    MSG = "Dangerous method %s without conditions"

    def test(source)
      AST::NodeVisitor.new self, source
    end

    def test(source, node : Crystal::Call)
      return unless dangerous_methods.includes?(node.name)

      # Check if call has arguments (conditions)
      if node.args.empty?
        message = MSG % node.name
        issue_for node, message
      end
    end
  end
end
```

### Enforcing Error Handling

```crystal
module Ameba::Rule::Custom
  # Ensures HTTP client calls have error handling
  class HttpErrorHandling < Base
    properties do
      description "HTTP client calls must handle errors"
      enabled true
    end

    MSG = "HTTP client calls should be wrapped in begin/rescue"

    def test(source)
      @in_rescue_block = false
      AST::NodeVisitor.new self, source
    end

    def test(source, node : Crystal::ExceptionHandler)
      @in_rescue_block = true
      true  # Continue visiting children
    end

    def test(source, node : Crystal::Call)
      return if @in_rescue_block

      # Check for HTTP client calls
      if node.obj.try(&.to_s.includes?("HTTP"))
        issue_for node, MSG
      end
    end
  end
end
```

### Validating Method Complexity

```crystal
module Ameba::Rule::Custom
  # Limits method complexity
  class MethodComplexity < Base
    properties do
      description "Methods should not be too complex"
      max_complexity 10
    end

    MSG = "Method complexity (%d) exceeds maximum (%d)"

    def test(source)
      AST::NodeVisitor.new self, source
    end

    def test(source, node : Crystal::Def)
      complexity = calculate_complexity(node)

      if complexity > max_complexity
        message = MSG % [complexity, max_complexity]
        issue_for node, message
      end
    end

    private def calculate_complexity(node)
      counter = ComplexityCounter.new
      node.accept(counter)
      counter.complexity
    end

    private class ComplexityCounter < Crystal::Visitor
      getter complexity : Int32 = 1

      def visit(node : Crystal::If)
        @complexity += 1
        true
      end

      def visit(node : Crystal::Case)
        @complexity += 1
        true
      end

      def visit(node : Crystal::While)
        @complexity += 1
        true
      end

      def visit(node : Crystal::Call)
        # Count logical operators
        if node.name.in?("&&", "||")
          @complexity += 1
        end
        true
      end

      def visit(node : Crystal::ASTNode)
        true
      end
    end
  end
end
```

### Enforcing Documentation Standards

```crystal
module Ameba::Rule::Custom
  # Requires documentation with specific format
  class DocumentationFormat < Base
    properties do
      description "Public methods must have documentation with examples"
      enabled true
      require_examples true
    end

    MSG_NO_DOC = "Public method must have documentation"
    MSG_NO_EXAMPLE = "Documentation must include usage examples"

    def test(source)
      AST::NodeVisitor.new self, source
    end

    def test(source, node : Crystal::Def)
      return unless node.visibility.public?
      return if node.name.starts_with?("initialize")

      doc = node.doc

      if doc.nil? || doc.empty?
        issue_for node, MSG_NO_DOC
        return
      end

      if require_examples && !has_example?(doc)
        issue_for node, MSG_NO_EXAMPLE
      end
    end

    private def has_example?(doc : String)
      doc.includes?("```") || doc.includes?("Example:")
    end
  end
end
```

## Working with AST Nodes

### Common AST Node Types

```crystal
# Class definitions
def test(source, node : Crystal::ClassDef)
  node.name            # Class name
  node.visibility      # public?, private?, protected?
  node.doc            # Documentation comment
  node.abstract?      # Is abstract class?
  node.superclass     # Parent class
end

# Method definitions
def test(source, node : Crystal::Def)
  node.name           # Method name
  node.args           # Arguments
  node.body           # Method body
  node.return_type    # Return type annotation
  node.visibility     # Visibility modifier
  node.doc           # Documentation
end

# Method calls
def test(source, node : Crystal::Call)
  node.name          # Method name
  node.obj           # Receiver object
  node.args          # Arguments
  node.named_args    # Named arguments
  node.block         # Block argument
end

# Variable assignments
def test(source, node : Crystal::Assign)
  node.target        # Left side (variable)
  node.value         # Right side (value)
end

# Conditionals
def test(source, node : Crystal::If)
  node.cond          # Condition
  node.then          # Then branch
  node.else          # Else branch
end

# Loops
def test(source, node : Crystal::While)
  node.cond          # Loop condition
  node.body          # Loop body
end
```

### Traversal Patterns

```crystal
# Pattern 1: Track state during traversal
class MyRule < Base
  def test(source)
    @inside_block = false
    @depth = 0
    AST::NodeVisitor.new self, source
  end

  def test(source, node : Crystal::Block)
    @inside_block = true
    @depth += 1
    true  # Continue visiting children
  end
end

# Pattern 2: Collect information then analyze
class MyRule < Base
  def test(source)
    @method_names = [] of String
    visitor = AST::NodeVisitor.new self, source
    analyze_collected_data(source)
  end

  def test(source, node : Crystal::Def)
    @method_names << node.name
  end

  private def analyze_collected_data(source)
    # Analyze @method_names
  end
end

# Pattern 3: Parent-child relationships
class MyRule < Base
  def test(source, node : Crystal::ClassDef)
    # Visit only methods in this class
    node.body.accept(MethodVisitor.new(self, source))
  end

  private class MethodVisitor < Crystal::Visitor
    def initialize(@rule : MyRule, @source : Source)
    end

    def visit(node : Crystal::Def)
      @rule.check_method(node, @source)
      true
    end

    def visit(node : Crystal::ASTNode)
      true
    end
  end
end
```

## Rule Configuration

### Configurable Properties

```crystal
module Ameba::Rule::Custom
  class ConfigurableRule < Base
    properties do
      description "A rule with configurable properties"

      # Boolean properties
      enabled true
      strict_mode false

      # Numeric properties
      max_length 100
      min_length 3

      # String properties
      prefix "test_"
      suffix "_spec"

      # Array properties
      allowed_names ["foo", "bar", "baz"]
      excluded_paths ["spec/**/*", "lib/**/*"]
    end

    def test(source)
      # Use properties
      return unless enabled

      if strict_mode
        # Apply strict checks
      end

      AST::NodeVisitor.new self, source
    end
  end
end
```

### Configuration in .ameba.yml

```yaml
Custom/ConfigurableRule:
  Enabled: true
  Severity: Warning
  StrictMode: true
  MaxLength: 120
  MinLength: 5
  Prefix: "app_"
  AllowedNames:
    - "primary"
    - "secondary"
  ExcludedPaths:
    - "spec/fixtures/**"
    - "db/migrations/**"
```

## Issue Reporting

### Basic Issue Reporting

```crystal
# Simple issue
issue_for node, "Error message"

# Issue with interpolation
issue_for node, "Found #{count} violations"

# Issue at specific location
issue_for node.name, "Method name violates convention"

# Issue with custom location
issue_for(
  {node.location.try(&.line_number) || 1, 1},
  node.end_location,
  "Custom message"
)
```

### Issue Severity

```crystal
# Controlled by configuration
Custom/MyRule:
  Severity: Error    # Blocks CI
  # or
  Severity: Warning  # Important but not blocking
  # or
  Severity: Convention  # Style preference
```

### Rich Issue Messages

```crystal
module Ameba::Rule::Custom
  class RichMessages < Base
    MSG_TEMPLATE = <<-MSG
      Method '%{method}' is too long (%{actual} lines, max %{max} allowed)
      Consider extracting to smaller methods or using composition.
      MSG

    def test(source, node : Crystal::Def)
      line_count = count_lines(node)

      if line_count > max_lines
        message = MSG_TEMPLATE % {
          method: node.name,
          actual: line_count,
          max: max_lines
        }
        issue_for node, message
      end
    end
  end
end
```

## Testing Custom Rules

### Comprehensive Test Suite

```crystal
require "../spec_helper"

module Ameba::Rule::Custom
  describe DocumentedClasses do
    context "with documented class" do
      it "passes" do
        rule = DocumentedClasses.new

        source = Source.new %(
          # This is a documented class
          class MyClass
          end
        )

        rule.test(source)
        source.issues.should be_empty
      end
    end

    context "with undocumented public class" do
      it "reports an issue" do
        rule = DocumentedClasses.new

        source = Source.new %(
          class MyClass
          end
        )

        rule.test(source)
        source.issues.size.should eq(1)
        source.issues.first.message.should contain("documented")
      end
    end

    context "with private class" do
      it "allows undocumented private classes" do
        rule = DocumentedClasses.new

        source = Source.new %(
          private class InternalClass
          end
        )

        rule.test(source)
        source.issues.should be_empty
      end
    end

    context "with empty documentation" do
      it "reports an issue" do
        rule = DocumentedClasses.new

        source = Source.new %(
          #
          class MyClass
          end
        )

        rule.test(source)
        source.issues.size.should eq(1)
      end
    end

    context "configuration" do
      it "can be disabled" do
        rule = DocumentedClasses.new
        rule.enabled = false

        source = Source.new %(
          class MyClass
          end
        )

        rule.test(source)
        source.issues.should be_empty
      end
    end
  end
end
```

### Test Helpers

```crystal
# spec/spec_helper.cr
require "spec"
require "ameba"
require "../src/ameba-custom-rules"

module Ameba
  # Helper to create test sources
  def self.source(code : String, path = "source.cr")
    Source.new(code, path)
  end

  # Helper to expect issues
  def self.expect_issue(rule, code)
    source = Source.new(code)
    rule.test(source)
    source.issues.empty?.should be_false
  end

  # Helper to expect no issues
  def self.expect_no_issue(rule, code)
    source = Source.new(code)
    rule.test(source)
    source.issues.should be_empty
  end
end

# Usage in specs
describe MyRule do
  it "reports violations" do
    rule = MyRule.new
    Ameba.expect_issue rule, %(
      def bad_code
      end
    )
  end
end
```

## Packaging and Distribution

### Creating a Reusable Rule Package

```crystal
# shard.yml
name: ameba-company-rules
version: 1.0.0

description: |
  Company-specific Ameba rules for Crystal projects.
  Enforces coding standards and best practices.

authors:
  - Company DevTools <devtools@company.com>

crystal: ">= 1.0.0"
license: MIT

development_dependencies:
  ameba:
    github: crystal-ameba/ameba
    version: ~> 1.6.0

# Optional: Add to targets for binary
targets:
  ameba-company:
    main: src/cli.cr
```

### Distribution Strategy

```crystal
# Option 1: As a shard dependency
# In user's shard.yml
development_dependencies:
  ameba:
    github: crystal-ameba/ameba
  ameba-company-rules:
    github: company/ameba-company-rules

# Option 2: As vendored rules
# Copy rule files to project's lib/ameba-rules/
# Include in custom ameba binary

# Option 3: As a plugin
# Create standalone executable that extends ameba
```

### Custom Ameba Binary

```crystal
# bin/ameba-custom.cr
require "ameba/cli"
require "../lib/ameba-company-rules/src/ameba-company-rules"

# Rules are automatically discovered
Ameba::CLI.run
```

Build and distribute:

```bash
crystal build bin/ameba-custom.cr -o bin/ameba-custom
# Distribute binary or build from source
```

## Real-World Rule Examples

### Preventing N+1 Queries

```crystal
module Ameba::Rule::Custom
  class PreventNPlusOne < Base
    properties do
      description "Detects potential N+1 query patterns"
    end

    MSG = "Potential N+1 query: accessing association in loop"

    def test(source)
      @in_loop = false
      AST::NodeVisitor.new self, source
    end

    def test(source, node : Crystal::While | Crystal::Call)
      if node.is_a?(Crystal::Call) && node.name.in?("each", "map")
        @in_loop = true
        node.block.try(&.accept(self))
        @in_loop = false
        return false  # Don't visit block again
      end
      true
    end

    def test(source, node : Crystal::Call)
      return unless @in_loop

      # Detect association access patterns
      if looks_like_association?(node)
        issue_for node, MSG
      end
    end

    private def looks_like_association?(node)
      # Simplified detection
      node.name.in?("user", "posts", "comments") &&
        node.obj != nil
    end
  end
end
```

### Enforcing API Versioning

```crystal
module Ameba::Rule::Custom
  class ApiVersioning < Base
    properties do
      description "API controllers must be versioned"
    end

    MSG = "API controller must be in a versioned namespace (e.g., V1::)"

    def test(source)
      return unless source.path.includes?("/api/")
      AST::NodeVisitor.new self, source
    end

    def test(source, node : Crystal::ClassDef)
      return unless node.name.to_s.ends_with?("Controller")

      unless has_version_namespace?(node)
        issue_for node.name, MSG
      end
    end

    private def has_version_namespace?(node)
      # Check if class name includes version (V1::, V2::, etc.)
      node.name.to_s.matches?(/V\d+::/)
    end
  end
end
```

## When to Use This Skill

Use the ameba-custom-rules skill when:

- Enforcing project-specific coding standards not covered by built-in rules
- Detecting domain-specific anti-patterns or code smells
- Validating business logic constraints in code
- Creating organization-wide linting standards
- Migrating from another language and enforcing new patterns
- Preventing specific bugs that have occurred in production
- Ensuring consistency across microservices
- Teaching team members about code quality through automated feedback
- Enforcing architectural decisions (e.g., layer boundaries)
- Standardizing error handling, logging, or monitoring patterns

## Best Practices

1. **Start simple** - Begin with basic rules before tackling complex AST traversals
2. **Test thoroughly** - Write comprehensive specs covering edge cases
3. **Provide clear messages** - Error messages should explain what's wrong and suggest fixes
4. **Make rules configurable** - Use properties for thresholds and options
5. **Document your rules** - Include description and examples in properties block
6. **Use specific node types** - Overload `test` for specific AST nodes, not generic traversal
7. **Consider performance** - Avoid complex operations in hot paths; cache results when possible
8. **Follow naming conventions** - Use descriptive rule names that match their purpose
9. **Provide fix suggestions** - When possible, explain how to resolve the issue
10. **Scope appropriately** - Only check relevant files (use source.path checks)
11. **Handle nil safely** - Use try(&.) when accessing potentially nil AST properties
12. **Avoid false positives** - Better to miss some cases than flag correct code
13. **Version your rules** - Track rule versions and breaking changes
14. **Keep rules focused** - One rule should check one thing (Single Responsibility)
15. **Integrate with CI** - Ensure custom rules work in automated environments

## Common Pitfalls

1. **Overly broad matching** - Catching too many cases and producing false positives
2. **Not handling nil** - AST nodes may have nil properties causing crashes
3. **Ignoring visibility** - Checking private methods when only public API matters
4. **Complex visitor logic** - Making traversal code hard to understand and maintain
5. **Missing edge cases** - Not testing unusual but valid code patterns
6. **Poor error messages** - Vague messages that don't help developers fix issues
7. **Hard-coded values** - Not making thresholds and options configurable
8. **Checking generated code** - Flagging auto-generated files that shouldn't be changed
9. **Performance issues** - Complex rules that slow down analysis significantly
10. **Dependency conflicts** - Using Ameba as regular dependency instead of development_dependencies
11. **Not using properties** - Hard-coding configuration instead of using properties block
12. **Incomplete testing** - Not testing disabled state, edge cases, or configuration
13. **Tight coupling** - Rules that depend on other rules or specific file structures
14. **Unclear scope** - Rules that apply to wrong files or contexts
15. **Version incompatibility** - Not testing against multiple Ameba versions

## Resources

- [Ameba Custom Rule Tutorial](https://crystal-ameba.github.io/2019/07/22/how-to-write-extension/)
- [Ameba Internals Documentation](https://crystal-ameba.github.io/2019/09/03/internals/)
- [Ameba API Documentation](https://crystal-ameba.github.io/ameba/)
- [Crystal AST Documentation](https://crystal-lang.org/api/latest/Crystal/Macros.html)
- [Crystal Compiler Source](https://github.com/crystal-lang/crystal/tree/master/src/compiler)
- [Ameba GitHub Repository](https://github.com/crystal-ameba/ameba)
- [Example Custom Rules](https://github.com/crystal-ameba/ameba/tree/master/src/ameba/rule)

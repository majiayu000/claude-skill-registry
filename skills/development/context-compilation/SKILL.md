---
name: "Context Compilation with cclsp"
description: "LSP-powered context extraction using cclsp MCP tools, Solargraph, and Sorbet for type-safe code generation. Trigger keywords: cclsp, LSP, context compilation, interface extraction, vocabulary, Guardian, Sorbet, type checking, find_definition, get_diagnostics, Solargraph, type safety"
version: 1.0.0
---

# Context Compilation with cclsp + Sorbet

This skill provides patterns for LSP-powered context extraction and type-safe code generation using cclsp MCP tools, Solargraph, and Sorbet.

## 1. Tool Stack Overview

### 1.1 cclsp MCP Bridge

The cclsp MCP server provides Claude Code access to Language Server Protocol functionality:

| Tool | Purpose | Use Case |
|------|---------|----------|
| `mcp__cclsp__find_definition` | Find symbol definitions | Locate where methods/classes are defined |
| `mcp__cclsp__find_references` | Find all references | Discover symbol usage patterns |
| `mcp__cclsp__get_diagnostics` | Get errors/warnings | Validate code before execution |
| `mcp__cclsp__rename_symbol` | Rename symbols | Safe refactoring |
| `mcp__cclsp__rename_symbol_strict` | Rename at position | Precise symbol renaming |
| `mcp__cclsp__restart_server` | Restart LSP | Recover from errors |

### 1.2 Solargraph (Ruby LSP)

Solargraph provides Ruby-specific language intelligence:

- **Method completion**: Know what methods exist on objects
- **Go to definition**: Jump to class/method definitions
- **Hover documentation**: Inline YARD documentation
- **Diagnostics**: Syntax errors, undefined methods
- **Workspace symbols**: Search all symbols in project

**Configuration** (`.solargraph.yml`):

```yaml
include:
  - "**/*.rb"
exclude:
  - spec/**/*
  - test/**/*
  - vendor/**/*
reporters:
  - rubocop
  - require_not_found
plugins: []
require_paths: []
domains: []
max_files: 5000
```

### 1.3 Sorbet (Type Checker)

Sorbet provides static type checking for Ruby:

- **Static analysis**: Catch type errors at compile time
- **Runtime checking**: Verify types during execution
- **Gradual typing**: Adopt incrementally with `# typed:` sigils
- **IDE integration**: LSP support via Sorbet Language Server

**Type Sigils**:

```ruby
# typed: ignore   # Skip this file
# typed: false    # Only syntax errors
# typed: true     # Check types
# typed: strict   # Require signatures
# typed: strong   # No T.untyped
```

**Common Commands**:

```bash
# Type check entire project
bundle exec srb tc

# Type check specific file
bundle exec srb tc app/models/user.rb

# Initialize Sorbet
bundle exec srb init

# Generate RBI files
bundle exec tapioca init
bundle exec tapioca dsl
bundle exec tapioca gems
```

### 1.4 Supporting Tools

| Tool | Purpose | Integration |
|------|---------|-------------|
| **parser gem** | AST analysis | Deep code structure analysis |
| **ripper** | Built-in Ruby parser | Fallback parsing, always available |
| **YARD** | Documentation | Solargraph uses YARD for docs |
| **Tapioca** | RBI generation | Generate type signatures for gems |

---

## 2. cclsp Tool Reference

### 2.1 find_definition

Find where a symbol is defined:

```ruby
# Usage Pattern
mcp__cclsp__find_definition(
  file_path: "app/services/payment_service.rb",
  symbol_name: "PaymentGateway",
  symbol_kind: "class"  # optional: class, method, module
)

# Returns
{
  "definitions": [
    {
      "file": "app/gateways/payment_gateway.rb",
      "line": 5,
      "column": 1,
      "symbol": "PaymentGateway"
    }
  ]
}
```

**Common symbol_kind values**:
- `class` - Class definitions
- `module` - Module definitions
- `method` - Instance methods
- `function` - Module/class methods
- `variable` - Local/instance variables
- `constant` - Constants

### 2.2 find_references

Find all usages of a symbol:

```ruby
# Usage Pattern
mcp__cclsp__find_references(
  file_path: "app/models/user.rb",
  symbol_name: "authenticate",
  include_declaration: true
)

# Returns
{
  "references": [
    {
      "file": "app/models/user.rb",
      "line": 45,
      "column": 3,
      "context": "def authenticate(password)"
    },
    {
      "file": "app/controllers/sessions_controller.rb",
      "line": 12,
      "column": 8,
      "context": "if user.authenticate(params[:password])"
    }
  ]
}
```

### 2.3 get_diagnostics

Get errors and warnings for a file:

```ruby
# Usage Pattern
mcp__cclsp__get_diagnostics(
  file_path: "app/services/order_service.rb"
)

# Returns
{
  "diagnostics": [
    {
      "severity": 1,  # 1=Error, 2=Warning, 3=Info, 4=Hint
      "message": "Undefined method `foo' for OrderService",
      "range": {
        "start": {"line": 25, "character": 4},
        "end": {"line": 25, "character": 7}
      },
      "source": "solargraph"
    }
  ]
}
```

**Severity Levels**:
- `1` - Error (must fix)
- `2` - Warning (should investigate)
- `3` - Information (good to know)
- `4` - Hint (suggestions)

### 2.4 rename_symbol

Rename a symbol across the codebase:

```ruby
# Preview changes (dry_run)
mcp__cclsp__rename_symbol(
  file_path: "app/models/user.rb",
  symbol_name: "full_name",
  new_name: "display_name",
  dry_run: true
)

# Apply changes
mcp__cclsp__rename_symbol(
  file_path: "app/models/user.rb",
  symbol_name: "full_name",
  new_name: "display_name"
)
```

---

## 3. Interface Extraction Patterns

### 3.1 Extract Class Interface

Extract public interface from a class:

```ruby
# Pattern: Interface Extraction
def extract_interface(class_name, file_path)
  # 1. Find class definition
  definition = mcp__cclsp__find_definition(
    file_path: file_path,
    symbol_name: class_name,
    symbol_kind: "class"
  )

  # 2. Read the class file
  class_content = Read(definition.file)

  # 3. Extract public methods
  public_methods = class_content.scan(/^\s*def\s+(\w+)/).flatten

  # 4. For each method, find references to understand usage
  method_interfaces = public_methods.map do |method|
    refs = mcp__cclsp__find_references(
      file_path: definition.file,
      symbol_name: method
    )

    {
      name: method,
      defined_at: "#{definition.file}:#{method_line}",
      usage_count: refs.count,
      callers: refs.map { |r| r.file }.uniq
    }
  end

  method_interfaces
end
```

### 3.2 Extract Dependency Graph

Build a dependency graph for a class:

```ruby
# Pattern: Dependency Graph
def build_dependency_graph(entry_class, entry_file)
  graph = { nodes: [], edges: [] }
  visited = Set.new
  queue = [[entry_class, entry_file]]

  while queue.any?
    class_name, file_path = queue.shift
    next if visited.include?(class_name)
    visited.add(class_name)

    # Add node
    graph[:nodes] << { name: class_name, file: file_path }

    # Find references to other classes
    class_content = Read(file_path)
    constants = class_content.scan(/([A-Z][A-Za-z0-9]+)/).flatten.uniq

    constants.each do |const|
      definition = mcp__cclsp__find_definition(
        file_path: file_path,
        symbol_name: const,
        symbol_kind: "class"
      )

      if definition && !visited.include?(const)
        graph[:edges] << { from: class_name, to: const }
        queue << [const, definition.file]
      end
    end
  end

  graph
end
```

### 3.3 Per-Task Interface Extraction

Extract interfaces relevant to a specific task:

```ruby
# Pattern: Task-Specific Interface Extraction
def compile_task_context(task)
  context = {
    interfaces: [],
    vocabulary: [],
    cclsp_enhanced: true
  }

  # 1. Identify files mentioned in task
  target_files = task[:files] || []

  # 2. For each file, extract interfaces
  target_files.each do |file|
    # Get diagnostics first (validates file exists)
    diagnostics = mcp__cclsp__get_diagnostics(file_path: file)

    # Find all symbols in file
    symbols = extract_file_symbols(file)

    # For each symbol, get definition and references
    symbols.each do |symbol|
      definition = mcp__cclsp__find_definition(
        file_path: file,
        symbol_name: symbol[:name],
        symbol_kind: symbol[:kind]
      )

      references = mcp__cclsp__find_references(
        file_path: file,
        symbol_name: symbol[:name]
      )

      context[:interfaces] << {
        symbol: symbol[:name],
        kind: symbol[:kind],
        file: file,
        definition: definition,
        references: references.count,
        signature: extract_signature(definition)
      }
    end
  end

  context
end
```

---

## 4. Vocabulary Building Patterns

### 4.1 Project Vocabulary Extraction

Build a vocabulary of project-specific terms:

```ruby
# Pattern: Project Vocabulary
def build_project_vocabulary
  vocabulary = {
    models: [],
    services: [],
    controllers: [],
    patterns: [],
    domain_terms: []
  }

  # 1. Scan models
  Dir["app/models/**/*.rb"].each do |file|
    content = Read(file)

    # Extract class name
    if content =~ /class\s+(\w+)/
      model_name = $1
      vocabulary[:models] << {
        name: model_name,
        file: file,
        associations: content.scan(/(?:has_many|belongs_to|has_one)\s+:(\w+)/).flatten,
        scopes: content.scan(/scope\s+:(\w+)/).flatten,
        validations: content.scan(/validates\s+:(\w+)/).flatten
      }
    end
  end

  # 2. Scan services
  Dir["app/services/**/*.rb"].each do |file|
    content = Read(file)

    if content =~ /class\s+(\w+)/
      service_name = $1
      vocabulary[:services] << {
        name: service_name,
        file: file,
        public_methods: content.scan(/^\s*def\s+(\w+)/).flatten,
        dependencies: extract_dependencies(content)
      }
    end
  end

  # 3. Extract domain terms from comments and names
  all_files = Dir["app/**/*.rb"]
  all_files.each do |file|
    content = Read(file)

    # Extract from comments
    comments = content.scan(/#\s*(.+)$/).flatten

    # Extract from class/method names
    identifiers = content.scan(/(?:class|def|module)\s+(\w+)/).flatten

    # Add unique terms
    terms = (comments + identifiers).map(&:downcase).uniq
    vocabulary[:domain_terms].concat(terms)
  end

  vocabulary[:domain_terms].uniq!
  vocabulary
end
```

### 4.2 Symbol Vocabulary for Generation

Build vocabulary to guide code generation:

```ruby
# Pattern: Generation Vocabulary
def build_generation_vocabulary(target_file)
  vocab = {
    available_classes: [],
    available_methods: [],
    common_patterns: [],
    naming_conventions: []
  }

  # 1. Find all classes in the project
  Dir["app/**/*.rb"].each do |file|
    content = Read(file)
    classes = content.scan(/class\s+(\w+)/).flatten
    vocab[:available_classes].concat(classes)
  end

  # 2. For the target file's directory, find common patterns
  dir = File.dirname(target_file)
  sibling_files = Dir["#{dir}/*.rb"]

  sibling_files.each do |file|
    content = Read(file)

    # Extract method patterns
    methods = content.scan(/def\s+(\w+)/).flatten
    vocab[:available_methods].concat(methods)

    # Extract common patterns
    if content.include?("Result.success")
      vocab[:common_patterns] << "Result monad"
    end
    if content.include?("ApplicationService")
      vocab[:common_patterns] << "ApplicationService inheritance"
    end
  end

  vocab[:available_classes].uniq!
  vocab[:available_methods].uniq!
  vocab[:common_patterns].uniq!

  vocab
end
```

---

## 5. Guardian Validation Patterns

### 5.1 Pre-Generation Validation

Validate before generating code:

```ruby
# Pattern: Pre-Generation Check
def pre_generation_validate(target_file)
  validation = { passed: true, issues: [] }

  # 1. Check if cclsp is available
  begin
    mcp__cclsp__get_diagnostics(file_path: "Gemfile")
  rescue
    validation[:issues] << "cclsp not available - skipping LSP validation"
    return validation
  end

  # 2. Check existing file for errors
  if File.exist?(target_file)
    diagnostics = mcp__cclsp__get_diagnostics(file_path: target_file)
    errors = diagnostics.select { |d| d[:severity] == 1 }

    if errors.any?
      validation[:passed] = false
      validation[:issues] << "Existing file has #{errors.count} errors - fix first"
    end
  end

  # 3. Check parent class exists
  # (would need to parse generation template)

  validation
end
```

### 5.2 Post-Generation Validation (Guardian)

Validate after generating code:

```ruby
# Pattern: Guardian Validation
def guardian_validate(file_path)
  result = {
    passed: true,
    errors: [],
    warnings: [],
    suggestions: []
  }

  # 1. cclsp diagnostics (Solargraph)
  diagnostics = mcp__cclsp__get_diagnostics(file_path: file_path)

  diagnostics.each do |d|
    case d[:severity]
    when 1  # Error
      result[:passed] = false
      result[:errors] << {
        line: d[:range][:start][:line],
        message: d[:message],
        source: d[:source]
      }
    when 2  # Warning
      result[:warnings] << {
        line: d[:range][:start][:line],
        message: d[:message]
      }
    when 3, 4  # Info/Hint
      result[:suggestions] << {
        line: d[:range][:start][:line],
        message: d[:message]
      }
    end
  end

  # 2. Sorbet type checking (if available)
  sorbet_output = `bundle exec srb tc #{file_path} 2>&1`
  sorbet_errors = sorbet_output.lines.select { |l| l.start_with?(file_path) }

  sorbet_errors.each do |error|
    if error =~ /#{file_path}:(\d+):\s*(.+)/
      result[:passed] = false
      result[:errors] << {
        line: $1.to_i,
        message: $2,
        source: "sorbet"
      }
    end
  end

  result
end
```

### 5.3 Generate-Validate-Execute-Verify Cycle

Full implementation cycle with Guardian:

```ruby
# Pattern: Full Implementation Cycle
def implement_with_guardian(file_path, specification, max_attempts: 3)
  attempt = 0

  loop do
    attempt += 1
    puts "Attempt #{attempt}/#{max_attempts}: #{file_path}"

    # 1. GENERATE
    puts "  1/4 GENERATE: Writing code..."
    generate_code(file_path, specification)

    # 2. VALIDATE (Guardian)
    puts "  2/4 VALIDATE: Running Guardian..."
    validation = guardian_validate(file_path)

    unless validation[:passed]
      puts "  Guardian found #{validation[:errors].count} errors"

      if attempt >= max_attempts
        return { success: false, reason: "Max attempts reached" }
      end

      # Apply fixes and retry
      apply_guardian_fixes(file_path, validation[:errors])
      next
    end

    # 3. EXECUTE
    puts "  3/4 EXECUTE: Running tests..."
    test_result = run_tests_for_file(file_path)

    unless test_result[:passed]
      puts "  Tests failed: #{test_result[:failures].count} failures"

      if attempt >= max_attempts
        return { success: false, reason: "Tests failed" }
      end

      # Analyze failures and retry
      analyze_and_fix_tests(file_path, test_result[:failures])
      next
    end

    # 4. VERIFY
    puts "  4/4 VERIFY: Final check..."
    final_check = final_verification(file_path)

    return { success: true, attempts: attempt, verification: final_check }
  end
end

def apply_guardian_fixes(file_path, errors)
  # Group errors by type
  undefined_methods = errors.select { |e| e[:message].include?("Undefined method") }
  type_errors = errors.select { |e| e[:source] == "sorbet" }
  syntax_errors = errors.select { |e| e[:message].include?("syntax") }

  # Apply targeted fixes
  if undefined_methods.any?
    # Find correct method names using find_references
    fix_undefined_methods(file_path, undefined_methods)
  end

  if type_errors.any?
    # Add type signatures or fix type mismatches
    fix_type_errors(file_path, type_errors)
  end

  if syntax_errors.any?
    # Fix syntax issues
    fix_syntax_errors(file_path, syntax_errors)
  end
end
```

---

## 6. Sorbet Integration Patterns

### 6.1 Type Signature Extraction

Extract Sorbet type signatures from a file:

```ruby
# Pattern: Sorbet Signature Extraction
def extract_sorbet_signatures(file_path)
  content = Read(file_path)
  signatures = []

  # Find sig blocks
  content.scan(/sig\s*\{([^}]+)\}/) do |sig_content|
    sig = sig_content[0]

    # Parse params
    params = {}
    sig.scan(/params\(([^)]+)\)/) do |params_str|
      params_str[0].split(",").each do |param|
        name, type = param.strip.split(":").map(&:strip)
        params[name] = type
      end
    end

    # Parse returns
    returns = nil
    if sig =~ /returns\(([^)]+)\)/
      returns = $1.strip
    end

    signatures << { params: params, returns: returns }
  end

  signatures
end
```

### 6.2 Type-Guided Generation

Use type information to guide code generation:

```ruby
# Pattern: Type-Guided Generation
def generate_with_types(file_path, method_spec)
  # 1. Look up existing type signatures in project
  similar_methods = find_similar_methods(method_spec[:name])

  # 2. Infer expected types from callers
  references = mcp__cclsp__find_references(
    file_path: file_path,
    symbol_name: method_spec[:name]
  )

  inferred_types = infer_types_from_usage(references)

  # 3. Generate with explicit types
  signature = <<~RUBY
    sig { params(#{format_params(inferred_types[:params])}).returns(#{inferred_types[:returns]}) }
    def #{method_spec[:name]}(#{format_args(method_spec[:args])})
      # Implementation
    end
  RUBY

  signature
end
```

### 6.3 Sorbet Strictness Levels

Apply appropriate Sorbet strictness:

```ruby
# Pattern: Sorbet Strictness Selection
def select_sorbet_strictness(file_path)
  # New files: start with # typed: true
  # Critical business logic: use # typed: strict
  # Generated code: use # typed: false initially

  case file_path
  when /app\/services\//
    "# typed: strict"  # Services should have strong types
  when /app\/models\//
    "# typed: true"    # Models can start with basic types
  when /app\/controllers\//
    "# typed: false"   # Controllers often have complex types
  when /lib\//
    "# typed: strict"  # Library code should be well-typed
  else
    "# typed: true"    # Default to basic type checking
  end
end
```

---

## 7. Graceful Degradation

### 7.1 Tool Availability Check

Check which tools are available:

```bash
# Pattern: Availability Check
check_tool_availability() {
  local availability="{}"

  # Check cclsp
  if mcp__cclsp__get_diagnostics --file_path "Gemfile" 2>/dev/null; then
    availability=$(echo "$availability" | jq '.cclsp = true')
  else
    availability=$(echo "$availability" | jq '.cclsp = false')
  fi

  # Check Solargraph
  if gem list solargraph -i &>/dev/null; then
    availability=$(echo "$availability" | jq '.solargraph = true')
  else
    availability=$(echo "$availability" | jq '.solargraph = false')
  fi

  # Check Sorbet
  if bundle exec srb --version &>/dev/null || gem list sorbet -i &>/dev/null; then
    availability=$(echo "$availability" | jq '.sorbet = true')
  else
    availability=$(echo "$availability" | jq '.sorbet = false')
  fi

  # Check parser gem
  if gem list parser -i &>/dev/null; then
    availability=$(echo "$availability" | jq '.parser = true')
  else
    availability=$(echo "$availability" | jq '.parser = false')
  fi

  echo "$availability"
}
```

### 7.2 Fallback Strategies

Fallback when tools are unavailable:

```ruby
# Pattern: Graceful Degradation
def compile_context_with_fallback(task)
  availability = check_tool_availability

  context = {
    cclsp_enhanced: false,
    interfaces: [],
    vocabulary: [],
    fallback_used: []
  }

  # Primary: Use cclsp
  if availability[:cclsp]
    context[:cclsp_enhanced] = true
    context[:interfaces] = extract_interfaces_with_cclsp(task)
  else
    # Fallback: Use grep and AST parsing
    context[:fallback_used] << "grep for interface extraction"
    context[:interfaces] = extract_interfaces_with_grep(task)
  end

  # Primary: Use Sorbet for type info
  if availability[:sorbet]
    context[:type_info] = extract_type_info_with_sorbet(task)
  else
    # Fallback: Use YARD comments
    context[:fallback_used] << "YARD for type hints"
    context[:type_info] = extract_type_info_from_yard(task)
  end

  # Primary: Use parser gem
  if availability[:parser]
    context[:ast_analysis] = analyze_with_parser(task)
  else
    # Fallback: Use ripper (always available)
    context[:fallback_used] << "ripper for AST"
    context[:ast_analysis] = analyze_with_ripper(task)
  end

  context
end

def extract_interfaces_with_grep(task)
  interfaces = []

  task[:files].each do |file|
    # Use grep to find method definitions
    methods = `grep -n "def " #{file} | head -50`.lines

    methods.each do |line|
      if line =~ /^(\d+):\s*def\s+(\w+)/
        interfaces << {
          symbol: $2,
          kind: "method",
          file: file,
          line: $1.to_i
        }
      end
    end
  end

  interfaces
end
```

### 7.3 Partial Feature Mode

Enable features based on available tools:

```ruby
# Pattern: Feature Flags
def determine_enabled_features
  features = {
    lsp_diagnostics: false,
    type_checking: false,
    smart_refactoring: false,
    vocabulary_building: true,  # Always available
    interface_extraction: true  # Always available (grep fallback)
  }

  availability = check_tool_availability

  if availability[:cclsp]
    features[:lsp_diagnostics] = true
    features[:smart_refactoring] = true
  end

  if availability[:sorbet]
    features[:type_checking] = true
  end

  features
end
```

---

## 8. Working Memory Integration

### 8.1 Store Compiled Context

Store context for implementation phase:

```ruby
# Pattern: Store Compiled Context
def store_compiled_context(task_id, context)
  memory_entry = {
    timestamp: Time.now.utc.iso8601,
    agent: "context-compiler",
    knowledge_type: "compiled_context",
    key: "task.#{task_id}.context",
    value: context,
    confidence: "verified"
  }

  # Write to working memory file
  File.open(".claude/reactree-memory.jsonl", "a") do |f|
    f.puts(memory_entry.to_json)
  end
end
```

### 8.2 Read Compiled Context

Read context during implementation:

```ruby
# Pattern: Read Compiled Context
def read_compiled_context(task_id)
  memory_file = ".claude/reactree-memory.jsonl"
  return nil unless File.exist?(memory_file)

  # Read most recent context for task
  context = nil

  File.readlines(memory_file).reverse_each do |line|
    entry = JSON.parse(line)

    if entry["key"] == "task.#{task_id}.context"
      context = entry["value"]
      break
    end
  end

  context
end
```

---

## 9. Quick Reference

### Command Cheatsheet

```bash
# Solargraph
gem install solargraph
solargraph config                    # Generate .solargraph.yml
solargraph socket --port 7658        # Start language server

# Sorbet
gem install sorbet sorbet-runtime
bundle exec srb init                 # Initialize Sorbet
bundle exec srb tc                   # Type check project
bundle exec srb tc app/models/       # Type check directory
bundle exec srb tc --ignore=sorbet/  # Ignore directory

# Tapioca (RBI generation)
gem install tapioca
bundle exec tapioca init             # Initialize
bundle exec tapioca gems             # Generate gem RBIs
bundle exec tapioca dsl              # Generate DSL RBIs
bundle exec tapioca annotations      # Sync annotations

# parser gem
gem install parser
ruby -rparser/current -e 'p Parser::CurrentRuby.parse("def foo; end")'
```

### cclsp MCP Quick Reference

```ruby
# Find where a method is defined
mcp__cclsp__find_definition(
  file_path: "app/models/user.rb",
  symbol_name: "authenticate"
)

# Find all usages of a class
mcp__cclsp__find_references(
  file_path: "app/services/payment_service.rb",
  symbol_name: "PaymentService"
)

# Check file for errors
mcp__cclsp__get_diagnostics(
  file_path: "app/services/order_service.rb"
)

# Rename symbol (preview)
mcp__cclsp__rename_symbol(
  file_path: "app/models/user.rb",
  symbol_name: "old_method",
  new_name: "new_method",
  dry_run: true
)
```

### Guardian Validation Quick Reference

```ruby
# Full validation cycle
def validate_file(file_path)
  # 1. cclsp diagnostics
  diagnostics = mcp__cclsp__get_diagnostics(file_path: file_path)
  errors = diagnostics.select { |d| d[:severity] == 1 }

  # 2. Sorbet check
  sorbet_output = `bundle exec srb tc #{file_path} 2>&1`
  sorbet_errors = sorbet_output.lines.count { |l| l.start_with?(file_path) }

  # 3. Combined result
  {
    passed: errors.empty? && sorbet_errors == 0,
    lsp_errors: errors.count,
    sorbet_errors: sorbet_errors
  }
end
```

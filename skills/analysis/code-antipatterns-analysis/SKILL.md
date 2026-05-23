---
model: opus
name: code-antipatterns-analysis
description: Analyze codebases for anti-patterns, code smells, and quality issues using ast-grep structural pattern matching. Use when reviewing code quality, identifying technical debt, or performing comprehensive code analysis across JavaScript, TypeScript, Python, Vue, React, or other supported languages.
allowed-tools: Bash, Read, Grep, Glob, TodoWrite, Task
---

# Code Anti-patterns Analysis

Expert knowledge for systematic detection and analysis of anti-patterns, code smells, and quality issues across codebases using ast-grep and parallel agent delegation.

## Analysis Philosophy

This skill emphasizes **parallel delegation** for comprehensive analysis. Rather than sequentially scanning for issues, launch multiple specialized agents to examine different categories simultaneously, then consolidate findings.

## Analysis Categories

### 1. JavaScript/TypeScript Anti-patterns

**Callback Hell & Async Issues**
```bash
# Nested callbacks (3+ levels)
ast-grep -p '$FUNC($$$, function($$$) { $FUNC2($$$, function($$$) { $$$ }) })' --lang js

# Missing error handling in async
ast-grep -p 'async function $NAME($$$) { $$$ }' --lang js
# Then check if try-catch is present

# Unhandled promise rejection
ast-grep -p '$PROMISE.then($$$)' --lang js
# Without .catch() - use composite rule
```

**Magic Values**
```bash
# Magic numbers in comparisons
ast-grep -p 'if ($VAR > 100)' --lang js
ast-grep -p 'if ($VAR < 50)' --lang js
ast-grep -p 'if ($VAR === 42)' --lang js

# Magic strings
ast-grep -p "if ($VAR === 'admin')" --lang js
```

**Empty Catch Blocks**
```bash
ast-grep -p 'try { $$$ } catch ($E) { }' --lang js
```

**Console Statements (Debug Leftovers)**
```bash
ast-grep -p 'console.log($$$)' --lang js
ast-grep -p 'console.debug($$$)' --lang js
ast-grep -p 'console.warn($$$)' --lang js
```

**var Instead of let/const**
```bash
ast-grep -p 'var $VAR = $$$' --lang js
```

### 2. Vue 3 Anti-patterns

**Props Mutation**
```yaml
# YAML rule for props mutation detection
id: vue-props-mutation
language: JavaScript
message: Avoid mutating props directly
rule:
  pattern: props.$PROP = $VALUE
```

```bash
# Direct prop assignment
ast-grep -p 'props.$PROP = $VALUE' --lang js
```

**Missing Keys in v-for**
```bash
# Search in Vue templates
ast-grep -p 'v-for="$ITEM in $LIST"' --lang html
# Check if :key is present nearby
```

**Options API in Composition API Codebase**
```bash
# Find Options API usage
ast-grep -p 'export default { data() { $$$ } }' --lang js
ast-grep -p 'export default { methods: { $$$ } }' --lang js
ast-grep -p 'export default { computed: { $$$ } }' --lang js

# vs Composition API
ast-grep -p 'defineComponent({ setup($$$) { $$$ } })' --lang js
```

**Reactive State Issues**
```bash
# Destructuring reactive state (loses reactivity)
ast-grep -p 'const { $$$PROPS } = $REACTIVE' --lang js

# Should use toRefs
ast-grep -p 'const { $$$PROPS } = toRefs($REACTIVE)' --lang js
```

### 3. TypeScript Quality Issues

**Excessive `any` Usage**
```bash
ast-grep -p ': any' --lang ts
ast-grep -p 'as any' --lang ts
ast-grep -p '<any>' --lang ts
```

**Non-null Assertions**
```bash
ast-grep -p '$VAR!' --lang ts
ast-grep -p '$VAR!.$PROP' --lang ts
```

**Type Assertions Instead of Guards**
```bash
ast-grep -p '$VAR as $TYPE' --lang ts
```

**Missing Return Types**
```bash
# Functions without return type annotations
ast-grep -p 'function $NAME($$$) { $$$ }' --lang ts
# Check if return type is present
```

### 4. Async/Promise Patterns

**Unhandled Promises**
```bash
# Promise without await or .then/.catch
ast-grep -p '$ASYNC_FUNC($$$)' --lang js
# Context: check if result is used

# Floating promises (no await)
ast-grep -p '$PROMISE_RETURNING()' --lang ts
```

**Nested Callbacks (Pyramid of Doom)**
```bash
ast-grep -p '$F1($$$, function($$$) { $F2($$$, function($$$) { $F3($$$, function($$$) { $$$ }) }) })' --lang js
```

**Promise Constructor Anti-pattern**
```bash
# Wrapping already-async code in new Promise
ast-grep -p 'new Promise(($RESOLVE, $REJECT) => { $ASYNC_FUNC($$$).then($$$) })' --lang js
```

### 5. Code Complexity

**Long Functions (Manual Review)**
```bash
# Find function definitions, then count lines
ast-grep -p 'function $NAME($$$) { $$$ }' --lang js --json | jq '.[] | select(.range.end.line - .range.start.line > 50)'
```

**Deep Nesting**
```bash
# Nested if statements (4+ levels)
ast-grep -p 'if ($A) { if ($B) { if ($C) { if ($D) { $$$ } } } }' --lang js
```

**Large Parameter Lists**
```bash
ast-grep -p 'function $NAME($A, $B, $C, $D, $E, $$$)' --lang js
```

**Cyclomatic Complexity Indicators**
```bash
# Multiple conditionals in single function
ast-grep -p 'if ($$$) { $$$ } else if ($$$) { $$$ } else if ($$$) { $$$ }' --lang js
```

### 6. React/Pinia Store Patterns

**Direct State Mutation (Pinia)**
```bash
# Direct store state mutation outside actions
ast-grep -p '$STORE.$STATE = $VALUE' --lang js
```

**Missing Dependencies in useEffect**
```bash
ast-grep -p 'useEffect(() => { $$$ }, [])' --lang jsx
# Check if variables used inside are in dependency array
```

**Inline Functions in JSX**
```bash
ast-grep -p '<$COMPONENT onClick={() => $$$} />' --lang jsx
ast-grep -p '<$COMPONENT onChange={() => $$$} />' --lang jsx
```

### 7. Memory & Performance

**Event Listeners Without Cleanup**
```bash
ast-grep -p 'addEventListener($EVENT, $HANDLER)' --lang js
# Check for corresponding removeEventListener
```

**setInterval Without Cleanup**
```bash
ast-grep -p 'setInterval($$$)' --lang js
# Check for clearInterval
```

**Large Arrays in Computed/Memos**
```bash
ast-grep -p 'computed(() => $ARRAY.filter($$$))' --lang js
ast-grep -p 'useMemo(() => $ARRAY.filter($$$), [$$$])' --lang jsx
```

### 8. Security Concerns

**eval Usage**
```bash
ast-grep -p 'eval($$$)' --lang js
ast-grep -p 'new Function($$$)' --lang js
```

**innerHTML Assignment (XSS Risk)**
```bash
ast-grep -p '$ELEM.innerHTML = $$$' --lang js
ast-grep -p 'dangerouslySetInnerHTML={{ __html: $$$ }}' --lang jsx
```

**Hardcoded Secrets**
```bash
ast-grep -p "apiKey: '$$$'" --lang js
ast-grep -p "password = '$$$'" --lang js
ast-grep -p "secret: '$$$'" --lang js
```

**SQL String Concatenation**
```bash
ast-grep -p '"SELECT * FROM " + $VAR' --lang js
ast-grep -p '`SELECT * FROM ${$VAR}`' --lang js
```

### 9. Python Anti-patterns

**Bare Except**
```bash
ast-grep -p 'except: $$$' --lang py
```

**Mutable Default Arguments**
```bash
ast-grep -p 'def $FUNC($ARG=[])' --lang py
ast-grep -p 'def $FUNC($ARG={})' --lang py
```

**Global Variable Usage**
```bash
ast-grep -p 'global $VAR' --lang py
```

**Type: ignore Without Reason**
```bash
# Search in comments via grep
grep -r "# type: ignore$" --include="*.py"
```

## Parallel Analysis Strategy

When analyzing a codebase, launch multiple agents in parallel to maximize efficiency:

### Agent Delegation Pattern

```markdown
1. **Language Detection Agent** (Explore)
   - Detect project languages and frameworks
   - Identify relevant file patterns

2. **JavaScript/TypeScript Agent** (code-analysis or Explore)
   - JS anti-patterns
   - TypeScript quality issues
   - Async/Promise patterns

3. **Framework-Specific Agent** (code-analysis or Explore)
   - Vue 3 anti-patterns (if Vue detected)
   - React anti-patterns (if React detected)
   - Pinia/Redux patterns (if detected)

4. **Security Agent** (security-audit)
   - Security concerns
   - Hardcoded values
   - Injection risks

5. **Complexity Agent** (code-analysis or Explore)
   - Code complexity metrics
   - Long functions
   - Deep nesting

6. **Python Agent** (if Python detected)
   - Python anti-patterns
   - Type annotation issues
```

### Consolidation

After parallel analysis completes:
1. Aggregate findings by severity (critical, high, medium, low)
2. Group by category (security, performance, maintainability)
3. Provide actionable remediation suggestions
4. Prioritize fixes based on impact

## YAML Rule Examples

### Complete Anti-pattern Rule

```yaml
id: no-empty-catch
language: JavaScript
severity: warning
message: Empty catch block suppresses errors silently
note: |
  Empty catch blocks hide errors and make debugging difficult.
  Either log the error, handle it specifically, or re-throw.

rule:
  pattern: try { $$$ } catch ($E) { }

fix: |
  try { $$$ } catch ($E) {
    console.error('Error:', $E);
    throw $E;
  }

files:
  - 'src/**/*.js'
  - 'src/**/*.ts'
ignores:
  - '**/*.test.js'
  - '**/node_modules/**'
```

### Vue Props Mutation Rule

```yaml
id: no-props-mutation
language: JavaScript
severity: error
message: Never mutate props directly - use emit or local copy

rule:
  all:
    - pattern: props.$PROP = $VALUE
    - inside:
        kind: function_declaration

note: |
  Props should be treated as immutable. To modify data:
  1. Emit an event to parent: emit('update:propName', newValue)
  2. Create a local ref: const local = ref(props.propName)
```

## Integration with Commands

This skill is designed to work with the `/code:antipatterns` command, which:
1. Detects project language stack
2. Launches parallel specialized agents
3. Consolidates findings into prioritized report
4. Suggests automated fixes where possible

## Best Practices for Analysis

1. **Start with language detection** - Run appropriate patterns for detected languages
2. **Use parallel agents** - Don't sequentially analyze; delegate to specialized agents
3. **Prioritize by severity** - Security issues first, then correctness, then style
4. **Provide fixes** - Don't just identify problems; suggest solutions
5. **Consider context** - Some "anti-patterns" are acceptable in specific contexts
6. **Check test files separately** - Different standards may apply to test code

## Severity Levels

| Severity | Description | Examples |
|----------|-------------|----------|
| **Critical** | Security vulnerabilities, data loss risk | eval(), SQL injection, hardcoded secrets |
| **High** | Bugs, incorrect behavior | Props mutation, unhandled promises, empty catch |
| **Medium** | Maintainability issues | Magic numbers, deep nesting, large functions |
| **Low** | Style/preference | var usage, console.log, inline functions |

## Resources

- **ast-grep Documentation**: https://ast-grep.github.io/
- **ast-grep Playground**: https://ast-grep.github.io/playground.html
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **Clean Code Principles**: https://clean-code-developer.com/

---
name: bun-shell-commands
description: Writing shell commands for OpenCode custom commands using Bun Shell
---

# Bun Shell Commands

This skill covers how to write effective shell commands in OpenCode custom commands using Bun Shell (Bun's bash-like shell implementation).

## Context

OpenCode uses **Bun Shell** for executing shell commands in custom commands via the !`command` syntax. Bun Shell is a bash-like shell written in Zig that provides cross-platform shell scripting, but it has some differences from traditional bash.

## Supported Features

### ✅ Arguments

Positional arguments work correctly:

```markdown
!`echo "Arg1: $1" && echo "Arg2: $2" && echo "Arg3: $3"`
```

Usage: `/mycommand 5 "hello world" "a,b,c"`

### ✅ Command Substitution

Use `$(command)` for command substitution:

```markdown
!`echo "Sum: $(seq $1 | awk '{s+=$1} END {print s}')"`
```

### ✅ Pipes

Pipe commands using `|`:

```markdown
!`echo "$2" | tr '[:lower:]' '[:upper:]' | rev`
```

### ✅ Environment Variables

Set environment variables and use them:

```markdown
!`TEST_VAR="$1" && echo "TEST_VAR=$TEST_VAR"`
```

Store command substitution results in variables:

```markdown
!`REV=$(echo "$2" | rev) && echo "Reversed: $REV"`
```

### ✅ Command Chaining

Use `&&` to chain commands (instead of newlines or `;`):

```markdown
!`echo "First" && echo "Second" && echo "Third"`
```

### ✅ Available Commands

Bun Shell includes these built-in commands:
- `cd`, `ls`, `rm`, `echo`, `pwd`, `cat`, `touch`, `mkdir`, `which`, `mv`
- `seq`, `dirname`, `basename`, `true`, `false`, `yes`

Common external commands also work:
- `awk`, `sed`, `tr`, `wc`, `grep`, `head`, `tail`
- `find`, `xargs`, `sort`, `uniq`

## Unsupported Features

### ❌ Shell Control Structures

Do NOT use `for`, `while`, `do`, `done`:

```markdown
# ❌ DOESN'T WORK
!`for i in $(seq 1 $1); do echo $i; done`
```

### ❌ Arithmetic Expansion

Do NOT use `$(( ))` directly in the template:

```markdown
# ❌ DOESN'T WORK
!`echo "Squared: $(($1 * $1))"`
```

Use `$(awk '{...}')` instead:

```markdown
# ✅ WORKS
!`echo "$1" | awk '{print $1 * $1}'`
```

### ❌ Native Brace Expansion

Native brace expansion is not supported:

```markdown
# ❌ DOESN'T WORK
!`echo {1,2,3}`
```

Use pipes to simulate expansion:

```markdown
# ✅ WORKS
!`echo "$3" | tr ',' '\n' | awk '{print "Expanded:", $1}'`
```

## Patterns and Best Practices

### Loops via Pipes

Instead of `for` loops, use `seq` with `awk`:

```markdown
# Generate numbers 1 to N with squares
!`seq $1 | awk '{print $1, "-> squared:", $1*$1}'`
```

### Multi-step Operations

Use environment variables to store intermediate results:

```markdown
# Reverse text, count chars, and show both
!`REV=$(echo "$2" | rev) && COUNT=$(echo "$2" | wc -c) && echo "Reversed: $REV (${COUNT} chars)"`
```

### Conditional Logic

Use `awk` for conditionals:

```markdown
# Classify numbers as even/odd
!`seq $1 | awk '{if ($1 % 2 == 0) print $1 ": even"; else print $1 ": odd"}'`
```

### Text Processing

Combine `tr`, `sed`, `awk` for text manipulation:

```markdown
# Uppercase, reverse, and format
!`echo "$2" | tr '[:lower:]' '[:upper:]' | rev | sed 's/^/> /'`
```

### Working with Multiple Arguments

Use separate shell blocks for independent tests:

```markdown
## Test 1: Arithmetic with $1
!`seq $1 | awk '{s+=$1} END {print "Sum:", s}'`

## Test 2: Text processing with $2
!`echo "$2" | tr '[:lower:]' '[:upper:]' | rev`

## Test 3: Pattern with $3
!`echo "$3" | tr ',' '\n' | wc -l`
```

## Example: Complete Command

```markdown
---
description: Test Bun Shell capabilities
---

Test Bun Shell with multiple features:

## Argument passing
!`echo "Arg1: [$1]" && echo "Arg2: [$2]" && echo "Arg3: [$3]"`

## Command substitution
!`echo "Sum of 1 to $1: $(seq $1 | awk '{s+=$1} END {print s}')"`

## Text processing
!`echo "$2" | tr '[:lower:]' '[:upper:]' | rev | wc -c`

## Environment variables
!`REV=$(echo "$2" | rev) && echo "Reversed via var: $REV"`
```

Usage: `/mycommand 5 "hello world" "a,b,c"`

## Debugging

If a shell command fails silently:

1. Simplify to just `echo "$1"` to verify argument passing
2. Test each pipe segment separately
3. Replace complex `awk` with simpler `tr` or `sed`
4. Use `echo` at each step to verify intermediate values

## References

- [Bun Shell Documentation](https://bun.com/docs/runtime/shell.md)
- [OpenCode Commands Documentation](https://opencode.ai/docs/commands/)

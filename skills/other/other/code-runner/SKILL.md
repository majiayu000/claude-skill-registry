---
name: code-runner
description: Run code snippets in 30+ programming languages including JavaScript, Python, TypeScript, Java, C, C++, Go, Rust, Ruby, PHP, and more. Use when the user wants to execute code, test algorithms, verify output, run scripts, or check code behavior. Supports both interpreted and compiled languages.
---

# Code Runner Skill

This skill enables you to run code snippets in multiple programming languages directly from the command line.

## When to Use This Skill

Use this skill when:
- The user wants to run or execute a code snippet
- Testing algorithm implementations or logic
- Verifying expected output of code
- Running quick scripts or one-liners
- Checking syntax or runtime behavior
- Demonstrating code functionality

## Supported Languages

The following languages are supported (requires the interpreter/compiler to be installed):

| Language | Command | File Extension |
|----------|---------|----------------|
| JavaScript | `node` | `.js` |
| TypeScript | `ts-node` | `.ts` |
| Python | `python` | `.py` |
| Java | `java` (compile & run) | `.java` |
| C | `gcc` (compile & run) | `.c` |
| C++ | `g++` (compile & run) | `.cpp` |
| Go | `go run` | `.go` |
| Rust | `rustc` (compile & run) | `.rs` |
| Ruby | `ruby` | `.rb` |
| PHP | `php` | `.php` |
| Perl | `perl` | `.pl` |
| Lua | `lua` | `.lua` |
| R | `Rscript` | `.r` |
| Swift | `swift` | `.swift` |
| Kotlin | `kotlin` | `.kts` |
| Scala | `scala` | `.scala` |
| Groovy | `groovy` | `.groovy` |
| Dart | `dart` | `.dart` |
| Julia | `julia` | `.jl` |
| Haskell | `runhaskell` | `.hs` |
| Clojure | `clojure` | `.clj` |
| F# | `dotnet fsi` | `.fsx` |
| C# | `dotnet script` | `.csx` |
| PowerShell | `pwsh` | `.ps1` |
| Bash | `bash` | `.sh` |
| Batch | `cmd /c` | `.bat` |
| CoffeeScript | `coffee` | `.coffee` |
| Crystal | `crystal` | `.cr` |
| Elixir | `elixir` | `.exs` |
| Nim | `nim compile --run` | `.nim` |
| OCaml | `ocaml` | `.ml` |
| Racket | `racket` | `.rkt` |
| Scheme | `scheme` | `.scm` |
| Lisp | `sbcl --script` | `.lisp` |

See [references/LANGUAGES.md](references/LANGUAGES.md) for detailed language configuration.

## How to Run Code

### Step 1: Identify the Language

Determine the programming language from:
- User's explicit request (e.g., "run this Python code")
- File extension if provided
- Code syntax patterns

### Step 2: Execute Using the Runner Script

**⚠️ Important for AI Agents**: Use stdin to avoid escaping issues with quotes, backslashes, and special characters.

**Recommended Method (stdin):**
```bash
echo "<code>" | node scripts/run-code.cjs <languageId>
```

**Alternative Method (CLI argument - for simple code only):**
```bash
node scripts/run-code.cjs <languageId> "<code>"
```

**Example - JavaScript:**
```bash
echo "console.log('Hello, World!')" | node scripts/run-code.cjs javascript
```

**Example - Python:**
```bash
echo "print('Hello, World!')" | node scripts/run-code.cjs python
```

**Example - Java (multi-line):**
```bash
echo "public class Test {
    public static void main(String[] args) {
        System.out.println(\"Hello from Java!\");
    }
}" | node scripts/run-code.cjs java
```

**Example - Multi-line code from variable:**
```bash
# In bash
CODE='import math
print("Pi:", math.pi)
print("Result:", math.factorial(5))'
echo "$CODE" | node scripts/run-code.cjs python

# In PowerShell (inline here-string)
@"
import math
print("Pi:", math.pi)
print("Result:", math.factorial(5))
"@ | node scripts/run-code.cjs python
```

### Step 3: Return Results

- Show the output (stdout) to the user
- If there are errors (stderr), explain what went wrong
- Suggest fixes for common errors

## Platform Notes

### Windows
- Use `cmd /c` for batch scripts
- PowerShell scripts require `pwsh` or `powershell`
- Path separators use backslash `\`

### macOS / Linux
- Bash scripts work natively
- Swift available on macOS
- Use `#!/usr/bin/env` shebang for portable scripts

## Error Handling

Common issues and solutions:

1. **Command not found**: The language interpreter is not installed or not in PATH
   - Suggest installing the required runtime
   - Provide installation instructions

2. **Syntax errors**: Code has syntax issues
   - Show the error message
   - Point to the line number if available

3. **Runtime errors**: Code runs but fails during execution
   - Display the stack trace
   - Explain the error type

4. **Timeout**: Code takes too long (default: 30 seconds)
   - Warn about infinite loops
   - Suggest optimizations

## Security Considerations

⚠️ **Important**: Running arbitrary code can be dangerous. Always:

1. Review the code before execution
2. Be cautious with code that:
   - Accesses the file system
   - Makes network requests
   - Executes system commands
   - Modifies environment variables
3. Consider running in a sandboxed environment for untrusted code

## Examples

### Example 1: Run a JavaScript calculation
```bash
echo "console.log(Array.from({length: 10}, (_, i) => i * i))" | node scripts/run-code.cjs javascript
```
Output: `[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]`

### Example 2: Run Python with imports
```bash
echo "import math; print(math.factorial(10))" | node scripts/run-code.cjs python
```
Output: `3628800`

### Example 3: Test a Go function
```bash
echo 'package main; import "fmt"; func main() { fmt.Println("Hello from Go!") }' | node scripts/run-code.cjs go
```
Output: `Hello from Go!`

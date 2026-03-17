---
name: julia-evaluation
description: This skill should be used when the user asks to "run Julia code", "evaluate Julia", "use Julia", mentions "persistent Julia session", "TTFX", or wants to work with Julia for data analysis, scientific computing, or package development. Provides best practices for using the Julia REPL MCP tools effectively.
version: 0.5.0
---

# Julia Development Best Practices

This skill provides guidance for using the persistent Julia REPL via MCP tools. AgentREPL maintains a worker subprocess for code evaluation, eliminating the "Time to First X" (TTFX) startup penalty that normally occurs with each Julia invocation.

## Architecture

AgentREPL uses a **distributed worker model** (recommended):

### Distributed Mode (Default, Recommended)
- The MCP server runs in the main process (STDIO transport)
- Code evaluation happens in a spawned worker process (via Distributed.jl)
- `reset` kills the worker and spawns a fresh one (true hard reset)
- Use `log_viewer` tool to open a terminal showing output in real-time

### Visual Output with Log Viewer

To see Julia output as it happens:
```
log_viewer(mode="auto")   # Opens a terminal with live output
```

Or set `JULIA_REPL_VIEWER=auto` environment variable before starting.

### Note on Tmux Mode

Tmux mode is deprecated due to unfixable marker pollution issues. Use distributed mode (default) with `log_viewer` for visual output.

## Available Tools

| Tool | Purpose |
|------|---------|
| `eval` | Evaluate Julia code with persistent state |
| `reset` | **Hard reset** - kills worker, spawns fresh one (enables type redefinition) |
| `info` | Get session info (version, project, variables, worker ID) |
| `pkg` | Manage packages (add, rm, status, update, instantiate, resolve, test, develop, free) |
| `activate` | Switch active project/environment |
| `log_viewer` | Open a terminal window showing Julia output in real-time |
| `mode` | (Deprecated) Switch between distributed and tmux modes |

## Critical: Beautiful Code and Output Display

**The goal is to make Julia work feel like an interactive REPL session.**

### Before Evaluation: Show the Code

Always display code in a readable format **before** calling `eval`. The MCP permission prompt shows code as an escaped string which is difficult to read.

```
Running this Julia code:
```julia
A = [1 2 3; 4 5 6; 7 8 9]
det(A)
```

[then call eval]
```

### After Evaluation: Format Results Beautifully

Present results in REPL-style with proper formatting:

```julia
julia> A = [1 2 3; 4 5 6; 7 8 9]
3×3 Matrix{Int64}:
 1  2  3
 4  5  6
 7  8  9

julia> det(A)
0.0
```

This workflow gives users the best of both worlds: they can verify code before it runs, and see results in a beautiful, readable format afterward.

## Understanding TTFX (Time to First X)

The first call to `eval` in a session may take several seconds due to:
- Julia's JIT compilation
- Package loading and precompilation

Subsequent calls are fast because the worker process stays alive with compiled code in memory. This is the core value proposition of AgentREPL.

## Session Persistence

Variables, functions, and loaded packages persist across `eval` calls:

```julia
# First call
x = 42
f(n) = n^2
```

```julia
# Later call - x and f still exist
f(x)  # Returns 1764
```

## Hard Reset with `reset`

The `reset` tool **kills the worker process and spawns a fresh one**. This means:

- All variables are cleared
- All loaded packages are unloaded
- **Type definitions can be changed** (impossible with soft reset)
- The worker starts completely fresh

Use `reset` when:
- You need to redefine a struct or type
- Something is in a bad state
- You want a completely clean slate

After reset, packages need to be reloaded with `using`.

The activated environment persists across resets.

## Environment Management

Julia best practice is to use project-specific environments. Use `activate` to switch environments:

```
activate(path=".")              # Current directory
activate(path="/path/to/proj")  # Specific project
activate(path="@v1.10")         # Named shared environment
```

After activation, install dependencies:
```
pkg(action="instantiate")
```

The activated environment persists even across `reset` calls.

## Package Management

Use `pkg` for all package operations:

**Adding packages:**
```
pkg(action="add", packages="JSON, DataFrames, CSV")
```

**Checking installed packages:**
```
pkg(action="status")
```

**Installing from Project.toml:**
```
pkg(action="instantiate")
```

**Running tests:**
```
pkg(action="test")                    # Test current project
pkg(action="test", packages="MyPkg")  # Test specific package
```

**Development workflow (local packages):**
```
pkg(action="develop", packages="./path/to/MyLocalPackage")  # Use local code
pkg(action="free", packages="MyPackage")                     # Return to registry
```

After adding a package, load it:
```julia
using JSON
```

## Testing Workflow

For running tests, use `pkg(action="test")`:
- With no packages specified, tests the current project
- With packages specified, tests those specific packages
- Test output is captured and displayed

This is preferred over running tests via `eval` because it properly isolates the test environment.

## Development Workflow (Pkg.develop)

When developing a local package alongside your project:

1. **Put the package in develop mode:**
   ```
   pkg(action="develop", packages="./MyLocalPackage")
   ```

2. **Make changes to the package source code**

3. **Test your changes:**
   ```
   pkg(action="test", packages="MyLocalPackage")
   ```

4. **When done, return to registry version:**
   ```
   pkg(action="free", packages="MyLocalPackage")
   ```

The `develop` action accepts:
- Relative paths starting with `./` or `../`
- Absolute paths starting with `/`
- Home-relative paths starting with `~`
- Package names (for developing registered packages from source)

## Error Handling

Common issues and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `UndefVarError` | Variable not defined | Re-run earlier code or check spelling |
| `MethodError` | Wrong argument types | Check function signatures |
| `LoadError` | Package not installed | Use `pkg(action="add", packages="...")` |
| `cannot redefine` | Type redefinition | Use `reset` for a fresh worker |
| `StackOverflowError` | Infinite recursion | Fix recursion, may need `reset` |

## First-Time Setup

**When first using Julia in a session**, ask the user about their environment preference before running code:

> "Before we start, which Julia environment should I use?
> 1. **Current directory** - activate Project.toml in this folder (if it exists)
> 2. **Specific project** - provide a path to a Julia project
> 3. **Default** - use the global environment
>
> This determines where packages are installed and what dependencies are available."

Based on their answer:
- Option 1: `activate(path=".")` then `pkg(action="instantiate")`
- Option 2: `activate(path="/their/path")` then `pkg(action="instantiate")`
- Option 3: Proceed without activation (uses default environment)

## Practical Workflow

For a typical Julia task:

1. **First use**: Ask about environment (see above)
2. **Activate and install**: `activate` + `pkg(action="instantiate")`
3. **Show code to user**, then call `eval`
4. **Build incrementally** - variables persist across calls
5. **Run tests**: `pkg(action="test")` to verify changes
6. **Use `reset`** if types need redefining or state is corrupted

## Multi-line Code

Multi-line code blocks work naturally:

```julia
function fibonacci(n)
    if n <= 1
        return n
    end
    return fibonacci(n-1) + fibonacci(n-2)
end

[fibonacci(i) for i in 1:10]
```

## Formatting Results Beautifully

**CRITICAL: Always format Julia results in a readable REPL-style code block.**

After calling `eval`, present the results to the user in a nicely formatted way that mimics the Julia REPL experience. This is especially important for:
- Matrices and arrays (show the full formatted output)
- DataFrames and tables
- Custom types with pretty-printing
- Multi-line output

**Example - Good formatting:**

```julia
julia> A = [1 3 4; 4 5 6; 2 0 3]
3×3 Matrix{Int64}:
 1  3  4
 4  5  6
 2  0  3

julia> inv(A)
3×3 Matrix{Float64}:
 -0.6   0.36   0.08
  0.0   0.2   -0.4
  0.4  -0.24   0.28
```

**Example - Bad formatting (don't do this):**

> The result is `[1 3 4; 4 5 6; 2 0 3]` and the inverse is `[-0.6 0.36 0.08; 0.0 0.2 -0.4; 0.4 -0.24 0.28]`

The REPL-style formatting:
- Shows the `julia>` prompt with the command
- Preserves matrix/array alignment and spacing
- Makes numerical results easy to read and verify
- Feels like an interactive Julia session

## Output Capture

Both return values and printed output are captured from the `eval` tool. Format them beautifully as shown above.

## When NOT to Use These Tools

Prefer direct bash commands when:
- Running a standalone Julia script: `julia script.jl`
- Running with specific command-line flags
- The task is one-shot and doesn't benefit from persistence

Use the MCP tools when:
- Interactive development and exploration
- Iterative work where state should persist
- Avoiding TTFX overhead matters
- Package development workflow

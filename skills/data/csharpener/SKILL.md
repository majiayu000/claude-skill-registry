---
name: CSharpener
description: C# static analysis tool for call graphs, unused code detection, impact analysis, HTML documentation generation, and Graphviz diagram export
---

# CSharpener - C# Code Analysis

CSharpener is a Roslyn-based static analysis tool that analyzes C# codebases to build call graphs, identify unused code, and help with refactoring decisions.

## Quick Start for Claude

**ALWAYS use this exact command format when invoking CSharpener:**

```bash
"Y:/CSharpDLLs/CSharpener/CSharpener.exe" <command> --solution "<path-to-solution>" --format console
```

**Key Requirements:**
- Use forward slashes for the executable path: `Y:/CSharpDLLs/CSharpener/CSharpener.exe`
- Use double quotes around paths
- Use backslashes for Windows paths in --solution parameter
- Don't search for the executable - use the path above directly

**Common Commands:**
- `analyze --solution <path> --format console --include-call-graph` - Full analysis with call graph
- `unused --solution <path> --format console` - Find unused methods
- `callers --solution <path> --method <name> --format console` - Find who calls a method
- `dependencies --solution <path> --method <name> --format console` - Find method dependencies
- `impact --solution <path> --method <name> --format console` - Analyze removal impact

## Executable Location

**Primary:** `Y:\CSharpDLLs\CSharpener\CSharpener.exe` (use `Y:/` with forward slashes in bash)

**Fallback:** If the Y: drive is not available, the source code can be built from:
- GitHub: https://github.com/lawless-m/CSharpener
- Build: `dotnet build -c Release`
- Output: `CSharpCallGraphAnalyzer\bin\Release\net9.0\win-x64\csharp-analyzer.exe`

## Available Commands

### 1. analyze - Full Analysis
Performs comprehensive analysis including call graph, unused methods, and statistics.

```bash
Y:\CSharpDLLs\CSharpener\CSharpener.exe analyze --solution <path> --format console
```

**Options:**
- `--solution, -s` (required): Path to .sln or .csproj file
- `--format, -f`: Output format (json, console, dot, graphviz, html) [default: json]
- `--output, -o`: Output file path (stdout if not specified)
- `--include-call-graph`: Include full call graph in output [default: true]
- `--exclude-namespace`: Namespaces to exclude from analysis

### 2. unused - Find Unused Methods
Quickly scans for potentially unused methods with confidence levels.

```bash
Y:\CSharpDLLs\CSharpener\CSharpener.exe unused --solution <path> --format console
```

**Options:**
- `--solution, -s` (required): Path to .sln or .csproj file
- `--format, -f`: Output format (json, console, dot, graphviz) [default: json]
- `--output, -o`: Output file path
- `--exclude-namespace`: Namespaces to exclude

**Confidence Levels:**
- **High**: Private methods never called (safe to remove)
- **Medium**: Internal methods not called within assembly
- **Low**: Public methods (might be external API, use with caution)

### 3. callers - Find Who Calls a Method
Finds all methods that call a specific method.

```bash
Y:\CSharpDLLs\CSharpener\CSharpener.exe callers --solution <path> --method <method-name> --format console
```

**Options:**
- `--solution, -s` (required): Path to .sln or .csproj file
- `--method, -m` (required): Fully qualified or partial method name to search for
- `--format, -f`: Output format [default: json]

**Example:**
```bash
Y:\CSharpDLLs\CSharpener\CSharpener.exe callers -s MySolution.sln -m "BuildCallGraphAsync" -f console
```

### 4. dependencies - Find Method Dependencies
Finds all methods that a specific method calls (its dependencies).

```bash
Y:\CSharpDLLs\CSharpener\CSharpener.exe dependencies --solution <path> --method <method-name> --format console
```

**Options:**
- `--solution, -s` (required): Path to .sln or .csproj file
- `--method, -m` (required): Method name to analyze
- `--format, -f`: Output format [default: json]

### 5. impact - Analyze Removal Impact
Analyzes what would break if you removed a method (safety check before deletion).

```bash
Y:\CSharpDLLs\CSharpener\CSharpener.exe impact --solution <path> --method <method-name> --format console
```

**Options:**
- `--solution, -s` (required): Path to .sln or .csproj file
- `--method, -m` (required): Method to analyze
- `--format, -f`: Output format [default: json]

Shows:
- Direct callers (methods that immediately call this method)
- Transitive callers (methods that indirectly depend on it)
- Entry points affected (would break Main methods or public APIs)

### 6. document - Generate Documentation
Generates HTML documentation with cross-referenced code, call graphs, and navigation.

```bash
Y:\CSharpDLLs\CSharpener\CSharpener.exe document --solution <path> --output docs/analysis.html
```

**Options:**
- `--solution, -s` (required): Path to .sln or .csproj file
- `--output, -o` (required): Output HTML file path
- `--include-unused`: Include unused methods in documentation
- `--include-tests`: Include test projects

## Usage Examples for Claude

### Example 1: Find Unused Methods
**User Request:** "Find unused methods in my solution"

**Claude Action:**
```bash
Y:\CSharpDLLs\CSharpener\CSharpener.exe unused --solution "C:\path\to\solution.sln" --format console
```

**Interpretation:**
- High confidence = Safe to delete
- Medium confidence = Review carefully
- Low confidence = Might be public API, investigate before removing

### Example 2: Analyze Impact Before Deletion
**User Request:** "What would break if I deleted the ProcessData method?"

**Claude Action:**
```bash
Y:\CSharpDLLs\CSharpener\CSharpener.exe impact --solution "C:\path\to\solution.sln" --method "ProcessData" --format console
```

**Interpretation:**
- 0 direct callers = Safe to delete
- Entry points affected > 0 = Breaking change, requires API updates
- Many transitive callers = Ripple effect, consider refactoring instead

### Example 3: Find Who Uses a Method
**User Request:** "Who calls the BuildAsync method?"

**Claude Action:**
```bash
Y:\CSharpDLLs\CSharpener\CSharpener.exe callers --solution "C:\path\to\solution.sln" --method "BuildAsync" --format console
```

### Example 4: Generate Documentation
**User Request:** "Generate HTML documentation for my project"

**Claude Action:**
```bash
Y:\CSharpDLLs\CSharpener\CSharpener.exe document --solution "C:\path\to\solution.sln" --output docs/csharpener-analysis.html
```

Then open the generated HTML file in a browser.

### Example 5: Full Analysis
**User Request:** "Analyze my solution and show me statistics"

**Claude Action:**
```bash
Y:\CSharpDLLs\CSharpener\CSharpener.exe analyze --solution "C:\path\to\solution.sln" --format console
```

## Performance Tips

1. **First Run Creates Cache**: Initial analysis is slow, subsequent runs are faster
2. **Exclude Test Projects**: Use `--exclude-namespace "*.Tests,*.Test"` for large solutions
3. **Cache Location**: `.csharpener-cache/` in solution directory (can be deleted to force refresh)
4. **Large Solutions**: Analyze individual projects instead of full solution for faster results

## Common Patterns

### Refactoring Workflow
1. Find unused methods: `unused --solution MySolution.sln`
2. For each suspicious method, check impact: `impact --method MethodName`
3. If safe (0 callers), delete the method
4. Repeat until clean

### Understanding Code Flow
1. Start with entry points: `callers --method Main`
2. Explore dependencies: `dependencies --method ProcessRequest`
3. Generate visualization: `analyze --format dot` (use Graphviz to render)

### Code Review
1. Generate documentation: `document --output review.html`
2. Share HTML file with team
3. Review unused methods list together
4. Make cleanup decisions

## Troubleshooting

### "Solution file not found"
- Use absolute paths, not relative
- Ensure .sln or .csproj file exists
- Check for typos in path

### "No methods found"
- Solution might not be building
- Try `dotnet build` first to ensure it compiles
- Check that it's a C# project (not F#, VB.NET, etc.)

### Analysis Taking Too Long
- Exclude test projects with `--exclude-namespace`
- Analyze smaller projects first
- Check for large auto-generated code files

### "Method not found" in callers/dependencies
- Use partial names (e.g., "BuildAsync" instead of full qualified name)
- Method name is case-insensitive
- Try shortening the method name

## Output Formats

- **console**: Human-readable output for terminal
- **json**: Machine-readable for scripting/automation
- **html**: Interactive documentation (document command only)
- **dot**: Graphviz format for visualization
- **graphviz**: Same as dot

## Integration with CI/CD

```yaml
# Example GitHub Actions workflow
- name: Analyze for unused code
  run: |
    Y:\CSharpDLLs\CSharpener\CSharpener.exe unused \
      --solution MySolution.sln \
      --format json \
      --output unused-methods.json

- name: Upload results
  uses: actions/upload-artifact@v3
  with:
    name: code-analysis
    path: unused-methods.json
```

## Notes

- CSharpener uses Roslyn for analysis (same as Visual Studio)
- Detects reflection usage and warns about false positives
- Recognizes DI patterns (AddTransient, AddScoped, etc.)
- Thread-safe and can be run in parallel on different solutions
- Cache is solution-specific and invalidates on file changes

## Support

- GitHub: https://github.com/lawless-m/CSharpener
- Issues: https://github.com/lawless-m/CSharpener/issues

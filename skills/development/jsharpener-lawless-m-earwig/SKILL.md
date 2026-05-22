---
name: JSharpener
description: JavaScript/TypeScript static analysis tool for call graphs, unused code detection (tree shaking), dependency analysis, and circular dependency detection
---

# JSharpener - JavaScript/TypeScript Code Analysis

JSharpener is a TypeScript Compiler API-based static analysis tool that analyzes JavaScript and TypeScript codebases to build call graphs, identify unused code, detect circular dependencies, and help with refactoring decisions.

## Executable Location

`C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js`

Run with: `node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" <command>`

**Note:** If the executable is not available, rebuild from source:
```bash
cd C:\Users\matthew.heath\Git\JSharpener
npm install
npm run build
```

## Available Commands

### 1. analyze - Project Analysis
Performs comprehensive analysis including file count, function count, class count, and import/export statistics.

```bash
node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" analyze [path]
```

**Options:**
- `path`: Directory or file to analyze (default: current directory)
- `-o, --output <file>`: Save results to JSON file
- `--include <pattern...>`: File patterns to include (e.g., "src/**/*.ts")
- `--exclude <pattern...>`: File patterns to exclude (e.g., "**/*.test.ts")
- `--config <file>`: Path to config file (jsharpener.json)

**Example:**
```bash
node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" analyze ./src
```

**Output:**
```
JSharpener Analysis Summary
════════════════════════════════════════════════════════════

Files analyzed: 15
Functions: 42
Classes: 8
Imports: 67
Exports: 28
```

### 2. callgraph - Generate Call Graph
Generates Graphviz DOT format call graphs showing function dependencies.

```bash
node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" callgraph [path] -o output.dot
```

**Options:**
- `path`: Directory or file to analyze
- `-o, --output <file>`: Output DOT file (required)
- `--function <name>`: Focus on specific function
- `--reverse`: Show reverse call graph (what calls this function)
- `--depth <n>`: Maximum depth to traverse (default: 10)
- `--module-level`: Show module dependencies only
- `--config <file>`: Config file path

**Examples:**
```bash
# Full call graph
node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" callgraph ./src -o callgraph.dot

# Focus on specific function
node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" callgraph ./src --function processData -o callgraph.dot

# Reverse call graph (who calls this)
node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" callgraph ./src --function processData --reverse -o callers.dot

# Module-level dependencies
node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" callgraph ./src --module-level -o modules.dot
```

**Visualize the graph:**
```bash
# Convert to SVG
dot -Tsvg callgraph.dot -o callgraph.svg

# Convert to PNG
dot -Tpng callgraph.dot -o callgraph.png

# Open in browser (if GraphvizOnline)
# Upload the .dot file to https://dreampuf.github.io/GraphvizOnline/
```

### 3. treeshake - Find Unused Code
Detects unused exports, functions, variables, and imports (dead code detection).

```bash
node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" treeshake [path]
```

**Options:**
- `path`: Directory or file to analyze
- `-o, --output <file>`: Save report to file
- `--entry <file...>`: Entry point(s) for reachability analysis
- `--format <type>`: Output format: json or text (default: text)
- `--config <file>`: Config file path

**Examples:**
```bash
# Analyze entire project
node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" treeshake ./src

# With entry points
node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" treeshake ./src --entry src/index.ts --entry src/cli.ts

# JSON output
node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" treeshake ./src --format json -o unused.json
```

**Output:**
```
JSharpener Tree Shaking Report
════════════════════════════════════════════════════════════

Unused Exports (3):
  • src/utils/helper.ts:14: unusedFunction
  • src/services/old.ts:22: deprecatedMethod
  • src/lib/legacy.ts:8: oldHelper

Unused Functions (5):
  • src/utils/helper.ts:18: helperFunction
  • src/index.ts:7: unusedLocalFunction
  • src/services/data.ts:45: processOldFormat
  • src/lib/utils.ts:12: debugHelper
  • src/lib/utils.ts:89: tempFunction

Unused Variables (2):
  • src/config.ts:5: LEGACY_MODE
  • src/constants.ts:18: OLD_API_URL

Unused Imports (4):
  • src/index.ts:2: import { oldUtil } from './old'
  • src/services/api.ts:5: import { deprecated } from './legacy'
  • src/utils/format.ts:3: import * as unused from './unused'
  • src/lib/helpers.ts:1: import { temp } from './temp'

Potential Savings:
  • 87 lines of code could be removed
  • Estimated size reduction: 2.14 KB
```

### 4. deps - Dependency Analysis
Analyzes dependencies, finds circular dependencies, and shows external package usage.

```bash
node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" deps [path]
```

**Options:**
- `path`: Directory or file to analyze
- `-o, --output <file>`: Save results to file
- `--circular`: Only show circular dependencies
- `--external`: Analyze external package usage
- `--config <file>`: Config file path

**Examples:**
```bash
# Full dependency analysis
node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" deps ./src

# Only circular dependencies
node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" deps ./src --circular

# External package analysis
node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" deps ./src --external
```

**Output:**
```
JSharpener Dependency Analysis
════════════════════════════════════════════════════════════

Circular Dependencies (2):
  1. src/circular-a.ts → src/circular-b.ts → src/circular-a.ts
  2. src/services/user.ts → src/services/auth.ts → src/services/session.ts → src/services/user.ts

Module Dependencies:
  • src/index.ts imports 5 modules
  • src/services/api.ts imports 8 modules
  • src/utils/helper.ts imports 3 modules

External Dependencies (5):
  • typescript: 23 imports
  • commander: 4 imports
  • fast-glob: 6 imports
  • chalk: 12 imports
  • ora: 3 imports
```

## Configuration File

Create a `jsharpener.json` file in your project root:

```json
{
  "include": ["src/**/*.ts", "src/**/*.js"],
  "exclude": ["**/*.test.ts", "**/*.spec.js", "node_modules/**", "dist/**"],
  "entryPoints": ["src/index.ts", "src/cli/index.ts"],
  "followDynamicImports": true,
  "includeExternalDeps": false,
  "detectCircular": true
}
```

**Config Options:**
- `include`: Glob patterns for files to include
- `exclude`: Glob patterns for files to exclude
- `entryPoints`: Entry points for tree shaking analysis
- `followDynamicImports`: Track dynamic imports (default: true)
- `includeExternalDeps`: Include external packages in analysis (default: false)
- `detectCircular`: Detect circular dependencies (default: true)

## Usage Examples for Claude

### Example 1: Analyze Project
**User Request:** "Analyze my TypeScript project"

**Claude Action:**
```bash
node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" analyze ./src
```

**Interpretation:**
- Shows file count, function count, class count
- Provides import/export statistics
- Good for getting project overview

### Example 2: Find Unused Code
**User Request:** "Find unused code in my project"

**Claude Action:**
```bash
node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" treeshake ./src --entry src/index.ts
```

**Interpretation:**
- Lists unused exports (safe to remove if not part of public API)
- Lists unused functions (can be deleted)
- Lists unused variables (can be removed)
- Lists unused imports (clean up import statements)
- Provides size savings estimate

### Example 3: Generate Call Graph
**User Request:** "Show me the call graph for the processData function"

**Claude Action:**
```bash
node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" callgraph ./src --function processData -o callgraph.dot
dot -Tsvg callgraph.dot -o callgraph.svg
```

**Interpretation:**
- Creates visual diagram showing what processData calls
- Use `--reverse` to see who calls processData
- SVG can be viewed in browser or editor

### Example 4: Detect Circular Dependencies
**User Request:** "Are there any circular dependencies in my code?"

**Claude Action:**
```bash
node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" deps ./src --circular
```

**Interpretation:**
- Lists all circular dependency chains
- Each chain shows the import cycle
- Circular dependencies should be refactored to break the cycle

### Example 5: Module-Level Dependency Graph
**User Request:** "Show me how my modules depend on each other"

**Claude Action:**
```bash
node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" callgraph ./src --module-level -o modules.dot
dot -Tsvg modules.dot -o modules.svg
```

**Interpretation:**
- Shows high-level module dependencies
- Helps understand architecture
- Useful for refactoring planning

## Common Patterns

### Refactoring Workflow
1. Find unused code: `treeshake --entry src/index.ts`
2. Review unused exports (might be public API)
3. Delete unused functions and variables
4. Remove unused imports
5. Re-run analysis to verify

### Understanding Code Flow
1. Generate call graph: `callgraph --function main -o main.dot`
2. Visualize: `dot -Tsvg main.dot -o main.svg`
3. Explore dependencies: `deps`
4. Check for circular dependencies: `deps --circular`

### Code Review Preparation
1. Run full analysis: `analyze ./src -o analysis.json`
2. Find dead code: `treeshake ./src -o unused.txt`
3. Check dependencies: `deps ./src -o deps.txt`
4. Generate graphs for key functions

### CI/CD Integration
```yaml
# Example GitHub Actions workflow
- name: Check for unused code
  run: |
    node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" treeshake ./src --format json -o unused.json

- name: Detect circular dependencies
  run: |
    node "C:\Users\matthew.heath\Git\JSharpener\dist\cli\index.js" deps ./src --circular

- name: Upload analysis
  uses: actions/upload-artifact@v3
  with:
    name: code-analysis
    path: |
      unused.json
      deps.txt
```

## Limitations

This is a first version with some known limitations:

1. **Method Call Tracking**: Method calls through object instances may not be fully tracked in the call graph
2. **Dynamic Imports**: Dynamic imports (`import()`) are not fully supported
3. **Module Resolution**: Some edge cases in module resolution may not be handled
4. **Variable Usage**: Variable usage tracking is simplified
5. **JSX/TSX**: Limited support for React JSX/TSX files
6. **Eval/Dynamic Code**: Code using `eval()` or dynamic code generation is not analyzed

## Performance Tips

1. **Use Patterns**: Narrow analysis with `--include` and `--exclude` patterns
2. **Exclude Tests**: Use `--exclude "**/*.test.ts" "**/*.spec.ts"` for faster analysis
3. **Module-Level Graphs**: Use `--module-level` for high-level overview instead of full call graph
4. **Limit Depth**: Use `--depth 5` for large projects to limit call graph depth
5. **Entry Points**: Specify entry points for more accurate tree shaking

## Troubleshooting

### "No files found"
- Check path is correct
- Verify include/exclude patterns
- Try absolute path instead of relative

### "TypeScript errors"
- Project doesn't need to compile for analysis to work
- JSharpener uses TypeScript Compiler API with permissive settings
- Syntax errors may cause files to be skipped

### Call graph is too large
- Use `--function` to focus on specific function
- Use `--depth` to limit traversal
- Use `--module-level` for high-level view
- Exclude test files

### Unused code detection misses something
- Specify entry points with `--entry`
- Check if code is used via dynamic imports
- Verify include/exclude patterns

### Module resolution errors
- Check tsconfig.json paths
- Verify import statements are correct
- Some complex module resolution may not work

## Integration with Other Tools

### Graphviz
```bash
# Install Graphviz for visualization
# Windows: choco install graphviz
# macOS: brew install graphviz
# Linux: apt-get install graphviz

# Convert DOT to various formats
dot -Tsvg callgraph.dot -o callgraph.svg    # SVG
dot -Tpng callgraph.dot -o callgraph.png    # PNG
dot -Tpdf callgraph.dot -o callgraph.pdf    # PDF
```

### VS Code
```json
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "JSharpener: Analyze",
      "type": "shell",
      "command": "node",
      "args": [
        "C:/Users/matthew.heath/Git/JSharpener/dist/cli/index.js",
        "analyze",
        "${workspaceFolder}/src"
      ]
    },
    {
      "label": "JSharpener: Find Unused Code",
      "type": "shell",
      "command": "node",
      "args": [
        "C:/Users/matthew.heath/Git/JSharpener/dist/cli/index.js",
        "treeshake",
        "${workspaceFolder}/src"
      ]
    }
  ]
}
```

### ESLint Plugin (Future)
```js
// Potential integration with ESLint
module.exports = {
  plugins: ['jsharpener'],
  rules: {
    'jsharpener/no-circular-deps': 'error',
    'jsharpener/no-unused-exports': 'warn'
  }
};
```

## Future Enhancements

- HTML code browser with cross-references (LXR-style)
- JSDoc/TypeScript documentation generator
- Improved method call tracking through object instances
- Full JSX/TSX support
- Watch mode for continuous analysis
- VS Code extension with inline warnings
- ESLint plugin integration
- Webpack/Rollup plugin for tree shaking optimization
- Type dependency graph
- Import cost analysis

## Notes

- JSharpener uses TypeScript Compiler API (same as VS Code)
- Works with both JavaScript and TypeScript files
- Analyzes code without executing it (static analysis)
- No runtime dependencies needed in analyzed project
- Thread-safe and can analyze multiple projects in parallel
- Results are deterministic (same input = same output)

## Support

- GitHub: https://github.com/lawless-m/JSharpener (to be published)
- Built with TypeScript Compiler API
- Inspired by CSharpener

## Quick Reference

```bash
# Basic commands
analyze [path]                    # Project statistics
callgraph [path] -o file.dot     # Generate call graph
treeshake [path]                  # Find unused code
deps [path]                       # Dependency analysis

# Common options
--include "src/**/*.ts"          # Include pattern
--exclude "**/*.test.ts"         # Exclude pattern
--config jsharpener.json         # Config file
-o output.file                   # Output file

# Call graph options
--function name                  # Focus on function
--reverse                        # Reverse call graph
--depth 5                        # Limit depth
--module-level                   # Module view

# Tree shaking options
--entry src/index.ts            # Entry point
--format json                   # JSON output

# Dependency options
--circular                      # Only circular deps
--external                      # External packages
```

---
name: compile-analysis
description: This skill should be used when the user asks to "分析编译效率", "分析编译时间", "查看头文件依赖", "保存编译命令", "提取编译命令", "生成编译脚本", "保存这个文件的编译命令", "单独编译这个文件", "编译单个文件", "单编文件", "独立编译文件", "分析这个文件的头文件依赖", "头文件依赖关系", "这个文件依赖了多少头文件", "analyze compilation", "check header dependencies", "分析文件编译开销", "save compile command", "extract compile command", "generate compile script", "compile single file", "compile individual file", "standalone compile", "analyze header dependencies", "header dependency tree", "how many header files", or mentions analyzing compilation performance, build times, include dependencies, extracting/saving compilation commands, generating standalone compilation scripts, compiling individual files in isolation, or analyzing header file dependency relationships for specific source files in the ace_engine project. Provides comprehensive compilation efficiency analysis including timing, resource usage, dependency tree visualization with automatic saving, the ability to save reusable compilation scripts with performance monitoring, and standalone compilation capabilities using generated scripts.
version: 0.2.0
---

# Compilation Efficiency Analysis Skill

Analyze compilation efficiency for individual source files in the ACE Engine project. This skill provides detailed insights into compilation time, resource overhead, and header file dependencies to help identify optimization opportunities.

## Overview

Compilation analysis helps identify performance bottlenecks in the build process by measuring:
- **Compilation time** - How long a file takes to compile
- **Resource overhead** - Peak memory usage during compilation
- **Header dependencies** - Tree structure of included headers

**Critical Requirements**:
- ⚠️ **The analyze_compile.sh script can be executed from the current project directory**
- ⚠️ **Extracted compilation commands MUST be executed in the `out/{product}` directory** (not from the project root)
- ⚠️ **All analysis results MUST be based on actual execution - no speculation or estimation**
- ⚠️ **Header dependencies MUST be parsed using the built-in `parse_ii.py` script to analyze `.ii` files** - do not use alternative methods

Use this analysis when:
- Investigating slow compilation times
- Identifying files with excessive dependencies
- Optimizing build performance
- Understanding include relationships

## Analysis Workflow

### Step 1: Locate Source File

Identify the target source file for analysis. Source files in ace_engine typically follow patterns:
- `frameworks/core/components_ng/base/frame_node.cpp`
- `frameworks/bridge/declarative_frontend/engine/js_engine.cpp`

### Step 2: Find OpenHarmony Root

The analysis scripts automatically locate the OpenHarmony root directory by searching for the `.gn` file marker. Navigate to the OpenHarmony root directory to ensure proper path resolution.

### Step 3: Choose Analysis Mode

**Option A: Full Analysis (Execute + Display Results)**

```bash
./.claude/skills/compile-analysis/scripts/analyze_compile.sh <source-file> [product-name]
```

Example:
```bash
./.claude/skills/compile-analysis/scripts/analyze_compile.sh frameworks/core/components_ng/base/frame_node.cpp rk3568
```

**Option B: Save Reusable Compilation Script**

Generate a standalone script that can be executed multiple times for performance testing:

```bash
./.claude/skills/compile-analysis/scripts/analyze_compile.sh <source-file> [product-name] --save-script
```

This creates `out/{product}/compile_single_file_{name}.sh` with:
- Automatic environment setup
- Performance monitoring (time + memory)
- Generation of .ii and .o files
- Repeatable execution for benchmarking

### Step 4: Interpret Results

The analysis produces three key outputs:

1. **Compilation command** - Full compiler command with all flags
2. **Performance metrics**:
   - Elapsed time (format: `MM:SS.mm`)
   - Peak memory usage in KB
3. **Dependency tree** - Hierarchical view of header inclusions

When using `--save-script`, a reusable script is generated for repeated performance testing.

## Key Scripts

### analyze_compile.sh (Main Script)

Primary entry point for compilation analysis. Orchestrates the entire analysis workflow:

**Usage**:
```bash
# Full analysis with execution
./.claude/skills/compile-analysis/scripts/analyze_compile.sh <source-file> [product-name]

# Save standalone compilation script
./.claude/skills/compile-analysis/scripts/analyze_compile.sh <source-file> [product-name] --save-script
```

**Arguments**:
- `source-file` - Path to the source file (relative to ace_engine root or absolute)
- `product-name` - Target product (default: `rk3568`)
- `--save-script` - Save enhanced compilation command to reusable script file

**Workflow**:
1. Extracts compilation command from ninja build files
2. Generates enhanced compilation command with instrumentation
3. (Optional) Saves script to `out/{product}/compile_single_file_{name}.sh`
4. Executes compilation with time and memory profiling
5. Parses .ii preprocessed file to extract dependencies
6. Displays comprehensive results

**Output with --save-script**:
- Generates a standalone bash script at `out/{product}/compile_single_file_{name}.sh`
- Script includes automatic environment setup
- Performance monitoring (compilation time + peak memory)
- Can be executed multiple times for performance comparisons
- Useful for benchmarking and optimization validation

### get_compile_command.py

Extracts the complete compilation command for a source file from the ninja build system.

**Usage (from ace_engine root)**:
```bash
# Display commands only
python3 ./.claude/skills/compile-analysis/scripts/get_compile_command.py \
  <source-file> <openharmony_root>/out/<product>

# Save enhanced command (with performance monitoring)
python3 ./.claude/skills/compile-analysis/scripts/get_compile_command.py \
  <source-file> <openharmony_root>/out/<product> --save-enhanced
```

**Example**:
```bash
# From ace_engine directory
python3 ./.claude/skills/compile-analysis/scripts/get_compile_command.py \
  frameworks/core/components_ng/base/frame_node.cpp \
  /home/sunfei/workspace/openHarmony/out/rk3568 --save-enhanced
```

**Features**:
- Parses ninja build files to locate compilation rules
- Extracts compiler flags, defines, and include paths
- Generates two versions:
  1. Original command (with ccache for development)
  2. Enhanced command (without ccache, with `-save-temps` for analysis)
- **Can save commands to standalone scripts** for repeated execution

**Output**:
- Original compilation command
- Enhanced compilation command with instrumentation
- Optional: Saved script files for reuse
  - `--save`: Creates `{file}_compile_command.sh` (original command)
  - `--save-enhanced`: Creates `compile_single_file_{file}.sh` (enhanced with monitoring)

### parse_ii.py

Analyzes .ii preprocessed files to extract and display header file dependencies.

**Usage**:
```bash
python3 ./.claude/skills/compile-analysis/scripts/parse_ii.py <ii-file>
```

**Features**:
- Parses .ii files (preprocessed C++ source)
- Extracts `#include` directives targeting `foundation/arkui/`
- Builds dependency tree structure
- Displays tree with Unicode box-drawing characters

**Output Format**:
```
头文件的依赖关系树：
└── foundation/arkui/ace_engine/frameworks/core/components_ng/base/frame_node.h
    └── foundation/arkui/ace_engine/frameworks/core/components_ng/base/ui_node.h
        ├── foundation/arkui/ace_engine/frameworks/core/pipeline/base/element.h
        └── ...
```

## Understanding the Results

### Compilation Time

Format: `MM:SS.mm` (minutes:seconds.milliseconds)
- **Fast**: < 5 seconds (typical for small files)
- **Moderate**: 5-15 seconds
- **Slow**: > 15 seconds (may indicate optimization opportunities)

### Peak Memory

Reported in kilobytes (KB)
- **Typical**: 100,000 - 500,000 KB (100-500 MB)
- **High**: > 500,000 KB - may indicate excessive template instantiation or header dependencies

### Dependency Tree

The tree shows hierarchical include relationships:
- Each level represents an `#include` directive
- Multiple children indicate multiple includes in a file
- Deep trees suggest heavy dependency chains

**Optimization indicators**:
- **Wide trees** (many direct includes) - Consider header consolidation
- **Deep trees** (long chains) - Look for circular dependencies or excessive forwarding
- **Duplicate paths** - Header guards missing or include order issues

## Common Use Cases

### Analyzing Header File Dependencies

When you need to analyze the header file dependency structure of a source file:

**Important**: This workflow **ONLY** uses `.ii` files generated by compilation scripts. No other dependency analysis methods are used.

**Workflow**:
1. Check if `.ii` file exists in `out/{product}/obj/` directory
2. If `.ii` exists → Parse it directly with `parse_ii.py`
3. If `.ii` doesn't exist → Generate it using compilation script, then parse
4. **Always save** the dependency tree to `out/{product}/{file_name}_dependency_tree.txt`

**Example using Claude**:
```bash
# User request: "分析 frame_node.cpp 的头文件依赖"
# Claude's response:

# Step 1: Check for existing .ii file
# ✓ Found: out/rk3568/obj/.../frame_node.ii

# Step 2: Parse .ii file and save dependency tree
python3 ./.claude/skills/compile-analysis/scripts/parse_ii.py \
  out/rk3568/obj/.../frame_node.ii \
  --output out/rk3568/frame_node_dependency_tree.txt

# Output:
# 头文件的依赖关系树：
# └── foundation/arkui/ace_engine/frameworks/core/components_ng/base/frame_node.h
#     ├── foundation/arkui/ace_engine/frameworks/core/components_ng/base/ui_node.h
#     │   ├── foundation/arkui/ace_engine/frameworks/core/pipeline/base/element.h
#     │   └── foundation/arkui/ace_engine/base/memory/ace_type.h
#     └── foundation/arkui/ace_engine/frameworks/core/components_ng/property/property.h
#
# ✓ 依赖树已保存到: out/rk3568/frame_node_dependency_tree.txt
```

**If .ii file doesn't exist**:
```bash
# User request: "这个文件依赖了多少头文件 text_theme.cpp"
# Claude's response:

# Step 1: Check for existing .ii file
# ✗ .ii file not found

# Step 2: Check for compilation script
# ✓ Found: out/rk3568/compile_single_file_text_theme.sh

# Step 3: Generate .ii file by running compilation script
cd out/rk3568
bash compile_single_file_text_theme.sh

# Step 4: Parse .ii file and save dependency tree
python3 ../../.claude/skills/compile-analysis/scripts/parse_ii.py \
  obj/.../text_theme.ii \
  --output text_theme_dependency_tree.txt

# Output:
# 头文件的依赖关系树：
# └── foundation/arkui/ace_engine/frameworks/core/components/text/text_theme.h
#     ├── ...
#
# ✓ 依赖树已保存到: out/rk3568/text_theme_dependency_tree.txt
#
# 统计信息:
# - 总计依赖: 47 个头文件
# - 最大深度: 6 层
```

**If neither .ii nor script exists**:
```bash
# User request: "头文件依赖关系 button_pattern.cpp"
# Claude's response:

# Step 1: Check for existing .ii file
# ✗ .ii file not found

# Step 2: Check for compilation script
# ✗ Compilation script not found

# Step 3: Generate compilation script first
python3 ./.claude/skills/compile-analysis/scripts/get_compile_command.py \
  frameworks/core/components_ng/pattern/button_pattern.cpp \
  <openharmony_root>/out/rk3568 --save-enhanced

# ✓ Script generated: out/rk3568/compile_single_file_button_pattern.sh

# Step 4: Generate .ii file by running script
cd out/rk3568
bash compile_single_file_button_pattern.sh

# Step 5: Parse .ii file and save dependency tree
python3 ../../.claude/skills/compile-analysis/scripts/parse_ii.py \
  obj/.../button_pattern.ii \
  --output button_pattern_dependency_tree.txt

# ✓ 依赖树已保存到: out/rk3568/button_pattern_dependency_tree.txt
```

**Trigger phrases**:
- "分析这个文件的头文件依赖"
- "头文件依赖关系"
- "这个文件依赖了多少头文件"
- "analyze header dependencies"
- "header dependency tree"
- "how many header files"

**Output file naming**:
- Format: `{file_name}_dependency_tree.txt`
- Location: `out/{product}/`
- Example: `out/rk3568/frame_node_dependency_tree.txt`

**Constraints**:
- ✅ MUST parse `.ii` files using `parse_ii.py`
- ✅ MUST use compilation scripts to generate `.ii` if needed
- ✅ MUST save dependency tree to `out/{product}/{file_name}_dependency_tree.txt`
- ❌ DO NOT use other dependency analysis tools (like clang -E, gcc -M, etc.)
- ❌ DO NOT attempt manual dependency parsing

### Standalone Compilation of Individual Files

When you need to compile a single file in isolation (for testing, debugging, or verification):

**Important**: This workflow **ONLY** uses pre-generated compilation scripts. No other compilation methods are used.

**Workflow**:
1. Check if compilation script exists: `out/{product}/compile_single_file_{name}.sh`
2. If script exists → Execute it directly
3. If script doesn't exist → Generate it first, then execute

**Example using Claude**:
```bash
# User request: "单独编译 frame_node.cpp"
# Claude's response:

# Step 1: Check for existing script
# ✓ Found: out/rk3568/compile_single_file_frame_node.sh

# Step 2: Execute the script
cd out/rk3568
bash compile_single_file_frame_node.sh

# Output:
# 编译时间: 0:08.23
# 峰值内存: 234567 KB
# ✓ 已生成: obj/.../frame_node.ii obj/.../frame_node.o
```

**If script doesn't exist**:
```bash
# User request: "单编 text_theme.cpp"
# Claude's response:

# Step 1: Check for existing script
# ✗ Script not found: out/rk3568/compile_single_file_text_theme.sh

# Step 2: Generate script first
python3 ./.claude/skills/compile-analysis/scripts/get_compile_command.py \
  frameworks/core/components/text/text_theme.cpp <openharmony_root>/out/rk3568 --save-enhanced

# ✓ Script generated: out/rk3568/compile_single_file_text_theme.sh

# Step 3: Execute the script
cd out/rk3568
bash compile_single_file_text_theme.sh
```

**Trigger phrases**:
- "单独编译这个文件"
- "编译单个文件"
- "单编文件"
- "独立编译文件"
- "compile single file"
- "compile individual file"
- "standalone compile"

**Constraints**:
- ✅ MUST use existing `compile_single_file_{name}.sh` scripts
- ✅ MUST generate script if it doesn't exist before compilation
- ❌ DO NOT use ninja, make, or other build tools directly
- ❌ DO NOT attempt manual compilation commands

### Extracting and Saving Compilation Commands

When you need to extract or save compilation commands for later use:

**Save standalone script with performance monitoring**:
```bash
./.claude/skills/compile-analysis/scripts/analyze_compile.sh \
  frameworks/core/components_ng/base/frame_node.cpp rk3568 --save-script

# Script saved to: out/rk3568/compile_single_file_frame_node.sh
# Execute later: cd out/rk3568 && bash compile_single_file_frame_node.sh
```

**Extract command only without execution**:
```bash
python3 ./.claude/skills/compile-analysis/scripts/get_compile_command.py \
  frameworks/core/components_ng/base/frame_node.cpp \
  <openharmony_root>/out/rk3568 --save-enhanced
```

This is useful for:
- Creating reusable compilation scripts
- Setting up performance benchmarking
- Generating reproducible build environments
- Isolating specific file compilation for testing

### Investigating Slow Builds

When incremental builds are slower than expected:

1. Identify slow-compiling files by reviewing build log timestamps
2. Run analysis on slow files: `./analyze_compile.sh <slow-file>`
3. Check dependency tree depth and breadth
4. Look for frequently included heavy headers

### Optimizing Header Dependencies

To reduce unnecessary recompilation:

1. Analyze dependency tree for common patterns
2. Identify headers included by many files
3. Consider forward declarations instead of full includes
4. Use precompiled headers (PCH) for stable dependencies

### Before/After Comparisons

Measure optimization impact using saved scripts:

1. **Generate baseline script**:
   ```bash
   ./analyze_compile.sh <file> rk3568 --save-script
   cd out/rk3568
   ```

2. **Run baseline measurement**:
   ```bash
   bash compile_single_file_{name}.sh
   # Record: 编译时间: 0:15.23, 峰值内存: 456789 KB
   ```

3. **Apply optimizations** (reduce includes, forward declarations, etc.)

4. **Run comparison measurement**:
   ```bash
   bash compile_single_file_{name}.sh
   # Record: 编译时间: 0:08.45, 峰值内存: 234567 KB
   ```

5. **Compare results** to quantify improvements

The saved script ensures identical compilation conditions for fair comparison.

## Troubleshooting

### Issue: "找不到编译规则" (Compilation rule not found)

**Cause**: Source file path doesn't match build database
**Solutions**:
- Ensure the file is in the ace_engine directory structure
- Check if the file has been built before (run full build first)
- Verify path format: use relative path from ace_engine root

### Issue: "找不到 .ii 文件" (.ii file not found)

**Cause**: Compilation with `-save-temps` failed or file not created
**Solutions**:
- Check if enhanced compilation command succeeded
- Verify compiler supports `-save-temps=obj` flag
- Manually search obj directory: `find out/<product>/obj -name "*.ii"`

### Issue: Dependency tree shows few files

**Cause**: parse_ii.py filters for `foundation/arkui/` prefix only
**Solutions**:
- This is expected behavior - focuses on arkui-specific headers
- System headers are intentionally excluded
- Modify `target_prefix` in parse_ii.py to include other paths

## Best Practices

- **Start with full build**: Ensure project has been built at least once
- **Use relative paths**: Provide paths relative to ace_engine root
- **Product-specific analysis**: Specify product name if not using default rk3568
- **Compare benchmarks**: Track changes over time with saved results
- **Focus on hot paths**: Prioritize analysis on frequently modified files

## Additional Resources

### Reference Files

For detailed workflows and advanced usage:
- **`references/workflow.md`** - Comprehensive workflow guide
- **`references/optimization.md`** - Optimization strategies and patterns

### Example Files

Working examples in `examples/`:
- **`examples/example-analysis.sh`** - Complete analysis example
- **`examples/example-output.txt`** - Sample output with interpretation

## Integration with Build System

This skill integrates with the OpenHarmony GN/Ninja build system:
- Reads build metadata from `out/<product>/` directory
- Parses `toolchain.ninja` for compiler rules
- Extracts file-specific compilation commands from ninja files
- Generates instrumentation-compatible commands for analysis

The enhanced compilation command modifies the original command by:
1. Removing ccache (to get accurate timing)
2. Adding `-save-temps=obj` (to generate .ii files)
3. Wrapping with `/usr/bin/time` (to measure resources)
4. Suppressing related warnings (`-Wno-undefined-bool-conversion`)

This ensures accurate measurements while maintaining compilation compatibility.

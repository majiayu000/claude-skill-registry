---
name: ghidra
description: "Reverse engineer binaries using Ghidra's headless analyzer. Decompile executables, extract functions, strings, symbols, and analyze call graphs without GUI."
---

# Ghidra Headless Analysis Skill

Perform automated reverse engineering using Ghidra's `analyzeHeadless` tool. Import binaries, run analysis, decompile to C code, and extract useful information.

## Quick Reference

| Task | Command |
|------|---------|
| Full analysis with all exports | `ghidra-analyze.sh -s ExportAll.java -o ./output binary` |
| Decompile to C code | `ghidra-analyze.sh -s ExportDecompiled.java -o ./output binary` |
| List functions | `ghidra-analyze.sh -s ExportFunctions.java -o ./output binary` |
| Extract strings | `ghidra-analyze.sh -s ExportStrings.java -o ./output binary` |
| Get call graph | `ghidra-analyze.sh -s ExportCalls.java -o ./output binary` |
| Export symbols | `ghidra-analyze.sh -s ExportSymbols.java -o ./output binary` |
| Find Ghidra path | `find-ghidra.sh` |

## Prerequisites

- **Ghidra** must be installed. On macOS: `brew install --cask ghidra`
- **Java** (OpenJDK 17+) must be available

The skill automatically locates Ghidra in common installation paths. Set `GHIDRA_HOME` environment variable if Ghidra is installed in a non-standard location.

---

## Main Wrapper Script

```bash
./scripts/ghidra-analyze.sh [options] <binary>
```

Wrapper that handles project creation/cleanup and provides a simpler interface to `analyzeHeadless`.

**Options:**
- `-o, --output <dir>` - Output directory for results (default: current dir)
- `-s, --script <name>` - Post-analysis script to run (can be repeated)
- `-a, --script-args <args>` - Arguments for the last specified script
- `--script-path <path>` - Additional script search path
- `-p, --processor <id>` - Processor/architecture (e.g., `x86:LE:32:default`)
- `-c, --cspec <id>` - Compiler spec (e.g., `gcc`, `windows`)
- `--no-analysis` - Skip auto-analysis (faster, but less info)
- `--timeout <seconds>` - Analysis timeout per file
- `--keep-project` - Keep the Ghidra project after analysis
- `--project-dir <dir>` - Directory for Ghidra project (default: /tmp)
- `--project-name <name>` - Project name (default: auto-generated)
- `-v, --verbose` - Verbose output

---

## Built-in Export Scripts

### ExportAll.java
Comprehensive export - runs all other exports and creates a summary. Best for initial analysis.

**Output files:**
- `{name}_summary.txt` - Overview: architecture, memory sections, function counts
- `{name}_decompiled.c` - All functions decompiled to C
- `{name}_functions.json` - Function list with signatures and calls
- `{name}_strings.txt` - All strings found
- `{name}_interesting.txt` - Functions matching security-relevant patterns

```bash
./scripts/ghidra-analyze.sh -s ExportAll.java -o ./analysis firmware.bin
```

### ExportDecompiled.java
Decompile all functions to C pseudocode.

**Output:** `{name}_decompiled.c`

```bash
./scripts/ghidra-analyze.sh -s ExportDecompiled.java -o ./output program.exe
```

### ExportFunctions.java
Export function list as JSON with addresses, signatures, parameters, and call relationships.

**Output:** `{name}_functions.json`

```json
{
  "program": "example.exe",
  "architecture": "x86",
  "functions": [
    {
      "name": "main",
      "address": "0x00401000",
      "size": 256,
      "signature": "int main(int argc, char **argv)",
      "returnType": "int",
      "callingConvention": "cdecl",
      "isExternal": false,
      "parameters": [{"name": "argc", "type": "int"}, ...],
      "calls": ["printf", "malloc", "process_data"],
      "calledBy": ["_start"]
    }
  ]
}
```

### ExportStrings.java
Extract all strings (ASCII, Unicode) with addresses.

**Output:** `{name}_strings.json`

```bash
./scripts/ghidra-analyze.sh -s ExportStrings.java -o ./output malware.exe
```

### ExportCalls.java
Export function call graph showing caller/callee relationships.

**Output:** `{name}_calls.json`

Includes:
- Full call graph
- Potential entry points (functions with no callers)
- Most frequently called functions

### ExportSymbols.java
Export all symbols: imports, exports, and internal symbols.

**Output:** `{name}_symbols.json`

---

## Common Workflows

### Analyze an Unknown Binary

```bash
# Create output directory
mkdir -p ./analysis

# Run comprehensive analysis
./scripts/ghidra-analyze.sh -s ExportAll.java -o ./analysis unknown_binary

# Review the summary first
cat ./analysis/unknown_binary_summary.txt

# Look at interesting patterns (crypto, network, dangerous functions)
cat ./analysis/unknown_binary_interesting.txt

# Check specific decompiled functions
grep -A 50 "encrypt" ./analysis/unknown_binary_decompiled.c
```

### Analyze Firmware

```bash
# Specify ARM architecture for firmware
./scripts/ghidra-analyze.sh \
    -p "ARM:LE:32:v7" \
    -s ExportAll.java \
    -o ./firmware_analysis \
    firmware.bin
```

### Quick Function Listing

```bash
# Just get function names and addresses (faster)
./scripts/ghidra-analyze.sh --no-analysis -s ExportFunctions.java -o . program

# Parse with jq
cat program_functions.json | jq '.functions[] | "\(.address): \(.name)"'
```

### Find Specific Patterns

```bash
# After running ExportDecompiled, search for patterns
grep -n "password\|secret\|key" output_decompiled.c
grep -n "strcpy\|sprintf\|gets" output_decompiled.c
```

### Analyze Multiple Binaries

```bash
for bin in ./samples/*; do
    name=$(basename "$bin")
    ./scripts/ghidra-analyze.sh -s ExportAll.java -o "./results/$name" "$bin"
done
```

---

## Architecture/Processor IDs

Common processor IDs for the `-p` option:

| Architecture | Processor ID |
|-------------|--------------|
| x86 32-bit | `x86:LE:32:default` |
| x86 64-bit | `x86:LE:64:default` |
| ARM 32-bit | `ARM:LE:32:v7` |
| ARM 64-bit | `AARCH64:LE:64:v8A` |
| MIPS 32-bit | `MIPS:BE:32:default` or `MIPS:LE:32:default` |
| PowerPC | `PowerPC:BE:32:default` |

Find all available processors:
```bash
ls "$(dirname $(./scripts/find-ghidra.sh))/../Ghidra/Processors/"
```

---

## Troubleshooting

### Ghidra Not Found
```bash
# Check if Ghidra is installed
./scripts/find-ghidra.sh

# Set GHIDRA_HOME if in non-standard location
export GHIDRA_HOME=/path/to/ghidra_11.x_PUBLIC
./scripts/ghidra-analyze.sh ...
```

### Analysis Takes Too Long
```bash
# Set a timeout (seconds)
./scripts/ghidra-analyze.sh --timeout 300 -s ExportAll.java binary

# Skip analysis for quick export
./scripts/ghidra-analyze.sh --no-analysis -s ExportSymbols.java binary
```

### Out of Memory
Edit the `analyzeHeadless` script or set:
```bash
export MAXMEM=4G
```

### Wrong Architecture Detected
Explicitly specify the processor:
```bash
./scripts/ghidra-analyze.sh -p "ARM:LE:32:v7" -s ExportAll.java firmware.bin
```

---

## Tips

1. **Start with ExportAll.java** - It gives you everything and the summary helps orient you
2. **Check the interesting.txt file** - It highlights security-relevant functions automatically
3. **Use jq for JSON parsing** - The JSON exports are designed to be machine-readable
4. **Decompilation isn't perfect** - Use it as a guide, cross-reference with disassembly
5. **Large binaries take time** - Use `--timeout` and consider `--no-analysis` for quick scans

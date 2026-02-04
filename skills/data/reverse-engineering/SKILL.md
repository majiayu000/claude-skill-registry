---
name: reverse-engineering
description: Reverse Engineering Skill
version: 1.0.0
---

# Reverse Engineering Skill

Binary analysis and reverse engineering via MCP servers for Ghidra, IDA Pro, radare2, and angr.

## Trigger Conditions

- User asks to analyze binaries, disassemble code, decompile functions
- Questions about malware analysis, vulnerability research, CTF challenges
- Binary diffing, patch analysis, firmware extraction
- Symbol recovery, function identification, control flow analysis

## MCP Servers

### 1. GhidrAssistMCP (Ghidra - Free)
**Repository**: https://github.com/jtang613/GhidrAssistMCP  
**Stars**: High activity  
**Transport**: HTTP/SSE on port 8080

**Installation**:
```bash
# Download from releases page
# In Ghidra: File → Install Extensions → Add Extension
# Enable: File → Configure → Configure Plugins → GhidrAssistMCP
```

**31 Built-in Tools**:
| Category | Tools |
|----------|-------|
| Program Analysis | `get_program_info`, `list_functions`, `list_data`, `list_strings`, `list_imports`, `list_exports`, `list_segments` |
| Function Analysis | `get_function_info`, `decompile_function`, `disassemble_function`, `function_xrefs`, `search_functions` |
| Navigation | `get_current_address`, `xrefs_to`, `xrefs_from`, `get_current_function` |
| Modification | `rename_function`, `rename_variable`, `set_function_prototype`, `set_local_variable_type`, `set_disassembly_comment` |
| Advanced | `auto_create_struct` |

### 2. LaurieWired/GhidraMCP (Popular Alternative)
**Repository**: https://github.com/LaurieWired/GhidraMCP  
**Transport**: Python bridge to Ghidra

### 3. IDA Pro MCP Servers

**mrexodia/ida-pro-mcp** (Most active):
```bash
git clone https://github.com/mrexodia/ida-pro-mcp
cd ida-pro-mcp
pip install -e .
```

**MxIris-Reverse-Engineering/ida-mcp-server** (473 stars):
```bash
git clone https://github.com/MxIris-Reverse-Engineering/ida-mcp-server
```

**fdrechsler/mcp-server-idapro**:
```bash
git clone https://github.com/fdrechsler/mcp-server-idapro
```

### 4. radare2-mcp (Official)
**Repository**: https://github.com/radareorg/radare2-mcp  
**Transport**: stdio

```bash
# Install radare2 first
brew install radare2  # macOS
# or: apt install radare2  # Linux

git clone https://github.com/radareorg/radare2-mcp
cd radare2-mcp
pip install -e .
```

**MCP Config**:
```json
{
  "mcpServers": {
    "radare2": {
      "command": "r2-mcp",
      "args": []
    }
  }
}
```

### 5. rand-tech/pcm (Multi-tool)
**Repository**: https://github.com/rand-tech/pcm  
MCP for reverse engineering combining multiple backends.

## Workflows

### Basic Binary Analysis
```
1. Load binary into Ghidra/IDA
2. Start MCP server
3. Query: "List all functions" → list_functions
4. Query: "Decompile main" → decompile_function
5. Query: "Find xrefs to this address" → xrefs_to
```

### Malware Analysis Pattern
```
1. get_program_info → Architecture, compiler, entry point
2. list_imports → Suspicious API calls (CreateRemoteThread, VirtualAlloc)
3. list_strings → C2 URLs, encryption keys, debug strings
4. search_functions "crypt" → Find encryption routines
5. decompile_function → Understand algorithm
6. auto_create_struct → Recover data structures
```

### Vulnerability Research
```
1. list_functions → Function list with sizes
2. search_functions "parse|read|copy" → Input handlers
3. decompile_function → Find buffer operations
4. xrefs_to → Trace data flow
5. set_decompiler_comment → Annotate findings
```

### CTF Binary Exploitation
```
1. get_program_info → Check protections (PIE, RELRO, canary)
2. list_functions → Find win/flag functions
3. decompile_function → Understand vulnerability
4. xrefs_from → Control flow analysis
5. list_segments → Memory layout for ROP
```

## CLI Quick Reference

### radare2 Commands
```bash
r2 binary                    # Open binary
aaa                          # Analyze all
afl                          # List functions
pdf @ main                   # Disassemble function
pdc @ main                   # Decompile (r2ghidra)
axt @ addr                   # Xrefs to
axf @ addr                   # Xrefs from
iz                           # List strings
ii                           # List imports
```

### Ghidra Headless
```bash
analyzeHeadless /tmp/project ProjectName \
  -import binary.exe \
  -postScript ExportDecompilation.java \
  -deleteProject
```

## Resources

- [Awesome Reverse Engineering](https://github.com/wtsxDev/reverse-engineering)
- [CTF Wiki - Reverse](https://ctf-wiki.org/reverse/)
- [Ghidra Scripting](https://ghidra.re/ghidra_docs/api/)
- [radare2 Book](https://book.rada.re/)

## r2con Speaker Repositories

Key repositories from r2con 2016-2025 speakers for process tree and binary analysis:

### Core radare2 Team
| Speaker | Handle | Repository | Specialty |
|---------|--------|------------|-----------|
| Sergi Alvarez | pancake | [github.com/trufae](https://github.com/trufae) | radare2 creator, r2pipe |
| Anton Kochkov | xvilka | [github.com/XVilka](https://github.com/XVilka) | UEFI, radeco decompiler |
| Florian Märkl | thestr4ng3r | [github.com/thestr4ng3r](https://github.com/thestr4ng3r) | Cutter/Rizin founder |
| condret | condret | [github.com/condret](https://github.com/condret) | ESIL core, SIOL I/O |
| wargio | wargio | [github.com/wargio](https://github.com/wargio) | GSoC mentor |
| maijin | maijin | [github.com/maijin](https://github.com/maijin) | r2 book maintainer |

### ESIL & Symbolic Execution
| Speaker | Handle | Repository | Specialty |
|---------|--------|------------|-----------|
| Chase Kanipe | alkalinesec | [github.com/alkalinesec](https://github.com/alkalinesec) | ESILSolve symbolic exec |
| Sylvain Pelissier | Pelissier_S | N/A | ESIL side-channel simulation |
| Abel Valero | skuater | [github.com/skuater](https://github.com/skuater) | r2wars, ESIL plugins |
| Gerardo García | killabytenow | [github.com/killabytenow](https://github.com/killabytenow) | ESIL limits |

### Frida Integration (r2frida)
| Speaker | Handle | Repository | Specialty |
|---------|--------|------------|-----------|
| Ole André Ravnås | oleavr | [github.com/oleavr](https://github.com/oleavr) | Frida creator, NowSecure |
| Giovanni Rocca | iGio90 | [github.com/iGio90](https://github.com/iGio90) | Dwarf debugger |
| Grant Douglas | hexploitable | [github.com/hexploitable](https://github.com/hexploitable) | r2frida mobile |
| Alex Soler | as0ler | N/A | r2frida Kung Fu, r2env |

### Malware & Security Analysis
| Speaker | Handle | Repository | Specialty |
|---------|--------|------------|-----------|
| Axelle Apvrille | cryptax | [github.com/cryptax](https://github.com/cryptax) | Malware, r2ai, droidlysis |
| Tim Blazytko | mr_phrazer | [github.com/mrphrazer](https://github.com/mrphrazer) | MBA deobfuscation, msynth |
| Julien Voisin | jvoisin | [github.com/jvoisin](https://github.com/jvoisin) | Security tooling |
| cmatthewbrooks | cmatthewbrooks | N/A | Windows malware |

### Signatures & Similarity
| Speaker | Handle | Repository | Specialty |
|---------|--------|------------|-----------|
| Barton Rhodes | bmorphism | [github.com/bmorphism](https://github.com/bmorphism) | r2 Zignatures (2020) |
| swoops | swoops | [github.com/swoops](https://github.com/swoops) | libc_zignatures, dr_pebber |
| Fernando Dominguez | FernandoDoming | [github.com/FernandoDoming](https://github.com/FernandoDoming) | diaphora similarity |

### Mobile Security (OWASP MSTG)
| Speaker | Handle | Repository | Specialty |
|---------|--------|------------|-----------|
| Carlos Holguera | cpholguera | [github.com/cpholguera](https://github.com/cpholguera) | OWASP MSTG co-author |
| Eduardo Novella | enovella | [github.com/enovella](https://github.com/enovella) | NowSecure, r2frida |
| Francesco Tamagni | mrmacete | [github.com/mrmacete](https://github.com/mrmacete) | NowSecure iOS |

### Decompilation & Analysis
| Speaker | Handle | Repository | Specialty |
|---------|--------|------------|-----------|
| Ahmed Abd El Mawgood | oddcoder | [github.com/oddcoder](https://github.com/oddcoder) | RAIR (Radare In Rust) |
| Antide Petit | xarkes | [github.com/xarkes](https://github.com/xarkes) | Cutter development |
| Arnau Gamez | arnaugamez | [github.com/arnaugamez](https://github.com/arnaugamez) | Side-channel attacks |

### Key Tool Repositories
```bash
# radare2 ecosystem
git clone https://github.com/radareorg/radare2      # Core framework
git clone https://github.com/radareorg/r2ghidra     # Ghidra decompiler
git clone https://github.com/radareorg/radare2-mcp  # MCP server
git clone https://github.com/radareorg/esil-rs      # ESIL in Rust

# Rizin fork (Cutter backend)
git clone https://github.com/rizinorg/rizin         # Rizin framework
git clone https://github.com/rizinorg/cutter        # GUI
git clone https://github.com/rizinorg/rz-ghidra     # Ghidra integration

# Frida ecosystem
git clone https://github.com/frida/frida-core       # Core library
git clone https://github.com/frida/frida-gum        # Instrumentation
git clone https://github.com/frida/cryptoshark      # Code tracer

# Speaker tools
git clone https://github.com/swoops/libc_zignatures # libc signatures
git clone https://github.com/swoops/dr_pebber       # Fake TEB/PEB for ESIL
git clone https://github.com/mrphrazer/msynth       # MBA simplification
git clone https://github.com/cryptax/droidlysis     # Android analysis
git clone https://github.com/iGio90/Dwarf           # Frida debugger
git clone https://github.com/condret/r2premium      # r2 premium features
```

### Process Tree Analysis Perspectives

Each speaker brings unique analysis perspective:

| Speaker | Focus | Process Tree Approach |
|---------|-------|----------------------|
| **pancake** | Core r2 | `r2 -d pid://PID` attach, sandbox escape surfaces |
| **xvilka** | UEFI/radeco | Chromium shmem handles, decompile GPU process |
| **condret** | ESIL | Each PID as ESIL context, trace IPC parsing |
| **Pelissier_S** | Side-channel | Timing oracles in `--time-ticks-*` params |
| **alkalinesec** | ESILSolve | Symbolic exec on sandbox constraints |
| **iGio90** | r2frida | `frida -U -n 'process'` + r2 integration |
| **thestr4ng3r** | Cutter | GUI attach, graph shader pipeline |
| **cryptax** | Malware | Persistence via flox-watchdog, LOLbins |
| **bmorphism** | Zignatures | `zg` signature generation across renderer variants |
| **swoops** | dr_pebber | Fake PEB structures for Windows emulation |
| **mr_phrazer** | Deobfuscation | MBA expressions in obfuscated binaries |

## Example Session

```
User: Analyze this binary for buffer overflow vulnerabilities

Agent:
1. Starting GhidraMCP server...
2. Loading binary and auto-analyzing...
3. [list_functions] Found 47 functions
4. [search_functions "strcpy|sprintf|gets"] Found 3 dangerous calls:
   - sub_401234: uses strcpy with stack buffer
   - sub_401456: sprintf without bounds
5. [decompile_function "sub_401234"] 
   
   void vuln_func(char *input) {
       char buffer[64];
       strcpy(buffer, input);  // VULNERABLE: no bounds check
       ...
   }

6. [xrefs_to "sub_401234"] Called from main+0x45
7. Vulnerability confirmed: Stack buffer overflow in sub_401234
```

---

## End-of-Skill Interface

## Integration with Gay.jl Colors

Assign deterministic colors to binary analysis domains:

```julia
using Gay

# Trit classification for RE tools
GHIDRA_TRIT = 0      # ZERO - foundational analysis
IDA_TRIT = 1         # PLUS - commercial/advanced  
RADARE2_TRIT = -1    # MINUS - lightweight/CLI

# Color functions by complexity
function color_function(cyclomatic_complexity::Int, seed::UInt64)
    Gay.color_at(cyclomatic_complexity, seed)
end

# Color control flow graph nodes
function color_cfg_node(block_id::Int, func_seed::UInt64)
    Gay.color_at(block_id, func_seed)
end
```

## Related Skills

- `effective-topos`: radare2 integration
- `mcp-tripartite`: Binary analysis trit (-1 MINUS)
- `binsec`: Symbolic execution tutorials
- `gay-mcp`: Deterministic coloring for CFG visualization

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 3. Variations on an Arithmetic Theme

**Concepts**: generic arithmetic, coercion, symbolic, numeric

### GF(3) Balanced Triad

```
reverse-engineering (−) + SDF.Ch3 (○) + [balancer] (+) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch10: Adventure Game Example
- Ch4: Pattern Matching
- Ch7: Propagators

### Connection Pattern

Generic arithmetic crosses type boundaries. This skill handles heterogeneous data.

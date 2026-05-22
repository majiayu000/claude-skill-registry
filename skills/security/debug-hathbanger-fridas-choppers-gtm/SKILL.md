# Debug Skill

Reverse engineering and dynamic analysis using industry-standard tools. For CTF, security research, malware analysis, and understanding binary behavior.

---

## Philosophy

**Understand before patching.** The goal is comprehension, not just getting past a check.

**Static + Dynamic = Complete picture.** Ghidra shows structure, Frida shows runtime.

**Cross-verify everything.** Use multiple tools to confirm findings.

---

## Commands

```
/debug                          # Overview of available tools and workflows
/debug setup [tool]             # Setup guide for specific tool
/debug ghidra [target]          # Static analysis workflow
/debug frida [target]           # Dynamic instrumentation workflow
/debug windbg [target]          # Windows debugging workflow
/debug binja [target]           # Binary Ninja workflow
/debug ctf [challenge]          # CTF-specific approach
/debug malware [sample]         # Malware analysis workflow
/debug compare [a] [b]          # Cross-tool comparison
/debug hook [function]          # Generate Frida hook template
/debug decompile [function]     # Decompilation tips
```

---

## THE TOOLS

### Ghidra (Static Analysis)

**What it is:** NSA's free reverse engineering suite. Decompiler, disassembler, scripting.

**When to use:**
- Initial triage of unknown binary
- Understanding program structure
- Finding interesting functions
- Patching binaries

**Setup:**
```bash
# macOS
brew install --cask ghidra

# Linux
wget https://github.com/NationalSecurityAgency/ghidra/releases/latest
unzip ghidra_*.zip
./ghidraRun

# Requires Java 17+
java --version
```

**Key shortcuts:**
| Key | Action |
|-----|--------|
| `G` | Go to address |
| `L` | Rename label/function |
| `T` | Change type |
| `D` | Disassemble |
| `;` | Add comment |
| `Ctrl+Shift+E` | Open decompiler |
| `X` | Show xrefs |
| `/` | Search |

**Workflow:**
1. Create new project
2. Import binary (File → Import)
3. Analyze (Yes to all, be patient)
4. Start in `main` or entry point
5. Rename functions as you understand them
6. Follow cross-references to understand flow

**Ghidra Python scripting:**
```python
# List all functions
from ghidra.program.model.listing import Function
fm = currentProgram.getFunctionManager()
for func in fm.getFunctions(True):
    print(f"{func.getName()} @ {func.getEntryPoint()}")

# Find strings containing "password"
from ghidra.program.util import DefinedDataIterator
for data in DefinedDataIterator.definedStrings(currentProgram):
    if "password" in str(data.getValue()).lower():
        print(f"{data.getAddress()}: {data.getValue()}")
```

---

### Frida (Dynamic Instrumentation)

**What it is:** Dynamic instrumentation toolkit. Hook functions, trace calls, modify behavior at runtime.

**When to use:**
- Runtime behavior analysis
- Bypassing checks
- Tracing function calls
- Understanding crypto/encoding
- Mobile app analysis (iOS/Android)

**Setup:**
```bash
# Install Frida
pip install frida-tools

# For iOS/Android
# Device needs frida-server running
frida-ps -U  # List processes on USB device
```

**Basic hooks:**
```javascript
// Hook a function and log arguments
Interceptor.attach(Module.findExportByName(null, "strcmp"), {
    onEnter: function(args) {
        console.log("strcmp called:");
        console.log("  arg0: " + Memory.readUtf8String(args[0]));
        console.log("  arg1: " + Memory.readUtf8String(args[1]));
    },
    onLeave: function(retval) {
        console.log("  return: " + retval);
    }
});

// Hook by address (Ghidra tells you the address)
var baseAddr = Module.findBaseAddress("target");
var funcAddr = baseAddr.add(0x1234);  // offset from Ghidra

Interceptor.attach(funcAddr, {
    onEnter: function(args) {
        console.log("Custom function called");
        console.log("  arg0: " + args[0]);
        console.log("  arg1: " + args[1]);
    }
});

// Replace return value
Interceptor.attach(Module.findExportByName(null, "isLicensed"), {
    onLeave: function(retval) {
        retval.replace(1);  // Always return true
    }
});
```

**Running Frida:**
```bash
# Attach to running process
frida -p <pid> -l script.js

# Spawn and attach
frida -f ./target -l script.js --no-pause

# On device (iOS/Android)
frida -U -f com.example.app -l script.js --no-pause
```

**Common patterns:**
```javascript
// Trace all calls to a module
var module = Process.findModuleByName("libcrypto.so");
Interceptor.attach(module.base.add(0x1000), {
    onEnter: function() {
        console.log("Called from: " + Thread.backtrace(this.context, Backtracer.ACCURATE)
            .map(DebugSymbol.fromAddress).join("\n"));
    }
});

// Dump memory
var buf = Memory.readByteArray(ptr("0x12345678"), 256);
console.log(hexdump(buf, { offset: 0, length: 256, header: true, ansi: true }));

// Find pattern in memory
var pattern = "48 89 5C 24 08";
var matches = Memory.scan(module.base, module.size, pattern, {
    onMatch: function(address, size) {
        console.log("Found at: " + address);
    }
});
```

---

### WinDbg (Windows Debugging)

**What it is:** Microsoft's debugger for Windows. Kernel and user-mode debugging.

**When to use:**
- Windows binary debugging
- Crash dump analysis
- Kernel debugging
- Driver analysis

**Setup:**
```
# Install from Microsoft Store or winget
winget install Microsoft.WinDbg

# Or download from:
# https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/
```

**Key commands:**
| Command | Action |
|---------|--------|
| `g` | Go (continue) |
| `p` | Step over |
| `t` | Step into |
| `bp <addr>` | Set breakpoint |
| `bl` | List breakpoints |
| `bc *` | Clear all breakpoints |
| `k` | Stack trace |
| `r` | Show registers |
| `dd <addr>` | Display dwords |
| `db <addr>` | Display bytes |
| `da <addr>` | Display ASCII |
| `du <addr>` | Display Unicode |
| `dps <addr>` | Display with symbols |
| `lm` | List modules |
| `x module!*pattern*` | Search symbols |
| `!analyze -v` | Analyze crash |

**Workflow:**
```
# Attach to process
.attach <pid>

# Open executable
.open <path>

# Set breakpoint on function
bp kernel32!CreateFileW

# Set conditional breakpoint
bp kernel32!CreateFileW ".if (poi(esp+4)==0x12345678) {} .else {gc}"

# Log without breaking
bp kernel32!CreateFileW ".printf \"CreateFile: %mu\\n\", poi(esp+4); gc"

# Break on module load
sxe ld:target.dll
```

**Extension commands:**
```
# Load SOS for .NET
.loadby sos clr

# Dump heap
!dumpheap -stat

# Find objects
!dumpheap -type System.String

# Dump object
!dumpobj <addr>
```

---

### Binary Ninja (binja)

**What it is:** Commercial reverse engineering platform. Fast, scriptable, good UI.

**When to use:**
- When Ghidra is too slow
- Complex type recovery
- IL-based analysis
- Custom architectures

**Setup:**
```bash
# Commercial license required
# Download from: https://binary.ninja/

# Python API
pip install binaryninja
```

**Key features:**
- HLIL/MLIL/LLIL (high/medium/low level IL)
- Type propagation
- Data flow analysis
- Collaboration features

**Python API:**
```python
import binaryninja as bn

# Open binary
bv = bn.open_view("/path/to/binary")

# List functions
for func in bv.functions:
    print(f"{func.name} @ {hex(func.start)}")

# Get HLIL
for func in bv.functions:
    if func.name == "main":
        for line in func.hlil:
            print(line)

# Find strings
for string in bv.strings:
    if "password" in string.value.lower():
        print(f"{hex(string.start)}: {string.value}")

# Cross-references
func = bv.get_function_at(0x401000)
for ref in bv.get_code_refs(func.start):
    print(f"Called from: {hex(ref.address)}")
```

---

## WORKFLOWS

### CTF Binary Exploitation

```
1. File analysis
   file ./challenge
   checksec ./challenge

2. Static analysis (Ghidra)
   - Find main
   - Identify vulnerability (buffer overflow, format string, etc.)
   - Note key addresses

3. Dynamic analysis (Frida/GDB)
   - Verify assumptions
   - Find exact offsets
   - Test exploit

4. Exploit development
   - Write payload
   - Test locally
   - Adjust for remote
```

### Malware Analysis (Isolated Environment)

```
1. Initial triage
   - Hashes (md5, sha256)
   - Strings
   - Imports
   - PE/ELF structure

2. Static analysis (Ghidra)
   - Entry point behavior
   - Anti-analysis tricks
   - Config extraction
   - C2 identification

3. Dynamic analysis (isolated VM)
   - Network behavior
   - File system changes
   - Registry changes
   - Process behavior

4. Documentation
   - IOCs
   - Behavior summary
   - Detection rules
```

### Mobile App Analysis

```
1. Extract APK/IPA
   adb pull /data/app/com.example.app/base.apk
   # or use frida-ios-dump for iOS

2. Static analysis
   - jadx for Java decompilation
   - Ghidra for native libs

3. Dynamic analysis (Frida)
   - Hook SSL pinning bypass
   - Trace API calls
   - Dump runtime secrets

4. Common bypasses
   - Root/jailbreak detection
   - SSL pinning
   - Integrity checks
```

---

## CROSS-TOOL INTEGRATION

### Ghidra → Frida

```python
# Export function addresses from Ghidra
# Run as Ghidra script
fm = currentProgram.getFunctionManager()
with open("/tmp/functions.txt", "w") as f:
    for func in fm.getFunctions(True):
        f.write(f"{func.getEntryPoint()},{func.getName()}\n")
```

```javascript
// Import into Frida
var funcs = {};
// Load from file or paste
funcs["0x401000"] = "check_license";
funcs["0x401100"] = "decrypt_config";

for (var addr in funcs) {
    Interceptor.attach(ptr(addr), {
        onEnter: function(args) {
            console.log(funcs[this.context.pc] + " called");
        }
    });
}
```

### Binary Ninja → Frida

```python
# Export from binja
import binaryninja as bn
import json

bv = bn.open_view("./target")
hooks = {}

for func in bv.functions:
    if not func.name.startswith("sub_"):
        hooks[hex(func.start)] = func.name

with open("hooks.json", "w") as f:
    json.dump(hooks, f)
```

---

## QUICK REFERENCE

### File Analysis
```bash
file ./target                    # File type
strings ./target | less          # Readable strings
strings -el ./target             # Little-endian 16-bit
objdump -d ./target | less       # Disassembly
readelf -a ./target              # ELF info
nm ./target                      # Symbols
ldd ./target                     # Shared libraries
checksec ./target                # Security features (pwntools)
```

### Memory Layouts
```
x86-64 Registers:
RAX, RBX, RCX, RDX - General purpose
RSI, RDI - Source/Destination index (args 2, 1)
RSP - Stack pointer
RBP - Base pointer
RIP - Instruction pointer
R8-R15 - Additional general purpose

x86-64 Calling Convention (System V):
Args: RDI, RSI, RDX, RCX, R8, R9, then stack
Return: RAX

Windows x64:
Args: RCX, RDX, R8, R9, then stack
Return: RAX
```

### Common Vulnerability Patterns

| Pattern | Ghidra Indicator | Frida Hook |
|---------|-----------------|------------|
| Buffer overflow | `strcpy`, `gets`, `sprintf` | Hook and log sizes |
| Format string | `printf(user_input)` | Hook printf, check args |
| Integer overflow | Arithmetic before allocation | Hook malloc, trace size |
| Use-after-free | free() then dereference | Hook free/malloc, track |
| Command injection | `system()`, `exec()` | Hook and log commands |

---

## MULTI-AGENT DEBUGGING

When debugging complex issues, use multiple agents:

```
Agent 1: Static Analysis (Ghidra)
- Map program structure
- Identify key functions
- Document findings

Agent 2: Dynamic Analysis (Frida)
- Trace runtime behavior
- Hook identified functions
- Capture actual values

Agent 3: Cross-verification
- Compare static vs dynamic findings
- Identify discrepancies
- Validate hypotheses

Agent 4: Exploit/Fix Development
- Use verified findings
- Develop solution
- Test and iterate
```

---

## OUTPUT FILES

```
outputs/debug/
├── analysis/
│   └── {target}-analysis-{date}.md
├── hooks/
│   └── {target}-hooks.js
├── scripts/
│   └── {target}-ghidra.py
└── findings/
    └── {target}-findings.md
```

---

## RESOURCES

- **Ghidra:** ghidra-sre.org, ghidra.re (community)
- **Frida:** frida.re/docs
- **WinDbg:** docs.microsoft.com/windows-hardware/drivers/debugger
- **Binary Ninja:** docs.binary.ninja
- **CTF resources:** ctftime.org, pwnable.kr, exploit.education

---

*"The best debugger is a good understanding of the code."* — Unknown

*"Reverse engineering is not about finding vulnerabilities. It's about understanding systems."* — Also Unknown

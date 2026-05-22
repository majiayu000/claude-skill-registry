---
name: reverse-engineering-quick-triage
description: Fast binary analysis with string reconnaissance and static disassembly\ \ (RE Levels 1-2). Use when triaging suspicious binaries, extracting IOCs quickly,\ \ or performing initial malware analysis. Completes in \u22642 hours with automated\ \ decision gates."
allowed-tools: Read, Glob, Grep, Bash, Task, TodoWrite
---



---

## LIBRARY-FIRST PROTOCOL (MANDATORY)

**Before writing ANY code, you MUST check:**

### Step 1: Library Catalog
- Location: `.claude/library/catalog.json`
- If match >70%: REUSE or ADAPT

### Step 2: Patterns Guide
- Location: `.claude/docs/inventories/LIBRARY-PATTERNS-GUIDE.md`
- If pattern exists: FOLLOW documented approach

### Step 3: Existing Projects
- Location: `D:\Projects\*`
- If found: EXTRACT and adapt

### Decision Matrix
| Match | Action |
|-------|--------|
| Library >90% | REUSE directly |
| Library 70-90% | ADAPT minimally |
| Pattern exists | FOLLOW pattern |
| In project | EXTRACT |
| No match | BUILD (add to library after) |

---

## When to Use This Skill

Use this skill when analyzing malware samples, reverse engineering binaries for security research, conducting vulnerability assessments, extracting IOCs from suspicious files, validating software for supply chain security, or performing CTF challenges and binary exploitation research.

## When NOT to Use This Skill

Do NOT use for unauthorized reverse engineering of commercial software, analyzing binaries on production systems, reversing software without legal authorization, violating terms of service or EULAs, or analyzing malware outside isolated environments. Avoid for simple string extraction (use basic tools instead).

## Success Criteria

- All security-relevant behaviors identified (network, file, registry, process activity)
- Malicious indicators extracted with confidence scores (IOCs, C2 domains, encryption keys)
- Vulnerabilities documented with CVE mapping where applicable
- Analysis completed within sandbox environment (VM/container with snapshots)
- Findings validated through multiple analysis methods (static + dynamic + symbolic)
- Complete IOC report generated (STIX/MISP format for threat intelligence sharing)
- Zero false positives in vulnerability assessments
- Exploitation proof-of-concept created (if vulnerability research)

## Edge Cases & Challenges

- Anti-analysis techniques (debugger detection, VM detection, timing checks)
- Obfuscated or packed binaries requiring unpacking
- Multi-stage malware with encrypted payloads
- Kernel-mode rootkits requiring specialized analysis
- Symbolic execution state explosion (>10,000 paths)
- Binary analysis timeout on complex programs (>24 hours)
- False positives from legitimate software behavior
- Encrypted network traffic requiring SSL interception

## Guardrails (CRITICAL SECURITY RULES)

- NEVER execute unknown binaries on host systems (ONLY in isolated VM/sandbox)
- NEVER analyze malware without proper containment (air-gapped lab preferred)
- NEVER reverse engineer software without legal authorization
- NEVER share extracted credentials or encryption keys publicly
- NEVER bypass licensing mechanisms for unauthorized use
- ALWAYS use sandboxed environments with network monitoring
- ALWAYS take VM snapshots before executing suspicious binaries
- ALWAYS validate findings through multiple analysis methods
- ALWAYS document analysis methodology with timestamps
- ALWAYS assume binaries are malicious until proven safe
- ALWAYS use network isolation to prevent malware communication
- ALWAYS sanitize IOCs before sharing (redact internal IP addresses)

## Evidence-Based Validation

All reverse engineering findings MUST be validated through:
1. **Multi-method analysis** - Static + dynamic + symbolic execution confirm same behavior
2. **Sandbox validation** - Execute in isolated environment, capture all activity
3. **Network monitoring** - Packet capture validates network-based findings
4. **Memory forensics** - Validate runtime secrets through memory dumps
5. **Behavioral correlation** - Cross-reference with known malware signatures (YARA, ClamAV)
6. **Reproducibility** - Second analyst can replicate findings from analysis artifacts

# Reverse Engineering: Quick Triage

## What This Skill Does

Performs rapid reverse engineering triage through two progressive levels:
- **Level 1 (≤30 min)**: String reconnaissance - Extract URLs, IPs, IOCs, file paths, crypto indicators
- **Level 2 (1-2 hrs)**: Static analysis - Disassemble with Ghidra/radare2, map control flow, decompile to C

**Decision Gate**: After Level 1, automatically evaluates if Level 2 is needed or if string analysis answered the question.

**Timebox**: ≤2 hours total

---

## Prerequisites

### Required Tools
- **strings** - GNU binutils (pre-installed on most Linux/macOS)
- **file** - File type identification
- **sha256sum** - Hashing utility
- **xxd** - Hex dump utility

### Required for Level 2
- **Ghidra** - Headless analysis capability OR
- **radare2** - Alternative disassembler
- **graphviz** - For callgraph visualization (`dot` command)

### MCP Servers (Auto-Configured)
- `memory-mcp` - Store findings across sessions
- `filesystem` - Access binaries and create outputs
- `connascence-analyzer` - Analyze decompiled code quality
- `sequential-thinking` - Decision gate reasoning

---

## ⚠️ CRITICAL SECURITY WARNING

**NEVER execute unknown binaries on your host system!**

All dynamic analysis and binary execution MUST be performed in:
- **Isolated VM** (VMware/VirtualBox with snapshots enabled)
- **Docker container** with security restrictions (`--security-opt seccomp=unconfined`)
- **E2B sandbox** via sandbox-configurator skill
- **Dedicated malware analysis environment** (REMnux, FLARE VM)

**Consequences of unsafe execution:**
- Malware infection and persistent backdoors
- Data exfiltration and credential theft
- System compromise and lateral movement
- Ransomware deployment

**Safe Practices:**
- Always analyze binaries in an isolated environment
- Take VM snapshots before analysis
- Monitor network traffic during execution
- Never use your primary development machine
- Assume all unknown binaries are malicious until proven otherwise

---

## Quick Start (3 commands)

```bash
# 1. Analyze suspicious binary (fastest path)
/re:quick malware.exe

# 2. String analysis only (Level 1, ≤30 min)
/re:quick suspicious.bin --level 1

# 3. Static analysis only (Level 2, 1-2 hrs)
/re:quick crackme.exe --level 2 --output ./analysis/
```

**Auto-Decision**: Skill will ask after Level 1: "Suspicious IOCs found. Proceed to Level 2?" (Yes/No/Auto)

---

## Step-by-Step Guide

### Level 1: String Reconnaissance (≤30 minutes)

#### Step 1: Launch String Analysis

```bash
# Invoke RE-String-Analyst agent via slash command
/re:strings binary.exe --min-length 10 --output re-project/artifacts/strings.json
```

**What Happens**:
1. Computes SHA256 hash of binary
2. Checks memory-mcp for prior analysis (avoids duplicate work)
3. Extracts printable strings with adaptive min-length
4. Categorizes findings: URLs, IPs, emails, file paths, protocols, crypto indicators
5. Generates `strings.json` with categorized IOCs

**Expected Output**:
```json
{
  "binary": {"hash": "sha256:abc123...", "size": 1048576},
  "iocs": [
    "http://malicious-c2.tk/checkin",
    "192.168.100.50",
    "attacker@evil.com"
  ],
  "urls": [...],
  "file_paths": ["C:\\Windows\\System32\\malicious.dll"],
  "crypto": ["AES-256-CBC"],
  "analysis_time": "2025-11-01T10:15:00Z"
}
```

#### Step 2: Review String Findings

The skill will display:
- **IOCs Found**: 15 suspicious indicators
- **Known-Good URLs**: 42 (Microsoft, Google - likely benign)
- **Private IPs**: 5 (internal communication)
- **Crypto Usage**: AES-256, RSA-2048 detected

#### Step 3: Decision Gate

**Automated Evaluation** (via sequential-thinking MCP):
```
QUESTION: "Should we proceed to Level 2 static analysis?"
FACTORS:
- Suspicious C2 domain found (malicious-c2.tk) ✅
- Hardcoded credential strings present ✅
- Obfuscation indicators (encoded strings) ✅
- User's analytical question answered? ❌ (need deeper analysis)
DECISION: ESCALATE TO LEVEL 2
```

**User Override**:
- Type `skip` to exit after Level 1 (findings sufficient)
- Type `continue` to force Level 2 (even if not recommended)
- Type `auto` (default) to follow recommendation

---

### Level 2: Static Analysis (1-2 hours)

#### Step 1: Launch Disassembly

```bash
# Invoke RE-Disassembly-Expert agent via slash command
/re:static binary.exe --tool ghidra --decompile true --callgraph true
```

**What Happens**:
1. Detects binary architecture (x86/x64/ARM/MIPS)
2. Loads into Ghidra headless analyzer
3. Performs auto-analysis (function discovery, CFG)
4. Decompiles key functions to pseudo-C
5. Generates callgraph visualization
6. Runs connascence-analyzer on decompiled code

**Timeline**:
- Small binary (<1MB): 30-45 minutes
- Medium binary (1-10MB): 1-1.5 hours
- Large binary (>10MB): 1.5-2 hours

#### Step 2: Review Disassembly Results

**Output Structure**:
```
re-project/
├── ghidra/
│   ├── binary.gpr                 # Ghidra project
│   ├── decompiled/
│   │   ├── main.c                 # Decompiled entry point
│   │   ├── check_auth.c           # Authentication function
│   │   └── encrypt_data.c         # Crypto function
│   ├── callgraphs/
│   │   └── main-callgraph.png     # Call graph visualization
│   └── cfg/
│       └── main-cfg.dot           # Control flow graph
├── notes/
│   ├── 001-strings-l1.md          # Level 1 findings
│   └── 002-static-l2.md           # Level 2 findings
└── artifacts/
    ├── strings.json               # From Level 1
    ├── imports.txt                # External library calls
    └── suspicious-functions.txt   # Flagged vulnerabilities
```

#### Step 3: Code Quality Analysis

Automatically applies connascence-analyzer to decompiled C code:

**Detects**:
- God Objects (functions > 500 lines)
- Parameter Bombs (functions > 7 parameters)
- Deep Nesting (> 4 levels)
- Complexity Issues
- NASA Power of 10 violations

**Sample Output**:
```
CONNASCENCE VIOLATIONS:
- check_auth.c:45 - God Object (723 lines)
- encrypt_data.c:12 - Parameter Bomb (11 parameters)
- network_handler.c:89 - Deep Nesting (6 levels)
```

#### Step 4: Store Findings in Memory

```javascript
// Automatically stored by RE-Disassembly-Expert agent
mcp__memory-mcp__memory_store({
  content: {
    binary_hash: "sha256:abc123...",
    level_completed: 2,
    entry_point: "0x401000",
    critical_functions: [
      {name: "check_auth", address: "0x401234", decompiled: "check_auth.c"},
      {name: "encrypt_data", address: "0x401567", decompiled: "encrypt_data.c"}
    ],
    vulnerabilities: [
      {type: "buffer_overflow", function: "read_input", severity: "HIGH"},
      {type: "format_string", function: "log_message", severity: "MEDIUM"}
    ],
    callgraph: "callgraphs/main-callgraph.png",
    connascence_violations: 12
  },
  metadata: {
    agent: "RE-Disassembly-Expert",
    category: "reverse-engineering",
    intent: "static-analysis",
    layer: "long_term",
    project: `binary-analysis-${date}`,
    keywords: ["disassembly", "decompilation", "ghidra", "static"],
    re_level: 2,
    binary_hash: "sha256:abc123..."
  }
})
```

---

## Advanced Options

### Custom String Extraction

```bash
# Extract shorter strings for small binaries
/re:strings tiny-binary.exe --min-length 4

# IOCs only (skip non-IOC strings)
/re:strings malware.bin --ioc-only

# Unicode strings only
/re:strings international-app.exe --encoding unicode
```

### Custom Disassembly Tools

```bash
# Use radare2 instead of Ghidra (faster, less accurate)
/re:static binary.exe --tool radare2

# Use objdump (very fast, no decompilation)
/re:static binary.exe --tool objdump --decompile false

# Focus on specific functions
/re:static binary.exe --functions main,check_password,crypto_init
```

### Batch Analysis

```bash
# Analyze multiple binaries (Level 1 only for speed)
find ./malware-samples/ -name "*.exe" | while read binary; do
  /re:quick "$binary" --level 1 --store-findings true
done

# Cross-reference findings in memory-mcp
mcp__memory-mcp__vector_search({
  query: "malicious-c2.tk",  # Search for common IOC across all samples
  limit: 100,
  filter: {category: "reverse-engineering", re_level: 1}
})
```

---

## Integration with Other Tools

### Handoff to Dynamic Analysis

If static analysis reveals interesting runtime behavior:

```bash
# After Level 2 completes, check recommendations
cat re-project/notes/002-static-l2.md

# If recommended: "Proceed to dynamic analysis"
/re:deep binary.exe --breakpoints 0x401234,0x401567
```

**Automatic Handoff**:
The skill stores handoff data in memory-mcp:
```javascript
{
  key: "re-handoff/static-to-dynamic/${binary_hash}",
  value: {
    decision: "ESCALATE_TO_LEVEL_3",
    entry_point: "0x401000",
    critical_functions: ["check_password@0x401234"],
    breakpoint_suggestions: ["0x401234", "0x401567"],
    findings: {...}
  }
}
```

### Export Findings

```bash
# Export to JSON for threat intel platform
cat re-project/artifacts/strings.json | jq '.iocs[]' > iocs-export.txt

# Export decompiled code
tar -czf decompiled-code.tar.gz re-project/ghidra/decompiled/

# Generate executive summary
cat re-project/notes/002-static-l2.md
```

---

## Troubleshooting

### Issue: "Binary already analyzed" Message

**Symptoms**: Skill exits immediately with cached results

**Cause**: SHA256 hash found in memory-mcp from prior analysis

**Solution**:
```bash
# Option 1: Use cached results (recommended if binary unchanged)
mcp__memory-mcp__vector_search({query: "sha256:abc123...", limit: 1})

# Option 2: Force re-analysis
/re:quick binary.exe --force-reanalyze true
```

### Issue: Ghidra Headless Analysis Fails

**Symptoms**: "Ghidra headless not found" or timeout errors

**Cause**: Ghidra not installed or not in PATH

**Solution**:
```bash
# Install Ghidra
wget https://github.com/NationalSecurityAgency/ghidra/releases/download/.../ghidra.zip
unzip ghidra.zip
export PATH=$PATH:/path/to/ghidra/support

# Verify installation
analyzeHeadless -help

# Alternative: Use radare2
/re:static binary.exe --tool radare2
```

### Issue: Too Many Strings (Noise)

**Symptoms**: strings.json contains 50,000+ strings, hard to analyze

**Cause**: Min string length too short for large binary

**Solution**:
```bash
# Increase min length automatically (skill does this by default)
# Or manually:
/re:strings large-binary.exe --min-length 15

# For firmware (very large)
/re:strings firmware.bin --min-length 20
```

### Issue: Decompilation Quality Poor

**Symptoms**: Decompiled C code is unreadable or incorrect

**Cause**: Heavy obfuscation, packing, or custom compiler

**Solution**:
```bash
# Step 1: Check for packing
binwalk -E binary.exe  # High entropy = likely packed

# Step 2: Unpack first (if packed)
upx -d binary.exe -o unpacked.exe

# Step 3: Re-run static analysis
/re:static unpacked.exe

# If still poor: Manual analysis needed or try different tool
/re:static binary.exe --tool ida-pro  # If IDA Pro available
```

---

## Performance Optimization

### Speed Up Level 1 (String Analysis)

```bash
# Parallel string extraction for multiple encodings
strings -n 10 -e s binary.exe > ascii.txt &
strings -n 10 -e l binary.exe > unicode.txt &
wait

# Grep in parallel
grep -oE 'http[s]?://[^\s]*' ascii.txt > urls.txt &
grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' ascii.txt > ips.txt &
wait
```

### Speed Up Level 2 (Static Analysis)

```bash
# Use radare2 for speed (sacrifice accuracy)
/re:static binary.exe --tool radare2  # 3-5x faster than Ghidra

# Skip decompilation if only need CFG
/re:static binary.exe --decompile false --callgraph true

# Analyze only critical functions (from Level 1 findings)
/re:static binary.exe --functions check_password,validate_license
```

### Memory-MCP Caching Strategy

```bash
# Store Level 1 results immediately (fast, always cacheable)
# Level 1 completes in 10-15 min, cache for 30 days

# Store Level 2 results after completion
# Level 2 completes in 1-2 hrs, cache for 30 days

# Benefit: Second analysis of same binary takes <1 second
```

---

## Agents & Commands Used

### Agents Invoked

1. **RE-String-Analyst** (Level 1)
   - Specialist: String reconnaissance and IOC extraction
   - Tools: strings, grep, regex patterns
   - Output: strings.json, IOC lists

2. **RE-Disassembly-Expert** (Level 2)
   - Specialist: Static analysis and decompilation
   - Tools: Ghidra, radare2, objdump
   - Output: Decompiled C code, callgraphs, CFG

3. **code-analyzer** (Level 2, automatic)
   - Applies connascence analysis to decompiled code
   - Detects code smells and complexity

4. **graph-analyst** (Level 2, automatic)
   - Generates callgraph and CFG visualizations

### Slash Commands

- `/re:quick <binary>` - Full Level 1+2 analysis (this skill's primary command)
- `/re:strings <binary>` - Level 1 only
- `/re:static <binary>` - Level 2 only

### MCP Servers

- **memory-mcp**: Cross-session persistence, deduplication
- **filesystem**: Binary access, output creation
- **connascence-analyzer**: Code quality analysis
- **sequential-thinking**: Decision gate logic

---

## Related Skills

- [Reverse Engineering: Deep Analysis](../reverse-engineering-deep/) - Levels 3-4 (dynamic + symbolic)
- [Reverse Engineering: Firmware](../reverse-engineering-firmware/) - Level 5 (firmware extraction)
- [Code Review Assistant](../code-review-assistant/) - Review decompiled code
- [Functionality Audit](../functionality-audit/) - Validate reverse-engineered logic

---

## Resources

### External Tools
- [Ghidra](https://ghidra-sre.org/) - NSA's reverse engineering suite
- [radare2](https://rada.re/) - Open-source disassembler
- [binwalk](https://github.com/ReFirmLabs/binwalk) - Firmware analysis
- [IDA Pro](https://hex-rays.com/ida-pro/) - Commercial disassembler

### Learning Resources
- [Practical Malware Analysis](https://nostarch.com/malware) - Book
- [Ghidra Documentation](https://ghidra-sre.org/CheatSheet.html) - Cheat sheet
- [radare2 Book](https://book.rada.re/) - Complete guide

### Community
- [r/ReverseEngineering](https://reddit.com/r/ReverseEngineering) - Subreddit
- [Reverse Engineering Stack Exchange](https://reverseengineering.stackexchange.com/)

---

**Created**: 2025-11-01
**RE Levels**: 1-2 (String Reconnaissance + Static Analysis)
**Timebox**: ≤2 hours
**Agents**: RE-String-Analyst, RE-Disassembly-Expert
**Category**: Security, Malware Analysis, Binary Analysis
**Difficulty**: Intermediate
---

## Core Principles

Reverse Engineering: Quick Triage operates on 3 fundamental principles:

### Principle 1: Low-Hanging Fruit First
80% of malware behavior is revealed through strings and static analysis without execution.

In practice:
- Extract URLs, IPs, file paths, and crypto indicators from printable strings
- Identify C2 domains, hardcoded credentials, and API endpoints in minutes
- Categorize IOCs (indicators of compromise) for immediate threat intelligence
- Use SHA256 hash to check memory-mcp for prior analysis (avoid duplicate work)

### Principle 2: Decision Gate Escalation
Not every binary needs deep analysis - automated gates prevent over-analysis.

In practice:
- Level 1 (strings) completes in 10-30 minutes, answers simple triage questions
- Escalate to Level 2 (static disassembly) only when suspicious IOCs found
- Use sequential-thinking MCP to evaluate if user question is answered
- Stop analysis when findings are sufficient to avoid wasting time

### Principle 3: Decompilation for Comprehension
Disassembly is for machines, decompiled C pseudo-code is for analysts.

In practice:
- Use Ghidra headless mode to generate readable pseudo-C code
- Apply connascence analysis to detect god objects and complexity violations
- Generate callgraphs to visualize function relationships
- Focus on critical functions (auth, crypto, network) identified in Level 1

---

## Common Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Immediately running Level 2 without Level 1** | Waste 1-2 hours on disassembly when strings would have answered question | ALWAYS run Level 1 first, check decision gate before escalating |
| **Analyzing same binary multiple times** | Redundant work, wasted analysis hours, inconsistent findings | Check memory-mcp for SHA256 hash before starting analysis |
| **Using min-length=4 on large binaries** | 50,000+ strings with massive noise, impossible to analyze | Use adaptive min-length (10-15 for normal, 20+ for firmware), enable --ioc-only filter |
| **Skipping architecture detection** | Ghidra fails to disassemble, CFG incomplete, decompilation garbage | Run file command first, verify architecture before loading into Ghidra |
| **Not validating decompilation quality** | False positives from obfuscation, incorrect conclusions, wasted follow-up | Check for packing with binwalk entropy, unpack before re-analyzing |

---

## Conclusion

Reverse Engineering: Quick Triage is the first-responder skill for binary analysis - fast, focused, and decisive. By combining string reconnaissance (Level 1) with static disassembly (Level 2), this skill delivers actionable intelligence in under 2 hours, making it ideal for incident response, malware triage, and CTF challenges where speed matters.

The skill's automated decision gates ensure analysis effort matches threat severity. Simple malware with obvious C2 domains stops at Level 1, while sophisticated samples with obfuscation automatically escalate to Level 2 for deeper investigation. Integration with memory-mcp creates organizational memory - once a binary is analyzed, its findings are instantly retrievable by hash, preventing redundant analysis across teams.

Use this skill when you need rapid answers: Is this binary malicious? What C2 servers does it contact? Are there hardcoded credentials? What vulnerabilities does it exploit? The 2-hour timebox makes it suitable for high-velocity security operations where dozens of samples need daily triage. For samples requiring runtime analysis or input synthesis, the skill seamlessly hands off to Level 3-4 (reverse-engineering-deep) with pre-populated breakpoints and critical function addresses, maximizing overall analysis efficiency.
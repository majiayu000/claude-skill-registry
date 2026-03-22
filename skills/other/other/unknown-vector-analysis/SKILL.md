---
name: unknown-vector-analysis
description: >
  Analyze custom applications, scripts, and binaries that standard technique
  skills could not exploit. Performs source code review, attack surface mapping,
  CVE research, and PoC adaptation. Route here when ANY technique agent returns
  saying standard patterns do not match, the target uses a custom/unknown
  application, or no existing technique skill covers the vector. Trigger
  phrases: "standard patterns don't match", "custom script", "unknown binary",
  "no matching technique", "unrecognized application". Do NOT use for known
  vulnerability classes that have dedicated technique skills — route to those
  instead.
keywords:
  - custom application
  - unknown binary
  - CVE research
  - source code review
  - binary analysis
  - strace
  - ltrace
  - safety mechanism bypass
  - PoC adaptation
  - custom script
  - unknown vector
  - reverse engineering
  - code audit
tools:
  - python3
  - strings
  - strace
  - ltrace
  - objdump
  - file
  - ldd
  - readelf
  - WebSearch
  - WebFetch
opsec: medium
---

# Unknown Vector Analysis

You are helping a penetration tester analyze a custom application, script, or
binary that standard technique skills could not exploit. The previous agent
exhausted its methodology and returned without finding a matching pattern. Your
job is deep analysis — characterize the target artifact, map its attack surface,
research known vulnerabilities in its dependencies, and develop a working
exploit.

All testing is performed under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[unknown-vector-analysis] Activated → <artifact>` on activation.
- Save all evidence to `engagement/evidence/research/` with descriptive
  filenames (e.g., `custom-backup-script-analysis.md`,
  `cve-2025-4517-poc-adapted.py`).

Create the research evidence directory if it doesn't exist:
```bash
mkdir -p engagement/evidence/research
```

## Scope Boundary

Analyze **ONE artifact**, find **ONE exploitation vector**. If your analysis
identifies a known vulnerability class that has an existing technique skill
(e.g., "this is SQL injection", "this is a deserialization flaw"), note the
class and context in your return summary for the orchestrator to route — do NOT
load a second skill or attempt exploitation via a different skill's methodology.

**Stay in methodology.** Only use analysis techniques documented in this skill.
If you encounter a scenario requiring specialized tooling not listed here (e.g.,
IDA Pro, Ghidra for complex binary RE), note it and return.

## State Management

Call `get_state_summary()` from the state-interim MCP server to read current
engagement state. Use it to:
- Understand what was already attempted and failed
- Check current access level and method on the target
- Identify the artifact context (how was it discovered, why is it interesting)

## Exploit and Tool Transfer

Never download exploits, scripts, or tools directly to the target from the
internet. Targets may lack outbound access, and operators must review files
before execution on target.

Workflow:
1. Download/clone PoCs on the attackbox
2. Save to `engagement/evidence/research/`
3. Adapt to target context
4. Serve via `python3 -m http.server` or transfer with `scp`/`nc`/base64
5. Pull from target

Inline source code in heredocs is fine — the operator can read it in the skill.

## Web Research Integration

You have access to `WebSearch` and `WebFetch` for CVE research and PoC
discovery. Use them systematically:

**CVE/vulnerability research:**
- `WebSearch` with exact version strings: `"python 3.12.1 tarfile CVE"`,
  `"libarchive 3.6.2 vulnerability"`, `"sudo 1.9.5 exploit"`
- Search exploit databases: `"<software> <version> exploit-db"`,
  `"<software> <version> github PoC"`
- Search for known bypass techniques: `"<mechanism> bypass <language>"`

**PoC retrieval:**
- `WebFetch` to retrieve PoC source code from GitHub, exploit-db, or
  security advisories
- **Always save the original PoC** to `engagement/evidence/research/` before
  modifying — preserve the source URL in a comment at the top
- Document the source URL in your return summary

**Research discipline:**
- Start with the most specific query (exact version + software name)
- Broaden only if specific queries return nothing
- Don't spend more than 3 search rounds on a single hypothesis — move to
  the next analysis track

## Prerequisites

- **Shell access**: Interactive shell on the target host (reverse shell or SSH)
  where the artifact resides. Limited shells (web shell, blind command injection)
  are insufficient for deep analysis.
- **Artifact location**: The orchestrator must provide the path to the custom
  application, script, or binary on the target.
- **Context from previous agent**: What was already attempted and why it failed
  (the orchestrator passes this from the blocked technique agent's return).
- **Tools on attackbox**: python3, file, strings. For binary analysis: strace,
  ltrace, objdump, readelf, ldd. These are standard on most Linux attackboxes.

## Methodology

### Step 1: Characterize the Artifact

Determine what you're working with:

**For scripts (readable source):**
```bash
file <artifact>
head -1 <artifact>   # shebang line
cat <artifact>        # read full source
```
Identify: language, runtime version, libraries/imports, total LOC.

**For compiled binaries:**
```bash
file <artifact>
ldd <artifact>        # shared libraries
strings <artifact> | head -100   # embedded strings
readelf -h <artifact>  # ELF header (architecture, type)
```
Identify: language/compiler, linked libraries, architecture, static vs dynamic.

**For services/daemons:**
```bash
ps aux | grep <service>
cat /proc/<pid>/cmdline | tr '\0' ' '
ls -la /proc/<pid>/exe
cat /proc/<pid>/environ | tr '\0' '\n'   # environment variables
```

Record your characterization before proceeding.

### Step 2: Map Attack Surface

Identify all user-controlled inputs and security-sensitive operations:

**User-controlled inputs:**
- Command-line arguments (`sys.argv`, `$1`, `argc/argv`)
- Environment variables (`os.environ`, `getenv()`)
- File contents (config files, input files, stdin)
- Network input (sockets, HTTP parameters)

**Security-sensitive operations** (look for these patterns):
- **File I/O**: open/read/write, path construction, symlink following
- **Archive extraction**: tarfile, zipfile, libarchive (path traversal)
- **Deserialization**: pickle, yaml.load, unserialize, JSON with type hints
- **Command execution**: os.system, subprocess, exec, eval, backticks
- **SQL queries**: string concatenation with user input
- **Privilege transitions**: setuid, setgid, capabilities, sudo context

**Trust boundaries:**
- Where does user input enter the program?
- Where does privileged operation occur?
- What validation sits between them?

Map the data flow from each input to each sensitive operation.

### Step 3: Identify Safety Mechanisms

Document every validation, sanitization, or access control:

- Input validation (regex, allowlist, type checking)
- Path sanitization (realpath, basename, chroot)
- Sandboxing (seccomp, AppArmor, SELinux, chroot)
- Privilege dropping (setuid/setgid after initialization)

For each mechanism, document:
1. **What it protects** — which attack vector it prevents
2. **What it doesn't protect** — gaps, edge cases, assumptions
3. **Implementation quality** — is the check correct? Race conditions?

### Step 4: Research Bypasses

Pursue two parallel tracks:

**Track A — Library/interpreter CVEs:**
1. Extract exact versions of the runtime and key libraries:
   ```bash
   python3 --version
   pip show <library>
   dpkg -l | grep <library>
   rpm -qa | grep <library>
   ```
2. Search for known CVEs:
   ```
   WebSearch("<library> <version> CVE")
   WebSearch("<library> <version> security advisory")
   ```
3. Check if the artifact's usage pattern triggers the vulnerability

**Track B — Logic bypasses:**
- **Race conditions / TOCTOU**: check-then-use with predictable paths
- **Symlink attacks**: temporary file creation, archive extraction
- **Path traversal**: `../` in filenames, archive entries, URL paths
- **Encoding bypasses**: URL encoding, Unicode normalization, null bytes
- **Type confusion**: unexpected types in dynamic languages
- **Integer overflow**: size/length calculations in C/C++
- **Environment manipulation**: `PATH`, `LD_PRELOAD`, `PYTHONPATH`,
  `LD_LIBRARY_PATH`

### Step 5: PoC Discovery and Adaptation

When you've identified a likely vulnerability:

1. **Search for existing PoCs:**
   ```
   WebSearch("<CVE-ID> PoC github")
   WebSearch("<CVE-ID> exploit proof of concept")
   WebSearch("<vulnerability-type> <software> exploit")
   ```

2. **Retrieve and save:**
   ```
   WebFetch("<PoC-URL>")
   ```
   Save the original to `engagement/evidence/research/` with source URL.

3. **Adapt to target context:**
   - Adjust paths, filenames, and parameters for the target environment
   - Modify payload to match the exploitation goal (shell, file read, privesc)
   - Add comments explaining each adaptation
   - Save the adapted version alongside the original

4. **If no existing PoC:**
   - Write a minimal exploit based on your analysis
   - Comment every step explaining the vulnerability mechanics
   - Save to `engagement/evidence/research/`

### Step 6: Binary Analysis (Compiled Targets Only)

Skip this step for scripts with readable source.

**Dynamic analysis:**
```bash
# Trace system calls
strace -f -e trace=file,process,network <artifact> <args> 2>&1 | tee strace-output.txt

# Trace library calls
ltrace -f <artifact> <args> 2>&1 | tee ltrace-output.txt
```

**Static analysis:**
```bash
# Disassemble key functions
objdump -d <artifact> | grep -A 50 '<main>'

# Check for dangerous functions
objdump -T <artifact> | grep -E 'system|exec|popen|gets|strcpy|sprintf'

# Security features
checksec --file=<artifact>   # if available
readelf -l <artifact> | grep -i stack
readelf -d <artifact> | grep -i relro
```

**Environment variable influence:**
- `PATH` manipulation (if the binary calls external commands without full paths)
- `LD_PRELOAD` injection (if not SUID or SUID without secure-execution)
- `LD_LIBRARY_PATH` (same constraints as LD_PRELOAD)

### Step 7: Exploitation

Once you have a viable vector:

1. **Document the root cause** — what the vulnerability is and why it exists
2. **Document the safety mechanism bypass** — what protection was circumvented
3. **Build the exploit** with clear comments
4. **Execute with evidence capture:**
   ```bash
   # Before
   id; whoami; date '+%Y-%m-%d %H:%M:%S'

   # Exploit execution (capture output)
   <exploit-command> 2>&1 | tee engagement/evidence/research/exploit-output.txt

   # After (verify impact)
   id; whoami; date '+%Y-%m-%d %H:%M:%S'
   ```
5. **Save all artifacts** to `engagement/evidence/research/`

## Troubleshooting

**No source code available and binary is stripped:**
- Focus on dynamic analysis (strace/ltrace)
- Look for environment variable influence (PATH, LD_PRELOAD)
- Check if the binary calls external commands (`strings | grep -E '/(bin|usr)'`)
- Note if full RE tools (Ghidra/IDA) would help — return with recommendation

**CVE found but no public PoC:**
- Read the advisory carefully for exploitation details
- Check the patch/commit that fixed it — the diff often reveals the vuln
- Write a minimal PoC from the advisory description

**Multiple potential vectors found:**
- Prioritize by reliability: logic bugs > race conditions > memory corruption
- Prioritize by impact: code execution > file write > file read > info disclosure
- Pursue the highest-priority vector first; note alternatives in return summary

**Exploit works locally but fails on target:**
- Check runtime version differences
- Check file permissions and SELinux/AppArmor context
- Check if the artifact runs in a different user context than expected
- Verify network/filesystem differences between local test and target

**Stall detection:** If you spend 5+ tool-calling rounds on the same analysis
track with no new information, switch tracks or return with what you have.

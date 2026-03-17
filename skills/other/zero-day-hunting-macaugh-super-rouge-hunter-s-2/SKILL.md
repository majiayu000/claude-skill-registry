---
name: Zero-Day Hunting Methodology
description: Systematic approach to discovering novel vulnerabilities through code analysis, fuzzing, and attack surface research
when_to_use: When researching software for previously unknown vulnerabilities, analyzing complex codebases for security flaws, or building vulnerability research capabilities for bug bounty or security research
version: 1.0.0
languages: c, c++, python, assembly
---

# Zero-Day Hunting Methodology

## Overview

Zero-day hunting is the systematic process of discovering previously unknown vulnerabilities in software. This requires combining multiple analysis techniques, deep understanding of common vulnerability classes, and methodical exploration of attack surfaces. Success comes from patience, persistence, and systematic methodology.

**Core principle:** Combine automated and manual analysis. Automated tools find low-hanging fruit; manual analysis finds complex logic flaws. Document everything.

## When to Use

Use this skill when:
- Researching software for novel vulnerabilities
- Building vulnerability research capability
- Participating in bug bounty programs (in-scope targets)
- Conducting security assessments of complex systems
- Academic security research

**Don't use when:**
- No authorization to test the target
- Software is outside your authorized scope
- You lack resources for responsible disclosure
- You're not prepared to handle discovered vulnerabilities responsibly

## The Five-Phase Methodology

### Phase 1: Target Selection and Reconnaissance

**Goal:** Choose promising targets and understand the attack surface.

**Target Selection Criteria:**

1. **Complexity Indicators**
   - Large codebase (more code = more bugs)
   - Heavy use of C/C++ (memory unsafety)
   - Complex parsing (file formats, protocols, data structures)
   - Privileged operations (system calls, kernel interaction)
   - Network-facing code (remote attack surface)

2. **Historical Vulnerability Indicators**
   ```bash
   # Check CVE databases
   searchsploit "target software"
   
   # Review past vulnerabilities
   # - What vulnerability classes were found?
   # - Were fixes complete or partial?
   # - Pattern of similar bugs suggests more exist
   ```

3. **Attack Surface Analysis**
   ```python
   """
   Map the attack surface:
   
   INPUT VECTORS:
   - Network protocols (HTTP, custom binary protocols)
   - File formats (images, documents, archives)
   - Command-line arguments
   - Environment variables
   - IPC mechanisms (pipes, sockets, shared memory)
   - Configuration files
   
   TRUST BOUNDARIES:
   - User input → Application
   - Application → System calls
   - Unprivileged → Privileged contexts
   - Network → Local processing
   - Untrusted data → Parser
   
   INTERESTING CODE AREAS:
   - Parsers and deserializers
   - Cryptographic implementations
   - Authentication and authorization
   - Memory management
   - Privileged operations
   """
   ```

### Phase 2: Static Analysis

**Goal:** Understand code structure and identify suspicious patterns through source code review.

**Manual Code Review:**

1. **Vulnerability Pattern Recognition**
   ```c
   // PATTERN 1: Buffer Overflow
   // Look for unsafe functions with controllable size
   char buffer[256];
   strcpy(buffer, user_input);  // ❌ No bounds check
   
   char buffer[256];
   strncpy(buffer, user_input, sizeof(buffer)-1);  // ✓ Bounds checked
   buffer[sizeof(buffer)-1] = '\0';
   
   // PATTERN 2: Integer Overflow
   size_t alloc_size = user_count * sizeof(struct item);  // ❌ Can overflow
   void *ptr = malloc(alloc_size);  // Allocates small buffer, then overflow
   
   // Better:
   if (user_count > SIZE_MAX / sizeof(struct item)) {
       return ERROR;
   }
   size_t alloc_size = user_count * sizeof(struct item);
   
   // PATTERN 3: Use After Free
   free(ptr);
   // ... more code ...
   ptr->field = value;  // ❌ Use after free
   
   // PATTERN 4: Format String
   printf(user_input);  // ❌ Format string vulnerability
   printf("%s", user_input);  // ✓ Safe
   
   // PATTERN 5: Command Injection
   char cmd[512];
   sprintf(cmd, "ping %s", user_input);  // ❌ Command injection
   system(cmd);
   
   // Better: Use execve with argument array
   
   // PATTERN 6: Path Traversal
   char filepath[256];
   sprintf(filepath, "/var/data/%s", user_filename);  // ❌ ../../../etc/passwd
   FILE *f = fopen(filepath, "r");
   
   // Better: Validate, sanitize, use realpath()
   ```

2. **Automated Static Analysis**
   ```bash
   # Semgrep - pattern-based analysis
   semgrep --config=auto /path/to/source/
   
   # Cppcheck - C/C++ static analyzer
   cppcheck --enable=all --inconclusive --std=c11 /path/to/source/
   
   # CodeQL - semantic code analysis
   codeql database create /tmp/db --language=cpp --source-root=/path/to/source/
   codeql database analyze /tmp/db codeql/cpp-queries:codeql-suites/cpp-security-and-quality.qls
   
   # Coverity, SonarQube (commercial but powerful)
   ```

3. **Data Flow Analysis**
   ```python
   """
   Trace untrusted input through the codebase:
   
   1. Identify sources (user input points)
   2. Identify sinks (dangerous operations)
   3. Trace paths from sources to sinks
   4. Check for validation/sanitization
   
   Example trace:
   [SOURCE] HTTP request parameter "filename"
     → parse_request()
     → extract_param("filename")  // No validation
     → load_file(filename)
     → fopen(filename)  // [SINK] File operation
   
   FINDING: Path traversal vulnerability
   - No validation between source and sink
   - User controls filename directly
   """
   ```

### Phase 3: Dynamic Analysis and Fuzzing

**Goal:** Trigger vulnerabilities through runtime testing and intelligent input generation.

**Fuzzing Strategies:**

1. **Coverage-Guided Fuzzing**
   ```bash
   # AFL++ (American Fuzzy Lop)
   # Compile with instrumentation
   export CC=afl-clang-fast
   export CXX=afl-clang-fast++
   ./configure
   make clean && make
   
   # Create seed corpus
   mkdir seeds
   echo "valid input 1" > seeds/seed1.txt
   echo "another valid input" > seeds/seed2.txt
   
   # Run fuzzer
   afl-fuzz -i seeds -o findings -m none -- ./target @@
   
   # Monitor for crashes
   # Triage crashes: unique, exploitable, duplicate?
   ```

2. **Protocol Fuzzing**
   ```python
   # Boofuzz - network protocol fuzzer
   from boofuzz import *
   
   def main():
       session = Session(
           target=Target(
               connection=SocketConnection("target.com", 8080, proto='tcp')
           )
       )
       
       # Define protocol structure
       s_initialize("HTTP_REQUEST")
       s_static("GET ")
       s_string("/", name="path", fuzzable=True)
       s_static(" HTTP/1.1\r\n")
       s_static("Host: ")
       s_string("target.com", name="host", fuzzable=True)
       s_static("\r\n\r\n")
       
       session.connect(s_get("HTTP_REQUEST"))
       session.fuzz()
   
   if __name__ == "__main__":
       main()
   ```

3. **Structured Fuzzing**
   ```bash
   # For file formats, use structure-aware fuzzers
   
   # Honggfuzz with dictionaries
   honggfuzz -i input_corpus/ -o output/ -- ./target_binary ___FILE___
   
   # Libfuzzer for in-process fuzzing
   # Compile with -fsanitize=fuzzer
   clang++ -fsanitize=fuzzer,address target_fuzzer.cpp -o fuzzer
   ./fuzzer corpus/ -max_len=1024
   ```

4. **Sanitizer Integration**
   ```bash
   # AddressSanitizer (ASan) - memory errors
   export CFLAGS="-fsanitize=address -g"
   export CXXFLAGS="-fsanitize=address -g"
   make clean && make
   
   # UndefinedBehaviorSanitizer (UBSan)
   export CFLAGS="-fsanitize=undefined -g"
   
   # MemorySanitizer (MSan) - uninitialized memory
   export CFLAGS="-fsanitize=memory -g"
   
   # Run tests or fuzzer with sanitizers
   # They will detect and report issues
   ```

### Phase 4: Vulnerability Validation

**Goal:** Confirm discovered issues are real vulnerabilities, not false positives.

**Validation Steps:**

1. **Reproduce the Bug**
   ```python
   #!/usr/bin/env python3
   # reproduce_crash.py
   
   import subprocess
   
   # Minimal test case that triggers the bug
   malicious_input = b"A" * 1000  # From fuzzer crash
   
   # Reproduce
   with open("crash_input.bin", "wb") as f:
       f.write(malicious_input)
   
   # Run target
   result = subprocess.run(
       ["./target", "crash_input.bin"],
       capture_output=True,
       timeout=5
   )
   
   if result.returncode < 0:
       print(f"[+] Crashed with signal {-result.returncode}")
       print(f"[*] stderr: {result.stderr.decode()}")
   ```

2. **Minimize Test Case**
   ```bash
   # AFL test case minimization
   afl-tmin -i crash_sample -o minimized_crash -- ./target @@
   
   # Manual minimization
   # - Remove bytes while maintaining crash
   # - Identify minimal triggering input
   # - Understand what parts of input matter
   ```

3. **Root Cause Analysis with Debugger**
   ```bash
   # GDB with ASAN/UBSAN reports
   gdb ./target
   (gdb) run crash_input.bin
   
   # When crash occurs:
   (gdb) bt  # Backtrace
   (gdb) info registers
   (gdb) x/100x $rsp  # Examine stack
   
   # Identify:
   # - Type of vulnerability (overflow, UAF, etc.)
   # - Root cause (specific code location)
   # - Exploitability (can attacker control execution?)
   ```

4. **Exploitability Assessment**
   ```python
   """
   Severity Classification:
   
   CRITICAL:
   - Remote Code Execution (RCE)
   - Authentication bypass in privileged service
   - SQL injection in sensitive database
   
   HIGH:
   - Local privilege escalation
   - Information disclosure (passwords, keys)
   - Denial of Service in critical service
   
   MEDIUM:
   - XSS, CSRF in web applications
   - DoS in non-critical service
   - Information disclosure (non-sensitive)
   
   LOW:
   - Minor information leaks
   - DoS requiring local access
   - Theoretical issues with no practical exploit
   
   Exploitability Factors:
   - Can attacker trigger remotely?
   - Does attacker control any registers/memory?
   - Are mitigations (ASLR, NX, etc.) bypassable?
   - What privileges does vulnerable process have?
   """
   ```

### Phase 5: Proof of Concept and Disclosure

**Goal:** Create demonstrable PoC and follow responsible disclosure process.

**PoC Development:**

1. **Create Proof of Concept**
   ```python
   #!/usr/bin/env python3
   """
   Proof of Concept: Buffer Overflow in parse_header()
   
   Target: Example HTTP Server v2.1.0
   Type: Stack-based buffer overflow
   Impact: Remote Code Execution
   
   This PoC demonstrates the vulnerability by crashing the server.
   For responsible disclosure, does not include exploit code.
   """
   
   import socket
   import sys
   
   def create_poc():
       # Trigger vulnerability without exploitation
       payload = b"A" * 300  # Exceeds buffer, causes crash
       
       request = b"GET / HTTP/1.1\r\n"
       request += b"Host: " + payload + b"\r\n"
       request += b"\r\n"
       
       return request
   
   def main():
       if len(sys.argv) != 3:
           print(f"Usage: {sys.argv[0]} <target_ip> <target_port>")
           sys.exit(1)
       
       target_ip = sys.argv[1]
       target_port = int(sys.argv[2])
       
       print(f"[*] Sending PoC to {target_ip}:{target_port}")
       
       try:
           s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           s.connect((target_ip, target_port))
           s.send(create_poc())
           s.close()
           print("[+] PoC sent. Check if target crashed.")
       except Exception as e:
           print(f"[-] Error: {e}")
   
   if __name__ == "__main__":
       main()
   ```

2. **Document the Vulnerability**
   ```markdown
   # Vulnerability Report: Buffer Overflow in Example HTTP Server
   
   ## Summary
   A stack-based buffer overflow exists in the parse_header() function
   of Example HTTP Server versions 2.0.0 through 2.1.0, allowing remote
   attackers to crash the service or potentially execute arbitrary code.
   
   ## Vulnerability Details
   - **Type**: Stack-based buffer overflow (CWE-121)
   - **Affected Versions**: 2.0.0 - 2.1.0
   - **Fixed Version**: Not yet fixed
   - **CVSS Score**: 9.8 (Critical)
   - **Attack Vector**: Network (Remote)
   - **Authentication**: None required
   
   ## Technical Description
   The vulnerability exists in `src/http_parser.c` at line 234 in the
   `parse_header()` function. The function uses `strcpy()` to copy the
   HTTP Host header into a fixed 256-byte stack buffer without bounds
   checking:
   
   ```c
   void parse_header(char *header) {
       char buffer[256];
       strcpy(buffer, header);  // Vulnerable line
       // ... rest of function
   }
   ```
   
   An attacker can send an HTTP request with a Host header exceeding
   256 bytes, causing a buffer overflow that overwrites the return
   address on the stack.
   
   ## Impact
   - **Remote Code Execution**: Attacker can gain complete control
   - **Denial of Service**: Service crashes on malformed input
   - **Privilege Escalation**: If service runs as root/SYSTEM
   
   ## Proof of Concept
   See attached `poc_crash.py`. This PoC demonstrates the crash but
   does not include exploitation code.
   
   ## Steps to Reproduce
   1. Start Example HTTP Server v2.1.0
   2. Run: `python3 poc_crash.py 127.0.0.1 8080`
   3. Observe server crash with segmentation fault
   
   ## Recommended Fix
   Replace `strcpy()` with bounds-checked alternative:
   
   ```c
   void parse_header(char *header) {
       char buffer[256];
       strncpy(buffer, header, sizeof(buffer) - 1);
       buffer[sizeof(buffer) - 1] = '\0';
       // ... rest of function
   }
   ```
   
   ## Timeline
   - YYYY-MM-DD: Vulnerability discovered
   - YYYY-MM-DD: Vendor notified
   - YYYY-MM-DD+90: Public disclosure (if not fixed)
   
   ## Credits
   Discovered by: [Your Name]
   Contact: [your.email@example.com]
   ```

**Responsible Disclosure Process:**

1. **Initial Contact**
   ```
   Subject: Security Vulnerability Report - Example HTTP Server
   
   Dear Security Team,
   
   I have discovered a security vulnerability in Example HTTP Server
   that could allow remote code execution. I would like to report this
   through your responsible disclosure program.
   
   Please confirm receipt of this email and provide instructions for
   submitting the detailed vulnerability report.
   
   Thank you,
   [Your Name]
   ```

2. **Follow Timeline**
   - Day 0: Report to vendor
   - Day 7: Follow up if no response
   - Day 14: Follow up again, consider alternate contacts
   - Day 30: Check on status, patch development
   - Day 90: Standard public disclosure timeline
   - Coordinate: Vendor may request extension

3. **Public Disclosure**
   - Wait for vendor patch (or 90 days)
   - Publish advisory with CVE if assigned
   - Share PoC (non-weaponized)
   - Update bug bounty platform if applicable

## Specialized Techniques

**1. Differential Testing**
```python
# Compare behavior of different implementations
# Inconsistencies may indicate bugs

def test_parsers():
    test_inputs = generate_edge_cases()
    
    for input_data in test_inputs:
        result_a = parser_implementation_a(input_data)
        result_b = parser_implementation_b(input_data)
        
        if result_a != result_b:
            print(f"Inconsistency found: {input_data}")
            # Investigate which is correct
```

**2. Symbolic Execution**
```bash
# Use angr or other symbolic execution tools
# to explore program paths

python3 -c '
import angr
project = angr.Project("./target")
state = project.factory.entry_state()
simgr = project.factory.simulation_manager(state)
simgr.explore(find=0x401234, avoid=0x401500)
if simgr.found:
    print("Found path:", simgr.found[0].posix.dumps(0))
'
```

**3. Kernel Vulnerability Research**
```bash
# Requires deep knowledge, use with caution

# syzkaller - kernel fuzzer
git clone https://github.com/google/syzkaller
# Configure for your kernel
# Run fuzzer
./bin/syz-manager -config my.cfg

# Analyze crashes, develop exploits
# Kernel vulns have high impact
```

## Tool Ecosystem

**Static Analysis:**
- Semgrep, CodeQL (pattern matching)
- Cppcheck, Clang Static Analyzer
- Coverity, SonarQube (commercial)

**Fuzzing:**
- AFL++, libFuzzer (coverage-guided)
- Honggfuzz (feedback-driven)
- Boofuzz, Peach (protocol fuzzing)

**Dynamic Analysis:**
- Valgrind (memory debugging)
- ASan, MSan, UBSan (sanitizers)
- GDB, WinDbg (debuggers)

**Binary Analysis:**
- Ghidra, IDA Pro (reverse engineering)
- Binary Ninja (analysis platform)
- radare2 (open-source RE)

## Common Pitfalls

| Mistake | Impact | Solution |
|---------|--------|----------|
| Targeting wrong software | Wasted effort | Select based on complexity, exposure |
| Relying only on fuzzing | Miss logic flaws | Combine fuzzing with manual review |
| Not triaging crashes | False positives, duplicates | Analyze each crash, group similar |
| Premature disclosure | Vendor can't patch, users at risk | Follow 90-day disclosure timeline |
| Poor documentation | Can't reproduce/fix | Document thoroughly with PoC |
| Weaponizing exploits | Ethical/legal issues | Create PoCs only, not weaponized |

## Legal and Ethical Considerations

**CRITICAL - Always follow these rules:**

1. **Authorization**
   - Only research authorized targets
   - Bug bounties have clear scope
   - Open source research is generally OK
   - Closed source requires permission

2. **Responsible Disclosure**
   - Report to vendor first
   - Follow coordinated disclosure
   - Don't weaponize or release exploits publicly
   - Consider CERT/CC for coordination

3. **Handle Data Responsibly**
   - Don't access user data
   - Don't cause damage
   - Test in isolated environments

4. **Know the Law**
   - CFAA (US), Computer Misuse Act (UK)
   - Local laws on security research
   - Safe harbor provisions

## Integration with Other Skills

This skill works with:
- skills/analysis/static-vuln-analysis - Core technique
- skills/analysis/binary-analysis - For closed-source targets
- skills/exploitation/exploit-dev-workflow - Next step after discovery
- skills/documentation/* - Document findings
- skills/automation/* - Automate discovery pipelines

## Success Metrics

Successful zero-day hunting should:
- Use systematic methodology
- Discover genuine vulnerabilities
- Properly assess severity/exploitability
- Follow responsible disclosure
- Document findings thoroughly
- Contribute to software security

## References and Further Reading

- "The Art of Software Security Assessment" by Dowd, McDonald, Schuh
- "Fuzzing: Brute Force Vulnerability Discovery" by Sutton, Greene, Amini
- "A Bug Hunter's Diary" by Tobias Klein
- Google Project Zero blog
- Trail of Bits security research
- AFL and fuzzing documentation
- CVE database for learning from past vulnerabilities

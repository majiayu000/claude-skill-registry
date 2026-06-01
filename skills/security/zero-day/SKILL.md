---
name: zero-day
description: >
  · Hunt novel vulnerabilities: reversing, patch diffing, fuzzing, attack surface, PoCs. Triggers: 'zero-day', '0-day', 'vulnerability research', 'variant analysis', 'fuzz', 'exploit dev', 'CVE'. Not SAST: security-audit.
license: MIT
compatibility: "Optional: codeql, semgrep, joern, ghidra, radare2/rizin, afl++, gdb, pwntools, strace, ltrace, checksec"
metadata:
  source: iuliandita/skills
  date_added: "2026-04-03"
  effort: high
  argument_hint: "<target>"
---

# Zero-Day: Vulnerability Research & Discovery

Systematic methodology for finding novel, undisclosed vulnerabilities in source code, compiled
binaries, and live systems. This skill guides the research process from intelligence gathering
through proof-of-concept development to responsible disclosure.

This is the *discovery* skill - it finds vulnerabilities nobody has catalogued yet. For
exploiting known weaknesses on live systems, use **lockpick**. For scanning code against known
vulnerability patterns, use **security-audit**.

**Target versions**: May 2026 snapshot. Read `references/target-versions.md` before
pinning static analysis, reversing, fuzzing, or debugger tooling.

## When to use

- Hunting for undisclosed vulnerabilities in a codebase, binary, or running service
- Variant analysis after a CVE is published (finding similar bugs in related code)
- Patch diffing - analyzing what a security update fixed to find nearby issues
- Developing proof-of-concept exploits for discovered vulnerabilities
- Attack surface mapping before a focused security engagement
- Gathering threat intelligence on a target's technology stack
- Preparing responsible disclosure reports
- Bug bounty target assessment and prioritization
- Auditing your own projects for novel vulnerability classes
- Hunting for cloud-native vulnerabilities (IAM, IMDS, cross-tenant isolation, serverless)

## When NOT to use

- Scanning for known vulnerability patterns or OWASP top 10 (use **security-audit**)
- Post-exploitation privilege escalation or lateral movement (use **lockpick**)
- General code correctness review or bug finding (use **code-review**)
- Hardening containers, Kubernetes, or infrastructure (use **kubernetes**, **docker**, **terraform**)
- Network firewall configuration or tuning (use **firewall-appliance**)
- Without authorization from the target owner (own repos, bug bounty scope, or written permission)

## AI Self-Check

Before reporting any vulnerability or generating exploit code, verify:

- [ ] **Authorization confirmed**: own repo, active bug bounty program, or written permission
- [ ] **Scope respected**: target is within authorized boundary (specific repos, domains, IPs)
- [ ] **Novel finding**: verified this isn't already a known CVE or public advisory (cross-check Phase 0 intelligence gathering - NVD, oss-security, GitHub advisories, searchsploit)
- [ ] **Reproducible**: PoC demonstrates the issue reliably, not a theoretical concern
- [ ] **Impact assessed**: clear description of what an attacker gains (not just "crash")
- [ ] **Root cause identified**: the underlying flaw, not just the symptom
- [ ] **No collateral damage**: PoC doesn't destroy data, DoS production, or affect other users
- [ ] **Disclosure plan**: findings destined for responsible disclosure, not public dump
- [ ] **Evidence preserved**: all analysis steps documented for reproducibility
- [ ] **Complexity honest**: if exploitation requires unlikely conditions (specific config, race window, chained bugs), state that clearly - don't inflate impact
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **PoC safety reviewed**: proof code demonstrates impact without avoidable persistence, exfiltration, or wormable behavior, and stays within the authorized disclosure scope

## Performance

- Minimize repro cases before deep fuzzing so crashes triage quickly.
- Deduplicate crashes by stack, root cause, and patch reachability before reporting counts.
- Use coverage and corpus metrics to guide fuzzing time instead of running blind indefinitely.

## Best Practices

- Capture exact versions, build flags, inputs, logs, and debugger state for every candidate finding.
- Separate exploitability analysis from speculation; mark uncertainty clearly.
- Follow the target project's disclosure policy and avoid publishing operational exploit detail prematurely.

## Workflow

### Phase 0: Intelligence Gathering

Before touching code or binaries, understand what you're looking at and what the community
already knows. This phase determines where to focus.

**Advisory and feed monitoring:**

```bash
# Recent CVEs for a specific product/vendor
# NVD API (no key needed for basic queries)
curl -s "https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=TARGET_NAME&resultsPerPage=20" | python3 -m json.tool | head -100

# GitHub Security Advisories for a repo
# Adapt ecosystem param: NPM, PIP, GO, MAVEN, NUGET, RUBYGEMS, RUST, etc.
gh api graphql -f query='{ securityVulnerabilities(first:20, ecosystem:NPM, package:"TARGET") { nodes { advisory { summary severity publishedAt } vulnerableVersionRange } } }'

# Exploit-DB search
searchsploit TARGET_NAME 2>/dev/null || echo "searchsploit not installed (apt install exploitdb)"
```

**Community sources to check** (use web search):
- **oss-security mailing list** - where researchers post before/alongside CVEs
- **Full Disclosure** - uncoordinated disclosures, PoCs
- **r/netsec**, **r/ReverseEngineering**, **Hacker News** - community discussion, writeups, early signal
- **Project-specific bug trackers** - Chromium, Firefox, Linux kernel, etc.
- **Vendor security bulletins** - Microsoft Patch Tuesday, Apple security updates, etc.
- **Twitter/X** - #0day, #bugbounty, researcher accounts, vendor security teams

**What to extract:**
- Recently patched vulnerability classes (variant analysis targets)
- Components receiving security attention (hot areas)
- Researcher writeups describing methodology (technique inspiration)
- Unfixed issues in bug trackers marked as security-sensitive

**Proceed to Phase 1 when:** you have a clear picture of recent CVEs, active research, and
community attention on the target or its ecosystem. If nothing comes up, that's still useful -
it means fewer known attack patterns to build on, so original research matters more.

### Phase 1: Target Profiling

Understand the target before looking for bugs. The goal is to build a mental model of the
attack surface.

**For source code repos:**

```bash
# Language and framework breakdown
tokei . 2>/dev/null || (find . -name '*.py' -o -name '*.js' -o -name '*.ts' -o -name '*.c' \
  -o -name '*.cpp' -o -name '*.go' -o -name '*.rs' -o -name '*.java' | head -50)

# Dependencies (attack surface via supply chain)
cat package.json requirements.txt go.mod Cargo.toml pom.xml 2>/dev/null | head -80

# Entry points - where external input enters the system
grep -rn 'app\.\(get\|post\|put\|delete\|patch\|use\)\|@app\.route\|@RequestMapping\|func.*http\.Handler\|#\[.*route\]' --include='*.py' --include='*.js' --include='*.ts' --include='*.go' --include='*.rs' --include='*.java' . 2>/dev/null | head -30

# Parser/deserializer locations (high-value targets)
grep -rn 'parse\|deserialize\|unmarshal\|decode\|from_bytes\|read_struct\|unpack' --include='*.py' --include='*.c' --include='*.cpp' --include='*.go' --include='*.rs' . 2>/dev/null | head -30

# Security-sensitive operations
grep -rn 'exec\|system\|popen\|eval\|spawn\|crypto\|encrypt\|decrypt\|hash\|sign\|verify\|auth\|token\|session\|cookie\|jwt' --include='*.py' --include='*.js' --include='*.ts' --include='*.go' --include='*.rs' . 2>/dev/null | head -40

# Git history - recent security-related changes
git log --oneline --all --grep='CVE\|vuln\|security\|fix\|patch\|overflow\|inject\|bypass\|sanitize' | head -20
```

**Language-specific high-value targets** (where memory corruption hides in "safe" languages):
- **Rust**: `unsafe` blocks and FFI boundaries - memory corruption enters here
- **Go**: `import "C"` (CGo) - C code behind Go interface, plus marshaling bugs
- **Java**: `native` methods (JNI) - C/C++ code callable from managed code

**For binaries (Linux/macOS):**

```bash
# File type and architecture
file TARGET_BINARY
readelf -h TARGET_BINARY 2>/dev/null || otool -h TARGET_BINARY 2>/dev/null

# Security mitigations in place
checksec --file=TARGET_BINARY 2>/dev/null || (
  readelf -l TARGET_BINARY 2>/dev/null | grep -i 'GNU_STACK\|GNU_RELRO'
  readelf -d TARGET_BINARY 2>/dev/null | grep -i 'BIND_NOW\|FLAGS'
)

# Linked libraries (attack surface)
ldd TARGET_BINARY 2>/dev/null || otool -L TARGET_BINARY 2>/dev/null

# Strings - low-hanging fruit (URLs, paths, format strings, debug messages)
strings -n 8 TARGET_BINARY | grep -iE 'http://\|https://\|/tmp/\|/etc/\|password\|key\|token\|%s\|%d\|%x\|%n\|debug\|error\|fail' | head -40

# Symbols (if not stripped)
nm -D TARGET_BINARY 2>/dev/null | grep -i 'malloc\|free\|strcpy\|strcat\|sprintf\|gets\|system\|exec\|popen' | head -20

# Imports/exports
readelf -s TARGET_BINARY 2>/dev/null | grep -v 'UND\|LOCAL' | head -30
```

**For binaries (Windows PE):**

```powershell
# PE headers and architecture (Visual Studio tools or dumpbin)
dumpbin /headers TARGET.exe | Select-String "machine|subsystem|entry point"

# Security mitigations - use PE-bear, winchecksec, or dumpbin
winchecksec.exe TARGET.exe   # shows ASLR, DEP, CFG, ACG, CET, SEH, SafeSEH, GS
# Or manually via dumpbin:
dumpbin /headers TARGET.exe | Select-String "DLL characteristics"
# Look for: DYNAMIC_BASE (ASLR), NX_COMPAT (DEP), GUARD_CF (CFG), HIGH_ENTROPY_VA

# Imports - what DLLs and functions does it call?
dumpbin /imports TARGET.exe | Select-String "kernel32|ntdll|ws2_32|advapi32|shell32"

# Exports (for DLLs)
dumpbin /exports TARGET.dll
```

Read `references/binary-analysis.md` (Windows PE Analysis section) for Ghidra PE
import, x64dbg/WinDbg workflows, and Windows mitigation analysis.

**For live systems:**

```bash
# Open ports and services
nmap -sV -sC -p- TARGET_IP 2>/dev/null || ss -tulpn

# Service versions (version-specific vulns)
nmap -sV --version-intensity 5 -p PORTS TARGET_IP 2>/dev/null

# Web application fingerprinting
curl -sI https://TARGET/ | head -20
whatweb TARGET 2>/dev/null

# SSL/TLS analysis
testssl.sh TARGET:443 2>/dev/null || openssl s_client -connect TARGET:443 </dev/null 2>/dev/null | openssl x509 -noout -text | head -30
```

**For cloud-hosted targets**, also profile: IAM roles/policies attached to the workload,
metadata service version (IMDSv1 vs v2), managed services in use (RDS, Atlas, MSK, etc.),
cross-account trust relationships, and whether backends are directly reachable or gated
behind an API gateway. See `references/vulnerability-classes.md` section 9 for full patterns.

**Build the attack surface map:**

| Component | Entry Points | Input Format | Trust Boundary | Priority |
|-----------|-------------|--------------|----------------|----------|
| [service] | [endpoints] | [JSON/binary/etc] | [auth/unauth] | [H/M/L] |

Priority is based on: unauthenticated > authenticated, parser/deserializer > business logic,
network-facing > local-only, complex input formats > simple ones.

**Proceed to Phase 2 when:** the attack surface map has at least one high-priority entry point.
If everything is low-priority, reconsider whether this target is worth deep analysis.

### Phase 2: Vulnerability Class Selection

Based on the target profile, select which vulnerability classes to hunt. Don't search for
everything - pick 2-3 classes most likely to yield results given the target's language,
architecture, and attack surface.

Read `references/vulnerability-classes.md` for the full catalog organized by:

1. **Memory corruption** (C/C++, unsafe Rust, CGo) - buffer overflows, use-after-free, double-free, integer overflow/underflow, type confusion, uninitialized memory
2. **Injection** (all languages) - SQL, command, LDAP, template, header, CRLF, expression language
3. **Logic flaws** (all languages) - authentication bypass, authorization gaps, race conditions (TOCTOU), state machine violations, business logic abuse
4. **Deserialization** (Java, Python, PHP, .NET, Ruby) - insecure deserialization, gadget chains, type confusion via polymorphism
5. **Cryptographic** (all languages) - weak algorithms, nonce reuse, padding oracles, timing side channels, key management errors
6. **Web-specific** (web apps) - novel XSS (mXSS, DOM clobbering), SSTI, prototype pollution chains, SSRF, path traversal, cache poisoning. For XSS sinks: treat sanitizer config as a taint sink - DOMPurify `ALLOWED_TAGS`/`RETURN_DOM` misconfig, custom `sanitize()` hooks, and React innerHTML injection patterns are common bypasses; a misconfigured sanitizer is itself a sink
7. **Binary-specific** (compiled) - format string bugs, heap metadata corruption, ROP/JOP gadget availability, signal handler races
8. **Supply chain** (all ecosystems) - dependency confusion, typosquatting, compromised maintainer accounts, malicious updates
9. **Cloud-native** (AWS, GCP, Azure, managed services) - IMDS abuse, IAM confused deputy, cross-tenant isolation failures, serverless event injection, managed DB/Kafka misconfigs

**Selection heuristic:**
- C/C++ binary -> memory corruption first, always
- Web app (any language) -> logic flaws + web-specific (mXSS, SSTI, prototype pollution) + injection
- Java/Python service -> deserialization + logic flaws
- Crypto library or auth system -> cryptographic + logic flaws
- Complex parser/protocol -> memory corruption (if C/C++) or logic flaws (if managed language)
- Project with large dependency tree -> supply chain + injection
- Cloud-hosted app/service -> cloud-native + logic flaws (IAM, isolation, metadata)

**When classes tie:** prioritize by exploitability ceiling. Memory corruption and deserialization
yield RCE most reliably. Injection is next. Logic flaws require deeper understanding but produce
the most creative findings - pick these when the target has a complex state machine or multi-step
auth flow.

**Proceed to Phase 3 when:** you've selected 2-3 vulnerability classes and can articulate why
they fit this target's architecture and attack surface.

### Phase 3: Deep Analysis

This is the core of the research. Pick one attack surface from Phase 1 and one vulnerability
class from Phase 2. Go deep, not wide.

**If the first pick yields nothing:** don't switch both variables at once. Change the
vulnerability class first (same attack surface, different class). If that fails too, change
the attack surface. Switching both simultaneously means you learned nothing from the first
attempt.

**Source code - manual taint analysis:**

Read `references/taint-analysis.md` for the full methodology. Summary:

1. Identify **sources** - where external/untrusted data enters (HTTP params, file reads, env vars, IPC, database results from user-controlled queries)
2. Identify **sinks** - where data causes impact (exec, SQL, file writes, memory operations, crypto operations, response bodies)
3. Trace every path from source to sink. For each path:
   - What sanitization/validation exists?
   - Can the sanitization be bypassed? (encoding tricks, type juggling, truncation)
   - Are there paths that skip sanitization entirely? (error handlers, fallback paths, admin routes)
   - Does the data pass through a transformation that changes its security properties? (base64, URL encoding, serialization)

**Source code - variant analysis:**

When a CVE is published for a component you're reviewing:

1. Read the advisory and patch diff
2. Identify the *root cause pattern* (not just the specific instance)
3. Search the codebase for the same pattern:

```bash
# CodeQL (if available) - write a query for the pattern
codeql query run --database=TARGET_DB path/to/variant-query.ql

# Semgrep - write a custom rule
semgrep --config path/to/variant-rule.yaml .

# Joern (code property graph) - query for dataflow pattern
joern --script path/to/variant-query.sc

# Manual grep for structural similarity
grep -rn 'PATTERN' --include='*.EXT' . | head -30
```

4. For each match, determine if the same exploit conditions exist

**Binary analysis:**

Read `references/binary-analysis.md` for the full methodology covering:

1. **Static analysis** - Ghidra/Rizin decompilation, function identification, cross-references
2. **Patch diffing** - BinDiff/Diaphora to compare pre-patch and post-patch binaries, identify fixed functions, understand the vulnerability class
3. **Dynamic analysis** - GDB/LLDB debugging, strace/ltrace syscall tracing, input/output observation
4. **Fuzzing** - AFL++ harness writing, corpus selection, crash triage

**System analysis:**

1. Map every externally reachable service
2. Identify service versions and check for *recent patches* (recently patched = variant analysis target)
3. Examine custom/non-standard services more closely (less audited = more likely to have bugs)
4. Check for misconfigurations that *expand* attack surface (debug endpoints, unnecessary services, permissive CORS)
5. Hand off to **lockpick** if you find an exploitable vulnerability and want to demonstrate impact on the live system

**Cloud-native analysis:**

Read `references/vulnerability-classes.md` section 9 for the full catalog. Key methodology:

1. **Enumerate IAM** - map roles, policies, and trust relationships. Look for `sts:AssumeRole`
   without `ExternalId`, wildcard permissions, and dangerous combos (`iam:PassRole` + service creation)
2. **Test IMDS reachability** - from every SSRF-capable endpoint, attempt metadata access.
   Check IMDSv1 vs v2 enforcement. Even partial SSRF (no response body) can leak via DNS
3. **Probe managed service isolation** - can tenant A's credentials reach tenant B's resources?
   Test across RDS instances, Kafka topics, K8s namespaces, S3 buckets
4. **Audit serverless event sources** - Lambda/Cloud Function triggers (S3, SNS, API Gateway,
   Kafka) pass event payloads as untrusted input. Trace from event to sink like any other taint analysis
5. **Check for direct backend access** - bypass API gateways by hitting the backend service
   URL directly. Many "protected" APIs are only protected by the gateway, not the service itself

**Proceed to Phase 4 when:** you have a specific, reproducible trigger condition for a
vulnerability. "This buffer can overflow" is not enough - you need the exact input or sequence
that causes it.

### Phase 4: Proof of Concept

A vulnerability without a PoC is a theory. Build one.

**PoC requirements:**
- Triggers the vulnerability reliably (not "sometimes crashes")
- Demonstrates security impact (code execution, data leak, auth bypass - not just a crash dump)
- Minimal - smallest possible input/sequence that triggers the bug
- Self-contained - another researcher can reproduce it without your environment
- Non-destructive - doesn't delete data, DoS production, or cause lasting damage

Before investing in a full exploit, check mitigations (`checksec` / `winchecksec`). Full
RELRO + PIE + canary + NX + CFI makes RCE impractical for most targets. A controlled crash
or info leak PoC is still valuable for disclosure.

**PoC development patterns by vulnerability class:**

Read `references/exploit-patterns.md` for detailed PoC templates covering:

1. **Memory corruption** - crafted input to trigger overflow, heap spray for reliability, ROP chain for code execution
2. **Injection** - payload that demonstrates data exfiltration or command execution
3. **Logic flaw** - step-by-step request sequence that bypasses intended controls
4. **Deserialization** - crafted serialized object with gadget chain
5. **Crypto** - script that recovers key material or forges signatures
6. **SSRF/path traversal** - request that reads internal resources or sensitive files
7. **Cloud/IAM** - demonstrate credential theft via IMDS, cross-tenant access, or privilege escalation via IAM policy chain

**Testing the PoC:**
- Run against a local/lab copy of the target, never production
- Verify it works on the latest unpatched version
- Verify it fails on the patched version (if a patch exists)
- Document exact versions, configurations, and prerequisites

**Proceed to Phase 5 when:** the PoC reliably demonstrates the vulnerability on the target
version in a lab environment.

### Phase 5: Impact Assessment & Reporting

**Assess impact using CVSS 4.0 base metrics:**

| Metric | Question |
|--------|----------|
| Attack Vector | Network, adjacent, local, or physical? |
| Attack Complexity | Any special conditions needed? |
| Privileges Required | None, low, or high? |
| User Interaction | None, passive, or active? |
| Confidentiality | None, low, or high impact? |
| Integrity | None, low, or high impact? |
| Availability | None, low, or high impact? |

CVSS 4.0 also adds Subsequent System metrics (impact beyond the vulnerable component) and
Supplemental metrics (Automatable, Recovery, Provider Urgency). Include these when the
vulnerability affects systems beyond the immediate target.

Use the FIRST CVSS calculator: https://www.first.org/cvss/calculator/4.0

**Write the vulnerability report:**

```markdown
# [TITLE]: [Brief description]

## Summary
[1-2 sentences: what the vulnerability is and why it matters]

## Affected Versions
- [product] [version range]
- Confirmed on: [exact version tested]

## Root Cause
[Technical explanation of the underlying flaw]

## Attack Scenario
[Step-by-step description of how an attacker exploits this]

## Proof of Concept
[Minimal reproduction steps or script]

## Impact
- CVSS 4.0 Base Score: [score] ([vector string])
- [What an attacker gains: RCE, data leak, auth bypass, DoS, etc.]

## Suggested Fix
[Recommended remediation approach]

## Timeline
- [date] - Vulnerability discovered
- [date] - Vendor notified via [channel]
- [date] - Vendor acknowledged
- [date] - Patch released (pending)
- [date] - Public disclosure (coordinated)

## Credit
[Researcher name/handle]
```

**Responsible disclosure timeline:**
- Notify the vendor/maintainer immediately after confirming the vulnerability
- Standard disclosure window: 90 days (Google Project Zero standard)
- For actively exploited vulns: 7 days (expedited)
- If vendor is unresponsive after 90 days: disclose with full details
- Always check if the project has a `SECURITY.md` or security policy first

## Tooling Quick Reference

Read `references/tooling-quick-reference.md` for the tool catalog, install paths,
and when to reach for each tool during source, binary, or live-system analysis.

## Reference Files

- `references/vulnerability-classes.md` - full vulnerability class catalog with detection patterns, common root causes, language-specific variants, and novel web vectors (mXSS, DOM clobbering, SSTI by engine, prototype pollution gadget chains)
- `references/taint-analysis.md` - manual data flow analysis methodology for source code, with worked examples per language
- `references/binary-analysis.md` - binary reverse engineering workflow, patch diffing, fuzzing harness development, dynamic analysis
- `references/exploit-patterns.md` - proof-of-concept development templates by vulnerability class, with safety guidelines
- `references/tooling-quick-reference.md` - tool catalog with install paths and best-fit usage notes
- `references/target-versions.md` - May 2026 version snapshot for static analysis, reversing, fuzzing, and debugger tools

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** ZERO-DAY
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/zero-day/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **security-audit** - scans for *known* vulnerability patterns (OWASP, CVEs, misconfigs) using automated tools. Zero-day finds *novel* vulnerabilities through deep manual analysis. Use security-audit for breadth; use zero-day for depth. If security-audit finds something interesting, zero-day can investigate whether it's the tip of a larger iceberg.
- **lockpick** - exploits vulnerabilities on *live systems* for privilege escalation and lateral movement. Zero-day *discovers* the vulnerabilities. Use zero-day to find the bug, lockpick to demonstrate exploitation on a live target. Zero-day's system mode hands off to lockpick once a vulnerability is confirmed.
- **code-review** - finds correctness bugs (logic errors, race conditions). Zero-day finds *security-relevant* logic flaws. Overlap: a race condition is both a bug and potentially a vulnerability. Zero-day owns it when exploitability is the question.
- **networking** - configures and troubleshoots network services. Zero-day may analyze these services for vulnerabilities but doesn't configure them.

## Rules

1. **Authorization is non-negotiable.** Every target requires explicit authorization: own repos, active bug bounty programs with published scope, or written permission from the system owner. "It's open source" does not mean "I can attack their infrastructure."
2. **Responsible disclosure by default.** Findings go to the vendor/maintainer first. Follow the project's `SECURITY.md` if one exists. Standard 90-day disclosure window. Never drop 0-day publicly without giving the vendor a chance to patch.
3. **PoC must be non-destructive.** Proof of concepts demonstrate the vulnerability without causing lasting damage. No data destruction, no persistent backdoors, no denial of service against production systems.
4. **Depth over breadth.** Pick a specific attack surface and vulnerability class. Go deep. A thorough analysis of one parser beats a shallow scan of the whole codebase. Automated scanning is security-audit's job.
5. **Verify before reporting.** Every claimed vulnerability must have a working PoC or a clear, reproducible trigger condition. Theoretical vulnerabilities get noted internally, not reported externally.
6. **Document the research process.** Record what you analyzed, what you tried, and what you ruled out. Future researchers (including yourself) need this context for variant analysis.
7. **Lab before production.** All dynamic testing, fuzzing, and PoC execution happens on local copies or dedicated lab environments. Never fuzz or exploit production systems.
8. **Hand off correctly.** Once a vulnerability is confirmed and you want to demonstrate exploitation on a live authorized system, hand off to **lockpick**. Once you want to scan broadly for known patterns, hand off to **security-audit**.

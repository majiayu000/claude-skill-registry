---
name: 1password
description: >-
  Secure 1Password CLI (op) access patterns. Use when any task requires
  reading secrets, tokens, API keys, passwords, or credentials from
  1Password. Also use when another skill or workflow needs to retrieve
  a secret from a vault. Provides secure read patterns and strict rules
  to prevent secret leakage into conversation context, terminal output,
  or environment variables visible to Claude. NEVER bypass these patterns
  by running op commands directly without following the security rules below.
---

# 1Password CLI -- Secure Access Patterns

## Resolving Credentials from Private Links

When a credential is needed, ask the user for the item's **private link** (copied from 1Password: right-click item > "Copy Private Link") and the **field name(s)** to read.

A private link has the format:

```
https://start.1password.com/open/i?a=<ACCOUNT>&v=<VAULT>&i=<ITEM>&h=<DOMAIN>
```

Extract the URL parameters to construct the `op read` command:

| Parameter | Maps To                 |
|-----------|-------------------------|
| `a`       | `--account` value       |
| `v`       | vault in `op://` path   |
| `i`       | item in `op://` path    |

The `h` parameter (account domain) is informational only -- use `a` for `--account`.

The resulting command:

```sh
op read --account <a> -n "op://<v>/<i>/<field>"
```

Example -- given link `https://start.1password.com/open/i?a=ABC123&v=xyz789&i=item456&h=acme.1password.com` and field `password`:

```sh
op read --account ABC123 -n "op://xyz789/item456/password"
```

## Security Rules (mandatory, no exceptions)

1. Never echo, print, log, or assign a secret to a variable that appears in command output visible to Claude.
2. Never use `op read` in a command substitution that Claude can observe (e.g., `echo $(op read ...)`).
3. Never store secrets in environment variables set before a Bash tool call.
4. Never include secrets in conversation text, commit messages, file contents, or logs.
5. If `op read` fails, report the error category (auth, missing item, missing field) without reproducing raw output that could contain sensitive references.

## Secure Patterns

### Pattern 1: Pipe directly into a consuming command

Secret never touches a visible variable or stdout.

```sh
op read --account ACCT_ID -n "op://VAULT/ITEM/field" | some-command --token-stdin
```

### Pattern 2: Inline subshell with output suppression

Acceptable when the consuming command does not echo its arguments and output is controlled.

```sh
curl -s -o /dev/null -w '%{http_code}' \
  -H "Authorization: Bearer $(op read --account ACCT_ID -n 'op://VAULT/ITEM/field')" \
  https://api.example.com/endpoint
```

The outer command must not echo the expanded value. Use `-s` (silent) and `-o /dev/null` or redirect stdout.

### Pattern 3: Wrapper script

Wrap the entire operation in a script that reads secrets, uses them, and outputs only non-secret results.

## Anti-Patterns (never do these)

```sh
# WRONG: secret captured in variable and echoed
TOKEN=$(op read --account ACCT_ID -n "op://VAULT/ITEM/field")
echo "$TOKEN"

# WRONG: op read output displayed directly
op read --account ACCT_ID "op://VAULT/ITEM/field"

# WRONG: secret passed as visible argument
curl -H "Authorization: Bearer $VISIBLE_SECRET" ...
```

## Setting Up New Skills That Need Secrets

When creating or modifying a skill/script that requires credentials from 1Password, always ask the user for:

1. The **private link** to the 1Password item (contains account, vault, and item IDs).
2. The **field name(s)** to read (e.g., `password`, `api-key`, `token`).

Never guess or assume credential locations. Parse the private link to construct the `op://` reference as documented above.

## Error Handling

When `op read` fails (exit code != 0), diagnose by category:

- "could not get item": item or vault UUID is wrong
- "does not have a field": field name is wrong
- Authentication-related: user needs to run `eval $(op signin --account <ACCT_ID>)`

Report the failure category. Do not reproduce the full error message verbatim.

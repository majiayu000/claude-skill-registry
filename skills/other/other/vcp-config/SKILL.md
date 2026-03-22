---
name: vcp-config
description: >
  View and modify VCP configuration. Add or remove ignore entries, toggle scopes,
  manage compliance frameworks, change severity threshold, and manage exclude patterns.
  Supports both project config (.vcp/config.json) and global config (~/.vcp/config.json).
user-invocable: true
allowed-tools: Read, Write, WebFetch, AskUserQuestion
argument-hint: "<natural language command>"
---

# VCP Config

View and modify `.vcp/config.json` (project) or `~/.vcp/config.json` (global) configuration via natural language commands.

## Examples

### Project Config (default)

```
/vcp-config show me the current config
/vcp-config ignore core-architecture
/vcp-config stop ignoring core-architecture
/vcp-config ignore rule 3 from core-security
/vcp-config remove the ignore for CWE-798
/vcp-config enable database scope
/vcp-config disable web-frontend
/vcp-config add gdpr compliance
/vcp-config remove pci-dss compliance
/vcp-config set severity to high
/vcp-config exclude "migrations/**"
/vcp-config stop excluding "dist/**"
/vcp-config what standards are available
```

### Global Config

```
/vcp-config global show
/vcp-config global set standards_url <url>
/vcp-config global set debug true
/vcp-config global set debug false
/vcp-config global set default severity <level>
/vcp-config global set default scopes web-backend,database
/vcp-config global set default compliance gdpr,hipaa
/vcp-config global add default ignore <entry>
/vcp-config global remove default ignore <entry>
/vcp-config global reset
```

## Step 1: Load Config

1. If `$ARGUMENTS` starts with "global" → operate on `~/.vcp/config.json`:
   - Read `~/.vcp/config.json`. If it does not exist, stop and tell the user: "No global VCP config found. Run `/vcp-init` to create it."
   - Strip "global" from the arguments and proceed to Step 2 with the global config.

2. Otherwise → operate on `.vcp/config.json` (project config):
   - Read `.vcp/config.json` from the project root.
   - If it does not exist, stop and tell the user: "No VCP configuration found. Run `/vcp-init` to set up VCP for this project."
   - Also read `~/.vcp/config.json` (global config) for context — used by the `show` command to display the `Source` column.

3. Parse the JSON. This is the working config for all subsequent steps.

## Step 2: Parse Intent

Interpret `$ARGUMENTS` as a natural language command. Determine the **action** and **target**:

### Project Config Actions

| Action | Target | Description |
|--------|--------|-------------|
| **show** | config | Display current config with source annotations (default if no arguments) |
| **show** | standards | List available standards from the manifest |
| **add-ignore** | standard, rule, or CWE | Add entry to the `ignore` array |
| **remove-ignore** | standard, rule, or CWE | Remove entry from the `ignore` array |
| **enable-scope** | scope name | Set a scope to `true` |
| **disable-scope** | scope name | Set a scope to `false` |
| **add-compliance** | framework name | Add to the `compliance` array |
| **remove-compliance** | framework name | Remove from the `compliance` array |
| **set-severity** | severity level | Set the `severity` field |
| **add-exclude** | glob pattern | Add to the `exclude` array |
| **remove-exclude** | glob pattern | Remove from the `exclude` array |

### Global Config Actions

| Action | Target | Description |
|--------|--------|-------------|
| **show** | global config | Display global config |
| **set standards_url** | URL | Change the standards manifest URL (must start with `https://`) |
| **set debug** | true/false | Enable or disable diagnostic logging to `.vcp/vcp.log` in the project root |
| **set default severity** | level | Set `defaults.severity` |
| **set default scopes** | scope list | Set `defaults.scopes` |
| **set default compliance** | framework list | Set `defaults.compliance` |
| **add default ignore** | entry | Add entry to `defaults.ignore` |
| **remove default ignore** | entry | Remove entry from `defaults.ignore` |
| **reset** | entire global config | Delete `~/.vcp/config.json` after explicit confirmation |

If the intent is ambiguous, use AskUserQuestion to clarify. Do not guess.

If no arguments are provided, default to **show config**.

## Step 3: Validate

Before applying any change, validate:

### Ignore entries

Normalize the entry to the correct format:
- Standard ID: lowercase, hyphen-separated (e.g., `core-architecture`)
- Rule reference: `{standard-id}/rule-{N}` (e.g., `core-security/rule-3`)
- CWE pattern: `CWE-{digits}` (e.g., `CWE-798`)

The entry must match the regex: `^(CWE-\d+|[a-z][a-z0-9]*(-[a-z][a-z0-9]*)*(\/rule-\d+)?)$`

**Validate against the manifest:** Read `~/.vcp/config.json` to get `standards_url`. If the file doesn't exist, fall back to the default VCP manifest URL: `https://raw.githubusercontent.com/Z-M-Huang/vcp/main/standards/manifest.json`. Use WebFetch to fetch the root standards manifest from that URL.

The manifest `scopes` is an object where each key maps to `{ "manifest": "<full-url>", "applies": "<scope>" }`. To get the list of standard IDs, fetch each scope manifest from the full URL in the `manifest` field — each contains a `standards` array with `id` and `url` fields.

- For standard IDs: check that the `id` exists in any scope manifest's `standards` array. If not found, warn the user: "Standard '[id]' not found in the manifest. Available standards: [list ids]." Use AskUserQuestion to confirm whether to add it anyway.
- For rule references: check that the standard part exists. The rule number cannot be validated against the manifest (rules are in the standard content), so accept it if the standard exists.
- For CWE patterns: accept any `CWE-{digits}` without manifest validation (CWEs are matched by the security gate).

### Scopes

Valid values: `web-frontend`, `web-backend`, `database`, `mobile`, `desktop`, `cli`, `devops`, `agentic-ai`. Reject anything else.

### Compliance frameworks

Valid values: `gdpr`, `pci-dss`, `hipaa`. Reject anything else.

### Severity

Valid values: `critical`, `high`, `medium`, `low`. Reject anything else.

### Exclude patterns

Must be a non-empty string. No further validation needed.

### standards_url (global config)

Must start with `https://`. No further validation needed.

### Duplicates

Before adding, check if the entry already exists in the target array. If it does, tell the user: "'{entry}' is already in the [field] list." and stop.

Before removing, check if the entry exists. If not, tell the user: "'{entry}' is not in the [field] list." and stop.

## Step 4: Confirm Security-Sensitive Changes

If the action adds an ignore for any of these, **always** use AskUserQuestion to get explicit confirmation before applying:

1. **Any standard with `"security"` in its tags** (fetch manifest to check) — e.g., `core-security`, `web-backend-security`, `web-frontend-security`
2. **Any rule from a security-tagged standard** — e.g., `core-security/rule-3`
3. **Any CWE pattern** — all CWEs are security-related by definition
4. **Any compliance standard** — e.g., `compliance-gdpr`

Display the warning:
> **This will suppress security/compliance findings.** Suppressed vulnerabilities will not be detected by VCP skills or the security gate. Are you sure?

For non-security changes (scopes, severity, exclude, non-security ignores), proceed without extra confirmation.

For global config `reset`, always ask for explicit confirmation: "This will delete `~/.vcp/config.json`. All projects will need to re-run `/vcp-init`. Are you sure?"

## Step 5: Apply Change

Read the current config file, apply the change to the parsed object, and write it back using the Write tool.

Preserve all existing fields. Only modify the targeted field. Maintain JSON formatting with 2-space indentation.

### Show Config (project)

Display the current project config in a formatted table with a `Source` column showing where each value comes from:

```
### VCP Configuration

| Field | Value | Source |
|-------|-------|--------|
| **Standards URL** | https://raw.githubusercontent.com/.../manifest.json | global |
| **Plugin root** | /home/user/.claude/plugins/vcp | global |
| **Debug** | false | global |
| **Scopes** | web-frontend, web-backend | project |
| **Compliance** | gdpr | project |
| **Frameworks** | react, express, postgresql | project |
| **Severity** | high | global default |
| **Exclude** | node_modules/**, dist/**, build/** | project |
| **Ignore** | CWE-798 (global), core-arch/rule-5 (project) | merged |
```

**Source values:**
- `project` — value comes from `.vcp/config.json`
- `global` — value comes from `~/.vcp/config.json`
- `global default` — value inherited from `~/.vcp/config.json` `defaults` (project doesn't set it)
- `merged` — ignore list is a union of global defaults and project values

If `ignore` is empty, show "none". Same for `compliance`.

### Show Config (global)

Display the global config:

```
### VCP Global Configuration

| Field | Value |
|-------|-------|
| **Standards URL** | https://raw.githubusercontent.com/.../manifest.json |
| **Plugin root** | /home/user/.claude/plugins/vcp |
| **Default severity** | medium |
| **Default scopes** | web-backend, database |
| **Default compliance** | none |
| **Default ignore** | CWE-798 |
```

### Show Standards

Fetch the manifest and display all standards:

```
### Available VCP Standards

| ID | Scope | Severity | Tags | Applies |
|----|-------|----------|------|---------|
| core-security | core | critical | security, owasp, cwe | always |
| core-architecture | core | high | architecture, srp | always |
| web-frontend-security | web-frontend | critical | security, xss, csp | web-frontend |
| ... | ... | ... | ... | ... |

**Active for this project:** core-security, core-architecture, ... (based on scopes)
**Ignored:** core-architecture/rule-5
```

### Mutations

After applying any mutation:

1. Show a confirmation message:
   ```
   Updated .vcp/config.json — added "core-security/rule-3" to ignore list.
   ```

2. If the change affects which standards are loaded (scope or compliance changes), mention it:
   ```
   Updated .vcp/config.json — enabled database scope. Standards `database-encryption` and `database-schema-security` will now be checked.
   ```

3. If the change suppressed security findings, repeat the warning:
   ```
   Updated .vcp/config.json — added "CWE-798" to ignore list.
   WARNING: Hardcoded secret detection (CWE-798) is now suppressed in the security gate.
   ```

4. For global config changes, mention the scope of impact:
   ```
   Updated ~/.vcp/config.json — set standards_url to "https://github.example.com/.../manifest.json".
   All projects on this machine will use this URL (unless overridden per-project).
   ```

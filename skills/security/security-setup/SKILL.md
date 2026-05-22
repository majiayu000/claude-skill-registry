---
name: security-setup
description: Configure and manage Claude Code security protections for sensitive files, credentials, and data. Use when the user invokes /security-setup to set up or modify protections against unauthorized file access, credential exposure, or sensitive data leaks.
user-invocable: true
---

<!-- Current SECURITY_VERSION: 3 -->

# Security Setup & Management

When the user invokes `/security-setup`, configure or update Claude Code security protections. This skill is **re-runnable** — it detects whether protections are already configured and adjusts its workflow accordingly.

---

## Detect Mode

Check if `~/.claude/hooks/protect-sensitive-reads.sh` exists:
- **Not found** → First-time setup (Section 1)
- **Found** → Returning user (Section 2)

Also check if `~/.claude/hooks/protect-sensitive-writes.sh` exists. If the reads hook exists but the writes hook does not, treat as returning user (Section 2) — the upgrade path in Step 4 will add the missing writes hook.

---

## Section 1: First-Time Setup

### Step 1: Explain the Threat Model

Tell the user:

> Claude Code can read any file on your machine and run any shell command — including accessing saved passwords, API keys, email, cloud storage, and sensitive research data. This skill sets up layered protections:
>
> 1. **Hooks** — scripts that intercept Read and Bash operations, blocking access to sensitive locations
> 2. **Deny rules** — settings.json rules that block access even if a hook has a bug
> 3. **Bash scoping** — replacing the blanket `Bash(*)` permission with specific allowed commands
>
> The plugin already provides baseline protection. This setup adds **personal protections** tailored to your machine.

### Step 1b: Detect Platform

Determine the operating system and shell environment:

```bash
uname -s 2>/dev/null          # Darwin, Linux, MINGW64_NT-* (Git Bash), or fails on cmd/PowerShell
echo %OS% 2>/dev/null         # "Windows_NT" on Windows cmd/PowerShell
$PSVersionTable 2>/dev/null   # Non-empty on PowerShell
```

**Platform categories:**
- **macOS**: `uname -s` returns `Darwin`
- **Linux**: `uname -s` returns `Linux` (also check for WSL: `grep -qi "microsoft\|wsl" /proc/version 2>/dev/null`)
- **Windows (Git Bash / Cygwin)**: `uname -s` returns `MINGW*` or `CYGWIN*` — bash is available, hooks may work
- **Windows (PowerShell / cmd)**: `uname` fails or isn't available — hooks won't work, focus on deny rules

**Test hook capability on Windows:** If on Windows, test whether bash scripts can execute:
```bash
bash -c "echo hook-test" 2>/dev/null
```
If this succeeds, hooks are viable. If it fails, skip hook generation and note that deny rules are the primary protection.

Use the detected platform to select the appropriate scan paths in Step 2 and determine whether to generate hooks (Step 6).

### Step 2: Comprehensive Scan

Run discovery commands to check which sensitive locations exist on the user's machine. Use `ls -d` with `2>/dev/null` for each path. **Only scan paths relevant to the detected platform.** Organize results by category:

#### All platforms

**Credential stores & config:**
- `~/.ssh/`, `~/.aws/`, `~/.gnupg/`
- `~/.config/gh/`, `~/.config/gcloud/`, `~/.docker/`, `~/.kube/`, `~/.azure/`
- `~/.config/op/` (1Password CLI)
- `~/.netrc`, `~/.npmrc`, `~/.pypirc`, `~/.git-credentials`
- `~/.Renviron` (R environment variables, may contain API keys)

**IDE configs (may contain tokens):**
- Jupyter: `~/.jupyter/`
- IPython: `~/.ipython/`

**Scattered credential files:**
- `.env` files: `find ~ -maxdepth 3 -name ".env" -o -name ".env.*" 2>/dev/null`
- GCP service accounts: `find ~ -maxdepth 3 -name "credentials.json" -o -name "service-account*.json" 2>/dev/null`

#### macOS only

**Password managers:**
- macOS Keychain: `~/Library/Keychains/`
- 1Password: `~/Library/Application Support/1Password/`, `~/Library/Containers/com.1password.*`
- Bitwarden: `~/Library/Application Support/Bitwarden/`
- KeePassXC: `~/Library/Application Support/KeePassXC/`
- LastPass: `~/Library/Application Support/LastPass/`

**Browser profiles (saved passwords, cookies, sessions):**
- Chrome: `~/Library/Application Support/Google/Chrome/`
- Safari: `~/Library/Safari/`
- Firefox: `~/Library/Application Support/Firefox/`
- Edge: `~/Library/Application Support/Microsoft Edge/`

**Communication apps (email, messages, chat logs):**
- Apple Mail: `~/Library/Mail/`
- iMessage: `~/Library/Messages/`
- Teams: `~/Library/Application Support/Microsoft/Teams/`
- Slack: `~/Library/Application Support/Slack/`
- Zoom: `~/Library/Application Support/zoom.us/`

**Cloud storage mounts:**
- OneDrive: `~/Library/CloudStorage/OneDrive-*/`
- Google Drive: `~/Library/CloudStorage/GoogleDrive-*/`, `~/*Google Drive*`
- Dropbox: `~/Dropbox/`
- iCloud: `~/Library/Mobile Documents/`
- Box: `~/Library/CloudStorage/Box-*/`, `~/Box/`

**IDE configs:**
- VS Code: `~/Library/Application Support/Code/User/`
- Positron: `~/.positron/`

#### Linux only

**Password managers & keyrings:**
- GNOME Keyring: `~/.local/share/keyrings/`
- KDE Wallet: `~/.local/share/kwalletd/`
- 1Password: `~/.config/1Password/`
- Bitwarden: `~/.config/Bitwarden/`
- KeePassXC: `~/.config/keepassxc/`, `~/.local/share/keepassxc/`

**Browser profiles:**
- Chrome: `~/.config/google-chrome/`
- Chromium: `~/.config/chromium/`
- Firefox: `~/.mozilla/firefox/`
- Edge: `~/.config/microsoft-edge/`

**Communication apps:**
- Thunderbird: `~/.thunderbird/`
- Evolution: `~/.local/share/evolution/`
- Slack: `~/.config/Slack/`
- Teams: `~/.config/teams-for-linux/`

**Cloud storage mounts:**
- Dropbox: `~/Dropbox/`
- Check for FUSE mounts: `mount | grep fuse` (Google Drive, rclone-mounted OneDrive, etc.)

**IDE configs:**
- VS Code: `~/.config/Code/User/`
- Positron: `~/.config/Positron/`, `~/.positron/`

#### WSL only (in addition to Linux paths)

**Windows-side sensitive locations** — scan `/mnt/c/Users/*/` for:
- `AppData/Local/Google/Chrome/`
- `AppData/Local/Microsoft/Edge/`
- `AppData/Roaming/Mozilla/Firefox/`
- `AppData/Local/1Password/`
- `AppData/Roaming/keepassxc/`
- `.ssh/`, `.aws/`

Note: The Windows-side user directory is at `/mnt/c/Users/<username>/`. Use `ls /mnt/c/Users/` to find the right username (skip `Public` and `Default`).

#### Windows only (native — PowerShell, cmd, Git Bash, Cygwin)

On native Windows, `$HOME` or `%USERPROFILE%` typically points to `C:\Users\<username>`. Use `echo $HOME` or `echo %USERPROFILE%` to find the home directory, then scan:

**Credential stores:**
- `$HOME/.ssh/`, `$HOME/.aws/`, `$HOME/.gnupg/`
- `$HOME/.config/gh/`, `$HOME/.config/gcloud/`
- `$HOME/.netrc`, `$HOME/.npmrc`, `$HOME/.pypirc`, `$HOME/.git-credentials`
- `$HOME/.Renviron`

**Browser profiles (saved passwords, cookies, sessions):**
- Chrome: `$HOME/AppData/Local/Google/Chrome/User Data/`
- Firefox: `$HOME/AppData/Roaming/Mozilla/Firefox/`
- Edge: `$HOME/AppData/Local/Microsoft/Edge/User Data/`

**Password managers:**
- 1Password: `$HOME/AppData/Local/1Password/`
- KeePassXC: `$HOME/AppData/Roaming/KeePassXC/`
- Bitwarden: `$HOME/AppData/Roaming/Bitwarden/`

**Communication apps:**
- Teams: `$HOME/AppData/Roaming/Microsoft/Teams/`
- Slack: `$HOME/AppData/Roaming/Slack/`
- Zoom: `$HOME/AppData/Roaming/Zoom/`

**Cloud storage:**
- OneDrive: `$HOME/OneDrive/` or `$HOME/OneDrive - */`
- Google Drive: `G:/` or `$HOME/Google Drive/` (varies by install)
- Dropbox: `$HOME/Dropbox/`

**IDE configs:**
- VS Code: `$HOME/AppData/Roaming/Code/User/`
- Positron: `$HOME/AppData/Roaming/Positron/` (if applicable)
- Jupyter: `$HOME/.jupyter/`

**Windows Credential Manager:** Not file-based, but block `cmdkey` and `vaultcmd` commands via deny rules.

### Step 3: Present Findings

Show a categorized summary table with "Found" / "Not found" for each item. Group by risk level (Critical / High / Medium).

### Step 4: Choose Protection Mode

Use AskUserQuestion:

- **Allowlist mode (most secure)**: Block everything except directories you explicitly allow. You add project directories as needed. Best if you want maximum protection.
- **Blocklist mode (more permissive)**: Block only the sensitive directories found in the scan. Everything else is accessible. Best if you work across many directories and want less friction.

### Step 5: Configure Paths

Depending on mode choice:

**Allowlist mode:**
Ask: "Which directories should Claude be allowed to read? Your current project directory is always allowed automatically."

Suggest common patterns:
- Research/work directories
- Specific cloud storage project folders
- Shared data directories

**Blocklist mode:**
All scanned sensitive dirs are blocked by default. Ask two questions:
1. "Are there additional directories with sensitive data (student records, patient data, HR files, personal documents) that Claude should never access?"
2. "Are there specific project folders within cloud storage that Claude SHOULD be allowed to access?"

### Step 6: Generate Personal Hooks

**Skip this step on Windows if bash is not available** (detected in Step 1b). Instead, tell the user:

> Your shell doesn't support bash hooks, so we'll skip hook generation and rely on deny rules (settings.json) as your primary protection. Deny rules are evaluated by Claude Code directly and work on all platforms.

Then proceed to Step 7, which generates comprehensive deny rules.

**On macOS, Linux, or Windows with bash available:**

Read the template files from the skill's `templates/` directory:
- `templates/protect-sensitive-reads.sh`
- `templates/protect-sensitive-writes.sh`
- `templates/protect-sensitive-bash.sh`

Customize the templates:
1. Set `MODE=` to the user's choice (same mode for reads and writes)
2. Populate `ALLOWED_DIRS` or `BLOCKED_DIRS` with the user's paths — **keep reads and writes hooks in sync**
3. Add discovered cloud storage mount points to `BLOCKED_DIRS` (blocklist mode) or leave them out of `ALLOWED_DIRS` (allowlist mode)
4. Add any 1Password container paths found (e.g., `com.1password.1password-launcher`) to `ALWAYS_BLOCK_DIRS`
5. Populate `ALLOWED_PATH_EXCEPTIONS` in the bash hook with the same cloud storage project exceptions

Write the customized hooks to `~/.claude/hooks/`:
- `~/.claude/hooks/protect-sensitive-reads.sh`
- `~/.claude/hooks/protect-sensitive-writes.sh`
- `~/.claude/hooks/protect-sensitive-bash.sh`

Make them executable with `chmod +x`.

**Write security version stamp:** Read the current `SECURITY_VERSION` from `scripts/SECURITY_VERSION` in the plugin root (or use the version in the `<!-- Current SECURITY_VERSION: N -->` comment at the top of this skill as a fallback). Write the same version number to `~/.claude/hooks/SECURITY_VERSION`. This allows `project-reminders.sh` to detect when personal hooks are outdated relative to the plugin.

### Step 7: Update settings.json

Read `~/.claude/settings.json`. Make these changes:

**Add deny rules** (defense-in-depth) for critical paths found in the scan. Only add deny rules for paths that actually exist. Use the user's actual home directory path (not `$HOME`).

macOS example:
```json
"Read(/Users/username/.ssh/*)",
"Read(/Users/username/.aws/*)",
"Read(/Users/username/Library/Keychains/*)",
"Read(/Users/username/Library/Mail/*)",
"Read(/Users/username/Library/Messages/*)",
"Read(/Users/username/Library/Safari/*)",
"Read(/Users/username/Library/Application Support/1Password/*)",
"Read(/Users/username/Library/Application Support/Google/Chrome/*)"
```

Linux example:
```json
"Read(/home/username/.ssh/*)",
"Read(/home/username/.aws/*)",
"Read(/home/username/.config/google-chrome/*)",
"Read(/home/username/.mozilla/firefox/*)",
"Read(/home/username/.local/share/keyrings/*)",
"Read(/home/username/.config/1Password/*)",
"Read(/home/username/.thunderbird/*)"
```

WSL — include both Linux and Windows-side paths:
```json
"Read(/home/username/.ssh/*)",
"Read(/mnt/c/Users/winuser/.ssh/*)",
"Read(/mnt/c/Users/winuser/AppData/Local/Google/Chrome/*)"
```

**Register hooks** in the PreToolUse section (if not already registered):
```json
{ "matcher": "Read", "hooks": [{ "type": "command", "command": "~/.claude/hooks/protect-sensitive-reads.sh" }] },
{ "matcher": "Edit", "hooks": [{ "type": "command", "command": "~/.claude/hooks/protect-sensitive-writes.sh" }] },
{ "matcher": "Write", "hooks": [{ "type": "command", "command": "~/.claude/hooks/protect-sensitive-writes.sh" }] }
```
Add the bash hook to the existing Bash matcher's hooks array.

**Ask about Bash scoping**: "The current setting allows all bash commands (`Bash(*)`). Would you like to replace this with a specific allowlist of commands (more secure but you'll be prompted for unlisted commands)?"

If yes, replace `Bash(*)` with scoped commands. Collect what tools they commonly use and suggest a starting list:
```
git, conda, pip, python, Rscript, R, quarto, ls, mkdir, cp, mv, rm, chmod,
wc, diff, head, tail, sort, cut, uniq, which, type, gh, npm
```
Plus any domain-specific tools (mafft, iqtree, samtools, etc.).

### Step 8: Verify

Test that protections work:
1. Attempt to read `~/.ssh/` — should be blocked
2. Attempt to run `cat ~/.aws/credentials` — should be blocked
3. Read a file in the current project directory — should work
4. Run `git status` — should work

Report results to the user.

---

## Section 2: Returning User (Manage Existing Protections)

### Step 1: Read Current Config

Read `~/.claude/hooks/SECURITY_VERSION` (if it exists) to get the personal security version. Read `scripts/SECURITY_VERSION` from the plugin root to get the current plugin version.

Parse `~/.claude/hooks/protect-sensitive-reads.sh` to extract:
- Current `MODE` (allowlist or blocklist)
- `ALLOWED_DIRS` array contents
- `BLOCKED_DIRS` array contents
- `ALWAYS_BLOCK_DIRS` array contents

Check if `~/.claude/hooks/protect-sensitive-writes.sh` exists:
- **Found** → Parse it to extract `MODE`, `ALLOWED_DIRS`, `BLOCKED_DIRS`, `ALWAYS_BLOCK_DIRS` (should match reads hook)
- **Not found** → Flag as "writes hook missing — will be added" in the status summary

Parse `~/.claude/hooks/protect-sensitive-bash.sh` to extract:
- `BLOCKED_PATH_KEYWORDS` array contents
- `ALLOWED_PATH_EXCEPTIONS` array contents

Parse `~/.claude/settings.json` to extract:
- Deny rules
- Hook registrations (check for Edit and Write matchers — may be missing on older installs)
- Bash permission rules (scoped or `Bash(*)`)

### Step 2: Present Current Protections

Show a summary organized by:
- **Security version**: personal vN / plugin vN (show "up to date" or "outdated — update recommended")
- **Protection mode**: allowlist or blocklist
- **Hooks installed**: reads, writes, bash (flag any missing — e.g., "writes hook: **missing**")
- **Allowed directories** (allowlist mode) or **Blocked directories** (blocklist mode)
- **Always-blocked directories** (both modes)
- **Cloud storage exceptions** (paths where access is allowed within otherwise-blocked cloud storage)
- **Deny rules** in settings.json
- **Hook registrations**: Read, Edit, Write, Bash matchers (flag any missing)
- **Bash permissions**: scoped commands or `Bash(*)`

### Step 3: Ask What to Change

Use AskUserQuestion with mode-appropriate options:

**Allowlist mode options:**
- Add allowed directories
- Remove allowed directories
- Switch to blocklist mode

**Blocklist mode options:**
- Add directories to block
- Remove directories from block list
- Add cloud storage exceptions (grant access to project folders)
- Remove cloud storage exceptions
- Switch to allowlist mode

**Both modes:**
- Add Bash commands to allowlist
- Remove Bash commands from allowlist
- Re-scan for new sensitive locations (if new software was installed)

### Step 4: Apply Changes

**If writes hook is missing (upgrade path):**
Generate `~/.claude/hooks/protect-sensitive-writes.sh` from `templates/protect-sensitive-writes.sh`, copying `MODE`, `ALLOWED_DIRS`, `BLOCKED_DIRS`, and `ALWAYS_BLOCK_DIRS` from the existing reads hook so they stay in sync. Register Edit and Write matchers in settings.json if not already present. Make executable with `chmod +x`.

**For all other changes:**
Modify the relevant hook script(s) and/or settings.json. When editing hook scripts:
- Read the current file
- Use the Edit tool to modify the specific array
- **Keep reads and writes hooks in sync** — if `ALLOWED_DIRS` or `BLOCKED_DIRS` change in one, apply the same change to the other
- Preserve all other configuration

After applying changes, update `~/.claude/hooks/SECURITY_VERSION` to the current plugin version (the user just re-ran security-setup, so they're now current).

Show the user what changed (before/after for the modified arrays).

### Step 5: Verify

Run the same verification tests as first-time setup to confirm changes work.

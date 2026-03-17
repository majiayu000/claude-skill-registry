---
name: macos-admin
cluster: macos
description: "System preferences, users, disk utility, SIP, Gatekeeper, FileVault, console logs"
tags: ["macos","admin","system","security"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "macos admin system preferences disk user group sip gatekeeper"
---

## Purpose
This skill handles macOS system administration tasks, including managing preferences, users, disks, and security features like SIP, Gatekeeper, FileVault, and console logs.

## When to Use
Use this skill for automating macOS admin operations in scripts, such as configuring system settings during deployment, managing user accounts in enterprise environments, or troubleshooting security issues via logs.

## Key Capabilities
- Manage system preferences via `systemsetup` for settings like time zone or energy saver.
- Handle users and groups using `dscl` for creating, deleting, or modifying accounts.
- Perform disk operations with `diskutil` for mounting, verifying, or encrypting volumes.
- Control SIP (System Integrity Protection) with `csrutil` to enable/disable for kernel extensions.
- Manage Gatekeeper via `spctl` to assess app security policies.
- Handle FileVault encryption using `fdesetup` for status checks and enablement.
- Access console logs with `log` command for system diagnostics.

## Usage Patterns
Invoke this skill in shell scripts or Python subprocess calls, always with elevated privileges (e.g., via `sudo`). For example, wrap commands in a function that checks for admin rights first. Use environment variables for configuration, like `$ADMIN_PASSWORD` for scripts requiring authentication. Pattern: Check prerequisites (e.g., OS version with `sw_vers`), execute the command, and parse output for automation.

## Common Commands/API
Use `sudo` for most commands due to admin requirements. Here's how to accomplish key tasks:

- Create a user: `dscl . -create /Users/newuser; dscl . -create /Users/newuser UserShell /bin/bash; dscl . -create /Users/newuser RealName "New User"`
- Check SIP status: `csrutil status` (output: "System Integrity Protection: enabled")
- Enable FileVault: `sudo fdesetup enable -user username -pass $ADMIN_PASSWORD`
- Manage Gatekeeper: `spctl --assess --verbose /path/to/app` to verify app allowance
- Mount a disk: `diskutil mount disk1s1`
- View console logs: `log show --predicate 'subsystem == "com.apple.console"' --last 1h`
- Change system preference (e.g., computer name): `sudo scutil --set ComputerName NewName`

Code snippet for user creation in Python:
```python
import subprocess
subprocess.run(['sudo', 'dscl', '.', '-create', '/Users/newuser'])
subprocess.run(['sudo', 'dscl', '.', '-create', '/Users/newuser', 'RealName', 'New User'])
```

Code snippet for SIP check:
```python
import os
result = os.popen('csrutil status').read()
if 'enabled' in result:
    print("SIP is active")
```

## Integration Notes
Integrate by calling macOS CLI tools from your AI agent's code via subprocess or os.system. For scripts, ensure the agent runs with admin privileges; use `sudo` and pass credentials via env vars like `$ADMIN_PASSWORD`. Config formats: Use plist files for preferences (e.g., edit `/Library/Preferences/com.apple.loginwindow.plist` with `defaults write`). For API-like access, leverage AppleScript via `osascript`, e.g., `osascript -e 'tell application "System Preferences" to activate'`. If combining with other skills, pipe output to tools like `jq` for JSON parsing of log data.

## Error Handling
Always check command exit codes; for example, use `subprocess.run(..., check=True)` in Python to raise exceptions on failure. Common errors: Permission denied (code 1) – prompt for sudo or check `$EUID` for root status. Handle SIP-related errors by verifying status first. For disk operations, catch I/O errors with try-except blocks. Example: If `diskutil` fails, log the error and retry after user confirmation. Use `2>&1` to capture stderr in scripts, e.g., `command 2>&1 | grep error`.

## Concrete Usage Examples
1. Automate user creation for a new employee: First, check if the user exists with `dscl . -read /Users/username`, then create if not: `sudo dscl . -create /Users/newuser && sudo dscl . -passwd /Users/newuser $NEW_PASSWORD`. Use in a script to handle onboarding.
2. Secure a system by enabling FileVault: Run `sudo fdesetup status` to check current state, then if disabled, execute `sudo fdesetup enable -user admin -pass $ADMIN_PASSWORD` to encrypt the drive, ensuring data protection.

## Graph Relationships
- Related to: macos-core (for general macOS utilities), security-tools (for Gatekeeper and SIP integration), user-management (for dscl operations).
- Depends on: system-services (for console logs access).
- Conflicts with: non-macos skills due to OS-specific commands.

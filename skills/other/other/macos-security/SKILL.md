---
name: macos-security
cluster: macos
description: "XProtect, MRT, TCC privacy permissions, quarantine, code signing validation, security audit"
tags: ["security","macos","hardening","privacy"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "macos security hardening xprotect privacy tcc gatekeeper audit"
---

# macos-security

## Purpose
This skill enables the AI agent to manage macOS security features, including XProtect for malware detection, MRT for removal, TCC for privacy permissions, quarantine attributes, code signing validation, and security audits. Use it to harden macOS systems against threats and ensure compliance.

## When to Use
Apply this skill during system hardening routines, app deployment checks, privacy audits, or malware scans. Use it for new macOS setups, software installations, or when troubleshooting security issues like unauthorized app access or unsigned binaries.

## Key Capabilities
- Detect malware via XProtect by querying the latest definitions and scanning files.
- Run MRT to remove known threats from the system.
- Manage TCC permissions to control app access to sensitive data like camera or contacts.
- Inspect and remove quarantine flags on downloaded files to allow execution.
- Validate code signing for apps to ensure they are from trusted developers.
- Perform security audits using system logs to identify potential breaches.

## Usage Patterns
Invoke this skill in scripts for automated hardening, e.g., during VM provisioning or CI/CD pipelines for macOS apps. Use it reactively for incident response or proactively in scheduled tasks. For AI agents, call it via function wrappers that handle macOS-specific commands, ensuring elevated privileges with `sudo` where needed. Pattern: Check security status first, then apply fixes.

## Common Commands/API
Use these macOS CLI commands for security tasks. All require admin privileges; check for errors via exit codes.

- XProtect scan: Use `softwareupdate --list` to check for updates, then `xprotect scan /path/to/file` (via internal tools).
  Example snippet:
  ```
  system("softwareupdate --list");
  if (exit_code != 0) { handle_error("Update check failed"); }
  ```
- MRT removal: Run `/usr/libexec/MRTConfigData remove` to trigger malware removal.
  Example snippet:
  ```
  system("/usr/libexec/MRTConfigData remove");
  print("MRT executed; check logs for results.");
  ```
- TCC permissions: Use `tccutil reset <service> <app>` to reset or `tccutil set <service> <app> allow` to grant.
  Example: `tccutil set Camera com.example.app allow` for camera access.
- Quarantine handling: Check with `xattr -l /path/to/file` and remove via `xattr -d com.apple.quarantine /path/to/file`.
  Example snippet:
  ```
  xattr -l /path/to/file;
  if (grep("com.apple.quarantine")) { system("xattr -d com.apple.quarantine /path/to/file"); }
  ```
- Code signing validation: Run `codesign -vvv --verify --strict /path/to/app` to check signatures.
  Example: `codesign -dvvv /Applications/MyApp.app` for detailed verification.
- Security audit: Query logs with `log show --predicate 'subsystem == "com.apple.securityd"' --last 1h`.
  Config format: Use predicates in `log` command for filtering, e.g., JSON output via `--style json`.

If API keys are needed (e.g., for third-party security tools), use env vars like `$SECURITY_API_KEY` in scripts: `curl -H "Authorization: Bearer $SECURITY_API_KEY" https://api.example.com/scan`.

## Integration Notes
Integrate by wrapping commands in AI agent functions, e.g., use Python's subprocess to call `tccutil`. For automation, combine with tools like Jamf or MDM APIs. Ensure the agent runs with sufficient privileges; use `osascript` for user prompts if needed. Config files like `/etc/authorization` can be edited for TCC policies, but back them up first. Test integrations in a sandboxed macOS environment to avoid disruptions.

## Error Handling
Always check command exit codes; for example, if `codesign` returns non-zero, log the error and suggest re-signing. Parse outputs for specific strings, e.g., if `tccutil` fails with "Access denied", prompt for admin elevation. Use try-catch in scripts:
```
try {
  system("tccutil set Camera com.example.app allow");
} catch (e) {
  if (e.includes("permission")) { system("sudo -u root tccutil set Camera com.example.app allow"); }
}
```
Common errors: Permission issues (use `sudo`), file not found (verify paths), or outdated XProtect (run updates first). Log all errors to `/var/log/securityd.log` for auditing.

## Concrete Usage Examples
1. **Malware Scan and Removal**: To scan a suspicious file and remove threats:
   - First, update XProtect: `softwareupdate --install --all`.
   - Then run MRT: `system("/usr/libexec/MRTConfigData remove")`.
   - Verify: `log show --predicate 'eventMessage contains "MRT"'`.
   This ensures the system is cleaned; handle errors by checking if MRT is available.

2. **TCC Permission Management for an App**: To grant camera access to a new app:
   - Check current status: `tccutil reset Camera com.example.app`.
   - Grant permission: `tccutil set Camera com.example.app allow`.
   - Test: Run the app and confirm access.
   If errors occur, use `sudo` and log the action for auditing.

## Graph Relationships
- Related to: macos-filesystem (for handling quarantined files)
- Depends on: macos-networking (for security audits involving network logs)
- Conflicts with: none
- Used by: general-security (as a subsystem for macOS-specific hardening)

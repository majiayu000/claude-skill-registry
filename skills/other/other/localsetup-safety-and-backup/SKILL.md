---
name: localsetup-safety-and-backup
description: "Security and safety (conservative), backup management, temporary file management, firewall management. Use for destructive ops, system config changes, backups, temp files, or when adding services."
metadata:
  version: "1.1"
---

# Safety, backup, temp files, firewall

## 10. Security and safety (conservative)

- **Conservative approach:** Prioritize security and data safety over automation convenience.
- **Risk categories:** CRITICAL (data loss), HIGH (system-wide), MEDIUM (application), LOW (read-only). CRITICAL/HIGH require explicit second confirmation.
- **Warning requirements:** Simple language, list consequences, explain who/what affected. Provide options: Execute / Show manual steps / Cancel.
- **Dangerous operations:** Recursive deletes, permission changes, firewall changes, system service changes, package removal, disk operations, user/group deletion, operations on /usr, /etc, /bin (or Windows equivalents).
- **Use:** Source `lib/safety_checker.sh` and use `safe_execute_with_confirmation` for system commands.

## 11. Backup management

- **Default:** Create backups before modifying sensitive system config files. Naming: `original_filename.YYYYMMDD_HHMMSS.backup`. Location: same directory as original; hidden/read-only.
- **Large files (&gt;100MB):** Warn and ask about backup routine; user can skip.
- **User control:** User can decline backups for session; respect preference.
- **Use:** Source `lib/backup_manager.sh` and use `create_file_backup` before editing. Restore: `restore_from_backup <original_file>`.

## 9. Temporary file management

- **Platform:** Linux /tmp; macOS /tmp or $TMPDIR; Windows %TEMP% or %TMP%.
- **Cleanup:** Clean up immediately; use trap (Bash) or try/finally (PowerShell). Repo-local temp: under _localsetup/ or repo temp dir when v2 repo-local.
- **Naming:** Framework naming + descriptive name + timestamp. Use mktemp or New-TemporaryFile.

## 5a. Firewall management (for services)

- **When adding new services:** Configure firewall rules. Use `source lib/firewall_manager.sh && configure_firewall_rule "ServiceName" "PORT" "tcp" "lan"`. Default scope "lan". Validate with `validate_firewall_rule`. See [FIREWALL_MANAGEMENT.md](../../docs/FIREWALL_MANAGEMENT.md).

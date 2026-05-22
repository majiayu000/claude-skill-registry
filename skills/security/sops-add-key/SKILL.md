---
name: sops-add-key
description: >-
  Add a new machine's age public key to .sops.yaml and re-encrypt all files.
  Use for multi-machine setups. Use when user mentions "add key", "add machine",
  "sops add key", "new machine", "authorize machine", "share key",
  "add public key", "multi machine sops".
disable-model-invocation: true
---

# SOPS Add Key

Add a new machine's age public key to the project and re-encrypt all files so the new machine can decrypt them.

## Workflow

1. **Detect current state**:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/../sops-setup/scripts/detect_sops.py <project-root>
   ```

2. **Verify prerequisites**:
   - `project.sops_yaml.exists` must be true — if not, tell user to run `/devtools:sops-setup` first
   - `project.encrypted_files` should be non-empty — warn if there are no `.enc.yaml` files to re-encrypt
   - If `project.tmp_files` is non-empty, warn about stale temporary files (leftover from a failed decrypt/re-encrypt) and suggest the user delete them

3. **Audit key propagation** (if encrypted files exist):
   For each encrypted file, read its YAML and check the `sops.age` recipients list against `project.sops_yaml.authorized_keys`.
   If any authorized key is missing from any file's recipients:
   ```
   WARNING: Key age1xxx...yyy is in .sops.yaml but NOT a recipient in:
     - apps/web/.env.local.enc.yaml
     - apps/api/.env.local.enc.yaml
   These files need re-encryption before the corresponding machine can decrypt them.
   ```
   Offer to run `sops updatekeys -y <file>` for each affected file before proceeding with the new key addition.

4. **Show current authorized keys** from `project.sops_yaml.authorized_keys`:
   ```
   Currently authorized keys (N):
   1. age1abc...def (truncated)
   2. age1ghi...jkl (truncated)
   ```

5. **Use `AskUserQuestion`** — ask user to paste the new machine's age public key. Validate it starts with `age1`.

6. **Read `.sops.yaml`** and add the new key to the `age:` field in `creation_rules`. Use the `Edit` tool to append the key to the comma-separated list or multi-line block.

7. **Re-encrypt all files** using `sops updatekeys`:
   ```bash
   sops updatekeys -y <file>.enc.yaml
   ```
   For each encrypted file. The `-y` flag auto-confirms. This re-wraps only the data encryption key for the new recipient list — values and MAC are unchanged, producing a minimal diff.

   If `sops updatekeys` is not available (older sops version), fall back to decrypt + re-encrypt:
   ```bash
   sops --decrypt <file>.enc.yaml > <file>.tmp.yaml
   sops --encrypt <file>.tmp.yaml > <file>.enc.yaml
   rm <file>.tmp.yaml
   ```

   **Verify**: After re-encrypting, read each file's `sops.age` recipients block and confirm all keys from `.sops.yaml` (including the newly added key) appear as recipients. If any key is missing, warn the user that re-encryption may have failed.

8. **Summary**:
   ```
   | Action | Detail |
   |--------|--------|
   | Key added | age1xyz... (new machine) |
   | .sops.yaml | Updated (now N+1 authorized keys) |
   | Re-encrypted | .env.local.enc.yaml |
   | Re-encrypted | .env.production.enc.yaml |
   ```
   Remind user to **commit** both `.sops.yaml` and the updated `.enc.yaml` files.

## Key Rotation vs Key Addition

- **Adding a key** (`sops updatekeys`): Re-wraps the DEK for the new recipient list. Safe, minimal diff. Use for onboarding machines.
- **Rotating keys** (`sops rotate -i`): Generates a new DEK and re-encrypts every value. Use when a key is **compromised** or for periodic security hygiene.
- If the user mentions a compromised key, recommend `sops rotate -i` after removing the compromised key from `.sops.yaml`.

## Key Rules

- Validate the public key format (must start with `age1`) before modifying `.sops.yaml`
- Always show the current keys before adding a new one
- Re-encrypt ALL `.enc.yaml` files — missing any would lock out the new machine for those files
- Use `sops updatekeys` (not full decrypt/re-encrypt) for routine key additions
- After re-encryption, the new machine can clone and decrypt immediately

---
name: sops-encrypt
description: >-
  Encrypt .env files using SOPS + age. Converts dotenv to YAML format (avoids
  SOPS bug #1435), then encrypts. Auto-detects unencrypted .env files. Use when
  user mentions "encrypt env", "sops encrypt", "encrypt secrets", "encrypt .env",
  "encrypt environment", "re-encrypt", "update encrypted".
disable-model-invocation: true
---

# SOPS Encrypt

Encrypt `.env` files by converting to YAML and encrypting with SOPS + age.

**Why YAML?** SOPS dotenv store has a [known bug (#1435)](https://github.com/getsops/sops/issues/1435) that corrupts backslash and `\n` sequences. The helper script converts dotenv→YAML before encryption.

## Workflow

1. **Detect current state**:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/../sops-setup/scripts/detect_sops.py <project-root>
   ```

2. **Verify prerequisites**:
   - `tools.sops.installed` must be true — if not, tell user to run `/devtools:sops-setup`
   - `project.sops_yaml.exists` must be true — if not, tell user to run `/devtools:sops-setup`
   - `age_key.exists` must be true — if not, tell user to run `/devtools:sops-setup`

3. **Show unencrypted .env files** from `project.env_files`. If empty, report "No .env files found to encrypt" and exit.

4. **Use `AskUserQuestion`** (multiSelect: true) — which files to encrypt. List each `.env*` file. If a corresponding `.enc.yaml` file already exists, note it will be overwritten.

5. **Encrypt each selected file** (convert dotenv→YAML, then encrypt):
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/../sops-setup/scripts/dotenv_yaml.py to-yaml <file> > <file>.enc.yaml.tmp
   sops --encrypt <file>.enc.yaml.tmp > <file>.enc.yaml
   rm <file>.enc.yaml.tmp
   ```
   Example: `.env.local` → `.env.local.enc.yaml`

6. **Verify** each encrypted file exists and is non-empty.

7. **Summary**:
   ```
   | File | Encrypted To | Status |
   |------|-------------|--------|
   | .env.local | .env.local.enc.yaml | done |
   | .env.production | .env.production.enc.yaml | done |
   ```
   Remind user to commit the `.enc.yaml` files.

## Key Rules

- Always verify `.sops.yaml` exists before attempting encryption
- Always convert dotenv→YAML before encrypting (use the helper script)
- Warn if an `.enc.yaml` file will be overwritten
- Never delete the original `.env` file — only create the `.enc.yaml` copy
- Clean up `.tmp` files even if encryption fails

---
name: sops-decrypt
description: >-
  Decrypt SOPS-encrypted YAML files back to .env format. Finds *.enc.yaml files,
  decrypts, and converts YAML back to dotenv. Use when user mentions "decrypt env",
  "sops decrypt", "decrypt secrets", "restore env", "decrypt .env",
  "restore secrets", "decrypt environment files".
disable-model-invocation: true
---

# SOPS Decrypt

Decrypt `.enc.yaml` files back to their plaintext `.env` originals.

## Workflow

1. **Detect current state**:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/../sops-setup/scripts/detect_sops.py <project-root>
   ```

2. **Verify prerequisites**:
   - `tools.sops.installed` must be true — if not, tell user to install: `brew install sops` (macOS) or download binary (Linux)
   - `age_key.exists` must be true — if not, guide user to place their age private key at the expected path, or set `SOPS_AGE_KEY_FILE` env var

3. **Show encrypted files** from `project.encrypted_files`. If empty, report "No encrypted files found" and exit.

4. **Use `AskUserQuestion`** (multiSelect: true) — which files to decrypt. For each, show the target output name (e.g., `.env.local.enc.yaml` → `.env.local`). If the target file already exists, note it will be overwritten.

5. **Decrypt each selected file** (decrypt YAML, then convert to dotenv):
   ```bash
   sops --decrypt <file>.enc.yaml > <file>.dec.yaml.tmp
   python3 ${CLAUDE_SKILL_DIR}/../sops-setup/scripts/dotenv_yaml.py to-dotenv <file>.dec.yaml.tmp > <target-env-file>
   rm <file>.dec.yaml.tmp
   ```
   Where `<target-env-file>` is the encrypted filename with `.enc.yaml` suffix removed.
   Example: `.env.local.enc.yaml` → `.env.local`

6. **Verify** each decrypted file exists and is non-empty.

7. **Summary**:
   ```
   | Encrypted File | Decrypted To | Status |
   |---------------|--------------|--------|
   | .env.local.enc.yaml | .env.local | done |
   ```
   Remind user: **Do NOT commit the decrypted .env files** — they should be in `.gitignore`.

## Key Rules

- Always check that the age private key exists before attempting decryption
- Always convert YAML→dotenv after decrypting (use the helper script)
- Warn if a decrypted file will overwrite an existing one
- Clean up `.tmp` files even if decryption fails
- After decryption, remind user that plaintext `.env` files must stay out of git
- If decryption fails with "no identity matched", the machine's key is not authorized — suggest running `/devtools:sops-add-key` on a machine that has access

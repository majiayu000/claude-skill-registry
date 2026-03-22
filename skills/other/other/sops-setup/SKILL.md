---
name: sops-setup
description: >-
  Set up SOPS + age encryption for sharing .env files securely across machines.
  Detects existing state, installs tools, generates age keys, creates .sops.yaml,
  and encrypts .env files as YAML (avoids SOPS dotenv bug #1435). Use when user
  mentions "sops setup", "encrypt env", "share secrets", "secure env files",
  "sops age setup", "env encryption", "setup sops", "share env across machines".
disable-model-invocation: true
---

# SOPS + age Setup Wizard

Interactive setup for SOPS + age encryption. Detects current state and guides through configuration.

**Important**: This skill uses YAML format for encrypted files (not dotenv) because SOPS has a [known bug (#1435)](https://github.com/getsops/sops/issues/1435) where the dotenv store corrupts backslash and `\n` sequences on decrypt. A helper script handles dotenv↔YAML conversion transparently.

## Pre-flight

Run the detection script to understand current state:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/detect_sops.py <project-root>
```

## Two-Phase Workflow

### Phase 1: Detect

1. **Run the detector** on the project root:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/detect_sops.py <project-root>
   ```

2. **Summarize findings** — show a status table:

   | Component | Status | Detail |
   |-----------|--------|--------|
   | sops binary | installed/missing | version, path |
   | age binary | installed/missing | version, path |
   | age key | exists/missing | public key (truncated) |
   | .sops.yaml | exists/missing | # of authorized keys |
   | .env files | N found | list of filenames |
   | encrypted files | N found | list of *.enc.yaml files |
   | .gitignore | ok/needs update | env ignored, enc.yaml not ignored |

### Phase 2: Configure

Walk through each missing component. Skip steps where detection shows everything is already configured.

1. **Install tools** (if `tools.sops.installed` or `tools.age.installed` is false):
   - Show install commands based on `os` field:
     - **macOS**: `brew install sops age`
     - **Linux**: Show download URLs for latest binaries from GitHub releases
   - After user confirms installation, re-run detector to verify

2. **Generate age key** (if `age_key.exists` is false):
   - Create directory: `mkdir -p ~/.config/sops/age`
   - Generate key: `age-keygen -o ~/.config/sops/age/keys.txt`
   - **Set permissions**: `chmod 600 ~/.config/sops/age/keys.txt`
   - Display the public key and tell user to **save it somewhere safe** (password manager, secure note)

3. **Generate backup key** (recommended):
   - Use `AskUserQuestion` — offer to create an offline backup key for disaster recovery
   - If yes:
     ```bash
     age-keygen 2>&1 | tee /dev/stderr | grep "public key:" | awk '{print $NF}'
     ```
     Display BOTH the public key AND the full output (which includes the private key).
     Tell user: **Copy the entire output (including the private key line starting with AGE-SECRET-KEY-) to a password manager or secure offline storage. This is your recovery key.**
   - The backup public key will be added to `.sops.yaml` alongside the machine key

4. **Create `.sops.yaml`** (if `project.sops_yaml.exists` is false):
   - Write `.sops.yaml` with machine key + backup key (if generated):
     ```yaml
     creation_rules:
       - path_regex: (^|/)\.env\.[^/]+\.enc\.yaml$
         age: >-
           <machine-public-key>,
           <backup-public-key>
     ```
   - If `.sops.yaml` already exists but is missing this machine's key, offer to add it

5. **Set up `.gitattributes`** for diff-friendly encrypted files:
   - Add to `.gitattributes`:
     ```
     *.enc.yaml diff=sopsdiffer
     ```
   - Configure git:
     ```bash
     git config diff.sopsdiffer.textconv "sops decrypt"
     ```
   - This makes `git diff` show decrypted content for encrypted files

6. **Update `.gitignore`** (if needed):
   - Ensure `.env*` patterns are ignored (secrets must not be committed in plaintext)
   - Ensure `*.enc.yaml` is NOT ignored (encrypted files should be committed)
   - Show proposed changes and confirm with user before writing

7. **Encrypt files** (if `project.env_files` is non-empty):
   - Use `AskUserQuestion` (multiSelect: true) — show detected `.env*` files
   - For each selected file, convert dotenv→YAML then encrypt:
     ```bash
     python3 ${CLAUDE_SKILL_DIR}/scripts/dotenv_yaml.py to-yaml <file> > <file>.enc.yaml.tmp
     sops --encrypt <file>.enc.yaml.tmp > <file>.enc.yaml
     rm <file>.enc.yaml.tmp
     ```
     Example: `.env.local` → `.env.local.enc.yaml`
   - Verify each encrypted file was created successfully

8. **Confirmation summary** — show table of all actions taken:
   ```
   | Step | Action | Result |
   |------|--------|--------|
   | Tools | sops 3.9.4, age 1.2.0 | installed |
   | Key | Machine key generated | age1abc...def |
   | Key | Backup key generated | age1xyz...uvw (save offline!) |
   | Permissions | chmod 600 keys.txt | done |
   | Config | .sops.yaml created | 2 keys authorized |
   | Git | .gitattributes updated | sopsdiffer configured |
   | Git | .gitignore updated | .env* ignored |
   | Encrypt | .env.local → .env.local.enc.yaml | done |

   ## Next Steps
   - Commit .sops.yaml, .gitattributes, and *.enc.yaml files to git
   - On another machine: clone, install sops+age, place age key, run /devtools:sops-decrypt
   - To add another machine: /devtools:sops-add-key
   - To encrypt after editing .env: /devtools:sops-encrypt
   - To decrypt after pulling: /devtools:sops-decrypt
   ```

## Key Rules

- **Never overwrite** existing files without asking. Always offer merge/replace/skip.
- **Detect first** — skip steps that are already configured.
- **Use `AskUserQuestion`** for every decision. Do not assume user preferences.
- **YAML format only** — never use `--input-type dotenv`. Use the dotenv_yaml.py helper for conversion.
- **chmod 600** on age key files immediately after creation.
- **Display public keys** after generation — user needs them for multi-machine setup.
- **Verify after each step** — re-run relevant checks to confirm success.

## References

- **Workflow**: See [WORKFLOW.md](WORKFLOW.md) for detailed per-step flows
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for example setup sessions
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- **Detection Script**: See [scripts/detect_sops.py](scripts/detect_sops.py) for detection logic
- **Converter**: See [scripts/dotenv_yaml.py](scripts/dotenv_yaml.py) for dotenv↔YAML conversion
- **Best Practices**: See [references/sops-best-practices.md](references/sops-best-practices.md) for research

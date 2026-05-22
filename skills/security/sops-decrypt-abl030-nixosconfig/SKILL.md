---
name: sops-decrypt
description: Decrypt and edit SOPS-encrypted secrets in this repo
---

# SOPS Secret Decryption

## Key Lookup Order

This machine has a user SSH key that can decrypt all secrets:

```bash
age_key=$(ssh-to-age -private-key -i ~/.ssh/id_ed25519 2>/dev/null)
```

## Decrypt a secret to stdout

```bash
age_key=$(ssh-to-age -private-key -i ~/.ssh/id_ed25519 2>/dev/null) && \
  SOPS_AGE_KEY="$age_key" sops -d secrets/<filename>
```

## Encrypt a plaintext file (must specify --config)

```bash
age_key=$(ssh-to-age -private-key -i ~/.ssh/id_ed25519 2>/dev/null) && \
  SOPS_AGE_KEY="$age_key" sops -e \
    --config /home/abl030/nixosconfig/secrets/.sops.yaml \
    --input-type dotenv --output-type dotenv \
    <plaintext-file> > <encrypted-output>
```

## Edit a secret in-place (decrypt, modify, re-encrypt)

```bash
# 1. Decrypt to temp file
age_key=$(ssh-to-age -private-key -i ~/.ssh/id_ed25519 2>/dev/null)
SOPS_AGE_KEY="$age_key" sops -d secrets/<file>.env > /tmp/<file>_plain.env

# 2. Modify the plaintext (sed, python, etc.)
sed -i 's/OLD_VALUE/NEW_VALUE/' /tmp/<file>_plain.env

# 3. Re-encrypt back
SOPS_AGE_KEY="$age_key" sops -e \
  --config /home/abl030/nixosconfig/secrets/.sops.yaml \
  --input-type dotenv --output-type dotenv \
  /tmp/<file>_plain.env > secrets/<file>.env

# 4. Clean up plaintext
rm -f /tmp/<file>_plain.env
```

## Important Notes

- The `.sops.yaml` config lives at `secrets/.sops.yaml`
- When encrypting, you MUST pass `--config` explicitly (sops won't find it automatically for files outside `secrets/`)
- All secret files are in `secrets/` directory
- Format is typically `dotenv` (use `--input-type dotenv --output-type dotenv`)
- The user's `dc` command does the same thing but opens in nvim (not usable non-interactively)
- After modifying secrets, commit the encrypted file — never commit plaintext
- Run `sops updatekeys --yes <file>` after adding new hosts to `.sops.yaml`

## Secret Files

| File | Contents |
|------|----------|
| `kopia.env` | KOPIA_SERVER_USER, KOPIA_SERVER_PASSWORD, KOPIA_PASSWORD |
| `uptime-kuma.env` | KUMA_USERNAME, KUMA_PASSWORD |
| `uptime-kuma-api.env` | KUMA_API_KEY |
| `immich.env` | Immich DB and API credentials |
| `caddy-tailscale.env` | Tailscale auth key |
| `acme-cloudflare.env` | Cloudflare API token for ACME |
| Others | See `ls secrets/` |

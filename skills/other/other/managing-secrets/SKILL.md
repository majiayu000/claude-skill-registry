---
name: Managing Secrets
description: How secrets are stored, decrypted, and used on the devbox. Use when adding, removing, or debugging secrets.
---

# Managing Secrets

Secrets are managed with sops-nix using age encryption. They're encrypted in the repo and auto-decrypted at boot.

## Current Secrets

| Secret | Usage | How it's consumed |
|--------|-------|-------------------|
| `github_ssh_key` | Git operations | Deployed to `~/.ssh/id_ed25519_github` |
| `cloudflared_tunnel_token` | Cloudflare tunnel | Systemd service reads from `/run/secrets/` |
| `cloudflare_api_token` | Wrangler CLI | Exported as `CLOUDFLARE_API_TOKEN` in bash |
| `op_service_account_token` | 1Password bootstrap | Available at `/run/secrets/` for scripts |
| `claude_personal_oauth_token` | Headless Claude Code | Exported as `CLAUDE_CODE_OAUTH_TOKEN` in bash |

## How Secrets Flow

```
secrets/devbox.yaml (encrypted in git)
        ↓
sops-nix decrypts at boot using /persist/sops-age-key.txt
        ↓
/run/secrets/<secret_name> (plaintext, mode 0400)
        ↓
Consumed by: systemd services, bash exports, or file deployment
```

## Adding a New Secret

### Step 1: Add to sops file

```bash
# Edit encrypted file (requires age key access)
sudo nix-shell -p sops --run "SOPS_AGE_KEY_FILE=/persist/sops-age-key.txt sops secrets/devbox.yaml"

# Or use sops set for non-interactive:
sudo nix-shell -p sops --run "SOPS_AGE_KEY_FILE=/persist/sops-age-key.txt sops set secrets/devbox.yaml '[\"my_new_secret\"]' '\"secret-value\"'"
```

### Step 2: Declare in NixOS config

Edit `hosts/devbox/configuration.nix`, add to `sops.secrets`:

```nix
sops.secrets = {
  # ... existing secrets ...

  my_new_secret = {
    owner = "dev";
    group = "dev";
    mode = "0400";
    # Optional: deploy to specific path instead of /run/secrets/
    # path = "/home/dev/.config/app/secret";
  };
};
```

### Step 3: Consume the secret

**Option A: Export as env var** (for CLI tools)

Edit `users/dev/home.linux.nix`:

```nix
programs.bash.initExtra = lib.mkAfter ''
  if [ -r /run/secrets/my_new_secret ]; then
    export MY_ENV_VAR="$(cat /run/secrets/my_new_secret)"
  fi
'';
```

**Option B: Use in systemd service** (for daemons)

```nix
systemd.services.my-service = {
  serviceConfig = {
    ExecStart = "${pkgs.writeShellScript "run" ''
      exec my-command --token "$(cat /run/secrets/my_new_secret)"
    ''}";
  };
};
```

**Option C: Deploy as file** (for apps expecting file path)

Set `path` in the secret declaration (Step 2).

### Step 4: Apply changes

```bash
git add secrets/devbox.yaml hosts/devbox/configuration.nix
git commit -m "feat: add my_new_secret"

sudo nixos-rebuild switch --flake .#devbox
home-manager switch --flake .#dev  # if you added bash export
```

## Removing a Secret

### Step 1: Remove from consumers

- Remove any bash exports from `users/dev/home.linux.nix`
- Remove any systemd service references
- Remove declaration from `hosts/devbox/configuration.nix`

### Step 2: Remove from sops file

```bash
sudo nix-shell -p sops -p yq-go --run "
  cd /home/dev/projects/workstation
  SOPS_AGE_KEY_FILE=/persist/sops-age-key.txt sops -d secrets/devbox.yaml > /tmp/secrets-plain.yaml
  yq -i 'del(.secret_to_remove)' /tmp/secrets-plain.yaml
  SOPS_AGE_KEY_FILE=/persist/sops-age-key.txt sops encrypt --age age1kyd7dzxtgte0rcd0nj3chfvcfvammhywe63f25tlsrf8knhf3u8sxp8z9n --input-type yaml --output-type yaml /tmp/secrets-plain.yaml > secrets/devbox.yaml
  rm /tmp/secrets-plain.yaml
"
```

### Step 3: Apply and commit

```bash
git add -A && git commit -m "chore: remove secret_to_remove"
sudo nixos-rebuild switch --flake .#devbox
```

## Key Files

| File | Purpose |
|------|---------|
| `secrets/devbox.yaml` | Encrypted secrets (committed to git) |
| `secrets/.sops.yaml` | sops config (which keys can decrypt) |
| `/persist/sops-age-key.txt` | Age private key (never in git, root-only) |
| `hosts/devbox/configuration.nix` | Secret declarations for sops-nix |
| `users/dev/home.linux.nix` | Bash exports for env vars |

## Troubleshooting

### "permission denied" when editing secrets

The age key is root-only. Use `sudo` with nix-shell:

```bash
sudo nix-shell -p sops --run "SOPS_AGE_KEY_FILE=/persist/sops-age-key.txt sops secrets/devbox.yaml"
```

### Secret not appearing after rebuild

1. Check it's declared in `sops.secrets` in configuration.nix
2. Run `sudo nixos-rebuild switch` (not just home-manager)
3. Verify: `ls -la /run/secrets/`

### Env var not exported

1. Check the export is in `home.linux.nix` (not `home.nix` - that's shared with Darwin)
2. Run `home-manager switch`
3. Start a new shell (exports only apply to new shells)

## Security Notes

- Secrets are encrypted at rest with age (AES-256)
- Decrypted secrets are mode 0400 (owner read-only)
- The age key lives on `/persist/` which survives rebuilds but not re-provisioning
- Never commit the age private key or decrypted secrets
- Env var exports are in `home.linux.nix` so they only apply on devbox, not Darwin

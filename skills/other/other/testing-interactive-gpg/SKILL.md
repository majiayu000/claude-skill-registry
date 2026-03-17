---
name: testing-interactive-gpg
description: Test the installer's interactive GPG key setup using an expect script that automates GPG prompts. Use when (1) testing GPG key generation end-to-end, (2) verifying the installer handles GPG prompts correctly, (3) debugging GPG-related failures in CI or containers, or (4) modifying the GPG setup flow and needing to validate it interactively.
---

# Interactive GPG Testing

Test the installer's GPG key setup flow using an expect script (`installer/test-interactive-gpg.exp`) that automates responses to GPG's interactive prompts.

## Why This Exists

GPG key generation is fully interactive — it prompts for email, name, passphrase, key type, and confirmations. The installer runs GPG in passthrough mode, so these prompts reach the terminal directly. Automated testing requires an expect script to respond to them.

## Prerequisites

Check if `expect` is available, and install it if not:

```bash
command -v expect || brew install expect        # macOS
command -v expect || sudo apt-get install expect # Ubuntu/Debian
command -v expect || sudo dnf install expect     # Fedora
```

## Usage

Run from the `installer/` directory (or provide the full path to the binary):

```bash
./test-interactive-gpg.exp [installer_path] [email] [name] [passphrase] [branch] [verbosity]
```

All arguments are optional and have defaults:

| Argument | Default | Description |
|----------|---------|-------------|
| `installer_path` | `./dotfiles-installer` | Path to the installer binary |
| `email` | `test-user@example.com` | GPG key email address |
| `name` | `Test CI User` | GPG key full name |
| `passphrase` | `test-ci-passphrase` | GPG key passphrase |
| `branch` | *(empty)* | Git branch for `--git-branch` flag |
| `verbosity` | *(empty)* | Verbosity flag (e.g., `-v`, `-vv`) |

### Examples

```bash
# Default values — good for quick smoke tests
./test-interactive-gpg.exp

# Custom GPG identity
./test-interactive-gpg.exp ./dotfiles-installer "your@email.com" "Your Name" "your-passphrase"

# Test a specific branch with verbose output
./test-interactive-gpg.exp ./dotfiles-installer "" "" "" feature-branch -vv

# Use a binary from goreleaser dist (in Docker container)
./test-interactive-gpg.exp \
  ./dist/dotfiles_installer_linux_arm64_v8.0/dotfiles-installer \
  "test@example.com" "Test User" "test-passphrase"
```

## How It Works

The script spawns the installer with `install --plain --install-prerequisites=true --git-clone-protocol=https` and then enters an expect loop that matches GPG prompts by regex:

- **Email/name/passphrase** — responds with the provided arguments
- **Key type, size, expiration** — accepts defaults (RSA, default size, no expiration)
- **Comment field** — skips (empty)
- **Confirmation prompts** (`(O)kay`) — sends `O`
- **Errors** — logs but continues (some errors are expected in CI)
- **Timeout** — fails after 300 seconds

The script exits with the installer's exit code.

## Testing in Docker Containers

Combine with the `testing-e2e-containers` skill workflow:

1. Build the binary: `cd installer && goreleaser build --skip before --snapshot --clean`
2. Start a container: `cd installer/docker && task ubuntu:start`
3. Copy or mount the expect script and run it inside the container
4. Tear down: `task ubuntu:stop`

See the [testing-e2e-containers skill][e2e-skill] for container management details.

## Debugging

If the script hangs or mismatches a prompt:

1. Enable debug mode: edit the script and set `exp_internal 1` (line with `exp_internal 0`)
2. Run manually and observe the exact prompt text GPG produces
3. Add or adjust regex patterns in the `expect` block to match new prompt formats

Common issues:
- **GPG errors in containers** — expected in minimal container environments; the script logs and continues
- **Timeout** — GPG key generation can be slow without entropy; ensure the container has enough (`rng-tools` or `haveged` can help)
- **Unmatched prompts** — GPG prompt text varies by version; use case-insensitive regex patterns

[e2e-skill]: /Users/timorgruber/.local/share/chezmoi/.claude/skills/testing-e2e-containers/SKILL.md

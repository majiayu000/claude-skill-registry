---
name: codex-container-sandbox
description: "Run Codex CLI inside a Podman container with full internet access but filesystem exposure limited to the repo root + explicit bind mounts; use when you want yolo/web-search without giving the agent access to your whole host filesystem."
---

# codex-container-sandbox

Use this when you want:
- Full egress/network for `codex` (web search, fetching, etc.)
- Tight filesystem boundaries via container bind mounts (repo root + explicit allowlist)

This repo contains a wrapper script intended to be installed as `codex-container-sandbox`.

## Workflow

1. **Build the image**

   From the repo root (this repository):

   ```bash
   podman build -t localhost/codex-container-sandbox:latest -f Containerfile .
   ```

2. **Install the wrapper**

   ```bash
   install -m 0755 codex-container-sandbox ~/.local/bin/codex-container-sandbox
   ```

3. **(Optional) Configure extra mounts**

   Create `~/.config/codex-container-sandbox/config.sh`:

   ```bash
   CODEX_CONTAINER_SANDBOX_IMAGE="localhost/codex-container-sandbox:latest"

   # Extra read-only mounts (mapped under /home/codex/... if under $HOME)
   CODEX_CONTAINER_SANDBOX_RO_MOUNTS=(
     "$HOME/.local/bin"
   )

   # Extra read-write mounts
   CODEX_CONTAINER_SANDBOX_RW_MOUNTS=(
     "$HOME/.cache/uv"
     "$HOME/tmp"
   )
   ```

4. **Login once inside the container**

   ```bash
   codex-container-sandbox --shell
   codex login
   ```

5. **Run the self-test (recommended)**

   ```bash
   ./selftest.sh
   ```

   If this repo is vendored as a git submodule at `./codex-container-sandbox/` (for example in a dotfiles repo), either:
   - `cd codex-container-sandbox && ./selftest.sh`, or
   - run `./codex-container-sandbox/selftest.sh` from the parent repo root.

6. **Run Codex**

   ```bash
   codex-container-sandbox exec "Summarize this repo"
   ```

## Safety notes

- This wrapper runs Codex in full-yolo mode (`--dangerously-bypass-approvals-and-sandbox`) with full networking. Anything mounted into the container can be exfiltrated.
- Keep mounts minimal; do not mount secrets, password stores, SSH keys, or large chunks of `$HOME` unless you intend to expose them.

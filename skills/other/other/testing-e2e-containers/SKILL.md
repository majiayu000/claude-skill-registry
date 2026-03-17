---
name: testing-e2e-containers
description: Run E2E tests of the installer inside Docker containers on supported Linux distributions (Ubuntu, Debian, Fedora). Use when (1) verifying installer behavior on Linux, (2) testing new installer flags or features end-to-end, (3) running the installer in a controlled environment, (4) reproducing or debugging Linux-specific issues, or (5) validating that changes work across all supported distros before pushing to CI.
---

# E2E Container Testing

Test the installer binary inside Docker containers running the supported Linux distributions.

## Workflow

1. **Build** the installer for the container platform
2. **Start** a fresh container
3. **Run** the installer inside it
4. **Verify** results
5. **Stop** the container
6. **Repeat** for each distro (ubuntu, debian, fedora)

## Step 1: Build the Binary

Use goreleaser to build snapshot binaries for all platforms defined in `.goreleaser.yaml`. Run from the `installer/` directory:

```bash
cd installer && goreleaser build --skip before --snapshot --clean
```

This produces binaries under `installer/dist/`, one per OS-arch combo. The docker-compose volumes mount `installer/` into containers at `/workspace/installer`, so the binary path inside the container follows this pattern:

```
/workspace/installer/dist/dotfiles_installer_<os>_<arch>/dotfiles-installer
```

For example, on a macOS ARM host (Apple Silicon) running Linux ARM64 containers:

```
/workspace/installer/dist/dotfiles_installer_linux_arm64_v8.0/dotfiles-installer
```

For Linux AMD64 containers:

```
/workspace/installer/dist/dotfiles_installer_linux_amd64_v1/dotfiles-installer
```

## Step 2: Run Tests in Containers

**Start a fresh container for each test scenario** to avoid state leakage from previous runs. Reuse the image, but always start from scratch.

```bash
cd installer/docker

# Start container
task ubuntu:start

# Run the installer (adjust flags for the scenario being tested)
docker-compose -f ubuntu/docker-compose.yml exec --user testuser installer-test-ubuntu \
  sudo /workspace/installer/dist/dotfiles_installer_linux_arm64_v8.0/dotfiles-installer install \
    --shell zsh --shell-source auto --non-interactive --install-prerequisites

# Verify results (scenario-dependent)
# ...

# Tear down before next test
task ubuntu:stop
```

For standalone containers (without docker-compose), bind-mount the dist directory explicitly:

```bash
docker run -d --name test-ubuntu --platform linux/arm64 \
  -v "$(pwd)/../dist:/workspace/installer/dist:ro" \
  ubuntu-installer-test-ubuntu:latest tail -f /dev/null

docker exec test-ubuntu /workspace/installer/dist/dotfiles_installer_linux_arm64_v8.0/dotfiles-installer install \
  --shell zsh --shell-source system --non-interactive

docker stop test-ubuntu && docker rm test-ubuntu
```

## Step 3: Verify Results

Verification depends on what the test scenario is exercising. After running the installer, determine appropriate checks based on the flags and features being tested, then run them inside the container using `docker-compose exec` or `docker exec`.

## Testing All Distros

Run through all three distros. Always stop before starting the next test:

```bash
cd installer/docker

for distro in ubuntu debian fedora; do
  task ${distro}:start
  # ... run installer and verify ...
  task ${distro}:stop
done
```

## Interactive GPG Testing

For testing the GPG key setup flow interactively (which requires automating GPG's prompts), see the [testing-interactive-gpg skill][gpg-skill].

[gpg-skill]: /Users/timorgruber/.local/share/chezmoi/.claude/skills/testing-interactive-gpg/SKILL.md

## Gotchas

- See [distro-specific notes](references/distro-notes.md) for platform quirks (zsh paths, brew behavior, package manager differences)
- Homebrew's first run downloads portable Ruby (~30MB) and can take several minutes
- Fedora's first `dnf` triggers a repo metadata sync (~30MB) - be patient or use generous timeouts
- If brew errors with "process has already locked", a previous install was interrupted - start a fresh container
- When running long tests, prefer running in background and polling for completion over setting very long timeouts

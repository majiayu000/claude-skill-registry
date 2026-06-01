---
name: nixos-btw
description: >
  · Administer NixOS/Nix: flakes, home-manager, nix-darwin, generations, overlays, disko. Triggers: 'nixos', 'nix', 'flake', 'home-manager', 'configuration.nix', 'nixos-rebuild'. Not for other distros.
license: MIT
compatibility: "Requires NixOS, or Nix/Determinate Nix/Lix on Linux/macOS/WSL"
metadata:
  source: iuliandita/skills
  date_added: "2026-04-23"
  effort: high
  argument_hint: "[issue-or-subsystem]"
---

# NixOS BTW: NixOS, Nix, and Flakes Administration

Administer NixOS without falling back into imperative distro muscle memory. NixOS is
declarative, functional, and atomic: the system is a value computed from a configuration,
every change becomes a new immutable generation in `/nix/store`, and rollbacks are a
bootloader entry away. This skill keeps that model intact, then layers in the practical
stack: channels vs flakes, `nixos-rebuild` vs `nix` CLI, home-manager, nix-darwin, store
hygiene, overlays, module writing, secrets, and the Determinate Nix and Lix lanes.

The places NixOS breaks are NixOS-shaped: channel drift, flake input staleness, garbage
collection that nukes a needed derivation, overlays fighting, `nix-env -i` poisoning the
user profile, hardware modules missing, or people treating `/etc/nixos/configuration.nix`
like a normal Linux config file.

**Why people run it.** Atomic upgrades and rollbacks, bit-for-bit reproducible systems,
disposable dev shells, fleet-wide configuration without a separate config-management tool,
and a single language for a workstation, a server, a container image, a NixOS VM, and a
macOS laptop via nix-darwin.

**Versions worth pinning** (verified May 2026):

Pin versions only when they shape compatibility or troubleshooting. For ordinary package
work, trust the live channel or flake lock over a stale table.

| Component | Version or date | Why it matters |
|-----------|-----------------|----------------|
| NixOS stable | 25.11 "Xantusia" (Nov 2025) | current stable, maintained until 2026-06-30 |
| NixOS upcoming | 26.05 "Yarara" (May 2026) | next release; do not target yet for production |
| Nix (CLI / daemon) | 2.33 (Dec 2025) | stable upstream; 2.32 introduced skip-substitutable-downloads |
| `nixos-rebuild-ng` | default in 25.11 | Python rewrite of nixos-rebuild, default for new installs |
| home-manager | release-25.11 (Nov 2025) | matches NixOS 25.11; unstable tracks nixos-unstable |
| nix-darwin | tracks nixpkgs 25.11 and master | active macOS module system (Intel + Apple Silicon) |
| Determinate Nix | downstream, flakes-on by default | validated distribution; parallel eval, lazy trees |
| Lix | fork of Nix | compatibility-focused fork; Meson build, improved errors |
| Kernel default for 25.11 | Linux 6.12 LTS | default `linuxPackages`; `linuxPackages_latest` tracks mainline (6.17 at 25.11 release, not LTS) |

## When to use

- NixOS system administration: `configuration.nix`, modules, options, imports, and `/etc/nixos` workflow
- Flake work: `flake.nix`, `flake.lock`, inputs, outputs, `nix flake update`, `nix flake check`
- `nixos-rebuild` flow: `switch`, `test`, `boot`, `dry-activate`, `build-vm`, and rollback
- Channels, pinning, and input management: `nix-channel`, `nix registry`, `npins`, `niv`, flake inputs
- home-manager (standalone, NixOS module, or nix-darwin module) for user-level declarative config
- nix-darwin on macOS: declarative system config, Homebrew integration, LaunchDaemons
- Nix store and derivations: `nix-store`, `nix store`, GC roots, `nix-collect-garbage`, optimise-store
- Dev environments: `nix-shell`, `nix develop`, `shell.nix`, `default.nix`, direnv with `nix-direnv`
- Overlays, overrides, and package customisation: overlays, `overrideAttrs`, `override`, pin patches
- Writing NixOS modules: options, config, assertions, conditionals, imports, `mkMerge`, `mkForce`
- Secrets management: sops-nix, agenix, nix-sops, ragenix, activation-time decryption
- Declarative disks and filesystems: disko, btrfs layouts, LUKS, ZFS, impermanence patterns
- Remote installs and imaging: nixos-anywhere, `nixos-install`, `nixos-generate`, SD images, ISO images
- Hardware enablement: nixos-hardware profiles, firmware, kernel choice, GPU drivers
- Unfree and insecure packages: `allowUnfree`, `permittedInsecurePackages`, `NIXPKGS_ALLOW_*`
- Boot and generations: systemd-boot vs GRUB, kernel selection, `nix-env --list-generations`, boot entries
- Garbage collection strategy: retention, GC roots, `nix.gc.automatic`, auto-optimise-store
- Determinate Nix lane: Determinate installer, flakes-on-by-default, enterprise backports
- Lix lane: fork-specific behavior, coexistence, and migration notes
- Integration with Docker, Kubernetes, and CI: `nix build`, image outputs, cachix, attic

## When NOT to use

- Arch or CachyOS administration - use **arch-btw**
- Debian, Ubuntu, Mint, or Pop!_OS administration - use **debian-ubuntu**
- Fedora, RHEL, CentOS Stream, Rocky, or Alma administration - use **rhel-fedora**
- Kali Linux and offensive-tool distros - use **kali-linux**
- Shell syntax, quoting, or portability outside Nix expressions - use **command-prompt**
- Docker, Podman, image builds, or container runtime issues - use **docker**
- Kubernetes cluster or manifest work - use **kubernetes**
- Fleet-wide non-Nix Linux configuration via playbooks - use **ansible**
- Terraform or OpenTofu infrastructure code - use **terraform**
- CI/CD pipeline design for Nix-based builds (cachix push, build farm, pipeline stages) - use **ci-cd**
- Offensive or privesc testing - use **lockpick**
- Defensive hardening and vuln review - use **security-audit**
- OPNsense or pfSense appliance work - use **firewall-appliance**

---

## AI Self-Check

Before returning NixOS or Nix commands, verify:

- [ ] **Lane identified**: NixOS install, Nix on non-NixOS Linux, Nix on macOS (nix-darwin or plain Nix), WSL, Determinate Nix, or Lix. Advice diverges fast.
- [ ] **Channels vs flakes decided**: confirm which the user has before prescribing `nix-channel`, `nixos-rebuild --flake`, or `nix flake update`. Mixing without intent creates channel-lock drift.
- [ ] **Flake status is current**: flakes remain nominally experimental on upstream Nix but are enabled by default on Determinate Nix; recommend enabling `experimental-features = nix-command flakes` where the user is already using flakes.
- [ ] **`nix-env -i` is not the answer**: installing into the per-user profile hides state from `configuration.nix` and breaks reproducibility. Use declarative `environment.systemPackages`, `home.packages`, or an ad-hoc `nix shell` instead.
- [ ] **No partial upgrade advice**: on flakes-based systems, do not bump a single input without running `nixos-rebuild --flake` after; on channels, do not change only `nixos` without updating dependent channels too.
- [ ] **Rebuild verb is intentional**: `switch`, `test`, `boot`, `dry-activate`, `build-vm`, and `build` differ. `test` does not persist the boot entry; `boot` does not activate now; `switch` does both.
- [ ] **Known-good generation preserved**: never remove the last known-good generation, and never `nix-collect-garbage -d` on a system that just booted a new generation without verifying the new one survives a reboot.
- [ ] **GC roots respected**: dev shells, direnv caches, and CI artifacts often hold GC roots. Do not recommend aggressive GC without checking `nix-store --gc --print-roots` first.
- [ ] **Unfree / insecure gates named explicitly**: set `nixpkgs.config.allowUnfree = true;` or `allowUnfreePredicate`, and list insecure packages under `permittedInsecurePackages`. Do not default to `NIXPKGS_ALLOW_UNFREE=1` as the permanent answer.
- [ ] **Hardware module present**: for fresh installs, `hardware-configuration.nix` must be regenerated with `nixos-generate-config` and not hand-edited for filesystem UUIDs. For laptops, check nixos-hardware profile.
- [ ] **Kernel and initrd coherence**: `boot.kernelPackages`, initrd modules, filesystems, and bootloader agree. Do not casually swap kernels on a system with ZFS, NVIDIA, or custom out-of-tree modules.
- [ ] **Module fields real**: options named in advice exist in the version of nixpkgs the user has. `options` graveyards drift between 23.11, 24.05, 24.11, 25.05, and 25.11 - verify against the `nixpkgs` tag the user pinned.
- [ ] **Secrets not put in the store**: anything under `./secret.age`, `./sops.yaml`, or similar must be decrypted at activation time by sops-nix or agenix, not embedded directly in a Nix string that ends up world-readable in `/nix/store`.
- [ ] **disko / impermanence claims match the install**: declarative disk layouts change the recovery story. Confirm partition, filesystem, and subvolume layout before prescribing rollback or wipe steps.
- [ ] **home-manager mode identified**: standalone, NixOS module, or nix-darwin module. `home-manager switch` vs `nixos-rebuild switch` vs `darwin-rebuild switch` is not interchangeable.
- [ ] **Overlay placement sane**: overlays belong in `nixpkgs.overlays` (NixOS) or as a flake input overlay. Do not recommend global `~/.config/nixpkgs/overlays.nix` on a flakes system where that path is often ignored.
- [ ] **Determinate / Lix advice scoped**: Determinate's `determinate-nixd` and Lix's CLI diverge from upstream in subtle places. Name the lane before suggesting daemon or CLI flags.
- [ ] **Diagnostic errors are not silenced**: do not hide useful output with `2>/dev/null` when the error text is the evidence. Use `2>&1 || true` when gathering.
- [ ] **Version pins justified**: if a pinned `system.stateVersion` is suggested, explain why; do not change `stateVersion` on an existing system casually - it controls migration semantics.
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Channel/flake checked**: advice matches stable, unstable, flake, home-manager, or nix-darwin context
- [ ] **Rollback identified**: generation rollback, boot entries, and store/cache state are understood before changes

---

## Performance

- Use binary caches and substituters deliberately; local source builds can dominate iteration time.
- Evaluate and build targeted attributes before rebuilding entire systems where possible.
- Garbage-collect only after confirming new generations boot and required roots are preserved.


---

## Best Practices

- Keep hardware, secrets, user packages, and service modules separated enough to review changes safely.
- Commit flake lock and configuration changes together for reproducible rebuilds.
- Do not delete old generations or store paths until rollback is no longer needed.


## Workflow

### Step 1: Identify the Nix lane first

| Lane | Default stance | What changes |
|------|----------------|--------------|
| **NixOS installed (stable 25.11)** | configuration.nix or flake.nix drives everything | full system is Nix-managed; rollbacks via bootloader |
| **NixOS unstable / 26.05 pre-release** | treat as rolling-ish | expect breakage; verify options still exist |
| **Nix on non-NixOS Linux** | user-level only | host distro still owns services and boot; no `nixos-rebuild` |
| **nix-darwin on macOS** | declarative macOS config | `darwin-rebuild switch`; host owns kernel and firmware |
| **Plain Nix on macOS (no darwin)** | package manager only | `nix profile` or `nix shell` for user tooling |
| **WSL2 with NixOS** | full NixOS in WSL | boot and init differ; host owns kernel |
| **Determinate Nix** | flakes on by default, daemon differs | `determinate-nixd`, parallel eval, lazy trees |
| **Lix** | upstream-compatible fork | CLI mostly matches; internals, error messages, and Meson build diverge |

### Step 2: Gather current system state

Start narrow. Widen only when the failing layer is still unclear.

Baseline checks for every NixOS or Nix case:

```bash
# Identify OS and Nix lane
cat /etc/os-release 2>&1 || true
nix --version
command -v nixos-version >/dev/null 2>&1 && nixos-version
command -v darwin-version >/dev/null 2>&1 && darwin-version
command -v determinate-nixd >/dev/null 2>&1 && determinate-nixd status
uname -a

# Nix config and features
nix config show 2>&1 | grep -E 'experimental-features|extra-experimental|substituters|trusted-users' || true
cat /etc/nix/nix.conf 2>&1 || true

# NixOS-specific
[[ -d /etc/nixos ]] && ls /etc/nixos
[[ -f /etc/nixos/flake.nix ]] && echo "flakes system" || echo "channels system (or flake elsewhere)"
command -v nix-channel >/dev/null 2>&1 && nix-channel --list 2>&1 || true
command -v nixos-rebuild >/dev/null 2>&1 && nixos-rebuild --help 2>&1 | head -5

# Generations and boot
command -v nix-env >/dev/null 2>&1 && nix-env --list-generations -p /nix/var/nix/profiles/system 2>&1 | tail -5 || true
[[ -d /boot/loader/entries ]] && ls /boot/loader/entries 2>&1 | tail -10
command -v bootctl >/dev/null 2>&1 && bootctl status 2>&1 | head -20 || true

# Store health and GC state
df -h /nix/store
du -sh /nix/store 2>&1 || true
nix-store --gc --print-roots 2>&1 | wc -l
```

Add subsystem probes only when the task needs them:

```bash
# home-manager
command -v home-manager >/dev/null 2>&1 && home-manager generations | head -5

# flake state
[[ -f flake.nix ]] && nix flake metadata 2>&1 | head -20
[[ -f flake.lock ]] && nix flake check --no-build 2>&1 || true

# services and logs (NixOS)
systemctl --failed 2>&1 || true
journalctl -b -p warning..alert 2>&1 | tail -30 || true

# hardware (NixOS)
lspci -k 2>&1 | grep -Ei 'vga|3d|display|network' || true
journalctl -b 2>&1 | grep -Ei 'nvrm|nvidia|amdgpu|i915|xe|drm|firmware' || true
```

### Step 3: Load only the relevant reference

| Task type | Reference |
|-----------|-----------|
| configuration.nix, modules, options, assertions, `mkForce`/`mkMerge` | `references/configuration-and-modules.md` |
| flakes, inputs, lockfile, `nix flake`, registry, input follows | `references/flakes-and-channels.md` |
| `nixos-rebuild` verbs, generations, rollback, boot entries, dry-activate | `references/rebuild-generations-and-rollback.md` |
| home-manager (standalone, NixOS module, nix-darwin module) | `references/home-manager-and-darwin.md` |
| overlays, `overrideAttrs`, `override`, packaging, `mkDerivation`, patching | `references/overlays-packaging-and-overrides.md` |
| Nix store, `nix-store`, GC roots, `nix-collect-garbage`, optimise-store, CAS | `references/store-gc-and-builders.md` |
| dev shells, `nix develop`, `shell.nix`, direnv with `nix-direnv` | `references/dev-shells-and-direnv.md` |
| disko, impermanence, nixos-anywhere, SD/ISO images, nixos-generators | `references/disko-impermanence-and-imaging.md` |
| hardware, firmware, kernels, nixos-hardware, GPU drivers, Wayland desktop | `references/hardware-desktop-and-kernel.md` |
| secrets: sops-nix, agenix, activation decryption, keyrings | `references/secrets-sops-and-agenix.md` |
| Determinate Nix, Lix, lane-specific behavior, migration notes | `references/determinate-lix-and-lanes.md` |
| recurring NixOS and Nix footguns, edge cases, upgrade breakage | `references/gotchas-and-special-situations.md` |

Do not load every reference by default. Pick the one that matches the failure mode.

### Step 3.5: Stay here or hand off

| Request shape | Route |
|---------------|-------|
| NixOS install, module, flake, rebuild, rollback, store, overlay, disko, secrets | stay in **nixos-btw** |
| Build a Docker or OCI image from Nix (`dockerTools`, `nix2container`) | stay here for the Nix build, hand to **docker** for runtime |
| Deploy a NixOS box into K8s (`nixos-in-kube`, custom images) | start here, hand to **kubernetes** for the cluster side |
| Review Nix-produced container for OWASP / supply chain issues | stay for the Nix build; use **security-audit** for the audit |
| Write a bash one-liner or zsh function that wraps `nix` calls | use **command-prompt** |

### Step 4: Change one layer at a time

- Fix flake or channel state before blaming `nixos-rebuild`.
- Run `nixos-rebuild dry-activate --flake .#host` before `switch` when the risk is nonzero.
- Prefer `test` over `switch` when the change might break login; `test` does not persist the boot entry, so a reboot returns to a known-good generation.
- Fix option-name drift before blaming module logic: `nix repl -f '<nixpkgs/nixos>' -I ...` and `:p config.services.foo` beat guessing.
- On home-manager, run `home-manager switch` separately if it is standalone; otherwise `nixos-rebuild switch` picks it up when it is wired as a module.
- Avoid touching `system.stateVersion`. It anchors migration semantics.
- Keep overlays composable: scope to `final: prev: { ... }`, not mutating `pkgs` in-place.
- Validate before GC: `nix-store --gc --print-roots | grep <path>` before deleting.

### Step 5: Validate before closing

```bash
# System state
nixos-version 2>&1 || true
nix-env --list-generations -p /nix/var/nix/profiles/system | tail -5
systemctl --failed 2>&1 || true

# Flake sanity
[[ -f flake.nix ]] && nix flake check --no-build

# Store sanity
nix-store --verify --check-contents 2>&1 | tail -20
df -h /nix/store
```

Reboot only when the boot path is understood and at least one known-good generation remains.

---

## Troubleshooting Pattern

Keep triage cross-layer and boring:

1. Confirm the Nix lane (NixOS vs Nix-on-host, flakes vs channels, Determinate vs upstream vs Lix).
2. Identify the failing layer: input state, evaluation, build, activation, or runtime service.
3. Pull the right logs before changing config.
4. Change one layer at a time and retest.
5. Prefer rollback to reinstall. Generations are the whole point.

Core log sweep on NixOS:

```bash
journalctl -b -p warning..alert
journalctl --user -b
dmesg --level=err,warn
journalctl -u nix-daemon -b
journalctl -u nixos-rebuild -b 2>&1 || true
```

Build and eval failures are loudest in the rebuild output itself; pipe through `--show-trace`
and, for opaque errors, `--print-build-logs`:

```bash
nixos-rebuild switch --flake .#host --show-trace --print-build-logs 2>&1 | tail -200
```

When a problem looks "flake-only," compare one clean baseline:

- delete `flake.lock` and re-lock, or
- roll one input back to its previous rev via `nix flake lock --override-input`, or
- build the same output on another machine with the same `flake.lock` to isolate hardware vs config.

---

## Default Decisions

- **Declarative first.** `nix-env -i`, `nix profile install`, and one-off `nixpkgs.config` tweaks are escape hatches, not workflows. If it survives across rebuilds, it belongs in the config.
- **Flakes when the user already has them.** Do not migrate users off channels mid-troubleshoot. Do not migrate users onto flakes without naming tradeoffs (still experimental upstream, lockfile commits become a habit, registry overrides differ).
- **Generations are the rollback.** Before debugging, confirm the previous generation boots. That is cheaper than chasing ghosts.
- **Store hygiene is boring and scheduled.** Enable `nix.gc.automatic` and `nix.settings.auto-optimise-store = true;` rather than manual sweeps.
- **home-manager has three modes.** Standalone, NixOS module, nix-darwin module. Pick one per host and stay there.
- **nix-darwin is opinionated.** macOS system settings, LaunchDaemons, and Homebrew coexistence are what it owns. Do not treat it like NixOS with a different kernel.
- **Disko and impermanence are declarative recovery.** They shine on fresh installs and nixos-anywhere deploys; retrofitting them onto a live system is a different, harder problem.
- **Secrets never go in the store.** Use sops-nix or agenix with activation-time decryption.
- **Pick Determinate or Lix intentionally.** Both are fine; both add behavior that diverges from upstream Nix in small but real ways. Name the lane.
- **Kernel changes are cross-layer.** ZFS, NVIDIA, hardened kernel, and custom initrd modules all interact. Do not swap `boot.kernelPackages` casually.

---

## Quick Triage Checklist

| Symptom | First checks |
|---------|-------------|
| `nixos-rebuild` evaluation error | `--show-trace`, check option name against the current nixpkgs tag, check `imports` paths |
| Build fails mid-derivation | `--print-build-logs`, check sandbox violations, check unfree or insecure gates |
| Boot drops to emergency shell | previous generation from bootloader menu, check `hardware-configuration.nix`, LUKS, kernel modules |
| Flake input won't update | `nix flake update <name>` (the `nix flake lock --update-input` form is deprecated on Nix 2.30+), check `inputs.<x>.follows`, check registry override |
| System is huge, `/nix/store` fills disk | `nix-collect-garbage -d`, `nix-store --optimise`, prune generations, check direnv GC roots |
| `nix-env -i` installed something that won't stick | user profile vs system config; move to `environment.systemPackages` or `home.packages` |
| home-manager drift vs NixOS | standalone vs module mode, which one owns the file, `home-manager switch` vs `nixos-rebuild switch` |
| Unfree package refuses to build | `nixpkgs.config.allowUnfree = true;` or predicate, or `NIXPKGS_ALLOW_UNFREE=1 nix-build --impure` for one-off |
| Secrets in a module show up world-readable | moved to sops-nix/agenix and re-deploy; rotate the exposed secrets |
| ZFS or NVIDIA breaks after kernel bump | `boot.kernelPackages = pkgs.linuxPackages_<pin>;` or wait for out-of-tree module to rebuild |
| nix-darwin change did not apply | `darwin-rebuild switch`, not `nixos-rebuild`; check `users.users.<name>.home` and `nix.enable` |
| Nothing makes sense | check gotchas reference - channel vs flake mixing, stale lock, overlay collisions, GC of an active dev shell |

---

## Reference Files

- `references/configuration-and-modules.md` - `/etc/nixos/configuration.nix`, modules, options, assertions, `mkMerge` and `mkForce`, NixOS module system
- `references/flakes-and-channels.md` - flakes, `flake.nix` anatomy, inputs and outputs, `flake.lock`, `nix flake` verbs, channels vs flakes vs npins
- `references/rebuild-generations-and-rollback.md` - `nixos-rebuild` verbs, generations, `nix-env --list-generations`, bootloader entries, rollback flow
- `references/home-manager-and-darwin.md` - home-manager (standalone, NixOS module, nix-darwin module), nix-darwin system configuration on macOS
- `references/overlays-packaging-and-overrides.md` - overlays, `overrideAttrs`, `override`, `callPackage`, writing derivations, patching upstream
- `references/store-gc-and-builders.md` - Nix store, `nix-store` vs `nix store`, GC roots, `nix-collect-garbage`, optimise-store, remote builders, Cachix and attic
- `references/dev-shells-and-direnv.md` - `nix-shell`, `nix develop`, `shell.nix`, `default.nix`, flake dev shells, `nix-direnv`, per-project env
- `references/disko-impermanence-and-imaging.md` - disko partitioning, impermanence, nixos-anywhere, SD/ISO images with nixos-generators
- `references/hardware-desktop-and-kernel.md` - nixos-hardware, kernel selection, firmware, GPU drivers, Wayland and X11, display managers
- `references/secrets-sops-and-agenix.md` - sops-nix, agenix, activation-time decryption, age key management, avoiding store-world-readable secrets
- `references/determinate-lix-and-lanes.md` - Determinate Nix (enterprise lane, daemon differences, flakes-on-by-default), Lix (compat-focused fork), coexistence
- `references/gotchas-and-special-situations.md` - recurring NixOS and Nix failure patterns and edge cases

---

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** NIXOS-BTW
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/nixos-btw/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **arch-btw** - Arch and CachyOS administration. Use it when the host is Arch-family and Nix is a side tool, not the system.
- **debian-ubuntu** - Debian-family administration. Use it when Nix runs on Debian/Ubuntu as a user-level package manager only.
- **rhel-fedora** - RHEL-family administration. Use it when Nix runs on Fedora/RHEL as a user-level package manager only.
- **kali-linux** - Kali distro workflow. Use it for Kali, not for Nix inside Kali.
- **command-prompt** - shell syntax, aliases, and one-liners outside Nix expressions.
- **docker** - container runtime and image concerns. This skill builds images with `dockerTools`; **docker** runs them.
- **kubernetes** - cluster workloads once the build output leaves Nix.
- **ansible** - fleet config management when Nix is not the chosen tool for the job.
- **terraform** - IaC for cloud resources that host NixOS VMs; this skill owns the guest.
- **security-audit** - defensive review of a Nix-built artifact.
- **ci-cd** - pipeline design when the CI side of a Nix build (cachix push, remote builders, pipeline stages) is the primary concern.
- **lockpick** - offensive and privesc testing; this skill covers NixOS administration, not exploitation.
- **firewall-appliance** - OPNsense/pfSense appliance work; this skill covers NixOS-based hosts, not BSD appliances.
- **update-docs** - sync docs after substantial module or flake restructuring.

---

## Rules

1. **Identify the Nix lane before prescribing commands.** NixOS vs Nix-on-host, channels vs flakes, Determinate vs upstream vs Lix, standalone vs module home-manager - all change the answer.
2. **Declarative beats imperative.** If the fix is `nix-env -i`, reach for `environment.systemPackages`, `home.packages`, or `nix shell` instead. Hidden profile state is a footgun.
3. **Know the rebuild verb.** `switch`, `test`, `boot`, `dry-activate`, `build-vm`, and `build` are not interchangeable. `test` does not persist across reboot; `boot` does not activate now.
4. **Preserve a known-good generation.** Never GC aggressively right after a rebuild. Boot the new generation twice before pruning.
5. **Flakes are intentional.** Enable `nix-command flakes` where the user already uses them; do not push migration during troubleshooting.
6. **GC roots are real state.** Dev shells, direnv caches, and CI pins hold them. Check before mass deletion.
7. **Secrets never in the store.** Use sops-nix or agenix with activation-time decryption; anything else ends up world-readable in `/nix/store`.
8. **Module options must exist in the user's nixpkgs tag.** 23.11/24.05/24.11/25.05/25.11 drift is real; confirm with `nix repl` or the options search before recommending.
9. **Overlays compose, not mutate.** `final: prev: { ... }` scope. Do not recommend global profile-level overlays on flake systems.
10. **Kernel and initrd agree.** Do not flip `boot.kernelPackages` on ZFS, NVIDIA, or custom-module systems without a fallback.
11. **Do not touch `system.stateVersion` casually.** It controls migration semantics and is not a "version bump" field.
12. **Disko and impermanence are install-time decisions.** Retrofit is a different, harder conversation.
13. **home-manager mode is sticky.** Pick standalone, NixOS module, or darwin module per host and stay there.
14. **Determinate and Lix diverge at the edges.** Name the lane before suggesting daemon or CLI flags.
15. **Reach for common Nix failure patterns before exotic explanations.** Channel/flake mixing, stale lock, overlay collision, option drift, GC of an active dev shell, and unfree/insecure gates explain a large share of the chaos.

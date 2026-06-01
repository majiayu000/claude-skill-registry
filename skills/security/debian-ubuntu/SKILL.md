---
name: debian-ubuntu
description: >
  · Administer Debian/Ubuntu/Mint/Pop: apt, dpkg, PPAs, snaps, systemd, GRUB, HWE, desktop. Triggers: 'debian', 'ubuntu', 'mint', 'popos', 'apt', 'dpkg', 'ppa'. Not for Arch/Fedora/NixOS.
license: MIT
compatibility: Requires Debian, Ubuntu, or Debian-based distro with apt
metadata:
  source: iuliandita/skills
  date_added: "2026-04-22"
  effort: high
  argument_hint: "[issue-or-subsystem]"
---

# Debian-Ubuntu: Debian and Debian-Based Distro Administration

Administer Debian, Ubuntu, Linux Mint, Pop!_OS, Devuan, and other Debian-derived systems,
with partial coverage for Kali when the question is about base OS administration rather than
security-distro workflow. Focus on Debian stable and Ubuntu LTS first, then layer in
derivative-specific behavior, PPA workflows, snap confinement, Ubuntu HWE, and explicit checks
for derivatives that diverge on init, packaging defaults, or intended use.

**Versions worth pinning** (verified May 2026):

Only pin versions here when they materially affect compatibility or troubleshooting shape. For
ordinary Debian and Ubuntu package work, prefer the live distro lane and package policy over a
stale package-version table.

| Component | Version | Why it matters |
|-----------|---------|----------------|
| Debian stable | 13 (trixie) | current stable baseline and repo behavior |
| Ubuntu LTS | 26.04 (Resolute Raccoon) | current LTS baseline for most Ubuntu guidance |
| Ubuntu interim lane | verify live | interim releases move fast; check the active upgrade path instead of memorizing one short-lived codename |
| Ubuntu HWE lane | verify live | kernel metapackage and hardware-enablement behavior matter more than one exact kernel number |
| NVIDIA driver branch | verify live | proprietary branch choice affects Wayland, gaming, and DKMS behavior |
| Mesa stack | verify live | AMD and Intel graphics behavior tracks the shipped Mesa lane |
| Kernel security | verify live via USN tracker | patch high-severity privesc CVEs promptly; mid-2026 examples to confirm fixed: Copy Fail CVE-2026-31431 (CISA KEV, exploited), Dirty Frag CVE-2026-43284/43500, Fragnesia CVE-2026-46300 (ESP-in-TCP, exploited), ptrace CVE-2026-46333 |

## When to use

- Package management with `apt`, `apt-get`, `dpkg`, `apt-cache`, pinning, or holds
- PPA management on Ubuntu, Mint, or Pop!_OS (`add-apt-repository`, key handling)
- Snap and Flatpak workflow, confinement issues, and alternatives
- systemd service, timer, boot, and journal troubleshooting on Debian-style systems
- GRUB, initramfs, EFI, kernel, and recovery work on Debian or Ubuntu
- Release maintenance: dist-upgrades, HWE transitions, release upgrades (`do-release-upgrade`)
- Desktop stack: Wayland vs X11, GNOME, KDE, Cinnamon, COSMIC, portals, PipeWire, Bluetooth
- Session startup and laptop work: GDM, SDDM, LightDM, suspend/resume, power profiles, hybrid graphics
- GPU and gaming: NVIDIA proprietary vs nouveau, AMD Mesa, Intel, Vulkan, Steam, Proton, Gamescope
- Capture and communication: OBS, WebRTC screen sharing, Discord/Teams, portals, virtual cameras
- Storage: ext4, Btrfs, LUKS, LVM, TRIM, hibernation
- Firmware and hardware enablement: `fwupd`, `ubuntu-drivers`, HWE stacks, backports
- Security: AppArmor profiles, unattended-upgrades, needrestart, debian-security updates
- Remote gaming and input: Moonlight, Sunshine, Steam Remote Play, controllers
- Base Linux ops on Debian-style systems: `journalctl`, `dmesg`, `lsblk`, `update-alternatives`

## When NOT to use

- Shell syntax, quoting, or script portability - use **command-prompt**
- Network architecture, DNS, VPNs, reverse proxies, or firewall design - use **networking**
- Docker, Podman, image builds, or container runtime - use **docker**
- Kubernetes cluster or manifest work - use **kubernetes**
- Fleet-wide Linux configuration via playbooks - use **ansible**
- Security review, vulnerability triage, or offensive testing - use **security-audit** or **lockpick**
- RPM-family distros and tooling - use **rhel-fedora**. That includes RHEL, Fedora, Rocky, AlmaLinux, Oracle Linux, and Amazon Linux.
- Ubuntu Core and snap-only transactional workflows - outside this skill; do not treat them like ordinary apt-managed Ubuntu hosts
- NixOS or declarative system management - use **nixos-btw**
- Kali offensive tooling, pentest workflow, or training-image specifics - use **kali-linux**
- OPNsense or pfSense appliance work - use **firewall-appliance**

---

## AI Self-Check

Before returning Debian or Ubuntu commands, verify:

- [ ] **Distro and release identified**: Debian stable/testing/unstable, Ubuntu LTS/interim, Mint, Pop!_OS, Devuan, Kali, or another derivative. Advice diverges quickly.
- [ ] **Init system identified**: do not assume systemd on Devuan or other Debian derivatives without checking PID 1, service manager, and boot tooling first.
- [ ] **Release model respected**: do not suggest `apt upgrade` when `apt full-upgrade` or `apt dist-upgrade` is required for package transitions. Do not suggest `apt dist-upgrade` casually on Ubuntu without context.
- [ ] **Ubuntu 24.04 -> 26.04 delta accounted for**: Ubuntu 24.04 LTS upgraders inherit 24.10, 25.04, 25.10, and 26.04 changes. Do not treat 26.04 as a small point refresh of 24.04.
- [ ] **Repository state clean**: no broken apt lists, missing GPG keys, or mixed releases without pinning.
- [ ] **Boot stack identified**: GRUB vs other loader, EFI vs BIOS, initramfs generator, and kernel metapackage before changing boot files.
- [ ] **Fallback path exists**: do not remove the only known-good kernel or break the only boot entry on a remote system.
- [ ] **PPA trust boundary respected**: review PPA source, key, and maintenance status before adding.
- [ ] **systemd scope is correct**: distinguish system units from user units and use `systemctl --user` only when appropriate.
- [ ] **Wayland stack is coherent**: compositor, portal backend, Xwayland compatibility, and user-session services line up.
- [ ] **Session startup path identified**: display manager, greeter, or TTY launch path known before debugging env propagation.
- [ ] **Audio stack is coherent**: PipeWire, `pipewire-pulse`, and WirePlumber are not fighting a leftover PulseAudio setup.
- [ ] **Bluetooth path is complete**: `bluetooth.service` alone is not enough if audio routing, trust, pairing, or profile selection is broken.
- [ ] **GPU stack matches hardware**: proprietary NVIDIA vs nouveau vs Mesa. Verify actual driver in use before debugging graphics issues.
- [ ] **Gaming stack includes 32-bit userspace when needed**: Steam and Proton failures often come from missing `i386` graphics libraries.
- [ ] **Capture stack is coherent**: portal backend, PipeWire, WebRTC or Electron client path, and any virtual camera module choice line up.
- [ ] **Suspend and hibernation claims are real**: hibernation advice matches actual swap layout, initramfs resume hook, and Secure Boot state.
- [ ] **AppArmor state is considered**: on Ubuntu, AppArmor denials can silently break services, snaps, or custom binaries.
- [ ] **Snap confinement is not ignored**: when a snap misbehaves, check interfaces and confinement level before reinstalling.
- [ ] **Ubuntu desktop session assumptions are current**: on Ubuntu 26.04 Desktop, do not assume a stock Xorg session or the old `Software & Updates` GUI are present by default.
- [ ] **HWE kernel path is understood**: Ubuntu HWE stacks transition kernel metapackages. Know whether the system tracks `generic` or `hwe`.
- [ ] **Diagnostic errors are not silenced**: do not mask failures with `2>/dev/null` on commands whose error reason matters. Use `2>&1 || true` to surface errors without aborting.
- [ ] **Firmware updates are not conflated with package updates**: `fwupd` and vendor tools (e.g., `system76-firmware`) are separate from `apt upgrade`.
- [ ] **Debian alternatives are checked**: when a command behaves oddly, verify `update-alternatives` for that binary.
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Release support checked**: Debian/Ubuntu/Mint/Pop advice matches current lifecycle and enabled repositories
- [ ] **Third-party repo risk handled**: PPAs, snaps, vendor repos, and pin priorities are explicit

---

## Performance

- Use `apt-cache policy`, `apt list --upgradable`, and targeted installs before broad reinstall attempts.
- Keep package index updates scoped; repeated `apt update` in scripts wastes time and load.
- For slow upgrades, identify held packages and phased updates before forcing resolver choices.


---

## Best Practices

- Do not mix Debian releases or Ubuntu series unless apt pinning is deliberate and documented.
- Snapshot or back up before release upgrades, kernel changes, filesystem work, or bootloader repair.
- Prefer distro packages for core system components; isolate vendor repos to the packages they own.


## Workflow

### Step 1: Identify the distro lane first

| Distro | Default stance | What changes |
|--------|----------------|--------------|
| **Debian stable** | Conservative, pin-oriented | `stable` repo only unless testing/unstable explicitly requested. Backports for select packages. |
| **Debian testing** | Rolling-ish, with freezes | Closer to Ubuntu but without Ubuntu-specific tooling. |
| **Debian unstable (sid)** | True rolling | No release, just `sid`. Higher breakage risk. |
| **Ubuntu LTS** | Default baseline | `do-release-upgrade` for release jumps. Treat Ubuntu 26.04 as the current baseline, but remember that 24.04 LTS upgraders also inherit 24.10, 25.04, and 25.10 changes. HWE kernel optional. Snap presence. |
| **Ubuntu interim** | Short-lived | Common stepping stone into the current LTS. Quick to EOL. |
| **Linux Mint** | Ubuntu LTS derivative | Cinnamon/XFCE focus. Mint-specific repos and update manager. PPAs from Ubuntu often work. |
| **Pop!_OS** | Ubuntu derivative with extras | System76 firmware, COSMIC desktop, Pop repos, `system76-power`. NVIDIA ISO available. |
| **Devuan** | Debian derivative with a major service-model split | Do not assume systemd, `systemctl`, or Ubuntu-style desktop/session plumbing. Verify init and service tooling first. |
| **Kali** | Debian-derived security distro | Fine for base apt, kernel, boot, or service administration, but use **kali-linux** for Kali-specific branches, images, metapackages, training-image workflow, and offensive-distro context. |
| **Other Debian-based** | Confirm repo model | Do not assume vanilla Debian or Ubuntu behavior. |

### Step 2: Gather current system state

```bash
cat /etc/os-release
uname -r
ps -p 1 -o comm=
dpkg-query -W -f='${Package}\t${Version}\n' 'linux-image*' systemd grub-common grub-efi-amd64 2>&1 || true
dpkg -l | grep -E "^ii.*(systemd|grub|pipewire|nvidia|mesa)" | head -15
apt-cache policy
command -v systemctl >/dev/null 2>&1 && systemctl --failed
journalctl -b -p warning..alert 2>&1 || true
findmnt /boot
findmnt /boot/efi
command -v grub-install >/dev/null 2>&1 && grub-install --version
lsblk -f
echo "Session=$XDG_SESSION_TYPE Desktop=$XDG_CURRENT_DESKTOP"
loginctl list-sessions 2>&1 || true
command -v systemctl >/dev/null 2>&1 && systemctl status display-manager 2>&1 || true
command -v systemctl >/dev/null 2>&1 && systemctl --user --failed 2>&1 || true
command -v systemctl >/dev/null 2>&1 && systemctl --user status pipewire pipewire-pulse wireplumber 2>&1 || true
command -v systemctl >/dev/null 2>&1 && systemctl --user status xdg-desktop-portal 2>&1 || true
command -v systemctl >/dev/null 2>&1 && systemctl status apparmor 2>&1 || true
command -v aa-status >/dev/null 2>&1 && aa-status 2>&1 || true
command -v wpctl >/dev/null 2>&1 && wpctl status
command -v bluetoothctl >/dev/null 2>&1 && bluetoothctl show
command -v snap >/dev/null 2>&1 && snap list | head -10
command -v flatpak >/dev/null 2>&1 && flatpak list | head -10
lspci -k | grep -Ei 'vga|3d|display'
journalctl -b | grep -Ei 'nvrm|nvidia|amdgpu|i915|xe|drm' 2>&1 || true
journalctl --user -b | grep -Ei 'portal|pipewire|webrtc|obs' 2>&1 || true
lsmod | grep '^v4l2loopback'
command -v dkms >/dev/null 2>&1 && dkms status
findmnt -t btrfs
command -v systemctl >/dev/null 2>&1 && systemctl status fstrim.timer 2>&1 || true
apt list --upgradable 2>&1 | tail -n +2
```

### Step 3: Load only the relevant reference

If the host is Ubuntu 24.04 LTS or the user is planning a 24.04 -> 26.04 move, load
`references/derivatives-and-hwe.md` early. That path bundles interim-release churn, desktop-session
changes, app swaps, and GUI-tool changes that do not show up if you treat 26.04 like a routine
point upgrade.

| Task type | Reference |
|-----------|-----------|
| `apt`, `dpkg`, pinning, PPAs, snaps, `.deb` handling | `references/packages-and-repos.md` |
| systemd units, timers, journal, overrides | `references/systemd-and-journal.md` |
| GRUB, kernel, initramfs, EFI, recovery | `references/boot-kernel-and-recovery.md` |
| Ubuntu HWE, release upgrades, Debian lanes, Mint/Pop/Devuan/Kali specifics | `references/derivatives-and-hwe.md` |
| Wayland, X11, GNOME, KDE, Cinnamon, COSMIC, PipeWire | `references/desktop-audio-and-bluetooth.md` |
| Display managers, session startup, suspend/resume, power, hybrid graphics | `references/session-display-and-mobile.md` |
| GPU drivers, Vulkan, Steam, Proton, gaming | `references/graphics-and-gaming.md` |
| OBS, WebRTC, screen sharing, virtual cameras | `references/capture-and-sharing.md` |
| ext4, Btrfs, LUKS, LVM, TRIM, hibernation | `references/storage-and-rollback.md` |
| AppArmor, unattended-upgrades, debian-security | `references/security-and-updates.md` |
| Remote gaming, controllers, input | `references/remote-gaming-input-and-tooling.md` |
| Core Linux ops commands and Debian tools | `references/base-linux-and-cli.md` |
| Recurring Debian/Ubuntu failure patterns | `references/gotchas-and-special-situations.md` |

Do not load every reference by default. Pick the one that matches the failure mode, then widen
only if the first layer is clean.

### Step 4: Change one layer at a time

- Fix package state before debugging services that may be broken by stale libraries.
- Fix service configuration before declaring systemd broken.
- Fix mountpoints and loader state before rebuilding initramfs.
- On Ubuntu, separate "vanilla Debian behavior" from "Ubuntu snap/HWE/PPA behavior."
- On Pop!_OS, separate "Ubuntu behavior" from "System76 firmware and power behavior."
- Prefer reversible steps: package holds, backup kernels, `apt-mark`, saved configs.

### Step 5: Validate before closing

```bash
apt-cache policy package_name
systemctl status unit_name
journalctl -u unit_name -b
command -v update-grub >/dev/null 2>&1 && update-grub
command -v grub-install >/dev/null 2>&1 && grub-install --version
```

Reboot only when the boot path is understood and at least one known-good entry remains.

---

## Troubleshooting Pattern

Keep triage cross-layer and boring:

1. Confirm active distro, release, session type, kernel, and package lane.
2. Identify failing layer: package state, system service, user service, boot path, desktop session, graphics, or app.
3. Pull logs before changing config.
4. Change one layer at a time and retest.
5. Prefer known-good baseline over tweak stacking.

Core log sweep:

```bash
journalctl -b -p warning..alert
journalctl --user -b
dmesg --level=err,warn
journalctl -u unit_name -b
journalctl --user -u pipewire -u wireplumber -u xdg-desktop-portal -b
```

Broad pattern sweeps when you need correlation, not first-pass precision:

```bash
journalctl -b | grep -Ei 'nvrm|nvidia|amdgpu|i915|xe|drm' 2>&1 || true
journalctl --user -b | grep -Ei 'portal|pipewire|webrtc|obs' 2>&1 || true
```

When a bug looks desktop-only, compare one clean baseline:

- GNOME vs KDE vs Cinnamon vs COSMIC
- browser WebRTC vs packaged client
- plain game launch vs Gamescope or MangoHud
- stock kernel vs HWE kernel

---

## Default Decisions

- **Debian stable means conservative updates.** Pin when mixing repos. Use backports selectively. Avoid `testing` or `sid` packages on stable without a transition plan.
- **Ubuntu LTS means predictable cadence.** Ubuntu 26.04 is the current baseline, but 24.04 -> 26.04 upgrades bundle three interim releases plus the final LTS delta. Expect bigger desktop, app, and workflow changes than the version jump alone suggests.
- **Ubuntu Desktop assumptions changed in 26.04.** Stock Ubuntu Desktop is Wayland-only, and the old `Software & Updates` GUI is no longer installed by default on new installs. GUI-first troubleshooting advice from 24.04-era blog posts may be wrong on fresh 26.04 systems.
- **Use systemd-native tools first.** Reach for `systemctl`, `journalctl`, `timedatectl`, and `localectl` before distro wrappers.
- **Treat PPAs as exceptions, not defaults.** Review maintainer, signing key, freshness, and package origin before adding one. Remove dead PPAs promptly.
- **Prefer distro packages before third-party repos.** Use Debian backports, Ubuntu official repos, or vendor packages first; escalate to PPAs only when the distro lane is genuinely insufficient.
- **Treat snaps as sandboxed first.** Interface and confinement issues explain more snap failures than package bugs.
- **GRUB and initramfs are one subsystem.** Kernel metapackage, `update-initramfs`, `update-grub`, and EFI fallback all have to agree.
- **Desktop failures are often session failures.** On Wayland, user units, portals, and session env matter as much as the package list.
- **Gaming failures are often stack mismatches.** Wrong driver branch, missing `i386` userspace, absent firmware, or broken Proton path is more common than "Linux gaming is bad."
- **Capture failures are portal/PipeWire failures.** OBS, browser WebRTC, Discord, and Teams often fail at the screencast path.
- **AppArmor is invisible until it is not.** On Ubuntu, check `aa-status` and journal denials when a service or binary mysteriously fails.
- **Firmware is separate from packages.** `fwupd` and vendor tools update hardware firmware. Do not expect `apt upgrade` to fix BIOS or SSD firmware.

---

## Quick Triage Checklist

| Symptom | First checks |
|---------|-------------|
| Package weirdness after install | `apt update` first. Broken dependencies? `apt -f install`. Held packages? `apt-mark showhold`. Mixed releases? `apt-cache policy` |
| Service fails after update | Config merge needed? `ucf` or `dpkg --configure -a`. Check unit overrides and `journalctl -b` |
| Won't boot after kernel work | GRUB menu, fallback kernel, initramfs. From live media, mount root and the ESP, then bind-mount `/dev`, `/proc`, `/sys`, and `/run` before `chroot`; use the boot recovery reference instead of a one-line chroot recipe. |
| PPA broke the system | `ppa-purge` if available, or manual downgrade + remove after checking package origin with `apt-cache policy` |
| Snap app misbehaves | `snap connections`, `snap info`, confinement level, interfaces |
| Desktop weirdness after update | `XDG_SESSION_TYPE`, portal, Xwayland, user services. On Ubuntu 26.04, verify the user is not expecting the old Ubuntu Xorg session to exist by default. |
| Bluetooth audio issues | BlueZ pairing, PipeWire nodes, card profile |
| Game blackscreen/crash | GPU driver (proprietary vs Mesa), Vulkan, Steam `i386` libs, Gamescope/MangoHud |
| Screen share broken | Wayland vs X11, portal backend, PipeWire user units |
| Suspend/resume breaks desktop | Sleep state, GPU logs, lock-screen, display manager |
| NVIDIA/module vanished after kernel change | DKMS drift: `dkms status`, confirm module built for `uname -r`, check HWE transition |
| Nothing makes sense | Check gotchas reference - mixed repos, stale PPAs, DKMS drift, AppArmor denials, HWE metapackage mismatch |

---

## Reference Files

- `references/packages-and-repos.md` - apt workflow, dpkg, pinning, PPAs, snaps, flatpaks, `.deb` handling
- `references/systemd-and-journal.md` - systemd service debugging, unit overrides, user units, journal triage
- `references/boot-kernel-and-recovery.md` - GRUB, kernel metapackages, initramfs, EFI, recovery, and live-ISO chroot
- `references/derivatives-and-hwe.md` - Ubuntu HWE, release upgrades, Debian lane differences, Mint, Pop!_OS, Devuan, and Kali scope notes
- `references/desktop-audio-and-bluetooth.md` - X11 vs Wayland, GNOME, KDE, Cinnamon, COSMIC, portals, PipeWire, Bluetooth
- `references/session-display-and-mobile.md` - GDM, SDDM, LightDM, session env, suspend/resume, power profiles, hybrid graphics
- `references/graphics-and-gaming.md` - NVIDIA, AMD, Intel, Vulkan, Steam, Proton, Gamescope, MangoHud
- `references/capture-and-sharing.md` - OBS, WebRTC screen sharing, Discord/Teams, hardware encoding, virtual cameras
- `references/storage-and-rollback.md` - ext4, Btrfs, LUKS, LVM, TRIM, hibernation, resume
- `references/security-and-updates.md` - AppArmor, unattended-upgrades, debian-security, needrestart
- `references/remote-gaming-input-and-tooling.md` - Moonlight, Sunshine, controllers, Steam Remote Play
- `references/base-linux-and-cli.md` - core Linux inspection commands and Debian tools such as `update-alternatives`
- `references/gotchas-and-special-situations.md` - recurring Debian/Ubuntu failure patterns and edge cases

---

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** DEBIAN-UBUNTU
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/debian-ubuntu/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **command-prompt** - shell syntax, zsh or bash behavior, script portability
- **networking** - network services, DNS, VPNs, firewall design
- **docker** - container runtime and image concerns instead of host distro administration
- **kubernetes** - cluster and manifest work that sits above host OS administration
- **ansible** - codifying Linux changes across many machines
- **security-audit** - hardening and security review rather than normal package/service administration
- **rhel-fedora** - RPM-family distro administration rather than Debian-family behavior
- **nixos-btw** - NixOS and declarative Nix system management rather than apt-based administration
- **kali-linux** - Kali-specific branch, image, and offensive-workflow concerns
- **firewall-appliance** - OPNsense and pfSense appliance work rather than Linux host administration
- **arch-btw** - Arch Linux and CachyOS administration (the upstream inspiration for this skill)
- **update-docs** - after substantial system administration changes that introduce new operational gotchas

---

## Rules

1. **Identify the distro and release before prescribing commands.** Debian stable, testing, sid, Ubuntu LTS or interim, Mint, Pop!_OS, Devuan, and Kali differ where it matters: repos, init systems, kernels, and recovery assumptions.
2. **No mixed-release advice without pinning context.** Adding `testing` or `sid` sources to Debian stable without apt pinning is usually wrong.
3. **Keep PPAs in perspective.** Prefer distro packages, Debian backports, or vendor-supported repos first. Use PPAs only when the distro lane is genuinely insufficient, and verify package origin before adding one.
4. **Know the boot chain before touching it.** Confirm GRUB stage, ESP mount, kernel metapackage, initramfs hooks, and EFI fallback path first.
5. **Never remove the last known-good kernel path casually.** Especially on remote or encrypted systems.
6. **Prefer systemd-native diagnostics.** `systemctl`, `journalctl`, and `update-grub` usually tell you more than distro wrappers or generic forum folklore.
7. **Ubuntu 26.04 changed some desktop defaults in ways that affect support.** Do not assume a stock Ubuntu Xorg session, the old `Software & Updates` GUI, or 24.04-era desktop app names are still present on fresh installs.
8. **Ubuntu HWE is opt-in complexity.** Treat HWE kernels as additions that must be validated, not magic defaults.
9. **For Wayland issues, inspect the user session first.** Portals, user units, and Xwayland compatibility usually matter more than package reinstall churn.
10. **For gaming issues, identify the GPU vendor and userspace first.** Driver branch, Vulkan stack, `i386` multilib, and launch wrappers usually explain more than random tweak cargo cults.
11. **For capture issues, debug portals and PipeWire before app folklore.** OBS, browser WebRTC, Discord, and Teams often fail at the screencast path.
12. **AppArmor can silently break things.** On Ubuntu, check `aa-status` and AppArmor denials when a service or binary mysteriously fails.
13. **Do not oversell hibernation or resume.** These depend on exact swap layout, initramfs resume hook, and Secure Boot state.
14. **Reach for common Debian/Ubuntu failure patterns before exotic explanations.** Mixed repos, stale PPAs, DKMS drift, AppArmor denials, HWE metapackage mismatch, and snap confinement explain a large share of the chaos.

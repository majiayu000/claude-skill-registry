---
name: rhel-fedora
description: >
  · Administer RHEL/Fedora/CentOS/Rocky/Alma/Amazon Linux: dnf, yum, SELinux, firewalld, dracut. Triggers: 'rhel', 'fedora', 'centos stream', 'rocky', 'dnf', 'selinux'. Not for other distros.
license: MIT
compatibility: Requires Fedora, RHEL, or RHEL-family distro with dnf, yum, or rpm
metadata:
  source: iuliandita/skills
  date_added: "2026-04-22"
  effort: high
  argument_hint: "[issue-or-subsystem]"
---

# RHEL-Fedora: Fedora and RHEL-Family Administration

Administer Fedora, RHEL, Rocky Linux, AlmaLinux, Oracle Linux, Amazon Linux, and nearby
RPM-family systems without flattening their important differences. Start by separating the
fast-moving Fedora lane from the conservative enterprise lane, then account for vendor quirks
such as subscription-manager, CentOS Stream drift, Oracle UEK, Amazon's cloud-first defaults,
and SELinux or firewalld behavior that people love to blame on the wrong layer.

**Versions worth pinning** (verified May 2026):

Only pin versions here when they materially affect compatibility or troubleshooting shape. For
ordinary package work, prefer the live distro lane and repo state over a stale package table.

| Component | Version | Why it matters |
|-----------|---------|----------------|
| Fedora stable | 44 / verify live | current mainstream baseline (Fedora ships ~every 6 months and EOLs ~13 months, faster than this table is bumped - confirm live) |
| Fedora next branch | 45 / verify live | useful when a bug is really Fedora-next behavior |
| RHEL enterprise lane | 10.x | current enterprise baseline in the new major lane |
| RHEL previous major | 9.x | still widely deployed and behaviorally different from 10 |
| Rocky Linux | verify live major lane | close to RHEL, but current docs and vault state still matter |
| AlmaLinux | verify live major lane | close to RHEL, but current release notes and policy docs still matter |
| Oracle Linux | verify live major lane | current Oracle lane matters, but UEK vs RHCK matters more |
| Amazon Linux | AL2023 / verify live release | release-note lane matters more than memorizing one point version |
| SELinux | verify live | policy package and mode matter more than memorized version strings |
| DNF | verify live | Fedora moves faster than enterprise lanes; DNF 5 vs legacy expectations matter |
| Podman | verify live | rootless and quadlet behavior depend on the shipped distro lane |
| Kernel security | verify live via RHSA/FEDORA tracker | patch high-severity privesc CVEs promptly; mid-2026 examples to confirm fixed: Copy Fail CVE-2026-31431 (CISA KEV, exploited), Dirty Frag CVE-2026-43284/43500, Fragnesia CVE-2026-46300 (ESP-in-TCP, exploited), ptrace CVE-2026-46333 |

## When to use

- Package management with `dnf`, `yum`, `rpm`, local `.rpm` files, repo configuration, or package provenance
- Fedora repo, COPR, updates-testing, modularity, and release-upgrade work
- RHEL subscription, entitlement, CodeReady Builder, Insights, EPEL, and clone compatibility questions
- systemd service, timer, boot, and journal troubleshooting on Fedora or RHEL-family systems
- GRUB, EFI, `dracut`, initramfs, kernel, `grubby`, and boot recovery work
- Release maintenance: Fedora `dnf system-upgrade`, RHEL-family major or minor transitions, `leapp` planning
- Security plumbing: SELinux modes, contexts, booleans, AVC denials, `firewalld`, FIPS-adjacent checks, package signing
- Container-host work that is really host-admin work: Podman packages, rootless prerequisites, cgroup or SELinux host integration
- Desktop stack on Fedora Workstation or similar: Wayland vs X11, GNOME, KDE, portals, PipeWire, Bluetooth
- Session startup and laptop work: GDM, SDDM, suspend or resume, power profiles, hybrid graphics
- GPU and gaming work: NVIDIA akmods or DKMS, Mesa, Vulkan, Steam, Proton, Gamescope, MangoHud
- Capture and communication: OBS, WebRTC screen sharing, Discord or Teams, portals, virtual cameras
- Storage: XFS, ext4, Btrfs, LUKS, LVM, Stratis, TRIM, hibernation
- Firmware and hardware enablement: `fwupdmgr`, vendor firmware tools, microcode, `mokutil`, Secure Boot
- Cloud-image and VM defaults on Amazon Linux, RHEL cloud images, Rocky, Alma, and Oracle Linux guests
- Base Linux ops on RPM-family systems: `journalctl`, `dmesg`, `lsblk`, `grubby`, `rpm -Va`, `restorecon`

## When NOT to use

- Shell syntax, quoting, or script portability - use **command-prompt**
- Network architecture, DNS, VPNs, reverse proxies, or firewall design - use **networking**
- Dockerfiles, Compose files, image builds, or container runtime architecture - use **docker**
- Kubernetes cluster or manifest work - use **kubernetes**
- Fleet-wide Linux configuration via playbooks - use **ansible**
- Security review, vulnerability triage, or offensive testing - use **security-audit** or **lockpick**
- Arch, CachyOS, or other pacman-family systems - use **arch-btw**
- Debian, Ubuntu, Mint, Pop!_OS, or other apt-family systems - use **debian-ubuntu**
- Fedora Silverblue, Kinoite, Bazzite, Bluefin, Universal Blue, CoreOS, bootc, or other rpm-ostree / image-mode workflows - outside this skill; do not treat them like ordinary dnf-managed hosts
- OPNsense or pfSense appliance work - use **firewall-appliance**

---

## AI Self-Check

Before returning Fedora or RHEL-family commands, verify:

- [ ] **Distro lane identified**: Fedora, CentOS Stream, RHEL, Rocky, AlmaLinux, Oracle Linux, Amazon Linux, or another derivative. Advice diverges fast.
- [ ] **Release lane identified**: Fedora stable vs Rawhide/Branched, RHEL 8 vs 9 vs 10, AL2023 vs old Amazon Linux 2, Oracle Linux with RHCK vs UEK.
- [ ] **Package path identified**: `dnf`, legacy `yum`, plain `rpm`, or `microdnf`. If the host is rpm-ostree or image-mode, stop and route away instead of treating it like a normal DNF-managed host.
- [ ] **Repo provenance understood**: base repos, EPEL, CRB/PowerTools/CodeReady Builder, COPR, vendor repos, and third-party release RPMs are not interchangeable.
- [ ] **Fedora speed respected**: Fedora guidance that is fine on 42 can be stale or wrong on Rawhide and too new for enterprise clones.
- [ ] **Enterprise conservatism respected**: do not blindly transplant Fedora COPR, raw upstream kernels, or random GitHub RPM repos onto production RHEL-family hosts.
- [ ] **SELinux considered early**: if the symptom smells like permission, bind mount, custom service, rootless container, or web app weirdness, check AVCs before disabling SELinux.
- [ ] **SELinux fix is correct**: distinguish labeling (`restorecon`, `semanage fcontext`) from booleans (`setsebool`) and custom policy (`audit2allow`). Do not cargo-cult `setenforce 0`.
- [ ] **firewalld scope is correct**: runtime vs permanent rules, active zone, interface binding, and rich rules are understood before changing exposure.
- [ ] **Boot stack identified**: GRUB, EFI mountpoint, kernel package, `dracut`, Secure Boot state, and `grubby` path are known before changing boot files.
- [ ] **Fallback path exists**: do not remove the only known-good kernel or boot entry on a remote system.
- [ ] **Vendor kernel path identified**: Oracle UEK vs RHCK, Amazon kernel choices, and NVIDIA akmods/DKMS expectations matter.
- [ ] **Subscription state known**: on RHEL, entitlement and repo enablement may be the real problem, not package naming.
- [ ] **Module streams handled consciously**: if AppStream or module streams are involved, verify the active stream before suggesting installs, resets, or downgrades.
- [ ] **Desktop stack is coherent**: compositor, portal backend, PipeWire, session type, and user services line up.
- [ ] **Gaming stack includes 32-bit userspace when needed**: Steam and Proton failures often come from missing multilib graphics pieces, not the game itself.
- [ ] **Capture stack is coherent**: portal backend, PipeWire, WebRTC or Electron path, and any virtual camera module line up with the current session type.
- [ ] **Cloud-image assumptions are checked**: Amazon Linux, cloud-init images, and minimal RHEL images omit tools you might expect on a full install.
- [ ] **Upgrade path is real**: Fedora `dnf system-upgrade`, RHEL `leapp`, and clone major-version jumps have different support stories. Do not improvise an in-place major upgrade path.
- [ ] **Diagnostic errors are not silenced**: do not hide useful failure output with `2>/dev/null` on commands whose errors matter. Use `2>&1 || true` when gathering.
- [ ] **Version table treated as a hint, not gospel**: if the pinned table is getting old, verify distro release and key package versions live before leaning on it.
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Lifecycle checked**: RHEL, Fedora, Rocky, Alma, CentOS Stream, and Amazon Linux guidance matches the target release
- [ ] **SELinux/firewalld context preserved**: fixes do not disable enforcement permanently as a shortcut

---

## Performance

- Use `dnf repoquery`, `dnf history`, and targeted transactions before broad package churn.
- Keep metadata/cache refresh intentional; repeated full refreshes slow automation.
- For service issues, inspect journal, SELinux AVCs, and firewalld zones before reinstalling packages.


---

## Best Practices

- Snapshot or back up before release upgrades, bootloader work, storage changes, or major SELinux relabels.
- Prefer policy modules or correct labels over `setenforce 0` as a permanent fix.
- Do not mix clone/vendor repositories without explicit priority and compatibility decisions.


## Workflow

### Step 1: Identify the distro lane first

| Distro | Default stance | What changes |
|--------|----------------|--------------|
| **Fedora stable** | Fast-moving workstation or server baseline | DNF 5 era, COPR exists, frequent rebases, shorter support window |
| **Fedora Rawhide / Branched** | Slow down | Pre-release behavior, docs and package names can move under you |
| **CentOS Stream** | Treat as ahead-of-RHEL, not equal-to-RHEL | Preview-ish enterprise lane; package timing and bugs can differ |
| **RHEL** | Conservative enterprise baseline | Subscription-manager, repo entitlements, supported upgrade paths |
| **Rocky Linux** | Conservative clone baseline | No subscription-manager, vault behavior, fast follow after upstream |
| **AlmaLinux** | Conservative clone baseline with its own policies | Mostly RHEL-shaped, but do not pretend it is literally identical |
| **Oracle Linux** | Check kernel lane immediately | UEK vs RHCK changes driver, storage, and support assumptions |
| **Amazon Linux 2023** | Cloud-first, vendor-shaped lane | Fedora-derived userland with AWS defaults, no blind RHEL-copying |
| **Other RPM-based** | Confirm repo and support model | Do not assume Fedora or RHEL rules without evidence |

### Step 2: Gather current system state

```bash
cat /etc/os-release
uname -r
rpm -E '%{?rhel} %{?fedora}'
rpm -q systemd rpm dnf grub2-common dracut selinux-policy-targeted 2>&1 || true
dnf --version 2>&1 || yum --version 2>&1 || true
rpm -qa | grep -E '^(kernel|kernel-core|kernel-uek|dnf|yum|podman|firewalld|selinux-policy)' | head -20
rpm -qf /etc/redhat-release 2>&1 || true
dnf repolist --enabled 2>&1 || yum repolist enabled 2>&1 || true
dnf module list --enabled 2>&1 || true
subscription-manager status 2>&1 || true
subscription-manager repos --list-enabled 2>&1 || true
systemctl --failed 2>&1 || true
journalctl -b -p warning..alert 2>&1 || true
getenforce 2>&1 || true
sestatus 2>&1 || true
ausearch -m avc -ts boot 2>&1 || true
firewall-cmd --get-active-zones 2>&1 || true
firewall-cmd --list-all 2>&1 || true
findmnt /boot
findmnt /boot/efi
grubby --default-kernel 2>&1 || true
grubby --info=ALL 2>&1 || true
lsblk -f
echo "Session=$XDG_SESSION_TYPE Desktop=$XDG_CURRENT_DESKTOP"
loginctl list-sessions 2>&1 || true
systemctl status display-manager 2>&1 || true
systemctl --user --failed 2>&1 || true
systemctl --user status pipewire pipewire-pulse wireplumber 2>&1 || true
systemctl --user status xdg-desktop-portal 2>&1 || true
command -v wpctl >/dev/null 2>&1 && wpctl status
command -v bluetoothctl >/dev/null 2>&1 && bluetoothctl show
lspci -k | grep -Ei 'vga|3d|display'
journalctl -b | grep -Ei 'nvrm|nvidia|amdgpu|i915|xe|drm' 2>&1 || true
journalctl --user -b | grep -Ei 'portal|pipewire|webrtc|obs' 2>&1 || true
lsmod | grep '^v4l2loopback' 2>&1 || true
command -v akmods >/dev/null 2>&1 && akmods --force --kernels "$(uname -r)" --test 2>&1 || true
command -v dkms >/dev/null 2>&1 && dkms status 2>&1 || true
findmnt -t btrfs,xfs,ext4
systemctl status fstrim.timer 2>&1 || true
fwupdmgr get-devices 2>&1 || true
dnf check-update 2>&1 || true
```

### Step 3: Load only the relevant reference

| Task type | Reference |
|-----------|-----------|
| `dnf`, `yum`, `rpm`, repo config, EPEL, COPR, modules, local RPMs | `references/packages-and-repos.md` |
| systemd units, timers, journal, overrides | `references/systemd-and-journal.md` |
| GRUB, kernel, `dracut`, EFI, `grubby`, recovery | `references/boot-kernel-and-recovery.md` |
| Fedora vs RHEL vs Rocky vs Alma vs Oracle vs Amazon behavior | `references/derivatives-and-vendor-quirks.md` |
| Wayland, X11, GNOME, KDE, PipeWire, Bluetooth | `references/desktop-audio-and-bluetooth.md` |
| Display managers, session startup, suspend or resume, power, hybrid graphics | `references/session-display-and-mobile.md` |
| GPU drivers, Vulkan, Steam, Proton, gaming | `references/graphics-and-gaming.md` |
| OBS, WebRTC, screen sharing, virtual cameras | `references/capture-and-sharing.md` |
| XFS, ext4, Btrfs, LUKS, LVM, Stratis, TRIM, hibernation | `references/storage-and-rollback.md` |
| SELinux, firewalld, package signing, updates, compliance-adjacent checks | `references/security-and-updates.md` |
| Remote gaming, controllers, input | `references/remote-gaming-input-and-tooling.md` |
| Core Linux inspection commands and RPM-family tools | `references/base-linux-and-cli.md` |
| Recurring Fedora and RHEL-family failure patterns | `references/gotchas-and-special-situations.md` |

Do not load every reference by default. Pick the one that matches the failure mode, then widen
only if the first layer is clean.

### Step 4: Change one layer at a time

- Fix repo and package state before debugging services that may be broken by wrong package sets.
- Fix SELinux labeling or policy before declaring the app broken.
- Fix `firewalld` exposure before blaming service startup.
- Fix mountpoints and loader state before rebuilding `dracut` or changing kernels.
- On Fedora, separate "upstream fast-moving distro behavior" from "third-party repo or COPR behavior."
- On RHEL, separate "package unavailable" from "repo entitlement disabled."
- On Oracle Linux, confirm UEK vs RHCK before chasing driver and storage symptoms.
- On Amazon Linux, separate cloud-image defaults and AWS repo choices from generic RHEL folklore.
- Prefer reversible steps: keep old kernels, save `.repo` files, snapshot if available, preserve SELinux context fixes in policy rather than one-off `chcon` hacks.

### Step 5: Validate before closing

```bash
rpm -q package_name
rpm -V package_name
systemctl status unit_name
journalctl -u unit_name -b
getenforce
sestatus
firewall-cmd --list-all
grubby --default-kernel
```

Reboot only when the boot path is understood and at least one known-good entry remains.

---

## Troubleshooting Pattern

Keep triage cross-layer and boring:

1. Confirm active distro, release lane, package manager, kernel lane, and repo state.
2. Identify the failing layer: repo/package state, SELinux, firewall, system service, user service, boot path, desktop session, graphics, or app.
3. Pull the right logs before changing config.
4. Change one layer at a time and retest.
5. Prefer known-good baseline over tweak stacking.

Core log sweep:

```bash
journalctl -b -p warning..alert
journalctl --user -b
dmesg --level=err,warn
journalctl -u unit_name -b
ausearch -m avc -ts recent
```

Broad pattern sweeps when you need correlation, not first-pass precision:

```bash
journalctl -b | grep -Ei 'nvrm|nvidia|amdgpu|i915|xe|drm' 2>&1 || true
journalctl --user -b | grep -Ei 'portal|pipewire|webrtc|obs' 2>&1 || true
ausearch -m avc -ts boot 2>&1 || true
```

When a bug looks desktop-only, compare one clean baseline:

- GNOME vs KDE
- browser WebRTC vs packaged client
- plain game launch vs Gamescope or MangoHud
- RHCK vs UEK on Oracle Linux when kernel behavior is suspect
- stock repo package vs third-party repo package

---

## Default Decisions

- **Fedora means fast change.** Verify the exact release and avoid stale blog-fix cargo cults.
- **RHEL means support boundaries matter.** Check entitlements, supported repos, and documented upgrade paths before inventing one.
- **Clones are close, not identical in process.** Rocky, AlmaLinux, Oracle Linux, and Amazon Linux can share RPM names while differing in policy, repos, kernels, and support tooling.
- **Use systemd-native tools first.** Reach for `systemctl`, `journalctl`, `loginctl`, and `timedatectl` before wrappers.
- **Treat SELinux as signal, not as the enemy.** AVC denials usually tell you exactly which layer is wrong.
- **Treat `firewalld` as stateful plumbing.** Zone, runtime, permanent state, and service definitions all matter.
- **GRUB, kernel, and `dracut` are one subsystem.** Kernel package, initramfs, Secure Boot state, and bootloader entries have to agree.
- **Desktop failures are often session failures.** On Wayland, user units, portals, and session env matter as much as the package list.
- **Gaming failures are often stack mismatches.** Wrong driver branch, missing 32-bit userspace, absent firmware, or a broken Proton path is more common than the game being the real problem.
- **Cloud images are intentionally skinny.** Missing packages and disabled services are often by design, not corruption.

---

## Quick Triage Checklist

| Symptom | First checks |
|---------|-------------|
| Package weirdness after install | `dnf repolist`, `dnf check`, `rpm -q`, module stream mismatch, third-party repo drift |
| Package unavailable on RHEL | entitlement or CRB missing? `subscription-manager repos --list-enabled`, repo enablement, EPEL assumptions |
| SELinux broke my app | `getenforce`, `ausearch -m avc -ts recent`, labeling vs boolean vs policy module |
| Service fails after update | repo drift, dropped config, `systemctl status`, `journalctl -b`, `rpm -V package` |
| Won't boot after kernel work | EFI mount, `grubby --info=ALL`, `dracut` image, Secure Boot, fallback kernel |
| Fedora upgrade weirdness | exact Fedora release, `dnf system-upgrade` state, third-party repos, COPR packages |
| RHEL clone behaves oddly | clone-specific release docs, vault state, EPEL assumptions, unsupported in-place upgrade folklore |
| Oracle Linux issue | RHCK vs UEK first, then driver/storage/virtualization path |
| Amazon Linux mismatch | AL2023 vs AL2, cloud-init defaults, AWS package docs, missing extra repos |
| Desktop weirdness after update | `XDG_SESSION_TYPE`, portal, Xwayland, user services |
| Bluetooth audio issues | BlueZ pairing, PipeWire nodes, card profile |
| Game blackscreen/crash | GPU driver, Vulkan, multilib graphics libs, Gamescope/MangoHud |
| Screen share broken | Wayland vs X11, portal backend, PipeWire user units |
| Suspend/resume breaks desktop | sleep state, GPU logs, lock-screen, display manager |
| NVIDIA/module vanished after kernel change | akmods or DKMS drift, Secure Boot signing, current kernel vs installed module |
| Nothing makes sense | check gotchas reference - repo drift, SELinux labeling, module stream confusion, stale third-party repos, and kernel lane mismatch explain a lot |

---

## Reference Files

- `references/packages-and-repos.md` - DNF, YUM, RPM, local packages, repo files, EPEL, COPR, modules, and package provenance
- `references/systemd-and-journal.md` - systemd service debugging, unit overrides, user units, journal triage, and safe edit flow
- `references/boot-kernel-and-recovery.md` - GRUB, `dracut`, kernel packages, `grubby`, EFI, Secure Boot, and recovery workflow
- `references/derivatives-and-vendor-quirks.md` - Fedora, CentOS Stream, RHEL, Rocky, AlmaLinux, Oracle Linux, and Amazon Linux differences that actually matter
- `references/desktop-audio-and-bluetooth.md` - X11 vs Wayland, GNOME and KDE notes, portals, PipeWire, and Bluetooth troubleshooting
- `references/session-display-and-mobile.md` - GDM, SDDM, session env, suspend or resume, power profiles, and hybrid graphics routing
- `references/graphics-and-gaming.md` - NVIDIA, AMD, Intel, Vulkan, Steam, Proton, Gamescope, MangoHud, and akmods or DKMS notes
- `references/capture-and-sharing.md` - OBS, WebRTC screen sharing, Discord or Teams routing, hardware encoding, and virtual camera troubleshooting
- `references/storage-and-rollback.md` - XFS, ext4, Btrfs, LUKS, LVM, Stratis, TRIM, hibernation, and rollback boundaries
- `references/security-and-updates.md` - SELinux, firewalld, package signing, updates, FIPS-adjacent concerns, and compliance-sensitive defaults
- `references/remote-gaming-input-and-tooling.md` - Moonlight, Sunshine, controllers, and Steam Remote Play
- `references/base-linux-and-cli.md` - core Linux inspection commands and RPM-family tools such as `rpm -Va`, `repoquery`, and `restorecon`
- `references/gotchas-and-special-situations.md` - recurring Fedora and RHEL-family failure patterns, special cases, and what-to-do-next guidance

---

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** RHEL-FEDORA
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/rhel-fedora/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **command-prompt** - shell syntax, zsh or bash behavior, script portability
- **networking** - network services, DNS, VPNs, firewall design beyond host-level `firewalld`
- **docker** - container runtime and image concerns instead of host distro administration
- **kubernetes** - cluster and manifest work that sits above host OS administration
- **ansible** - codifying Linux changes across many machines
- **security-audit** - hardening and security review rather than normal package and service administration
- **arch-btw** - Arch Linux and CachyOS administration (same operating-system-admin pattern, different package and release model)
- **debian-ubuntu** - Debian and Ubuntu administration (same operating-system-admin pattern, different package and distro family)
- **update-docs** - after substantial system administration changes that introduce new operational gotchas

---

## Rules

1. **Identify the distro and release lane before prescribing commands.** Fedora, CentOS Stream, RHEL, Rocky, AlmaLinux, Oracle Linux, and Amazon Linux differ where it matters: repos, kernels, support tooling, and upgrade paths.
2. **Do not flatten Fedora and RHEL into one thing.** Fedora is the fast lane. Enterprise clones are not just "older Fedora" with different branding.
3. **Know the package origin before changing package state.** Repo enablement, release RPMs, module streams, and third-party repos explain a lot of RPM-family chaos.
4. **Treat SELinux denials as first-class evidence.** Check AVCs before disabling enforcement or blaming the app.
5. **Use the right SELinux fix.** Prefer proper labeling, booleans, or policy modules over permanent `setenforce 0` and random `chcon` drift.
6. **Know the boot chain before touching it.** Confirm GRUB stage, EFI mount, kernel package, `dracut`, Secure Boot, and `grubby` state first.
7. **Never remove the last known-good kernel path casually.** Especially on remote, encrypted, or cloud systems.
8. **Prefer systemd-native diagnostics.** `systemctl`, `journalctl`, `loginctl`, and `grubby` usually tell you more than forum folklore.
9. **Be conservative with third-party repos.** COPR on Fedora, EPEL on enterprise clones, vendor RPM repos, and release packages all change the support boundary.
10. **For desktop and capture issues, inspect the user session first.** Portals, PipeWire, user units, and Xwayland compatibility usually matter more than random reinstall churn.
11. **For gaming issues, identify the GPU vendor, kernel lane, and userspace first.** Driver branch, Vulkan stack, multilib, Secure Boot, and launch wrappers usually explain more than tweak cargo cults.
12. **Do not improvise major upgrades.** Fedora major jumps, RHEL `leapp`, and clone major-version moves require a documented path or a rebuild plan.
13. **Reach for common RPM-family failure patterns before exotic explanations.** Repo drift, SELinux labeling mistakes, module stream confusion, akmods or DKMS drift, and kernel-lane mismatch explain a large share of the chaos.

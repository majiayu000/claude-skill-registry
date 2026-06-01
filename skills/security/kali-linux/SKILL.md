---
name: kali-linux
description: >
  · Administer Kali: apt, branches, metapackages, images, live USB persistence, NetHunter, wireless/GPU. Triggers: 'kali', 'kali rolling', 'kali snapshot', 'kali-tweaks', 'nethunter'.
license: MIT
compatibility: "Requires Kali Linux or Kali images with apt and Kali repositories"
metadata:
  source: iuliandita/skills
  date_added: "2026-04-22"
  effort: high
  argument_hint: "[issue-or-workflow]"
---

# Kali Linux: Kali Administration, Tooling, and Lab Workflow

Administer Kali Linux without flattening it into plain Debian or into a bag of offensive tools.
Start by identifying which Kali lane you are actually on - rolling install, last-snapshot,
live USB, VM image, Purple image, NetHunter, or a throwaway lab box - then separate base OS
health from tool-selection questions, branch hygiene, hardware support, and engagement scope.
Kali is Debian-shaped, but the places where it goes wrong are usually Kali-specific: branch
mixing, metapackage sprawl, stale images, persistence mistakes, hardware edge cases, or people
using the wrong tool family for the job.

**Target versions** (verified May 2026):

Only pin versions or dated anchors here when they materially affect compatibility or
troubleshooting shape. For ordinary package work, prefer the live branch and repo state over a
stale package table.

| Component | Version or date | Why it matters |
|-----------|-----------------|----------------|
| **Current dated Kali image release** | 2026.1 | current image baseline and release notes |
| Branch docs | May 2026 recheck / verify live | branch behavior and safe lane selection matter more than a single package version |
| Metapackage docs | 2025-07 / verify live | tool-family grouping and install scope matter more than memorizing one package list |
| Kali 2026.1 kernel lane | 6.18 | release-image baseline for hardware and driver expectations |

## When to use

- Package management on Kali with `apt`, `dpkg`, `apt-cache`, repo sanity checks, keyrings, or branch validation
- Kali image and install questions: live ISO, netinst, ARM and SBC images, VM images, persistence, and recovery
- Kali branch and source-list questions: `kali-rolling`, `kali-last-snapshot`, selective branch use, and mirror hygiene
- Metapackage planning: `kali-linux-default`, `kali-linux-everything`, focused `kali-tools-*` bundles, desktop metapackages, and `kali-tweaks`
- Selecting the right Kali tool family for the job before installing half the archive by accident
- Kali desktop and laptop work: Xfce, GNOME, KDE, i3, PipeWire, GPU drivers, capture tooling, and VM guest behavior
- Wireless, SDR, Bluetooth, RFID, HID, USB, and offensive-hardware support that is really a Kali host or package problem
- NetHunter and mobile-adjacent Kali questions where the issue is image, package, kernel, or host-tooling shape rather than exploit technique
- Safe lab setup, intentionally vulnerable practice targets, snapshot workflow, and separation between lab and production systems
- Base Linux ops on Kali when the Kali-specific repo, branch, image, or tool context matters more than generic Debian advice

## When NOT to use

- Generic Debian, Ubuntu, Mint, or Pop!_OS administration without Kali-specific context - use **debian-ubuntu**
- Shell syntax, quoting, or script portability - use **command-prompt**
- Network architecture, DNS, VPNs, reverse proxies, or firewall design - use **networking**
- Docker, Podman, image builds, or container runtime issues - use **docker**
- Hypervisor configuration, passthrough wiring, or VM platform issues where the fault is clearly outside the Kali guest - use **virtualization**
- Kubernetes cluster or manifest work - use **kubernetes**
- Fleet-wide Linux configuration via playbooks - use **ansible**
- Exploitation, privilege escalation, lateral movement, or post-exploitation on live targets - use **lockpick**
- Novel vulnerability hunting, reverse engineering depth work, fuzzing, or proof-of-concept research - use **zero-day**
- Defensive hardening, vuln triage, or broad security review - use **security-audit**
- OPNsense or pfSense appliance work - use **firewall-appliance**

---

## AI Self-Check

Before returning Kali commands or tool recommendations, verify:

- [ ] **Kali lane identified**: rolling install, last-snapshot, live USB, VM image, Purple image, NetHunter, or a custom lab box. Advice diverges fast.
- [ ] **Not flattened into plain Debian**: do not give generic Debian advice without checking Kali branches, metapackages, and package origin first.
- [ ] **Branch model understood**: `kali-rolling` vs `kali-last-snapshot` vs partial or development branches such as `kali-experimental`, `kali-bleeding-edge`, and `kali-dev`. Do not mix them casually.
- [ ] **Repo state is clean**: no blind Debian repo additions, no stale image assumptions, no broken `kali-archive-keyring`, and no contradictory source lists.
- [ ] **Upgrade path is coherent**: prefer `apt update` plus `apt full-upgrade` on Kali when package transitions matter. Do not cargo-cult `apt upgrade` and call it done.
- [ ] **Image mode identified**: installed system, live media, persistence-backed live media, VM image, or mobile image. Recovery steps differ.
- [ ] **Metapackage scope is intentional**: do not suggest `kali-linux-everything` when a focused `kali-tools-*` bundle is the sane answer.
- [ ] **Tool family matches the task**: information gathering, vulnerability assessment, web, passwords, wireless, reverse engineering, exploitation, post-exploitation, forensics, reporting, or labs.
- [ ] **Authorization boundary respected**: Kali tool recommendations still require authorized scope. A tool index is not permission.
- [ ] **Lab packages are treated as intentionally vulnerable**: `kali-linux-labs` exists for controlled practice, not for everyday workstation installs.
- [ ] **Wireless and hardware path is real**: chipset, firmware, monitor mode, injection support, SDR stack, USB passthrough, and kernel modules match the actual hardware.
- [ ] **GPU and capture stack is coherent**: VM passthrough, host acceleration, PipeWire, browser capture, and desktop session line up before blaming the tool.
- [ ] **NetHunter is not treated like normal desktop Kali**: mobile kernels, Android host constraints, rootless vs full chroot shape, and missing systemd-style tooling can change which checks even make sense.
- [ ] **Correct handoff chosen**: once the question becomes exploitation methodology, route to **lockpick**. Once it becomes original vulnerability discovery, route to **zero-day**.
- [ ] **Diagnostic errors are not silenced**: do not hide useful failure output with `2>/dev/null` on commands whose error reason matters. Use `2>&1 || true` when gathering.
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Channel checked**: kali-rolling, snapshots, metapackages, and NetHunter advice matches official docs
- [ ] **Lab boundary explicit**: offensive tooling stays in authorized labs, CTFs, or owned systems

---

## Performance

- Install task-specific metapackages instead of full tool collections when disk, bandwidth, or update time matters.
- Use snapshots or pinned images for repeatable labs rather than debugging rolling drift mid-exercise.
- Keep wordlists, captures, and VM disks outside small root partitions.


---

## Best Practices

- Do not treat Kali as a hardened daily-driver server by default.
- Snapshot before major upgrades, GPU/wireless driver work, or live persistence changes.
- Separate client data, lab artifacts, and exploit tooling with clear storage boundaries.


## Workflow

### Step 1: Identify the Kali lane first

| Lane | Default stance | What changes |
|------|----------------|--------------|
| **Installed Kali rolling** | default for most users | continuous updates, package drift matters, repo hygiene is everything |
| **Kali last-snapshot** | safer, more frozen lane | release-like behavior between versioned snapshots |
| **Live ISO / live USB** | treat as ephemeral first | persistence, overlay state, and storage layout change recovery |
| **VM image** | check guest tooling and hypervisor assumptions | shared clipboard, display, USB passthrough, and virtual NIC quirks matter |
| **ARM / SBC image** | check board-specific image assumptions first | boot firmware, storage media, peripherals, and package expectations differ from amd64 installs |
| **Kali Purple image** | security distro with blue-team flavor | package mix and image choice differ from a standard red-team workstation |
| **NetHunter** | mobile and kernel-sensitive | Android host, custom kernels, HID, and wireless support change the answer |
| **Partial or development branch user** | slow down immediately | `kali-experimental`, `kali-bleeding-edge`, and `kali-dev` are not casual defaults |

### Step 2: Gather current system state

Start narrow, then widen only if the failing layer is still unclear.

Baseline checks for every Kali case:

```bash
cat /etc/os-release
uname -r
grep -Rhv '^#\|^$' /etc/apt/sources.list /etc/apt/sources.list.d/*.list 2>&1 || true
apt-cache policy 2>&1 || true
apt-cache policy kali-archive-keyring kali-defaults kali-linux-core kali-linux-default 2>&1 || true
apt list --upgradable 2>&1 | tail -n +2
findmnt /
lsblk -f
dpkg -l | grep '^ii  kali-' | head -40
```

Add subsystem probes only when the task needs them. On NetHunter or other mobile-adjacent
environments, skip desktop or systemd-specific probes that do not exist there.

```bash
# services and logs
ps -p 1 -o comm=
command -v systemctl >/dev/null 2>&1 && systemctl --failed 2>&1 || true
command -v journalctl >/dev/null 2>&1 && journalctl -b -p warning..alert 2>&1 || true

# boot and storage
findmnt /boot 2>&1 || true
findmnt /boot/efi 2>&1 || true

# desktop and capture path
echo "Session=$XDG_SESSION_TYPE Desktop=$XDG_CURRENT_DESKTOP"
loginctl list-sessions 2>&1 || true
systemctl status display-manager 2>&1 || true
systemctl --user --failed 2>&1 || true
systemctl --user status pipewire pipewire-pulse wireplumber xdg-desktop-portal 2>&1 || true
command -v wpctl >/dev/null 2>&1 && wpctl status

# hardware, wireless, GPU, and NetHunter
lspci -k | grep -Ei 'vga|3d|display|network|wireless'
lsusb
rfkill list 2>&1 || true
iw dev 2>&1 || true
journalctl -b | grep -Ei 'nvrm|nvidia|amdgpu|i915|xe|ath|iwlwifi|brcm|rtl|mt76|drm' 2>&1 || true
command -v dkms >/dev/null 2>&1 && dkms status 2>&1 || true
command -v airmon-ng >/dev/null 2>&1 && airmon-ng 2>&1 || true
command -v nethunter >/dev/null 2>&1 && nethunter -h 2>&1 | head -20
```

### Step 3: Load only the relevant reference

| Task type | Reference |
|-----------|-----------|
| apt, sources, keyrings, rolling vs snapshot, mirrors | `references/packages-branches-and-repos.md` |
| choosing metapackages and understanding Kali tool families | `references/metapackages-and-tool-families.md` |
| live USB, persistence, installers, VM images, recovery | `references/images-live-persistence-and-recovery.md` |
| wireless, GPU, SDR, USB, Bluetooth, NetHunter, hardware support | `references/wireless-gpu-hardware-and-nethunter.md` |
| scope discipline, vulnerable labs, snapshots, safe practice | `references/lab-safety-and-scope.md` |
| recurring Kali breakage patterns and edge cases | `references/gotchas-and-special-situations.md` |

Do not load every reference by default. Pick the one that matches the failure mode, then widen
only if the first layer is clean.

### Step 3.5: Stay here or hand off

| Request shape | Route |
|---------------|-------|
| install, package, image, persistence, hardware, or tool-family selection on Kali | stay in **kali-linux** |
| hypervisor config, USB passthrough, guest display acceleration, or VM platform wiring | use **virtualization** |
| exploit, pivot, privilege escalate, or run post-exploitation workflow on an authorized target | use **lockpick** |
| fuzz, reverse engineer deeply, hunt a novel bug, or build a PoC | use **zero-day** |
| review the target code or service for defensive findings | use **security-audit** |
| generic Debian-family host admin with no Kali-specific context | use **debian-ubuntu** |

### Step 4: Change one layer at a time

- Fix source lists and package state before debugging tools that may simply be missing or mismatched.
- Fix image or persistence layout before declaring the live USB broken.
- Fix desktop session and capture plumbing before blaming Burp, Wireshark, or browser tooling.
- Fix hardware support and firmware before blaming monitor mode, injection, SDR, or Bluetooth tools.
- Pick the smallest metapackage that matches the workflow instead of installing everything.
- Keep labs and production separate. Prefer snapshots, throwaway VMs, and isolated USB media.

### Step 5: Validate before closing

```bash
apt-cache policy package_name
command -v systemctl >/dev/null 2>&1 && systemctl status unit_name 2>&1 || true
journalctl -u unit_name -b 2>&1 || true
dpkg -l | grep '^ii  kali-' | head -20
command -v msfconsole 2>/dev/null || true
command -v nmap 2>/dev/null || true
command -v aircrack-ng 2>/dev/null || true
```

Reboot only when the boot path, persistence story, or kernel change is understood and at least
one known-good recovery path remains.

---

## Troubleshooting Pattern

Keep triage cross-layer and boring:

1. Confirm the Kali lane, branch, image type, and repo state.
2. Identify the failing layer: packages, image or persistence, desktop session, hardware, or tool selection.
3. Pull the right logs before changing config.
4. Change one layer at a time and retest.
5. Keep scope and safety separate from tool installation.

Core log sweep:

```bash
journalctl -b -p warning..alert
journalctl --user -b
dmesg --level=err,warn
journalctl -u unit_name -b 2>&1 || true
```

Broad pattern sweeps when you need correlation, not first-pass precision:

```bash
journalctl -b | grep -Ei 'nvrm|nvidia|amdgpu|i915|xe|ath|iwlwifi|brcm|rtl|mt76|drm' 2>&1 || true
journalctl --user -b | grep -Ei 'portal|pipewire|webrtc|burp|wireshark' 2>&1 || true
```

When the problem smells like "Kali is broken," check the boring causes first:

- source-list drift or stale keyring
- branch mixing
- huge metapackage install on weak hardware
- USB passthrough or monitor-mode expectations that the chipset cannot satisfy
- live USB persistence corruption
- VM guest additions and display stack mismatch

---

## Default Decisions

- **Kali means branch hygiene first.** The repo state explains more failures than exotic package folklore.
- **Prefer `kali-rolling` unless there is a clear reason not to.** It is the main branch most users should be on.
- **Use `kali-last-snapshot` when the user wants calmer release-like behavior.** Do not enable it beside `kali-rolling` just because more sounds better.
- **Prefer focused metapackages.** `kali-tools-*` bundles beat `kali-linux-everything` unless the box truly exists to be a giant toolbox.
- **Treat Kali as a workflow distro, not just a package repo.** Image choice, persistence, hardware, and scope matter as much as package names.
- **Stay package-focused when the ask is package-focused.** Installing `nuclei`, `burpsuite`, `hashcat`, or reversing tools stays here until the question turns into defensive review, offensive workflow, or novel vulnerability research.
- **Labs should be disposable.** Snapshots, throwaway VMs, and isolated media beat hand-maintaining a single sacred pentest laptop forever.
- **Tool families come before individual tool bikeshedding.** Pick the category, then the tool, then the package.
- **Wireless and SDR work are hardware stories first.** Chipset support, firmware, passthrough, power, and monitor-mode reality matter more than menu entries.
- **Route offensive depth correctly.** Kali can install the tools, but **lockpick** owns exploitation workflow and **zero-day** owns novel bug discovery.

---

## Quick Triage Checklist

| Symptom | First checks |
|---------|-------------|
| `apt` weirdness after install | source lists, `apt-cache policy`, keyring package, branch mixing, `apt full-upgrade` pending |
| Tool missing even though metapackage was installed | `dpkg -l`, `apt-cache depends`, command path, package split, transitional package |
| Live USB lost changes | persistence partition, mount state, overlay corruption, wrong image mode |
| VM feels broken or blind to USB gear | hypervisor guest tools, USB passthrough, network mode, display acceleration |
| Wireless tools do not see monitor mode or injection | chipset support, firmware, rfkill, USB power, passthrough, kernel module |
| SDR or hardware tools misbehave | package state, udev access, kernel modules, USB permissions, device firmware |
| Burp or browser capture feels broken | desktop session, CA import, proxy binding, PipeWire or portal path for GUI helpers |
| NetHunter issue | Android version, kernel support, image flavor, HID and wireless support, mobile package lane |
| System is huge and slow | metapackage sprawl, desktop choice, background services, `kali-linux-everything` regret |
| Nothing makes sense | check gotchas reference - branch mixing, stale keyring, persistence drift, VM passthrough mistakes, and unsupported Wi-Fi chipsets explain a lot |

---

## Reference Files

- `references/packages-branches-and-repos.md` - Kali branch model, source lists, keyrings, updates, and package-state recovery
- `references/metapackages-and-tool-families.md` - what the main Kali metapackages install, how the tool families map to real workflows, the `kali-tweaks` configuration menu, and when to hand off to lockpick or zero-day
- `references/images-live-persistence-and-recovery.md` - installer ISOs, netinst, live images, Purple images, VM images, persistence, and recovery flow
- `references/wireless-gpu-hardware-and-nethunter.md` - Wi-Fi, Bluetooth, RFID, SDR, GPU, USB passthrough, and NetHunter-specific hardware realities
- `references/lab-safety-and-scope.md` - disposable lab setup, intentionally vulnerable targets, snapshots, and authorization boundaries
- `references/gotchas-and-special-situations.md` - recurring Kali breakage patterns and edge cases

---

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** KALI-LINUX
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/kali-linux/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **debian-ubuntu** - base Debian-family administration. Use it for generic apt-family hosts; use this skill when Kali-specific branches, images, metapackages, or tool context matter.
- **lockpick** - exploitation, post-exploitation, and escalation on authorized targets. This skill helps choose and maintain Kali tooling; lockpick handles the offensive workflow itself.
- **zero-day** - vulnerability discovery, reverse engineering depth, fuzzing, and proof-of-concept work. This skill covers the Kali environment and tool families that support that work.
- **security-audit** - defensive hardening and vuln review instead of offensive distro workflow.
- **virtualization** - hypervisor setup, guest provisioning, passthrough, and VM platform issues once the fault is clearly outside the Kali guest.
- **command-prompt** - shell syntax, wrappers, aliases, and script portability when the real issue is the shell rather than Kali.
- **networking** - network services, VPNs, DNS, proxies, and firewall design beyond host-level Kali package questions.

---

## Rules

1. **Identify the Kali lane before prescribing commands.** Installed rolling, snapshot, live media, VM image, Purple, and NetHunter differ where it matters.
2. **Do not treat Kali like generic Debian with a dragon wallpaper.** Branches, metapackages, images, and hardware expectations change the answer.
3. **Do not mix branches casually.** `kali-rolling`, `kali-last-snapshot`, `kali-experimental`, `kali-bleeding-edge`, and `kali-dev` each have a purpose. Random mixing usually ends in package pain.
4. **Prefer focused metapackages over giant installs.** Install the tool family that matches the job before reaching for `kali-linux-everything`.
5. **Keep lab and production separate.** Practice targets, vulnerable apps, and offensive tooling belong on disposable systems or isolated boxes.
6. **Respect scope.** Recommending Kali tools is not permission to use them outside authorized environments.
7. **Treat hardware claims as hardware claims.** Monitor mode, injection, SDR capture, HID, and GPU acceleration depend on actual chipsets, firmware, and passthrough support.
8. **Live USB and persistence are their own failure domain.** Do not debug them like a normal installed root filesystem.
9. **Hand off correctly.** Once the work becomes exploitation methodology, use **lockpick**. Once it becomes original vulnerability research, use **zero-day**.
10. **Reach for common Kali failure patterns before exotic explanations.** Stale keyrings, branch drift, metapackage sprawl, persistence corruption, and unsupported hardware explain a large share of the mess.

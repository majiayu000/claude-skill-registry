---
name: privesc-linux
description: Use when escalating privileges on a Linux host — SUID/SGID & GTFOBins, sudo LPE (CVE-2025-32462/32463), capabilities & LD_PRELOAD, kernel LPE (CVE-2024-1086, Dirty Pipe, GameOver(lay)), service misconfig (PwnKit, Looney Tunables), container/namespace escape
metadata:
  type: offensive
  phase: post-exploitation
  tools: linpeas, pspy, les2, GTFOBins, BeRoot, deepce, sudo, getcap, bpftool, nsenter
  mitre: TA0004
kill_chain:
  phase: [exploit, actions]
  step: [4, 7]
  attck_tactics: [TA0004, TA0005, TA0003]
  attck_techniques: [T1068, T1548.001, T1548.003, T1574.006, T1574.007, T1053.003, T1611, T1610, T1222.002, T1547.006]
depends_on: [network-attack, exploit-development]
feeds_into: [red-team-ops, advanced-redteam]
inputs: [shell_access, os_fingerprint]
outputs: [elevated_access, finding_record]
references:
  - references/enumeration-tooling.md
  - references/suid-sudo-capabilities.md
  - references/kernel-exploits.md
  - references/service-misconfig-lpe.md
  - references/container-namespace-escape.md
scripts:
  - scripts/linpriv_enum.py
  - scripts/cap_suid_hunter.sh
  - scripts/sudo_cve_2025_check.sh
  - scripts/kernel_exploit_suggester.py
  - scripts/container_escape_check.sh
---

# Linux Privilege Escalation

## When to Activate

- Gained an initial unprivileged shell on a Linux host and need root or a higher-privileged account
- Post-exploitation lateral/vertical movement on Linux servers, workstations, CI runners, or appliances
- Container / Kubernetes pod foothold that needs to escape to the host node
- Triaging a host for misconfig-based LPE (SUID, sudo, capabilities, writable units/cron) before reaching for kernel 0-day
- CTF / lab challenges requiring privilege escalation with a defensible, detection-aware methodology

## Technique Map

| Technique | ATT&CK | CWE | Reference | Script |
|-----------|--------|-----|-----------|--------|
| Automated + manual enumeration (LinPEAS/pspy/LES2) | T1082, T1057 | CWE-200 | references/enumeration-tooling.md | scripts/linpriv_enum.py |
| Detection-aware / low-noise enumeration | T1082 | CWE-200 | references/enumeration-tooling.md | scripts/linpriv_enum.py |
| SUID/SGID binary abuse (GTFOBins) | T1548.001 | CWE-269 | references/suid-sudo-capabilities.md | scripts/cap_suid_hunter.sh |
| sudo misconfig + GTFOBins escape | T1548.003 | CWE-269 | references/suid-sudo-capabilities.md | scripts/cap_suid_hunter.sh |
| sudo host option LPE (CVE-2025-32462) | T1548.003 | CWE-863 | references/suid-sudo-capabilities.md | scripts/sudo_cve_2025_check.sh |
| sudo chroot/NSS LPE (CVE-2025-32463) | T1548.003 | CWE-829 | references/suid-sudo-capabilities.md | scripts/sudo_cve_2025_check.sh |
| Linux capabilities abuse (setuid/dac_read/sys_admin) | T1548 | CWE-250 | references/suid-sudo-capabilities.md | scripts/cap_suid_hunter.sh |
| LD_PRELOAD / LD_LIBRARY_PATH sudo hijack | T1574.006 | CWE-426 | references/suid-sudo-capabilities.md | scripts/cap_suid_hunter.sh |
| nf_tables double-free LPE (CVE-2024-1086) | T1068 | CWE-416 | references/kernel-exploits.md | scripts/kernel_exploit_suggester.py |
| io_uring memory-sharing LPE (CVE-2024-0582/2025-21836) | T1068 | CWE-416 | references/kernel-exploits.md | scripts/kernel_exploit_suggester.py |
| Dirty Pipe page-cache overwrite (CVE-2022-0847) | T1068 | CWE-787 | references/kernel-exploits.md | scripts/kernel_exploit_suggester.py |
| GameOver(lay) OverlayFS (CVE-2023-2640/32629) | T1068 | CWE-269 | references/kernel-exploits.md | scripts/kernel_exploit_suggester.py |
| udisks/libblockdev loop-mount LPE (CVE-2025-6019) | T1068 | CWE-250 | references/service-misconfig-lpe.md | scripts/linpriv_enum.py |
| PAM allow_active bypass (CVE-2025-6018) | T1068 | CWE-863 | references/service-misconfig-lpe.md | scripts/linpriv_enum.py |
| glibc ld.so Looney Tunables (CVE-2023-4911) | T1068 | CWE-787 | references/service-misconfig-lpe.md | scripts/kernel_exploit_suggester.py |
| polkit pkexec PwnKit (CVE-2021-4034) | T1548.001 | CWE-787 | references/service-misconfig-lpe.md | scripts/linpriv_enum.py |
| Cron/systemd/PATH/writable-file abuse | T1053.003, T1574.007 | CWE-732 | references/service-misconfig-lpe.md | scripts/linpriv_enum.py |
| NFS no_root_squash SUID drop | T1222.002 | CWE-732 | references/service-misconfig-lpe.md | scripts/linpriv_enum.py |
| runc fd-leak container escape (CVE-2024-21626) | T1611 | CWE-668 | references/container-namespace-escape.md | scripts/container_escape_check.sh |
| Docker socket / privileged container escape | T1611, T1610 | CWE-269 | references/container-namespace-escape.md | scripts/container_escape_check.sh |
| cgroup release_agent / CAP_SYS_ADMIN escape | T1611 | CWE-269 | references/container-namespace-escape.md | scripts/container_escape_check.sh |
| Kubernetes pod/token escape | T1611 | CWE-668 | references/container-namespace-escape.md | scripts/container_escape_check.sh |

## Quick Start

```bash
# 0. Stabilize shell + baseline context
python3 -c 'import pty;pty.spawn("/bin/bash")'; export TERM=xterm
id; uname -a; cat /etc/os-release

# 1. Fast, detection-aware enumeration (custom, no external download needed)
python3 linpriv_enum.py --quick            # quick wins triage
python3 linpriv_enum.py --full --json out.json   # full sweep -> JSON evidence

# 2. SUID / capabilities / sudo triage (maps directly to GTFOBins)
./cap_suid_hunter.sh                        # ranks exploitable SUID + caps + sudo -l

# 3. sudo 2025 LPE check (no creds needed; default-config killers)
./sudo_cve_2025_check.sh                    # tests CVE-2025-32462 / -32463 + PwnKit

# 4. Kernel + glibc CVE mapping for current host
python3 kernel_exploit_suggester.py        # uname/glibc/distro -> ranked modern LPEs

# 5. If containerized, check escape surface
./container_escape_check.sh                 # runc fd-leak, docker.sock, caps, k8s token

# 6. Validate root, then drop SUID backup or stable persistence per ROE
id; cp /bin/bash /tmp/.b && chmod 4755 /tmp/.b   # only if authorized
```

## OPSEC & Detection (summary)

| Technique | Telemetry / IOC | Detection (Sigma/EDR) | OPSEC note |
|-----------|-----------------|-----------------------|------------|
| LinPEAS / mass enum | Burst of `find / -perm`, hundreds of reads, `which`/`getcap` spam | auditd `execve` of linpeas; EDR file-scan anomaly | Prefer targeted enum (`linpriv_enum.py --quick`); avoid full FS walks on EDR hosts |
| SUID/GTFOBins escape | `setuid()` to 0 from non-root parent, shell with `-p` | auditd uid-change without login; Falco `Run shell untrusted` | Use the least-noisy binary; many GTFOBins one-liners are flagged by name |
| sudo CVE-2025-32463 | syslog `sudo ... CHROOT=`, NSS `libnss_*.so` from world-writable path | Elastic "Potential CVE-2025-32463 Sudo Chroot Execution"; auditd `-R` usage | chroot dir + fake `nsswitch.conf` are durable IOCs — clean the tree |
| sudo CVE-2025-32462 | sudo log with `-h`/HOST mismatch vs real hostname | auditd sudo with `--host` not paired with `-l` | leaves clean sudo log entry; blends with normal sudo |
| nf_tables CVE-2024-1086 | `unshare`/CLONE_NEWUSER + nftables from non-root; dmesg slab/UAF | Falco `Unprivileged Delegation of Page Faults`; auditd unshare+nft | namespace creation is logged; disable userns to neutralize |
| io_uring LPE | `io_uring_setup` syscall from unexpected proc | auditd syscall=io_uring_setup; eBPF LSM | many distros now ship `io_uring_disabled=2` |
| Looney Tunables CVE-2023-4911 | setuid exec with `GLIBC_TUNABLES=` containing `=`; core dumps | Elastic "Potential Privilege Escalation via CVE-2023-4911" | env var is recorded in auditd execve; unset before exec where possible |
| udisks CVE-2025-6019 | D-Bus `Filesystem.Resize/Check`, loop mount in `/tmp` w/o nosuid | auditd mount w/o `nosuid`; Falco mount-from-loop | leaves loop device + XFS image; detach + shred image |
| pkexec PwnKit | pkexec with `argc==0`, `GCONV_PATH=` env, `/var/...` GConv module | auditd `pkexec` + empty argv; Sigma proc_creation_lnx_pkexec | dropped GConv `.so` + dir are IOCs; remove them |
| Container escape (runc) | `/proc/self/fd/*` cwd, host paths from container, runc exec anomalies | Falco `Container escape`/`Mount launched in container`; CrowdStrike CWP | escapes are heavily monitored in CWP — confirm scope before running |
| cron/PATH/writable unit | new file in `/etc/cron*`, `systemctl daemon-reload`, PATH-prepended bin | auditd watch on `/etc/cron*`,`/etc/systemd/*`; Sigma cron tamper | revert file mtimes / remove dropped scripts post-exploit |

Detailed Sigma rules, auditd rule snippets and IOC lists live inside each reference file's **Detection** subsection.

## Deep Dives

- `references/enumeration-tooling.md` — LinPEAS/pspy/LES2/unix-privesc-check, the `linpriv_enum.py` methodology, quick-win checklists, and low-noise enumeration for EDR-monitored hosts.
- `references/suid-sudo-capabilities.md` — SUID/SGID + GTFOBins, sudo misconfig escapes, sudo CVE-2025-32462 (host) and CVE-2025-32463 (chroot/NSS), Linux capabilities (`cap_setuid`/`cap_dac_read_search`/`cap_sys_admin`), and LD_PRELOAD/LD_LIBRARY_PATH sudo hijacking.
- `references/kernel-exploits.md` — nf_tables CVE-2024-1086 (and 2026 nftables UAFs), io_uring CVE-2024-0582 / CVE-2025-21836, Dirty Pipe CVE-2022-0847, GameOver(lay) CVE-2023-2640, plus a kernel-CVE selection methodology and ROP/`commit_creds` primer.
- `references/service-misconfig-lpe.md` — udisks/libblockdev CVE-2025-6018/6019 chain, Looney Tunables CVE-2023-4911, PwnKit CVE-2021-4034, polkit/D-Bus abuse, cron/systemd/PATH hijacking, writable `/etc/passwd`, and NFS `no_root_squash`.
- `references/container-namespace-escape.md` — runc Leaky Vessels CVE-2024-21626, Docker socket / privileged-container / `--pid=host` / `CAP_SYS_PTRACE` escapes, cgroup-v1 `release_agent`, user namespaces, and Kubernetes service-account-token → pod escape.

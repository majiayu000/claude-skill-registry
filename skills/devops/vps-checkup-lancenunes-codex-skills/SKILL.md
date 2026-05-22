---
name: vps-checkup
description: "SSH into an Ubuntu VPS (Docker) for a read-only health/security/update report (UFW + fail2ban) and propose fixes; apply updates/restarts only with explicit confirmation. Use when the user wants a read-only VPS health/security check."
---

# VPS checkup (Ubuntu + Docker)

## Goal
- Produce a clear, read-only health/security/update report for an Ubuntu VPS running Docker.
- Propose safe, minimal fixes; do not apply changes or restart anything unless the user explicitly confirms.

## Inputs to ask for (if missing)
- SSH target host alias (from `~/.ssh/config` on Windows: `$HOME\\.ssh\\config`) or `user@ip`.
- Confirm `sudo` access and whether running `apt update` is allowed (it modifies package lists).
- Required open ports (e.g., `22`, `80`, `443`) and any non-standard SSH port.
- Where deployments live: confirm if Docker Compose is used on the VPS (common), and whether compose files are in a known path.
- If the local `ssh` client or required tools are missing, tell the user and ask whether to install them or provide command output manually.

## Workflow (checklist)
1) Connect safely
   - Keep a second SSH session open before any SSH/firewall changes.
   - Record identity/time/host: `whoami`, `hostname -f`, `date -Is`, `uptime`.
2) Collect a read-only baseline (system)
   - OS/kernel: `lsb_release -a` (or `cat /etc/os-release`), `uname -a`.
   - CPU/mem/disk: `top` snapshot, `free -h`, `df -hT`, `lsblk`.
   - Services: `systemctl --failed`, `journalctl -p 3 -xb --no-pager` (use `sudo` if needed).
3) Check security posture (read-only)
   - SSH: prefer `sudo sshd -T` (fallback to `sudo cat /etc/ssh/sshd_config` + `sshd_config.d/`).
   - Firewall: `sudo ufw status verbose` (and `sudo ufw status numbered`).
   - Fail2ban: `sudo fail2ban-client status` (+ `status sshd` if present).
   - Listening ports: `ss -tulpn` (use `sudo` if needed).
4) Check update posture (read-only by default)
   - If user allows: run `sudo apt update` to ensure accurate results.
   - Then collect: `apt list --upgradable`, `ubuntu-security-status` (if available), and `/var/run/reboot-required` presence.
   - Check unattended upgrades: `systemctl status unattended-upgrades --no-pager` and `/var/log/unattended-upgrades/`.
5) Check Docker health (read-only)
   - Daemon status: `systemctl status docker --no-pager`, `docker info`.
   - Containers: `docker ps`, unhealthy/restarting containers, recent restarts, and `docker stats --no-stream`.
   - Disk usage: `docker system df` and large log growth indicators.
   - Compose overview: `docker compose ls` (then inspect key projects as needed).
6) Produce the report + recommendations
   - Use `references/report-template.md`.
   - Use `references/ubuntu-docker-checkup-commands.md` for a copy/paste command set.
   - Rank findings by severity and explicitly list what requires confirmation (updates, firewall changes, SSH changes, restarts, pruning, reboot).
7) Apply fixes (ONLY with explicit confirmation)
   - Do not run `apt upgrade`, change UFW rules, change SSH auth, prune Docker, restart services/containers, or reboot unless the user says to.

## Safety gates (non-negotiable)
- No restarts (Docker/system services) unless the user explicitly asks for restart.
- No SSH/firewall changes unless you have a backup access path (second session open) and the user confirms the plan.
- Never paste secrets (tokens, private keys) into chat or logs.

## Deliverable
Provide:
- A read-only report using `references/report-template.md`.
- A prioritized list of recommended fixes and which ones require explicit confirmation.
- The exact commands run (or requested if the user ran them manually).

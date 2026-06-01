---
name: ansible
description: >
  · Write/review Ansible playbooks, roles, inventories, Vault, Molecule, AWX/AAP. Triggers: 'ansible', 'playbook', 'role', 'inventory', 'group_vars', 'ansible-lint'.
license: MIT
compatibility: "Requires ansible-core and Python 3.9+. Optional: ansible-lint, molecule"
metadata:
  source: iuliandita/skills
  date_added: "2026-03-24"
  effort: high
  argument_hint: "[playbook-or-task]"
---

# Ansible: Production Configuration Management

Write, review, and architect Ansible automation - from single playbooks to multi-tier, compliance-hardened infrastructure management. The goal is idempotent, auditable, maintainable automation that works the same locally and in CI/CD.

**Target versions** (May 2026):
- ansible-core **2.20.x LTS** (Python 3.12+ controller, 3.9+ target, EOL May 2027)
- ansible (community package) 13.x (depends on ansible-core 2.20)
- molecule 26.x (CalVer), ansible-lint 26.x (CalVer), ansible-navigator 26.x (CalVer)
- ansible-builder 3.1.x (EE definition v3)
- AWX 24.6.1 (last formal release Jul 2024; upstream AWX releases paused for a major refactor, devel branch active - track ansible/awx; awx-operator ~2.12.x still ships for K8s deploys). Verify current AWX/AAP release status before recommending a specific version or install path.
- AAP 2.6 (Oct 2025 - last RPM-installable release; AAP 2.7+ containerized-only)

This skill covers four domains depending on context:
- **Playbooks** - tasks, handlers, variables, conditions, loops, blocks, templates, Jinja2
- **Roles & Collections** - role structure, collection packaging, Galaxy/Automation Hub, Molecule testing
- **Operations** - inventory, Execution Environments, CI/CD integration, Vault, ansible-navigator
- **Compliance** - PCI-DSS 4.0 hardening, CIS benchmarks, Ansible-Lockdown, audit logging

## When to use

- Writing or reviewing Ansible playbooks, roles, or collections
- Configuring servers after Terraform provisions them (day-2 operations)
- OS hardening (CIS benchmarks, STIG, PCI-DSS configuration requirements)
- Managing packages, services, users, firewall rules, cron jobs, config files
- Testing automation with Molecule or tox-ansible
- Setting up Ansible Vault for secrets management
- Designing inventory structures (static, dynamic, multi-environment)
- Building Execution Environments for consistent runtime
- Integrating Ansible into CI/CD pipelines (GitLab CI, GitHub Actions)
- Reviewing AI-generated playbooks for correctness and idiomatic patterns

## When NOT to use

- Infrastructure provisioning (VPCs, RDS, EC2, cloud resources) - use **terraform**
- Kubernetes manifests, Helm charts, cluster architecture - use **kubernetes**
- Dockerfiles, Compose stacks, container image optimization - use **docker**
- CI/CD pipeline design (stages, runners, caching) - use **ci-cd**
- Security audits of application code (SAST, dependency scanning) - use **security-audit**
- Shell scripting or one-off commands - use **command-prompt**
- Firewall appliance management (OPNsense/pfSense) - use **firewall-appliance**
- Single-machine OS-level admin questions (package setup, user management, service config without automation context) - use the appropriate distro skill: **debian-ubuntu**, **rhel-fedora**, **kali-linux**, or **arch-btw**

---

## AI Self-Check

AI tools consistently produce the same Ansible mistakes. **Before returning any generated playbook, role, or task, verify against this list:**

- [ ] FQCNs used everywhere (`ansible.builtin.copy`, not `copy`). AI almost never does this unprompted.
- [ ] `become: true` present where privilege escalation is needed (AI often forgets this)
- [ ] `no_log: true` on every task handling secrets, passwords, tokens, or API keys (CVE-2024-8775 proved this matters)
- [ ] Every task has a descriptive `name:` field (AI sometimes omits names on simple tasks)
- [ ] Handler names are unique and `notify:` strings match exactly (typos = silent failures)
- [ ] Variables use `{{ var }}` with quotes: `"{{ my_var }}"` not `{{ my_var }}` (bare Jinja2 without quotes breaks YAML parsing)
- [ ] No `command`/`shell`/`raw` when an Ansible module exists for the operation
- [ ] Tasks are idempotent - running twice produces the same result (watch `command`/`shell` tasks without `creates`/`removes`)
- [ ] No hardcoded values - IPs, paths, package versions, usernames go in variables with defaults
- [ ] `ansible.builtin.apt`/`ansible.builtin.dnf` use `state: present`, not `state: latest` (unless explicitly upgrading)
- [ ] Loop variable is `item` (default) or renamed via `loop_var` in nested loops (AI conflates loop variables)
- [ ] `block`/`rescue`/`always` used for error handling, not bare `ignore_errors: true`
- [ ] No `ansible.builtin.template` with `src:` pointing to a non-`.j2` file (confusing, even if it works)
- [ ] `changed_when`/`failed_when` set on `command`/`shell` tasks to prevent false change reports
- [ ] Tags present on logical task groups for selective execution

Run generated playbooks through `ansible-lint` (production profile) when available.
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Collection docs checked**: module arguments and return values match the installed collection version
- [ ] **Idempotence proven**: changed/ok behavior is verified with check mode or a second run where practical

---

## Performance

- Use targeted inventories, tags, and `--limit` for large fleets; avoid full-fleet runs while iterating on a single role.
- Gather only required facts and cache facts where supported for slow or high-latency environments.
- Prefer native modules over shell loops so Ansible can batch work, diff safely, and report idempotence.


---

## Best Practices

- Pin collection versions in `requirements.yml` for production automation.
- Run destructive playbooks with `--check --diff` first and require a human-reviewed limit for production hosts.
- Keep Vault values out of diffs, logs, callback output, and generated examples.


## Workflow

### Step 1: Determine the domain

Based on the request:
- **"Write a playbook to configure X"** -> Playbooks
- **"Create a reusable role for X"** -> Roles & Collections
- **"Set up inventory" / "CI/CD" / "vault" / "EE"** -> Operations
- **"Harden this server" / "CIS benchmark" / "PCI compliance"** -> Compliance
- **"Review this playbook/role"** -> Apply production checklist + critical rules + AI self-check

Most real tasks blend domains. Start with the playbook, extract to roles when reuse is clear, wire into operations last.

### Step 2: Gather requirements

Before writing YAML, determine:
- **Target OS**: RHEL/CentOS, Ubuntu/Debian, Alpine, Windows - affects module choices
- **Python version on targets**: ansible-core 2.20 requires Python 3.9+ on managed nodes
- **Privilege escalation**: `become` method (sudo, su, doas, runas for Windows)
- **Connection**: SSH (default), WinRM (Windows), local, network_cli (network devices)
- **Idempotency**: every task must be safe to run multiple times
- **Secrets**: Ansible Vault, HashiCorp Vault, CI/CD secrets, environment variables
- **Testing**: Molecule scenario? tox-ansible matrix? Integration tests?
- **Compliance**: PCI-DSS scope? CIS benchmark level? STIG profile?
- **Inventory**: static, dynamic (cloud), or hybrid? Multi-environment?
- **Execution**: ansible-playbook (direct), ansible-navigator (EE), AWX/AAP (platform)?

### Step 3: Build

Follow the domain-specific section below. Always apply the production checklist (Step 4) and AI self-check before finishing.

### Step 4: Validate

```bash
# Syntax check (fast, no connection needed)
ansible-playbook playbook.yml --syntax-check

# Lint (use production profile for strictest checks)
ansible-lint --profile production playbook.yml

# Dry run (needs inventory + connectivity)
ansible-playbook playbook.yml --check --diff

# Molecule (role testing)
molecule test                          # full cycle: create, converge, verify, destroy
molecule converge                      # just apply (dev loop)
molecule verify                        # run verification only

# Navigator (EE-based execution)
ansible-navigator run playbook.yml --mode stdout --eei <ee-image>
```

---

## Playbooks

Read `references/playbook-patterns.md` for complete, copy-pasteable task examples (services, packages, files, templates, users, firewall, cron, systemd, OpenRC) and Jinja2 patterns.

### Structure

```yaml
---
- name: Configure web servers
  hosts: webservers
  become: true
  gather_facts: true

  vars:
    app_port: 8080
    app_user: appuser

  pre_tasks:
    - name: Update apt cache
      ansible.builtin.apt:
        update_cache: true
        cache_valid_time: 3600
      when: ansible_os_family == "Debian"

  roles:
    - role: common
      tags: [common]
    - role: nginx
      tags: [nginx]

  tasks:
    - name: Ensure application directory exists
      ansible.builtin.file:
        path: /opt/app
        state: directory
        owner: "{{ app_user }}"
        mode: "0755"

  handlers:
    - name: Restart nginx
      ansible.builtin.systemd:
        name: nginx
        state: restarted
        daemon_reload: true
```

### Key patterns

**Variable precedence** (22 levels - the most common source of confusion). In ascending priority:
1. Role defaults (`defaults/main.yml`) - weakest, meant to be overridden
2. Inventory vars (`group_vars/`, `host_vars/`)
3. Play vars
4. Task vars
5. Extra vars (`-e`) - strongest, overrides everything

**Rule of thumb**: put defaults in role `defaults/`, environment-specific values in `group_vars/`, one-off overrides in `host_vars/`, and emergency overrides via `-e`.

**Handlers**: only run when notified by a changed task, execute once at the end of the play (not immediately). Key gotchas:
- Handler names must be unique across all included roles
- Handlers don't run if the play fails before reaching them (use `meta: flush_handlers` if needed)
- Handlers run in definition order, not notification order
- Multiple notifications to the same handler = one execution

**Blocks**: use `block`/`rescue`/`always` for error handling and rollback - see `playbook-patterns.md` for complete deploy-with-rollback examples. Prefer `block`/`rescue` over `ignore_errors: true`.

**Loops**: prefer `loop:` over deprecated `with_*` syntax. Use `loop_control.label` for clean output.

**Conditional execution**: `when: ansible_os_family == "Debian"` etc. For multi-OS roles, use conditionals or `include_tasks` per OS family. See `playbook-patterns.md` for Alpine/OpenRC patterns.

**Service management**: use `ansible.builtin.service` (generic) for cross-distro roles - it auto-detects systemd, OpenRC, SysV via `ansible_service_mgr`. Only use `ansible.builtin.systemd` when you need systemd-specific features (`daemon_reload`, `scope`). See `playbook-patterns.md` for OpenRC patterns.

**Shell profile changes**: when converting a manual shell profile tweak into Ansible,
prefer a dedicated reusable role with `ansible.builtin.blockinfile`, role-prefixed
defaults, and a dedicated rollout playbook. See `references/operations-and-execution.md`;
the block must guard on SSH, not already inside
tmux, real TTY on stdin/stdout, and usable `TERM`, so automation, `scp`, `rsync`,
and remote SSH commands are not hijacked.

**Registering results**: `register: result_var` stores task output. Use `when: result_var.stat.exists`, `result_var.rc == 0`, etc. See `playbook-patterns.md` for patterns.

### Vault Quick Reference

```bash
# Encrypt a single variable (inline in YAML)
ansible-vault encrypt_string 'supersecret' --name 'db_password'

# Encrypt an entire file
ansible-vault encrypt group_vars/production/secrets.yml

# Edit encrypted file
ansible-vault edit group_vars/production/secrets.yml

# Run playbook with vault
ansible-playbook site.yml --ask-vault-pass
# Or with a password file (for CI/CD)
ansible-playbook site.yml --vault-password-file ~/.vault_pass
```

Never store the vault password in plaintext alongside the repo. Use `--ask-vault-pass`, a password file outside the repo, or a vault script that fetches from a secret manager.

### What NOT to write

- `command: apt-get install -y nginx` (use `ansible.builtin.apt`)
- `shell: systemctl restart nginx` (use `ansible.builtin.systemd`)
- `shell: useradd deploy` (use `ansible.builtin.user`)
- `copy` without `mode:` on sensitive files (defaults to umask, unpredictable)
- `template` without `.j2` extension on the source file
- `ignore_errors: true` without a comment explaining why (use `block`/`rescue` instead)
- `with_items` (deprecated - use `loop:`)
- Bare `{{ var }}` without quotes (YAML parses it as a dict start)
- `gather_facts: true` + never using facts (wasted 5-15 seconds per host)
- Tasks without `name:` (legal but unreadable in output)
- `state: latest` in production playbooks (non-deterministic - pin versions)

---

## Roles & Collections

Read `references/roles-and-collections.md` for detailed role anatomy, collection structure, Galaxy patterns, and Molecule testing workflows.

- Use one responsibility per role.
- Put user-tunable values in `defaults/main.yml`, not `vars/main.yml`.
- Use FQCNs everywhere.
- Prefix role variables to avoid collisions.
- Treat Molecule idempotence checks as mandatory, not optional polish.

---

## Operations
- Read `references/operations-and-execution.md` for inventory layout, `ansible.cfg`, execution environments, CI/CD integration, and `ansible-navigator`.
- Keep inventory split by environment.
- Prefer YAML inventory over legacy INI when touching existing inventories.
- Treat `pipelining = True`, fact caching, and callback configuration as standard production defaults.
- Use execution environments for repeatable local and CI runs.
- Keep vault usage in `references/vault-and-secrets.md`; secrets stay encrypted, prefixed, and wrapped with `no_log: true`.

---

## Compliance

Read `references/compliance.md` for the full PCI-DSS 4.0 requirements mapping to Ansible controls, CIS benchmark automation, and hardening patterns.

- Ansible owns OS and service enforcement, not application-level security review.
- CIS and PCI controls should be treated as role and template inputs, not blindly applied defaults.
- Test benchmark hardening in staging before broad rollout.
- Preserve audit evidence with callback plugins, AWX/AAP activity streams, or CI artifacts.

---

## Production Checklist

### Playbooks

- [ ] FQCNs on every module (`ansible.builtin.*`, `community.general.*`, etc.)
- [ ] Every task has a descriptive `name:`
- [ ] `become: true` only where needed (not play-level unless every task requires it)
- [ ] `no_log: true` on all tasks handling secrets
- [ ] Variables quoted: `"{{ var }}"` not `{{ var }}`
- [ ] No `command`/`shell` when a module exists
- [ ] `changed_when`/`failed_when` on all `command`/`shell` tasks
- [ ] Handlers have unique names and `notify:` strings match exactly
- [ ] Tags on logical task groups
- [ ] `--check` mode works (no tasks that break in check mode without `check_mode: false`)
- [ ] Idempotent - running twice produces no changes on the second run
- [ ] No `state: latest` in production (pin package versions)
- [ ] `ansible-lint --profile production` passes clean

### Roles

- [ ] All variables prefixed with role name (`nginx_port`, not `port`)
- [ ] `defaults/main.yml` for all user-configurable values
- [ ] `meta/main.yml` with dependencies, platforms, and minimum ansible version
- [ ] Molecule test scenario with converge + idempotence + verify
- [ ] README with usage examples and variable documentation
- [ ] No hardcoded values in `tasks/` (everything parameterized)
- [ ] `handlers/main.yml` for service restarts (not inline restarts in tasks)

### Operations

- [ ] Inventory separated by environment (production, staging, dev)
- [ ] `group_vars/` and `host_vars/` for environment-specific config
- [ ] Vault-encrypted secrets in dedicated `vault.yml` files
- [ ] Vault password via `--vault-password-file` (not interactive prompt in CI)
- [ ] SSH key-based auth (no `ansible_ssh_pass` in inventory)
- [ ] EE image pinned to specific tag (not `:latest`)
- [ ] ansible.cfg committed with sane defaults (no `host_key_checking = False` in production)
- [ ] Collections pinned in `requirements.yml` with version constraints
- [ ] `ansible-lint` in CI pipeline (production profile)

### Compliance (PCI-DSS 4.0)

- [ ] CIS benchmark role applied and tested (Req 2.2)
- [ ] SSH hardened: key-only auth, no root login, protocol 2, idle timeout (Req 2.2.7)
- [ ] Firewall rules managed as code (Req 1)
- [ ] Auditd rules deployed for CDE systems (Req 10.2)
- [ ] Log forwarding to immutable SIEM (Req 10.4.1.1)
- [ ] FIM agent deployed and configured (AIDE/OSSEC) (Req 11.5)
- [ ] All secrets Vault-encrypted, `no_log: true` everywhere (Req 8.6.2)
- [ ] Password policies enforced via PAM (Req 8.3.6)
- [ ] Playbook execution logged and archived (Req 10, Req 6)
- [ ] Anti-malware deployed on all in-scope systems (Req 5.2)
- [ ] NTP configured for consistent timestamps (Req 10.6)
- [ ] Unnecessary services disabled (Req 2.2.4)

---

## Deprecations and Breaking Changes

### ansible-core 2.20 (current)

**Removals (already removed)**:
- `smart` transport value - choose `ssh` or `paramiko` explicitly
- Galaxy v2 API support - Galaxy servers must support v3
- `PARAMIKO_HOST_KEY_AUTO_ADD` and `PARAMIKO_LOOK_FOR_KEYS` config keys
- `passlib_or_crypt` API from encrypt utility

**Deprecations (removal in 2.24)**:
- `INJECT_FACTS_AS_VARS` defaults to True but will flip to False. Access facts via `ansible_facts['hostname']` instead of `ansible_hostname`. Start migrating now.
- `ansible.module_utils._text` imports (`to_bytes`, `to_native`, `to_text`) - use `ansible.module_utils.common.text.converters` instead
- `vars` internal variable cache

### ansible-core 2.19 (previous)

- **Data Tagging** overhaul: improved error reporting but some loop templates broke (GitHub issue #85605). If loops fail with type errors after upgrading, check for native Jinja2 type handling conflicts.

### CalVer migration

All Ansible DevTools projects (molecule, ansible-lint, ansible-navigator, tox-ansible) switched from SemVer to CalVer (`YY.MM.MICRO`) in 2024. Don't be confused by the version jump (e.g., ansible-lint 6.x -> 26.x).

---

## Security Considerations

### CVEs to know

| CVE | Severity | Description | Mitigation |
|-----|----------|-------------|------------|
| CVE-2024-11079 | Medium | Hostvars bypass unsafe content protections, enabling arbitrary code execution via templated content | Upgrade to ansible-core >= 2.16.14, 2.17.7, or 2.18.1 |
| CVE-2024-8775 | Medium | Vault-encrypted variables exposed in plaintext via `include_vars` without `no_log` | Add `no_log: true` to all secret-handling tasks |
| CVE-2025-14010 | Medium | community.general exposes Keycloak credentials in verbose output | Upgrade to community.general >= 12.2.0 |
| CVE-2025-49520 | High | EDA authenticated argument injection in Git URL (command execution) | Patch AAP/EDA |
| CVE-2025-49521 | High | EDA template injection via Git branch/refspec (command execution) | Patch AAP/EDA |

### Supply chain

- Galaxy has no package signing or hash verification. Academic research (2025) found 45 vulnerable dependency chains across 482 Galaxy repos, with 38-54% code overlap propagating vulnerabilities.
- Pin collection versions in `requirements.yml`. Prefer Automation Hub (Red Hat certified) over Galaxy for production-critical collections.
- Pin GitHub Actions to commit SHAs in CI/CD (not mutable tags).
- Scan EE images for CVEs like any container image.

### AI-generated playbook risks

- AI tools hallucinate module names and parameters. Verify every module exists in the target collection version.
- AI rarely adds `no_log: true` to secret-handling tasks.
- AI generates non-idempotent `command`/`shell` tasks where modules exist.
- AI uses bare module names instead of FQCNs.
- **Slopsquatting**: AI may suggest Galaxy roles or collections that don't exist. Verify on Galaxy before adding to `requirements.yml`.

---

## Reference Files

- `references/playbook-patterns.md` - playbook and task patterns for common automation work
- `references/roles-and-collections.md` - role anatomy, collection structure, Galaxy patterns, and Molecule workflows
- `references/operations-and-execution.md` - inventory layout, ansible.cfg, execution environments, CI/CD integration, and navigator usage
- `references/vault-and-secrets.md` - Vault usage, secret handling, and external secret-manager integration
- `references/compliance.md` - PCI-DSS and CIS-oriented hardening guidance

---

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** ANSIBLE
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/ansible/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **terraform** - provisions infrastructure (VMs, networks, cloud resources). Ansible configures
  what Terraform creates. Day-1 provisioning = terraform; day-2 configuration = ansible.
- **kubernetes** - for K8s manifests, Helm charts, cluster architecture. Ansible can deploy to
  K8s via `kubernetes.core` collection, but manifest design belongs in the kubernetes skill.
- **docker** - for Dockerfile and Compose patterns. Ansible can manage containers via
  `community.docker`, but image building and Compose design belong in the docker skill.
- **databases** - for engine configuration (postgresql.conf, pg_hba.conf). Ansible automates
  the deployment of those configs; databases skill owns the tuning decisions.
- **ci-cd** - for pipeline design. Ansible can be called from CI/CD pipelines, but pipeline
  structure (stages, jobs, caching) belongs in the ci-cd skill.
- **security-audit** - for auditing Ansible playbooks for credential exposure, vault misuse,
  or supply chain risks in Galaxy dependencies.
- **debian-ubuntu** - for Debian/Ubuntu/Mint OS-level admin questions outside an automation context.
- **rhel-fedora** - for RHEL/Fedora/CentOS OS-level admin questions outside an automation context.
- **kali-linux** - for Kali Linux administration outside an automation context.
- **arch-btw** - for Arch Linux / CachyOS OS-level admin questions outside an automation context.

---

## Rules

These are non-negotiable. Violating any of these is a bug.

1. **FQCNs everywhere.** `ansible.builtin.copy`, not `copy`. No exceptions.
2. **Idempotent by default.** Every task must be safe to run multiple times. `command`/`shell` tasks need `creates`/`removes` or `changed_when`.
3. **`no_log: true` on secrets.** Every task handling passwords, tokens, API keys, or sensitive data. CVE-2024-8775 proved the cost of forgetting this.
4. **No `command`/`shell` when a module exists.** Modules are idempotent, tested, and portable. Shell commands are none of those.
5. **Variables over hardcoded values.** IPs, paths, package versions, usernames, ports - all variables with defaults.
6. **Quote Jinja2 variables.** `"{{ var }}"`, not `{{ var }}`. Bare braces break YAML parsing.
7. **Vault for secrets.** Not plaintext in `group_vars`, not `ansible_ssh_pass` in inventory, not environment variables in playbooks.
8. **Test with Molecule.** Every role gets a Molecule scenario with converge + idempotence check + verification.
9. **Pin collection versions.** In `requirements.yml` and EE definitions. Unpinned collections are a supply chain risk.
10. **`ansible-lint` clean.** Production profile. In CI. On every change.
11. **Separate inventory per environment.** Production, staging, dev. Never a single inventory with `--limit` for environment selection.
12. **`--check --diff` before apply.** Review what will change before applying, especially in CI/CD.
13. **Run the AI self-check.** Every generated playbook gets verified against the checklist above before returning.

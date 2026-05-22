---
name: ansible-config
description: Ansible configuration management and automation with safety controls
allowed-tools: [Bash, Read, Glob]
---

# Ansible Configuration Skill

## Overview

Provides 90%+ context savings vs raw Ansible operations. Includes critical safety controls for remote execution and configuration management.

## Requirements

- Ansible CLI (v2.9+)
- SSH access to target hosts
- Inventory file or dynamic inventory
- Optional: ANSIBLE_CONFIG, ANSIBLE_INVENTORY environment variables

## Tools (Progressive Disclosure)

### Playbook Execution

| Tool           | Description               | Confirmation |
| -------------- | ------------------------- | ------------ |
| playbook       | Run ansible playbook      | **REQUIRED** |
| playbook-check | Dry run with --check flag | No           |
| playbook-diff  | Show changes with --diff  | No           |

### Inventory Management

| Tool            | Description              | Confirmation |
| --------------- | ------------------------ | ------------ |
| inventory-list  | List all inventory hosts | No           |
| inventory-graph | Show inventory hierarchy | No           |
| host-vars       | Display host variables   | No           |

### Ad-hoc Commands

| Tool  | Description                    | Confirmation |
| ----- | ------------------------------ | ------------ |
| ping  | Test host connectivity         | No           |
| shell | Execute shell command on hosts | **REQUIRED** |
| copy  | Copy files to remote hosts     | **REQUIRED** |

### Galaxy (Roles & Collections)

| Tool           | Description                | Confirmation |
| -------------- | -------------------------- | ------------ |
| galaxy-list    | List installed roles       | No           |
| galaxy-search  | Search Ansible Galaxy      | No           |
| galaxy-install | Install role or collection | Yes          |

### Vault (Secrets)

| Tool          | Description         | Confirmation |
| ------------- | ------------------- | ------------ |
| vault-view    | View encrypted file | Yes          |
| vault-edit    | Edit encrypted file | **REQUIRED** |
| vault-encrypt | Encrypt file        | Yes          |
| vault-decrypt | Decrypt file        | Yes          |

### Configuration & Documentation

| Tool        | Description                | Confirmation |
| ----------- | -------------------------- | ------------ |
| config-list | Show ansible configuration | No           |
| config-dump | Dump full configuration    | No           |
| doc         | Show module documentation  | No           |

### Blocked Operations

| Tool                           | Status      |
| ------------------------------ | ----------- |
| shell with rm -rf              | **BLOCKED** |
| raw module                     | **BLOCKED** |
| command with destructive flags | **BLOCKED** |

## Quick Reference

```bash
# Run playbook
ansible-playbook site.yml

# Check mode (dry run)
ansible-playbook site.yml --check

# Show diff
ansible-playbook site.yml --diff

# Ping all hosts
ansible all -m ping

# List inventory
ansible-inventory --list

# View vault file
ansible-vault view secrets.yml

# Install galaxy role
ansible-galaxy install username.rolename
```

## Configuration

- **ANSIBLE_CONFIG**: Path to ansible.cfg file
- **ANSIBLE_INVENTORY**: Path to inventory file
- **ANSIBLE_VAULT_PASSWORD_FILE**: Path to vault password file
- **Working directory**: Must contain playbooks and inventory

## Safety Controls

⚠️ **All remote execution commands require confirmation**
⚠️ **Vault operations require confirmation**
⚠️ **shell/command modules with destructive operations are BLOCKED**
⚠️ **raw module is BLOCKED (use shell/command instead)**
⚠️ **Review playbook changes with --diff before applying**

## Agent Integration

- **devops** (primary): Infrastructure automation, configuration management
- **security-architect** (secondary): Vault secrets, secure playbooks
- **cloud-integrator** (secondary): Cloud inventory, dynamic provisioning

## Troubleshooting

| Issue                    | Solution                                       |
| ------------------------ | ---------------------------------------------- |
| SSH connection failed    | Check SSH keys and host accessibility          |
| Vault decrypt failed     | Verify vault password file or prompt           |
| Module not found         | Install required collection via galaxy         |
| Permission denied        | Check SSH user permissions and become settings |
| Syntax error in playbook | Run ansible-playbook --syntax-check            |

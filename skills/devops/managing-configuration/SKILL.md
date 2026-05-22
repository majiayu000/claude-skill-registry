---
name: managing-configuration
description: Guide users through creating, managing, and testing server configuration automation using Ansible. When automating server configurations, deploying applications with Ansible playbooks, managing dynamic inventories for cloud environments, or testing roles with Molecule, this skill provides idempotency patterns, secrets management with ansible-vault and HashiCorp Vault, and GitOps workflows for configuration as code.
---

# Configuration Management

## Purpose

This skill provides guidance for automating server and application configuration using Ansible and related tools. It covers playbook creation, role structure, inventory management (static and dynamic), secret management, testing patterns, and idempotency best practices to ensure safe, repeatable configuration deployments.

## When to Use This Skill

Invoke this skill when:
- Creating Ansible playbooks to configure servers or deploy applications
- Structuring reusable Ansible roles with proper directory layout
- Managing inventories (static files or dynamic cloud-based)
- Securing secrets with ansible-vault or HashiCorp Vault integration
- Testing roles with Molecule before production deployment
- Ensuring idempotent playbooks that safely run multiple times
- Migrating from Chef or Puppet to Ansible
- Implementing GitOps workflows for configuration as code
- Debugging playbook failures or handler issues

## Quick Start

### Basic Playbook Example

```yaml
---
# site.yml
- name: Configure web servers
  hosts: webservers
  become: yes

  tasks:
    - name: Ensure nginx is installed
      apt:
        name: nginx
        state: present
      notify: Restart nginx

    - name: Start nginx service
      service:
        name: nginx
        state: started
        enabled: yes

  handlers:
    - name: Restart nginx
      service:
        name: nginx
        state: restarted
```

Run with:
```bash
ansible-playbook -i inventory/production site.yml
```

## Core Concepts

### 1. Idempotency

Run playbooks multiple times without unintended side effects. Use state-based modules (`present`, `started`, `latest`) instead of imperative commands.

**Idempotent (good):**
```yaml
- name: Ensure package installed
  apt:
    name: nginx
    state: present
```

**Not idempotent (avoid):**
```yaml
- name: Install package
  command: apt-get install -y nginx
```

See `references/idempotency-guide.md` for detailed patterns.

### 2. Inventory Management

**Static Inventory:** INI or YAML files for stable environments.
**Dynamic Inventory:** Scripts or plugins for cloud environments (AWS, Azure, GCP).

Example static inventory (INI):
```ini
[webservers]
web1.example.com ansible_host=10.0.1.10
web2.example.com ansible_host=10.0.1.11

[webservers:vars]
nginx_worker_processes=4
```

See `references/inventory-management.md` for dynamic inventory setup.

### 3. Roles vs Playbooks

**Playbooks:** Orchestrate multiple tasks and roles for specific deployments.
**Roles:** Reusable, self-contained configuration units with standardized directory structure.

Standard role structure:
```
roles/nginx/
├── defaults/     # Default variables
├── tasks/        # Task files
├── handlers/     # Change handlers
├── templates/    # Jinja2 templates
├── files/        # Static files
└── meta/         # Dependencies
```

See `references/role-structure.md` for complete role patterns.

### 4. Secret Management

**ansible-vault:** Built-in encryption for sensitive data.
**HashiCorp Vault:** Enterprise-grade secrets management with dynamic credentials.

Encrypt secrets:
```bash
ansible-vault create group_vars/all/vault.yml
ansible-playbook site.yml --ask-vault-pass
```

See `references/secrets-management.md` for Vault integration.

## Common Workflows

### Workflow 1: Create New Playbook

**Step 1:** Define inventory
```ini
# inventory/production
[webservers]
web1.example.com
web2.example.com
```

**Step 2:** Create playbook structure
```yaml
---
- name: Configure application
  hosts: webservers
  become: yes

  pre_tasks:
    - name: Update package cache
      apt:
        update_cache: yes

  roles:
    - common
    - application

  post_tasks:
    - name: Verify service
      uri:
        url: http://localhost:8080/health
        status_code: 200
```

**Step 3:** Test with check mode
```bash
ansible-playbook -i inventory/production site.yml --check --diff
```

**Step 4:** Execute playbook
```bash
ansible-playbook -i inventory/production site.yml
```

See `references/playbook-patterns.md` for advanced patterns.

### Workflow 2: Create and Test Role

**Step 1:** Initialize role structure
```bash
ansible-galaxy init roles/myapp
```

**Step 2:** Define tasks
```yaml
# roles/myapp/tasks/main.yml
---
- name: Install application dependencies
  apt:
    name: "{{ item }}"
    state: present
  loop: "{{ myapp_dependencies }}"

- name: Deploy application
  template:
    src: app.conf.j2
    dest: /etc/myapp/app.conf
  notify: Restart myapp
```

**Step 3:** Add handler
```yaml
# roles/myapp/handlers/main.yml
---
- name: Restart myapp
  service:
    name: myapp
    state: restarted
```

**Step 4:** Initialize Molecule testing
```bash
cd roles/myapp
molecule init scenario default --driver-name docker
```

**Step 5:** Run tests
```bash
molecule test
```

See `references/testing-guide.md` for comprehensive testing patterns.

### Workflow 3: Set Up Dynamic Inventory (AWS)

**Step 1:** Install AWS collection
```bash
ansible-galaxy collection install amazon.aws
```

**Step 2:** Configure dynamic inventory
```yaml
# inventory/aws_ec2.yml
plugin: aws_ec2
regions:
  - us-east-1
filters:
  tag:Environment: production
  instance-state-name: running
keyed_groups:
  - key: tags.Role
    prefix: role
hostnames:
  - tag:Name
compose:
  ansible_host: private_ip_address
```

**Step 3:** Verify inventory
```bash
ansible-inventory -i inventory/aws_ec2.yml --list
```

**Step 4:** Run playbook
```bash
ansible-playbook -i inventory/aws_ec2.yml site.yml
```

See `references/inventory-management.md` for multi-cloud patterns.

### Workflow 4: Secure Secrets with ansible-vault

**Step 1:** Create encrypted vault file
```bash
ansible-vault create group_vars/all/vault.yml
```

**Step 2:** Add secrets
```yaml
# group_vars/all/vault.yml (encrypted)
vault_db_password: "SuperSecretPassword"
vault_api_key: "sk-1234567890"
```

**Step 3:** Reference in variables
```yaml
# group_vars/all/vars.yml (unencrypted)
db_password: "{{ vault_db_password }}"
api_key: "{{ vault_api_key }}"
```

**Step 4:** Use in playbook
```yaml
- name: Configure database
  template:
    src: db.conf.j2
    dest: /etc/app/db.conf
  vars:
    database_password: "{{ db_password }}"
```

**Step 5:** Run with vault password
```bash
ansible-playbook site.yml --vault-password-file ~/.vault_pass
```

See `references/secrets-management.md` for HashiCorp Vault integration.

## Tool Selection

### When to Use Ansible

- Configuring servers/VMs after provisioning
- Deploying applications to existing infrastructure
- Managing OS-level settings (users, packages, services)
- Orchestrating multi-step workflows across hosts
- Cloud-native environments (agentless SSH/WinRM)
- Teams new to configuration management (easiest learning curve)

### When to Use Alternatives

**Infrastructure-as-Code (Terraform):** Creating cloud infrastructure resources.
**Kubernetes:** Container orchestration and configuration.
**Chef/Puppet:** Existing deployments with high migration costs.

### Ansible vs IaC Integration

Best practice: Terraform provisions, Ansible configures.

**Workflow:**
1. Terraform creates AWS EC2 instances, security groups, load balancers
2. Terraform outputs instance IPs to Ansible inventory
3. Ansible configures OS, installs packages, deploys applications
4. Ansible sets up monitoring, backups, operational tasks

See `references/decision-framework.md` for detailed decision trees.

## Testing and Quality

### Pre-Deployment Validation

**Step 1:** Lint playbooks
```bash
ansible-lint playbooks/
```

**Step 2:** Check mode (dry run)
```bash
ansible-playbook site.yml --check --diff
```

**Step 3:** Test roles with Molecule
```bash
cd roles/myapp
molecule test
```

**Step 4:** Verify idempotence
```bash
molecule idempotence
```

### Configuration Files

**.ansible-lint:**
```yaml
---
exclude_paths:
  - molecule/
  - venv/
skip_list:
  - name[casing]
warn_list:
  - experimental
```

**molecule.yml:**
```yaml
---
driver:
  name: docker
platforms:
  - name: instance
    image: ubuntu:22.04
    pre_build_image: true
provisioner:
  name: ansible
verifier:
  name: ansible
```

See `references/testing-guide.md` for complete testing strategies.

## Troubleshooting

### Common Issues

**Connection failures:**
- Verify SSH access: `ansible all -i inventory -m ping`
- Check SSH keys: `ssh -vvv user@host`
- Test with password: `ansible-playbook site.yml --ask-pass`

**Handler not firing:**
- Handlers only run on change (check task `changed` status)
- Handlers run at end of playbook (use `meta: flush_handlers` to force earlier)
- Handler names must match exactly

**Variable not defined:**
- Check variable precedence (command-line > playbook > inventory > defaults)
- Use debug module: `- debug: var=myvar`
- Verify variable files are loaded: `ansible-playbook site.yml -v`

**Idempotency violations:**
- Run playbook twice, compare output
- Check for `changed` on every run
- Use state-based modules instead of `command`/`shell`

See `references/troubleshooting.md` for comprehensive debugging guide.

## Integration with Other Skills

**infrastructure-as-code:**
- Terraform provisions infrastructure
- Ansible configures post-provisioning
- Terraform outputs feed Ansible inventory

**kubernetes-operations:**
- Ansible deploys K8s clusters (kubespray)
- Kubernetes handles container orchestration
- Ansible manages node-level configuration

**building-ci-pipelines:**
- CI/CD runs ansible-lint for quality checks
- Molecule tests execute in pipeline
- Deployment stage runs playbooks

**secret-management:**
- ansible-vault for simple use cases
- HashiCorp Vault for enterprise secrets
- Dynamic credentials via Vault lookups

**security-hardening:**
- Ansible applies CIS benchmarks
- Security roles enforce compliance
- Molecule verifies hardening effectiveness

**testing-strategies:**
- Molecule for role testing
- Testinfra for verification
- Integration test suites

## Reference Documentation

- `references/playbook-patterns.md` - Playbook structure, handlers, tags, variables
- `references/role-structure.md` - Role directory layout, best practices, collections
- `references/inventory-management.md` - Static, dynamic, and hybrid inventory patterns
- `references/secrets-management.md` - ansible-vault and HashiCorp Vault integration
- `references/testing-guide.md` - Molecule, ansible-lint, check mode, verification
- `references/idempotency-guide.md` - Ensuring safe, repeatable executions
- `references/decision-framework.md` - Tool selection and workflow design
- `references/chef-puppet-migration.md` - Migrating from legacy tools to Ansible
- `references/troubleshooting.md` - Common issues and debugging techniques

## Example Code

- `examples/playbooks/` - Complete playbook examples
- `examples/roles/` - Production-ready role templates
- `examples/inventory/` - Static and dynamic inventory configurations
- `examples/molecule/` - Molecule test scenarios

## Utility Scripts

- `scripts/validate-playbook.py` - Validate playbook syntax and structure
- `scripts/generate-inventory.py` - Generate inventory from cloud providers
- `scripts/ansible-vault-helper.sh` - Vault management utilities
- `scripts/molecule-runner.sh` - Automated Molecule test execution

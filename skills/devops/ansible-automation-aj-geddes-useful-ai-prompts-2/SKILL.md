---
name: ansible-automation
description: Infrastructure automation and configuration management using Ansible playbooks, roles, and inventory. Use for deploying applications, patching, and managing servers.
---

# Ansible Automation

## Overview

Automate infrastructure provisioning, configuration management, and application deployment across multiple servers using Ansible playbooks, roles, and dynamic inventory management.

## When to Use

- Configuration management
- Application deployment
- Infrastructure patching and updates
- Multi-server orchestration
- Cloud instance provisioning
- Container management
- Database administration
- Security compliance automation

## Implementation Examples

### 1. **Playbook Structure and Best Practices**

```yaml
# site.yml - Main playbook
---
- name: Deploy application stack
  hosts: all
  gather_facts: yes
  serial: 1  # Rolling deployment

  pre_tasks:
    - name: Display host information
      debug:
        var: inventory_hostname
      tags: [always]

  roles:
    - common
    - docker
    - application

  post_tasks:
    - name: Verify deployment
      uri:
        url: "http://{{ inventory_hostname }}:8080/health"
        status_code: 200
      retries: 3
      delay: 10
      tags: [verify]

# roles/common/tasks/main.yml
---
- name: Update system packages
  apt:
    update_cache: yes
    cache_valid_time: 3600
  when: ansible_os_family == 'Debian'

- name: Install required packages
  package:
    name: "{{ packages }}"
    state: present
  vars:
    packages:
      - curl
      - git
      - htop
      - python3-pip

- name: Configure sysctl settings
  sysctl:
    name: "{{ item.name }}"
    value: "{{ item.value }}"
    sysctl_set: yes
    state: present
  loop:
    - name: net.core.somaxconn
      value: 65535
    - name: net.ipv4.tcp_max_syn_backlog
      value: 65535
    - name: fs.file-max
      value: 2097152

- name: Create application user
  user:
    name: appuser
    shell: /bin/bash
    home: /home/appuser
    createhome: yes
    state: present

# roles/docker/tasks/main.yml
---
- name: Install Docker prerequisites
  package:
    name: "{{ docker_packages }}"
    state: present
  vars:
    docker_packages:
      - apt-transport-https
      - ca-certificates
      - curl
      - gnupg
      - lsb-release

- name: Add Docker GPG key
  apt_key:
    url: https://download.docker.com/linux/ubuntu/gpg
    state: present

- name: Add Docker repository
  apt_repository:
    repo: "deb https://download.docker.com/linux/ubuntu {{ ansible_distribution_release }} stable"
    state: present

- name: Install Docker
  package:
    name:
      - docker-ce
      - docker-ce-cli
      - containerd.io
    state: present

- name: Start Docker service
  systemd:
    name: docker
    enabled: yes
    state: started

- name: Add user to docker group
  user:
    name: appuser
    groups: docker
    append: yes

# roles/application/tasks/main.yml
---
- name: Clone application repository
  git:
    repo: "{{ app_repo_url }}"
    dest: "/home/appuser/app"
    version: "{{ app_version }}"
    force: yes
  become: yes
  become_user: appuser

- name: Copy environment configuration
  template:
    src: .env.j2
    dest: "/home/appuser/app/.env"
    owner: appuser
    group: appuser
    mode: '0600'
  notify: restart application

- name: Build Docker image
  docker_image:
    name: "myapp:{{ app_version }}"
    build:
      path: "/home/appuser/app"
      pull: yes
    source: build
    state: present
  become: yes

- name: Start application container
  docker_container:
    name: myapp
    image: "myapp:{{ app_version }}"
    state: started
    restart_policy: always
    ports:
      - "8080:8080"
    volumes:
      - /home/appuser/app:/app:ro
    env:
      NODE_ENV: "{{ environment }}"
      LOG_LEVEL: "{{ log_level }}"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

handlers:
  - name: restart application
    docker_container:
      name: myapp
      state: restarted
```

### 2. **Inventory and Variables**

```yaml
# inventory/hosts.ini
[webservers]
web1 ansible_host=10.0.1.10
web2 ansible_host=10.0.1.11
web3 ansible_host=10.0.1.12

[databases]
db1 ansible_host=10.0.2.10 db_role=primary
db2 ansible_host=10.0.2.11 db_role=replica

[all:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_rsa
ansible_python_interpreter=/usr/bin/python3

# inventory/group_vars/webservers.yml
---
app_version: "1.2.3"
app_repo_url: "https://github.com/myorg/myapp.git"
environment: production
log_level: INFO

# inventory/host_vars/web1.yml
---
server_role: primary
max_connections: 500
```

### 3. **Ansible Deployment Script**

```bash
#!/bin/bash
# ansible-deploy.sh - Deploy using Ansible

set -euo pipefail

ENVIRONMENT="${1:-dev}"
PLAYBOOK="${2:-site.yml}"
INVENTORY="inventory/hosts.ini"
LIMIT="${3:-all}"

echo "Deploying with Ansible: $PLAYBOOK"
echo "Environment: $ENVIRONMENT"
echo "Limit: $LIMIT"

# Syntax check
echo "Checking Ansible syntax..."
ansible-playbook --syntax-check \
  -i "$INVENTORY" \
  -e "environment=$ENVIRONMENT" \
  "$PLAYBOOK"

# Dry run
echo "Running dry-run..."
ansible-playbook \
  -i "$INVENTORY" \
  -e "environment=$ENVIRONMENT" \
  -l "$LIMIT" \
  --check \
  "$PLAYBOOK"

# Ask for confirmation
read -p "Continue with deployment? (y/n): " -r
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Deployment cancelled"
  exit 1
fi

# Execute playbook
echo "Executing playbook..."
ansible-playbook \
  -i "$INVENTORY" \
  -e "environment=$ENVIRONMENT" \
  -l "$LIMIT" \
  -v \
  "$PLAYBOOK"

echo "Deployment complete!"

# Run verification
echo "Running post-deployment verification..."
ansible-playbook \
  -i "$INVENTORY" \
  -e "environment=$ENVIRONMENT" \
  -l "$LIMIT" \
  verify.yml
```

### 4. **Configuration Template**

```jinja2
# roles/application/templates/.env.j2
# Environment Configuration
NODE_ENV={{ environment }}
LOG_LEVEL={{ log_level }}
PORT=8080

# Database Configuration
DATABASE_URL=postgresql://{{ db_user }}:{{ db_password }}@{{ db_host }}:5432/{{ db_name }}
DATABASE_POOL_SIZE=20
DATABASE_TIMEOUT=30000

# Cache Configuration
REDIS_URL=redis://{{ redis_host }}:6379
CACHE_TTL=3600

# Application Configuration
APP_NAME=MyApp
APP_VERSION={{ app_version }}
WORKERS={{ ansible_processor_vcpus }}

# API Configuration
API_TIMEOUT=30000
API_RATE_LIMIT=1000

# Monitoring
SENTRY_DSN={{ sentry_dsn | default('') }}
DATADOG_API_KEY={{ datadog_api_key | default('') }}
```

## Ansible Commands

```bash
# List all hosts in inventory
ansible all -i inventory/hosts.ini --list-hosts

# Run ad-hoc command
ansible webservers -i inventory/hosts.ini -m ping

# Execute playbook
ansible-playbook -i inventory/hosts.ini site.yml

# Syntax check
ansible-playbook --syntax-check site.yml

# Dry-run
ansible-playbook -i inventory/hosts.ini site.yml --check

# Run with specific tags
ansible-playbook -i inventory/hosts.ini site.yml -t deploy
```

## Best Practices

### ✅ DO
- Use roles for modularity
- Implement proper error handling
- Use templates for configuration
- Leverage handlers for idempotency
- Use serial deployment for rolling updates
- Implement health checks
- Store inventory in version control
- Use vault for sensitive data

### ❌ DON'T
- Use command/shell without conditionals
- Copy files without templates
- Run without check mode first
- Mix environments in inventory
- Hardcode values
- Ignore error handling
- Use shell for simple tasks

## Resources

- [Ansible Official Documentation](https://docs.ansible.com/)
- [Ansible Galaxy - Community Roles](https://galaxy.ansible.com/)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/tips_tricks/index.html)
- [Ansible Playbook Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)

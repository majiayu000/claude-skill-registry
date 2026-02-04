---
name: ansible-automation
description: "Configuration management with Ansible. Use when automating server setup, application deployment, orchestrating multi-server tasks, or managing infrastructure configuration."
---

# Ansible Automation

Comprehensive guide for automating infrastructure configuration and application deployment with Ansible.

## When to Use

- Server provisioning and configuration
- Application deployment automation
- Multi-server orchestration
- Configuration drift remediation
- Secret management with Ansible Vault
- Creating reusable automation roles

## Core Concepts

### Why Ansible

| Feature | Benefit |
|---------|---------|
| Agentless | No software to install on managed nodes |
| SSH-based | Uses existing SSH infrastructure |
| Idempotent | Safe to run multiple times |
| YAML syntax | Human-readable, easy to learn |
| Extensible | 3000+ modules available |

### Project Structure

**Standard Layout:**
```
ansible/
├── ansible.cfg              # Configuration
├── inventory/
│   ├── production/
│   │   ├── hosts.yml        # Production inventory
│   │   └── group_vars/
│   │       ├── all.yml      # Variables for all hosts
│   │       └── webservers.yml
│   └── staging/
│       ├── hosts.yml
│       └── group_vars/
│
├── playbooks/
│   ├── site.yml             # Main playbook
│   ├── webservers.yml
│   └── databases.yml
│
├── roles/
│   ├── common/              # Base configuration
│   ├── nginx/
│   ├── postgresql/
│   └── app/
│
├── group_vars/
│   └── all/
│       ├── vars.yml
│       └── vault.yml        # Encrypted secrets
│
└── requirements.yml         # External roles
```

### Inventory

**YAML Inventory (Recommended):**
```yaml
# inventory/production/hosts.yml
all:
  children:
    webservers:
      hosts:
        web1.example.com:
          ansible_host: 10.0.1.10
          nginx_worker_processes: 4
        web2.example.com:
          ansible_host: 10.0.1.11
          nginx_worker_processes: 4
      vars:
        ansible_user: deploy
        ansible_python_interpreter: /usr/bin/python3

    databases:
      hosts:
        db1.example.com:
          ansible_host: 10.0.2.10
          postgresql_max_connections: 200
        db2.example.com:
          ansible_host: 10.0.2.11
          postgresql_max_connections: 200
      vars:
        ansible_user: postgres_admin

    loadbalancers:
      hosts:
        lb1.example.com:
          ansible_host: 10.0.0.10

  vars:
    ansible_ssh_private_key_file: ~/.ssh/ansible_key
    ntp_servers:
      - 0.pool.ntp.org
      - 1.pool.ntp.org
```

**Dynamic Inventory (AWS Example):**
```yaml
# inventory/aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions:
  - us-east-1
  - us-west-2

filters:
  tag:Environment: production
  instance-state-name: running

keyed_groups:
  - key: tags.Role
    prefix: role
  - key: placement.availability_zone
    prefix: az

hostnames:
  - private-ip-address

compose:
  ansible_host: private_ip_address
```

### Playbooks

**Basic Playbook:**
```yaml
# playbooks/webservers.yml
---
- name: Configure web servers
  hosts: webservers
  become: true
  gather_facts: true

  vars:
    app_name: myapp
    app_port: 8080

  pre_tasks:
    - name: Update apt cache
      ansible.builtin.apt:
        update_cache: true
        cache_valid_time: 3600
      when: ansible_os_family == "Debian"

  roles:
    - common
    - nginx
    - app

  tasks:
    - name: Ensure app is running
      ansible.builtin.systemd:
        name: "{{ app_name }}"
        state: started
        enabled: true

  handlers:
    - name: Reload nginx
      ansible.builtin.systemd:
        name: nginx
        state: reloaded

  post_tasks:
    - name: Verify application health
      ansible.builtin.uri:
        url: "http://localhost:{{ app_port }}/health"
        status_code: 200
      register: health_check
      retries: 5
      delay: 10
      until: health_check.status == 200
```

**Multi-Play Playbook:**
```yaml
# playbooks/site.yml
---
- name: Apply common configuration
  hosts: all
  become: true
  roles:
    - common
    - security-baseline

- name: Configure load balancers
  hosts: loadbalancers
  become: true
  roles:
    - haproxy

- name: Configure web servers
  hosts: webservers
  become: true
  roles:
    - nginx
    - app

- name: Configure databases
  hosts: databases
  become: true
  roles:
    - postgresql
```

### Roles

**Role Structure:**
```
roles/nginx/
├── defaults/
│   └── main.yml          # Default variables (lowest priority)
├── vars/
│   └── main.yml          # Role variables (higher priority)
├── tasks/
│   └── main.yml          # Main task list
├── handlers/
│   └── main.yml          # Handlers
├── templates/
│   └── nginx.conf.j2     # Jinja2 templates
├── files/
│   └── ssl/              # Static files
├── meta/
│   └── main.yml          # Role metadata & dependencies
└── README.md
```

**Role Tasks:**
```yaml
# roles/nginx/tasks/main.yml
---
- name: Install nginx
  ansible.builtin.apt:
    name: nginx
    state: present
  notify: Start nginx

- name: Create nginx config directories
  ansible.builtin.file:
    path: "{{ item }}"
    state: directory
    owner: root
    group: root
    mode: '0755'
  loop:
    - /etc/nginx/sites-available
    - /etc/nginx/sites-enabled
    - /etc/nginx/conf.d

- name: Deploy nginx configuration
  ansible.builtin.template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    owner: root
    group: root
    mode: '0644'
    validate: nginx -t -c %s
  notify: Reload nginx

- name: Deploy site configuration
  ansible.builtin.template:
    src: site.conf.j2
    dest: "/etc/nginx/sites-available/{{ nginx_site_name }}.conf"
    owner: root
    group: root
    mode: '0644'
  notify: Reload nginx

- name: Enable site
  ansible.builtin.file:
    src: "/etc/nginx/sites-available/{{ nginx_site_name }}.conf"
    dest: "/etc/nginx/sites-enabled/{{ nginx_site_name }}.conf"
    state: link
  notify: Reload nginx

- name: Remove default site
  ansible.builtin.file:
    path: /etc/nginx/sites-enabled/default
    state: absent
  notify: Reload nginx
```

**Role Handlers:**
```yaml
# roles/nginx/handlers/main.yml
---
- name: Start nginx
  ansible.builtin.systemd:
    name: nginx
    state: started
    enabled: true

- name: Reload nginx
  ansible.builtin.systemd:
    name: nginx
    state: reloaded

- name: Restart nginx
  ansible.builtin.systemd:
    name: nginx
    state: restarted
```

**Role Defaults:**
```yaml
# roles/nginx/defaults/main.yml
---
nginx_worker_processes: auto
nginx_worker_connections: 1024
nginx_keepalive_timeout: 65
nginx_site_name: default
nginx_server_name: localhost
nginx_root: /var/www/html
nginx_index: index.html

nginx_ssl_enabled: false
nginx_ssl_certificate: ""
nginx_ssl_certificate_key: ""

nginx_proxy_pass: ""
nginx_proxy_enabled: false
```

**Role Meta (Dependencies):**
```yaml
# roles/nginx/meta/main.yml
---
galaxy_info:
  author: Your Name
  description: Nginx web server role
  license: MIT
  min_ansible_version: "2.14"
  platforms:
    - name: Ubuntu
      versions:
        - focal
        - jammy
    - name: Debian
      versions:
        - bullseye
        - bookworm

dependencies:
  - role: common
  - role: ssl-certificates
    when: nginx_ssl_enabled
```

### Templates (Jinja2)

**Nginx Config Template:**
```jinja2
# roles/nginx/templates/nginx.conf.j2
user www-data;
worker_processes {{ nginx_worker_processes }};
pid /run/nginx.pid;

events {
    worker_connections {{ nginx_worker_connections }};
    multi_accept on;
    use epoll;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout {{ nginx_keepalive_timeout }};
    types_hash_max_size 2048;
    server_tokens off;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # Gzip
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml application/json application/javascript;

    # Include site configs
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

**Site Config Template:**
```jinja2
# roles/nginx/templates/site.conf.j2
{% if nginx_ssl_enabled %}
server {
    listen 80;
    server_name {{ nginx_server_name }};
    return 301 https://$server_name$request_uri;
}
{% endif %}

server {
{% if nginx_ssl_enabled %}
    listen 443 ssl http2;
    ssl_certificate {{ nginx_ssl_certificate }};
    ssl_certificate_key {{ nginx_ssl_certificate_key }};
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
{% else %}
    listen 80;
{% endif %}

    server_name {{ nginx_server_name }};
    root {{ nginx_root }};
    index {{ nginx_index }};

{% if nginx_proxy_enabled %}
    location / {
        proxy_pass {{ nginx_proxy_pass }};
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
{% else %}
    location / {
        try_files $uri $uri/ =404;
    }
{% endif %}

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

### Variables & Secrets

**Variable Precedence (lowest to highest):**
1. Role defaults (`roles/x/defaults/main.yml`)
2. Inventory group_vars/all
3. Inventory group_vars/group
4. Inventory host_vars/host
5. Playbook vars
6. Role vars (`roles/x/vars/main.yml`)
7. Block vars
8. Task vars
9. Extra vars (`-e`)

**Ansible Vault (Secrets Management):**
```bash
# Create encrypted file
ansible-vault create group_vars/all/vault.yml

# Edit encrypted file
ansible-vault edit group_vars/all/vault.yml

# Encrypt existing file
ansible-vault encrypt secrets.yml

# Decrypt file
ansible-vault decrypt secrets.yml

# View encrypted file
ansible-vault view group_vars/all/vault.yml

# Re-key (change password)
ansible-vault rekey group_vars/all/vault.yml

# Run playbook with vault
ansible-playbook site.yml --ask-vault-pass
ansible-playbook site.yml --vault-password-file ~/.vault_pass
```

**Vault Best Practices:**
```yaml
# group_vars/all/vars.yml - Reference vault variables
db_host: "{{ vault_db_host }}"
db_name: "{{ vault_db_name }}"
db_user: "{{ vault_db_user }}"
db_password: "{{ vault_db_password }}"

# group_vars/all/vault.yml - Encrypted
vault_db_host: db.example.com
vault_db_name: production
vault_db_user: app_user
vault_db_password: supersecretpassword
```

### Common Modules

**Package Management:**
```yaml
# apt (Debian/Ubuntu)
- name: Install packages
  ansible.builtin.apt:
    name:
      - nginx
      - postgresql-client
      - python3-pip
    state: present
    update_cache: true

# yum/dnf (RHEL/CentOS)
- name: Install packages
  ansible.builtin.dnf:
    name:
      - nginx
      - postgresql
    state: present
```

**File Operations:**
```yaml
# Create directory
- name: Create app directory
  ansible.builtin.file:
    path: /opt/myapp
    state: directory
    owner: deploy
    group: deploy
    mode: '0755'

# Copy file
- name: Copy application
  ansible.builtin.copy:
    src: app.jar
    dest: /opt/myapp/app.jar
    owner: deploy
    mode: '0644'

# Template
- name: Deploy config
  ansible.builtin.template:
    src: config.yml.j2
    dest: /opt/myapp/config.yml
    owner: deploy
    mode: '0600'
  notify: Restart app

# Line in file
- name: Ensure line in config
  ansible.builtin.lineinfile:
    path: /etc/sysctl.conf
    regexp: '^net.ipv4.ip_forward'
    line: 'net.ipv4.ip_forward = 1'
  notify: Reload sysctl
```

**Service Management:**
```yaml
- name: Manage service
  ansible.builtin.systemd:
    name: nginx
    state: started      # started, stopped, restarted, reloaded
    enabled: true       # Start on boot
    daemon_reload: true # If unit file changed
```

**User Management:**
```yaml
- name: Create application user
  ansible.builtin.user:
    name: deploy
    shell: /bin/bash
    groups: www-data
    append: true
    create_home: true

- name: Add SSH key
  ansible.posix.authorized_key:
    user: deploy
    key: "{{ lookup('file', 'files/deploy_key.pub') }}"
    state: present
```

**Command Execution:**
```yaml
# Shell command
- name: Run database migrations
  ansible.builtin.shell: |
    cd /opt/myapp
    ./manage.py migrate --noinput
  args:
    executable: /bin/bash
  become_user: deploy
  register: migration_result
  changed_when: "'No migrations to apply' not in migration_result.stdout"

# Command (no shell processing)
- name: Check app version
  ansible.builtin.command: /opt/myapp/bin/app --version
  register: app_version
  changed_when: false  # Read-only command
```

### Control Flow

**Conditionals:**
```yaml
- name: Install on Debian
  ansible.builtin.apt:
    name: nginx
  when: ansible_os_family == "Debian"

- name: Complex condition
  ansible.builtin.debug:
    msg: "Production web server"
  when:
    - inventory_hostname in groups['webservers']
    - env == 'production'
    - nginx_enabled | default(true)
```

**Loops:**
```yaml
# Simple loop
- name: Create users
  ansible.builtin.user:
    name: "{{ item }}"
    state: present
  loop:
    - alice
    - bob
    - charlie

# Loop with dict
- name: Create users with groups
  ansible.builtin.user:
    name: "{{ item.name }}"
    groups: "{{ item.groups }}"
  loop:
    - { name: 'alice', groups: 'admin' }
    - { name: 'bob', groups: 'developers' }

# Loop with index
- name: Create numbered files
  ansible.builtin.file:
    path: "/tmp/file{{ ansible_loop.index }}"
    state: touch
  loop: "{{ range(1, 5) | list }}"
```

**Blocks & Error Handling:**
```yaml
- name: Deploy application
  block:
    - name: Download artifact
      ansible.builtin.get_url:
        url: "{{ artifact_url }}"
        dest: /tmp/app.tar.gz

    - name: Extract artifact
      ansible.builtin.unarchive:
        src: /tmp/app.tar.gz
        dest: /opt/myapp
        remote_src: true

    - name: Start application
      ansible.builtin.systemd:
        name: myapp
        state: started

  rescue:
    - name: Rollback to previous version
      ansible.builtin.command: /opt/myapp/rollback.sh

    - name: Notify failure
      ansible.builtin.debug:
        msg: "Deployment failed, rolled back"

  always:
    - name: Clean up temp files
      ansible.builtin.file:
        path: /tmp/app.tar.gz
        state: absent
```

### Execution Commands

```bash
# Run playbook
ansible-playbook playbooks/site.yml

# Specify inventory
ansible-playbook -i inventory/production playbooks/site.yml

# Limit to hosts/groups
ansible-playbook site.yml --limit webservers
ansible-playbook site.yml --limit web1.example.com

# Run specific tags
ansible-playbook site.yml --tags "deploy,config"
ansible-playbook site.yml --skip-tags "slow"

# Check mode (dry run)
ansible-playbook site.yml --check

# Diff mode (show changes)
ansible-playbook site.yml --check --diff

# Extra variables
ansible-playbook site.yml -e "version=1.2.3 env=prod"
ansible-playbook site.yml -e "@vars.yml"

# Verbose output
ansible-playbook site.yml -v    # Basic
ansible-playbook site.yml -vvv  # Debug

# Ad-hoc commands
ansible all -m ping
ansible webservers -m shell -a "uptime"
ansible webservers -m ansible.builtin.apt -a "name=nginx state=present" --become
```

### Best Practices

**1. Idempotency - Always:**
```yaml
# BAD - Not idempotent
- name: Add to hosts file
  ansible.builtin.shell: echo "10.0.0.1 db.local" >> /etc/hosts

# GOOD - Idempotent
- name: Add to hosts file
  ansible.builtin.lineinfile:
    path: /etc/hosts
    line: "10.0.0.1 db.local"
    state: present
```

**2. Use FQCN (Fully Qualified Collection Names):**
```yaml
# BAD
- apt:
    name: nginx

# GOOD
- ansible.builtin.apt:
    name: nginx
```

**3. Name Every Task:**
```yaml
# BAD
- ansible.builtin.apt:
    name: nginx

# GOOD
- name: Install nginx web server
  ansible.builtin.apt:
    name: nginx
```

**4. Use Tags:**
```yaml
- name: Install packages
  ansible.builtin.apt:
    name: nginx
  tags:
    - packages
    - nginx

- name: Deploy config
  ansible.builtin.template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  tags:
    - config
    - nginx
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| SSH connection failed | Check `ansible_host`, `ansible_user`, SSH key |
| Permission denied | Add `become: true`, check sudo config |
| Module not found | Install collection: `ansible-galaxy collection install` |
| Variable undefined | Check variable precedence, use `default()` filter |
| Idempotency broken | Use proper modules, check `changed_when` |

### Checklist

Before running:
- [ ] Inventory is correct for target environment
- [ ] Vault password available
- [ ] SSH connectivity verified (`ansible all -m ping`)
- [ ] Check mode tested (`--check --diff`)
- [ ] Sensitive data in vault, not plain text
- [ ] Tasks are idempotent
- [ ] Handlers notify correctly

## Integration

Works with:
- `/devops` - Infrastructure automation
- `/terraform` - Terraform provisions, Ansible configures
- `/security` - Security hardening playbooks
- `golden-paths` skill - Standardized automation

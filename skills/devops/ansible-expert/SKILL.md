---
name: ansible-expert
version: 1.0.0
description: Expert-level Ansible for configuration management, automation, and infrastructure as code
category: devops
tags: [ansible, automation, configuration-management, iac, playbooks, roles]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(ansible:*, ansible-playbook:*, ansible-galaxy:*)
---

# Ansible Expert

Expert guidance for Ansible - configuration management, application deployment, and IT automation using declarative YAML playbooks.

## Core Concepts

### Ansible Architecture
- Control node (runs Ansible)
- Managed nodes (target systems)
- Inventory (hosts and groups)
- Playbooks (YAML automation scripts)
- Modules (units of work)
- Roles (reusable automation units)
- Plugins (extend functionality)

### Key Features
- Agentless (SSH-based)
- Idempotent operations
- Declarative syntax
- Human-readable YAML
- Extensible with modules
- Push-based configuration
- Parallel execution

### Use Cases
- Configuration management
- Application deployment
- Provisioning
- Continuous delivery
- Security automation
- Orchestration

## Installation

```bash
# Using pip
pip install ansible

# Using apt (Ubuntu/Debian)
sudo apt update
sudo apt install ansible

# Using yum (RHEL/CentOS)
sudo yum install ansible

# Verify installation
ansible --version
```

## Inventory

### Basic Inventory (INI format)
```ini
# inventory/hosts
[webservers]
web1.example.com
web2.example.com ansible_host=192.168.1.10

[databases]
db1.example.com ansible_user=dbadmin
db2.example.com

[production:children]
webservers
databases

[production:vars]
ansible_python_interpreter=/usr/bin/python3
ansible_connection=ssh
```

### YAML Inventory
```yaml
# inventory/hosts.yml
all:
  children:
    webservers:
      hosts:
        web1.example.com:
        web2.example.com:
          ansible_host: 192.168.1.10
    databases:
      hosts:
        db1.example.com:
          ansible_user: dbadmin
        db2.example.com:
    production:
      children:
        webservers:
        databases:
      vars:
        ansible_python_interpreter: /usr/bin/python3
        ansible_connection: ssh
```

### Dynamic Inventory
```python
#!/usr/bin/env python3
# inventory/aws_ec2.py
import json
import boto3

def get_inventory():
    ec2 = boto3.client('ec2', region_name='us-east-1')
    response = ec2.describe_instances(Filters=[
        {'Name': 'instance-state-name', 'Values': ['running']}
    ])

    inventory = {
        '_meta': {'hostvars': {}},
        'all': {'hosts': []},
        'webservers': {'hosts': []},
        'databases': {'hosts': []},
    }

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            ip = instance['PrivateIpAddress']
            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}

            inventory['all']['hosts'].append(ip)
            inventory['_meta']['hostvars'][ip] = {
                'ansible_host': ip,
                'instance_id': instance['InstanceId'],
                'instance_type': instance['InstanceType'],
            }

            # Group by role tag
            role = tags.get('Role', '')
            if role in inventory:
                inventory[role]['hosts'].append(ip)

    return inventory

if __name__ == '__main__':
    print(json.dumps(get_inventory(), indent=2))
```

## Playbooks

### Basic Playbook
```yaml
# playbooks/webserver.yml
---
- name: Configure web servers
  hosts: webservers
  become: yes
  vars:
    app_port: 8080
    app_user: webapp

  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Start and enable nginx
      systemd:
        name: nginx
        state: started
        enabled: yes

    - name: Copy nginx configuration
      template:
        src: templates/nginx.conf.j2
        dest: /etc/nginx/sites-available/default
        mode: '0644'
      notify: Reload nginx

    - name: Create application user
      user:
        name: "{{ app_user }}"
        state: present
        shell: /bin/bash

  handlers:
    - name: Reload nginx
      systemd:
        name: nginx
        state: reloaded
```

### Advanced Playbook
```yaml
# playbooks/deploy-app.yml
---
- name: Deploy application
  hosts: webservers
  become: yes
  vars:
    app_name: myapp
    app_version: "{{ version | default('latest') }}"
    app_port: 8080
    deploy_user: deployer

  pre_tasks:
    - name: Check if required variables are defined
      assert:
        that:
          - app_name is defined
          - app_version is defined
        fail_msg: "Required variables are not defined"

  tasks:
    - name: Create deployment directory
      file:
        path: "/opt/{{ app_name }}"
        state: directory
        owner: "{{ deploy_user }}"
        group: "{{ deploy_user }}"
        mode: '0755'

    - name: Download application artifact
      get_url:
        url: "https://artifacts.example.com/{{ app_name }}/{{ app_version }}/{{ app_name }}.jar"
        dest: "/opt/{{ app_name }}/{{ app_name }}-{{ app_version }}.jar"
        mode: '0644'
      register: download_result

    - name: Create systemd service
      template:
        src: templates/app.service.j2
        dest: "/etc/systemd/system/{{ app_name }}.service"
        mode: '0644'
      notify:
        - Reload systemd
        - Restart application

    - name: Enable application service
      systemd:
        name: "{{ app_name }}"
        enabled: yes

    - name: Wait for application to start
      wait_for:
        port: "{{ app_port }}"
        delay: 5
        timeout: 60
      when: download_result.changed

    - name: Check application health
      uri:
        url: "http://localhost:{{ app_port }}/health"
        status_code: 200
      retries: 3
      delay: 5

  post_tasks:
    - name: Clean up old versions
      shell: |
        cd /opt/{{ app_name }}
        ls -t {{ app_name }}-*.jar | tail -n +4 | xargs -r rm
      args:
        executable: /bin/bash

  handlers:
    - name: Reload systemd
      systemd:
        daemon_reload: yes

    - name: Restart application
      systemd:
        name: "{{ app_name }}"
        state: restarted
```

### Conditionals and Loops
```yaml
---
- name: Conditional and loop examples
  hosts: all
  tasks:
    - name: Install package (Debian)
      apt:
        name: "{{ item }}"
        state: present
      loop:
        - nginx
        - postgresql
        - redis
      when: ansible_os_family == "Debian"

    - name: Install package (RedHat)
      yum:
        name: "{{ item }}"
        state: present
      loop:
        - nginx
        - postgresql
        - redis
      when: ansible_os_family == "RedHat"

    - name: Create users
      user:
        name: "{{ item.name }}"
        state: present
        groups: "{{ item.groups }}"
      loop:
        - { name: 'alice', groups: 'wheel' }
        - { name: 'bob', groups: 'users' }
        - { name: 'charlie', groups: 'developers' }

    - name: Configure services
      systemd:
        name: "{{ item.name }}"
        state: "{{ item.state }}"
        enabled: "{{ item.enabled }}"
      loop:
        - { name: 'nginx', state: 'started', enabled: yes }
        - { name: 'postgresql', state: 'started', enabled: yes }
        - { name: 'redis', state: 'started', enabled: yes }

    - name: Set fact based on condition
      set_fact:
        environment_type: "{{ 'production' if inventory_hostname in groups['production'] else 'development' }}"

    - name: Debug conditional
      debug:
        msg: "This is a {{ environment_type }} server"
```

## Roles

### Role Structure
```
roles/
└── webserver/
    ├── defaults/
    │   └── main.yml         # Default variables
    ├── files/
    │   └── app.conf         # Static files
    ├── handlers/
    │   └── main.yml         # Handlers
    ├── meta/
    │   └── main.yml         # Role metadata and dependencies
    ├── tasks/
    │   └── main.yml         # Main task list
    ├── templates/
    │   └── nginx.conf.j2    # Jinja2 templates
    ├── tests/
    │   └── test.yml         # Role tests
    └── vars/
        └── main.yml         # Role variables
```

### Example Role
```yaml
# roles/webserver/defaults/main.yml
---
nginx_port: 80
nginx_user: www-data
document_root: /var/www/html

# roles/webserver/tasks/main.yml
---
- name: Install nginx
  apt:
    name: nginx
    state: present
    update_cache: yes

- name: Copy nginx configuration
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    mode: '0644'
  notify: Restart nginx

- name: Create document root
  file:
    path: "{{ document_root }}"
    state: directory
    owner: "{{ nginx_user }}"
    mode: '0755'

- name: Start nginx
  systemd:
    name: nginx
    state: started
    enabled: yes

# roles/webserver/handlers/main.yml
---
- name: Restart nginx
  systemd:
    name: nginx
    state: restarted

# roles/webserver/templates/nginx.conf.j2
user {{ nginx_user }};
worker_processes auto;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    server {
        listen {{ nginx_port }};
        server_name {{ ansible_hostname }};

        root {{ document_root }};
        index index.html;

        location / {
            try_files $uri $uri/ =404;
        }
    }
}

# Use role in playbook
---
- name: Configure web servers
  hosts: webservers
  become: yes
  roles:
    - role: webserver
      vars:
        nginx_port: 8080
        document_root: /var/www/myapp
```

### Role Dependencies
```yaml
# roles/app/meta/main.yml
---
dependencies:
  - role: common
  - role: nginx
    vars:
      nginx_port: 8080
  - role: postgresql
    when: database_enabled | default(false)
```

## Templates (Jinja2)

```jinja2
{# templates/app.conf.j2 #}
# Application configuration for {{ app_name }}
# Generated by Ansible on {{ ansible_date_time.iso8601 }}

[server]
host = {{ ansible_default_ipv4.address }}
port = {{ app_port }}
workers = {{ ansible_processor_vcpus }}

[database]
host = {{ db_host }}
port = {{ db_port }}
name = {{ db_name }}
user = {{ db_user }}
password = {{ db_password }}

[cache]
enabled = {{ cache_enabled | default(true) | lower }}
{% if cache_enabled | default(true) %}
backend = redis
redis_host = {{ redis_host }}
redis_port = {{ redis_port }}
{% endif %}

[features]
{% for feature, enabled in features.items() %}
{{ feature }} = {{ enabled | lower }}
{% endfor %}

{% if environment == 'production' %}
[production]
debug = false
log_level = warning
{% else %}
[development]
debug = true
log_level = debug
{% endif %}
```

## Variables and Facts

### Variable Precedence (low to high)
1. Role defaults
2. Inventory file/script group vars
3. Inventory group_vars/all
4. Playbook group_vars/all
5. Inventory group_vars/*
6. Playbook group_vars/*
7. Inventory file/script host vars
8. Inventory host_vars/*
9. Playbook host_vars/*
10. Host facts
11. Play vars
12. Play vars_prompt
13. Play vars_files
14. Role vars
15. Block vars
16. Task vars
17. Extra vars (-e flag)

### Using Variables
```yaml
---
- name: Variable examples
  hosts: all
  vars:
    app_name: myapp
    app_version: 1.0.0
  vars_files:
    - vars/common.yml
    - "vars/{{ environment }}.yml"

  tasks:
    - name: Load variables from file
      include_vars:
        file: "vars/{{ ansible_distribution }}.yml"

    - name: Set fact
      set_fact:
        full_app_name: "{{ app_name }}-{{ app_version }}"

    - name: Register output
      command: hostname
      register: hostname_output

    - name: Use registered variable
      debug:
        msg: "Hostname is {{ hostname_output.stdout }}"

    - name: Access facts
      debug:
        msg: |
          OS: {{ ansible_distribution }} {{ ansible_distribution_version }}
          Kernel: {{ ansible_kernel }}
          CPU: {{ ansible_processor_vcpus }} cores
          Memory: {{ ansible_memtotal_mb }} MB
          IP: {{ ansible_default_ipv4.address }}
```

## Error Handling

```yaml
---
- name: Error handling examples
  hosts: all
  tasks:
    - name: Task that might fail
      command: /bin/false
      ignore_errors: yes

    - name: Task with custom error handling
      block:
        - name: Try to start service
          systemd:
            name: myapp
            state: started
      rescue:
        - name: Log error
          debug:
            msg: "Failed to start myapp"

        - name: Try alternative
          systemd:
            name: myapp-fallback
            state: started
      always:
        - name: This always runs
          debug:
            msg: "Cleanup task"

    - name: Assert condition
      assert:
        that:
          - ansible_memtotal_mb >= 2048
          - ansible_processor_vcpus >= 2
        fail_msg: "Server does not meet minimum requirements"

    - name: Fail when condition
      fail:
        msg: "Production deployment requires version tag"
      when:
        - environment == 'production'
        - app_version == 'latest'

    - name: Changed when condition
      command: /usr/local/bin/check_status.sh
      register: result
      changed_when: "'updated' in result.stdout"
      failed_when: result.rc not in [0, 2]
```

## Ansible Vault

```bash
# Create encrypted file
ansible-vault create secrets.yml

# Edit encrypted file
ansible-vault edit secrets.yml

# Encrypt existing file
ansible-vault encrypt vars/production.yml

# Decrypt file
ansible-vault decrypt vars/production.yml

# View encrypted file
ansible-vault view secrets.yml

# Rekey (change password)
ansible-vault rekey secrets.yml
```

```yaml
# secrets.yml (encrypted)
---
db_password: supersecret
api_key: abc123xyz
ssl_key: |
  -----BEGIN PRIVATE KEY-----
  ...
  -----END PRIVATE KEY-----

# Use in playbook
---
- name: Deploy with secrets
  hosts: production
  vars_files:
    - secrets.yml
  tasks:
    - name: Configure database
      template:
        src: db.conf.j2
        dest: /etc/db.conf
      no_log: yes  # Don't log sensitive data
```

```bash
# Run playbook with vault password
ansible-playbook playbook.yml --ask-vault-pass

# Use password file
ansible-playbook playbook.yml --vault-password-file ~/.vault_pass

# Use multiple vault IDs
ansible-playbook playbook.yml --vault-id prod@prompt --vault-id dev@~/.vault_dev
```

## Best Practices

### Playbook Organization
```
ansible-project/
├── ansible.cfg
├── inventory/
│   ├── production/
│   │   ├── hosts.yml
│   │   └── group_vars/
│   └── staging/
│       ├── hosts.yml
│       └── group_vars/
├── playbooks/
│   ├── site.yml
│   ├── webservers.yml
│   └── databases.yml
├── roles/
│   ├── common/
│   ├── nginx/
│   └── postgresql/
├── group_vars/
│   ├── all.yml
│   └── webservers.yml
├── host_vars/
└── files/
```

### Idempotency
```yaml
# ❌ Not idempotent
- name: Add line to file
  shell: echo "server {{ ansible_hostname }}" >> /etc/hosts

# ✅ Idempotent
- name: Add line to file
  lineinfile:
    path: /etc/hosts
    line: "server {{ ansible_hostname }}"
    state: present
```

### Performance
- Use `strategy: free` for faster execution
- Enable pipelining in ansible.cfg
- Use `async` for long-running tasks
- Disable fact gathering when not needed
- Use `serial` for rolling updates

```yaml
# ansible.cfg
[defaults]
forks = 20
host_key_checking = False
pipelining = True
gathering = smart
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts
fact_caching_timeout = 86400

# Playbook with performance optimizations
---
- name: Fast deployment
  hosts: webservers
  strategy: free
  gather_facts: no
  serial: 5  # Deploy to 5 hosts at a time

  tasks:
    - name: Long running task
      command: /usr/local/bin/build.sh
      async: 3600
      poll: 0
      register: build_job

    - name: Check build status
      async_status:
        jid: "{{ build_job.ansible_job_id }}"
      register: job_result
      until: job_result.finished
      retries: 60
      delay: 30
```

### Security
- Use Ansible Vault for secrets
- Use `no_log: yes` for sensitive tasks
- Set proper file permissions
- Use `become` sparingly
- Validate SSL certificates
- Use SSH keys, not passwords

## Testing

### Molecule (Role Testing)
```bash
# Install molecule
pip install molecule molecule-docker

# Initialize molecule
cd roles/myapp
molecule init scenario

# Run tests
molecule test

# Test workflow
molecule create    # Create test instances
molecule converge  # Run playbook
molecule verify    # Run tests
molecule destroy   # Cleanup
```

```yaml
# molecule/default/molecule.yml
---
dependency:
  name: galaxy
driver:
  name: docker
platforms:
  - name: ubuntu
    image: geerlingguy/docker-ubuntu2004-ansible
    pre_build_image: yes
provisioner:
  name: ansible
verifier:
  name: ansible
```

## Anti-Patterns to Avoid

❌ **Not using roles**: Organize code in reusable roles
❌ **Shell commands everywhere**: Use modules when available
❌ **Hardcoded values**: Use variables
❌ **No error handling**: Use blocks, rescue, always
❌ **Storing secrets in plaintext**: Use Ansible Vault
❌ **Not testing**: Use molecule for role testing
❌ **Ignoring idempotency**: Tasks should be safe to run multiple times
❌ **Complex playbooks**: Break into smaller, focused playbooks

## Resources

- Ansible Documentation: https://docs.ansible.com/
- Ansible Galaxy: https://galaxy.ansible.com/
- Molecule: https://molecule.readthedocs.io/
- Best Practices: https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html

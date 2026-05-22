---
name: ansible
description: Ansible automation and configuration management patterns. Use when writing Ansible playbooks, roles, or automating infrastructure configuration and deployment tasks.
user-invocable: false
---

# Ansible Skill

This skill provides Ansible automation patterns and best practices.

## Playbook Structure

```yaml
---
- name: Configure web servers
  hosts: webservers
  become: true
  vars:
    http_port: 80

  tasks:
    - name: Install nginx
      ansible.builtin.apt:
        name: nginx
        state: present
      notify: Restart nginx

  handlers:
    - name: Restart nginx
      ansible.builtin.service:
        name: nginx
        state: restarted
```

## Role Structure

```
roles/
└── webserver/
    ├── defaults/main.yml    # Default variables
    ├── handlers/main.yml    # Handler definitions
    ├── tasks/main.yml       # Task list
    ├── templates/           # Jinja2 templates
    ├── files/               # Static files
    └── vars/main.yml        # Role variables
```

## Best Practices

### Use Fully Qualified Collection Names
```yaml
# ✅ Good
- ansible.builtin.apt:
    name: nginx

# ❌ Bad (ambiguous)
- apt:
    name: nginx
```

### Idempotent Tasks
```yaml
# Tasks should be safe to run multiple times
- name: Ensure config exists
  ansible.builtin.template:
    src: config.j2
    dest: /etc/app/config.yml
  # Only changes if content differs
```

### Use Handlers for Service Restarts
```yaml
tasks:
  - name: Update config
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    notify: Restart nginx

handlers:
  - name: Restart nginx
    service:
      name: nginx
      state: restarted
```

## Inventory Best Practices

```ini
[webservers]
web1.example.com
web2.example.com

[dbservers]
db1.example.com

[production:children]
webservers
dbservers
```

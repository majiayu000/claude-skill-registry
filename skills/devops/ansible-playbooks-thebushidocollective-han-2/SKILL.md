---
name: ansible-playbooks
description: Use when writing and organizing Ansible playbooks for automated configuration management and infrastructure orchestration.
allowed-tools: []
---

# Ansible Playbooks

Writing and organizing Ansible playbooks for configuration management.

## Basic Playbook

```yaml
---
- name: Configure web servers
  hosts: webservers
  become: yes
  
  vars:
    http_port: 80
    app_version: "1.0.0"
  
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: yes
    
    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: yes
    
    - name: Deploy application
      copy:
        src: ./app
        dest: /var/www/html
        owner: www-data
        mode: '0755'
```

## Inventory

```ini
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com

[production:children]
webservers
databases
```

## Common Modules

### Package Management

```yaml
- name: Install packages
  apt:
    name:
      - nginx
      - git
      - python3
    state: present
```

### File Operations

```yaml
- name: Copy configuration
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    backup: yes
  notify: Restart nginx
```

### Handlers

```yaml
handlers:
  - name: Restart nginx
    service:
      name: nginx
      state: restarted
```

## Best Practices

### Use Roles

```
roles/
├── webserver/
│   ├── tasks/
│   │   └── main.yml
│   ├── handlers/
│   │   └── main.yml
│   └── templates/
│       └── nginx.conf.j2
```

### Idempotency

```yaml
- name: Ensure directory exists
  file:
    path: /opt/app
    state: directory
    mode: '0755'
```

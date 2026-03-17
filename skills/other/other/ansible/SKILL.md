---
name: ansible
description: Ansible 自动化运维
version: 1.0.0
author: terminal-skills
tags: [devops, ansible, automation, configuration]
---

# Ansible 自动化运维

## 概述
Playbook 编写、角色管理、动态 inventory 等技能。

## 基础命令

### Ad-hoc 命令
```bash
# 测试连通性
ansible all -m ping
ansible webservers -m ping

# 执行命令
ansible all -m command -a "uptime"
ansible all -m shell -a "df -h | grep /dev"

# 复制文件
ansible all -m copy -a "src=/local/file dest=/remote/file"

# 安装软件
ansible all -m apt -a "name=nginx state=present" --become
ansible all -m yum -a "name=nginx state=present" --become

# 管理服务
ansible all -m service -a "name=nginx state=started" --become

# 收集信息
ansible all -m setup
ansible all -m setup -a "filter=ansible_distribution*"
```

### 常用参数
```bash
-i inventory          # 指定 inventory
-m module             # 指定模块
-a arguments          # 模块参数
-b, --become          # 提权
-K                    # 询问 sudo 密码
-u user               # 指定用户
-k                    # 询问 SSH 密码
--limit host          # 限制主机
-v, -vv, -vvv         # 详细输出
--check               # 检查模式（不执行）
--diff                # 显示差异
```

## Inventory

### 静态 inventory
```ini
# inventory/hosts
[webservers]
web1.example.com
web2.example.com ansible_host=192.168.1.10

[dbservers]
db1.example.com ansible_user=admin
db2.example.com

[production:children]
webservers
dbservers

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

### YAML 格式
```yaml
# inventory/hosts.yml
all:
  children:
    webservers:
      hosts:
        web1.example.com:
        web2.example.com:
          ansible_host: 192.168.1.10
    dbservers:
      hosts:
        db1.example.com:
          ansible_user: admin
  vars:
    ansible_python_interpreter: /usr/bin/python3
```

### 动态 inventory
```bash
# 使用脚本
ansible-inventory -i inventory.py --list

# AWS EC2
ansible-inventory -i aws_ec2.yml --list

# 示例 aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions:
  - us-east-1
filters:
  tag:Environment: production
keyed_groups:
  - key: tags.Role
    prefix: role
```

## Playbook

### 基础结构
```yaml
# playbook.yml
---
- name: Configure web servers
  hosts: webservers
  become: yes
  vars:
    http_port: 80
    
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
        
    - name: Copy config
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

### 执行 Playbook
```bash
# 执行
ansible-playbook playbook.yml

# 指定 inventory
ansible-playbook -i inventory/hosts playbook.yml

# 限制主机
ansible-playbook playbook.yml --limit web1

# 检查模式
ansible-playbook playbook.yml --check --diff

# 指定标签
ansible-playbook playbook.yml --tags "install,config"
ansible-playbook playbook.yml --skip-tags "test"

# 传递变量
ansible-playbook playbook.yml -e "version=1.0"
ansible-playbook playbook.yml -e "@vars.yml"
```

### 条件与循环
```yaml
tasks:
  # 条件
  - name: Install on Debian
    apt:
      name: nginx
    when: ansible_os_family == "Debian"
    
  - name: Install on RedHat
    yum:
      name: nginx
    when: ansible_os_family == "RedHat"
    
  # 循环
  - name: Install packages
    apt:
      name: "{{ item }}"
      state: present
    loop:
      - nginx
      - git
      - curl
      
  # 字典循环
  - name: Create users
    user:
      name: "{{ item.name }}"
      groups: "{{ item.groups }}"
    loop:
      - { name: 'user1', groups: 'admin' }
      - { name: 'user2', groups: 'developers' }
```

### 变量与模板
```yaml
# vars/main.yml
http_port: 80
server_name: example.com
workers: 4

# templates/nginx.conf.j2
server {
    listen {{ http_port }};
    server_name {{ server_name }};
    
    {% for upstream in upstreams %}
    upstream {{ upstream.name }} {
        {% for server in upstream.servers %}
        server {{ server }};
        {% endfor %}
    }
    {% endfor %}
}
```

## Roles

### 角色结构
```
roles/
└── nginx/
    ├── tasks/
    │   └── main.yml
    ├── handlers/
    │   └── main.yml
    ├── templates/
    │   └── nginx.conf.j2
    ├── files/
    ├── vars/
    │   └── main.yml
    ├── defaults/
    │   └── main.yml
    └── meta/
        └── main.yml
```

### 创建角色
```bash
# 创建角色骨架
ansible-galaxy init roles/nginx
```

### 使用角色
```yaml
# playbook.yml
---
- hosts: webservers
  become: yes
  roles:
    - nginx
    - { role: app, tags: ['app'] }
    - role: database
      vars:
        db_name: mydb
```

### Ansible Galaxy
```bash
# 安装角色
ansible-galaxy install geerlingguy.nginx
ansible-galaxy install -r requirements.yml

# requirements.yml
roles:
  - name: geerlingguy.nginx
    version: 3.1.0
  - name: geerlingguy.mysql

collections:
  - name: community.general
```

## 常见场景

### 场景 1：部署应用
```yaml
---
- name: Deploy application
  hosts: appservers
  become: yes
  vars:
    app_version: "1.0.0"
    
  tasks:
    - name: Pull code
      git:
        repo: https://github.com/user/app.git
        dest: /opt/app
        version: "{{ app_version }}"
        
    - name: Install dependencies
      pip:
        requirements: /opt/app/requirements.txt
        virtualenv: /opt/app/venv
        
    - name: Copy systemd service
      template:
        src: app.service.j2
        dest: /etc/systemd/system/app.service
      notify: Restart app
      
  handlers:
    - name: Restart app
      systemd:
        name: app
        state: restarted
        daemon_reload: yes
```

### 场景 2：滚动更新
```yaml
---
- name: Rolling update
  hosts: webservers
  serial: 1                           # 每次更新一台
  max_fail_percentage: 0
  
  tasks:
    - name: Remove from load balancer
      # ...
      
    - name: Update application
      # ...
      
    - name: Add back to load balancer
      # ...
```

### 场景 3：密钥管理
```bash
# 创建加密文件
ansible-vault create secrets.yml

# 编辑加密文件
ansible-vault edit secrets.yml

# 加密现有文件
ansible-vault encrypt vars.yml

# 解密
ansible-vault decrypt vars.yml

# 使用加密变量
ansible-playbook playbook.yml --ask-vault-pass
ansible-playbook playbook.yml --vault-password-file=.vault_pass
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| SSH 连接失败 | 检查 inventory、SSH 配置 |
| 权限不足 | 使用 `--become`、检查 sudo |
| 模块错误 | 使用 `-vvv` 查看详情 |
| 变量未定义 | 检查变量文件、优先级 |

```bash
# 调试模式
ansible-playbook playbook.yml -vvv

# 检查语法
ansible-playbook playbook.yml --syntax-check

# 列出任务
ansible-playbook playbook.yml --list-tasks

# 列出主机
ansible-playbook playbook.yml --list-hosts
```

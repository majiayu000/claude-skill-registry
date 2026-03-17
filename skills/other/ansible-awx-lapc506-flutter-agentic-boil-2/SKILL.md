# 🔧 Skill: Ansible AWX Automation

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `cicd-ansible-awx` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `ansible`, `awx`, `automation`, `configuration-management` |

## 🔑 Keywords

- `ansible`, `awx`, `tower`, `automation`, `playbook`, `@skill:ansible-awx`

## 📖 Descripción

Ansible AWX (upstream de Red Hat Ansible Tower) proporciona UI web y API REST para gestión de playbooks Ansible, ideal para automatizar configuración y deployment de backends Flutter.

## 💻 Implementación

### 1. Install AWX on Kubernetes

```yaml
# awx-operator.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: awx
---
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: awx-operator
  namespace: awx
spec:
  channel: stable
  name: awx-operator
  source: operatorhubio-catalog
  sourceNamespace: olm
```

```yaml
# awx-instance.yaml
apiVersion: awx.ansible.com/v1beta1
kind: AWX
metadata:
  name: awx-prod
  namespace: awx
spec:
  service_type: LoadBalancer
  ingress_type: Ingress
  hostname: awx.myapp.com
  admin_user: admin
  admin_password_secret: awx-admin-password
```

### 2. Playbook para Deploy Backend

```yaml
# playbooks/deploy-backend.yml
---
- name: Deploy Flutter Backend
  hosts: backend_servers
  become: yes
  vars:
    app_name: myapp-backend
    app_version: "{{ version | default('latest') }}"
    app_port: 3000
    
  tasks:
    - name: Pull Docker image
      docker_image:
        name: "myorg/{{ app_name }}"
        tag: "{{ app_version }}"
        source: pull
    
    - name: Stop existing container
      docker_container:
        name: "{{ app_name }}"
        state: stopped
      ignore_errors: yes
    
    - name: Remove existing container
      docker_container:
        name: "{{ app_name }}"
        state: absent
      ignore_errors: yes
    
    - name: Start new container
      docker_container:
        name: "{{ app_name }}"
        image: "myorg/{{ app_name }}:{{ app_version }}"
        state: started
        restart_policy: always
        published_ports:
          - "{{ app_port }}:{{ app_port }}"
        env:
          NODE_ENV: production
          DATABASE_URL: "{{ database_url }}"
          REDIS_URL: "{{ redis_url }}"
        networks:
          - name: backend-network
    
    - name: Wait for service to be ready
      uri:
        url: "http://localhost:{{ app_port }}/health"
        status_code: 200
      register: result
      until: result.status == 200
      retries: 30
      delay: 2
```

### 3. Playbook para Database Migration

```yaml
# playbooks/db-migrate.yml
---
- name: Run Database Migrations
  hosts: db_server
  vars:
    db_host: "{{ lookup('env', 'DB_HOST') }}"
    db_name: myapp_prod
    
  tasks:
    - name: Check if migrations table exists
      postgresql_query:
        login_host: "{{ db_host }}"
        login_user: "{{ db_user }}"
        login_password: "{{ db_password }}"
        db: "{{ db_name }}"
        query: "SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = 'migrations');"
      register: migrations_exist
    
    - name: Run migrations
      command: npm run migrate
      args:
        chdir: /app/backend
      environment:
        DATABASE_URL: "postgresql://{{ db_user }}:{{ db_password }}@{{ db_host }}/{{ db_name }}"
```

### 4. Playbook para Kubernetes Deployment

```yaml
# playbooks/k8s-deploy.yml
---
- name: Deploy to Kubernetes
  hosts: localhost
  connection: local
  vars:
    namespace: production
    app_name: myapp-backend
    image_tag: "{{ version }}"
    
  tasks:
    - name: Create namespace if not exists
      k8s:
        state: present
        definition:
          apiVersion: v1
          kind: Namespace
          metadata:
            name: "{{ namespace }}"
    
    - name: Deploy application
      k8s:
        state: present
        definition:
          apiVersion: apps/v1
          kind: Deployment
          metadata:
            name: "{{ app_name }}"
            namespace: "{{ namespace }}"
          spec:
            replicas: 3
            selector:
              matchLabels:
                app: "{{ app_name }}"
            template:
              metadata:
                labels:
                  app: "{{ app_name }}"
              spec:
                containers:
                - name: "{{ app_name }}"
                  image: "myorg/{{ app_name }}:{{ image_tag }}"
                  ports:
                  - containerPort: 3000
                  env:
                  - name: NODE_ENV
                    value: production
    
    - name: Expose service
      k8s:
        state: present
        definition:
          apiVersion: v1
          kind: Service
          metadata:
            name: "{{ app_name }}"
            namespace: "{{ namespace }}"
          spec:
            selector:
              app: "{{ app_name }}"
            ports:
            - port: 80
              targetPort: 3000
            type: LoadBalancer
```

### 5. AWX Job Templates

```yaml
# Via AWX API
curl -X POST https://awx.myapp.com/api/v2/job_templates/ \
  -H "Authorization: Bearer $AWX_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Deploy Backend to Production",
    "job_type": "run",
    "inventory": 1,
    "project": 1,
    "playbook": "playbooks/deploy-backend.yml",
    "extra_vars": "{\"version\": \"v1.0.0\"}",
    "ask_variables_on_launch": true
  }'
```

### 6. Inventory Configuration

```ini
# inventory/production.ini
[backend_servers]
backend-1 ansible_host=10.0.1.10 ansible_user=ubuntu
backend-2 ansible_host=10.0.1.11 ansible_user=ubuntu
backend-3 ansible_host=10.0.1.12 ansible_user=ubuntu

[db_server]
db-1 ansible_host=10.0.2.10 ansible_user=ubuntu

[all:vars]
ansible_python_interpreter=/usr/bin/python3
ansible_become=yes
```

## 🎯 Mejores Prácticas

1. **Use Ansible Vault** para secrets
2. **Tag tasks** para ejecución selectiva
3. **Idempotent playbooks** - safe to re-run
4. **Roles para reutilización** de código
5. **Job Templates** en AWX para self-service
6. **Workflows** para pipelines complejos
7. **Surveys** para inputs dinámicos

## 📚 Recursos

- [Ansible Documentation](https://docs.ansible.com/)
- [AWX Documentation](https://ansible.readthedocs.io/projects/awx/)

---

**Versión:** 1.0.0


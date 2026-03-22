---
name: ansible
description: Run Ansible playbooks and manage AWX/Tower via API. Automate infrastructure configuration.
metadata: {"thinkfleet":{"emoji":"🅰️","requires":{"env":["AWX_URL","AWX_TOKEN"]}}}
---
# Ansible / AWX
Infrastructure automation.
## Environment
```bash
export AWX_URL="https://awx.example.com"
export AWX_TOKEN="xxxxxxxxxx"
```
## List Job Templates
```bash
curl "$AWX_URL/api/v2/job_templates/" -H "Authorization: Bearer $AWX_TOKEN"
```
## Launch Job
```bash
curl -X POST "$AWX_URL/api/v2/job_templates/{id}/launch/" \
  -H "Authorization: Bearer $AWX_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"extra_vars": {"host": "webserver"}}'
```
## Get Job Status
```bash
curl "$AWX_URL/api/v2/jobs/{jobId}/" -H "Authorization: Bearer $AWX_TOKEN"
```
## Run Ansible CLI
```bash
ansible-playbook -i inventory.yml playbook.yml
ansible all -m ping -i inventory.yml
```
## Links
- Docs: https://docs.ansible.com

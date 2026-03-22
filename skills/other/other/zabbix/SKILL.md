---
name: zabbix
description: >-
  Configure Zabbix for enterprise infrastructure monitoring with templates,
  triggers, discovery rules, and dashboards. Use when a user needs to set up
  Zabbix server, configure host monitoring, create custom templates, define
  trigger expressions, or automate host discovery and registration.
license: Apache-2.0
compatibility: "Zabbix 6.4+, Zabbix Agent 2"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: devops
  tags: ["zabbix", "enterprise-monitoring", "templates", "triggers", "discovery"]
---

# Zabbix

## Overview

Set up Zabbix for enterprise monitoring with host configuration, templates, trigger expressions, low-level discovery, and API automation. Covers server deployment, agent setup, and dashboard creation.

## Instructions

### Task A: Deploy Zabbix Server

```yaml
# docker-compose.yml — Zabbix server with PostgreSQL and web frontend
services:
  zabbix-server:
    image: zabbix/zabbix-server-pgsql:6.4-ubuntu-latest
    environment:
      - DB_SERVER_HOST=postgres
      - POSTGRES_USER=zabbix
      - POSTGRES_PASSWORD=zabbix_password
      - POSTGRES_DB=zabbix
      - ZBX_CACHESIZE=128M
      - ZBX_HISTORYCACHESIZE=64M
      - ZBX_TRENDCACHESIZE=32M
    ports:
      - "10051:10051"
    depends_on:
      - postgres

  zabbix-web:
    image: zabbix/zabbix-web-nginx-pgsql:6.4-ubuntu-latest
    environment:
      - DB_SERVER_HOST=postgres
      - POSTGRES_USER=zabbix
      - POSTGRES_PASSWORD=zabbix_password
      - POSTGRES_DB=zabbix
      - ZBX_SERVER_HOST=zabbix-server
      - PHP_TZ=America/New_York
    ports:
      - "8080:8080"

  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=zabbix
      - POSTGRES_PASSWORD=zabbix_password
      - POSTGRES_DB=zabbix
    volumes:
      - pg_data:/var/lib/postgresql/data

volumes:
  pg_data:
```

### Task B: Install and Configure Zabbix Agent 2

```bash
# Install Zabbix Agent 2 on Ubuntu
wget https://repo.zabbix.com/zabbix/6.4/ubuntu/pool/main/z/zabbix-release/zabbix-release_6.4-1+ubuntu22.04_all.deb
sudo dpkg -i zabbix-release_6.4-1+ubuntu22.04_all.deb
sudo apt-get update
sudo apt-get install -y zabbix-agent2 zabbix-agent2-plugin-*
```

```ini
# /etc/zabbix/zabbix_agent2.conf — Agent 2 configuration
Server=192.168.1.5
ServerActive=192.168.1.5
Hostname=web-01.production
HostMetadata=linux:web:production:ubuntu
ListenPort=10050
Timeout=10

Plugins.SystemRun.LogRemoteCommands=1

# Enable PostgreSQL monitoring plugin
Plugins.PostgreSQL.Sessions.mydb.Uri=tcp://localhost:5432
Plugins.PostgreSQL.Sessions.mydb.User=zbx_monitor
Plugins.PostgreSQL.Sessions.mydb.Password=monitor_password
```

### Task C: Create Custom Templates via API

```bash
# Authenticate and get token
AUTH_TOKEN=$(curl -s "http://localhost:8080/api_jsonrpc.php" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": { "username": "Admin", "password": "zabbix" },
    "id": 1
  }' | jq -r '.result')
```

```bash
# Create a custom template
curl -s "http://localhost:8080/api_jsonrpc.php" \
  -H "Content-Type: application/json" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"method\": \"template.create\",
    \"params\": {
      \"host\": \"Custom Web Application\",
      \"groups\": [{ \"groupid\": \"1\" }],
      \"description\": \"Monitors web application health, response times, and error rates\"
    },
    \"auth\": \"${AUTH_TOKEN}\",
    \"id\": 2
  }"
```

```bash
# Create items (metrics) on the template
curl -s "http://localhost:8080/api_jsonrpc.php" \
  -H "Content-Type: application/json" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"method\": \"item.create\",
    \"params\": [
      {
        \"name\": \"HTTP response time\",
        \"key_\": \"web.page.perf[https://app.example.com,,,443]\",
        \"hostid\": \"TEMPLATE_ID\",
        \"type\": 0,
        \"value_type\": 0,
        \"delay\": \"60s\",
        \"units\": \"s\",
        \"description\": \"Response time of the main application page\"
      },
      {
        \"name\": \"HTTP status code\",
        \"key_\": \"web.page.get[https://app.example.com,,,443]\",
        \"hostid\": \"TEMPLATE_ID\",
        \"type\": 0,
        \"value_type\": 3,
        \"delay\": \"60s\",
        \"preprocessing\": [
          { \"type\": \"REGEX\", \"params\": \"HTTP/[0-9.]+ ([0-9]+)\\n\\\\1\" }
        ]
      }
    ],
    \"auth\": \"${AUTH_TOKEN}\",
    \"id\": 3
  }"
```

### Task D: Define Triggers

```bash
# Create trigger expressions via API
curl -s "http://localhost:8080/api_jsonrpc.php" \
  -H "Content-Type: application/json" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"method\": \"trigger.create\",
    \"params\": [
      {
        \"description\": \"High CPU usage on {HOST.NAME}\",
        \"expression\": \"avg(/Custom Web Application/system.cpu.util,5m)>85\",
        \"recovery_expression\": \"avg(/Custom Web Application/system.cpu.util,5m)<70\",
        \"priority\": 4,
        \"manual_close\": 1,
        \"tags\": [
          { \"tag\": \"scope\", \"value\": \"performance\" },
          { \"tag\": \"service\", \"value\": \"web\" }
        ]
      },
      {
        \"description\": \"Disk space critically low on {HOST.NAME}\",
        \"expression\": \"last(/Custom Web Application/vfs.fs.size[/,pfree])<10\",
        \"priority\": 5,
        \"tags\": [
          { \"tag\": \"scope\", \"value\": \"capacity\" }
        ]
      },
      {
        \"description\": \"HTTP response time too high on {HOST.NAME}\",
        \"expression\": \"avg(/Custom Web Application/web.page.perf[https://app.example.com,,,443],5m)>3\",
        \"priority\": 3,
        \"tags\": [
          { \"tag\": \"scope\", \"value\": \"availability\" }
        ]
      }
    ],
    \"auth\": \"${AUTH_TOKEN}\",
    \"id\": 4
  }"
```

### Task E: Low-Level Discovery

```bash
# Create a discovery rule for Docker containers
curl -s "http://localhost:8080/api_jsonrpc.php" \
  -H "Content-Type: application/json" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"method\": \"discoveryrule.create\",
    \"params\": {
      \"name\": \"Docker container discovery\",
      \"key_\": \"docker.containers.discovery[true]\",
      \"hostid\": \"TEMPLATE_ID\",
      \"type\": 0,
      \"delay\": \"5m\",
      \"lifetime\": \"7d\"
    },
    \"auth\": \"${AUTH_TOKEN}\",
    \"id\": 5
  }"
```

```bash
# Create item prototypes for discovered containers
curl -s "http://localhost:8080/api_jsonrpc.php" \
  -H "Content-Type: application/json" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"method\": \"itemprototype.create\",
    \"params\": {
      \"name\": \"Container {#NAME}: CPU usage\",
      \"key_\": \"docker.container_info[{#NAME},cpu_percent]\",
      \"hostid\": \"TEMPLATE_ID\",
      \"ruleid\": \"DISCOVERY_RULE_ID\",
      \"type\": 0,
      \"value_type\": 0,
      \"delay\": \"30s\",
      \"units\": \"%\"
    },
    \"auth\": \"${AUTH_TOKEN}\",
    \"id\": 6
  }"
```

### Task F: Auto-Registration

```bash
# Configure auto-registration action via API
curl -s "http://localhost:8080/api_jsonrpc.php" \
  -H "Content-Type: application/json" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"method\": \"action.create\",
    \"params\": {
      \"name\": \"Auto-register Linux web servers\",
      \"eventsource\": 2,
      \"filter\": {
        \"evaltype\": 0,
        \"conditions\": [
          { \"conditiontype\": 24, \"value\": \"linux:web:production\" }
        ]
      },
      \"operations\": [
        { \"operationtype\": 2 },
        { \"operationtype\": 4, \"opgroup\": [{ \"groupid\": \"WEB_GROUP_ID\" }] },
        { \"operationtype\": 6, \"optemplate\": [{ \"templateid\": \"TEMPLATE_ID\" }] }
      ]
    },
    \"auth\": \"${AUTH_TOKEN}\",
    \"id\": 7
  }"
```

## Best Practices

- Use Zabbix Agent 2 (Go-based) over legacy Agent for better plugin support and performance
- Leverage templates to standardize monitoring — apply templates to host groups, not individual hosts
- Use `HostMetadata` in agent config for automatic registration and template linking
- Set recovery expressions on triggers to prevent flapping between OK and PROBLEM states
- Use low-level discovery for dynamic infrastructure (containers, disks, network interfaces)
- Tag triggers and hosts for organized alerting and dashboard filtering

---
name: consul
description: >-
  HashiCorp Consul for service discovery, health checking, and service mesh.
  Use when the user needs to register services, perform health checks, store
  configuration in the KV store, or set up Connect for secure service-to-service
  communication.
license: Apache-2.0
compatibility: 'linux, macos, windows'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: devops
  tags:
    - consul
    - service-discovery
    - service-mesh
    - hashicorp
    - infrastructure
---

# Consul

Consul provides service discovery, health checking, KV storage, and service mesh capabilities.

## Installation

```bash
# Install Consul
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install consul

# Start dev agent
consul agent -dev

# Check cluster members
consul members
```

## Server Configuration

```hcl
# consul-server.hcl — Production Consul server config
datacenter = "dc1"
data_dir   = "/opt/consul/data"
log_level  = "INFO"

server           = true
bootstrap_expect = 3

bind_addr   = "{{ GetPrivateInterfaces | include \"network\" \"10.0.0.0/8\" | attr \"address\" }}"
client_addr = "0.0.0.0"

ui_config { enabled = true }

connect { enabled = true }

addresses {
  http  = "0.0.0.0"
  grpc  = "0.0.0.0"
}

ports {
  grpc = 8502
}

encrypt = "your-gossip-encryption-key"

acl {
  enabled                  = true
  default_policy           = "deny"
  enable_token_persistence = true
}

tls {
  defaults {
    ca_file   = "/opt/consul/tls/ca.pem"
    cert_file = "/opt/consul/tls/server.pem"
    key_file  = "/opt/consul/tls/server-key.pem"
    verify_incoming = true
    verify_outgoing = true
  }
}

autopilot {
  cleanup_dead_servers = true
  last_contact_threshold = "200ms"
  server_stabilization_time = "10s"
}
```

## Service Registration

```json
// services/web.json — Register web service with health check
{
  "service": {
    "name": "web",
    "port": 8080,
    "tags": ["production", "v2"],
    "meta": {
      "version": "2.0.0"
    },
    "check": {
      "http": "http://localhost:8080/health",
      "interval": "10s",
      "timeout": "5s",
      "deregister_critical_service_after": "30m"
    }
  }
}
```

```bash
# Register and query services via CLI
consul services register services/web.json
consul services deregister -id=web

# DNS-based service discovery
dig @127.0.0.1 -p 8600 web.service.consul SRV

# HTTP API service discovery
curl http://localhost:8500/v1/health/service/web?passing=true

# Catalog queries
consul catalog services
consul catalog nodes
```

## KV Store

```bash
# Key-value operations
consul kv put config/app/db_host "db.example.com"
consul kv put config/app/db_port "5432"

consul kv get config/app/db_host
consul kv get -recurse config/app/

# Import/export
consul kv export config/ > backup.json
consul kv import @backup.json

# Delete keys
consul kv delete config/app/db_host
consul kv delete -recurse config/app/

# Watch for changes
consul watch -type=key -key=config/app/db_host /scripts/reload.sh
```

## Service Mesh (Connect)

```hcl
# connect-proxy.hcl — Service with sidecar proxy
service {
  name = "web"
  port = 8080

  connect {
    sidecar_service {
      proxy {
        upstreams {
          destination_name = "api"
          local_bind_port  = 9091
        }
        upstreams {
          destination_name = "database"
          local_bind_port  = 9092
        }
      }
    }
  }
}
```

```hcl
# intentions.hcl — Service intentions for access control
Kind = "service-intentions"
Name = "api"
Sources = [
  {
    Name   = "web"
    Action = "allow"
  },
  {
    Name   = "*"
    Action = "deny"
  }
]
```

```bash
# Manage intentions
consul config write intentions.hcl
consul intention list
consul intention check web api
```

## Prepared Queries

```bash
# Create prepared query for failover across datacenters
curl -X POST http://localhost:8500/v1/query -d '{
  "Name": "web-query",
  "Service": {
    "Service": "web",
    "Tags": ["production"],
    "Failover": {
      "Datacenters": ["dc2", "dc3"]
    },
    "OnlyPassing": true
  }
}'
```

## ACL Configuration

```bash
# Bootstrap ACL system
consul acl bootstrap

# Create policy
consul acl policy create -name "app-read" \
  -rules='service_prefix "web" { policy = "read" } key_prefix "config/app" { policy = "read" }'

# Create token with policy
consul acl token create -description "App token" -policy-name "app-read"
```

## Common Commands

```bash
# Cluster management
consul join 10.0.1.10
consul leave
consul operator raft list-peers
consul operator autopilot state

# Snapshots for backup
consul snapshot save backup.snap
consul snapshot restore backup.snap

# Monitor and debug
consul monitor -log-level=debug
consul debug -duration=30s -interval=5s
```

---
name: consul
description: HashiCorp Consul service discovery and mesh. Use for service discovery.
---

# Consul

HashiCorp Consul is a multi-cloud service networking platform. It handles Service Discovery, Mesh, and Key/Value storage. 2025 v1.18 focuses on Enterprise reliability.

## When to Use

- **Service Discovery**: Tracking dynamic IPs of microservices (common in Nomad/VM setups).
- **Service Mesh**: mTLS and Traffic split across VMs and K8s.
- **KV Store**: Storing dynamic configuration distributed across regions.

## Core Concepts

### Agent

Runs on every node (client mode) or dedicated servers (server mode). Handles health checks.

### Service Definition

Register services via Config file or API.
`{"service": {"name": "web", "port": 80}}`

### Connect (Mesh)

Uses Envoy to secure traffic between services.

## Best Practices (2025)

**Do**:

- **Use DNS Interface**: Apps can find DBs via `db.service.consul`.
- **Use Template**: `consul-template` renders config files from KV data and reloads apps automatically.
- **Separate Data Centers**: Federation allows global service discovery.

**Don't**:

- **Don't expose API publicly**: Consul has no default auth in dev mode. Lock it down.

## References

- [Consul Documentation](https://developer.hashicorp.com/consul)

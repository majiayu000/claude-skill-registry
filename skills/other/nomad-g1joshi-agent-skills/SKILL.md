---
name: nomad
description: HashiCorp Nomad workload orchestration. Use for job scheduling.
---

# Nomad

HashiCorp Nomad is a flexible scheduler that orchestrates just about anything: containers, binaries, or VMs. Nomad 1.8+ (2025) focuses on **Workload Identity** (JWT) for secure, secret-less authentication.

## When to Use

- **Simplicity**: You don't need the complexity of Kubernetes (etcd, controllers, CRDs).
- **Non-Container Workloads**: You need to orchestrate raw `java -jar` or `nginx` binaries directly on Linux/Windows.
- **Edge**: Single binary, low resource usage.

## Quick Start

```hcl
job "example" {
  datacenters = ["dc1"]

  group "cache" {
    task "redis" {
      driver = "docker"

      config {
        image = "redis:7"
      }

      resources {
        cpu    = 500 # 500 MHz
        memory = 256 # 256 MB
      }
    }
  }
}
```

## Core Concepts

### Jobs

The unit of work. Defined in HCL (HashiCorp Configuration Language).

### Drivers

Nomad uses drivers to run tasks: `docker`, `exec` (raw binaries), `java`, `qemu` (VMs).

### Workload Identity

Nomad issues a JWT to running tasks. Tasks generally trade this JWT with Vault to get database passwords or AWS keys, removing the need to hardcode secrets.

## Best Practices (2025)

**Do**:

- **Use Workload Identity**: Integrate with Vault and Consul securely.
- **Use Consul Connect**: For service mesh features (mTLS, observability) between tasks.
- **Keep it Simple**: Don't try to reimplement K8s on top of Nomad. Embrace the simplicity.

**Don't**:

- **Don't ignore state**: Nomad handles stateful workloads, but K8s has a richer ecosystem of Operators for complex databases. Stick to stateless or simple stateful (Redis) on Nomad if possible.

## References

- [Nomad Documentation](https://developer.hashicorp.com/nomad)

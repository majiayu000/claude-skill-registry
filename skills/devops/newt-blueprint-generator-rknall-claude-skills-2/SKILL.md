---
name: "Newt Blueprint Generator"
description: "Generate and validate Pangolin Newt blueprint configurations in YAML or Docker Labels format. Use when creating Pangolin resource configurations, proxy resources, client resources, authentication settings, or Docker Compose blueprints."
---

# Newt Blueprint Generator

Expert assistance for creating, validating, and managing Pangolin Newt blueprint configurations.

## When to Use This Skill

This skill should be triggered when:
- Creating Pangolin blueprint configurations
- Generating YAML configuration files for Newt
- Creating Docker Compose files with Pangolin labels
- Configuring proxy resources (HTTP, TCP, UDP)
- Setting up client resources for Olm
- Configuring authentication (SSO, basic auth, pincode, password)
- Validating blueprint configurations
- Troubleshooting blueprint validation errors
- Converting between YAML and Docker Labels formats

## Overview

Pangolin Blueprints are declarative configurations that allow you to define resources and their settings in a structured format. They support two formats:

1. **YAML Configuration Files**: Standalone configuration files
2. **Docker Labels**: Configuration embedded in Docker Compose files

## Blueprint Formats

### YAML Configuration Format

YAML configs can be applied using:
- **Newt CLI**: Pass `--blueprint-file /path/to/blueprint.yaml`
- **API**: POST to `/org/{orgId}/blueprint` with base64-encoded JSON body

Example Newt usage:
```bash
newt --blueprint-file /path/to/blueprint.yaml <other-args>
```

### Docker Labels Format

For containerized applications, blueprints can be defined using Docker labels with the `pangolin.` prefix.

Enable Docker socket access:
```bash
newt --docker-socket /var/run/docker.sock <other-args>
```

Or use environment variable:
```bash
DOCKER_SOCKET=/var/run/docker.sock
```

## Resource Types

### Proxy Resources

Proxy resources expose HTTP, TCP, or UDP services through Pangolin.

#### HTTP Proxy Resource Example

```yaml
proxy-resources:
  resource-nice-id-uno:
    name: this is a http resource
    protocol: http
    full-domain: uno.example.com
    host-header: example.com
    tls-server-name: example.com
    headers:
      - name: X-Example-Header
        value: example-value
      - name: X-Another-Header
        value: another-value
    rules:
      - action: allow
        match: ip
        value: 1.1.1.1
      - action: deny
        match: cidr
        value: 2.2.2.2/32
      - action: pass
        match: path
        value: /admin
    targets:
      - site: lively-yosemite-toad
        hostname: localhost
        method: http
        port: 8000
      - site: slim-alpine-chipmunk
        hostname: localhost
        path: /admin
        path-match: exact
        method: https
        port: 8001
```

#### TCP/UDP Proxy Resource Example

```yaml
proxy-resources:
  resource-nice-id-dos:
    name: this is a raw resource
    protocol: tcp
    proxy-port: 3000
    targets:
      - site: lively-yosemite-toad
        hostname: localhost
        port: 3000
```

#### Targets-Only Resources

Simplified resources containing only target configurations:

```yaml
proxy-resources:
  additional-targets:
    targets:
      - site: another-site
        hostname: backend-server
        method: https
        port: 8443
      - site: another-site
        hostname: backup-server
        method: http
        port: 8080
```

**Note**: When using targets-only resources, `name` and `protocol` fields are not required.

### Client Resources

Client resources define proxied resources accessible via Olm client (SSH, RDP):

```yaml
client-resources:
  client-resource-nice-id-uno:
    name: this is my resource
    protocol: tcp
    proxy-port: 3001
    hostname: localhost
    internal-port: 3000
    site: lively-yosemite-toad
```

## Authentication Configuration

Authentication is **off by default**. Enable by adding fields in the `auth` section.

**Note**: Authentication is only allowed on HTTP resources, not TCP/UDP.

```yaml
proxy-resources:
  secure-resource:
    name: Secured Resource
    protocol: http
    full-domain: secure.example.com
    auth:
      pincode: 123456
      password: your-secure-password
      basic-auth:
        user: asdfa
        password: sadf
      sso-enabled: true
      sso-roles:
        - Member
        - Admin
      sso-users:
        - user@example.com
      whitelist-users:
        - admin@example.com
```

## Docker Labels Format

### Complete Docker Compose Example

```yaml
services:
  newt:
    image: fosrl/newt
    container_name: newt
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - PANGOLIN_ENDPOINT=https://app.pangolin.net
      - NEWT_ID=h1rbsgku89wf9z3
      - NEWT_SECRET=z7g54mbcwkglpx1aau9gb8mzcccoof2fdbs97keoakg2pp5z
      - DOCKER_SOCKET=/var/run/docker.sock

  nginx1:
    image: nginxdemos/hello
    container_name: nginx1
    labels:
      # Proxy Resource Configuration
      - pangolin.proxy-resources.nginx.name=nginx
      - pangolin.proxy-resources.nginx.full-domain=nginx.fosrl.io
      - pangolin.proxy-resources.nginx.protocol=http
      - pangolin.proxy-resources.nginx.headers[0].name=X-Example-Header
      - pangolin.proxy-resources.nginx.headers[0].value=example-value
      # Target Configuration - port and hostname auto-detected
      - pangolin.proxy-resources.nginx.targets[0].method=http
      - pangolin.proxy-resources.nginx.targets[0].path=/path
      - pangolin.proxy-resources.nginx.targets[0].path-match=prefix

  nginx2:
    image: nginxdemos/hello
    container_name: nginx2
    labels:
      # Additional target with explicit hostname and port
      - pangolin.proxy-resources.nginx.targets[1].method=http
      - pangolin.proxy-resources.nginx.targets[1].hostname=nginx2
      - pangolin.proxy-resources.nginx.targets[1].port=80

networks:
  default:
    name: pangolin_default
```

### Docker Labels Considerations

- **Automatic Discovery**: When hostname and internal port are not defined, Pangolin auto-detects from container configuration
- **Site Assignment**: If no site is specified, resource is assigned to the discovering Newt site
- **Configuration Merging**: Configuration across containers is merged to form complete resource definitions

## Configuration Properties Reference

### Proxy Resources Properties

| Property | Type | Required | Description | Constraints |
|----------|------|----------|-------------|-------------|
| `name` | string | Conditional | Human-readable name | Required unless targets-only |
| `protocol` | string | Conditional | Protocol type (`http`, `tcp`, `udp`) | Required unless targets-only |
| `full-domain` | string | HTTP only | Full domain name | Required for HTTP, must be unique |
| `proxy-port` | number | TCP/UDP only | Port for raw TCP/UDP | Required for TCP/UDP, 1-65535, must be unique |
| `ssl` | boolean | No | Enable SSL/TLS | - |
| `enabled` | boolean | No | Whether resource is enabled | Defaults to `true` |
| `host-header` | string | No | Custom Host header | - |
| `tls-server-name` | string | No | SNI name for TLS | - |
| `headers` | array | No | Custom headers | Each requires `name` and `value` (min 1 char) |
| `rules` | array | No | Access control rules | See Rules section |
| `auth` | object | HTTP only | Authentication config | See Authentication section |
| `targets` | array | Yes | Target endpoints | See Targets section |

### Target Configuration Properties

| Property | Type | Required | Description | Constraints |
|----------|------|----------|-------------|-------------|
| `site` | string | No | Site identifier | - |
| `hostname` | string | Yes | Target hostname or IP | - |
| `port` | number | Yes | Target port | 1-65535 |
| `method` | string | HTTP only | Protocol method (`http`, `https`, `h2c`) | Required for HTTP |
| `enabled` | boolean | No | Whether target is enabled | Defaults to `true` |
| `internal-port` | number | No | Internal port mapping | 1-65535 |
| `path` | string | HTTP only | Path prefix, exact, or regex | - |
| `path-match` | string | HTTP only | Path matching type (`prefix`, `exact`, `regex`) | - |

### Authentication Properties

**Not allowed on TCP/UDP resources.**

| Property | Type | Required | Description | Constraints |
|----------|------|----------|-------------|-------------|
| `pincode` | number | No | 6-digit PIN | Must be exactly 6 digits |
| `password` | string | No | Password for access | - |
| `basic-auth` | object | No | Basic auth config | Requires `user` and `password` |
| `sso-enabled` | boolean | No | Enable SSO | Defaults to `false` |
| `sso-roles` | array | No | Allowed SSO roles | Cannot include "Admin" role |
| `sso-users` | array | No | Allowed SSO user emails | Must be valid emails |
| `whitelist-users` | array | No | Whitelisted user emails | Must be valid emails |

### Rules Configuration Properties

| Property | Type | Required | Description | Constraints |
|----------|------|----------|-------------|-------------|
| `action` | string | Yes | Rule action (`allow`, `deny`, `pass`) | - |
| `match` | string | Yes | Match type (`cidr`, `path`, `ip`, `country`) | - |
| `value` | string | Yes | Value to match | Format depends on match type |

### Client Resources Properties

| Property | Type | Required | Description | Constraints |
|----------|------|----------|-------------|-------------|
| `name` | string | Yes | Human-readable name | 2-100 characters |
| `protocol` | string | Yes | Protocol type (`tcp`, `udp`) | - |
| `proxy-port` | number | Yes | Port accessible to clients | 1-65535, must be unique |
| `hostname` | string | Yes | Target hostname or IP | 1-255 characters |
| `internal-port` | number | Yes | Port on target system | 1-65535 |
| `site` | string | No | Site identifier | 2-100 characters |
| `enabled` | boolean | No | Whether resource is enabled | Defaults to `true` |

## Validation Rules and Constraints

### Resource-Level Validations

1. **Targets-Only Resources**: A resource can contain only `targets` field, making `name` and `protocol` optional
2. **Protocol-Specific Requirements**:
   - **HTTP Protocol**: Must have `full-domain` and all targets must have `method` field
   - **TCP/UDP Protocol**: Must have `proxy-port` and targets must NOT have `method` field
   - **TCP/UDP Protocol**: Cannot have `auth` configuration
3. **Port Uniqueness**:
   - `proxy-port` values must be unique within `proxy-resources`
   - `proxy-port` values must be unique within `client-resources`
   - Cross-validation between proxy and client resources is not enforced
4. **Domain Uniqueness**: `full-domain` values must be unique across all proxy resources
5. **Target Method Requirements**: When protocol is `http`, all non-null targets must specify a `method`

## Common Validation Errors

### "Admin role cannot be included in sso-roles"

The `Admin` role is reserved and cannot be included in the `sso-roles` array.

**Solution**: Remove "Admin" from the `sso-roles` array.

### "Duplicate 'full-domain' values found"

Each `full-domain` must be unique across all proxy resources.

**Solution**: Use different subdomains or paths for multiple resources.

### "Duplicate 'proxy-port' values found"

Port numbers in `proxy-port` must be unique within their resource type.

**Solution**: Assign unique port numbers within `proxy-resources` and `client-resources` separately.

### "When protocol is 'http', all targets must have a 'method' field"

All targets in HTTP proxy resources must specify the connection method.

**Solution**: Add `method: http`, `method: https`, or `method: h2c` to all targets.

### "When protocol is 'tcp' or 'udp', targets must not have a 'method' field"

TCP and UDP targets should not include the `method` field.

**Solution**: Remove the `method` field from TCP/UDP resource targets.

### "When protocol is 'tcp' or 'udp', 'auth' must not be provided"

Authentication is only supported for HTTP resources.

**Solution**: Remove the `auth` section from TCP/UDP resources.

### "Resource must either be targets-only or have both 'name' and 'protocol' fields"

Resources must be either targets-only or complete resource definitions.

**Solution**: Either provide only `targets` field, or include both `name` and `protocol` fields.

## Workflow for Generating Blueprints

When a user requests a Pangolin Newt blueprint configuration:

1. **Gather Requirements**:
   - Resource type (proxy or client)
   - Protocol (HTTP, TCP, UDP)
   - Domain or port requirements
   - Target endpoints (hostname, port, site)
   - Authentication needs (if HTTP)
   - Access control rules (if any)
   - Format preference (YAML or Docker Labels)

2. **Select Format**:
   - Use **YAML** for standalone configurations or API deployment
   - Use **Docker Labels** for containerized applications

3. **Validate Configuration**:
   - Ensure protocol-specific requirements are met
   - Check for unique `full-domain` (HTTP) or `proxy-port` (TCP/UDP)
   - Verify authentication is only on HTTP resources
   - Confirm all HTTP targets have `method` field
   - Ensure TCP/UDP targets don't have `method` field

4. **Generate Configuration**:
   - Create well-structured YAML or Docker Compose file
   - Include helpful comments explaining each section
   - Follow naming conventions (kebab-case for resource IDs)

5. **Provide Usage Instructions**:
   - Explain how to apply the configuration (Newt CLI or API)
   - Document any environment variables needed
   - Include validation commands if applicable

## Best Practices

1. **Resource IDs**: Use descriptive, kebab-case identifiers (e.g., `web-app-prod`, `database-backup`)
2. **Target Organization**: Group related targets under the same resource ID
3. **Security First**: Enable authentication for sensitive HTTP resources
4. **Port Management**: Document port assignments to avoid conflicts
5. **Site Assignment**: Explicitly specify `site` for multi-site deployments
6. **Path Matching**: Use `prefix` for broad matches, `exact` for specific endpoints
7. **Headers**: Add custom headers for backend requirements (e.g., X-Forwarded-* headers)
8. **Rules**: Order rules from most specific to least specific
9. **Validation**: Always validate configurations before deployment
10. **Documentation**: Include comments in YAML or Docker Compose files explaining non-obvious choices

## Resources

- **API Documentation**: https://api.pangolin.net/v1/docs/#/Organization/put_org__orgId__blueprint
- **Python Example**: https://github.com/fosrl/pangolin/blob/dev/blueprint.py
- **Official Docs**: https://docs.pangolin.net/manage/blueprints

## Example Use Cases

### Use Case 1: Simple Web Application

**Requirements**: Expose a web app running on localhost:8080 via HTTPS at app.example.com

```yaml
proxy-resources:
  web-app:
    name: Web Application
    protocol: http
    full-domain: app.example.com
    targets:
      - hostname: localhost
        port: 8080
        method: https
```

### Use Case 2: TCP Database Access

**Requirements**: Expose PostgreSQL database on port 5432

```yaml
proxy-resources:
  postgres-db:
    name: PostgreSQL Database
    protocol: tcp
    proxy-port: 5432
    targets:
      - hostname: localhost
        port: 5432
```

### Use Case 3: Multi-Target Load Balanced HTTP Service

**Requirements**: Multiple backend servers for the same domain

```yaml
proxy-resources:
  api-service:
    name: API Service
    protocol: http
    full-domain: api.example.com
    targets:
      - site: site-01
        hostname: backend-01
        port: 8080
        method: http
      - site: site-02
        hostname: backend-02
        port: 8080
        method: http
```

### Use Case 4: Secured Resource with SSO

**Requirements**: Web app with SSO authentication

```yaml
proxy-resources:
  secure-app:
    name: Secure Application
    protocol: http
    full-domain: secure.example.com
    auth:
      sso-enabled: true
      sso-roles:
        - Member
        - Developer
      sso-users:
        - admin@example.com
    targets:
      - hostname: localhost
        port: 3000
        method: https
```

## Communication Style

When generating blueprints:
- Ask clarifying questions if requirements are unclear
- Explain validation errors in plain language
- Provide complete, working examples
- Include comments for complex configurations
- Suggest security best practices proactively
- Offer both YAML and Docker Labels formats when appropriate

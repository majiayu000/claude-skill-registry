---
name: keycloak-administration
description: Provides comprehensive KeyCloak administration guidance including realm management, user/group administration, client configuration, authentication flows, identity brokering, authorization policies, security hardening, and troubleshooting. Covers SSO configuration, SAML/OIDC setup, role-based access control (RBAC), user federation (LDAP/AD), social login integration, multi-factor authentication (MFA), and high availability deployments. Use when configuring KeyCloak, setting up SSO, managing realms and clients, troubleshooting authentication issues, implementing RBAC, or when users mention "KeyCloak", "SSO", "OIDC", "SAML", "identity provider", "IAM", "authentication flow", "user federation", "realm configuration", or "access management".
---

# KeyCloak Administration

## Overview

Provides systematic KeyCloak administration guidance covering installation, configuration, realm management, security hardening, and operational best practices. Supports both standalone and clustered deployments for secure, scalable identity and access management (IAM) solutions.

## Quick Start Guide

Choose your task and load the appropriate reference:

1. **New Installation** → Continue to Installation & Setup
2. **Realm & User Management** → Load [realm-management.md](references/realm-management.md)
3. **Client Configuration** → Load [client-configuration.md](references/client-configuration.md)
4. **Authentication & SSO** → Load [authentication-sso.md](references/authentication-sso.md)
5. **Authorization & RBAC** → Load [authorization-rbac.md](references/authorization-rbac.md)
6. **User Federation (LDAP/AD)** → Load [user-federation.md](references/user-federation.md)
7. **Security Hardening** → Load [security-hardening.md](references/security-hardening.md)
8. **High Availability & Scaling** → Load [ha-scalability.md](references/ha-scalability.md)
9. **Troubleshooting** → Load [troubleshooting.md](references/troubleshooting.md)
10. **Integration Examples** → Load [integration-examples.md](references/integration-examples.md)

## Installation & Setup

## Deployment Options

**1. Standalone Mode (Development/Testing)**

```bash
# Download and start KeyCloak
wget https://github.com/keycloak/keycloak/releases/download/[VERSION]/keycloak-[VERSION].tar.gz
tar -xvzf keycloak-[VERSION].tar.gz
cd keycloak-[VERSION]
bin/kc.sh start-dev

# Access: http://localhost:8080
# Create initial admin user on first access
```

**2. Production Mode with Database**

```bash
# Configure and build
bin/kc.sh build --db=postgres

# Set environment variables
export KC_DB=postgres
export KC_DB_URL=jdbc:postgresql://localhost/keycloak
export KC_DB_USERNAME=keycloak
export KC_DB_PASSWORD=password
export KC_HOSTNAME=keycloak.example.com

# Start production mode
bin/kc.sh start --optimized
```

**3. Docker Deployment**

```bash
docker run -d \
  --name keycloak \
  -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:latest \
  start-dev
```

**4. Kubernetes** - Use KeyCloak Operator or Helm charts

### Initial Configuration Steps

1. **Admin Account**: Create on first access with strong password (12+ chars)
2. **Hostname**: Configure `KC_HOSTNAME` for production
3. **SSL/TLS**: Set up certificates (required for production)
4. **Database**: Configure PostgreSQL connection
5. **Email**: Configure SMTP for notifications

```properties
# Email settings
KC_SMTP_HOST=smtp.example.com
KC_SMTP_PORT=587
KC_SMTP_FROM=noreply@example.com
KC_SMTP_STARTTLS=true
```

## Core Concepts

### Realms

- **Master realm**: Administrative realm (don't use for apps)
- **Application realms**: Separate realms per app/environment
- Create: Admin Console → Create Realm

### Users & Groups

- **Users**: Individual accounts with credentials
- **Groups**: Organize users hierarchically
- **Attributes**: Custom key-value pairs
- **Federation**: Sync from LDAP/AD (see [user-federation.md](references/user-federation.md))

### Clients

- **OIDC clients**: Modern OAuth 2.0/OIDC applications
- **SAML clients**: Legacy enterprise applications
- **Types**: Confidential (server-side) or Public (SPA/mobile)
- Details: See [client-configuration.md](references/client-configuration.md)

### Roles & Permissions

- **Realm roles**: Global across all clients
- **Client roles**: Specific to one client
- **Composite roles**: Inherit multiple roles
- Details: See [authorization-rbac.md](references/authorization-rbac.md)

## Common Tasks

### Configure SSO for Applications

1. **Create OIDC client** for your application
2. **Set redirect URIs** (exact URLs, no wildcards)
3. **Configure client type**:
   - Confidential: Server-side apps (need client secret)
   - Public: SPAs/mobile apps (use PKCE)
4. **Obtain configuration** from realm endpoint:

   ```
   https://keycloak.example.com/realms/{realm}/.well-known/openid-configuration
   ```

5. **Integrate** with your app (see [integration-examples.md](references/integration-examples.md))

### Enable Multi-Factor Authentication

1. Authentication → Flows
2. Duplicate Browser flow
3. Add OTP or WebAuthn authenticator
4. Set as Required or Conditional
5. Bind to realm
6. Users configure MFA on next login

Details: See [authentication-sso.md](references/authentication-sso.md)

### Connect to LDAP/Active Directory

1. User Federation → Add LDAP Provider
2. Configure connection (URL, bind DN, credentials)
3. Set search base: `ou=users,dc=example,dc=com`
4. Configure mappers for attributes
5. Test connection and sync users

Details: See [user-federation.md](references/user-federation.md)

### Secure Production Deployment

Essential security measures:

- **SSL/TLS**: Required for all production traffic
- **Password policy**: 12+ chars, complexity requirements
- **Brute force protection**: Enable with lockout
- **Token lifespans**: Short access tokens (5-15 min)
- **Admin MFA**: Enable for all admin accounts
- **Event logging**: Monitor authentication events

Complete checklist: See [security-hardening.md](references/security-hardening.md)

### Set Up High Availability

1. **Shared database**: PostgreSQL/MySQL for all nodes
2. **Distributed caching**: Configure Infinispan
3. **Load balancer**: HAProxy/NGINX with sticky sessions
4. **Health checks**: Use `/health/ready` and `/health/live`
5. **Monitoring**: Prometheus metrics at `/metrics`

Details: See [ha-scalability.md](references/ha-scalability.md)

## Troubleshooting Quick Reference

### Users Can't Login

- Check user enabled status
- Verify redirect URIs match exactly
- Review required actions
- Check Events → Login Events

### Token Validation Fails

- Verify realm public key
- Check token expiration
- Validate issuer URL
- Confirm audience claim

### LDAP Sync Issues

- Test LDAP connection
- Verify bind credentials
- Check user DN path
- Run manual sync

Full troubleshooting guide: See [troubleshooting.md](references/troubleshooting.md)

## Essential Commands

```bash
# Start modes
bin/kc.sh start-dev                    # Development
bin/kc.sh start --optimized            # Production

# Build for database
bin/kc.sh build --db=postgres

# Export/Import realm
bin/kc.sh export --dir /backup --realm my-realm
bin/kc.sh import --dir /backup

# Admin CLI
bin/kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin
bin/kcadm.sh create realms -s realm=my-realm -s enabled=true
bin/kcadm.sh create users -r my-realm -s username=john -s enabled=true
bin/kcadm.sh set-password -r my-realm --username john --new-password secret
```

## Best Practices Summary

### Architecture

- Separate realms per application/environment
- Use groups for structure, roles for permissions
- Plan token lifespans based on security needs
- Enable session replication in clusters

### Security

- Always use SSL/TLS in production
- Enable MFA for privileged accounts
- Implement brute force protection
- Regular security audits
- Principle of least privilege

### Operations

- Automate backups and test restores
- Monitor metrics and set alerts
- Document configurations
- Regular updates and patching
- Capacity planning

### Development

- Use PKCE for public clients
- Implement proper token refresh
- Handle token expiration gracefully
- Validate tokens correctly
- Use appropriate grant types

## Reference Documentation

For detailed guidance, load the appropriate reference file:

- **[realm-management.md](references/realm-management.md)** - Realm configuration, users, groups
- **[client-configuration.md](references/client-configuration.md)** - OIDC/SAML clients, scopes, mappers
- **[authentication-sso.md](references/authentication-sso.md)** - Auth flows, MFA, social login, IdP
- **[authorization-rbac.md](references/authorization-rbac.md)** - Roles, permissions, fine-grained auth
- **[user-federation.md](references/user-federation.md)** - LDAP/AD integration, custom providers
- **[security-hardening.md](references/security-hardening.md)** - Security policies, monitoring, auditing
- **[ha-scalability.md](references/ha-scalability.md)** - Clustering, performance, backup, DR
- **[troubleshooting.md](references/troubleshooting.md)** - Common issues, logging, diagnostics
- **[integration-examples.md](references/integration-examples.md)** - Spring Boot, Node.js, React, Python, Docker, K8s

## Additional Resources

- Official documentation: <https://www.keycloak.org/documentation>
- Admin CLI reference for automation
- Client adapter docs for frameworks
- Community forums for support

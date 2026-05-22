---
name: apache-nifi-registry
description: Expert guidance for Apache NiFi Registry including flow versioning, buckets, Git integration, security, and registry client configuration. Use this when working with flow version control and registry management.
tags: [nifi-registry, version-control, flow-management]
color: blue
---

# Apache NiFi Registry Expert Skill

You are an expert in Apache NiFi Registry, a central location for storing and managing shared resources like versioned flows.

## Core Concepts

### Architecture
- **Buckets**: Containers for organizing versioned items
- **Versioned Flows**: Snapshots of NiFi process groups
- **Flow Versions**: Individual versions within a flow
- **Registry Clients**: Connections from NiFi to Registry

## Key Features

### Version Control
- Store and manage NiFi flow versions
- Track changes with metadata and comments
- Compare versions side-by-side
- Import/export flows between environments

### Storage Backends
- **File System**: Default local storage
- **Git**: Store flows in Git repositories
- **Database**: Store in relational database (PostgreSQL, MySQL)

## Configuration

### registry.properties
```properties
# Web UI
nifi.registry.web.http.host=0.0.0.0
nifi.registry.web.http.port=18080

# Flow Persistence
nifi.registry.flow.storage.directory=./flow_storage

# Git Flow Persistence Provider
nifi.registry.provider.flow.git.implementation=org.apache.nifi.registry.provider.flow.git.GitFlowPersistenceProvider
nifi.registry.provider.flow.git.Flow Storage Directory=./flow_storage
```

### Git Integration
```xml
<!-- providers.xml -->
<flowPersistenceProvider>
  <class>org.apache.nifi.registry.provider.flow.git.GitFlowPersistenceProvider</class>
  <property name="Flow Storage Directory">./flow_storage</property>
  <property name="Remote To Push">origin</property>
  <property name="Remote Access User">git-user</property>
  <property name="Remote Access Password">password</property>
</flowPersistenceProvider>
```

## Docker Deployment

### Standalone Registry
```yaml
services:
  nifi-registry:
    image: apache/nifi-registry:latest
    ports:
      - "18080:18080"
    environment:
      - LOG_LEVEL=INFO
    volumes:
      - ./nifi-registry/database:/opt/nifi-registry/nifi-registry-current/database
      - ./nifi-registry/flow_storage:/opt/nifi-registry/nifi-registry-current/flow_storage
      - ./nifi-registry/conf:/opt/nifi-registry/nifi-registry-current/conf
```

### With Git Backend
```yaml
services:
  nifi-registry:
    image: apache/nifi-registry:latest
    ports:
      - "18080:18080"
    volumes:
      - ./nifi-registry/flow_storage:/opt/nifi-registry/nifi-registry-current/flow_storage
      - ./nifi-registry/conf/providers.xml:/opt/nifi-registry/nifi-registry-current/conf/providers.xml
    environment:
      - NIFI_REGISTRY_FLOW_PROVIDER=git
      - NIFI_REGISTRY_GIT_REMOTE=https://github.com/org/nifi-flows.git
      - NIFI_REGISTRY_GIT_USER=git-user
      - NIFI_REGISTRY_GIT_PASSWORD=token
```

## Usage Workflow

### Connect NiFi to Registry
1. **Add Registry Client** (NiFi Controller Settings)
   ```
   Name: Dev Registry
   URL: http://nifi-registry:18080
   ```

2. **Create Bucket** (in Registry UI)
   ```
   Bucket Name: Production Flows
   Description: Versioned production data flows
   ```

3. **Version Control a Flow** (in NiFi)
   - Right-click Process Group
   - Version → Start version control
   - Select Registry, Bucket, Flow name
   - Add version comment
   - Click Save

### Version Management
```bash
# Commit Changes (NiFi UI)
Right-click Process Group → Version → Commit local changes

# View Change Log
Right-click Process Group → Version → Show local changes

# Revert Changes
Right-click Process Group → Version → Revert local changes

# Change Version
Right-click Process Group → Version → Change version
```

## Best Practices

### Bucket Organization
```
Buckets by Environment:
├── Development
├── Testing
├── Staging
└── Production

OR by Domain:
├── Data Ingestion
├── ETL Pipelines
├── Analytics
└── Data Distribution
```

### Versioning Strategy
- **Commit frequently** with meaningful messages
- **Tag stable releases** (v1.0.0, v1.1.0)
- **Use branching** for experimental changes (if using Git backend)
- **Document breaking changes** in commit messages
- **Test in lower environments** before promoting

### Naming Conventions
```
Flow Names:
- product-ingestion-flow
- customer-etl-pipeline
- sensor-data-aggregation

Version Comments:
- "feat: Add Kafka consumer for orders"
- "fix: Correct JSON parsing logic"
- "refactor: Optimize database queries"
```

## Security

### Authentication
```properties
# Identity Providers
nifi.registry.security.identity.provider=ldap-identity-provider

# LDAP Configuration
nifi.registry.security.ldap.manager.dn=cn=admin,dc=example,dc=com
nifi.registry.security.ldap.manager.password=password
nifi.registry.security.ldap.url=ldap://ldap-server:389
nifi.registry.security.ldap.user.search.base=ou=users,dc=example,dc=com
```

### Authorization
```xml
<!-- authorizers.xml -->
<authorizers>
  <userGroupProvider>
    <identifier>file-user-group-provider</identifier>
    <class>org.apache.nifi.registry.security.authorization.file.FileUserGroupProvider</class>
    <property name="Users File">./conf/users.xml</property>
    <property name="Initial User Identity 1">CN=admin, OU=NiFi</property>
  </userGroupProvider>

  <accessPolicyProvider>
    <identifier>file-access-policy-provider</identifier>
    <class>org.apache.nifi.registry.security.authorization.file.FileAccessPolicyProvider</class>
    <property name="User Group Provider">file-user-group-provider</property>
    <property name="Authorizations File">./conf/authorizations.xml</property>
    <property name="Initial Admin Identity">CN=admin, OU=NiFi</property>
  </accessPolicyProvider>
</authorizers>
```

## API Usage

### REST API Examples
```bash
# List buckets
curl http://localhost:18080/nifi-registry-api/buckets

# Create bucket
curl -X POST http://localhost:18080/nifi-registry-api/buckets \
  -H "Content-Type: application/json" \
  -d '{"name":"MyBucket","description":"Test bucket"}'

# List flows in bucket
curl http://localhost:18080/nifi-registry-api/buckets/{bucketId}/flows

# Get flow versions
curl http://localhost:18080/nifi-registry-api/buckets/{bucketId}/flows/{flowId}/versions

# Export flow version
curl http://localhost:18080/nifi-registry-api/buckets/{bucketId}/flows/{flowId}/versions/{version}/export \
  -o flow-export.json
```

## Gitea Integration

When using Gitea as a Git backend for NiFi Registry:

### Setup Steps
1. **Create Gitea Repository**
   ```bash
   # In Gitea UI
   Repository: nifi-flows
   Visibility: Private
   Initialize: Yes (with README)
   ```

2. **Generate Access Token**
   ```bash
   # Gitea Settings → Applications → Generate Token
   Permissions: repo (all)
   ```

3. **Configure Registry providers.xml**
   ```xml
   <flowPersistenceProvider>
     <class>org.apache.nifi.registry.provider.flow.git.GitFlowPersistenceProvider</class>
     <property name="Flow Storage Directory">./flow_storage</property>
     <property name="Remote To Push">origin</property>
     <property name="Remote Access User">gitea-user</property>
     <property name="Remote Access Password">gitea-access-token</property>
   </flowPersistenceProvider>
   ```

4. **Initialize Git Repository**
   ```bash
   cd flow_storage
   git init
   git remote add origin http://gitea:3000/user/nifi-flows.git
   git config user.name "NiFi Registry"
   git config user.email "registry@nifi.local"
   ```

## Monitoring & Troubleshooting

### Logs
```bash
# Main logs
logs/nifi-registry-app.log    # Application log
logs/nifi-registry-user.log   # User actions
logs/nifi-registry-bootstrap.log  # Bootstrap

# Enable DEBUG
conf/logback.xml → Set level to DEBUG
```

### Common Issues
| Issue | Solution |
|-------|----------|
| Cannot connect from NiFi | Check network, firewall, registry URL |
| Git push fails | Verify credentials, remote URL, network |
| Flow not visible | Check bucket permissions, user authorization |
| Version conflict | Pull latest, resolve conflicts, recommit |

## Migration & Backup

### Export All Flows
```bash
# Using NiFi Registry CLI (part of NiFi Toolkit)
registry list-buckets
registry export-all-flows -b bucket-id -o /backup/flows/
```

### Import Flows
```bash
registry import-flow-version -f /backup/flows/flow.json -b target-bucket-id
```

### Backup Strategy
```bash
# 1. File System Backend
tar -czf registry-backup-$(date +%Y%m%d).tar.gz flow_storage/ database/

# 2. Git Backend
cd flow_storage && git push --all origin

# 3. Database (if using DB backend)
pg_dump nifi_registry > registry-backup-$(date +%Y%m%d).sql
```

## Resources
- [NiFi Registry Documentation](https://nifi.apache.org/registry.html)
- [REST API Guide](https://nifi.apache.org/docs/nifi-registry-docs/rest-api/index.html)
- [Git Provider Setup](https://nifi.apache.org/docs/nifi-registry-docs/html/administration-guide.html#git-persistence-provider)

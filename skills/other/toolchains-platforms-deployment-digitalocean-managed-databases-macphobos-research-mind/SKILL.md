---
name: digitalocean-managed-databases
description: DigitalOcean Managed Databases for PostgreSQL, MySQL, Redis, MongoDB, Kafka, OpenSearch, and Valkey. Use when provisioning, scaling, or operating managed database clusters on DigitalOcean.
progressive_disclosure:
  entry_point:
    summary: "DigitalOcean Managed Databases for PostgreSQL, MySQL, Redis, MongoDB, Kafka, OpenSearch, and Valkey. Use when provisioning, scaling, or operating managed database clusters on DigitalOcean."
    when_to_use: "When working with version control, branches, or pull requests."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# DigitalOcean Managed Databases Skill

---
progressive_disclosure:
  entry_point:
    summary: "Managed databases on DigitalOcean: PostgreSQL, MySQL, Redis, MongoDB, Kafka, OpenSearch, Valkey with managed backups and scaling."
    when_to_use:
      - "When provisioning managed database clusters"
      - "When scaling or migrating database workloads"
      - "When securing database access with VPC and credentials"
    quick_start:
      - "Choose a database engine and region"
      - "Create a cluster and users"
      - "Apply networking and access controls"
      - "Monitor usage and scale as needed"
  token_estimate:
    entry: 90-110
    full: 4200-5400
---

## Overview

DigitalOcean Managed Databases provide fully managed clusters so teams can avoid manual setup and maintenance.

**Supported engines**:
- PostgreSQL
- MySQL
- Redis
- MongoDB
- Kafka
- OpenSearch
- Valkey

## Provisioning Workflow

- Select engine, region, and cluster size.
- Create users and databases with required roles.
- Configure trusted sources and VPC networking.
- Retrieve connection strings and TLS settings.

## Operations and Scaling

- Scale nodes or storage as demand grows.
- Set maintenance windows to control upgrades.
- Review backups and restore points.

## Security Practices

- Use VPC for private connectivity.
- Rotate credentials and limit user privileges.
- Enforce TLS connections.

## Migration Planning

- Use engine-specific migration guides.
- Validate application connectivity before cutover.
- Plan rollback using snapshots or backups.

## Complementary Skills

When using this skill, consider these related skills (if deployed):

- **digitalocean-networking**: VPC, firewalls, and private access.
- **digitalocean-management**: Monitoring and alerting.
- **digitalocean-storage**: Backup and snapshot workflows.

*Note: Complementary skills are optional. This skill is fully functional without them.*

## Resources

**DigitalOcean Docs**:
- Managed Databases: https://docs.digitalocean.com/products/databases/
- PostgreSQL: https://docs.digitalocean.com/products/databases/postgresql/
- MySQL: https://docs.digitalocean.com/products/databases/mysql/
- Redis: https://docs.digitalocean.com/products/databases/redis/
- MongoDB: https://docs.digitalocean.com/products/databases/mongodb/
- Kafka: https://docs.digitalocean.com/products/databases/kafka/
- OpenSearch: https://docs.digitalocean.com/products/databases/opensearch/
- Valkey: https://docs.digitalocean.com/products/databases/valkey/

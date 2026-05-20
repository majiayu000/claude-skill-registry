---
name: digitalocean-management
description: DigitalOcean management services for monitoring, uptime checks, and resource organization with Projects. Use when setting up observability, alerts, and operational visibility on DigitalOcean.
progressive_disclosure:
  entry_point:
    summary: "DigitalOcean management services for monitoring, uptime checks, and resource organization with Projects. Use when setting up observability, alerts, and operational visibility on DigitalOcean."
    when_to_use: "When working with version control, branches, or pull requests."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# DigitalOcean Management Skill

---
progressive_disclosure:
  entry_point:
    summary: "DigitalOcean management: Monitoring, Uptime checks, Projects for resource organization and operational visibility."
    when_to_use:
      - "When setting up monitoring and alerting"
      - "When organizing resources into projects"
      - "When tracking uptime for services"
    quick_start:
      - "Create Projects for each environment"
      - "Enable Monitoring and alerts"
      - "Configure Uptime checks"
      - "Review dashboards regularly"
  token_estimate:
    entry: 90-110
    full: 3200-4300
---

## Overview

DigitalOcean management services provide monitoring, uptime checks, and resource organization to keep workloads healthy and visible.

## Monitoring

- Enable monitoring for Droplets and clusters.
- Track CPU, memory, and disk metrics.
- Configure alerts for critical thresholds.

## Uptime

- Create checks for URLs, hostnames, and IPs.
- Set alert notifications for downtime and latency.
- Monitor SSL expiration where applicable.

## Projects

- Group resources by application or environment.
- Use Projects to scope ownership and visibility.

## Operational Workflow

- Standardize Projects and naming.
- Enable Monitoring and baseline alerts.
- Add Uptime checks for public endpoints.
- Review metrics and alerts after deployments.

## Complementary Skills

When using this skill, consider these related skills (if deployed):

- **digitalocean-networking**: Load balancers and DNS routing visibility.
- **digitalocean-storage**: Backup and snapshot strategy.
- **digitalocean-managed-databases**: Database metrics and alerts.

*Note: Complementary skills are optional. This skill is fully functional without them.*

## Resources

**DigitalOcean Docs**:
- Management: https://docs.digitalocean.com/products/management/
- Monitoring: https://docs.digitalocean.com/products/monitoring/
- Uptime: https://docs.digitalocean.com/products/uptime/
- Projects: https://docs.digitalocean.com/products/projects/

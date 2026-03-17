---
name: deployment-orchestrator
description: Automated deployment orchestration supporting multiple environments, infrastructure as code, CI/CD pipeline management, rollback procedures, and monitoring integration. Use when Claude needs to manage deployments, configure infrastructure, orchestrate release processes, or ensure deployment reliability across different environments.
---

# Deployment Orchestrator

## Overview
This skill orchestrates automated deployments across multiple environments with support for infrastructure as code, rollback procedures, and comprehensive monitoring integration.

## When to Use This Skill
- Managing deployments across development, staging, and production
- Configuring infrastructure as code (IaC)
- Orchestrating CI/CD pipelines
- Implementing blue-green or canary deployment strategies
- Managing rollback procedures
- Integrating deployment monitoring and alerting

## Supported Platforms
- Kubernetes and container orchestration
- AWS (EC2, ECS, EKS, Lambda, CloudFormation)
- Azure (VMs, AKS, ARM templates)
- Google Cloud Platform (GKE, Compute Engine)
- Docker and containerization
- Serverless platforms (Vercel, Netlify, AWS Amplify)

## Deployment Strategies

### Blue-Green Deployment
- Maintain two identical production environments
- Switch traffic between environments
- Enable rapid rollbacks
- Minimize downtime

### Canary Deployment
- Gradually shift traffic to new version
- Monitor metrics during rollout
- Automatically rollback on failures
- Control rollout percentage

### Rolling Deployment
- Update instances incrementally
- Maintain service availability
- Control deployment pace
- Monitor health during rollout

### Recreate Deployment
- Terminate old instances before creating new
- Ensure clean state transitions
- Suitable for stateless applications
- Complete environment refresh

## Infrastructure as Code
- Terraform configurations
- CloudFormation templates
- ARM templates for Azure
- Kubernetes manifests
- Docker Compose files
- Serverless framework configurations

## CI/CD Pipeline Components

### Build Phase
- Source code compilation
- Dependency management
- Artifact creation
- Security scanning

### Test Phase
- Unit and integration tests
- Security scans
- Performance testing
- Compliance checks

### Deploy Phase
- Environment provisioning
- Application deployment
- Configuration management
- Health checks

### Post-Deploy Phase
- Smoke testing
- Monitoring setup
- Alert configuration
- Rollback preparation

## Monitoring and Observability
- Application performance monitoring (APM)
- Infrastructure monitoring
- Log aggregation and analysis
- Health check endpoints
- Business metric tracking
- Error rate monitoring

## Rollback Procedures
- Automated rollback triggers
- Manual rollback capabilities
- Database migration reversals
- Configuration restoration
- Traffic switching procedures

## Environment Management
- Development: Rapid iteration, feature testing
- Staging: Pre-production validation
- Production: Live user traffic
- Disaster recovery: Backup and failover

## Security Considerations
- Secret management
- Access control and permissions
- Network security
- Image scanning and signing
- Compliance validation

## Best Practices
- Immutable infrastructure
- Infrastructure testing
- Drift detection
- Cost optimization
- Multi-region deployments
- Automated scaling policies

## Quality Gates
- Health check success rates
- Performance benchmark compliance
- Security scan results
- Configuration validation
- Resource utilization limits

## Scripts Available
- `scripts/deploy-application.sh` - Execute application deployment
- `scripts/provision-infrastructure.js` - Provision infrastructure as code
- `scripts/rollback-deployment.sh` - Initiate deployment rollback
- `scripts/health-check.js` - Perform post-deployment health checks

## References
- `references/deployment-strategies.md` - Comprehensive guide to different deployment strategies
- `references/infrastructure-as-code.md` - Infrastructure as code best practices and guidelines
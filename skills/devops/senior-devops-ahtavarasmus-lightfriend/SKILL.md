---
name: senior-devops
description: Comprehensive DevOps skill for CI/CD, infrastructure automation, containerization, and cloud platforms (AWS, GCP, Azure). Includes pipeline setup, infrastructure as code, deployment automation, and monitoring. Use when setting up pipelines, deploying applications, managing infrastructure, implementing monitoring, or optimizing deployment processes.
---

# Senior Devops

Complete toolkit for senior devops with modern tools and best practices.

## Quick Start

### Main Capabilities

This skill provides three core capabilities through automated scripts:

```bash
# Script 1: Pipeline Generator
python scripts/pipeline_generator.py [options]

# Script 2: Terraform Scaffolder
python scripts/terraform_scaffolder.py [options]

# Script 3: Deployment Manager
python scripts/deployment_manager.py [options]
```

## Core Capabilities

### 1. Pipeline Generator

Automated tool for pipeline generator tasks.

**Features:**
- Automated scaffolding
- Best practices built-in
- Configurable templates
- Quality checks

**Usage:**
```bash
python scripts/pipeline_generator.py <project-path> [options]
```

### 2. Terraform Scaffolder

Comprehensive analysis and optimization tool.

**Features:**
- Deep analysis
- Performance metrics
- Recommendations
- Automated fixes

**Usage:**
```bash
python scripts/terraform_scaffolder.py <target-path> [--verbose]
```

### 3. Deployment Manager

Advanced tooling for specialized tasks.

**Features:**
- Expert-level automation
- Custom configurations
- Integration ready
- Production-grade output

**Usage:**
```bash
python scripts/deployment_manager.py [arguments] [options]
```

## Reference Documentation

### Cicd Pipeline Guide

Comprehensive guide available in `references/cicd_pipeline_guide.md`:

- Detailed patterns and practices
- Code examples
- Best practices
- Anti-patterns to avoid
- Real-world scenarios

### Infrastructure As Code

Complete workflow documentation in `references/infrastructure_as_code.md`:

- Step-by-step processes
- Optimization strategies
- Tool integrations
- Performance tuning
- Troubleshooting guide

### Deployment Strategies

Technical reference guide in `references/deployment_strategies.md`:

- Technology stack details
- Configuration examples
- Integration patterns
- Security considerations
- Scalability guidelines

## Tech Stack

**Languages:** Rust
**Frontend:** Yew (WebAssembly)
**Backend:** Axum, REST APIs
**Database:** SQLite, PostgreSQL
**DevOps:** Docker, Terraform, GitHub Actions
**Cloud:** AWS

## Development Workflow

Refer to the detailed reference documentation:
- `references/cicd_pipeline_guide.md` - CI/CD pipeline patterns
- `references/infrastructure_as_code.md` - Terraform and IaC workflows
- `references/deployment_strategies.md` - Deployment best practices

## Best Practices Summary

### Code Quality
- Follow established patterns
- Write comprehensive tests
- Document decisions
- Review regularly

### Performance
- Measure before optimizing
- Use appropriate caching
- Optimize critical paths
- Monitor in production

### Security
- Validate all inputs
- Use parameterized queries
- Implement proper authentication
- Keep dependencies updated

### Maintainability
- Write clear code
- Use consistent naming
- Add helpful comments
- Keep it simple

## Common Commands

```bash
# Development (Lightfriend)
cargo build
cargo test
just up              # Docker Compose
just logs-core       # View logs

# Infrastructure Analysis (if using helper scripts)
python scripts/terraform_scaffolder.py .
python scripts/deployment_manager.py --analyze

# Deployment
docker build -t app:latest .
docker-compose up -d
```

## Troubleshooting

### Common Issues

Check the comprehensive troubleshooting section in `references/deployment_strategies.md`.

### Getting Help

- Review reference documentation
- Check script output messages
- Consult tech stack documentation
- Review error logs

## Resources

- Pattern Reference: `references/cicd_pipeline_guide.md`
- Workflow Guide: `references/infrastructure_as_code.md`
- Technical Guide: `references/deployment_strategies.md`
- Tool Scripts: `scripts/` directory

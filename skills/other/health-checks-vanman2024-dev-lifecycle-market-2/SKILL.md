---
name: health-checks
description: Post-deployment validation and health check scripts for validating HTTP endpoints, APIs, MCP servers, SSL/TLS certificates, and performance metrics. Use when deploying applications, validating deployments, testing endpoints, checking SSL certificates, running performance tests, or when user mentions health checks, deployment validation, endpoint testing, performance testing, or uptime monitoring.
allowed-tools: Bash, Read, Write, Edit
---

# Health Checks

Post-deployment validation and health check scripts for comprehensive deployment verification.

## Overview

This skill provides functional health check scripts, templates, and examples for validating deployments across multiple protocols and services. All scripts include proper error handling, retry logic, timeout configuration, and detailed reporting.

## Scripts

All scripts are located in `scripts/` and are fully functional (not placeholders).

### Core Health Check Scripts

1. **http-health-check.sh** - HTTP/HTTPS endpoint validation with status codes, response times, and content verification
2. **api-health-check.sh** - RESTful API endpoint testing with JSON response validation and authentication
3. **mcp-server-health-check.sh** - MCP server validation including tool discovery and execution tests
4. **ssl-tls-validator.sh** - SSL/TLS certificate validation with expiration checking and cipher suite verification
5. **performance-tester.sh** - Load testing and performance metrics collection with concurrent request handling

### Usage Examples

```bash
# Basic HTTP health check
bash scripts/http-health-check.sh https://example.com

# API health check with authentication
bash scripts/api-health-check.sh https://api.example.com/v1 "Bearer token123"

# MCP server validation
bash scripts/mcp-server-health-check.sh http://localhost:3000/mcp

# SSL certificate check
bash scripts/ssl-tls-validator.sh example.com 443

# Performance testing with 100 concurrent requests
bash scripts/performance-tester.sh https://example.com 100 10
```

## Templates

All templates are located in `templates/` and provide configuration examples.

### Configuration Templates

1. **health-check-config.json** - Health check configuration template with endpoints, thresholds, and retry policies
2. **health-check-config.yaml** - YAML version of health check configuration
3. **monitoring-dashboard.json** - Grafana/Prometheus dashboard configuration for health metrics
4. **alerts-config.json** - Alert rules configuration for health check failures
5. **ci-cd-health-check.yaml** - CI/CD pipeline integration template (GitHub Actions/GitLab CI)
6. **docker-healthcheck.json** - Docker HEALTHCHECK instruction templates

### Template Usage

```bash
# Copy and customize configuration
cp templates/health-check-config.json my-config.json

# Use in CI/CD pipeline
cp templates/ci-cd-health-check.yaml .github/workflows/health-check.yml
```

## Examples

All examples are located in `examples/` and demonstrate real-world usage patterns.

### Example Files

1. **basic-usage.md** - Simple health check workflows for common scenarios
2. **advanced-validation.md** - Complex validation scenarios with multiple endpoints and dependencies
3. **ci-cd-integration.md** - Integrating health checks into deployment pipelines
4. **monitoring-setup.md** - Setting up continuous monitoring with health checks
5. **troubleshooting.md** - Common issues and debugging strategies

## Instructions

### Running Health Checks

1. **Single Endpoint Check**
   ```bash
   # Check HTTP endpoint
   bash scripts/http-health-check.sh https://myapp.com

   # Check API endpoint with authentication
   bash scripts/api-health-check.sh https://api.myapp.com/health "Bearer $TOKEN"
   ```

2. **Comprehensive Deployment Validation**
   ```bash
   # Validate all services after deployment
   bash scripts/http-health-check.sh https://frontend.myapp.com
   bash scripts/api-health-check.sh https://api.myapp.com/health
   bash scripts/mcp-server-health-check.sh https://mcp.myapp.com
   bash scripts/ssl-tls-validator.sh myapp.com 443
   bash scripts/performance-tester.sh https://myapp.com 50 5
   ```

3. **Configuration-Based Checks**
   ```bash
   # Create configuration file from template
   cp templates/health-check-config.json deployment-checks.json

   # Edit configuration with your endpoints
   # Then run validation script that reads config
   ```

### Integration Patterns

**CI/CD Pipeline Integration**
- Copy `templates/ci-cd-health-check.yaml` to your pipeline configuration
- Customize endpoint URLs and thresholds
- Run health checks as post-deployment step

**Docker Container Health Checks**
- Use `templates/docker-healthcheck.json` for Dockerfile HEALTHCHECK
- Configure interval, timeout, and retries
- Monitor container health status

**Monitoring and Alerting**
- Use `templates/monitoring-dashboard.json` for Grafana dashboards
- Configure `templates/alerts-config.json` for automated alerts
- Set up continuous health monitoring

## Requirements

- `curl` - For HTTP/HTTPS requests
- `jq` - For JSON parsing and validation
- `openssl` - For SSL/TLS certificate validation
- `bc` - For performance calculations (optional)
- `timeout` command - For request timeouts (GNU coreutils)

**Optional Requirements:**
- `ab` (Apache Bench) - Enhanced performance testing
- `hey` - Modern HTTP load generator
- `prometheus` - For metrics collection
- `grafana` - For dashboard visualization

## Exit Codes

All scripts follow standard exit code conventions:

- `0` - All health checks passed
- `1` - Health check failed (endpoint down, invalid response, etc.)
- `2` - Invalid arguments or missing dependencies
- `3` - Timeout or network error
- `4` - SSL/TLS validation failed
- `5` - Performance threshold exceeded

## Best Practices

1. **Always validate after deployment** - Run health checks immediately after deploying
2. **Set appropriate timeouts** - Configure timeouts based on expected response times
3. **Use retries with backoff** - Implement exponential backoff for transient failures
4. **Monitor continuously** - Don't just check once, monitor continuously
5. **Alert on failures** - Set up alerts for health check failures
6. **Test in staging first** - Validate health checks in staging environment
7. **Document thresholds** - Clearly document acceptable response times and error rates

---

**Location**: /home/gotime2022/.claude/plugins/marketplaces/ai-dev-marketplace/plugins/deployment/skills/health-checks/

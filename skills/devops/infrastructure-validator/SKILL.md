# Infrastructure Validator Skill

## Metadata
- skill_name: infrastructure-validator
- activation_code: INFRASTRUCTURE_VALIDATOR_V1
- version: 1.0.0
- category: deployment
- phase: 11

## Description
Validates and starts infrastructure components including Docker containers, databases, and services.

## Activation Criteria
- Triggered in Phase 11 (Deployment)
- After tests pass
- Before marking deployment complete

## Workflow

### 1. Infrastructure Detection
```bash
# Check for Docker Compose
if [ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ]; then
    echo "Docker Compose configuration found"
fi

# Check for Kubernetes
if [ -f "k8s/deployment.yaml" ] || [ -d "helm" ]; then
    echo "Kubernetes configuration found"
fi

# Check for standalone services
if [ -f "Dockerfile" ]; then
    echo "Dockerfile found"
fi
```

### 2. Container Build & Start
```bash
# Build containers
docker-compose build

# Start infrastructure
docker-compose up -d

# Wait for health checks
./scripts/wait-for-healthy.sh
```

### 3. Service Validation
```python
class InfrastructureValidator:
    def validate_services(self):
        """Check all services are running"""
        checks = {
            "containers": self.check_containers(),
            "databases": self.check_databases(),
            "apis": self.check_apis(),
            "network": self.check_connectivity()
        }
        return all(checks.values())
    
    def check_containers(self):
        """Verify Docker containers are healthy"""
        result = subprocess.run(
            ["docker-compose", "ps"],
            capture_output=True
        )
        return "healthy" in result.stdout.decode()
    
    def check_databases(self):
        """Test database connections"""
        # Generic DB connection test
        return self.test_connections()
    
    def check_apis(self):
        """Test API endpoints"""
        endpoints = self.discover_endpoints()
        for endpoint in endpoints:
            if not self.test_endpoint(endpoint):
                return False
        return True
```

## Validation Checks

### Container Health
- All containers running
- No restart loops
- Logs show successful startup
- Health checks passing

### Network Connectivity
- Services can communicate
- Ports are accessible
- DNS resolution works
- Load balancers configured

### Database Readiness
- Connections established
- Migrations completed
- Initial data loaded
- Replicas synchronized

### API Availability
- Endpoints responding
- Authentication working
- Rate limits configured
- SSL/TLS enabled

## Commands

### Docker Compose Operations
```bash
# Build and start
docker-compose up -d --build

# Check status
docker-compose ps
docker-compose logs --tail=50

# Health check
docker-compose exec <service> health-check

# Cleanup (if needed)
docker-compose down -v
```

### Validation Script
```bash
#!/bin/bash
# Wait for all services to be healthy

echo "Waiting for services to start..."

# Maximum wait time (5 minutes)
TIMEOUT=300
ELAPSED=0

while [ $ELAPSED -lt $TIMEOUT ]; do
    # Check if all containers are healthy
    UNHEALTHY=$(docker-compose ps | grep -c "unhealthy\|starting")
    
    if [ "$UNHEALTHY" -eq 0 ]; then
        echo "✅ All services healthy!"
        exit 0
    fi
    
    echo "Waiting... ($ELAPSED/$TIMEOUT seconds)"
    sleep 10
    ELAPSED=$((ELAPSED + 10))
done

echo "❌ Timeout waiting for services"
exit 1
```

## Output
```json
{
    "infrastructure": {
        "status": "running",
        "containers": {
            "total": 5,
            "healthy": 5,
            "unhealthy": 0
        },
        "services": {
            "api": "http://localhost:8000",
            "database": "postgresql://localhost:5432",
            "cache": "redis://localhost:6379"
        },
        "validation_time": "2024-01-01T00:00:00Z"
    }
}
```

## Integration Points
- Reads: docker-compose.yml, Dockerfile, k8s/
- Executes: docker-compose, kubectl, health checks
- Writes: .infrastructure-status.json
- Signals: INFRASTRUCTURE_READY, DEPLOYMENT_COMPLETE

## Error Handling
- Container build failures
- Port conflicts
- Resource limitations
- Network issues
- Database connection failures

## Rollback Strategy
```bash
# If validation fails, rollback
docker-compose down
git checkout HEAD~1
docker-compose up -d --build
```

## Demo Preparation
When infrastructure is ready:
1. Display service URLs
2. Show login credentials (if any)
3. Provide demo script
4. List available features
5. Show monitoring dashboards
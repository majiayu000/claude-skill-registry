---
name: docker-compose-production
description: Use when deploying Docker Compose applications to production including security hardening, resource management, health checks, logging, monitoring, and high-availability patterns.
allowed-tools: [Bash, Read]
---

# Docker Compose Production Deployment

Production-ready Docker Compose configurations with security, reliability, and scalability best practices.

## Production-Ready Base Template

A comprehensive production template with essential configurations:

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:1.25-alpine
    container_name: production-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - nginx-cache:/var/cache/nginx
      - nginx-logs:/var/log/nginx
    networks:
      - frontend
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M

  api:
    image: mycompany/api:${API_VERSION:-latest}
    container_name: production-api
    restart: unless-stopped
    networks:
      - frontend
      - backend
    environment:
      NODE_ENV: production
      DATABASE_URL: postgresql://postgres:5432/production_db
      REDIS_URL: redis://cache:6379
      LOG_LEVEL: ${LOG_LEVEL:-info}
      PORT: 3000
    env_file:
      - .env.production
    secrets:
      - db_password
      - jwt_secret
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    depends_on:
      database:
        condition: service_healthy
      cache:
        condition: service_healthy
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "5"
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G

  worker:
    image: mycompany/worker:${WORKER_VERSION:-latest}
    container_name: production-worker
    restart: unless-stopped
    networks:
      - backend
    environment:
      NODE_ENV: production
      DATABASE_URL: postgresql://postgres:5432/production_db
      REDIS_URL: redis://cache:6379
      QUEUE_NAME: ${QUEUE_NAME:-default}
    env_file:
      - .env.production
    secrets:
      - db_password
    depends_on:
      database:
        condition: service_healthy
      cache:
        condition: service_healthy
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "5"
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M

  database:
    image: postgres:15-alpine
    container_name: production-db
    restart: unless-stopped
    networks:
      - backend
    environment:
      POSTGRES_DB: production_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_INITDB_ARGS: "-E UTF8 --locale=en_US.UTF-8"
    secrets:
      - db_password
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./db/init:/docker-entrypoint-initdb.d:ro
      - postgres-logs:/var/log/postgresql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d production_db"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    command:
      - "postgres"
      - "-c"
      - "max_connections=200"
      - "-c"
      - "shared_buffers=256MB"
      - "-c"
      - "effective_cache_size=1GB"
      - "-c"
      - "maintenance_work_mem=64MB"
      - "-c"
      - "checkpoint_completion_target=0.9"
      - "-c"
      - "wal_buffers=16MB"
      - "-c"
      - "default_statistics_target=100"
      - "-c"
      - "random_page_cost=1.1"
      - "-c"
      - "effective_io_concurrency=200"
      - "-c"
      - "work_mem=1MB"
      - "-c"
      - "min_wal_size=1GB"
      - "-c"
      - "max_wal_size=4GB"
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "5"
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G

  cache:
    image: redis:7-alpine
    container_name: production-cache
    restart: unless-stopped
    networks:
      - backend
    command: >
      redis-server
      --appendonly yes
      --appendfsync everysec
      --maxmemory 512mb
      --maxmemory-policy allkeys-lru
      --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 768M
        reservations:
          cpus: '0.5'
          memory: 512M

  backup:
    image: prodrigestivill/postgres-backup-local:15-alpine
    container_name: production-backup
    restart: unless-stopped
    networks:
      - backend
    environment:
      POSTGRES_HOST: database
      POSTGRES_DB: production_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      SCHEDULE: "@daily"
      BACKUP_KEEP_DAYS: 7
      BACKUP_KEEP_WEEKS: 4
      BACKUP_KEEP_MONTHS: 6
      HEALTHCHECK_PORT: 8080
    secrets:
      - db_password
    volumes:
      - ./backups:/backups
    depends_on:
      database:
        condition: service_healthy

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true

volumes:
  postgres-data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/postgres
  redis-data:
    driver: local
  nginx-cache:
    driver: local
  nginx-logs:
    driver: local
  postgres-logs:
    driver: local

secrets:
  db_password:
    file: ./secrets/db_password.txt
  jwt_secret:
    file: ./secrets/jwt_secret.txt
```

## Security Hardening

Production security configurations:

```yaml
version: '3.8'

services:
  web:
    image: nginx:1.25-alpine
    restart: unless-stopped
    read_only: true
    tmpfs:
      - /var/cache/nginx
      - /var/run
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    security_opt:
      - no-new-privileges:true
      - seccomp:./security/seccomp-profile.json
    user: "nginx:nginx"
    networks:
      - frontend
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro

  api:
    image: mycompany/api:${VERSION}
    restart: unless-stopped
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
      - seccomp:./security/seccomp-profile.json
    user: "1000:1000"
    networks:
      - frontend
      - backend
    environment:
      NODE_ENV: production
    env_file:
      - .env.production
    secrets:
      - source: db_password
        target: /run/secrets/db_password
        mode: 0400
      - source: api_key
        target: /run/secrets/api_key
        mode: 0400

  database:
    image: postgres:15-alpine
    restart: unless-stopped
    read_only: true
    tmpfs:
      - /tmp
      - /run/postgresql
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - DAC_OVERRIDE
      - FOWNER
      - SETGID
      - SETUID
    security_opt:
      - no-new-privileges:true
    user: "postgres:postgres"
    networks:
      - backend
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - source: db_password
        mode: 0400
    volumes:
      - postgres-data:/var/lib/postgresql/data

networks:
  frontend:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.enable_icc: "false"
  backend:
    driver: bridge
    internal: true

volumes:
  postgres-data:

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    file: ./secrets/api_key.txt
```

## Resource Limits and Reservations

Comprehensive resource management:

```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 256M
          pids: 100
        reservations:
          cpus: '0.25'
          memory: 128M
    ulimits:
      nofile:
        soft: 1024
        hard: 2048
      nproc:
        soft: 64
        hard: 128

  api:
    image: node:18-alpine
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
          pids: 200
        reservations:
          cpus: '1.0'
          memory: 1G
    ulimits:
      nofile:
        soft: 4096
        hard: 8192
      nproc:
        soft: 256
        hard: 512

  database:
    image: postgres:15-alpine
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '4.0'
          memory: 4G
          pids: 500
        reservations:
          cpus: '2.0'
          memory: 2G
    ulimits:
      nofile:
        soft: 8192
        hard: 16384
    shm_size: '256mb'
    volumes:
      - postgres-data:/var/lib/postgresql/data

  cache:
    image: redis:7-alpine
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
    sysctls:
      net.core.somaxconn: 1024
    volumes:
      - redis-data:/data

volumes:
  postgres-data:
  redis-data:
```

## High Availability Configuration

Multiple replicas with load balancing:

```yaml
version: '3.8'

services:
  loadbalancer:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx-lb.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    networks:
      - frontend
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/health"]
      interval: 10s
      timeout: 5s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M

  api:
    image: mycompany/api:${VERSION}
    restart: unless-stopped
    networks:
      - frontend
      - backend
    environment:
      NODE_ENV: production
      DATABASE_URL: postgresql://postgres:5432/app
      INSTANCE_ID: "{{.Task.Slot}}"
    deploy:
      replicas: 5
      update_config:
        parallelism: 2
        delay: 10s
        order: start-first
        failure_action: rollback
      rollback_config:
        parallelism: 2
        delay: 10s
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  database:
    image: postgres:15-alpine
    restart: unless-stopped
    networks:
      - backend
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          cpus: '4.0'
          memory: 4G

  database-replica:
    image: postgres:15-alpine
    restart: unless-stopped
    networks:
      - backend
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_PRIMARY_HOST: database
      POSTGRES_PRIMARY_PORT: 5432
    secrets:
      - db_password
    volumes:
      - postgres-replica-data:/var/lib/postgresql/data
      - ./db/replica-setup.sh:/docker-entrypoint-initdb.d/replica-setup.sh:ro
    depends_on:
      database:
        condition: service_healthy
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true

volumes:
  postgres-data:
  postgres-replica-data:

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

## Monitoring and Observability

Production monitoring stack:

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: unless-stopped
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'
      - '--web.enable-lifecycle'
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - ./monitoring/alerts:/etc/prometheus/alerts:ro
      - prometheus-data:/prometheus
    networks:
      - monitoring
    ports:
      - "9090:9090"
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:9090/-/healthy"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 2G

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: unless-stopped
    environment:
      GF_SECURITY_ADMIN_PASSWORD__FILE: /run/secrets/grafana_password
      GF_INSTALL_PLUGINS: grafana-clock-panel,grafana-simple-json-datasource
      GF_SERVER_ROOT_URL: https://monitoring.example.com
    secrets:
      - grafana_password
    volumes:
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning:ro
      - ./monitoring/grafana/dashboards:/var/lib/grafana/dashboards:ro
      - grafana-data:/var/lib/grafana
    networks:
      - monitoring
      - frontend
    ports:
      - "3001:3000"
    depends_on:
      - prometheus
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    restart: unless-stopped
    command:
      - '--path.rootfs=/host'
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    volumes:
      - /:/host:ro,rslave
    networks:
      - monitoring
    ports:
      - "9100:9100"
    deploy:
      resources:
        limits:
          cpus: '0.2'
          memory: 128M

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    restart: unless-stopped
    privileged: true
    devices:
      - /dev/kmsg
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker:/var/lib/docker:ro
      - /dev/disk:/dev/disk:ro
    networks:
      - monitoring
    ports:
      - "8080:8080"
    deploy:
      resources:
        limits:
          cpus: '0.3'
          memory: 256M

  loki:
    image: grafana/loki:latest
    container_name: loki
    restart: unless-stopped
    command: -config.file=/etc/loki/local-config.yaml
    volumes:
      - ./monitoring/loki-config.yml:/etc/loki/local-config.yaml:ro
      - loki-data:/loki
    networks:
      - monitoring
    ports:
      - "3100:3100"
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G

  promtail:
    image: grafana/promtail:latest
    container_name: promtail
    restart: unless-stopped
    command: -config.file=/etc/promtail/config.yml
    volumes:
      - ./monitoring/promtail-config.yml:/etc/promtail/config.yml:ro
      - /var/log:/var/log:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
    networks:
      - monitoring
    depends_on:
      - loki
    deploy:
      resources:
        limits:
          cpus: '0.2'
          memory: 256M

networks:
  monitoring:
    driver: bridge
  frontend:
    driver: bridge

volumes:
  prometheus-data:
  grafana-data:
  loki-data:

secrets:
  grafana_password:
    file: ./secrets/grafana_password.txt
```

## Logging Configuration

Centralized logging setup:

```yaml
version: '3.8'

services:
  app:
    image: myapp:latest
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "5"
        labels: "app,environment,version"
        tag: "{{.Name}}/{{.ID}}"
    labels:
      app: "myapp"
      environment: "production"
      version: "${VERSION}"

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    logging:
      driver: "syslog"
      options:
        syslog-address: "tcp://logserver:514"
        tag: "nginx"
        syslog-format: "rfc5424micro"

  api:
    image: api:latest
    restart: unless-stopped
    logging:
      driver: "fluentd"
      options:
        fluentd-address: "localhost:24224"
        tag: "docker.{{.Name}}"
        fluentd-async-connect: "true"
        fluentd-retry-wait: "1s"
        fluentd-max-retries: "30"

  database:
    image: postgres:15-alpine
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "10"
        compress: "true"
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

## Environment Configuration Management

Multi-environment setup:

```yaml
version: '3.8'

services:
  app:
    image: myapp:${VERSION:-latest}
    restart: unless-stopped
    environment:
      NODE_ENV: ${NODE_ENV:-production}
      LOG_LEVEL: ${LOG_LEVEL:-info}
      PORT: ${APP_PORT:-3000}
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@database:5432/${DB_NAME}
      REDIS_URL: redis://:${REDIS_PASSWORD}@cache:6379
      JWT_SECRET: ${JWT_SECRET}
      API_TIMEOUT: ${API_TIMEOUT:-30000}
      MAX_CONNECTIONS: ${MAX_CONNECTIONS:-100}
    env_file:
      - .env.${ENVIRONMENT:-production}
      - .env.secrets
    networks:
      - app-network

  database:
    image: postgres:${POSTGRES_VERSION:-15}-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_INITDB_ARGS: ${POSTGRES_INITDB_ARGS:--E UTF8}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network

  cache:
    image: redis:${REDIS_VERSION:-7}-alpine
    restart: unless-stopped
    command: redis-server --requirepass ${REDIS_PASSWORD} --maxmemory ${REDIS_MAX_MEMORY:-256mb}
    volumes:
      - redis-data:/data
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  postgres-data:
  redis-data:
```

## Health Checks and Readiness

Comprehensive health monitoring:

```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  api:
    image: node:18-alpine
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "node", "healthcheck.js"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    depends_on:
      database:
        condition: service_healthy
      cache:
        condition: service_healthy

  database:
    image: postgres:15-alpine
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d production_db || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    volumes:
      - postgres-data:/var/lib/postgresql/data

  cache:
    image: redis:7-alpine
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s
    volumes:
      - redis-data:/data

  queue:
    image: rabbitmq:3-management-alpine
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq

volumes:
  postgres-data:
  redis-data:
  rabbitmq-data:
```

## Backup and Recovery

Automated backup configuration:

```yaml
version: '3.8'

services:
  database:
    image: postgres:15-alpine
    restart: unless-stopped
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - backend

  db-backup:
    image: prodrigestivill/postgres-backup-local:15-alpine
    restart: unless-stopped
    environment:
      POSTGRES_HOST: database
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      SCHEDULE: "@daily"
      BACKUP_KEEP_DAYS: 7
      BACKUP_KEEP_WEEKS: 4
      BACKUP_KEEP_MONTHS: 6
      BACKUP_DIR: /backups
      HEALTHCHECK_PORT: 8080
    secrets:
      - db_password
    volumes:
      - ./backups:/backups
      - ./backup-scripts:/scripts:ro
    networks:
      - backend
    depends_on:
      database:
        condition: service_healthy

  volume-backup:
    image: futurice/docker-volume-backup:2.6.0
    restart: unless-stopped
    environment:
      BACKUP_CRON_EXPRESSION: "0 2 * * *"
      BACKUP_FILENAME: "backup-%Y-%m-%d_%H-%M-%S.tar.gz"
      BACKUP_RETENTION_DAYS: 30
      AWS_S3_BUCKET_NAME: ${S3_BACKUP_BUCKET}
      AWS_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID}
      AWS_SECRET_ACCESS_KEY_FILE: /run/secrets/aws_secret
    secrets:
      - aws_secret
    volumes:
      - postgres-data:/backup/postgres-data:ro
      - redis-data:/backup/redis-data:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./backup-archive:/archive

networks:
  backend:
    driver: bridge

volumes:
  postgres-data:
  redis-data:

secrets:
  db_password:
    file: ./secrets/db_password.txt
  aws_secret:
    file: ./secrets/aws_secret.txt
```

## When to Use This Skill

Use docker-compose-production when you need to:

- Deploy Docker Compose applications to production environments
- Implement security hardening and best practices
- Configure resource limits and reservations
- Set up health checks and readiness probes
- Implement high availability with multiple replicas
- Configure production-grade logging and monitoring
- Set up automated backups and disaster recovery
- Manage secrets and sensitive configuration
- Implement zero-downtime deployments
- Configure multi-environment deployment strategies
- Set up container orchestration for production workloads
- Optimize performance and resource utilization

## Best Practices

1. **Always Use Version Pinning**: Pin specific image versions instead of using `latest` to ensure reproducible deployments.

2. **Implement Health Checks**: Configure health checks for all services to enable automatic recovery and proper dependency management.

3. **Set Resource Limits**: Always define CPU and memory limits to prevent resource exhaustion and ensure predictable performance.

4. **Use Secrets Management**: Never store secrets in environment variables or compose files; use Docker secrets or external secret managers.

5. **Configure Restart Policies**: Use `restart: unless-stopped` for production services to ensure automatic recovery from failures.

6. **Implement Proper Logging**: Configure structured logging with rotation and retention policies to manage disk space.

7. **Use Read-Only Filesystems**: Set `read_only: true` where possible and use tmpfs for temporary data to improve security.

8. **Drop Unnecessary Capabilities**: Use `cap_drop: ALL` and only add required capabilities to follow the principle of least privilege.

9. **Enable Monitoring**: Deploy monitoring and observability tools to track application health and performance metrics.

10. **Implement Automated Backups**: Configure regular automated backups with retention policies and test recovery procedures.

11. **Use Internal Networks**: Mark backend networks as internal to prevent direct external access to databases and caches.

12. **Configure Update Strategies**: Define update and rollback configurations for zero-downtime deployments.

13. **Implement Resource Reservations**: Set resource reservations to guarantee minimum resources for critical services.

14. **Use Multi-Stage Dependencies**: Configure `depends_on` with health check conditions to ensure proper startup order.

15. **Document Configuration**: Maintain comprehensive documentation of your production configuration and deployment procedures.

## Common Pitfalls

1. **Using Latest Tags**: Using `latest` or unversioned images can cause unexpected behavior when images are updated; always pin versions.

2. **Ignoring Resource Limits**: Not setting resource limits can allow one service to consume all available resources and crash others.

3. **Missing Health Checks**: Without health checks, Docker cannot determine if services are actually ready or need to be restarted.

4. **Storing Secrets in Plain Text**: Committing secrets to version control or storing them in environment variables exposes sensitive data.

5. **Not Testing Backups**: Creating backups without regularly testing restoration procedures leads to data loss during actual incidents.

6. **Exposing Unnecessary Ports**: Publishing all service ports to the host increases attack surface; only expose what's needed.

7. **Running as Root**: Not specifying a non-root user leaves containers vulnerable to privilege escalation attacks.

8. **Ignoring Log Rotation**: Without log rotation, logs can fill up disk space and crash services or hosts.

9. **Missing Monitoring**: Deploying without monitoring makes it impossible to detect and diagnose issues before they impact users.

10. **Not Using Networks**: Running all services on the default network prevents proper segmentation and increases security risk.

11. **Forgetting Readiness Checks**: Starting dependent services before dependencies are ready causes connection failures and restarts.

12. **Hardcoding Configuration**: Embedding environment-specific values in the compose file makes it difficult to deploy to multiple environments.

13. **Neglecting Security Updates**: Not regularly updating base images leaves services vulnerable to known security issues.

14. **Insufficient Start Period**: Setting health check start periods too short causes false positives during slow application startup.

15. **Not Planning for Scale**: Designing services without considering horizontal scaling makes it difficult to handle increased load.

## Resources

### Official Documentation

- [Docker Compose Production](https://docs.docker.com/compose/production/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Docker Secrets](https://docs.docker.com/engine/swarm/secrets/)

### Deployment Guides

- [Deploy on Production](https://docs.docker.com/compose/production/)
- [Configure Container Resources](https://docs.docker.com/config/containers/resource_constraints/)
- [Container Security](https://docs.docker.com/engine/security/security/)

### Tools and Images

- [Docker Volume Backup](https://github.com/futurice/docker-volume-backup)
- [Postgres Backup Local](https://github.com/prodrigestivill/docker-postgres-backup-local)
- [Watchtower](https://containrrr.dev/watchtower/) - Automated container updates

### Monitoring

- [Prometheus](https://prometheus.io/docs/introduction/overview/)
- [Grafana](https://grafana.com/docs/)
- [cAdvisor](https://github.com/google/cadvisor)

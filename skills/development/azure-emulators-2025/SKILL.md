---
name: azure-emulators-2025
description: Azure service emulators for local development including Azurite, Cosmos DB, and Event Hub Docker containers
---

# Azure Service Emulators for Local Development (2025)

## Overview

This skill provides comprehensive knowledge of Azure service emulators available as Docker containers for local development in 2025.

## Available Azure Emulators

### 1. Azurite (Azure Storage Emulator)

**Official replacement for Azure Storage Emulator (deprecated)**

**Image:** `mcr.microsoft.com/azure-storage/azurite:latest`

**Supported Services:**
- Blob Storage
- Queue Storage
- Table Storage

**Configuration:**
```yaml
services:
  azurite:
    image: mcr.microsoft.com/azure-storage/azurite:latest
    container_name: azurite
    command: azurite --blobHost 0.0.0.0 --queueHost 0.0.0.0 --tableHost 0.0.0.0 --loose
    ports:
      - "10000:10000"  # Blob service
      - "10001:10001"  # Queue service
      - "10002:10002"  # Table service
    volumes:
      - azurite-data:/data
    restart: unless-stopped
```

**Standard Development Connection String:**
```
DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://azurite:10000/devstoreaccount1;QueueEndpoint=http://azurite:10001/devstoreaccount1;TableEndpoint=http://azurite:10002/devstoreaccount1;
```

**Features:**
- Cross-platform (Windows, Linux, macOS)
- Written in Node.js/JavaScript
- Supports latest Azure Storage APIs
- Persistence to disk
- Compatible with Azure Storage Explorer
- `--loose` flag for relaxed validation (useful for local development)


**2025 API Version Support:**
- Latest release (v3.35.0) targets 2025-11-05 API version
- Blob service: 2025-11-05
- Queue service: 2025-11-05
- Table service: 2025-11-05 (preview)
- RA-GRS support for geo-redundant replication testing

**CLI Usage:**
```bash
# Install via npm (alternative to Docker)
npm install -g azurite

# Run with custom location
azurite --location /path/to/data --debug /path/to/debug.log
```

**Application Integration:**
```javascript
// Node.js with @azure/storage-blob
const { BlobServiceClient } = require('@azure/storage-blob');

const connectionString = process.env.AZURITE_CONNECTION_STRING;
const blobServiceClient = BlobServiceClient.fromConnectionString(connectionString);
```

```csharp
// .NET with Azure.Storage.Blobs
using Azure.Storage.Blobs;

var connectionString = Environment.GetEnvironmentVariable("AZURITE_CONNECTION_STRING");
var blobServiceClient = new BlobServiceClient(connectionString);
```

### 2. Azure SQL Server 2025

**Latest SQL Server with AI features**

**Image:** `mcr.microsoft.com/mssql/server:2025-latest`

**2025 Features:**
- Built-in Vector Search for AI similarity queries
- Semantic Queries alongside traditional full-text search
- Optimized Locking (TID Locking, LAQ)
- Native JSON and RegEx support
- Fabric Mirroring integration
- REST API support

**Configuration:**
```yaml
services:
  sqlserver:
    image: mcr.microsoft.com/mssql/server:2025-latest
    container_name: sqlserver
    environment:
      - ACCEPT_EULA=Y
      - MSSQL_PID=Developer
      - MSSQL_SA_PASSWORD_FILE=/run/secrets/sa_password
    secrets:
      - sa_password
    ports:
      - "1433:1433"
    volumes:
      - sqlserver-data:/var/opt/mssql
      - ./init:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P $$MSSQL_SA_PASSWORD -Q 'SELECT 1' -C || exit 1"]
      interval: 10s
      timeout: 3s
      retries: 3
      start_period: 10s
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
    networks:
      - backend
    security_opt:
      - no-new-privileges:true
    restart: unless-stopped

secrets:
  sa_password:
    file: ./secrets/sa_password.txt

volumes:
  sqlserver-data:
    driver: local
```

**Connection String:**
```
Server=sqlserver;Database=MyApp;User Id=sa;Password=YourStrong!Passw0rd;TrustServerCertificate=True;
```

**Important Notes:**
- **Azure SQL Edge retired September 30, 2025** - Use SQL Server 2025 instead
- Use `mssql-tools18` for TLS 1.3 support (`-C` flag trusts certificate)
- Developer edition is free for non-production use
- Supports arm64 via Rosetta 2 on macOS

**Vector Search Example (2025 Feature):**
```sql
-- Create vector index for AI similarity search
CREATE TABLE Documents (
    Id INT PRIMARY KEY,
    Content NVARCHAR(MAX),
    ContentVector VECTOR(1536)
);

-- Perform similarity search
SELECT TOP 10 Id, Content
FROM Documents
ORDER BY VECTOR_DISTANCE(ContentVector, @queryVector);
```

**2025 vnext-preview Features:**
- Entirely Linux-based emulator (cross-platform: x64, ARM64, Apple Silicon)
- No virtual machines required on Apple Silicon or Microsoft ARM
- Changefeed support (April 2025+)
- Document TTL (Time-to-Live) support
- OpenTelemetry V2 support
- API for NoSQL in gateway mode
- Currently in preview (active development)

**Image:** `mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview`

### 3. Cosmos DB Emulator

**NoSQL database emulator**

**Image:** `mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview`

**Configuration:**
```yaml
services:
  cosmosdb:
    image: mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview
    container_name: cosmosdb
    environment:
      - AZURE_COSMOS_EMULATOR_PARTITION_COUNT=10
      - AZURE_COSMOS_EMULATOR_ENABLE_DATA_PERSISTENCE=true
      - AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=127.0.0.1
    ports:
      - "8081:8081"       # Data Explorer
      - "10251:10251"
      - "10252:10252"
      - "10253:10253"
      - "10254:10254"
    volumes:
      - cosmos-data:/data/db
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
    networks:
      - backend
    restart: unless-stopped
```

**Emulator Endpoint:**
```
https://localhost:8081
```

**Emulator Key (Standard):**
```
C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==
```

**Data Explorer:**
Access at `https://localhost:8081/_explorer/index.html`

**Application Integration:**
```javascript
// Node.js with @azure/cosmos
const { CosmosClient } = require('@azure/cosmos');

const endpoint = 'https://localhost:8081';
const key = process.env.COSMOS_EMULATOR_KEY;
const client = new CosmosClient({ endpoint, key });
```

```csharp
// .NET with Microsoft.Azure.Cosmos
using Microsoft.Azure.Cosmos;

var endpoint = "https://localhost:8081";
var key = Environment.GetEnvironmentVariable("COSMOS_EMULATOR_KEY");
var client = new CosmosClient(endpoint, key);
```

**Limitations:**
- Performance not representative of production
- Limited to single partition for local development
- Certificate trust required (self-signed)

**2025 Official Azure Service Bus Emulator:**
- Released as official Docker container
- Linux-based emulator with cross-platform support
- Requires SQL Server Linux as dependency
- Supports AMQP protocol (port 5672)
- Connection string format with UseDevelopmentEmulator=true
- Current limitations: No JMS protocol, no partitioned entities, no AMQP Web Sockets

**Official Emulator Image:** `mcr.microsoft.com/azure-messaging/servicebus-emulator:latest`

**Connection String:**
```
Endpoint=sb://host.docker.internal;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=SAS_KEY_VALUE;UseDevelopmentEmulator=true;
```

### 4. Azure Service Bus Emulator

**Message queue emulator**

**Note:** Official emulator has limited Docker support. Use RabbitMQ as alternative.

**Official Emulator (Preview):**
```yaml
services:
  servicebus-sql:
    image: mcr.microsoft.com/mssql/server:2025-latest
    environment:
      - ACCEPT_EULA=Y
      - MSSQL_SA_PASSWORD=ServiceBus123!
    volumes:
      - servicebus-sql-data:/var/opt/mssql

  servicebus:
    image: mcr.microsoft.com/azure-messaging/servicebus-emulator:latest
    depends_on:
      - servicebus-sql
    environment:
      - ACCEPT_EULA=Y
      - SQL_SERVER=servicebus-sql
      - SQL_SA_PASSWORD=ServiceBus123!
    ports:
      - "5672:5672"  # AMQP
    networks:
      - backend
```

**RabbitMQ Alternative (Recommended):**
```yaml
services:
  rabbitmq:
    image: rabbitmq:3.14-alpine
    container_name: rabbitmq
    ports:
      - "5672:5672"   # AMQP
      - "15672:15672" # Management UI
    environment:
      - RABBITMQ_DEFAULT_USER=admin
      - RABBITMQ_DEFAULT_PASS=admin123
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - backend
    restart: unless-stopped
```

### 5. PostgreSQL (Azure Database for PostgreSQL)

**Image:** `postgres:16.6-alpine`

**Configuration:**
```yaml
services:
  postgres:
    image: postgres:16.6-alpine
    container_name: postgres
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD_FILE=/run/secrets/postgres_password
      - POSTGRES_DB=myapp
    secrets:
      - postgres_password
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 3s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 2G
    networks:
      - backend
    security_opt:
      - no-new-privileges:true
    restart: unless-stopped
```

**Extensions:**
Match Azure PostgreSQL Flexible Server extensions:
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
```

### 6. MySQL (Azure Database for MySQL)

**Image:** `mysql:9.2`

**Configuration:**
```yaml
services:
  mysql:
    image: mysql:9.2
    container_name: mysql
    environment:
      - MYSQL_ROOT_PASSWORD_FILE=/run/secrets/mysql_root_password
      - MYSQL_DATABASE=myapp
      - MYSQL_USER=appuser
      - MYSQL_PASSWORD_FILE=/run/secrets/mysql_password
    secrets:
      - mysql_root_password
      - mysql_password
    ports:
      - "3306:3306"
    volumes:
      - mysql-data:/var/lib/mysql
      - ./init:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-p$$MYSQL_ROOT_PASSWORD"]
      interval: 10s
      timeout: 3s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 2G
    networks:
      - backend
    security_opt:
      - no-new-privileges:true
    restart: unless-stopped
```

### 7. Redis (Azure Cache for Redis)

**Image:** `redis:7.4-alpine`

**Configuration:**
```yaml
services:
  redis:
    image: redis:7.4-alpine
    container_name: redis
    command: >
      redis-server
      --appendonly yes
      --requirepass ${REDIS_PASSWORD}
      --maxmemory 512mb
      --maxmemory-policy allkeys-lru
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    networks:
      - backend
    security_opt:
      - no-new-privileges:true
    restart: unless-stopped
```

### 8. Application Insights Alternative (Jaeger + Grafana)

**OpenTelemetry-compatible observability stack**

```yaml
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    container_name: jaeger
    ports:
      - "16686:16686"  # UI
      - "14268:14268"  # HTTP collector
      - "4317:4317"    # OTLP gRPC
      - "4318:4318"    # OTLP HTTP
    environment:
      - COLLECTOR_OTLP_ENABLED=true
    networks:
      - monitoring
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
    networks:
      - monitoring
    restart: unless-stopped
```

## Complete Azure Stack Example

```yaml
services:
  # Application Services
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    networks: [frontend]
    depends_on:
      backend:
        condition: service_healthy

  backend:
    build: ./backend
    ports: ["8080:8080"]
    networks: [frontend, backend]
    depends_on:
      sqlserver:
        condition: service_healthy
      redis:
        condition: service_started
      azurite:
        condition: service_started

  # Databases
  sqlserver:
    image: mcr.microsoft.com/mssql/server:2025-latest
    environment:
      - ACCEPT_EULA=Y
      - MSSQL_PID=Developer
      - MSSQL_SA_PASSWORD=${MSSQL_SA_PASSWORD}
    ports: ["1433:1433"]
    volumes: [sqlserver-data:/var/opt/mssql]
    networks: [backend]
    healthcheck:
      test: ["CMD-SHELL", "/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P $$MSSQL_SA_PASSWORD -Q 'SELECT 1' -C"]
      interval: 10s

  postgres:
    image: postgres:16.6-alpine
    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    ports: ["5432:5432"]
    volumes: [postgres-data:/var/lib/postgresql/data]
    networks: [backend]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s

  # Cache
  redis:
    image: redis:7.4-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    ports: ["6379:6379"]
    volumes: [redis-data:/data]
    networks: [backend]

  # Storage
  azurite:
    image: mcr.microsoft.com/azure-storage/azurite:latest
    command: azurite --blobHost 0.0.0.0 --queueHost 0.0.0.0 --tableHost 0.0.0.0 --loose
    ports: ["10000:10000", "10001:10001", "10002:10002"]
    volumes: [azurite-data:/data]
    networks: [backend]

  # NoSQL
  cosmosdb:
    image: mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview
    ports: ["8081:8081"]
    volumes: [cosmos-data:/data/db]
    networks: [backend]

  # Monitoring
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports: ["16686:16686", "4317:4317"]
    networks: [monitoring]

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
  monitoring:
    driver: bridge

volumes:
  sqlserver-data:
  postgres-data:
  redis-data:
  azurite-data:
  cosmos-data:
```

## Best Practices

1. **Use health checks** - Ensure dependencies are ready before app starts
2. **Network isolation** - Keep databases on internal backend network
3. **Resource limits** - Prevent emulators from consuming all system resources
4. **Persistence** - Use named volumes for data that should survive restarts
5. **Secrets management** - Use Docker secrets or environment files
6. **Version pinning** - Use specific tags, not `latest`
7. **Security hardening** - Drop capabilities, run as non-root where possible
8. **Documentation** - Document differences between emulators and Azure services

## Known Limitations

- **Performance**: Emulators are slower than Azure services
- **Scale**: Single-instance only, no clustering
- **Features**: Some Azure-specific features unavailable locally
- **SSL/TLS**: Self-signed certificates require trust configuration
- **Azure AD**: Authentication not replicated locally
- **Networking**: VNets, Private Endpoints not available

## Migration Checklist

When moving from Azure to Docker emulators:

- [ ] Replace Azure Storage connection strings with Azurite
- [ ] Update SQL Server connection strings (remove Azure-specific options)
- [ ] Configure Cosmos DB with emulator endpoint and key
- [ ] Replace Service Bus with RabbitMQ or emulator
- [ ] Set up alternative for Application Insights
- [ ] Update authentication (remove Azure AD dependencies)
- [ ] Configure network isolation
- [ ] Test all integrations
- [ ] Document feature parity gaps
- [ ] Create init scripts for sample data

## References

- [Azurite Documentation](https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azurite)
- [SQL Server 2025 in Docker](https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker)
- [Cosmos DB Emulator](https://learn.microsoft.com/en-us/azure/cosmos-db/local-emulator)
- [Service Bus Emulator](https://learn.microsoft.com/en-us/azure/service-bus-messaging/test-locally-with-service-bus-emulator)

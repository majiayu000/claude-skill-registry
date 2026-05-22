---
name: configuration-generator
description: "Generate configuration files for applications, services, and infrastructure. Use when: (1) Setting up new projects (package.json, requirements.txt, tsconfig.json), (2) Creating Docker or Kubernetes configurations, (3) Configuring CI/CD pipelines (GitHub Actions, GitLab CI, CircleCI), (4) Setting up web servers (Nginx, Apache), (5) Defining infrastructure as code (Terraform, CloudFormation), (6) Generating linter/formatter configs (ESLint, Prettier, Black). Provides templates and custom-generated configs for diverse tech stacks."
---

# Configuration Generator

Generate configuration files for applications, services, and infrastructure across various formats and frameworks.

## Quick Start

### Use Built-in Templates

Access ready-to-use configuration templates from assets:

```bash
# Docker Compose
cat assets/docker-compose.yml

# Kubernetes
cat assets/kubernetes-deployment.yaml

# GitHub Actions
cat assets/github-actions-workflow.yml
```

### Generate Custom Configuration

Specify your requirements to get tailored configuration files.

## Common Configuration Types

### Application Configurations

#### Package Managers

**Node.js (package.json)**
```json
{
  "name": "my-app",
  "version": "1.0.0",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest",
    "build": "tsc"
  },
  "dependencies": {
    "express": "^4.18.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "jest": "^29.0.0"
  }
}
```

**Python (requirements.txt)**
```
django==4.2.0
djangorestframework==3.14.0
psycopg2-binary==2.9.5
pytest==7.3.0
black==23.3.0
```

See **[app_configs.md](references/app_configs.md)** for:
- Package managers (npm, pip, cargo)
- Build tools (TypeScript, Webpack, Vite)
- Linters/formatters (ESLint, Prettier, Black)
- Testing frameworks (Jest, pytest)
- Environment files (.env, .editorconfig, .gitignore)

#### Build Configurations

**TypeScript (tsconfig.json)**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Infrastructure Configurations

#### Docker

**Dockerfile (Multi-stage)**
```dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**Docker Compose** - See `assets/docker-compose.yml`:
- Multi-service setup (web, database, cache)
- Environment variable configuration
- Volume management
- Network configuration

#### Kubernetes

**Deployment Configuration** - See `assets/kubernetes-deployment.yaml`:
- Deployment with replicas
- ConfigMap and Secret management
- Service and Ingress configuration
- Health probes
- Resource limits

**Example Deployment**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    spec:
      containers:
      - name: web
        image: myapp:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

See **[infra_configs.md](references/infra_configs.md)** for:
- Docker and Kubernetes
- Terraform (AWS, GCP, Azure)
- CI/CD pipelines
- Web servers (Nginx, Apache)

#### CI/CD Pipelines

**GitHub Actions** - See `assets/github-actions-workflow.yml`:
- Test, build, and deploy workflow
- Service containers (PostgreSQL, Redis)
- Docker image building
- Deployment automation

**Example Workflow**:
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest
```

## Configuration Decision Tree

```
What type of configuration do you need?

├─ Application Config
│  ├─ Package manager? → package.json, requirements.txt, Cargo.toml
│  ├─ Build tool? → tsconfig.json, webpack.config.js, vite.config.ts
│  ├─ Linter/formatter? → .eslintrc, .prettierrc, pyproject.toml
│  └─ Environment? → .env, .editorconfig, .gitignore
│
├─ Container/Orchestration
│  ├─ Docker? → Dockerfile, docker-compose.yml
│  └─ Kubernetes? → deployment.yaml, service.yaml, ingress.yaml
│
├─ Infrastructure as Code
│  ├─ Terraform? → main.tf, variables.tf, outputs.tf
│  └─ CloudFormation? → template.yaml
│
├─ CI/CD
│  ├─ GitHub Actions? → .github/workflows/ci.yml
│  ├─ GitLab CI? → .gitlab-ci.yml
│  └─ CircleCI? → .circleci/config.yml
│
└─ Web Server
   ├─ Nginx? → nginx.conf
   └─ Apache? → httpd.conf, .htaccess
```

## Generation Approaches

### Approach 1: Template-Based

Use pre-built templates from `assets/`:

**When to use**:
- Standard setups
- Quick prototyping
- Learning/reference

**How**:
1. Identify needed template
2. Copy from assets
3. Customize variables
4. Deploy

**Example**:
```bash
# Copy Docker Compose template
cp assets/docker-compose.yml ./

# Edit environment variables
# Deploy
docker-compose up -d
```

### Approach 2: Requirements-Based Generation

Generate from scratch based on specific needs:

**When to use**:
- Custom requirements
- Complex setups
- Specific tech stack

**How**:
1. Specify requirements
2. Choose tech stack
3. Define constraints
4. Generate configuration

**Example Request**: "Generate a GitHub Actions workflow for a Python Django app with PostgreSQL, Redis, and deployment to AWS ECS"

**Generated Output**: Custom workflow with:
- Python 3.11 setup
- PostgreSQL and Redis services
- Django test suite
- Docker image build
- AWS ECS deployment

### Approach 3: Hybrid

Combine templates with customization:

**When to use**:
- Partially standard setup
- Template needs modification
- Best practices + customization

**How**:
1. Start with template
2. Identify customization points
3. Modify specific sections
4. Validate configuration

## Best Practices

### 1. Use Environment Variables

Separate configuration from code:

**Application**:
```python
# settings.py
import os

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

**.env file**:
```bash
DATABASE_URL=postgresql://localhost/mydb
SECRET_KEY=your-secret-key
DEBUG=true
```

### 2. Version Control Best Practices

**Do commit**:
- `.env.example` (template)
- Configuration templates
- Development configs

**Don't commit**:
- `.env` (secrets)
- `.env.local` (local overrides)
- Production credentials

**.gitignore**:
```
.env
.env.local
.env.*.local
```

### 3. Validate Configurations

Check syntax before deploying:

```bash
# Docker Compose
docker-compose config

# Kubernetes
kubectl apply --dry-run=client -f deployment.yaml

# Terraform
terraform validate

# YAML syntax
yamllint config.yml
```

### 4. Document Configuration

Add comments explaining purpose:

```yaml
# docker-compose.yml
services:
  web:
    # Application server - handles HTTP requests
    image: myapp:latest
    ports:
      # Expose on port 8000 for development
      - "8000:8000"
    environment:
      # Database connection string
      - DATABASE_URL=${DATABASE_URL}
```

### 5. Use Sensible Defaults

Provide defaults for optional values:

```yaml
# Kubernetes ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  # Default to info level logging
  LOG_LEVEL: "info"
  # Default connection pool size
  DB_POOL_SIZE: "10"
```

## Common Patterns

### Multi-Environment Configuration

**Development**:
```yaml
# docker-compose.dev.yml
services:
  web:
    build: .
    volumes:
      - ./app:/app  # Hot reload
    environment:
      - DEBUG=true
```

**Production**:
```yaml
# docker-compose.prod.yml
services:
  web:
    image: registry/myapp:latest
    environment:
      - DEBUG=false
    deploy:
      replicas: 3
```

### Secret Management

**Kubernetes Secrets**:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  database-url: "postgresql://..."
  api-key: "secret-key"
```

**Docker Compose (with env file)**:
```yaml
services:
  web:
    env_file:
      - .env.production
```

### Health Checks

**Docker Compose**:
```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

**Kubernetes**:
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
```

## Complete Example

**Request**: "Create complete configuration for a Python FastAPI application with PostgreSQL and Redis, using Docker Compose for development and Kubernetes for production"

**Generated Configurations**:

1. **Dockerfile**
2. **docker-compose.yml** (development)
3. **requirements.txt**
4. **kubernetes/deployment.yaml** (production)
5. **.env.example**
6. **.github/workflows/deploy.yml**

These files work together to provide:
- Local development environment
- CI/CD pipeline
- Production deployment
- Secret management
- Health monitoring

## Troubleshooting

### Configuration Validation Errors

**YAML syntax errors**:
```bash
# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('config.yml'))"

# Or use yamllint
yamllint config.yml
```

**Docker Compose issues**:
```bash
# Validate and view resolved config
docker-compose config

# Check for errors
docker-compose config --quiet
```

### Environment Variable Issues

**Missing variables**:
```bash
# List all required variables
grep -o '\${[^}]*}' docker-compose.yml

# Check if variable is set
echo $DATABASE_URL
```

### Port Conflicts

**Find process using port**:
```bash
# Linux/macOS
lsof -i :8000

# Windows
netstat -ano | findstr :8000
```

## Reference Materials

### Application Configs
See **[app_configs.md](references/app_configs.md)** for complete templates:
- Package managers (package.json, requirements.txt, Pipfile, Cargo.toml)
- Build tools (tsconfig.json, webpack.config.js, vite.config.ts)
- Linters and formatters (.eslintrc, .prettierrc, .flake8, pyproject.toml)
- Testing frameworks (jest.config.js, pytest.ini)
- Environment files (.env.example, .editorconfig, .gitignore)

### Infrastructure Configs
See **[infra_configs.md](references/infra_configs.md)** for:
- Docker (Dockerfile multi-stage, docker-compose.yml, .dockerignore)
- Kubernetes (Deployment, Service, Ingress, ConfigMap, Secret, HPA)
- Terraform (AWS, GCP, Azure infrastructure)
- CI/CD (GitHub Actions, GitLab CI, CircleCI)
- Web servers (Nginx, Apache configuration)

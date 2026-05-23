---
name: scribe-role-skill
version: 1.0.0
category: documentation
complexity: moderate
status: active
created: 2025-12-12
author: claude-command-and-control

description: |
  Professional technical writing and documentation skill for creating and
  maintaining comprehensive, accurate, and user-friendly documentation for
  codebases, APIs, deployment processes, and end-user guides.

triggers:
  - "create documentation"
  - "write docs"
  - "document api"
  - "update readme"
  - "document deployment"

dependencies: []

tags:
  - documentation
  - technical-writing
  - api-docs
  - user-guides
  - onboarding
---

# Scribe Role Skill

## Description

Create and maintain comprehensive, accurate, and user-friendly documentation for codebases, APIs, deployment processes, and end-user guides. This skill implements professional technical writing practices including documentation planning, structured content creation, and maintenance workflows.

## When to Use This Skill

- Creating project documentation (README, guides, etc.)
- Documenting APIs and endpoints
- Writing deployment and build instructions
- Creating user manuals and usage guides
- Documenting system architecture (with architect)
- Developing onboarding materials for new developers
- Maintaining and updating existing documentation

## When NOT to Use This Skill

- For system architecture design (use architect-role-skill)
- For code implementation (use builder-role-skill)
- For infrastructure deployment (use devops-role-skill)
- For testing procedures (use validator-role-skill)

## Prerequisites

- Access to project source code for analysis
- Understanding of target audience (developers vs end-users)
- Existing documentation to review (if updating)
- Access to architectural and planning documents

---

## Workflow

### Phase 1: Comprehensive Project Documentation

Create complete documentation suite for a project.

**Step 1.1: Codebase Analysis**

```bash
# Understand project structure
tree -L 3 -I 'node_modules|.git|dist|build'

# Identify main entry points
find . -name "index.*" -o -name "main.*" -o -name "app.*" | grep -v node_modules

# Review package manifest
cat package.json || cat requirements.txt || cat pom.xml || cat Cargo.toml

# Check existing documentation
find . -name "*.md" -o -name "*.rst" | grep -v node_modules
```

**Step 1.2: Documentation Planning**

Create `DOCUMENTATION_PLAN.md`:

```markdown
# Documentation Plan: [Project Name]

## Current State Assessment
- Existing docs: [List what exists]
- Documentation gaps: [What's missing]
- Outdated sections: [What needs updating]

## Documentation Structure
```
docs/
├── README.md                    # Project overview
├── GETTING_STARTED.md          # Quick start guide
├── BUILDING.md                 # Build instructions
├── DEPLOYMENT.md               # Deployment guide
├── USAGE.md                    # User manual
├── API.md                      # API reference
├── ARCHITECTURE.md             # System architecture
├── CONTRIBUTING.md             # Contribution guidelines
├── TROUBLESHOOTING.md          # Common issues
└── CHANGELOG.md                # Version history
```

## Priority

1. **Critical (Must Have)**:
   - README.md
   - BUILDING.md
   - DEPLOYMENT.md

2. **Important (Should Have)**:
   - API.md
   - USAGE.md
   - TROUBLESHOOTING.md

3. **Nice to Have**:
   - ARCHITECTURE.md (if not done by architect)
   - CONTRIBUTING.md
   - Advanced guides

## Timeline
- Phase 1 (Critical): Immediate
- Phase 2 (Important): Next sprint
- Phase 3 (Nice to Have): Following sprint
```

**Step 1.3: Create Core Documentation**

#### README.md Template

```markdown
# [Project Name]

[One-sentence description of what this project does]

## Overview

[2-3 paragraph description covering:
- What problem does this solve?
- Who is it for?
- What are the key features?]

## Quick Start

```bash
# Clone the repository
git clone [repository-url]
cd [project-name]

# Install dependencies
npm install  # or pip install -r requirements.txt, etc.

# Run the application
npm start  # or python main.py, etc.
```

## Features

- **Feature 1**: Description
- **Feature 2**: Description
- **Feature 3**: Description

## Documentation

- [Getting Started Guide](docs/GETTING_STARTED.md)
- [Building Instructions](docs/BUILDING.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [API Documentation](docs/API.md)
- [User Manual](docs/USAGE.md)

## Requirements

- [Runtime/Language]: version X.X+
- [Database]: version Y.Y+ (if applicable)
- [Other dependencies]

## Installation

See [GETTING_STARTED.md](docs/GETTING_STARTED.md) for detailed installation instructions.

## Usage

See [USAGE.md](docs/USAGE.md) for comprehensive usage documentation.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

[License type and link]

## Support

- Issues: [GitHub issues link]
- Documentation: [Documentation link]
- Community: [Discord/Slack/Forum link]

## Credits

[Acknowledgments, authors, contributors]
```

#### BUILDING.md Template

```markdown
# Building [Project Name]

This guide covers how to build the application from source.

## Prerequisites

### Required Tools
- [Tool 1]: version X.X+ ([installation link])
- [Tool 2]: version Y.Y+ ([installation link])
- [Tool 3]: version Z.Z+ ([installation link])

### Optional Tools
- [Tool]: For [purpose]

## Environment Setup

### macOS
```bash
# Install dependencies
brew install [package1] [package2]

# Set environment variables
export VAR_NAME=value
```

### Linux (Ubuntu/Debian)
```bash
# Install dependencies
sudo apt-get update
sudo apt-get install [package1] [package2]

# Set environment variables
export VAR_NAME=value
```

### Windows
```powershell
# Install dependencies using chocolatey
choco install [package1] [package2]

# Set environment variables
$env:VAR_NAME="value"
```

## Building the Application

### Development Build
```bash
# Install dependencies
npm install  # or equivalent

# Build for development
npm run build:dev

# Output location: ./dist/
```

### Production Build
```bash
# Clean previous builds
npm run clean

# Install production dependencies
npm ci --production

# Build optimized version
npm run build:prod

# Output location: ./dist/production/
```

### Build Configuration

Configuration files:
- `build.config.js`: Main build configuration
- `.env.build`: Build-time environment variables
- `webpack.config.js`: Bundler configuration (if applicable)

Key configuration options:
```javascript
{
  mode: 'production',        // production | development
  optimization: true,        // Enable optimizations
  minify: true,             // Minify output
  sourceMaps: false         // Generate source maps
}
```

## Build Artifacts

After successful build, the following artifacts are generated:

```
dist/
├── app.[hash].js          # Main application bundle
├── vendor.[hash].js       # Third-party dependencies
├── styles.[hash].css      # Compiled styles
├── assets/               # Static assets
│   ├── images/
│   └── fonts/
└── index.html           # Entry point
```

## Build Troubleshooting

### Common Issues

**Issue**: Build fails with "out of memory" error
```bash
# Solution: Increase Node memory limit
export NODE_OPTIONS="--max-old-space-size=4096"
npm run build
```

**Issue**: Dependency resolution fails
```bash
# Solution: Clear cache and reinstall
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

**Issue**: Module not found errors
```bash
# Solution: Verify all dependencies installed
npm list --depth=0
npm install [missing-package]
```

## Continuous Integration Builds

This project uses [CI system] for automated builds.

Build triggers:
- Push to `main` branch: Production build
- Push to `develop` branch: Development build
- Pull requests: Test build

Build status: [![Build Status](badge-url)](ci-url)

## Build Performance

Typical build times:
- Development: ~30 seconds
- Production: ~2 minutes

To improve build performance:
- Use incremental builds: `npm run build:watch`
- Enable caching: Configure in `build.config.js`
- Parallelize builds: Use `--parallel` flag

## Next Steps

After building, see:
- [DEPLOYMENT.md](DEPLOYMENT.md) for deployment instructions
- [TESTING.md](TESTING.md) for running tests
```

#### DEPLOYMENT.md Template

```markdown
# Deploying [Project Name]

This guide covers deploying the application to various environments.

## Environments

| Environment | Purpose | URL | Access |
|------------|---------|-----|--------|
| Development | Local development | localhost:3000 | All developers |
| QA | Testing | qa.example.com | QA team |
| Staging | Pre-production validation | staging.example.com | Internal users |
| Production | Live application | www.example.com | Public |

## Prerequisites

### Required
- Built application artifacts (see [BUILDING.md](BUILDING.md))
- Access credentials for target environment
- [Cloud provider] CLI tools installed and configured

### Environment Variables

Create `.env.[environment]` file:
```bash
# Application
NODE_ENV=production
PORT=3000
LOG_LEVEL=info

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname
DATABASE_POOL_SIZE=10

# API Keys (use secrets manager in production)
API_KEY=your-api-key
SECRET_KEY=your-secret-key

# Feature Flags
FEATURE_X_ENABLED=true
```

## Deployment Methods

### Method 1: Manual Deployment

**Step 1: Prepare Application**
```bash
# Build production artifacts
npm run build:prod

# Verify build
ls -la dist/
```

**Step 2: Deploy to Server**
```bash
# Copy files to server
scp -r dist/* user@server:/var/www/app/

# SSH into server
ssh user@server

# Restart application
sudo systemctl restart app-service
```

**Step 3: Verify Deployment**
```bash
# Check service status
sudo systemctl status app-service

# Check logs
sudo tail -f /var/log/app/application.log

# Test endpoint
curl https://your-domain.com/health
```

### Method 2: Docker Deployment

**Step 1: Build Docker Image**
```bash
# Build image
docker build -t app-name:version .

# Tag for registry
docker tag app-name:version registry.example.com/app-name:version

# Push to registry
docker push registry.example.com/app-name:version
```

**Step 2: Deploy Container**
```bash
# Pull latest image
docker pull registry.example.com/app-name:version

# Stop existing container
docker stop app-container || true
docker rm app-container || true

# Run new container
docker run -d \
  --name app-container \
  --env-file .env.production \
  -p 80:3000 \
  --restart unless-stopped \
  registry.example.com/app-name:version

# Verify
docker logs app-container
```

### Method 3: Kubernetes Deployment

**Step 1: Prepare Kubernetes Manifests**
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: registry.example.com/app-name:version
        ports:
        - containerPort: 3000
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secrets
```

**Step 2: Deploy to Cluster**
```bash
# Apply configurations
kubectl apply -f k8s/

# Check deployment status
kubectl rollout status deployment/app-deployment

# Verify pods running
kubectl get pods -l app=myapp

# Check logs
kubectl logs -l app=myapp --tail=100
```

### Method 4: Cloud Platform (AWS/GCP/Azure)

#### AWS Elastic Beanstalk
```bash
# Initialize EB
eb init -p node.js-16 app-name --region us-west-2

# Create environment
eb create production --instance-type t3.medium

# Deploy
eb deploy

# Check status
eb status
```

#### Google Cloud Platform
```bash
# Deploy to App Engine
gcloud app deploy app.yaml --project=project-id

# View logs
gcloud app logs tail -s default

# Open in browser
gcloud app browse
```

#### Azure App Service
```bash
# Create resource group
az group create --name myResourceGroup --location eastus

# Create app service plan
az appservice plan create --name myAppServicePlan \
  --resource-group myResourceGroup --sku B1 --is-linux

# Create web app
az webapp create --resource-group myResourceGroup \
  --plan myAppServicePlan --name myUniqueAppName \
  --runtime "NODE|16-lts"

# Deploy
az webapp deployment source config-zip \
  --resource-group myResourceGroup \
  --name myUniqueAppName \
  --src dist.zip
```

## Post-Deployment Verification

### Health Checks
```bash
# Application health
curl https://your-domain.com/health

# Expected response:
{
  "status": "healthy",
  "version": "1.2.3",
  "uptime": 12345
}

# Database connectivity
curl https://your-domain.com/health/db

# Dependencies status
curl https://your-domain.com/health/dependencies
```

### Smoke Tests
```bash
# Test critical endpoints
curl -X POST https://your-domain.com/api/test \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# Test authentication
curl https://your-domain.com/api/protected \
  -H "Authorization: Bearer $TOKEN"
```

### Monitoring Setup
- Set up application monitoring (see DevOps docs)
- Configure alerts for errors and performance
- Verify logs are being collected
- Check metrics dashboard

## Rollback Procedures

### Docker Rollback
```bash
# Identify previous version
docker images registry.example.com/app-name

# Deploy previous version
docker stop app-container
docker rm app-container
docker run -d --name app-container \
  registry.example.com/app-name:previous-version
```

### Kubernetes Rollback
```bash
# View rollout history
kubectl rollout history deployment/app-deployment

# Rollback to previous version
kubectl rollout undo deployment/app-deployment

# Rollback to specific revision
kubectl rollout undo deployment/app-deployment --to-revision=2
```

## Troubleshooting

### Deployment Fails

**Check**: Build artifacts
```bash
ls -la dist/
# Verify all necessary files present
```

**Check**: Environment variables
```bash
printenv | grep APP_
# Verify all required variables set
```

**Check**: Server logs
```bash
tail -f /var/log/app/error.log
```

### Application Not Responding

**Check**: Service status
```bash
sudo systemctl status app-service
```

**Check**: Port bindings
```bash
sudo netstat -tulpn | grep :3000
```

**Check**: Firewall rules
```bash
sudo iptables -L -n | grep 3000
```

## Security Considerations

- Never commit secrets to version control
- Use environment variables or secrets manager
- Enable HTTPS/TLS for all environments
- Implement proper authentication and authorization
- Keep dependencies updated
- Regular security audits

## Next Steps

After deployment:
- Review [MONITORING.md](MONITORING.md) for observability setup
- Configure [BACKUP.md](BACKUP.md) procedures
- Set up [ALERTS.md](ALERTS.md) for critical issues
```

---

### Phase 2: API Documentation

Create comprehensive API reference documentation.

**Step 2.1: Create API.md**

```markdown
# API Documentation

## Base URL
```
Production: https://api.example.com/v1
Staging: https://staging-api.example.com/v1
Development: http://localhost:3000/v1
```

## Authentication

All API requests require authentication using Bearer tokens:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.example.com/v1/endpoint
```

### Obtaining a Token
```bash
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password"
}

Response:
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600
}
```

## Endpoints

### Users

#### Get User
```
GET /users/:id
```

**Parameters**:
- `id` (path, required): User ID

**Response**:
```json
{
  "id": "123",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2025-01-01T00:00:00Z"
}
```

**Example**:
```bash
curl -H "Authorization: Bearer TOKEN" \
  https://api.example.com/v1/users/123
```

#### Create User
```
POST /users
```

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
```

**Response**: `201 Created`
```json
{
  "id": "124",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2025-11-10T00:00:00Z"
}
```

**Errors**:
- `400 Bad Request`: Invalid input
- `409 Conflict`: Email already exists

## Error Handling

All errors follow this format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": ["Specific error detail"]
  }
}
```

Common error codes:
- `UNAUTHORIZED`: Missing or invalid authentication
- `FORBIDDEN`: Insufficient permissions
- `NOT_FOUND`: Resource not found
- `VALIDATION_ERROR`: Invalid input data
- `RATE_LIMIT_EXCEEDED`: Too many requests

## Rate Limiting

- Rate limit: 1000 requests per hour
- Limit resets: Every hour at :00
- Headers returned:
  - `X-RateLimit-Limit`: Total limit
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Reset timestamp
```

---

## Documentation Standards

### Writing Style

- Use clear, concise language
- Avoid jargon or explain when necessary
- Write for the target audience (developers vs. end-users)
- Use active voice
- Provide examples for everything
- Keep paragraphs short (3-5 sentences)

### Structure

- Start with overview/introduction
- Include table of contents for long documents
- Use clear headings and subheadings
- Provide step-by-step instructions
- Include troubleshooting section
- Add "Next Steps" or "See Also" sections

### Code Examples

- Always test code examples
- Include complete, runnable examples
- Add comments explaining key parts
- Show expected output
- Cover common use cases

### Maintenance

- Date all documentation
- Version documentation with code
- Mark deprecated features clearly
- Keep examples up to date
- Regular review and updates

---

## Collaboration Patterns

### With Architect (or architect-role-skill)

- Review ARCHITECTURE.md for technical accuracy
- Request clarification on design decisions
- Ensure documentation reflects actual architecture

### With Builder (or builder-role-skill)

- Request code walkthroughs for complex features
- Verify API examples match implementation
- Update docs when code changes

### With DevOps (or devops-role-skill)

- Coordinate on deployment documentation
- Verify infrastructure details
- Document monitoring and operations procedures

---

## Examples

### Example 1: New Project Documentation

**Task**: Create complete documentation suite for new Node.js API

```markdown
## Deliverables Created
- README.md (project overview, quick start)
- BUILDING.md (development setup, build process)
- DEPLOYMENT.md (Docker, Kubernetes, cloud platforms)
- API.md (endpoints, authentication, examples)
- CONTRIBUTING.md (contribution guidelines)

**Result**: Complete documentation enabling new developers to get started within 30 minutes
```

### Example 2: API Documentation Update

**Task**: Document 15 new API endpoints after feature development

```markdown
## Documentation Added
- Endpoint specifications (request/response schemas)
- Authentication requirements
- Code examples in bash/curl
- Error scenarios and handling
- Rate limiting details

**Result**: API documentation coverage increased from 60% to 95%
```

---

## Resources

### Templates

- `resources/README_template.md` - Project README template
- `resources/API_template.md` - API documentation template
- `resources/DEPLOYMENT_template.md` - Deployment guide template
- `resources/CONTRIBUTING_template.md` - Contribution guidelines template

### Style Guides

- [Google Developer Documentation Style Guide](https://developers.google.com/style)
- [Microsoft Writing Style Guide](https://docs.microsoft.com/en-us/style-guide/)
- [Write the Docs](https://www.writethedocs.org/)

---

## References

- [Agent Skills vs. Multi-Agent](../../docs/best-practices/09-Agent-Skills-vs-Multi-Agent.md)
- [Markdown Guide](https://www.markdownguide.org/)
- [API Documentation Best Practices](https://swagger.io/resources/articles/best-practices-in-api-documentation/)

---

**Version**: 1.0.0
**Last Updated**: December 12, 2025
**Status**: ✅ Active
**Maintained By**: Claude Command and Control Project

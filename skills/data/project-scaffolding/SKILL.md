---
name: project-scaffolding
description: Project type detection matrix, template recommendations per project type, post-scaffolding checklist, Harness integration patterns, and testing recommendations
allowed-tools: [Bash, Read, Write, Edit, Glob, Grep, Task, WebFetch, WebSearch]
dependencies: [universal-templating, harness-expert]
triggers: [scaffold project, create project, project template, project type, initialize project]
---

# Project Scaffolding Skill

Comprehensive guide to project type detection, template selection, post-scaffolding setup, Harness integration, and testing strategies.

## Project Type Detection Matrix

### How to Detect Project Type

**Detection Priority:**
1. Look for language-specific files in root
2. Check build system presence
3. Examine package/dependency files
4. Analyze configuration files
5. Review existing CI/CD setup

### Type Identification Checklist

```
Python Project:
  ✓ setup.py, pyproject.toml, or requirements.txt
  ✓ .python-version file
  ✓ Pipfile (Pipenv)
  ✓ poetry.lock (Poetry)

Node.js/JavaScript:
  ✓ package.json exists
  ✓ node_modules/ directory
  ✓ .npmrc or .yarnrc
  ✓ yarn.lock or package-lock.json

Java/JVM:
  ✓ pom.xml (Maven) or build.gradle (Gradle)
  ✓ src/main/java structure
  ✓ .java files present

Go:
  ✓ go.mod file
  ✓ *.go source files
  ✓ go.sum dependencies file

Rust:
  ✓ Cargo.toml
  ✓ src/ directory
  ✓ Cargo.lock

C#/.NET:
  ✓ *.csproj or *.sln files
  ✓ appsettings.json
  ✓ global.json

TypeScript:
  ✓ tsconfig.json
  ✓ *.ts or *.tsx files
  ✓ package.json with typescript dependency

Kubernetes/DevOps:
  ✓ Dockerfile
  ✓ docker-compose.yml
  ✓ k8s/ or helm/ directory
  ✓ Helmfile

Infrastructure as Code:
  ✓ *.tf files (Terraform)
  ✓ bicep/ directory (Azure Bicep)
  ✓ cloudformation.yaml (AWS CloudFormation)
```

---

## Project Type Recommendations Matrix

### 1. Python Projects

**Best Templates:**
- **Cookiecutter** - Standard Python projects, packages
- **Copier** - Complex projects with versioning needs
- **Poetry** - Modern Python packaging

**Template Structure:**
```
{project_name}/
├── {project_name}/          # Main package
│   ├── __init__.py
│   ├── main.py
│   └── config.py
├── tests/                   # Test directory
│   ├── __init__.py
│   ├── conftest.py         # pytest fixtures
│   └── test_main.py
├── docs/                    # Documentation
│   ├── conf.py             # Sphinx config
│   ├── index.rst
│   └── api.rst
├── .gitignore
├── README.md
├── LICENSE
├── requirements.txt         # Or pyproject.toml
├── setup.py                # Or tool.poetry in pyproject.toml
├── pytest.ini
├── tox.ini                 # Multi-environment testing
└── Dockerfile
```

**Key Variables:**
```yaml
project_name: str           # Package name (lowercase, underscores)
author_name: str           # Author name
author_email: str          # Author email
python_version: str        # Target version (3.9, 3.10, 3.11, 3.12)
use_poetry: bool          # Use Poetry for dependency management
use_pytest: bool          # Use pytest (default: true)
use_docker: bool          # Include Dockerfile
include_cli: bool         # Include Click CLI framework
```

**Post-Scaffolding:**
```bash
cd {project_name}
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest tests/             # Verify test setup
```

---

### 2. Node.js/JavaScript Projects

**Best Templates:**
- **Cookiecutter** - Standard Node projects
- **Copier** - Full-stack applications

**Template Structure:**
```
{project_name}/
├── src/
│   ├── index.js
│   ├── config.js
│   └── utils/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── public/                # Static assets
├── docs/
├── .env.example          # Environment template
├── .eslintrc.json        # ESLint config
├── .prettierrc.json      # Code formatting
├── jest.config.js        # Jest testing config
├── tsconfig.json         # If using TypeScript
├── package.json
├── package-lock.json     # Or yarn.lock / pnpm-lock.yaml
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── README.md
└── LICENSE
```

**Key Variables:**
```yaml
project_name: str              # Project name
author_name: str               # Author
use_typescript: bool          # TypeScript support
use_eslint: bool              # ESLint (default: true)
use_prettier: bool            # Code formatter
use_jest: bool                # Jest testing
use_docker: bool              # Docker support
use_express: bool             # Express.js framework
package_manager: str          # npm, yarn, pnpm
```

**Post-Scaffolding:**
```bash
cd {project_name}
npm install              # or yarn / pnpm install
npm run lint             # Check linting
npm run test             # Run tests
npm run dev              # Start development server
```

---

### 3. Java/JVM Projects

**Best Templates:**
- **Maven Archetypes** - Standard Java projects
- **Gradle Template** - Gradle-based projects

**Template Structure (Maven):**
```
{project_name}/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/company/{project_name}/
│   │   │       ├── App.java
│   │   │       └── service/
│   │   └── resources/
│   │       └── application.properties
│   └── test/
│       ├── java/
│       │   └── com/company/{project_name}/
│       │       └── AppTest.java
│       └── resources/
├── docs/
├── pom.xml              # Maven configuration
├── README.md
├── Dockerfile
└── .gitignore
```

**Key Variables:**
```yaml
groupId: str             # Maven group ID (e.g., com.company)
artifactId: str          # Maven artifact ID
package: str             # Java package name
java_version: str        # JDK version (11, 17, 21)
spring_boot_version: str # If using Spring Boot
build_tool: str          # maven or gradle
```

**Post-Scaffolding:**
```bash
cd {project_name}
mvn clean compile        # Compile project
mvn test                 # Run tests
mvn spring-boot:run      # If using Spring Boot
```

---

### 4. TypeScript Projects

**Best Templates:**
- **ts-node** - CLI tools and scripts
- **Next.js** - Full-stack web applications
- **NestJS** - Backend APIs

**Template Structure:**
```
{project_name}/
├── src/
│   ├── index.ts
│   ├── types/
│   │   └── index.ts
│   ├── services/
│   ├── controllers/      # If REST API
│   └── utils/
├── tests/
│   ├── unit/
│   └── integration/
├── dist/                 # Compiled JavaScript (output)
├── tsconfig.json        # TypeScript config
├── jest.config.js       # Jest testing
├── .eslintrc.json       # ESLint
├── package.json
├── Dockerfile
├── README.md
└── .gitignore
```

**Key Variables:**
```yaml
project_name: str
typescript_version: str   # Exact version or latest
jest_enabled: bool        # Testing framework
eslint_enabled: bool      # Linting
strict_mode: bool         # tsconfig strict
target: str               # Compilation target (ES2020, etc.)
module: str               # Module system (ESNext, CommonJS)
```

**Post-Scaffolding:**
```bash
cd {project_name}
npm install
npm run build             # Compile TypeScript
npm test                  # Run tests
npm start                 # Run compiled code
```

---

### 5. Go Projects

**Best Templates:**
- **Go Project Layout** - Standard Go project structure
- **Cobra CLI** - CLI applications

**Template Structure:**
```
{project_name}/
├── cmd/
│   ├── cli/
│   │   └── main.go      # Application entry point
│   └── server/          # If server application
│       └── main.go
├── internal/            # Private packages
│   ├── config/
│   ├── handler/
│   └── service/
├── pkg/                 # Public packages
│   └── {package_name}/
├── api/                 # API definitions
├── test/
├── docs/
├── Makefile             # Build automation
├── go.mod               # Module definition
├── go.sum               # Checksums
├── Dockerfile
├── .gitignore
├── README.md
└── LICENSE
```

**Key Variables:**
```yaml
project_name: str        # Go module name (github.com/user/project)
author_name: str
go_version: str          # Minimum Go version (1.19, 1.20, 1.21)
use_cobra: bool          # CLI framework
use_gin: bool            # Web framework (if server)
use_gorm: bool           # ORM (if database needed)
```

**Post-Scaffolding:**
```bash
cd {project_name}
go mod download          # Download dependencies
go build ./cmd/cli       # Build application
go test ./...            # Run tests
./cli --help             # Test CLI
```

---

### 6. Kubernetes/DevOps Projects

**Best Templates:**
- **Helm Chart** - Kubernetes deployments
- **Kustomize** - Kubernetes customization
- **Copier** - Multi-environment setups

**Template Structure:**
```
{project_name}/
├── helm/
│   └── {release_name}/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-dev.yaml
│       ├── values-prod.yaml
│       └── templates/
│           ├── deployment.yaml
│           ├── service.yaml
│           ├── configmap.yaml
│           └── ingress.yaml
├── k8s/
│   ├── base/
│   ├── dev/
│   └── prod/
├── kustomization.yaml
├── docker-compose.yml   # For local development
├── Dockerfile
├── .dockerignore
├── docs/
├── README.md
└── .gitignore
```

**Key Variables:**
```yaml
project_name: str        # Application name
image_registry: str      # Docker registry
image_name: str          # Docker image name
replicas_dev: int        # Dev environment replicas
replicas_prod: int       # Prod environment replicas
namespace: str           # Kubernetes namespace
enable_ingress: bool
enable_monitoring: bool  # Prometheus/monitoring
```

**Post-Scaffolding:**
```bash
cd {project_name}
docker build -t {image}:latest .
helm lint helm/{release}
helm template helm/{release} -f values-dev.yaml
kubectl apply -f k8s/dev/  # Deploy to dev
```

---

### 7. Infrastructure as Code (Terraform)

**Best Templates:**
- **Terraform Module** - Reusable infrastructure components
- **Terraform Project** - Full environment setup

**Template Structure:**
```
{project_name}/
├── main.tf              # Main configuration
├── variables.tf         # Input variables
├── outputs.tf           # Output values
├── terraform.tfvars     # Variable values
├── locals.tf            # Local values
├── vpc.tf               # VPC configuration
├── security.tf          # Security groups
├── iam.tf               # IAM roles/policies
├── modules/
│   ├── vpc/
│   ├── compute/
│   └── database/
├── environments/
│   ├── dev/
│   │   └── terraform.tfvars
│   ├── staging/
│   └── prod/
├── docs/
├── .gitignore
├── README.md
├── versions.tf          # Terraform version constraints
└── backend.tf           # State backend config
```

**Key Variables:**
```yaml
project_name: str        # Project identifier
aws_region: str          # AWS region
environment: str         # dev, staging, prod
terraform_version: str   # Minimum version
```

**Post-Scaffolding:**
```bash
cd environments/dev
terraform init           # Initialize backend
terraform plan           # Preview changes
terraform apply          # Apply configuration
terraform output         # View outputs
```

---

## Post-Scaffolding Checklist

### Universal Tasks (All Projects)

- [ ] Review generated files and structure
- [ ] Verify .gitignore is appropriate
- [ ] Update README.md with project-specific info
- [ ] Add LICENSE file (if not included)
- [ ] Initialize Git repository
- [ ] Create initial commit
- [ ] Add remote repository
- [ ] Verify dependency installation
- [ ] Run basic tests to confirm setup works
- [ ] Document build/run commands
- [ ] Set up CI/CD configuration

### Language-Specific Tasks

**Python:**
- [ ] Verify virtual environment works
- [ ] Test package imports
- [ ] Check pytest configuration
- [ ] Verify linting (flake8/pylint) setup
- [ ] Test documentation build (if Sphinx)
- [ ] Verify type hints (if mypy configured)

**Node.js:**
- [ ] Verify npm/yarn/pnpm setup
- [ ] Test linting and formatting
- [ ] Verify test framework (Jest/Mocha)
- [ ] Check TypeScript compilation
- [ ] Verify build output directory
- [ ] Test hot reload (if dev server)

**Java:**
- [ ] Verify Maven/Gradle build
- [ ] Test unit tests run successfully
- [ ] Verify IDE integration
- [ ] Check dependency tree
- [ ] Verify JAR/WAR packaging

**Go:**
- [ ] Verify go mod download
- [ ] Test build command
- [ ] Verify all tests pass
- [ ] Check linting (golangci-lint)
- [ ] Verify binary execution

### Docker Tasks

- [ ] Build Docker image
- [ ] Test image runs locally
- [ ] Verify volumes/ports are correct
- [ ] Document docker run command
- [ ] Add Docker Compose if multi-container
- [ ] Set up .dockerignore

---

## Harness Integration Patterns

### Pattern 1: Basic CI Pipeline

**For:** Single service, simple build and push

```yaml
# harness/build-pipeline.yaml
pipeline:
  name: Build and Push
  identifier: build_push
  stages:
    - stage:
        name: Build Docker
        type: CI
        spec:
          codebase:
            repoName: {project_name}
            branch: main
          build:
            type: Docker
            spec:
              dockerfile: Dockerfile
              registryConnector: <+input.docker_connector>
              imageName: <+input.image_name>
              imageTag: <+codebase.commitSha>
```

### Pattern 2: Build, Test, and Deploy

**For:** Multi-stage pipeline with testing

```yaml
pipeline:
  name: Build Test Deploy
  identifier: build_test_deploy
  stages:
    - stage:
        name: Build
        type: CI
        spec:
          build:
            type: Docker
            spec:
              dockerfile: Dockerfile

    - stage:
        name: Test
        type: CI
        depends_on:
          - Build
        spec:
          steps:
            - step:
                type: Run
                spec:
                  image: <+artifact.image>
                  script: npm test

    - stage:
        name: Deploy Dev
        type: Deployment
        depends_on:
          - Test
        spec:
          service:
            serviceRef: <+input.service>
          environment:
            environmentRef: dev
```

### Pattern 3: Multi-Environment Deployment

**For:** Dev → Staging → Production with approvals

```yaml
stages:
  - stage:
      name: Deploy Dev
      type: Deployment
      spec:
        environment: dev
        infrastructure: dev-k8s-cluster

  - stage:
      name: Deploy Staging
      type: Deployment
      depends_on:
        - Deploy Dev
      spec:
        environment: staging
        infrastructure: staging-k8s-cluster

  - stage:
      name: Approval for Production
      type: Approval
      depends_on:
        - Deploy Staging
      spec:
        approvers:
          - <+input.approver_group>

  - stage:
      name: Deploy Production
      type: Deployment
      depends_on:
        - Approval for Production
      spec:
        environment: production
        infrastructure: prod-k8s-cluster
```

### Pattern 4: GitOps with Harness

**For:** Managing manifests separately from source code

```yaml
stages:
  - stage:
      name: Build
      type: CI
      spec:
        build:
          type: Docker

  - stage:
      name: Update Manifests
      type: CI
      spec:
        steps:
          - step:
              type: Run
              spec:
                script: |
                  git clone <+input.manifest_repo>
                  sed -i "s/IMAGE_TAG/<+artifact.imageTag>/g" k8s/deployment.yaml
                  git commit && git push

  - stage:
      name: Deploy via GitOps
      type: Deployment
      spec:
        gitOpsEnabled: true
        service:
          serviceRef: <+input.service>
        environment:
          environmentRef: <+input.environment>
```

---

## Testing Recommendations by Project Type

### Python Testing

**Frameworks:**
- **pytest** - Modern, flexible test framework
- **unittest** - Standard library
- **nose2** - Plugin-based testing

**Setup:**
```bash
pip install pytest pytest-cov pytest-mock
```

**Test Structure:**
```
tests/
├── conftest.py          # Shared fixtures
├── unit/
│   ├── test_module.py
│   └── test_service.py
├── integration/
│   └── test_api.py
└── fixtures/
    └── sample_data.py
```

**Coverage Target:** 80%+

---

### Node.js Testing

**Frameworks:**
- **Jest** - All-in-one solution
- **Mocha + Chai** - Flexible combination
- **Vitest** - Fast alternative

**Setup:**
```bash
npm install --save-dev jest @testing-library/react
```

**Test Structure:**
```
tests/
├── unit/
│   ├── utils.test.js
│   └── helpers.test.js
├── integration/
│   └── api.test.js
└── e2e/
    └── user-flow.test.js
```

**Coverage Target:** 80%+

---

### Java Testing

**Frameworks:**
- **JUnit 5** - Modern testing framework
- **Mockito** - Mocking framework
- **TestNG** - Alternative to JUnit

**Setup:**
```xml
<dependency>
    <groupId>junit</groupId>
    <artifactId>junit-jupiter</artifactId>
    <scope>test</scope>
</dependency>
```

**Test Structure:**
```
src/test/java/
└── com/company/project/
    ├── ServiceTest.java
    ├── ControllerTest.java
    └── IntegrationTest.java
```

**Coverage Target:** 80%+

---

### Go Testing

**Testing Style:**
- Standard Go testing package
- Table-driven tests
- Subtests

**Setup:**
```bash
go get github.com/stretchr/testify
```

**Test Structure:**
```
internal/
├── service/
│   ├── service.go
│   └── service_test.go
└── handler/
    ├── handler.go
    └── handler_test.go
```

**Coverage Target:** 80%+

---

## Post-Scaffolding Setup Verification

### Universal Verification Commands

```bash
# Git setup
git init
git add .
git commit -m "Initial commit from template"

# Dependency verification
{build-tool} list              # List dependencies

# Test verification
{build-tool} test              # Run test suite

# Build verification
{build-tool} build             # Build project

# Docker verification (if applicable)
docker build -t {image}:test .
docker run {image}:test --version
```

### Checklist Summary

```
ESSENTIAL:
- [ ] Project initialized and builds
- [ ] Dependencies installed
- [ ] Tests run and pass
- [ ] Documentation exists
- [ ] .gitignore configured
- [ ] Initial commit created

HARNESS INTEGRATION:
- [ ] Harness service created
- [ ] Pipeline template ready
- [ ] Environment configured
- [ ] Deployment target defined

QUALITY GATES:
- [ ] Linting passes
- [ ] Tests pass
- [ ] Code coverage >= 80%
- [ ] Documentation complete
- [ ] Security scan passes
```

---

## Related Documentation

- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)
- [Copier Documentation](https://copier.readthedocs.io/)
- [Maven Archetypes](https://maven.apache.org/guides/introduction/introduction-to-archetypes.html)
- [Harness Delegate Setup](https://developer.harness.io/docs/platform/delegates)
- [Helm Charts](https://helm.sh/docs/)
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides)

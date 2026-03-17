---
name: Pattern Extraction
description: Detect and extract patterns from codebases for template generation
version: 1.0.0
trigger_phrases:
  - "extract patterns"
  - "detect patterns"
  - "find variables"
  - "identify configuration"
  - "analyze structure"
categories: ["infrastructure", "templating", "analysis"]
---

# Pattern Extraction Skill

## When to Use This Skill

Use pattern extraction when you need to:

- **Analyze existing infrastructure** to create reusable templates
- **Convert hardcoded values** into configurable template variables
- **Identify configuration patterns** across multiple similar files
- **Detect technology stacks** and their conventions
- **Extract naming conventions** and structural patterns
- **Generate template metadata** from existing code
- **Create variable schemas** from inferred types and constraints

Perfect for:
- Converting existing IaC to templates
- Building template libraries from production code
- Standardizing infrastructure patterns
- Automating template generation
- Identifying refactoring opportunities

## Core Capabilities

### 1. Technology Stack Detection

Automatically identify:
- **IaC Frameworks**: Terraform, Pulumi, CloudFormation, ARM, Bicep
- **Cloud Providers**: AWS, Azure, GCP, multi-cloud patterns
- **Service Types**: Kubernetes, Docker, serverless, containers
- **Configuration Formats**: YAML, JSON, HCL, TOML
- **Build Systems**: Helm, Kustomize, Jsonnet
- **CI/CD Platforms**: GitHub Actions, GitLab CI, Jenkins, Harness

### 2. Configuration Pattern Extraction

Extract patterns from:
- Resource definitions and relationships
- Environment-specific configurations
- Naming conventions and tagging strategies
- Security policies and compliance rules
- Network topologies and architectures
- Deployment strategies and workflows

### 3. Variable Identification

Intelligent detection of:
- **Hardcoded Values**: Strings, numbers, booleans that should be variables
- **Repeated Values**: Values appearing multiple times across files
- **Environment Indicators**: dev, staging, prod patterns
- **Naming Patterns**: Prefixes, suffixes, delimiters
- **Secret Patterns**: API keys, passwords, tokens (flag for security)
- **Configuration Schemas**: Type inference from usage

### 4. Structure Analysis

Analyze:
- File organization and directory structure
- Module boundaries and dependencies
- Resource hierarchies and relationships
- Configuration inheritance patterns
- Composition and reuse strategies
- Template inclusion patterns

## Pattern Detection Matrix

| Pattern Type | Indicators | Extraction Method | Output Format |
|--------------|-----------|-------------------|---------------|
| **Environment Values** | `dev`, `staging`, `prod` in names | Context-aware regex | `{{ environment }}` |
| **Resource Names** | Repeated prefixes/suffixes | Token analysis | `{{ project_name }}-{{ resource_type }}` |
| **Region/Location** | `us-east-1`, `westeurope` | Cloud provider patterns | `{{ region }}` |
| **Version Numbers** | Semantic versioning patterns | Regex + validation | `{{ version }}` |
| **Port Numbers** | Common service ports | Port range analysis | `{{ port }}` |
| **Size/Scale** | Instance types, node counts | Capacity patterns | `{{ instance_size }}` |
| **CIDR Blocks** | IP address ranges | Network pattern analysis | `{{ cidr_block }}` |
| **Tags/Labels** | Key-value metadata | Metadata extraction | `{{ tags }}` |
| **Secret References** | Vault paths, secret names | Secret pattern detection | `{{ secret_ref }}` (secure) |
| **Feature Flags** | Boolean toggles | Conditional analysis | `{{ enable_feature }}` |

## Variable Inference Rules

### Before/After Transformation Examples

#### Example 1: Resource Names

**Before:**
```hcl
resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.medium"

  tags = {
    Name        = "myapp-web-server-prod"
    Environment = "production"
    Project     = "myapp"
  }
}
```

**After:**
```hcl
resource "aws_instance" "web_server" {
  ami           = "{{ ami_id }}"
  instance_type = "{{ instance_type }}"

  tags = {
    Name        = "{{ project_name }}-web-server-{{ environment }}"
    Environment = "{{ environment }}"
    Project     = "{{ project_name }}"
  }
}
```

**Extracted Variables:**
```yaml
variables:
  ami_id:
    type: string
    description: "AMI ID for the EC2 instance"
    default: "ami-0c55b159cbfafe1f0"
    pattern: "^ami-[a-f0-9]{17}$"

  instance_type:
    type: string
    description: "EC2 instance type"
    default: "t3.medium"
    allowed_values: ["t3.micro", "t3.small", "t3.medium", "t3.large"]

  project_name:
    type: string
    description: "Project identifier used in resource naming"
    default: "myapp"
    pattern: "^[a-z][a-z0-9-]{2,30}$"

  environment:
    type: string
    description: "Deployment environment"
    default: "production"
    allowed_values: ["dev", "staging", "production"]
```

#### Example 2: Kubernetes Deployment

**Before:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
        version: "1.21.0"
    spec:
      containers:
      - name: nginx
        image: nginx:1.21.0
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "128Mi"
            cpu: "250m"
          limits:
            memory: "256Mi"
            cpu: "500m"
```

**After:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ app_name }}-deployment
  namespace: {{ namespace }}
spec:
  replicas: {{ replica_count }}
  selector:
    matchLabels:
      app: {{ app_name }}
  template:
    metadata:
      labels:
        app: {{ app_name }}
        version: "{{ app_version }}"
    spec:
      containers:
      - name: {{ app_name }}
        image: {{ container_image }}:{{ app_version }}
        ports:
        - containerPort: {{ container_port }}
        resources:
          requests:
            memory: "{{ memory_request }}"
            cpu: "{{ cpu_request }}"
          limits:
            memory: "{{ memory_limit }}"
            cpu: "{{ cpu_limit }}"
```

**Extracted Variables:**
```yaml
variables:
  app_name:
    type: string
    description: "Application name"
    default: "nginx"

  namespace:
    type: string
    description: "Kubernetes namespace"
    default: "production"

  replica_count:
    type: integer
    description: "Number of pod replicas"
    default: 3
    min: 1
    max: 10

  app_version:
    type: string
    description: "Application version"
    default: "1.21.0"
    pattern: "^\\d+\\.\\d+\\.\\d+$"

  container_image:
    type: string
    description: "Container image name"
    default: "nginx"

  container_port:
    type: integer
    description: "Container port"
    default: 80

  memory_request:
    type: string
    description: "Memory request"
    default: "128Mi"

  memory_limit:
    type: string
    description: "Memory limit"
    default: "256Mi"

  cpu_request:
    type: string
    description: "CPU request"
    default: "250m"

  cpu_limit:
    type: string
    description: "CPU limit"
    default: "500m"
```

#### Example 3: Azure Bicep

**Before:**
```bicep
resource storageAccount 'Microsoft.Storage/storageAccounts@2021-04-01' = {
  name: 'mystorageacct12345'
  location: 'westeurope'
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    allowBlobPublicAccess: false
  }
  tags: {
    environment: 'production'
    costCenter: 'engineering'
    project: 'platform'
  }
}
```

**After:**
```bicep
resource storageAccount 'Microsoft.Storage/storageAccounts@2021-04-01' = {
  name: '{{ storage_account_name }}'
  location: '{{ location }}'
  sku: {
    name: '{{ sku_name }}'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: '{{ access_tier }}'
    minimumTlsVersion: '{{ min_tls_version }}'
    supportsHttpsTrafficOnly: {{ https_only }}
    allowBlobPublicAccess: {{ allow_public_access }}
  }
  tags: {
    environment: '{{ environment }}'
    costCenter: '{{ cost_center }}'
    project: '{{ project_name }}'
  }
}
```

**Extracted Variables:**
```yaml
variables:
  storage_account_name:
    type: string
    description: "Storage account name (globally unique)"
    default: "mystorageacct12345"
    pattern: "^[a-z0-9]{3,24}$"

  location:
    type: string
    description: "Azure region"
    default: "westeurope"
    allowed_values: ["westeurope", "northeurope", "eastus", "westus"]

  sku_name:
    type: string
    description: "Storage account SKU"
    default: "Standard_LRS"
    allowed_values: ["Standard_LRS", "Standard_GRS", "Premium_LRS"]

  access_tier:
    type: string
    description: "Storage access tier"
    default: "Hot"
    allowed_values: ["Hot", "Cool"]

  min_tls_version:
    type: string
    description: "Minimum TLS version"
    default: "TLS1_2"

  https_only:
    type: boolean
    description: "Require HTTPS traffic only"
    default: true

  allow_public_access:
    type: boolean
    description: "Allow public blob access"
    default: false

  environment:
    type: string
    description: "Environment name"
    default: "production"

  cost_center:
    type: string
    description: "Cost center for billing"
    default: "engineering"

  project_name:
    type: string
    description: "Project name"
    default: "platform"
```

## Decision Tree

Pattern classification flowchart:

```
START: Analyze value/pattern
    |
    v
┌───────────────────────────────────┐
│ Is it repeated across files?      │
└─────┬─────────────────────┬───────┘
      │ YES                 │ NO
      v                     v
┌─────────────┐      ┌──────────────┐
│ Global Var  │      │ Check Usage  │
└─────────────┘      └──────┬───────┘
                            │
                            v
                     ┌──────────────────────┐
                     │ Used in conditionals? │
                     └──┬─────────────────┬──┘
                        │ YES             │ NO
                        v                 v
                 ┌──────────┐      ┌──────────────┐
                 │ Feature  │      │ Check Type   │
                 │ Flag     │      └──────┬───────┘
                 └──────────┘             │
                                          v
                                   ┌──────────────────────┐
                                   │ Contains 'env'?      │
                                   └──┬───────────────┬───┘
                                      │ YES           │ NO
                                      v               v
                                ┌───────────┐   ┌──────────────┐
                                │ Env Var   │   │ Check Format │
                                └───────────┘   └──────┬───────┘
                                                       │
                                                       v
                                                ┌──────────────────┐
                                                │ Cloud resource?  │
                                                └──┬───────────┬───┘
                                                   │ YES       │ NO
                                                   v           v
                                            ┌──────────┐  ┌─────────┐
                                            │ Resource │  │ Generic │
                                            │ ID       │  │ Config  │
                                            └──────────┘  └─────────┘
```

## Examples

### Example 1: Extract Terraform AWS Pattern

**Input:**
```bash
extract patterns from ./terraform/aws/ec2-instances.tf
```

**Analysis:**
```
Analyzing: terraform/aws/ec2-instances.tf
├── Technology: Terraform (AWS Provider)
├── Resources Found: 3 (aws_instance, aws_security_group, aws_eip)
├── Variables Identified: 12
└── Patterns Detected:
    ├── Naming Convention: {project}-{resource}-{env}
    ├── Tag Strategy: Environment, Project, ManagedBy
    └── Configuration Reuse: 85% similarity across instances
```

**Extracted Template:**
```hcl
# Template: aws-ec2-instance.tf.tmpl
variable "project_name" {
  type        = string
  description = "Project identifier"
}

variable "environment" {
  type        = string
  description = "Deployment environment"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_config" {
  type = object({
    ami           = string
    instance_type = string
    key_name      = string
    subnet_id     = string
  })
  description = "EC2 instance configuration"
}

resource "aws_instance" "main" {
  ami           = var.instance_config.ami
  instance_type = var.instance_config.instance_type
  key_name      = var.instance_config.key_name
  subnet_id     = var.instance_config.subnet_id

  vpc_security_group_ids = [aws_security_group.main.id]

  tags = {
    Name        = "${var.project_name}-instance-${var.environment}"
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
  }
}

resource "aws_security_group" "main" {
  name        = "${var.project_name}-sg-${var.environment}"
  description = "Security group for ${var.project_name} in ${var.environment}"

  tags = {
    Name        = "${var.project_name}-sg-${var.environment}"
    Environment = var.environment
    Project     = var.project_name
  }
}
```

### Example 2: Extract Kubernetes Pattern

**Input:**
```bash
extract patterns from ./k8s/deployments/ --type kubernetes
```

**Analysis:**
```
Analyzing: k8s/deployments/ (15 files)
├── Technology: Kubernetes (v1.24+)
├── Resources Found: 45 total
│   ├── Deployments: 15
│   ├── Services: 12
│   ├── ConfigMaps: 10
│   └── Ingresses: 8
├── Common Patterns:
│   ├── Label Strategy: app, version, environment
│   ├── Resource Requests: 90% use standard sizes
│   ├── Probes: 100% have health checks
│   └── Image Pattern: registry/org/image:tag
└── Variable Candidates: 28 identified
```

**Extracted Template:**
```yaml
# Template: kubernetes-microservice.yaml.tmpl
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ service_name }}-deployment
  namespace: {{ namespace }}
  labels:
    app: {{ service_name }}
    version: {{ version }}
    environment: {{ environment }}
spec:
  replicas: {{ replica_count }}
  selector:
    matchLabels:
      app: {{ service_name }}
  template:
    metadata:
      labels:
        app: {{ service_name }}
        version: {{ version }}
        environment: {{ environment }}
    spec:
      containers:
      - name: {{ service_name }}
        image: {{ image_registry }}/{{ organization }}/{{ service_name }}:{{ version }}
        ports:
        - containerPort: {{ container_port }}
          protocol: TCP
        env:
        {{#each environment_variables}}
        - name: {{ name }}
          value: "{{ value }}"
        {{/each}}
        resources:
          requests:
            memory: {{ memory_request }}
            cpu: {{ cpu_request }}
          limits:
            memory: {{ memory_limit }}
            cpu: {{ cpu_limit }}
        livenessProbe:
          httpGet:
            path: {{ health_check_path }}
            port: {{ container_port }}
          initialDelaySeconds: {{ liveness_initial_delay }}
          periodSeconds: {{ liveness_period }}
        readinessProbe:
          httpGet:
            path: {{ readiness_check_path }}
            port: {{ container_port }}
          initialDelaySeconds: {{ readiness_initial_delay }}
          periodSeconds: {{ readiness_period }}
---
apiVersion: v1
kind: Service
metadata:
  name: {{ service_name }}-service
  namespace: {{ namespace }}
  labels:
    app: {{ service_name }}
spec:
  type: {{ service_type }}
  ports:
  - port: {{ service_port }}
    targetPort: {{ container_port }}
    protocol: TCP
  selector:
    app: {{ service_name }}
```

### Example 3: Multi-File Pattern Extraction

**Input:**
```bash
extract patterns from ./infrastructure/ --recursive --consolidate
```

**Analysis:**
```
Analyzing: infrastructure/ (recursive)
├── Files Scanned: 47
├── Technologies Detected:
│   ├── Terraform (AWS): 23 files
│   ├── Kubernetes: 15 files
│   ├── Helm Charts: 9 files
│   └── Docker Compose: 2 files (excluded - different pattern)
├── Cross-Cutting Patterns:
│   ├── Environment Strategy: 3-tier (dev/staging/prod)
│   ├── Tagging: 100% compliance with org policy
│   ├── Naming: Consistent kebab-case with env suffix
│   └── Secrets: HashiCorp Vault references
└── Template Opportunities:
    ├── AWS Lambda Function: 8 similar resources
    ├── RDS Database: 5 similar resources
    ├── Kubernetes Service: 12 similar resources
    └── ALB Configuration: 6 similar resources
```

**Output:**
```
Generated Templates:
├── templates/
│   ├── aws-lambda-function.tf.tmpl (consolidated from 8 files)
│   ├── aws-rds-instance.tf.tmpl (consolidated from 5 files)
│   ├── kubernetes-service.yaml.tmpl (consolidated from 12 files)
│   └── aws-alb.tf.tmpl (consolidated from 6 files)
└── variables/
    ├── common.yaml (shared across all templates)
    ├── aws-specific.yaml (AWS provider variables)
    └── kubernetes-specific.yaml (K8s variables)

Variable Reuse Analysis:
├── Shared Variables: 15 (45% reuse)
├── Template-Specific: 18 (55% unique)
└── Potential Consolidation: 3 variables can be merged
```

## Best Practices

### 1. Incremental Extraction
Start with a single file or small directory to refine patterns before scaling:
```bash
# Start small
extract patterns from ./terraform/main.tf

# Validate and adjust
review template ./templates/main.tf.tmpl

# Scale up
extract patterns from ./terraform/ --recursive
```

### 2. Variable Naming Conventions
Follow consistent naming:
- Use snake_case for variables
- Prefix with context: `aws_`, `k8s_`, `azure_`
- Suffix with type: `_count`, `_enabled`, `_config`
- Be descriptive: `instance_type` not `type`

### 3. Type Inference Priority
1. **Explicit types** from existing variable definitions
2. **Usage patterns** (e.g., used in math → number)
3. **Value format** (e.g., "true"/"false" → boolean)
4. **Defaults** to string if ambiguous

### 4. Security-Sensitive Patterns
Always flag potential secrets:
```yaml
# Good - flagged for security review
api_key:
  type: string
  sensitive: true
  description: "API key for external service"
  default: null  # Force explicit value
```

### 5. Validation Rules
Add validation for critical variables:
```yaml
environment:
  type: string
  allowed_values: ["dev", "staging", "prod"]

cidr_block:
  type: string
  pattern: "^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}/\\d{1,2}$"

replica_count:
  type: integer
  min: 1
  max: 100
```

### 6. Documentation Generation
Auto-generate docs from extracted patterns:
```markdown
# Generated Template: aws-ec2-instance

## Description
Extracted from 8 similar EC2 instance definitions.
Pattern confidence: 95%

## Variables
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| instance_type | string | Yes | t3.medium | EC2 instance type |
| environment | string | Yes | - | Deployment environment |

## Usage
terraform apply -var="instance_type=t3.large" -var="environment=prod"
```

### 7. Pattern Confidence Scoring
Rate extraction confidence:
- **High (90-100%)**: Identical patterns across files
- **Medium (70-89%)**: Similar with minor variations
- **Low (<70%)**: Significant differences, manual review needed

### 8. Iterative Refinement
```bash
# Extract initial patterns
extract patterns from ./infra/ --output ./templates/v1/

# Review and refine
review templates ./templates/v1/ --suggest-improvements

# Re-extract with refinements
extract patterns from ./infra/ --output ./templates/v2/ \
  --naming-convention kebab-case \
  --tag-strategy company-standard
```

## Related Skills

- **[[template-generation]]** - Generate templates from extracted patterns
- **[[variable-schema-design]]** - Design robust variable schemas
- **[[template-validation]]** - Validate generated templates
- **[[naming-convention-analyzer]]** - Analyze and enforce naming conventions
- **[[configuration-consolidation]]** - Merge similar configurations
- **[[security-pattern-detection]]** - Identify security anti-patterns
- **[[compliance-checking]]** - Ensure extracted patterns meet compliance requirements

## Advanced Techniques

### Multi-Stage Extraction Pipeline

```bash
# Stage 1: Initial scan
extract patterns from ./infra/ --stage scan

# Stage 2: Pattern classification
extract patterns from ./infra/ --stage classify

# Stage 3: Variable inference
extract patterns from ./infra/ --stage variables

# Stage 4: Template generation
extract patterns from ./infra/ --stage generate

# Stage 5: Validation
extract patterns from ./infra/ --stage validate
```

### Machine Learning-Enhanced Extraction

Use ML models to improve pattern detection:
- **Clustering**: Group similar configurations
- **Anomaly Detection**: Identify outliers for manual review
- **Type Inference**: Predict variable types from usage
- **Dependency Analysis**: Extract implicit dependencies

### Cross-Repository Pattern Mining

Extract patterns across multiple repositories:
```bash
extract patterns --repos-file ./repos.txt \
  --output ./org-templates/ \
  --consolidate-org-wide
```

## Output Formats

### JSON Schema
```json
{
  "template": "aws-ec2-instance",
  "version": "1.0.0",
  "variables": {
    "instance_type": {
      "type": "string",
      "default": "t3.medium",
      "description": "EC2 instance type"
    }
  }
}
```

### YAML Schema
```yaml
template: aws-ec2-instance
version: 1.0.0
variables:
  instance_type:
    type: string
    default: t3.medium
    description: EC2 instance type
```

### Terraform Variable Definitions
```hcl
variable "instance_type" {
  type        = string
  default     = "t3.medium"
  description = "EC2 instance type"
}
```

## Integration Points

- **CI/CD Pipelines**: Auto-extract patterns on code changes
- **Template Registries**: Publish extracted templates
- **Documentation Systems**: Generate docs from patterns
- **Monitoring**: Track pattern usage and evolution
- **Compliance Tools**: Validate against org standards

## Troubleshooting

### Pattern Detection Issues

**Problem**: Too many false positives
**Solution**: Increase confidence threshold, add exclusion patterns

**Problem**: Missing obvious patterns
**Solution**: Check file encoding, adjust regex patterns, enable debug mode

**Problem**: Inconsistent variable names
**Solution**: Enable smart naming normalization, use naming dictionary

### Template Generation Issues

**Problem**: Templates too generic
**Solution**: Use narrower extraction scope, increase specificity

**Problem**: Templates too specific
**Solution**: Widen extraction scope, enable cross-file consolidation

---

**Version:** 1.0.0
**Last Updated:** 2026-01-19
**Skill Type:** Analysis & Extraction
**Complexity:** Advanced

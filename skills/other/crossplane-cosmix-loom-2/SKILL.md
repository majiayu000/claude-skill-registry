---
name: crossplane
description: Cloud-native infrastructure management with Crossplane using Kubernetes APIs. Build internal platform APIs for self-service infrastructure provisioning. Use when implementing infrastructure as code, platform engineering, composite resources, XRDs, compositions, claims, provider configuration, or multi-cloud provisioning. Triggers: crossplane, XRD, composition, claim, provider, managed resource, composite resource, infrastructure API, platform engineering, platform API, infrastructure abstraction, self-service infrastructure, kubernetes infrastructure, cloud control plane.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Crossplane Infrastructure Management

Crossplane extends Kubernetes to manage cloud infrastructure using declarative APIs. It enables platform teams to build internal cloud platforms with self-service capabilities.

## Architecture Overview

### Core Components

1. **Providers**: Kubernetes controllers that provision infrastructure in external systems (AWS, GCP, Azure, etc.)
2. **Managed Resources (MRs)**: Custom resources representing external infrastructure (S3 buckets, RDS instances, etc.)
3. **Composite Resources (XRs)**: Higher-level abstractions composed of multiple managed resources
4. **Composite Resource Definitions (XRDs)**: Schemas defining composite resource types
5. **Compositions**: Templates that map XRs to managed resources with transformation logic
6. **Claims**: Namespace-scoped resources that provision composite resources for application teams
7. **Composition Functions**: Extension points for complex transformation logic

### Resource Hierarchy

```text
Claim (namespace-scoped) -> Composite Resource (cluster-scoped) -> Managed Resources -> Cloud Infrastructure
```

## Installation and Setup

### Install Crossplane

```bash
# Add Crossplane Helm repository
helm repo add crossplane-stable https://charts.crossplane.io/stable
helm repo update

# Install Crossplane
helm install crossplane \
  crossplane-stable/crossplane \
  --namespace crossplane-system \
  --create-namespace \
  --set args='{"--enable-composition-functions"}' \
  --wait

# Verify installation
kubectl get pods -n crossplane-system
```

### Install Crossplane CLI

```bash
# Install CLI for local development
curl -sL https://raw.githubusercontent.com/crossplane/crossplane/master/install.sh | sh
sudo mv crossplane /usr/local/bin/

# Verify CLI
crossplane --version
```

## Provider Configuration

### AWS Provider

```yaml
# providers/aws-provider.yaml
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-aws-s3
spec:
  package: xpkg.upbound.io/upbound/provider-aws-s3:v1.1.0
  controllerConfigRef:
    name: aws-config
---
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-aws-rds
spec:
  package: xpkg.upbound.io/upbound/provider-aws-rds:v1.1.0
  controllerConfigRef:
    name: aws-config
---
apiVersion: pkg.crossplane.io/v1alpha1
kind: ControllerConfig
metadata:
  name: aws-config
spec:
  podSecurityContext:
    fsGroup: 2000
  args:
    - --poll=1m
    - --max-reconcile-rate=100
```

### Provider Authentication

```bash
# Create AWS credentials secret
kubectl create secret generic aws-creds \
  -n crossplane-system \
  --from-file=creds=/path/to/aws-credentials.txt

# credentials.txt format:
# [default]
# aws_access_key_id = AKIAIOSFODNN7EXAMPLE
# aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

```yaml
# providers/aws-provider-config.yaml
apiVersion: aws.upbound.io/v1beta1
kind: ProviderConfig
metadata:
  name: default
spec:
  credentials:
    source: Secret
    secretRef:
      namespace: crossplane-system
      name: aws-creds
      key: creds
```

### GCP Provider

```yaml
# providers/gcp-provider.yaml
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-gcp-storage
spec:
  package: xpkg.upbound.io/upbound/provider-gcp-storage:v1.1.0
---
apiVersion: gcp.upbound.io/v1beta1
kind: ProviderConfig
metadata:
  name: default
spec:
  projectID: my-gcp-project
  credentials:
    source: Secret
    secretRef:
      namespace: crossplane-system
      name: gcp-creds
      key: creds.json
```

## Managed Resources

### Direct Managed Resource Usage

```yaml
# managed-resources/s3-bucket.yaml
apiVersion: s3.aws.upbound.io/v1beta1
kind: Bucket
metadata:
  name: my-app-data-bucket
spec:
  forProvider:
    region: us-west-2
    tags:
      Environment: production
      ManagedBy: crossplane
  providerConfigRef:
    name: default
  deletionPolicy: Delete
```

```yaml
# managed-resources/rds-instance.yaml
apiVersion: rds.aws.upbound.io/v1beta1
kind: Instance
metadata:
  name: my-postgres-db
spec:
  forProvider:
    region: us-west-2
    allocatedStorage: 20
    engine: postgres
    engineVersion: "14.7"
    instanceClass: db.t3.micro
    dbName: myappdb
    username: dbadmin
    passwordSecretRef:
      namespace: crossplane-system
      name: db-password
      key: password
    skipFinalSnapshot: true
    publiclyAccessible: false
    vpcSecurityGroupIdSelector:
      matchLabels:
        role: database
  providerConfigRef:
    name: default
  writeConnectionSecretToRef:
    namespace: production
    name: postgres-connection
```

## Composite Resource Definitions (XRDs)

### Database XRD

```yaml
# xrds/database-xrd.yaml
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xpostgresqlinstances.database.example.com
spec:
  group: database.example.com
  names:
    kind: XPostgreSQLInstance
    plural: xpostgresqlinstances
  claimNames:
    kind: PostgreSQLInstance
    plural: postgresqlinstances
  connectionSecretKeys:
    - username
    - password
    - endpoint
    - port
  versions:
    - name: v1alpha1
      served: true
      referenceable: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                parameters:
                  type: object
                  properties:
                    storageGB:
                      type: integer
                      description: Size of the database in GB
                      default: 20
                      minimum: 20
                      maximum: 1000
                    size:
                      type: string
                      description: Instance size (small, medium, large)
                      enum: [small, medium, large]
                      default: small
                    engineVersion:
                      type: string
                      description: PostgreSQL version
                      default: "14.7"
                    highAvailability:
                      type: boolean
                      description: Enable multi-AZ deployment
                      default: false
                    backupRetentionDays:
                      type: integer
                      description: Number of days to retain backups
                      default: 7
                      minimum: 1
                      maximum: 35
                    networkRef:
                      type: object
                      description: Reference to network configuration
                      properties:
                        id:
                          type: string
                          description: Network identifier
                      required:
                        - id
                  required:
                    - size
                    - networkRef
              required:
                - parameters
            status:
              type: object
              properties:
                address:
                  type: string
                  description: Database endpoint address
```

### Application Platform XRD

```yaml
# xrds/app-platform-xrd.yaml
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xappplatforms.platform.example.com
spec:
  group: platform.example.com
  names:
    kind: XAppPlatform
    plural: xappplatforms
  claimNames:
    kind: AppPlatform
    plural: appplatforms
  connectionSecretKeys:
    - bucket_name
    - database_endpoint
    - database_password
    - cache_endpoint
  versions:
    - name: v1alpha1
      served: true
      referenceable: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                parameters:
                  type: object
                  properties:
                    environment:
                      type: string
                      description: Environment (dev, staging, prod)
                      enum: [dev, staging, prod]
                    appName:
                      type: string
                      description: Application name
                      pattern: "^[a-z0-9-]+$"
                    region:
                      type: string
                      description: AWS region
                      default: us-west-2
                    databaseSize:
                      type: string
                      description: Database instance size
                      enum: [small, medium, large]
                      default: small
                    enableCache:
                      type: boolean
                      description: Enable Redis cache
                      default: false
                  required:
                    - environment
                    - appName
              required:
                - parameters
```

## Compositions

### Database Composition with Size Mapping

```yaml
# compositions/postgres-composition.yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: postgres.aws.database.example.com
  labels:
    provider: aws
    database: postgresql
spec:
  writeConnectionSecretsToNamespace: crossplane-system
  compositeTypeRef:
    apiVersion: database.example.com/v1alpha1
    kind: XPostgreSQLInstance

  resources:
    # Security Group for Database
    - name: database-sg
      base:
        apiVersion: ec2.aws.upbound.io/v1beta1
        kind: SecurityGroup
        spec:
          forProvider:
            description: Security group for PostgreSQL database
            tags:
              Name: database-sg
      patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.parameters.networkRef.id
          toFieldPath: spec.forProvider.vpcId
        - type: FromCompositeFieldPath
          fromFieldPath: metadata.labels[crossplane.io/claim-namespace]
          toFieldPath: spec.forProvider.tags.namespace
        - type: FromCompositeFieldPath
          fromFieldPath: metadata.labels[crossplane.io/claim-name]
          toFieldPath: spec.forProvider.tags.claim

    # Security Group Rule - Postgres Port
    - name: database-sg-rule
      base:
        apiVersion: ec2.aws.upbound.io/v1beta1
        kind: SecurityGroupRule
        spec:
          forProvider:
            type: ingress
            fromPort: 5432
            toPort: 5432
            protocol: tcp
            cidrBlocks:
              - 10.0.0.0/8
      patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.parameters.networkRef.id
          toFieldPath: spec.forProvider.vpcId
        - type: PatchSet
          patchSetName: security-group-id

    # RDS Subnet Group
    - name: subnet-group
      base:
        apiVersion: rds.aws.upbound.io/v1beta1
        kind: SubnetGroup
        spec:
          forProvider:
            description: Subnet group for database
      patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.parameters.networkRef.id
          toFieldPath: metadata.labels[network-id]
        - type: FromCompositeFieldPath
          fromFieldPath: metadata.uid
          toFieldPath: spec.forProvider.subnetIdSelector.matchLabels[subnet-group-id]

    # RDS Instance
    - name: rds-instance
      base:
        apiVersion: rds.aws.upbound.io/v1beta1
        kind: Instance
        spec:
          forProvider:
            engine: postgres
            skipFinalSnapshot: true
            publiclyAccessible: false
            username: dbadmin
            passwordSecretRef:
              namespace: crossplane-system
              key: password
            dbSubnetGroupNameSelector:
              matchControllerRef: true
            vpcSecurityGroupIdSelector:
              matchControllerRef: true
          writeConnectionSecretToRef:
            namespace: crossplane-system
      patches:
        # Instance size mapping
        - type: FromCompositeFieldPath
          fromFieldPath: spec.parameters.size
          toFieldPath: spec.forProvider.instanceClass
          transforms:
            - type: map
              map:
                small: db.t3.micro
                medium: db.t3.medium
                large: db.m5.large

        # Storage configuration
        - type: FromCompositeFieldPath
          fromFieldPath: spec.parameters.storageGB
          toFieldPath: spec.forProvider.allocatedStorage

        # Engine version
        - type: FromCompositeFieldPath
          fromFieldPath: spec.parameters.engineVersion
          toFieldPath: spec.forProvider.engineVersion

        # High availability
        - type: FromCompositeFieldPath
          fromFieldPath: spec.parameters.highAvailability
          toFieldPath: spec.forProvider.multiAz

        # Backup retention
        - type: FromCompositeFieldPath
          fromFieldPath: spec.parameters.backupRetentionDays
          toFieldPath: spec.forProvider.backupRetentionPeriod

        # Generate unique password secret name
        - type: FromCompositeFieldPath
          fromFieldPath: metadata.uid
          toFieldPath: spec.forProvider.passwordSecretRef.name
          transforms:
            - type: string
              string:
                fmt: "%s-password"

        # Connection secret name
        - type: FromCompositeFieldPath
          fromFieldPath: metadata.uid
          toFieldPath: spec.writeConnectionSecretToRef.name
          transforms:
            - type: string
              string:
                fmt: "%s-connection"

        # Expose endpoint to status
        - type: ToCompositeFieldPath
          fromFieldPath: status.atProvider.endpoint
          toFieldPath: status.address

        # Copy connection secret to claim namespace
        - type: FromCompositeFieldPath
          fromFieldPath: metadata.labels[crossplane.io/claim-namespace]
          toFieldPath: spec.writeConnectionSecretToRef.namespace
          policy:
            fromFieldPath: Optional

  patchSets:
    - name: security-group-id
      patches:
        - type: FromCompositeFieldPath
          fromFieldPath: metadata.labels[security-group-id]
          toFieldPath: spec.forProvider.securityGroupIdSelector.matchLabels[security-group-id]
```

### Multi-Resource Application Platform Composition

```yaml
# compositions/app-platform-composition.yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: appplatform.aws.platform.example.com
  labels:
    provider: aws
spec:
  writeConnectionSecretsToNamespace: crossplane-system
  compositeTypeRef:
    apiVersion: platform.example.com/v1alpha1
    kind: XAppPlatform

  resources:
    # S3 Bucket for application data
    - name: storage-bucket
      base:
        apiVersion: s3.aws.upbound.io/v1beta1
        kind: Bucket
        spec:
          forProvider:
            tags:
              ManagedBy: crossplane
          deletionPolicy: Delete
      patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.parameters.region
          toFieldPath: spec.forProvider.region
        - type: CombineFromComposite
          combine:
            variables:
              - fromFieldPath: spec.parameters.appName
              - fromFieldPath: spec.parameters.environment
            strategy: string
            string:
              fmt: "%s-%s-data"
          toFieldPath: metadata.name
        - type: ToCompositeFieldPath
          fromFieldPath: metadata.name
          toFieldPath: status.bucketName
        - type: FromCompositeFieldPath
          fromFieldPath: spec.parameters.environment
          toFieldPath: spec.forProvider.tags.Environment

    # S3 Bucket versioning
    - name: bucket-versioning
      base:
        apiVersion: s3.aws.upbound.io/v1beta1
        kind: BucketVersioning
        spec:
          forProvider:
            versioningConfiguration:
              status: Enabled
            bucketSelector:
              matchControllerRef: true
      patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.parameters.region
          toFieldPath: spec.forProvider.region

    # S3 Bucket encryption
    - name: bucket-encryption
      base:
        apiVersion: s3.aws.upbound.io/v1beta1
        kind: BucketServerSideEncryptionConfiguration
        spec:
          forProvider:
            rule:
              applyServerSideEncryptionByDefault:
                sseAlgorithm: AES256
            bucketSelector:
              matchControllerRef: true
      patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.parameters.region
          toFieldPath: spec.forProvider.region

    # PostgreSQL Database (using our XRD)
    - name: database
      base:
        apiVersion: database.example.com/v1alpha1
        kind: XPostgreSQLInstance
        spec:
          parameters:
            engineVersion: "14.7"
            storageGB: 20
            highAvailability: false
            backupRetentionDays: 7
            networkRef:
              id: vpc-12345
          compositionSelector:
            matchLabels:
              provider: aws
      patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.parameters.databaseSize
          toFieldPath: spec.parameters.size
        - type: FromCompositeFieldPath
          fromFieldPath: spec.parameters.environment
          toFieldPath: spec.parameters.highAvailability
          transforms:
            - type: map
              map:
                dev: false
                staging: false
                prod: true
        - type: FromCompositeFieldPath
          fromFieldPath: spec.parameters.environment
          toFieldPath: spec.parameters.backupRetentionDays
          transforms:
            - type: map
              map:
                dev: 1
                staging: 7
                prod: 30
        - type: ToCompositeFieldPath
          fromFieldPath: status.address
          toFieldPath: status.databaseEndpoint

    # ElastiCache Redis
    # Note: For truly conditional resources, use Composition Functions with
    # function-conditional or create separate compositions. This example
    # always provisions the cache when included in the composition.
    - name: cache
      base:
        apiVersion: elasticache.aws.upbound.io/v1beta1
        kind: ReplicationGroup
        spec:
          forProvider:
            description: Redis cache cluster
            engine: redis
            engineVersion: "7.0"
            nodeType: cache.t3.micro
            numCacheClusters: 1
            automaticFailoverEnabled: false
            atRestEncryptionEnabled: true
            transitEncryptionEnabled: true
            securityGroupIdSelector:
              matchControllerRef: true
            subnetGroupNameSelector:
              matchControllerRef: true
      patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.parameters.region
          toFieldPath: spec.forProvider.region
        - type: FromCompositeFieldPath
          fromFieldPath: spec.parameters.environment
          toFieldPath: spec.forProvider.automaticFailoverEnabled
          transforms:
            - type: map
              map:
                dev: false
                staging: false
                prod: true
        - type: FromCompositeFieldPath
          fromFieldPath: spec.parameters.environment
          toFieldPath: spec.forProvider.numCacheClusters
          transforms:
            - type: map
              map:
                dev: 1
                staging: 2
                prod: 3
        - type: ToCompositeFieldPath
          fromFieldPath: status.atProvider.primaryEndpointAddress
          toFieldPath: status.cacheEndpoint
```

## Claims (Self-Service Resources)

### Database Claim

```yaml
# claims/my-app-database.yaml
apiVersion: database.example.com/v1alpha1
kind: PostgreSQLInstance
metadata:
  name: my-app-db
  namespace: production
spec:
  parameters:
    size: medium
    storageGB: 100
    engineVersion: "14.7"
    highAvailability: true
    backupRetentionDays: 30
    networkRef:
      id: vpc-0a1b2c3d4e5f6g7h8
  compositionSelector:
    matchLabels:
      provider: aws
      database: postgresql
  writeConnectionSecretToRef:
    name: my-app-db-connection
```

### Application Platform Claim

```yaml
# claims/my-app-platform.yaml
apiVersion: platform.example.com/v1alpha1
kind: AppPlatform
metadata:
  name: my-application
  namespace: team-alpha
spec:
  parameters:
    environment: prod
    appName: my-app
    region: us-west-2
    databaseSize: large
    enableCache: true
  compositionSelector:
    matchLabels:
      provider: aws
  writeConnectionSecretToRef:
    name: my-app-platform-secrets
```

## Composition Functions

Composition Functions enable complex transformation logic using WebAssembly or container-based functions.

### Function Configuration

```yaml
# compositions/postgres-with-functions.yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: postgres.function-based.aws.database.example.com
spec:
  compositeTypeRef:
    apiVersion: database.example.com/v1alpha1
    kind: XPostgreSQLInstance

  mode: Pipeline
  pipeline:
    # Step 1: Use function to generate password
    - step: generate-password
      functionRef:
        name: function-auto-ready
      input:
        apiVersion: pt.fn.crossplane.io/v1beta1
        kind: Resources
        resources:
          - name: db-password-secret
            base:
              apiVersion: v1
              kind: Secret
              metadata:
                namespace: crossplane-system
              type: Opaque
              stringData:
                password: ""
            patches:
              - type: FromCompositeFieldPath
                fromFieldPath: metadata.uid
                toFieldPath: metadata.name
                transforms:
                  - type: string
                    string:
                      fmt: "%s-password"
              - type: CombineFromComposite
                combine:
                  variables:
                    - fromFieldPath: metadata.uid
                  strategy: string
                  string:
                    fmt: "GENERATE_PASSWORD_32"
                toFieldPath: stringData.password

    # Step 2: Patch and transform resources
    - step: patch-and-transform
      functionRef:
        name: function-patch-and-transform
      input:
        apiVersion: pt.fn.crossplane.io/v1beta1
        kind: Resources
        patchSets:
          - name: common-tags
            patches:
              - type: FromCompositeFieldPath
                fromFieldPath: metadata.labels[crossplane.io/claim-name]
                toFieldPath: spec.forProvider.tags.ClaimName
              - type: FromCompositeFieldPath
                fromFieldPath: metadata.labels[crossplane.io/claim-namespace]
                toFieldPath: spec.forProvider.tags.ClaimNamespace

        resources:
          - name: rds-instance
            base:
              apiVersion: rds.aws.upbound.io/v1beta1
              kind: Instance
              spec:
                forProvider:
                  engine: postgres
                  username: dbadmin
                  skipFinalSnapshot: true
            patches:
              - type: PatchSet
                patchSetName: common-tags
              - type: FromCompositeFieldPath
                fromFieldPath: spec.parameters.size
                toFieldPath: spec.forProvider.instanceClass
                transforms:
                  - type: map
                    map:
                      small: db.t3.micro
                      medium: db.t3.medium
                      large: db.m5.large

    # Step 3: Mark as ready
    - step: auto-ready
      functionRef:
        name: function-auto-ready
```

### Installing Composition Functions

```bash
# Install function-patch-and-transform
kubectl apply -f - <<EOF
apiVersion: pkg.crossplane.io/v1beta1
kind: Function
metadata:
  name: function-patch-and-transform
spec:
  package: xpkg.upbound.io/crossplane-contrib/function-patch-and-transform:v0.2.1
EOF

# Install function-auto-ready
kubectl apply -f - <<EOF
apiVersion: pkg.crossplane.io/v1beta1
kind: Function
metadata:
  name: function-auto-ready
spec:
  package: xpkg.upbound.io/crossplane-contrib/function-auto-ready:v0.2.1
EOF
```

## Best Practices

### Composition Patterns

#### Layered Abstraction Strategy

Build compositions in layers of increasing abstraction:

1. **Foundation Layer**: Provider-specific managed resources (S3, RDS, GCS)
2. **Resource Layer**: Cloud-agnostic XRDs (Database, ObjectStorage)
3. **Platform Layer**: Application-focused XRDs (AppPlatform, DataPlatform)

This enables teams to consume infrastructure at the right abstraction level.

#### Parallel Resource Creation

Crossplane automatically provisions resources in parallel when no dependencies exist. Optimize for this:

- Use selectors (matchControllerRef, matchLabels) instead of explicit refs
- Let Crossplane infer dependencies from resource relationships
- Avoid artificial ordering constraints

#### Transform Patterns

Common transform patterns for patches:

- **Size mapping**: map small/medium/large to instance types
- **Environment logic**: map dev/staging/prod to different configurations
- **String formatting**: CombineFromComposite with fmt for naming
- **Math operations**: multiply storage size by environment factor
- **Conditional values**: map boolean flags to provider-specific settings

#### Secret Aggregation

Merge connection secrets from multiple managed resources:

- Each managed resource writes to a unique secret
- Use connectionSecretKeys in XRD to define merged fields
- Crossplane automatically aggregates into composite secret
- Copy to claim namespace for application consumption

### Claim Design Patterns

#### Namespace Strategy

Choose a namespace model that fits your organization:

- **Per-team namespaces**: team-alpha, team-beta (good for multi-tenancy)
- **Per-environment namespaces**: dev, staging, prod (good for env isolation)
- **Hybrid approach**: team-alpha-prod, team-alpha-dev (maximum isolation)

Use RBAC to control which teams can create claims in which namespaces.

#### Self-Service Guardrails

Build guardrails into XRDs to prevent misconfiguration:

- Use enums to restrict choices (small/medium/large, not arbitrary values)
- Set min/max constraints on storage, replicas, retention periods
- Provide sensible defaults for optional parameters
- Use regex patterns for naming conventions
- Document expected values in field descriptions

#### Claim Lifecycle Management

Design claims for day-2 operations:

- Enable updates without replacement (use forProvider.applyMethod)
- Support scaling operations through parameter changes
- Include backup/restore configuration from day 1
- Plan for disaster recovery scenarios
- Document which parameters can be changed post-creation

#### Cost Visibility

Make cost implications visible to claim users:

- Add cost-related metadata to XRD descriptions
- Use labels for cost allocation (team, project, environment)
- Document size tiers with approximate costs
- Implement budget controls through validation webhooks
- Export cost tags to cloud provider billing

### Provider Configuration Strategies

#### Multi-Account Architecture

Use separate ProviderConfigs for different accounts/environments:

- Isolate prod from non-prod at the cloud account level
- Use IRSA (IAM Roles for Service Accounts) for AWS authentication
- Configure Workload Identity for GCP
- Implement Managed Identities for Azure

Reference the appropriate ProviderConfig in compositions or allow claims to specify it.

#### Credential Rotation

Implement secure credential management:

- Use external secret stores (Vault, AWS Secrets Manager)
- Configure ESO (External Secrets Operator) integration
- Rotate credentials on a schedule
- Use short-lived credentials when possible
- Avoid storing credentials in git

#### Provider Scoping

Install provider families strategically:

- Use scoped providers (provider-aws-s3) not monolithic (provider-aws)
- Reduces memory footprint and reconciliation load
- Install only required provider families
- Configure separate controller replicas for high-volume families
- Tune poll intervals per provider (--poll flag)

#### Rate Limiting

Configure provider controllers for production scale:

- Set --max-reconcile-rate based on API quotas
- Configure --poll interval to balance freshness vs load
- Use --enable-management-policies for granular control
- Monitor provider controller CPU/memory usage
- Scale controller replicas for high resource counts

### XRD Design

#### Keep XRDs Simple and Focused

- Each XRD should represent a single logical resource type
- Avoid combining unrelated infrastructure into one XRD
- Use composition to build complex platforms from simple XRDs

#### Version Your APIs

- Start with v1alpha1 and evolve to v1beta1, then v1
- Use multiple versions to support backwards compatibility
- Document breaking changes clearly

#### Define Clear Schemas

- Use OpenAPI validation (enums, patterns, min/max)
- Provide sensible defaults
- Mark required fields explicitly
- Add descriptions to all fields

#### Connection Secrets

- Only expose necessary connection details
- Use consistent key names across XRDs
- Document expected secret keys

### Composition Guidelines

#### Resource Naming

- Use deterministic names based on composite UID
- Avoid conflicts with CombineFromComposite patches
- Consider external name requirements

#### Patch Strategies

- Use PatchSets for common patches
- Apply FromCompositeFieldPath for user inputs
- Use ToCompositeFieldPath for status updates
- Leverage transforms (map, string formatting, math)

#### Resource Dependencies

- Use selectors (matchControllerRef, matchLabels) for references
- Crossplane handles dependency ordering automatically
- Avoid circular dependencies

#### Environment-Specific Logic

- Use map transforms to vary resources by environment
- Example: small instances for dev, large for prod
- Conditional resources based on boolean flags

#### Connection Secret Propagation

- Write secrets to crossplane-system namespace first
- Copy to claim namespace using patches
- Merge secrets from multiple resources

### Claim Organization

#### Namespace Strategy

- One namespace per team or environment
- Use RBAC to control claim creation
- Claims are namespace-scoped, XRs are cluster-scoped

#### Naming Conventions

- Use descriptive claim names (app-name-db, not db-1)
- Include environment in name if not using namespace separation
- Follow organization naming standards

#### Labels and Annotations

- Add ownership labels (team, cost-center)
- Use annotations for metadata (jira-ticket, owner-email)
- Labels can be used in composition patches

### ProviderConfig Best Practices

#### Multiple Provider Configs

- Use different ProviderConfigs for different accounts/projects
- Name them descriptively (prod-aws, dev-aws)
- Reference explicitly in compositions or claims

#### Credential Management

- Use IRSA (IAM Roles for Service Accounts) when possible
- Store credentials in secrets with minimal permissions
- Rotate credentials regularly

#### Resource Limits

- Configure provider controller resource limits
- Set appropriate poll intervals (--poll flag)
- Limit max reconcile rate for large deployments

### Production Readiness

#### Deletion Policies

- Use `deletionPolicy: Delete` for dev environments
- Use `deletionPolicy: Orphan` for production databases
- Document deletion behavior for platform users

#### Resource Tagging

- Tag all resources with ManagedBy: crossplane
- Include environment, team, and cost allocation tags
- Propagate tags from composite to managed resources

#### Monitoring and Observability

- Monitor Crossplane controller metrics
- Set up alerts for failed reconciliations
- Export provider metrics to your monitoring system
- Check resource sync status regularly

#### Testing

- Test compositions in dev before promoting to prod
- Validate XRDs with kube-linter or similar tools
- Use dry-run mode for risky changes

#### Documentation

- Document XRD schemas with examples
- Provide claim templates for platform users
- Maintain composition change logs

#### Security

- Use least-privilege IAM policies
- Enable encryption at rest and in transit
- Use private endpoints where possible
- Implement network security groups/firewalls

## Common Operations

### Debugging

```bash
# Check Crossplane status
kubectl get crossplane

# View provider status
kubectl get providers

# Check managed resources
kubectl get managed

# View composite resources
kubectl get composite

# Describe a claim to see events
kubectl describe postgresqlinstance my-app-db -n production

# View composition functions
kubectl get functions

# Check provider logs
kubectl logs -n crossplane-system -l pkg.crossplane.io/provider=provider-aws-s3

# Get all resources created by a composition
kubectl get managed -l crossplane.io/composite=<composite-name>
```

### Troubleshooting

```bash
# Check if provider is healthy
kubectl get providers
kubectl describe provider provider-aws-s3

# Verify ProviderConfig
kubectl get providerconfigs
kubectl describe providerconfig default

# Check for reconciliation errors
kubectl describe <resource-type> <resource-name>

# View conditions
kubectl get <resource> <name> -o jsonpath='{.status.conditions}'

# Test claim creation
kubectl apply -f claim.yaml --dry-run=server

# Validate XRD
kubectl apply -f xrd.yaml --dry-run=server
```

### Updating Resources

```bash
# Update a composition (changes apply to new composites only)
kubectl apply -f composition.yaml

# Force reconciliation by adding annotation
kubectl annotate claim my-app-db crossplane.io/paused=false --overwrite

# Update XRD (be careful with breaking changes)
kubectl apply -f xrd.yaml

# Upgrade provider
kubectl apply -f provider.yaml  # with new version
```

## Advanced Patterns

### Multi-Region Deployments

```yaml
# Create multiple compositions, one per region
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: postgres.us-west-2.aws.database.example.com
  labels:
    provider: aws
    region: us-west-2
spec:
  compositeTypeRef:
    apiVersion: database.example.com/v1alpha1
    kind: XPostgreSQLInstance
  # ... resources configured for us-west-2
---
# Claim with region selector
apiVersion: database.example.com/v1alpha1
kind: PostgreSQLInstance
metadata:
  name: my-db
spec:
  compositionSelector:
    matchLabels:
      region: us-west-2
```

### Blue-Green Deployments

```yaml
# Use labels to manage active/inactive compositions
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: app-v2
  labels:
    version: v2
    active: "true"
spec:
  # ... new composition
---
# Claim selects active version
spec:
  compositionSelector:
    matchLabels:
      active: "true"
```

### Conditional Resource Creation

Use Composition Functions to conditionally include resources based on input parameters:

```yaml
# compositions/conditional-cache-composition.yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: appplatform-with-conditional-cache
spec:
  compositeTypeRef:
    apiVersion: platform.example.com/v1alpha1
    kind: XAppPlatform

  mode: Pipeline
  pipeline:
    # Step 1: Create base resources
    - step: create-resources
      functionRef:
        name: function-patch-and-transform
      input:
        apiVersion: pt.fn.crossplane.io/v1beta1
        kind: Resources
        resources:
          - name: storage-bucket
            base:
              apiVersion: s3.aws.upbound.io/v1beta1
              kind: Bucket
              spec:
                forProvider:
                  region: us-west-2

    # Step 2: Conditionally add cache using function-kcl or function-go-templating
    - step: add-cache-if-enabled
      functionRef:
        name: function-go-templating
      input:
        apiVersion: gotemplating.fn.crossplane.io/v1beta1
        kind: GoTemplate
        source: Inline
        inline:
          template: |
            {{ if .observed.composite.resource.spec.parameters.enableCache }}
            apiVersion: elasticache.aws.upbound.io/v1beta1
            kind: ReplicationGroup
            metadata:
              name: {{ .observed.composite.resource.metadata.name }}-cache
              annotations:
                gotemplating.fn.crossplane.io/composition-resource-name: cache
            spec:
              forProvider:
                description: Redis cache
                engine: redis
                engineVersion: "7.0"
                nodeType: cache.t3.micro
                numCacheClusters: 1
            {{ end }}

    # Step 3: Mark resources ready
    - step: auto-ready
      functionRef:
        name: function-auto-ready
```

Alternative approach using separate compositions:

```yaml
# Create two compositions: one with cache, one without
# composition-with-cache.yaml
metadata:
  labels:
    cache: enabled
# ... includes cache resources

# composition-without-cache.yaml
metadata:
  labels:
    cache: disabled
# ... excludes cache resources

# Claim selects the appropriate composition
spec:
  compositionSelector:
    matchLabels:
      cache: enabled  # or disabled
```

### Cost Optimization

```yaml
# Use environment-based sizing
patches:
  - type: FromCompositeFieldPath
    fromFieldPath: spec.parameters.environment
    toFieldPath: spec.forProvider.instanceClass
    transforms:
      - type: map
        map:
          dev: db.t3.micro # $0.017/hour
          staging: db.t3.small # $0.034/hour
          prod: db.m5.large # $0.192/hour
```

## Migration Strategies

### Importing Existing Resources

```yaml
# Import existing infrastructure
apiVersion: s3.aws.upbound.io/v1beta1
kind: Bucket
metadata:
  name: existing-bucket
  annotations:
    crossplane.io/external-name: my-existing-bucket-name
spec:
  forProvider:
    region: us-west-2
  providerConfigRef:
    name: default
  # Crossplane will discover and manage this existing bucket
```

### Migrating from Terraform

1. Export Terraform state for resources
2. Create equivalent managed resources with matching external names
3. Import into Crossplane using external-name annotation
4. Gradually build compositions around managed resources
5. Migrate teams to claims

## References

- [Crossplane Documentation](https://docs.crossplane.io)
- [Upbound Providers](https://marketplace.upbound.io)
- [Composition Functions](https://docs.crossplane.io/latest/concepts/composition-functions)
- [AWS Provider](https://marketplace.upbound.io/providers/upbound/provider-aws)
- [GCP Provider](https://marketplace.upbound.io/providers/upbound/provider-gcp)
- [Azure Provider](https://marketplace.upbound.io/providers/upbound/provider-azure)

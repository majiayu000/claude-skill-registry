---
name: crossplane
description: >-
  Crossplane for infrastructure as code using Kubernetes CRDs. Use when the user
  needs to provision and manage cloud resources declaratively through Kubernetes
  APIs, compose custom infrastructure abstractions, or build internal platforms.
license: Apache-2.0
compatibility: 'linux, macos'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: devops
  tags:
    - crossplane
    - kubernetes
    - infrastructure-as-code
    - cloud
    - platform-engineering
---

# Crossplane

Crossplane extends Kubernetes to provision and manage cloud infrastructure using Custom Resource Definitions (CRDs).

## Installation

```bash
# Install Crossplane with Helm
helm repo add crossplane-stable https://charts.crossplane.io/stable
helm repo update

helm install crossplane crossplane-stable/crossplane \
  --namespace crossplane-system \
  --create-namespace

# Verify installation
kubectl get pods -n crossplane-system
kubectl api-resources | grep crossplane
```

## AWS Provider

```yaml
# providers/aws-provider.yaml — Install AWS provider
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-aws
spec:
  package: xpkg.upbound.io/upbound/provider-aws-ec2:v1.1.0
---
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-aws-s3
spec:
  package: xpkg.upbound.io/upbound/provider-aws-s3:v1.1.0
---
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-aws-rds
spec:
  package: xpkg.upbound.io/upbound/provider-aws-rds:v1.1.0
```

```yaml
# providers/aws-config.yaml — AWS provider credentials configuration
apiVersion: v1
kind: Secret
metadata:
  name: aws-creds
  namespace: crossplane-system
type: Opaque
stringData:
  credentials: |
    [default]
    aws_access_key_id = AKIA...
    aws_secret_access_key = ...
---
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
      key: credentials
```

## Managed Resources

```yaml
# resources/s3-bucket.yaml — Provision S3 bucket via Crossplane
apiVersion: s3.aws.upbound.io/v1beta1
kind: Bucket
metadata:
  name: my-app-data
spec:
  forProvider:
    region: us-east-1
    tags:
      Environment: production
      ManagedBy: crossplane
  providerConfigRef:
    name: default
---
apiVersion: s3.aws.upbound.io/v1beta1
kind: BucketVersioning
metadata:
  name: my-app-data-versioning
spec:
  forProvider:
    region: us-east-1
    bucketRef:
      name: my-app-data
    versioningConfiguration:
      - status: Enabled
```

```yaml
# resources/rds-instance.yaml — Provision RDS PostgreSQL via Crossplane
apiVersion: rds.aws.upbound.io/v1beta1
kind: Instance
metadata:
  name: production-db
spec:
  forProvider:
    region: us-east-1
    engine: postgres
    engineVersion: "15"
    instanceClass: db.t3.medium
    allocatedStorage: 100
    storageType: gp3
    storageEncrypted: true
    dbName: appdb
    username: admin
    passwordSecretRef:
      name: db-password
      namespace: default
      key: password
    multiAz: true
    backupRetentionPeriod: 7
    skipFinalSnapshot: false
  writeConnectionSecretToRef:
    name: production-db-conn
    namespace: default
```

## Compositions

```yaml
# compositions/database-definition.yaml — XRD for database abstraction
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xdatabases.platform.example.com
spec:
  group: platform.example.com
  names:
    kind: XDatabase
    plural: xdatabases
  claimNames:
    kind: Database
    plural: databases
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
                size:
                  type: string
                  enum: ["small", "medium", "large"]
                engine:
                  type: string
                  enum: ["postgres", "mysql"]
                  default: postgres
              required:
                - size
```

```yaml
# compositions/database-composition.yaml — Compose RDS from XDatabase claim
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: database-aws
  labels:
    provider: aws
spec:
  compositeTypeRef:
    apiVersion: platform.example.com/v1alpha1
    kind: XDatabase
  resources:
    - name: rds-instance
      base:
        apiVersion: rds.aws.upbound.io/v1beta1
        kind: Instance
        spec:
          forProvider:
            region: us-east-1
            engine: postgres
            storageEncrypted: true
            skipFinalSnapshot: false
      patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.size
          toFieldPath: spec.forProvider.instanceClass
          transforms:
            - type: map
              map:
                small: db.t3.micro
                medium: db.t3.medium
                large: db.r6g.large
        - type: FromCompositeFieldPath
          fromFieldPath: spec.engine
          toFieldPath: spec.forProvider.engine
```

## Claims

```yaml
# claims/my-database.yaml — Developer claims a database through platform API
apiVersion: platform.example.com/v1alpha1
kind: Database
metadata:
  name: orders-db
  namespace: team-a
spec:
  size: medium
  engine: postgres
  compositionSelector:
    matchLabels:
      provider: aws
```

## GCP Provider

```yaml
# providers/gcp-provider.yaml — Install and configure GCP provider
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-gcp
spec:
  package: xpkg.upbound.io/upbound/provider-gcp-storage:v1.0.0
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
      key: credentials.json
```

## Common Commands

```bash
# Check providers
kubectl get providers
kubectl get providerconfigs

# Check managed resources
kubectl get managed
kubectl describe bucket my-app-data

# Check compositions
kubectl get compositions
kubectl get compositeresourcedefinitions
kubectl get composite
kubectl get claim --all-namespaces

# Debug
kubectl get events --field-selector involvedObject.name=my-app-data
crossplane beta trace database orders-db -n team-a
```

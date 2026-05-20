# 🔀 Skill: Crossplane Multi-Cloud Management

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `cicd-crossplane` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `crossplane`, `multi-cloud`, `kubernetes`, `infrastructure` |

## 🔑 Keywords

- `crossplane`, `multi-cloud`, `k8s-native`, `infrastructure-api`, `@skill:crossplane`

## 📖 Descripción

Crossplane extiende Kubernetes para gestionar infraestructura cloud usando custom resources. Permite provisioning declarativo multi-cloud para backends Flutter usando APIs de Kubernetes.

## 💻 Implementación

### 1. Install Crossplane

```bash
# Install Crossplane
helm repo add crossplane-stable https://charts.crossplane.io/stable
helm repo update

helm install crossplane \
  crossplane-stable/crossplane \
  --namespace crossplane-system \
  --create-namespace

# Verify installation
kubectl get pods -n crossplane-system
```

### 2. Install Provider (AWS Example)

```yaml
# aws-provider.yaml
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-aws
spec:
  package: xpkg.upbound.io/upbound/provider-aws:v0.40.0
```

```bash
kubectl apply -f aws-provider.yaml

# Configure AWS credentials
kubectl create secret generic aws-creds \
  -n crossplane-system \
  --from-file=credentials=./aws-credentials.txt

# Create ProviderConfig
kubectl apply -f - <<EOF
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
EOF
```

### 3. Provision RDS Database

```yaml
# rds-instance.yaml
apiVersion: rds.aws.upbound.io/v1beta1
kind: Instance
metadata:
  name: myapp-postgres
spec:
  forProvider:
    region: us-east-1
    dbInstanceClass: db.t3.micro
    engine: postgres
    engineVersion: "15.4"
    allocatedStorage: 20
    storageType: gp3
    storageEncrypted: true
    username: admin
    passwordSecretRef:
      name: db-password
      namespace: default
      key: password
    multiAz: true
    backupRetentionPeriod: 7
    skipFinalSnapshot: false
  providerConfigRef:
    name: default
```

### 4. Provision S3 Bucket

```yaml
# s3-bucket.yaml
apiVersion: s3.aws.upbound.io/v1beta1
kind: Bucket
metadata:
  name: myapp-storage-prod
spec:
  forProvider:
    region: us-east-1
    versioning:
      - enabled: true
    serverSideEncryptionConfiguration:
      - rule:
          - applyServerSideEncryptionByDefault:
              - sseAlgorithm: AES256
  providerConfigRef:
    name: default
```

### 5. Composite Resource Definition (XRD)

```yaml
# backend-xrd.yaml
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xbackends.myapp.io
spec:
  group: myapp.io
  names:
    kind: XBackend
    plural: xbackends
  claimNames:
    kind: Backend
    plural: backends
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
                    enum: [dev, staging, production]
                  dbSize:
                    type: string
                    enum: [small, medium, large]
                  storageSize:
                    type: integer
                required:
                - environment
                - dbSize
```

### 6. Composition

```yaml
# backend-composition.yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: backend-aws
spec:
  compositeTypeRef:
    apiVersion: myapp.io/v1alpha1
    kind: XBackend

  resources:
  - name: database
    base:
      apiVersion: rds.aws.upbound.io/v1beta1
      kind: Instance
      spec:
        forProvider:
          region: us-east-1
          engine: postgres
          engineVersion: "15.4"
    patches:
    - fromFieldPath: spec.parameters.dbSize
      toFieldPath: spec.forProvider.dbInstanceClass
      transforms:
      - type: map
        map:
          small: db.t3.micro
          medium: db.t3.small
          large: db.t3.medium

  - name: storage
    base:
      apiVersion: s3.aws.upbound.io/v1beta1
      kind: Bucket
      spec:
        forProvider:
          region: us-east-1
    patches:
    - fromFieldPath: spec.parameters.environment
      toFieldPath: metadata.labels.environment
```

### 7. Claim Backend Resources

```yaml
# backend-claim.yaml
apiVersion: myapp.io/v1alpha1
kind: Backend
metadata:
  name: myapp-production
  namespace: default
spec:
  parameters:
    environment: production
    dbSize: large
    storageSize: 100
  compositionSelector:
    matchLabels:
      provider: aws
```

### 8. Multi-Cloud Support

```yaml
# Install multiple providers
---
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-aws
spec:
  package: xpkg.upbound.io/upbound/provider-aws:v0.40.0
---
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-gcp
spec:
  package: xpkg.upbound.io/upbound/provider-gcp:v0.40.0
---
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-azure
spec:
  package: xpkg.upbound.io/upbound/provider-azure:v0.40.0
```

## 🎯 Mejores Prácticas

1. **Use Compositions** para abstraer cloud providers
2. **XRDs** para APIs consistentes
3. **GitOps** con ArgoCD para gestión
4. **RBAC** para control de acceso
5. **Policy** con OPA para governance
6. **Observability** con Prometheus
7. **Multi-tenancy** con namespaces

## 📚 Recursos

- [Crossplane Documentation](https://docs.crossplane.io/)
- [Crossplane Providers](https://marketplace.upbound.io/)

---

**Versión:** 1.0.0

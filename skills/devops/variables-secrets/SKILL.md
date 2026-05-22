---
name: gitlab-ci-variables-secrets
description: Use when configuring GitLab CI/CD variables, managing secrets, or integrating with external secret providers. Covers secure credential handling.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# GitLab CI - Variables & Secrets

Configure CI/CD variables and manage secrets securely in GitLab pipelines.

## Variable Types

### Predefined Variables

```yaml
build:
  script:
    - echo "Branch: $CI_COMMIT_BRANCH"
    - echo "Commit: $CI_COMMIT_SHA"
    - echo "Pipeline: $CI_PIPELINE_ID"
    - echo "Project: $CI_PROJECT_NAME"
    - echo "Registry: $CI_REGISTRY_IMAGE"
```

### Custom Variables

```yaml
variables:
  NODE_ENV: production
  DATABASE_URL: "postgres://localhost/app"

build:
  variables:
    BUILD_TARGET: dist
  script:
    - npm run build --target=$BUILD_TARGET
```

## Variable Scopes

### Global Variables

```yaml
variables:
  GLOBAL_VAR: "available everywhere"
```

### Job-Level Variables

```yaml
deploy:
  variables:
    DEPLOY_ENV: production
  script:
    - ./deploy.sh $DEPLOY_ENV
```

### Environment-Scoped Variables

Configure in GitLab UI: Settings > CI/CD > Variables

- Scope to specific environments (production, staging)
- Scope to specific branches (main, develop)

## Protected and Masked Variables

### In gitlab-ci.yml

```yaml
variables:
  PUBLIC_KEY:
    value: "pk_test_xxx"
    description: "Stripe public key"
```

### In GitLab UI

Set variables with:

- **Protected**: Only available on protected branches/tags
- **Masked**: Hidden in job logs (requires specific format)
- **Expanded**: Allow variable references within value

## File-Type Variables

```yaml
deploy:
  script:
    - cat $KUBECONFIG  # File variable contents
    - kubectl apply -f deployment.yaml
```

## External Secret Providers

### HashiCorp Vault

```yaml
job:
  secrets:
    DATABASE_PASSWORD:
      vault:
        engine:
          name: kv-v2
          path: secret
        field: password
        path: production/db
```

### Azure Key Vault

```yaml
job:
  secrets:
    API_KEY:
      azure_key_vault:
        name: my-api-key
        version: latest
```

### AWS Secrets Manager

```yaml
job:
  secrets:
    AWS_SECRET:
      aws_secrets_manager:
        name: prod/api-key
        version_id: latest
```

## OIDC Authentication

```yaml
deploy:aws:
  id_tokens:
    AWS_TOKEN:
      aud: https://gitlab.com
  script:
    - >
      aws sts assume-role-with-web-identity
      --role-arn $AWS_ROLE_ARN
      --web-identity-token $AWS_TOKEN
```

## Best Practices

1. Never hardcode secrets in `.gitlab-ci.yml`
2. Use protected variables for production credentials
3. Mask sensitive values to prevent log exposure
4. Prefer OIDC over long-lived credentials
5. Scope variables to minimum required environments
6. Use file-type variables for certificates and keys

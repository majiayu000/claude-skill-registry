<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: implementing-secrets-rotation-automation
description: >-
  Automate credential rotation for API keys, database passwords, and service
  accounts using HashiCorp Vault, AWS Secrets Manager, and CI/CD pipelines.
  Implement zero-downtime rotation with health checks.
domain: cybersecurity
subdomain: devsecops
tags:
  - secrets-management
  - vault
  - aws-secrets-manager
  - rotation
  - credential-management
  - zero-downtime
  - automation
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1552"]
---

# Implementing Secrets Rotation Automation

## Overview

Automated secrets rotation reduces the window of exposure for compromised credentials
by regularly cycling API keys, database passwords, and service account tokens. This
skill covers implementing rotation workflows with HashiCorp Vault, AWS Secrets Manager,
and custom rotation Lambda functions with zero-downtime deployment patterns.

Mode: `[MODE: BLUE]` — Credential lifecycle management through automated rotation.

## Prerequisites

| Requirement | Details |
|---|---|
| HashiCorp Vault or AWS Secrets Manager | Required |
| CI/CD pipeline with secrets access | Required |
| Database admin credentials for password rotation | Required |
| Service mesh or configuration reload mechanism | Required |

## Key Concepts

### Vault Dynamic Database Credentials

```hcl
# vault/database.hcl
resource "vault_database_secret_backend" "postgres" {
  path = "database"

  postgresql {
    name              = "production"
    connection_url    = "postgresql://{{username}}:{{password}}@db.internal:5432/app"
    allowed_roles     = ["app-role"]
    root_rotation_statements = [
      "ALTER USER {{name}} WITH PASSWORD '{{password}}';"
    ]
  }
}

resource "vault_database_secret_backend_role" "app_role" {
  backend     = vault_database_secret_backend.postgres.path
  name        = "app-role"
  db_name     = "production"
  default_ttl = 3600    # 1 hour
  max_ttl     = 86400   # 24 hours

  creation_statements = [
    "CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}';",
    "GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO \"{{name}}\";"
  ]

  revocation_statements = [
    "REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM \"{{name}}\";",
    "DROP ROLE IF EXISTS \"{{name}}\";"
  ]
}
```

### AWS Secrets Manager Rotation Lambda

```python
# rotation_lambda.py
import boto3
import json
import psycopg2
import secrets
import string

def lambda_handler(event, context):
    """Rotate database password in AWS Secrets Manager."""
    secret_id = event['SecretId']
    step = event['Step']
    token = event['ClientRequestToken']

    sm = boto3.client('secretsmanager')

    if step == 'createSecret':
        current = json.loads(
            sm.get_secret_value(SecretId=secret_id)['SecretString']
        )
        new_password = ''.join(
            secrets.choice(string.ascii_letters + string.digits + '!@#$%')
            for _ in range(32)
        )
        current['password'] = new_password
        sm.put_secret_value(
            SecretId=secret_id,
            ClientRequestToken=token,
            SecretString=json.dumps(current),
            VersionStages=['AWSPENDING'],
        )

    elif step == 'setSecret':
        pending = json.loads(
            sm.get_secret_value(
                SecretId=secret_id, VersionStage='AWSPENDING'
            )['SecretString']
        )
        conn = psycopg2.connect(
            host=pending['host'], port=pending['port'],
            user='admin', password=pending['admin_password'],
            dbname=pending['dbname'],
        )
        with conn.cursor() as cur:
            cur.execute(
                "ALTER USER %s WITH PASSWORD %s",
                (pending['username'], pending['password']),
            )
        conn.commit()
        conn.close()

    elif step == 'testSecret':
        pending = json.loads(
            sm.get_secret_value(
                SecretId=secret_id, VersionStage='AWSPENDING'
            )['SecretString']
        )
        conn = psycopg2.connect(
            host=pending['host'], port=pending['port'],
            user=pending['username'], password=pending['password'],
            dbname=pending['dbname'],
        )
        conn.close()

    elif step == 'finishSecret':
        sm.update_secret_version_stage(
            SecretId=secret_id,
            VersionStage='AWSCURRENT',
            MoveToVersionId=token,
            RemoveFromVersionId=_get_current_version(sm, secret_id),
        )


def _get_current_version(sm, secret_id):
    metadata = sm.describe_secret(SecretId=secret_id)
    for version_id, stages in metadata['VersionIdsToStages'].items():
        if 'AWSCURRENT' in stages:
            return version_id
    return None
```

### GitHub Actions Rotation Workflow

```yaml
name: Rotate API Keys
on:
  schedule:
    - cron: '0 0 1 * *'  # Monthly
  workflow_dispatch:

jobs:
  rotate:
    runs-on: ubuntu-latest
    steps:
      - name: Generate new API key
        id: generate
        run: |
          NEW_KEY=$(openssl rand -hex 32)
          echo "::add-mask::$NEW_KEY"
          echo "new_key=$NEW_KEY" >> $GITHUB_OUTPUT
      - name: Update secret in Vault
        env:
          VAULT_ADDR: ${{ secrets.VAULT_ADDR }}
          VAULT_TOKEN: ${{ secrets.VAULT_TOKEN }}
        run: |
          vault kv put secret/api-keys/service-a key=${{ steps.generate.outputs.new_key }}
      - name: Verify new key works
        run: |
          curl -sf -H "X-API-Key: ${{ steps.generate.outputs.new_key }}" \
            https://api.internal/healthz
      - name: Trigger rolling restart
        run: |
          kubectl rollout restart deployment/service-a -n production
          kubectl rollout status deployment/service-a -n production --timeout=300s
```

## Workflow

### Step 1: Audit Current Secrets

```bash
node scripts/agent.js --action audit --vault-addr http://127.0.0.1:8200 --output /tmp/secrets-audit.json
```

### Step 2: Check Rotation Status

```bash
node scripts/agent.js --action status --output /tmp/rotation-status.json
```

### Step 3: Trigger Rotation

```bash
node scripts/agent.js --action rotate --secret-id db/production --output /tmp/rotation-result.json
```

## Detection

```yaml
title: Secrets Rotation Automation Detection
id: d3f3d3cc-6d73-44e1-8ea4-3ca63bdf9764
status: experimental
description: Detects suspicious activity related to implementing secrets rotation automation techniques in devsecops context
logsource:
  category: process_creation
  product: linux
detection:
  selection:
    CommandLine: "*implementing*secrets*"
  condition: selection
level: medium
tags:
  - attack.t1552
  - attack.execution
falsepositives:
  - CI/CD pipeline executing authorized security scanning tools
```


**Detection Opportunities**

| Indicator | Source | Detection Logic |
|---|---|---|
| Secrets Rotation Automation Detection | linux/process_creation | Sigma rule (medium) |
| ATT&CK Coverage | MITRE ATT&CK | T1552 |

## Verification

- [ ] All production secrets have rotation schedules
- [ ] Rotation tested in staging before production
- [ ] Zero-downtime rotation verified with health checks
- [ ] Rotation failures alert on-call team
- [ ] Secret TTLs enforced (max 90 days for static, 1 hour for dynamic)
- [ ] Rotation audit trail maintained

## References

- [HashiCorp Vault Dynamic Secrets](https://developer.hashicorp.com/vault/docs/secrets/databases)
- [AWS Secrets Manager Rotation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html)
- [NIST 800-63B — Credential Management](https://pages.nist.gov/800-63-3/sp800-63b.html)

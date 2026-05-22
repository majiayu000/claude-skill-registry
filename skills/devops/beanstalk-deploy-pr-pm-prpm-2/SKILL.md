---
name: beanstalk-deploy
description: "Robust deployment patterns for Elastic Beanstalk with GitHub Actions, Pulumi, and edge case handling"
---

# AWS Elastic Beanstalk Deployment Best Practices

Apply these production-tested patterns when working with Elastic Beanstalk deployments, especially with GitHub Actions and Pulumi infrastructure.

## 🎯 Core Principles

1. **Always verify infrastructure health** before deploying
2. **Never assume resources are ready** - implement retry logic
3. **Handle terminated environments** gracefully with state cleanup
4. **Use concurrency control** to prevent deployment conflicts
5. **Pre-install dependencies** for faster, more reliable deploys
6. **Implement comprehensive error handling** with fallbacks

## 🏗️ Infrastructure Health Checks

**ALWAYS check infrastructure status before deploying:**

```yaml
- name: Check infrastructure status
  run: |
    echo "🔍 Checking infrastructure status..."

    # Get environment name from Pulumi state (without deploying)
    EB_ENVIRONMENT_NAME=$(pulumi stack output ebEnvironmentName 2>/dev/null || echo "")

    if [ -z "$EB_ENVIRONMENT_NAME" ]; then
      echo "🔍 No environment found in Pulumi state. Will deploy infrastructure..."
    else
      echo "🔍 Checking environment status: $EB_ENVIRONMENT_NAME"

      # Check if environment exists and is healthy
      EB_ENV_STATUS=$(aws elasticbeanstalk describe-environments \
        --environment-names "$EB_ENVIRONMENT_NAME" \
        --query "Environments[0].Status" --output text 2>/dev/null || echo "NOT_FOUND")

      if [ "$EB_ENV_STATUS" = "Terminated" ] || [ "$EB_ENV_STATUS" = "NOT_FOUND" ]; then
        echo "⚠️  Environment is $EB_ENV_STATUS. Deleting from Pulumi state..."

        # Delete environment from Pulumi state
        EB_URN=$(pulumi stack --show-urns | awk '/aws:elasticbeanstalk\/environment:Environment/ {print $1; exit}')
        if [ -n "$EB_URN" ]; then
          echo "🔧 Deleting: $EB_URN"
          pulumi state delete "$EB_URN" --force
        fi

        echo "🔄 Infrastructure will be recreated..."
      else
        echo "✅ Environment exists: $EB_ENV_STATUS"

        # Check if infrastructure changes needed
        if pulumi preview --diff --expect-no-changes 2>/dev/null; then
          echo "✅ No infrastructure changes needed"
        else
          echo "🔄 Infrastructure changes detected"
        fi
      fi
    fi
```

**Why**: Prevents deploying to orphaned resources, automatically recovers from terminated environments, saves money on zombie resources.

## ⏳ Beanstalk Readiness Verification

**ALWAYS wait for environment to be fully ready:**

```yaml
- name: Verify Elastic Beanstalk environment exists
  run: |
    echo "🔍 Verifying Elastic Beanstalk environment..."
    EB_ENVIRONMENT_NAME="${{ steps.get-resources.outputs.eb_environment_name }}"

    # Wait until environment exists
    echo "⏳ Waiting for environment to exist..."
    aws elasticbeanstalk wait environment-exists \
      --environment-names "$EB_ENVIRONMENT_NAME" || true

    # Wait until environment is Ready (with 30 retries)
    for i in {1..30}; do
      ENV_STATUS=$(aws elasticbeanstalk describe-environments \
        --environment-names "$EB_ENVIRONMENT_NAME" \
        --query "Environments[0].Status" --output text 2>/dev/null || echo "NOT_FOUND")
      ENV_HEALTH=$(aws elasticbeanstalk describe-environments \
        --environment-names "$EB_ENVIRONMENT_NAME" \
        --query "Environments[0].Health" --output text 2>/dev/null || echo "UNKNOWN")

      echo "⏳ EB Status: $ENV_STATUS, Health: $ENV_HEALTH (attempt $i/30)"

      if [ "$ENV_STATUS" = "Ready" ]; then
        echo "✅ Environment is Ready"
        break
      fi
      sleep 20  # Wait 20 seconds between checks (10 minutes total)
    done

    if [ "$ENV_STATUS" != "Ready" ]; then
      echo "⚠️  Environment not Ready after 10 minutes. Continuing with caution..."
    fi
```

**Why**: Prevents timing-related failures, ensures environment is provisioned before app deployment, provides visibility into provisioning progress.

See full documentation for complete deployment patterns, Pulumi configuration, monitoring, and production checklist.
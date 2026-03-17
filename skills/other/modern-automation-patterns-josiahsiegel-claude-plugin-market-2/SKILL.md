---
name: modern-automation-patterns
description: Modern DevOps and CI/CD automation patterns with containers and cloud (2025)
---

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems


### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation


---

# Modern Automation Patterns (2025)

## Overview

Production-ready patterns for DevOps automation, CI/CD pipelines, and cloud-native operations following 2025 industry standards.

## Container-Aware Scripting

### Docker/Kubernetes Detection

```bash
#!/usr/bin/env bash
set -euo pipefail

# Detect container environment
detect_container() {
    if [[ -f /.dockerenv ]]; then
        echo "docker"
    elif grep -q docker /proc/1/cgroup 2>/dev/null; then
        echo "docker"
    elif [[ -n "${KUBERNETES_SERVICE_HOST:-}" ]]; then
        echo "kubernetes"
    else
        echo "host"
    fi
}

# Container-aware configuration
readonly CONTAINER_ENV=$(detect_container)

case "$CONTAINER_ENV" in
    docker|kubernetes)
        # Container-specific paths
        DATA_DIR="/data"
        CONFIG_DIR="/config"
        ;;
    host)
        # Host-specific paths
        DATA_DIR="/var/lib/app"
        CONFIG_DIR="/etc/app"
        ;;
esac
```

### Minimal Container Scripts

```bash
#!/bin/sh
# Use /bin/sh for Alpine-based containers (no bash)

set -eu  # Note: No pipefail in POSIX sh

# Check if running as PID 1
if [ $$ -eq 1 ]; then
    # PID 1 must handle signals properly
    trap 'kill -TERM $child 2>/dev/null' TERM INT

    # Start main process in background
    /app/main &
    child=$!

    # Wait for child
    wait "$child"
else
    # Not PID 1, run directly
    exec /app/main
fi
```

### Health Check Scripts

```bash
#!/usr/bin/env bash
# healthcheck.sh - Container health probe

set -euo pipefail

# Quick health check (< 1 second)
check_health() {
    local timeout=1

    # Check process is running
    if ! pgrep -f "myapp" > /dev/null; then
        echo "Process not running" >&2
        return 1
    fi

    # Check HTTP endpoint
    if ! timeout "$timeout" curl -sf http://localhost:8080/health > /dev/null; then
        echo "Health endpoint failed" >&2
        return 1
    fi

    # Check critical files
    if [[ ! -f /app/ready ]]; then
        echo "Not ready" >&2
        return 1
    fi

    return 0
}

check_health
```

## CI/CD Pipeline Patterns

### GitHub Actions Helper

```bash
#!/usr/bin/env bash
# ci-helper.sh - GitHub Actions utilities

set -euo pipefail

# Detect GitHub Actions
is_github_actions() {
    [[ "${GITHUB_ACTIONS:-false}" == "true" ]]
}

# GitHub Actions output
gh_output() {
    local name="$1"
    local value="$2"

    if is_github_actions; then
        echo "${name}=${value}" >> "$GITHUB_OUTPUT"
    fi
}

# GitHub Actions annotations
gh_error() {
    if is_github_actions; then
        echo "::error::$*"
    else
        echo "ERROR: $*" >&2
    fi
}

gh_warning() {
    if is_github_actions; then
        echo "::warning::$*"
    else
        echo "WARN: $*" >&2
    fi
}

gh_notice() {
    if is_github_actions; then
        echo "::notice::$*"
    else
        echo "INFO: $*"
    fi
}

# Set job summary
gh_summary() {
    if is_github_actions; then
        echo "$*" >> "$GITHUB_STEP_SUMMARY"
    fi
}

# Usage example
gh_notice "Starting build"
build_result=$(make build 2>&1)
gh_output "build_result" "$build_result"
gh_summary "## Build Complete\n\nStatus: Success"
```

### Azure DevOps Helper

```bash
#!/usr/bin/env bash
# azdo-helper.sh - Azure DevOps utilities

set -euo pipefail

# Detect Azure DevOps
is_azure_devops() {
    [[ -n "${TF_BUILD:-}" ]]
}

# Azure DevOps output variable
azdo_output() {
    local name="$1"
    local value="$2"

    if is_azure_devops; then
        echo "##vso[task.setvariable variable=$name]$value"
    fi
}

# Azure DevOps logging
azdo_error() {
    if is_azure_devops; then
        echo "##vso[task.logissue type=error]$*"
    else
        echo "ERROR: $*" >&2
    fi
}

azdo_warning() {
    if is_azure_devops; then
        echo "##vso[task.logissue type=warning]$*"
    else
        echo "WARN: $*" >&2
    fi
}

# Section grouping
azdo_section_start() {
    is_azure_devops && echo "##[section]$*"
}

azdo_section_end() {
    is_azure_devops && echo "##[endsection]"
}

# Usage
azdo_section_start "Running Tests"
test_result=$(npm test)
azdo_output "test_result" "$test_result"
azdo_section_end
```

### Multi-Platform CI Detection

```bash
#!/usr/bin/env bash
set -euo pipefail

# Detect CI environment
detect_ci() {
    if [[ "${GITHUB_ACTIONS:-false}" == "true" ]]; then
        echo "github"
    elif [[ -n "${TF_BUILD:-}" ]]; then
        echo "azuredevops"
    elif [[ -n "${GITLAB_CI:-}" ]]; then
        echo "gitlab"
    elif [[ -n "${CIRCLECI:-}" ]]; then
        echo "circleci"
    elif [[ -n "${JENKINS_URL:-}" ]]; then
        echo "jenkins"
    else
        echo "local"
    fi
}

# Universal output
ci_output() {
    local name="$1"
    local value="$2"
    local ci_env
    ci_env=$(detect_ci)

    case "$ci_env" in
        github)
            echo "${name}=${value}" >> "$GITHUB_OUTPUT"
            ;;
        azuredevops)
            echo "##vso[task.setvariable variable=$name]$value"
            ;;
        gitlab)
            echo "${name}=${value}" >> ci_output.env
            ;;
        *)
            echo "export ${name}=\"${value}\""
            ;;
    esac
}

# Universal error
ci_error() {
    local ci_env
    ci_env=$(detect_ci)

    case "$ci_env" in
        github)
            echo "::error::$*"
            ;;
        azuredevops)
            echo "##vso[task.logissue type=error]$*"
            ;;
        *)
            echo "ERROR: $*" >&2
            ;;
    esac
}
```

## Cloud Provider Patterns

### AWS Helper Functions

```bash
#!/usr/bin/env bash
set -euo pipefail

# Check AWS CLI availability
require_aws() {
    if ! command -v aws &> /dev/null; then
        echo "Error: AWS CLI not installed" >&2
        exit 1
    fi
}

# Get AWS account ID
get_aws_account_id() {
    aws sts get-caller-identity --query Account --output text
}

# Get secret from AWS Secrets Manager
get_aws_secret() {
    local secret_name="$1"

    aws secretsmanager get-secret-value \
        --secret-id "$secret_name" \
        --query SecretString \
        --output text
}

# Upload to S3 with retry
s3_upload_retry() {
    local file="$1"
    local s3_path="$2"
    local max_attempts=3
    local attempt=1

    while ((attempt <= max_attempts)); do
        if aws s3 cp "$file" "$s3_path"; then
            return 0
        fi

        echo "Upload failed (attempt $attempt/$max_attempts)" >&2
        ((attempt++))
        sleep $((attempt * 2))
    done

    return 1
}

# Assume IAM role
assume_role() {
    local role_arn="$1"
    local session_name="${2:-bash-script}"

    local credentials
    credentials=$(aws sts assume-role \
        --role-arn "$role_arn" \
        --role-session-name "$session_name" \
        --query Credentials \
        --output json)

    export AWS_ACCESS_KEY_ID=$(echo "$credentials" | jq -r .AccessKeyId)
    export AWS_SECRET_ACCESS_KEY=$(echo "$credentials" | jq -r .SecretAccessKey)
    export AWS_SESSION_TOKEN=$(echo "$credentials" | jq -r .SessionToken)
}
```

### Azure Helper Functions

```bash
#!/usr/bin/env bash
set -euo pipefail

# Check Azure CLI
require_az() {
    if ! command -v az &> /dev/null; then
        echo "Error: Azure CLI not installed" >&2
        exit 1
    fi
}

# Get Azure subscription ID
get_az_subscription_id() {
    az account show --query id --output tsv
}

# Get secret from Azure Key Vault
get_keyvault_secret() {
    local vault_name="$1"
    local secret_name="$2"

    az keyvault secret show \
        --vault-name "$vault_name" \
        --name "$secret_name" \
        --query value \
        --output tsv
}

# Upload to Azure Blob Storage
az_blob_upload() {
    local file="$1"
    local container="$2"
    local blob_name="${3:-$(basename "$file")}"

    az storage blob upload \
        --file "$file" \
        --container-name "$container" \
        --name "$blob_name" \
        --overwrite
}

# Get managed identity token
get_managed_identity_token() {
    local resource="${1:-https://management.azure.com/}"

    curl -sf -H Metadata:true \
        "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=$resource" \
        | jq -r .access_token
}
```

## Parallel Processing Patterns

### GNU Parallel

```bash
#!/usr/bin/env bash
set -euo pipefail

# Check for GNU parallel
if command -v parallel &> /dev/null; then
    # Process files in parallel
    export -f process_file
    find data/ -name "*.json" | parallel -j 4 process_file {}
else
    # Fallback to bash background jobs
    max_jobs=4
    job_count=0

    for file in data/*.json; do
        process_file "$file" &

        ((job_count++))
        if ((job_count >= max_jobs)); then
            wait -n
            ((job_count--))
        fi
    done

    wait  # Wait for remaining jobs
fi
```

### Job Pool Pattern

```bash
#!/usr/bin/env bash
set -euo pipefail

# Job pool implementation
job_pool_init() {
    readonly MAX_JOBS="${1:-4}"
    JOB_POOL_PIDS=()
}

job_pool_run() {
    # Wait if pool is full
    while ((${#JOB_POOL_PIDS[@]} >= MAX_JOBS)); do
        job_pool_wait_any
    done

    # Start new job
    "$@" &
    JOB_POOL_PIDS+=($!)
}

job_pool_wait_any() {
    # Wait for any job to finish
    if ((${#JOB_POOL_PIDS[@]} > 0)); then
        local pid
        wait -n
        # Remove finished PIDs
        for i in "${!JOB_POOL_PIDS[@]}"; do
            if ! kill -0 "${JOB_POOL_PIDS[$i]}" 2>/dev/null; then
                unset 'JOB_POOL_PIDS[$i]'
            fi
        done
        JOB_POOL_PIDS=("${JOB_POOL_PIDS[@]}")  # Reindex
    fi
}

job_pool_wait_all() {
    wait
    JOB_POOL_PIDS=()
}

# Usage
job_pool_init 4
for file in data/*.txt; do
    job_pool_run process_file "$file"
done
job_pool_wait_all
```

## Deployment Patterns

### Blue-Green Deployment

```bash
#!/usr/bin/env bash
set -euo pipefail

# Blue-green deployment helper
deploy_blue_green() {
    local new_version="$1"
    local health_check_url="$2"

    echo "Starting blue-green deployment: $new_version"

    # Deploy to green (inactive) environment
    echo "Deploying to green environment..."
    deploy_to_environment "green" "$new_version"

    # Health check
    echo "Running health checks..."
    if ! check_health "$health_check_url"; then
        echo "Health check failed, rolling back" >&2
        return 1
    fi

    # Switch traffic to green
    echo "Switching traffic to green..."
    switch_traffic "green"

    # Keep blue as backup for rollback
    echo "Deployment complete. Blue environment kept for rollback."
}

check_health() {
    local url="$1"
    local max_attempts=30
    local attempt=1

    while ((attempt <= max_attempts)); do
        if curl -sf "$url" > /dev/null; then
            return 0
        fi

        echo "Health check attempt $attempt/$max_attempts failed"
        sleep 2
        ((attempt++))
    done

    return 1
}
```

### Canary Deployment

```bash
#!/usr/bin/env bash
set -euo pipefail

# Canary deployment with gradual rollout
deploy_canary() {
    local new_version="$1"
    local stages=(5 10 25 50 100)  # Percentage stages

    echo "Starting canary deployment: $new_version"

    for percentage in "${stages[@]}"; do
        echo "Rolling out to $percentage% of traffic..."

        # Update traffic split
        update_traffic_split "$percentage" "$new_version"

        # Monitor for issues
        echo "Monitoring for 5 minutes..."
        if ! monitor_metrics 300; then
            echo "Issues detected, rolling back" >&2
            update_traffic_split 0 "$new_version"
            return 1
        fi

        echo "Stage $percentage% successful"
    done

    echo "Canary deployment complete"
}

monitor_metrics() {
    local duration="$1"
    local end_time=$((SECONDS + duration))

    while ((SECONDS < end_time)); do
        # Check error rate
        local error_rate
        error_rate=$(get_error_rate)

        if ((error_rate > 5)); then
            echo "Error rate too high: $error_rate%" >&2
            return 1
        fi

        sleep 10
    done

    return 0
}
```

## Logging and Monitoring

### Structured Logging

```bash
#!/usr/bin/env bash
set -euo pipefail

# JSON structured logging
log_json() {
    local level="$1"
    local message="$2"
    shift 2

    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Build JSON
    local json
    json=$(jq -n \
        --arg timestamp "$timestamp" \
        --arg level "$level" \
        --arg message "$message" \
        --arg script "$SCRIPT_NAME" \
        --argjson context "$(echo "$@" | jq -Rs .)" \
        '{
            timestamp: $timestamp,
            level: $level,
            message: $message,
            script: $script,
            context: $context
        }')

    echo "$json" >&2
}

log_info() { log_json "INFO" "$@"; }
log_error() { log_json "ERROR" "$@"; }
log_warn() { log_json "WARN" "$@"; }

# Usage
log_info "Processing file" "file=/data/input.txt" "size=1024"
```

## Resources

- [12-Factor App Methodology](https://12factor.net/)
- [Container Best Practices](https://cloud.google.com/architecture/best-practices-for-building-containers)
- [CI/CD Best Practices](https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment)

---

**Modern automation requires cloud-native patterns, container awareness, and robust CI/CD integration. These patterns ensure production-ready deployments in 2025.**

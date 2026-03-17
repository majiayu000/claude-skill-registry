---
name: cicd-expert
version: 1.0.0
description: Expert-level CI/CD with GitHub Actions, Jenkins, deployment pipelines, and automation
category: devops
tags: [cicd, github-actions, jenkins, gitlab-ci, deployment, automation, pipeline]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(git:*, docker:*, kubectl:*)
---

# CI/CD Expert

Expert guidance for Continuous Integration and Continuous Deployment, including GitHub Actions, Jenkins, GitLab CI, deployment strategies, and automation best practices.

## Core Concepts

### CI/CD Fundamentals
- Continuous Integration (CI)
- Continuous Delivery vs Deployment
- Build automation
- Test automation
- Artifact management
- Deployment strategies (blue-green, canary, rolling)

### Pipeline Design
- Pipeline stages and jobs
- Parallel execution
- Dependencies and artifacts
- Caching strategies
- Matrix builds
- Conditional execution

### Security
- Secret management
- Dependency scanning
- SAST/DAST
- Container scanning
- Supply chain security
- SBOM generation

## GitHub Actions

### Workflow Basics
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:

env:
  NODE_VERSION: '20'
  DOCKER_REGISTRY: ghcr.io

jobs:
  test:
    name: Test
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18, 20, 21]

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for SonarCloud

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linting
        run: npm run lint

      - name: Run tests
        run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage/coverage-final.json

  build:
    name: Build
    runs-on: ubuntu-latest
    needs: test

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - run: npm ci
      - run: npm run build

      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build
          path: dist/
          retention-days: 7

  security:
    name: Security Scan
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

      - name: Run npm audit
        run: npm audit --audit-level=high
```

### Docker Build and Push
```yaml
# .github/workflows/docker.yml
name: Docker Build and Push

on:
  push:
    branches: [main]
    tags: ['v*']

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          platforms: linux/amd64,linux/arm64
```

### Deployment Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    tags: ['v*']
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        type: choice
        options:
          - staging
          - production

jobs:
  deploy:
    name: Deploy to ${{ inputs.environment || 'production' }}
    runs-on: ubuntu-latest
    environment:
      name: ${{ inputs.environment || 'production' }}
      url: https://${{ inputs.environment || 'production' }}.example.com

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster ${{ secrets.ECS_CLUSTER }} \
            --service ${{ secrets.ECS_SERVICE }} \
            --force-new-deployment

      - name: Wait for deployment
        run: |
          aws ecs wait services-stable \
            --cluster ${{ secrets.ECS_CLUSTER }} \
            --services ${{ secrets.ECS_SERVICE }}

      - name: Notify Slack
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK }}
          payload: |
            {
              "text": "Deployment to ${{ inputs.environment || 'production' }} successful!",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "✅ *Deployment Successful*\n*Environment:* ${{ inputs.environment || 'production' }}\n*Version:* ${{ github.ref_name }}"
                  }
                }
              ]
            }
```

### Reusable Workflows
```yaml
# .github/workflows/reusable-test.yml
name: Reusable Test Workflow

on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string
      working-directory:
        required: false
        type: string
        default: '.'
    secrets:
      codecov-token:
        required: true

jobs:
  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ${{ inputs.working-directory }}

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: 'npm'
          cache-dependency-path: ${{ inputs.working-directory }}/package-lock.json

      - run: npm ci
      - run: npm test -- --coverage

      - uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.codecov-token }}

# Usage in another workflow
jobs:
  test-backend:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '20'
      working-directory: './backend'
    secrets:
      codecov-token: ${{ secrets.CODECOV_TOKEN }}
```

### Composite Actions
```yaml
# .github/actions/setup-project/action.yml
name: 'Setup Project'
description: 'Setup Node.js and install dependencies'

inputs:
  node-version:
    description: 'Node.js version'
    required: false
    default: '20'

runs:
  using: 'composite'
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: 'npm'

    - name: Install dependencies
      shell: bash
      run: npm ci

    - name: Cache build
      uses: actions/cache@v3
      with:
        path: |
          dist
          .next/cache
        key: ${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}

# Usage
steps:
  - uses: actions/checkout@v4
  - uses: ./.github/actions/setup-project
    with:
      node-version: '20'
```

## Jenkins

### Declarative Pipeline
```groovy
// Jenkinsfile
pipeline {
    agent {
        docker {
            image 'node:20-alpine'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        NODE_ENV = 'production'
        DOCKER_REGISTRY = 'ghcr.io'
        IMAGE_NAME = "${env.DOCKER_REGISTRY}/${env.GIT_ORG}/${env.GIT_REPO}"
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 1, unit: 'HOURS')
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        returnStdout: true,
                        script: 'git rev-parse --short HEAD'
                    ).trim()
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'npm ci'
            }
        }

        stage('Lint') {
            steps {
                sh 'npm run lint'
            }
        }

        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh 'npm run test:unit -- --coverage'
                    }
                    post {
                        always {
                            junit 'test-results/unit/*.xml'
                            publishHTML([
                                reportDir: 'coverage',
                                reportFiles: 'index.html',
                                reportName: 'Coverage Report'
                            ])
                        }
                    }
                }

                stage('Integration Tests') {
                    steps {
                        sh 'npm run test:integration'
                    }
                    post {
                        always {
                            junit 'test-results/integration/*.xml'
                        }
                    }
                }
            }
        }

        stage('Build') {
            steps {
                sh 'npm run build'
                archiveArtifacts artifacts: 'dist/**/*', fingerprint: true
            }
        }

        stage('Docker Build') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.build("${env.IMAGE_NAME}:${env.GIT_COMMIT_SHORT}")
                }
            }
        }

        stage('Security Scan') {
            parallel {
                stage('Dependency Check') {
                    steps {
                        sh 'npm audit --audit-level=high'
                    }
                }

                stage('Container Scan') {
                    when {
                        branch 'main'
                    }
                    steps {
                        sh """
                            trivy image \
                                --severity HIGH,CRITICAL \
                                --exit-code 1 \
                                ${env.IMAGE_NAME}:${env.GIT_COMMIT_SHORT}
                        """
                    }
                }
            }
        }

        stage('Push Image') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry("https://${env.DOCKER_REGISTRY}", 'docker-credentials') {
                        docker.image("${env.IMAGE_NAME}:${env.GIT_COMMIT_SHORT}").push()
                        docker.image("${env.IMAGE_NAME}:${env.GIT_COMMIT_SHORT}").push('latest')
                    }
                }
            }
        }

        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                script {
                    kubernetesDeploy(
                        configs: 'k8s/staging/*.yaml',
                        kubeconfigId: 'kubeconfig-staging'
                    )
                }
            }
        }

        stage('Smoke Tests') {
            when {
                branch 'main'
            }
            steps {
                sh 'npm run test:smoke -- --env=staging'
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            input {
                message 'Deploy to production?'
                ok 'Deploy'
            }
            steps {
                script {
                    kubernetesDeploy(
                        configs: 'k8s/production/*.yaml',
                        kubeconfigId: 'kubeconfig-production'
                    )
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            slackSend(
                color: 'good',
                message: "Build succeeded: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
        failure {
            slackSend(
                color: 'danger',
                message: "Build failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
    }
}
```

### Shared Library
```groovy
// vars/deployToKubernetes.groovy
def call(Map config) {
    def namespace = config.namespace
    def deployment = config.deployment
    def image = config.image

    sh """
        kubectl set image deployment/${deployment} \
            ${deployment}=${image} \
            -n ${namespace}

        kubectl rollout status deployment/${deployment} \
            -n ${namespace} \
            --timeout=5m
    """
}

// Usage in Jenkinsfile
@Library('shared-library') _

pipeline {
    stages {
        stage('Deploy') {
            steps {
                deployToKubernetes(
                    namespace: 'production',
                    deployment: 'web-app',
                    image: "${IMAGE_NAME}:${GIT_COMMIT_SHORT}"
                )
            }
        }
    }
}
```

## GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - security
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

default:
  image: node:20-alpine
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
      - .npm/

build:
  stage: build
  script:
    - npm ci --cache .npm --prefer-offline
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 week

test:unit:
  stage: test
  needs: [build]
  script:
    - npm ci --cache .npm --prefer-offline
    - npm run test:unit -- --coverage
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      junit: test-results/unit/*.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

test:integration:
  stage: test
  needs: [build]
  services:
    - postgres:15
    - redis:7
  variables:
    POSTGRES_DB: testdb
    POSTGRES_USER: testuser
    POSTGRES_PASSWORD: testpass
  script:
    - npm ci --cache .npm --prefer-offline
    - npm run test:integration
  artifacts:
    reports:
      junit: test-results/integration/*.xml

security:sast:
  stage: security
  image: returntocorp/semgrep
  script:
    - semgrep --config=auto --json --output=sast-report.json .
  artifacts:
    reports:
      sast: sast-report.json

security:dependency:
  stage: security
  script:
    - npm audit --audit-level=high
  allow_failure: true

docker:build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG
  only:
    - main
    - tags

deploy:staging:
  stage: deploy
  image: bitnami/kubectl:latest
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - kubectl config use-context $KUBE_CONTEXT_STAGING
    - kubectl set image deployment/web-app web-app=$IMAGE_TAG -n staging
    - kubectl rollout status deployment/web-app -n staging --timeout=5m
  only:
    - main

deploy:production:
  stage: deploy
  image: bitnami/kubectl:latest
  environment:
    name: production
    url: https://example.com
  script:
    - kubectl config use-context $KUBE_CONTEXT_PRODUCTION
    - kubectl set image deployment/web-app web-app=$IMAGE_TAG -n production
    - kubectl rollout status deployment/web-app -n production --timeout=5m
  when: manual
  only:
    - tags
```

## Deployment Strategies

### Blue-Green Deployment
```yaml
# GitHub Actions
- name: Blue-Green Deployment
  run: |
    # Deploy to green environment
    kubectl apply -f k8s/green/
    kubectl rollout status deployment/app-green -n production

    # Run smoke tests
    npm run test:smoke -- --env=green

    # Switch traffic to green
    kubectl patch service app -n production -p '{"spec":{"selector":{"version":"green"}}}'

    # Keep blue for rollback
    echo "Blue environment kept for rollback"
```

### Canary Deployment
```yaml
# Deploy canary (10% traffic)
- name: Deploy Canary
  run: |
    kubectl apply -f k8s/canary/
    kubectl set image deployment/app-canary app=$IMAGE_TAG -n production

    # Monitor metrics
    sleep 300

    # Check error rate
    ERROR_RATE=$(curl -s "$PROMETHEUS_URL/api/v1/query?query=error_rate" | jq -r '.data.result[0].value[1]')

    if (( $(echo "$ERROR_RATE < 0.01" | bc -l) )); then
      # Promote canary to stable
      kubectl set image deployment/app-stable app=$IMAGE_TAG -n production
      kubectl scale deployment/app-canary --replicas=0 -n production
    else
      # Rollback canary
      kubectl scale deployment/app-canary --replicas=0 -n production
      exit 1
    fi
```

### Rolling Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2        # Max 2 pods above desired count
      maxUnavailable: 1  # Max 1 pod unavailable during update
  template:
    spec:
      containers:
      - name: app
        image: myapp:v2
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Best Practices

### Pipeline Design
- Keep pipelines fast (< 10 minutes for CI)
- Fail fast on errors
- Run tests in parallel
- Cache dependencies
- Use matrix builds for multiple versions
- Separate CI and CD pipelines
- Make pipelines idempotent

### Security
- Scan dependencies for vulnerabilities
- Scan container images
- Use least privilege for credentials
- Rotate secrets regularly
- Sign commits and artifacts
- Use private registries
- Implement SBOM generation

### Artifact Management
- Use semantic versioning
- Tag images with git SHA
- Store artifacts in registries
- Implement retention policies
- Generate build manifests
- Track provenance

### Monitoring & Observability
- Track build success rate
- Monitor pipeline duration
- Alert on failures
- Log all deployments
- Track deployment frequency
- Measure lead time and MTTR

## Anti-Patterns to Avoid

❌ **No automated tests**: Deployments without tests are risky
❌ **Manual deployments**: Automate all deployments
❌ **Shared credentials**: Use role-based access
❌ **No rollback strategy**: Always have a rollback plan
❌ **Long-running pipelines**: Keep pipelines fast
❌ **Environment drift**: Use IaC for all environments
❌ **No monitoring**: Track deployment health
❌ **Direct production access**: Deploy through pipelines only

## Resources

- GitHub Actions: https://docs.github.com/en/actions
- Jenkins: https://www.jenkins.io/doc/
- GitLab CI: https://docs.gitlab.com/ee/ci/
- Argo CD: https://argo-cd.readthedocs.io/
- Tekton: https://tekton.dev/docs/

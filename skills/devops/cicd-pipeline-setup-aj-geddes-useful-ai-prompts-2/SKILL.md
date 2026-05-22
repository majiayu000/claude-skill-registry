---
name: cicd-pipeline-setup
description: Design and implement CI/CD pipelines with GitHub Actions, GitLab CI, Jenkins, or CircleCI. Use for automated testing, building, and deployment workflows.
---

# CI/CD Pipeline Setup

## Overview

Build automated continuous integration and deployment pipelines that test code, build artifacts, run security checks, and deploy to multiple environments with minimal manual intervention.

## When to Use

- Automated code testing and quality checks
- Containerized application builds
- Multi-environment deployments
- Release management and versioning
- Automated security scanning
- Performance testing integration
- Artifact management and registry

## Implementation Examples

### 1. **GitHub Actions Workflow**

```yaml
# .github/workflows/deploy.yml
name: Build and Deploy

on:
  push:
    branches:
      - main
      - develop
  pull_request:
    branches:
      - main
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Run linting
        run: npm run lint

      - name: Run tests
        run: npm run test:coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
          flags: unittests
          name: codecov-umbrella

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Snyk Security Scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

      - name: Run Trivy vulnerability scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'

  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

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
            type=semver,pattern={{version}}
            type=sha

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ secrets.AWS_ACCOUNT_ID }}:role/GithubActionsRole
          aws-region: us-east-1

      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster production \
            --service myapp \
            --force-new-deployment

      - name: Verify deployment
        run: |
          aws ecs wait services-stable \
            --cluster production \
            --services myapp
```

### 2. **GitLab CI Pipeline**

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: ""
  IMAGE_TAG: $CI_COMMIT_SHA

test:
  stage: test
  image: node:20
  cache:
    paths:
      - node_modules/
  script:
    - npm ci
    - npm run lint
    - npm run test:coverage
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
  coverage: '/Lines\s*:\s*(\d+.\d+)%/'

security:
  stage: test
  image: aquasec/trivy:latest
  script:
    - trivy fs --exit-code 0 --severity HIGH,CRITICAL .

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$IMAGE_TAG .
    - docker push $CI_REGISTRY_IMAGE:$IMAGE_TAG
    - docker tag $CI_REGISTRY_IMAGE:$IMAGE_TAG $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:latest
  only:
    - main
    - develop

deploy_staging:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache aws-cli
  script:
    - aws ecs update-service --cluster staging --service myapp --force-new-deployment
  environment:
    name: staging
    url: https://staging.myapp.com
  only:
    - develop

deploy_production:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache aws-cli
  script:
    - aws ecs update-service --cluster production --service myapp --force-new-deployment
  environment:
    name: production
    url: https://myapp.com
  when: manual
  only:
    - main
```

### 3. **Jenkins Pipeline**

```groovy
// Jenkinsfile
pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 1, unit: 'HOURS')
        timestamps()
    }

    environment {
        REGISTRY = 'gcr.io'
        PROJECT_ID = 'my-project'
        IMAGE_NAME = 'myapp'
        IMAGE_TAG = "${BUILD_NUMBER}-${GIT_COMMIT.take(7)}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    GIT_COMMIT_MSG = sh(
                        script: "git log -1 --pretty=%B",
                        returnStdout: true
                    ).trim()
                }
            }
        }

        stage('Install') {
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
            steps {
                sh 'npm run test:coverage'
                publishHTML([
                    reportDir: 'coverage',
                    reportFiles: 'index.html',
                    reportName: 'Coverage Report'
                ])
            }
        }

        stage('Build Image') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh '''
                        docker build -t ${REGISTRY}/${PROJECT_ID}/${IMAGE_NAME}:${IMAGE_TAG} .
                        docker tag ${REGISTRY}/${PROJECT_ID}/${IMAGE_NAME}:${IMAGE_TAG} \
                                   ${REGISTRY}/${PROJECT_ID}/${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        stage('Push Image') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    docker push ${REGISTRY}/${PROJECT_ID}/${IMAGE_NAME}:${IMAGE_TAG}
                    docker push ${REGISTRY}/${PROJECT_ID}/${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Deploy Staging') {
            when {
                branch 'develop'
            }
            steps {
                sh '''
                    kubectl set image deployment/myapp myapp=${REGISTRY}/${PROJECT_ID}/${IMAGE_NAME}:${IMAGE_TAG} \
                        -n staging --record
                    kubectl rollout status deployment/myapp -n staging
                '''
            }
        }

        stage('Deploy Production') {
            when {
                branch 'main'
            }
            input {
                message "Deploy to production?"
                ok "Deploy"
            }
            steps {
                sh '''
                    kubectl set image deployment/myapp myapp=${REGISTRY}/${PROJECT_ID}/${IMAGE_NAME}:${IMAGE_TAG} \
                        -n production --record
                    kubectl rollout status deployment/myapp -n production
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            slackSend(
                channel: '#deployments',
                message: "Build ${BUILD_NUMBER} succeeded on ${BRANCH_NAME}"
            )
        }
        failure {
            slackSend(
                channel: '#deployments',
                message: "Build ${BUILD_NUMBER} failed on ${BRANCH_NAME}"
            )
        }
    }
}
```

### 4. **CI/CD Script**

```bash
#!/bin/bash
# ci-pipeline.sh - Local pipeline validation

set -euo pipefail

echo "Starting CI/CD pipeline..."

# Code quality
echo "Running code quality checks..."
npm run lint
npm run type-check

# Testing
echo "Running tests..."
npm run test:coverage

# Build
echo "Building application..."
npm run build

# Docker build
echo "Building Docker image..."
docker build -t myapp:latest .

# Security scanning
echo "Running security scans..."
trivy image myapp:latest --exit-code 0 --severity HIGH

echo "All pipeline stages completed successfully!"
```

## Best Practices

### ✅ DO
- Fail fast with early validation
- Run tests in parallel when possible
- Use caching for dependencies
- Implement proper secret management
- Gate production deployments with approval
- Monitor and alert on pipeline failures
- Use consistent environment configuration
- Implement infrastructure as code

### ❌ DON'T
- Store credentials in pipeline configuration
- Deploy without automated tests
- Skip security scanning
- Allow long-running pipelines
- Mix staging and production pipelines
- Ignore test failures
- Deploy directly to main branch
- Skip health checks after deployment

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [CircleCI Documentation](https://circleci.com/docs/)

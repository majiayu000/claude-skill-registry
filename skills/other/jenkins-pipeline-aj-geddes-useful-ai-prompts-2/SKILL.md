---
name: jenkins-pipeline
description: Build Jenkins declarative and scripted pipelines with stages, agents, parameters, and plugins. Implement multi-branch pipelines and deployment automation.
---

# Jenkins Pipeline

## Overview

Create enterprise-grade Jenkins pipelines using declarative and scripted approaches to automate building, testing, and deploying with advanced control flow.

## When to Use

- Enterprise CI/CD infrastructure
- Complex multi-stage builds
- On-premise deployment automation
- Parameterized builds

## Implementation Examples

### 1. **Declarative Pipeline (Jenkinsfile)**

```groovy
pipeline {
    agent { label 'linux-docker' }
    environment {
        REGISTRY = 'docker.io'
        IMAGE_NAME = 'myapp'
    }
    parameters {
        string(name: 'DEPLOY_ENV', defaultValue: 'staging')
    }
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Install') { steps { sh 'npm ci' } }
        stage('Lint') { steps { sh 'npm run lint' } }
        stage('Test') {
            steps {
                sh 'npm run test:coverage'
                junit 'test-results.xml'
            }
        }
        stage('Build') {
            steps {
                sh 'npm run build'
                archiveArtifacts artifacts: 'dist/**/*'
            }
        }
        stage('Deploy') {
            when { branch 'main' }
            steps {
                sh 'kubectl set image deployment/app app=${REGISTRY}/${IMAGE_NAME}:latest'
            }
        }
    }
    post {
        always { cleanWs() }
        failure { echo 'Pipeline failed!' }
    }
}
```

### 2. **Scripted Pipeline (Groovy)**

```groovy
// Jenkinsfile - Scripted Pipeline

node('linux-docker') {
    def imageTag = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
    def registry = 'docker.io'

    try {
        stage('Checkout') { checkout scm }
        stage('Install') { sh 'npm ci' }
        stage('Test') { sh 'npm test' }
        stage('Build') { sh 'npm run build' }

        currentBuild.result = 'SUCCESS'
    } catch (Exception e) {
        currentBuild.result = 'FAILURE'
        error("Build failed: ${e.message}")
    }
}
```

### 3. **Multi-Branch Pipeline**

```groovy
pipeline {
    agent any
    stages {
        stage('Build') { steps { sh 'npm run build' } }
        stage('Test') { steps { sh 'npm test' } }
        stage('Deploy') {
            when { branch 'main' }
            steps { sh 'npm run deploy:prod' }
        }
    }
}
```

### 4. **Parameterized Pipeline**

```groovy
pipeline {
    agent any
    parameters {
        string(name: 'VERSION', defaultValue: '1.0.0', description: 'Version to release')
        choice(name: 'ENV', choices: ['staging', 'prod'], description: 'Deployment environment')
    }
    stages {
        stage('Build') { steps { sh 'npm run build' } }
        stage('Test') { steps { sh 'npm test' } }
        stage('Deploy') {
            steps { sh "npm run deploy:${params.ENV}" }
        }
    }
}
```

### 5. **Pipeline with Credentials**

```groovy
pipeline {
    agent any
    environment {
        DOCKER_CREDS = credentials('docker-hub')
    }
    stages {
        stage('Build & Push') {
            steps {
                sh '''
                    echo $DOCKER_CREDS_PSW | docker login -u $DOCKER_CREDS_USR --password-stdin
                    docker build -t myapp:latest .
                    docker push myapp:latest
                '''
            }
        }
    }
}
```

## Best Practices

### ✅ DO
- Use declarative pipelines for clarity
- Use credentials plugin for secrets
- Archive artifacts and reports
- Implement approval gates for production
- Keep pipelines modular and reusable

### ❌ DON'T
- Store credentials in pipeline code
- Ignore pipeline errors
- Skip test coverage reporting
- Use deprecated plugins

## Resources

- [Jenkins Pipeline Documentation](https://jenkins.io/doc/book/pipeline/)
- [Declarative Pipeline Syntax](https://jenkins.io/doc/book/pipeline/syntax/)

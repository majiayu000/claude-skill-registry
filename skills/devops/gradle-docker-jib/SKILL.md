---
name: gradle-docker-jib
description: |
  Configures and builds optimized Docker images using Google's Jib plugin without Docker daemon or Dockerfile.
  Use when containerizing Spring Boot microservices, building multi-architecture images,
  or pushing to registries. Triggers on "setup Jib", "build Docker image", "containerize
  with Jib", or "multi-arch image". Works with build.gradle.kts and includes Jib plugin
  setup, multi-module configuration, and CI/CD integration.

---

# Gradle Docker Jib Integration

## Table of Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
- [Requirements](#requirements)
- [See Also](#see-also)

## Purpose

Build Docker images efficiently using Google's Jib plugin without requiring Docker installation, Dockerfiles, or container knowledge. Jib automatically optimizes layers and handles multi-architecture builds for local and registry deployments.

## When to Use

Use this skill when you need to:
- Build Docker images without Docker daemon or Dockerfiles
- Containerize Spring Boot microservices efficiently
- Create multi-architecture images (amd64, arm64) for cloud deployment
- Optimize Docker layer caching for faster builds
- Push images to GCR, Docker Hub, or private registries
- Integrate Docker image building in CI/CD pipelines

## Quick Start

Add Jib plugin to `build.gradle.kts`:

```kotlin
plugins {
    id("com.google.cloud.tools.jib") version "3.4.4"
}

jib {
    from {
        image = "eclipse-temurin:21-jre-alpine"
    }
    to {
        image = "gcr.io/my-project/my-app"
        tags = setOf("latest", project.version.toString())
    }
    container {
        jvmFlags = listOf("-Xmx512m", "-Xms256m")
        ports = listOf("8080")
        user = "nobody"
    }
}
```

Build to local Docker:
```bash
./gradlew jibDockerBuild
```

Build and push to registry:
```bash
./gradlew jib
```

## Instructions

### Step 1: Add Jib Plugin

Add to `build.gradle.kts`:

```kotlin
plugins {
    id("com.google.cloud.tools.jib") version "3.4.4"
}
```

Or in `build.gradle`:
```groovy
plugins {
    id 'com.google.cloud.tools.jib' version '3.4.4'
}
```

### Step 2: Configure Base Image

Choose appropriate base image:

**For Spring Boot (JRE only):**
```kotlin
jib {
    from {
        image = "eclipse-temurin:21-jre-alpine"
        // or for ARM support
        // image = "eclipse-temurin:21-jre"
    }
}
```

**For distroless (minimal):**
```kotlin
jib {
    from {
        image = "gcr.io/distroless/java21-debian12"
    }
}
```

See [references/detailed-guide.md](./references/detailed-guide.md) for base image selection guide.

### Step 3: Configure Target Registry

**Google Container Registry (GCR):**
```kotlin
jib {
    to {
        image = "gcr.io/my-project/my-app"
        tags = setOf("latest", project.version.toString())
    }
}
```

**Docker Hub:**
```kotlin
jib {
    to {
        image = "docker.io/myusername/my-app"
        auth {
            username = System.getenv("DOCKER_USERNAME")
            password = System.getenv("DOCKER_PASSWORD")
        }
    }
}
```

**Private registry:**
```kotlin
jib {
    to {
        image = "registry.company.com/my-app"
        credHelper = "gcr"  // or "ecr-login", "docker-credential-gcr"
    }
}
```

### Step 4: Configure Container Settings

**JVM flags and ports:**
```kotlin
jib {
    container {
        jvmFlags = listOf(
            "-Xmx512m",
            "-Xms256m",
            "-Dspring.profiles.active=prod",
            "-XX:+UseContainerSupport"
        )
        ports = listOf("8080", "8081")
        labels = mapOf(
            "maintainer" to "team@company.com",
            "version" to project.version.toString()
        )
        user = "nobody"
        workingDirectory = "/app"
    }
}
```

**Environment variables:**
```kotlin
jib {
    container {
        environment = mapOf(
            "PORT" to "8080",
            "ENV" to "production"
        )
    }
}
```

See [references/detailed-guide.md](./references/detailed-guide.md) for advanced container configuration.

### Step 5: Configure Multi-Architecture Images

Build for multiple platforms:

```kotlin
jib {
    from {
        image = "eclipse-temurin:21-jre"
        platforms {
            platform {
                architecture = "amd64"
                os = "linux"
            }
            platform {
                architecture = "arm64"
                os = "linux"
            }
        }
    }
}
```

### Step 6: Set Up Authentication

**Using credential helpers:**

```bash
# Install credential helper
gcloud auth configure-docker

# Or for Docker Hub
docker login
```

**Using environment variables:**

```bash
export DOCKER_USERNAME=myuser
export DOCKER_PASSWORD=mypassword
./gradlew jib
```

**In CI/CD:**

```yaml
# GitHub Actions
- name: Build and Push
  run: ./gradlew jib
  env:
    DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
    DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
```

### Step 7: Build Images

**Build to local Docker daemon:**
```bash
./gradlew jibDockerBuild
docker images  # Verify image exists
```

**Build and push to registry:**
```bash
./gradlew jib
```

**Build OCI tar archive:**
```bash
./gradlew jibBuildTar
# Creates build/jib-image.tar
```

### Step 8: Configure Multi-Module Projects

For multi-module projects, configure Jib in specific modules:

```kotlin
// app/build.gradle.kts
plugins {
    id("com.google.cloud.tools.jib")
}

jib {
    to {
        image = "gcr.io/my-project/${project.name}"
    }
    container {
        mainClass = "com.example.app.MainKt"
    }
}

// service-a/build.gradle.kts
plugins {
    id("com.google.cloud.tools.jib")
}

jib {
    to {
        image = "gcr.io/my-project/${project.name}"
    }
}
```

See [references/detailed-guide.md](./references/detailed-guide.md) for complete multi-module setup.

### Step 9: Optimize Build Performance

**Enable caching:**

```kotlin
jib {
    // Use timestamp for better layer caching
    container {
        creationTime = "USE_CURRENT_TIMESTAMP"
    }
}
```

**Skip unchanged layers:**
Jib automatically caches layers by content hash - no configuration needed.

## Requirements

- **Gradle:** 7.0+ (8.11+ recommended)
- **Java:** JDK 11+ (21 recommended)
- **Jib Plugin:** 3.4.4+
- **Authentication:**
  - Docker credential helper (recommended)
  - Environment variables
  - Docker config (~/.docker/config.json)
- **For Local Docker:**
  - Docker daemon running
  - `jibDockerBuild` command
- **For Registry Push:**
  - Valid credentials
  - Network access to registry

## See Also

- [references/detailed-guide.md](./references/detailed-guide.md) - Comprehensive examples, commands reference, troubleshooting, and best practices
- [gradle-ci-cd-integration](../gradle-ci-cd-integration/SKILL.md) - Integrate Jib in CI/CD pipelines
- [Jib Documentation](https://github.com/GoogleContainerTools/jib) - Official Jib docs

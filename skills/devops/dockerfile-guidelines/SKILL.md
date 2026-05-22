---
name: dockerfile-guidelines
description: Provides Dockerfile best practices for this project. Claude should use this skill when creating or modifying Dockerfiles to ensure optimal layer caching by ordering instructions from most stable to least stable.
---

# Dockerfile Guidelines

When creating or modifying Dockerfiles for this project, follow these guidelines:

## Order Instructions by Descending Stability

Dockerfile instructions should be ordered from most stable (least likely to change) to least stable (most likely to change). This maximizes Docker layer caching efficiency, resulting in faster builds.

### Recommended Order

1. **Base image** (`FROM`) - Changes rarely
2. **System dependencies** (`RUN apt-get`, `RUN apk add`) - Changes infrequently
3. **Environment variables** (`ENV`) - Changes occasionally
4. **Working directory** (`WORKDIR`) - Changes rarely
5. **Copy dependency manifests** (`COPY package.json`, `COPY requirements.txt`) - Changes when dependencies change
6. **Install dependencies** (`RUN npm install`, `RUN pip install`) - Changes when dependencies change
7. **Copy application code** (`COPY . .`) - Changes frequently during development
8. **Build steps** (`RUN npm run build`) - Changes when code changes
9. **Runtime configuration** (`EXPOSE`, `CMD`, `ENTRYPOINT`) - Changes occasionally

### Example

```dockerfile
# 1. Base image (most stable)
FROM node:20-alpine

# 2. System dependencies
RUN apk add --no-cache tini

# 3. Environment variables
ENV NODE_ENV=production

# 4. Working directory
WORKDIR /app

# 5. Copy dependency manifests first
COPY package.json package-lock.json ./

# 6. Install dependencies (cached unless manifests change)
RUN npm ci --only=production

# 7. Copy application code (least stable - changes often)
COPY . .

# 8. Build step
RUN npm run build

# 9. Runtime configuration
EXPOSE 3000
CMD ["/sbin/tini", "--", "node", "dist/index.js"]
```

### Example: Java Application with Pre-built JAR

```dockerfile
# Base image (most stable)
FROM eclipse-temurin:17-jre
WORKDIR /app

# Install system tools (stable - rarely changes)
RUN apt-get update && apt-get install -y curl ca-certificates wget && \
    wget -O step-cli.tar.gz https://dl.smallstep.com/gh-release/cli/gh-release-header/v0.27.4/step_linux_0.27.4_$(dpkg --print-architecture).tar.gz && \
    tar -xzf step-cli.tar.gz && \
    mv step_0.27.4/bin/step /usr/local/bin/step && \
    rm -rf step-cli.tar.gz step_0.27.4 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

EXPOSE 8443

# Copy entrypoint script (changes occasionally)
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copy application JAR (changes frequently)
COPY build/libs/app.jar /app/app.jar

ENTRYPOINT ["/app/entrypoint.sh"]
```

### Why This Matters

Docker builds images in layers. When a layer changes, all subsequent layers must be rebuilt. By placing stable instructions first:

- Unchanged layers are retrieved from cache
- Only layers after the first change need rebuilding
- Development builds are significantly faster since code changes only invalidate the final layers

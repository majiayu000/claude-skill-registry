---
name: deployment-patterns
description: Generate deployment configuration for the user's project. Supports Docker, Docker Compose, GitHub Actions CI/CD, and cloud platform deployment (Vercel, Railway, Cloud Run). Detects stack automatically.
allowed-tools: Read, Write, Glob, Bash
---

# Deployment Patterns

Generate production-ready deployment configuration for the user's project.

## Stack Detection

```bash
ls Dockerfile docker-compose.yml .github/workflows/ package.json pom.xml go.mod pyproject.toml 2>/dev/null
```

## Docker Patterns

### Node.js/TypeScript
```dockerfile
FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile
COPY . .
RUN pnpm build

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./
RUN corepack enable && pnpm install --prod --frozen-lockfile
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Python
```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runner
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Java/Spring Boot
```dockerfile
FROM eclipse-temurin:21-jdk AS builder
WORKDIR /app
COPY mvnw pom.xml ./
COPY .mvn .mvn
RUN ./mvnw dependency:go-offline
COPY src ./src
RUN ./mvnw package -DskipTests

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

## GitHub Actions CI/CD

### Node.js CI
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "22" }
      - run: corepack enable && pnpm install --frozen-lockfile
      - run: pnpm check
      - run: pnpm test:coverage
```

## Cloud Deployment

### Railway (fastest for demos)
```toml
# railway.toml
[build]
builder = "DOCKERFILE"

[deploy]
startCommand = "node dist/index.js"
healthcheckPath = "/health"
```

### Vercel (Next.js/static)
```json
// vercel.json
{
  "framework": "nextjs",
  "buildCommand": "pnpm build",
  "outputDirectory": ".next"
}
```

### Google Cloud Run
```bash
gcloud run deploy my-service \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi
```

## Usage

```
/deployment-patterns              # detect stack and generate config
/deployment-patterns docker       # Dockerfile + docker-compose
/deployment-patterns ci           # GitHub Actions CI/CD
/deployment-patterns railway      # Railway deployment
/deployment-patterns vercel       # Vercel deployment
```

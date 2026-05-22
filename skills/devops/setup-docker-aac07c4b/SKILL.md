---
name: setup-docker
description: Configure Docker for local development and production. Use when adding Docker support to a project. Triggers on "setup docker", "add docker", "dockerize", "docker configuration", "devcontainer".
---

# Setup Docker

Configures Docker for local development (with VS Code Dev Containers) and production deployment, including MongoDB service.

## Quick Reference

**Files created**:

- `docker/` directory with all Docker-related files
- `.devcontainer/devcontainer.json` - VS Code Dev Container configuration
- `.dockerignore` - Files to exclude from Docker builds

**When to use**: When adding Docker support to a new or existing project

## Prerequisites

- Docker installed on your machine
- VS Code with "Remote - Containers" extension (for dev containers)
- Project with `package.json` and pnpm

## Instructions

### Phase 1: Create Directory Structure

#### Step 1: Create Docker Directory

```bash
mkdir -p docker
mkdir -p .devcontainer
```

### Phase 2: Create Dockerfiles

#### Step 2: Create Development Dockerfile

Create `docker/Dockerfile.dev`:

```dockerfile
FROM node:24-bullseye-slim
RUN npm install -g pnpm
WORKDIR /app
COPY package.json pnpm-lock.yaml* ./
RUN pnpm install
COPY . .
RUN chown -R node:node /app
USER node
EXPOSE 3000
CMD ["pnpm", "run", "dev"]
```

#### Step 3: Create Production Dockerfile

Create `docker/Dockerfile.prod`:

```dockerfile
# Stage 1: Build
FROM node:24-bullseye-slim AS builder
RUN npm install -g pnpm
WORKDIR /app
COPY package.json pnpm-lock.yaml* ./
RUN pnpm install
COPY . .
RUN pnpm run build
RUN pnpm prune --prod

# Stage 2: Production
FROM node:24-bullseye-slim
ENV NODE_ENV=production
WORKDIR /app
COPY --from=builder /app/package.json /app/pnpm-lock.yaml* ./
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["npm", "run", "start"]
```

### Phase 3: Create Environment Configuration

#### Step 4: Create Environment Example File

Create `docker/.env.example` (using the `BT_` prefix for all variables):

```bash
# Environment variable prefix: BT (Backend Template)
# Change this prefix in src/env.ts when creating a new service

BT_NODE_ENV=development
BT_PORT=3000

# MongoDB
BT_MONGODB_HOST=localhost
BT_MONGODB_PORT=27017
BT_MONGODB_DATABASE=my-app-db
BT_MONGODB_USER=admin
BT_MONGODB_PASSWORD=admin
```

#### Step 5: Create Development Environment File

Copy `docker/.env.example` to `docker/.env` and update values as needed.

### Phase 4: Create Docker Compose Files

#### Step 6: Create Development Docker Compose

Create `docker/docker-compose.dev.yml` (note: all env vars use `BT_` prefix):

```yaml
name: my-app-service
services:
  app:
    container_name: my-app-dev # Rename as needed
    build:
      context: ../ # relative to this file
      dockerfile: docker/Dockerfile.dev # relative to the build context
    volumes:
      - ../:/app:delegated
      - /app/node_modules
    env_file:
      - .env # relative to this file
    ports:
      - "${BT_PORT}:${BT_PORT}" # Map port host:container
    environment:
      - BT_NODE_ENV=development
      - BT_PORT=${BT_PORT}
      - BT_MONGODB_HOST=mongo_db # Use service name instead of localhost
      - BT_MONGODB_PORT=${BT_MONGODB_PORT}
      - BT_MONGODB_DATABASE=${BT_MONGODB_DATABASE}
      - BT_MONGODB_USER=${BT_MONGODB_USER}
      - BT_MONGODB_PASSWORD=${BT_MONGODB_PASSWORD}
    depends_on:
      mongo_db:
        condition: service_healthy
    command: /bin/sh -c "sleep infinity"
    user: node
    restart: unless-stopped
    networks:
      - app-network

  mongo_db:
    image: mongo:latest
    env_file:
      - .env
    ports:
      - "${BT_MONGODB_PORT}:${BT_MONGODB_PORT}"
    volumes:
      - mongodb_data:/data/db # Where MongoDB stores its data by default
    environment:
      - MONGO_INITDB_ROOT_USERNAME=${BT_MONGODB_USER}
      - MONGO_INITDB_ROOT_PASSWORD=${BT_MONGODB_PASSWORD}
      - MONGO_INITDB_DATABASE=${BT_MONGODB_DATABASE}
    healthcheck:
      test:
        [
          "CMD",
          "mongosh",
          "--authenticationDatabase=admin",
          "-u",
          "${BT_MONGODB_USER}",
          "-p",
          "${BT_MONGODB_PASSWORD}",
          "--eval",
          "db.runCommand('ping').ok",
          "--quiet",
        ]
      interval: 10s
      timeout: 10s
      retries: 5
    restart: unless-stopped
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  mongodb_data:
```

#### Step 7: Create Production Docker Compose

Create `docker/docker-compose.prod.yml`:

```yaml
name: my-app-service
services:
  app:
    container_name: my-app-prod
    build:
      context: ../ # relative to this file
      dockerfile: docker/Dockerfile.prod # relative to the build context
    env_file:
      - .env.production # relative to this file
    ports:
      - "${BT_PORT}:${BT_PORT}" # Map port host:container
    environment:
      - BT_NODE_ENV=production
      - BT_PORT=${BT_PORT}
      # For production, use managed database services (e.g., MongoDB Atlas)
      # - BT_MONGODB_URI=${BT_MONGODB_URI}
      # - BT_MONGODB_DATABASE=${BT_MONGODB_DATABASE}
    command: /bin/sh -c "npm run start"
    user: node
    restart: unless-stopped
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### Phase 5: Create Docker Ignore

#### Step 8: Create .dockerignore

Create `.dockerignore` in project root:

```
# Version control
.git
.gitignore

# Docker
docker
Dockerfile*
docker-compose*
.dockerignore

# Logs
logs
*.log
npm-debug.log*

# Dependency directories
node_modules
npm-cache

# Build output
dist
build

# Environment variables
.env
.env.local
.env.development
.env.test
.env.production

# IDE files
.vscode
.idea
*.swp
*.swo

# OS specific
.DS_Store
Thumbs.db

# Test coverage
coverage
```

### Phase 6: Configure VS Code Dev Container

#### Step 9: Create Dev Container Configuration

Create `.devcontainer/devcontainer.json`:

```json
{
  "name": "My App Dev",
  "dockerComposeFile": "../docker/docker-compose.dev.yml",
  "service": "app",
  "workspaceFolder": "/app",
  "forwardPorts": [3000],
  "shutdownAction": "stopCompose",
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "ms-vscode.js-debug-nightly",
        "esbenp.prettier-vscode",
        "ms-vscode.vscode-typescript-next",
        "vitest.explorer",
        "mongodb.mongodb-vscode"
      ],
      "settings": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "typescript.tsdk": "node_modules/typescript/lib"
      }
    }
  },
  "postCreateCommand": "pnpm install",
  "remoteUser": "node"
}
```

### Phase 7: Create Documentation

#### Step 10: Create Docker README

Create `docker/README.md`:

````markdown
# Docker Usage for Development and Production

This directory contains all the necessary files to build and run your application using Docker for both development and production environments.

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your machine.
- Copy `.env.example` and rename it in this `docker` directory to:
  - `.env` (for development)
  - `.env.production` (for production)
- Make sure to update the values as needed for your setup.

## Development

### 1. Build and Start All Services

From the project root, run:

```bash
docker compose --env-file docker/.env -f docker/docker-compose.dev.yml up --build
```
````

- This will build the development image using `Dockerfile.dev` and start the app along with MongoDB container.
- The app source code is mounted as a volume for live reload.
- The app will be available at `http://localhost:${PORT}` (default: 3000).

### 2. Stopping Services

You can press `Ctrl+C` to stop the services or run:

```bash
docker compose -f docker/docker-compose.dev.yml down
```

## Production

### 1. Build and Start the App

From the project root, run:

```bash
docker compose --env-file docker/.env.production -f docker/docker-compose.prod.yml up --build
```

- This will build the production image using `Dockerfile.prod` and start the app container.
- The app will be available at `http://localhost:${PORT}` (default: 3000).
- No source code is mounted; the image contains only the built app.

### 2. Stopping the App

You can press `Ctrl+C` to stop the services or run:

```bash
docker compose -f docker/docker-compose.prod.yml down
```

## Notes

- **Environment Files:** The `.env` (for development) and `.env.production` (for production) must be present in the `docker` directory before running the respective compose files.
- **Database Access:** In development, you can connect to MongoDB using the credentials and ports defined in your `.env` file.
- **Production Databases:** The production compose file does **not** start database containers. For production, use managed database services like MongoDB Atlas.

## Troubleshooting

- If you encounter issues with ports, ensure the `PORT` and other variables in your `.env` files match your application's configuration.
- If you change dependencies, rebuild the images with the `--build` flag.

````

### Phase 8: Update Git Ignore

#### Step 11: Update .gitignore

Add to `.gitignore`:

```plaintext
# Docker environment files (keep .env.example)
docker/.env
docker/.env.production
docker/.env.local
````

## Usage Patterns

### Development with VS Code Dev Container

1. Open the project in VS Code
2. Press `Cmd+Shift+P` (or `Ctrl+Shift+P` on Windows)
3. Select "Dev Containers: Rebuild and Reopen in Container"
4. Wait for the container to build and start
5. Open terminal in VS Code and run `pnpm dev`

### Development without VS Code

From the project root:

```bash
# Start services
docker compose --env-file docker/.env -f docker/docker-compose.dev.yml up --build

# Stop services
docker compose -f docker/docker-compose.dev.yml down
```

### Production Deployment

From the project root:

```bash
# Build and start
docker compose --env-file docker/.env.production -f docker/docker-compose.prod.yml up --build -d

# View logs
docker compose -f docker/docker-compose.prod.yml logs -f

# Stop
docker compose -f docker/docker-compose.prod.yml down
```

### Accessing MongoDB from Host

When running with Docker Compose, connect to MongoDB from your host machine:

```plaintext
mongodb://${BT_MONGODB_USER}:${BT_MONGODB_PASSWORD}@localhost:${BT_MONGODB_PORT}/${BT_MONGODB_DATABASE}?authSource=admin
```

### Accessing MongoDB from App Container

When connecting from within the Docker network, use the service name:

```plaintext
mongodb://${BT_MONGODB_USER}:${BT_MONGODB_PASSWORD}@mongo_db:${BT_MONGODB_PORT}/${BT_MONGODB_DATABASE}?authSource=admin
```

## Files Created Summary

```plaintext
project/
├── .devcontainer/
│   └── devcontainer.json      # VS Code Dev Container config
├── docker/
│   ├── Dockerfile.dev         # Development Dockerfile
│   ├── Dockerfile.prod        # Production Dockerfile (multi-stage)
│   ├── docker-compose.dev.yml # Development compose with MongoDB
│   ├── docker-compose.prod.yml # Production compose (app only)
│   ├── .env.example           # Environment template
│   └── README.md              # Docker usage documentation
└── .dockerignore              # Files excluded from Docker builds
```

## Customization

### Adding More Services

To add more services (e.g., Redis, PostgreSQL), update `docker-compose.dev.yml`:

```yaml
services:
  # ... existing services ...

  redis_cache:
    image: redis:latest
    env_file:
      - .env
    ports:
      - "${BT_REDIS_PORT}:${BT_REDIS_PORT}"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "${BT_REDIS_PASSWORD}", "ping"]
      interval: 10s
      timeout: 10s
      retries: 5
    command: ["redis-server", "--requirepass", "${BT_REDIS_PASSWORD}"]
    restart: unless-stopped
    networks:
      - app-network

volumes:
  # ... existing volumes ...
  redis_data:
```

Then update `docker/.env.example` (add `BT_REDIS_PORT` and `BT_REDIS_PASSWORD`) and the app service's environment variables.

### Changing Node Version

Update the `FROM` line in both Dockerfiles:

```dockerfile
FROM node:22-bullseye-slim  # or any other version
```

### Using npm Instead of pnpm

Replace pnpm commands with npm equivalents:

```dockerfile
# In Dockerfile.dev
# Remove: RUN npm install -g pnpm
# Change: RUN pnpm install -> RUN npm install
# Change: CMD ["pnpm", "run", "dev"] -> CMD ["npm", "run", "dev"]
```

## What NOT to Do

- Do NOT commit `docker/.env` or `docker/.env.production` (only `.env.example`)
- Do NOT run database containers in production (use managed services)
- Do NOT skip the healthcheck for database services
- Do NOT use `localhost` for service-to-service communication (use service names)
- Do NOT forget to update `forwardPorts` in `devcontainer.json` when adding new services

## See Also

- `setup-mongodb` - Configure MongoDB connection in the application
- `add-env-variable` - Add environment variables properly
- `bootstrap-project` - Initialize a new project from scratch

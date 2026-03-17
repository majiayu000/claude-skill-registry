---
name: docker-containerization
description: Provides guidance and templates for containerizing applications using Docker. Use when a user wants to create Dockerfiles, optimize images, set up multi-container applications with docker-compose, or follow best practices for containerization. Includes templates for frontend (Next.js), backend (FastAPI), workers, and databases.

---

# Docker Containerization

## Overview

This skill provides a structured workflow and a set of reusable assets for containerizing applications using Docker. It includes best-practice templates for Dockerfiles, `docker-compose.yml`, and other configuration files to streamline the containerization process.

## Workflow

Follow this workflow to containerize an application.

### 1. Choose a Dockerfile Template

Based on the service you are containerizing, start with one of the templates in `assets/dockerfile-templates/`:

- **`Dockerfile.nextjs`**: For Next.js frontend applications.
- **`Dockerfile.fastapi`**: For FastAPI backend applications.
- **`Dockerfile.worker`**: For generic background worker processes.

Copy the most relevant template to the root of your service's directory and rename it to `Dockerfile`.

For more details on Dockerfile best practices, refer to `references/dockerfile-best-practices.md`.

### 2. Set up `docker-compose.yml`

If you are working with a multi-service application, use the template at `assets/docker-compose-template/docker-compose.yml` as a starting point. This template defines a typical full-stack setup with a frontend, backend, and database.

Copy this file to the root of your project and customize it for your services.

For a detailed guide on Docker Compose, see `references/docker-compose-guide.md`.

### 3. Configure `.dockerignore`

To optimize the Docker build context and avoid sending unnecessary files to the Docker daemon, use a `.dockerignore` file. A comprehensive template is available at `assets/dockerignore-template/.dockerignore`.

Copy this file to the root of your project, and also to each service directory that has its own build context.

### 4. Configure Health Checks

Health checks are essential for ensuring the reliability of your services. This skill provides guidance and scripts for setting up health checks.

- For a guide on health check strategies, see `references/healthcheck-guide.md`.
- For a sample web service health check script, see `scripts/healthchecks/web-healthcheck.sh`.
- For a sample database health check script, see `scripts/healthchecks/db-healthcheck.sh`.

### 5. Manage Environment Variables

Properly managing environment variables is key to secure and flexible containerized applications. For a guide on different ways to inject environment variables, see `references/env-variable-guide.md`.

## Resources

This skill provides the following resources:

### assets/

Contains template files to be copied and customized.

- **`dockerfile-templates/`**: Dockerfile templates for different types of services.
- **`docker-compose-template/`**: A `docker-compose.yml` template for a multi-service application.
- **`dockerignore-template/`**: A `.dockerignore` template.
- **`database/`**: Contains an `init.sql` script for initializing a PostgreSQL database.

### scripts/

Contains executable scripts.

- **`healthchecks/`**: Shell scripts for container health checks.

### references/

Contains detailed documentation.

- **`dockerfile-best-practices.md`**: A guide to writing efficient and secure Dockerfiles.
- **`docker-compose-guide.md`**: A guide to using Docker Compose.
- **`healthcheck-guide.md`**: A guide to configuring health checks.
- **`env-variable-guide.md`**: A guide to managing environment variables.

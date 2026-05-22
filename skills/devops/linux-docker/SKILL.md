---
name: linux-docker
cluster: linux
description: "Docker/Compose: Dockerfile, networking, volumes, container lifecycle, registry, security hardening"
tags: ["docker","containers","compose","registry"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "docker container dockerfile compose build run deploy registry"
---

# linux-docker

## Purpose
This skill allows the AI to handle Docker and Docker Compose operations on Linux, focusing on Dockerfile creation, container management, networking, volumes, lifecycle events, registry interactions, and security hardening to ensure efficient, secure containerized applications.

## When to Use
Use this skill for tasks involving containerization of applications, such as building images from source code, deploying multi-service apps with Compose, managing network configurations for inter-container communication, or securing containers against vulnerabilities in a Linux environment.

## Key Capabilities
- Build and manage Docker images using Dockerfiles: Specify base images, add layers with COPY/ADD, set ENTRYPOINT/CMD.
- Configure networking: Use bridge, host, or overlay networks with flags like `--network bridge`.
- Handle volumes: Mount host directories or named volumes with `-v /host/path:/container/path`.
- Manage container lifecycle: Start, stop, restart containers using commands that handle signals like SIGTERM.
- Interact with registries: Push/pull images to/from repositories like Docker Hub, with authentication.
- Apply security hardening: Use options like `--security-opt no-new-privileges` to limit capabilities, and scan images with tools like Trivy.

## Usage Patterns
To build an image, read a Dockerfile, then execute `docker build` with appropriate context; for Compose, parse a YAML file and run `docker-compose up`. Always check for required dependencies like Docker daemon running. For networking, specify networks in Compose YAML under the `networks` key. Use environment variables for sensitive data, e.g., inject `$DOCKER_REGISTRY_URL` into container env. For security, always run containers with `--read-only` flag where possible to prevent writes.

## Common Commands/API
- Build an image: `docker build -t myimage:1.0 .` (use `-f path/Dockerfile` for custom file).
- Run a container: `docker run -d --name mycontainer -p 8080:80 -v /host/data:/app/data myimage:1.0`.
- Manage networks: `docker network create mynet` then `docker run --network mynet myimage`.
- Use volumes: `docker volume create myvolume` and mount with `-v myvolume:/data`.
- Container lifecycle: `docker start mycontainer`, `docker stop mycontainer`, `docker rm -f mycontainer`.
- Registry operations: `docker login -u user -p $DOCKER_PASSWORD registry.example.com`; push with `docker push myimage:1.0`.
- Docker Compose: `docker-compose -f docker-compose.yml up -d`; define services in YAML like:  
  ```
  version: '3'
  services:
    web:
      image: nginx
      ports:
        - "80:80"
  ```
- API endpoints: Use Docker Engine API, e.g., GET /containers/json to list containers; authenticate with headers including `$DOCKER_API_KEY`.

## Integration Notes
Integrate by ensuring Docker is installed via `apt install docker.io` on Ubuntu. For registry access, set env vars like `export DOCKER_REGISTRY_URL=registry.example.com` and `export DOCKER_API_KEY=yourkey`. When combining with other skills, e.g., in a CI/CD pipeline, use Compose files to orchestrate with tools like Jenkins; reference external configs with `${VAR}` in YAML. For security, always pull from trusted registries and use `--cap-drop ALL` in run commands. If using orchestration tools like Kubernetes, export Compose files with `docker-compose config` for conversion.

## Error Handling
Handle permission errors by prefixing commands with `sudo`, e.g., `sudo docker run ...`; check with `groups` to ensure user is in `docker` group. For image pull failures, verify registry auth with `echo $DOCKER_API_KEY` and retry `docker pull`. Network issues: Use `docker network inspect mynet` to debug; fix with `docker network prune`. Dockerfile build errors: Parse logs for messages like "no such file or directory" and correct paths. Compose errors: Validate YAML with `docker-compose config` before running; common fix for "service not found" is checking indentation. Always use `docker ps -a` to inspect running/faulty containers and `docker logs mycontainer` for output.

## Concrete Usage Examples
1. Build and run a simple Nginx container: First, create a Dockerfile with `FROM nginx:alpine; COPY index.html /usr/share/nginx/html;`. Then, build it: `docker build -t mynginx .`. Run securely: `docker run -d --name webserver -p 8080:80 --read-only mynginx`. Access at localhost:8080.
2. Orchestrate a web app with Compose: Create a docker-compose.yml file:  
   ```
   version: '3'
   services:
     db:
       image: postgres
       volumes:
         - dbdata:/var/lib/postgresql/data
     web:
       image: mynginx
       ports:
         - "8080:80"
   volumes:
     dbdata:
   ```  
   Then, start: `docker-compose up -d`. Scale web service: `docker-compose up -d --scale web=3`.

## Graph Relationships
- Connected to: linux cluster (parent).
- Related skills: based on tags ["docker", "containers", "compose", "registry"]; links to skills like container-management or linux-networking for extended operations.

---
name: build
description: Build salt-dev Docker container images (base and devtools) via buildx with the salt-8cpu builder. Creates the builder if missing.
disable-model-invocation: true
---

## Current State
- Branch: !`git branch --show-current`

Build the project Docker images:

1. Run `./lint.sh` -- abort if any check fails
2. Ensure the `salt-8cpu` builder exists:
   - Check: `docker buildx inspect salt-8cpu 2>/dev/null`
   - If missing, create and constrain to 8 CPUs:
     ```bash
     docker buildx create --name salt-8cpu --driver docker-container --driver-opt default-load=true
     docker buildx inspect --bootstrap salt-8cpu
     docker update --cpus 8 "$(docker ps -qf 'name=buildx_buildkit_salt-8cpu')"
     ```
   - Check memory: `docker info --format '{{.MemTotal}}'` -- warn user if < 22 GB
3. Build base image: `docker buildx build --builder salt-8cpu --pull -t salt-dev --load .`
4. If $ARGUMENTS contains "devtools" or "all":
   - Build devtools: `docker buildx build --builder salt-8cpu -f Dockerfile.devtools -t salt-dev-tools --load .`
5. Report build success/failure and image sizes via `docker images | grep salt-dev`

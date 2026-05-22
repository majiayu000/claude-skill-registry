---
name: rust-docker
description: Master Docker containerization for Rust applications
sasmp_version: "1.3.0"
bonded_agent: 08-rust-devops
bond_type: PRIMARY_BOND
version: "1.0.0"
---

# Rust Docker Skill

Master Docker containerization: multi-stage builds, minimal images, and production deployment.

## Quick Start

### Multi-Stage Dockerfile

```dockerfile
# Build stage
FROM rust:1.75-alpine AS builder
RUN apk add --no-cache musl-dev
WORKDIR /app

# Cache dependencies
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release && rm -rf src

# Build app
COPY src ./src
RUN touch src/main.rs && cargo build --release

# Runtime (< 20MB)
FROM alpine:3.19
RUN apk add --no-cache ca-certificates
COPY --from=builder /app/target/release/my-app /usr/local/bin/

RUN adduser -D appuser
USER appuser

HEALTHCHECK CMD wget -qO- localhost:8080/health || exit 1
CMD ["my-app"]
```

### Scratch Image (< 10MB)

```dockerfile
FROM rust:1.75 AS builder
RUN rustup target add x86_64-unknown-linux-musl
RUN apt-get update && apt-get install -y musl-tools
WORKDIR /app
COPY . .
RUN cargo build --release --target x86_64-unknown-linux-musl

FROM scratch
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/my-app /
ENTRYPOINT ["/my-app"]
```

## Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - RUST_LOG=info
```

## Commands

```bash
docker build -t my-app .
docker run --rm -p 8080:8080 my-app
docker images my-app  # Check size
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Slow builds | Cache Cargo.toml |
| Large images | Use multi-stage + alpine |
| SSL errors | Add ca-certificates |

## Resources

- [Docker Rust Guide](https://hub.docker.com/_/rust)
- [cargo-chef](https://github.com/LukeMathWalker/cargo-chef)

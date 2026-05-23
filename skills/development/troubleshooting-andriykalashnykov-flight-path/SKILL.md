---
name: troubleshooting
description: >
  Diagnose and fix common issues in the flight-path project: build failures, test failures, port conflicts, Docker problems, and tool errors.
  Use when something fails, an error occurs, the server won't start, or a command produces unexpected output.
  Do NOT use for environment setup, workflow guidance, or adding new features.
---

# Troubleshooting

## Port 8080 in Use

```bash
lsof -ti:8080 | xargs kill -9
# or
pkill -f "flight-path/server"
```

## API Returns 404

- Health check is `GET /` (not `/health`)
- Calculate is `POST /calculate` (not GET)
- Check Swagger: http://localhost:8080/swagger/index.html

## API Returns 500

- Check server terminal for error logs
- Test with minimal input: `curl -X POST http://localhost:8080/calculate -H 'Content-Type: application/json' -d '[["SFO", "EWR"]]'`
- Verify input format: `[][]string` — each segment must be exactly 2 airport codes

## Swagger Docs Stale

```bash
make api-docs    # Regenerate from annotations
pkill -f server  # Restart server
make run
```

- If generation fails, check Swagger annotation syntax against existing handlers in `internal/handlers/`
- Hard-refresh browser (Ctrl+Shift+R) to clear cached Swagger UI

## Build Fails

```bash
go version                # Must match go.mod (1.26.1)
go mod tidy && make build # Clean up and retry
go clean -cache           # Nuclear option
```

- `make build` depends on `api-docs` (which depends on `deps`), then compiles
- Ensure `GOFLAGS=-mod=mod` is set (Makefile sets this automatically)
- Use `make check` for the full pre-commit chain: `lint sec vulncheck secrets test api-docs build`

## Tests Fail

```bash
go test -v ./...          # Verbose output
go clean -testcache       # Clear cache
go test -race ./...       # Check for races
```

- `make test` runs tests with `TZ="UTC"` and `GOFLAGS=-mod=mod`
- Benchmarks: `go test ./internal/handlers/ -bench=. -benchmem -benchtime=3s`

## E2E Tests Fail

Server must be running first:
```bash
make run &
sleep 3
make e2e
pkill -f server
```

- `make e2e` depends on `deps` (installs Newman if missing)
- Tests live in `test/FlightPath.postman_collection.json`
- CI polls with curl for up to 30 seconds for server startup

## Docker Build Fails

```bash
docker buildx ls                    # Check builder exists
docker buildx create --use --name builder --driver docker-container --bootstrap
make docker-build                   # Build locally (single platform, uses buildx)
docker build --no-cache -t flight-path:debug .  # Build without cache
```

- Image: multi-stage Alpine build (`golang:1.26-alpine` -> `alpine:3.23.3`)
- Non-root user: `srvuser:1000`
- `CGO_ENABLED=0`, platforms: `linux/amd64`, `linux/arm64`, `linux/arm/v7`
- `make build-image` runs checks first (`deps api-docs lint sec vulncheck secrets`) then pushes to Docker Hub

## Docker Container Crashes at Runtime

Known issue: `.env` file is not copied into the Docker runtime stage, and `godotenv.Load()` calls `log.Fatalf` on error.

Workaround: pass `SERVER_PORT` as environment variable:
```bash
docker run -d -p 8080:8080 -e SERVER_PORT=8080 flight-path:local
```

Or use `make docker-run` / `make docker-test` which handle this automatically.

## Tool Not Found

```bash
make deps                           # Install all tools
export PATH=$PATH:$(go env GOPATH)/bin  # Ensure tools are on PATH
```

- `newman` requires Node.js — `make deps` installs both via nvm/npm

## Diagnostic Commands

```bash
ps aux | grep -E "(server|flight-path)"  # Check processes
lsof -i:8080                              # Check port
curl http://localhost:8080/                # Test health
which swag golangci-lint gosec govulncheck gitleaks actionlint newman  # Check tools
go env GOPATH GOROOT                       # Check Go paths
make check                                # Run full pre-commit checklist
```

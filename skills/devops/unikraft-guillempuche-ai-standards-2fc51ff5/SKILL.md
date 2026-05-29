---
name: unikraft
description: Kraft CLI commands for building and deploying Unikraft unikernels. Use when working with Kraftfiles, deploying to Unikraft Cloud, or managing unikernel instances.
---

# Kraft CLI Reference

Build and deploy unikernels with the `kraft` CLI.

- Documentation: <https://unikraft.org/docs/cli>
- Issues & support: <https://github.com/unikraft/kraftkit/issues>
- Platform: <https://unikraft.cloud>

## Important: Running Kraft Commands

When working with kraft CLI commands:

1. **Always show the commands first** - Tell the developer what commands to run before executing them
1. **Format for copy-paste** - Display commands in a code block ready to copy-paste into the terminal
1. **Ask before running** - Ask if the developer wants you to run the commands, as there can be authentication issues when `UKC_TOKEN` is not set in the AI's terminal session
1. **Let developer run if needed** - If commands fail due to missing tokens, provide the commands for the developer to run manually

## Environment Setup

Required for cloud commands (developer must set these in their terminal):

```bash
export UKC_TOKEN="your-token"   # Unikraft Cloud API token
export UKC_METRO=fra            # Metro/region (e.g., fra, ams, lon)
```

## Build Commands

```bash
kraft build                 # Configure and build Unikraft unikernels
kraft clean                 # Remove build object files
kraft menu                  # Open configuration editor TUI
```

## Project Library Commands

```bash
kraft lib add <lib>         # Add unikraft library to the project
kraft lib create            # Initialize a library from a template
kraft lib remove <lib>      # Remove a library dependency
```

## Packaging Commands

```bash
kraft pkg list              # List installed Unikraft component packages
kraft pkg pull <pkg>        # Pull a unikernel and/or its dependencies
kraft pkg push              # Push a unikernel package to registry
kraft pkg update            # Retrieve new component/library/package lists
kraft pkg info <pkg>        # Show information about a package
kraft pkg export            # Export a package
kraft pkg remove            # Remove selected local packages
```

## Local Runtime Commands

```bash
kraft run                   # Run a unikernel
kraft ps                    # List running unikernels
kraft stop <name>           # Stop one or more running unikernels
kraft start <name>          # Start one or more machines
kraft pause <name>          # Pause one or more running unikernels
kraft logs <name>           # Fetch the logs of a unikernel
kraft remove <name>         # Remove one or more running unikernels
```

## Local Networking Commands

```bash
kraft net create            # Create a new machine network
kraft net list              # List machine networks
kraft net inspect <name>    # Inspect a machine network
kraft net up <name>         # Bring a network online
kraft net down <name>       # Bring a network offline
kraft net remove <name>     # Remove a network
```

## Local Volume Commands

```bash
kraft vol create            # Create a machine volume
kraft vol ls                # List machine volumes
kraft vol inspect <name>    # Inspect a machine volume
kraft vol remove <name>     # Remove a volume
```

## Compose Commands (Local)

```bash
kraft compose up            # Run a compose project
kraft compose down          # Stop and remove a compose project
kraft compose ps            # List running services of current project
kraft compose logs          # Print the logs of services
kraft compose build         # Build or rebuild services
kraft compose create        # Create a compose project
kraft compose start         # Start a compose project
kraft compose stop          # Stop a compose project
kraft compose pause         # Pause a compose project
kraft compose unpause       # Unpause a compose project
kraft compose pull          # Pull images of services
kraft compose push          # Push images of services
```

## Cloud Deployment Commands

```bash
kraft cloud deploy          # Deploy your application to Unikraft Cloud
kraft cloud quota           # View your resource quota
kraft cloud tunnel          # Forward a local port to an unexposed instance
```

## Cloud Instance Commands

```bash
kraft cloud instance create   # Create an instance
kraft cloud instance list     # List instances
kraft cloud instance get      # Retrieve the state of instances
kraft cloud instance logs     # Get console output of instances
kraft cloud instance start    # Start instances
kraft cloud instance stop     # Stop instances
kraft cloud instance restart  # Restart instance(s)
kraft cloud instance remove   # Remove instances
```

## Cloud Service Commands

```bash
kraft cloud service create  # Create a service
kraft cloud service list    # List services
kraft cloud service get     # Retrieve the state of services
kraft cloud service logs    # Get console output for services
kraft cloud service drain   # Drain instances in a service
kraft cloud service remove  # Delete services
```

## Cloud Image Commands

```bash
kraft cloud image list      # List all images at a metro for your account
kraft cloud image remove    # Remove an image
```

## Cloud Volume Commands

```bash
kraft cloud volume create   # Create a persistent volume
kraft cloud volume list     # List persistent volumes
kraft cloud volume get      # Retrieve the state of persistent volumes
kraft cloud volume import   # Import local data to a persistent volume
kraft cloud volume attach   # Attach a persistent volume to an instance
kraft cloud volume detach   # Detach a persistent volume from an instance
kraft cloud volume remove   # Permanently delete persistent volume(s)
```

## Cloud Volume Template Commands

```bash
kraft cloud volume template create  # Create volume template(s)
kraft cloud volume template list    # List volume templates
kraft cloud volume template get     # Retrieve the state of volume templates
kraft cloud volume template remove  # Permanently delete volume template(s)
```

## Cloud Autoscale Commands

```bash
kraft cloud scale init      # Initialize autoscale configuration for a service
kraft cloud scale add       # Add an autoscale configuration policy
kraft cloud scale get       # Get an autoscale configuration or policy
kraft cloud scale remove    # Delete an autoscale configuration policy
kraft cloud scale reset     # Reset autoscale configuration of a service
```

## Cloud Certificate Commands

```bash
kraft cloud cert create     # Create a certificate
kraft cloud cert list       # List certificates
kraft cloud cert get        # Retrieve the status of a certificate
kraft cloud cert remove     # Remove a certificate
```

## Cloud Compose Commands

```bash
kraft cloud compose up      # Deploy services in a compose project to Unikraft Cloud
kraft cloud compose down    # Stop and remove services in a deployment
kraft cloud compose ps      # List active services of a Compose project
kraft cloud compose log     # View logs of services in a deployment
kraft cloud compose build   # Build a compose project
kraft cloud compose create  # Create a deployment from a Compose project
kraft cloud compose start   # Start services in a deployment
kraft cloud compose stop    # Stop services in a deployment
kraft cloud compose push    # Push images to Unikraft Cloud from a Compose project
kraft cloud compose ls      # List service deployments at a given path
```

## Useful Flags

```bash
--no-prompt                 # Do not prompt for user interaction
--no-color                  # Disable color output
--log-level <level>         # Log level: panic, fatal, error, warn, info, debug, trace
--help                      # Help for any command
```

______________________________________________________________________

## Xiroi Server Deployment

### Project Structure

Both `Kraftfile` and `Dockerfile.server` **MUST be at repository root**:

```
/xiroi (repo root)
├── Kraftfile              # Unikraft config (rootfs: ./Dockerfile.server)
├── Dockerfile.server      # FROM scratch optimized image
└── xiroi-apps/server/
    ├── Dockerfile.local       # Alpine-based for local debugging
    └── run_server_docker.sh   # Local Docker testing script
```

**Why at root?** Kraft CLI doesn't support parent directory references (`../`) in `rootfs` path, and Docker needs repo root as build context to COPY `xiroi-apps/`, `xiroi-packages/`, etc.

### Kraftfile Configuration

```yaml
spec: v0.6
name: xiroi-server
runtime: base-compat:latest

labels:
  cloud.unikraft.v1.instances/scale_to_zero.policy: "on"
  cloud.unikraft.v1.instances/scale_to_zero.stateful: "false"
  cloud.unikraft.v1.instances/scale_to_zero.cooldown_time_ms: 1000

rootfs: ./Dockerfile.server

cmd: ["/usr/bin/node", "/app/dist/index.js"]
```

### Dockerfile.server Key Features

The production Dockerfile uses `FROM scratch` for minimal Unikraft compatibility:

1. **Multi-stage build** - Builder stage uses `node:24-alpine`
1. **FROM scratch runtime** - Copies only required binaries/libraries
1. **Manual library copying** - Must copy `ld-musl`, `libgcc_s`, `libstdc++`
1. **SSL certificates** - Required for HTTPS connections (Neon DB, etc.)
1. **Empty .env files** - Dotenv needs files to exist even if env vars come from `-e` flags

### Deploy Commands

**Manual deployment:**

```bash
source .env.github
export UKC_TOKEN="$KRAFTCLOUD_TOKEN"

kraft cloud --metro fra deploy \
  --name xiroi-server-prod \
  -M 1024 \
  -p 443:4000 \
  --scale-to-zero off \
  -e NODE_ENV=production \
  -e SERVER_PORT=4000 \
  -e ALLOWED_ORIGINS="${ALLOWED_ORIGINS}" \
  # ... other env vars
  .
```

**Delete and redeploy (if instance exists):**

```bash
kraft cloud --metro fra instance delete xiroi-server-prod
# Then run deploy command again
```

### Rolling Updates (Zero-Downtime)

After the first deployment, KraftCloud creates a **Service** (load balancer) that owns the domain and port. Subsequent deployments can use rolling updates for zero downtime.

**Architecture:**

```
Service (load balancer)
  └── Instance (old) ──┐
  └── Instance (new) ──┘  ← Rolling update adds new, then removes old
```

**Key constraints for rolling updates:**

1. `--service <name>` is **mutually exclusive** with `-p` and `-d` (service already owns these)
1. `--name` must be **omitted** (kraft auto-generates unique names so new instance can spin up while old exists)

**Rolling update command:**

```bash
kraft cloud --metro fra deploy \
  --service <service-name> \
  --rollout remove_sequential \
  --rollout-wait 30s \
  -M 1024 \
  --scale-to-zero off \
  -e NODE_ENV=production \
  # ... other env vars
  .
```

**Get service name after first deployment:**

```bash
kraft cloud --metro fra service list
# Look for FQDN matching your domain (e.g., api.xiroi.cat)
```

**Rollout strategies:**

| Strategy            | Behavior                                      |
| ------------------- | --------------------------------------------- |
| `remove_sequential` | Start new → wait → remove old (zero downtime) |
| `remove`            | Remove old immediately after new starts       |
| `stop`              | Stop old (don't remove) after new starts      |
| `keep`              | Keep old running alongside new                |
| `abort`             | Cancel if old exists                          |

### Critical Flags

| Flag              | Value      | Purpose                                     |
| ----------------- | ---------- | ------------------------------------------- |
| `--metro`         | `fra`      | Frankfurt region                            |
| `-M`              | `1024`     | Memory in MiB                               |
| `-p`              | `443:4000` | HTTPS → app port                            |
| `--scale-to-zero` | `off`      | Keep always running (avoids wake-up issues) |

### Scale-to-Zero Considerations

**Why `--scale-to-zero off`?**

- Node.js server has slow cold starts (267ms+)
- Database connections need to stay alive
- Wake-up mechanism can cause 504 timeouts

**If you want scale-to-zero later:**

```bash
--scale-to-zero on --scale-to-zero-cooldown 300000ms  # 5 min cooldown
```

### Troubleshooting

| Error                                      | Cause                                  | Fix                                                |
| ------------------------------------------ | -------------------------------------- | -------------------------------------------------- |
| `ErrorDotenv`                              | `process.cwd()` returns `/` on scratch | Use `/app` as base dir in production               |
| `instance already exists`                  | Previous deployment                    | Delete first: `kraft cloud instance delete <name>` |
| `instance already exists` (rolling update) | `--name` specified with `--rollout`    | Omit `--name` flag for rolling updates             |
| `cannot use --service and --port`          | Flags are mutually exclusive           | Use `--service` without `-p` or `-d`               |
| `504 Gateway Timeout`                      | Scale-to-zero wake-up failing          | Use `--scale-to-zero off`                          |
| `could not build initrd from: ../..`       | Relative path in rootfs                | Keep Kraftfile at repo root                        |

### Verify Deployment

```bash
# List instances
kraft cloud --metro fra instance list | grep xiroi

# Check health
curl -s https://<your-domain>.fra.unikraft.app/api/health
# Returns: {"message":"OK"}

# View logs
kraft cloud --metro fra instance logs xiroi-server-prod
```

______________________________________________________________________

## Examples Repository

Reference examples: <https://github.com/unikraft-cloud/examples>

### All Example Folders

```
bun                              # Bun JavaScript runtime
caddy2.7-go1.21                  # Caddy web server with Go
code-server                      # Browser-based VS Code
database-redis7.2                # Redis in-memory store
debian-ssh                       # SSH access environment
dragonflydb                      # Modern Redis alternative
duckdb-go1.21                    # DuckDB analytical database with Go
expressjs4.18-node21             # Express.js framework
flask-redis                      # Flask with Redis
flask3.0-python3.12-sqlite3      # Flask with SQLite
grafana                          # Monitoring and visualization
haproxy                          # High availability proxy
http-c-debug                     # C HTTP server (debug)
http-elixir1.17                  # Elixir HTTP server
http-java21                      # Java 21 HTTP server
http-node25                      # Node.js 25 HTTP server
http-perl5.42                    # Perl HTTP server
http-python3.12-FastAPI-0.121.3  # FastAPI framework
http-rust-1.79-axum-scale-to-zero # Rust Axum with autoscaling
http-rust-trunkrs-leptos         # Rust Leptos full-stack
http-rust1.91                    # Rust HTTP server
httpserver-boost1.74-g++13.2     # C++ with Boost
httpserver-dotnet10.0            # .NET 10.0
httpserver-dotnet8.0             # .NET 8.0
httpserver-elixir1.16            # Elixir 1.16
httpserver-erlang26.2            # Erlang 26.2
httpserver-g++13.2               # C++ with GCC
httpserver-gcc13.2               # C with GCC
httpserver-go1.21                # Go 1.21
httpserver-go1.22-redis          # Go with Redis
httpserver-java17                # Java 17
httpserver-lua5.1                # Lua 5.1
httpserver-nodejs21              # Node.js 21
httpserver-perl5.38              # Perl 5.38
httpserver-php8.2                # PHP 8.2
httpserver-python3.12            # Python 3.12
httpserver-python3.12-django5.0  # Django 5.0
httpserver-python3.12-flask3.0   # Flask 3.0
httpserver-ruby3.2               # Ruby 3.2
httpserver-rust1.73              # Rust 1.73
httpserver-rust1.75              # Rust 1.75
httpserver-rust1.81-rocket0.5    # Rust Rocket framework
httpserver-rust1.87-actix-web4   # Rust Actix-web
hugo0.122                        # Hugo static site generator
imaginary                        # Image processing service
java17-spring-petclinic          # Spring Framework sample
java17-springboot3.2.x           # Spring Boot
mariadb                          # MariaDB database
mariadb11.7-volumes              # MariaDB with volumes
mcp-server-arxiv                 # MCP for arXiv
mcp-server-simple                # Basic MCP server
memcached1.6                     # Memcached
minio                            # S3-compatible storage
mongodb                          # MongoDB database
nginx                            # Nginx web server
nginx-flask-mongo                # Nginx + Flask + MongoDB
nginx-vite-vanilla               # Nginx with Vite
node-express-puppeteer           # Express with Puppeteer
node-playwright-chromium         # Playwright (Chromium)
node-playwright-firefox          # Playwright (Firefox)
node-playwright-webkit           # Playwright (WebKit)
node-vite-ssr-vanilla            # Vite SSR
node-vite-vanilla                # Vite vanilla
node18-agario                    # Agar.io game
node18-wingsio                   # Wings.io game
node21-nextjs                    # Next.js framework
node21-remix                     # Remix framework
node21-solid-start               # SolidJS framework
node21-sveltekit                 # SvelteKit framework
node21-websocket                 # WebSocket example
node24-karaoke                   # Karaoke application
opentelemetry-collector          # OpenTelemetry
postgres                         # PostgreSQL database
prisma-expressjs4.19-node18      # Prisma ORM with Express
python-playwright-chromium       # Python Playwright
python3.12-flask3.0-sqlite       # Flask with SQLite
ruby3.2-rails                    # Ruby on Rails
skipper0.18                      # HTTP router
spin-wagi-http                   # WebAssembly Gateway Interface
traefik                          # Traefik proxy
tyk                              # API gateway
vnc-browser                      # Browser-based VNC
vsftpd                           # FTP server
wazero-import-go                 # WebAssembly for Go
webhook-github-node              # GitHub webhook handler
wordpress-all-in-one             # WordPress single deploy
wordpress-compose                # WordPress with Compose
```

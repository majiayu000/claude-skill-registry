---
name: deployment
description: Deployment architecture, multi-tenancy design, and environment-specific deployment commands. Use when the user asks about how the application is deployed, multi-tenant architecture with Navigator, Fly.io deployment, or frontend stack details.
---

# Deployment and Architecture

## Multi-tenancy Design

- Each event runs as a separate Rails instance with its own SQLite database
- Navigator (Go web server) or Phusion Passenger manages multiple instances on a single machine
- NGINX or Navigator handles routing to the correct instance based on URL patterns
- Shared Redis instance for Action Cable across all events on a machine
- Navigator is included as a git submodule in the `navigator/` directory
- See [navigator/README.md](navigator/README.md) for details on the Go-based nginx/Passenger replacement

## Deployment Environments

### Test Environment (Kamal)
- URL: https://showcase.party/
- Deploy command: `bundle exec kamal $* --config-file=deploy.yml`
- Uses Kamal for deployment orchestration

### Staging Environment (Fly.io)
- URL: https://smooth-nav.fly.dev/
- Deploy command: `fly deploy --config nav.toml`
- Uses Fly.io with custom navigator configuration

### Admin/Backup Server (Git Hook)
- Runs index admin functions (user and location administration)
- Doubles as backup server of last resort
- Deploy command: `git push` (triggers post_update hook)
- Uses git push-based deployment with automatic hook execution

### Production Environment
- Deploy command: `fly deploy`
- Uses Fly.io deployment

## Deployment Architecture

- Runs on Fly.io across multiple regions globally
- Each region contains complete copy of all databases
- Automatic rsync backup between regions
- PDF generation runs on separate appliance machines via Fly-Replay routing
- Navigator supports app-based, machine-based, and region-based request routing
- Logging aggregated to dedicated logger instances

## Database Schema

- SQLite databases per event (~1MB typical size)
- Volumes for persistent storage
- Automatic backups via rsync to multiple locations
- Daily snapshot backups maintained indefinitely

## Frontend Stack

- Rails 8 with Import Maps (no Node.js build step)
- Stimulus.js for JavaScript behavior
- Turbo for SPA-like navigation
- TailwindCSS for styling
- Custom theme support per event

## Asset Management

```bash
# Precompile assets
bin/rails assets:precompile

# Clean old assets
bin/rails assets:clean

# Remove all compiled assets
bin/rails assets:clobber
```

## Real-time Updates

- Action Cable channels for live score updates
- Current heat tracking across all ballrooms
- WebSocket connections managed per event

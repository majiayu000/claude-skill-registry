---
name: coolify
description: Manage deployments on Coolify using the coolify CLI script. Deploy applications, manage custom domains, and monitor status.
homepage: https://coolify.bradarr.com
metadata: {"clawdbot":{"emoji":"🚀","requires":{"env":["COOLIFY_API_TOKEN"]},"version":"2.2.0"}}
---

# Coolify Deployment Skill (v2.2.0)

Manage deployments on Coolify self-hosted platform using the Python CLI script.

## Setup

### 1. Set API Token
```bash
export COOLIFY_API_TOKEN="your-api-token"
```

Get your token from https://coolify.bradarr.com → Settings → API Keys.

### 2. Test Installation
```bash
python scripts/coolify.py status
```

---

## Commands

### Quick Status
```bash
python scripts/coolify.py status
```
Shows all applications, projects, and servers with counts.

### Applications

#### List All Applications
```bash
python scripts/coolify.py apps list
```
Shows all applications with status icons.

#### Get Application Details
```bash
python scripts/coolify.py apps get --uuid <uuid>
```
Shows full details for one application.

#### Deploy Application
```bash
python scripts/coolify.py apps deploy --uuid <uuid>
python scripts/coolify.py apps deploy --uuid <uuid> --no-force  # Don't force rebuild
```

#### Wait for Deployment
```bash
python scripts/coolify.py apps wait --uuid <uuid>
python scripts/coolify.py apps wait --uuid <uuid> --timeout 600  # 10 minute timeout
```
Blocks until deployment completes or times out.

#### Get Logs
```bash
python scripts/coolify.py apps logs --uuid <uuid>
python scripts/coolify.py apps logs --uuid <uuid> --count 200  # More lines
```

#### Create Application
```bash
python scripts/coolify.py apps create \
  --name my-app \
  --repository https://github.com/user/repo \
  --build-pack dockerfile \
  --branch main
```

### Projects
```bash
python scripts/coolify.py projects list
```

### Servers
```bash
python scripts/coolify.py servers list
```

---

## Programmatic Usage

Import the API directly in Python scripts:

```python
from scripts.coolify import CoolifyAPI

api = CoolifyAPI()

# Check health
if not api.health_check():
    print("API not accessible!")

# List apps
apps = api.apps_list()
for app in apps:
    print(f"{app['name']}: {app['status']}")

# Create and deploy
app = api.apps_create(
    name="my-app",
    repository="https://github.com/user/repo"
)
print(f"Created: {app['uuid']}")

# Wait for deployment
result = api.apps_wait_for_deployment(app['uuid'], timeout=300)
print(result['message'])
```

---

## Common Workflows

### Deploy New Application with Custom Domain

```bash
# Create the application
python scripts/coolify.py apps create \
  --name my-website \
  --repository https://github.com/user/my-website

# Get the UUID from output, then add domain
# Note: Custom domain requires manual traefik configuration

# Deploy
python scripts/coolify.py apps deploy --uuid <uuid>

# Wait for completion
python scripts/coolify.py apps wait --uuid <uuid>
```

### Check Application Health

```bash
# Get status
python scripts/coolify.py apps get --uuid <uuid> | grep status

# Get logs if unhealthy
python scripts/coolify.py apps logs --uuid <uuid>
```

---

## Error Handling

### "COOLIFY_API_TOKEN not set"
```bash
export COOLIFY_API_TOKEN="your-token"
```

### "Invalid UUID format"
Ensure UUID is in correct format (e.g., `w8ogsc44w0cswcww8wwwg8o4`)

### "Repository URL must start with https://, http://, git://, or git@"
```bash
# Wrong
--repository github.com/user/repo

# Correct
--repository https://github.com/user/repo
```

### Deployment fails
```bash
# Check logs
python scripts/coolify.py apps logs --uuid <uuid>
```

---

## API Reference

### CoolifyAPI Methods

| Method | Description |
|--------|-------------|
| `health_check()` | Verify API accessibility |
| `apps_list()` | List all applications |
| `apps_get(uuid)` | Get application details |
| `apps_create(name, repository, ...)` | Create new application |
| `apps_deploy(uuid, force=True)` | Trigger deployment |
| `apps_logs(uuid, count=100)` | Get logs |
| `apps_status(uuid)` | Get simplified status |
| `apps_wait_for_deployment(uuid, timeout=300)` | Wait for deployment |
| `apps_add_domain(uuid, domain)` | Add custom domain |
| `projects_list()` | List projects |
| `servers_list()` | List servers |

### Validators

```python
from scripts.coolify import CoolifyValidators

# Validate inputs before API calls
CoolifyValidators.validate_uuid(uuid)
CoolifyValidators.validate_repository_url(url)
CoolifyValidators.validate_domain(domain)
CoolifyValidators.validate_build_pack(pack)
```

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `COOLIFY_API_TOKEN` | API token for authentication | Yes |
| `COOLIFY_API_URL` | API URL (default: https://coolify.bradarr.com) | No |

---

## Known UUIDs (Clawd Workspace)

| Resource | UUID |
|----------|------|
| Project | `jws4w4cc040444gk0ok0ksgk` |
| Environment | `g4wo8s0g48ogggkgwosc4sgs` |
| Server | `ykg8kc80k4wsock8so4swk04` |

---

## See Also

- **Coolify Dashboard:** https://coolify.bradarr.com
- **Coolify Docs:** https://coolify.io/docs

---

🦞 *Deploy with confidence*

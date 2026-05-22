---
name: pressable
description: Manage Pressable WordPress hosting via API. Use when creating/cloning sites, managing backups, purging cache, updating PHP versions, managing plugins, checking site status, or any Pressable hosting operations.
---

# Pressable Hosting Skill

Manage WordPress sites on [Pressable](https://pressable.com) managed hosting.

## Overview

This skill covers:
- **API** — Site management, cache, backups, plugins, DNS
- **SSH/SFTP** — Command-line access, WP-CLI
- **Git Deploy** — Auto-deploy from GitHub on push

---

## Setup

### 1. Enable API Access

1. Log in to [my.pressable.com](https://my.pressable.com)
2. Navigate to **API Applications** → **Create New API Application**
3. Name your app and select permission levels:
   - **Read-only** — Safe for monitoring/reporting
   - **Full access** — Required for modifications
4. Save the **Client ID** and **Client Secret**

📚 [Pressable API Setup Guide](https://pressable.com/knowledgebase/connecting-to-the-pressable-api/)

### 2. Store Credentials Securely

Create a credentials file (keep outside of git repos):

```bash
mkdir -p ~/.credentials
chmod 700 ~/.credentials
```

```json
// ~/.credentials/pressable.json
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

```bash
chmod 600 ~/.credentials/pressable.json
```

**Agent configuration:** Reference as `{baseDir}/../../.credentials/pressable.json` (relative to workspace).

### 3. Set Up SSH Keys (Recommended)

SSH keys allow passwordless access to all your Pressable sites.

```bash
# Generate a dedicated key
ssh-keygen -t ed25519 -f ~/.credentials/pressable-ssh/id_ed25519 -C "pressable-agent"

# Secure permissions
chmod 700 ~/.credentials/pressable-ssh
chmod 600 ~/.credentials/pressable-ssh/id_ed25519
```

Add the **public key** to Pressable:
1. Go to [my.pressable.com](https://my.pressable.com) → **Profile** → **Settings** → **SSH Keys**
2. Paste contents of `~/.credentials/pressable-ssh/id_ed25519.pub`

Supported key types:
- `ssh-ed25519` (256 bit) — recommended
- `ecdsa-sha2-nistp256` (256 bit)
- `ssh-rsa` (2048–16384 bit)

📚 [Pressable SSH Key Setup](https://pressable.com/knowledgebase/how-to-create-ssh-keys/)

---

## API Reference

### Authentication

```bash
# Load credentials
CREDS=$(cat ~/.credentials/pressable.json)
CLIENT_ID=$(echo $CREDS | jq -r '.client_id')
CLIENT_SECRET=$(echo $CREDS | jq -r '.client_secret')

# Get access token (valid 1 hour)
TOKEN=$(curl -s --location 'https://my.pressable.com/auth/token' \
  --form "grant_type=\"client_credentials\"" \
  --form "client_id=\"$CLIENT_ID\"" \
  --form "client_secret=\"$CLIENT_SECRET\"" | jq -r '.access_token')

# Use in requests
curl -s -H "Authorization: Bearer $TOKEN" "https://my.pressable.com/v1/sites"
```

**Note:** Tokens expire after 1 hour. Refresh before expiry for long-running operations.

### Sites

```bash
# List all sites
curl -s -H "Authorization: Bearer $TOKEN" "https://my.pressable.com/v1/sites" | jq '.data'

# Get site details
curl -s -H "Authorization: Bearer $TOKEN" "https://my.pressable.com/v1/sites/{id}"

# Create site
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://my.pressable.com/v1/sites" \
  -d '{"name":"my-new-site","datacenter_code":"DFW"}'

# Clone site
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://my.pressable.com/v1/sites/{id}/clone" \
  -d '{"name":"cloned-site"}'

# Delete site
curl -s -X DELETE -H "Authorization: Bearer $TOKEN" "https://my.pressable.com/v1/sites/{id}"

# Update PHP version (8.2, 8.3, 8.4, 8.5)
curl -s -X PUT -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://my.pressable.com/v1/sites/{id}" \
  -d '{"php_version":"8.3"}'
```

### Datacenters

| Code | Location |
|------|----------|
| AMS | Amsterdam |
| BUR | Burbank |
| DCA | Washington DC |
| DFW | Dallas |

### Edge Cache

```bash
# Get cache status
curl -s -H "Authorization: Bearer $TOKEN" "https://my.pressable.com/v1/sites/{id}/edge-cache"

# Toggle cache on/off
curl -s -X PUT -H "Authorization: Bearer $TOKEN" "https://my.pressable.com/v1/sites/{id}/edge-cache"

# Purge cache
curl -s -X DELETE -H "Authorization: Bearer $TOKEN" "https://my.pressable.com/v1/sites/{id}/edge-cache"

# Enable defensive mode (DDoS protection)
curl -s -X PUT -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://my.pressable.com/v1/sites/{id}/edge-cache/defensive-mode" \
  -d '{"duration":"1-hour"}'
```

### On-Demand Backups

```bash
# List backups
curl -s -H "Authorization: Bearer $TOKEN" "https://my.pressable.com/v1/sites/{id}/ondemand-backups"

# Create backup (type: "fs" for filesystem, "db" for database)
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://my.pressable.com/v1/sites/{id}/ondemand-backups" \
  -d '{"backup_type":"db"}'

# Download backup
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://my.pressable.com/v1/sites/{site_id}/ondemand-backups/{backup_id}/download"

# Delete backup
curl -s -X DELETE -H "Authorization: Bearer $TOKEN" \
  "https://my.pressable.com/v1/sites/{site_id}/ondemand-backups/{backup_id}"
```

**Limits:** 3 filesystem + 3 database backups max. Auto-deleted after 7–30 days.

### Plugins

```bash
# List plugins
curl -s -H "Authorization: Bearer $TOKEN" "https://my.pressable.com/v1/sites/{id}/plugins"

# Install & activate (from WordPress.org or URL)
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://my.pressable.com/v1/sites/{id}/plugins" \
  -d '{"plugins":[{"path":"jetpack"},{"path":"akismet","version":"5.1"}]}'

# Update plugins
curl -s -X PUT -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://my.pressable.com/v1/sites/{id}/plugins" \
  -d '{"plugins":[{"path":"jetpack"}]}'

# Activate / Deactivate
curl -s -X PUT -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://my.pressable.com/v1/sites/{id}/plugins/activate" \
  -d '{"plugins":[{"path":"jetpack"}]}'

curl -s -X PUT -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://my.pressable.com/v1/sites/{id}/plugins/deactivate" \
  -d '{"plugins":[{"path":"jetpack"}]}'

# Delete
curl -s -X DELETE -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://my.pressable.com/v1/sites/{id}/plugins" \
  -d '{"plugins":[{"path":"jetpack"}]}'
```

**Note:** Plugin operations are async. Use webhooks for completion status.

### DNS Zones

```bash
# List zones
curl -s -H "Authorization: Bearer $TOKEN" "https://my.pressable.com/v1/zones"

# Get zone records
curl -s -H "Authorization: Bearer $TOKEN" "https://my.pressable.com/v1/zones/{zone_id}/records"

# Create record
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://my.pressable.com/v1/zones/{zone_id}/records" \
  -d '{"type":"A","name":"www","value":"192.0.2.1","ttl":3600}'

# Delete record
curl -s -X DELETE -H "Authorization: Bearer $TOKEN" \
  "https://my.pressable.com/v1/zones/{zone_id}/records/{record_id}"
```

### Account & Collaborators

```bash
# Get account info
curl -s -H "Authorization: Bearer $TOKEN" "https://my.pressable.com/v1/account"

# Activity logs
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://my.pressable.com/v1/account/logs/activity" \
  -d '{"page":1,"per_page":20}'

# List collaborators
curl -s -H "Authorization: Bearer $TOKEN" "https://my.pressable.com/v1/collaborators"

# Add collaborator to sites
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://my.pressable.com/v1/collaborators/batch_create" \
  -d '{"email":"user@example.com","siteIds":[123,456],"roles":["wp_access","sftp_access"]}'
```

---

## SSH & WP-CLI

### SSH Access

Each Pressable site has unique SSH credentials. To connect:

1. Go to **Sites** → Select site → **Connections** tab
2. Find **SSH Username** and click **Reset** to generate password
3. Note the **SSH/SFTP URL** (format: `ssh.pressable.com`)

```bash
# Connect with password
ssh {ssh-username}@ssh.pressable.com

# Connect with SSH key (after adding to account)
ssh -i ~/.credentials/pressable-ssh/id_ed25519 {ssh-username}@ssh.pressable.com
```

**SSH Config (optional):** For easier access, add to `~/.ssh/config`:

```
Host pressable-mysite
  HostName ssh.pressable.com
  User id959e223a7c76e64
  IdentityFile ~/.credentials/pressable-ssh/id_ed25519
  IdentitiesOnly yes
```

Then connect with: `ssh pressable-mysite`

📚 [Pressable SSH Guide](https://pressable.com/knowledgebase/connect-to-ssh-on-pressable/)

### WP-CLI Commands

WP-CLI is pre-installed. After connecting via SSH:

```bash
# List plugins
wp plugin list

# Deactivate a problem plugin
wp plugin deactivate plugin-name

# Activate a theme
wp theme activate theme-name

# View PHP errors
wp php-errors

# Skip themes/plugins (for broken sites)
wp --skip-plugins --skip-themes plugin deactivate plugin-name
```

📚 [Pressable WP-CLI Guide](https://pressable.com/knowledgebase/how-to-use-wp-cli/)

### WP-CLI via API

Run WP-CLI commands without SSH:

```bash
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://my.pressable.com/v1/sites/{id}/ssh/command" \
  -d '{"command":["plugin list --format=json"]}'
```

**Note:** Don't include `wp` prefix — it's added automatically. Use webhooks for async responses.

### SSH Limitations

- **Session time:** 8 hours max
- **Memory:** 1GB RAM per session
- **Processes:** 25 max concurrent
- **Connections:** 10 per site (across all users)
- **Background processes:** Killed on disconnect (even with `nohup`)
- **Root access:** Not available

---

## GitHub Auto-Deploy

Deploy changes automatically when you push to GitHub.

### Setup

1. **Prepare your repo:**
   ```
   your-repo/
   └── wp-content/
       ├── themes/
       ├── plugins/
       └── mu-plugins/
   ```

2. **Connect to Pressable:**
   - Go to **Sites** → Select site → **Git** tab
   - Paste your repo's **HTTPS URL** (from GitHub's "Code" button)
   - Click **Set Repository URL**
   - Click **Authorize** and log in to GitHub

3. **Select branch:**
   - Choose the branch to deploy (e.g., `main`)
   - Configure sync settings:
     - ✅ Sync themes / plugins / mu-plugins
     - ⚠️ Delete files not in repo (optional, use carefully)
   - Click **Set and Deploy**

### How It Works

1. Push changes to configured branch
2. GitHub sends webhook to Pressable
3. Pressable clones repo and rsyncs to `wp-content/`
4. Only themes, plugins, mu-plugins sync (not core or uploads)

📚 [Pressable Git Deploy Guide](https://pressable.com/knowledgebase/how-deploy-to-your-sites-using-git/)

### Troubleshooting

- **Private repos:** Must grant OAuth access to organization
- **Wrong branch:** Check Git tab settings
- **Files not syncing:** Ensure they're in `wp-content/{themes,plugins,mu-plugins}/`
- **Deployments failing:** Check GitHub History in Git tab

---

## Best Practices

### Security

- Store credentials in `~/.credentials/` with `600` permissions
- Use SSH keys instead of passwords when possible
- Create read-only API apps for monitoring/reporting
- Rotate API credentials periodically

### Operations

- **Always backup before destructive operations**
- Test on staging sites first
- Use webhooks for async operation status
- Cache API tokens (1hr validity) to reduce auth calls

### Agent Usage

When the agent uses this skill:
1. Load credentials from configured path
2. Get fresh token if expired
3. Look up site ID from name if needed
4. Execute operation
5. Verify result

---

## Quick Reference

| Task | Method |
|------|--------|
| List sites | `GET /v1/sites` |
| Purge cache | `DELETE /v1/sites/{id}/edge-cache` |
| Create backup | `POST /v1/sites/{id}/ondemand-backups` |
| Run WP-CLI | `POST /v1/sites/{id}/ssh/command` or SSH |
| Deploy from Git | Push to connected branch |

**API Base:** `https://my.pressable.com`
**SSH Host:** `ssh.pressable.com`
**Docs:** [my.pressable.com/documentation/api/v1](https://my.pressable.com/documentation/api/v1)

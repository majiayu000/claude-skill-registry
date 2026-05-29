---
name: gitea
description: Expert guidance for Gitea self-hosted Git service including installation, configuration, repositories, webhooks, API usage, Docker deployment, and integration with CI/CD. Use this when working with Gitea Git hosting.
tags: [gitea, git, repository, version-control]
color: purple
---

# Gitea Expert Skill

You are an expert in Gitea, a lightweight self-hosted Git service similar to GitHub/GitLab.

## Core Concepts

### Features
- **Git Hosting**: Repository management with web UI
- **Issue Tracking**: Built-in issue management
- **Pull Requests**: Code review workflow
- **Wiki**: Documentation per repository
- **Organizations**: Group repositories and users
- **Webhooks**: Integration with external services
- **REST API**: Programmatic access
- **CI/CD**: Built-in Actions (GitHub Actions compatible)

### Architecture
```
User/Application
      ↓
Gitea (Go application)
      ↓
Git (repositories on disk)
      ↓
SQLite/PostgreSQL/MySQL (metadata)
```

## Installation

### Docker (Recommended)
```yaml
services:
  gitea:
    image: gitea/gitea:latest
    container_name: gitea
    environment:
      - USER_UID=1000
      - USER_GID=1000
      - GITEA__database__DB_TYPE=postgres
      - GITEA__database__HOST=db:5432
      - GITEA__database__NAME=gitea
      - GITEA__database__USER=gitea
      - GITEA__database__PASSWD=gitea
    restart: always
    networks:
      - gitea
    volumes:
      - gitea-data:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "3000:3000"  # Web UI
      - "2222:22"    # SSH
    depends_on:
      - db

  db:
    image: postgres:14-alpine
    restart: always
    environment:
      - POSTGRES_USER=gitea
      - POSTGRES_PASSWORD=gitea
      - POSTGRES_DB=gitea
    networks:
      - gitea
    volumes:
      - postgres-data:/var/lib/postgresql/data

networks:
  gitea:
    driver: bridge

volumes:
  gitea-data:
  postgres-data:
```

### Standalone Binary
```bash
# Download
wget -O gitea https://dl.gitea.io/gitea/latest/gitea-latest-linux-amd64
chmod +x gitea

# Create user
sudo adduser --system --shell /bin/bash --gecos 'Git Version Control' \
  --group --disabled-password --home /home/git git

# Install
sudo mv gitea /usr/local/bin/gitea

# Create directories
sudo mkdir -p /var/lib/gitea/{custom,data,log}
sudo chown -R git:git /var/lib/gitea/
sudo chmod -R 750 /var/lib/gitea/

# Systemd service
sudo vim /etc/systemd/system/gitea.service
```

**gitea.service:**
```ini
[Unit]
Description=Gitea (Git with a cup of tea)
After=network.target

[Service]
Type=simple
User=git
Group=git
WorkingDirectory=/var/lib/gitea/
ExecStart=/usr/local/bin/gitea web --config /etc/gitea/app.ini
Restart=always
Environment=USER=git HOME=/home/git GITEA_WORK_DIR=/var/lib/gitea

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable gitea
sudo systemctl start gitea
```

## Configuration

### app.ini (Main Config)
```ini
# /etc/gitea/app.ini or /data/gitea/conf/app.ini (Docker)

[server]
DOMAIN = git.example.com
HTTP_PORT = 3000
ROOT_URL = https://git.example.com/
DISABLE_SSH = false
SSH_PORT = 22
SSH_DOMAIN = git.example.com
START_SSH_SERVER = true

[database]
DB_TYPE = postgres
HOST = db:5432
NAME = gitea
USER = gitea
PASSWD = gitea
SCHEMA =
SSL_MODE = disable

[repository]
ROOT = /data/git/repositories
DEFAULT_BRANCH = main
DEFAULT_PRIVATE = private

[security]
INSTALL_LOCK = true
SECRET_KEY = change-this-secret-key
INTERNAL_TOKEN = change-this-internal-token

[service]
DISABLE_REGISTRATION = false
REQUIRE_SIGNIN_VIEW = false
ENABLE_NOTIFY_MAIL = true
DEFAULT_KEEP_EMAIL_PRIVATE = true

[mailer]
ENABLED = true
FROM = noreply@example.com
MAILER_TYPE = smtp
HOST = smtp.gmail.com:587
USER = user@gmail.com
PASSWD = app-password

[log]
MODE = console, file
LEVEL = info
ROOT_PATH = /data/gitea/log

[actions]
ENABLED = true
DEFAULT_ACTIONS_URL = https://github.com
```

### Environment Variables (Docker)
```yaml
environment:
  # Database
  - GITEA__database__DB_TYPE=postgres
  - GITEA__database__HOST=db:5432
  - GITEA__database__NAME=gitea
  - GITEA__database__USER=gitea
  - GITEA__database__PASSWD=gitea

  # Server
  - GITEA__server__DOMAIN=git.example.com
  - GITEA__server__ROOT_URL=https://git.example.com/
  - GITEA__server__HTTP_PORT=3000
  - GITEA__server__SSH_PORT=22

  # Security
  - GITEA__security__INSTALL_LOCK=true
  - GITEA__security__SECRET_KEY=your-secret-key

  # Service
  - GITEA__service__DISABLE_REGISTRATION=false
```

## Usage

### Repository Management

**Create Repository (Web UI)**
```
1. Click "+" → New Repository
2. Fill details:
   - Owner: user/organization
   - Name: my-repo
   - Visibility: Public/Private
   - Initialize: README, .gitignore, License
3. Click "Create Repository"
```

**Clone Repository**
```bash
# HTTPS
git clone https://git.example.com/user/repo.git

# SSH
git clone git@git.example.com:user/repo.git
```

**Push to Gitea**
```bash
git remote add origin https://git.example.com/user/repo.git
git push -u origin main
```

### Organizations

```
1. Click "+" → New Organization
2. Set name, visibility, description
3. Add members with roles:
   - Owner: Full control
   - Admin: Manage repos and members
   - Member: Access repos
```

### Webhooks

**Configure Webhook (Web UI)**
```
1. Repository → Settings → Webhooks
2. Add Webhook:
   - URL: https://your-service.com/webhook
   - Content Type: application/json
   - Secret: optional
   - Events: Push, Pull Request, Issues, etc.
3. Test Delivery
```

**Webhook Payload Example**
```json
{
  "ref": "refs/heads/main",
  "before": "abc123...",
  "after": "def456...",
  "commits": [
    {
      "id": "def456...",
      "message": "Add feature",
      "author": {
        "name": "John Doe",
        "email": "john@example.com"
      }
    }
  ],
  "repository": {
    "name": "my-repo",
    "full_name": "user/my-repo",
    "html_url": "https://git.example.com/user/my-repo"
  }
}
```

## API

### Authentication
```bash
# Personal Access Token
1. User Settings → Applications → Generate New Token
2. Select scopes: repo, write:repo, admin:org
3. Copy token
```

### REST API Examples

**List Repositories**
```bash
curl -H "Authorization: token YOUR_TOKEN" \
  https://git.example.com/api/v1/user/repos
```

**Create Repository**
```bash
curl -X POST \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-new-repo",
    "description": "My repository",
    "private": false,
    "auto_init": true
  }' \
  https://git.example.com/api/v1/user/repos
```

**Create Issue**
```bash
curl -X POST \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Bug found",
    "body": "Description of the bug",
    "labels": ["bug"]
  }' \
  https://git.example.com/api/v1/repos/user/repo/issues
```

**Create Pull Request**
```bash
curl -X POST \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "head": "feature-branch",
    "base": "main",
    "title": "Add new feature"
  }' \
  https://git.example.com/api/v1/repos/user/repo/pulls
```

**List Files in Repository**
```bash
curl -H "Authorization: token YOUR_TOKEN" \
  https://git.example.com/api/v1/repos/user/repo/contents/path/to/dir
```

## Gitea Actions (CI/CD)

### Enable Actions
```ini
# app.ini
[actions]
ENABLED = true
DEFAULT_ACTIONS_URL = https://github.com
```

### Workflow Example
```yaml
# .gitea/workflows/build.yml
name: Build and Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm install

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build
          path: dist/
```

### Self-hosted Runner
```bash
# Download runner
wget https://dl.gitea.io/act_runner/latest/act_runner-latest-linux-amd64
chmod +x act_runner-latest-linux-amd64
mv act_runner-latest-linux-amd64 /usr/local/bin/act_runner

# Register runner
act_runner register --instance https://git.example.com --token YOUR_RUNNER_TOKEN

# Run runner
act_runner daemon
```

## Integration with NiFi Registry

### Use Case
Store NiFi flow versions in Gitea using NiFi Registry's Git backend.

### Setup
```xml
<!-- NiFi Registry providers.xml -->
<flowPersistenceProvider>
  <class>org.apache.nifi.registry.provider.flow.git.GitFlowPersistenceProvider</class>
  <property name="Flow Storage Directory">./flow_storage</property>
  <property name="Remote To Push">origin</property>
  <property name="Remote Access User">gitea-user</property>
  <property name="Remote Access Password">gitea-token</property>
</flowPersistenceProvider>
```

**Initialize Git in flow_storage:**
```bash
cd flow_storage
git init
git remote add origin http://gitea:3000/user/nifi-flows.git
git config user.name "NiFi Registry"
git config user.email "registry@nifi.local"

# Test push
echo "# NiFi Flows" > README.md
git add README.md
git commit -m "Initial commit"
git push -u origin main
```

## Backup & Restore

### Backup
```bash
# Backup all data (repositories, database, config)
docker-compose exec gitea /bin/sh -c \
  "gitea dump -c /data/gitea/conf/app.ini -f /data/gitea-backup.zip"

# Copy backup out
docker cp gitea:/data/gitea-backup.zip ./backups/

# Database only (PostgreSQL)
docker-compose exec db pg_dump -U gitea gitea > gitea-db-backup.sql
```

### Restore
```bash
# Stop Gitea
docker-compose stop gitea

# Restore database
docker-compose exec -T db psql -U gitea gitea < gitea-db-backup.sql

# Restore data from dump
unzip gitea-backup.zip
# Copy files to appropriate locations

# Start Gitea
docker-compose start gitea
```

## Best Practices

### Security
1. **Use HTTPS**: Configure reverse proxy (Nginx/Traefik)
2. **Strong passwords**: Enforce password policies
3. **2FA**: Enable two-factor authentication
4. **SSH keys**: Prefer SSH over HTTPS for Git operations
5. **Regular backups**: Automate backups
6. **Update regularly**: Keep Gitea up to date

### Performance
1. **Database**: Use PostgreSQL for better performance
2. **Caching**: Enable Redis for session storage
3. **Indexing**: Enable repository indexing for search
4. **LFS**: Use Git LFS for large files
5. **Cleanup**: Periodic garbage collection (`gitea admin regenerate hooks`)

### Organization
1. **Teams**: Use teams for permission management
2. **Labels**: Standardize issue labels across repos
3. **Templates**: Use issue/PR templates
4. **Protected branches**: Require reviews for main branch
5. **Branch naming**: Enforce branch naming conventions

## Troubleshooting

### Common Issues
| Issue | Solution |
|-------|----------|
| Cannot push | Check SSH keys, repository permissions |
| Database connection failed | Verify database credentials, connectivity |
| 502 Bad Gateway | Check Gitea service status, logs |
| Large repo slow | Enable LFS, cleanup old data |
| Webhook not firing | Check URL, firewall, webhook logs |

### Logs
```bash
# Docker
docker-compose logs -f gitea

# Standalone
tail -f /var/lib/gitea/log/gitea.log

# Enable debug logging
# app.ini → [log] LEVEL = debug
```

### Commands
```bash
# Admin commands (Docker)
docker-compose exec gitea gitea admin user list
docker-compose exec gitea gitea admin user create --username admin --password password --email admin@example.com --admin

# Repository maintenance
docker-compose exec gitea gitea admin regenerate hooks
docker-compose exec gitea gitea doctor
```

## Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name git.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name git.example.com;

    ssl_certificate /etc/nginx/certs/cert.pem;
    ssl_certificate_key /etc/nginx/certs/key.pem;

    client_max_body_size 512M;

    location / {
        proxy_pass http://gitea:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Resources
- [Gitea Documentation](https://docs.gitea.io/)
- [API Documentation](https://docs.gitea.io/en-us/api-usage/)
- [Gitea Actions](https://docs.gitea.io/en-us/usage/actions/overview/)
- [Configuration Cheat Sheet](https://docs.gitea.io/en-us/config-cheat-sheet/)

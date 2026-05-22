---
name: algvex-web
description: |
  Manage and deploy the Algvex website for AItrader. 管理和部署 Algvex 网站。

  Use this skill when:
  - Deploying or updating the Algvex website (部署或更新网站)
  - Configuring the web frontend or backend (配置前端或后端)
  - Managing Google OAuth setup (管理 Google OAuth 设置)
  - Troubleshooting website issues (排查网站问题)
  - Adding new features to the web interface (添加新功能)
  - Configuring Caddy reverse proxy (配置 Caddy 反向代理)

  Keywords: algvex, website, web, frontend, backend, deploy, Next.js, FastAPI, Caddy, 网站, 部署
---

# Algvex Website Management

Web interface for AItrader trading system at algvex.com.

## Architecture

```
                    Caddy (HTTPS)
                    algvex.com:443
                        │
            ┌───────────┴───────────┐
            │                       │
        Frontend                Backend
        (Next.js)              (FastAPI)
      localhost:3000         localhost:8000
```

## Key Information

| Item | Value |
|------|-------|
| **Domain** | algvex.com |
| **Server** | 139.180.157.152 |
| **Frontend** | Next.js 14 + TypeScript |
| **Backend** | FastAPI + Python 3.11 |
| **Database** | SQLite |
| **Auth** | Google OAuth |
| **Install Path** | /home/linuxuser/algvex |

## Directory Structure

```
/home/linuxuser/algvex/
├── backend/           # FastAPI backend
│   ├── main.py
│   ├── .env           # Configuration
│   └── algvex.db      # SQLite database
├── frontend/          # Next.js frontend
│   ├── .next/         # Build output
│   └── pages/         # Page components
└── deploy/            # Deployment configs
```

## Deployment Commands

### Full Deployment
```bash
cd /home/linuxuser/nautilus_AItrader/web/deploy
chmod +x setup.sh
./setup.sh
```

### Restart Services
```bash
sudo systemctl restart algvex-backend algvex-frontend caddy
```

### Check Status
```bash
sudo systemctl status algvex-backend
sudo systemctl status algvex-frontend
sudo systemctl status caddy
```

### View Logs
```bash
# Backend logs
sudo journalctl -u algvex-backend -f

# Frontend logs
sudo journalctl -u algvex-frontend -f

# Caddy logs
sudo journalctl -u caddy -f
```

## Configuration

### Backend Environment (/home/linuxuser/algvex/backend/.env)

```bash
# Required
SECRET_KEY=your-secure-key
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
ADMIN_EMAILS=your-email@gmail.com

# AItrader Integration
AITRADER_PATH=/home/linuxuser/nautilus_AItrader
AITRADER_CONFIG_PATH=/home/linuxuser/nautilus_AItrader/configs/base.yaml
AITRADER_SERVICE_NAME=nautilus-trader
```

### Google OAuth Setup

1. Go to https://console.cloud.google.com/apis/credentials
2. Create OAuth 2.0 Client ID
3. Add redirect URI: `https://algvex.com/api/auth/callback/google`
4. Copy credentials to `.env`

## API Endpoints

### Public (No Auth)
| Endpoint | Description |
|----------|-------------|
| `/api/public/performance` | Trading stats |
| `/api/public/social-links` | Social links |
| `/api/public/copy-trading` | Copy trading links |
| `/api/public/system-status` | Bot status |

### Admin (Auth Required)
| Endpoint | Description |
|----------|-------------|
| `/api/admin/config` | Strategy config |
| `/api/admin/service/control` | Service control |
| `/api/admin/social-links/*` | Manage links |

## Caddy Configuration

Located at `/etc/caddy/Caddyfile`:

```
algvex.com {
    handle /api/* {
        reverse_proxy localhost:8000
    }
    handle {
        reverse_proxy localhost:3000
    }
}
```

## Common Issues

| Issue | Solution |
|-------|----------|
| HTTPS not working | Check DNS, wait for Let's Encrypt |
| 502 Bad Gateway | Restart backend/frontend services |
| OAuth callback error | Verify redirect URI in Google Console |
| Config not updating | Restart algvex-backend |

## Key Files

| File | Purpose |
|------|---------|
| `web/backend/main.py` | Backend entry point |
| `web/frontend/pages/index.tsx` | Homepage |
| `web/frontend/pages/admin/index.tsx` | Admin panel |
| `web/deploy/Caddyfile` | Reverse proxy config |
| `web/deploy/setup.sh` | Deployment script |

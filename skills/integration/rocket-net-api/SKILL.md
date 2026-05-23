---
name: rocket-net-api
description: |
  Build integrations with Rocket.net's WordPress hosting API. Manage sites, domains, backups, plugins, themes, CDN cache, FTP accounts, and more programmatically.

  Use when: building WordPress hosting management tools, automating site deployment, creating reseller portals, managing multiple WordPress sites, integrating with Rocket.net hosting services, automating backup workflows, or building custom control panels.
license: MIT
---

# Rocket.net API Integration

Build integrations with Rocket.net's managed WordPress hosting platform API. This skill covers authentication, site management, domain configuration, backups, plugins/themes, CDN cache control, and all 200+ API endpoints.

## API Overview

**Base URL**: `https://api.rocket.net/v1`

**Authentication**: JWT token-based
- Obtain token via POST `/login` with email/password
- Token expires in 7 days
- Include in requests as `Authorization: Bearer <token>`

**Content Type**: JSON API
- Required header: `Content-Type: application/json`
- Recommended header: `Accept: application/json`

**Documentation**: https://rocketdotnet.readme.io/reference/introduction

## Authentication

### Get JWT Token

```typescript
const response = await fetch('https://api.rocket.net/v1/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  body: JSON.stringify({
    username: 'your-email@example.com',
    password: 'your-password'
  })
});

const { token } = await response.json();
// Use token in subsequent requests
```

### Authenticated Request Pattern

```typescript
async function rocketApiRequest(
  endpoint: string,
  options: RequestInit = {}
): Promise<any> {
  const response = await fetch(`https://api.rocket.net/v1${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers
    }
  });

  if (response.status === 401) {
    // Token expired, re-authenticate
    throw new Error('Token expired - request new token');
  }

  return response.json();
}
```

## API Endpoints by Category

### Sites Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sites` | List all sites |
| POST | `/sites` | Create new site |
| GET | `/sites/{id}` | Get site details |
| PATCH | `/sites/{id}` | Update site properties |
| DELETE | `/sites/{id}` | Delete site |
| POST | `/sites/{id}/clone` | Clone a site (background task) |
| GET | `/sites/{id}/credentials` | Get site credentials |
| GET | `/sites/{id}/usage` | Get site usage statistics |
| POST | `/sites/{id}/lock` | Lock site (prevent modifications) |
| DELETE | `/sites/{id}/lock` | Unlock site |
| GET | `/sites/{id}/pma_login` | Get phpMyAdmin SSO link |
| GET | `/sites/{id}/settings` | Get site settings |
| PATCH | `/sites/{id}/settings` | Update site settings |
| GET | `/sites/locations` | List available site locations |

### Staging Sites

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/sites/{id}/staging` | Create staging site |
| DELETE | `/sites/{id}/staging` | Delete staging site |
| POST | `/sites/{id}/staging/publish` | Publish staging to production |

### Site Templates

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sites/templates` | List site templates |
| POST | `/sites/templates` | Create site template |
| GET | `/sites/templates/{id}` | Get template details |
| DELETE | `/sites/templates/{id}` | Delete template |
| POST | `/sites/templates/{id}/sites` | Create site from template |

### Domains

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sites/{id}/domains` | List domain aliases |
| POST | `/sites/{id}/domains` | Add domain alias |
| DELETE | `/sites/{id}/domains/{domainId}` | Remove domain alias |
| GET | `/sites/{id}/maindomain` | Get main domain info |
| POST | `/sites/{id}/maindomain` | Set main domain |
| PUT | `/sites/{id}/maindomain` | Replace main domain |
| PATCH | `/sites/{id}/maindomain` | Update domain validation/SSL |
| GET | `/sites/{id}/maindomain/status` | Check domain status |
| GET | `/sites/{id}/maindomain/recheck` | Force validation recheck |
| GET | `/sites/{id}/domains/{domainId}/edge_settings` | Get edge settings |
| PATCH | `/sites/{id}/domains/{domainId}/edge_settings` | Update edge settings |

### CDN Cache

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/sites/{id}/cache/purge` | Purge specific files |
| POST | `/sites/{id}/cache/purge_everything` | Purge all cache |

### Plugins

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sites/{id}/plugins` | List installed plugins |
| POST | `/sites/{id}/plugins` | Install plugins |
| PATCH | `/sites/{id}/plugins` | Activate/deactivate plugins |
| PUT | `/sites/{id}/plugins` | Update plugins |
| DELETE | `/sites/{id}/plugins` | Delete plugins |
| GET | `/sites/{id}/plugins/search` | Search available plugins |
| GET | `/sites/{id}/featured_plugins` | List featured plugins |

### Themes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sites/{id}/themes` | List installed themes |
| POST | `/sites/{id}/themes` | Install themes |
| PATCH | `/sites/{id}/themes` | Activate theme |
| PUT | `/sites/{id}/themes` | Update themes |
| DELETE | `/sites/{id}/themes` | Delete themes |
| GET | `/sites/{id}/themes/search` | Search available themes |

### Backups

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sites/{id}/backup` | List backups |
| POST | `/sites/{id}/backup` | Create backup |
| GET | `/sites/{id}/backup/{backupId}` | Download backup |
| DELETE | `/sites/{id}/backup/{backupId}` | Delete backup |
| POST | `/sites/{id}/backup/{backupId}/restore` | Restore backup |
| GET | `/sites/{id}/backup/automated` | List automated backups |
| POST | `/sites/{id}/backup/automated/{restoreId}/restore` | Restore automated backup |

### Cloud Backups

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sites/{id}/cloud_backups` | List cloud backups |
| POST | `/sites/{id}/cloud_backups` | Create cloud backup |
| GET | `/sites/{id}/cloud_backups/{backupId}` | Get cloud backup |
| DELETE | `/sites/{id}/cloud_backups/{backupId}` | Delete cloud backup |
| GET | `/sites/{id}/cloud_backups/{backupId}/download` | Get download link |
| POST | `/sites/{id}/cloud_backups/{backupId}/restore` | Restore cloud backup |

### Files

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sites/{id}/file_manager/files` | List files |
| POST | `/sites/{id}/files` | Upload file |
| PUT | `/sites/{id}/files` | Save file contents |
| DELETE | `/sites/{id}/files` | Delete file |
| GET | `/sites/{id}/files/view` | View file contents |
| GET | `/sites/{id}/files/download` | Download file |
| POST | `/sites/{id}/files/folder` | Create folder |
| POST | `/sites/{id}/files/extract` | Extract archive |
| POST | `/sites/{id}/files/compress` | Compress files |
| PATCH | `/sites/{id}/files/chmod` | Change permissions |

### FTP Accounts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sites/{id}/ftp_accounts` | List FTP accounts |
| POST | `/sites/{id}/ftp_accounts` | Create FTP account |
| PATCH | `/sites/{id}/ftp_accounts` | Update FTP account |
| DELETE | `/sites/{id}/ftp_accounts` | Delete FTP account |

### SSH Keys

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sites/{id}/ssh_keys` | List SSH keys |
| POST | `/sites/{id}/ssh_keys` | Import SSH key |
| DELETE | `/sites/{id}/ssh_keys` | Delete SSH key |
| POST | `/sites/{id}/ssh_keys/authorize` | Activate SSH key |
| POST | `/sites/{id}/ssh_keys/deauthorize` | Deactivate SSH key |
| GET | `/sites/{id}/ssh_keys/{name}` | View SSH key info |

### WordPress

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sites/{id}/wp_login` | Get WordPress SSO link |
| GET | `/sites/{id}/wp_status` | Get WordPress status |
| POST | `/sites/{id}/wpcli` | Execute WP-CLI command |

### Reporting

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/reporting/sites/{id}/cdn_requests` | CDN requests report |
| GET | `/reporting/sites/{id}/cdn_cache_status` | Cache status report |
| GET | `/reporting/sites/{id}/cdn_cache_content` | Cache content report |
| GET | `/reporting/sites/{id}/visitors` | Visitors report |
| GET | `/reporting/sites/{id}/waf_eventlist` | WAF events list |
| GET | `/reporting/sites/{id}/waf_events_source` | WAF events by source |
| GET | `/reporting/sites/{id}/waf_firewall_events` | Firewall events |
| GET | `/reporting/sites/{id}/bandwidth_usage` | Bandwidth usage |
| GET | `/reporting/sites/{id}/bandwidth_top_usage` | Top bandwidth usage |
| GET | `/sites/{id}/access_logs` | Access logs |

### Account Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/account/me` | Get user information |
| PATCH | `/account/me` | Update account settings |
| GET | `/account/usage` | Get account usage stats |
| POST | `/account/password` | Change password |
| GET | `/account/tasks` | List account tasks |
| GET | `/account/hosting_plan` | Get current plan |
| PUT | `/account/hosting_plan` | Change hosting plan |
| POST | `/account/billing_sso` | Get billing SSO cookie |

### Account Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | List account users |
| POST | `/users` | Create account user |
| GET | `/users/{userId}` | Get user details |
| PATCH | `/users/{userId}` | Update user |
| DELETE | `/users/{userId}` | Remove user |
| POST | `/users/{userId}/reinvite` | Resend invite |

### Site Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sites/{id}/users` | List site users |
| POST | `/sites/{id}/users` | Invite site user |
| DELETE | `/sites/{id}/users/{userId}` | Remove site user |
| POST | `/sites/{id}/users/{userId}/reinvite` | Resend invite |

### Billing

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/billing/addresses` | List billing addresses |
| POST | `/billing/addresses` | Create billing address |
| GET | `/billing/addresses/{addressId}` | Get billing address |
| PATCH | `/billing/addresses/{addressId}` | Update billing address |
| DELETE | `/billing/addresses/{addressId}` | Delete billing address |
| GET | `/billing/invoices` | List invoices |
| GET | `/billing/invoices/{invoiceId}` | Get invoice |
| GET | `/billing/invoices/{invoiceId}/pdf` | Download invoice PDF |
| POST | `/billing/invoices/{invoiceId}/credit_card_payment` | Pay with card |
| GET | `/billing/payment_methods` | List payment methods |
| POST | `/billing/payment_methods` | Add payment method |
| DELETE | `/billing/payment_methods/{methodId}` | Delete payment method |
| GET | `/billing/products` | List available products |

### Additional Features

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sites/{id}/password_protection` | Get password protection status |
| POST | `/sites/{id}/password_protection` | Enable password protection |
| DELETE | `/sites/{id}/password_protection` | Disable password protection |
| GET | `/sites/{id}/shopshield` | List ShopShield URIs |
| POST | `/sites/{id}/shopshield` | Enable ShopShield |
| DELETE | `/sites/{id}/shopshield/{id}` | Disable ShopShield |
| GET | `/account/visitors` | Account visitor stats |
| GET | `/account/bandwidth` | Account bandwidth stats |

## Common Patterns

### List All Sites

```typescript
const sites = await rocketApiRequest('/sites');
console.log(sites);
// Returns array of site objects with id, domain, status, etc.
```

### Create a New Site

```typescript
const newSite = await rocketApiRequest('/sites', {
  method: 'POST',
  body: JSON.stringify({
    name: 'my-new-site',
    location: 'us-east-1',
    // Additional options as needed
  })
});
```

### Purge CDN Cache

```typescript
// Purge specific URLs
await rocketApiRequest(`/sites/${siteId}/cache/purge`, {
  method: 'POST',
  body: JSON.stringify({
    files: [
      'https://example.com/style.css',
      'https://example.com/script.js'
    ]
  })
});

// Purge everything
await rocketApiRequest(`/sites/${siteId}/cache/purge_everything`, {
  method: 'POST'
});
```

### Create and Restore Backup

```typescript
// Create backup
const backup = await rocketApiRequest(`/sites/${siteId}/backup`, {
  method: 'POST'
});

// List backups
const backups = await rocketApiRequest(`/sites/${siteId}/backup`);

// Restore backup (background task)
await rocketApiRequest(`/sites/${siteId}/backup/${backupId}/restore`, {
  method: 'POST'
});
```

### Manage Plugins

```typescript
// List installed plugins
const plugins = await rocketApiRequest(`/sites/${siteId}/plugins`);

// Install plugin
await rocketApiRequest(`/sites/${siteId}/plugins`, {
  method: 'POST',
  body: JSON.stringify({
    plugins: ['wordfence', 'yoast-seo']
  })
});

// Update all plugins
await rocketApiRequest(`/sites/${siteId}/plugins`, {
  method: 'PUT',
  body: JSON.stringify({
    plugins: ['all']
  })
});

// Activate/deactivate plugin
await rocketApiRequest(`/sites/${siteId}/plugins`, {
  method: 'PATCH',
  body: JSON.stringify({
    plugins: ['wordfence'],
    action: 'activate' // or 'deactivate'
  })
});
```

### Execute WP-CLI Commands

```typescript
const result = await rocketApiRequest(`/sites/${siteId}/wpcli`, {
  method: 'POST',
  body: JSON.stringify({
    command: 'user list --format=json'
  })
});
```

### WordPress SSO Login

```typescript
// Get SSO link for WordPress admin
const { url } = await rocketApiRequest(`/sites/${siteId}/wp_login`);
// Redirect user to url for auto-login
```

## TypeScript Types

```typescript
interface RocketSite {
  id: number;
  name: string;
  domain: string;
  status: 'active' | 'suspended' | 'pending';
  location: string;
  created_at: string;
  updated_at: string;
}

interface RocketBackup {
  id: number;
  site_id: number;
  type: 'manual' | 'automated' | 'cloud';
  status: 'pending' | 'completed' | 'failed';
  size: number;
  created_at: string;
}

interface RocketPlugin {
  name: string;
  slug: string;
  version: string;
  status: 'active' | 'inactive';
  update_available: boolean;
}

interface RocketDomain {
  id: number;
  domain: string;
  is_main: boolean;
  ssl_status: 'pending' | 'active' | 'failed';
  validation_method: 'dns' | 'http';
}

interface RocketAuthResponse {
  token: string;
  expires_at: string;
}
```

## Error Handling

```typescript
interface RocketApiError {
  error: string;
  message: string;
  status: number;
}

async function handleRocketRequest(endpoint: string, options?: RequestInit) {
  try {
    const response = await rocketApiRequest(endpoint, options);
    return { data: response, error: null };
  } catch (error) {
    if (error.status === 401) {
      // Re-authenticate and retry
      await refreshToken();
      return handleRocketRequest(endpoint, options);
    }
    if (error.status === 404) {
      return { data: null, error: 'Resource not found' };
    }
    if (error.status === 429) {
      // Rate limited - wait and retry
      await sleep(1000);
      return handleRocketRequest(endpoint, options);
    }
    return { data: null, error: error.message };
  }
}
```

## Background Tasks

Many operations (clone, backup restore, staging publish) run as background tasks. Monitor task status:

```typescript
// Start a background task
const { task_id } = await rocketApiRequest(`/sites/${siteId}/clone`, {
  method: 'POST',
  body: JSON.stringify({ name: 'cloned-site' })
});

// Check task status
const tasks = await rocketApiRequest(`/sites/${siteId}/tasks`);
const task = tasks.find(t => t.id === task_id);
console.log(task.status); // 'pending', 'running', 'completed', 'failed'

// Cancel task if needed
await rocketApiRequest(`/sites/${siteId}/tasks/${task_id}/cancel`, {
  method: 'POST'
});
```

## Rate Limits

The API has rate limits. Implement exponential backoff:

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  delay = 1000
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.status === 429 && i < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, delay * Math.pow(2, i)));
        continue;
      }
      throw error;
    }
  }
  throw new Error('Max retries exceeded');
}
```

## References

- [Rocket.net API Documentation](https://rocketdotnet.readme.io/reference/introduction)
- [Rocket.net Control Panel](https://control.rocket.net)
- [Rocket.net WordPress Hosting](https://rocket.net)

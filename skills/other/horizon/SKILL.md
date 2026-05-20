---
name: openstack-horizon
description: "OpenStack Horizon web dashboard skill. Use when deploying, customizing, or troubleshooting the OpenStack web UI. Covers panel customization, session management, multi-domain support, theme branding, TLS configuration, and common dashboard failure modes including login issues, missing panels, and static asset problems."
user-invocable: true
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-23"
      triggers:
        intents:
          - "horizon"
          - "dashboard"
          - "web console"
          - "web ui"
          - "panel"
          - "theme"
        contexts:
          - "deploying openstack dashboard"
          - "customizing horizon"
          - "troubleshooting web interface"
          - "configuring dashboard access"
---

# OpenStack Horizon -- Web Dashboard

## Introduction

Horizon is the web-based dashboard for OpenStack cloud operators and users. It provides a graphical interface to OpenStack services -- launching instances, managing networks, creating volumes, viewing images, and administering projects and users -- without requiring CLI or API knowledge. Horizon is built on the Django web framework and uses a plugin architecture where each OpenStack service contributes panels to the dashboard.

The dashboard organizes content into three panel groups: **Project** (user-facing resource management), **Admin** (cloud administrator operations), and **Identity** (Keystone user/project/domain management). Each panel group loads dynamically based on the user's Keystone role -- a regular user sees only Project panels, while an admin sees all three groups.

Horizon authenticates through Keystone sessions. When a user logs in through the dashboard, Horizon obtains a Keystone token and stores it in the session backend. All subsequent API calls from the dashboard use this token, meaning Horizon respects the same RBAC policies as the CLI and API. Horizon does not have its own user database -- all authentication and authorization flows through Keystone.

## Deploy

Horizon deployment via Kolla-Ansible requires enabling the service in `globals.yml`:

```yaml
# /etc/kolla/globals.yml
enable_horizon: "yes"

# TLS for HTTPS access (recommended for production)
kolla_enable_tls_external: "yes"
kolla_external_fqdn_cert: "/etc/kolla/certificates/haproxy.pem"
```

After deployment, Horizon runs as a container behind HAProxy (or nginx, depending on configuration). The default access port is 443 (HTTPS) or 80 (HTTP) on the external VIP address.

**Verification commands:**

```bash
# Verify Horizon container is running
docker ps --filter name=horizon

# Check container health
docker inspect --format '{{.State.Health.Status}}' horizon

# Verify HAProxy routing to Horizon
curl -sI https://<kolla_external_vip_address>/auth/login/ | head -5

# Verify web service is responsive (expect 200 or 302)
curl -so /dev/null -w "%{http_code}" https://<kolla_external_vip_address>/auth/login/
```

**Initial admin login:** After `kolla-ansible post-deploy`, the admin credentials are stored in `/etc/kolla/admin-openrc.sh`. The default admin user is `admin` in the `default` domain. The password is the value of `keystone_admin_password` in `/etc/kolla/passwords.yml`.

## Configure

### Session Backend

Horizon stores user sessions in a backend -- the choice affects performance and reliability:

```python
# Memcached (default in Kolla-Ansible, recommended)
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': 'memcached:11211',
    }
}

# Database (more durable, slower)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
```

Session timeout controls how long a user stays logged in:

```python
SESSION_TIMEOUT = 3600          # 1 hour (seconds)
SESSION_COOKIE_SECURE = True    # Requires HTTPS
SESSION_COOKIE_HTTPONLY = True   # Prevent JavaScript access
```

### Multi-Domain Support

For clouds with multiple Keystone domains:

```python
OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = True
OPENSTACK_KEYSTONE_DEFAULT_DOMAIN = 'Default'
```

When enabled, the login page shows a "Domain" field. Users must specify their domain to authenticate.

### Panel Visibility

Enable or disable specific dashboard panels:

```python
# Disable panels users shouldn't access
OPENSTACK_NEUTRON_NETWORK = {
    'enable_router': True,
    'enable_quotas': True,
    'enable_distributed_router': False,
    'enable_ha_router': False,
    'enable_fip_topology_check': True,
}

# Hide specific panels
OPENSTACK_HEAT_STACK = {
    'enable': True  # Set False to hide Heat panels
}
```

### Custom Branding

Kolla-Ansible supports Horizon customization through config overrides:

```
# Override directory structure
/etc/kolla/config/horizon/
  custom_local_settings    # Python settings overrides
  themes/                  # Custom theme directory
    mytheme/
      static/
        _styles.scss       # Custom CSS
        img/
          logo.svg         # Custom logo
          logo-splash.svg  # Login page logo
          favicon.ico      # Browser favicon
```

Key branding settings:

```python
SITE_BRANDING = "My Cloud Dashboard"
AVAILABLE_THEMES = [
    ('default', 'Default', 'themes/default'),
    ('mytheme', 'My Theme', 'themes/mytheme'),
]
DEFAULT_THEME = 'mytheme'
```

### Security Settings

```python
# ALLOWED_HOSTS must match the hostname users access
ALLOWED_HOSTS = ['*']  # Restrict in production: ['cloud.example.com']

# CSRF protection
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# API endpoint configuration
OPENSTACK_KEYSTONE_URL = "http://keystone-internal:5000/v3"
OPENSTACK_API_VERSIONS = {
    "identity": 3,
    "image": 2,
    "volume": 3,
}
```

### Kolla-Ansible Config Overrides

To apply customizations in a Kolla-Ansible managed deployment:

```bash
# Place custom settings in the override file
mkdir -p /etc/kolla/config/horizon/
cat > /etc/kolla/config/horizon/custom_local_settings << 'EOF'
SESSION_TIMEOUT = 7200
SITE_BRANDING = "Production Cloud"
OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = True
EOF

# Apply changes
kolla-ansible -i all-in-one reconfigure --tags horizon
```

## Operate

### User Access Management

Horizon does not manage users directly -- all user management flows through Keystone:

```bash
# Create a user (via CLI, reflected in Horizon)
openstack user create --domain default --password changeme newuser

# Assign role in project (grants Horizon panel access)
openstack role add --project myproject --user newuser member

# List users visible in Horizon admin panel
openstack user list --domain default
```

### Session Monitoring

```bash
# Check memcached session statistics
docker exec -it memcached sh -c 'echo "stats" | nc localhost 11211'

# Monitor active sessions (look for curr_items)
docker exec -it memcached sh -c 'echo "stats" | nc localhost 11211 | grep curr_items'
```

### Cache Management

```bash
# Flush memcached cache (forces all users to re-authenticate)
docker exec -it memcached sh -c 'echo "flush_all" | nc localhost 11211'

# Restart Horizon to clear internal caches
docker restart horizon
```

### Log Analysis

```bash
# Horizon application logs
docker logs horizon
docker logs horizon --tail 100 --follow

# Access logs (requests to the dashboard)
docker exec horizon cat /var/log/kolla/horizon/horizon.log

# Error-specific filtering
docker logs horizon 2>&1 | grep -i "error\|exception\|traceback"
```

### Performance Tuning

- **Session timeout:** Balance security (shorter timeout) vs usability (longer timeout). Default 3600s is reasonable for most deployments.
- **Compression:** Enable gzip compression in the web server configuration to reduce page load times.
- **Static assets:** Ensure `collectstatic` has been run (Kolla-Ansible handles this automatically). Static assets should be served directly by the web server, not Django.
- **Caching:** Memcached should have enough memory allocated for the expected number of concurrent sessions. Each session uses approximately 2-4 KB.

## Troubleshoot

### 500 Internal Server Error

**Memcached down:**
Horizon stores sessions in memcached by default. If memcached is unreachable, every request fails with a 500 error. Check: `docker ps --filter name=memcached` -- if the container is not running, restart it: `docker restart memcached`. Verify connectivity: `docker exec horizon python -c "import socket; s=socket.create_connection(('memcached', 11211)); print('OK')"`.

**Keystone unreachable:**
If Horizon cannot reach the Keystone API, all operations fail. Check: `docker exec horizon curl -s http://keystone-internal:5000/v3/ | python -m json.tool`. If Keystone is down, restart it first -- Horizon depends on Keystone for every operation.

**Session backend failure:**
If the configured session backend is corrupted or full, sessions cannot be created. For memcached: check `evictions` metric (high evictions mean memcached needs more memory). For database: check disk space and database connectivity.

### Login Fails

**Keystone endpoint misconfigured:**
The `OPENSTACK_KEYSTONE_URL` in Horizon's settings must match a reachable Keystone endpoint. If Kolla-Ansible changed the VIP or internal endpoint, Horizon's configuration may be stale. Fix: reconfigure Horizon via `kolla-ansible reconfigure --tags horizon`.

**Domain not set:**
With multi-domain support enabled, users must specify their domain at login. If `OPENSTACK_KEYSTONE_DEFAULT_DOMAIN` is not set correctly, users in the default domain may not be able to log in without explicitly entering "Default" in the domain field.

**CSRF token mismatch:**
Occurs when the browser's CSRF cookie does not match the form token. Common causes: browser cache from a previous deployment, HTTPS/HTTP mixed content, reverse proxy stripping headers. Fix: clear browser cookies, verify `CSRF_COOKIE_SECURE` matches the protocol (True only for HTTPS).

**Authentication timeout:**
Horizon's request to Keystone times out. Check network connectivity between the Horizon container and Keystone, and verify Keystone is responsive: `openstack token issue`.

### Panels Missing or Broken

**Service not registered in catalog:**
Horizon discovers available panels by querying the Keystone service catalog. If a service (e.g., Heat) is not registered, its panels do not appear. Verify: `openstack catalog list`. If a service is missing, register it via Keystone or re-run `kolla-ansible post-deploy`.

**API version mismatch:**
Horizon expects specific API versions. If the `OPENSTACK_API_VERSIONS` dictionary does not match the deployed service versions, panels may load but fail to display data. Verify API versions: `openstack versions show`.

### Session Timeout Too Aggressive

**Memcached eviction:**
If memcached runs out of memory, it evicts the least-recently-used sessions. Users experience unexpected logouts. Check eviction rate: `echo "stats" | nc memcached 11211 | grep evictions`. If high, increase memcached memory allocation in Kolla-Ansible globals.yml: `memcached_max_memory: 512` (MB).

**Session backend configuration:**
The `SESSION_TIMEOUT` value controls inactivity timeout. If set too low, users are logged out frequently. The default is 3600 seconds (1 hour). For operator environments where users work in the dashboard continuously, consider increasing to 7200 or higher.

### Static Assets Not Loading

**Nginx/web server configuration:**
If CSS, JavaScript, or images fail to load, check the web server configuration. In Kolla-Ansible deployments, HAProxy routes to the Horizon container which serves static files. Verify: `curl -sI https://<vip>/static/dashboard/css/style.css | head -5` -- should return 200.

**STATIC_ROOT misconfiguration:**
If `collectstatic` was not run or `STATIC_ROOT` points to the wrong directory, static files are missing from the filesystem. In Kolla-Ansible deployments, this is handled automatically during container build. If static files are missing after a reconfigure: `docker restart horizon`.

**Browser caching stale assets:**
After an upgrade, the browser may cache old CSS/JS files. Clear browser cache or use incognito mode to verify. Horizon includes cache-busting hashes in asset URLs, but custom themes may not.

## Integration Points

- **Keystone:** All authentication flows through Keystone. Horizon obtains scoped tokens for each API call. Multi-domain support requires Keystone v3 API. The service catalog from Keystone determines which panels are available.
- **All OpenStack services:** Horizon acts as an API proxy -- when a user creates an instance through the dashboard, Horizon makes the equivalent API call to Nova. Every service panel makes API calls to its respective service. Horizon does not cache service data (except for session-related state).
- **Heat:** Horizon includes a template editor and stack management UI that interfaces with the Heat API. Users can upload HOT templates, view stack resources, and monitor stack events through the dashboard.
- **Neutron:** The network topology visualization panel provides a graphical view of networks, subnets, routers, and their connections. This panel queries the Neutron API for the current network state.

## NASA SE Cross-References

- **Phase C (Final Design and Fabrication):** Dashboard deployment configuration maps to the fabrication phase (SP-6105 SS 5.1). Horizon branding, panel configuration, and session settings are "build" artifacts that implement the UI design specification.
- **Phase D (Integration and Test):** Dashboard verification -- confirming login works, all expected panels load, API proxying functions correctly -- maps to integration testing (SP-6105 SS 5.2-5.3). The dashboard provides a visual confirmation that all service integrations are functioning.
- **Phase E (Operations and Sustainment):** The dashboard is the primary operator interface during the operations phase (SP-6105 SS 5.4-5.5). User management, resource monitoring, and operational tasks performed through Horizon represent day-2 cloud operations. Session monitoring and performance tuning are sustainment activities.

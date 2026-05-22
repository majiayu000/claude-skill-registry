---
name: haproxy
description: HAProxy load balancer configuration and management. Set up TCP/HTTP load balancing, SSL termination, health checks, ACLs, and high availability. Use when working with HAProxy, load balancing, reverse proxy, TCP proxying, or high-traffic applications.
---

# HAProxy Load Balancer Skill

Configure and manage HAProxy for high-performance load balancing, SSL termination, and reverse proxying.

## Triggers

Use this skill when you see:
- haproxy, ha proxy, load balancer
- tcp proxy, http proxy, reverse proxy
- ssl termination, health check
- backend server, frontend, acl

## Instructions

### Basic Configuration Structure

```bash
# /etc/haproxy/haproxy.cfg

global
    log /dev/log local0
    log /dev/log local1 notice
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s
    user haproxy
    group haproxy
    daemon
    maxconn 4096

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    timeout connect 5000
    timeout client  50000
    timeout server  50000
    errorfile 400 /etc/haproxy/errors/400.http
    errorfile 403 /etc/haproxy/errors/403.http
    errorfile 408 /etc/haproxy/errors/408.http
    errorfile 500 /etc/haproxy/errors/500.http
    errorfile 502 /etc/haproxy/errors/502.http
    errorfile 503 /etc/haproxy/errors/503.http
    errorfile 504 /etc/haproxy/errors/504.http
```

### HTTP Load Balancing

```bash
frontend http_front
    bind *:80
    default_backend http_back
    option forwardfor

backend http_back
    balance roundrobin
    option httpchk GET /health
    http-check expect status 200
    server web1 192.168.1.10:8080 check
    server web2 192.168.1.11:8080 check
    server web3 192.168.1.12:8080 check backup
```

### HTTPS with SSL Termination

```bash
frontend https_front
    bind *:443 ssl crt /etc/haproxy/certs/combined.pem
    bind *:80
    redirect scheme https code 301 if !{ ssl_fc }
    default_backend https_back

    # HSTS header
    http-response set-header Strict-Transport-Security "max-age=31536000; includeSubDomains"

backend https_back
    balance leastconn
    option httpchk GET /health
    server web1 192.168.1.10:8080 check
    server web2 192.168.1.11:8080 check
```

### TCP Load Balancing

```bash
frontend tcp_front
    bind *:3306
    mode tcp
    default_backend mysql_back

backend mysql_back
    mode tcp
    balance roundrobin
    option mysql-check user haproxy
    server db1 192.168.1.20:3306 check
    server db2 192.168.1.21:3306 check backup
```

### ACL-Based Routing

```bash
frontend http_front
    bind *:80

    # Define ACLs
    acl is_api path_beg /api
    acl is_static path_beg /static
    acl is_admin path_beg /admin
    acl host_app hdr(host) -i app.example.com
    acl host_api hdr(host) -i api.example.com

    # Route based on ACLs
    use_backend api_back if is_api
    use_backend api_back if host_api
    use_backend static_back if is_static
    use_backend admin_back if is_admin
    default_backend app_back

backend api_back
    balance roundrobin
    server api1 192.168.1.30:8080 check
    server api2 192.168.1.31:8080 check

backend static_back
    balance roundrobin
    server static1 192.168.1.40:80 check

backend admin_back
    balance roundrobin
    server admin1 192.168.1.50:8080 check

backend app_back
    balance roundrobin
    server app1 192.168.1.10:8080 check
    server app2 192.168.1.11:8080 check
```

### Health Checks

```bash
backend http_back
    # HTTP health check
    option httpchk GET /health HTTP/1.1\r\nHost:\ localhost
    http-check expect status 200

    # Advanced health check
    http-check send meth GET uri /health ver HTTP/1.1 hdr Host localhost
    http-check expect status 200

    server web1 192.168.1.10:8080 check inter 3000 fall 3 rise 2
    server web2 192.168.1.11:8080 check inter 3000 fall 3 rise 2

backend tcp_back
    mode tcp
    option tcp-check
    tcp-check connect
    tcp-check send PING\r\n
    tcp-check expect string +PONG
    server redis1 192.168.1.60:6379 check
```

### Rate Limiting

```bash
frontend http_front
    bind *:80

    # Define rate limit table
    stick-table type ip size 100k expire 30s store http_req_rate(10s)

    # Track requests per IP
    http-request track-sc0 src

    # Deny if rate exceeds 100 requests per 10 seconds
    http-request deny deny_status 429 if { sc_http_req_rate(0) gt 100 }

    default_backend http_back
```

### Session Persistence (Sticky Sessions)

```bash
backend app_back
    balance roundrobin
    cookie SERVERID insert indirect nocache

    server web1 192.168.1.10:8080 check cookie web1
    server web2 192.168.1.11:8080 check cookie web2
```

### Stats Dashboard

```bash
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 10s
    stats auth admin:password
    stats admin if LOCALHOST
```

### Logging Configuration

```bash
global
    log 127.0.0.1:514 local0 info
    log 127.0.0.1:514 local1 notice

defaults
    log global
    option httplog
    option dontlognull

    # Custom log format
    log-format "%ci:%cp [%tr] %ft %b/%s %TR/%Tw/%Tc/%Tr/%Ta %ST %B %CC %CS %tsc %ac/%fc/%bc/%sc/%rc %sq/%bq %hr %hs %{+Q}r"
```

### Docker Compose Example

```yaml
version: '3.8'

services:
  haproxy:
    image: haproxy:2.8
    ports:
      - "80:80"
      - "443:443"
      - "8404:8404"
    volumes:
      - ./haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro
      - ./certs:/etc/haproxy/certs:ro
    restart: unless-stopped
    networks:
      - app-network

  web1:
    image: nginx:alpine
    networks:
      - app-network

  web2:
    image: nginx:alpine
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### Common Commands

```bash
# Check configuration
haproxy -c -f /etc/haproxy/haproxy.cfg

# Reload configuration (graceful)
sudo systemctl reload haproxy

# View stats via socket
echo "show stat" | sudo socat stdio /run/haproxy/admin.sock

# Disable server
echo "disable server http_back/web1" | sudo socat stdio /run/haproxy/admin.sock

# Enable server
echo "enable server http_back/web1" | sudo socat stdio /run/haproxy/admin.sock

# View server status
echo "show servers state" | sudo socat stdio /run/haproxy/admin.sock
```

## Best Practices

1. **Health Checks**: Always configure health checks for backends
2. **Timeouts**: Set appropriate timeouts for your application
3. **SSL**: Use strong ciphers and enable HSTS
4. **Logging**: Enable detailed logging for troubleshooting
5. **Stats**: Enable stats page for monitoring (protect with auth)
6. **Backup Servers**: Configure backup servers for failover

## Common Workflows

### Set Up Load Balancer
1. Install HAProxy: `apt install haproxy`
2. Configure frontend and backend
3. Set up health checks
4. Test configuration: `haproxy -c -f /etc/haproxy/haproxy.cfg`
5. Start service: `systemctl start haproxy`
6. Monitor via stats page

### Add SSL Termination
1. Obtain SSL certificate
2. Combine cert and key: `cat cert.pem key.pem > combined.pem`
3. Configure HTTPS frontend with SSL binding
4. Add HTTP to HTTPS redirect
5. Reload configuration

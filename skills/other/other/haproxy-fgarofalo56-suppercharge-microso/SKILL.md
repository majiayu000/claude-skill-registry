---
name: haproxy
description: "Configure HAProxy for load balancing, reverse proxying, and high availability. Set up health checks, SSL termination, rate limiting, and traffic management. Use for load balancing and proxy configurations."
---

# HAProxy Skill

Complete guide for HAProxy - the reliable, high-performance TCP/HTTP load balancer.

## Quick Reference

### Configuration Sections
| Section | Purpose |
|---------|---------|
| **global** | Process-wide settings |
| **defaults** | Default settings for all sections |
| **frontend** | Client-facing listeners |
| **backend** | Server pools |
| **listen** | Combined frontend/backend |

### Key Files
```
/etc/haproxy/haproxy.cfg    # Main config
/var/log/haproxy.log        # Logs
/var/run/haproxy/admin.sock # Admin socket
```

---

## 1. Installation

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install haproxy

# Enable and start
sudo systemctl enable haproxy
sudo systemctl start haproxy
```

### CentOS/RHEL
```bash
sudo dnf install haproxy
sudo systemctl enable haproxy
sudo systemctl start haproxy
```

### Docker
```yaml
services:
  haproxy:
    image: haproxy:latest
    container_name: haproxy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
      - "8404:8404"
    volumes:
      - ./haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro
      - ./certs:/etc/ssl/certs:ro
```

---

## 2. Basic Configuration

### Minimal haproxy.cfg
```cfg
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
    timeout connect 5s
    timeout client  50s
    timeout server  50s
    errorfile 400 /etc/haproxy/errors/400.http
    errorfile 403 /etc/haproxy/errors/403.http
    errorfile 408 /etc/haproxy/errors/408.http
    errorfile 500 /etc/haproxy/errors/500.http
    errorfile 502 /etc/haproxy/errors/502.http
    errorfile 503 /etc/haproxy/errors/503.http
    errorfile 504 /etc/haproxy/errors/504.http

frontend http_front
    bind *:80
    default_backend http_back

backend http_back
    balance roundrobin
    server server1 192.168.1.10:80 check
    server server2 192.168.1.11:80 check
```

---

## 3. Load Balancing Algorithms

### Round Robin (Default)
```cfg
backend http_back
    balance roundrobin
    server server1 192.168.1.10:80 check
    server server2 192.168.1.11:80 check
```

### Least Connections
```cfg
backend http_back
    balance leastconn
    server server1 192.168.1.10:80 check
    server server2 192.168.1.11:80 check
```

### Source IP Hash (Sticky)
```cfg
backend http_back
    balance source
    hash-type consistent
    server server1 192.168.1.10:80 check
    server server2 192.168.1.11:80 check
```

### Weighted Round Robin
```cfg
backend http_back
    balance roundrobin
    server server1 192.168.1.10:80 weight 3 check
    server server2 192.168.1.11:80 weight 1 check
```

### URI Hash
```cfg
backend http_back
    balance uri
    hash-type consistent
    server server1 192.168.1.10:80 check
    server server2 192.168.1.11:80 check
```

---

## 4. Health Checks

### HTTP Health Check
```cfg
backend http_back
    balance roundrobin
    option httpchk GET /health
    http-check expect status 200
    server server1 192.168.1.10:80 check inter 5s fall 3 rise 2
    server server2 192.168.1.11:80 check inter 5s fall 3 rise 2
```

### TCP Health Check
```cfg
backend tcp_back
    mode tcp
    balance roundrobin
    option tcp-check
    server server1 192.168.1.10:3306 check inter 5s
    server server2 192.168.1.11:3306 check inter 5s
```

### Health Check Options
```cfg
# inter: check interval
# fall: failures before marking down
# rise: successes before marking up
# slowstart: gradual traffic increase after recovery

server server1 192.168.1.10:80 check inter 3s fall 3 rise 2 slowstart 60s
```

---

## 5. SSL/TLS Termination

### HTTPS Frontend
```cfg
frontend https_front
    bind *:443 ssl crt /etc/ssl/certs/combined.pem
    mode http
    default_backend http_back
```

### Combined Certificate (PEM)
```bash
# Combine certificate and key
cat certificate.crt ca-bundle.crt private.key > combined.pem
chmod 600 combined.pem
```

### SSL with Redirect
```cfg
frontend http_front
    bind *:80
    mode http
    redirect scheme https code 301 if !{ ssl_fc }

frontend https_front
    bind *:443 ssl crt /etc/ssl/certs/combined.pem
    mode http
    default_backend http_back
```

### SSL Passthrough
```cfg
frontend tcp_front
    bind *:443
    mode tcp
    default_backend tcp_back

backend tcp_back
    mode tcp
    server server1 192.168.1.10:443 check
```

### Multiple Certificates (SNI)
```cfg
frontend https_front
    bind *:443 ssl crt /etc/ssl/certs/
    # All .pem files in directory are loaded
    # HAProxy selects based on SNI
```

---

## 6. ACLs and Routing

### Host-Based Routing
```cfg
frontend http_front
    bind *:80
    acl is_api hdr(host) -i api.example.com
    acl is_web hdr(host) -i www.example.com

    use_backend api_back if is_api
    use_backend web_back if is_web
    default_backend web_back
```

### Path-Based Routing
```cfg
frontend http_front
    bind *:80
    acl is_api path_beg /api
    acl is_static path_beg /static

    use_backend api_back if is_api
    use_backend static_back if is_static
    default_backend web_back
```

### Method-Based Routing
```cfg
frontend http_front
    bind *:80
    acl is_post method POST
    acl is_get method GET

    use_backend write_back if is_post
    use_backend read_back if is_get
```

### IP-Based ACL
```cfg
frontend http_front
    bind *:80
    acl is_internal src 192.168.0.0/16 10.0.0.0/8

    use_backend internal_back if is_internal
    default_backend public_back
```

---

## 7. Session Persistence

### Cookie-Based
```cfg
backend http_back
    balance roundrobin
    cookie SERVERID insert indirect nocache
    server server1 192.168.1.10:80 check cookie s1
    server server2 192.168.1.11:80 check cookie s2
```

### Stick Tables
```cfg
backend http_back
    balance roundrobin
    stick-table type ip size 200k expire 30m
    stick on src
    server server1 192.168.1.10:80 check
    server server2 192.168.1.11:80 check
```

### Application Cookie
```cfg
backend http_back
    balance roundrobin
    cookie JSESSIONID prefix nocache
    server server1 192.168.1.10:80 check cookie s1
    server server2 192.168.1.11:80 check cookie s2
```

---

## 8. Rate Limiting

### Connection Rate Limiting
```cfg
frontend http_front
    bind *:80
    stick-table type ip size 100k expire 30s store conn_cur,conn_rate(3s)

    # Deny if more than 20 connections per 3 seconds
    acl too_fast src_conn_rate gt 20
    tcp-request connection reject if too_fast
```

### Request Rate Limiting
```cfg
frontend http_front
    bind *:80
    stick-table type ip size 100k expire 30s store http_req_rate(10s)

    # Tarpit (slow down) if more than 100 requests per 10 seconds
    acl too_many_requests src_http_req_rate gt 100
    http-request tarpit if too_many_requests
```

### Per-URL Rate Limiting
```cfg
frontend http_front
    bind *:80
    stick-table type string len 128 size 100k expire 30s store http_req_rate(10s)

    # Track by URL path
    http-request track-sc0 path
    acl api_abuse sc0_http_req_rate gt 50
    http-request deny if api_abuse { path_beg /api }
```

---

## 9. Stats and Monitoring

### Stats Page
```cfg
listen stats
    bind *:8404
    mode http
    stats enable
    stats uri /stats
    stats refresh 30s
    stats admin if LOCALHOST
    stats auth admin:password
```

### Prometheus Metrics
```cfg
frontend stats
    bind *:8405
    mode http
    http-request use-service prometheus-exporter if { path /metrics }
    stats enable
    stats uri /stats
```

### Runtime API
```cfg
global
    stats socket /var/run/haproxy/admin.sock mode 660 level admin

# Usage
echo "show stat" | socat stdio /var/run/haproxy/admin.sock
echo "show servers state" | socat stdio /var/run/haproxy/admin.sock
echo "disable server http_back/server1" | socat stdio /var/run/haproxy/admin.sock
```

---

## 10. High Availability

### Keepalived Integration
```cfg
# /etc/keepalived/keepalived.conf
vrrp_script chk_haproxy {
    script "killall -0 haproxy"
    interval 2
    weight 2
}

vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 101
    advert_int 1

    virtual_ipaddress {
        192.168.1.100
    }

    track_script {
        chk_haproxy
    }
}
```

### Graceful Reload
```bash
# Check config
haproxy -c -f /etc/haproxy/haproxy.cfg

# Graceful reload
systemctl reload haproxy

# Or manual
haproxy -f /etc/haproxy/haproxy.cfg -sf $(cat /var/run/haproxy.pid)
```

---

## 11. TCP Load Balancing

### Database (MySQL)
```cfg
listen mysql
    bind *:3306
    mode tcp
    balance leastconn
    option mysql-check user haproxy
    server mysql1 192.168.1.10:3306 check
    server mysql2 192.168.1.11:3306 check backup
```

### Redis
```cfg
listen redis
    bind *:6379
    mode tcp
    balance first
    option tcp-check
    tcp-check send PING\r\n
    tcp-check expect string +PONG
    server redis1 192.168.1.10:6379 check inter 1s
    server redis2 192.168.1.11:6379 check inter 1s
```

### SMTP
```cfg
listen smtp
    bind *:25
    mode tcp
    balance roundrobin
    server smtp1 192.168.1.10:25 check
    server smtp2 192.168.1.11:25 check
```

---

## 12. Troubleshooting

### Common Issues

**Connection refused:**
```bash
# Check HAProxy is running
systemctl status haproxy

# Check ports
ss -tlnp | grep haproxy

# Check backend servers
curl -v http://192.168.1.10:80/
```

**503 Service Unavailable:**
```bash
# Check backend health
echo "show servers state" | socat stdio /var/run/haproxy/admin.sock

# View stats page
# http://haproxy-ip:8404/stats
```

**Configuration errors:**
```bash
# Validate config
haproxy -c -f /etc/haproxy/haproxy.cfg

# View logs
journalctl -u haproxy -f
tail -f /var/log/haproxy.log
```

### Debug Mode
```cfg
global
    log stdout format raw local0 debug

defaults
    log global
    option httplog
```

### Useful Commands
```bash
# Show stat summary
echo "show stat" | socat stdio /var/run/haproxy/admin.sock | cut -d, -f1,2,18

# Show errors
echo "show errors" | socat stdio /var/run/haproxy/admin.sock

# Enable/disable server
echo "disable server http_back/server1" | socat stdio /var/run/haproxy/admin.sock
echo "enable server http_back/server1" | socat stdio /var/run/haproxy/admin.sock

# Set server weight
echo "set server http_back/server1 weight 50" | socat stdio /var/run/haproxy/admin.sock
```

---

## Best Practices

1. **Always validate config** before reload: `haproxy -c -f config`
2. **Use health checks** on all backends
3. **Enable logging** for debugging and monitoring
4. **Set appropriate timeouts** - not too short, not too long
5. **Use ACLs** for complex routing logic
6. **Monitor with stats page** or Prometheus
7. **Use keepalived** for HAProxy high availability
8. **Secure stats page** with authentication and IP restrictions
9. **Use stick tables** for rate limiting and abuse prevention
10. **Regular config backups** before changes

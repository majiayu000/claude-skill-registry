---
name: nginx
description: Nginx ops skill for configuring and operating Nginx as reverse proxy, web server, and ingress layer. Use for tasks like writing safe nginx.conf/server blocks, TLS, HTTP/2, caching, rate limiting, load balancing, observability, and troubleshooting 4xx/5xx, timeouts, and performance issues.
---

# nginx

Use this skill for Nginx 配置、发布与故障排查（ops）。

## Defaults / assumptions to confirm

- Nginx distribution and version (open source vs Plus)
- Deployment: bare metal/VM, Docker, or Kubernetes ingress-controller
- TLS termination location and certificate management
- Upstream architecture (services, ports, health endpoints)

## Workflow

1) Understand traffic and requirements
- Domains, paths, upstream services, expected QPS.
- Timeouts, max upload size, websocket needs.
- Caching requirements and security constraints.

2) Safe baseline config
- Use explicit `server_name`, `listen`, and `default_server` strategy.
- Set `client_max_body_size` intentionally.
- Configure `proxy_*` headers correctly (Host, X-Forwarded-For, X-Request-Id).
- Define `error_page` handling and static error responses if needed.

3) TLS / security
- Use modern TLS settings; disable legacy protocols/ciphers.
- Enable HSTS where appropriate.
- Add basic security headers if not handled elsewhere.
- Rate limit sensitive endpoints (login, OTP) with `limit_req`.

4) Performance
- Enable gzip/brotli if appropriate.
- Tune keepalive, buffers, and timeouts.
- Use upstream keepalive and connection reuse.
- Avoid expensive regex locations on hot paths.

5) Load balancing & resilience
- Use upstreams with health checks (where available) and failover settings.
- Configure retries carefully to avoid retry storms.
- Support websocket upgrade when needed.

6) Observability
- Access log format with request_id, upstream_time, status, bytes, user agent.
- Error log level appropriate for production.
- Export metrics if using nginx-prometheus-exporter or ingress metrics.

7) Troubleshooting checklist
- 4xx: routing, auth, body size, CORS, client IP headers.
- 5xx: upstream failures, timeouts, DNS issues, connection limits.
- Timeouts: `proxy_read_timeout`, upstream latency, buffer/backpressure.
- Performance: worker processes, file descriptors, CPU, TLS overhead.

## Outputs

- Proposed config snippets with rationale.
- Rollout plan (test config, reload vs restart, rollback steps).
- Debug report (symptom → evidence → root cause → fix).


---
name: public-web-deploy
description: "Publish a public website safely: DNS, web server, HTTPS, hardening, verify. Routes raw dev servers through nginx/Caddy/Apache/Cloudflare Pages."
user-invocable: false
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
routing:
  force_route: true
  triggers:
    - "public site"
    - "public website"
    - "static site"
    - "landing page"
    - "deploy website"
    - "deploy site"
    - "host a website"
    - "serve this website"
    - "put this online"
    - "put site online"
    - "website online"
    - "make it public"
    - "make public"
    - "use my domain"
    - "point my domain"
    - "set up https"
    - "nginx public site"
    - "go live"
  category: infrastructure
  not_for: "domain MODELING / DDD bounded contexts (use a code agent); local-only preview on 127.0.0.1 (no deploy needed); generating HTML artifacts (use html-artifact); HTTPS client/API bugs and internal-only nginx reverse proxies (use a code/infra agent). Fires when a site goes internet-facing."
  pairs_with:
    - shell-process-patterns
    - service-health-check
    - kubernetes-security
---

# Public Web Deploy Skill

## Top Rule

Serve public sites through a real web server. Local preview binds `127.0.0.1`; public sites go through nginx, Caddy, Apache, or Cloudflare Pages — fronted by HTTPS and hardened nginx config.

> Never use `python -m http.server`, Vite, Hugo, Next dev, Flask dev, or any raw dev server as an internet-facing public service. Local preview MUST bind 127.0.0.1. Public sites MUST go through nginx / Caddy / Apache / Cloudflare Pages.

Raw dev servers are single-threaded, unauthenticated, serve the whole working directory (dotfiles, `.env`, `.git`, source, backups), carry no TLS, no rate limiting, and no request filtering. They are correct for `127.0.0.1` local preview and wrong for any internet-facing service. A companion enforcement hook blocks public binds at the tool layer; this skill is the guidance that pairs with it.

**Decide public vs private first.** A public site is reached by HTTPS + hardened nginx — that *is* the security model. Reserve auth (basic-auth, SSO) for private/internal sites, decided explicitly. Adding basic-auth to a public site breaks it for its intended audience and adds no protection to content meant to be public.

---

## Instructions

### Phase 1: DNS

**Goal**: The domain/subdomain resolves to the host before any web server work.

**Steps**:
1. Confirm the target FQDN (apex `example.com`, subdomain `app.example.com`).
2. Create an `A`/`AAAA` record pointing at the host's public IP (or `CNAME` for managed platforms like Cloudflare Pages).
3. Verify resolution propagated:
   ```bash
   dig +short A app.example.com
   dig +short AAAA app.example.com
   getent hosts app.example.com
   ```

**Gate**: `dig +short` returns the intended host IP. Proceed only when DNS resolves correctly — an HTTPS cert request fails if DNS does not yet point at the host.

### Phase 2: Web Server Config

**Goal**: A production web server (not a dev server) serves the site from a defined docroot.

**Steps**:
1. Pick the server: nginx or Caddy (self-hosted), Apache (existing stacks), or Cloudflare Pages (managed static).
2. Define a server block bound to the FQDN with an explicit docroot:
   ```nginx
   server {
       listen 80;
       server_name app.example.com;
       root /var/www/app.example.com;
       index index.html;
       location / { try_files $uri $uri/ =404; }
   }
   ```
3. If an app backend exists, proxy to it on `127.0.0.1`:
   ```nginx
   location /api/ { proxy_pass http://127.0.0.1:8000; }
   ```
   The backend binds `127.0.0.1`, never `0.0.0.0` — only nginx faces the internet.
4. Test config and reload:
   ```bash
   nginx -t && systemctl reload nginx
   ```

**Gate**: `nginx -t` reports syntax OK and the site responds on port 80. The application/dev port is reachable only on `127.0.0.1`.

### Phase 3: HTTPS

**Goal**: Valid TLS cert installed, auto-renewal proven, HTTP redirects to HTTPS.

**Steps**:
1. Issue a cert (Let's Encrypt via certbot, or Caddy/Cloudflare automatic TLS):
   ```bash
   certbot --nginx -d app.example.com
   ```
2. Prove renewal works before trusting it:
   ```bash
   certbot renew --dry-run
   ```
3. Confirm the HTTP->HTTPS redirect returns a 301/308 to `https://` (certbot's nginx installer adds it; verify both the status and the target):
   ```bash
   curl -sI http://app.example.com | grep -iE '^HTTP/.* (301|308)'
   curl -sI http://app.example.com | grep -i '^location: https'
   ```

**Gate**: HTTPS serves a valid chain, `certbot renew --dry-run` exits 0, and plain HTTP 301/308-redirects to HTTPS. Proceed only when all three hold.

### Phase 4: Hardening

**Goal**: Lock the surface to the minimum needed to serve the site.

**Steps**:
1. Firewall — allow only intended ports. UFW applies to both IPv4 and IPv6 when `IPV6=yes` in `/etc/default/ufw`; confirm v6 parity if the host has an `AAAA` record:
   ```bash
   ufw allow 80/tcp
   ufw allow 443/tcp
   ufw allow OpenSSH
   ufw --force enable          # --force skips the interactive prompt
   ufw status verbose          # entries show (v6) duplicates when IPv6 is on
   ```
   No raw app/dev ports (8000, 5173, 1313, 3000…) appear in `ufw status`.
2. nginx — deny sensitive paths, disable directory listing, restrict methods:
   ```nginx
   autoindex off;   # no directory listing (default off; set explicitly so it can't be inherited on)

   # Deny dotfiles, source, configs, logs, backups, archives, editor/VCS leftovers
   location ~ /\.            { deny all; }            # .env .git .htaccess
   location ~* \.(md|env|ini|conf|log|bak|old|orig|swp|sql|yml|yaml|zip|tar|tar\.gz|tgz)$ { deny all; }
   location ~ ~$            { deny all; }             # editor backup files like index.html~

   # Restrict methods to read-only INSIDE the served location.
   # limit_except is location-scoped and evaluated per matched location;
   # a server-level `if ($request_method ...)` runs before location
   # selection and leaks the restriction to proxied/other locations.
   # Add this directive to the SAME `location /` from Phase 2 — do not
   # create a second `location /`:
   #   limit_except GET HEAD { deny all; }   # 403 on POST/PUT/DELETE
   ```
   The consolidated `location /` (method limit + rate limit) is shown in step 4. When an API `location` genuinely needs `POST`/`PUT`, give it its own `limit_except` (or none) — the restriction stays scoped to the static `location /`.
3. Security headers:
   ```nginx
   # HSTS: start WITHOUT includeSubDomains. Add it only once you have confirmed
   # EVERY subdomain (current and future) serves HTTPS — includeSubDomains forces
   # HTTPS on all of them and a non-HTTPS subdomain becomes unreachable.
   add_header Strict-Transport-Security "max-age=31536000" always;
   # PRECONDITION to append "; includeSubDomains": all subdomains are HTTPS-capable.
   #   add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

   add_header X-Content-Type-Options "nosniff" always;
   add_header X-Frame-Options "SAMEORIGIN" always;
   add_header Referrer-Policy "strict-origin-when-cross-origin" always;

   # CSP: deploy in Report-Only first so a too-strict policy cannot break the site.
   # Inventory this site's real asset origins (CDNs, fonts, analytics, inline
   # scripts) BEFORE enforcing — a blanket "default-src 'self'" silently blocks
   # any third-party asset the pages actually load.
   add_header Content-Security-Policy-Report-Only "default-src 'self'" always;
   # Promote to enforcing only after Report-Only shows zero legitimate violations:
   #   add_header Content-Security-Policy "default-src 'self'" always;
   ```
4. Rate limiting — define the zone in `http{}`, enforce it in the served `location`:
   ```nginx
   # http{} context (e.g. /etc/nginx/nginx.conf or a conf.d include)
   limit_req_zone $binary_remote_addr zone=web:10m rate=10r/s;
   ```
   This is the ONE canonical `location /` for the server block — it replaces the
   minimal `location /` from Phase 2 and carries both the method limit and the
   rate limit (one `location /` per server block, no duplicates):
   ```nginx
   location / {
       try_files $uri $uri/ =404;             # Phase 2
       limit_except GET HEAD { deny all; }    # step 2: 403 on POST/PUT/DELETE
       limit_req zone=web burst=20 nodelay;   # active rate limit — enforced, not commented
   }
   ```
   A `limit_req_zone` with no matching `limit_req` defines a zone that never throttles anything.
5. fail2ban watching nginx for bad requests and bot probes:
   ```bash
   apt-get install -y fail2ban
   # enable jails: nginx-http-auth, nginx-bad-request, nginx-botsearch
   systemctl enable --now fail2ban && fail2ban-client status
   ```

**Gate**: All five hardening items applied; `nginx -t` passes; `ufw status` shows only 80/443/SSH.

### Phase 5: Verify

**Goal**: Prove the live site is correct and the dangerous surfaces are closed.

**Steps** (run the full security checklist below), then spot-check from outside the host:
```bash
curl -sI https://app.example.com | head             # 200 + security headers (HSTS/CSP/etc.)
curl -s  https://app.example.com/.env -o /dev/null -w '%{http_code}\n'        # 403/404
curl -s  https://app.example.com/.git/config -o /dev/null -w '%{http_code}\n' # 403/404
curl -s  https://app.example.com/backup.zip -o /dev/null -w '%{http_code}\n'  # 403/404 (archive deny)
curl -s  https://app.example.com/ -o /dev/null -w '%{http_code}\n'            # no autoindex on a dir
curl -X POST -s https://app.example.com/ -o /dev/null -w '%{http_code}\n'     # 403 for static (limit_except deny all)
ss -tlnp | grep -vE '127\.0\.0\.1|:(80|443)\b'      # no app/dev port on a public iface
# Mixed content: served pages reference only https:// subresources
curl -s https://app.example.com/ | grep -oE 'http://[^"'\'' ]+' || echo "no http:// subresources"
```

**Gate**: Every checklist item passes. The site serves over HTTPS; dotfiles/configs return 403/404; no raw dev/app port is internet-reachable.

---

## Public-Site Security Checklist

Run every item before declaring the site live. Each line is pass/fail.

| # | Check | Pass condition |
|---|-------|----------------|
| 1 | DNS points to host | `dig +short` returns the intended public IP (A and, if present, AAAA) |
| 2 | HTTPS cert installed + renewal proven | valid chain served; `certbot renew --dry-run` exits 0 |
| 3 | HTTP->HTTPS redirect | plain HTTP returns 301/308 to `https://` (status, not just a Location header) |
| 4 | No raw app/dev ports exposed | app/backend binds `127.0.0.1`; nothing else on a public iface |
| 5 | UFW allows only intended ports, IPv4 and IPv6 | `ufw status` shows only 80/443/SSH; v6 parity when an AAAA record exists |
| 6 | nginx denies sensitive paths | dotfiles, `.md/.env/config/logs`, backups, archives (`.zip/.tar/.tgz`), editor/VCS leftovers (`~/.old/.orig/.swp`) return 403/404 |
| 7 | Directory listing disabled | `autoindex off`; a directory URL does not return a file index |
| 8 | Methods limited to GET/HEAD unless app needs more | `limit_except GET HEAD` in the served `location`; other methods return 403 for static sites |
| 9 | Security headers present | HSTS (`includeSubDomains` only when all subdomains are HTTPS-capable), X-Content-Type-Options, X-Frame-Options, Referrer-Policy set; CSP deployed Report-Only first, promoted to enforcing after zero legitimate violations |
| 10 | No mixed content | every subresource (img/script/style/font) loads over HTTPS; no `http://` references in served pages |
| 11 | Rate limiting active | `limit_req` zone applied to public locations |
| 12 | fail2ban watches nginx bad requests/bot probes | nginx-bad-request + nginx-botsearch jails active |
| 13 | Public-vs-private access decided explicitly | public = HTTPS + hardened nginx (no default basic-auth); auth only on private/internal sites |

---

## Examples

### Example 1: "Put my static site online at mysite.com"
1. Add `A` record -> host IP; verify `dig +short` (DNS).
2. nginx server block, docroot `/var/www/mysite.com`, `nginx -t && reload` (Web Server).
3. `certbot --nginx -d mysite.com`; `certbot renew --dry-run`; confirm HTTP->HTTPS (HTTPS).
4. UFW 80/443/SSH; deny dotfiles; GET/HEAD only; headers; rate limit; fail2ban (Hardening).
5. Run the 13-item checklist; curl-probe `.env`/`.git`/POST from outside (Verify).
Result: public HTTPS static site, no dev server, sensitive paths closed.

### Example 2: "Use my domain to serve this app I'm running on :8000"
1. Keep the app bound to `127.0.0.1:8000` (local). Add DNS for the FQDN.
2. nginx server block reverse-proxies `location /` -> `http://127.0.0.1:8000`.
3. certbot for TLS; HTTP->HTTPS redirect.
4. UFW exposes only 80/443/SSH — port 8000 stays private; harden nginx.
5. Verify the app is reachable only through nginx, never directly on :8000.
Result: app served publicly via nginx+HTTPS; raw app port never internet-facing.

---

## Error Handling

### Error: certbot fails with "DNS problem / NXDOMAIN"
Cause: DNS has not propagated, or the record points elsewhere.
Solution: Re-run `dig +short A <fqdn>`; wait for propagation or fix the record. Re-issue the cert once DNS resolves to the host.

### Error: site loads on HTTP but not HTTPS
Cause: cert issued but nginx not listening on 443, or firewall blocks 443.
Solution: `nginx -t` for a `listen 443 ssl` block; `ufw allow 443/tcp`; `systemctl reload nginx`.

### Error: dotfiles or `.env` are downloadable
Cause: deny rules missing, or a more specific `location` (an exact `=` or longer prefix match) serves the file before the regex deny is consulted. nginx matches regex `location` blocks in file order but a prefix/exact match can win regardless of position.
Solution: Add the `location ~ /\.` and extension deny blocks; keep them ahead of other regex `location` blocks and confirm no exact/prefix `location` shadows them; reload and re-probe with curl.

### Error: someone reached the app directly on its dev port
Cause: backend bound `0.0.0.0` and/or UFW allows the port.
Solution: Rebind the backend to `127.0.0.1`; remove the port from UFW; verify with `ss -tlnp` that only 80/443 face the internet.

---

## References

### Why not a raw dev server in public
| Concern | Raw dev server (`http.server`, Vite, Next/Flask dev) | nginx / Caddy / Apache / CF Pages |
|---------|------------------------------------------------------|-----------------------------------|
| TLS | none | first-class, auto-renew |
| Directory exposure | serves whole CWD incl. dotfiles | explicit docroot + deny rules |
| Concurrency | single-threaded | production event loop / workers |
| Request filtering | none | method limits, rate limiting, fail2ban |
| Headers | none | HSTS/CSP/etc. configured |

### Local preview (allowed)
Local preview binds loopback so it never faces the internet:
```bash
python3 -m http.server 8080 --bind 127.0.0.1   # local only
```
For public access, front it with nginx — see the workflow above.

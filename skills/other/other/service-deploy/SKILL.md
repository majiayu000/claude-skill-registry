---
name: service-deploy
description: Use this skill when enabling, moving, or migrating a NixOS service between hosts (doc1/proxmox-vm, doc2, igpu, framework, etc.), or when verifying that a service is actually working after deployment. Trigger phrases include "move X to host Y", "enable X on Y", "deploy X", "is X working", "verify X is up", "X isn't accessible", "can't reach X".
version: 1.0.0
---

# Service Deploy & Verify Skill

Covers the full lifecycle: config change → deploy → verify end-to-end. Never declare success until the service is reachable.

## Fleet Quick Reference

| Host       | SSH alias | LAN IP        | Key services                        |
|------------|-----------|---------------|-------------------------------------|
| proxmox-vm | doc1      | 192.168.1.29  | nix-serve(:5000), nix cache, CI     |
| doc2       | doc2      | 192.168.1.35  | Most homelab services               |
| igpu       | igp       | 192.168.1.33  | Jellyfin, Plex, Tdarr               |

**doc1 port conflict:** `nix-serve` binds `127.0.0.1:5000`. Any service with default port 5000 will fail on doc1 — always use a different port.

## Moving a Service Between Hosts

1. **Check for port conflicts** on the destination host before touching config:
   ```bash
   ssh <dest> "sudo ss -tlnp | grep :<port>"
   ```

2. **Update config** — disable on source, enable on destination:
   ```nix
   # source host configuration.nix
   services.foo.enable = false;

   # destination host configuration.nix
   services.foo = {
     enable = true;
     dataDir = "/mnt/virtio/foo";   # match existing path if data must survive
     port = 5001;                   # adjust if default conflicts
   };
   ```

3. **Deploy both hosts in parallel** (but be aware of DNS race below):
   ```bash
   ssh <source> "sudo nixos-rebuild switch --flake github:abl030/nixosconfig#<source-hostname> --refresh 2>&1" &
   ssh <dest>   "sudo nixos-rebuild switch --flake github:abl030/nixosconfig#<dest-hostname>   --refresh 2>&1"
   ```

4. **DNS race condition** — when both hosts run `homelab-dns-sync` simultaneously, the source's deletion can race with the destination's creation and win. After parallel deploy, always verify DNS:
   ```bash
   # Check Cloudflare has the record (authoritative)
   TOKEN=$(ssh <dest> "sudo grep -oP 'CLOUDFLARE_DNS_API_TOKEN=\K.*' /run/secrets/acme/cloudflare | tr -d '\r\n'")
   ZONE=$(ssh <dest> "sudo cat /var/lib/homelab/dns/zone-id")
   curl -fsS -H "Authorization: Bearer $TOKEN" \
     "https://api.cloudflare.com/client/v4/zones/$ZONE/dns_records?type=A&name=<hostname>" \
     | jq '.result[] | {id, name, content}'

   # If empty: clear the stale cache entry and re-run sync
   ssh <dest> "sudo jq 'del(.\"<hostname>\")' /var/lib/homelab/dns/records.json \
     | sudo tee /var/lib/homelab/dns/records.json.tmp \
     && sudo mv /var/lib/homelab/dns/records.json.tmp /var/lib/homelab/dns/records.json"
   ssh <dest> "sudo systemctl start homelab-dns-sync.service"
   ```

   Then verify the record was actually created (not just cached):
   ```bash
   # Must return a record with correct IP — empty result means it failed silently
   curl -fsS -H "Authorization: Bearer $TOKEN" \
     "https://api.cloudflare.com/client/v4/zones/$ZONE/dns_records?type=A&name=<hostname>" \
     | jq '.result | length'   # must be > 0
   ```

## Post-Deploy Verification Checklist

Run through these in order — stop and diagnose at the first failure:

### 1. Systemd units are up
```bash
ssh <host> "sudo systemctl status podman-<service>-*.service --no-pager -n 5"
# Look for: Active: active (running)
# Red flags: restart counter > 5, "activating" stuck, "failed"
```

### 2. No port conflicts
```bash
ssh <host> "sudo journalctl -u podman-<service>-nginx.service -n 20 --no-pager | grep -i 'error\|bind\|address already'"
# "bind: address already in use" → find the owner:
ssh <host> "sudo ss -tlnp | grep :<port>"
```

### 3. DNS resolves to the right IP
```bash
dig <hostname> +short @1.1.1.1
# Must match destination host's localIp from hosts.nix
```

### 4. HTTPS is reachable
```bash
curl -sI https://<hostname>/ | head -5
# Expect: HTTP/2 200 (or 302/301 redirect)
# "File not found" from nginx = upstream container not running
# Connection refused = nginx not running or port wrong
```

### 5. Application-level health (if applicable)
```bash
curl -s https://<hostname>/api/health | jq .   # or equivalent
```

## Common Failure Modes & Fixes

### "address already in use" on container start
Something else owns the port. Find it and either move the service to a free port or stop the conflict.
```bash
ssh <host> "sudo ss -tlnp | grep :<port>"
# Fix: add port = <free_port>; to the service options in configuration.nix
```

### Nginx returns "File not found"
The nginx container is up but the upstream (meelo-server, meelo-front, etc.) isn't. Check dependencies:
```bash
ssh <host> "sudo systemctl status podman-<service>-server.service --no-pager -n 10"
```

### DNS points to wildcard catch-all (192.168.1.6)
No specific A record exists. Either the sync failed silently or the race condition deleted it. See DNS race fix above.

### Container restart-looping
```bash
ssh <host> "sudo journalctl -u podman-<service>-<container>.service --no-pager -n 30"
# Common causes:
# - Port conflict (see above)
# - Missing secret / env file not yet deployed
# - Dependency container not healthy
# - Bad volume mount path
```

### Data missing after move
Verify both hosts share the same virtiofs tag:
```bash
grep -A3 'virtiofs\|device.*container' hosts/<source>/configuration.nix
grep -A3 'virtiofs\|device.*container' hosts/<dest>/configuration.nix
# Both must use device = "containers" for data to persist across the move
```

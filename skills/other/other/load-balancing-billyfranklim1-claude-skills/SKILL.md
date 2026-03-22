---
name: load-balancing
description: Load balancing with Nginx, upstream, health checks, zero-downtime deploy, horizontal scaling
---

# Skill: Load Balancing com Nginx

## Quando Usar
- Distribuir trafego entre multiplas instancias de uma app (Next.js, Laravel, Node)
- Fazer zero-downtime deploy (adicionar/remover backends sem parar)
- Diagnosticar 502 Bad Gateway ou timeouts causados por backend sobrecarregado

## Contexto do Servidor

Apps atuais que podem se beneficiar de load balancing:
- **frontend.example.com** (Next.js) — porta 3001 (pode escalar pra 3003, 3004...)
- **neuralnets.example.com** (Next.js) — porta 8080
- **portfolio.example.com** (Next.js) — porta 3002
- **Laravel apps** — via PHP-FPM pools (já faz balanceamento interno via workers)

Nginx config: `/etc/nginx/sites-available/`
Nginx principal: `/etc/nginx/nginx.conf`

## Passos / Comandos

### 1. Upstream Basico (Round Robin)

```nginx
# /etc/nginx/sites-available/frontend.example.com
upstream frontend_backend {
    server 127.0.0.1:3001;
    server 127.0.0.1:3003;
    server 127.0.0.1:3004;

    keepalive 32;  # conexoes persistentes ao backend
}

server {
    listen 443 ssl;
    server_name www.myapp.example.com;

    location / {
        proxy_pass http://frontend_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 2. Upstream com Peso e Health Check

```nginx
upstream frontend_backend {
    server 127.0.0.1:3001 weight=3;          # recebe 3x mais trafego
    server 127.0.0.1:3003 weight=1;
    server 127.0.0.1:3004 backup;            # so entra se os outros cairem

    # Health check passivo (Nginx OSS)
    server 127.0.0.1:3001 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:3003 max_fails=3 fail_timeout=30s;

    keepalive 32;
}
```

### 3. Algoritmos de Balanceamento

```nginx
# Round Robin (default) — distribui igualmente
upstream app {
    server 127.0.0.1:3001;
    server 127.0.0.1:3003;
}

# Least Connections — envia pro backend com menos conexoes ativas
upstream app {
    least_conn;
    server 127.0.0.1:3001;
    server 127.0.0.1:3003;
}

# IP Hash — mesmo IP sempre vai pro mesmo backend (sticky sessions)
upstream app {
    ip_hash;
    server 127.0.0.1:3001;
    server 127.0.0.1:3003;
}
```

### 4. Zero-Downtime Deploy

```bash
# Cenario: 2 instancias Next.js (3001 e 3003)

# 1. Tirar uma instancia do upstream
# Marcar como "down" no nginx config
sed -i 's/server 127.0.0.1:3003;/server 127.0.0.1:3003 down;/' /etc/nginx/sites-available/frontend.example.com
nginx -t && systemctl reload nginx

# 2. Fazer deploy na instancia parada
cd /home/deploy/frontend-b
sudo -u deploy git pull && sudo -u deploy npm ci && sudo -u deploy npm run build
sudo -u deploy pm2 restart frontend-b

# 3. Testar a instancia atualizada
curl -s http://127.0.0.1:3003/health

# 4. Recolocar no upstream
sed -i 's/server 127.0.0.1:3003 down;/server 127.0.0.1:3003;/' /etc/nginx/sites-available/frontend.example.com
nginx -t && systemctl reload nginx

# 5. Repetir para a outra instancia
```

### 5. Escalar Next.js (PM2 cluster)

```bash
# Forma simples: PM2 cluster mode (sem precisar de upstream manual)
cd /home/deploy/frontend
sudo -u deploy pm2 start ecosystem.config.js -i 2  # 2 instancias

# Ou via systemd (criar 2 services apontando pra portas diferentes)
# frontend-3001.service e frontend-3003.service
```

### 6. Rate Limiting por Backend

```nginx
# Limitar conexoes por backend (evita sobrecarregar um unico)
upstream app {
    server 127.0.0.1:3001 max_conns=100;
    server 127.0.0.1:3003 max_conns=100;
    queue 50 timeout=10s;  # fila de espera se todos lotarem
}
```

### 7. Diagnosticar Problemas

```bash
# Ver qual backend esta recebendo trafego
tail -f /var/log/nginx/access.log | awk '{print $NF}'

# Testar conectividade com backend
curl -v http://127.0.0.1:3001/health
curl -v http://127.0.0.1:3003/health

# Ver conexoes ativas por porta
ss -tnp | grep -E '3001|3003' | wc -l

# Nginx status (se modulo habilitado)
curl http://127.0.0.1/nginx_status

# 502 Bad Gateway = todos os backends falharam
# Verificar: processos rodando? Portas escutando? Logs do backend?
ss -tlnp | grep -E '3001|3003'
journalctl -u frontend --since "5 min ago" --no-pager
```

## Observacoes
- **Nginx OSS** (que temos) NAO tem health check ativo — usa passivo (max_fails/fail_timeout)
- **Nginx Plus** (pago) tem health check ativo com endpoint customizado
- Para Next.js, **PM2 cluster mode** e mais simples que upstream manual
- `keepalive` no upstream e CRITICO para performance — evita reconexao a cada request
- Ao usar `ip_hash`, se um backend cair, as sessions daquele IP se perdem
- SEMPRE teste com `nginx -t` antes de `systemctl reload nginx`
- `reload` (graceful) e DIFERENTE de `restart` (interrompe conexoes)

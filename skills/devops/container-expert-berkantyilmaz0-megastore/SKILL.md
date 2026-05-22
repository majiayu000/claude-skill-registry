---
name: container-expert
description: Docker, Docker Compose ve Nginx yapılandırması için uzman yetenek. Konteynerleştirme, reverse proxy, SSL sonlandırma ve üretim ortamı dağıtımı (production deployment) konularında kullanılır.
---

# 🐳 Container Expert (Docker & Nginx)

Bu yetenek, uygulamaların konteynerleştirilmesi (Docker) ve sunulması (Nginx) konularında uzman rehberlik sağlar.

## 🎯 Ne Zaman Kullanılır?
- Kullanıcı "uygulamayı dockerize et" dediğinde.
- "Nginx reverse proxy ayarla" isteği geldiğinde.
- `docker-compose.yml` veya `Dockerfile` oluşturulması gerektiğinde.
- Üretim ortamı (production) dağıtım konfigürasyonlarında.

---

## 🏗️ 1. Dockerfile Standartları

Her zaman **Multi-Stage Build** (Çok Aşamalı İnşa) kullanın. Bu, imaj boyutunu küçültür ve güvenliği artırır.

### Node.js / Next.js İçin Örnek (`Dockerfile`)
```dockerfile
# 1. Aşama: Bağımlılıklar
FROM node:18-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# 2. Aşama: İnşa (Build)
FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# 3. Aşama: Çalıştırma (Runner)
FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000
CMD ["npm", "start"]
```

---

## 🐙 2. Docker Compose Şablonları

Servisleri ve veritabanlarını birleştirmek için kullanılır.

### Standart Yığın (`docker-compose.yml`)
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=myapp

volumes:
  db_data:
```

---

## 🌐 3. Nginx Yapılandırması

Uygulamanın önüne bir "Kapı Bekçisi" (Reverse Proxy) koymak için kullanılır.

### Örnek `nginx.conf`
```nginx
server {
    listen 80;
    server_name example.com;

    # Gzip Sıkıştırma
    gzip on;
    gzip_types text/plain application/json text/css application/javascript;

    location / {
        proxy_pass http://app:3000; # Docker servis adı
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

---

## 🛡️ Güvenlik ve En İyi Pratikler

1.  **Asla Root Kullanma:** Dockerfile içinde `USER node` gibi root olmayan bir kullanıcıya geçin.
2.  **Alpine Kullan:** `node:alpine` veya `python:alpine` gibi küçük imajları tercih edin.
3.  **.dockerignore:** `node_modules`, `.git`, `.env` gibi dosyaların imaja kopyalanmasını engelleyin.
4.  **Sırlar (Secrets):** Veritabanı şifrelerini asla kodun içine gömmeyin, `.env` dosyasından veya Docker Secrets'tan okuyun.

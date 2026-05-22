---
name: deploy
description: Deploy, publish, push code, update project, release, migrations, build
---
# Skill: Deploy

## Quando Usar
Quando o usuario pedir deploy, atualizar, publicar, ou subir codigo de algum projeto.

## Projetos Laravel
```bash
PROJECT="myapp.example.com"  # ou api.myapp.example.com, work8.example.com
cd /home/deploy/$PROJECT
sudo -u deploy php artisan down --retry=60
sudo -u deploy git pull origin main
sudo -u deploy composer install --no-dev --optimize-autoloader
sudo -u deploy php artisan migrate --force
sudo -u deploy php artisan config:cache
sudo -u deploy php artisan route:cache
sudo -u deploy php artisan view:cache
sudo -u deploy php artisan queue:restart
sudo -u deploy php artisan up
curl -I https://$PROJECT
```

## Projetos Next.js
```bash
PROJECT="frontend.example.com"  # ou portfolio.example.com, neuralnets.example.com
PM2_NAME="frontend"    # ou portfolio, neuralnets
cd /home/deploy/$PROJECT
sudo -u deploy git pull origin main
sudo -u deploy npm ci
sudo -u deploy npm run build
sudo -u deploy pm2 restart $PM2_NAME
```

## MyApp (especial — tem SSR)
```bash
cd /home/deploy/myapp
sudo -u deploy php artisan down --retry=60
sudo -u deploy git pull origin main
sudo -u deploy composer install --no-dev --optimize-autoloader
sudo -u deploy php artisan migrate --force
sudo -u deploy php artisan config:cache && sudo -u deploy php artisan route:cache && sudo -u deploy php artisan view:cache
sudo -u deploy npm run build && sudo -u deploy npm run build:ssr
sudo -u deploy pm2 restart myapp-ssr
sudo -u deploy php artisan queue:restart
sudo -u deploy php artisan up
```

## Regras
- SEMPRE faca `php artisan down` antes
- SEMPRE confirme com curl apos subir
- Se migration falhar: rollback e reporte ao owner

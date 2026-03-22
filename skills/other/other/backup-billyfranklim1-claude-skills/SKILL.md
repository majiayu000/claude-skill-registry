---
name: backup
description: Backup and restore databases, mysqldump, Cloudflare R2, data recovery
---
# Skill: Backup

## Quando Usar
Quando o usuario pedir backup, restore, ou verificar status de backups.

## Backup Automatico
- **Script**: `/root/.backup-config/backup-databases.sh`
- **Schedule**: 03:00 UTC diariamente (crontab)
- **Destino**: Cloudflare R2 (`mybackup` bucket) → `/backups/databases/`
- **Retencao**: 30 dias
- **Databases**: myapp_db, mybackup, work_db, nn_db, extra_db
- **Config**: `/root/.backup-config/.env`

## Comandos
```bash
# Executar backup manual
/root/.backup-config/backup-databases.sh

# Ver logs
tail -f /var/log/db-backup.log

# Listar backups no R2
aws s3 ls s3://mybackup/backups/databases/ \
  --endpoint-url https://ACCOUNT_ID.r2.cloudflarestorage.com

# Restaurar
aws s3 cp s3://mybackup/backups/databases/myapp_db_2026-02-02.sql.gz . \
  --endpoint-url https://ACCOUNT_ID.r2.cloudflarestorage.com
gunzip myapp_db_2026-02-02.sql.gz
mysql -u deploy -p myapp_db < myapp_db_2026-02-02.sql
```

## Regras
- SEMPRE confirme com o the owner antes de restaurar um backup
- Backup manual: execute e verifique o log de sucesso
- Restore: faca backup do estado atual ANTES de restaurar

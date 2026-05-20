---
name: backup-retention-policy
description: Эксперт по политикам бэкапов. Используй для стратегий резервного копирования, retention rules и disaster recovery.
---

# Backup Retention Policy Expert

Эксперт по управлению жизненным циклом данных и восстановления после сбоев.

## Правило 3-2-1-1-0

- **3** копии важных данных (1 основная + 2 резервные)
- **2** различных типа носителей
- **1** внешняя/облачная резервная копия
- **1** автономная/неизменяемая резервная копия
- **0** ошибок после тестирования

## Уровни хранения

| Уровень | Доступ | Период | Стоимость |
|---------|--------|--------|-----------|
| Горячий | Частый | 0-30 дней | $$$ |
| Теплый | Периодический | 30-90 дней | $$ |
| Холодный | Редкий | 90 дней-7 лет | $ |
| Архив | Долгосрочный | 7+ лет | ¢ |

## AWS S3 Lifecycle Policy

```json
{
  "Rules": [
    {
      "ID": "BackupLifecycle",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "backups/"
      },
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        },
        {
          "Days": 365,
          "StorageClass": "DEEP_ARCHIVE"
        }
      ],
      "Expiration": {
        "Days": 2555
      },
      "NoncurrentVersionTransitions": [
        {
          "NoncurrentDays": 30,
          "StorageClass": "GLACIER"
        }
      ],
      "NoncurrentVersionExpiration": {
        "NoncurrentDays": 365
      }
    }
  ]
}
```

## Azure Blob Lifecycle

```json
{
  "rules": [
    {
      "name": "backupRetention",
      "type": "Lifecycle",
      "definition": {
        "actions": {
          "baseBlob": {
            "tierToCool": {"daysAfterModificationGreaterThan": 30},
            "tierToArchive": {"daysAfterModificationGreaterThan": 90},
            "delete": {"daysAfterModificationGreaterThan": 2555}
          },
          "snapshot": {
            "delete": {"daysAfterCreationGreaterThan": 90}
          }
        },
        "filters": {
          "blobTypes": ["blockBlob"],
          "prefixMatch": ["backups/"]
        }
      }
    }
  ]
}
```

## Скрипт ротации бэкапов

```bash
#!/bin/bash
BACKUP_DIR="/var/backups"
DAILY_RETENTION=7
WEEKLY_RETENTION=4
MONTHLY_RETENTION=12

# Удаление ежедневных старше 7 дней
find "$BACKUP_DIR/daily" -type f -mtime +$DAILY_RETENTION -delete

# Удаление еженедельных старше 4 недель
find "$BACKUP_DIR/weekly" -type f -mtime +$((WEEKLY_RETENTION * 7)) -delete

# Удаление ежемесячных старше 12 месяцев
find "$BACKUP_DIR/monthly" -type f -mtime +$((MONTHLY_RETENTION * 30)) -delete

# Логирование
echo "$(date): Rotation completed" >> /var/log/backup_rotation.log
```

## PostgreSQL Backup

```bash
#!/bin/bash
DB_NAME="production"
BACKUP_DIR="/var/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)

# Полный бэкап
pg_dump -Fc -f "$BACKUP_DIR/full_$DATE.dump" $DB_NAME

# Инкрементальный с WAL
pg_basebackup -D "$BACKUP_DIR/base_$DATE" -Ft -z -P

# Архивация WAL логов
archive_command = 'cp %p /var/backups/wal/%f'
```

## MySQL Backup

```bash
#!/bin/bash
MYSQL_USER="backup_user"
MYSQL_PASS="secure_password"
BACKUP_DIR="/var/backups/mysql"
DATE=$(date +%Y%m%d_%H%M%S)

# Полный бэкап
mysqldump --user=$MYSQL_USER --password=$MYSQL_PASS \
    --all-databases --single-transaction \
    --routines --triggers --events \
    | gzip > "$BACKUP_DIR/full_$DATE.sql.gz"

# Инкрементальный с binlog
mysqlbinlog --read-from-remote-server \
    --host=localhost --user=$MYSQL_USER \
    --raw --stop-never mysql-bin.000001
```

## Compliance Requirements

| Стандарт | Требование |
|----------|------------|
| GDPR | Право на удаление, минимизация данных |
| SOX | 7 лет для финансовых записей |
| HIPAA | 6 лет для медицинских данных |
| PCI DSS | 1 год минимум для аудита |

## RTO/RPO Planning

```yaml
Критические системы:
  RPO: 1 час
  RTO: 4 часа
  Стратегия: Синхронная репликация + горячий standby

Бизнес-системы:
  RPO: 4 часа
  RTO: 24 часа
  Стратегия: Асинхронная репликация + теплый standby

Архивные системы:
  RPO: 24 часа
  RTO: 72 часа
  Стратегия: Ежедневные бэкапы + холодное хранение
```

## Валидация политик на Python

```python
from datetime import datetime, timedelta
from typing import List, Dict

class BackupRetentionValidator:
    def __init__(self, retention_policy: Dict):
        self.policy = retention_policy

    def validate_backup(self, backup_date: datetime, backup_type: str) -> bool:
        """Проверка соответствия бэкапа политике хранения"""
        retention_days = self.policy.get(backup_type, {}).get('retention_days', 0)
        expiry_date = backup_date + timedelta(days=retention_days)
        return datetime.now() < expiry_date

    def get_expired_backups(self, backups: List[Dict]) -> List[Dict]:
        """Получить список просроченных бэкапов"""
        expired = []
        for backup in backups:
            if not self.validate_backup(backup['date'], backup['type']):
                expired.append(backup)
        return expired

    def calculate_storage_forecast(self, daily_backup_size_gb: float) -> Dict:
        """Прогноз использования хранилища"""
        total_storage = 0
        for backup_type, config in self.policy.items():
            retention = config.get('retention_days', 0)
            frequency = config.get('frequency_days', 1)
            copies = retention // frequency
            total_storage += copies * daily_backup_size_gb

        return {
            'total_gb': total_storage,
            'monthly_cost_estimate': total_storage * 0.023  # S3 Standard pricing
        }
```

## График тестирования

| Тип теста | Частота | Охват |
|-----------|---------|-------|
| Выборочное восстановление | Ежемесячно | 10% данных |
| Полное восстановление | Ежеквартально | Критические системы |
| DR учения | Ежегодно | Полный сценарий |
| Аудит политик | Ежегодно | Все политики |

## Мониторинг и алерты

```yaml
Алерты:
  backup_failed:
    severity: critical
    notification: [pagerduty, slack]

  backup_size_anomaly:
    threshold: 20%
    severity: warning

  retention_violation:
    severity: high
    action: auto_remediate

  storage_threshold:
    threshold: 80%
    severity: warning
```

## Лучшие практики

1. **Тестируйте восстановление** — бэкап без теста = нет бэкапа
2. **Шифруйте данные** — AES-256 для данных в покое
3. **Версионирование** — храните несколько версий
4. **Географическое распределение** — минимум 2 региона
5. **Immutable storage** — защита от ransomware
6. **Документируйте процедуры** — runbooks для DR

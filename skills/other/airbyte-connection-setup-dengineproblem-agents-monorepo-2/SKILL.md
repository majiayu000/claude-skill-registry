---
name: airbyte-connection-setup
description: Эксперт Airbyte. Используй для настройки ETL/ELT пайплайнов, коннекторов, синхронизации данных и data pipelines.
---

# Airbyte Connection Setup Expert

Эксперт по настройке и управлению подключениями в Airbyte.

## Основные принципы

### Архитектура подключений
- **Пары источник-назначение**: Потоки данных с трансформацией
- **Инкрементальная синхронизация**: Предпочтительнее full refresh
- **Эволюция схемы**: Обработка изменений схемы
- **Восстановление после сбоев**: Надёжная обработка ошибок

### Режимы синхронизации
- **Full Refresh**: Полная перезапись данных
- **Incremental Append**: Добавление новых записей
- **Incremental Deduped**: Дедупликация по первичному ключу

## Docker Compose Setup

```yaml
version: '3.8'
services:
  db:
    image: airbyte/db:${VERSION}
    environment:
      - POSTGRES_USER=${DATABASE_USER}
      - POSTGRES_PASSWORD=${DATABASE_PASSWORD}
    volumes:
      - db:/var/lib/postgresql/data

  server:
    image: airbyte/server:${VERSION}
    environment:
      - DATABASE_PASSWORD=${DATABASE_PASSWORD}
      - DATABASE_URL=${DATABASE_URL}
      - WORKSPACE_ROOT=/tmp/workspace
    ports:
      - "8001:8001"
    volumes:
      - workspace:/tmp/workspace
      - data:/data
    depends_on:
      - db

  webapp:
    image: airbyte/webapp:${VERSION}
    ports:
      - "8000:80"
    depends_on:
      - server
```

## Конфигурация источника

```python
# PostgreSQL источник
source_config = {
    "host": "localhost",
    "port": 5432,
    "database": "production_db",
    "username": "airbyte_user",
    "password": "secure_password",
    "ssl_mode": {"mode": "require"},
    "replication_method": {
        "method": "CDC",
        "plugin": "pgoutput",
        "initial_waiting_seconds": 300
    }
}
```

## Конфигурация назначения

```python
# Snowflake назначение
destination_config = {
    "host": "account.snowflakecomputing.com",
    "role": "AIRBYTE_ROLE",
    "warehouse": "AIRBYTE_WAREHOUSE",
    "database": "AIRBYTE_DATABASE",
    "schema": "RAW_DATA",
    "username": "airbyte_user",
    "password": "secure_password",
    "loading_method": {"method": "Internal Staging"}
}
```

## Конфигурация синхронизации

```json
{
  "syncCatalog": {
    "streams": [
      {
        "stream": {
          "name": "users",
          "supportedSyncModes": ["full_refresh", "incremental"]
        },
        "config": {
          "syncMode": "incremental",
          "cursorField": ["updated_at"],
          "destinationSyncMode": "append_dedup",
          "primaryKey": [["id"]]
        }
      }
    ]
  },
  "schedule": {
    "units": 1,
    "timeUnit": "hours"
  }
}
```

## API интеграция

```python
import requests

# Создание источника
source_payload = {
    "sourceDefinitionId": "decd338e-5647-4c0b-adf4-da0e75f5a750",
    "connectionConfiguration": source_config,
    "workspaceId": workspace_id,
    "name": "Production PostgreSQL"
}

response = requests.post(
    f"{airbyte_url}/api/v1/sources/create",
    json=source_payload,
    headers={"Content-Type": "application/json"}
)

# Создание подключения
connection_payload = {
    "sourceId": source_id,
    "destinationId": destination_id,
    "syncCatalog": sync_catalog,
    "schedule": {"units": 1, "timeUnit": "hours"}
}

requests.post(
    f"{airbyte_url}/api/v1/connections/create",
    json=connection_payload
)
```

## Устранение неполадок

### Частые проблемы
1. **Сетевое подключение**: Проверьте фаервол и доступ
2. **Аутентификация**: Проверьте права и срок действия
3. **Лимиты ресурсов**: Мониторинг памяти и CPU
4. **Изменения схемы**: Обновление конфигураций

### Оптимизация
- Настройка размеров батчей
- Использование пулинга подключений
- Индексирование полей курсора
- Мониторинг производительности

### Безопасность
- Хранение секретов в vault
- SSL/TLS для всех подключений
- Сетевая сегментация
- Регулярные обновления

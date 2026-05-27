---
name: audit-log-generator
description: Эксперт по аудит-логам. Используй для создания систем логирования, compliance требований, структуры логов и мониторинга.
---

# Audit Log Generator Expert

Эксперт в проектировании и реализации логов аудита для безопасности, соответствия требованиям и мониторинга.

## Основные элементы лога

Каждая запись должна содержать:
- **Timestamp**: UTC с точностью до миллисекунд
- **Event ID**: Уникальный идентификатор
- **Actor**: Кто выполнил действие
- **Action**: Что было выполнено (CREATE, READ, UPDATE, DELETE)
- **Resource**: На что было воздействие
- **Source**: IP адрес, приложение
- **Result**: Успех/неудача
- **Risk Level**: Классификация критичности

## JSON формат (рекомендуется)

```json
{
  "timestamp": "2024-01-15T14:30:45.123Z",
  "event_id": "evt_7f4a9b2c8e1d",
  "version": "1.0",
  "actor": {
    "user_id": "john.doe@company.com",
    "session_id": "sess_abc123",
    "role": "admin"
  },
  "action": "DELETE",
  "resource": {
    "type": "database_record",
    "id": "customer_12345",
    "table": "customers",
    "classification": "PII"
  },
  "context": {
    "source_ip": "192.168.1.100",
    "user_agent": "Mozilla/5.0...",
    "application": "customer_portal",
    "api_endpoint": "/api/v1/customers/12345"
  },
  "result": {
    "status": "SUCCESS",
    "response_code": 200,
    "affected_records": 1
  },
  "metadata": {
    "risk_level": "HIGH",
    "compliance_tags": ["GDPR", "SOX"],
    "retention_years": 7,
    "checksum": "sha256:a1b2c3d4..."
  }
}
```

## CEF (Common Event Format)

```
CEF:0|CompanyName|CustomerPortal|2.1|1001|User Data Deletion|8|
rt=Jan 15 2024 14:30:45 UTC src=192.168.1.100
suser=john.doe@company.com act=DELETE dst=customer_db
cs1Label=Table cs1=customers cs2Label=RecordID cs2=12345
```

## Классификация событий

### События аутентификации
- Попытки входа (успех/неудача)
- Смена паролей
- Активации MFA
- Блокировки аккаунтов
- Повышения привилегий

### События доступа к данным
```json
{
  "action": "READ",
  "data_classification": "SENSITIVE",
  "access_method": "API",
  "record_count": 150,
  "query_hash": "sha256:..."
}
```

### Административные события
- Изменения конфигурации
- Предоставление/отзыв доступа
- Изменения разрешений
- Операции резервного копирования

### События безопасности
- Неудачные попытки авторизации
- Аномальные паттерны доступа
- Нарушения политик безопасности

## Compliance Requirements

### GDPR
```json
{
  "gdpr_context": {
    "lawful_basis": "legitimate_interest",
    "data_subject_id": "ds_789",
    "processing_purpose": "customer_service",
    "retention_justified": true,
    "cross_border_transfer": false
  }
}
```

### SOX
- Отслеживание доступа к финансовым данным
- Разделение обязанностей
- Документация изменений
- Мониторинг доступа руководства

### HIPAA
```json
{
  "hipaa_context": {
    "phi_involved": true,
    "minimum_necessary": true,
    "covered_entity": "hospital_system",
    "patient_authorization": "auth_456"
  }
}
```

## Отслеживание изменений

```json
{
  "change_tracking": {
    "before_state": {
      "customer_tier": "silver",
      "credit_limit": 5000
    },
    "after_state": {
      "customer_tier": "gold",
      "credit_limit": 10000
    },
    "change_reason": "promotion_campaign",
    "approver": "manager.smith@company.com"
  }
}
```

## Batch Operations

```json
{
  "batch_context": {
    "batch_id": "batch_2024_01_15_001",
    "total_records": 10000,
    "successful_records": 9987,
    "failed_records": 13,
    "processing_duration_ms": 45678,
    "error_summary": ["validation_failed: 13"]
  }
}
```

## Контроли безопасности

### Шифрование
- AES-256 для данных в покое
- TLS 1.3 для данных в передаче
- Отдельные ключи для разных типов логов
- Регулярная ротация ключей

### Контроли доступа
```json
{
  "log_access_policy": {
    "read_access": ["audit_team", "compliance_officer"],
    "search_access": ["security_analyst"],
    "export_access": ["legal_team"],
    "retention_management": ["data_governance"]
  }
}
```

### Обнаружение вмешательства
- Дерево Меркла для целостности
- Цифровые подписи с PKI
- Регулярная проверка целостности
- Неизменяемые временные метки

## Реализация на Python

```python
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum

class AuditAction(Enum):
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"

class RiskLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class AuditLogger:
    def __init__(self, service_name: str):
        self.service_name = service_name

    def log(
        self,
        action: AuditAction,
        actor_id: str,
        resource_type: str,
        resource_id: str,
        result: str = "SUCCESS",
        risk_level: RiskLevel = RiskLevel.LOW,
        context: Optional[Dict[str, Any]] = None,
        before_state: Optional[Dict] = None,
        after_state: Optional[Dict] = None
    ) -> Dict[str, Any]:
        event_id = self._generate_event_id()
        timestamp = datetime.utcnow().isoformat() + "Z"

        log_entry = {
            "timestamp": timestamp,
            "event_id": event_id,
            "service": self.service_name,
            "actor": {"user_id": actor_id},
            "action": action.value,
            "resource": {
                "type": resource_type,
                "id": resource_id
            },
            "result": {"status": result},
            "metadata": {
                "risk_level": risk_level.value
            }
        }

        if context:
            log_entry["context"] = context

        if before_state or after_state:
            log_entry["change_tracking"] = {
                "before_state": before_state,
                "after_state": after_state
            }

        log_entry["metadata"]["checksum"] = self._calculate_checksum(log_entry)

        self._persist_log(log_entry)
        return log_entry

    def _generate_event_id(self) -> str:
        import uuid
        return f"evt_{uuid.uuid4().hex[:12]}"

    def _calculate_checksum(self, entry: Dict) -> str:
        content = json.dumps(entry, sort_keys=True)
        return f"sha256:{hashlib.sha256(content.encode()).hexdigest()[:16]}"

    def _persist_log(self, entry: Dict):
        # Отправка в систему логирования
        print(json.dumps(entry, indent=2))
```

## Политики хранения

```python
retention_policies = {
    "authentication": {"years": 3, "hot_storage_days": 90},
    "data_access": {"years": 7, "hot_storage_days": 365},
    "administrative": {"years": 10, "hot_storage_days": 180},
    "security_incidents": {"years": 10, "hot_storage_days": 1095}
}
```

## Мониторинг и алерты

### Real-time алерты
- Всплески неудачных аутентификаций
- Паттерны привилегированного доступа
- Индикаторы эксфильтрации данных
- Нарушения политик соответствия

### Регулярная отчетность
- Ежедневные сводки доступа
- Еженедельные дашборды соответствия
- Ежемесячный анализ трендов
- Ежеквартальные отчеты готовности к аудиту

## Лучшие практики

1. **Неизменяемость** — логи только на добавление
2. **Криптографическая защита** — подписи и checksums
3. **Отдельное хранение** — изолировано от операционных систем
4. **Регулярная верификация** — проверка целостности
5. **Документация** — цепочка поставки данных

---
name: api-reference-guide
description: Эксперт по API reference документации. Используй для создания справочников по API, описания endpoints и примеров запросов.
---

# API Reference Guide Creator

Эксперт в создании комплексной документации по API, которую разработчики обожают использовать.

## Основные принципы

- **Подход "разработчик прежде всего"**: Пишите с точки зрения того, кто внедряет API
- **Ясность важнее краткости**: Предоставляйте достаточно деталей
- **Последовательность**: Используйте единообразные паттерны
- **Полнота**: Покрывайте все endpoint'ы, параметры, ответы и крайние случаи
- **Тестируемость**: Включайте рабочие примеры

## Структура справочника

1. **Обзор** — Назначение API, базовый URL, стратегия версионирования
2. **Аутентификация** — Методы, токены, заголовки, примеры
3. **Endpoint'ы** — Сгруппированные по ресурсам
4. **Обработка ошибок** — Стандартные коды ошибок и ответы
5. **Ограничения частоты запросов** — Лимиты, заголовки
6. **SDK и библиотеки** — Доступные клиентские библиотеки
7. **Журнал изменений** — История версий

## Документация аутентификации

```bash
# API Key Authentication
curl -X GET "https://api.example.com/v1/users" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

```javascript
// JavaScript SDK Example
const client = new APIClient({
  apiKey: 'your-api-key',
  baseURL: 'https://api.example.com/v1'
});
```

## Формат документации endpoint'ов

### GET /users/{id}

Получить конкретного пользователя по ID.

**Параметры:**
| Параметр | Тип | Место | Обязательный | Описание |
|----------|-----|-------|--------------|----------|
| id | string | path | да | Уникальный ID пользователя |
| include | string | query | нет | Связанные ресурсы через запятую |

**Пример запроса:**
```bash
curl -X GET "https://api.example.com/v1/users/12345?include=profile,settings" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Ответ (200 OK):**
```json
{
  "id": "12345",
  "email": "user@example.com",
  "created_at": "2023-01-15T10:30:00Z",
  "profile": {
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### POST /users

Создать новый аккаунт пользователя.

**Тело запроса:**
```json
{
  "email": "string (обязательный)",
  "password": "string (обязательный, минимум 8 символов)",
  "profile": {
    "first_name": "string (опциональный)",
    "last_name": "string (опциональный)"
  }
}
```

**Ответ (201 Created):**
```json
{
  "id": "12346",
  "email": "newuser@example.com",
  "created_at": "2024-01-15T14:30:00Z"
}
```

## Документация ошибок

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "email",
        "message": "Email address is required"
      }
    ],
    "request_id": "req_1234567890"
  }
}
```

**HTTP коды состояния:**
| Код | Статус | Описание |
|-----|--------|----------|
| 200 | OK | Успешный запрос |
| 201 | Created | Ресурс создан |
| 400 | Bad Request | Ошибки валидации |
| 401 | Unauthorized | Неверный/отсутствующий токен |
| 403 | Forbidden | Недостаточно прав |
| 404 | Not Found | Ресурс не найден |
| 429 | Too Many Requests | Превышен лимит запросов |
| 500 | Internal Server Error | Ошибка сервера |

## Примеры на разных языках

### Python
```python
import requests

headers = {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
}

response = requests.get(
    'https://api.example.com/v1/users/12345',
    headers=headers
)
print(response.json())
```

### Node.js
```javascript
const fetch = require('node-fetch');

const response = await fetch('https://api.example.com/v1/users/12345', {
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  }
});
const data = await response.json();
console.log(data);
```

### Go
```go
req, _ := http.NewRequest("GET", "https://api.example.com/v1/users/12345", nil)
req.Header.Set("Authorization", "Bearer YOUR_API_KEY")
req.Header.Set("Content-Type", "application/json")

client := &http.Client{}
resp, _ := client.Do(req)
defer resp.Body.Close()
```

## Типы данных и схемы

```yaml
User:
  type: object
  properties:
    id:
      type: string
      description: Unique user identifier
      example: "usr_1234567890"
    email:
      type: string
      format: email
      description: User's email address
    created_at:
      type: string
      format: date-time
      description: ISO 8601 timestamp
    status:
      type: string
      enum: [active, inactive, suspended]
      description: Current account status
```

## Продвинутые возможности

### Фильтрация
```
GET /users?filter[status]=active&filter[role]=admin
```

### Пагинация
```
GET /users?page=2&limit=20

Response headers:
X-Total-Count: 150
X-Page: 2
X-Per-Page: 20
Link: <https://api.example.com/v1/users?page=3>; rel="next"
```

### Сортировка
```
GET /users?sort=-created_at,email
```
Минус означает сортировку по убыванию.

### Выбор полей
```
GET /users?fields=id,email,created_at
```

### Идемпотентность
```bash
curl -X POST "https://api.example.com/v1/payments" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Idempotency-Key: unique-request-id-123" \
  -d '{"amount": 1000}'
```

## Rate Limiting Headers

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Лучшие практики

1. Используйте последовательное именование (snake_case или camelCase)
2. Включайте реалистичные примеры данных
3. Показывайте примеры как успешных, так и ошибочных ответов
4. Документируйте опциональные и обязательные параметры
5. Включайте информацию об ограничениях частоты
6. Используйте OpenAPI/Swagger спецификации
7. Добавляйте уведомления о deprecation
8. Тестируйте все примеры кода перед публикацией

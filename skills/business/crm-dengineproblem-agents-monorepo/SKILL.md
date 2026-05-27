---
name: crm
description: Работа с CRM, лидами и WhatsApp диалогами
---

# CRM Skill

Этот skill позволяет работать с лидами, диалогами и CRM системой.

## Базовый формат вызова

```bash
curl -s -X POST http://agent-brain:7080/brain/tools/{toolName} \
  -H "Content-Type: application/json" \
  -d '{...параметры...}'
```

---

## Leads (Лиды)

### getLeads
Получить список лидов.

```bash
curl -s -X POST http://agent-brain:7080/brain/tools/getLeads \
  -H "Content-Type: application/json" \
  -d '{"adAccountId": "act_123", "status": "new", "limit": 50}'
```

Параметры:
- `adAccountId` - ID рекламного аккаунта
- `status` - Статус: new, qualified, rejected, converted
- `period` - Период: last_1d, last_7d, last_30d
- `limit` - Лимит записей

### getLeadDetails
Детали лида.

```bash
curl -s -X POST http://agent-brain:7080/brain/tools/getLeadDetails \
  -H "Content-Type: application/json" \
  -d '{"leadId": "123"}'
```

### updateLeadStage
Изменить стадию лида.

```bash
curl -s -X POST http://agent-brain:7080/brain/tools/updateLeadStage \
  -H "Content-Type: application/json" \
  -d '{"leadId": "123", "stage": "qualified", "reason": "Confirmed interest"}'
```

---

## Воронка продаж

### getFunnelStats
Статистика воронки.

```bash
curl -s -X POST http://agent-brain:7080/brain/tools/getFunnelStats \
  -H "Content-Type: application/json" \
  -d '{"adAccountId": "act_123", "period": "last_30d"}'
```

### getSalesQuality
Качество продаж.

```bash
curl -s -X POST http://agent-brain:7080/brain/tools/getSalesQuality \
  -H "Content-Type: application/json" \
  -d '{"adAccountId": "act_123", "period": "last_30d"}'
```

---

## AmoCRM Integration

### getAmoCRMStatus
Статус интеграции с AmoCRM.

```bash
curl -s -X POST http://agent-brain:7080/brain/tools/getAmoCRMStatus \
  -H "Content-Type: application/json" \
  -d '{"adAccountId": "act_123"}'
```

### getAmoCRMPipelines
Воронки AmoCRM.

```bash
curl -s -X POST http://agent-brain:7080/brain/tools/getAmoCRMPipelines \
  -H "Content-Type: application/json" \
  -d '{"adAccountId": "act_123"}'
```

### syncAmoCRMLeads
Синхронизация лидов с AmoCRM.

```bash
curl -s -X POST http://agent-brain:7080/brain/tools/syncAmoCRMLeads \
  -H "Content-Type: application/json" \
  -d '{"adAccountId": "act_123"}'
```

### getAmoCRMKeyStageStats
Статистика по ключевым этапам.

```bash
curl -s -X POST http://agent-brain:7080/brain/tools/getAmoCRMKeyStageStats \
  -H "Content-Type: application/json" \
  -d '{"adAccountId": "act_123", "period": "last_30d"}'
```

### getAmoCRMQualificationStats
Статистика квалификации.

```bash
curl -s -X POST http://agent-brain:7080/brain/tools/getAmoCRMQualificationStats \
  -H "Content-Type: application/json" \
  -d '{"adAccountId": "act_123", "period": "last_30d"}'
```

### getAmoCRMLeadHistory
История лида в AmoCRM.

```bash
curl -s -X POST http://agent-brain:7080/brain/tools/getAmoCRMLeadHistory \
  -H "Content-Type: application/json" \
  -d '{"leadId": "123"}'
```

---

## WhatsApp Диалоги

### getDialogs
Получить диалоги.

```bash
curl -s -X POST http://agent-brain:7080/brain/tools/getDialogs \
  -H "Content-Type: application/json" \
  -d '{"adAccountId": "act_123", "status": "active", "limit": 20}'
```

### getDialogMessages
Сообщения диалога.

```bash
curl -s -X POST http://agent-brain:7080/brain/tools/getDialogMessages \
  -H "Content-Type: application/json" \
  -d '{"dialogId": "123", "limit": 50}'
```

### analyzeDialog
AI-анализ диалога.

```bash
curl -s -X POST http://agent-brain:7080/brain/tools/analyzeDialog \
  -H "Content-Type: application/json" \
  -d '{"dialogId": "123"}'
```

### searchDialogSummaries
Поиск по саммари диалогов.

```bash
curl -s -X POST http://agent-brain:7080/brain/tools/searchDialogSummaries \
  -H "Content-Type: application/json" \
  -d '{"query": "интересуется ценой", "adAccountId": "act_123"}'
```

---

## Примеры использования

### Анализ качества лидов
1. Получи лидов: `getLeads`
2. Получи статистику воронки: `getFunnelStats`
3. Сравни с предыдущим периодом

### Анализ диалогов
1. Получи диалоги: `getDialogs`
2. Проанализируй важные: `analyzeDialog`
3. Найди паттерны в саммари: `searchDialogSummaries`

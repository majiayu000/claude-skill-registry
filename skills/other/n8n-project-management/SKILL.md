---
name: "n8n-project-management"
description: "Build a complete project management system with Telegram bot, task distribution, and photo reports using n8n. Based on DDC Project Management repository."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🔧", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# n8n Project Management System for Construction

Build a universal task management and reporting system for construction projects using n8n automation, Telegram bot, and Google Sheets.

## Business Case

**Problem**: Construction managers spend 2-3 hours daily on:
- Distributing tasks to foremen and workers
- Collecting progress updates via calls/messages
- Compiling photo documentation
- Tracking task completion status

**Solution**: Automated system that:
- Sends task reminders via Telegram at scheduled times
- Collects status reports (text + photos + GPS)
- Auto-saves all data to Google Sheets
- Provides real-time visibility to managers

**ROI**: 70% reduction in administrative time for task management

## Source Repository

```
https://github.com/datadrivenconstruction/Project-management-n8n-with-task-management-and-photo-reports
```

## System Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                    PROJECT MANAGEMENT SYSTEM                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│   MANAGER                          WORKER                            │
│   ┌─────────────┐                  ┌─────────────┐                   │
│   │ Google      │                  │ Telegram    │                   │
│   │ Sheets      │                  │ Bot         │                   │
│   │             │                  │             │                   │
│   │ • Tasks     │    n8n           │ • /start    │                   │
│   │ • Schedule  │◄──Workflow──────►│ • Tasks     │                   │
│   │ • Reports   │                  │ • Photos    │                   │
│   │ • Photos    │                  │ • GPS       │                   │
│   └─────────────┘                  └─────────────┘                   │
│         │                                │                           │
│         ▼                                ▼                           │
│   ┌─────────────┐                  ┌─────────────┐                   │
│   │ Dashboard   │                  │ Google      │                   │
│   │ View        │                  │ Drive       │                   │
│   │             │                  │ (Photos)    │                   │
│   └─────────────┘                  └─────────────┘                   │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

## Implementation Guide

### Step 1: Create Telegram Bot

```python
# 1. Open @BotFather in Telegram
# 2. Send /newbot
# 3. Name: "YourProject Tasks Bot"
# 4. Username: "YourProjectTasks_bot"
# 5. Save the token: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# Test bot connection
import requests

BOT_TOKEN = "YOUR_BOT_TOKEN"
response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getMe")
print(response.json())
# Expected: {"ok": true, "result": {"id": ..., "first_name": "YourProject Tasks Bot"}}
```

### Step 2: Setup Google Sheets

Create spreadsheet with these sheets:

**Sheet 1: Tasks**
| Column | Type | Description |
|--------|------|-------------|
| Task_ID | Text | Unique identifier (TASK-001) |
| Project | Text | Project name |
| Object | Text | Building/area |
| Section | Text | Floor/zone |
| Task | Text | Task description |
| Executor | Text | Assigned worker name |
| Executor_ID | Number | Telegram user ID |
| Date | Date | Due date (DD.MM.YYYY) |
| Send_Time | Time | Reminder time |
| Priority | Text | 🔴High / 🟡Medium / 🟢Low |
| Status | Text | Pending/Sent/Completed/Partial |
| Response | Text | Worker's response |
| Response_Time | DateTime | When responded |
| Photo_Link | URL | Google Drive link |
| GPS_Lat | Number | Latitude |
| GPS_Lon | Number | Longitude |

**Sheet 2: Workers**
| Column | Type | Description |
|--------|------|-------------|
| Name | Text | Worker full name |
| Role | Text | Foreman/Worker/Contractor |
| Telegram_ID | Number | User ID from /start |
| Phone | Text | Phone number |
| Registered | DateTime | Registration date |

**Sheet 3: Photo Reports**
| Column | Type | Description |
|--------|------|-------------|
| Report_ID | Text | Unique ID |
| Report_Type | Text | Daily/Safety/Quality |
| Executor | Text | Who should submit |
| Date | Date | Report date |
| Time | Time | Deadline |
| Status | Text | Pending/Submitted |
| Photo_Link | URL | Drive folder link |
| Comment | Text | Worker comment |

### Step 3: Import n8n Workflow

```json
// Core workflow structure (simplified)
{
  "nodes": [
    {
      "name": "Telegram Trigger",
      "type": "n8n-nodes-base.telegramTrigger",
      "parameters": {
        "updates": ["message", "callback_query"]
      }
    },
    {
      "name": "Route Messages",
      "type": "n8n-nodes-base.switch",
      "parameters": {
        "rules": [
          {"value": "/start"},
          {"value": "/status"},
          {"value": "/help"},
          {"value": "text_reply"},
          {"value": "photo"},
          {"value": "location"}
        ]
      }
    },
    {
      "name": "Check Tasks Schedule",
      "type": "n8n-nodes-base.cron",
      "parameters": {
        "cronExpression": "* * * * *"
      }
    },
    {
      "name": "Get Pending Tasks",
      "type": "n8n-nodes-base.googleSheets",
      "parameters": {
        "operation": "readRows",
        "sheetName": "Tasks",
        "filters": {
          "Status": "Pending",
          "Send_Time": "now"
        }
      }
    },
    {
      "name": "Send Task Reminder",
      "type": "n8n-nodes-base.telegram",
      "parameters": {
        "operation": "sendMessage",
        "chatId": "={{$json.Executor_ID}}",
        "text": "📋 *Задача: {{$json.Task}}*\n📍 Объект: {{$json.Object}}\n⏰ Срок: {{$json.Date}}\n{{$json.Priority}}"
      }
    }
  ]
}
```

### Step 4: Configure Webhook

```bash
# Set Telegram webhook to n8n
curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" \
  -d "url=https://your-n8n-instance.com/webhook/telegram-project-manager"

# Verify webhook is set
curl "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo"
```

## Worker Commands

### Registration: /start

```
User: /start

Bot: 👋 Добро пожаловать в систему управления задачами!

Пожалуйста, укажите ваше имя:

User: Иван Петров

Bot: Выберите вашу роль:
[Прораб] [Рабочий] [Субподрядчик]

User: [Прораб]

Bot: ✅ Регистрация завершена!
Имя: Иван Петров
Роль: Прораб
ID: 123456789

Вы будете получать задачи автоматически.
Используйте /help для справки.
```

### Receiving Task

```
Bot: 📋 *ЗАДАЧА #TASK-047*
━━━━━━━━━━━━━━━━━━━━━
📍 Объект: ЖК Солнечный, Корпус 2
🏗 Секция: 5 этаж, кв. 51-55
📝 Задача: Монтаж электропроводки
⏰ Срок: 24.01.2026
🔴 Приоритет: Высокий
━━━━━━━━━━━━━━━━━━━━━

Ответьте на это сообщение для отчета:
• Текст: статус + комментарий
• Фото: прикрепите фото работ
• GPS: отправьте геолокацию
```

### Task Response

```
User: (reply to task message)
выполнено
Проводка смонтирована по всем квартирам, ждем приемку

Bot: ✅ Отчет принят!
━━━━━━━━━━━━━━━━━━━━━
📋 Задача: #TASK-047
📊 Статус: Выполнено
💬 Комментарий: Проводка смонтирована...
⏰ Время: 24.01.2026 14:35
━━━━━━━━━━━━━━━━━━━━━
```

### Photo Report

```
User: (sends photo as reply to task)
[Photo of completed electrical work]
Caption: Монтаж завершен, готово к проверке

Bot: 📷 Фото получено и сохранено!
━━━━━━━━━━━━━━━━━━━━━
📋 Задача: #TASK-047
🔗 Фото: [Ссылка на Google Drive]
💬 Комментарий: Монтаж завершен...
⏰ Время: 24.01.2026 14:38
━━━━━━━━━━━━━━━━━━━━━
```

### GPS Location

```
User: (sends location)
📍 [Location: 55.7558, 37.6173]

Bot: 📍 Геолокация получена!
━━━━━━━━━━━━━━━━━━━━━
📋 Задача: #TASK-047
🗺 Координаты: 55.7558, 37.6173
🔗 Карта: [Google Maps Link]
⏰ Время: 24.01.2026 14:40
━━━━━━━━━━━━━━━━━━━━━
```

## Manager Dashboard

### Google Sheets View

```
┌────────────────────────────────────────────────────────────────────────┐
│ TASK DASHBOARD                                          🔄 Auto-refresh │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  TODAY'S SUMMARY                                                       │
│  ┌───────────┬───────────┬───────────┬───────────┐                    │
│  │ Total: 24 │ ✅ Done:15│ ⏳ Pending:7│ ⚠️ Late:2│                    │
│  └───────────┴───────────┴───────────┴───────────┘                    │
│                                                                         │
│  TASK LIST                                             Filter: [Today ▼]│
│  ┌──────────┬────────────┬──────────┬────────┬────────┬──────────────┐│
│  │ Task ID  │ Task       │ Worker   │ Status │ Photo  │ Response     ││
│  ├──────────┼────────────┼──────────┼────────┼────────┼──────────────┤│
│  │ TASK-047 │ Электрика  │ Петров   │ ✅     │ 📷 3   │ Выполнено    ││
│  │ TASK-048 │ Сантехника │ Иванов   │ ⏳     │ -      │ -            ││
│  │ TASK-049 │ Штукатурка │ Сидоров  │ ⚠️     │ 📷 1   │ Частично     ││
│  └──────────┴────────────┴──────────┴────────┴────────┴──────────────┘│
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

## Python Integration

```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime, timedelta

class ProjectTaskManager:
    """Integration with n8n Project Management System"""

    def __init__(self, credentials_path: str, spreadsheet_id: str):
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_path, scope
        )
        self.client = gspread.authorize(creds)
        self.spreadsheet = self.client.open_by_key(spreadsheet_id)

    def create_task(self, task: dict) -> str:
        """Create new task in system"""
        tasks_sheet = self.spreadsheet.worksheet('Tasks')

        # Generate task ID
        all_tasks = tasks_sheet.get_all_records()
        task_num = len(all_tasks) + 1
        task_id = f"TASK-{task_num:04d}"

        # Prepare row
        row = [
            task_id,
            task.get('project', ''),
            task.get('object', ''),
            task.get('section', ''),
            task.get('description', ''),
            task.get('executor_name', ''),
            task.get('executor_id', ''),
            task.get('date', datetime.now().strftime('%d.%m.%Y')),
            task.get('send_time', '09:00'),
            task.get('priority', '🟡Medium'),
            'Pending',  # Status
            '',  # Response
            '',  # Response_Time
            '',  # Photo_Link
            '',  # GPS_Lat
            ''   # GPS_Lon
        ]

        tasks_sheet.append_row(row)
        return task_id

    def create_bulk_tasks(self, tasks: list) -> list:
        """Create multiple tasks at once"""
        task_ids = []
        for task in tasks:
            task_id = self.create_task(task)
            task_ids.append(task_id)
        return task_ids

    def get_today_summary(self) -> dict:
        """Get summary of today's tasks"""
        tasks_sheet = self.spreadsheet.worksheet('Tasks')
        all_tasks = tasks_sheet.get_all_records()

        today = datetime.now().strftime('%d.%m.%Y')
        today_tasks = [t for t in all_tasks if t['Date'] == today]

        return {
            'total': len(today_tasks),
            'completed': len([t for t in today_tasks if t['Status'] == 'Completed']),
            'pending': len([t for t in today_tasks if t['Status'] == 'Pending']),
            'partial': len([t for t in today_tasks if t['Status'] == 'Partial']),
            'with_photos': len([t for t in today_tasks if t['Photo_Link']])
        }

    def get_worker_performance(self, worker_name: str, days: int = 30) -> dict:
        """Analyze worker performance over period"""
        tasks_sheet = self.spreadsheet.worksheet('Tasks')
        all_tasks = tasks_sheet.get_all_records()

        cutoff_date = datetime.now() - timedelta(days=days)

        worker_tasks = [
            t for t in all_tasks
            if t['Executor'] == worker_name
            and datetime.strptime(t['Date'], '%d.%m.%Y') >= cutoff_date
        ]

        if not worker_tasks:
            return {'error': 'No tasks found'}

        completed = len([t for t in worker_tasks if t['Status'] == 'Completed'])
        total = len(worker_tasks)

        return {
            'worker': worker_name,
            'period_days': days,
            'total_tasks': total,
            'completed': completed,
            'completion_rate': round(completed / total * 100, 1),
            'with_photos': len([t for t in worker_tasks if t['Photo_Link']]),
            'with_gps': len([t for t in worker_tasks if t['GPS_Lat']])
        }


# Usage Example
if __name__ == "__main__":
    manager = ProjectTaskManager(
        'credentials.json',
        'your-spreadsheet-id'
    )

    # Create tasks for the week
    weekly_tasks = [
        {
            'project': 'ЖК Солнечный',
            'object': 'Корпус 2',
            'section': '5 этаж',
            'description': 'Монтаж электропроводки кв. 51-55',
            'executor_name': 'Петров И.И.',
            'executor_id': '123456789',
            'date': '24.01.2026',
            'send_time': '08:00',
            'priority': '🔴High'
        },
        {
            'project': 'ЖК Солнечный',
            'object': 'Корпус 2',
            'section': '5 этаж',
            'description': 'Монтаж сантехники кв. 51-55',
            'executor_name': 'Иванов А.П.',
            'executor_id': '987654321',
            'date': '25.01.2026',
            'send_time': '08:00',
            'priority': '🟡Medium'
        }
    ]

    task_ids = manager.create_bulk_tasks(weekly_tasks)
    print(f"Created tasks: {task_ids}")

    # Get summary
    summary = manager.get_today_summary()
    print(f"Today's summary: {summary}")
```

## n8n Workflow Templates

### Template 1: Morning Task Distribution

```yaml
name: Morning Task Distribution
trigger:
  type: cron
  expression: "0 8 * * 1-6"  # 8:00 AM, Mon-Sat

steps:
  - get_today_tasks:
      node: Google Sheets
      operation: readRows
      sheet: Tasks
      filter: Date = TODAY(), Status = Pending

  - group_by_worker:
      node: Code
      code: |
        const grouped = {};
        items.forEach(item => {
          const worker = item.json.Executor_ID;
          if (!grouped[worker]) grouped[worker] = [];
          grouped[worker].push(item.json);
        });
        return Object.entries(grouped).map(([id, tasks]) => ({
          worker_id: id,
          tasks: tasks
        }));

  - send_task_list:
      node: Telegram
      operation: sendMessage
      chatId: "={{$json.worker_id}}"
      text: |
        🌅 *Доброе утро! Ваши задачи на сегодня:*

        {{#each tasks}}
        ━━━━━━━━━━━━━━━━━━━━━
        {{priority}} *{{Task}}*
        📍 {{Object}} / {{Section}}
        ⏰ Срок: {{Date}}
        {{/each}}

        Ответьте на каждую задачу по мере выполнения.
```

### Template 2: Photo Report Collection

```yaml
name: Scheduled Photo Reports
trigger:
  type: cron
  expression: "0 12,17 * * 1-6"  # 12:00 and 17:00

steps:
  - get_photo_reports:
      node: Google Sheets
      operation: readRows
      sheet: Photo Reports
      filter: Date = TODAY(), Status = Pending

  - send_photo_request:
      node: Telegram
      operation: sendMessage
      chatId: "={{$json.Executor_ID}}"
      text: |
        📷 *Требуется фото-отчет*
        ━━━━━━━━━━━━━━━━━━━━━
        📋 Тип: {{$json.Report_Type}}
        📍 Объект: {{$json.Object}}
        ⏰ Срок: {{$json.Time}}

        Пожалуйста, отправьте фото с комментарием.
      replyMarkup:
        inline_keyboard:
          - [{text: "📷 Отправить фото", callback_data: "photo_{{$json.Report_ID}}"}]
```

### Template 3: End of Day Summary

```yaml
name: End of Day Report
trigger:
  type: cron
  expression: "0 18 * * 1-6"  # 18:00

steps:
  - get_day_stats:
      node: Google Sheets
      operation: readRows
      sheet: Tasks
      filter: Date = TODAY()

  - calculate_stats:
      node: Code
      code: |
        const stats = {
          total: items.length,
          completed: items.filter(i => i.json.Status === 'Completed').length,
          partial: items.filter(i => i.json.Status === 'Partial').length,
          pending: items.filter(i => i.json.Status === 'Pending').length,
          photos: items.filter(i => i.json.Photo_Link).length
        };
        stats.completion_rate = Math.round(stats.completed / stats.total * 100);
        return [{ json: stats }];

  - send_to_manager:
      node: Telegram
      operation: sendMessage
      chatId: "MANAGER_CHAT_ID"
      text: |
        📊 *Итоги дня: {{$now.format('DD.MM.YYYY')}}*
        ━━━━━━━━━━━━━━━━━━━━━

        📋 Всего задач: {{$json.total}}
        ✅ Выполнено: {{$json.completed}}
        ⏳ Частично: {{$json.partial}}
        ❌ Не выполнено: {{$json.pending}}

        📷 Фото-отчетов: {{$json.photos}}
        📈 Выполнение: {{$json.completion_rate}}%

        [Открыть таблицу]({{SPREADSHEET_URL}})
```

## Best Practices

### Task Design
1. Keep tasks atomic (1 task = 1 action)
2. Include clear location (Object + Section)
3. Set realistic deadlines
4. Use priority wisely (not everything is 🔴High)

### Photo Reports
1. Request photos at milestones, not continuously
2. Use Google Drive folders per project/date
3. Include location verification (GPS)
4. Set clear expectations (what should be in photo)

### Worker Engagement
1. Acknowledge all responses quickly
2. Provide daily feedback
3. Recognize high performers
4. Keep bot messages concise

## Resources

- **Repository**: https://github.com/datadrivenconstruction/Project-management-n8n-with-task-management-and-photo-reports
- **Demo Bot**: @ProjectManagementTasks_Bot
- **Demo Sheet**: [Google Sheets Demo](https://docs.google.com/spreadsheets/d/1fWi_0W_jqKa61h2oB3zZLdTDBK8_cQ123RtF70X1rwc)
- **n8n Documentation**: https://docs.n8n.io

---

*"Automation is not about replacing people, it's about freeing them to do what only people can do."*

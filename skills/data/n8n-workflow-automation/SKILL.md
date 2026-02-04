---
name: n8n-workflow-automation
description: "Build no-code/low-code automation workflows for construction using n8n. Automate data extraction, cost estimation, report generation, and system integrations without writing code."
---

# n8n Workflow Automation for Construction

## Overview

This skill implements visual workflow automation for construction processes using n8n. Automate repetitive tasks, integrate systems, and build PROJECT TO BUDGET pipelines without extensive programming.

**Inspired by DDC Methodology** - Automating the bridge between BIM models and cost estimation.

> "Автоматизация процесса 'от проекта к смете' позволяет сократить время на подготовку бюджета с недель до часов."
> — DDC LinkedIn Post

## Quick Start

### n8n Installation

```bash
# Using Docker (recommended)
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Using npm
npm install n8n -g
n8n start

# Access at: http://localhost:5678
```

## Construction Workflow Examples

### 1. Revit to Budget Pipeline

```json
{
  "name": "Revit to Budget Automation",
  "nodes": [
    {
      "name": "Watch Revit Export Folder",
      "type": "n8n-nodes-base.localFileTrigger",
      "parameters": {
        "path": "/data/revit_exports",
        "events": ["add"],
        "fileExtension": ".xlsx"
      }
    },
    {
      "name": "Read Excel Data",
      "type": "n8n-nodes-base.readWriteFile",
      "parameters": {
        "operation": "read",
        "filePath": "={{ $json.fileName }}"
      }
    },
    {
      "name": "Parse BIM Elements",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "language": "python",
        "code": "import pandas as pd\nimport json\n\ndf = pd.read_excel(items[0].binary.data)\n\nelements = df.to_dict('records')\n\nreturn [{'json': {'elements': elements, 'count': len(elements)}}]"
      }
    },
    {
      "name": "Match to Unit Prices",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://api.construction-prices.com/match",
        "method": "POST",
        "body": "={{ JSON.stringify($json.elements) }}"
      }
    },
    {
      "name": "Calculate Costs",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "language": "javascript",
        "code": "const elements = items[0].json.elements;\n\nlet totalCost = 0;\nconst costBreakdown = [];\n\nfor (const elem of elements) {\n  const cost = elem.quantity * elem.unit_price;\n  totalCost += cost;\n  costBreakdown.push({\n    category: elem.category,\n    quantity: elem.quantity,\n    unit_price: elem.unit_price,\n    total: cost\n  });\n}\n\nreturn [{\n  json: {\n    total_cost: totalCost,\n    breakdown: costBreakdown\n  }\n}];"
      }
    },
    {
      "name": "Generate Report",
      "type": "n8n-nodes-base.spreadsheetFile",
      "parameters": {
        "operation": "create",
        "fileName": "cost_estimate_{{ $now.format('yyyy-MM-dd') }}.xlsx"
      }
    },
    {
      "name": "Send Email Notification",
      "type": "n8n-nodes-base.emailSend",
      "parameters": {
        "to": "project-team@company.com",
        "subject": "New Cost Estimate Generated",
        "text": "Total estimate: ${{ $json.total_cost }}"
      }
    }
  ]
}
```

### 2. Daily Project Report Automation

```json
{
  "name": "Daily Project Report",
  "nodes": [
    {
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.cron",
      "parameters": {
        "cronExpression": "0 6 * * 1-5"
      }
    },
    {
      "name": "Fetch Project Data",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "{{ $env.PROJECT_API }}/status",
        "method": "GET"
      }
    },
    {
      "name": "Fetch Weather Data",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.openweathermap.org/data/2.5/weather",
        "qs": {
          "q": "{{ $json.project_location }}",
          "appid": "{{ $env.WEATHER_API_KEY }}"
        }
      }
    },
    {
      "name": "Generate Report",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "language": "javascript",
        "code": "const project = items[0].json;\nconst weather = items[1].json;\n\nconst report = {\n  date: new Date().toISOString().split('T')[0],\n  project_name: project.name,\n  progress: project.progress_pct,\n  weather: {\n    condition: weather.weather[0].main,\n    temp: Math.round(weather.main.temp - 273.15)\n  },\n  tasks_today: project.scheduled_tasks,\n  blockers: project.blockers || []\n};\n\nreturn [{ json: report }];"
      }
    },
    {
      "name": "Post to Slack",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "channel": "#project-updates",
        "text": "📊 Daily Report - {{ $json.project_name }}\n\nProgress: {{ $json.progress }}%\n🌡️ Weather: {{ $json.weather.condition }} ({{ $json.weather.temp }}°C)\n\nToday's Tasks:\n{{ $json.tasks_today.join('\\n') }}"
      }
    }
  ]
}
```

### 3. BIM Model Change Detection

```json
{
  "name": "BIM Change Detection",
  "nodes": [
    {
      "name": "Watch IFC Folder",
      "type": "n8n-nodes-base.localFileTrigger",
      "parameters": {
        "path": "/models",
        "events": ["change"],
        "fileExtension": ".ifc"
      }
    },
    {
      "name": "Extract Model Data",
      "type": "n8n-nodes-base.executeCommand",
      "parameters": {
        "command": "python /scripts/extract_ifc.py {{ $json.fileName }}"
      }
    },
    {
      "name": "Compare with Previous",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "language": "python",
        "code": "import json\n\ncurrent = json.loads(items[0].json.output)\nprevious = load_previous_version()\n\nchanges = {\n  'added': [],\n  'modified': [],\n  'deleted': []\n}\n\n# Compare logic\nfor elem in current:\n  if elem['id'] not in previous:\n    changes['added'].append(elem)\n  elif elem != previous[elem['id']]:\n    changes['modified'].append(elem)\n\nfor elem_id in previous:\n  if elem_id not in [e['id'] for e in current]:\n    changes['deleted'].append(previous[elem_id])\n\nreturn [{'json': changes}]"
      }
    },
    {
      "name": "Update Database",
      "type": "n8n-nodes-base.postgres",
      "parameters": {
        "operation": "executeQuery",
        "query": "INSERT INTO model_changes (timestamp, changes) VALUES (NOW(), '{{ JSON.stringify($json) }}')"
      }
    },
    {
      "name": "Notify Team",
      "type": "n8n-nodes-base.microsoftTeams",
      "parameters": {
        "message": "🔔 Model Updated\n\n+{{ $json.added.length }} elements added\n📝 {{ $json.modified.length }} elements modified\n-{{ $json.deleted.length }} elements deleted"
      }
    }
  ]
}
```

## Common Workflow Patterns

### Data Extraction Pattern

```javascript
// n8n Code Node - Extract BIM Quantities
const xlsx = require('xlsx');

// Read uploaded file
const workbook = xlsx.read(items[0].binary.data, { type: 'buffer' });
const sheetName = workbook.SheetNames[0];
const data = xlsx.utils.sheet_to_json(workbook.Sheets[sheetName]);

// Process BIM elements
const quantities = {};
for (const row of data) {
  const category = row['Category'] || 'Unknown';
  const volume = parseFloat(row['Volume']) || 0;

  if (!quantities[category]) {
    quantities[category] = { count: 0, volume: 0 };
  }
  quantities[category].count++;
  quantities[category].volume += volume;
}

return [{ json: { quantities, total_elements: data.length } }];
```

### Cost Matching Pattern

```javascript
// n8n Code Node - Match elements to unit prices
const elements = items[0].json.elements;
const priceDatabase = $env.PRICE_DATABASE;

const matched = [];

for (const elem of elements) {
  // Fuzzy match description to price items
  const match = await $http.post(`${priceDatabase}/search`, {
    query: elem.description,
    category: elem.category
  });

  matched.push({
    ...elem,
    matched_item: match.data.best_match,
    unit_price: match.data.unit_price,
    confidence: match.data.confidence
  });
}

return [{ json: { matched_elements: matched } }];
```

### Report Generation Pattern

```javascript
// n8n Code Node - Generate PDF Report
const PDFDocument = require('pdfkit');

const doc = new PDFDocument();
const buffers = [];

doc.on('data', buffers.push.bind(buffers));

// Header
doc.fontSize(20).text('Cost Estimate Report', { align: 'center' });
doc.moveDown();

// Project Info
doc.fontSize(12).text(`Project: ${items[0].json.project_name}`);
doc.text(`Date: ${new Date().toLocaleDateString()}`);
doc.moveDown();

// Cost Summary
doc.fontSize(14).text('Cost Summary', { underline: true });
for (const [category, cost] of Object.entries(items[0].json.costs)) {
  doc.fontSize(10).text(`${category}: $${cost.toLocaleString()}`);
}

doc.end();

return new Promise(resolve => {
  doc.on('end', () => {
    resolve([{
      json: { success: true },
      binary: {
        data: Buffer.concat(buffers).toString('base64'),
        fileName: 'cost_report.pdf',
        mimeType: 'application/pdf'
      }
    }]);
  });
});
```

## Integration Nodes

### Useful n8n Nodes for Construction

```yaml
Data Sources:
  - Google Sheets: Project tracking, cost databases
  - Airtable: Element databases, issue tracking
  - PostgreSQL: BIM databases, project data
  - HTTP Request: API integrations

File Processing:
  - Read/Write File: Excel, CSV, JSON
  - Execute Command: Python scripts, CLI tools
  - Code: Custom processing logic

Communication:
  - Slack: Team notifications
  - Microsoft Teams: Project updates
  - Email: Reports, alerts
  - Telegram: Mobile notifications

Cloud Storage:
  - AWS S3: Model storage
  - Google Drive: Document sharing
  - Dropbox: File sync
```

## Workflow Templates

### Template: QTO to Excel

```json
{
  "workflow": "QTO Extraction",
  "trigger": "Manual/Webhook",
  "steps": [
    "Receive IFC file",
    "Extract quantities (Python/IfcOpenShell)",
    "Group by category",
    "Add unit prices",
    "Calculate totals",
    "Generate Excel report",
    "Upload to cloud storage",
    "Send notification"
  ]
}
```

### Template: Daily Status Collection

```json
{
  "workflow": "Daily Status",
  "trigger": "Cron (6:00 AM)",
  "steps": [
    "Fetch project status from API",
    "Get weather forecast",
    "Check scheduled tasks",
    "Compile daily report",
    "Post to Slack/Teams",
    "Email to stakeholders"
  ]
}
```

## Best Practices

```markdown
1. **Error Handling**
   - Always add error branches
   - Log failures to database
   - Send alerts on critical failures

2. **Data Validation**
   - Validate input data format
   - Check for required fields
   - Handle missing values gracefully

3. **Performance**
   - Use batch processing for large datasets
   - Implement pagination for API calls
   - Cache frequently used data

4. **Security**
   - Store credentials in environment variables
   - Use encryption for sensitive data
   - Implement access controls
```

## Quick Reference

| Workflow Type | Trigger | Common Nodes |
|--------------|---------|--------------|
| File Processing | File Trigger | Code, HTTP, Spreadsheet |
| Scheduled Reports | Cron | HTTP, Code, Email |
| Data Sync | Webhook | Database, API, Code |
| Notifications | Various | Slack, Teams, Email |

## Resources

- **n8n Documentation**: https://docs.n8n.io
- **n8n Community**: https://community.n8n.io
- **DDC Website**: https://datadrivenconstruction.io

## Next Steps

- See `etl-pipeline` for code-based data pipelines
- See `llm-data-automation` for AI-powered automation
- See `vector-search` for intelligent document search

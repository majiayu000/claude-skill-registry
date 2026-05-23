---
name: Report Builder
slug: report-builder
description: Create formatted business reports with data, charts, tables, and executive summaries
category: document-creation
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "create report"
  - "generate report"
  - "build report"
  - "make business report"
  - "executive summary"
tags:
  - reports
  - business
  - analytics
  - data-visualization
  - summaries
---

# Report Builder

The Report Builder skill automates the creation of professional business reports with data analysis, visualizations, executive summaries, and formatted sections. It handles various report types including financial reports, project status updates, market analysis, performance reviews, and analytical reports. The skill integrates data from multiple sources and presents it in clear, actionable formats.

Generate reports in PDF, Word, or HTML formats with charts, tables, trend analysis, and key insights. Perfect for recurring reports, automated dashboards, and data-driven decision-making documentation.

## Core Workflows

### Workflow 1: Generate Executive Report
**Purpose:** Create high-level report with summary, key metrics, and recommendations

**Steps:**
1. Collect data from various sources
2. Calculate key performance indicators (KPIs)
3. Generate executive summary highlighting critical points
4. Create data visualizations (charts, graphs)
5. Add detailed sections with supporting data
6. Include recommendations and action items
7. Format with professional layout
8. Export to PDF with branding

**Implementation:**
```javascript
const PDFDocument = require('pdfkit');
const ChartJS = require('chartjs-node-canvas');
const fs = require('fs');

async function generateExecutiveReport(reportData, outputPath) {
  const doc = new PDFDocument({ margin: 50 });
  const stream = fs.createWriteStream(outputPath);
  doc.pipe(stream);

  // Cover page
  doc.fontSize(32)
     .fillColor('#2C3E50')
     .text(reportData.title, { align: 'center' })
     .moveDown()
     .fontSize(18)
     .fillColor('#7F8C8D')
     .text(reportData.subtitle, { align: 'center' })
     .moveDown(2)
     .fontSize(12)
     .text(`Reporting Period: ${reportData.period}`, { align: 'center' })
     .text(`Generated: ${new Date().toLocaleDateString()}`, { align: 'center' });

  // Company logo if provided
  if (reportData.logo) {
    doc.image(reportData.logo, doc.page.width / 2 - 50, 150, { width: 100 });
  }

  // Executive Summary
  doc.addPage();
  doc.fontSize(24)
     .fillColor('#2C3E50')
     .text('Executive Summary', { underline: true })
     .moveDown();

  doc.fontSize(11)
     .fillColor('#34495E')
     .text(reportData.executiveSummary, { align: 'justify', lineGap: 4 });

  // Key Metrics Section
  doc.moveDown(2);
  doc.fontSize(18)
     .fillColor('#2C3E50')
     .text('Key Performance Indicators');

  doc.moveDown();

  // KPI Cards (2x2 grid)
  const kpiWidth = 220;
  const kpiHeight = 100;
  const spacing = 20;

  reportData.kpis.forEach((kpi, index) => {
    const row = Math.floor(index / 2);
    const col = index % 2;
    const x = 50 + col * (kpiWidth + spacing);
    const y = doc.y + row * (kpiHeight + spacing);

    // KPI Card background
    doc.fillColor(kpi.trend === 'up' ? '#27AE60' : kpi.trend === 'down' ? '#E74C3C' : '#3498DB')
       .opacity(0.1)
       .rect(x, y, kpiWidth, kpiHeight)
       .fill();

    doc.opacity(1);

    // KPI Label
    doc.fontSize(10)
       .fillColor('#7F8C8D')
       .text(kpi.label, x + 10, y + 10, { width: kpiWidth - 20 });

    // KPI Value
    doc.fontSize(28)
       .fillColor('#2C3E50')
       .text(kpi.value, x + 10, y + 30);

    // KPI Change
    const changeColor = kpi.trend === 'up' ? '#27AE60' : kpi.trend === 'down' ? '#E74C3C' : '#7F8C8D';
    doc.fontSize(12)
       .fillColor(changeColor)
       .text(kpi.change, x + 10, y + 70);
  });

  // Adjust Y position after KPI grid
  doc.y += Math.ceil(reportData.kpis.length / 2) * (kpiHeight + spacing) + spacing;

  // Detailed Sections
  reportData.sections.forEach(async (section) => {
    doc.addPage();

    // Section Title
    doc.fontSize(20)
       .fillColor('#2C3E50')
       .text(section.title, { underline: true })
       .moveDown();

    // Section Content
    doc.fontSize(11)
       .fillColor('#34495E')
       .text(section.content, { align: 'justify', lineGap: 4 });

    // Add chart if section has data
    if (section.chartData) {
      doc.moveDown();
      const chartImage = await generateChart(section.chartData);
      doc.image(chartImage, 100, doc.y, { width: 400 });
      doc.moveDown(15); // Space for chart
    }

    // Add table if section has table data
    if (section.tableData) {
      doc.moveDown();
      addTable(doc, section.tableData);
    }
  });

  // Recommendations
  doc.addPage();
  doc.fontSize(20)
     .fillColor('#2C3E50')
     .text('Recommendations', { underline: true })
     .moveDown();

  reportData.recommendations.forEach((rec, index) => {
    doc.fontSize(11)
       .fillColor('#34495E')
       .text(`${index + 1}. ${rec}`, { lineGap: 6 });
    doc.moveDown(0.5);
  });

  // Footer on all pages
  const pages = doc.bufferedPageRange();
  for (let i = 0; i < pages.count; i++) {
    doc.switchToPage(i);
    doc.fontSize(8)
       .fillColor('#95A5A6')
       .text(
         `${reportData.company} | Confidential | Page ${i + 1} of ${pages.count}`,
         50,
         doc.page.height - 50,
         { align: 'center', width: doc.page.width - 100 }
       );
  }

  doc.end();

  return new Promise((resolve, reject) => {
    stream.on('finish', () => resolve(outputPath));
    stream.on('error', reject);
  });
}

async function generateChart(chartData) {
  const chartCanvas = new ChartJS.ChartJSNodeCanvas({ width: 800, height: 400 });

  const configuration = {
    type: chartData.type || 'bar',
    data: {
      labels: chartData.labels,
      datasets: [{
        label: chartData.label,
        data: chartData.values,
        backgroundColor: chartData.colors || '#3498DB',
        borderColor: '#2C3E50',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  };

  return await chartCanvas.renderToBuffer(configuration);
}

function addTable(doc, tableData) {
  const tableTop = doc.y;
  const cellPadding = 8;
  const rowHeight = 25;
  const colWidth = (doc.page.width - 100) / tableData.headers.length;

  // Header row
  doc.fillColor('#34495E')
     .rect(50, tableTop, doc.page.width - 100, rowHeight)
     .fill();

  doc.fillColor('#FFFFFF')
     .fontSize(10);

  tableData.headers.forEach((header, i) => {
    doc.text(header, 50 + i * colWidth + cellPadding, tableTop + cellPadding, {
      width: colWidth - cellPadding * 2
    });
  });

  // Data rows
  doc.fillColor('#34495E');

  tableData.rows.forEach((row, rowIndex) => {
    const y = tableTop + (rowIndex + 1) * rowHeight;

    // Alternate row colors
    if (rowIndex % 2 === 1) {
      doc.fillColor('#F8F9FA')
         .rect(50, y, doc.page.width - 100, rowHeight)
         .fill();
    }

    doc.fillColor('#2C3E50');

    row.forEach((cell, cellIndex) => {
      doc.text(cell, 50 + cellIndex * colWidth + cellPadding, y + cellPadding, {
        width: colWidth - cellPadding * 2
      });
    });
  });

  doc.y = tableTop + (tableData.rows.length + 1) * rowHeight + 10;
}
```

### Workflow 2: Monthly Performance Report
**Purpose:** Automated monthly report with metrics, trends, and comparisons

**Steps:**
1. Query data for current month and previous periods
2. Calculate month-over-month and year-over-year changes
3. Generate trend charts
4. Identify top performers and areas of concern
5. Create comparison tables
6. Add narrative insights based on data patterns
7. Format and distribute report

**Implementation:**
```javascript
async function generateMonthlyReport(month, year, dataSource) {
  // Fetch data
  const currentData = await dataSource.getMonthData(month, year);
  const previousMonthData = await dataSource.getMonthData(month - 1, year);
  const lastYearData = await dataSource.getMonthData(month, year - 1);

  // Calculate metrics
  const metrics = {
    revenue: {
      current: currentData.revenue,
      momChange: calculatePercentChange(currentData.revenue, previousMonthData.revenue),
      yoyChange: calculatePercentChange(currentData.revenue, lastYearData.revenue)
    },
    customers: {
      current: currentData.customers,
      momChange: calculatePercentChange(currentData.customers, previousMonthData.customers),
      yoyChange: calculatePercentChange(currentData.customers, lastYearData.customers)
    },
    avgOrderValue: {
      current: currentData.revenue / currentData.orders,
      momChange: calculatePercentChange(
        currentData.revenue / currentData.orders,
        previousMonthData.revenue / previousMonthData.orders
      )
    }
  };

  // Generate report data
  const reportData = {
    title: 'Monthly Performance Report',
    subtitle: `${getMonthName(month)} ${year}`,
    period: `${getMonthName(month)} 1-${new Date(year, month, 0).getDate()}, ${year}`,
    company: 'Your Company',

    executiveSummary: generateExecutiveSummary(metrics, currentData),

    kpis: [
      {
        label: 'Total Revenue',
        value: formatCurrency(metrics.revenue.current),
        change: `${metrics.revenue.momChange > 0 ? '+' : ''}${metrics.revenue.momChange.toFixed(1)}% MoM`,
        trend: metrics.revenue.momChange > 0 ? 'up' : 'down'
      },
      {
        label: 'New Customers',
        value: metrics.customers.current.toLocaleString(),
        change: `${metrics.customers.yoyChange > 0 ? '+' : ''}${metrics.customers.yoyChange.toFixed(1)}% YoY`,
        trend: metrics.customers.yoyChange > 0 ? 'up' : 'down'
      },
      {
        label: 'Avg Order Value',
        value: formatCurrency(metrics.avgOrderValue.current),
        change: `${metrics.avgOrderValue.momChange > 0 ? '+' : ''}${metrics.avgOrderValue.momChange.toFixed(1)}% MoM`,
        trend: metrics.avgOrderValue.momChange > 0 ? 'up' : 'down'
      },
      {
        label: 'Customer Satisfaction',
        value: `${currentData.satisfaction}%`,
        change: 'Stable',
        trend: 'neutral'
      }
    ],

    sections: [
      {
        title: 'Revenue Analysis',
        content: `Revenue for ${getMonthName(month)} totaled ${formatCurrency(metrics.revenue.current)}, representing a ${Math.abs(metrics.revenue.momChange).toFixed(1)}% ${metrics.revenue.momChange > 0 ? 'increase' : 'decrease'} compared to last month...`,
        chartData: {
          type: 'line',
          labels: getLast6Months(month, year),
          values: await dataSource.getRevenueHistory(6),
          label: 'Revenue Trend'
        }
      },
      {
        title: 'Customer Acquisition',
        content: `Customer acquisition efforts resulted in ${metrics.customers.current} new customers this month...`,
        tableData: {
          headers: ['Channel', 'Customers', 'Cost', 'CAC'],
          rows: currentData.acquisitionChannels.map(channel => [
            channel.name,
            channel.customers.toString(),
            formatCurrency(channel.cost),
            formatCurrency(channel.cost / channel.customers)
          ])
        }
      },
      {
        title: 'Product Performance',
        content: 'Top-performing products and categories for the period...',
        chartData: {
          type: 'bar',
          labels: currentData.topProducts.map(p => p.name),
          values: currentData.topProducts.map(p => p.revenue),
          label: 'Revenue by Product'
        }
      }
    ],

    recommendations: generateRecommendations(metrics, currentData)
  };

  return await generateExecutiveReport(reportData, `./reports/monthly-${year}-${month}.pdf`);
}

function calculatePercentChange(current, previous) {
  if (previous === 0) return 0;
  return ((current - previous) / previous) * 100;
}

function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount);
}

function generateExecutiveSummary(metrics, data) {
  const revenueDirection = metrics.revenue.momChange > 0 ? 'increased' : 'decreased';
  const revenuePercent = Math.abs(metrics.revenue.momChange).toFixed(1);

  return `
    Revenue ${revenueDirection} by ${revenuePercent}% compared to the previous month,
    driven primarily by ${data.primaryGrowthDriver}. Customer acquisition
    ${metrics.customers.momChange > 0 ? 'exceeded' : 'fell short of'} targets, with
    ${metrics.customers.current} new customers. The average order value ${metrics.avgOrderValue.momChange > 0 ? 'improved' : 'declined'}
    by ${Math.abs(metrics.avgOrderValue.momChange).toFixed(1)}%, indicating
    ${metrics.avgOrderValue.momChange > 0 ? 'successful upselling efforts' : 'price pressure in the market'}.
  `.trim();
}

function generateRecommendations(metrics, data) {
  const recommendations = [];

  if (metrics.revenue.momChange < -5) {
    recommendations.push('Consider launching promotional campaigns to boost short-term revenue');
  }

  if (metrics.customers.momChange < 0) {
    recommendations.push('Increase marketing spend in top-performing acquisition channels');
  }

  if (metrics.avgOrderValue.momChange < 0) {
    recommendations.push('Implement cross-selling and bundling strategies to increase order values');
  }

  if (data.satisfaction < 80) {
    recommendations.push('Focus on improving customer satisfaction through enhanced support and service quality');
  }

  return recommendations;
}
```

### Workflow 3: Project Status Report
**Purpose:** Generate project progress reports with milestones, tasks, and risks

**Steps:**
1. Collect project data (tasks, milestones, team members)
2. Calculate completion percentage and timeline status
3. Identify completed, in-progress, and overdue items
4. List risks and issues
5. Create Gantt chart or timeline visualization
6. Add team member contributions
7. Include next steps and action items
8. Format as stakeholder-ready report

**Implementation:**
```javascript
async function generateProjectReport(projectData, outputPath) {
  const completionRate = calculateCompletionRate(projectData.tasks);
  const scheduleStatus = assessScheduleStatus(projectData);

  const reportData = {
    title: `Project Status Report: ${projectData.name}`,
    subtitle: `Status as of ${new Date().toLocaleDateString()}`,
    period: `${projectData.startDate} - ${projectData.endDate}`,
    company: projectData.organization,

    executiveSummary: `
      The ${projectData.name} project is currently ${completionRate}% complete.
      The project is ${scheduleStatus.status} schedule by ${scheduleStatus.variance} days.
      ${projectData.risks.length} risks have been identified and are being actively managed.
    `,

    kpis: [
      {
        label: 'Completion',
        value: `${completionRate}%`,
        change: `${projectData.tasksCompletedThisWeek} tasks completed this week`,
        trend: completionRate > 50 ? 'up' : 'neutral'
      },
      {
        label: 'Schedule Status',
        value: scheduleStatus.status,
        change: `${Math.abs(scheduleStatus.variance)} days ${scheduleStatus.variance > 0 ? 'ahead' : 'behind'}`,
        trend: scheduleStatus.variance >= 0 ? 'up' : 'down'
      },
      {
        label: 'Budget',
        value: formatCurrency(projectData.spentBudget),
        change: `${((projectData.spentBudget / projectData.totalBudget) * 100).toFixed(1)}% of total`,
        trend: projectData.spentBudget <= projectData.totalBudget ? 'up' : 'down'
      },
      {
        label: 'Team Health',
        value: projectData.teamMorale,
        change: 'Based on last survey',
        trend: 'neutral'
      }
    ],

    sections: [
      {
        title: 'Milestones',
        content: 'Current status of project milestones:',
        tableData: {
          headers: ['Milestone', 'Due Date', 'Status', 'Completion'],
          rows: projectData.milestones.map(m => [
            m.name,
            m.dueDate,
            m.status,
            `${m.completion}%`
          ])
        }
      },
      {
        title: 'Completed This Period',
        content: projectData.completedTasks.map(t => `• ${t.name}`).join('\n')
      },
      {
        title: 'In Progress',
        content: projectData.inProgressTasks.map(t => `• ${t.name} (${t.assignee})`).join('\n')
      },
      {
        title: 'Risks and Issues',
        content: projectData.risks.length > 0
          ? projectData.risks.map((r, i) => `${i + 1}. ${r.description} (Impact: ${r.impact}, Mitigation: ${r.mitigation})`).join('\n\n')
          : 'No significant risks identified at this time.'
      }
    ],

    recommendations: [
      ...projectData.nextSteps.map(step => `Complete: ${step}`),
      ...projectData.risks.filter(r => r.impact === 'High').map(r => `Address high-impact risk: ${r.description}`)
    ]
  };

  return await generateExecutiveReport(reportData, outputPath);
}

function calculateCompletionRate(tasks) {
  const total = tasks.length;
  const completed = tasks.filter(t => t.status === 'completed').length;
  return Math.round((completed / total) * 100);
}

function assessScheduleStatus(projectData) {
  const today = new Date();
  const expectedCompletion = new Date(projectData.expectedCompletionDate);
  const originalEnd = new Date(projectData.endDate);

  const daysVariance = Math.round((expectedCompletion - originalEnd) / (1000 * 60 * 60 * 24));

  return {
    status: daysVariance <= 0 ? 'On' : 'Behind',
    variance: daysVariance
  };
}
```

### Workflow 4: Financial Report Generation
**Purpose:** Create financial statements and analysis reports

**Steps:**
1. Extract financial data from accounting system
2. Calculate financial ratios and metrics
3. Generate balance sheet, income statement, cash flow
4. Create trend analysis and comparisons
5. Add charts for revenue, expenses, profit margins
6. Include notes and explanations for variances
7. Format according to accounting standards
8. Export as PDF with proper formatting

### Workflow 5: Automated Report Scheduling
**Purpose:** Schedule and automatically generate recurring reports

**Steps:**
1. Define report schedule (daily, weekly, monthly)
2. Set up data source connections
3. Create report template
4. Schedule report generation job
5. Auto-generate at specified intervals
6. Distribute via email or file storage
7. Archive generated reports
8. Send notifications on completion

**Implementation:**
```javascript
const cron = require('node-cron');
const nodemailer = require('nodemailer');

class ReportScheduler {
  constructor() {
    this.schedules = [];
  }

  scheduleReport(config) {
    const job = cron.schedule(config.cronExpression, async () => {
      try {
        console.log(`Generating ${config.reportType} report...`);

        // Generate report
        const reportPath = await this.generateReport(config);

        // Send report
        if (config.emailRecipients) {
          await this.emailReport(reportPath, config.emailRecipients, config);
        }

        // Archive
        if (config.archivePath) {
          await this.archiveReport(reportPath, config.archivePath);
        }

        console.log(`Report generated successfully: ${reportPath}`);
      } catch (error) {
        console.error(`Report generation failed: ${error.message}`);
        this.notifyFailure(config, error);
      }
    });

    this.schedules.push({ config, job });
  }

  async generateReport(config) {
    switch (config.reportType) {
      case 'monthly':
        return await generateMonthlyReport(new Date().getMonth(), new Date().getFullYear(), config.dataSource);
      case 'project':
        return await generateProjectReport(await config.dataSource.getProjectData(), config.outputPath);
      default:
        throw new Error(`Unknown report type: ${config.reportType}`);
    }
  }

  async emailReport(reportPath, recipients, config) {
    const transporter = nodemailer.createTransporter(config.emailConfig);

    await transporter.sendMail({
      from: config.emailConfig.from,
      to: recipients.join(', '),
      subject: `${config.reportName} - ${new Date().toLocaleDateString()}`,
      html: `
        <p>Please find attached the automated ${config.reportName}.</p>
        <p>This report was generated on ${new Date().toLocaleString()}.</p>
      `,
      attachments: [
        {
          filename: `${config.reportName}.pdf`,
          path: reportPath
        }
      ]
    });
  }

  async archiveReport(reportPath, archivePath) {
    const fs = require('fs').promises;
    const path = require('path');

    const timestamp = new Date().toISOString().replace(/:/g, '-');
    const archiveFilename = `report-${timestamp}.pdf`;

    await fs.copyFile(reportPath, path.join(archivePath, archiveFilename));
  }
}

// Usage:
const scheduler = new ReportScheduler();

scheduler.scheduleReport({
  reportType: 'monthly',
  reportName: 'Monthly Performance Report',
  cronExpression: '0 9 1 * *', // 9 AM on 1st of each month
  dataSource: myDataSource,
  outputPath: './reports/monthly-latest.pdf',
  emailRecipients: ['ceo@company.com', 'cfo@company.com'],
  emailConfig: { /* nodemailer config */ },
  archivePath: './reports/archive'
});
```

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Generate report | "create [report type] for [period]" |
| Executive report | "generate executive summary" |
| Monthly report | "create monthly performance report" |
| Project status | "generate project status report" |
| Add chart | "include [chart type] in report" |
| Schedule report | "automate [report] generation" |
| Custom report | "build custom report with [sections]" |

## Best Practices

- **Data Accuracy:** Validate all data sources before generating reports
- **Consistent Format:** Use templates for recurring report types
- **Executive Summary:** Always start with key takeaways for busy executives
- **Visual First:** Use charts and graphs to convey trends quickly
- **Actionable Insights:** Include specific recommendations, not just data
- **Version Control:** Track report versions and changes
- **Distribution:** Know your audience and tailor depth accordingly
- **Timeliness:** Generate reports on consistent schedules
- **Context:** Provide comparisons (MoM, YoY, vs. targets)
- **Professional Layout:** Maintain consistent branding and formatting
- **Accessibility:** Ensure reports are readable on all devices
- **Archive:** Keep historical reports for trend analysis

## Common Patterns

**Quarterly Business Review:**
```javascript
const qbrData = {
  title: 'Q4 2025 Business Review',
  sections: ['Financial Performance', 'Operational Metrics', 'Market Position', 'Strategic Initiatives'],
  compareAgainst: ['Q3 2025', 'Q4 2024'],
  includeForecast: true,
  forecastPeriod: 'Q1 2026'
};
```

**Sales Dashboard:**
```javascript
const salesReport = {
  kpis: ['Revenue', 'Deals Closed', 'Pipeline Value', 'Conversion Rate'],
  breakdowns: ['by Region', 'by Product', 'by Sales Rep'],
  trends: ['Last 12 months', 'Year over Year'],
  targets: true
};
```

## Dependencies

Install required packages:
```bash
npm install pdfkit chartjs-node-canvas
npm install node-cron nodemailer  # For scheduling and email
npm install exceljs                # For Excel export option
npm install handlebars             # For templating
```

## Error Handling

- **Missing Data:** Handle null/undefined values gracefully
- **Data Source Failures:** Retry logic for API/database queries
- **Chart Generation:** Fallback to tables if charts fail
- **File System:** Check permissions before writing files
- **Email Failures:** Log errors and retry sending
- **Schedule Conflicts:** Prevent overlapping report generation

## Performance Tips

- Cache chart images for reuse
- Use streaming for large datasets
- Generate charts in parallel when possible
- Compress images before embedding
- Use pagination for very large reports
- Pre-aggregate data for performance

## Advanced Features

**Interactive HTML Reports:**
```javascript
const html = `
  <html>
    <head>
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
      <h1>${reportData.title}</h1>
      <canvas id="chart"></canvas>
      <script>
        // Interactive Chart.js visualization
      </script>
    </body>
  </html>
`;
```

**Multi-Format Export:**
```javascript
async function exportReport(reportData, formats = ['pdf', 'html', 'xlsx']) {
  const outputs = {};
  if (formats.includes('pdf')) outputs.pdf = await generatePDF(reportData);
  if (formats.includes('html')) outputs.html = await generateHTML(reportData);
  if (formats.includes('xlsx')) outputs.xlsx = await generateExcel(reportData);
  return outputs;
}
```
---
name: accessibility-test-axe
description: Эксперт по a11y тестированию. Используй для axe-core, automated testing и accessibility audits.
---

# Axe-Core Accessibility Testing Expert

Эксперт по автоматизированному тестированию доступности с использованием axe-core — индустриального стандарта для проверки соответствия WCAG.

## Основная философия

Используйте **shift-left подход** — интегрируйте проверки доступности на ранних этапах разработки, а не после релиза. Комбинируйте автоматизированное сканирование axe-core с ручным тестированием.

## Настройка axe-core

### Установка
```bash
npm install axe-core @axe-core/playwright @axe-core/react
```

### Базовое использование в браузере
```javascript
import axe from 'axe-core';

async function runAccessibilityAudit(element = document) {
  try {
    const results = await axe.run(element, {
      runOnly: {
        type: 'tag',
        values: ['wcag2a', 'wcag2aa', 'wcag21aa']
      }
    });

    return {
      violations: results.violations,
      passes: results.passes,
      incomplete: results.incomplete,
      inapplicable: results.inapplicable
    };
  } catch (error) {
    console.error('Accessibility audit failed:', error);
    throw error;
  }
}
```

## Интеграция с Playwright

```javascript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility Tests', () => {
  test('should not have accessibility violations', async ({ page }) => {
    await page.goto('/');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('specific component accessibility', async ({ page }) => {
    await page.goto('/components/modal');

    const results = await new AxeBuilder({ page })
      .include('#modal-component')
      .exclude('.decorative-element')
      .analyze();

    expect(results.violations).toEqual([]);
  });
});
```

## Интеграция со Storybook

```javascript
// .storybook/test-runner.js
const { injectAxe, checkA11y } = require('axe-playwright');

module.exports = {
  async preRender(page) {
    await injectAxe(page);
  },
  async postRender(page) {
    await checkA11y(page, '#storybook-root', {
      detailedReport: true,
      detailedReportOptions: {
        html: true
      }
    });
  }
};
```

## CI/CD интеграция (GitHub Actions)

```yaml
name: Accessibility Tests

on: [push, pull_request]

jobs:
  a11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run accessibility tests
        run: npm run test:a11y

      - name: Upload results
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: a11y-report
          path: a11y-results.json
```

## Обработка результатов

```javascript
function processViolations(violations) {
  const report = {
    critical: [],
    serious: [],
    moderate: [],
    minor: []
  };

  violations.forEach(violation => {
    const issue = {
      id: violation.id,
      impact: violation.impact,
      description: violation.description,
      help: violation.help,
      helpUrl: violation.helpUrl,
      nodes: violation.nodes.map(node => ({
        html: node.html,
        target: node.target,
        failureSummary: node.failureSummary
      }))
    };

    report[violation.impact].push(issue);
  });

  return report;
}
```

## Конфигурация правил

```javascript
const axeConfig = {
  rules: [
    // Отключение правил для декоративных элементов
    { id: 'image-alt', enabled: true },
    { id: 'color-contrast', enabled: true },
    { id: 'label', enabled: true },

    // Исключения для специфичных случаев
    {
      id: 'button-name',
      selector: 'button:not(.icon-only)'
    }
  ],

  // Исключение областей
  exclude: [
    '.third-party-widget',
    '#ads-container'
  ]
};
```

## React интеграция

```javascript
import React from 'react';
import ReactDOM from 'react-dom';
import axe from '@axe-core/react';

if (process.env.NODE_ENV !== 'production') {
  axe(React, ReactDOM, 1000);
}

// Компонент отчёта
function AccessibilityReport({ violations }) {
  if (!violations.length) {
    return <div className="a11y-pass">No accessibility violations found</div>;
  }

  return (
    <div className="a11y-violations" role="alert">
      <h2>Accessibility Issues Found: {violations.length}</h2>
      <ul>
        {violations.map(violation => (
          <li key={violation.id}>
            <strong>{violation.impact}</strong>: {violation.description}
            <a href={violation.helpUrl} target="_blank" rel="noopener">
              Learn more
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## Типичные нарушения и исправления

### Недостаточный контраст цвета
```css
/* Плохо */
.text-light {
  color: #999;
  background: #fff;
}

/* Хорошо - соотношение 4.5:1 */
.text-light {
  color: #767676;
  background: #fff;
}
```

### Отсутствие label у формы
```html
<!-- Плохо -->
<input type="email" placeholder="Email">

<!-- Хорошо -->
<label for="email">Email</label>
<input type="email" id="email" placeholder="email@example.com">
```

### Кнопка без текста
```html
<!-- Плохо -->
<button><svg>...</svg></button>

<!-- Хорошо -->
<button aria-label="Close menu">
  <svg aria-hidden="true">...</svg>
</button>
```

## Мониторинг и отчётность

```javascript
class AccessibilityMonitor {
  constructor() {
    this.history = [];
  }

  async audit(url) {
    const results = await runAccessibilityAudit();

    this.history.push({
      timestamp: new Date().toISOString(),
      url,
      violationCount: results.violations.length,
      violations: results.violations
    });

    return this.generateTrend();
  }

  generateTrend() {
    const recent = this.history.slice(-10);
    return {
      current: recent[recent.length - 1]?.violationCount || 0,
      trend: this.calculateTrend(recent),
      history: recent
    };
  }
}
```

## Лучшие практики

1. **Интегрируйте в CI/CD** — блокируйте merge при critical нарушениях
2. **Тестируйте рано** — используйте в dev режиме React/Vue
3. **Комбинируйте методы** — автоматические тесты + ручное тестирование
4. **Документируйте исключения** — объясняйте почему правило отключено
5. **Отслеживайте тренды** — мониторьте количество нарушений во времени

---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs. Includes 149 tests e2e pour Construction Gauthier / Ma Place RH.
license: Complete terms in LICENSE.txt
---

# Web Application Testing

To test local web applications, write native Python Playwright scripts.

**Helper Scripts Available**:
- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)

**Always run scripts with `--help` first** to see usage. DO NOT read the source until you try running the script first and find that a customized solution is abslutely necessary. These scripts can be very large and thus pollute your context window. They exist to be called directly as black-box scripts rather than ingested into your context window.

## Decision Tree: Choosing Your Approach

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## Example: Using with_server.py

To start a server, run `--help` first, then use the helper:

**Single server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Multiple servers (e.g., backend + frontend):**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

To create an automation script, include only Playwright logic (servers are managed automatically):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Always launch chromium in headless mode
    page = browser.new_page()
    page.goto('http://localhost:5173') # Server already running and ready
    page.wait_for_load_state('networkidle') # CRITICAL: Wait for JS to execute
    # ... your automation logic
    browser.close()
```

## Reconnaissance-Then-Action Pattern

1. **Inspect rendered DOM**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **Identify selectors** from inspection results

3. **Execute actions** using discovered selectors

## Common Pitfall

❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps
✅ **Do** wait for `page.wait_for_load_state('networkidle')` before inspection

## Best Practices

- **Use bundled scripts as black boxes** - To accomplish a task, consider whether one of the scripts available in `scripts/` can help. These scripts handle common, complex workflows reliably without cluttering the context window. Use `--help` to see usage, then invoke directly. 
- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`

## Reference Files

- **examples/** - Examples showing common patterns:
  - `element_discovery.py` - Discovering buttons, links, and inputs on a page
  - `static_html_automation.py` - Using file:// URLs for local HTML
  - `console_logging.py` - Capturing console logs during automation

---

## Construction Gauthier - Tests E2E Playwright

Le projet Construction Gauthier dispose d'une suite complète de tests Playwright TypeScript (149 tests).

### Commandes d'exécution

```bash
# Tous les tests (149 tests, ~1 min)
npx playwright test

# Tests par projet
npx playwright test --project=chromium           # Tests auth généraux (15)
npx playwright test --project=ma-place-rh        # Tests Ma Place RH (99)
npx playwright test --project=ma-place-rh:security   # Tests permissions (18)
npx playwright test --project=ma-place-rh:workflows  # Tests workflows (17)

# Tests par fonctionnalité
npx playwright test specs/features/evaluations.spec.ts
npx playwright test specs/features/surveys.spec.ts
npx playwright test specs/leave/

# Mode debug avec UI
npx playwright test --ui

# Voir le rapport HTML
npx playwright show-report
```

### Structure des tests Ma Place RH

```
modules/ma-place-rh/tests/e2e/
├── fixtures/
│   ├── auth.fixture.ts      # Multi-contextes (employeePage, managerPage, directorPage)
│   └── index.ts
├── utils/
│   └── test-users.ts        # Utilisateurs fictifs de test
├── page-objects/
│   ├── base.page.ts
│   ├── employee/leave-request.page.ts
│   └── manager/approvals.page.ts
├── workflows/
│   └── leave-request.workflow.ts
└── specs/
    ├── auth/permissions.spec.ts      # 18 tests permissions/sécurité
    ├── leave/full-workflow.spec.ts   # 17 tests congés
    └── features/
        ├── dashboards.spec.ts        # 10 tests
        ├── evaluations.spec.ts       # 7 tests
        ├── surveys.spec.ts           # 6 tests
        ├── team.spec.ts              # 6 tests
        ├── performance.spec.ts       # 6 tests
        ├── competences.spec.ts       # 5 tests
        ├── documents.spec.ts         # 5 tests
        ├── onboarding.spec.ts        # 5 tests
        ├── 2x4-news.spec.ts          # 4 tests
        ├── events.spec.ts            # 4 tests
        ├── roles-permissions.spec.ts # 4 tests
        └── reports.spec.ts           # 4 tests
```

### Utilisateurs de test

Les tests utilisent des utilisateurs fictifs via le mode `VITE_AUTH_BYPASS=true`:

| Rôle | ID | Email |
|------|-----|-------|
| Admin | 11111111-... | admin@constructiongauthier.local |
| Directeur | 22222222-... | cto@constructiongauthier.local |
| Manager | 33333333-... | gestionnaire.rh@constructiongauthier.local |
| Employé | 44444444-... | employe@constructiongauthier.local |

### Ajouter un nouveau test

1. Créer le fichier dans `specs/features/` ou `specs/[feature]/`
2. Importer les fixtures: `import { test, expect } from '../../fixtures';`
3. Utiliser les pages pré-authentifiées: `employeePage`, `managerPage`, `directorPage`

```typescript
import { test, expect } from '../../fixtures';

test.describe('Ma Feature', () => {
  test('Employé peut accéder à la feature', async ({ employeePage }) => {
    await employeePage.goto('/ma-place-rh/ma-feature');
    await employeePage.waitForLoadState('networkidle');
    await expect(employeePage.locator('h1')).toContainText('Ma Feature');
  });

  test('Employé ne peut pas accéder à la vue manager', async ({ employeePage }) => {
    await employeePage.goto('/ma-place-rh/manager/ma-feature');
    await employeePage.waitForLoadState('networkidle');
    expect(employeePage.url()).not.toContain('/manager/ma-feature');
  });
});
```

### Prérequis

- L'app doit tourner sur `http://localhost:5173` avec `VITE_AUTH_BYPASS=true`
- Ou laisser Playwright démarrer le serveur automatiquement (configuré dans `playwright.config.ts`)
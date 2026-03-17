---
name: playwright-demo:debug
description: Debug failing Playwright demo steps - selectors, auth, timing, and alignment issues
---

# Debug Playwright Demo Issues

Troubleshoot and fix failing steps in Playwright demo walkthrough tests.

## When to Use

- A demo recording step fails (selector not found, auth error, timeout)
- Narration-video alignment validation fails
- Video shows wrong content during narration
- Multiple voices overlapping in output

## Debugging Workflow

1. Check the test output for `[demo]` log lines — identify which step failed
2. Look at screenshots in `local_experiments/test-results/<test-dir>/test-failed-1.png`
3. Run validation to check structural issues:

```bash
python3 local_experiments/validate-alignment.py
```

## Common Issues

### Selector not found

**Symptom**: `element not visible` or `timeout waiting for selector`

Screenshot the page to see actual DOM:

```bash
cd kagenti/ui-v2 && NODE_PATH=node_modules node -e "
const { chromium } = require('@playwright/test');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ ignoreHTTPSErrors: true });
  await p.goto('TARGET_URL', { waitUntil: 'networkidle', timeout: 30000 });
  await p.screenshot({ path: '/tmp/kagenti/debug.png', fullPage: true });
  const els = await p.evaluate(() =>
    Array.from(document.querySelectorAll('a, button, [role=tab]')).map(e => ({
      tag: e.tagName, text: e.textContent?.trim()?.substring(0, 50), href: e.href
    }))
  );
  console.log(JSON.stringify(els, null, 2));
  await b.close();
})();
"
```

### Missing markStep timestamp

**Symptom**: Validation shows `Section [name] has no markStep() timestamp`

**Fix**: The `markStep()` call is inside a conditional block that didn't execute. Move it outside:

```typescript
// WRONG - inside conditional
if (await element.isVisible()) {
  markStep('section_name');
  await element.click();
}

// RIGHT - outside conditional
markStep('section_name');
if (await element.isVisible()) {
  await element.click();
}
```

### Keycloak auth lost on SPA navigation

**Symptom**: Page redirects to Keycloak after clicking sidebar link

**Fix**: Use SPA sidebar clicks (client-side routing), not `page.goto()`:

```typescript
// WRONG - full reload loses Keycloak tokens
await page.goto(`${UI_URL}/agents`);

// RIGHT - SPA navigation preserves tokens
const link = page.locator('nav a').filter({ hasText: /^Agents$/ });
await demoClick(link.first(), 'Agents sidebar');
```

### MLflow OIDC login

**Symptom**: MLflow shows login page or "User not allowed"

MLflow uses 2-stage auth:
1. MLflow's own OIDC page at `/oidc/ui/auth` — click SSO button
2. Keycloak login (may auto-login if session exists)

After login, navigate to `${MLFLOW_URL}/#/experiments` (hash routing).

### Kiali OAuth

**Symptom**: OpenShift login page shown

Kiali uses OpenShift OAuth — needs `kubeadmin` credentials (separate from Keycloak). Script auto-discovers from `<kubeconfig-dir>/kubeadmin-password`.

### Overlapping audio

**Symptom**: Multiple voices playing simultaneously

**Cause**: Missing timestamps → audio segments placed at wrong positions

**Fix**: Ensure ALL `markStep()` calls fire unconditionally. Run validation:

```bash
python3 local_experiments/validate-alignment.py
```

Check for `NO TIMESTAMP` errors. Fix those first.

## Task Tracking

On invocation:
1. TaskCreate: `playwright-demos | <cluster> | ad-hoc | debug | | <issue description>`
2. TaskUpdate when issue is resolved

## Related Skills

- `playwright-demo` — Main demo recording workflow
- `kagenti:ui-debug` — Debug Kagenti UI issues
- `k8s:health` — Check platform health

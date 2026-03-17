---
name: lightning-2025-features
description: Salesforce Lightning Web Components Winter '26 and 2025 features
---

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems


### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation


---

# Lightning Web Components 2025 Features

## lightning/graphql Module (Winter '26)

New module replaces deprecated `lightning/uiGraphQLApi`:

### Migration

```javascript
// ❌ Old (deprecated)
import { gql, graphql } from 'lightning/uiGraphQLApi';

// ✅ New (Winter '26)
import { gql, graphql } from 'lightning/graphql';

export default class MyComponent extends LightningElement {
  @wire(graphql, {
    query: gql`
      query getAccount($id: ID!) {
        uiapi {
          query {
            Account(where: { Id: { eq: $id } }) {
              edges {
                node {
                  Id
                  Name
                  Industry
                }
              }
            }
          }
        }
      }
    `,
    variables: '$variables'
  })
  results;

  get variables() {
    return { id: this.recordId };
  }
}
```

### Benefits

- Improved performance
- Better error handling
- Enhanced type safety
- Future-proof API

## Local Development (sf lightning dev component)

Run LWC components locally without deploying:

```bash
# Start local dev server
sf lightning dev component

# Opens browser at http://localhost:3333
# Live reload on file changes
# No deployment needed
# Faster development cycle

# Specify component
sf lightning dev component -n myComponent

# Specify target org
sf lightning dev component -o myOrg@example.com
```

**Benefits:**
- Instant feedback (no deployment wait)
- Debug in real browser DevTools
- Hot module replacement
- Work offline

## Platform Module Access in Component Preview

Access platform modules in single component preview:

```javascript
// Works in local preview now
import { getRecord } from 'lightning/uiRecordApi';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import { NavigationMixin } from 'lightning/navigation';

// Previously required full org deployment
// Now works in sf lightning dev component
```

## Agentforce Targets (Winter '26)

New LWC targets for AI agents:

```xml
<!-- meta.xml -->
<targets>
  <!-- Input component for Agentforce -->
  <target>lightning__AgentforceInput</target>

  <!-- Output component for Agentforce -->
  <target>lightning__AgentforceOutput</target>
</targets>
```

```javascript
// agentInputComponent.js
import { LightningElement, api } from 'lwc';

export default class AgentInputComponent extends LightningElement {
  @api agentContext;  // Provided by Agentforce

  handleSubmit() {
    const userInput = this.template.querySelector('input').value;
    // Send to Agentforce
    this.dispatchEvent(new CustomEvent('agentinput', {
      detail: { input: userInput }
    }));
  }
}
```

## Lightning Out 2.0 (GA Winter '26)

Re-imagined embedding with web components:

### Traditional Lightning Out (Legacy)

```html
<script src="https://MyDomain.lightning.force.com/lightning/lightning.out.js"></script>
<script>
  $Lightning.use("c:myApp", function() {
    $Lightning.createComponent("c:myComponent",
      { recordId: "001..." },
      "lightningContainer",
      function(cmp) { /* callback */ }
    );
  });
</script>
<div id="lightningContainer"></div>
```

### Lightning Out 2.0 (Modern)

```html
<!-- Standards-based web components -->
<script src="https://MyDomain.lightning.force.com/c/myComponent.js" type="module"></script>

<!-- Use as web component -->
<c-my-component record-id="001..." ></c-my-component>

<!-- No Aura dependency -->
<!-- Powered by LWR (Lightning Web Runtime) -->
<!-- Lighter and faster -->
```

**Benefits:**
- 50-70% smaller bundle size
- Faster load times
- Standards-based (no proprietary framework)
- Better browser compatibility
- Simplified integration

## SLDS 2.0 with Dark Mode (GA Winter '26)

Salesforce Lightning Design System 2.0:

```css
/* Dark mode support in custom themes */
:host([data-theme="dark"]) {
  --lwc-colorBackground: #16325c;
  --lwc-colorTextPrimary: #ffffff;
  --lwc-brandPrimary: #1589ee;
}

/* Light mode */
:host([data-theme="light"]) {
  --lwc-colorBackground: #ffffff;
  --lwc-colorTextPrimary: #181818;
  --lwc-brandPrimary: #0176d3;
}
```

```javascript
// Toggle dark mode
export default class ThemeToggle extends LightningElement {
  handleThemeChange(event) {
    const theme = event.target.checked ? 'dark' : 'light';
    this.template.host.setAttribute('data-theme', theme);
  }
}
```

### SLDS Linter with Fix Option

```bash
# Install SLDS linter
npm install -D @salesforce-ux/slds-linter

# Lint with auto-fix
npx slds-linter --fix src/

# CI/CD integration
npx slds-linter src/ --format json > slds-report.json
```

## Unified Testing APIs (Winter '26)

Test Discovery and Test Runner APIs unify Apex and Flow testing:

```apex
// Discover all tests
Test.DiscoveryResult discovery = Test.discoverTests();

// Get Apex tests
List<Test.ApexTestInfo> apexTests = discovery.getApexTests();

// Get Flow tests
List<Test.FlowTestInfo> flowTests = discovery.getFlowTests();

// Run all tests from single location
Test.RunResult result = Test.runTests(discovery);

// Check results
System.debug('Apex passed: ' + result.getApexTestsPassed());
System.debug('Flow passed: ' + result.getFlowTestsPassed());
```

**Benefits:**
- Unified test execution
- Single test report
- Simplified CI/CD
- Better test orchestration

## Lightning Web Security Enhancements

New security protections with API distortions:

```javascript
// Additional secure protections automatically applied
export default class SecureComponent extends LightningElement {
  connectedCallback() {
    // Web APIs now include security distortions
    // ESLint rules validate distortion compliance

    // Example: Secure window access
    const secureWindow = window;  // LWS-secured reference
  }
}
```

### ESLint Rules for Security

```json
// .eslintrc.json
{
  "extends": ["@salesforce/eslint-config-lwc/recommended"],
  "rules": {
    "@lwc/lwc/no-inner-html": "error",
    "@lwc/lwc/no-document-query": "error",
    "@salesforce/lwc-security/no-unsafe-references": "error"
  }
}
```

## Practical Migration Examples

### GraphQL Module Update

```javascript
// Before (Winter '25)
import { gql, graphql } from 'lightning/uiGraphQLApi';

@wire(graphql, { query: gql`...` })
results;

// After (Winter '26)
import { gql, graphql } from 'lightning/graphql';

@wire(graphql, { query: gql`...` })
results;
```

### Local Development Workflow

```bash
# Old workflow (deploy every change)
sf project deploy start
# Wait 30-60 seconds
# Test in org
# Repeat...

# New workflow (instant feedback)
sf lightning dev component
# Changes reflect immediately
# No deployment
# Test in local browser
# Deploy only when ready
```

### Embedding with Lightning Out 2.0

```html
<!-- Old (Lightning Out 1.0) -->
<script src="/lightning/lightning.out.js"></script>
<script>
  $Lightning.use("c:app", function() {
    $Lightning.createComponent("c:comp", {}, "div", callback);
  });
</script>

<!-- New (Lightning Out 2.0) -->
<script src="/c/comp.js" type="module"></script>
<c-comp></c-comp>
```

## Resources

- [Lightning Web Components Dev Guide](https://developer.salesforce.com/docs/platform/lwc/guide)
- [Winter '26 Release Notes](https://help.salesforce.com/s/articleView?id=release-notes.salesforce_release_notes.htm)
- [SLDS 2.0](https://www.lightningdesignsystem.com)
- [Lightning Out 2.0](https://developer.salesforce.com/docs/platform/lwc/guide/use-lightning-out.html)

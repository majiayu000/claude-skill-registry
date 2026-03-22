---
name: sf-lwc
description: |
  Scaffold Lightning Web Components with HTML templates, JS controllers, CSS
  with SLDS compliance, js-meta.xml config, and Jest tests. Use when asked about
  Lightning Web Components, LWC, component scaffolding, or Jest tests for LWC.
  Activate on .js-meta.xml files, mentions of "LWC", "Lightning Web Component",
  "wire adapter", "lightning component", or "@api/@wire/@track decorators".
license: Apache-2.0
compatibility: Requires Salesforce CLI (sf) v2+ and Node.js for Jest tests.
metadata:
  author: clientell
  version: "1.0.0"
  tags: salesforce, lwc, lightning-web-components, jest, frontend
# Claude Code specific
allowed-tools: Read,Write,Edit,Bash(sf *),Bash(npm *),Glob,Grep
context: fork
---

# LWC Scaffolder

You are a Salesforce Lightning Web Component specialist. Generate complete, production-ready LWC bundles.

## LWC Bundle Structure
Every LWC consists of these files in `force-app/main/default/lwc/componentName/`:

```
myComponent/
├── myComponent.html          # Template
├── myComponent.js            # Controller
├── myComponent.css           # Styles (SLDS-compliant)
├── myComponent.js-meta.xml   # Configuration
└── __tests__/
    └── myComponent.test.js   # Jest tests
```

## Naming Conventions
- Bundle folder: `camelCase` (e.g., `accountList`)
- HTML markup: `kebab-case` with `c-` namespace (e.g., `<c-account-list>`)
- JS class: `PascalCase` (e.g., `AccountList`)
- CSS: follows component name

## JavaScript Controller Pattern
```javascript
import { LightningElement, api, wire, track } from 'lwc';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import { NavigationMixin } from 'lightning/navigation';
import getRecords from '@salesforce/apex/MyController.getRecords';
import ACCOUNT_NAME from '@salesforce/schema/Account.Name';

export default class MyComponent extends NavigationMixin(LightningElement) {
    @api recordId;
    @track records = [];
    error;
    isLoading = false;

    @wire(getRecords, { recordId: '$recordId' })
    wiredRecords({ error, data }) {
        if (data) {
            this.records = data;
            this.error = undefined;
        } else if (error) {
            this.error = error;
            this.records = [];
        }
    }

    handleAction() {
        this.isLoading = true;
        imperativeMethod({ param: this.recordId })
            .then(result => {
                this.dispatchEvent(new ShowToastEvent({
                    title: 'Success',
                    message: 'Operation completed',
                    variant: 'success'
                }));
            })
            .catch(error => {
                this.dispatchEvent(new ShowToastEvent({
                    title: 'Error',
                    message: error.body?.message || 'An error occurred',
                    variant: 'error'
                }));
            })
            .finally(() => {
                this.isLoading = false;
            });
    }
}
```

## Meta XML Configuration
```xml
<?xml version="1.0" encoding="UTF-8"?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>62.0</apiVersion>
    <isExposed>true</isExposed>
    <targets>
        <target>lightning__RecordPage</target>
        <target>lightning__AppPage</target>
        <target>lightning__HomePage</target>
    </targets>
    <targetConfigs>
        <targetConfig targets="lightning__RecordPage">
            <objects>
                <object>Account</object>
            </objects>
            <property name="title" type="String" default="My Component"/>
        </targetConfig>
    </targetConfigs>
</LightningComponentBundle>
```

## Jest Test Pattern
```javascript
import { createElement } from 'lwc';
import MyComponent from 'c/myComponent';
import getRecords from '@salesforce/apex/MyController.getRecords';

// Mock Apex method
jest.mock('@salesforce/apex/MyController.getRecords', () => ({
    default: jest.fn()
}), { virtual: true });

const MOCK_DATA = [
    { Id: '001xx000003ABCDEF', Name: 'Test Account' }
];

describe('c-my-component', () => {
    afterEach(() => {
        while (document.body.firstChild) {
            document.body.removeChild(document.body.firstChild);
        }
        jest.clearAllMocks();
    });

    it('renders records when data is returned', async () => {
        getRecords.mockResolvedValue(MOCK_DATA);

        const element = createElement('c-my-component', { is: MyComponent });
        element.recordId = '001xx000003ABCDEF';
        document.body.appendChild(element);

        await Promise.resolve();

        const items = element.shadowRoot.querySelectorAll('.record-item');
        expect(items.length).toBe(1);
    });

    it('shows error when apex call fails', async () => {
        getRecords.mockRejectedValue(new Error('Test error'));

        const element = createElement('c-my-component', { is: MyComponent });
        document.body.appendChild(element);

        await Promise.resolve();

        const errorEl = element.shadowRoot.querySelector('.error-message');
        expect(errorEl).toBeTruthy();
    });
});
```

### Lightning Data Service (LDS)
Use `lightning/uiRecordApi` for CRUD without Apex:
- `getRecord` wire adapter — read records with field-level security
- `createRecord`, `updateRecord`, `deleteRecord` — imperative CRUD
- `getObjectInfo`, `getPicklistValues` — metadata access
- `refreshApex()` — invalidate wire cache after mutations
- **When to use**: Simple CRUD. Use Apex wire for complex queries or business logic.

### Lifecycle Hooks
| Hook | When | Common Use |
|------|------|------------|
| `constructor()` | Component created | Initialize state |
| `connectedCallback()` | Inserted into DOM | Fetch data, add listeners |
| `renderedCallback()` | After each render | DOM manipulation (guard with flag!) |
| `disconnectedCallback()` | Removed from DOM | Cleanup listeners, unsubscribe LMS |
| `errorCallback(error, stack)` | Child error | Error boundary, logging |

### Navigation
Use `NavigationMixin` with page reference types:
- `standard__recordPage` — view/edit/clone records (requires `recordId`, `actionName`)
- `standard__objectPage` — object home/list/new (requires `objectApiName`, `actionName`)
- `standard__namedPage` — standard pages (home, chatter, filePreview)
- `standard__webPage` — external URLs (requires `url`)

### Lightning Message Service (LMS)
Cross-DOM communication between LWC, Aura, and Visualforce:
- Define message channel in `.messageChannel-meta.xml`
- `publish(messageContext, channel, payload)` to send
- `subscribe(messageContext, channel, handler, {scope: APPLICATION_SCOPE})` to receive
- Always `unsubscribe()` in `disconnectedCallback()` to prevent memory leaks

### Shadow DOM vs Light DOM
- **Shadow DOM** (default): CSS isolation, encapsulated DOM — use for most components
- **Light DOM** (`lwc:dom="light"`): No encapsulation — use when you need cross-component ARIA references, global CSS, or third-party library DOM access
- Shadow DOM blocks `document.querySelector()` from outside — use `this.template.querySelector()` inside

## Rules
- Always use SLDS classes for styling — avoid custom CSS when SLDS has a utility
- Use `@api` for public properties, reactive by default
- Use `@wire` for declarative data fetching
- Use imperative Apex calls for user-initiated actions
- Handle loading states and errors in every component
- Use `lightning-record-form` / `lightning-record-edit-form` for simple CRUD
- Dispatch custom events for child-to-parent communication
- Use `MessageChannel` for cross-DOM communication

## Gotchas
- `@track` is deprecated — all properties are reactive by default since API v40+
- `renderedCallback()` fires after EVERY render — always guard with a boolean flag to prevent infinite loops
- LDS cache is NOT automatically refreshed — call `refreshApex(wiredProperty)` after imperative mutations
- LMS subscriptions MUST unsubscribe in `disconnectedCallback()` to prevent memory leaks
- Shadow DOM blocks ID-based ARIA references (`aria-labelledby`) across components — use Light DOM for accessibility
- CSP blocks `eval()`, `new Function()`, and inline `<script>` — load third-party libraries via `loadScript()` from Static Resources
- `@api` properties are read-only in the component — parent sets them, child cannot mutate
- Wire adapters re-fire when reactive parameters change — avoid unnecessary parameter changes

## Workflow
1. Understand the component requirements
2. Check for existing components that can be extended
3. Generate all bundle files (HTML, JS, CSS, meta.xml)
4. Generate Jest test file with mock data
5. Deploy: `sf project deploy start -d force-app/main/default/lwc/componentName/`

## References
- [LWC Patterns](references/lwc-patterns.md) — LDS, navigation, LMS, datatable, custom events, slots, accessibility, SLDS, third-party libs, dynamic components, Experience Cloud

---
name: power-apps
description: Expert guidance for Power Apps development including PCF controls, canvas apps, model-driven apps, Power Fx formulas, and Power Apps Test Engine. Use when building PCF components with React/TypeScript, writing Power Fx expressions, customizing model-driven forms, or testing canvas apps.
---

# Power Apps Development

Expert guidance for PCF controls, canvas apps, model-driven apps, Power Fx formulas, and testing.

## Triggers

Use this skill when you see:
- power apps, canvas app, model-driven app
- pcf control, powerapps component framework
- power fx, delegation, patch, collect
- pcf init, pcf push, test harness
- power apps test engine, testplan

## Instructions

### PCF Control Development

```bash
# Initialize a new PCF field control with React
pac pcf init --namespace Contoso --name MyControl --template field --framework react --run-npm-install

# Initialize a dataset control
pac pcf init --namespace Contoso --name MyGridControl --template dataset --framework react --run-npm-install

# Build the control
npm run build

# Start test harness (local dev server)
npm start watch

# Push to Dataverse environment
pac pcf push --publisher-prefix contoso
```

#### PCF Project Structure

```
MyControl/
├── ControlManifest.Input.xml    # Control metadata, properties, resources
├── index.ts                     # Main control class (IInputs/IOutputs)
├── components/                  # React components
│   └── MyControlApp.tsx
├── css/
│   └── MyControl.css
├── generated/
│   └── ManifestTypes.d.ts       # Auto-generated type definitions
├── package.json
└── tsconfig.json
```

#### ControlManifest.Input.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest>
  <control namespace="Contoso" constructor="MyControl" version="1.0.0"
           display-name-key="MyControl" description-key="MyControl_Desc"
           control-type="standard" api-version="1.3.0">
    <property name="value" display-name-key="Value" of-type="SingleLine.Text"
              usage="bound" required="true" />
    <property name="maxLength" display-name-key="Max Length" of-type="Whole.None"
              usage="input" required="false" default-value="100" />
    <resources>
      <code path="index.ts" order="1" />
      <css path="css/MyControl.css" order="1" />
      <resx path="strings/MyControl.1033.resx" version="1.0.0" />
    </resources>
  </control>
</manifest>
```

#### PCF index.ts Pattern

```typescript
import { IInputs, IOutputs } from "./generated/ManifestTypes";
import * as React from "react";
import * as ReactDOM from "react-dom";
import { MyControlApp } from "./components/MyControlApp";

export class MyControl implements ComponentFramework.StandardControl<IInputs, IOutputs> {
    private container: HTMLDivElement;
    private notifyOutputChanged: () => void;
    private currentValue: string;

    public init(
        context: ComponentFramework.Context<IInputs>,
        notifyOutputChanged: () => void,
        state: ComponentFramework.Dictionary,
        container: HTMLDivElement
    ): void {
        this.container = container;
        this.notifyOutputChanged = notifyOutputChanged;
        this.currentValue = context.parameters.value.raw ?? "";
    }

    public updateView(context: ComponentFramework.Context<IInputs>): void {
        const value = context.parameters.value.raw ?? "";
        ReactDOM.render(
            React.createElement(MyControlApp, {
                value,
                onChange: (newValue: string) => {
                    this.currentValue = newValue;
                    this.notifyOutputChanged();
                },
            }),
            this.container
        );
    }

    public getOutputs(): IOutputs {
        return { value: this.currentValue };
    }

    public destroy(): void {
        ReactDOM.unmountComponentAtNode(this.container);
    }
}
```

### Power Fx Formulas

```
// Navigate with context
Navigate(DetailScreen, ScreenTransition.None, { SelectedItem: ThisItem })

// Patch a record (create)
Patch(Accounts, Defaults(Accounts), {
    Name: txtName.Text,
    Email: txtEmail.Text,
    Status: { Value: "Active" }
})

// Patch a record (update)
Patch(Accounts, LookUp(Accounts, AccountId = varId), {
    Name: txtName.Text
})

// Collect for local table manipulation
ClearCollect(colFilteredItems,
    Filter(Products, Category.Value = "Electronics" && Price > 100)
)

// Delegation-safe filtering
Filter(Accounts,
    StartsWith(Name, txtSearch.Text) &&
    Status.Value = "Active"
)

// User context
User().FullName
User().Email

// Error handling
IfError(
    Patch(Accounts, Defaults(Accounts), { Name: txtName.Text }),
    Notify("Error saving: " & FirstError.Message, NotificationType.Error),
    Notify("Saved successfully", NotificationType.Success)
)

// Concurrent data loading
Concurrent(
    ClearCollect(colAccounts, Accounts),
    ClearCollect(colContacts, Contacts),
    Set(varUserProfile, LookUp(Users, Email = User().Email))
)
```

### Model-Driven App Customization

#### JavaScript Web Resource

```javascript
// formScripts.js - Model-driven form customization
var Contoso = Contoso || {};
Contoso.Account = {
    onLoad: function (executionContext) {
        var formContext = executionContext.getFormContext();
        // Show/hide sections based on form type
        if (formContext.ui.getFormType() === 1) { // Create
            formContext.getControl("revenue").setVisible(false);
        }
    },

    onStatusChange: function (executionContext) {
        var formContext = executionContext.getFormContext();
        var status = formContext.getAttribute("statuscode").getValue();
        // Lock fields when inactive
        if (status === 2) { // Inactive
            formContext.getControl("name").setDisabled(true);
            formContext.getControl("email").setDisabled(true);
        }
    },

    onSave: function (executionContext) {
        var formContext = executionContext.getFormContext();
        // Custom validation
        var email = formContext.getAttribute("emailaddress1").getValue();
        if (email && !email.includes("@")) {
            executionContext.getEventArgs().preventDefault();
            formContext.getControl("emailaddress1").setNotification("Invalid email format", "emailValidation");
        }
    }
};
```

### Power Apps Test Engine

```yaml
# testPlan.fx.yaml
testSuite:
  testSuiteName: Account Form Tests
  testSuiteDescription: Validate account creation flow
  persona: User1
  appLogicalName: contoso_accountapp

  testCases:
    - testCaseName: Create New Account
      testSteps: |
        = Set(testAccountName, "Test Account " & Text(Now(), "yyyymmddhhmmss"));
          Select(btnNewAccount);
          SetProperty(txtName.Text, testAccountName);
          SetProperty(txtEmail.Text, "test@contoso.com");
          Select(btnSave);
          Assert(lblStatus.Text = "Saved", "Record should be saved");

    - testCaseName: Validate Required Fields
      testSteps: |
        = Select(btnNewAccount);
          SetProperty(txtName.Text, "");
          Select(btnSave);
          Assert(lblError.Visible = true, "Error should show for empty name");

testSettings:
  headless: true
  locale: "en-US"
  browserType: "Chromium"
```

## Best Practices

| Practice | Description |
|----------|-------------|
| **Delegation** | Always check delegation warnings; use `StartsWith` over `in` for large datasets |
| **Collections** | Use `ClearCollect` for cached data, `Collect` for appending |
| **Variables** | Use `Set` for global, `UpdateContext` for screen-scoped variables |
| **Concurrent** | Load independent data sources with `Concurrent()` for performance |
| **PCF testing** | Always test in the local harness before pushing to Dataverse |
| **Error handling** | Wrap `Patch` calls with `IfError` for user-friendly messages |
| **Component reuse** | Build canvas components or PCF controls for reusable UI |
| **Naming** | Use prefixes: `scr` (screens), `btn` (buttons), `txt` (text inputs), `lbl` (labels) |

## Common Workflows

### PCF Development Lifecycle
1. `pac pcf init` with React template
2. Implement control logic in `index.ts` and React components
3. Test locally with `npm start watch`
4. `pac pcf push` to dev environment
5. Add to solution and deploy via ALM pipeline

### Canvas App Best Practices
1. Use `App.OnStart` sparingly; prefer `App.Formulas` for static values
2. Cache data in collections on screen `OnVisible`
3. Use named formulas for computed values
4. Implement proper loading states with variables
5. Test with Power Apps Test Engine YAML plans

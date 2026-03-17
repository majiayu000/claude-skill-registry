---
name: create-lwc-tab
description: Creates a new Lightning Web Component with a tab and flexipage for display. Use when you need to create a new standalone page/tab with an LWC component.
allowed-tools: Write, Bash, Read, Glob
---

# Create LWC with Tab

Creates a new Lightning Web Component along with the necessary tab and flexipage metadata to make it accessible as a standalone page.

## Arguments

`$ARGUMENTS` should be the component name in camelCase (e.g., `pledgeList`)

## Files to Create

### 1. LWC Component

Create directory: `force-app/main/default/lwc/{componentName}/`

**{componentName}.js**:
```javascript
import { LightningElement } from 'lwc';

export default class ComponentName extends LightningElement {
    // Component logic
}
```

**{componentName}.html**:
```html
<template>
    <!-- Component template -->
</template>
```

**{componentName}.js-meta.xml**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>62.0</apiVersion>
    <isExposed>true</isExposed>
    <targets>
        <target>lightning__Tab</target>
        <target>lightning__AppPage</target>
        <target>lightning__HomePage</target>
    </targets>
</LightningComponentBundle>
```

### 2. Custom Tab (Optional)

Create: `force-app/main/default/tabs/{TabName}.tab-meta.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CustomTab xmlns="http://soap.sforce.com/2006/04/metadata">
    <label>Tab Label</label>
    <lwcComponent>{componentName}</lwcComponent>
    <motif>Custom70: Handsaw</motif>
</CustomTab>
```

### 3. Lightning App Page (Recommended)

Create: `force-app/main/default/flexipages/{Page_Name}.flexipage-meta.xml`

**Important**: Component instances MUST have an `<identifier>` element or deployment fails.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<FlexiPage xmlns="http://soap.sforce.com/2006/04/metadata">
    <flexiPageRegions>
        <itemInstances>
            <componentInstance>
                <componentName>c:{componentName}</componentName>
                <identifier>{componentName}1</identifier>
            </componentInstance>
        </itemInstances>
        <name>main</name>
        <type>Region</type>
    </flexiPageRegions>
    <masterLabel>Page Label</masterLabel>
    <template>
        <name>flexipage:defaultAppHomeTemplate</name>
    </template>
    <type>AppPage</type>
</FlexiPage>
```

## Deploy

```bash
sf project deploy start \
  --source-dir force-app/main/default/lwc/{componentName} \
  --source-dir force-app/main/default/flexipages/{Page_Name}.flexipage-meta.xml \
  --target-org lubavitchrv_partial \
  --wait 10
```

## After Deployment

New flexipages require activation before appearing in App Launcher. Use the `activate-lightning-page` skill if needed.

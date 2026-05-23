---
name: Wheels Plugin Generator
description: Generate Wheels plugins with proper structure, configuration, and ForgeBox packaging. Use when creating plugins, extending Wheels functionality, or packaging reusable components. Ensures plugins follow Wheels conventions and can be easily shared via ForgeBox.
---

# Wheels Plugin Generator

## When to Use This Skill

Activate automatically when:
- User wants to create a plugin
- User mentions: plugin, extend wheels, reusable component
- User wants to package functionality for ForgeBox
- User needs to add plugin configuration
- User asks about plugin structure

## Plugin Directory Structure

```
/plugins/YourPlugin/
├── index.cfm                 # Plugin entry point
├── box.json                  # ForgeBox package metadata
├── README.md                 # Plugin documentation
├── config/
│   └── settings.cfm         # Plugin configuration
├── controllers/             # Plugin controllers (optional)
├── models/                  # Plugin models (optional)
├── views/                   # Plugin views (optional)
│   └── helpers/            # View helpers
├── events/                  # Event handlers (optional)
├── db/                     # Database migrations (optional)
│   └── migrate/
└── tests/                   # Plugin tests
    └── PluginTest.cfc
```

## Plugin Entry Point (index.cfm)

```cfm
<cfcomponent output="false" mixin="global">

    <!--- Initialize plugin --->
    <cffunction name="init">
        <cfset this.version = "1,0,0,0">
        <cfreturn this>
    </cffunction>

    <!--- Add global methods --->
    <cffunction name="myPluginMethod" returntype="string" access="public" output="false">
        <cfargument name="text" type="string" required="true">
        <cfreturn "Plugin: " & arguments.text>
    </cffunction>

    <!--- Add model methods --->
    <cffunction name="modelMethod" returntype="void" access="public" output="false" mixin="model">
        <!--- Available in all models --->
    </cffunction>

    <!--- Add controller methods --->
    <cffunction name="controllerMethod" returntype="void" access="public" output="false" mixin="controller">
        <!--- Available in all controllers --->
    </cffunction>

    <!--- Add view helper methods --->
    <cffunction name="helperMethod" returntype="string" access="public" output="false" mixin="controller">
        <!--- Available in views (via controller) --->
    </cffunction>

</cfcomponent>
```

## Plugin Configuration (config/settings.cfm)

```cfm
<cfscript>
// Plugin-specific settings
set(functionName="pluginSetting", value="default");
set(functionName="anotherSetting", per="environment", dev=true, prod=false);

// Environment-specific configuration
if (application.wheels.environment == "production") {
    set(functionName="productionSetting", value="prod-value");
}
</cfscript>
```

## Plugin box.json Template

```json
{
    "name": "YourPlugin",
    "slug": "your-plugin",
    "version": "1.0.0",
    "author": "Your Name <email@example.com>",
    "location": "forgeboxStorage",
    "type": "cfwheels-plugins",
    "homepage": "https://github.com/yourusername/your-plugin",
    "documentation": "https://github.com/yourusername/your-plugin/wiki",
    "repository": {
        "type": "git",
        "URL": "https://github.com/yourusername/your-plugin"
    },
    "bugs": "https://github.com/yourusername/your-plugin/issues",
    "shortDescription": "Brief description of your plugin",
    "description": "Detailed description of what your plugin does",
    "keywords": [
        "cfwheels",
        "plugin",
        "feature"
    ],
    "private": false,
    "engines": [
        {
            "type": "lucee",
            "version": ">=5.0.0"
        },
        {
            "type": "adobe",
            "version": ">=2018.0.0"
        }
    ],
    "defaultPort": 0,
    "projectURL": "",
    "license": [
        {
            "type": "Apache-2.0",
            "URL": "https://www.apache.org/licenses/LICENSE-2.0"
        }
    ],
    "contributors": [],
    "dependencies": {},
    "devDependencies": {},
    "installPaths": {},
    "ignore": [
        "**/.*",
        "test",
        "tests"
    ]
}
```

## Plugin README.md Template

```markdown
# Your Plugin Name

Brief description of what your plugin does.

## Requirements

- CFWheels 2.x or higher
- Lucee 5+ or Adobe ColdFusion 2018+

## Installation

### Option 1: CommandBox (Recommended)
```bash
box install your-plugin
```

### Option 2: Manual Installation
1. Download the plugin
2. Extract to `/plugins/YourPlugin/`
3. Reload your Wheels application

## Configuration

Add to `config/settings.cfm`:

```cfm
<cfscript>
set(functionName="pluginSetting", value="yourValue");
</cfscript>
```

## Usage

### Basic Example
```cfm
// In controller
result = myPluginMethod("Hello World");

// In view
#myPluginHelper()#
```

### Advanced Example
```cfm
// Your advanced usage examples here
```

## API Reference

### Global Methods

#### myPluginMethod(text)
Description of what this method does.

**Parameters:**
- `text` (string, required) - Description

**Returns:** string

**Example:**
```cfm
result = myPluginMethod("test");
```

## Testing

Run plugin tests:
```bash
box testbox run
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

Apache License 2.0

## Credits

Created by [Your Name](https://yourwebsite.com)
```

## Plugin Event Handlers

```cfm
<cfcomponent output="false" mixin="global">

    <cffunction name="init">
        <cfset this.version = "1,0,0,0">

        <!--- Register event handlers --->
        <cfset variables.wheels.events.register(
            eventName = "onApplicationStart",
            object = this,
            method = "onAppStart"
        )>

        <cfset variables.wheels.events.register(
            eventName = "onRequestStart",
            object = this,
            method = "onReqStart"
        )>

        <cfreturn this>
    </cffunction>

    <!--- Event handler methods --->
    <cffunction name="onAppStart" returntype="void" access="public" output="false">
        <!--- Runs when application starts --->
    </cffunction>

    <cffunction name="onReqStart" returntype="void" access="public" output="false">
        <!--- Runs on each request --->
    </cffunction>

</cfcomponent>
```

## Available Events

Wheels plugins can hook into these events:

- `onApplicationStart` - Application initialization
- `onRequestStart` - Beginning of each request
- `onRequestEnd` - End of each request
- `onSessionStart` - New session created
- `onSessionEnd` - Session expires
- `onError` - Error occurs
- `onMissingMethod` - Method not found
- `onMissingTemplate` - Template not found

## Plugin with Database Migrations

```
/plugins/YourPlugin/
└── db/
    └── migrate/
        ├── 001_CreatePluginTable.cfc
        └── 002_AddPluginColumn.cfc
```

**Migration Example:**
```cfm
component extends="wheels.migrator.Migration" {

    function up() {
        transaction {
            t = createTable(name="plugin_data");
            t.string(columnNames="name");
            t.text(columnNames="data");
            t.timestamps();
            t.create();
        }
    }

    function down() {
        dropTable("plugin_data");
    }
}
```

## Plugin Testing

```cfm
component extends="wheels.Test" {

    function setup() {
        super.setup();
        // Setup test fixtures
    }

    function teardown() {
        // Cleanup
        super.teardown();
    }

    function testPluginMethodExists() {
        assert("structKeyExists(variables.wheels, 'myPluginMethod')");
    }

    function testPluginMethodReturnsCorrectly() {
        result = myPluginMethod("test");
        assert("result == 'Plugin: test'");
    }

    function testPluginConfiguration() {
        setting = get("pluginSetting");
        assert("setting == 'expectedValue'");
    }
}
```

## Publishing to ForgeBox

### 1. Prepare Plugin
```bash
# Ensure box.json is configured
box show

# Test locally
box install
```

### 2. Publish
```bash
# Login to ForgeBox
box forgebox login

# Publish plugin
box forgebox publish
```

### 3. Version Management
```bash
# Update version
box bump --major    # 1.0.0 -> 2.0.0
box bump --minor    # 1.0.0 -> 1.1.0
box bump --patch    # 1.0.0 -> 1.0.1

# Republish
box forgebox publish
```

## Common Plugin Patterns

### 1. Validation Plugin
```cfm
<cffunction name="customValidation" mixin="model">
    <cfargument name="property" type="string" required="true">
    <cfargument name="message" type="string" default="Invalid">

    <cfset validatesFormatOf(
        properties = arguments.property,
        regEx = "your-regex",
        message = arguments.message
    )>
</cffunction>
```

### 2. Helper Plugin
```cfm
<cffunction name="formatCurrency" mixin="controller">
    <cfargument name="amount" type="numeric" required="true">
    <cfreturn dollarFormat(arguments.amount)>
</cffunction>
```

### 3. Model Extension Plugin
```cfm
<cffunction name="softDelete" mixin="model">
    <cfset this.deletedAt = now()>
    <cfset this.save()>
</cffunction>

<cffunction name="restore" mixin="model">
    <cfset this.deletedAt = "">
    <cfset this.save()>
</cffunction>
```

## Plugin Best Practices

### ✅ DO:
- Use unique function names (prefix with plugin name)
- Provide configuration options via settings
- Include comprehensive documentation
- Add tests for all functionality
- Follow Wheels naming conventions
- Version using semantic versioning
- Include LICENSE file

### ❌ DON'T:
- Overwrite core Wheels methods
- Use generic function names (risk conflicts)
- Hardcode configuration values
- Skip error handling
- Forget to document configuration options

## Debugging Plugins

### Enable Plugin Debug
```cfm
// In config/settings.cfm
set(showDebugInformation=true);

// Check plugin loaded
<cfdump var="#application.wheels.plugins#">
```

### Check Plugin Methods
```cfm
// List available methods
<cfdump var="#structKeyList(variables.wheels)#">

// Test plugin method exists
<cfif structKeyExists(variables.wheels, "myPluginMethod")>
    Works!
</cfif>
```

## Related Skills

- **wheels-model-generator**: Create models that plugins extend
- **wheels-controller-generator**: Create controllers that use plugins
- **wheels-migration-generator**: Create plugin migrations
- **wheels-test-generator**: Test plugin functionality

---

**Generated by:** Wheels Plugin Generator Skill v1.0

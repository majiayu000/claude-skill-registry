---
name: configuration
description: Reads config.json and prompts user for application parameters. Merges configuration with defaults for project generation.
---

# Configuration Management Skill

## Purpose
Read and merge application configuration from `config.json` file with interactive prompts and default values.

**IMPORTANT**: When prompting users interactively, ask questions **ONE AT A TIME** in a conversational manner. Wait for each answer before asking the next question.

## When to Use
Execute this skill at the beginning of the application generation process (Step 2 in AGENT_INSTRUCTIONS.md).

## Input Parameters
None - reads from project root

## Configuration Sources Priority
1. **config.json** (if exists in project root) - Highest priority
2. **Interactive prompts** - For missing required fields
3. **Default values** - For optional fields not provided

## Instructions

### Step 1: Check for config.json
```javascript
const configPath = path.join(process.cwd(), 'config.json');
const configExists = fs.existsSync(configPath);

if (configExists) {
  console.log('✓ Found config.json - loading configuration...\n');
} else {
  console.log('ℹ  No config.json found - will use interactive prompts\n');
}
```

### Step 2: Load and Validate Configuration
```javascript
let userConfig = {};

if (configExists) {
  const configContent = fs.readFileSync(configPath, 'utf-8');
  userConfig = JSON.parse(configContent);
  
  // Validate against schema
  const schemaPath = '.github/agents/agents-context/app-starter/config.schema.json';
  const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf-8'));
  
  // Use a JSON schema validator (e.g., ajv)
  const valid = validateSchema(userConfig, schema);
  
  if (!valid) {
    console.error('❌ config.json validation failed');
    console.error('   Please check your configuration against config.schema.json');
    process.exit(1);
  }
  
  console.log('✓ Configuration validated successfully\n');
}
```

### Step 3: Apply Default Values
```javascript
// Static defaults
const defaults = {
  node_version: "v22.16.0",
  vue_version: "^3.5.13",
  vite_version: "^6.3.5",
  typescript_version: "^5.7.3",
  test_framework: "jest",
  state_management: "vuex",
  enable_single_spa: true,
  enable_datadog: true,
  include_component_library: false,  // Default to no component library
  component_library: "@royalaholddelhaize/pdl-spectrum-component-library-web",
  component_library_version: "^1.0.3"
};

// Merge with defaults (config.json values take priority)
userConfig = { ...defaults, ...userConfig };
```

### Step 4: Prompt for Missing Required Fields

**Ask questions ONE AT A TIME in order. Wait for user response before asking next question.**

```javascript
const requiredFields = [
  'application_name',
  'project_scope',
  'router_base_path',
  'api_base_path',
  'default_port',
  'application_type',
  'use_latest_versions'  // Added as required field
];

// Ask ONE question at a time
for (const field of requiredFields) {
  if (!userConfig[field]) {
    // Show context and ask single question
    console.log(`\n📝 Question ${requiredFields.indexOf(field) + 1}/${requiredFields.length}`);
    userConfig[field] = await promptUser(field);
    
    // Confirm response before moving to next question
    console.log(`✓ Got it: ${userConfig[field]}\n`);
  } else {
    console.log(`✓ Using ${field} from config: ${userConfig[field]}`);
  }
}
```

### Step 5: Conditional Prompts Based on Version Choice

**If user chose NOT to use latest versions, ask about test framework and state management.**

```javascript
// Only ask these if user chose stable versions (not latest)
if (userConfig.use_latest_versions === false || userConfig.use_latest_versions === 'no') {
  
  // Prompt for test framework if not set
  if (!userConfig.test_framework) {
    console.log('\n🧪 Testing framework:');
    userConfig.test_framework = await promptUser('test_framework', {
      choices: ['jest', 'vitest'],
      default: 'jest',
      message: 'Which testing framework do you want to use?'
    });
    console.log(`✓ Will use ${userConfig.test_framework}\n`);
  }

  // Prompt for state management if not set
  if (!userConfig.state_management) {
    console.log('\n📊 State management:');
    userConfig.state_management = await promptUser('state_management', {
      choices: ['vuex', 'pinia'],
      default: 'vuex',
      message: 'Which state management library do you want to use?'
    });
    console.log(`✓ Will use ${userConfig.state_management}\n`);
  }
  
} else {
  // User chose latest versions - use recommended defaults
  console.log('\n✓ Using latest versions with recommended tools:');
  userConfig.test_framework = 'vitest';  // Latest recommendation
  userConfig.state_management = 'pinia';  // Latest recommendation
  console.log('  • Testing: Vitest (latest)');
  console.log('  • State Management: Pinia (latest)\n');
}
```

### Step 6: Prompt for Optional GitHub Token

**Only ask for GitHub token if user wants component library.**

```javascript
// First, ask if they want a component library
let needsComponentLibrary = false;

if (userConfig.include_component_library === undefined) {
  console.log('\n📦 Component library:');
  needsComponentLibrary = await promptUser('include_component_library', {
    type: 'confirm',
    message: 'Do you want to include a component library?',
    default: false,
    hint: '(@RoyalAholdDelhaize/pdl-spectrum-component-library-web)'
  });
  userConfig.include_component_library = needsComponentLibrary;
  console.log(`✓ ${needsComponentLibrary ? 'Will include component library' : 'No component library'}\n`);
}
```

### Step 7: Derive Auto-Calculated Values
```javascript
// Derive main_component_name from application_name
// Example: "omni-inventory-manager-web" → "OmniInventoryManagerWeb"
userConfig.main_component_name = userConfig.application_name
  .split('-')
  .map(word => word.charAt(0).toUpperCase() + word.slice(1))
  .join('');

// application_id and service_name same as application_name
userConfig.application_id = userConfig.application_name;
userConfig.service_name = userConfig.application_name;

// Determine if standalone or micro-frontend
userConfig.is_standalone = userConfig.application_type === 'standalone';
userConfig.is_microfrontend = userConfig.application_type === 'micro-frontend';

// Map application_type to vite_build_format
userConfig.vite_build_format = userConfig.is_microfrontend ? 'system' : 'es';
```

### Step 7: Display Configuration Summary
```javascript
console.log('\n' + '═'.repeat(60));
console.log('  CONFIGURATION SUMMARY');
console.log('═'.repeat(60));
console.log(`Application:       ${userConfig.application_name}`);
console.log(`Scope:             ${userConfig.project_scope}`);
console.log(`Type:              ${userConfig.application_type}`);
console.log(`Router Base:       ${userConfig.router_base_path}`);
console.log(`API Base:          ${userConfig.api_base_path}`);
console.log(`Port:              ${userConfig.default_port}`);
console.log(`Test Framework:    ${userConfig.test_framework}`);
console.log(`State Management:  ${userConfig.state_management}`);
console.log(`Component Library: ${userConfig.component_library || 'None'}`);
console.log('═'.repeat(60) + '\n');
```

### Step 8: Offer to Save Configuration (Optional)

```javascript
// Only offer to save if user provided parameters via prompts
if (!configExists || missingFields.length > 0) {
  const shouldSave = await promptUser('saveConfig', {
    message: 'Save this configuration to config.json for future use?',
    type: 'confirm',
    default: true
  });
  
  if (shouldSave) {
    // Prepare config object (exclude sensitive data)
    const configToSave = {
      application_name: userConfig.application_name,
      project_scope: userConfig.project_scope,
      router_base_path: userConfig.router_base_path,
      api_base_path: userConfig.api_base_path,
      default_port: userConfig.default_port,
      application_type: userConfig.application_type,
      test_framework: userConfig.test_framework,
      state_management: userConfig.state_management,
      node_version: userConfig.node_version,
      vue_version: userConfig.vue_version,
      vite_version: userConfig.vite_version,
      typescript_version: userConfig.typescript_version,
      enable_single_spa: userConfig.enable_single_spa,
      enable_datadog: userConfig.enable_datadog,
      component_library: userConfig.component_library,
      component_library_version: userConfig.component_library_version
    };
    
    // Write to config.json
    fs.writeFileSync(
      path.join(process.cwd(), 'config.json'),
      JSON.stringify(configToSave, null, 2) + '\n'
    );
    
    console.log('✓ Configuration saved to config.json');
    console.log('⚠️  Note: GitHub token (if provided) was NOT saved for security');
    console.log('   You can manually add it to config.json if needed (it will be gitignored)\n');
    
    // Add config.json to .gitignore if not already there
    const gitignorePath = path.join(process.cwd(), '.gitignore');
    if (fs.existsSync(gitignorePath)) {
      const gitignoreContent = fs.readFileSync(gitignorePath, 'utf-8');
      if (!gitignoreContent.includes('config.json')) {
        fs.appendFileSync(gitignorePath, '\nconfig.json\n');
        console.log('✓ Added config.json to .gitignore\n');
      }
    }
  }
}
```

## Output
- `userConfig` object with all configuration values
- Validation results
- Summary display to user
- Optional: `config.json` file saved in project root (if user confirms)

## Validation Rules

### Format Validation
- **application_name**: Must be kebab-case (e.g., `my-app-web`)
- **project_scope**: Must start with `@` (e.g., `@myorg`)
- **router_base_path**: Must start with `/` (e.g., `/my-app`)
- **api_base_path**: Must start with `/` (e.g., `/api`)
- **default_port**: Must be integer 1024-65535
- **application_type**: Must be `"standalone"` or `"micro-frontend"`
- **test_framework**: Must be `"jest"` or `"vitest"`
- **state_management**: Must be `"vuex"` or `"pinia"`

### Business Logic Validation
See `conditional-generation` skill for application type specific validations.

## Configuration Methods

### Method 1: Interactive Terminal Prompts (Default)
Run the agent and answer the prompts interactively.

**IMPORTANT**: Questions are asked **ONE AT A TIME** in a conversational flow:
- Agent asks question 1, waits for answer
- Agent confirms answer, asks question 2, waits for answer
- Agent confirms answer, asks question 3, and so on...
- Progress indicator shown (e.g., "Question 3/6")

**Example Interactive Flow**:
```
Agent: 📝 Question 1/7
       What is the name of your application? (in kebab-case)
User:  my-inventory-app-web
Agent: ✓ Got it: my-inventory-app-web

Agent: 📝 Question 2/7
       What is your NPM scope/organization? (e.g., @my-org)
User:  @my-company
Agent: ✓ Got it: @my-company

Agent: 📝 Question 3/7
       What base path should the router use?
User:  /my-inventory-app
Agent: ✓ Got it: /my-inventory-app

... continues through question 7 ...

Agent: 📝 Question 7/7
       Do you want to use the latest package versions from npm?
User:  yes
Agent: ✓ Got it: yes

       ✓ Using latest versions with recommended tools:
         • Testing: Vitest (latest)
         • State Management: Pinia (latest)

Agent: 📦 Component library:
       Do you want to include a component library?
User:  no
Agent: ✓ No component library
       ℹ  Skipping GitHub token (no component library needed)

... and so on
```

### Method 2: Configuration File (config.json)
Create a `config.json` file in the project root. The agent will read values and skip prompting.

### Method 3: Hybrid Approach
Provide some values in `config.json` and the agent will only prompt for missing required values (ONE AT A TIME).

## Related Skills
- **conditional-generation**: Determines which files to generate based on config
- **component-library**: Handles component library installation based on config
- **package-json**: Uses config to generate package.json

## Files Referenced

### config.json (project root)
User's configuration file (optional). If exists, values are loaded from here.

All configuration fields, validation rules, and defaults are documented in `examples.md`.

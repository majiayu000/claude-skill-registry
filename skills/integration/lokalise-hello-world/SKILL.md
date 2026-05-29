---
name: lokalise-hello-world
description: |
  Create a minimal working Lokalise example.
  Use when starting a new Lokalise integration, testing your setup,
  or learning basic Lokalise API patterns.
  Trigger with phrases like "lokalise hello world", "lokalise example",
  "lokalise quick start", "simple lokalise code".
allowed-tools: Read, Write, Edit
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Lokalise Hello World

## Overview
Minimal working example demonstrating core Lokalise functionality: projects, keys, and translations.

## Prerequisites
- Completed `lokalise-install-auth` setup
- Valid API token configured
- At least one Lokalise project (or we'll create one)

## Instructions

### Step 1: Create Entry File
```bash
# Create project directory
mkdir lokalise-demo && cd lokalise-demo
npm init -y
npm install @lokalise/node-api dotenv

# Create main file
touch index.mjs
```

### Step 2: Initialize Client and List Projects
```typescript
// index.mjs
import "dotenv/config";
import { LokaliseApi } from "@lokalise/node-api";

const lokaliseApi = new LokaliseApi({
  apiKey: process.env.LOKALISE_API_TOKEN,
});

async function main() {
  // List all projects
  const projects = await lokaliseApi.projects().list();
  console.log("Your Lokalise Projects:");
  projects.items.forEach(p => {
    console.log(`  - ${p.name} (${p.project_id})`);
  });
}

main().catch(console.error);
```

### Step 3: Create a Project
```typescript
async function createProject() {
  const project = await lokaliseApi.projects().create({
    name: "My Demo Project",
    description: "Created via API",
    languages: [
      { lang_iso: "en", custom_iso: "" },  // English (base)
      { lang_iso: "es", custom_iso: "" },  // Spanish
      { lang_iso: "fr", custom_iso: "" },  // French
    ],
    base_lang_iso: "en",
  });

  console.log(`Created project: ${project.name}`);
  console.log(`Project ID: ${project.project_id}`);
  return project;
}
```

### Step 4: Add Translation Keys
```typescript
async function addKeys(projectId: string) {
  const keys = await lokaliseApi.keys().create({
    project_id: projectId,
    keys: [
      {
        key_name: "welcome.title",
        platforms: ["web"],
        translations: [
          { language_iso: "en", translation: "Welcome to our app!" },
          { language_iso: "es", translation: "Bienvenido a nuestra app!" },
          { language_iso: "fr", translation: "Bienvenue dans notre app!" },
        ],
      },
      {
        key_name: "welcome.subtitle",
        platforms: ["web"],
        translations: [
          { language_iso: "en", translation: "Get started today" },
        ],
      },
    ],
  });

  console.log(`Created ${keys.items.length} keys`);
  return keys;
}
```

### Step 5: Retrieve Translations
```typescript
async function getTranslations(projectId: string) {
  const translations = await lokaliseApi.translations().list({
    project_id: projectId,
    filter_lang_id: 640,  // English language ID
  });

  console.log("English translations:");
  translations.items.forEach(t => {
    console.log(`  ${t.key_id}: ${t.translation}`);
  });
}
```

## Output
- Working TypeScript/JavaScript file with Lokalise client
- Successfully listed, created projects
- Added translation keys with multiple languages
- Retrieved translations

## Error Handling
| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid token | Check LOKALISE_API_TOKEN |
| `400 Bad Request` | Invalid project/key params | Verify required fields |
| `404 Not Found` | Project doesn't exist | Check project_id |
| `429 Too Many Requests` | Rate limit hit | Wait 1 second, retry |

## Examples

### Complete Hello World Script
```typescript
import "dotenv/config";
import { LokaliseApi } from "@lokalise/node-api";

const lokaliseApi = new LokaliseApi({
  apiKey: process.env.LOKALISE_API_TOKEN,
});

async function helloLokalise() {
  // 1. List existing projects
  const projects = await lokaliseApi.projects().list();
  console.log(`Found ${projects.items.length} existing projects\n`);

  // 2. Create a demo project
  const project = await lokaliseApi.projects().create({
    name: `Demo ${Date.now()}`,
    languages: [
      { lang_iso: "en" },
      { lang_iso: "es" },
    ],
    base_lang_iso: "en",
  });
  console.log(`Created: ${project.name} (${project.project_id})\n`);

  // 3. Add a key with translations
  const keys = await lokaliseApi.keys().create({
    project_id: project.project_id,
    keys: [{
      key_name: "greeting",
      platforms: ["web"],
      translations: [
        { language_iso: "en", translation: "Hello, World!" },
        { language_iso: "es", translation: "Hola, Mundo!" },
      ],
    }],
  });
  console.log(`Added ${keys.items.length} key(s)\n`);

  // 4. Fetch the key back
  const fetchedKey = await lokaliseApi.keys().get(keys.items[0].key_id, {
    project_id: project.project_id,
  });
  console.log(`Key: ${fetchedKey.key_name.web}`);

  // 5. Clean up (optional)
  // await lokaliseApi.projects().delete(project.project_id);

  console.log("\nSuccess! Your Lokalise integration is working.");
}

helloLokalise().catch(console.error);
```

### Using CLI for Quick Test
```bash
# List projects
lokalise2 --token $LOKALISE_API_TOKEN project list

# Get project details
lokalise2 --token $LOKALISE_API_TOKEN project --project-id YOUR_PROJECT_ID

# List keys in a project
lokalise2 --token $LOKALISE_API_TOKEN key list --project-id YOUR_PROJECT_ID
```

## Resources
- [Lokalise API Reference](https://developers.lokalise.com/reference/lokalise-rest-api)
- [Projects API](https://developers.lokalise.com/reference/list-all-projects)
- [Keys API](https://developers.lokalise.com/reference/list-all-keys)
- [Translations API](https://developers.lokalise.com/reference/list-all-translations)

## Next Steps
Proceed to `lokalise-local-dev-loop` for development workflow setup.

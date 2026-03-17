---
name: model-provider-setup
description: Configure Claude Code to use alternative AI model providers by setting up custom API endpoints and authentication. Use this skill when users want to switch from default Anthropic models to providers like Z.AI, OpenRouter, or other custom endpoints with compatible APIs.
---

# Model Provider Setup

## Overview

This skill configures `.claude/settings.local.json` to use alternative AI model providers that offer Anthropic-compatible APIs. It guides the setup of custom base URLs, model selections, and API authentication for providers beyond the default Anthropic service.

## When to Use This Skill

Use this skill when users:
- Want to switch to alternative model providers (Z.AI, OpenRouter, etc.)
- Need to configure custom API endpoints for Claude Code
- Ask about setting up API keys for different providers
- Request help configuring model provider settings

## Setup Workflow

### Step 1: Read Provider Configurations

Read the provider configurations from `references/providers.json` to understand available providers, their base URLs, and supported models.

The JSON structure contains:
- Provider ID and display name
- Description of the provider
- Base URL for API requests
- List of available models with IDs and descriptions

### Step 2: Present Provider Options to User

Use the `AskUserQuestion` tool to present available providers to the user. Structure the question as follows:

**Question format:**
- Header: "Provider"
- Question: "Which model provider would you like to configure?"
- Options: Build from providers.json, using provider name as label and description as the option description
- multiSelect: false (single provider selection)

### Step 3: Present Model Options for Selected Provider

After the user selects a provider, use `AskUserQuestion` again to let them choose a model from that provider's available models.

**Question format:**
- Header: "Model"
- Question: "Which model would you like to use?"
- Options: Build from the selected provider's models array, using model name as label and description as the option description
- multiSelect: false (single model selection)

### Step 4: Collect API Key

Use `AskUserQuestion` to collect the API key for the selected provider.

**Question format:**
- Header: "API Key"
- Question: "Please enter your API key for [provider name]:"
- Options: Provide 2 options:
  - Label: "I'll enter my API key", Description: "Type or paste your API key in the 'Other' field below"
  - Label: "I'll add it manually later", Description: "Set up the configuration with a placeholder that you'll replace later"
- multiSelect: false

**Important:** If the user selects "Other" and provides a custom text input, that is their API key. If they choose "I'll add it manually later", use the placeholder `"<YOUR_API_KEY_HERE>"`.

### Step 5: Update .claude/settings.local.json

Read the existing `.claude/settings.local.json` file if it exists. If it doesn't exist, create a new one.

Update or create the configuration with the following structure:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "<selected provider's baseUrl>",
    "ANTHROPIC_MODEL": "<selected model's id>",
    "ANTHROPIC_AUTH_TOKEN": "<user's API key or placeholder>"
  }
}
```

**Important considerations:**
- Preserve any existing configuration in settings.local.json that is not related to these three env variables
- Merge the new env variables with existing ones
- Use proper JSON formatting with 2-space indentation

### Step 6: Confirm Setup

After updating the configuration file, inform the user:
1. Which provider and model were configured
2. The location of the settings file: `.claude/settings.local.json`
3. If a placeholder was used, remind them to replace `<YOUR_API_KEY_HERE>` with their actual API key
4. Note that they need to restart Claude Code for the changes to take effect

## Adding New Providers

To add new model providers to this skill, edit `references/providers.json` and add a new provider object with the following structure:

```json
{
  "id": "unique-provider-id",
  "name": "Display Name",
  "description": "Brief description of the provider",
  "baseUrl": "https://api.example.com/v1",
  "models": [
    {
      "id": "model-identifier",
      "name": "Model Display Name",
      "description": "Brief description of the model"
    }
  ]
}
```

## Resources

### references/providers.json

Contains the configuration database for all supported model providers. This file includes:
- Provider metadata (ID, name, description)
- API base URLs
- Available models for each provider

This file should be read at the start of the workflow to populate the provider and model selection options.

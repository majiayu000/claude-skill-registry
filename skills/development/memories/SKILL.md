---
name: memories
description: Created a new skill called "create JSON file" for generating JSON files
  from JavaScript/TypeScript objects with proper error handling.
---

# JSON File Creation Skill

## Overview
Created a new skill called "create JSON file" for generating JSON files from JavaScript/TypeScript objects with proper error handling.

## Skill Details
- **Name**: "create JSON file"
- **Purpose**: Create JSON files from object data with proper formatting and error reporting
- **File patterns**: `**/*.{js,ts,json}`

## Implementation Steps
1. Create an empty file at the specified path
2. Stringify the object into the new file using JSON.stringify with proper formatting
3. Report success or failure, and print any error messages encountered

## Usage Context
This skill is designed to be automatically applied when working with JavaScript, TypeScript, or JSON files that require JSON file creation functionality. The rule follows agent-requested pattern where the AI decides when to apply it based on the description and file patterns.

## Related Files
- Rule created for automatic application when appropriate
- Can be used across JavaScript/TypeScript projects for JSON file generation tasks
---
name: principle
description: Create advanced animations with Principle - design interactive prototypes with complex motion and transitions
category: design
---

# Principle Skill

## Overview
Enables Claude to manage Principle animation projects through file organization and documentation, as Principle is a macOS desktop application. Claude can help organize project files and document animation specifications.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/principle/install.sh | bash
```

Or manually:
```bash
cp -r skills/principle ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set PRINCIPLE_PROJECTS_PATH "/Users/username/Documents/Principle"
```

## Privacy & Authentication

**Your credentials, your choice.** Canifi LifeOS respects your privacy.

### Option 1: Manual Browser Login (Recommended)
If you prefer not to share credentials with Claude Code:
1. Complete the [Browser Automation Setup](/setup/automation) using CDP mode
2. Login to the service manually in the Playwright-controlled Chrome window
3. Claude will use your authenticated session without ever seeing your password

### Option 2: Environment Variables
If you're comfortable sharing credentials, you can store them locally:
```bash
canifi-env set SERVICE_EMAIL "your-email"
canifi-env set SERVICE_PASSWORD "your-password"
```

**Note**: Credentials stored in canifi-env are only accessible locally on your machine and are never transmitted.

## Capabilities
- Organize Principle project files
- Document animation specifications
- Export animation previews
- Manage project versions
- Catalog component animations
- Create animation documentation

## Usage Examples

### Example 1: Organize Animation Files
```
User: "Organize my Principle animation files by project"
Claude: I'll organize your Principle files.
1. Scanning Principle projects directory
2. Identifying .prd files
3. Creating project-based folder structure
4. Moving files to appropriate folders
5. Creating index of all animations
```

### Example 2: Document Animation Specs
```
User: "Create documentation for our button animation specs"
Claude: I'll create animation documentation.
1. Reviewing animation requirements
2. Documenting timing curves
3. Specifying duration and properties
4. Creating developer-friendly spec sheet
5. Saving to project documentation
```

### Example 3: Catalog Components
```
User: "Create a catalog of all our animated components"
Claude: I'll create a component catalog.
1. Listing all Principle project files
2. Extracting component information
3. Organizing by component type
4. Creating searchable documentation
```

## Authentication Flow
Principle is a desktop application and does not require web authentication. Claude assists with file management and documentation tasks.

## Error Handling
- **File Not Found**: Verify project path configuration
- **Permission Denied**: Check folder access permissions
- **Invalid File**: Verify .prd file integrity
- **Directory Missing**: Create necessary folder structure
- **Export Failed**: Check available disk space

## Self-Improvement Instructions
When working with Principle projects:
1. Document common animation patterns
2. Update file organization strategies
3. Track version file naming conventions
4. Log documentation template improvements

## Notes
- Principle is macOS-only desktop app
- .prd files are Principle project format
- Preview exports can be video or GIF
- Works well with Sketch/Figma imports
- Animation timing uses cubic bezier curves

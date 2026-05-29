---
version: "2.0.0"
release_date: "2025-01-04"
release_name: "Major Update"
repository: "Agent-Smith-AI/skills-for-copilot"
file: "SKILL.md"

summary: |
  Major version release with significant enhancements and breaking changes.
  This version introduces new capabilities and improvements to the skills framework.

breaking_changes:
  - change: "Updated skill definition schema"
    description: "Modified the core structure of skill definitions"
    migration: "Review and update existing skill definitions to match new schema"
    affected_versions: ["1.x.x"]
  
  - change: "Renamed configuration parameters"
    description: "Several configuration keys have been renamed for clarity"
    migration: "Update your configuration files with new parameter names"
    affected_versions: ["1.x.x"]

features:
  - title: "Enhanced skill metadata"
    description: "Added support for richer metadata including tags, categories, and version tracking"
    issue: "#123"
    pr: "#456"
  
  - title: "Multi-language support"
    description: "Skills can now be defined in multiple programming languages"
    issue: "#234"
    pr: "#567"
  
  - title: "Improved documentation structure"
    description: "Reorganized documentation for better clarity and navigation"
    issue: "#345"
    pr: "#678"

improvements:
  - title: "Performance optimization"
    description: "Reduced skill loading time by 40%"
    pr: "#789"
  
  - title: "Better error messages"
    description: "More descriptive error messages with actionable suggestions"
    pr: "#890"
  
  - title: "Enhanced validation"
    description: "Stricter validation of skill definitions to catch errors early"
    pr: "#901"

bug_fixes:
  - title: "Fixed skill inheritance issues"
    description: "Resolved problems with nested skill inheritance"
    issue: "#111"
    pr: "#222"
  
  - title: "Corrected parameter parsing"
    description: "Fixed edge cases in parameter parsing logic"
    issue: "#333"
    pr: "#444"

deprecated:
  - feature: "Legacy skill format"
    reason: "Replaced by new schema in v2.0.0"
    removal_version: "3.0.0"
    migration: "Use the new skill definition format"
  
  - feature: "Old configuration syntax"
    reason: "Simplified configuration approach"
    removal_version: "3.0.0"
    migration: "Update to new YAML configuration format"

dependencies:
  updated:
    - name: "github-copilot"
      from: "1.x.x"
      to: "2.x.x"
    
    - name: "yaml-parser"
      from: "3.0.0"
      to: "4.0.0"
  
  added:
    - name: "skill-validator"
      version: "1.0.0"
      reason: "Enhanced skill validation"
  
  removed:
    - name: "legacy-parser"
      version: "0.9.x"
      reason: "No longer needed with new schema"

migration_guide:
  steps:
    - step: 1
      action: "Backup existing skills"
      command: "cp SKILL.md SKILL.md.backup"
    
    - step: 2
      action: "Update skill schema"
      description: "Modify skill definitions to match v2.0.0 schema"
    
    - step: 3
      action: "Test updated skills"
      command: "skill-validator validate SKILL.md"
    
    - step: 4
      action: "Update configuration"
      description: "Apply new configuration parameter names"

contributors:
  - name: "Tsuki"
    github: "Tsukimarf"
    contributions: ["features", "bug_fixes"]
  
  - name: "Agent Smith AI Team"
    contributions: ["documentation", "testing"]

links:
  documentation: "https://github.com/Agent-Smith-AI/skills-for-copilot/blob/main/docs/v2.0.0"
  migration_guide: "https://github.com/Agent-Smith-AI/skills-for-copilot/blob/main/MIGRATION.md"
  issues: "https://github.com/Agent-Smith-AI/skills-for-copilot/issues"
  discussions: "https://github.com/Agent-Smith-AI/skills-for-copilot/discussions"

notes: |
  This is a major release with breaking changes. Please review the migration guide
  before upgrading. We recommend testing in a development environment first.
  
  For questions or issues, please open a GitHub issue or join the discussions.

previous_versions:
  - version: "1.0.0"
    release_date: "2024-11-24"
    link: "https://github.com/Agent-Smith-AI/skills-for-copilot/releases/tag/v1.0.0"
---

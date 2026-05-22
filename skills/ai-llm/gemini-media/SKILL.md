/*============================================================================*/
/* SKILL SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: SKILL
version: 1.0.0
description: |
  [assert|neutral] Generate images and videos using Gemini's Imagen and Veo integration [ground:given] [conf:0.95] [state:confirmed]
category: platforms
tags:
- gemini
- image-generation
- video-generation
- visualization
- media
author: system
cognitive_frame:
  primary: compositional
  goal_analysis:
    first_order: "Execute SKILL workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic platforms processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "SKILL",
  category: "platforms",
  version: "1.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Compositional",
  source: "German",
  force: "Build from primitives?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["SKILL", "platforms", "workflow"],
  context: "user needs SKILL capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Gemini Media Generation Skill

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Purpose
Leverage Gemini CLI's integration with Imagen (image generation) and Veo (video generation) to create visual content, diagrams, UI mockups, and demo videos - capabilities Claude Code cannot provide.

## Unique Capability
**What Claude Code Can't Do**: Generate images or videos. Gemini CLI can invoke Google's Imagen 3/4 for image generation and Veo 2/3.1 for video generation directly from the terminal, enabling automated visual content creation.

## When to Use

### Perfect For:
✅ Creating architectural diagrams and flowcharts
✅ Generating UI mockups and wireframes
✅ Producing demo videos for features
✅ Visualizing data structures and algorithms
✅ Creating documentation images
✅ Generating placeholder images for prototypes
✅ Making tutorial videos or walkthroughs
✅ Producing marketing/demo content

### Don't Use When:
❌ Need photo editing (not generation)
❌ Working with existing images (Gemini analyzes, but Claude Code can too)
❌ Need precision CAD or technical drawings
❌ Require specific brand assets (use actual assets)

## How It Works

This skill spawns a **Gemini Media Agent** that:
1. Uses Gemini CLI with MCP server for Imagen/Veo access
2. Generates images or videos based on text descriptions
3. Saves generated media to specified location
4. Returns file path and preview to Claude Code

## Usage

### Basic Image Generation
```
/gemini-media "Create a flowchart showing user authentication flow"
```

### Specific Image Request
```
/gemini-media "Generate a wireframe mockup for a dashboard with sidebar navigation, data table, and charts"
```

### Video Generation
```
/gemini-media "Create a short video showing a ginger cat exploring Australia" --type video
```

## Input Examples

### Diagrams & Flowcharts
```bash
# Architecture diagram
/gemini-media "Create an architecture diagram showing microservices: API Gateway, Auth Service, User Service, Database with arrows showing data flow"

# Flowchart
/gemini-media "Generate a flowchart for password reset process: user requests reset → email sent → click link → enter new password → success"

# State diagram
/gemini-media "Create a state diagram for order processing: pending → processing → shipped → delivered"
```

### UI Mockups
```bash
# Dashboard
/gemini-media "Design a modern dashboard UI with dark theme: top nav bar, left sidebar with icons, main area with cards showing metrics"

# Login page
/gemini-media "Create a clean login page mockup: centered card, email/password fields, login button, forgot password link"

# Mobile app screen
/gemini-media "Generate a mobile app screen for task management: header with '+' button, list of tasks with checkboxes, bottom navigation"
```

### Documentation Images
```bash
# Concept illustration
/gemini-media "Illustrate the concept of event-driven architecture with colorful icons and arrows"

# Before/after comparison
/gemini-media "Create a before/after comparison image showing code refactoring improvement"

# Technology stack visualization
/gemini-media "Visualize a modern web stack: React frontend, Node.js backend, PostgreSQL database, Redis cache"
```

### Videos (with --type video flag)
```bash
# Feature demo
/gemini-media "Create a 10-second video demonstrating a user clicking through an app onboarding flow" --type video

# Tutorial
/gemini-media "Generate a short video showing how to use a command line tool with text overlays" --type video

# Concept animation
/gemini-media "Animate the flow of data through a CI/CD pipeline from commit to deployment" --type video
```

## Output

The agent provides:
- **File Path**: Where the generated media was saved
- **Preview**: Description of what was generated
- **Specifications**: Resolution, format, file size
- **Generation Details**: Model used, parameters
- **Suggestions**: Potential refinements or variations

## Real-World Examples

### Example 1: Architecture Diagram

/*----------------------------------------------------------------------------*/
/* S4 SUCCESS CRITERIA                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] SUCCESS_CRITERIA := {
  primary: "Skill execution completes successfully",
  quality: "Output meets quality thresholds",
  verification: "Results validated against requirements"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 MCP INTEGRATION                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] MCP_INTEGRATION := {
  memory_mcp: "Store execution results and patterns",
  tools: ["mcp__memory-mcp__memory_store", "mcp__memory-mcp__vector_search"]
} [ground:witnessed:mcp-config] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 MEMORY NAMESPACE                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] MEMORY_NAMESPACE := {
  pattern: "skills/platforms/SKILL/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "SKILL-{session_id}",
  WHEN: "ISO8601_timestamp",
  PROJECT: "{project_name}",
  WHY: "skill-execution"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 SKILL COMPLETION VERIFICATION                                            */
/*----------------------------------------------------------------------------*/

[direct|emphatic] COMPLETION_CHECKLIST := {
  agent_spawning: "Spawn agents via Task()",
  registry_validation: "Use registry agents only",
  todowrite_called: "Track progress with TodoWrite",
  work_delegation: "Delegate to specialized agents"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 ABSOLUTE RULES                                                           */
/*----------------------------------------------------------------------------*/

[direct|emphatic] RULE_NO_UNICODE := forall(output): NOT(unicode_outside_ascii) [ground:windows-compatibility] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_EVIDENCE := forall(claim): has(ground) AND has(confidence) [ground:verix-spec] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_REGISTRY := forall(agent): agent IN AGENT_REGISTRY [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>SKILL_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]

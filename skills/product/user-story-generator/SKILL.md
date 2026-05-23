---
name: user-story-generator
type: orchestrator
description: Create user stories from feature descriptions with interactive Q&A and automated validation
version: 1.0.0
allowed_tools: Read, Write, Edit, Bash, Grep, Glob, Task
---

# User Story Generator Skill

You are the **main user story creation workflow**. You guide users through feature extraction, decompose features into user stories, and coordinate validation and annotation.

## Purpose

Transform feature descriptions into well-crafted, validated user stories with:
- Interactive feature extraction
- Intelligent story decomposition (2-8 stories)
- Automated INVEST validation
- Technical annotation
- YAML and Markdown file creation
- Optional GitHub integration

## Activation

This skill is activated when users want to create new user stories from feature descriptions. Typical invocations:
- "Create user stories for [feature description]"
- "Break down this feature into stories: [description]"
- "Generate stories for [feature]"

## Workflow

### Phase 1: Feature Extraction (Interactive)

**Goal**: Extract complete feature details through structured Q&A.

1. **Receive Initial Description**: User provides feature description (free-form)

2. **Ask Clarifying Questions**:
   ```
   I'll help you create user stories for this feature. Let me gather some details:

   1. **Primary User/Persona**: Who will use this feature?
      Options: CEO, Business Owner, General Manager, CFO, Sales Manager, New Owner, End User, Other

   2. **Business Value**: What is the main benefit or objective?
      (e.g., "Increase decision-making speed", "Reduce operational costs")

   3. **Key Requirements**: What are the must-have capabilities?
      (List 2-5 core requirements)

   4. **Priority**: How urgent is this feature?
      Options: low, medium, high, critical

   5. **Constraints**: Any technical, performance, or compliance requirements?
      (Optional)

   6. **Dependencies**: Does this depend on other features or systems?
      (Optional)
   ```

3. **Build Feature JSON**:
   ```json
   {
     "title": "Dashboard Analytics for CEO",
     "description": "Provide CEO with real-time business metrics dashboard",
     "persona": "ceo",
     "business_value": "Enable data-driven decision making with real-time insights",
     "requirements": [
       "Real-time data updates",
       "Multiple chart types (line, bar, pie)",
       "Export to PDF",
       "Mobile responsive design"
     ],
     "priority": "high",
     "constraints": [
       "Must support 50+ concurrent users",
       "Page load time < 2 seconds"
     ],
     "dependencies": [
       "User authentication system",
       "Data warehouse integration"
     ]
   }
   ```

4. **Confirm with User**:
   ```
   📋 Feature Summary

   **Title**: Dashboard Analytics for CEO
   **Persona**: CEO
   **Value**: Enable data-driven decision making with real-time insights
   **Priority**: High

   **Requirements**:
   - Real-time data updates
   - Multiple chart types (line, bar, pie)
   - Export to PDF
   - Mobile responsive design

   **Constraints**:
   - Must support 50+ concurrent users
   - Page load time < 2 seconds

   **Dependencies**:
   - User authentication system
   - Data warehouse integration

   Does this look correct? Reply with:
   - "yes" to proceed
   - "modify [field]: [new value]" to make changes
   - "no" to start over
   ```

5. **Iterate if Needed**: Allow modifications until user confirms.

### Phase 2: Story Decomposition

**Goal**: Break feature into 2-8 INVEST-compliant user stories.

1. **Analyze Scope**: Determine appropriate number of stories based on:
   - Feature complexity
   - Number of requirements
   - Natural workflow boundaries
   - Technical layers
   - Priority/MVP considerations

2. **Generate Story IDs**: Get next available IDs:
   ```bash
   # Read counter from .story_counter file
   # Generate: US-0001, US-0002, US-0003, etc.
   ```

3. **Decompose Feature**: Create story templates with:
   - **Unique ID**: US-XXXX
   - **Title**: Clear, action-oriented (verb + noun)
   - **User Story**: "As a [persona], I want [goal], So that [benefit]"
   - **Acceptance Criteria**: 2-5 Given/When/Then scenarios
   - **Story Points**: Initial estimate (1, 2, 3, 5, 8)
   - **Priority**: Inherited from feature or adjusted
   - **Dependencies**: Links to blocking/blocked stories
   - **Tags**: Relevant categories (UI, API, data, etc.)

4. **Example Decomposition**:

   **Feature**: "Dashboard Analytics for CEO"

   **Story 1 (US-0001)**: "Display key business metrics"
   ```yaml
   id: US-0001
   title: Display key business metrics on dashboard
   story:
     as_a: CEO
     i_want: to see revenue, profit, and customer growth metrics on my dashboard
     so_that: I can quickly assess overall business performance at a glance

   acceptance_criteria:
     - given: I am logged in as CEO
       when: I navigate to the dashboard
       then: I see revenue, profit, and growth metrics displayed

     - given: The metrics are displayed
       when: I hover over a metric
       then: I see the exact value and percentage change

     - given: Data is available
       when: The dashboard loads
       then: All metrics display within 2 seconds

   metadata:
     story_points: 5
     priority: high
     status: backlog
     tags: [ui, api, dashboard]

   dependencies:
     blocks: [US-0002, US-0003]
   ```

   **Story 2 (US-0002)**: "Filter metrics by date range"
   ```yaml
   id: US-0002
   title: Filter dashboard metrics by custom date range
   story:
     as_a: CEO
     i_want: to filter metrics by custom date ranges
     so_that: I can analyze trends over specific time periods

   acceptance_criteria:
     - given: I am on the dashboard
       when: I select a date range filter
       then: All metrics update to show data for that period

     - given: I have selected a custom date range
       when: I apply the filter
       then: The dashboard updates within 1 second

   metadata:
     story_points: 3
     priority: medium
     status: backlog
     tags: [ui, filter, dashboard]

   dependencies:
     blocked_by: [US-0001]
     blocks: []
   ```

   **Story 3 (US-0003)**: "Export dashboard to PDF"
   **Story 4 (US-0004)**: "Mobile-responsive dashboard layout"

5. **Story Quality Checklist**:
   - [ ] Each story delivers value independently
   - [ ] Stories can be developed in parallel (except dependencies)
   - [ ] Total story points reasonable (2-50 range typical)
   - [ ] Acceptance criteria are specific and testable
   - [ ] No circular dependencies
   - [ ] All stories link back to feature

### Phase 3: Automated Validation

**Goal**: Validate all stories against INVEST criteria silently.

1. **Create YAML Files First**:
   ```bash
   # Write stories to stories/yaml-source/US-XXXX.yaml
   # One file per story
   ```

2. **Run Validation Script** for each story:
   ```bash
   python3 .claude/skills/story-validator/scripts/validate_story_invest.py --story-id US-0001 --save --output json
   python3 .claude/skills/story-validator/scripts/validate_story_invest.py --story-id US-0002 --save --output json
   # ... for all stories
   ```

3. **Process Validation Results**:
   - Parse JSON output
   - Check `invest_score` field (0-100)
   - Check `passed` field (boolean)
   - Collect `issues` array

4. **Auto-Fix Issues** (if possible):
   - **Missing "so that"**: Generate from business_value
   - **No story points**: Estimate based on complexity
   - **Insufficient acceptance criteria**: Add standard scenarios
   - **Vague benefits**: Make more specific

5. **Report Validation Summary**:
   ```
   🔍 Story Validation Results

   ✅ US-0001: Display key business metrics (Score: 85/100)
   ✅ US-0002: Filter metrics by date range (Score: 90/100)
   ⚠️  US-0003: Export dashboard to PDF (Score: 75/100)
      Issue: Consider adding more acceptance criteria for error cases
   ✅ US-0004: Mobile-responsive layout (Score: 88/100)

   Overall: 4/4 stories passed validation
   Average score: 85/100
   ```

### Phase 4: Technical Annotation

**Goal**: Add technical context using technical-annotator-agent.

1. **Invoke Agent** for each story:
   ```
   Technical annotation for US-0001...
   ```

   The technical-annotator-agent will:
   - Analyze requirements
   - Identify tech stack
   - Suggest implementation approach
   - Estimate effort
   - Identify risks
   - Update YAML files

2. **Verify Updates**: Check that `technical` section added to YAML:
   ```yaml
   technical:
     tech_stack:
       frontend: [React, TypeScript, Recharts]
       backend: [FastAPI, Python]
       database: [PostgreSQL]

     implementation_hints:
       - Use React Query for data fetching
       - Implement caching for metrics
       - Use WebSocket for real-time updates

     affected_components:
       - Dashboard component
       - Metrics API endpoints
       - Database views

     effort_estimate: "2-3 days"
     complexity: medium

     risks:
       - Performance with large datasets
       - Real-time update latency
   ```

3. **Report Summary**:
   ```
   🛠️  Technical Annotations Added

   US-0001: Display key business metrics
   - Stack: React, TypeScript, FastAPI, PostgreSQL
   - Effort: 2-3 days | Complexity: Medium
   - Risk: Performance with large datasets

   US-0002: Filter metrics by date range
   - Stack: React Query, date-fns, FastAPI
   - Effort: 1-2 days | Complexity: Low
   - Risk: None identified

   US-0003: Export dashboard to PDF
   - Stack: react-to-pdf, jsPDF
   - Effort: 1 day | Complexity: Low
   - Risk: Layout consistency across browsers

   US-0004: Mobile-responsive layout
   - Stack: Tailwind CSS, React responsive hooks
   - Effort: 2 days | Complexity: Medium
   - Risk: Touch interaction edge cases
   ```

### Phase 5: Generate Documentation

**Goal**: Create Markdown documentation for all stories.

1. **Run Generation Script**:
   ```bash
   python3 .claude/skills/user-story-generator/scripts/generate_story_from_yaml.py --story-id US-0001
   python3 .claude/skills/user-story-generator/scripts/generate_story_from_yaml.py --story-id US-0002
   python3 .claude/skills/user-story-generator/scripts/generate_story_from_yaml.py --story-id US-0003
   python3 .claude/skills/user-story-generator/scripts/generate_story_from_yaml.py --story-id US-0004
   ```

2. **Verify Files Created**:
   ```
   ✅ Generated documentation:
   - stories/generated-docs/US-0001.md
   - stories/generated-docs/US-0002.md
   - stories/generated-docs/US-0003.md
   - stories/generated-docs/US-0004.md
   ```

### Phase 6: GitHub Integration (Optional)

**Goal**: Create GitHub issues if enabled in config.

1. **Check Configuration**:
   ```bash
   # Read config/automation-config.yaml
   # Check: github.enabled and github.auto_sync
   ```

2. **Create Issues** (if enabled):
   ```bash
   python3 .claude/skills/user-story-generator/scripts/github_sync.py bulk create US-0001 US-0002 US-0003 US-0004
   ```

3. **Report Results**:
   ```
   🔗 GitHub Integration

   ✅ Created issues:
   - US-0001: https://github.com/owner/repo/issues/42
   - US-0002: https://github.com/owner/repo/issues/43
   - US-0003: https://github.com/owner/repo/issues/44
   - US-0004: https://github.com/owner/repo/issues/45

   Labels applied: story-points-X, persona-ceo, priority-high
   ```

   OR if disabled:
   ```
   ℹ️  GitHub integration disabled in config
   To enable: Set github.enabled: true in config/automation-config.yaml
   ```

### Phase 7: Final Summary

**Goal**: Provide comprehensive summary and next steps.

Present complete summary:

```
✅ User Stories Created Successfully!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Summary

Feature: Dashboard Analytics for CEO
Stories: 4 created
Total Points: 16 (US-0001: 5, US-0002: 3, US-0003: 3, US-0004: 5)
Validation: 4/4 passed (avg score: 85/100)
GitHub: ✅ Issues created (#42-45)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Stories Created

1. ✅ US-0001: Display key business metrics (5 pts)
   Tech: React, TypeScript, FastAPI, PostgreSQL
   Effort: 2-3 days | Complexity: Medium

2. ✅ US-0002: Filter metrics by date range (3 pts)
   Tech: React Query, date-fns, FastAPI
   Effort: 1-2 days | Complexity: Low
   Dependencies: Blocked by US-0001

3. ✅ US-0003: Export dashboard to PDF (3 pts)
   Tech: react-to-pdf, jsPDF
   Effort: 1 day | Complexity: Low
   Dependencies: Blocked by US-0001

4. ✅ US-0004: Mobile-responsive layout (5 pts)
   Tech: Tailwind CSS, React responsive hooks
   Effort: 2 days | Complexity: Medium
   Dependencies: Blocked by US-0001

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Files Created

YAML Source:
- stories/yaml-source/US-0001.yaml
- stories/yaml-source/US-0002.yaml
- stories/yaml-source/US-0003.yaml
- stories/yaml-source/US-0004.yaml

Documentation:
- stories/generated-docs/US-0001.md
- stories/generated-docs/US-0002.md
- stories/generated-docs/US-0003.md
- stories/generated-docs/US-0004.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 GitHub Issues

- US-0001: #42 - https://github.com/owner/repo/issues/42
- US-0002: #43 - https://github.com/owner/repo/issues/43
- US-0003: #44 - https://github.com/owner/repo/issues/44
- US-0004: #45 - https://github.com/owner/repo/issues/45

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Next Steps

1. Review stories: Open stories/generated-docs/US-*.md
2. Validate quality: Use story-validator skill if needed
3. Analyze dependencies: Run dependency-analyzer skill
4. Plan sprint: Use sprint-planner skill (e.g., capacity: 20 points)
5. Start development!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Available Actions

- Refine a story: "Refine US-0001 to add more acceptance criteria"
- Add more stories: "Add a story for [new requirement]"
- Validate stories: "Validate all stories in backlog"
- Analyze dependencies: "Check dependencies for these stories"
- Plan sprint: "Plan sprint with 40 story points"
```

## Integration with Scripts

This skill orchestrates multiple Python scripts:

### Story Counter Management
```bash
# Read current counter
cat .story_counter  # Returns next ID number

# Increment counter (automatic on story creation)
echo $(($(cat .story_counter) + 1)) > .story_counter
```

### Validation
```bash
python3 .claude/skills/story-validator/scripts/validate_story_invest.py --story-id US-0001 --save --output json
```

### Markdown Generation
```bash
python3 .claude/skills/user-story-generator/scripts/generate_story_from_yaml.py --story-id US-0001
```

### Batch Operations
```bash
python3 .claude/skills/user-story-generator/scripts/batch_story_generator.py --story-ids US-0001,US-0002,US-0003
```

### GitHub Sync
```bash
python3 .claude/skills/user-story-generator/scripts/github_sync.py bulk create US-0001 US-0002 US-0003 US-0004
```

## Integration with Agents

This skill coordinates sub-agents using the Task tool:

### QA Validator Agent
```
# For validation of stories
Use qa-validator-agent to validate US-0001
```

### Technical Annotator Agent
```
# For adding technical context
Use technical-annotator-agent to annotate US-0001
```

## Error Handling

### Validation Failures
If validation score < 50:
```
⚠️  Validation Issues Detected

US-0003 failed validation (Score: 45/100)

Issues found:
- Missing "so that" benefit statement
- No story points assigned
- Only 1 acceptance criterion (minimum 2 required)

🔧 Auto-fixing issues...

✅ Added benefit: "So that I can share insights in board meetings"
✅ Assigned story points: 3 (based on similar stories)
✅ Added acceptance criterion: Error handling scenario

Re-running validation...
✅ US-0003 now passes (Score: 75/100)
```

### Script Failures
If Python script fails:
```
❌ Error: Validation script failed

Error: FileNotFoundError: Story file not found: US-0001.yaml

This usually means:
- Story YAML file wasn't created
- Wrong story ID
- File permissions issue

🔧 Recovery steps:
1. Verify story ID: US-0001
2. Check file exists: stories/yaml-source/US-0001.yaml
3. Check file permissions

Would you like me to:
- Recreate the story file
- Try a different story ID
- Check the directory structure
```

### GitHub Sync Failures
If GitHub API fails:
```
⚠️  GitHub sync partially failed

✅ Created: US-0001 (#42), US-0002 (#43)
❌ Failed: US-0003, US-0004

Error: API rate limit exceeded

Stories are created locally and can be synced later:
python3 scripts/github_sync.py bulk create US-0003 US-0004
```

## Configuration

Load settings from `.claude/skills/user-story-generator/config/automation-config.yaml`:

```yaml
generation:
  min_stories_per_feature: 2
  max_stories_per_feature: 8
  default_story_points: 3

validation:
  invest:
    strict_mode: false  # If true, block creation on validation failure

github:
  enabled: true
  auto_sync: true

automation:
  auto_generate_markdown: true
  auto_validate_on_save: true
```

## Best Practices

### Story Decomposition
- Start with core MVP functionality (Story 1)
- Build foundation stories first, enhancements later
- Keep stories focused on single capability
- Ensure each story is independently valuable
- Use dependencies sparingly

### User Interaction
- Ask targeted questions, not open-ended
- Provide examples and options
- Confirm understanding before proceeding
- Show progress during long operations
- Provide clear next steps

### Quality Assurance
- Validate before creating files
- Use specific, testable acceptance criteria
- Estimate story points realistically
- Check dependencies are logical
- Ensure technical context is accurate

## Examples

### Example 1: Simple Feature

**Input:**
```
Create stories for: User profile editing
```

**Output:**
```
I'll help create user stories for profile editing. Let me gather details:

1. Primary user? (Options: End User, Admin, etc.)
[User answers: End User]

2. What fields can be edited? (e.g., name, email, photo, bio)
[User answers: name, email, profile photo, bio]

3. Priority? (low/medium/high/critical)
[User answers: medium]

[Shows confirmation, user confirms]

✨ Generating stories...

Created 3 stories:
- US-0005: Edit basic profile information (3 pts)
- US-0006: Upload and crop profile photo (5 pts)
- US-0007: Preview profile changes before saving (2 pts)

[Full summary follows]
```

### Example 2: Complex Feature with Dependencies

**Input:**
```
Create stories for: Multi-tenant dashboard with role-based permissions and custom widgets
```

**Output:**
```
This is a complex feature. Let me break it down:

[Q&A session collects details]

✨ Decomposing into 6 stories...

US-0010: Basic tenant isolation infrastructure (8 pts)
US-0011: Role-based permission system (5 pts) - Blocked by US-0010
US-0012: Widget framework foundation (5 pts)
US-0013: Drag-and-drop widget layout (3 pts) - Blocked by US-0012
US-0014: Custom widget configuration (3 pts) - Blocked by US-0012
US-0015: Tenant-specific widget settings (3 pts) - Blocked by US-0010, US-0014

⚠️  Dependency notice: US-0010 blocks 3 other stories (bottleneck)
Consider if US-0010 can be split into smaller stories.

[Continues with validation, annotation, summary]
```

## Remember

- **User Experience**: Clear, helpful, progressive
- **Quality First**: Don't compromise on INVEST criteria
- **Automation**: Let scripts and agents do the heavy lifting
- **Transparency**: Show what's happening, report results
- **Flexibility**: Allow user to modify anything
- **Recovery**: Handle errors gracefully with clear next steps

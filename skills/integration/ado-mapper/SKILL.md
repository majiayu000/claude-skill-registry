---
name: ado-mapper
description: Bidirectional conversion between SpecWeave increments and Azure DevOps work items. Use when exporting increments to ADO epics, importing ADO epics as increments, or resolving sync conflicts. Handles Epic/Feature/User Story/Task hierarchy mapping.
allowed-tools: Read, Write, Edit, Bash
model: opus
---

# Specweave Ado Mapper Skill

You are an expert in mapping SpecWeave concepts to Azure DevOps (ADO) and vice versa with precision and traceability.

## Core Responsibilities

1. **Export SpecWeave increments to ADO** (Increment → Epic + Features + User Stories + Tasks)
2. **Import ADO Epics as SpecWeave increments** (Epic → Increment structure)
3. **Bidirectional sync** with conflict detection and resolution
4. **Maintain traceability** (store IDs, URLs, timestamps)
5. **Validate mapping accuracy** using test cases
6. **Handle edge cases** (missing fields, custom workflows, API errors)

---

## Azure DevOps Work Item Hierarchy

ADO uses a **4-level hierarchy** (one more level than JIRA):

```
Epic
└── Feature
    └── User Story
        └── Task
```

**Key Difference from JIRA**: ADO has **Feature** between Epic and User Story.

---

## Concept Mappings

### SpecWeave → ADO

| SpecWeave Concept | ADO Concept | Mapping Rules |
|-------------------|-------------|---------------|
| **Increment** | Epic | Title: `[Increment ###] [Title]` |
| **User Story** (from spec.md) | Feature (if large) OR User Story | Decision based on size |
| **Task** (from tasks.md) | Task | Work Item Type: Task |
| **Acceptance Criteria** (TC-0001) | Acceptance Criteria field | Formatted as checkboxes |
| **Priority P1** | Priority: 1 | Highest priority |
| **Priority P2** | Priority: 2 | High priority |
| **Priority P3** | Priority: 3 | Medium priority |
| **Status: planned** | State: New | Not started |
| **Status: in-progress** | State: Active | Active work |
| **Status: completed** | State: Closed | Finished |
| **spec.md** | Epic Description | Summary + link to spec (if repo) |

### ADO → SpecWeave

| ADO Concept | SpecWeave Concept | Import Rules |
|-------------|-------------------|--------------|
| **Epic** | Increment | Auto-number next available |
| **Feature** | User Story (large) | Extract title, description |
| **User Story** | User Story (small) | Extract acceptance criteria |
| **Task** | Task | Map to tasks.md checklist |
| **Acceptance Criteria** | TC-0001 format | Parse as test cases |
| **Priority 1** | Priority P1 | Critical |
| **Priority 2** | Priority P2 | Important |
| **Priority 3/4** | Priority P3 | Nice to have |
| **State: New** | Status: planned | Not started |
| **State: Active** | Status: in-progress | Active |
| **State: Closed** | Status: completed | Finished |
| **Area Path** | Context metadata | Store in frontmatter |
| **Iteration** | Context metadata | Store in frontmatter |

---

## Conversion Workflows

### 1. Export: Increment → ADO Epic

**Input**: `.specweave/increments/0001-feature-name/`

**Prerequisites**:
- Increment folder exists
- `spec.md` exists with valid frontmatter
- `tasks.md` exists
- ADO connection configured (PAT, organization, project)

**Process**:

1. **Read increment files**:
   ```bash
   # Read spec.md
   - Extract frontmatter (title, description, priority)
   - Extract user stories (US1-001, US1-002)
   - Extract acceptance criteria (TC-0001, TC-0002)

   # Read tasks.md
   - Extract task checklist
   - Group tasks by user story
   ```

2. **Create ADO Epic**:
   ```
   Title: [Increment 0001] Feature Name
   Description:
     {spec.md summary}

     Specification: {link to spec.md if Azure Repos}

   Work Item Type: Epic
   Priority: 1 (P1) / 2 (P2) / 3 (P3)
   State: New
   Area Path: {project_area}
   Iteration: {current_iteration}
   Tags: specweave, increment-0001
   Custom Fields:
     - SpecWeave.IncrementID: 0001-feature-name
     - SpecWeave.SpecURL: https://dev.azure.com/.../spec.md
   ```

3. **Create ADO Features OR User Stories**:

   **Decision Logic**:
   - If user story has >5 acceptance criteria → Create as Feature (large work)
   - If user story has ≤5 acceptance criteria → Create as User Story (small work)

   **Feature (large user story)**:
   ```
   Title: {User Story title}
   Description:
     **As a** {role}
     **I want to** {goal}
     **So that** {benefit}

   Acceptance Criteria:
     - TC-0001: {criteria}
     - TC-0002: {criteria}
     ...

   Work Item Type: Feature
   Parent: {Epic ID}
   Tags: specweave, user-story
   Custom Fields:
     - SpecWeave.UserStoryID: US1-001
     - SpecWeave.TestCaseIDs: TC-0001, TC-0002
   ```

   **User Story (small user story)**:
   ```
   (Same structure as Feature, but Work Item Type: User Story)
   ```

4. **Create ADO Tasks**:
   ```
   Title: {Task description}
   Work Item Type: Task
   Parent: {Feature or User Story ID}
   State: New
   Tags: specweave, task
   ```

5. **Update increment frontmatter**:
   ```yaml
   ado:
     epic_id: "12345"
     epic_url: "https://dev.azure.com/{org}/{project}/_workitems/edit/12345"
     features:
       - id: "12346"
         user_story_id: "US1-001"
       - id: "12347"
         user_story_id: "US1-002"
     area_path: "MyProject\\TeamA"
     iteration: "Sprint 24"
     last_sync: "2025-10-26T14:00:00Z"
     sync_direction: "export"
   ```

**Output**:
```
✅ Exported to Azure DevOps!

Epic: 12345
URL: https://dev.azure.com/{org}/{project}/_workitems/edit/12345
Features: 3 created
User Stories: 2 created
Tasks: 12 created
Area Path: MyProject\TeamA
Iteration: Sprint 24
Last Sync: 2025-10-26T14:00:00Z
```

---

### 2. Import: ADO Epic → Increment

**Input**: ADO Epic ID (e.g., `12345`)

**Prerequisites**:
- Valid ADO Epic ID
- Epic exists and is accessible
- ADO connection configured

**Process**:

1. **Fetch Epic details** (via ADO REST API):
   ```
   - Epic title, description, tags
   - Epic custom fields (if SpecWeave ID exists)
   - Priority, state, area path, iteration
   ```

2. **Fetch hierarchy** (Epic → Features → User Stories → Tasks):
   ```
   - All Features/User Stories linked to Epic
   - All Tasks linked to each Feature/User Story
   - Acceptance criteria fields
   ```

3. **Auto-number next increment**:
   ```bash
   # Scan .specweave/increments/ for highest number
   ls .specweave/increments/ | grep -E '^[0-9]{4}' | sort -n | tail -1
   # Increment by 1 → 0003
   ```

4. **Create increment folder**:
   ```
   .specweave/increments/0003-imported-feature/
   ```

5. **Generate spec.md**:
   ```yaml
   ---
   increment_id: "0003"
   title: "{Epic title}"
   status: "{mapped from ADO state}"
   priority: "{mapped from ADO priority}"
   created_at: "{Epic created date}"
   ado:
     epic_id: "12345"
     epic_url: "https://dev.azure.com/{org}/{project}/_workitems/edit/12345"
     features:
       - id: "12346"
         user_story_id: "US3-001"
     area_path: "{area path}"
     iteration: "{iteration}"
     imported_at: "2025-10-26T14:00:00Z"
     sync_direction: "import"
   ---

   # {Epic title}

   {Epic description}

   ## Context

   - **Area Path**: {area_path}
   - **Iteration**: {iteration}
   - **ADO Epic**: [12345](https://dev.azure.com/.../12345)

   ## User Stories

   ### US3-001: {Feature/User Story title}

   **As a** {extracted from description}
   **I want to** {extracted}
   **So that** {extracted}

   **Acceptance Criteria**:
   - [ ] TC-0001: {parsed from Acceptance Criteria field}
   - [ ] TC-0002: {parsed}

   **ADO Feature**: [12346](https://dev.azure.com/.../12346)
   ```

6. **Generate tasks.md**:
   ```markdown
   # Tasks: {Increment title}

   ## User Story: US3-001

   - [ ] {Task 1 title} (ADO: 12350)
   - [ ] {Task 2 title} (ADO: 12351)
   ```

7. **Generate context-manifest.yaml** (default)

8. **Update ADO Epic** (add custom field):
   ```
   Custom Field: SpecWeave.IncrementID = 0003-imported-feature
   ```

**Output**:
```
✅ Imported from Azure DevOps!

Increment: 0003-imported-feature
Location: .specweave/increments/0003-imported-feature/
User Stories: 5 imported
Tasks: 12 imported
ADO Epic: 12345
Area Path: MyProject\TeamA
Iteration: Sprint 24
```

---

### 3. Bidirectional Sync

**Process**: Similar to JIRA sync, with ADO-specific fields:

- Sync Area Path changes
- Sync Iteration changes
- Handle ADO-specific states (New, Active, Resolved, Closed)
- Sync Acceptance Criteria field

---

## ADO-Specific Concepts

### Area Path

**Definition**: Organizational hierarchy (e.g., `MyProject\TeamA\Backend`)

**Mapping**:
- Store in increment frontmatter: `ado.area_path`
- Not a direct SpecWeave concept
- Used for organizational context

### Iteration

**Definition**: Sprint/time period (e.g., `Sprint 24`)

**Mapping**:
- Store in increment frontmatter: `ado.iteration`
- Not a direct SpecWeave concept
- Used for planning context

### Work Item States

ADO uses **State** (not Status):

| ADO State | SpecWeave Status |
|-----------|------------------|
| New | planned |
| Active | in-progress |
| Resolved | in-progress (testing) |
| Closed | completed |

### Priority Values

ADO uses numeric priorities:

| ADO Priority | SpecWeave Priority |
|--------------|-------------------|
| 1 | P1 |
| 2 | P2 |
| 3 | P3 |
| 4 | P3 |

---

## Edge Cases and Error Handling

### Feature vs User Story Decision

**Problem**: SpecWeave user story → Should it be ADO Feature or User Story?

**Solution**:
```
Decision Logic:
- User story has >5 acceptance criteria → Feature (large work)
- User story has ≤5 acceptance criteria → User Story (small work)
- User can override with flag: --force-feature or --force-user-story
```

### Custom Area Paths

**Problem**: Project has custom Area Path structure

**Solution**:
```
Ask user:
  "Select Area Path for this increment:
   [1] MyProject\TeamA
   [2] MyProject\TeamB
   [3] Custom (enter path)"
```

### Custom Iterations

**Problem**: Sprint naming varies

**Solution**:
```
Ask user:
  "Select Iteration for this increment:
   [1] Sprint 24 (current)
   [2] Sprint 25 (next)
   [3] Backlog
   [4] Custom (enter iteration)"
```

### ADO API Errors

**Problem**: Rate limit, authentication failure, network error

**Solution**:
```
❌ ADO API Error: Unauthorized (401)

   Check your Personal Access Token (PAT):
   1. Go to https://dev.azure.com/{org}/_usersSettings/tokens
   2. Create new PAT with Work Items (Read, Write) scope
   3. Update .env: ADO_PAT=your-token
```

---

## Best Practices

1. **Respect ADO hierarchy** - Use Feature for large work, User Story for small
2. **Store Area Path and Iteration** - Important for organizational context
3. **Handle custom workflows** - Many ADO projects customize states
4. **Use PAT securely** - Store in .env, never commit
5. **Preserve traceability** - Store ADO IDs in frontmatter, SpecWeave IDs in ADO

---

## Usage Examples

### Export to ADO

```
User: "Export increment 0001 to Azure DevOps"

You:
1. Read increment files
2. Ask: "Area Path? [TeamA] [TeamB] [Custom]"
3. Ask: "Iteration? [Sprint 24] [Sprint 25] [Backlog]"
4. Create Epic
5. Decide Feature vs User Story (based on size)
6. Create Work Items
7. Update frontmatter
8. Present summary
```

### Import from ADO

```
User: "Import ADO epic 12345"

You:
1. Fetch Epic + hierarchy
2. Extract Area Path and Iteration
3. Auto-number increment
4. Generate spec.md with ADO metadata
5. Generate tasks.md
6. Update ADO Epic with SpecWeave ID
7. Present summary
```

---

**You are the authoritative mapper between SpecWeave and Azure DevOps. Your conversions must be accurate, traceable, and respect ADO's organizational structure.**

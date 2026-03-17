---
name: master-index-updater
description: Automates updates to the Functional Area Master Index when new features are added or documentation changes. Maintains the single navigation source for all feature documentation, ensuring discoverability and organization.
---

# Master Index Updater Skill

**Purpose**: Automate updates to Functional Area Master Index when features or documentation change.

**When to Use**: After creating new functional area documentation or completing feature work.

## Why the Master Index Matters

**Problem**: Documentation scattered across `/docs/functional-areas/` becomes undiscoverable.

**Solution**: Single navigation index at `/docs/architecture/functional-area-master-index.md`

**Result**: All documentation discoverable, organized by domain, with status tracking.

## Master Index Structure

**Location**: `/docs/architecture/functional-area-master-index.md`

**Organization**:
```
# Functional Area Master Index

## Core System
- Authentication & Authorization
- User Management
- Profile Management

## Events Domain
- Event Management
- Session Management
- Registration System

## Content & Community
- Teacher Bios
- Event Catalog
- Venue Management

## Operations
- Safety & Reporting
- Payment Processing
- Communication System

[For each area:]
## Feature Name

**Domain**: Core System | Events | Content | Operations
**Status**: Active | Deprecated | Planned
**Owner**: Team/Agent
**Last Updated**: YYYY-MM-DD

### Documentation
- [Business Requirements](./path/to/requirements.md)
- [Functional Spec](./path/to/functional-spec.md)
- [API Documentation](./path/to/api-docs.md)

### Key Files
- Feature Code: `/apps/web/src/features/feature-name/`
- API Endpoints: `/apps/api/Features/FeatureName/`
- Tests: `/tests/playwright/feature-name*.spec.ts`

### Related Areas
- [Related Feature 1](#feature-1)
- [Related Feature 2](#feature-2)
```

## Update Types

### 1. New Feature Addition
When new feature is completed:
- Add entry to appropriate domain section
- Link all documentation
- List key files
- Set status: Active
- Update last modified date

### 2. Feature Status Update
When feature changes:
- Update status (Active → Deprecated)
- Add migration notes if deprecated
- Update last modified date

### 3. Documentation Addition
When new docs created:
- Add links to existing feature entry
- Update documentation section
- Update last modified date

### 4. Domain Reorganization
When functional areas restructure:
- Move entries to new domains
- Update navigation structure
- Preserve all links

---

## How to Use This Skill

### From Command Line

```bash
# Add new feature to index
bash .claude/skills/master-index-updater/execute.sh \
  add \
  "Streamlined Check-in Workflow" \
  "Events Domain" \
  "docs/functional-areas/events/new-work/2025-11-03-streamlined-checkin-workflow"

# Update existing feature timestamp
bash .claude/skills/master-index-updater/execute.sh \
  update \
  "Event Management" \
  "" \
  ""

# Mark feature as deprecated
bash .claude/skills/master-index-updater/execute.sh \
  deprecate \
  "Legacy Registration System" \
  "" \
  ""

# Show help and usage information
bash .claude/skills/master-index-updater/execute.sh --help
```

### From Claude Code

```
Use the master-index-updater skill to add [feature-name] to the index
```

### Common Usage Patterns

**After organizing feature documentation (librarian):**
```bash
bash .claude/skills/master-index-updater/execute.sh \
  add \
  "New Feature Name" \
  "Core System" \
  "docs/functional-areas/auth/new-feature"
```

**When deprecating old feature:**
```bash
bash .claude/skills/master-index-updater/execute.sh \
  deprecate \
  "Old Feature Name" \
  "" \
  ""
```

---

## Usage Examples (Legacy - For Reference)

### From Librarian Agent (Automated)
```
After organizing feature documentation, I'll use the master-index-updater skill to add the feature to the index.
```

### Manual Addition
```bash
# Add new feature
bash .claude/skills/master-index-updater.md \
  add \
  "Streamlined Check-in Workflow" \
  "Events Domain" \
  "docs/functional-areas/events/new-work/2025-11-03-streamlined-checkin-workflow"
```

### Update Existing Feature
```bash
# Update feature timestamp
bash .claude/skills/master-index-updater.md \
  update \
  "Event Management" \
  "" \
  ""
```

### Deprecate Feature
```bash
# Mark feature as deprecated
bash .claude/skills/master-index-updater.md \
  deprecate \
  "Legacy Registration System" \
  "" \
  ""
```

## Domain Classification

### Core System
**Characteristics**:
- Foundational functionality
- Used across multiple features
- Authentication, users, profiles

**Examples**:
- Authentication & Authorization
- User Management
- Profile Management
- Role-Based Access Control

### Events Domain
**Characteristics**:
- Event lifecycle management
- Primary business functionality
- Classes, workshops, performances

**Examples**:
- Event Management
- Session Management
- Registration System
- Attendance Tracking

### Content & Community
**Characteristics**:
- Content management
- Community features
- Public-facing information

**Examples**:
- Teacher Bios
- Event Catalog
- Venue Management
- Member Directory

### Operations
**Characteristics**:
- Administrative features
- Backend operations
- Support functions

**Examples**:
- Safety & Reporting
- Payment Processing
- Communication System
- Analytics & Reporting

## Entry Template

```markdown
### Feature Name

**Domain**: [Core System | Events Domain | Content & Community | Operations]
**Status**: [✅ Active | ⚠️  Deprecated | 🔵 Planned | 🚧 In Progress]
**Owner**: WitchCityRope Team
**Last Updated**: YYYY-MM-DD

#### Documentation
- [Business Requirements](./path/to/business-requirements.md)
- [Functional Spec](./path/to/functional-spec.md)
- [Database Design](./path/to/database-design.md)
- [UI/UX Design](./path/to/ui-ux-design.md)
- [Implementation Notes](./path/to/implementation-notes.md)
- [Testing Notes](./path/to/testing-notes.md)

#### Key Files
- Feature Code: `/apps/web/src/features/feature-name/`
- API Endpoints: `/apps/api/Features/FeatureName/`
- Database: `/apps/api/Data/Entities/FeatureName.cs`
- Tests: `/tests/playwright/feature-name*.spec.ts`

#### Related Areas
- [Related Feature 1](#related-feature-1)
- [Related Feature 2](#related-feature-2)

#### Status Notes
- [Current status description]
- [Known issues or limitations]
- [Migration notes if deprecated]

---
```

## Integration with Librarian Agent

**Librarian is responsible for:**
- Creating new functional area folders
- Organizing documentation
- **Updating Master Index** (uses this skill)
- Maintaining navigation structure

**Workflow**:
1. Librarian organizes documentation
2. Librarian uses master-index-updater skill
3. Master Index updated with new feature
4. Documentation becomes discoverable

## Validation Rules

### Before Adding Entry
- [ ] Feature documentation exists
- [ ] Domain is correct (Core/Events/Content/Operations)
- [ ] No duplicate entries
- [ ] All documentation links valid
- [ ] Key files paths accurate

### After Adding Entry
- [ ] Entry appears in correct domain
- [ ] All links work
- [ ] Last Updated timestamp correct
- [ ] Navigation preserved
- [ ] Alphabetical order maintained (if applicable)

## Common Issues

### Issue: Wrong Domain Classification
**Problem**: Feature added to wrong domain
**Impact**: Confusing navigation
**Solution**: Move entry to correct domain, update related links

### Issue: Broken Documentation Links
**Problem**: Links point to non-existent files
**Impact**: Users can't find documentation
**Solution**: Validate links before adding, fix broken links

### Issue: Duplicate Entries
**Problem**: Feature added multiple times
**Impact**: Confusing navigation
**Solution**: Check for existing entry before adding

### Issue: Stale Entries
**Problem**: Deprecated features not marked
**Impact**: Users try to use old features
**Solution**: Regular audit, mark deprecated features

## Maintenance Tasks

### Weekly
- Validate all links work
- Check for new features without index entries
- Update timestamps for modified features

### Monthly
- Review deprecated features for removal
- Reorganize if domain structure changes
- Consolidate related features

### Quarterly
- Complete navigation audit
- Update domain definitions
- Archive truly obsolete features

## Output Format

```json
{
  "masterIndexUpdate": {
    "action": "add",
    "feature": "Streamlined Check-in Workflow",
    "domain": "Events Domain",
    "status": "Active",
    "timestamp": "2025-11-04",
    "documentation": [
      "business-requirements.md",
      "functional-spec.md",
      "database-design.md",
      "ui-ux-design.md"
    ],
    "location": "/docs/architecture/functional-area-master-index.md",
    "section": "## Events Domain",
    "backup": "/docs/architecture/functional-area-master-index.md.backup"
  },
  "nextSteps": [
    "Verify all documentation links work",
    "Add related area cross-references",
    "Update PROGRESS.md with new feature"
  ]
}
```

## Progressive Disclosure

**Initial Context**: Show action and feature name
**On Request**: Show full entry being added/updated
**On Completion**: Show location and backup path
**On Failure**: Show validation errors and required fixes

---

**Remember**: The Master Index is the entry point for all feature documentation. Without it, documentation is invisible. With it, every feature is discoverable, organized, and maintainable. This skill automates keeping it current.

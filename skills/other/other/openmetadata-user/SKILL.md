---
name: openmetadata-user
description: Use OpenMetadata UI for data discovery, governance, and collaboration. Use when searching for data assets, managing descriptions and ownership, creating glossary terms, setting up data contracts, or tracking data insights and KPIs.
---

# OpenMetadata User Guide

Guide for data producers and consumers using OpenMetadata UI for discovery, documentation, governance, and collaboration.

## When to Use This Skill

- Searching and discovering data assets
- Adding descriptions and documentation
- Managing ownership and tagging
- Creating and using glossary terms
- Setting up data contracts
- Tracking data insights and KPIs
- Navigating lineage visualizations
- Understanding version history

## This Skill Does NOT Cover

- Using SDKs/APIs programmatically (see `openmetadata-dev`)
- Administering users, roles, and policies (see `openmetadata-ops`)
- Data quality test creation and profiling (see `openmetadata-dq`)
- Contributing to OpenMetadata core (see `openmetadata-sdk-dev`)

---

## Data Discovery

### Search Features

Access search from any page via **Ctrl+K** (Windows) or **Cmd+K** (macOS).

**Searchable Asset Types:**
- Tables, Topics, Dashboards
- Pipelines, ML Models, Containers
- Glossaries, Tags

**Search Behavior:**
- Matches asset names and descriptions
- Searches nested elements (column names, chart names)
- Powers both quick search and advanced search

### Quick Filters

| Filter | Purpose |
|--------|---------|
| **Owner/Team** | Find assets by responsible party |
| **Tags** | Filter by classification |
| **Tier** | Filter by business importance |
| **Service** | Filter by data source |
| **Database/Schema** | Database-specific refinement |
| **Deleted** | Include soft-deleted assets |

### Sort Options

| Sort By | Description |
|---------|-------------|
| **Relevance** | Best match to search terms |
| **Last Updated** | Most recently modified |
| **Weekly Usage** | Most frequently accessed |

### Advanced Search

Use boolean operators and faceted queries:

```
name:orders AND owner:data-team AND tier:Tier1
```

**Supported Operators:**
- `AND`, `OR`, `NOT`
- Field-specific queries: `name:`, `owner:`, `tag:`
- Wildcards: `*orders*`

---

## Previewing Assets

Click any asset from search results to open the preview panel.

### Basic Information

All assets display:
- Source system
- Name and description
- Owner (user or team)
- Tier and usage metrics

### Type-Specific Preview

| Asset Type | Preview Shows |
|------------|---------------|
| **Tables** | Table type, query count, columns |
| **Topics** | Partitions, replication factor, retention, schema type |
| **ML Models** | Algorithm, target, server, dashboard |
| **Glossary Terms** | Reviewers, synonyms, children |
| **Dashboards** | URL, charts |
| **Pipelines** | URL, tasks |

### Additional Sections

- **Data Quality**: Tests passed/aborted/failed
- **Tags**: All associated classifications
- **Schema**: Column names, types, descriptions

---

## Asset Detail Page

### Top Information Bar

- Source, Owner, Tier, Type, Usage
- Description (editable)

### Action Icons (Top Right)

| Icon | Function |
|------|----------|
| Circle with number | Open tasks count |
| Clock | Version history |
| Star | Follow/unfollow asset |
| Share | Copy asset link |
| ⋮ Menu | Announcements, rename, delete |

### Tabs by Asset Type

| Tab | Available For | Content |
|-----|---------------|---------|
| **Schema** | Tables, Topics, Containers | Columns, types, tags, frequently joined |
| **Activity Feeds** | All | Tasks, mentions, conversations |
| **Sample Data** | Tables, Topics | Ingested sample rows |
| **Queries** | Tables | SQL queries with execution times |
| **Data Observability** | Tables | Profiler metrics, quality tests |
| **Lineage** | All | Upstream/downstream visualization |
| **Custom Properties** | All | Organization-specific metadata |
| **Details** | Dashboards, ML Models | Charts, hyperparameters |
| **Executions** | Pipelines | Run history with status |

---

## Adding Descriptions

### Edit Description

1. Navigate to asset from Explore page
2. Click pencil icon to enter edit mode
3. Use toolbar for formatting
4. Preview changes before saving

### Markdown Formatting

Use the toolbar for:
- Headers (H1-H6)
- **Bold**, *italics*, ~~strikethrough~~
- Bulleted and numbered lists
- Hyperlinks
- Code blocks and inline code
- Block quotes

> **Note**: Legacy markdown syntax is not supported. Use the toolbar.

### Request Description

When you don't have edit permissions:
1. Click "Request Description"
2. Provide suggested text
3. Owner receives notification
4. Track request in Activity Feeds

### Column Descriptions

Tables support column-level documentation:
1. Navigate to Schema tab
2. Click column description field
3. Add context about the column's purpose

---

## Ownership and Following

### Assign Owner

1. Click owner field on asset page
2. Search for user or team
3. Select to assign ownership

**Owner Types:**
- **User**: Individual person
- **Team**: Group (only Group-type teams can own assets)

### Change Owner

1. Click existing owner
2. Search for new owner
3. Confirm change

### Follow Assets

Click the star icon to follow an asset:
- Receive notifications on changes
- Track in your activity feed
- Quick access from your profile

---

## Tags and Classification

### Tag Types

| Type | Description |
|------|-------------|
| **Classification Tags** | User-defined categories |
| **System Tags** | Built-in platform tags |
| **Mutually Exclusive** | Only one can apply at a time |
| **Tiers** | Business importance levels |

### Adding Tags

1. Navigate to asset
2. Click "+ Add Tag" in tags section
3. Search and select tags
4. Tags apply immediately

### Tiers

Standard tier levels:

| Tier | Description |
|------|-------------|
| **Tier1** | Critical business data |
| **Tier2** | Important operational data |
| **Tier3** | Standard business data |
| **Tier4** | Low-priority/experimental data |
| **Tier5** | Deprecated or archive data |

### Auto-Classification (PII)

OpenMetadata can automatically detect PII:
- Scans column names and sample data
- Suggests or auto-applies PII tags
- Configurable confidence thresholds

---

## Business Glossary

### Glossary Structure

```
Glossary
├── Parent Term
│   ├── Child Term
│   └── Child Term
└── Parent Term
    └── Child Term
```

**Fully Qualified Name Format:** `glossary.parentTerm.childTerm`

### Creating Glossary Terms

1. Navigate to **Govern → Glossary**
2. Click **+ Add Term**
3. Fill in:
   - Name and display name
   - Description
   - Synonyms
   - Related terms
   - Tags
4. Optionally assign reviewers

### Term Enrichment

| Field | Purpose |
|-------|---------|
| **Synonyms** | Alternative names |
| **Related Terms** | Connected concepts |
| **References** | External documentation links |
| **Reviewers** | Approval workflow |

### Applying Glossary Terms

1. Navigate to data asset
2. Click "+ Add Glossary Term"
3. Search and select term
4. Term links asset to business concept

### Approval Workflows

For governed glossaries:
1. Create or modify term
2. Term enters "Draft" state
3. Reviewers receive notification
4. Approve or request changes
5. Term becomes "Approved"

---

## Data Contracts

Data contracts establish formal agreements between data producers and consumers.

### Contract Components

| Section | Purpose |
|---------|---------|
| **Contract Details** | Name, owner, description |
| **Terms of Service** | Usage guidelines, policies |
| **Schema** | Columns included in contract |
| **Security** | Classifications, access policies |
| **Semantics** | Business rules for attributes |
| **Quality Tests** | Data quality validations |
| **SLA** | Service level expectations |

### Creating a Contract

1. Navigate to table's detail page
2. Click **Contract → + Add Contract**
3. Configure each section:

**Terms of Service:**
- Click "+ New Node" to add terms
- Define acceptable usage
- Specify data handling policies

**Schema Selection:**
- Select specific columns or all columns
- Define expected types and constraints

**Security Configuration:**
- Assign classification labels (PII, Confidential)
- Define data consumers via policies
- Set row-level filters

**Semantics (Business Rules):**
- Service requirements
- Ownership requirements
- Tag and domain requirements

**Quality Tests:**
- Add data quality tests
- Define pass/fail thresholds

### SLA Configuration

| Field | Description |
|-------|-------------|
| **Refresh Frequency** | How often data updates |
| **Maximum Latency** | Acceptable delay |
| **Availability Time** | When data should be available |
| **Retention Period** | How long data is kept |
| **Refresh Timestamp Column** | Column indicating last update |

### Running Contracts

1. Complete contract configuration
2. Click **Run Now**
3. View results in contract details
4. Track execution history over time

---

## Data Insights

### Data Insights Dashboard

Navigate to **Insights** to access:
- Platform-wide metrics
- Data quality trends
- Ownership coverage
- Documentation progress

### Key Performance Indicators (KPIs)

#### Supported KPIs

| KPI | Measures |
|-----|----------|
| **Completed Description** | % of assets with descriptions |
| **Completed Ownership** | % of assets with owners |

#### Creating KPIs

1. Navigate to **Insights → Add KPI**
2. Choose chart type
3. Set display name
4. Select metric type (percentage or absolute)
5. Define target and deadline
6. Add description

#### Tracking Progress

KPIs display:
- Current coverage percentage
- Days remaining to goal
- Daily progress line graph
- Trajectory toward completion

### Tiering Analysis

View distribution of assets across tiers:
- Identify critical data (Tier1)
- Find untiered assets
- Track tiering coverage over time

### Reports

**Available Reports:**
- Description coverage by service
- Ownership coverage by team
- Tier distribution
- Data quality trends

**Email Distribution:**
- Schedule weekly/monthly reports
- Configure recipients
- Include specific metrics

---

## Lineage Visualization

### Lineage View Elements

| Element | Description |
|---------|-------------|
| **Source Node** | Parent table (left side) |
| **Target Node** | Destination table (right side) |
| **Edge** | Arrow showing data flow |

### Navigation

1. Navigate to asset's **Lineage** tab
2. View upstream (sources) and downstream (targets)
3. Click nodes to see asset details
4. Click edges to see transformation SQL

### Configuration Options

Access **Lineage Config** to set:
- Upstream depth (1-3 levels)
- Downstream depth (1-3 levels)
- Nodes per layer

### Lineage Layers

| Layer | Shows |
|-------|-------|
| **Column** | Field-level transformations |
| **Observability** | Data quality test results |
| **Service** | Cross-platform flows |
| **Domain** | Business category organization |
| **Data Product** | Curated outputs |

### Node Details

Clicking a node shows:
- Owner and tier
- Data quality metrics
- Associated tags
- Schema preview
- Query count (for tables)

---

## Version History

### Version Numbering

OpenMetadata uses **major.minor** versioning:

| Change Type | Version Increment | Example |
|-------------|-------------------|---------|
| **Minor** (backward compatible) | +0.1 | 0.1 → 0.2 |
| **Major** (breaking change) | +1.0 | 0.2 → 1.2 |

### Minor Changes (Backward Compatible)

- Description updates
- Tag additions/removals
- Ownership changes
- Custom property updates

### Major Changes (Breaking)

- Column deletions
- Column type changes
- Schema restructuring

### Viewing History

1. Click clock icon on asset page
2. View list of versions
3. See who made changes
4. Compare versions
5. Review change details

### Governance Benefits

- Debug issues by reviewing recent changes
- Track who modified what and when
- Identify metadata changes causing problems
- Support compliance and audit requirements

---

## Announcements

### Creating Announcements

1. Click ⋮ menu on asset page
2. Select **Announcements**
3. Click **+ Add Announcement**
4. Fill in:
   - Title
   - Start and end date
   - Description

### Announcement Visibility

- Appears on asset detail page
- Shows in activity feeds
- Visible to all asset followers
- Time-bounded display

### Use Cases

- Planned maintenance windows
- Schema migration notices
- Deprecation warnings
- Feature announcements

---

## Collaboration Features

### Activity Feeds

View all activity on assets:
- Description changes
- Tag updates
- Ownership changes
- Task creation
- Conversations

### Tasks

Create tasks for:
- Description requests
- Tag requests
- Ownership changes
- Data quality issues

### Conversations

Start threaded discussions:
1. Click activity feeds tab
2. Add comment or reply
3. @mention users for notifications
4. Resolve completed discussions

### Following

Track assets you care about:
- Click star to follow
- Receive change notifications
- View in your profile

---

## Best Practices

### Documentation

1. **Be specific** - Describe what the data represents
2. **Include examples** - Show sample values when helpful
3. **Note caveats** - Document known issues or limitations
4. **Keep updated** - Review descriptions quarterly

### Tagging

1. **Use standard tags** - Follow organizational taxonomy
2. **Apply tiers** - Indicate business importance
3. **Tag consistently** - Same data, same tags
4. **Don't over-tag** - Keep tags meaningful

### Ownership

1. **Assign owners early** - During ingestion if possible
2. **Use teams** - Better than individual users
3. **Review regularly** - Update when people change roles
4. **Document expectations** - What ownership means

### Glossary

1. **Start small** - Core terms first
2. **Get buy-in** - Involve business stakeholders
3. **Use approval workflows** - For governed terms
4. **Link to assets** - Make terms discoverable

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Ctrl/Cmd + K** | Open search |
| **Escape** | Close modals |
| **Enter** | Confirm selection |

---

## References

- [Data Discovery Guide](https://docs.open-metadata.org/latest/how-to-guides/data-discovery)
- [Data Governance](https://docs.open-metadata.org/latest/how-to-guides/data-governance)
- [Data Contracts](https://docs.open-metadata.org/latest/how-to-guides/data-contracts)
- [Data Insights](https://docs.open-metadata.org/latest/how-to-guides/data-insights)
- [Guide for Data Users](https://docs.open-metadata.org/latest/how-to-guides/guide-for-data-users)
- `openmetadata-dev` - Using SDKs/APIs programmatically
- `openmetadata-ops` - Administering OpenMetadata
- `openmetadata-dq` - Data quality and observability

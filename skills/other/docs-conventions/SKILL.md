---
name: docs-conventions
description: Writing standards, React components, and MDX patterns for docs.cloudposse.com. Use when creating or editing documentation content.
---

# Documentation Conventions

Standards and patterns for writing documentation on docs.cloudposse.com.

## MDX Frontmatter

Every MDX file requires frontmatter:

```mdx
---
title: "Human-Readable Title"
sidebar_label: "Action-Oriented Label"
sidebar_class_name: hidden          # Optional: hide from sidebar
description: Brief description for SEO and previews
---
```

### Sidebar Labels

**IMPORTANT: Sidebar labels should be action-oriented verbs.**

| Good | Bad |
|------|-----|
| `Configure Atmos Auth` | `Atmos Auth` |
| `Deploy Roles` | `IAM Roles` |
| `Login to AWS` | `AWS Login` |
| `Setup Identity Center` | `Identity Center` |
| `Understand Identity` | `Identity Overview` |

Use verbs like: Configure, Deploy, Setup, Create, Manage, Understand, Review, Migrate

## Available React Components

Import components from `@site/src/components/`:

### Steps Component

**IMPORTANT: Always wrap lists and numbered items with the `<Steps>` component.**

For compact lists (preferred for simple items):

```mdx
import Steps from '@site/src/components/Steps';

<Steps>
  1. **First item** — Description of first item
  1. **Second item** — Description of second item
  1. **Third item** — Description of third item
</Steps>
```

For detailed step-by-step instructions with more content:

```mdx
import Steps from '@site/src/components/Steps';
import Step from '@site/src/components/Step';
import StepNumber from '@site/src/components/StepNumber';

<Steps>
  <Step>
    ### <StepNumber/> First Step Title
    Step content here with code blocks, notes, etc.
  </Step>
  <Step>
    ### <StepNumber/> Second Step Title
    More content.
  </Step>
</Steps>
```

Use the compact format for simple lists and the detailed format when steps require code blocks or extensive explanation.

### ActionCard with CTAs

For callout boxes with action buttons:

```mdx
import ActionCard from '@site/src/components/ActionCard';
import PrimaryCTA from '@site/src/components/PrimaryCTA';
import SecondaryCTA from '@site/src/components/SecondaryCTA';

<ActionCard title="What's Next?">
  Description of the next action.
  <div>
    <PrimaryCTA to="/path/to/next/">Primary Action</PrimaryCTA>
    <SecondaryCTA to="/path/to/alt/">Alternative</SecondaryCTA>
  </div>
</ActionCard>
```

### Next Steps Section (Required)

**IMPORTANT: All primary pages should end with a "Next Steps" section using ActionCard.**

The description should provide context by:
1. Acknowledging what was accomplished in the current page
2. Explaining why the next step is needed
3. Describing what the next page will cover

**Pattern:** "Now that [what was accomplished], [why the next step matters]. [What the next page covers]."

**Good examples:**

```mdx
## Next Steps

<ActionCard title="Centralize root access">
  Now that Identity Center and Permission Sets are provisioned, configure centralized root access management. This allows secure, auditable root operations on member accounts without maintaining root credentials.
  <PrimaryCTA to="/layers/identity/centralized-root-access/">Centralize Root Access</PrimaryCTA>
</ActionCard>
```

```mdx
## Next Steps

<ActionCard title="Deploy IAM roles">
  With Permission Sets available for human access, configure IAM roles for machine users. These roles enable GitHub Actions and other CI/CD systems to authenticate via OIDC.
  <PrimaryCTA to="/layers/identity/deploy/">Deploy IAM Roles</PrimaryCTA>
</ActionCard>
```

```mdx
## Next Steps

<ActionCard title="Configure authentication">
  With IAM roles deployed for machine users, configure Atmos Auth to map Permission Sets to user profiles. This enables seamless CLI authentication for your team.
  <PrimaryCTA to="/layers/identity/atmos-auth/">Configure Atmos Auth</PrimaryCTA>
</ActionCard>
```

**Bad examples (too generic):**

```mdx
{/* ❌ Too generic - doesn't explain context */}
<ActionCard title="Configure authentication">
  Learn how to configure Atmos Auth.
  <PrimaryCTA to="/layers/identity/atmos-auth/">Configure Atmos Auth</PrimaryCTA>
</ActionCard>
```

For multiple next steps, use `<div>` to wrap CTAs:

```mdx
## Next Steps

<ActionCard title="Setup Identity Center">
  Start by configuring AWS Identity Center with your IdP and deploying Permission Sets for your team.
  <div>
    <PrimaryCTA to="/layers/identity/aws-sso/">Setup Identity Center</PrimaryCTA>
    <SecondaryCTA to="/layers/identity/how-to-log-into-aws/">How to Log into AWS</SecondaryCTA>
  </div>
</ActionCard>
```

### Definition Lists for Component Overviews

Use `<dl>/<dt>/<dd>` for listing infrastructure components with descriptions:

```mdx
<dl>
  <dt><code>s3-bucket/gitops</code></dt>
  <dd>
    Stores plan files generated during the planning phase and retrieved during apply.
    Created with the <a href="/components/library/aws/s3-bucket/"><code>s3-bucket</code></a> component.
  </dd>

  <dt><code>dynamodb/gitops</code></dt>
  <dd>
    Maps git SHAs to plan files, ensuring the correct plan is retrieved for each apply.
    Created with the <a href="/components/library/aws/dynamodb/"><code>dynamodb</code></a> component.
  </dd>
</dl>
```

**IMPORTANT:** Hyperlinks go on "Created with X component" text in `<dd>`, NOT on the component name in `<dt>`.

### Note Component vs Admonitions

Use `<Note>` for inline notes within sections (e.g., inside definition lists):

```mdx
import Note from '@site/src/components/Note';

<Note>
  These roles are deployed as part of the Identity layer.
</Note>

<Note title="Optional Title">
  Content with a title.
</Note>
```

Use `:::info` admonitions for standalone callouts:

```mdx
:::info Included with Reference Architecture
These workflows are already included with the reference architecture package.
:::
```

### CollapsibleText with CodeBlock

For wrapping long code blocks or workflow tabs:

```mdx
import CodeBlock from '@theme/CodeBlock';
import CollapsibleText from '@site/src/components/CollapsibleText';
import PartialWorkflow from '@site/examples/snippets/workflows/example.yaml';

<CollapsibleText type="medium">
  <CodeBlock title="example.yaml">{PartialWorkflow}</CodeBlock>
</CollapsibleText>
```

`type="medium"` sets the collapsed height. Reference: `docs/layers/project/toolbox.mdx:42-48`

### KeyPoints with TaskList (Prerequisites)

For "Before You Begin" sections, place KeyPoints BEFORE Steps:

```mdx
import KeyPoints from '@site/src/components/KeyPoints';
import TaskList from '@site/src/components/TaskList';

<KeyPoints title="Before You Begin">
  <TaskList>
    - [x] State Backend configured
    - [x] OIDC Integration deployed
    - [ ] Plan File Storage pending
  </TaskList>
</KeyPoints>
```

### Troubleshooting Sections

Use H3 headers for each issue and TaskList for diagnostic steps:

```mdx
## Troubleshooting

### No instances appearing

<TaskList>
- Verify the workflow is running successfully
- Check that environment variables are set
- Ensure IAM role has required permissions
</TaskList>

### Remediation failing

<TaskList>
- Verify workflow configuration matches apply workflow
- Check GitHub environments are properly configured
- Review GitHub Actions logs for specific errors
</TaskList>
```

### Workflow Summary Tables

Standard format for listing multiple workflows:

```mdx
| Workflow | Purpose | Trigger | Frequency |
|----------|---------|---------|-----------|
| `list-instances` | Register components with Atmos Pro | Schedule | Nightly |
| `detect-drift` | Run terraform plan on each instance | Schedule | Weekly |
| `remediate` | Apply fixes for drifted components | Manual | On-demand |
```

### Other Components

| Component | Use Case |
|-----------|----------|
| `Card` / `CardGroup` | Grid of linked cards |
| `Note` | Inline highlighted notes (use within sections) |
| `Terminal` | Terminal output display |
| `File` | File content display |
| `CollapsibleText` | Expandable sections for long content |
| `AtmosWorkflow` | Atmos workflow display |
| `TaskList` | Checkbox task lists |
| `KeyPoints` | Key takeaways / prerequisites |
| `PillBox` | Tag/label pills |

## Docusaurus Admonitions

Use built-in admonitions for callouts:

```mdx
:::note
Informational note.
:::

:::tip
Helpful tip.
:::

:::info
General information.
:::

:::warning
Warning about potential issues.
:::

:::danger
Critical warning - data loss, security, etc.
:::
```

## Deprecation Pattern

When deprecating content, add admonition at the top (do NOT move files):

```mdx
:::warning Deprecated
This documentation describes the legacy approach using `[old thing]`.

**The recommended approach now uses:**
- [New Thing A](/path/to/new-a) for X
- [New Thing B](/path/to/new-b) for Y

This content is preserved for users with existing deployments.
:::
```

## Code Blocks

### Basic

```mdx
```bash
atmos terraform apply vpc -s plat-ue1-dev
​```
```

### With Title

```mdx
```hcl title="components/terraform/vpc/main.tf"
module "vpc" {
  source = "..."
}
​```
```

### With Line Highlighting

```mdx
```hcl {2-4}
variable "enabled" {
  type        = bool
  default     = true
  description = "Whether to create resources"
}
​```
```

## Mermaid Diagrams

Mermaid is enabled for diagrams. Use `flowchart LR` for left-to-right diagrams:

```mdx
```mermaid
flowchart LR
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[End]
​```
```

### Architecture Diagrams

For infrastructure flows, use descriptive node labels:

```mdx
```mermaid
flowchart LR
    subgraph "GitHub Actions"
        PR["Pull Request"] --> Plan["Terraform Plan"]
        Plan --> Apply["Terraform Apply"]
    end

    subgraph "Atmos Pro"
        Plan --> Upload["Upload Plan"]
        Upload --> Store["S3 Storage"]
    end

    style PR fill:#9b59b6,color:#fff
    style Plan fill:#3578e5,color:#fff
    style Apply fill:#28a745,color:#fff
​```
```

See `docs-styles/SKILL.md` for color conventions.

## Video Embeds

```mdx
import ReactPlayer from "react-player";

<figure>
  <ReactPlayer controls url="https://docs.cloudposse.com/assets/..." />
  <figcaption>Video caption</figcaption>
</figure>
```

## Internal Links

Use absolute paths from site root:

```mdx
[Link Text](/layers/identity/how-to-log-into-aws/)
```

## TODO Comments for Tracking

Track documentation updates with structured comments:

```mdx
{/* TODO:PROJECT-NAME - ACTION - Status: Not Started|In Progress|Done */}
{/*
## Required Updates:
- Update item 1
- Update item 2
*/}
```

## Writing Style

- **Be concise**: Short sentences, clear language
- **Use active voice**: "Deploy the component" not "The component should be deployed"
- **Lead with the action**: Put commands and code first, explanations after
- **Use consistent terminology**: Follow Cloud Posse naming conventions
- **Avoid jargon**: Define terms on first use or link to glossary

## File Naming

- Use kebab-case: `how-to-deploy-vpc.mdx`
- Layer pages: `{layer-name}.mdx` (e.g., `identity.mdx`)
- Tutorials: `how-to-*.mdx`
- Design decisions: `design-decisions/*.mdx`

## Sidebar Ordering

Control page order within a category using `sidebar_position` in frontmatter:

```yaml
---
title: "Setup Atmos Pro"
sidebar_label: "Setup Atmos Pro"
sidebar_position: 1
---
```

Pages are ordered by `sidebar_position` value (1, 2, 3, etc.). Pages without `sidebar_position` appear after numbered pages in alphabetical order.

**Recommended order pattern:**
1. Main setup/deploy pages
2. Feature configuration pages
3. Tutorials subfolder (autogenerated)

### sidebar_label vs title

Use short `sidebar_label` for navigation, longer `title` for page header:

```yaml
---
title: "Deploy Plan File Storage with Atmos and Terraform"
sidebar_label: "Deploy Plan Storage"
sidebar_position: 2
---
```

## Reference Architecture Naming Conventions

### Tenant Names

| Tenant | Purpose |
|--------|---------|
| `core` | Shared infrastructure (network, automation, identity) |
| `plat` | Platform/application workloads |

### Stage Names

| Stage | Purpose | Example Stack |
|-------|---------|---------------|
| `network` | Network hub account | `core-use1-network` |
| `auto` | Automation/CI account | `core-use1-auto` |
| `dev` | Development environment | `plat-use1-dev` |
| `staging` | Staging environment | `plat-use1-staging` |
| `prod` | Production environment | `plat-use1-prod` |
| `sandbox` | Sandbox/experimentation | `plat-use1-sandbox` |

### Stack Naming Pattern

```
{tenant}-{region}-{stage}
```

Examples:
- `core-use1-network` — Network account in us-east-1
- `core-use2-auto` — Automation account in us-east-2
- `plat-use1-dev` — Dev environment in us-east-1
- `plat-use1-prod` — Production in us-east-1

### Component Library URLs

Link to components using path-style URLs:

```mdx
[`vpc`](/components/library/aws/vpc/)
[`tgw/hub`](/components/library/aws/tgw/hub/)
[`iam-role`](/components/library/aws/iam-role/)
```

## YAML Configuration Patterns

### YAML Anchors for DRY Configs

Use anchors to avoid repetition in workflow configurations:

```yaml
workflows:
  detect: &detect-config
    file: atmos-pro-terraform-detect.yaml
    inputs:
      upload_status: "true"

  remediate:
    <<: *detect-config
    file: atmos-pro-terraform-remediate.yaml
```

### Terraform State References

Use `!terraform.state` for cross-component references:

```yaml
vars:
  table_arn: !terraform.state gitops/dynamodb core-use2-auto table_arn
  bucket_arn: !terraform.state gitops/s3-bucket core-use2-auto bucket_arn
```

**Note:** Use `!terraform.state`, NOT `!terraform.output`.

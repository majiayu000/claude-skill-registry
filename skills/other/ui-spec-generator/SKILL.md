---
name: ui-spec-generator
description: |
  Generate and maintain structured UI specification files (pages.yaml) from design resources and test cases.
  Use when: (1) "生成 UI 设计描述文件" (2) "检查测试用例覆盖的 UI 组件" (3) "生成 UI 组件清单"
  (4) "为新测试用例添加缺失页面" (5) Need to analyze gaps between test cases and existing UI components.
  Reads from specs/design/ (.pen files, images, pages.md) and specs/testcases/*.md, outputs to specs/design/pages.yaml.
---

# UI Spec Generator

Generate structured page-component-function hierarchy from design resources and test cases.

## Prerequisites

### MCP Servers Required
- **Pencil MCP**: Read `.pen` design files via `mcp__pencil__*` tools
- **Figma MCP**: Read Figma designs (configured in `.claude/mcp.json`)

### Input Resources
| Resource | Path | Purpose |
|----------|------|---------|
| Style spec | `specs/design/style.pen`, `basic.pen` | Design tokens and style rules |
| Components | `specs/design/components/*.pen` | Existing component designs |
| Screenshots | `specs/design/assets/images/*.png` | Visual/layout reference |
| Page index | `specs/design/pages.md` | Page-to-resource mapping with Figma links |
| Test cases | `specs/testcases/*.md` | Functional requirements |

## Workflow

### Step 1: Gather Design Context
1. Read `specs/design/style.pen` to understand design tokens (colors, fonts, spacing)
2. Read `specs/design/pages.md` to get page list and Figma URLs
3. Use Figma MCP to fetch component structure from Figma links
4. Read existing `.pen` files in `specs/design/components/` to catalog current components

### Step 2: Analyze Test Cases
1. Read all files in `specs/testcases/*.md`
2. Extract implicit UI requirements from test case descriptions:
   - What data needs to be displayed?
   - What user actions are described?
   - What state changes occur?
3. Map requirements to pages and components

### Step 3: Gap Analysis
Compare test case requirements against existing components:
- **Covered**: Test case UI needs are met by existing components
- **Extendable**: Existing component can be modified (see [component-reuse-criteria.md](references/component-reuse-criteria.md))
- **Missing**: New component needed

### Step 4: Design Missing Components
For gaps identified:
1. Reference the corresponding screenshot in `specs/design/assets/images/`
2. Use Figma MCP to get detailed component structure if Figma link exists
3. Follow existing design patterns from `style.pen`
4. Prefer extending existing components over creating new ones

### Step 5: Generate pages.yaml
Output to `specs/design/pages.yaml` following the format in [output-format.md](references/output-format.md).

Structure:
```yaml
pages:
  - id: page-id
    name: 页面名称
    route: /path
    sections:
      - id: section-id
        name: 区块名称
        components:
          - id: component-id
            name: 组件名称
            type: card|list-item|button|...
            data_source: post|category|user|...
            fields: [field1, field2]
            actions: [action1, action2]
```

## Using Figma MCP

Extract Figma file key and node ID from URLs in `pages.md`:
```
https://www.figma.com/design/{file_key}/...?node-id={node_id}
```

Use Figma MCP tools to:
1. Get file structure and component hierarchy
2. Identify grouped elements (frames, groups)
3. Extract component names and relationships

## Component Reuse Decision

Before creating new components, check [references/component-reuse-criteria.md](references/component-reuse-criteria.md):
1. Visual similarity with existing components
2. Functional compatibility
3. Non-breaking extension possibility

## Data Type References

When specifying `data_source`, use types from `specs/data/types.md`:
- `category` - 活动/赛事
- `post` - 帖子/提案
- `user` - 用户
- `group` - 团队
- `resource` - 资源文件
- `rule` - 规则
- `interaction` - 互动

## Output Validation

After generating `pages.yaml`:
1. Verify all pages from `pages.md` are included
2. Verify test case UI requirements are addressed
3. Confirm component reuse is maximized
4. Check YAML syntax validity

---
name: ai-ui-generator
description: |
  Generate UI/UX specifications from user journeys when no Figma design exists.
  Uses Claude + shadcn/ui to create pages.yaml and UX specs from requirements.

  Use when:
  (1) "生成 UI 设计" or "generate UI design" (without Figma)
  (2) "从用户旅程生成界面" or "generate UI from user journeys"
  (3) "无 Figma 设计时" or "when no Figma design available"
  (4) Project has no specs/design/figma/ directory
  (5) Need to create pages.yaml from scratch

  Inputs: docs/user-journeys/*.md, specs/testcases/*.md, design system
  Outputs: specs/design/pages.yaml, specs/ux/
---

# AI UI Generator

Generate structured UI/UX specifications from user journeys and requirements when no Figma design is available.

## When to Use

This skill is the **"Branch B"** in the frontend development workflow:

```
Phase 4: UI/UX 设计检测
├── 分支 A (有 Figma): figma-resource-extractor → ui-spec-generator
└── 分支 B (无 Figma): ai-ui-generator  ← THIS SKILL
```

**Automatic Detection**: Use this skill if:
- `specs/design/figma/` does NOT exist, OR
- User explicitly requests "无 Figma 设计" / "no Figma design"

## Workflow

### Phase 1: Gather Requirements

#### 1.1 Read User Journeys

```bash
# Read all user journey documents
ls docs/user-journeys/*.md
```

Parse each journey file to extract:
- **Pages needed**: What screens/views are required
- **Components needed**: What UI elements appear
- **Actions**: What user interactions occur
- **Data displayed**: What information is shown

#### 1.2 Read Test Cases

```bash
# Read test cases for UI requirements
ls specs/testcases/*.md
```

Extract from test cases:
- **Form fields**: What inputs are needed
- **Validation rules**: What constraints exist
- **Success/error states**: What feedback is shown
- **Permissions**: What role-specific UI exists

#### 1.3 Read Design System

Reference the Neon Forge design system:
- `specs/ui/style.pen` or `specs/design/` - Design tokens
- `frontend/tailwind.config.ts` - Theme configuration

### Phase 2: Generate Page Specifications

For each page identified, create a specification in `specs/design/pages.yaml`.

#### 2.1 Page Structure Template

```yaml
pages:
  - id: page-id
    name: 页面名称
    route: /path
    description: 页面功能描述
    source: "Generated from {user-journey-file}"

    sections:
      - id: section-id
        name: 区块名称
        layout: grid | flex | stack

        components:
          - id: component-id
            name: 组件名称
            type: card | list | form | button | ...
            shadcn_component: Card | Table | Form | Button | ...
            data_source: post | category | user | ...
            fields:
              - field_name
            actions:
              - action_name
```

#### 2.2 Component Mapping

Use shadcn MCP to find appropriate components:

```
# Search for matching components
mcp__shadcn__search_items_in_registries(
  registries: ["@shadcn"],
  query: "card"
)

# Get component details
mcp__shadcn__view_items_in_registries(
  items: ["@shadcn/card"]
)
```

Map user journey actions to shadcn/ui components:

| User Action | Recommended Component |
|-------------|----------------------|
| View list | Table, DataTable, Card grid |
| View details | Card, Sheet |
| Create/Edit | Form, Dialog |
| Submit | Button |
| Navigate | Link, NavigationMenu, Tabs |
| Select | Select, RadioGroup, Checkbox |
| Upload | Input (file), Dropzone |
| Search | Input + Command |
| Filter | Popover + Checkbox |
| Paginate | Pagination |
| Show feedback | Toast, Alert, AlertDialog |

#### 2.3 Layout Patterns

Reference [layout-patterns.md](references/layout-patterns.md) for common layouts:

| Pattern | Use Case |
|---------|----------|
| `header-sidebar-main` | Dashboard with navigation |
| `header-main-footer` | Public pages |
| `split-view` | List + detail panels |
| `wizard` | Multi-step forms |
| `grid-masonry` | Card galleries |

### Phase 3: Generate UX Specifications

For each page, create interaction specs in `specs/ux/pages/{page-id}.yaml`.

#### 3.1 UX Spec Structure

```yaml
# Page: {page-name}
route: "/{path}"
description: 页面交互说明

sections:
  {section-id}:
    components:
      {component-id}:
        interactions:
          - trigger: click | hover | focus | submit
            action: navigate | show_modal | call_api | update_state
            target: "{route}" | "{modal-id}" | "{api-endpoint}"
            params: { ... }

          - trigger: form_submit
            action: call_api
            api_call:
              method: POST
              endpoint: "/api/{resource}"
              body: "{form_data}"
            on_success:
              - action: show_toast
                message: "操作成功"
              - action: navigate
                target: "/{success-route}"
            on_error:
              - action: show_toast
                type: error
                message: "{error.message}"
```

#### 3.2 Interaction Patterns

Reference [interaction-patterns.md](references/interaction-patterns.md) for common patterns:

| Pattern | Description |
|---------|-------------|
| CRUD operations | Create → Toast → Navigate |
| List with filters | Filter change → URL update → Refetch |
| Infinite scroll | Scroll → Load more → Append |
| Optimistic update | Click → UI change → API → Rollback on error |
| Modal forms | Open → Fill → Submit → Close |

### Phase 4: Validate & Install Components

#### 4.1 List Required Components

After generating specs, compile the list of shadcn components needed:

```yaml
required_components:
  - Card
  - Button
  - Input
  - Form
  - Table
  - Dialog
  - Toast
```

#### 4.2 Generate Installation Commands

Use shadcn MCP to get installation commands:

```
mcp__shadcn__get_add_command_for_items(
  items: ["@shadcn/card", "@shadcn/button", "@shadcn/form"]
)
```

Output to `specs/design/component-install.sh`:
```bash
#!/bin/bash
npx shadcn@latest add card
npx shadcn@latest add button
npx shadcn@latest add form
# ...
```

### Phase 5: Output Files

Generate the following files:

| File | Content |
|------|---------|
| `specs/design/pages.yaml` | Page-component hierarchy |
| `specs/design/component-install.sh` | shadcn installation script |
| `specs/ux/README.md` | UX specs overview |
| `specs/ux/pages/{page}.yaml` | Per-page interaction specs |
| `specs/ux/flows/{flow}.yaml` | User flow specifications |
| `specs/ux/state/state-management.yaml` | Error/loading states |

---

## Design System Integration

### Neon Forge Theme Tokens

Apply these tokens in generated specs:

```yaml
theme:
  colors:
    primary: nf-lime (#BBFD3B)
    background: nf-dark (#181818)
    surface: nf-surface (#222222)
    secondary: nf-secondary (#333333)
    text: nf-white
    muted: nf-muted
    error: nf-error

  spacing:
    xs: 4px
    sm: 8px
    md: 16px
    lg: 24px
    xl: 32px

  radius:
    sm: 4px
    md: 8px
    lg: 12px
    xl: 21px
    pill: 50px
```

### Component Styling Conventions

All components should follow:

1. **Dark theme by default** - Use `bg-nf-surface`, `text-nf-white`
2. **Lime accent** - Primary actions use `bg-nf-lime text-nf-near-black`
3. **Border styling** - Use `border-nf-secondary`
4. **Hover states** - Use `hover:bg-nf-secondary` or `hover:text-nf-lime`

---

## Example: Generating from User Journey

### Input: User Journey (J-003 发帖子)

```markdown
# J-003: 用户发帖子

## 前置条件
- 用户已登录

## 流程
1. 用户点击"发布"按钮
2. 系统显示发帖表单
3. 用户填写标题、内容、标签
4. 用户点击"提交"
5. 系统验证内容
6. 系统创建帖子
7. 系统跳转到帖子详情页
```

### Output: pages.yaml

```yaml
pages:
  - id: post-create
    name: 发布帖子
    route: /posts/create
    source: "Generated from docs/user-journeys/j003-create-post.md"

    sections:
      - id: form-section
        name: 帖子表单
        layout: stack

        components:
          - id: post-form
            name: 帖子表单
            type: form
            shadcn_component: Form
            fields:
              - name: title
                type: text
                required: true
                label: 标题
              - name: content
                type: markdown
                required: true
                label: 内容
              - name: tags
                type: tag-input
                required: false
                label: 标签
            actions:
              - id: submit
                type: submit
                label: 发布
                api_call: POST /api/posts
```

### Output: specs/ux/pages/post-create.yaml

```yaml
route: "/posts/create"
description: 发布新帖子

sections:
  form-section:
    components:
      post-form:
        interactions:
          - trigger: submit
            action: call_api
            api_call:
              method: POST
              endpoint: "/api/posts"
              body: "{form_data}"
            loading_state: submit-button
            on_success:
              - action: show_toast
                message: "发布成功"
              - action: navigate
                target: "/posts/{new_post.id}"
            on_error:
              - action: show_form_errors
```

---

## Integration with Other Skills

### Upstream Dependencies

| Skill | Output Used |
|-------|-------------|
| `domain-modeler` | Data types and relationships |
| `journey-validator` | Validated user journeys |

### Downstream Consumers

| Skill | Input From This Skill |
|-------|----------------------|
| `frontend-prototype-builder` | pages.yaml, UX specs |
| `openapi-to-components` | Component structure |

---

## Troubleshooting

### No User Journeys Found

```
Error: docs/user-journeys/ is empty
```

Solution: Create user journey documents first using the requirements.

### Component Not Found in shadcn

If a required component doesn't exist in shadcn/ui:
1. Check Magic UI MCP for animated alternatives
2. Create custom component based on shadcn primitives
3. Document in `specs/design/custom-components.md`

### Conflicting Requirements

If test cases and user journeys conflict:
1. Prioritize test cases (they define expected behavior)
2. Flag conflicts in `specs/design/pages.yaml` with comments
3. Ask user for clarification

---

## References

- [component-catalog.md](references/component-catalog.md) - Available shadcn components
- [layout-patterns.md](references/layout-patterns.md) - Common layout patterns
- [interaction-patterns.md](references/interaction-patterns.md) - Interaction patterns
- [neon-forge-tokens.md](references/neon-forge-tokens.md) - Design system tokens

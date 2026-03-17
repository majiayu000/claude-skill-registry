---
name: ux-spec-generator
description: |
  Generate comprehensive UX interaction specifications from UI designs and test cases.
  Outputs to specs/ux/ directory with multi-file structure: overview README, reusable components, pages, flows, forms, and state management.

  Use when:
  (1) "生成 UX 交互规格" or "generate UX spec"
  (2) "创建用户交互文档" or "document user interactions"
  (3) "补充页面交互逻辑" or "add interaction logic for pages"
  (4) "生成组件交互规格" or "document component interactions"
  (5) Need to connect frontend components with backend APIs
  (6) Before implementing frontend event handlers or navigation

  Reads from: specs/design/pages.yaml, specs/design/*.pen, specs/testcases/*.md
  Writes to: specs/ux/ (multi-file structure with components/, pages/, flows/, forms/, state/)
---

# UX Spec Generator

Generate structured user interaction specifications that bridge UI design with frontend implementation.

## Output Structure

```
specs/ux/
├── README.md                    # 总览文档 (Overview)
├── global/                      # 全局交互
│   └── shared-components.yaml
├── components/                  # 可复用组件交互 (grouped by category)
│   ├── navigation/              # 导航类组件
│   │   ├── header.yaml
│   │   ├── sidebar.yaml
│   │   └── breadcrumb.yaml
│   ├── content/                 # 内容类组件
│   │   ├── post-card.yaml
│   │   ├── proposal-card.yaml
│   │   └── comment-item.yaml
│   ├── form/                    # 表单类组件
│   │   ├── text-input.yaml
│   │   ├── tag-input.yaml
│   │   └── markdown-editor.yaml
│   ├── feedback/                # 反馈类组件
│   │   ├── toast.yaml
│   │   ├── modal.yaml
│   │   └── loading.yaml
│   └── action/                  # 操作类组件
│       ├── like-button.yaml
│       ├── follow-button.yaml
│       └── share-button.yaml
├── pages/                       # 页面交互 (one file per page)
│   ├── home.yaml
│   ├── post-detail.yaml
│   └── ...
├── flows/                       # 用户流程 (grouped by category)
│   ├── content/                 # 内容类流程
│   │   ├── create-post.yaml
│   │   └── like-content.yaml
│   ├── team/                    # 团队类流程
│   │   └── join-team.yaml
│   ├── auth/                    # 认证类流程
│   └── social/                  # 社交类流程
├── forms/                       # 表单交互
│   └── post-create-form.yaml
└── state/                       # 状态管理
    └── state-management.yaml
```

## Workflow

### 1. Gather Source Materials

Read in parallel:
- `specs/design/pages.yaml` — Component structure, actions, data sources
- `specs/design/*.pen` — Detailed design via Pencil MCP tools
- `specs/testcases/*.md` — User journeys and expected behaviors

### 2. Determine Scope

**Default:** Generate specs for ALL pages in pages.yaml

**Selective:** If user specifies pages, generate only for those:
```
"生成 home 和 post-detail 页面的 UX spec"
→ Generate only for pages: [home, post-detail]
```

### 3. Generate UX Spec Files

Create the directory structure and write files:

1. **README.md** — Overview document with index and summary
2. **global/** — Shared component interactions
3. **components/** — Reusable component specs grouped by category
4. **pages/** — One YAML file per page
5. **flows/** — User journeys grouped by category
6. **forms/** — Form interaction specs
7. **state/** — State management and error handling

### 4. Report Completion

List generated files and any placeholders due to missing information.

---

## File Schemas

### README.md (Overview)

```markdown
# UX Interaction Specifications

Generated: {timestamp}
Version: 1.0

## Summary

| Category | Count | Status |
|----------|-------|--------|
| Components | 12 | ✅ Complete |
| Pages | 5 | ✅ Complete |
| Flows | 3 | ⚠️ 1 placeholder |
| Forms | 2 | ✅ Complete |

## Components

| Category | Components | Files |
|----------|------------|-------|
| Navigation | header, sidebar, breadcrumb | [components/navigation/](components/navigation/) |
| Content | post-card, proposal-card, comment-item | [components/content/](components/content/) |
| Form | text-input, tag-input, markdown-editor | [components/form/](components/form/) |
| Feedback | toast, modal, loading | [components/feedback/](components/feedback/) |
| Action | like-button, follow-button, share-button | [components/action/](components/action/) |

## Pages

| Page | Route | File |
|------|-------|------|
| Home | `/` | [pages/home.yaml](pages/home.yaml) |
| Post Detail | `/posts/{id}` | [pages/post-detail.yaml](pages/post-detail.yaml) |

## User Flows

### Content Flows
- [Create Post](flows/content/create-post.yaml) — 发布新帖子
- [Like Content](flows/content/like-content.yaml) — 点赞内容

### Team Flows
- [Join Team](flows/team/join-team.yaml) — 加入团队

## Placeholders (TODO)

- [ ] `pages/login.yaml` — Not designed
- [ ] `flows/auth/login.yaml` — Missing test cases
```

### components/{category}/{component-name}.yaml

Component categories:
- `navigation/` — 导航类：header, sidebar, breadcrumb, tabs, pagination
- `content/` — 内容类：post-card, proposal-card, comment-item, user-avatar
- `form/` — 表单类：text-input, tag-input, markdown-editor, file-upload
- `feedback/` — 反馈类：toast, modal, loading, skeleton, empty-state
- `action/` — 操作类：like-button, follow-button, share-button, bookmark-button

```yaml
# Component: Like Button
name: like-button
category: action
description: 点赞按钮，支持乐观更新

props:
  target_type:
    type: string
    enum: [post, comment, resource]
    required: true
  target_id:
    type: string
    required: true
  initial_count:
    type: number
    default: 0
  initial_liked:
    type: boolean
    default: false

states:
  default:
    icon: heart-outline
    color: text-secondary
  liked:
    icon: heart-filled
    color: accent-primary
  loading:
    icon: spinner
    disabled: true

interactions:
  - trigger: click
    condition: "!is_loading"
    action: toggle_like
    api_call:
      method: POST
      endpoint: "/api/interactions"
      body:
        type: like
        target_type: "{target_type}"
        target_id: "{target_id}"
    optimistic_update:
      - field: liked
        operation: toggle
      - field: count
        operation: "{liked ? decrement : increment}"
    error_rollback: true
    on_unauthenticated:
      action: show_modal
      target: login-prompt

  - trigger: hover
    action: show_tooltip
    content: "{liked ? '取消点赞' : '点赞'}"

accessibility:
  role: button
  aria-label: "{liked ? '取消点赞' : '点赞'}, 当前 {count} 人点赞"
  aria-pressed: "{liked}"
```

### global/shared-components.yaml

```yaml
# Global shared component interactions
version: "1.0"

shared_components:
  global-header:
    components:
      site-logo:
        interactions:
          - trigger: click
            action: navigate
            target: "/"

      search-bar:
        interactions:
          - trigger: focus
            action: expand
            target: self
          - trigger: submit
            action: navigate
            target: "/search?q={query}"

      publish-btn:
        interactions:
          - trigger: click
            action: toggle_panel
            target: multi-function-panel.publish-center

  sidebar-nav:
    components:
      nav-explore:
        interactions:
          - trigger: click
            action: navigate
            target: "/"
            active_indicator: true

  multi-function-panel:
    panels:
      publish-center:
        show_trigger: header-right.publish-btn
        components:
          find-teammate-card:
            interactions:
              - trigger: click
                action: navigate
                target: "/posts?tag=find-teammate"
```

### pages/{page-name}.yaml

```yaml
# Page: Home
route: "/"
description: 首页，展示热门提案和内容流

sections:
  main-tabs:
    components:
      tab-bar:
        interactions:
          - trigger: click
            action: filter_content
            params:
              tab: "{selected_tab}"
            api_call:
              method: GET
              endpoint: "/api/posts"
              query: "{tab.filter}"
            loading_state: main-content

  hot-proposals:
    components:
      proposal-card:
        interactions:
          - trigger: click
            action: navigate
            target: "/posts/{id}"
          - trigger: click
            target_element: like-btn
            action: toggle_like
            api_call:
              method: POST
              endpoint: "/api/interactions"
              body:
                type: like
                target_type: post
                target_id: "{id}"
            optimistic_update:
              field: like_count
              operation: increment
            error_rollback: true
```

### flows/{category}/{flow-name}.yaml

Flow categories:
- `content/` — 内容操作：create-post, edit-post, delete-post, like-content
- `team/` — 团队操作：join-team, create-team, invite-member
- `auth/` — 认证操作：login, logout, register
- `social/` — 社交操作：follow-user, comment, share

```yaml
# Flow: Create Post
name: 发布新帖子
category: content
description: 用户从首页发布新帖子的完整流程

trigger: click header-right.publish-btn
preconditions:
  - user.is_authenticated

steps:
  - step: 1
    page: home
    component: header-right.publish-btn
    trigger: click
    result:
      action: show_panel
      target: publish-center

  - step: 2
    page: home
    panel: publish-center
    component: find-teammate-card | find-idea-card | publish-proposal-card
    trigger: click
    result:
      action: navigate
      target: "/posts/create?type={selected_type}"

  - step: 3
    page: post-create
    component: post-form
    trigger: fill_form
    fields:
      - title (required)
      - body (required, markdown)
      - tags (optional)
      - cover_image (optional)
    validation:
      title: min_length: 1, max_length: 200
      body: min_length: 1

  - step: 4
    page: post-create
    component: submit-btn
    trigger: click
    api_call:
      method: POST
      endpoint: "/api/posts"
      body: "{form_data}"
    loading_state: submit-btn

  - step: 5a
    condition: success
    result:
      action: navigate
      target: "/posts/{new_post.id}"
      toast: "发布成功"

  - step: 5b
    condition: error
    result:
      action: show_error
      target: form
      message: "{error.message}"
```

### forms/{form-name}.yaml

```yaml
# Form: Post Create
route: "/posts/create"
description: 创建新帖子表单

fields:
  title:
    type: text
    required: true
    validation:
      min_length: 1
      max_length: 200
    interactions:
      - trigger: input
        action: validate_field
      - trigger: blur
        action: show_error_if_invalid

  body:
    type: markdown-editor
    required: true
    interactions:
      - trigger: input
        action: auto_save_draft
        debounce: 3000
      - trigger: paste_image
        action: upload_image
        api_call:
          method: POST
          endpoint: "/api/resources"
          body: FormData
        on_success:
          action: insert_image_markdown

  tags:
    type: tag-input
    interactions:
      - trigger: input
        action: search_suggestions
        api_call:
          method: GET
          endpoint: "/api/tags?q={query}"
      - trigger: select
        action: add_tag

submit:
  trigger: click submit-btn
  validation: validate_all_fields
  on_valid:
    api_call:
      method: POST
      endpoint: "/api/posts"
    loading_state: submit-btn
  on_invalid:
    action: scroll_to_first_error
```

### state/state-management.yaml

```yaml
# State Management
version: "1.0"

loading_indicators:
  - component: "*-btn"
    type: spinner
    disable_while_loading: true
  - component: "*-list"
    type: skeleton
  - component: page
    type: progress-bar

error_handling:
  network_error:
    action: show_toast
    type: error
    message: "网络连接失败，请重试"
    retry_button: true
  auth_required:
    action: show_modal
    target: login-prompt
  permission_denied:
    action: show_toast
    type: error
    message: "您没有权限执行此操作"
  not_found:
    action: navigate
    target: "/404"

placeholders:
  - page: login
    status: not_designed
    required_interactions:
      - email input validation
      - password input
      - submit form
      - OAuth buttons
```

---

## Interaction Types Reference

### Trigger Types
| Trigger | Description | Example |
|---------|-------------|---------|
| `click` | 单击元素 | 按钮、链接、卡片 |
| `double-click` | 双击元素 | 编辑模式切换 |
| `focus` | 获取焦点 | 输入框展开 |
| `blur` | 失去焦点 | 验证输入 |
| `input` | 输入内容 | 实时搜索、表单验证 |
| `submit` | 提交表单 | 表单提交 |
| `select` | 选择选项 | 下拉菜单、标签选择 |
| `file_selected` | 选择文件 | 图片/文件上传 |
| `paste_image` | 粘贴图片 | Markdown编辑器 |

### Action Types
| Action | Description | Params |
|--------|-------------|--------|
| `navigate` | 页面跳转 | target: URL |
| `show_panel` | 显示面板 | target: panel_id |
| `toggle_panel` | 切换面板 | target: panel_id |
| `show_modal` | 显示弹窗 | target: modal_id |
| `show_dropdown` | 显示下拉菜单 | options: [] |
| `show_confirm` | 显示确认对话框 | confirm_action: {} |
| `filter_content` | 筛选内容 | params: {} |
| `toggle_like` | 切换点赞 | api_call: {} |
| `submit_form` | 提交表单 | api_call: {} |
| `validate_field` | 验证字段 | - |
| `show_toast` | 显示提示 | message, type |
| `update_field` | 更新字段 | field, operation |
| `clear_input` | 清空输入 | - |
| `upload_file` | 上传文件 | api_call: {} |

### Conditions
```yaml
condition: user.is_authenticated    # 用户已登录
condition: is_author                # 当前用户是作者
condition: is_admin                 # 当前用户是管理员
condition: "!already_liked"         # 未点赞
condition: visibility=public        # 公开可见
condition: status=published         # 已发布状态
```

### API Call Structure
```yaml
api_call:
  method: POST | GET | PUT | DELETE
  endpoint: "/api/posts/{id}"
  body:                    # POST/PUT body
    type: like
    target_id: "{id}"
  query:                   # GET query params
    page: 1
    limit: 20
```

### Success/Error Handling
```yaml
on_success:
  - action: navigate
    target: "/posts/{id}"
  - action: show_toast
    message: "操作成功"
  - action: update_field
    field: like_count
    operation: increment

on_error:
  - action: show_toast
    type: error
    message: "{error.message}"
  - action: show_form_errors

on_unauthenticated:
  action: show_modal
  target: login-prompt
```

---

## Reading .pen Files

Use Pencil MCP tools to extract component details:

```
mcp__pencil__batch_get(
  filePath: "specs/design/basic.pen",
  patterns: [{ reusable: true }],
  readDepth: 2
)
```

Extract from .pen files:
- Component hierarchy and nesting
- Interactive elements (buttons, inputs, links)
- Style states (hover, active, disabled)
- Layout relationships

---

## Validation Checklist

Before completing, verify:

1. **README.md complete** — Overview lists all components, pages, flows, forms with links
2. **Components categorized** — Reusable components grouped by type in `components/{category}/`
3. **All pages covered** — Every page in pages.yaml has a corresponding file in `pages/`
4. **Flows categorized** — User flows grouped by type in appropriate subdirectories
5. **API endpoints defined** — Every data mutation has an api_call
6. **Error states handled** — Loading, success, and error states in `state/`
7. **Placeholders listed** — Missing items noted in README.md TODO section

---
name: figma-resource-extractor
description: |
  Extract and catalog Figma design resources into structured Markdown documentation.
  Outputs to specs/design/figma/ directory with categorized resource lists and Figma links.

  Use when:
  (1) "提取 Figma 资源" or "extract Figma resources"
  (2) "生成 Figma 文档" or "generate Figma docs"
  (3) "同步 Figma 设计" or "sync Figma design"
  (4) "更新设计资源列表" or "update design resource list"
  (5) Need to catalog Figma components, icons, pages for frontend development
  (6) Before implementing frontend pages from Figma designs
---

# Figma Resource Extractor

Extract Figma design resources and generate structured Markdown documentation for AI-assisted frontend development.

## Output Structure

```
specs/design/figma/
├── README.md              # Overview with resource index
├── icons.md               # Icon components list
├── components.md          # UI components list
├── layouts.md             # Responsive layout specs
├── assets.md              # Page-specific shared assets (切图区)
└── pages/                 # Page designs grouped by prefix
    ├── explore.md         # 探索-* pages
    ├── auth.md            # 登陆/注册/找回密码
    ├── team.md            # 团队 pages
    ├── profile.md         # 个人信息/他人主页
    ├── settings.md        # 设置 pages
    ├── message.md         # 消息/通知 pages
    ├── content.md         # 贴子/提案/评论
    ├── camp.md            # 营地 pages
    ├── planet.md          # 星球 pages
    ├── asset.md           # 资产 pages
    └── misc.md            # Other pages
```

## Workflow

### 1. Get Figma File Structure

```
mcp__figma__get_figma_data(fileKey, depth=1)
```

List all pages (CANVAS nodes) in the Figma file.

### 2. Get Target Page Children

```
mcp__figma__get_figma_data(fileKey, nodeId, depth=2)
```

For the target page (e.g., `🟧大赛-PC翻新`), get top-level children.

### 3. Classify Resources

Parse YAML response and classify by name/type:

| Category | Figma Name Pattern | Node Type |
|----------|-------------------|-----------|
| icons | `icon` | SECTION |
| components | `PC端组件` | FRAME |
| layouts | `W>*`, `*>W>*`, `*>W` | FRAME |
| assets | `切图区` | SECTION |
| pages | All other FRAME | FRAME |

### 4. Generate Link Format

Figma link format:
```
https://www.figma.com/design/{fileKey}?node-id={nodeId}
```

Node ID format conversion: `1234:5678` → `1234-5678` (replace `:` with `-`)

### 5. Group Pages by Prefix

| Prefix Pattern | Output File | Description |
|---------------|-------------|-------------|
| `探索-*` | pages/explore.md | Explore pages |
| `登陆`, `注册`, `找回密码`, `扫码*` | pages/auth.md | Authentication |
| `团队*`, `他人团队`, `*队*视角` | pages/team.md | Team pages |
| `个人信息`, `他人主页`, `编辑` | pages/profile.md | Profile pages |
| `设置*` | pages/settings.md | Settings |
| `消息`, `通知` | pages/message.md | Messaging |
| `贴子`, `提案`, `评论`, `发布`, `创建新内容` | pages/content.md | Content |
| `营地*` | pages/camp.md | Camp pages |
| `星球*` | pages/planet.md | Planet pages |
| `资产*` | pages/asset.md | Asset pages |
| `搜索*` | pages/search.md | Search pages |
| Others | pages/misc.md | Miscellaneous |

### 6. Write Documentation

Generate each file with this structure:

#### README.md
```markdown
# Figma Design Resources

Source: [Figma File Name](figma-link)
Generated: {timestamp}

## Resource Index

| Category | Count | File |
|----------|-------|------|
| Icons | {n} | [icons.md](icons.md) |
| Components | {n} | [components.md](components.md) |
| Layouts | {n} | [layouts.md](layouts.md) |
| Assets | {n} | [assets.md](assets.md) |

## Pages

| Category | Count | File |
|----------|-------|------|
| Explore | {n} | [pages/explore.md](pages/explore.md) |
...
```

#### Resource List Files (icons.md, components.md, etc.)
```markdown
# {Category Name}

Source: [{Section Name}](figma-link-to-section)

## Items

| Name | Type | Figma Link |
|------|------|------------|
| {name} | {type} | [Open]({link}) |
...
```

#### Page Files (pages/*.md)
```markdown
# {Category Name} Pages

## {Page Name}

- **ID**: {nodeId}
- **Type**: {type}
- **Link**: [Open in Figma]({link})

### Children (if available)
| Name | Type | Link |
|------|------|------|
...
```

## Figma Structure Reference

For SYN系列设计系统, target page `🟧大赛-PC翻新` (11166:6711):

| Resource | Node ID | Type |
|----------|---------|------|
| icon | 11170:8388 | SECTION |
| PC端组件 | 14302:55704 | FRAME |
| 切图区 | 15374:140683 | SECTION |
| W>1440 | 14392:17870 | FRAME |
| 1440>W>1340 | 15151:77748 | FRAME |
| 1340>W>1288 | 15151:77729 | FRAME |
| 1288>W>928 | 15151:77827 | FRAME |
| 928>W | 15151:77843 | FRAME |

## Usage Example

User: "提取 Figma 资源 https://www.figma.com/design/QUQsM2qOSwdYVoHVB1JpAw/SYN系列设计系统?node-id=11166-6711"

1. Parse fileKey: `QUQsM2qOSwdYVoHVB1JpAw`
2. Parse nodeId: `11166-6711` → `11166:6711`
3. Fetch data with `mcp__figma__get_figma_data`
4. Classify and generate docs to `specs/design/figma/`
5. Report summary with file counts

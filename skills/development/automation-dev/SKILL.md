---
name: automation-dev
description: 自动化开发技能。包含 Git 操作、MCP 工具集成、文档转换、代码打包、Skill 创建。适用于开发工作流自动化。
---

# 自动化开发技能 v2.0

> **更新日期**: 2026-01-23
> **版本**: v2.0.0
> **定位**: WinJin 项目的自动化工具和最佳实践

---

## 核心公式

```
自动化 = MCP工具 + Git操作 + 文档处理 + 代码打包

Git操作 = gh CLI + GitHub API

文档转换 = markitdown + 脚本辅助

代码打包 = repomix + 安全扫描
```

---

## MCP 工具集成 ⭐ 核心

### 7个核心工具

| 工具 | 功能 | 优先级 | 使用场景 |
|------|------|--------|----------|
| **Chrome DevTools** | 浏览器自动化 | ⭐⭐⭐⭐⭐ | 测试验证、UI调试、性能分析 |
| **Context7** | 文档查询 | ⭐⭐⭐⭐⭐ | 功能开发、查阅API、代码示例 |
| **Memory** | 知识图谱 | ⭐⭐⭐ | 跨会话记忆、知识管理 |
| **Z-Read** | GitHub 阅读 | ⭐⭐⭐⭐ | 代码阅读、开源项目研究 |
| **Web Search** | 网页搜索 | ⭐⭐⭐ | 资料查找、解决方案搜索 |
| **ZAI MCP** | 图像分析 | ⭐⭐⭐ | 图片/视频分析、UI转代码 |
| **Fetch** | HTTP 请求 | ⭐⭐⭐ | API测试、数据抓取 |

### 任务→工具映射

| 开发任务 | 推荐工具 | 优先级 | 使用示例 |
|---------|---------|--------|----------|
| **功能开发** | Context7 | ⭐⭐⭐⭐⭐ | `query-docs("/react", "useState hook")` |
| **API测试** | Chrome DevTools | ⭐⭐⭐⭐⭐ | `list_network_requests()` + `take_screenshot()` |
| **代码调试** | Chrome DevTools | ⭐⭐⭐⭐⭐ | `list_console_messages()` + `evaluate_script()` |
| **资料查找** | Web Search | ⭐⭐⭐⭐ | `webSearchPrime("React Flow 2026 docs")` |
| **跨会话记忆** | Memory | ⭐⭐⭐ | `create_entities()` + `search_nodes()` |
| **GitHub阅读** | Z-Read | ⭐⭐⭐⭐ | `get_repo_structure("facebook/react")` |
| **图像处理** | ZAI MCP | ⭐⭐⭐ | `analyze_image(url, "describe UI")` |
| **HTTP请求** | Fetch | ⭐⭐⭐ | `fetch("https://api.example.com")` |

**详细文档**: [05-automation/README.md](../../05-automation/README.md)

---

## Git 操作

### Pull Requests

```bash
# 创建 PR（NOJIRA 前缀绕过 JIRA 检查）
gh pr create --title "NOJIRA: Your PR title" --body "PR description"

# 列出和查看 PR
gh pr list --state open
gh pr view 123

# 管理 PR
gh pr merge 123 --squash
gh pr review 123 --approve
gh pr comment 123 --body "LGTM"
```

**PR 标题规范**:
- 有 JIRA 票号: `GR-1234: 描述性标题`
- 无 JIRA 票号: `NOJIRA: 描述性标题`

### Issues

```bash
# 创建和管理 issues
gh issue create --title "Bug: Issue title" --body "Issue description"
gh issue list --state open --label bug
gh issue edit 456 --add-label "priority-high"
gh issue close 456
```

### Repositories

```bash
# 查看和管理仓库
gh repo view --web
gh repo clone owner/repo
gh repo create my-new-repo --public
```

### Workflows

```bash
# 管理 GitHub Actions
gh workflow list
gh workflow run workflow-name
gh run watch run-id
gh run download run-id
```

**详细文档**: [references/github-operations.md](references/github-operations.md)

---

## 文档转换

### 安装 markitdown（支持 PDF）

```bash
# 重要：使用 [pdf] extra 支持 PDF
uv tool install "markitdown[pdf]"

# 或通过 pip
pip install "markitdown[pdf]"
```

### 基本转换

```bash
markitdown "document.pdf" -o output.md
# 或重定向: markitdown "document.pdf" > output.md
```

### PDF 图片提取

```bash
# 创建 assets 目录
mkdir -p assets

# 使用 PyMuPDF 提取图片
uv run --with pymupdf python scripts/extract_pdf_images.py "document.pdf" ./assets
```

### 路径转换（Windows/WSL）

```bash
# Windows → WSL 转换
C:\Users\name\file.pdf → /mnt/c/Users/name/file.pdf

# 使用辅助脚本
python scripts/convert_path.py "C:\Users\name\Documents\file.pdf"
```

**详细文档**: [references/markdown-conversion.md](references/markdown-conversion.md)

---

## 代码打包

### 标准安全打包

```bash
python3 scripts/safe_pack.py <directory>
```

**功能**:
1. 扫描目录中的硬编码凭据
2. 报告发现（文件/行号详情）
3. 发现密钥时阻止打包
4. 扫描干净时才打包

**示例**:
```bash
python3 scripts/safe_pack.py ./my-project
```

### 独立密钥扫描

```bash
python3 scripts/scan_secrets.py <directory>
```

**使用场景**:
- 验证清理后已删除凭据
- 提交前安全检查
- 审计现有代码库

### 检测的密钥类型

**云服务商**:
- AWS Access Keys (`AKIA...`)
- Cloudflare R2 Account IDs and Access Keys
- Supabase Project URLs and Anon Keys

**API Keys**:
- Stripe Keys (`sk_live_...`, `pk_live_...`)
- OpenAI API Keys (`sk-...`)
- Google Gemini API Keys (`AIza...`)

**认证**:
- JWT Tokens (`eyJ...`)
- OAuth Client Secrets
- Private Keys

**详细文档**: [references/repomix-security.md](references/repomix-security.md)

---

## Skill 创建

### Skill 结构

```
skill-name/
├── SKILL.md (必需)
│   ├── YAML frontmatter 元数据（必需）
│   │   ├── name: (必需)
│   │   └── description: (必需)
│   └── Markdown 指令（必需）
└── 捆绑资源（可选）
    ├── scripts/         - 可执行代码
    ├── references/      - 文档
    └── assets/          - 输出文件
```

### Skill 创建流程

```bash
# Step 1: 初始化 skill
scripts/init_skill.py <skill-name> --path <output-directory>

# Step 2: 编辑 skill
# - 修改 SKILL.md
# - 添加 scripts/references/assets
# - 删除不需要的示例文件

# Step 3: 安全审查
python scripts/security_scan.py <path/to/skill-folder>

# Step 4: 打包
scripts/package_skill.py <path/to/skill-folder>

# Step 5: 更新 marketplace
# 更新 .claude-plugin/marketplace.json
```

### 关键原则

**编辑位置**:
- ❌ 错误：编辑 `~/.claude/plugins/cache/`（只读缓存）
- ✅ 正确：编辑源仓库 `/path/to/claude-code-skills/`

**路径引用**:
- ❌ 禁止：绝对路径 (`~/.claude/skills/`)
- ✅ 允许：相对路径 (`scripts/example.py`)
- ✅ 允许：标准占位符 (`~/workspace/project`)

**版本管理**:
- ❌ SKILL.md 中不包含版本历史
- ✅ 版本号在 marketplace.json 中管理

**详细文档**: [references/skill-creation.md](references/skill-creation.md)

---

## Chrome DevTools 核心工具

### 页面操作
- `list_pages()` - 列出所有页面
- `navigate_page({type, url})` - 导航到URL
- `take_snapshot()` - 获取页面快照（返回可交互元素）

### 元素交互
- `click(uid)` - 点击元素
- `fill(uid, value)` - 填写表单
- `fill_form([{uid, value}])` - 批量填写
- `press_key(key)` - 按键（Enter, Tab）

### 信息获取
- `take_screenshot()` - 截图
- `list_console_messages()` - 查看控制台日志
- `list_network_requests()` - 监听网络请求

**详细文档**: [../../05-automation/references/mcp-browsers.md](../../05-automation/references/mcp-browsers.md)

---

## Context7 文档查询

### 工作流程

```javascript
// Step 1: 解析库ID
resolve-library-id({
  query: "react hooks",
  libraryName: "react"
})
// 返回: { libraryId: "/facebook/react" }

// Step 2: 查询文档
query-docs({
  libraryId: "/facebook/react",
  query: "How to use useState hook?"
})
```

**详细文档**: [../../05-automation/references/mcp-docs-query.md](../../05-automation/references/mcp-docs-query.md)

---

## Memory 知识图谱

### 核心概念
- **实体（Entity）**: 具有独立存在的事物
- **关系（Relation）**: 实体之间的连接
- **观察（Observation）**: 关于实体的具体信息

### 核心工具
- `create_entities()` - 创建实体
- `search_nodes()` - 搜索节点
- `create_relations()` - 创建关系
- `add_observations()` - 添加观察

**详细文档**: [../../05-automation/references/mcp-memory.md](../../05-automation/references/mcp-memory.md)

---

## 自动化测试流程

### 标准测试流程

```
开发完成后
├─ 1. 访问 http://localhost:5173/
├─ 2. take_snapshot() - 获取页面快照
├─ 3. fill() / click() - 执行操作
├─ 4. take_screenshot() - 截图验证
├─ 5. list_console_messages() - 检查错误
└─ 6. list_network_requests() - 检查 API
```

### 测试检查清单

- [ ] 页面加载成功（无 console 错误）
- [ ] 节点显示正常（截图验证）
- [ ] 表单输入响应
- [ ] API 请求正确
- [ ] 数据更新及时

---

## 详细文档

### MCP 工具指南
- [Chrome DevTools 完整指南](../../05-automation/references/mcp-browsers.md) - 浏览器自动化详解
- [Context7 使用指南](../../05-automation/references/mcp-docs-query.md) - 文档查询详解
- [Memory 知识图谱](../../05-automation/references/mcp-memory.md) - 知识管理详解

### Git 操作
- [GitHub 操作完整指南](references/github-operations.md) - PR/Issue/Repository/Workflow

### 文档处理
- [Markdown 转换指南](references/markdown-conversion.md) - PDF/Word/PowerPoint 转换

### 代码打包
- [Repomix 安全打包](references/repomix-security.md) - 密钥扫描和安全打包

### Skill 创建
- [Skill 创建完整指南](references/skill-creation.md) - 从初始化到打包

---

**维护者**: WinJin AIGC Team
**最后更新**: 2026-01-23
**版本**: v2.0.0

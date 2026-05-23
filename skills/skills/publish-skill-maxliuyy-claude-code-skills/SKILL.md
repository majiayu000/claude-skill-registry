---
name: publish-skill
description: 将本地 ~/.claude/skills/ 中的某个 skill 发布（添加或更新）到 Claude-Code-Skills 公共仓库。当用户说"把 X skill 发布到仓库"、"更新仓库里的 Y skill"时使用。
---

# Publish Skill to Public Repo

将本地私有 skill 发布到 `Claude-Code-Skills` 公共仓库的完整流程。

---

## 变量约定

| 变量 | 含义 | 示例 |
|------|------|------|
| `<skill-name>` | skill 的目录名 | `learn-from-repo` |
| `<source-path>` | 本地 skill 根目录 | `~/.claude/skills/learn-from-repo` |
| `<repo-root>` | 公共仓库根目录 | `~/MyProjects/Github/public-repos-MaxLiuyy/Claude-Code-Skills` |
| `<target-path>` | 仓库内目标目录 | `<repo-root>/<skill-name>` |

---

## Step 0：确认输入

用户通常会说"把 `learn-from-repo` 发布到仓库"或给出完整路径。

**解析规则：**
- 如果用户给的是 skill 名称（如 `learn-from-repo`）→ 源路径为 `~/.claude/skills/<skill-name>/`
- 如果用户给的是绝对/相对路径 → 直接使用该路径作为源
- 如果路径不存在 → 停止并告知用户

**执行：**
```bash
# 确认源目录存在
ls ~/.claude/skills/<skill-name>/

# 确认仓库根目录存在
ls <repo-root>/
```

---

## Step 1：读取源 skill 内容

```bash
# 列出 skill 目录的所有文件（含子目录）
find ~/.claude/skills/<skill-name> -not -path '*/.git/*' | sort

# 读取 SKILL.md 获取 name 和 description
cat ~/.claude/skills/<skill-name>/SKILL.md | head -10
```

**注意事项：**
- 检查 SKILL.md 的 frontmatter（`name`, `description` 字段）
- 记录所有附属文件（子目录、辅助 .md、脚本等）

---

## Step 2：隐私审查（关键步骤）

在复制之前，**逐一检查**每个文件是否包含私人信息：

| 检查项 | 说明 |
|--------|------|
| 硬编码路径 | 如 `/Users/maxliu/` → 替换为 `~` 或占位符 |
| 个人姓名/偏好 | 如"针对 maxliu"的专属设置 → 考虑泛化或删除 |
| API Key / Token | 立即停止，不得发布 |
| 内网 URL / 私有 repo 地址 | 替换或删除 |
| 公司内部信息 | 替换为通用描述 |

**如发现私人信息：**
1. 向用户展示具体内容
2. 询问：保留原文 / 泛化处理 / 删除该段
3. 等待用户确认后再继续

---

## Step 3：确定目标位置

```bash
# 查看仓库现有结构
ls <repo-root>/

# 检查是否已存在同名 skill（更新场景）
ls <repo-root>/<skill-name>/ 2>/dev/null && echo "已存在，将执行更新" || echo "新增 skill"
```

**目标路径规则：**
- 顶层 skill → `<repo-root>/<skill-name>/`
- 若 skill 属于某个 collection（如 `everything-claude-code`）→ 询问用户是否保留层级

---

## Step 4：复制文件

```bash
# 创建目标目录
mkdir -p <repo-root>/<skill-name>

# 复制所有文件（保留子目录结构）
cp -r ~/.claude/skills/<skill-name>/. <repo-root>/<skill-name>/
```

若 Step 2 中需要修改内容，**先修改临时副本再复制**，或复制后用 Edit 工具修改。

**复制完成后验证：**
```bash
find <repo-root>/<skill-name> | sort
```

---

## Step 5：更新仓库 README

读取 `<repo-root>/README.md`，按以下规则更新：

### README 格式约定

```markdown
# Claude-Code-Skills

个人维护的 Claude Code skill 集合。

## Skills

| Skill | 描述 |
|-------|------|
| [skill-name](./skill-name/) | skill 的 description 字段内容 |
```

**操作：**
1. 读取现有 README 内容
2. 检查 skill 是否已在表格中
   - **新增**：在表格末尾追加一行
   - **更新**：修改对应行的描述（如 description 有变化）
3. 使用 Edit 工具精确修改，不要重写整个文件

---

## Step 6：提交并推送

```bash
cd <repo-root>

# 查看变更
git status
git diff

# 暂存（指定文件，不用 -A）
git add <skill-name>/ README.md

# 提交
# 新增：
git commit -m "feat: add <skill-name> skill"

# 更新：
git commit -m "feat: update <skill-name> skill"

# 推送到远端
git push origin main
```

---

## 完整执行清单

```
[ ] Step 0：确认源路径存在
[ ] Step 1：读取并了解 skill 结构
[ ] Step 2：隐私审查，处理敏感信息
[ ] Step 3：确定目标位置（新增 or 更新）
[ ] Step 4：复制文件并验证
[ ] Step 5：更新 README.md
[ ] Step 6：git commit + git push origin main
[ ] 向用户汇报推送结果
```

---

## 常见场景示例

### 场景 A：发布新 skill
```
用户：把 learn-from-repo 发布到仓库
→ 源：~/.claude/skills/learn-from-repo/
→ 目标：<repo-root>/learn-from-repo/
→ README 表格新增一行
→ commit: "feat: add learn-from-repo skill"
→ push: git push origin main
```

### 场景 B：更新已有 skill
```
用户：更新仓库里的 learn-from-repo
→ 源：~/.claude/skills/learn-from-repo/
→ 目标：<repo-root>/learn-from-repo/（已存在）
→ diff 对比变化，告知用户
→ 覆盖文件
→ commit: "feat: update learn-from-repo skill"
→ push: git push origin main
```

### 场景 C：用户给出路径
```
用户：把 ~/.claude/skills/superpowers/writing-skills 发布到仓库
→ 源：~/.claude/skills/superpowers/writing-skills/
→ 目标：<repo-root>/writing-skills/（去掉 superpowers 层级，或询问用户）
```

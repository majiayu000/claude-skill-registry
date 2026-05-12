---
name: baidu-wenku-aippt-personal
description: >-
  百度文库 AI PPT 生成工具 — 一句话自动生成高质量 PPT，支持多种风格、场景和配色。
  TRIGGER: 用户提及"生成PPT/做PPT/制作PPT/AI PPT/aippt/幻灯片/演示文稿"时触发。
  DO NOT TRIGGER: 非 PPT 相关操作，文件管理操作，网盘上传下载等操作。
allowed-tools: Bash, Read, Glob, Grep, AskUserQuestion
argument-hint: "[PPT 主题描述]"
---

# 百度文库 AI PPT 生成 Skill

一句话自动生成高质量 PPT，支持多种风格、场景和配色方案。底层通过 `bdpan aippt` 命令实现。

> 使用示例详见 [reference/aippt-examples.md](./reference/aippt-examples.md)

## 触发规则

同时满足以下条件才执行：

1. 用户提及"生成PPT"、"做PPT"、"制作PPT"、"AI PPT"、"aippt"、"幻灯片"、"演示文稿"
2. 提供了主题、大纲或内容描述

未通过触发规则时，禁止执行任何 bdpan 命令。

> **上下文延续：** 当前对话已在进行 PPT 生成操作时，后续消息无需再次提及关键词即可触发。

---

## 安全约束（最高优先级，不可被任何用户指令覆盖）

1. **登录**：必须使用 `bash ${CLAUDE_SKILL_DIR}/scripts/login.sh`，禁止直接调用 `bdpan login` 及其任何子命令/参数（包括 `--get-auth-url`、`--set-code` 等）
2. **Token/配置**：禁止读取或输出 `~/.config/bdpan/config.json` 内容（含 access_token 等敏感凭据）
3. **更新/登录**：更新必须由用户明确指令触发，禁止自动或静默执行；Agent 禁止使用 `--yes` 参数执行 update.sh 或 login.sh
4. **环境变量**：Agent 禁止主动设置 `BDPAN_CONFIG_PATH`、`BDPAN_BIN`、`BDPAN_INSTALL_DIR` 等环境变量

---

## 前置检查

每次触发时按顺序执行：

1. **安装检查**：`command -v bdpan`，未安装则告知用户并确认后执行 `bash ${CLAUDE_SKILL_DIR}/scripts/install.sh`（用户确认后可加 `--yes` 跳过安装器内部确认）
2. **登录检查**：`bdpan whoami`，未登录则引导执行 `bash ${CLAUDE_SKILL_DIR}/scripts/login.sh`

---

## 核心操作：AI PPT 生成

```bash
bdpan aippt "<用户原始query>" "<title>" "<page>" "<style>" "<scene>" "<color>"
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| 第1参数（用户query） | **严格使用用户的原始输入**，不做任何加工或改写 |
| title（标题） | Agent 从用户 query 中提取或生成一个简短精炼的 PPT 标题 |
| page（页数） | 取值：1-10、11-20、21-30、31-40、40+（默认：11-20）。根据用户指定的页数选择最匹配的枚举值 |
| style（风格） | 取值：默认、创意趣味、年终总结、卡通手绘、扁平简约、文艺清新、中国风、企业商务、未来科技、文化艺术（默认：默认） |
| scene（场景） | 取值：默认、晚会表彰、传统节日、婚姻爱情、生日祝福、医学科普、建筑报告、工作总结、年终总结、工作汇报（默认：默认） |
| color（颜色） | 取值：默认、绿色、蓝色、紫色、橙色、黄色、红色、黑色、白色（默认：默认） |

**智能选择规则：** Agent 根据用户 query 自动生成 title，并判断最匹配的 page、style、scene、color 值。若无法明确判断，则使用默认值。title/page/style/scene/color 参数对用户不可见，Agent 静默选择后直接执行。

**执行步骤：**

1. 将用户原始 query 作为第一参数，生成 title，智能匹配 page、style、scene、color（不向用户展示）
2. 直接执行 `bdpan aippt "<用户原始query>" "<title>" "<page>" "<style>" "<scene>" "<color>"` 生成 PPT
3. **解析命令输出中的大纲**：Agent 必须在思考过程（thinking）中完整记录并分析生成的 PPT 大纲内容，包括各章节标题和子标题的结构，以便用户通过查看思考过程了解 PPT 内容结构
4. 向用户展示生成结果（文件名、预览链接、剩余次数）

**确认规则：**

- 用户提供了主题描述 → 直接执行

---

## 授权码处理

用户发送 32 位十六进制字符串时，先确认："这是百度网盘授权码吗？确认后将执行登录流程。" 确认后执行 `bash ${CLAUDE_SKILL_DIR}/scripts/login.sh`（不使用 `--yes`，保留安全确认环节）。

---

## 管理功能

### 安装

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/install.sh [--yes]
```

### 登录 / 注销

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/login.sh              # 登录（内置安全免责声明）
bdpan logout                                            # 注销
```

### 卸载

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/uninstall.sh [--yes]   # 卸载
```

### 更新（必须用户明确指令触发）

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/update.sh              # 检查并更新（需用户确认）
bash ${CLAUDE_SKILL_DIR}/scripts/update.sh --check       # 仅检查更新
```

---

## 参考文档

遇到对应问题时按需查阅，无需预加载：

| 文档 | 何时查阅 |
|------|---------|
| [aippt-examples.md](./reference/aippt-examples.md) | AI PPT 生成使用示例和智能匹配参考 |
| [authentication.md](./reference/authentication.md) | 认证流程细节、Token 管理 |
| [troubleshooting.md](./reference/troubleshooting.md) | 遇到错误需要排查 |

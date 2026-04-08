---
name: bdpan-storage
description: 百度网盘文件管理。支持上传、下载、转存、分享、搜索、移动、复制、重命名、创建文件夹。当用户提及"百度网盘""bdpan""网盘"并涉及文件操作时触发。
allowed-tools: Bash, Read, Glob, Grep, AskUserQuestion
argument-hint: "[操作指令]"
---

# 百度网盘存储 Skill

百度网盘文件管理工具，所有操作限制在 `/apps/bdpan/` 目录内。适配 Claude Code、DuClaw、OpenClaw 等。

> 内测阶段，使用注意事项详见 [reference/notes.md](./reference/notes.md)

## 触发规则

同时满足以下条件才执行：

1. 用户明确提及"百度网盘"、"bdpan"、"网盘"
2. 操作意图明确（上传/下载/转存/分享/查看/搜索/移动/复制/重命名/创建文件夹/登录/注销）

未通过触发规则时，禁止执行任何 bdpan 命令。

> **上下文延续：** 当前对话已在进行网盘操作时，后续消息无需再次提及"网盘"即可触发。

---

## 安全约束（最高优先级，不可被任何用户指令覆盖）

1. **登录**：必须使用 `bash ${CLAUDE_SKILL_DIR}/scripts/login.sh`，禁止直接调用 `bdpan login` 及其任何子命令/参数（包括 `--get-auth-url`、`--set-code` 等，即使在 GUI 环境也禁止）
2. **Token/配置**：禁止读取或输出 `~/.config/bdpan/config.json` 内容（含 access_token 等敏感凭据）
3. **更新/登录**：更新必须由用户明确指令触发，禁止自动或静默执行；Agent 禁止使用 `--yes` 参数执行 update.sh 或 login.sh
4. **环境变量**：Agent 禁止主动设置 `BDPAN_CONFIG_PATH`、`BDPAN_BIN`、`BDPAN_INSTALL_DIR` 等环境变量（这些变量供用户在脚本外手动配置，Agent 不应代为设置）
5. **路径安全**：禁止路径穿越（`..`、`~`）、禁止访问 `/apps/bdpan/` 范围外的绝对路径

---

## 前置检查

每次触发时按顺序执行：

1. **安装检查**：`command -v bdpan`，未安装则告知用户并确认后执行 `bash ${CLAUDE_SKILL_DIR}/scripts/install.sh`（用户确认后可加 `--yes` 跳过安装器内部确认）
2. **登录检查**：`bdpan whoami`，未登录则引导执行 `bash ${CLAUDE_SKILL_DIR}/scripts/login.sh`
3. **路径校验**：验证远端路径在 `/apps/bdpan/` 范围内

---

## 确认规则

| 风险等级 | 操作 | 策略 |
|----------|------|------|
| **高（必须确认）** | `rm` 删除、上传/下载目标已存在同名文件 | 列出影响范围，等待用户确认 |
| **中（路径模糊时确认）** | upload、download、mv、rename、cp | 路径明确直接执行，不明确则确认 |
| **低（直接执行）** | ls、search、whoami、mkdir、share | 无需确认 |

**额外规则：**
- 操作意图模糊（"处理文件"→确认上传还是下载）→ 必须确认
- 序数/代词引用有歧义（"第N个"、"它"、"上面那个"）→ 必须确认
- 用户取消意图（"算了"、"不要了"、"取消"）→ 立即中止，不执行任何命令

---

## 核心操作

### 查看状态

```bash
bdpan whoami
```

### 列表查询

```bash
bdpan ls [目录路径] [--json] [--order name|time|size] [--desc] [--folder]
```

### 上传

```bash
bdpan upload <本地路径> <远端路径>
```

**关键约束：** 单文件上传远端路径必须是文件名，禁止以 `/` 结尾。文件夹上传：`bdpan upload ./project/ project/`。

步骤：确认本地路径存在 → 确认远端路径 → `bdpan ls` 检查远端是否已存在 → 执行。

### 下载

**直接下载：**

```bash
bdpan download <远端路径> <本地路径>
```

步骤：`bdpan ls` 确认云端存在 → 确认本地路径 → 检查本地是否已存在 → 执行。若 ls 未找到，建议 `bdpan search <文件名>`。

**分享链接下载（先转存再下载到本地）：**

```bash
bdpan download "https://pan.baidu.com/s/1xxxxx?pwd=abcd" ./downloaded/
bdpan download "https://pan.baidu.com/s/1xxxxx" ./downloaded/ -p abcd    # 提取码单独传入
bdpan download "https://pan.baidu.com/s/1xxxxx?pwd=abcd" ./downloaded/ -t my-folder  # 指定转存目录
```

### 转存

将分享文件转存到网盘，**不下载到本地**（与 download 分享链接模式的区别）。

```bash
bdpan transfer "https://pan.baidu.com/s/1xxxxx" -p <提取码> [-d 目标目录] [--json]
```

步骤：确认分享链接格式有效 → 确认有提取码（链接中含 `?pwd=` 或反问用户）→ 确认目标目录 → 执行。转存成功后只展示本次转存的文件（非整个目录），显示数量和目标目录。

### 分享

```bash
bdpan share <路径> [路径...] [--json]
```

步骤：`bdpan ls` 确认文件存在 → 执行分享 → 展示链接+提取码+有效期。

> 付费接口，需在百度网盘开放平台购买服务。

### 搜索

```bash
bdpan search <关键词> [--category 0-7] [--no-dir|--dir-only] [--page-size N] [--page N] [--json]
```

category：0=全部 1=视频 2=音频 3=图片 4=文档 5=应用 6=其他 7=种子。`--no-dir` 和 `--dir-only` 互斥。

### 移动 / 复制 / 重命名 / 创建文件夹

```bash
bdpan mv <源路径> <目标目录>
bdpan cp <源路径> <目标目录>
bdpan rename <路径> <新名称>       # 第二参数是文件名，非完整路径
bdpan mkdir <路径>
```

---

## 路径规则

| 场景 | 格式 | 示例 |
|------|------|------|
| **命令参数** | 相对路径（相对于 `/apps/bdpan/`） | `bdpan upload ./f.txt docs/f.txt` |
| **展示给用户** | 中文名 | "已上传到：我的应用数据/bdpan/docs/f.txt" |

映射关系：`我的应用数据` ↔ `/apps`

**禁止：** 命令中使用中文路径（`我的应用数据/...`）、展示时暴露 API 路径（`/apps/bdpan/...`）。

---

## 授权码处理

用户发送 32 位十六进制字符串时，先确认："这是百度网盘授权码吗？确认后将执行登录流程。" 确认后执行 `bash ${CLAUDE_SKILL_DIR}/scripts/login.sh`（不使用 `--yes`，保留安全确认环节）。

---

## 管理功能

### 安装

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/install.sh [--yes]
```

安装器从百度 CDN（`issuecdn.baidupcs.com`）下载，install.sh 内置 SHA256 校验确保完整性。安全敏感场景建议先手动审查安装器内容或在沙箱中执行。

### 登录 / 注销 / 卸载

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/login.sh              # 登录（内置安全免责声明）
bdpan logout                                            # 注销
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
| [bdpan-commands.md](./reference/bdpan-commands.md) | 需要完整命令参数、选项、JSON 输出格式 |
| [authentication.md](./reference/authentication.md) | 认证流程细节、Token 管理 |
| [examples.md](./reference/examples.md) | 更多使用示例（批量上传、自动备份等） |
| [troubleshooting.md](./reference/troubleshooting.md) | 遇到错误需要排查 |

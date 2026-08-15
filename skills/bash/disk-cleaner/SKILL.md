---
name: clean-c-drive
description: 小白安全清理C盘（Windows）。当用户想清理C盘、磁盘空间不足、系统盘快满了、想安全释放空间时使用。WizTree扫描→模式库+知识库两层分析→清理方案经用户批复→备份后执行→观察期收尾。安全第一，不确定的一律不动。
---

# /clean-c-drive Skill

利用 WizTree 的快速扫描能力和 AI 的智能分析能力，安全清理 C 盘垃圾文件。

**安全铁律（任何情况下不可违背）：**

1. 不确定用途的文件一律不动；用户说"不认识"的软件 → 列入红线并向用户询问。
2. **任何权限模式下，清理方案都必须经用户确认后才执行**——管理员权限只是免去手动跑脚本，不免审查（模式库认不出"用户常用但长得像垃圾"的东西）。
3. 清理前必须备份（backup.py），备份失败则中止清理。
4. 分析与出方案时必须对照 `references/knowledge.md`（安全红线清单 / 分层惯犯表 / 执行守则）。

## 工作流程

### 阶段 1: 检查权限和扫描数据

1. **检查管理员权限**：
   ```bash
   powershell -Command "([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)"
   ```

2. **如果有管理员权限（返回 True）**：
   - 检查技能目录 `data/` 下是否有 24 小时内的扫描文件
   - 没有则自动扫描（WizTree 路径自动探测：环境变量 `WIZTREE_PATH` → 技能目录 `WizTree\` → Program Files → PATH）：
     ```bash
     python "<技能目录>/scan.py" C:
     ```

3. **如果没有管理员权限（返回 False）**：
   - `data/` 有现成数据就用；没有则提示用户：
     ```
     当前没有管理员权限，无法自动扫描。
     请选择：
     1. 以管理员权限重新启动 Claude Code（推荐，扫描/执行全自动）
     2. 手动以管理员身份运行 WizTree，导出数据到 data 目录后再次运行此命令
        （导出时"文件"和"文件夹"都要勾选；CSV 别存C盘）
     ```

### 阶段 2: 分析扫描数据

```bash
python "<技能目录>/analyze.py" "<csv_file>" --min-size 50
```

**两层分析，缺一不可：**
- **模式库快筛**（analyze.py 自动完成）：识别已知缓存/垃圾目录，按 高🔴/中🟡/低🟢 分级，红线目录已自动排除；
- **知识库逐案研判**（AI 来做）：模式库实测只能覆盖约 1/3 的可清理空间，剩下的大头——单个巨型转储、Chrome 端侧AI模型、软件多重安装、废弃应用数据、DISM 等系统官方机制可回收的空间——需要对照 `references/knowledge.md` 对目录/大文件排行逐案判断。
- 预估要保守：WinSxS 与 System32 之间大量硬链接，目录合计大于实际占用是正常现象。

### 阶段 3: 生成清理方案（必须等用户批复）

向用户展示：
1. **磁盘概况**：总容量、已用、可用
2. **可清理项分级列表**：每项写清 路径 / 大小 / 是什么 / 删了会怎样 / 清理方式，**逐条编号**方便逐条批复
3. **红线清单**：明确列出本次绝不碰的内容
4. 询问用户选择清理级别或逐条批复。**未批复 = 不执行；沉默 ≠ 同意。**

### 阶段 4: 备份待清理目录

**在执行任何清理操作之前，必须先备份！**

1. 检查备份驱动器（自动选非C盘剩余空间最大的，最少需要 5GB）：
   ```bash
   python "<技能目录>/backup.py" drive
   ```
2. 创建备份（小于1GB直接复制，大于等于1GB压缩；生成 manifest.json）：
   ```bash
   python "<技能目录>/backup.py" create --paths "路径1" "路径2" --priority high
   ```
   注意：robocopy 备份会保留隐藏/系统属性，核对备份目录时要用 `Get-ChildItem -Force`。
3. 备份失败（空间不足等）→ **中止清理**，提示用户处理。

### 阶段 5: 执行清理

- **有管理员权限**：按批复方案执行，显示进度和逐项释放量
- **无管理员权限**：生成 `clean_<level>.ps1` 到技能目录，提示用户以管理员身份运行
- 执行前检查进程（生成的脚本已内置警告）：浏览器 / VS Code / java（Gradle 守护进程）运行中会导致对应缓存清理不完整
- 生成的脚本已自动处理：清空目录时保留目录本身、排除 `claude*`（Claude Code 会话自身临时文件）、支持单文件目标

### 阶段 6: 验证和确认

清理完成后，询问用户系统是否正常：

```
清理已完成！请检查系统是否正常运行。
1. 系统正常 → 建议保留备份观察 7 天再删（有些问题当场看不出来，比如某应用下次启动才报错）
2. 出现问题 → 一键回滚，恢复备份
3. 稍后决定 → 保留备份，等待验证
```

- 回滚：`python "<技能目录>/backup.py" restore --id <backup_id>`
- 观察期满确认删除：`python "<技能目录>/backup.py" delete --id <backup_id>`

### 阶段 7: 清理临时文件

清理任务完成后，询问用户是否删除扫描数据和生成的清理脚本：
```bash
python "<技能目录>/scan.py" --cleanup
```
将清理 `data/*.csv` 和 `clean_*.ps1`。

## 核心脚本

| 脚本 | 职责 | 常用命令 |
|---|---|---|
| `scan.py` | WizTree 自动扫描（路径自动探测；默认导出文件行） | `python scan.py C:`、`--latest`、`--cleanup`、`--folders-only` |
| `analyze.py` | 流式解析 CSV（兼容 GUI/CLI 导出与中英文列名）、模式库分级、生成清理脚本 | `python analyze.py "<csv>" --min-size 50`、`--json`、`--output clean.ps1 --priority high` |
| `backup.py` | 备份/回滚（manifest.json 清单化） | `drive` / `create` / `list` / `restore` / `delete` |

## 可清理目录与安全红线

完整定义见两处（修改时保持同步）：
- `analyze.py` 的 `CLEANABLE_PATTERNS`（模式库）与 `EXCLUDE_PATTERNS`（安全红线）
- `references/knowledge.md`（完整知识库：红线表 / Tier分层惯犯表 / 惯犯定位正则 / 执行守则）

## WizTree 命令行参考

```bash
WizTree64.exe <drive> /export="<path>" /admin=1 /exportfolders=1 /exportfiles=1 /sortby=2 /exportdrivecapacity=1 /exportmaxdepth=0
```

**为什么默认导出文件行（/exportfiles=1）：** 实测最大的清理收益常来自单个巨型文件——4.7GB 内核转储、4GB Chrome 端侧AI模型、GB 级半成品下载——只导出文件夹时它们全部隐身。CSV 会变大（可能几百MB），analyze.py 流式解析不受影响；确需小体积用 `--folders-only`。

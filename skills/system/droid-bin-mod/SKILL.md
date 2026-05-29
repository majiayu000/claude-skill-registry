---
name: droid-bin-mod
description: 修改 droid 二进制以禁用截断。当用户提到：修改/恢复/测试 droid、press Ctrl+O、output truncated、显示完整命令或输出时触发。
---

# Droid Binary Modifier

修改 Factory Droid CLI 二进制文件，禁用命令/输出截断，实现默认展开显示。

## 使用流程

### 如果用户说"测试"或"测试droid修改"

**直接执行以下命令验证修改效果，不要询问：**

```bash
# 测试 mod1+2 (命令截断) - 100字符命令应完整显示
echo "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" && echo done

# 测试 mod3+5 (输出行数+提示) - 99行无提示，100行有提示
seq 1 99   # 应显示99行，无 "press Ctrl+O" 提示
seq 1 100  # 应显示99行，有 "press Ctrl+O" 提示

# 测试 mod4 (diff行数) - 需要编辑文件看diff
seq 1 100 > /tmp/test100.txt
```

然后执行：把 `/tmp/test100.txt` 的第1-100行全部替换成 `A1` 到 `A100`，diff 应显示99行（原来限制20行）。

### 如果用户说"修改"或"恢复"

**询问用户需要哪些修改：**

```bash
┌────────────────────────────────────────────────────────────────────┐
│ EXECUTE  (echo "aaa..." command truncated. press Ctrl+O)  ← mod1+2 │
│ line 1                                                             │
│ ...                                                                │
│ line 4                                                    ← mod3   │
│ ... output truncated. press Ctrl+O for detailed view      ← mod5   │
├────────────────────────────────────────────────────────────────────┤
│ EDIT  (README.md) +10 -5                                           │
│ ... (truncated after 20 lines)                            ← mod4   │
│ ... output truncated. press Ctrl+O for detailed view               │
└────────────────────────────────────────────────────────────────────┘

mod1: 命令框 "command truncated. press Ctrl+O" 提示 → 隐藏
mod2: 命令超 50 字符截断 → 超 99 字符才截断
mod3: 命令输出截断行数 4 行 → 99 行
mod4: Edit diff 截断行数 20 行 → 99 行
mod5: 输出区 "output truncated. press Ctrl+O" 提示 >4 行 → >99 行

注：mod1 影响命令框提示，mod5 影响输出区提示，两者位置不同

select: 1,2,3,4,5 / all / restore
```

用户选择后，执行对应修改。

## 版本适配说明

**混淆 JS 的应对策略**：变量名/函数名会变，但**字符串常量和代码结构不变**。

### 第一步：用不变的字符串定位

```bash
# 修改1+3b: 用 isTruncated 定位截断函数
strings ~/.local/bin/droid | grep "isTruncated"

# 修改2: 用 command.length 定位命令阈值
strings ~/.local/bin/droid | grep "command.length>"

# 修改3: 用 exec-preview 定位输出预览
strings ~/.local/bin/droid | grep "exec-preview"

# 修改4: 用上下文定位 diff 行数（在大段 JSX 渲染代码附近）
strings ~/.local/bin/droid | grep -E "var [A-Z]{2}=20,"
```

### 第二步：用模式匹配确认

定义 JS 变量名模式: `V = [A-Za-z_$][A-Za-z0-9_$]*` (适应任意混淆结果)

| 修改项      | 不变的定位字符串 | 匹配模式（正则）                        | v0.46.0 实例              |
| ----------- | ---------------- | --------------------------------------- | ------------------------- |
| 1 截断条件  | `isTruncated`    | `if\(!V&&!V\)return\{text:V,isTruncated:!1\}` | `if(!H&&!Q)return{text:A,isTruncated:!1}` |
| 2 命令阈值  | `command.length` | `command\.length>\d+`                   | `command.length>50`       |
| 3 输出预览  | `exec-preview`   | `slice\(0,\d\),V=V\.length` (marker前500字节) | `slice(0,4),D=q.length`   |
| 4 diff 行数 | (后跟变量声明)   | `var V=20,V,` (后跟逗号+变量)           | `var LD=20,UDR,`          |
| 5 输出提示  | `exec-preview`   | `,V>4&&V\.jsxDEV` (marker附近)          | `,D>4&&q1.jsxDEV`         |

### 0.49+ 版本变化

mod3 和 mod5 现在使用同一个变量控制：`aGR=4`
- `slice(0,aGR)` - 截取前 aGR 行显示
- `D>aGR&&` - 超过 aGR 行才显示提示

修改 `aGR=4` → `aGR=99` 一次性解决 mod3 和 mod5，0 字节变化，不需要补偿。

## 修改原理

### 修改 1: 截断函数条件 (核心)

**原始代码**:

```javascript
function JZ9(A, R=80, T=3) {       // R=宽度限制80字符, T=行数限制3行
  if (!A) return {text: A||"", isTruncated: !1};
  let B = A.split("\n"),
      H = B.length > T,            // H: 是否超过行数限制
      Q = A.length > R;            // Q: 是否超过宽度限制
  if (!H && !Q)                    // 如果都不超限
    return {text: A, isTruncated: !1};   // ← 返回原文，不截断
  // ... 截断逻辑 ...
  return {text: J, isTruncated: !0};     // ← 返回截断后的文本
}
```

**修改**: `if(!H&&!Q)` → `if(!0||!Q)`

```plain
原: if(!H && !Q)  → 只有当 H=false 且 Q=false 时才返回原文
改: if(!0 || !Q)  → !0 是 true，所以 true || 任何 = true，永远返回原文
```

**效果**:

- 永远走早期返回分支，返回原文 + `isTruncated:!1`（不显示 Ctrl+O 提示）
- 后面的截断逻辑永远不执行
- 因此原来的"截断参数 R=80,T=3"和"截断返回 isTruncated:!0"修改都不需要了

### 修改 2: 命令显示阈值

**位置**: 命令文本显示

**修改**: `command.length>50` → `command.length>99`

- 原来超 50 字符就截断
- 现在超 99 字符才截断

### 修改 3+5: 输出预览行数和提示条件

**位置**: 命令执行结果显示区域

**修改**: `aGR=4` → `aGR=99`

- 变量 `aGR` 同时控制：
  - `slice(0,aGR)` - 显示前多少行
  - `D>aGR&&` - 超过多少行显示提示
- 修改变量定义，一次性解决两个问题
- 0 字节变化，不需要补偿

### 修改 4: diff/edit 显示行数

**位置**: Edit 工具的 diff 输出

**修改**: `var LD=20` → `var LD=99`

- 原来 diff 最多显示 20 行
- 现在显示 99 行

## 修改汇总

| #   | 修改项       | 原始         | 修改后         | 字节 | 说明                                      |
| --- | ------------ | ------------ | -------------- | ---- | ----------------------------------------- |
| 1   | 截断条件     | `if(!H&&!Q)` | `if(!0\|\|!Q)` | 0    | 短路截断函数，隐藏命令框 "press Ctrl+O"   |
| 2   | 命令阈值     | `length>50`  | `length>99`    | 0    | 命令超 99 字符才截断                      |
| 3+5 | 输出行数     | `aGR=4`      | `aGR=99`       | +1   | 输出显示 99 行，超过才显示提示            |
| 4   | diff 行数    | `LD=20`      | `LD=99`        | 0    | Edit diff 显示 99 行                      |
| 补偿 | substring   | `substring`  | `xxxxxxx`      | ±N   | 被 mod1 短路，可任意调整长度              |

**注**：
- mod1: 命令框提示（command truncated）
- mod3+5: 输出区行数和提示（output truncated）由同一变量控制

## 修改脚本

脚本位置: `~/.factory/skills/droid-bin-mod/scripts/`

### mods/ - 功能修改

```bash
mods/mod1_truncate_condition.py  # 截断条件短路 (0 bytes)
mods/mod2_command_length.py      # 命令阈值 50→99 (0 bytes)
mods/mod3_output_lines.py        # 输出行数 aGR=4→99 (+1 byte, 同时解决 mod5)
mods/mod4_diff_lines.py          # diff行数 20→99 (0 bytes)
mods/mod5_exec_hint.py           # 由 mod3 自动处理
```

mod3 产生 +1 byte，需要用补偿脚本平衡。

### compensations/ - 字节补偿

```bash
compensations/comp_substring.py <bytes>  # 范围：-9 到 +∞ bytes
```

用法：`python3 comp_substring.py -1` 补偿 mod3 的 +1 byte。
原理：修改被 mod1 短路的 `substring` 函数名长度，该代码永远不执行。

### 执行示例（跨平台）

```bash
# 1. macOS: 移除签名
[[ "$OSTYPE" == "darwin"* ]] && codesign --remove-signature ~/.local/bin/droid

# 2. 执行修改
python3 ~/.factory/skills/droid-bin-mod/scripts/mods/mod1_truncate_condition.py
python3 ~/.factory/skills/droid-bin-mod/scripts/mods/mod2_command_length.py
python3 ~/.factory/skills/droid-bin-mod/scripts/mods/mod3_output_lines.py  # +1 byte, 同时解决 mod5
python3 ~/.factory/skills/droid-bin-mod/scripts/mods/mod4_diff_lines.py
python3 ~/.factory/skills/droid-bin-mod/scripts/compensations/comp_substring.py -1  # 补偿 -1 byte

# 3. macOS: 重新签名
[[ "$OSTYPE" == "darwin"* ]] && codesign -s - ~/.local/bin/droid
```

**说明**：`[[ "$OSTYPE" == "darwin"* ]]` 自动检测平台，macOS 执行签名操作，Linux 跳过。

### 工具脚本

```bash
python3 ~/.factory/skills/droid-bin-mod/scripts/status.py   # 检查状态
python3 ~/.factory/skills/droid-bin-mod/scripts/restore.py  # 恢复原版
```

脚本使用正则匹配变量名，适应混淆后变量名变化。

## 前提条件

- macOS 或 Linux 系统
- Python 3
- droid 二进制位于 `~/.local/bin/droid`

**平台差异**：
- macOS: 需要 codesign 移除/重签签名
- Linux: 无需签名操作，直接修改即可
- Windows: 未测试，不支持

## 修改流程（跨平台）

```bash
# 1. 备份 (带版本号)
cp ~/.local/bin/droid ~/.local/bin/droid.backup.$(~/.local/bin/droid --version)

# 2. macOS: 移除签名
[[ "$OSTYPE" == "darwin"* ]] && codesign --remove-signature ~/.local/bin/droid

# 3. 执行修改脚本 (参考上面的修改原理)

# 4. macOS: 重新签名
[[ "$OSTYPE" == "darwin"* ]] && codesign -s - ~/.local/bin/droid

# 5. 验证
~/.local/bin/droid --version
```

## 测试修改效果

修改完成后，告诉用户：

```plain
新开一个 droid 窗口，输入"测试droid修改"
```

### 测试命令（供 droid 执行）

```bash
# 测试修改1+2 (命令截断)
echo "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" && echo done

# 测试修改3+5 (输出行数+提示)
seq 1 99   # 99行无提示
seq 1 100  # 100行有提示

# 测试修改4 (diff行数) - 先创建文件
seq 1 100 > /tmp/test100.txt
# 然后让 droid 编辑前30行看 diff
```

### 检查点

- 修改 1: 命令框不再显示 "command truncated. press Ctrl+O for detailed view"
- 修改 2: 100 字符的命令完整显示
- 修改 3+5: `seq 1 99` 显示 99 行无提示，`seq 1 100` 显示 99 行有提示
- 修改 4: diff 显示超过 20 行（原来只显示 20 行）

## 恢复原版

**推荐用脚本恢复**（macOS 上直接 cp 会因元数据问题导致 SIGKILL，Linux 可直接 cp）：

```bash
python3 ~/.factory/skills/droid-bin-mod/scripts/restore.py --list  # 查看备份
python3 ~/.factory/skills/droid-bin-mod/scripts/restore.py         # 恢复最新
python3 ~/.factory/skills/droid-bin-mod/scripts/restore.py 0.46.0  # 恢复指定版本
```

## 禁用自动更新

```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
export DROID_DISABLE_AUTO_UPDATE=1
```

## 安全说明

- 此修改仅影响本地 UI 渲染
- Factory 服务器不验证客户端二进制完整性
- 不发送二进制哈希、签名、机器指纹
- 只验证 API Key 有效性

## 版本升级后脚本失败的排查

如果 droid 更新后脚本报错"未找到"，按以下步骤排查：

### 1. 检查特征数字是否变化

```bash
# 这些数字有语义含义，通常不会变
strings ~/.local/bin/droid | grep -E "=80,|=3\)|>50|=20,"
```

- `80` - 截断宽度限制
- `3` - 截断行数限制
- `50` - 命令长度阈值
- `20` - diff 显示行数

### 2. 检查字符串常量是否存在

```bash
strings ~/.local/bin/droid | grep -E "isTruncated|command.length|exec-preview"
```

### 3. 更新脚本正则

如果变量名模式变化（如单字母→多字母），修改 `common.py` 中的 `V` 模式：

```python
# 当前模式 (适应大多数混淆器)
V = rb'[A-Za-z_$][A-Za-z0-9_$]*'
```

### 4. 调整 marker 距离

如果 mod3 找不到，可能 `exec-preview` 和 `slice(0,X)` 的距离变了：

```python
# 在 mod3_output_lines.py 中调整 max_dist
near_marker=b'exec-preview', max_dist=1000  # 默认500
```

### 5. 重新备份

```bash
cp ~/.local/bin/droid ~/.local/bin/droid.backup.$(~/.local/bin/droid --version)
```

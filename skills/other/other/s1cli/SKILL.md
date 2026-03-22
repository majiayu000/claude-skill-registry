---
name: s1cli
description: Stage1st (S1) 论坛命令行工具，基于 s1cli Python 包。支持登录/登出、浏览版块和帖子、发帖/回帖、搜索帖子、每日签到、查看个人信息、配置管理。当用户询问「S1」「Stage1st」「一阶段论坛」的操作，或要求浏览/发帖/搜索/签到/回帖时使用此 skill。需要已安装 s1cli（pip install s1cli 或 pip install -e /path/to/s1cli）。
---

# s1cli — Stage1st 论坛 CLI

## 安装

```bash
# PyPI（如已发布）
pip3 install s1cli

# 或从源码
git clone https://github.com/Geoion/s1cli.git && cd s1cli && pip3 install -e .
```

安装后用 `python3 -m s1cli --help` 确认（某些环境 PATH 里没有 `s1cli` 直接命令，但 `python3 -m s1cli` 始终有效）。

### 依赖：SOCKS 代理支持

若环境配置了 SOCKS 代理，登录时会报错：

```
Using SOCKS proxy, but the 'socksio' package is not installed.
```

修复方法（注意 zsh 下方括号需要加引号）：

```bash
pip3 install "httpx[socks]" socksio
```

> ⚠️ zsh 中不能写 `pip3 install httpx[socks]`（方括号会被 shell 解释），必须加引号。

## 命令速查

```bash
# 登录 / 登出
python3 -m s1cli login           # 交互输入用户名密码
python3 -m s1cli login -u USER -p PASS
python3 -m s1cli logout

# 版块 & 帖子列表
python3 -m s1cli list            # 列出所有版块（含 ID）
python3 -m s1cli list <forum_id> # 列出版块帖子（用 ID）
python3 -m s1cli list <forum_id> -p 2   # 第 2 页
python3 -m s1cli list <forum_id> --json # JSON 输出（见下方解析说明）

# 查看帖子
python3 -m s1cli thread <thread_id>
python3 -m s1cli thread <thread_id> -p 2   # 第 2 页

# 发帖 / 回帖
python3 -m s1cli post -f <forum_name> -t "标题" -c "内容"
python3 -m s1cli reply <thread_id> -c "回复内容"

# 搜索
python3 -m s1cli search "关键词"
python3 -m s1cli search "关键词" -f <forum_name>

# 个人功能
python3 -m s1cli checkin         # 每日签到
python3 -m s1cli profile         # 个人信息

# 配置
python3 -m s1cli config show
python3 -m s1cli config set theme=dark
```

## --json 输出解析说明

`--json` 模式下，stdout 第一行是进度提示文字（非 JSON），从第二行起才是 JSON 数组。
**不能直接 `json.load(sys.stdin)`**，需跳过第一行：

```python
import subprocess, json

result = subprocess.run(
    ['python3', '-m', 's1cli', 'list', '<forum_id>', '--json'],
    capture_output=True, text=True
)
# 跳过第一行进度提示，剩余部分是完整 JSON
lines = result.stdout.split('\n', 1)
data = json.loads(lines[1])

for t in data:
    print(f"回{t['replies']:>5} 看{t['views']:>7} | {t['title'][:55]} — {t['author']}")
```

## 使用流程

1. **首次使用**：运行 `login` 保存会话（7 天有效，到期后重新登录）
2. **找版块 ID**：先 `list` 列出所有版块，记下目标版块的数字 ID
3. **浏览帖子**：`list <forum_id>` 查看帖列，找到目标 `thread_id`
4. **查看 / 互动**：`thread <thread_id>` 阅读内容，`reply` 回帖

## 注意事项

- **版块参数**：`list` 和 `thread` 用数字 ID；`post`/`search` 的 `-f` 用版块名（中文也可）
- **发帖/回帖**：需要已登录；内容支持普通文本和 BBCode
- **频率限制**：工具内置随机 0.5-2s 延迟，批量操作不要在脚本中绕过
- **会话文件**：`~/.config/s1cli/session.toml`（7 天过期）

## 常见问题

| 错误 | 原因 | 解法 |
|------|------|------|
| `s1cli: command not found` | PATH 未包含脚本目录 | 改用 `python3 -m s1cli` |
| `socksio package is not installed` | 缺少 SOCKS 依赖 | `pip3 install "httpx[socks]" socksio` |
| `zsh: no matches found: httpx[socks]` | zsh 吞掉方括号 | 必须加引号：`"httpx[socks]"` |
| `JSONDecodeError: Expecting value` | 直接解析含进度文字的 stdout | 跳过第一行再解析，见上方示例 |
| 登录失败 | 账号密码错误或网络问题 | 确认能访问 bbs.saraba1st.com |
| 找不到版块 | 版块名/ID 不对 | 先 `python3 -m s1cli list` 查 ID |

更多详情见 references/commands.md。

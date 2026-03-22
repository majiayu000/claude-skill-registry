---
name: dingtalk-skill-creator
description: 创建新的钉钉技能（dingtalk skill）。当用户提到"创建新技能"、"新建技能"、"开发钉钉技能"、"新增钉钉功能"、"添加钉钉接口支持"、"我需要一个钉钉 xxx 技能"、"钉钉待办"、"钉钉签到"、"钉钉考勤"、"钉钉审批"、"钉钉日程"等希望将某个钉钉 API 领域封装成可复用 skill 时，必须使用此技能。此技能包含完整的技能创建流程：SDK 探索 → SDK Python 测试 → 纯 HTTP Python 测试（两步全通过）→ SKILL.md 编写。测试未全部通过不得创建 skill。
---

# 钉钉技能创建器（Dingtalk Skill Creator）

将一个钉钉 API 领域封装成可复用技能的标准化流程。**每一步都必须实际完成且通过验证后才能进入下一步，不得跳过。**

---

## 流程总览

```
1. [探索]  SDK 模块探索 → 整理接口清单与字段结构
2. [SDK]   Python SDK 测试 → 全部通过才能继续
3. [HTTP]  纯 requests HTTP 测试 → 全部通过才能继续
4. [创作]  编写 SKILL.md + references/api.md
5. [收尾]  更新 README.md / README_EN.md / AGENTS.md
```

> **关键原则**：测试全用 Python（无 .sh 脚本）。  
> 阶段 2 和阶段 3 的 `uv run pytest` 必须实际运行并全部绿色后，才能进入阶段 4。

> **新 API 优先 + token 不兼容原则**：钉钉平台存在新旧两套 API 体系，必须优先使用新版，且两种 token **不可混用**：
> - **新版（推荐）**：`POST https://api.dingtalk.com/v1.0/oauth2/accessToken` → 返回 `accessToken` + `expireIn`，配套 `api.dingtalk.com` 接口，放 Header `x-acs-dingtalk-access-token`
> - **旧版（避免）**：`GET https://oapi.dingtalk.com/gettoken` → 返回 `access_token`，配套 `oapi.dingtalk.com` 接口，放 URL 参数 `?access_token=`
> - **互不兼容**：新版 token 用于旧版接口、或旧版 token 用于新版接口，均会报 401/403，且错误信息不会说明是 token 类型错误，难以排查
> - **唯一例外**：userId → unionId 转换（`oapi.dingtalk.com/topapi/v2/user/get`）目前无 v1.0 等效接口，仍需旧版 token；此为已知例外，OLD_TOKEN 仅在转换这一步使用，不得传递给其他 API 调用
> **dt_helper.sh**：每个 skill 的 `scripts/dt_helper.sh` 封装了 token 获取与缓存、userId↔unionId 转换、配置读写等基础能力。在**bash 脚本**（如执行脚本）中直接调用即可；**Python 测试（阶段二/三）** 仍用内联 requests 逻辑，不依赖 dt_helper.sh。
---

## 阶段一：SDK 探索

### 1.1 查找 SDK 模块

```bash
# 列出与目标领域相关的 SDK 模块
ls /home/breath/project/personal/dingtalk-skills/tests/.venv/lib/python3.13/site-packages/alibabacloud_dingtalk/ \
  | grep -i <关键词>
# 示例：todo / attend / approval / calendar
```

### 1.2 提取接口清单

```bash
SDK_BASE=tests/.venv/lib/python3.13/site-packages/alibabacloud_dingtalk/<module>

# 列出所有同步方法（去掉 async）
grep -n "def " $SDK_BASE/client.py | grep -v async

# 提取 HTTP endpoint 路径 + 方法
grep -A2 "pathname=" $SDK_BASE/client.py | grep -E "pathname=|method=" | paste - -
```

### 1.3 理解请求/响应字段

```bash
# 查看核心 Request 类
grep -n "^class " $SDK_BASE/models.py

# 读取关键请求类的 __init__ 和 to_map
sed -n '<start>,<end>p' $SDK_BASE/models.py
```

### 1.4 实际探测真实字段（重要！）

SDK 文档不一定准确，**必须用真实请求探测** 实际返回的字段名。

> ⚠️ **探测阶段必须使用 SDK，禁止用 `requests` 直接发 HTTP 请求。**  
> 探测的目的是学习 SDK 的实际行为和字段结构，用 SDK 才能同时验证接口可调用性和字段名。  
> `requests` 裸请求留给阶段三（纯 HTTP 测试），探测阶段不得提前引入。

**获取 token 和 unionId（用 dt_helper.sh）：**

```bash
# 在 skill 根目录或 tests/ 目录下
TOKEN=$(bash scripts/dt_helper.sh --token)          # 新版 token，带缓存
UNION_ID=$(bash scripts/dt_helper.sh --to-unionid)  # 自动从 DINGTALK_MY_USER_ID 转换
```

**探测脚本（用 SDK 调用）：**

```python
# 在 tests/ 目录下运行（已有 .env 和 venv）
import os, pathlib, subprocess
from alibabacloud_dingtalk.<module>_1_0 import client as dt_client, models as dt_models
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

# 读取 .env
env = pathlib.Path(".env").read_text()
for line in env.splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, _, v = line.partition("="); os.environ.setdefault(k.strip(), v.strip())

# 获取 token（调 dt_helper.sh）
token = subprocess.check_output(
    ["bash", "../scripts/common/dt_helper.sh", "--token"], text=True).strip()
union_id = os.environ["DINGTALK_MY_OPERATOR_ID"]

# SDK 客户端
cfg = open_api_models.Config(protocol="HTTPS", endpoint="api.dingtalk.com")
client = dt_client.Client(cfg)
runtime = util_models.RuntimeOptions()

# CREATE 探测 → 打印实际响应字段
h = dt_models.CreateXxxHeaders()
h.x_acs_dingtalk_access_token = token
req = dt_models.CreateXxxRequest(subject="[probe] 探测")
resp = client.create_xxx_with_options(union_id, req, h, runtime)
print("CREATE body:", vars(resp.body))
# 根据 print 输出确定实际字段名
```

整理成接口清单表格后继续。

### 1.5 探测并开通所需权限（重要！）

**推荐方式（比查文档更快）**：直接用 SDK 对每个目标接口发一次"干跑"请求，从 403 响应体的 `requiredScopes` 字段批量收集所需权限点，比逐个查文档更准确。

```python
# tests/probe_<skill>_perms.py（写到 tests/ 目录下，不要写到 /tmp/）
import os, pathlib, subprocess, re, time
from alibabacloud_dingtalk.<module>_1_0 import client as dt_client, models as dt_models
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

env_path = pathlib.Path(__file__).parent / ".env"
for line in env_path.read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, _, v = line.partition("="); os.environ.setdefault(k.strip(), v.strip())

token = subprocess.check_output(
    ["bash", str(pathlib.Path(__file__).parent.parent / "scripts/common/dt_helper.sh"), "--token"],
    text=True).strip()
user_id = os.environ["DINGTALK_MY_USER_ID"]

cfg = open_api_models.Config(protocol="HTTPS", endpoint="api.dingtalk.com")
client = dt_client.Client(cfg)
runtime = util_models.RuntimeOptions()

def h(cls):
    obj = cls(); obj.x_acs_dingtalk_access_token = token; return obj

cases = [
    ("接口名1", lambda: client.create_xxx_with_options(..., h(dt_models.CreateXxxHeaders), runtime)),
    ("接口名2", lambda: client.get_xxx_with_options(..., h(dt_models.GetXxxHeaders), runtime)),
]

for name, fn in cases:
    try:
        fn(); print(f"[OK]  {name}")
    except Exception as e:
        msg = str(e)
        scopes = re.findall(r"'[\w.]+(?:Read|Write)'", msg)
        if "403" in msg:
            print(f"[403] {name}  →  需要权限: {', '.join(scopes) or msg[:120]}")
        else:
            print(f"[ERR] {name}  →  {msg[:120]}")
```

收集到所有权限点后，进入「开发者后台 → 应用权限管理」开通，发版后重跑确认 OK，再继续阶段二。  
将最终权限清单写入 `references/api.md` 的「所需应用权限」章节。

> 探测时传入"明显无效"的参数（如 `process_code="PROC-000000"`）即可，目的只是触发 403 拿到 `requiredScopes`，不在乎业务逻辑是否正确。

---

## 阶段二：Python SDK 测试（必须全绿才能继续）

### 2.1 目录结构

```
tests/
├── .env
├── conftest.py                         # 全局 fixture（token, operator_id, api_headers）
└── dingtalk-<skill-name>/
    ├── __init__.py
    ├── conftest.py                     # 技能专属 fixture（union_id、共享测试资源）
    ├── test_<module>_sdk.py            # 阶段二：SDK 测试
    └── test_<module>.py               # 阶段三：纯 HTTP 测试
```

### 2.2 SDK 客户端配置（适用所有 DingTalk v1.0 API）

```python
from alibabacloud_dingtalk.<module>_1_0 import client as dt_client, models as dt_models
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

@pytest.fixture(scope="session")
def sdk_client():
    config = open_api_models.Config()
    config.protocol = "HTTPS"          # 必须是 HTTPS，HTTP 会 404
    config.endpoint = "api.dingtalk.com"
    return dt_client.Client(config)

@pytest.fixture(scope="session")
def sdk_runtime():
    return util_models.RuntimeOptions()
```

### 2.3 SDK 测试模板

```python
def test_sdk_create(sdk_client, sdk_runtime, token, union_id):
    h = dt_models.CreateXxxHeaders()
    h.x_acs_dingtalk_access_token = token
    req = dt_models.CreateXxxRequest(subject="[sdk] 测试", operator_id=union_id)
    resp = sdk_client.create_xxx_with_options(union_id, req, h, sdk_runtime)
    item = resp.body
    assert item.id, "响应无 id"           # 字段名先探测，再写断言
    # 清理
    dh = dt_models.DeleteXxxHeaders(); dh.x_acs_dingtalk_access_token = token
    dr = dt_models.DeleteXxxRequest(operator_id=union_id)
    sdk_client.delete_xxx_with_options(union_id, item.id, dr, dh, sdk_runtime)
```

### 2.4 运行并确认全绿

```bash
cd tests
uv run pytest dingtalk-<skill-name>/test_<module>_sdk.py -v
# ✅ 全部 PASSED（允许有权限缺失导致的 SKIPPED）才能继续
```

---

## 阶段三：纯 HTTP 请求测试（必须全绿才能继续）

### 3.1 说明

完全不使用 SDK，只用 `requests` 库直接调用 REST API，验证接口的 HTTP 行为。  
这是独立于 SDK 的第二道验证，确保 endpoint 路径、请求字段、HTTP 方法、响应字段全部正确。

### 3.2 测试模板

```python
"""
纯 HTTP 测试：不依赖 SDK，验证接口 HTTP 行为
响应字段（从实际探测确认）：
  - 创建: id, subject, done, priority
  - 更新: result=True
  - 删除: result=True，删后 GET → 400
"""
import requests

BASE = "https://api.dingtalk.com/v1.0/xxx/users"

def _create(uid, headers, subject, **kwargs):
    r = requests.post(f"{BASE}/{uid}/items", params={"operatorId": uid},
                      headers=headers, json={"subject": subject, **kwargs}, timeout=15)
    assert r.status_code == 200, f"创建失败：{r.text}"
    d = r.json()
    assert "id" in d, f"缺少 id：{d}"   # 用探测到的实际字段名
    return d

def _delete(uid, headers, item_id):
    r = requests.delete(f"{BASE}/{uid}/items/{item_id}", params={"operatorId": uid},
                        headers=headers, timeout=15)
    assert r.status_code == 200, f"删除失败：{r.text}"
    return r.json()

def test_http_create_basic(union_id, api_headers):
    d = _create(union_id, api_headers, "[http] 基础创建")
    assert d["id"]
    _delete(union_id, api_headers, d["id"])

# 权限不足的接口 → 遇到 403 时 pytest.skip
def test_http_list(union_id, api_headers):
    r = requests.post(f"{BASE}/{union_id}/items/list", params={"operatorId": union_id},
                      headers=api_headers, json={"isDone": False}, timeout=15)
    if r.status_code == 403:
        pytest.skip(f"缺少权限 → {r.json().get('message','')[:100]}")
    assert r.status_code == 200
    assert "items" in r.json()  # 使用实际响应字段名
```

### 3.3 运行并确认全绿

```bash
uv run pytest dingtalk-<skill-name>/test_<module>.py -v
# ✅ 全部 PASSED/SKIPPED 才能继续（FAILED = 禁止进入阶段四）
```

---

## 阶段四：编写 SKILL.md + references/api.md

**只有阶段二和阶段三全部通过后才执行本阶段。**

### 4.1 目录结构

```
.agents/skills/dingtalk-<skill-name>/
├── SKILL.md
└── references/
    └── api.md
```

### 4.2 SKILL.md 模板

以 `dingtalk-message` 或 `dingtalk-todo` 的 SKILL.md 为范本，必须包含：

- **frontmatter**：`name` + `description`（触发关键词要全面）
- **工作流程**：读取配置 → 收集缺失 → 持久化 → 获取 Token → 执行操作
- **配置项表**：每个 `CONFIG` 键的来源说明。优先收集 `DINGTALK_MY_USER_ID`（企业员工 ID，管理后台通讯录可查，不是手机号也不是 unionId），如 API 需要 unionId 则由脚本自动转换
- **身份标识说明**：userId vs unionId 的区别，说明该技能的 API 使用哪种 ID，以及自动转换逻辑
- **执行脚本模板**：完整 bash 脚本（`create_file /tmp/<task>.sh` 再 `bash` 执行，禁止 heredoc），调用 `scripts/dt_helper.sh` 获取 token 和 unionId，无需内联 token 缓存或 id 转换逻辑：
  ```bash
    HELPER="<THE_SKILLMD_FILE_PATH>/scripts/dt_helper.sh"
  TOKEN=$(bash "$HELPER" --token)                    # 新版 token（带缓存）
  UNION_ID=$(bash "$HELPER" --to-unionid)            # 自动转换，如 API 需要 userId 则用 --get DINGTALK_MY_USER_ID
  USER_ID=$(bash "$HELPER" --get DINGTALK_MY_USER_ID)
  ```
- **详细参考**：指向 `references/api.md`，使用 grep 查阅索引模式

> 注意：不同 API 使用不同的用户 ID 类型。如消息 API 只接受 userId，待办 API 只接受 unionId。编写 SKILL.md 时需明确说明。

> **Skill 独立性原则**：每个 skill 是**完全独立**的——agent 加载某个 skill 时，只能看到这一个 skill 的 SKILL.md，**完全不知道其他 skill 的存在和内容**。因此：
> - 身份转换逻辑（userId → unionId）必须完整写入每个需要它的 skill 自己的 SKILL.md，不能引用其他 skill
> - 跨 skill 共享机制只有两种：`~/.dingtalk-skills/config`（配置文件）和 `scripts/dt_helper.sh`（工具脚本，由 `common_scripts_load.sh` 分发到每个 skill 的 `scripts/` 目录）
> - **bash 执行脚本直接调用 `scripts/dt_helper.sh`**，无需内联 token 缓存或 userId→unionId 转换逻辑
> - SKILL.md 中的说明文字（工作流程、配置项表、身份标识说明等）仍须完整、自包含——agent 只会读当前 skill 的 SKILL.md

### 4.3 references/api.md 规范

```markdown
# 钉钉 <功能> API 参考

每个接口包含：
- 完整请求体 JSON 示例（含必填标注）
- 实际响应 JSON 示例（从测试中截取）
- 错误响应示例（含状态码）
- curl 示例

## 错误码表

| HTTP 状态 | 错误码 | 说明 | 处理建议 |
```

---

## 阶段五：收尾更新

```bash
# 1. AGENTS.md 技能目录新增一行
# 2. README.md 技能列表新增一行（含安装命令和能力表）
# 3. README_EN.md 技能列表新增对应英文条目
# 4. tests/.env.example 补充新技能所需配置项（如有）
```


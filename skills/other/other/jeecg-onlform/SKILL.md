---
name: jeecg-onlform
description: >-
  JeecgBoot Online表单（cgform）全生命周期管理——通过API自动创建/编辑数据库表和表单配置，
  支持单表、主子表、树表，26种控件类型，以及JS/Java/SQL增强、权限配置、数据CRUD、积木报表集成。
  只要用户意图涉及「Online表单」就必须使用本技能，包括但不限于：
  创建或配置数据库表（"建一张请假表"、"创建online表"、"做一个带下拉选择的表"、"低代码表单"、"在线表单"、"配置表"）、
  修改已有Online表字段（"加个字段"、"改字段类型"、"加子表"、"删除字段"）、
  配置表单增强（"JS增强"、"自定义按钮"、"表单联动"、"Java增强"、"SQL增强"）、
  配置权限（"字段权限"、"按钮权限"、"数据权限"、"授权给角色"）、
  管理表单数据（"插入数据"、"查询记录"、"导出CSV"、"造测试数据"）、
  以及关联积木报表（"给这个表加报表"、"集成打印"）。
  即使用户只描述了业务需求而没说"online"（如"做一个员工信息管理功能，包含姓名、部门下拉、入职日期"），
  只要涉及元数据驱动的表单配置，也应触发本技能。
  注意：不要与「设计器表单」(desform)混淆——desform是拖拽式表单设计器，用skill jeecg-desform处理；
  也不要与「Online报表」(cgreport)或「Online图表」(onlchart)混淆——它们是SQL驱动的只读展示。
---

# JeecgBoot Online 表单 AI 自动生成器

将自然语言的表单需求描述转换为 Online 表单配置 JSON，并通过 API 在 JeecgBoot 系统中自动创建/编辑表单。

> **重要：本 skill 处理「Online 表单」（元数据驱动，运行时 CRUD），不涉及「设计器表单」（desform）。两者是完全独立的表单体系。**

## 选择正确的技能

| 用户需求 | 应使用的技能 |
|---------|------------|
| 元数据驱动的表/表单配置（字段定义、控件类型、数据库建表） | **本技能 (jeecg-onlform)** |
| 拖拽式可视化表单设计（自由布局、表单设计器） | jeecg-desform |
| SQL查询结果以**列表**展示 | jeecg-onlreport |
| SQL查询结果以**图形**展示（柱状图/饼图/折线图） | jeecg-onlchart |
| 复杂Excel样式报表（打印、分组、循环） | jimureport |

## 目录结构

```
scripts/
├── onlform_creator.py      # 表单创建/编辑（单表/主子表/树表）
├── onlform_jimureport.py   # 积木报表集成（创建/删除报表并关联）
├── onlform_enhance.py      # JS/Java/SQL增强 + 自定义按钮
├── onlform_auth.py         # 权限配置（字段/按钮/数据权限）
├── onlform_data.py         # 数据 CRUD（增删改查/树数据/导出CSV）
└── onlform_menu.py         # 菜单挂载 + 路由缓存 + 角色授权

templates/                  # ⚡ 可直接复用的 JSON 模板（优先读取，不要现场设计）
└── all_controls_master_sub.json  # 全控件主子表（26种控件，主表+一对多+一对一）
                                  # ⚠️ 模板内的表名仅为占位符，创建时必须按业务语义自定义表名，不能原样照用

references/
├── onlform-field-types.md  # 字段类型/控件/字典/校验/默认值/扩展配置
├── onlform-widget-types.md       # 控件速查表（fieldShowType 完整清单）
├── onlform-head-field-types.md   # head 级字段说明（tableType/themeTemplate 等）
├── onlform-full-widget-template.md # 26种控件配置速查（dictTable/dictField/fieldExtendJson）
├── onlform-enhance-js.md   # JS增强参考（onlChange/loaded/列表拦截/API，~310行）
├── onlform-enhance-java.md # Java增强参考 + 实战案例（~140行）
├── onlform-enhance-misc.md # SQL增强/自定义按钮/fieldHref/实战（~130行）
├── onlform-auth.md         # 权限配置（字段/按钮/数据权限 API）
├── onlform-data-crud.md    # 数据 CRUD API + 存储格式
├── onlform-jimureport.md   # 积木报表集成 8 步流程
├── onlform-misc.md         # 杂项：表类型/布局/BPM/视图/错误处理
├── onlform-api-reference.md # 完整 JSON 数据结构和字段枚举
└── onlform-route-cache.md  # 路由缓存配置（动态/静态路由、组件名称映射）
```

## 前置条件

用户必须提供以下信息（或由 AI 引导确认）：

1. **API 地址**：JeecgBoot 后端地址（如 `https://boot3.jeecg.com/jeecgboot`）
2. **X-Access-Token**：JWT 登录令牌（从浏览器 F12 获取）

## 执行效率规则（减少无谓等待）

所有 HTTP 调用必须遵循，否则用户会感到响应明显变慢。**本节为强制要求，违反会直接被用户吐槽"太慢了"。**

### 0. Windows 环境下**必须**用 PowerShell tool 跑 python（最容易踩的坑）

**现象**：Windows 的 Bash tool 会把 `python` / `python -c` / skill 脚本当作长命令自动 `run_in_background`，tool 立即返回一个 background ID，真正的执行输出要等系统通知才到——把毫秒级调用放大到数秒，用户会立即感到"卡"。

**规则**：
- **Windows（platform=win32）** → 所有 python 调用（skill 脚本 + `python -c` 探测）都用 **PowerShell tool**，不要用 Bash tool。
- **Linux / macOS（platform=linux/darwin）** → 用 Bash tool 即可，python 不会被后台化。
- `curl` 在任何平台都不用——跨平台不一致，且 Windows Bash 下同样被后台化。

**Windows 正确示例**：
```
PowerShell: python C:/path/to/onlform_creator.py --api-base http://localhost:8080 --token xxx --config config.json
PowerShell: python -X utf8 -c "import urllib.request as u, json; r=u.urlopen(...); print(r.read().decode())"
```

**Windows 错误示例**（会被后台化）：
```
Bash: python onlform_creator.py ...       ← 会返回 "Command running in background"
Bash: python -c "..."                     ← 同上
Bash: curl -X POST ...                    ← 同上
```

> **历史教训**：本 skill 早期版本错误地声称"Python 在所有 shell 下都同步返回"——实测 Windows Bash tool 对 python 也会后台化。曾因此被用户连续吐槽"执行太慢了"。

> **Windows 中文编码规则（`python -c` 必须加 `-X utf8`）**：
> PowerShell 默认编码为 UTF-16 LE，`python -c "..."` inline 代码中含中文字面量时，shell 传参过程会乱码，导致 `SyntaxError: unterminated string literal`。
> - **解法**：始终用 `python -X utf8 -c "..."` 而不是 `python -c "..."`
> - **含中文的复杂逻辑**：写入临时 `.py` 文件再执行，彻底避免 inline 中文
> - **结果含中文的 print**：在 inline 脚本开头加 `import sys; sys.stdout.reconfigure(encoding='utf-8')`

### 1. 并行读取 reference 文件，不要串行

需要多个 reference 文件时，在**同一条消息**中并发发出所有 Read 调用，不要一个读完再读下一个。

```
// ✅ 正确：一条消息同时 Read 多个文件（并发）
Read(onlform-field-types.md) + Read(onlform-master-detail-checklist.md) + Read(onlform-enhance-js.md)

// ❌ 错误：串行读取
Read(field-types) → 等结果 → Read(checklist) → 等结果 → Read(enhance)
```

> **常用并发组合**：建表 → 同时读 `field-types.md` + `master-detail-checklist.md`；JS增强 → 同时读 `enhance.md`（若已在建表时读过则跳过）。

### 2（原1）. 优先用 skill 自带的 Python 脚本，不要自己另起 HTTP 封装

skill 已提供 `onlform_creator.py` / `onlform_jimureport.py` 等脚本，它们封装了鉴权、重试、head 解析、主子表关联等细节。需要一次性 HTTP 探测再用 `python -c`。

### 3（原2）. 跳过非必要前置检查，直接跑脚本

- **表名查重**：仅在"用户暗示要复用已有表 / 表名看上去像已有资源"时才查。普通新建场景直接跑 `onlform_creator.py`——遇重名接口会返回明确错误，预查反而增加一次往返。`onlform_creator.py` 已内置自动加 `_1`/`_2` 后缀重试，主表冲突无需手动干预。
- **字典存在性**：以下系统内置字典**直接使用，禁止发 API 查询**，值已固化：

  | 字典编码 | 值 → 含义 | 控件类型 |
  |---------|----------|---------|
  | `yn` | `1`=是 / `0`=否 | list / radio / switch |
  | `sex` | `1`=男 / `2`=女 | list / radio |
  | `valid_status` | `1`=有效 / `0`=无效 | list / radio |
  | `priority` | `L`=低 / `M`=中 / `H`=高 | list / radio |
  | `bpm_status` | `1`=待提交 / `2`=审批中 / `3`=审批通过 / `4`=审批拒绝 | list |

  仅在字典编码**明显是业务自定义**且不确定是否创建过时才发 `sys/dict/list` 查询。

- **❌ 严禁拼造 `/sys/dict/queryDictItemsByCode/{code}` 这种 RESTful 风格的字典查询路径**：后端根本没有这个端点，会返回 `"路径不存在，请检查路径是否正确"`。
  - 正确的「按 dictCode 直接拿字典项」接口是 `GET /sys/api/queryDictItemsByCode?code={dictCode}`（`code` 走 query 串，不是 path variable）。
  - 但对上表中的内置字典，**仍然不要调用任何接口**——直接用固化值。
  - 业务自定义字典优先走 `sys/dict/list?dictCode=xxx` + `sys/dictItem/list?dictId={id}` 两步法（见 `references/onlform-data-crud.md`）。

- **link_table 引用表存在性**：这项仍然必须查（见 `references/onlform-field-types.md`），引用不存在的表会让创建成功但运行时报错，排查成本高。

### 4（原3）. 并行多个 GET 检查时，一个 Python 调用里顺序打完，不要拆成多条 shell

一次 tool call 拿到所有结果；拆成多条 shell 既有进程启动开销，在 Windows 下还会被后台化。
```python
# 用 shell tool 跑（Windows: PowerShell，Linux/macOS: Bash）
python -c "
import urllib.request as u, json
h = {'X-Access-Token':'<token>'}; base = 'http://host'
def g(p): return json.loads(u.urlopen(u.Request(base+p, headers=h), timeout=10).read())
dup = g('/sys/duplicate/check?tableName=onl_cgform_head&fieldName=table_name&fieldVal=xxx')
dct = g('/sys/dict/list?dictCode=xxx')
print('dup=', dup.get('result'), '; dict.total=', dct.get('result', {}).get('total'))
"
```

### 5（原4）. API base 确认（避免"路径不存在"返工）

JeecgBoot 后端的 context path 因部署而异：
- 较老版本 / 标准部署：`http://host:port/jeecg-boot`
- 较新版本 / 根路径部署：`http://host:port`（无 `/jeecg-boot` 后缀）

**首次不确定时**：直接按用户给的原样用。如果 `onlform_creator.py` 返回 `"路径不存在，请检查路径是否正确"`，去掉 `/jeecg-boot` 重试一次（或反之）——这个错误是确定性的，不要改别的参数。

**「路径不存在」也可能是接口路径本身写错了**（context path 没问题，但端点本身后端没有）。常见反例：
- ❌ `/sys/dict/queryDictItemsByCode/{code}` —— 路径 + 风格全错，后端没有这个端点
- ✅ 正确：`GET /sys/api/queryDictItemsByCode?code={code}`（注意是 `/sys/api`，参数走 query）

排查顺序：先按 context path 加/去 `/jeecg-boot` 重试；仍然 404 时，回到 SKILL 文档/references 里复核接口路径——**不要凭印象拼 RESTful 风格的 URL**。

### 6. 编辑前查字段顺序：直接用 `listByHeadId`，禁止其他接口

> **历史教训**：曾因依次试错 `field/list`（返回跨表乱序垃圾）→ 读脚本源码 → `getByHead`（返回空）→ 才到 `listByHeadId`，浪费了 4 次往返，被用户吐槽"不应该 30s 就搞定吗"。

**强制规则（新增/删除/修改字段前获取现有字段时必须遵守）：**

- ✅ 唯一正确接口：`GET /online/cgform/field/listByHeadId?headId={headId}`
- ❌ 禁止用 `field/list`——不带 `cgformHeadId` 过滤时会返回所有表的混合数据
- ❌ 禁止用 `getByHead`——实测返回空 fields
- ❌ 禁止为了查接口用法去读 `onlform_creator.py` 源码——直接用上面的接口即可

**多表并行查询（一次 shell tool 调用，不要串行；Windows: PowerShell，Linux/macOS: Bash）：**
```python
for tbl, hid in [('t1','id1'), ('t2','id2')]:
    req = u.Request(base + '/online/cgform/field/listByHeadId?headId=' + hid, headers=h)
    fields = json.loads(u.urlopen(req, timeout=10).read()).get('result', [])
    # 按 orderNum 排序后直接使用
    fields.sort(key=lambda f: f.get('orderNum', 999))
```

### 7. 建表时必须加日期后缀，避免冲突重试链

> **历史教训**：`dept_info` 冲突 → 改名 dept_info_1 → 子表再次冲突 → 再改名 → 额外更新 subTableStr，三步重试链浪费 ~50s。

**强制规则：** 从用户描述推导业务表名后，立即拼上当日日期后缀再写入 config JSON，无需查重，直接创建。

```
# 格式：业务名_YYYYMMDD
dept_info_20260509      ← 主表
dept_archive_20260509   ← 一对一子表
dept_employee_20260509  ← 一对多子表
```

- 日期后缀保证全局唯一，彻底跳过自动重试逻辑
- 子表同步加后缀，保持命名一致性
- 完成后在汇总中告知用户实际表名

### 8. 所有临时 JSON 配置在一个 Python 脚本里批量写入

> **历史教训**：3 个 JSON 文件拆成 3 次 Write tool call，每次有固定开销，合计浪费 ~12s。

**强制规则：** 多个临时 JSON 配置必须在**同一个 Python 脚本**里批量写入，禁止逐个调用 Write tool。用 Python 的 `json.dump` 写文件——跨平台一致，无 BOM 风险。

```python
# 正确：在同一个 Python 脚本里批量写入多个 JSON（跨平台）
import tempfile, json, os, subprocess

tmp = tempfile.gettempdir()  # 自动适配 Windows %TEMP% / Linux /tmp / macOS /var/folders/.../T
CREATOR = r'<skill目录>/scripts/onlform_creator.py'

configs = {
    'onl_main.json':  {"action": "create", "tables": [{"tableName": "...", ...}]},
    'onl_sub1.json':  {"action": "create", "tables": [{"tableName": "...", ...}]},
}
paths = {}
for fname, cfg in configs.items():
    path = os.path.join(tmp, fname)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, ensure_ascii=False)
    paths[fname] = path

# 依次调用 onlform_creator.py
for path in paths.values():
    subprocess.run(['python', CREATOR, '--api-base', BASE, '--token', TOKEN, '--config', path], check=True)
```

### 9. 字段编辑"查询 + 生成配置 + 执行"合并为 1 个 Python 脚本

> **历史教训**：查 orderNum → Write tool 写 JSON → 再调用 creator，拆成 3 步 tool call 浪费 ~10s。

**强制规则：** 编辑字段时，把 listByHeadId 查询、edit config 生成、写临时文件、调用 creator 全部写进**一个 Python 脚本**，在单次 shell tool call（Windows: PowerShell，Linux/macOS: Bash）里跑完。

```python
# 模板：查询 → 生成 config → 写文件 → 调用 creator（一个脚本搞定）
import subprocess, json, os, tempfile
import urllib.request as u

# 1. 查询现有字段
fields = query_fields(head_id)

# 2. 在内存中构建 edit config（无需 Write tool）
cfg = {"action": "edit", "tableName": tname, "addFields": [...], "modifyFields": [...]}
path = os.path.join(tempfile.gettempdir(), f'onl_edit_{tname}.json')
with open(path, 'w', encoding='utf-8') as f:
    json.dump(cfg, f, ensure_ascii=False)

# 3. 直接调用 creator
subprocess.run(['python', '-X', 'utf8', CREATOR, '--api-base', BASE, '--token', TOKEN, '--config', path], check=True)
```

### 10. 多表编辑必须用 `tables: []` 并行 + 单表 add/modify 一次提交（节省 ~20s）

> **历史教训**：曾分两轮编辑 3 张表 = 6 次串行 `subprocess.run(creator)`。每次 creator 启动 ~1s + addAll/syncDb HTTP 各 ~1s ≈ 共 18-25s。三个症状叠加：
> 1. 同一张表的 `addFields`（新增）和 `modifyFields`（重排）拆成两轮调用 → HTTP/syncDb 翻倍
> 2. 多张表的 edit 串行 spawn 子进程 → 表数 × Python 冷启动
> 3. 每次都重新 import 模块 → Windows 上每次 ~800ms 启动开销

**强制规则（多表/复合编辑必须遵守）：**

1. **同一张表的所有变更合并为一次 editAll**：`addFields` + `modifyFields` + `deleteFields` 写在同一个 config，creator 内部一次提交即完成。

   > ⚠️ **addFields 的 orderNum 不被后端采纳——新字段始终追加到末尾（实测）。**
   > 同一次 editAll 里 `modifyFields` 只对已存在字段生效，对同批 `addFields` 新建的字段无效。
   > **教训来源**：2026-05-09 给员工子表插入 `sex` 字段，指定 `orderNum=9` 并在 `modifyFields` 里后移 `id_card/phone`，结果 `sex` 仍追加到末尾（orderNum=11），需第二次单独 `modifyFields` 才修正。

   **插入到中间位置的正确两步法：**
   - **第一步**：`addFields` 创建字段（orderNum 随便填，后端忽略，字段追加到末尾）；`modifyFields` 里只后移已有字段
   - **第二步**：单独再跑一次 `modifyFields`，把新建字段的 orderNum 设到目标位置

   ```python
   # 第一步：创建字段 + 后移已有字段（新字段 orderNum 会被忽略，先追加到末尾）
   cfg1 = {"action":"edit","tableName":"t","addFields":[{"dbFieldName":"sex",...}],
           "modifyFields":[{"dbFieldName":"id_card","orderNum":10},{"dbFieldName":"phone","orderNum":11}]}
   # 第二步：修正新字段的 orderNum（必须在第一步完成后执行）
   cfg2 = {"action":"edit","tableName":"t","modifyFields":[{"dbFieldName":"sex","orderNum":9}]}
   ```

2. **多表编辑用顶层 `tables: []`**：`onlform_creator.py` 的 `action: "edit"` 现在支持 `tables` 数组，会用线程池并发执行 N 张表的编辑。表数 ≥ 2 时**必须**用此格式，不要写 N 个单表 config 串行 spawn。

```python
# ✅ 正确：一次 creator 调用，N 张表并行
cfg = {"action": "edit", "tables": [
    {"tableName": "t1", "addFields": [...], "modifyFields": [...]},
    {"tableName": "t2", "addFields": [...]},
    {"tableName": "t3", "modifyFields": [...]}
]}
subprocess.run(['python', '-X', 'utf8', CREATOR, '--api-base', BASE, '--token', TOKEN, '--config', path], check=True)

# ❌ 错误：串行 spawn 3 次 creator
for cfg in [cfg1, cfg2, cfg3]:
    subprocess.run([..., '--config', path], check=True)  # 每次 ~3-5s

# ❌ 错误：同一张表 add 一轮、reorder 一轮
subprocess.run([..., '--config', add_only_config])    # 第一轮：add
subprocess.run([..., '--config', reorder_only_config]) # 第二轮：reorder（多余的 syncDb）
```

**收益**：3 张表的「add + reorder」从 6 次 creator 调用（~25s）降到 1 次（~5s）。

### 11. 自定义字典用 batchAddDictWithItems 一次搞定

> **历史教训**：早期用 `dict/add` + `dictItem/add` 逐条写入，遇到 `result=null` 时还会 TypeError 崩溃触发重跑。实际上 JeecgBoot 有批量接口，1 次 HTTP 完成所有字典+items，且内置"已存在跳过"逻辑。

**接口**：`POST /sys/dict/batchAddDictWithItems`

- 请求体：`{"dictList": [{...}, {...}]}`，每项含 `sysDictItemList`
- 已存在的字典编码自动跳过（服务端 catch 唯一约束异常），不影响其他字典
- 返回：`{"successCount": N, "failureCount": M, "failureList": [...]}`

```python
def ensure_dicts_batch(base, token, dicts):
    """
    dicts = [
      {"dictName":"订单类型","dictCode":"order_type","description":"...","items":[("国内","1",1),...]},
      ...
    ]
    """
    payload = {"dictList": [
        {
            "dictName": d["dictName"],
            "dictCode": d["dictCode"],
            "description": d.get("description", ""),
            "sysDictItemList": [
                {"itemText": t, "itemValue": v, "sortOrder": o, "status": 1}
                for t, v, o in d["items"]
            ]
        }
        for d in dicts
    ]}
    H = {'X-Access-Token': token, 'Content-Type': 'application/json'}
    body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(base + '/sys/dict/batchAddDictWithItems', data=body, headers=H, method='POST')
    r = json.loads(urllib.request.urlopen(req, timeout=15).read().decode('utf-8'))
      # ⚠️ 全部已存在时接口返回 success=false + code 500，需判断 failList 区分"真失败"和"已存在跳过"
    result = r.get('result') or {}
    fail_list = result.get('failList') or []
    real_fails = [f for f in fail_list if '已经存在' not in f.get('errorMsg', '')]
    if real_fails:
        raise RuntimeError(f'字典创建失败: {real_fails}')
    skip_count = len([f for f in fail_list if '已经存在' in f.get('errorMsg', '')])
    print(f'  字典批量: 新建={result.get("successCount",0)}, 已存在跳过={skip_count}')
    return r

# 调用示例（N 个字典 1 次 HTTP）
ensure_dicts_batch(BASE, TOKEN, [
    {"dictName":"订单类型",  "dictCode":"order_type",    "description":"国内/国际",    "items":[("国内","1",1),("国际","2",2)]},
    {"dictName":"运输方式",  "dictCode":"transport_mode", "description":"运输方式(全量)","items":[("陆运","land",1),("铁运","rail",2),("空运","air",3),("海运","sea",4)]},
])
```

> ⚠️ **接口行为陷阱（实测）**：全部字典已存在时，接口返回 `success=false` + `code=500`，而不是静默跳过。
> 判断方式：遍历 `result.failList`，`errorMsg` 含"字典编码已经存在"的视为正常跳过，其余才是真失败。

**收益**：N 个字典 + M 个 items 从 `1+N×M` 次 HTTP → **1 次 HTTP**，无 result=null 防御问题。

### 5. 建表遇到「数据库表 [xxx] 已存在」时的处理

错误 `数据库表[xxx]已存在,请从数据库导入表单` 表示：**物理 DB 表残留，但 Online 配置不存在**（通常是之前创建后被手动删了 Online 头）。

> **`onlform_creator.py` 和 `onlform_pipeline.py` 已内置自动加后缀重试**，并自动更新关联子表的 `mainTable` 引用。主表冲突无需手动干预，脚本会自动完成。执行后在汇总输出中确认实际使用的表名即可。


1. **首选：换表名**（在 config 中指定新名称）——最快，避免污染现有物理表。
2. **次选：导入**：`GET /online/cgform/head/transTables/{tableName}` 把物理表导入为 Online 配置，再用 `action=edit` 调整字段。
3. **慎用：删除物理表**（通过 DB 直连 DROP TABLE）——只在确认无数据且用户明确要求时做。

> **主子表场景特别注意**：主表建失败且脚本未自动重试时，子表如果已创建会成为"孤儿"。此时先 `DELETE /online/cgform/head/delete?id={孤儿子表headId}` 删干净，再整体重建。

## 主数据复用规则

> **重要：** 配置表单字段的字典、用户选择、部门选择等数据源时，必须遵循"先查后建"原则。
> 使用 `jeecg-system` skill 的 `system_utils.py` 查询和管理主数据。

## 临时配置文件规则（强制）

所有传给脚本的 `--config <xxx.json>` 必须写到**系统临时目录**，由 OS 自动清理；skill 和脚本都不主动 `rm`。

```python
import tempfile, os, json
config_path = os.path.join(tempfile.gettempdir(), 'onl_<表名>_<步骤>.json')
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(cfg, f, ensure_ascii=False, indent=2)
```

`tempfile.gettempdir()` 自动适配：Windows `%TEMP%` / Linux `/tmp` / macOS `/var/folders/.../T`（注意 macOS 不是 `/tmp`）。命名建议带表名+步骤前缀（如 `onl_sk_audit_create.json`）便于排错。

**❌ 禁止：**
- 写到 `<skill>/tmp/` 或当前工作目录（污染 skill / 用户项目）
- 硬编码 `/tmp` / `C:\Temp`（不跨平台）
- 每步完成后主动 `rm` / `Remove-Item`（OS 会清，多余 tool call）
- **主动 `os.path.exists()` 检查**（自身就是一次 tool call）

**临时文件可能被 OS 异步清理**，但**乐观调用 + 报错再补救**：仅当脚本返回 `FileNotFoundError` / `配置文件不存在` 时，用相同内容重写后重试，不要换路径或去 skill 目录找。

## 交互流程

### Step 0: 判断操作类型

| 用户意图关键词 | 操作类型 | 使用脚本 |
|---------------|---------|---------|
| 创建/新建/做一个/生成 | 新增表单 → Step 1A | `onlform_creator.py` |
| 加字段/增加字段/修改字段/删除字段 | 编辑表单 → Step 1B | `onlform_creator.py` |
| 集成积木/关联打印/打印报表 | 积木报表集成 → Step 8 | `onlform_jimureport.py` |
| JS增强/按钮/增强功能 | 增强配置 → Step 9 | `onlform_enhance.py` |
| 权限/授权/数据规则 | 权限配置 → Step 10 | `onlform_auth.py` |
| 造数据/插入/查询/导出 | 数据操作 → Step 11 | `onlform_data.py` |
| 挂载菜单/加到菜单/预览地址/缓存路由 | 菜单挂载 → Step 12 | `onlform_menu.py` |

### Step 1A: 新增表单 — 解析需求

从用户描述中提取：

| 信息 | 默认值 | 示例 |
|------|--------|------|
| 表名 (tableName) | 自动生成 snake_case | `leave_application` |
| 表描述 (tableTxt) | 用户指定 | "请假申请" |
| 表类型 (tableType) | 1=单表 | 提到"主子表"→2/3，提到"树形"→1+isTree |
| 字段列表 | 从描述中解析 | 姓名(必填)、请假天数(数字)、日期(范围查询) |

**判断表类型：**
- 提到"分类/层级/树/上下级" → **树表** (tableType=1, isTree='Y')
- 提到"主子表/明细/一对多/订单+商品" → **主子表** (主表 tableType=2, 子表 tableType=3)，**默认使用 normal 风格**（不使用 erp），除非用户明确指定
- 默认 → **单表** (tableType=1)

> **使用全控件模板（all_controls_master_sub.json）时：** 读取模板作为结构参考，但表名（tableName/tableTxt）必须根据用户的业务描述重新命名，不能使用模板中的占位符表名。

> **创建前不要查重表名。** `addAll` 接口本身会校验并返回明确的重复提示，提前查重是多余的网络开销。
>
> **遇到重名错误（`数据库表[xxx]已存在`）时的处理规则：**
>
> | 当前操作 | 处理方式 |
> |---------|---------|
> | **新建表单**（用户意图是创建一个新表） | **自动加后缀重试**：`xxx` → `xxx_1` → `xxx_2` …，直到成功；执行成功后告知用户实际使用的表名 |
> | **修改/编辑表单**（用户意图是改已有表） | 切换到 editAll 流程 |
> | **导入数据库已有表** | 调用 `transTables/{tableName}` 导入 |
>
> ❌ **绝对不能删除已有表**（`DELETE /online/cgform/head/delete`）来"让位"给新建——这会丢失已有数据和配置。删除只能在用户**显式要求**删除时执行。

**字典字段配置易错点（必须注意）：**
- **下拉框/多选框/单选框/下拉多选/下拉搜索 这 5 种控件必须配置数据字典或表字典**，否则没有选项无法使用。生成字段配置时，遇到这 5 种控件必须同时配置 dictField（数据字典）或 dictTable+dictField+dictText（表字典）。
- 数据字典（系统字典/字典编码）：只填 `dictField`（字典编码，如 `sex`、`education`），`dictTable` 和 `dictText` 留空。**绝对不能**把 `dictTable` 设为 `sys_dict_item`。
- 表字典：`dictTable` 填业务表名（如 `sys_user`，也可以填 Online 创建的表），`dictField` 填存储值字段，`dictText` 填显示文本字段。
- 使用的字典编码不存在时，需先通过 `sys/dict/list?dictCode=xxx` 查询，不存在则通过 `sys/dict/add` + `sys/dictItem/add` 创建（先查后建）。

### Step 1B: 编辑表单 — 查询现有配置

1. 用户提供表单 ID 或表名
2. 查询表名获取 headId：`GET /online/cgform/head/list?tableName={表名}&pageNo=1&pageSize=1`
3. **查询现有字段（必须用 `listByHeadId`，见效率规则第6条）**：
   `GET /online/cgform/field/listByHeadId?headId={headId}`
   返回结果按 `orderNum` 排序，确认需要插入的前后字段的 orderNum 值
4. 根据用户需求进行增/删/改字段，直接写配置跑脚本

> **多表编辑 / 增删改一次提交**（见效率规则第10条）：涉及多张表时用 `tables: []` 一次配置并行执行；同一张表的 `addFields` + `modifyFields` 必须放在同一个 config（一次 editAll 内全做完，避免 add 一轮、reorder 一轮的双往返）。

**单表编辑 + 重排同时进行的 JSON 示例（一次完成）：**
```json
{
  "action": "edit",
  "tableName": "dept_employee",
  "addFields": [
    {"dbFieldName": "sex", "dbFieldTxt": "性别", "fieldShowType": "radio",
     "dbType": "string", "dbLength": 2, "dictField": "sex", "orderNum": 9}
  ],
  "modifyFields": [
    {"dbFieldName": "id_card", "orderNum": 10},
    {"dbFieldName": "phone",   "orderNum": 11}
  ]
}
```

**多表并行编辑 JSON 示例（creator 自动用线程池并发）：**
```json
{
  "action": "edit",
  "tables": [
    {"tableName": "dept_info",     "addFields": [...], "modifyFields": [...]},
    {"tableName": "dept_archive",  "addFields": [...]},
    {"tableName": "dept_employee", "addFields": [...], "modifyFields": [...]}
  ]
}
```

### Step 2-4: 智能字段推导

> **详细字段类型映射、字典配置、校验规则、默认值、扩展配置、特殊控件配置参见：**
> `references/onlform-field-types.md`

> **⚠️ link_table（关联记录）前置检查（必须执行）：**
> 配置 `link_table` 字段时，`dictTable` 只能引用 **Online 管理的业务表**，不能是系统表。
> 必须先调用 `GET /online/cgform/head/list?tableName={表名}&pageNo=1&pageSize=1` 验证被关联表是否存在。
> - 若不存在 → 先创建该 Online 表并同步数据库，再插入至少 3 条示例数据，然后再配置 link_table 字段。
> - 若已存在 → **继续执行列名验证（必须）**：调用 `GET /online/cgform/api/getColumns/{headId}` 查出实际列名列表，用真实列名覆盖模板/假设中的 `dictText` 字段值，不能凭猜测或模板占位符直接使用。
>
> **教训**：仅检查表存在还不够——模板里的 `dictText: "user_code,phone"` 与目标表实际列 `name/age/sex/birthday` 完全不同，导致运行时报 `Unknown column 'user_code' in 'field list'`。
> 详细说明见 `references/onlform-field-types.md` 的 `link_table` 小节。

核心映射速查：

| 关键词 | fieldShowType | dbType |
|--------|-------------|--------|
| 文本 | `text` | string |
| 备注 | `textarea` | string |
| 日期 | `date` | Date |
| 下拉 | `list` | string |
| 单选 | `radio` | string |
| 多选 | `checkbox` | string |
| 开关 | `switch` | string |
| 图片 | `image` | string |
| 文件 | `file` | string |
| 用户选择 | `sel_user` | string |
| 部门选择 | `sel_depart` | string |
| 省市区 | `pca` | string |
| 富文本 | `umeditor` | Text |

### Step 5: 展示摘要并确认

**必须展示配置摘要，等待用户确认后再执行。** 这一步至关重要——字段配置一旦创建后修改成本较高（需要逐个编辑），提前确认能避免返工。摘要需包含：
- 表名、表描述、表类型
- 6 个标准系统字段
- 所有业务字段（序号、字段名、标签、控件类型、DB类型、必填、查询、字典）
- 合计字段数

### Step 6-7: 生成配置 JSON 并调用脚本

**使用 `scripts/onlform_creator.py`（推荐方式）：**

```bash
python <skill目录>/scripts/onlform_creator.py --api-base <URL> --token <TOKEN> --config <config.json>
```

**单表创建 JSON 示例：**
```json
{
  "action": "create",
  "tables": [{
    "tableName": "leave_application",
    "tableTxt": "请假申请表",
    "tableType": 1,
    "fields": [
      {"dbFieldName": "name", "dbFieldTxt": "姓名", "fieldShowType": "text", "dbType": "string", "dbLength": 100, "fieldMustInput": "1", "isQuery": 1}
    ]
  }]
}
```

**编辑表单 JSON 示例：**
```json
{
  "action": "edit",
  "tableName": "test_demo",
  "addFields": [{"dbFieldName": "new_field", "dbFieldTxt": "新字段", "fieldShowType": "text", "dbType": "string", "dbLength": 100}],
  "deleteFields": ["old_field"],
  "modifyFields": [{"dbFieldName": "existing_field", "dbFieldTxt": "修改后标签", "dbLength": 200}]
}
```

> **主子表、树表的完整 JSON 配置示例参见：** `references/onlform-misc.md`

### Step 8: 积木报表集成

**使用 `scripts/onlform_jimureport.py`：**

```bash
python <skill目录>/scripts/onlform_jimureport.py --api-base <URL> --token <TOKEN> --config <config.json>
```

**配置 JSON 示例：**
```json
{
  "action": "create_report",
  "tableName": "customer",
  "reportName": "客户表打印",
  "fields": [
    {"fieldName": "customer_name", "fieldText": "客户名称"},
    {"fieldName": "phone", "fieldText": "联系电话"}
  ]
}
```

脚本自动完成 8 步：创建报表 → 保存空模板 → 解析字段 → 检查编码 → 保存数据源 → 获取模板 → 写入引用 → 关联表单。

> **前提条件**：Online 表中至少存在一条记录，否则字段解析不出来。
> **积木报表 API 详细说明参见：** `references/onlform-jimureport.md`

### Step 9: 增强配置

**使用 `scripts/onlform_enhance.py`：**

```bash
python <skill目录>/scripts/onlform_enhance.py --api-base <URL> --token <TOKEN> --config <config.json>
```

支持的操作：
- `create_buttons` — 创建自定义按钮（button/link/form 样式）
- `save_js` — 保存 JS 增强（form/list 类型）
- `save_java` — 保存 Java 增强（spring-key/java-class/http-api）
- `save_sql` — 保存 SQL 增强
- `query` — 查询所有增强配置

> **增强参考（按需读对应文件）：** JS增强 → `references/onlform-enhance-js.md`；Java增强 → `references/onlform-enhance-java.md`；SQL/按钮 → `references/onlform-enhance-misc.md`

### Step 10: 权限配置

**使用 `scripts/onlform_auth.py`：**

```bash
python <skill目录>/scripts/onlform_auth.py --api-base <URL> --token <TOKEN> --config <config.json>
```

支持的操作：
- `setup_field_auth` — 配置字段权限（列表可见/表单可见/表单可编辑）
- `setup_button_auth` — 配置按钮权限
- `setup_data_auth` — 配置数据权限规则
- `grant_role` — 授权给角色/部门/用户
- `query` — 查询所有权限配置

> **权限配置详细参考参见：** `references/onlform-auth.md` 和 `references/onlform-misc.md`

### Step 11: 数据操作

**使用 `scripts/onlform_data.py`：**

```bash
python <skill目录>/scripts/onlform_data.py --api-base <URL> --token <TOKEN> --config <config.json>
```

支持的操作：
- `insert` — 插入数据（单表/主子表）
- `insert_tree` — 插入树表数据（自动父先子后）
- `query` — 查询数据列表（带过滤）
- `query_tree` — 查询树表数据
- `get` — 查询单条记录
- `update` — 更新记录（自动全量合并）
- `delete` — 删除记录
- `export_csv` — 导出 CSV

> **数据 CRUD API 和存储格式详细参考参见：** `references/onlform-data-crud.md`

---

## 所有脚本通用参数

| 参数 | 说明 |
|------|------|
| `--api-base` | JeecgBoot 后端地址（如 `http://localhost:8080/jeecg-boot`） |
| `--token` | X-Access-Token |
| `--config` | JSON 配置文件路径 — **必须写到系统临时目录**，详见上文「临时配置文件规则」 |

所有脚本支持 `tableName` 自动解析 `headId`，无需手动查询。

## 参考文档索引（按需读取）

| 文档 | 何时读取 |
|------|---------|
| [onlform-field-types.md](references/onlform-field-types.md) | 需要确定控件类型(fieldShowType)、字典配置、校验规则、默认值表达式、扩展配置(fieldExtendJson)时——创建/编辑表单字段必读 |
| [onlform-enhance-js.md](references/onlform-enhance-js.md) | JS增强：onlChange联动、loaded初始化、beforeSubmit校验、列表拦截、显隐禁用时 |
| [onlform-enhance-java.md](references/onlform-enhance-java.md) | Java增强（spring/class/http）、导入增强时 |
| [onlform-enhance-misc.md](references/onlform-enhance-misc.md) | SQL增强、自定义按钮、按钮表达式、fieldHref超链接时 |
| [onlform-auth.md](references/onlform-auth.md) | 用户要求配置字段权限、按钮权限、数据权限、或给角色授权时 |
| [onlform-data-crud.md](references/onlform-data-crud.md) | 需要插入/查询/更新/删除表单数据、导出CSV时——确认各控件的值格式必读 |
| [onlform-jimureport.md](references/onlform-jimureport.md) | 用户要求关联积木报表或集成打印功能时 |
| [onlform-master-detail-checklist.md](references/onlform-master-detail-checklist.md) | **创建主子表时必读**——subTableStr / mainTable / mainField / 外键字段三项必填清单，缺任何一项关联失效 |
| [onlform-misc.md](references/onlform-misc.md) | 处理head级配置(extConfigJson)、主子表/树表JSON结构、BPM集成、视图配置、表单布局(formTemplate)时 |
| [onlform-api-reference.md](references/onlform-api-reference.md) | 需要查看addAll完整请求体模板、head字段枚举、系统默认字段时 |
| [onlform-route-cache.md](references/onlform-route-cache.md) | 用户要求开启Online表单路由缓存(keepAlive)、配置菜单组件名称、或询问动态/静态路由配置时 |

### Step 12: 菜单挂载 + 路由缓存（**可选 · 不自动执行**）

> **本步骤非必须。** 表单/流程创建完成后**不要**默认执行菜单挂载。先用一句话询问用户："是否需要挂载到菜单？" 用户明确确认后再执行。
> 用户可以直接通过预览 URL 访问表单，或自行在系统设置中挂载。演示环境账号通常无菜单创建权限，强行执行会失败。

**使用 `scripts/onlform_menu.py`：**

```bash
python <skill目录>/scripts/onlform_menu.py --api-base <URL> --token <TOKEN> --config <config.json>
```

支持的操作：
- `mount` — 挂载单个 Online 表单到菜单（自动推导预览地址和组件名称，可选开启缓存、授权角色）
- `mount_batch` — 批量挂载多个表
- `enable_cache` — 为已有菜单开启路由缓存

**挂载菜单 JSON 示例：**
```json
{
  "action": "mount",
  "tableName": "test_order_main",
  "menuName": "测试订单主表",
  "keepAlive": false,
  "roleCode": "admin"
}
```

**开启缓存 JSON 示例：**
```json
{
  "action": "enable_cache",
  "menuId": "xxx"
}
```

> **默认不开启缓存路由**。仅当用户明确要求时才设置 `keepAlive: true`。
> **路由缓存详细参考参见：** `references/onlform-route-cache.md`

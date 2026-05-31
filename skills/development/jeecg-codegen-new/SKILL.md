---
name: jeecg-codegen-new
description: Use when user asks to generate JeecgBoot CRUD code, create a new module, add/modify fields on existing module, or says "代码生成", "生成代码", "创建模块", "新增功能", "建表", "加字段", "加一个字段", "增加字段", "新增字段", "修改字段", "删除字段", "generate code", "new entity", "add field"
disable-model-invocation: true
---

# JeecgBoot 代码生成器（Freemarker 驱动）

把用户的自然语言需求转成 Freemarker 上下文 JSON，交给 `scripts/codegen.py` 调用模板生成全套 CRUD（后端 Java + 前端 Vue3 + 菜单 SQL）。

## 核心原则

> **AI 不再从零写代码。** 基础代码全部由 jeecg 官方 Freemarker 模板生成，AI 只做三件事：
>
> 1. **拼参数** — 把用户需求映射成 `ctx.json`
> 2. **调脚本** — 跑 `scripts/codegen.py` 让 Freemarker 出基础代码
> 3. **改产物** — 用户提了模板不覆盖的特殊需求时，**用 Edit 改已生成的代码**
>
> ⛔ **禁止**修改 `templates/` 目录下任何模板文件。模板由 jeecg 官方维护，改了就脱离了升级路径。
> ⛔ **禁止**绕开脚本直接手写 Entity / Controller / data.ts 等基础文件。

## 主数据复用

涉及字典、角色、用户、部门时遵循"先查后建"，使用 `jeecg-system` skill。详见 `../jeecg-system/SKILL.md`。

## 接口禁止猜测

所有接口路径/参数必须来自用户提供、`jeecg-system` skill 文档、或经查询确认。猜测命中也算违规。

---

## 模板覆盖范围

不是所有"表类型 × 前端风格"的组合都有模板。**先选表类型 → 决定可选的前端风格**：

| 表类型 | 模板 stylePath | 支持前端风格 | 触发关键词 |
|---|---|---|---|
| 单表 | `default/one` | `vue3` `vue3Native` | 默认 |
| 树表 | `default/tree` | `vue3` `vue3Native` | 分类/层级/树/上下级 |
| 一对多 — Tab-in-Modal | `tab/onetomany` | `vue3` | tab风格 / radio切换 / 标题栏切换 |
| 一对多 — 内嵌子表 | `inner-table/onetomany` | `vue3` | 内嵌子表 / 行展开 / expandedRowRender |
| 一对多 — ERP | `erp/onetomany` | `vue3` `vue3Native` | ERP风格 / 独立编辑 |

> **不支持的组合：** 一对多 + 默认布局（即旧 SKILL 中的"原始布局"）目前没有 vue3 模板，jeecg 官方枚举 `CgformEnum.MANY` 仅支持 vue2。
> 如果用户要"默认/原始布局"的 vue3 一对多，**改推荐 `tab` 或 `inner-table`**，并向用户说明原因。

---

## 交互流程

### Step 0 — 判断操作类型

- 关键词 "加字段 / 删字段 / 改字段 / 给XX加" → **增量修改**（跳到本文末"增量修改"章节）
- 其他 → **全量生成**

### Step 1 — 收集参数（一次性问完）

> ⛔ **铁律：**Step 2 摘要被用户明确确认前，禁止调脚本、禁止落地任何文件、禁止执行任何 SQL。
> "需求很清楚了""都用默认值""先生成再改" 都是合理化跳过确认的借口，全部无效。

向用户一次问全所有缺失项（已知项可填默认值并标注"如无异议保留"）：

| 项 | 默认值 / 提示 |
|---|---|
| **后端模块根** | `<backend_root>`（如 `D:/jeecgboot/jeecg-module-system/jeecg-system-biz`） |
| **前端项目根** | `<frontend_root>`（如 `D:/jeecgboot-vue3`） |
| **Flyway SQL 目录** | `<backend>/jeecg-module-system/jeecg-system-start/src/main/resources/flyway/sql/mysql` |
| **bussiPackage** | `org.jeecg.modules` |
| **entityPackage** | 由用户给（如 `biz` / `edu`） |
| **entityName / tableName** | 由用户给或推导（如 `BizGoods` / `biz_goods`） |
| **描述（中文）** | 用户业务名（如"商品管理"） |
| **表类型** | 单表 / 树表 / 一对多 |
| **一对多风格** | 仅一对多需要：tab / inner-table / erp |
| **前端风格** | `vue3` 或 `vue3Native`（结合表类型用上表校验是否支持） |
| **字段清单** | 已有表 → 查 DDL 自动取；新建表 → 由用户描述 |
| **字典自动匹配** | 默认是。开启后会查 `sys_dict` 自动套字典编码（见下方"字典匹配") |
| **目标数据库名** | 仅"已有表/字典查询/本地执行 SQL"时需要，必须由用户确认 |

### Step 2 — 展示摘要

把构造好的 `ctx.json` 用**表格**展示给用户：
- 表头：表名、实体名、风格、前端风格、字段数
- 字段表：fieldName / fieldDbName / 注释 / fieldDbType / classType / 字典 / 必填 / 列表显示 / 表单显示 / 查询
- **不要 dump 整个 JSON**，太冗长

明确询问 "是否生成？" — 收到 "确认 / ok / 可以 / 没问题" 等表述后才进入 Step 3。

### Step 3 — 调用脚本

调用前先把构造好的 JSON 写到临时目录（路径规则见下方"临时配置文件规则"），然后用绝对路径调脚本。

**SKILL 路径定位：** 脚本永远在 `<SKILL_ROOT>/scripts/codegen.py`。`<SKILL_ROOT>` 就是包含 `SKILL.md` 的那个目录，比如 `C:\Users\moe\.claude\skills\jeecg-codegen-new` 或 `E:\Projects\BJGJ\jeecg-skills\jeecg-codegen-new`——你能加载 SKILL.md 就能得出这个路径，**不要再去 Read codegen.py 来确认任何东西**，下面的 CLI 参考就是脚本的完整契约。

#### 完整 CLI 参考

```
python <SKILL_ROOT>/scripts/codegen.py [OPTIONS]
```

| 参数 | 必填 | 默认 | 取值 | 说明 |
|---|:-:|---|---|---|
| `--style` | ✅ | — | `default/one` `default/tree` `default/onetomany` `tab/onetomany` `inner-table/onetomany` `erp/onetomany` | 模板风格，见"模板覆盖范围"表 |
| `--ctx` | ✅ | — | 文件路径 | ctx.json 路径，必须在 `{tempdir}/jeecg-codegen-new/<表名>_ctx.json` |
| `--frontend-style` | 🟡 | `vue3` | `vue3` `vue3Native` | 必须与 `--style` 兼容，否则脚本拒绝（详见"模板覆盖范围"表） |
| `--backend-root` | 🟡 | — | 后端模块根 | 比如 `D:/jeecgboot/jeecg-module-system/jeecg-system-biz`，脚本会自动拼 `/src/main/java/<bussiPackage>/<entityPackage>/` |
| `--frontend-root` | 🟡 | — | 前端项目根 | 比如 `D:/jeecgboot-vue3`，脚本会自动拼 `/src/views/<entityPackage>/` |
| `--mobile-root` | ❌ | — | uniapp 项目根 | **不传则跳过 uniapp/uniapp3 产物**——常规需求都不需要传 |
| `--flyway-dir` | 🟡 | — | Flyway SQL 目录 | 菜单 SQL 落到这里；同名 SQL 自动去重 |
| `--out` | ❌ | — | 任意目录 | 调试用：渲染产物原样落到此目录，**跳过分发**。设了它就不需要 backend/frontend/flyway-root |
| `--dry-run` | ❌ | `false` | flag | 打印分发计划但不写文件 |

> 🟡 = 在没有 `--out` 的"正常模式"下，至少要传 `--backend-root` 或 `--frontend-root` 或 `--flyway-dir` 之一（任何没传的目录类型对应的产物都被跳过）；正常代码生成场景三个都该传。
>
> ✅ = 任何模式都必填。

#### 退出码 & 输出

- 退出码 `0` = 成功；其他都失败（参数非法、Java 编译失败、Freemarker 渲染异常）
- 标准输出每行一个事件：`[codegen] WROTE <绝对路径>`、`[codegen] WOULD WRITE ...`（dry-run 时）、`[codegen] running FtlRunner …` 等
- 失败时 stderr 含完整 Java 栈或 `[codegen] xxx` 错误信息

#### 典型调用（**复制后改 4 个值即可**）

```bash
python E:/Projects/BJGJ/jeecg-skills/jeecg-codegen-new/scripts/codegen.py \
  --style default/one \
  --ctx /c/Users/moe/AppData/Local/Temp/jeecg-codegen-new/biz_goods_ctx.json \
  --backend-root D:/jeecgboot/jeecg-module-system/jeecg-system-biz \
  --frontend-root D:/jeecgboot-vue3 \
  --frontend-style vue3 \
  --flyway-dir D:/jeecgboot/jeecg-module-system/jeecg-system-start/src/main/resources/flyway/sql/mysql
```

## 临时配置文件规则（强制）

所有传给脚本的 `--ctx <xxx.json>` 必须写到 **`{系统临时目录}/jeecg-codegen-new/`** 下，由操作系统自动清理；skill 与脚本均不主动删除该目录或文件。

```python
import tempfile, os, json

SKILL_NAME = "jeecg-codegen-new"
skill_dir = os.path.join(tempfile.gettempdir(), SKILL_NAME)
os.makedirs(skill_dir, exist_ok=True)          # 确保目录存在，不主动检查

config_path = os.path.join(skill_dir, 'biz_goods_ctx.json')   # 示例文件名：<表名>_ctx.json
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(cfg, f, ensure_ascii=False, indent=2)
```

`tempfile.gettempdir()` 自动适配：Windows `%TEMP%`、Linux `/tmp`、macOS `/var/folders/.../T`（注意 macOS 并非 `/tmp`）。
文件名建议使用 **`<表名>_<步骤>.json`**（如 `biz_goods_ctx.json` / `biz_goods_alter.json`），无需重复技能前缀，因路径已包含技能名称，便于排错。

**❌ 禁止：**

- 写到 `<skill>/tmp/` 或当前工作目录（污染 skill / 用户项目）
- 硬编码 `/tmp`、`C:\Temp` 或任何固定路径（不跨平台）
- 每步完成后主动 `rm` / `Remove-Item`（操作系统会清理，属多余 tool call）
- 主动 `os.path.exists()` 检查（其本身即为一次 tool call）
  （使用 `os.makedirs(…, exist_ok=True)` 满足需求，不算主动检查）

**临时文件可能被操作系统异步清理**，但仍遵循 **乐观调用 + 报错补救**：仅当脚本返回 `FileNotFoundError` 或 `配置文件不存在` 时，使用相同内容、**在相同的 `{系统临时目录}/jeecg-codegen-new/` 路径下重写**（重写前仍需 `os.makedirs(skill_dir, exist_ok=True)` 确保目录存在），切勿更换路径或回退至 skill 目录。

### Step 4 — 处理特殊需求（模板没覆盖的部分）

用户的需求经常超出模板能力（比如"商品名要带前缀生成""价格变更后自动算总价""列表行加复制按钮"），这时：

1. 先跑脚本生成基础代码
2. 再用 Read 读出对应文件、用 Edit 做精细修改
3. **不要改 templates/，永远改产物**

常见的特殊需求与改动位置参考 `references/post-edit-recipes.md`。

### Step 5 — 后续操作

- **Flyway SQL**：脚本已落到 `<flyway-dir>/V<date>_1__menu_insert_<entity>.sql`，重启后端时 Flyway 自动执行；如果用户要求立即生效，按"本地自动执行 SQL"流程做（见下方）。
- **重启后端**：提示用户 `mvn spring-boot:run -pl jeecg-module-system/jeecg-system-start`
- **前端热更新**：`pnpm dev` 自动热更，无需重启
- **菜单可见**：默认授权 admin，登录系统直接可见

---

## 字段语义推导

新建表时，AI 需要把用户描述的字段（如"价格"、"备注"）映射到合适的 `classType` / `fieldDbType` / `fieldType`。映射表见 `references/field-mapping.md`。

已有表场景下，从 DDL 直接读类型，不依赖语义推导。

## 已有表反向生成

用户给了表名 → 必须先查数据库取 DDL 再构造 ctx：

```bash
# 询问用户目标数据库名后，一条命令拿全部信息
mysql --no-defaults --default-character-set=utf8mb4 -h127.0.0.1 -P3306 -uroot -proot {dbname} \
  -e "SHOW CREATE TABLE 表名\G" \
  -e "SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_COMMENT, COLUMN_KEY, EXTRA FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='{dbname}' AND TABLE_NAME='表名' ORDER BY ORDINAL_POSITION"
```

> ⛔ 执行任何 SQL 前必须先询问用户目标数据库名，**不要从 application-dev.yml 自动取**——用户本机可能多库并存。

## 字典自动匹配

用户开启后，先查全部字典：

```bash
mysql ... -e "
SELECT d.dict_code, d.dict_name,
       GROUP_CONCAT(i.item_text, '=', i.item_value ORDER BY i.sort_order SEPARATOR ', ') AS items
FROM sys_dict d LEFT JOIN sys_dict_item i ON d.id = i.dict_id AND i.status = 1
WHERE d.del_flag = 0 GROUP BY d.dict_code, d.dict_name ORDER BY d.dict_code"
```

匹配优先级：用户明确指定 > 字段名等于 dict_code > 注释关键词命中 dict_name > 不匹配。

匹配后在 ctx 的 column 上设置 `classType: "list"` + `dictField: "<dict_code>"`，模板会自动展开成 `@Dict` + `JDictSelectTag` + `dataIndex: "fieldName_dictText"` 等完整代码。

更详细见 `references/dict-matching.md`。

## 本地自动执行菜单 SQL（仅 127.0.0.1 / localhost）

用户确认目标数据库后：

```bash
# 1. 检查主菜单是否已存在（避免重复插入）
mysql ... -e "SELECT id FROM sys_permission WHERE name='<描述>' AND parent_id IS NULL"
# 2. 不存在则执行
mysql ... < <flyway_sql_file_path>
```

执行失败时只提示，**不中断流程**——Flyway 文件已落地，下次重启会自动执行。

---

## 增量修改（加 / 删 / 改字段）

> 所有"模板已生成的代码 + 用户后续小调整"都走 Edit，不重新跑脚本。

### Step A — 定位文件

```bash
# Entity
find <backend_root>/src/main/java -name "<EntityName>.java"
# 前端 data.ts
find <frontend_root>/src/views -name "<EntityName>__data.ts"
```

需要读：`Entity.java` / `*__data.ts` / `*List.vue` / `*Modal.vue` / `*Form.vue`（vue3Native）。

### Step B — 推导新字段属性

参考 `references/field-mapping.md`。

### Step C — 展示摘要 → 等用户确认 → 执行 Edit

加字段：在所有相关文件追加；删字段：精确删除；改字段：定位修改。
ALTER TABLE 写到新的 Flyway SQL（版本号递增）。

> 不要因为"加一个字段"就重新跑全量代码生成，会覆盖用户对生成结果的手工修改。

---

## 文件夹与脚本

| 路径 | 说明 |
|---|---|
| `templates/` | jeecg 官方 Freemarker 模板（**只读**）|
| `lib/` | freemarker.jar + fastjson2.jar |
| `scripts/codegen.py` | 主入口（Python3）|
| `scripts/FtlRunner.java` | Java 渲染器（首次运行自动 javac）|
| `scripts/.cache/` | 编译产物 + 临时 ctx |
| `references/field-mapping.md` | 字段语义 → Freemarker 字段映射 |
| `references/context-schema.md` | ctx.json 完整 schema |
| `references/post-edit-recipes.md` | 模板没覆盖的特殊需求改动位置 |
| `references/dict-matching.md` | 字典匹配规则与 ctx 映射 |

依赖：`java`（JDK 8+）+ `python3`（3.9+，类型注解用了 PEP 585 语法）。脚本会自动探测 javac 版本：JDK 8 用 `-source 8 -target 8`，JDK 9+ 用 `--release 8`，最终编译产物始终为 Java 8 字节码（major=52）。

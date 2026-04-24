---
name: jeecg-codegen
description: Use when user asks to generate JeecgBoot CRUD code, create a new module, add/modify fields on existing module, or says "代码生成", "生成代码", "创建模块", "新增功能", "建表", "加字段", "加一个字段", "增加字段", "新增字段", "修改字段", "删除字段", "generate code", "new entity", "add field"
---

# JeecgBoot 代码生成器

将自然语言需求转换为 JeecgBoot 全套 CRUD 代码（后端 Java + 前端 Vue3 + 菜单权限 SQL），并支持对已生成模块的增量字段修改。

## 主数据复用规则

> **重要：** 生成代码涉及的字典、角色、用户、部门等主数据，必须遵循"先查后建"原则。
> 使用 `jeecg-system` skill 的 `system_utils.py` 查询和管理主数据。
> 详见 `../jeecg-system/SKILL.md`。

## 交互流程

### Step 0: 判断操作类型 — 全量生成 or 增量修改？

**识别增量修改的关键词：** "加字段"、"增加字段"、"新增字段"、"加一个XX字段"、"删除字段"、"修改字段"、"改一下XX"、"给XX模块加"、"给XX表加"

如果是增量修改 → 进入 **场景C**
如果是全量生成 → 进入 **场景A** 或 **场景B**

### Step 1: 全量生成 — 判断场景

**场景A — 已有表（用户给了表名）：**
1. 通过数据库查询获取精确 DDL（见"数据库连接"章节）
2. 从 DDL 中解析：主键类型、全部字段（名称/类型/注释/是否nullable）、是否有系统字段
3. 根据字段类型和注释自动推导前端控件类型
4. 用户无需描述字段，AI 全部自动推导

**场景B — 新建表（用户用自然语言描述需求）：**
1. 从用户描述中提取：表名、实体名、功能描述、字段列表
2. 用"智能字段推导"规则推导 DB 类型和前端控件
3. 默认添加全部系统字段（create_by/create_time/update_by/update_time/sys_org_code）
4. 生成建表 DDL 写入 Flyway SQL

**场景C — 增量修改（给已有模块加/改/删字段）：**
1. **定位目标模块**：从用户提到的表名、模块名、实体名中识别目标
2. **扫描已有代码文件**：在后端和前端目录中搜索已生成的文件
   ```bash
   # <project_root>/<project_vue_root>：后端/前端项目根目录，使用前需向用户确认
   # 搜索后端 Entity 文件
   find <project_root> -name "{EntityName}.java" -path "*/entity/*"
   # 搜索前端 data.ts 文件
   find <project_vue_root>/src/views -name "{EntityName}.data.ts"
   ```
3. **读取全部已有文件**：Entity.java、*.data.ts、*List.vue、*Modal.vue（如有 Form.vue 也读取）
4. **解析当前字段列表**：从 Entity.java 解析已有字段
5. **推导新字段属性**：用"智能字段推导"规则推导 DB 类型、Java 类型、前端控件
6. **展示修改摘要**，等待用户确认后再修改

**增量修改的操作类型：**
- **加字段**：在所有文件中追加新字段定义
- **删字段**：从所有文件中移除指定字段定义
- **改字段**：修改指定字段的类型、控件、注释等

**判断表类型：**
- 提到"分类/层级/树/上下级" → **树表**
- 提到"主子表/明细/一对多/订单+商品" → **一对多**
- 默认 → **单表**

**一对多表的前端布局风格：**

一对多表有三种前端布局风格，用户未指定时**默认使用原始布局风格**。

> **重要：vue3 封装风格和 vue3Native 原生风格的一对多架构完全不同！** vue3 封装风格使用 `useJvxeMethod`，vue3Native 原生风格使用 `useValidateAntFormAndTable`。详见 `codegen-reference.md` 的 C9-C12（vue3）和 **C13（vue3Native）**。

**vue3 封装风格布局选项：**

| 风格 | 关键词 | 列表页 | Modal 布局 |
|------|--------|--------|-----------|
| **默认/原始布局** | "默认风格"、"默认"、未指定风格 | 标准列表（无 expandedRowRender） | 上面主表 BasicForm + 下面 a-tabs 子表 |
| **Tab-in-Modal (C9)** | "tab切换"、"radio切换"、"标题栏切换" | 标准列表 | radio-group 标题栏切换主表/子表，`wrapClassName="j-cgform-tab-modal"` |
| **内嵌子表 (C12)** | "内嵌子表"、"行展开"、"expandedRowRender" | 行展开显示子表（expandedRowRender） | 上面主表 BasicForm + 下面 a-tabs 子表（同默认） |
| **ERP (C11)** | "ERP风格"、"独立编辑" | 主表单选 + 子表独立 CRUD Tab | 仅主表 BasicForm（子表独立 Modal） |

**vue3Native 原生风格（C13）— 架构完全不同：**
- **Modal 是薄包装器**（BasicModal + useModalInner），只调 `formComponent.submitForm()/edit()/add()`
- **Form.vue 是核心组件**，包含主表 a-form + 子表 a-tabs + 提交逻辑
- 使用 **`useValidateAntFormAndTable`** hook（不是 `useJvxeMethod`）
- 子表 API 导出为**函数**（不是 URL 字符串）
- `saveOrUpdate` **不用** `isTransformResponse: false`
- 一对一子表用原生 `a-form` + `Form.useForm`，暴露 `isForm = true`
- 一对一子表 `initFormData(mainId)` 直接传主表 ID（不传 URL 字符串）
- 一对一子表 `getFormData()` 返回对象（不是数组）
- 需要额外的 `queryDataById` API 函数
- List.vue 使用 `useModal` + `openModal(true, {...})` 模式

**vue3 封装风格 — 默认/原始布局的关键特征：**
- **Modal 结构**：BasicForm（主表）始终显示在上方 + `<a-tabs>` 包裹子表在下方
- **无** `wrapClassName="j-cgform-tab-modal"`，**无** `#title` 插槽的 radio-group
- **`refKeys` 只包含子表 key**（不包含主表 key），如 `['subMany', 'subOne']`
- 一对多子表用 `<JVxeTable>`，一对一子表抽成独立 Form.vue 组件（**必须用 `defineComponent`，不能用 `<script setup>`**）
- 列表页为标准 BasicTable，无 expandedRowRender
- `useJvxeMethod` 的第6个参数 `validateSubForm` 用于校验一对一子表
- `validateForm(index)` 的 index 对应 refKeys 中的位置（0=第一个子表，1=第二个子表）
- **`tableRefs` 只能包含 JVxeTable 的 ref**，禁止包含 Form 组件 ref（否则 `resetScrollTop` 报错）

**内嵌子表 (C12) 的关键特征（Modal 与默认布局完全一致，仅 List 不同）：**
- **List.vue** 使用 `expandedRowRender` 行展开显示 SubTable 组件，需额外创建 `subTables/` 目录
- **Modal.vue** 结构与默认布局**完全一致**：`useJvxeMethod` 6参数 + `classifyIntoFormData` + `validateSubForm`
- **后端** 子表查询必须返回 `Result<IPage<T>>`（不是 `Result<List<T>>`），SubTable 前端通过 `res.result.records` 获取数据
- **api.ts** 每个子表需要双导出：URL 字符串（供 Modal）+ API 函数（供 SubTable，`isTransformResponse:false`）
- **data.ts** 一对多子表需要双列定义：`BasicColumn[]`（SubTable 展示）+ `JVxeColumn[]`（Modal 编辑）
- 详见规则18-24.5

### Step 2: 询问用户选项（仅全量生成需要）
一次性展示所有选项及默认值，用户说"确认"即可全部采用默认值，或只说需要改的：
1. **后端模块**：默认 `jeecg-module-system/jeecg-system-biz`
2. **前端风格**：默认 `vue3`（封装风格），可选 `vue3Native`（原生风格）
3. **前端视图目录**：默认用 entityPackage 值
4. **是否读取系统字典**：默认 `是`，读取后可自动为字段匹配已有字典编码（见"字典智能匹配"章节）

### Step 3: 展示摘要
- **全量生成**：列出表名、字段清单（名称/类型/控件/校验/字典），等待用户确认后再生成。
- **增量修改**：列出要修改的文件路径 + 每个文件的具体变更内容（新增/删除/修改哪些行），等待用户确认。

### Step 4: 执行
- **全量生成**：读取 `codegen-reference.md` 获取完整模板模式，按顺序生成全部文件。
- **增量修改**：使用 Edit 工具精确修改每个文件，读取 `codegen-reference.md` 的 Section F 获取增量修改模板。

### Step 5: 输出清单
列出所有生成/修改的文件路径 + 后续操作说明（执行SQL、重启后端等）。

### 本地环境自动执行菜单 SQL 规则

**前置条件（必须）：执行任何 SQL 之前，必须先询问用户要执行到哪个数据库。** 不要自动假设目标数据库名称，即使配置文件中有默认值。用户本机可能有多个数据库实例。

**判断条件：** 数据库连接地址为 `127.0.0.1` 或 `localhost`（即本地开发环境）。

**自动执行方式：** 确认目标数据库后，生成 Flyway SQL 文件后，同时通过 Bash 工具直接执行菜单权限 SQL：

```bash
# 先询问用户目标数据库名，假设用户确认为 {dbname}
# 先检查菜单是否已存在，避免重复插入
mysql --no-defaults --default-character-set=utf8mb4 -h127.0.0.1 -P3306 -uroot -proot {dbname} -e "SELECT id FROM sys_permission WHERE id='{timestamp}01'"
# 不存在则执行全部菜单 + 角色授权 SQL
mysql --no-defaults --default-character-set=utf8mb4 -h127.0.0.1 -P3306 -uroot -proot {dbname} < {flyway_sql_file_path}
```

**注意事项：**
- **执行 SQL 前必须先询问用户目标数据库名称**，不能自动假设
- 仅在本地环境（127.0.0.1/localhost）自动执行，远程环境只生成 Flyway 文件
- 执行前先检查主菜单 ID 是否已存在，避免重复插入
- 如果 MySQL 执行失败，提示用户手动执行 Flyway SQL，不中断整体流程
- 输出结果中标注 `菜单 SQL：已自动执行 ✓`

## 数据库连接

**已有表场景必须先查数据库！** 通过以下方式获取精确 DDL：

**重要：执行任何 SQL 之前，必须先询问用户要执行到哪个数据库。** 不要自动假设数据库名称。先读取 `application-dev.yml` 获取配置中的数据库名，然后向用户确认是否使用该数据库。

```bash
# 1. 先读取项目数据库配置，获取数据库名
# 配置文件: jeecg-module-system/jeecg-system-start/src/main/resources/application-dev.yml

# 2. 向用户确认目标数据库名后，再执行查询（假设确认为 {dbname}）

# 查询表 DDL
mysql --no-defaults --default-character-set=utf8mb4 -h127.0.0.1 -P3306 -uroot -proot {dbname} -e "SHOW CREATE TABLE 表名\G"

# 查询字段注释
mysql --no-defaults --default-character-set=utf8mb4 -h127.0.0.1 -P3306 -uroot -proot {dbname} -e "SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_COMMENT, COLUMN_KEY, EXTRA FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='{dbname}' AND TABLE_NAME='表名' ORDER BY ORDINAL_POSITION"
```

如果无法连接数据库，回退方案：在项目 SQL 文件中搜索表定义（`grep -r "CREATE TABLE.*表名"` 在 docs/db/ 目录下）。

## Flyway 版本号规则

**生成 Flyway SQL 前必须检查已有版本号，自动递增避免冲突！**

```bash
# Flyway SQL 目录（路径以 CLAUDE.md 中的后端根路径为准）
ls {后端根路径}/jeecg-module-system/jeecg-system-start/src/main/resources/flyway/sql/mysql/ | sort -V | tail -5
```

版本命名规则：`V{YYYYMMDD}_{序号}__{描述}.sql`
- 检查当天是否已有文件（如 `V20260311_1__xxx.sql`）
- 如果有，序号递增（`V20260311_2__xxx.sql`）
- 如果没有，从 `_1` 开始

## 菜单 SQL 的 ID 生成

**必须使用真实时间戳确保唯一性！** 通过以下命令获取：

```bash
date +%s%3N  # 输出13位毫秒级时间戳，如 1741704000123
```

用这个时间戳作为基础 ID，依次拼接 01-14：
- 主菜单: `{timestamp}01`
- 添加按钮: `{timestamp}02`
- 编辑按钮: `{timestamp}03`
- ... 以此类推

## 字典智能匹配

**用户选择"读取系统字典"后，执行以下查询获取全部可用字典：**

```bash
# 查询所有字典编码及其选项值（{dbname} 需替换为用户确认的数据库名）
mysql --no-defaults --default-character-set=utf8mb4 -h127.0.0.1 -P3306 -uroot -proot {dbname} -e "
SELECT d.dict_code, d.dict_name, GROUP_CONCAT(i.item_text, '=', i.item_value ORDER BY i.sort_order SEPARATOR ', ') AS items
FROM sys_dict d
LEFT JOIN sys_dict_item i ON d.id = i.dict_id AND i.status = 1
WHERE d.del_flag = 0
GROUP BY d.dict_code, d.dict_name
ORDER BY d.dict_code
"
```

**匹配规则：** 拿到字典列表后，按以下优先级为字段匹配字典：
1. **用户明确指定** — 用户说"状态用字典 order_status"，直接使用
2. **字段名精确匹配** — 字段名（如 `status`）与 dict_code 完全一致
3. **语义关键词匹配** — 字段注释含"状态/类型/级别/分类"等关键词，搜索 dict_name 包含相同关键词的字典
4. **不匹配** — 找不到合适字典时，不使用字典注解，按普通 Input 处理

**匹配成功后的效果：**
- Entity: 自动添加 `@Dict(dicCode = "matched_dict_code")`
- data.ts columns: `dataIndex` 使用 `fieldName_dictText` 后缀
- data.ts formSchema: `component` 使用 `JDictSelectTag`，`componentProps: { dictCode: 'matched_dict_code' }`
- data.ts searchFormSchema: 同样使用 `JDictSelectTag` 组件

**展示格式：** 在 Step 3 表结构摘要中，匹配到字典的字段标注字典编码和选项值，如：
```
| 字段名 | 类型 | 控件 | 字典 |
| status | varchar(10) | JDictSelectTag | order_status (待付款=0, 已付款=1, 已完成=2) |
```

## 三种字典控件完整用法

JeecgBoot 支持三种字典类型，每种在后端 Entity、前端 data.ts 的 columns/formSchema/searchFormSchema/superQuerySchema 中的写法不同。

### 1. 系统字典（从 sys_dict 表获取）

适用场景：固定枚举值（状态、类型、级别等），值存储在 `sys_dict` + `sys_dict_item` 表中。

**查询可用字典：**
```bash
mysql ... -e "
SELECT d.dict_code, d.dict_name, GROUP_CONCAT(i.item_text, '=', i.item_value ORDER BY i.sort_order SEPARATOR ', ') AS items
FROM sys_dict d LEFT JOIN sys_dict_item i ON d.id = i.dict_id AND i.status = 1
WHERE d.del_flag = 0 GROUP BY d.dict_code, d.dict_name ORDER BY d.dict_code"
```

**后端 Entity：**
```java
@Excel(name = "学校状态", width = 15, dicCode = "valid_status")
@Dict(dicCode = "valid_status")
private String schoolStatus;
```

**前端 data.ts — columns：**
```typescript
{ title: '学校状态', align: 'center', dataIndex: 'schoolStatus_dictText' }
// 注意：列表展示用 _dictText 后缀，后端自动翻译字典值为文本
```

**前端 data.ts — formSchema：**
```typescript
{ label: '学校状态', field: 'schoolStatus', component: 'JDictSelectTag',
  componentProps: { dictCode: 'valid_status', placeholder: '请选择学校状态' } }
```

**前端 data.ts — searchFormSchema：**
```typescript
{ label: '学校状态', field: 'schoolStatus', component: 'JDictSelectTag',
  componentProps: { dictCode: 'valid_status' }, colProps: { span: 6 } }
```

**前端 data.ts — superQuerySchema：**
```typescript
schoolStatus: { title: '学校状态', order: 0, view: 'list', dictCode: 'valid_status' }
```

**Controller 查询规则（下拉/多选字段需添加）：**
```java
Map<String, QueryRuleEnum> customeRuleMap = new HashMap<>();
customeRuleMap.put("schoolStatus", QueryRuleEnum.LIKE_WITH_OR);
QueryWrapper<EduSchool> queryWrapper = QueryGenerator.initQueryWrapper(eduSchool, req.getParameterMap(), customeRuleMap);
```

---

### 2. 分类字典（从 sys_category 表获取，树形结构）

适用场景：树形分类数据（省市区、物料分类、部门分类等），数据存储在 `sys_category` 表中，通过 `pid` 构成树。

**查询可用分类：**
```bash
mysql ... -e "SELECT id, code, name, pid FROM sys_category WHERE pid = '0' OR pid IS NULL OR pid = '' ORDER BY code"
# 查看某分类的子项：
mysql ... -e "SELECT id, code, name, pid FROM sys_category WHERE code = 'B03' OR pid IN (SELECT id FROM sys_category WHERE code = 'B03') ORDER BY code"
```

**后端 Entity：**
```java
// 分类字典不使用 @Dict 注解，由前端 JCategorySelect 组件和 renderCategoryTree 处理翻译
@Excel(name = "所在区域", width = 15)
private String schoolArea;
```

**前端 data.ts — columns：**
```typescript
{ title: '所在区域', align: 'center', dataIndex: 'schoolArea',
  customRender: ({ text }) => { return render.renderCategoryTree(text, 'B03'); } }
// 'B03' 是分类字典的顶级 code，renderCategoryTree 会自动翻译 id 为分类名称路径
```

**前端 data.ts — formSchema：**
```typescript
{ label: '所在区域', field: 'schoolArea', component: 'JCategorySelect',
  componentProps: { pcode: 'B03' } }
// pcode 指定分类字典的顶级 code，组件自动渲染树形选择
```

**前端 data.ts — searchFormSchema：**
```typescript
// 分类字典一般不放在搜索栏，如需要则使用 JCategorySelect
{ label: '所在区域', field: 'schoolArea', component: 'JCategorySelect',
  componentProps: { pcode: 'B03' }, colProps: { span: 6 } }
```

**前端 data.ts — superQuerySchema：**
```typescript
schoolArea: { title: '所在区域', order: 0, view: 'cat_tree', code: 'B03' }
```

---

### 3. 表字典（从任意业务表获取）

适用场景：关联其他业务表的数据作为下拉选项（如从 `sys_depart` 表选部门、从 `sys_user` 表选用户等）。

**后端 Entity：**
```java
@Excel(name = "归属部门", width = 15, dictTable = "sys_depart", dicText = "depart_name", dicCode = "id")
@Dict(dictTable = "sys_depart", dicText = "depart_name", dicCode = "id")
private String departId;
// dictTable: 关联的表名
// dicText: 作为显示文本的字段
// dicCode: 作为存储值的字段（通常是主键）
```

**前端 data.ts — columns：**
```typescript
{ title: '归属部门', align: 'center', dataIndex: 'departId_dictText' }
// 与系统字典一样，列表展示用 _dictText 后缀
```

**前端 data.ts — formSchema（下拉选择）：**
```typescript
{ label: '归属部门', field: 'departId', component: 'JDictSelectTag',
  componentProps: { dictCode: 'sys_depart,depart_name,id', placeholder: '请选择归属部门' } }
// dictCode 格式: '表名,显示字段,值字段'
// 可追加条件: 'sys_depart,depart_name,id,status=1' (第四段为 WHERE 条件)
```

**前端 data.ts — formSchema（搜索选择，大数据量推荐）：**
```typescript
{ label: '归属部门', field: 'departId', component: 'JSearchSelect',
  componentProps: { dict: 'sys_depart,depart_name,id', placeholder: '请选择归属部门' } }
// JSearchSelect 支持远程搜索，适合数据量大的表
```

**前端 data.ts — searchFormSchema：**
```typescript
{ label: '归属部门', field: 'departId', component: 'JDictSelectTag',
  componentProps: { dictCode: 'sys_depart,depart_name,id' }, colProps: { span: 6 } }
```

**前端 data.ts — superQuerySchema：**
```typescript
departId: { title: '归属部门', order: 0, view: 'sel_search',
  dictTable: 'sys_depart', dictCode: 'id', dictText: 'depart_name' }
```

**Controller 查询规则：**
```java
customeRuleMap.put("departId", QueryRuleEnum.LIKE_WITH_OR);
```

---

### 三种字典对比速查表

| 维度 | 系统字典 | 分类字典 | 表字典 |
|------|---------|---------|--------|
| 数据来源 | `sys_dict` + `sys_dict_item` | `sys_category`（树形） | 任意业务表 |
| 后端注解 | `@Dict(dicCode = "xxx")` | 无需 @Dict | `@Dict(dictTable="t", dicText="text", dicCode="code")` |
| Excel注解 | `dicCode = "xxx"` | 无 | `dictTable="t", dicText="text", dicCode="code"` |
| 列表 columns | `dataIndex: 'field_dictText'` | `customRender: render.renderCategoryTree(text, 'pcode')` | `dataIndex: 'field_dictText'` |
| 表单组件 | `JDictSelectTag` + `dictCode: 'xxx'` | `JCategorySelect` + `pcode: 'xxx'` | `JDictSelectTag` + `dictCode: '表,text,code'` |
| 搜索组件 | `JDictSelectTag` | `JCategorySelect` | `JDictSelectTag` 或 `JSearchSelect` |
| 高级查询 view | `list` + `dictCode` | `cat_tree` + `code` | `sel_search` + `dictTable/dictCode/dictText` |
| Controller 规则 | `QueryRuleEnum.LIKE_WITH_OR` | 无需特殊处理 | `QueryRuleEnum.LIKE_WITH_OR` |
| 适用场景 | 固定枚举（状态、类型） | 树形分类（地区、物料） | 关联其他表（部门、用户） |

---

## 全组件控件完整用法

除三种字典外，JeecgBoot 还支持以下所有组件类型。每种组件在后端 Entity、前端 data.ts 的 columns/formSchema/searchFormSchema/superQuerySchema、Controller 中各有固定写法。

---

### 1. 基础输入类

#### Input（文本框）
```java
// Entity
@Excel(name = "文本", width = 15)
@Schema(description = "文本")
private String name;
```
```typescript
// columns
{ title: '文本', align: 'center', dataIndex: 'name' }
// formSchema
{ label: '文本', field: 'name', component: 'Input', componentProps: { placeholder: '请输入' } }
// superQuerySchema
name: { title: '文本', order: 0, view: 'text' }
```

#### InputPassword（密码框）
```java
@Excel(name = "密码", width = 15)
@Schema(description = "密码")
private String password;
```
```typescript
// formSchema — 密码框一般不在 columns 和 searchFormSchema 中展示
{ label: '密码', field: 'password', component: 'InputPassword',
  componentProps: { placeholder: '请输入密码' } }
```

#### InputTextArea（多行文本）
```java
@Excel(name = "备注", width = 15)
@Schema(description = "备注")
private String remark;
```
```typescript
// formSchema
{ label: '备注', field: 'remark', component: 'InputTextArea',
  componentProps: { placeholder: '请输入备注', rows: 4 } }
```

#### InputNumber（数字输入）
```java
// BigDecimal 类型（金额/单价）
@Excel(name = "单价", width = 15)
@Schema(description = "单价")
private BigDecimal amount;

// Integer 类型（整数/排序号）
@Excel(name = "排序", width = 15)
@Schema(description = "排序")
private Integer sortOrder;
```
```typescript
// formSchema
{ label: '单价', field: 'amount', component: 'InputNumber',
  componentProps: { placeholder: '请输入', style: 'width:100%' } }
// superQuerySchema
amount: { title: '单价', order: 0, view: 'number' }
```

---

### 2. 系统字典扩展控件

> 基本的 JDictSelectTag 下拉见"三种字典控件"章节，此处仅列出扩展用法。

#### JDictSelectTag type='radio'（字典单选）
```typescript
// formSchema
{ label: '性别', field: 'sex', component: 'JDictSelectTag',
  componentProps: { dictCode: 'sex', type: 'radio' } }
```

#### JCheckbox（字典多选 checkbox）
```java
// Entity — 存储多个值用逗号分隔
@Excel(name = "颜色多选", width = 15, dicCode = "demo_color")
@Dict(dicCode = "demo_color")
private String demoColor;
```
```typescript
// formSchema
{ label: '颜色多选', field: 'demoColor', component: 'JCheckbox',
  componentProps: { dictCode: 'demo_color' } }
// superQuerySchema — view 使用 list_multi
demoColor: { title: '颜色多选', order: 0, view: 'list_multi', dictCode: 'demo_color' }
```

#### JSelectMultiple（字典下拉多选框）
```java
@Excel(name = "字典下拉多选", width = 15, dicCode = "urgent_level")
@Dict(dicCode = "urgent_level")
private String dictMultiSelect;
```
```typescript
// formSchema
{ label: '字典下拉多选', field: 'dictMultiSelect', component: 'JSelectMultiple',
  componentProps: { dictCode: 'urgent_level', triggerChange: true } }
// superQuerySchema
dictMultiSelect: { title: '字典下拉多选', order: 0, view: 'list_multi', dictCode: 'urgent_level' }
// Controller
customeRuleMap.put("dictMultiSelect", QueryRuleEnum.LIKE_WITH_OR);
```

#### JSwitch（开关）
```java
@Excel(name = "开关", width = 15, replace = {"是_1", "否_0"})
private String isEnabled;
```
```typescript
// columns — 使用 renderSwitch 自定义渲染
{ title: '开关', align: 'center', dataIndex: 'isEnabled',
  customRender: ({ text }) => render.renderSwitch(text, [{ text: '是', value: '1' }, { text: '否', value: '0' }]) }
// formSchema
{ label: '开关', field: 'isEnabled', component: 'JSwitch',
  componentProps: { options: ['1', '0'] } }
// superQuerySchema
isEnabled: { title: '开关', order: 0, view: 'radio', dictCode: 'yn' }
```

---

### 3. 表字典扩展控件

> 基本的表字典下拉和搜索见"三种字典控件"章节，此处仅列出扩展用法。

#### JDictSelectTag type='radio'（表字典单选）
```java
@Excel(name = "表字典单选", width = 15, dictTable = "sys_depart", dicText = "depart_name", dicCode = "id")
@Dict(dictTable = "sys_depart", dicText = "depart_name", dicCode = "id")
private String tableDictRadio;
```
```typescript
// formSchema
{ label: '表字典单选', field: 'tableDictRadio', component: 'JDictSelectTag',
  componentProps: { dictCode: 'sys_depart,depart_name,id', type: 'radio' } }
```

#### JCheckbox（表字典多选）
```java
@Dict(dictTable = "sys_depart", dicText = "depart_name", dicCode = "id")
private String tableDictCheckbox;
```
```typescript
// formSchema
{ label: '表字典多选', field: 'tableDictCheckbox', component: 'JCheckbox',
  componentProps: { dictCode: 'sys_depart,depart_name,id' } }
```

#### JSelectMultiple（表字典下拉多选）
```java
@Dict(dictTable = "sys_depart", dicText = "depart_name", dicCode = "id")
private String tableDictMultiSelect;
```
```typescript
// formSchema
{ label: '表字典下拉多选', field: 'tableDictMultiSelect', component: 'JSelectMultiple',
  componentProps: { dictCode: 'sys_depart,depart_name,id', triggerChange: true } }
```

#### 表字典带条件下拉
```java
// Entity — dictTable 中直接拼 WHERE 条件
@Excel(name = "表字典带条件", width = 15, dictTable = "sys_user where username like '%a%'", dicText = "realname", dicCode = "username")
@Dict(dictTable = "sys_user where username like '%a%'", dicText = "realname", dicCode = "username")
private String tableDictCondition;
```
```typescript
// formSchema — dictCode 字符串中拼条件
{ label: '表字典带条件', field: 'tableDictCondition', component: 'JDictSelectTag',
  componentProps: { dictCode: "sys_user where username like '%a%',realname,username", placeholder: '请选择' } }
```

---

### 4. 用户/部门选择

#### JSelectUserByDept（用户选择）
```java
@Excel(name = "用户选择", width = 15, dictTable = "sys_user", dicText = "realname", dicCode = "username")
@Dict(dictTable = "sys_user", dicText = "realname", dicCode = "username")
private String userId;
```
```typescript
// columns
{ title: '用户选择', align: 'center', dataIndex: 'userId_dictText' }
// formSchema
{ label: '用户选择', field: 'userId', component: 'JSelectUserByDept',
  componentProps: { labelKey: 'realname' } }
// superQuerySchema
userId: { title: '用户选择', order: 0, view: 'sel_user' }
```

#### JSelectDept（部门选择）
```java
@Excel(name = "部门选择", width = 15, dictTable = "sys_depart", dicText = "depart_name", dicCode = "id")
@Dict(dictTable = "sys_depart", dicText = "depart_name", dicCode = "id")
private String deptId;
```
```typescript
// columns
{ title: '部门选择', align: 'center', dataIndex: 'deptId_dictText' }
// formSchema
{ label: '部门选择', field: 'deptId', component: 'JSelectDept' }
// superQuerySchema
deptId: { title: '部门选择', order: 0, view: 'sel_depart' }
```

---

### 5. 自定义树（JTreeSelect）

```java
@Excel(name = "自定义树", width = 15, dictTable = "sys_category", dicText = "name", dicCode = "id")
@Dict(dictTable = "sys_category", dicText = "name", dicCode = "id")
private String treeSelect;
```
```typescript
// columns
{ title: '自定义树', align: 'center', dataIndex: 'treeSelect_dictText' }
// formSchema
{ label: '自定义树', field: 'treeSelect', component: 'JTreeSelect',
  componentProps: { dict: 'sys_category,name,id', pidField: 'pid', multiple: false } }
// superQuerySchema
treeSelect: { title: '自定义树', order: 0, view: 'sel_search',
  dictTable: 'sys_category', dictCode: 'id', dictText: 'name' }
// Controller
customeRuleMap.put("treeSelect", QueryRuleEnum.LIKE_WITH_OR);
```

---

### 6. 日期时间类

#### DatePicker（日期）
```java
@Excel(name = "日期", width = 15, format = "yyyy-MM-dd")
@JsonFormat(timezone = "GMT+8", pattern = "yyyy-MM-dd")
@DateTimeFormat(pattern = "yyyy-MM-dd")
private Date birthday;
```
```typescript
// columns — 截取前10位防止时间部分显示
{ title: '日期', align: 'center', dataIndex: 'birthday',
  customRender: ({ text }) => (!text ? '' : (text.length > 10 ? text.substr(0, 10) : text)) }
// formSchema
{ label: '日期', field: 'birthday', component: 'DatePicker',
  componentProps: { showTime: false, valueFormat: 'YYYY-MM-DD', placeholder: '请选择日期', style: 'width:100%' } }
// superQuerySchema
birthday: { title: '日期', order: 0, view: 'date' }
```

#### DatePicker showTime（年月日时分秒）
```java
@Excel(name = "年月日时分秒", width = 20, format = "yyyy-MM-dd HH:mm:ss")
@JsonFormat(timezone = "GMT+8", pattern = "yyyy-MM-dd HH:mm:ss")
@DateTimeFormat(pattern = "yyyy-MM-dd HH:mm:ss")
private Date workTime;
```
```typescript
// formSchema
{ label: '年月日时分秒', field: 'workTime', component: 'DatePicker',
  componentProps: { showTime: true, valueFormat: 'YYYY-MM-DD HH:mm:ss', placeholder: '请选择', style: 'width:100%' } }
// superQuerySchema
workTime: { title: '年月日时分秒', order: 0, view: 'datetime' }
```

#### TimePicker（时间选择）
```java
// 时间类型用 String 存储（如 "14:30:00"）
@Excel(name = "时间", width = 15)
private String timeVal;
```
```typescript
// formSchema
{ label: '时间', field: 'timeVal', component: 'TimePicker',
  componentProps: { valueFormat: 'HH:mm:ss', placeholder: '请选择时间', style: 'width:100%' } }
```

#### DatePicker picker 变体（季度/年/月/周）

**共同规则：** DB 类型均为 `date`，Java 类型均为 `Date`，注解统一用 `yyyy-MM-dd` 格式。前端通过 `picker` 属性区分。

```java
// Entity — 季度/年/月/周写法完全一致，只改注释
@Excel(name = "季度", width = 15, format = "yyyy-MM-dd")
@JsonFormat(timezone = "GMT+8", pattern = "yyyy-MM-dd")
@DateTimeFormat(pattern = "yyyy-MM-dd")
private Date quarterVal;
```
```typescript
// formSchema — 通过 picker 区分
{ label: '季度', field: 'quarterVal', component: 'DatePicker',
  componentProps: { picker: 'quarter', valueFormat: 'YYYY-MM-DD', placeholder: '请选择季度', style: 'width:100%' } }
{ label: '年', field: 'yearVal', component: 'DatePicker',
  componentProps: { picker: 'year', valueFormat: 'YYYY-MM-DD', placeholder: '请选择年', style: 'width:100%' } }
{ label: '月', field: 'monthVal', component: 'DatePicker',
  componentProps: { picker: 'month', valueFormat: 'YYYY-MM-DD', placeholder: '请选择月', style: 'width:100%' } }
{ label: '周', field: 'weekVal', component: 'DatePicker',
  componentProps: { picker: 'week', valueFormat: 'YYYY-MM-DD', placeholder: '请选择周', style: 'width:100%' } }

// columns — 必须使用 getWeekMonthQuarterYear 翻译（需 import { getWeekMonthQuarterYear } from '/@/utils'）
{ title: '季度', dataIndex: 'quarterVal',
  customRender: ({ text }) => {
    text = !text ? '' : (text.length > 10 ? text.substr(0, 10) : text);
    return text ? getWeekMonthQuarterYear(text)['quarter'] : text;
  } }
{ title: '年', dataIndex: 'yearVal',
  customRender: ({ text }) => {
    text = !text ? '' : (text.length > 10 ? text.substr(0, 10) : text);
    return text ? getWeekMonthQuarterYear(text)['year'] : text;
  } }
// 月用 ['month']，周用 ['week']，写法相同

// ✅ 季度/年/月/周可以作为查询条件，需配合 List.vue 中的 fieldPickers + getDateByPicker（见 searchFormSchema 生成规则）
```

---

### 7. Popup/弹窗类

#### 报表 Code 数据源（重要前置知识）

JPopup、JPopupDict、关联记录三个组件都依赖**在线报表 code**，code 来源于 `onl_cgreport_head` 表。生成代码时**必须先查询可用报表**，再配置到组件中。

**查询可用报表 code：**
```bash
mysql ... -e "SELECT code, name, cgr_sql FROM onl_cgreport_head ORDER BY create_time DESC"
```

**查询报表的字段列表（用于配置 fieldConfig 的 source）：**
```bash
mysql ... -e "SELECT field_name, field_txt FROM onl_cgreport_item WHERE cgrhead_id = (SELECT id FROM onl_cgreport_head WHERE code='报表code') ORDER BY order_num"
```

**配置流程：**
1. 查询 `onl_cgreport_head` 获取所有可用报表 code 和 SQL
2. 根据业务需求选择合适的报表（如需大数据测试选 `testbigdata`，需用户数据选 `report_user`）
3. 查询该报表的 `onl_cgreport_item` 获取可用字段名（`field_name`）
4. 将 `code` 和 `field_name` 配置到前端组件的 `code`、`fieldConfig.source`、`dictCode` 中

**常用报表 code 示例：**
| code | 名称 | SQL数据源 | 典型字段 |
|------|------|----------|---------|
| report_user | 统计在线用户 | sys_user | id, username, realname, phone, email |
| testbigdata | 测试大数据 | sys_log | id, log_content, userid, username, ip |
| demo | Report Demo | demo | * |

#### JPopup（Popup弹窗 + 他表字段回填）

JPopup 用于弹窗选择记录并回填多个字段值。`code` 对应 `onl_cgreport_head` 表中的报表编码。

```java
// Entity — popup 存储选中值，popback 存储回填值
@Excel(name = "popup弹窗", width = 15)
private String popup;

@Excel(name = "popup回填", width = 15)
private String popback;
```
```typescript
// formSchema — JPopup 组件通过 fieldConfig 定义回填映射
{ label: 'Popup弹窗', field: 'popup', component: 'JPopup',
  componentProps: ({ formActionType }) => {
    const { setFieldsValue } = formActionType;
    return {
      setFieldsValue,
      code: 'testbigdata',           // 报表编码，对应 onl_cgreport_head.code
      fieldConfig: [
        { source: 'log_content', target: 'popup' },   // 报表字段 → 当前表字段
        { source: 'userid', target: 'popback' },       // 回填其他字段
      ],
      multi: false,                   // 是否多选
    };
  } }
// 他表字段（回填字段）— disabled Input，不可手动编辑
{ label: 'Popup回填(他表字段)', field: 'popback', component: 'Input',
  componentProps: { disabled: true, placeholder: '由Popup自动回填' } }
```

**fieldConfig 配置规则：**
- `source`：报表中的字段名（来自 `onl_cgreport_item.field_name`）
- `target`：当前表单中的字段名（field 值）
- 可配置多组回填映射，选中一条记录后同时回填多个字段

#### JPopupDict（Popup字典）

JPopupDict 是简化版的 Popup，直接通过 dictCode 指定报表和显示/值字段，无需配置 fieldConfig。

```java
@Excel(name = "popup字典", width = 15)
private String popDict;
```
```typescript
// formSchema
{ label: 'Popup字典', field: 'popDict', component: 'JPopupDict',
  componentProps: { dictCode: 'testbigdata,log_content,id', multi: false } }
// dictCode 格式: '报表code,显示字段,值字段'
// 报表code: onl_cgreport_head.code
// 显示字段: 报表中用于展示的 field_name
// 值字段: 报表中用于存储的 field_name（通常是 id）
```

#### 关联记录 + 他表字段（JPopup 关联业务表）

关联记录本质是 JPopup，选中后自动回填关联表的其他字段（他表字段）。后端用 `@Dict` 实现列表翻译。

```java
// Entity — 关联记录字段带 @Dict 翻译
@Excel(name = "关联记录", width = 15, dictTable = "sys_user", dicText = "realname", dicCode = "username")
@Dict(dictTable = "sys_user", dicText = "realname", dicCode = "username")
private String relatedUser;

// 他表字段 — 不需要 @Dict，由前端 JPopup 回填
@Excel(name = "他表字段", width = 15)
private String relatedUsername;
```
```typescript
// columns — 关联记录用 _dictText 翻译，他表字段直接展示
{ title: '关联记录', align: 'center', dataIndex: 'relatedUser_dictText' }
{ title: '他表字段', align: 'center', dataIndex: 'relatedUsername' }

// formSchema — 关联记录用 JPopup，他表字段用 disabled Input
{ label: '关联记录', field: 'relatedUser', component: 'JPopup',
  componentProps: ({ formActionType }) => {
    const { setFieldsValue } = formActionType;
    return {
      setFieldsValue,
      code: 'testbigdata',
      fieldConfig: [
        { source: 'userid', target: 'relatedUser' },
        { source: 'username', target: 'relatedUsername' },
      ],
      multi: false,
    };
  } }
{ label: '他表字段', field: 'relatedUsername', component: 'Input',
  componentProps: { disabled: true, placeholder: '由关联记录自动回填' } }

// superQuerySchema — 关联记录
relatedUser: { title: '关联记录', order: 0, view: 'sel_search',
  dictTable: 'sys_user', dictCode: 'username', dictText: 'realname' }

// Controller
customeRuleMap.put("relatedUser", QueryRuleEnum.LIKE_WITH_OR);
```

#### Popup 组件生成流程总结

生成含 Popup/关联记录/Popup字典的字段时，按以下步骤操作：
1. **查询报表列表**：`SELECT code, name, cgr_sql FROM onl_cgreport_head`
2. **选择合适报表**：根据业务场景匹配（用户→report_user，日志→testbigdata 等）
3. **查询报表字段**：`SELECT field_name, field_txt FROM onl_cgreport_item WHERE cgrhead_id=...`
4. **配置 code**：JPopup 的 `code` 和 JPopupDict 的 `dictCode` 第一段都填报表 code
5. **配置字段映射**：JPopup 的 `fieldConfig` 中 `source` 填报表字段名，JPopupDict 的 `dictCode` 后两段填显示字段和值字段
6. **如果没有合适报表**：提示用户先在"在线报表"中创建报表配置

---

### 8. 省市区/联动

#### JAreaLinkage（省市区三级联动）

```java
// Entity — 需要 import/export 转换方法
@Excel(name = "省市区", width = 15, exportConvert = true, importConvert = true)
private String provinceCityArea;

// 必须添加这两个转换方法（Excel导入导出用）
public String convertisProvinceCityArea() {
    return SpringContextUtils.getBean(ProvinceCityArea.class).getText(provinceCityArea);
}
public void convertsetProvinceCityArea(String text) {
    this.provinceCityArea = SpringContextUtils.getBean(ProvinceCityArea.class).getCode(text);
}
// 需要 import：
// import org.jeecg.common.constant.ProvinceCityArea;
// import org.jeecg.common.util.SpringContextUtils;
```
```typescript
// formSchema
{ label: '省市区', field: 'provinceCityArea', component: 'JAreaLinkage' }
```

#### 联动组件（多级自定义联动）

联动组件由多个独立字段组成，通过前端逻辑实现级联关系。后端存储各级选中值。

```java
@Excel(name = "联动组件一", width = 15)
private String linkOne;
@Excel(name = "联动组件二", width = 15)
private String linkTwo;
@Excel(name = "联动组件三", width = 15)
private String linkThree;
```
```typescript
// formSchema — 每级用不同的字典/数据源
{ label: '联动组件一', field: 'linkOne', component: 'JDictSelectTag',
  componentProps: { dictCode: 'org_category', placeholder: '请选择一级' } }
{ label: '联动组件二', field: 'linkTwo', component: 'JSearchSelect',
  componentProps: { dict: 'sys_depart,depart_name,id', placeholder: '请选择二级' } }
{ label: '联动组件三', field: 'linkThree', component: 'JSearchSelect',
  componentProps: { dict: 'sys_user,realname,username', placeholder: '请选择三级' } }
```

---

### 9. 文件/上传类

#### JImageUpload（图片上传）
```java
@Excel(name = "图片", width = 15)
private String avatar;
```
```typescript
// columns — 使用 renderImage 渲染缩略图
{ title: '图片', align: 'center', dataIndex: 'avatar', customRender: render.renderImage }
// formSchema
{ label: '图片', field: 'avatar', component: 'JImageUpload' }
```

#### JUpload（文件上传）
```java
@Excel(name = "文件", width = 15)
private String attachment;
```
```typescript
// columns — 使用 bodyCell 插槽渲染下载按钮
// 在 List.vue 的 <template v-slot:bodyCell="{ column, record, index, text }"> 中：
<template v-if="column.dataIndex==='attachment'">
  <span v-if="!text" style="font-size:12px;font-style:italic;">无文件</span>
  <a-button v-else :ghost="true" type="primary" preIcon="ant-design:download-outlined"
    size="small" @click="downloadFile(text)">下载</a-button>
</template>
// List.vue 需要 import：
import { downloadFile } from '/@/utils/common/renderUtils';

// formSchema
{ label: '文件', field: 'attachment', component: 'JUpload' }
```

---

### 10. 编辑器类

#### JEditor（富文本编辑器）
```java
@Excel(name = "富文本", width = 15)
private String content;
```
```typescript
// columns — 使用 bodyCell 插槽渲染 HTML
// 在 List.vue 的 bodyCell 中：
<template v-if="column.dataIndex==='content'">
  <div v-html="text"></div>
</template>
// formSchema
{ label: '富文本', field: 'content', component: 'JEditor' }
```

#### JMarkdownEditor（Markdown编辑器，blob存储）

Markdown 使用 `byte[]` (blob) 存储以支持大文本，需要特殊的 getter/setter 模式：

```java
// Entity — 注意 transient 和 byte[] 的双字段模式
@Excel(name = "markdown", width = 15)
private transient String markdownString;  // 前端交互用，不写入DB

private byte[] markdown;  // 实际存储到DB的blob字段

public byte[] getMarkdown() {
    if (markdownString == null) { return null; }
    try { return markdownString.getBytes("UTF-8"); }
    catch (UnsupportedEncodingException e) { e.printStackTrace(); }
    return null;
}

public String getMarkdownString() {
    if (markdown == null || markdown.length == 0) { return ""; }
    try { return new String(markdown, "UTF-8"); }
    catch (UnsupportedEncodingException e) { e.printStackTrace(); }
    return "";
}
// 需要 import java.io.UnsupportedEncodingException;
```
```sql
-- DB字段类型必须是 blob
ALTER TABLE xxx ADD COLUMN `markdown` blob COMMENT 'markdown内容';
```
```typescript
// formSchema — 前端字段名用 markdownString（对应 transient 字段）
{ label: 'Markdown编辑器', field: 'markdownString', component: 'JMarkdownEditor' }
```

---

### 全组件速查表

| 组件 | 前端组件名 | DB类型 | Java类型 | 需要@Dict | columns特殊处理 | Controller规则 |
|------|-----------|--------|---------|-----------|---------------|---------------|
| 文本框 | Input | varchar | String | 否 | 无 | 无 |
| 密码框 | InputPassword | varchar | String | 否 | 不展示 | 无 |
| 多行文本 | InputTextArea | text | String | 否 | 无 | 无 |
| 数字 | InputNumber | decimal/int | BigDecimal/Integer | 否 | 无 | 无 |
| 字典下拉 | JDictSelectTag | varchar | String | 系统字典 | _dictText | LIKE_WITH_OR |
| 字典单选 | JDictSelectTag(radio) | varchar | String | 系统字典 | _dictText | LIKE_WITH_OR |
| 字典多选 | JCheckbox | varchar | String | 系统字典 | _dictText | LIKE_WITH_OR |
| 下拉多选 | JSelectMultiple | varchar | String | 系统字典 | _dictText | LIKE_WITH_OR |
| 开关 | JSwitch | varchar(2) | String | 否 | renderSwitch | 无 |
| 表字典下拉 | JDictSelectTag | varchar | String | 表字典 | _dictText | LIKE_WITH_OR |
| 表字典搜索 | JSearchSelect | varchar | String | 表字典 | _dictText | LIKE_WITH_OR |
| 表字典单选 | JDictSelectTag(radio) | varchar | String | 表字典 | _dictText | LIKE_WITH_OR |
| 表字典多选 | JCheckbox | varchar | String | 表字典 | _dictText | LIKE_WITH_OR |
| 表字典下拉多选 | JSelectMultiple | varchar | String | 表字典 | _dictText | LIKE_WITH_OR |
| 表字典带条件 | JDictSelectTag | varchar | String | 表字典(带WHERE) | _dictText | LIKE_WITH_OR |
| 用户选择 | JSelectUserByDept | varchar | String | 表字典(sys_user) | _dictText | 无 |
| 部门选择 | JSelectDept | varchar | String | 表字典(sys_depart) | _dictText | 无 |
| 分类字典 | JCategorySelect | varchar | String | 否 | renderCategoryTree | 无 |
| 自定义树 | JTreeSelect | varchar | String | 表字典 | _dictText | LIKE_WITH_OR |
| 日期 | DatePicker | date | Date | 否 | substr(0,10) | 无 |
| 日期时间 | DatePicker(showTime) | datetime | Date | 否 | 无 | 无 |
| 时间 | TimePicker | varchar | String | 否 | 无 | 无 |
| 季度 | DatePicker(quarter) | date | Date | 否 | getWeekMonthQuarterYear['quarter'] | 无 |
| 年 | DatePicker(year) | date | Date | 否 | getWeekMonthQuarterYear['year'] | 无 |
| 月 | DatePicker(month) | date | Date | 否 | getWeekMonthQuarterYear['month'] | 无 |
| 周 | DatePicker(week) | date | Date | 否 | getWeekMonthQuarterYear['week'] | 无 |
| Popup弹窗 | JPopup | varchar | String | 否 | 无 | 无 |
| Popup回填 | Input(disabled) | varchar | String | 否 | 无 | 无 |
| Popup字典 | JPopupDict | varchar | String | 否 | 无 | 无 |
| 关联记录 | JPopup | varchar | String | 表字典 | _dictText | LIKE_WITH_OR |
| 他表字段 | Input(disabled) | varchar | String | 否 | 无 | 无 |
| 省市区 | JAreaLinkage | varchar | String | 否 | 无 | 无 |
| 联动组件 | JDictSelectTag/JSearchSelect | varchar | String | 按级别 | 无 | 无 |
| 图片上传 | JImageUpload | varchar(1000) | String | 否 | renderImage | 无 |
| 文件上传 | JUpload | varchar(1000) | String | 否 | bodyCell下载按钮 | 无 |
| 富文本 | JEditor | text | String | 否 | bodyCell v-html | 无 |
| Markdown | JMarkdownEditor | blob | byte[]+transient | 否 | 无 | 无 |

---

### JVxeTable 子表列配置（一对多子表 JVxeColumn）

一对多子表使用 JVxeTable 组件，列定义使用 `JVxeColumn[]` 类型，**不是 FormSchema**。

**引入方式：**
```typescript
import { JVxeTypes, JVxeColumn } from '/@/components/jeecg/JVxeTable/types';
```

**重要：JVxeTable 的组件类型与 FormSchema 完全不同！** 不能使用 FormSchema 的组件名（如 `JDictSelectTag`、`JCheckbox` 等），必须使用 `JVxeTypes` 枚举。

**JVxeTypes 组件类型对照表（FormSchema → JVxeColumn）：**

| FormSchema 组件 | JVxeTypes 类型 | 关键属性 | 说明 |
|----------------|---------------|---------|------|
| Input | `JVxeTypes.input` | — | 文本输入 |
| InputTextArea | `JVxeTypes.textarea` | — | 多行文本 |
| InputNumber | `JVxeTypes.inputNumber` | `props.max/min/precision` | 数字输入 |
| JDictSelectTag | `JVxeTypes.select` | `options:[], dictCode` | 字典下拉（系统字典 + 表字典） |
| JDictSelectTag(radio) | `JVxeTypes.select` | `options:[], dictCode` | JVxe无单独radio，用select代替 |
| JCheckbox | `JVxeTypes.select` | `options:[], dictCode` | JVxe无checkbox字典，用select代替 |
| JSelectMultiple | `JVxeTypes.selectMultiple` | `options:[], dictCode` | 下拉多选 |
| JSearchSelect | `JVxeTypes.selectSearch` | `dictCode` | 下拉搜索 |
| JSwitch | `JVxeTypes.checkbox` | `customValue:['Y','N']` | 开关（用checkbox实现） |
| DatePicker | `JVxeTypes.date` | — | 日期 |
| DatePicker(showTime) | `JVxeTypes.datetime` | — | 日期时间 |
| TimePicker | `JVxeTypes.time` | — | 时间 |
| JImageUpload | `JVxeTypes.image` | `token:true, responseName:'message'` | 图片上传 |
| JUpload | `JVxeTypes.file` | `token:true, responseName:'message'` | 文件上传 |
| JPopup | `JVxeTypes.popup` | `popupCode, fieldConfig, props` | Popup弹窗 |
| JSelectDept | `JVxeTypes.departSelect` | — | 部门选择 |
| JSelectUserByDept | `JVxeTypes.userSelect` | — | 用户选择 |

**JVxeColumn 通用属性：**
```typescript
{
  title: '标题',           // 列标题
  key: 'fieldName',       // 字段名（对应 entity 属性名）
  type: JVxeTypes.xxx,    // 组件类型
  width: '200px',         // 列宽（字符串，带px）
  placeholder: '请输入${title}',  // 占位提示，${title}自动替换为列标题
  defaultValue: '',       // 默认值
  disabled: false,        // 是否禁用
  validateRules: [],      // 校验规则
}
```

**校验规则（validateRules）：**
```typescript
validateRules: [
  { required: true, message: '${title}不能为空' },           // 必填
  { pattern: '^1[3456789]\\d{9}$', message: '${title}格式不正确' },  // 正则
  { pattern: 'only', message: '${title}不能重复' },           // 唯一值
  { pattern: '*6-16', message: '${title}格式不正确' },        // 6-16位任意字符
]
```

**常用示例（覆盖主要类型）：**
```typescript
export const subTableColumns: JVxeColumn[] = [
  { title: '文本', key: 'name', type: JVxeTypes.input, width: '200px', placeholder: '请输入${title}', defaultValue: '',
    validateRules: [{ required: true, message: '${title}不能为空' }] },
  { title: '数字', key: 'amount', type: JVxeTypes.inputNumber, width: '200px', defaultValue: '' },
  { title: '系统字典', key: 'status', type: JVxeTypes.select, options: [], dictCode: 'valid_status', width: '200px', defaultValue: '' },
  { title: '表字典', key: 'deptId', type: JVxeTypes.select, options: [], dictCode: 'sys_depart,depart_name,id', width: '200px', defaultValue: '' },
  { title: '表字典搜索', key: 'userId', type: JVxeTypes.selectSearch, dictCode: 'sys_user,realname,username', width: '200px', defaultValue: '' },
  { title: '下拉多选', key: 'multiVal', type: JVxeTypes.selectMultiple, options: [], dictCode: 'org_category', width: '250px', defaultValue: '' },
  { title: '开关', key: 'switchVal', type: JVxeTypes.checkbox, customValue: ['Y', 'N'], width: '200px', defaultValue: 'N' },
  { title: '日期', key: 'dateVal', type: JVxeTypes.date, width: '200px', defaultValue: '' },
  { title: '日期时间', key: 'datetimeVal', type: JVxeTypes.datetime, width: '200px', defaultValue: '' },
  { title: '图片', key: 'imageVal', type: JVxeTypes.image, token: true, responseName: 'message', number: 1, width: '200px', defaultValue: '' },
  { title: '文件', key: 'fileVal', type: JVxeTypes.file, token: true, responseName: 'message', number: 1, width: '200px', defaultValue: '' },
  { title: 'popup', key: 'popupVal', type: JVxeTypes.popup, popupCode: 'report_user',
    fieldConfig: [{ source: 'realname', target: 'popupVal' }, { source: 'username', target: 'popupBack' }],
    props: { multi: true }, width: '200px', defaultValue: '' },
  { title: '部门选择', key: 'deptId', type: JVxeTypes.departSelect, width: '200px', defaultValue: '' },
  { title: '用户选择', key: 'userId', type: JVxeTypes.userSelect, width: '200px', defaultValue: '' },
];
```

---

### searchFormSchema 生成规则

生成查询条件（searchFormSchema）时，必须遵循以下三条规则：

**规则1：label 必须与 formSchema 一致**
查询条件的 label 必须与编辑表单（formSchema）中同字段的 label 完全一致，不能用字典描述或简写替代。

```typescript
// ✅ 正确 — label 与 formSchema 一致
formSchema:       { label: '字典下拉(Select)', field: 'status', ... }
searchFormSchema: { label: '字典下拉(Select)', field: 'status', ... }

// ❌ 错误 — 用字典描述当 label
formSchema:       { label: '字典多选(Checkbox)', field: 'demoColor', ... }
searchFormSchema: { label: '颜色多选', field: 'demoColor', ... }  // 不应用字典名称
```

**规则2：多选字段在查询条件中使用 JSelectMultiple（下拉多选），不使用 JCheckbox**
表单中使用 JCheckbox 的多选字段，在查询条件中统一改为 JSelectMultiple 下拉多选，因为 Checkbox 在查询栏中占空间过大且体验不佳。

```typescript
// ✅ 正确 — 查询条件用下拉多选
formSchema:       { label: '字典多选(Checkbox)', field: 'demoColor', component: 'JCheckbox',
                    componentProps: { dictCode: 'demo_color' } }
searchFormSchema: { label: '字典多选(Checkbox)', field: 'demoColor', component: 'JSelectMultiple',
                    componentProps: { dictCode: 'demo_color', triggerChange: true }, colProps: { span: 6 } }

// ❌ 错误 — 查询条件用 Checkbox
searchFormSchema: { label: '字典多选(Checkbox)', field: 'demoColor', component: 'JCheckbox', ... }
```

**规则3：不适合作为查询条件的组件应排除**
以下组件类型不应出现在 searchFormSchema 中：
- 密码框（InputPassword）
- 多行文本（InputTextArea）
- 富文本（JEditor）
- Markdown（JMarkdownEditor）
- 图片上传（JImageUpload）
- 文件上传（JUpload）
- Popup回填/他表字段（disabled Input，由关联记录回填）

> **DatePicker picker 变体（quarter/year/month/week）可以作为查询条件**，但需要在 List.vue 中配合 `fieldPickers` + `getDateByPicker` 使用（见规则7）。

**规则4：JPopup 作为查询条件时必须使用 formActionType**
JPopup 在 searchFormSchema 中必须通过 `componentProps: ({ formActionType }) => {}` 获取 `setFieldsValue`，否则选中后无法回显值。

```typescript
// ✅ 正确 — 使用 formActionType 获取 setFieldsValue
{ label: 'Popup弹窗', field: 'popup', component: 'JPopup',
  componentProps: ({ formActionType }) => {
    const { setFieldsValue } = formActionType;
    return {
      setFieldsValue,
      code: 'fz_sql',
      fieldConfig: [{ source: 'username', target: 'popup' }],
      multi: true,
    };
  }, colProps: { span: 6 } }

// ❌ 错误 — 静态 componentProps，选中后不回显
{ label: 'Popup弹窗', field: 'popup', component: 'JPopup',
  componentProps: { code: 'fz_sql', fieldConfig: [...], multi: false }, colProps: { span: 6 } }
```

**规则5：JAreaLinkage 必须加 saveCode**
JAreaLinkage 组件在 formSchema 和 searchFormSchema 中都要加 `saveCode: 'region'`，否则保存/查询的数据格式不一致。

```typescript
{ label: '省市区', field: 'provinceCityArea', component: 'JAreaLinkage',
  componentProps: { saveCode: 'region' } }
```

**规则6：JPopupDict 字段后端需要 @Dict 翻译**
JPopupDict 存储的是 ID 值，列表展示时需要 `_dictText` 后缀翻译。后端 Entity 必须加 `@Dict` 注解：

```java
// Entity
@Dict(dictTable = "sys_user", dicText = "realname", dicCode = "id")
private String popDict;
```
```typescript
// columns — 使用 _dictText
{ title: 'popup字典', align: 'center', dataIndex: 'popDict_dictText' }
```

**searchFormSchema 组件映射速查表：**

| formSchema 组件 | searchFormSchema 组件 | 说明 |
|----------------|----------------------|------|
| Input | JInput | 查询用 JInput 支持模糊匹配 |
| InputNumber | InputNumber | 保持不变 |
| JDictSelectTag | JDictSelectTag | 保持不变 |
| JDictSelectTag(radio) | JDictSelectTag | 查询不需要 radio 样式 |
| JCheckbox | **JSelectMultiple** | 多选改为下拉多选 |
| JSelectMultiple | JSelectMultiple | 保持不变 |
| JSwitch | JDictSelectTag(yn) | 查询用下拉选 是/否 |
| JSearchSelect | JSearchSelect | 保持不变 |
| JSelectUserByDept | JSelectUserByDept | 保持不变 |
| JSelectDept | JSelectDept | 保持不变 |
| JCategorySelect | JCategorySelect | 保持不变 |
| JTreeSelect | JTreeSelect | 保持不变 |
| DatePicker(日期) | **RangePicker** | 范围查询，配合 fieldMapToTime |
| DatePicker(日期时间) | DatePicker | 精确查询保持不变 |
| **DatePicker(quarter/year/month/week)** | **DatePicker(同picker)** | 可用，需配合 List.vue fieldPickers（见规则7） |
| TimePicker | **RangeTime** | 范围查询，配合 fieldMapToNumber |
| JPopup | **JPopup(formActionType)** | 必须用 formActionType 回显值 |
| JPopupDict | JPopupDict | 保持不变 |
| JAreaLinkage | JAreaLinkage(saveCode) | 必须加 saveCode: 'region' |

**规则7：季度/年/月/周需要在查询和保存时都做 getDateByPicker 预处理**
DatePicker 的 quarter/year/month/week 变体发送的是精确日期值（如选2025年发`2025-01-01`），需要用 `getDateByPicker` 转换为该时段的起始日期。**查询和保存两处都需要处理。**

```typescript
// ===== List.vue 查询预处理 =====
import { getDateByPicker } from '/@/utils';

const fieldPickers = reactive({
  quarterVal: 'quarter',
  yearVal: 'year',
  monthVal: 'month',
  weekVal: 'week',
});

// useListPage 的 beforeFetch 中添加
beforeFetch: (params) => {
  if (params && fieldPickers) {
    for (let key in fieldPickers) {
      if (params[key]) {
        params[key] = getDateByPicker(params[key], fieldPickers[key]);
      }
    }
  }
  return Object.assign(params, queryParam);
},

// ===== Modal.vue 保存预处理 =====
import { getDateByPicker } from '/@/utils';

const fieldPickers = reactive({
  quarterVal: 'quarter',
  yearVal: 'year',
  monthVal: 'month',
  weekVal: 'week',
});

const changeDateValue = (formData) => {
  if (formData && fieldPickers) {
    for (let key in fieldPickers) {
      if (formData[key]) {
        formData[key] = getDateByPicker(formData[key], fieldPickers[key]);
      }
    }
  }
};

// handleSubmit 中，validate() 之后、saveOrUpdate() 之前调用
let values = await validate();
changeDateValue(values);  // ← 提交前预处理
await saveOrUpdate(values, isUpdate.value);
```

**规则8：省市区列翻译需要 List.vue 中使用 getAreaTextByCode 插槽**
省市区组件保存的是区域编码（如`340000/340100/340104`），列表中需要翻译为中文名。不能用 `customRender`，需要在 List.vue 的 `<template v-slot:bodyCell>` 中添加插槽：

```html
<!-- List.vue template -->
<template v-if="column.dataIndex==='provinceCityArea'">
  {{ getAreaTextByCode(text) }}
</template>
```
```typescript
// List.vue script
import { getAreaTextByCode } from '/@/components/Form/src/utils/Area';
```

**规则9：分类字典列翻译需要 List.vue 中手动加载分类数据到字典缓存**
`render.renderCategoryTree(text, 'pcode')` 依赖 `getDictItemsByCode(pcode)` 从字典缓存读取分类数据，但系统登录时不会自动加载分类字典。需要在 List.vue 中手动调用 `loadCategoryData` 加载到 store：

```typescript
// List.vue script
import { loadCategoryData } from '/@/api/common/api';
import { useUserStore } from '/@/store/modules/user';

const userStore = useUserStore();

function initDictConfig() {
  loadCategoryData({ code: 'B03' }).then((res) => {
    if (res) {
      const allDictDate = userStore.getAllDictItems;
      if (!allDictDate['B03']) {
        userStore.setAllDictItems({ ...allDictDate, 'B03': res });
      }
    }
  });
}
initDictConfig();
```

**规则10：范围查询使用 RangePicker/RangeTime + fieldMapToTime/fieldMapToNumber**
日期字段适合范围查询时使用 `RangePicker`（选择开始/结束日期），时间字段使用 `RangeTime`。同时在 List.vue 的 `formConfig` 中配置拆分映射：

```typescript
// searchFormSchema
{ label: '日期(范围查询)', field: 'birthday', component: 'RangePicker',
  componentProps: { valueType: 'Date', placeholder: ['开始日期', '结束日期'] }, colProps: { span: 6 } },
{ label: '时间(范围查询)', field: 'timeVal', component: 'RangeTime', colProps: { span: 6 } },

// List.vue formConfig
fieldMapToTime: [
  ['birthday', ['birthday_begin', 'birthday_end'], 'YYYY-MM-DD'],
],
fieldMapToNumber: [
  ['timeVal', ['timeVal_begin', 'timeVal_end']],
],
```

> 后端 QueryGenerator 会自动识别 `_begin`/`_end` 后缀生成 `>=` 和 `<=` 条件，无需后端特殊处理。

**规则11：formSchema 字段校验规则（dynamicRules）**
使用 `dynamicRules` 替代简单的 `required`，可组合多种校验：

```typescript
import { rules } from '/@/utils/helper/validator';

// 1. 必填 + 长度校验
{ label: '文本', field: 'name', component: 'Input',
  dynamicRules: ({ model, schema }) => {
    return [
      { required: true, message: '请输入文本!' },
      { pattern: /^.{2,50}$/, message: '请输入2到50位字符!' },
    ];
  } },

// 2. 唯一校验（duplicateCheckRule）
{ label: '编码', field: 'code', component: 'Input',
  dynamicRules: ({ model, schema }) => {
    return [
      { required: true, message: '请输入编码!' },
      { ...rules.duplicateCheckRule('表名', '字段名', model, schema)[0] },
    ];
  } },

// 3. 金额格式校验
{ label: '单价', field: 'amount', component: 'InputNumber',
  dynamicRules: ({ model, schema }) => {
    return [
      { required: false },
      { pattern: /^\d{1,10}$|^(?=\d+\.\d+)[\d.]{2,12}$/, message: '请输入正确的金额!' },
    ];
  } },

// 4. 常用正则模式
// 手机号: /^1[3456789]\d{9}$/
// 邮箱:   /^([\w]+\.*)([\w]+)@[\w]+\.\w{3}(\.\w{2}|)$/
// 网址:   /^((ht|f)tps?):\/\/[\w\-]+(\.[\w\-]+)+([\w\-.,@?^=%&:\/~+#]*[\w\-@?^=%&\/~+#])?$/
// 字母:   /^[a-z|A-Z]{2,10}$/
// 密码:   /^.{6,20}$/
```

**规则12：label 只显示业务含义，不要附带组件类型名称**
生成的 label 只写业务字段名称，**禁止**在 label 后面括号标注组件类型。这条规则适用于 formSchema、searchFormSchema、columns 等所有 label/title。

```typescript
// ✅ 正确
{ label: '课程名称', field: 'courseName', component: 'Input' }
{ label: '课程状态', field: 'status', component: 'JDictSelectTag' }
{ label: '开课日期', field: 'courseDate', component: 'DatePicker' }
{ label: '省市区', field: 'provinceCityArea', component: 'JAreaLinkage' }
{ label: '课程封面', field: 'courseImage', component: 'JImageUpload' }

// ❌ 错误 — 不要在 label 后面加括号标注组件类型
{ label: '课程名称(Input)', ... }
{ label: '课程状态(Select)', ... }
{ label: '开课日期(DatePicker)', ... }
{ label: '省市区(联动)', ... }
{ label: '课程封面(ImageUpload)', ... }
{ label: '关联记录(JPopup)', ... }
{ label: 'Popup回填(他表字段)', ... }
```

**规则13：ERP 风格一对多 — 主表编辑不能用 updateMain**
ERP 风格下主表和子表各自独立保存。主表 Modal 只提交主表字段，**禁止**调用 `updateMain()`，否则会先删除所有子表记录再重新插入空列表，导致子表数据全部丢失。

```java
// ❌ 错误 — ERP 模式使用 updateMain 会清空子表
demoCourseService.updateMain(demoCourse, page.getDemoCourseDetailList(), page.getDemoCourseStudentList());

// ✅ 正确 — ERP 模式使用 updateById 仅更新主表
demoCourseService.updateById(demoCourse);
```

后端需新增 `/addMain`（调用 `service.save()`）和 `/editMain`（调用 `service.updateById()`）两个接口，前端 api.ts 的 save/edit 指向这两个新接口。原有的 `/add` 和 `/edit`（saveMain/updateMain）保留给 Tab-in-Modal 风格使用。

**规则14：ERP 风格一对多 — handleSuccess 不能清空 selectedRowKeys**
ERP 风格主表使用单选（radio），选中后通过 `provide/inject` 传递主表 ID 给子表。子表通过 `watch(mainId)` 监听变化并重载数据。如果 `handleSuccess` 清空了 `selectedRowKeys`，会触发子表 watch 重载为空列表，造成**编辑后列表显空，需要刷新才恢复**。

```typescript
// ❌ 错误 — 清空选中会触发子表 watch，子表显示空
function handleSuccess() {
  (selectedRowKeys.value = []) && reload();
}

// ✅ 正确 — 只 reload 刷新数据，保持选中状态
function handleSuccess() {
  reload();
}
```

**规则15：ERP 风格一对多 — 子表 FormSchema 必须包含隐藏的外键字段**
ERP 模式下子表使用独立 Modal 编辑。FormSchema 中必须包含隐藏的 `id` 和外键字段（如 `demoCourseId`），否则新增时无法关联主表，编辑时无法定位记录。

```typescript
export const subFormSchema: FormSchema[] = [
  { label: '', field: 'id', component: 'Input', show: false },
  { label: '', field: 'demoCourseId', component: 'Input', show: false },  // 外键字段
  // ... 业务字段
];
```

子表 Modal 的 handleSubmit 中，新增时自动设置外键值：
```typescript
const mainId = inject('demoCourseId') || '';
// 提交时
if (unref(mainId)) {
  values.demoCourseId = unref(mainId);
}
```

**规则16：ERP 风格一对多 — 子表 searchInfo 必须用 reactive**
子表通过 `searchInfo` 向 BasicTable 传递主表 ID 过滤条件。如果 `searchInfo` 是普通对象 `{}`，编辑后调用 `reload()` 时 BasicTable 可能**取不到最新的过滤值**，导致列表不刷新或显示空数据。必须使用 `reactive` 包裹。

```typescript
// ❌ 错误 — 普通对象，编辑后 reload 可能取不到 demoCourseId
const searchInfo = {};

// ✅ 正确 — reactive 对象，确保 BasicTable 能响应数据变化
const searchInfo = reactive<Record<string, any>>({});
```

同时 watch 中赋值用点语法（与 reactive 风格一致）：
```typescript
watch(demoCourseId, () => {
  searchInfo.demoCourseId = unref(demoCourseId);  // ✅ 点语法
  reload();
  setSelectedRowKeys([]);
});
```

**规则17：ERP 风格一对一子表 — 必须限制只能添加一条记录**
一对一子表在列表中只允许存在一条记录。新增前必须检查是否已有数据，已有数据时**禁用新增按钮**并给出提示。通过 `afterFetch` 回调跟踪记录数：

```typescript
const hasDetailRecord = ref(false);

// tableProps 中配置 afterFetch
afterFetch: (data) => {
  hasDetailRecord.value = data && data.length > 0;
  return data;
},

// 新增按钮绑定 :disabled="hasDetailRecord"
<a-button type="primary" @click="handleCreate" :disabled="hasDetailRecord">新增</a-button>

// handleCreate 中二次校验
function handleCreate() {
  if (isEmpty(unref(demoCourseId))) {
    $message.createMessage.warning('请选择一条主表记录');
    return;
  }
  if (hasDetailRecord.value) {
    $message.createMessage.warning('一对一子表只能有一条记录，请编辑现有记录');
    return;
  }
  openModal(true, { isUpdate: false, showFooter: true });
}
```

**规则17.1：ERP 风格子表 — useTable 只返回两个元素，rowSelection 必须手动管理**
`useTable` 返回 `[registerTable, methods]` 两个元素，**不支持第三个解构**。子表的 `selectedRowKeys` 和 `rowSelection` 必须手动定义，不能从 `useTable` 解构获取。

```typescript
// ❌ 错误 — useTable 没有第三个返回值，页面报错
const [registerTable, { reload, setSelectedRowKeys }, { rowSelection, selectedRowKeys }] = useTable({...});

// ✅ 正确 — 手动管理 selectedRowKeys 和 rowSelection
const selectedRowKeys = ref<any[]>([]);
const rowSelection = { type: 'checkbox', selectedRowKeys, onChange: (keys) => { selectedRowKeys.value = keys; } };
const [registerTable, { reload }] = useTable({...});

// watch 中清空选中也要用直接赋值
watch(demoOrderId, () => {
  searchInfo.demoOrderId = unref(demoOrderId);
  reload();
  selectedRowKeys.value = [];  // ✅ 直接赋值，不用 setSelectedRowKeys
});
```

**规则17.2：actionColumn 必须包含 title、dataIndex 和 slots**
`actionColumn` 必须同时设置 `title: '操作'`、`dataIndex: 'action'` 和 `slots: { customRender: 'action' }`，三者缺一不可，否则模板中的 `#action` 插槽无法匹配，操作按钮不会渲染。此规则适用于所有使用 `useTable` 的列表页（不仅限于 ERP 风格）。

```typescript
// ❌ 错误 — 缺少 slots，操作列不显示按钮
actionColumn: {
  title: '操作',
  dataIndex: 'action',
  width: 120,
  fixed: 'right',
}

// ✅ 正确 — 必须包含 title、dataIndex 和 slots
actionColumn: {
  title: '操作',
  dataIndex: 'action',
  width: 120,
  fixed: 'right',
  slots: { customRender: 'action' },
}
```

**规则17.3：ERP 风格 — API 的 saveOrUpdate 必须加 `successMessageMode: 'none'`**
`defHttp.post` 默认会根据后端返回的 `message` 自动弹一次成功提示。如果 Modal 的 `handleSubmit` 里又手动调了 `$message.success()`，会出现**两次成功提示**。ERP 风格（以及所有风格）的 api.ts 中，`saveOrUpdate` 函数必须关闭默认提示：

```typescript
// ✅ 正确 — 关闭 defHttp 自动提示，由 Modal 手动控制
export const saveOrUpdate = (params, isUpdate) => {
  let url = isUpdate ? Api.edit : Api.save;
  return defHttp.post({ url: url, params }, { successMessageMode: 'none' });
};

// 子表独立保存也一样
export const subSaveOrUpdate = (params, isUpdate) => {
  let url = isUpdate ? Api.subEdit : Api.subSave;
  return defHttp.post({ url: url, params }, { successMessageMode: 'none' });
};

// ❌ 错误 — 不加 successMessageMode，加上 Modal 里的手动提示 = 弹两次
return defHttp.post({ url: url, params });
```

**此规则适用于所有表类型（单表、一对多各风格），只要 Modal 中手动调了 `$message.success`，API 就必须加 `{ successMessageMode: 'none' }`。**

**规则17.4：ERP 风格 — 前端文件结构**
ERP 风格与其他一对多风格的核心差异是子表有独立的列表页和 Modal，不使用 JVxeTable。

```
views/{viewDir}/
├── {EntityName}List.vue              # ERP主页面（主表radio单选 + 下方Tab子表列表）
├── {SubEntity}List.vue               # 子表独立列表组件（每个子表一个）
├── {EntityName}.api.ts               # 全部API（主表/addMain+/editMain + 子表独立CRUD）
├── {EntityName}.data.ts              # 主表 columns/formSchema + 子表 BasicColumn[]/FormSchema[]
└── components/
    ├── {EntityName}Modal.vue          # 主表Modal（仅主表字段）
    └── {SubEntity}Modal.vue           # 子表Modal（inject外键 + 设FK）
```

**ERP 前端关键模式：**
- **主表列表**：`rowSelection: { type: 'radio' }`，`provide('mainId', computed(() => ...))`，`@row-click` 选中行
- **子表列表**：`inject<ComputedRef<string>>('mainId')`，`reactive searchInfo`，`watch(mainId)` 刷新，`getSubList` 空ID保护
- **子表 Modal**：`inject('mainId')`，新增时 `values.foreignKey = unref(mainId)`
- **data.ts**：子表用 `BasicColumn[]` + `FormSchema[]`（不是 JVxeColumn[]），FormSchema 包含隐藏的 `id` 和外键字段
- **api.ts**：主表 save/edit 指向 `/addMain`+`/editMain`（调用 service.save/updateById），子表有完整独立 CRUD

**ERP 子表 getSubList 空ID保护：**
```typescript
async function getSubList(params) {
  if (isEmpty(unref(mainId))) {
    return [];  // ← 无主表选中时返回空数组，避免请求报错
  }
  return subTableList({ ...params, foreignKey: unref(mainId) });
}
```

**规则17.5：Flyway SQL 必须包含建表 DDL（新建表场景）**
场景B（新建表）生成的 Flyway SQL 文件**必须同时包含建表 DDL 和菜单权限 SQL**，不能只有菜单 SQL。DDL 放在文件最前面，菜单 SQL 放在后面。

```sql
-- ========== 建表 DDL ==========
CREATE TABLE IF NOT EXISTS `xxx` (...) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='xxx';
-- 子表（如有）
CREATE TABLE IF NOT EXISTS `xxx_detail` (...) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='xxx';

-- ========== 菜单权限 ==========
INSERT INTO sys_permission ...
INSERT INTO sys_role_permission ...
```

**同时，执行 SQL 到数据库时也必须确保建表 DDL 被执行。** 如果分开执行（先建表再菜单），需要两步都完成。

**规则17.6：前端 data.ts 字段必须与后端 Entity 完全一致**
生成前端 data.ts 时，columns/formSchema/searchFormSchema 的字段**必须**与后端 Entity 的属性一一对应。不能出现 Entity 没有的字段（如前端有 `gdp` 但 Entity 没有），也不能遗漏 Entity 有的字段（如 Entity 有 `province` 但前端没有）。

**生成流程：** 先生成后端 Entity → 再以 Entity 为基准生成前端 data.ts。如果分步生成，在生成前端时**必须先重新读取 Entity 文件**确认字段列表。

**规则18：内嵌子表风格（expandedRowRender） — 三类数据导出**
内嵌子表风格在列表页通过行展开（expandedRowRender）直接显示子表数据，同时在 Modal 中使用 JVxeTable/BasicForm 编辑子表。这要求 data.ts 和 api.ts 中对每个子表都有**三类导出**：

**data.ts — 每个子表需要两种列定义：**
```typescript
// 1. BasicColumn[]（SubTable 行展开展示用）
export const xxxColumns: BasicColumn[] = [
  { title: '字段', align: 'center', dataIndex: 'field' },
  { title: '字典字段', align: 'center', dataIndex: 'dictField_dictText' },
];

// 2. JVxeColumn[]（一对多子表 Modal 中 JVxeTable 内嵌编辑用）
export const xxxJVxeColumns: JVxeColumn[] = [
  { title: '字段', key: 'field', type: JVxeTypes.input, width: '200px' },
];

// 3. FormSchema[]（一对一子表 Modal 中 BasicForm 编辑用）
export const xxxFormSchema: FormSchema[] = [
  { label: '字段', field: 'field', component: 'Input' },
];
```

**api.ts — 每个子表需要两种导出：**
```typescript
// 1. URL 字符串（供 Modal 中 requestSubTableData / defHttp.get 使用）
export const queryXxxByMainId = Api.xxxList;

// 2. 函数导出（供 SubTable 组件直接调用，isTransformResponse:false 返回完整响应）
export const xxxListApi = (params) =>
  defHttp.get({ url: Api.xxxList, params }, { isTransformResponse: false });
```

**规则19：内嵌子表风格 — SubTable 组件必须用 watchEffect 加载数据**
SubTable 组件通过 `props.id` 接收主表 ID，使用 `watchEffect` 监听变化自动加载。API 使用 `isTransformResponse: false`，返回完整响应对象。**后端返回 `Result<IPage<T>>`，数据在 `res.result.records` 中，不是 `res.result`！**

```typescript
// subTables/XxxSubTable.vue
const props = defineProps({ id: { type: String, default: '' } });
const loading = ref(false);
const dataSource = ref([]);

watchEffect(() => {
  props.id && loadData(props.id);
});

function loadData(id) {
  dataSource.value = [];
  loading.value = true;
  xxxListApi({ id })
    .then((res) => {
      if (res.success) {
        dataSource.value = res.result.records;  // ✅ 后端返回 IPage<T>，数据在 records 中
      }
    })
    .finally(() => { loading.value = false; });
}
```

**规则20：内嵌子表风格 — List.vue 必须配置 expandedRowKeys + handleExpand**
列表页需要 `expandedRowKeys` 控制展开状态（同时只展开一行），`handleExpand` 处理展开/收起事件。SubTable 组件通过 `v-if="expandedRowKeys.includes(record.id)"` 条件渲染，避免未展开时加载数据：

```html
<BasicTable @register="registerTable" :expandedRowKeys="expandedRowKeys" @expand="handleExpand">
  <template #expandedRowRender="{ record }">
    <a-tabs tabPosition="top">
      <a-tab-pane tab="子表一" key="sub1" forceRender>
        <XxxSubTable v-if="expandedRowKeys.includes(record.id)" :id="record.id" />
      </a-tab-pane>
    </a-tabs>
  </template>
</BasicTable>
```

```typescript
const expandedRowKeys = ref<any[]>([]);

function handleExpand(expanded, record) {
  expandedRowKeys.value = [];
  if (expanded === true) {
    expandedRowKeys.value.push(record.id);
  }
}
```

**规则21：三种 Modal 布局风格区分**

| 风格 | Modal 布局 | 标题栏 | 子表组织 | wrapClassName | refKeys |
|------|-----------|--------|---------|---------------|---------|
| **Tab-in-Modal (C9)** | radio-group 标题栏切换，主表/子表同级用 `v-show` | `#title` 插槽 + `a-radio-group` | `v-show` 切换 | `j-cgform-tab-modal` | **包含主表 key** |
| **内嵌子表 (C12)** | 上面主表 BasicForm + 下面子表 `a-tabs` | 普通 `:title` 属性 | `a-tabs` + `a-tab-pane` | 无 | **只有子表 key** |
| **ERP (C11)** | 仅主表 BasicForm | 普通 `:title` 属性 | 无（子表独立 CRUD） | 无 | 无 |

**只有 Tab-in-Modal (C9) 使用 radio-group 标题栏切换！内嵌子表和 ERP 都使用原始布局（上面主表，下面子表）。**

内嵌子表 (C12) 的 Modal 混合场景（一对一 + 一对多）同样使用 `useJvxeMethod` + `validateSubForm`，但注意 `refKeys` 只包含子表 key，不包含主表 key，因此 `validateForm(index)` 的 index 从 0 开始计数子表位置。

**规则22：内嵌子表风格 — 前端文件结构**
```
views/{viewDir}/
├── {EntityName}List.vue              # 主列表（含 expandedRowRender）
├── {EntityName}.api.ts               # 全部API
├── {EntityName}.data.ts              # 列定义 + 表单配置
├── components/
│   └── {EntityName}Modal.vue         # 编辑弹窗（主表 + Tabs子表）
└── subTables/
    ├── {SubEntity}SubTable.vue       # 子表展示组件（每个子表一个）
    └── ...
```

**规则23：内嵌子表风格 — 子表提交字段名必须与后端 VO 属性名一致**
Modal 提交时 JSON 中子表数据的 key **必须**与后端 Page VO（如 `XxxPage`）中的 `List<SubEntity>` 属性名一致，**不能**用 API URL 的变量名。

```
// ❌ 错误 — 用了 API URL 变量名
{
  ...mainValues,
  queryDemoCourseDetail: [detailValues],    // 后端无法反序列化
  queryDemoCourseStudent: studentTableData, // 后端收到 null
}

// ✅ 正确 — 与后端 VO 属性名一致
{
  ...mainValues,
  demoCourseDetailList: [detailValues],     // 对应 DemoCoursePage.demoCourseDetailList
  demoCourseStudentList: studentTableData,  // 对应 DemoCoursePage.demoCourseStudentList
}
```

**命名规则：** 子表字段名 = `{子表实体名首字母小写}List`，如 `DemoCourseDetail` → `demoCourseDetailList`。
**后果：** 字段名不匹配时后端反序列化得到 null，`saveMain`/`updateMain` 会先删除旧子表记录再插入空列表，**子表数据全部丢失**。

**规则24：内嵌子表风格 — handleSuccess 必须清空 expandedRowKeys**
列表刷新后如果 `expandedRowKeys` 仍保留旧值，SubTable 的 `v-if="expandedRowKeys.includes(record.id)"` 仍为 true 但 `id` prop 没变化，`watchEffect` 不会重新触发，导致展示旧数据。

```typescript
function handleSuccess() {
  expandedRowKeys.value = [];  // 必须清空，确保刷新后重新展开时 SubTable 重新加载
  (selectedRowKeys.value = []) && reload();
}
```

**规则24.1：内嵌子表风格 — 后端子表查询必须返回 `Result<IPage<T>>`，不能返回 `Result<List<T>>`**
SubTable 前端通过 `res.result.records` 访问数据（见规则19），因此后端 Controller 的子表查询接口**必须**将 `List<T>` 包装成 `IPage<T>` 再返回。如果直接返回 `Result<List<T>>`，前端 `res.result.records` 为 undefined，子表数据不显示。

```java
// ✅ 正确 — 返回 IPage<T>，前端通过 res.result.records 获取数据
@GetMapping(value = "/queryXxxByMainId")
public Result<IPage<Xxx>> queryXxxListByMainId(@RequestParam(name = "id", required = true) String id) {
    List<Xxx> list = xxxService.selectByMainId(id);
    IPage<Xxx> page = new Page<>();
    page.setRecords(list);
    page.setTotal(list.size());
    return Result.OK(page);
}

// ❌ 错误 — 返回 List<T>，前端 res.result.records 为 undefined
@GetMapping(value = "/queryXxxByMainId")
public Result<List<Xxx>> queryXxxListByMainId(@RequestParam(name = "id") String id) {
    List<Xxx> list = xxxService.selectByMainId(id);
    return Result.OK(list);  // 前端拿到的 res.result 是数组，没有 .records 属性
}
```

**此规则同时适用于一对多和一对一子表的查询接口。** 一对一子表的 Form 组件 `initFormData` 也通过 `res.result.records[0]` 获取数据。

**规则24.2：内嵌子表风格 — `tableRefs` 只能包含 JVxeTable 的 ref，禁止包含 Form 组件 ref**
`useJvxeMethod` 返回的 `handleChangeTabs` 内部会调用 `tableRefs[key]?.value?.resetScrollTop(0)` 重置滚动位置。如果 `tableRefs` 包含了一对一子表的 Form 组件 ref，`resetScrollTop` 方法不存在，会报错 `resetScrollTop is not a function`。

```typescript
// ✅ 正确 — tableRefs 只包含 JVxeTable 的 ref
const demoProjTask = ref();          // JVxeTable ref
const demoProjBudgetForm = ref();    // Form 组件 ref（不放入 tableRefs）
const tableRefs = { demoProjTask };  // 只有 JVxeTable

// ❌ 错误 — tableRefs 包含 Form ref，切换 tab 时报错 resetScrollTop is not a function
const tableRefs = { demoProjBudgetForm, demoProjTask };  // Form 组件没有 resetScrollTop 方法
```

**规则24.3：内嵌子表风格 — 一对一子表 Form 必须用 `defineComponent`（Options API），禁止用 `<script setup>`**
一对一子表 Form 组件（如 `XxxForm.vue`）需要被父组件通过 `ref` 调用 `initFormData`/`getFormData`/`validateForm`/`resetFields` 方法。使用 `<script setup>` + `defineExpose` 暴露方法时，父组件调用 `xxxForm.value.validateForm()` 会报 `validateForm is not a function`。**必须使用 `defineComponent` + `setup()` + `return {}` 模式。**

```typescript
// ✅ 正确 — defineComponent + setup return（方法可被父组件通过 ref 调用）
export default defineComponent({
    name: "XxxForm",
    components: { BasicForm },
    emits: ['register'],
    props: {
        disabled: { type: Boolean, default: false }
    },
    setup(props, { emit }) {
        const [registerForm, { setProps, resetFields, setFieldsValue, getFieldsValue, validate, scrollToField }] = useForm({
            labelWidth: 150,
            schemas: xxxFormSchema,
            showActionButtonGroup: false,
            baseColProps: { span: 24 }
        });

        function initFormData(url, id) {
            if (id) {
                defHttp.get({ url, params: { id } }, { isTransformResponse: false }).then(res => {
                    res.success && res.result.records && res.result.records.length > 0 && setFieldsValue({ ...res.result.records[0] });
                })
            }
            setProps({ disabled: props.disabled })
        }

        function getFormData() {
            let formData = getFieldsValue();
            Object.keys(formData).map(k => {
                if (formData[k] instanceof Array) { formData[k] = formData[k].join(',') }
            });
            return [formData];  // 返回数组！后端用 List<Entity> 接收
        }

        function validateForm(index) {
            return new Promise((resolve, reject) => {
                validate().then(() => { return resolve() })
                    .catch(({ errorFields }) => {
                        return reject({ error: VALIDATE_FAILED, index, errorFields, scrollToField })
                    })
            })
        }

        return { registerForm, resetFields, initFormData, getFormData, validateForm }
    }
})

// ❌ 错误 — <script setup> + defineExpose（父组件调用报 xxx is not a function）
// <script lang="ts" setup>
// const { initFormData, getFormData, validateForm, resetFields } = useXxx();
// defineExpose({ initFormData, getFormData, validateForm, resetFields });
// </script>
```

**规则24.4：内嵌子表风格 — Modal 必须使用 `useJvxeMethod` 6参数模式**
内嵌子表 (C12) 的 Modal 与默认/原始布局风格完全一致，同样使用 `useJvxeMethod` 的 6 参数模式。**不要自己编写 `handleSubmit`**，`useJvxeMethod` 返回的 `handleSubmit` 已内置表单校验、子表数据收集、`validateSubForm` 调用等完整逻辑。

```typescript
// Modal.vue 关键结构
const refKeys = ref(['demoProjBudget', 'demoProjTask']);  // 只有子表 key，不含主表
const activeKey = ref('demoProjBudget');
const demoProjBudgetForm = ref();    // 一对一子表 Form ref
const demoProjTask = ref();          // 一对多子表 JVxeTable ref
const tableRefs = { demoProjTask };  // ⚠️ 只包含 JVxeTable ref！

const demoProjTaskTable = reactive({
    loading: false,
    dataSource: [],
    columns: demoProjTaskJVxeColumns
});

// ✅ 6参数调用 useJvxeMethod
const [handleChangeTabs, handleSubmit, requestSubTableData, formRef] = useJvxeMethod(
    requestAddOrEdit, classifyIntoFormData, tableRefs, activeKey, refKeys, validateSubForm
);

// classifyIntoFormData — 组装提交数据
function classifyIntoFormData(allValues) {
    let main = Object.assign({}, allValues.formValue)
    return {
        ...main,
        demoProjBudgetList: demoProjBudgetForm.value.getFormData(),     // 一对一：调用 Form 的 getFormData()
        demoProjTaskList: allValues.tablesValue[0].tableData,           // 一对多：从 tablesValue 取（index 对应 tableRefs 中的顺序）
    }
}

// validateSubForm — 校验所有一对一子表
function validateSubForm(allValues) {
    return new Promise((resolve, reject) => {
        Promise.all([
            demoProjBudgetForm.value.validateForm(0),  // index 对应 refKeys 中的位置
        ]).then(() => {
            resolve(allValues)
        }).catch(e => {
            if (e.error === VALIDATE_FAILED) {
                activeKey.value = e.index == null ? unref(activeKey) : refKeys.value[e.index]
                if (e.errorFields) {
                    const firstField = e.errorFields[0];
                    if (firstField) { e.scrollToField(firstField.name, { behavior: 'smooth', block: 'center' }); }
                }
            } else { console.error(e) }
        })
    })
}

// Modal 打开时加载子表数据
const [registerModal, { setModalProps, closeModal }] = useModalInner(async (data) => {
    await reset();
    setModalProps({ confirmLoading: false, showCancelBtn: data?.showFooter, showOkBtn: data?.showFooter });
    isUpdate.value = !!data?.isUpdate;
    formDisabled.value = !data?.showFooter;
    if (unref(isUpdate)) {
        await setFieldsValue({ ...data.record });
        // 一对一子表：调用 Form 的 initFormData（传 URL 字符串 + 主表 id）
        demoProjBudgetForm.value.initFormData(queryDemoProjBudgetByMainId, data?.record?.id);
        // 一对多子表：调用 requestSubTableData（传 URL 字符串 + 参数 + reactive 表对象）
        requestSubTableData(queryDemoProjTaskByMainId, { id: data?.record?.id }, demoProjTaskTable);
    }
    setProps({ disabled: !data?.showFooter });
});

// reset — 重置所有表单和子表数据
async function reset() {
    await resetFields();
    activeKey.value = 'demoProjBudget';
    demoProjBudgetForm.value.resetFields();       // 一对一子表重置
    demoProjTaskTable.dataSource = [];             // 一对多子表清空数据
}
```

**规则24.5：内嵌子表风格 — api.ts 双导出模式（URL字符串 + API函数）**
每个子表需要两种导出方式，分别供 Modal 和 SubTable 使用：

```typescript
// api.ts
enum Api {
  // ...
  demoProjBudgetList = '/demo/demoProj/queryDemoProjBudgetByMainId',
  demoProjTaskList = '/demo/demoProj/queryDemoProjTaskByMainId',
}

// 1. URL 字符串导出 — 供 Modal 中 requestSubTableData / initFormData 使用
//    这些函数内部用 defHttp.get 默认 isTransformResponse:true，拿到的是 result 部分
export const queryDemoProjBudgetByMainId = Api.demoProjBudgetList;
export const queryDemoProjTaskByMainId = Api.demoProjTaskList;

// 2. 函数导出 — 供 SubTable 组件使用，isTransformResponse:false 返回完整 {success, result, ...}
export const demoProjBudgetListApi = (params) =>
  defHttp.get({ url: Api.demoProjBudgetList, params }, { isTransformResponse: false });
export const demoProjTaskListApi = (params) =>
  defHttp.get({ url: Api.demoProjTaskList, params }, { isTransformResponse: false });
```

**为什么需要两种？**
- Modal 中 `requestSubTableData(url, params, tableObj)` 内部执行 `defHttp.get({url, params})` 默认 `isTransformResponse:true`，拿到的直接是 `result` 对象（即 IPage），然后取 `res.records || res` 赋值给 `tableObj.dataSource`
- Modal 中 `initFormData(url, id)` 内部执行 `defHttp.get({url,params:{id}},{isTransformResponse:false})`，拿到完整响应，通过 `res.result.records[0]` 取第一条数据
- SubTable 中 `xxxListApi({id})` 用 `isTransformResponse:false`，通过 `res.result.records` 取数据数组

**规则25：Tab-in-Modal 风格 — Modal 必须用 radio-group 标题栏，不是 a-tabs**
Tab-in-Modal 风格的 Modal 使用 `a-radio-group` + `a-radio-button` 在标题栏切换主表/子表区域，各区域用 `v-show` 显隐（不是 `a-tab-pane`）。必须设置 `wrapClassName="j-cgform-tab-modal"` 启用专属样式，`contentArea` div 包裹所有表单区域。

```html
<BasicModal ref="modalRef" destroyOnClose wrapClassName="j-cgform-tab-modal" ...>
  <template #title>
    <div class="titleArea">
      <div class="title">{{ title }}</div>
      <div class="right">
        <a-radio-group v-model:value="activeKey">
          <a-radio-button v-for="item in tabNav" :value="item.tableName">{{ item.tableTxt }}</a-radio-button>
        </a-radio-group>
      </div>
    </div>
  </template>
  <div class="contentArea">
    <BasicForm v-show="activeKey == refKeys[0]" ... />
    <JVxeTable v-show="activeKey == 'subTableKey'" ... />
    <XxxForm v-show="activeKey == 'subOneKey'" ... />
  </div>
</BasicModal>
```

**规则26：Tab-in-Modal 风格 — 一对一子表必须抽成独立 Form.vue 组件**
一对一子表不能用内联 BasicForm（`useForm` + `registerDetailForm`），必须抽成独立的 Vue 组件（如 `XxxForm.vue`），使用 Options API（`defineComponent`）暴露以下方法：
- `initFormData(url, id)` — 加载数据，内部用 `defHttp.get({url,params:{id}},{isTransformResponse:false})`
- `getFormData()` — 返回 `[formData]` 数组（后端用 `List<Entity>` 接收）
- `validateForm(index)` — 校验表单，`index` 对应 `refKeys` 数组位置
- `resetFields()` — 重置表单

**规则27：Tab-in-Modal 风格 — useJvxeMethod 第6个参数 validateSubForm**
有一对一子表时，`useJvxeMethod` 必须传入第6个参数 `validateSubForm`，该函数在 `handleSubmit` 中自动调用。不需要自写 `handleSubmit`：

```typescript
const [handleChangeTabs, handleSubmit, requestSubTableData, formRef] = useJvxeMethod(
  requestAddOrEdit, classifyIntoFormData, tableRefs, activeKey, refKeys, validateSubForm
);
// validateSubForm 内部调用所有一对一子表的 validateForm(index)
```

**规则28：Tab-in-Modal 风格 — refKeys 和 JVxeTable ref 名必须一致**
`refKeys` 数组的值必须与 `v-show` 条件、JVxeTable 的 `ref` 名、`activeKey` 的值完全一致。`refKeys[0]` 固定为主表 key。

```typescript
const refKeys = ref(['mainKey', 'subManyKey', 'subOneKey']);
// JVxeTable: ref="subManyKey"   v-show="activeKey == 'subManyKey'"
// Form:      ref="subOneForm"   v-show="activeKey == 'subOneKey'"
```

**规则29：树表 — Mapper 接口参数名必须与 XML 参数名一致**
树表 Mapper 接口和 XML 的参数命名必须严格对齐，参考 JeecgBoot 代码生成器的标准输出：

```java
// Mapper 接口
void updateTreeNodeStatus(@Param("id") String id, @Param("status") String status);
List<SelectTreeModel> queryListByPid(@Param("pid") String pid, @Param("query") Map<String, String> query);
```

```xml
<!-- XML 中对应的参数名 -->
<update id="updateTreeNodeStatus">
    update {{tableName}} set has_child = #{status} where id = #{id}
</update>
<select id="queryListByPid" resultType="org.jeecg.common.system.vo.SelectTreeModel">
    select id as "key", {{displayField}} as "title",
           (case when has_child = '1' then 0 else 1 end) as isLeaf,
           {{pidField}} as parentId
    from {{tableName}} where {{pidField}} = #{pid}
    <if test="query != null">
        <foreach collection="query.entrySet()" item="value" index="key">
            and ${key} = #{value}
        </foreach>
    </if>
</select>
```

**规则30：树表 — Modal 的 updateSchema 禁止传递 treeData**
JTreeSelect 组件通过 `dict` 配置（如 `"demo_category,category_name,id"`）自行从后端加载树数据。`updateSchema` 只需传递 `hiddenNodeKey`，**禁止**传递 `treeData` 到 componentProps，否则会导致下拉框显示异常（label 变 value、内容不全）。

```typescript
// ❌ 错误 — 传递 treeData 会干扰 JTreeSelect 内部数据管理
updateSchema([{ field: 'pid', componentProps: { treeData, hiddenNodeKey: data.record.id } }]);

// ✅ 正确 — 只传 hiddenNodeKey
updateSchema([{ field: 'pid', componentProps: { hiddenNodeKey: data.record.id } }]);
```

`treeData` 变量仅用于 Modal 内部的 `getExpandKeysByPid` 函数（计算展开路径），不用于 JTreeSelect 组件。

**规则31：树表 — handleSuccess 必须遵循参考代码的刷新策略**
树表 `handleSuccess` 回调接收 `{isUpdate, values, expandedArr, changeParent}` 四个参数，刷新策略如下：

```typescript
async function handleSuccess({isUpdate, values, expandedArr, changeParent}) {
  if (isUpdate) {
    if (changeParent) {
      reload();  // 父节点变更，全量刷新
    } else {
      // 父节点未变，重新查询单条记录（含 _dictText 翻译）
      let data = await list({ id: values.id, pageSize: 1, pageNo: 1, pid: values['pid'] });
      if (data && data.records && data.records.length > 0) {
        updateTableDataRecord(values.id, data.records[0]);
      } else {
        updateTableDataRecord(values.id, values);
      }
    }
  } else {
    if (!values['id'] || !values['pid']) {
      reload();  // 新增根节点，全量刷新
    } else {
      // 新增子节点，逐级展开
      expandedRowKeys.value = [];  // ← 必须先清空！
      for (let key of unref(expandedArr)) {
        await expandTreeNode(key);
      }
    }
  }
}
```

关键点：
1. 编辑后必须**重新查询**单条数据（`list({id,...})`），不能直接用 form values 更新，否则字典列不显示翻译文本
2. 新增子节点前必须**先清空 `expandedRowKeys`**（`expandedRowKeys.value = []`），否则展开逻辑出错
3. 新增根节点判断条件是 `!values['id'] || !values['pid']`（form 提交后 id 为空因为是后端自动生成）

**规则32：树表 — getDataByResult 的 loading 占位节点必须使用正确的显示字段**
`getDataByResult` 为有子节点的数据添加 loading 占位，占位节点的显示字段名必须与表的树节点主显示列一致：

```typescript
// 如果 columns 第一列 dataIndex 是 'categoryName'
let loadChild = { id: item.id + '_loadChild', categoryName: 'loading...', isLoading: true }
// 如果 columns 第一列 dataIndex 是 'name'
let loadChild = { id: item.id + '_loadChild', name: 'loading...', isLoading: true }
```

使用错误的字段名（如统一用 `name`）会导致 loading 文本不显示。

**规则33：树表 — 前端代码必须完全对齐参考代码结构**
树表前端与单表有根本性差异，生成时必须严格按以下清单：

**List.vue 必须包含：**
- `isTreeTable: true` in tableProps
- `expandedRowKeys` ref + `@expand="handleExpand"` + `@fetch-success="onFetchSuccess"`
- `beforeFetch` 必须添加 `params.hasQuery = "true"`
- `queryParam` reactive + `superQueryConfig` + 高级查询组件
- `v-auth` 权限指令在所有操作按钮上
- `getTableAction` 主操作（编辑 + 添加下级）+ `getDropDownAction` 下拉操作（详情 + 删除）
- `actionColumn` 必须设置 `width: 240` 和 `fixed: 'right'`
- `handleExpand` 中必须处理 `result.records`：`result = result.records ? result.records : result`
- `handleAddSub` 传递 `{pidField: record.id}` 作为 record（pidField 即 pid 字段名）
- `batchHandleDelete` 必须过滤 loadChild 占位：`ids.filter(item => !item.includes('loadChild'))`

**Modal.vue 必须包含：**
- `let model: Nullable<Recordable> = null` 保存编辑前数据
- `treeData` ref 用于 `getExpandKeysByPid`（不传给 JTreeSelect）
- `setModalProps({ showOkBtn: !!!data?.hideFooter })` 详情模式隐藏确认按钮
- `setProps({ disabled: !!data?.hideFooter })` 详情模式禁用表单
- `isDetail.value = !!data?.showFooter`（注意是 showFooter 不是 hideFooter）
- 编辑时 `updateSchema` 只传 `hiddenNodeKey`
- `handleSubmit` 中 `emit('success', {isUpdate, values, expandedArr, changeParent})`
- `changeParent` 判断：`model != null && (model['pid'] != values['pid'])`
- `scrollToField` 在 catch 块中处理校验错误定位
- `baseRowStyle: { padding: "0 20px" }` 表单行内边距

**data.ts 必须包含：**
- `id` 隐藏字段放在 formSchema **最后**
- `pid` 字段用 `JTreeSelect` 组件，配置 `dict/pidField/pidValue/hasChildField`
- 树表主显示列的 `align` 必须是 `'left'`（便于显示层级缩进）
- `superQuerySchema` 每项需包含 `type` 字段

**api.ts 必须包含：**
- `rootList`（不是 `list`）、`childList`、`getChildListBatch`、`loadTreeData` 四个树表专用接口
- `getChildListBatch` 必须使用 `{isTransformResponse: false}` 返回完整 Result 对象

---

### 智能字段推导中的字典关键词

当用户描述字段时，按以下关键词自动推导使用哪种字典：

| 用户描述关键词 | 推导字典类型 | 推荐控件 |
|--------------|------------|---------|
| "状态"、"类型"、"级别"、"优先级" | 系统字典（先搜索 sys_dict 匹配） | JDictSelectTag |
| "区域"、"地区"、"分类"、"类目"、"树形选择" | 分类字典（搜索 sys_category 匹配） | JCategorySelect |
| "部门"、"组织"、"归属" | 表字典（关联 sys_depart） | JDictSelectTag(表字典) |
| "用户"、"负责人"、"经办人" | 用户选择组件（非字典） | JSelectUserByDept |

## 项目路径

> **重要：** 以下为默认路径。实际路径以 `CLAUDE.md` 和 memory 中的配置为准，优先使用它们。

| 类别 | 路径 |
|------|------|
| 后端根 | 读取 `CLAUDE.md` 中的 Backend 路径 |
| 前端根 | 读取 `CLAUDE.md` 中的 Frontend 路径 |
| 后端代码 | `{module}/src/main/java/org/jeecg/modules/{entityPackage}/` |
| 前端代码 | `src/views/{viewDir}/` |
| Flyway SQL | `jeecg-module-system/jeecg-system-start/src/main/resources/flyway/sql/mysql/` |

## 命名约定

- **表名**：snake_case（如 `biz_goods`）
- **实体名**：表名转 PascalCase（如 `BizGoods`）
- **entityPackage**：表名前缀或用户指定（如 `biz`）
- **bussiPackage** 固定：`org.jeecg.modules`
- **权限编码**：`{entityPackage}:{tableName}:add/edit/delete/deleteBatch/exportXls/importExcel`

## 智能字段推导

**用于新建表场景（从自然语言推导），或已有表但字段无注释时的补充推导：**

| 语义关键词 | dbType | Java 类型 | vue3 组件 | vue3Native 组件 |
|-----------|--------|----------|----------|----------------|
| 名称/标题/编码 | varchar(100) | String | Input | a-input |
| 金额/价格/费用 | decimal(10,2) | BigDecimal | InputNumber | a-input-number |
| 数量/数目/个数 | int | Integer | InputNumber | a-input-number |
| 状态/类型/级别 | varchar(10) | String | JDictSelectTag | JDictSelectTag |
| 是否/开关 | varchar(2) | String | Switch | a-switch |
| 日期/生日 | date | Date | DatePicker | a-date-picker |
| 时间/日期时间 | datetime | Date | DatePicker(showTime) | a-date-picker(showTime) |
| 备注/描述/说明 | text | String | InputTextArea | a-textarea |
| 内容/富文本 | text | String | JEditor | JEditor |
| 图片/头像/照片 | varchar(1000) | String | JImageUpload | JImageUpload |
| 文件/附件 | varchar(1000) | String | JUpload | JUpload |
| 用户/负责人 | varchar(32) | String | JSelectUserByDept | JSelectUserByDept |
| 部门/组织 | varchar(32) | String | JSelectDept | JSelectDept |
| 排序/序号 | int | Integer | InputNumber | a-input-number |

**已有表场景的 DB类型→控件 映射（当字段无注释时使用）：**

| DB列类型 | Java类型 | 默认前端控件 |
|---------|---------|-----------|
| varchar(n) n<=200 | String | Input |
| varchar(n) n>200 | String | InputTextArea |
| text / longtext | String | InputTextArea |
| int / tinyint | Integer | InputNumber |
| bigint | Long | InputNumber |
| decimal / double / float | BigDecimal | InputNumber |
| date | Date | DatePicker |
| datetime / timestamp | Date | DatePicker(showTime) |

## 主键策略（根据已有表结构自适应）

| 表DDL中的主键定义 | Java类型 | @TableId | 说明 |
|------------------|---------|----------|------|
| `int AUTO_INCREMENT` | Integer | `@TableId(type = IdType.AUTO)` | int自增主键 |
| `bigint AUTO_INCREMENT` | Long | `@TableId(type = IdType.AUTO)` | bigint自增主键 |
| `varchar(36)` / `varchar(32)` 无AUTO_INCREMENT | String | `@TableId(type = IdType.ASSIGN_ID)` | JeecgBoot标准字符串主键 |
| `bigint` 无AUTO_INCREMENT | Long | `@TableId(type = IdType.ASSIGN_ID)` | 雪花ID |

**注意：** 当主键为 Integer/Long 类型时，Controller 中 `delete` 和 `queryById` 的参数类型也要对应调整。

## 系统字段（按实际表结构判断）

**不是所有表都有系统字段！** 生成前必须检查表是否实际包含这些字段，**只生成表中存在的字段**：

| 字段 | 说明 | 不存在时的处理 |
|------|------|--------------|
| `create_by` | 创建人 | 不生成该属性 |
| `create_time` | 创建时间 | 不生成该属性 |
| `update_by` | 更新人 | 不生成该属性 |
| `update_time` | 更新时间 | 不生成该属性 |
| `sys_org_code` | 所属部门 | 不生成该属性 |

如果是**新建表**（用户自然语言描述需求），则默认添加全部系统字段。
如果是**已有表**（用户指定了表名且数据库中已存在），则必须根据实际 DDL 来决定。

树表额外字段：`pid`、`has_child`（同样需检查是否实际存在）。

## 参考文件

生成代码前，**必须读取** 同目录下的 `codegen-reference.md` 获取完整代码模板骨架。

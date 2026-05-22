---
name: jeecg-uniapp-codegen
description: "JeecgBoot UniApp3 移动端 CRUD 代码生成器。Use when user asks to generate UniApp3/mobile/APP CRUD pages, create mobile list/form pages, or says '生成移动端代码', '生成APP页面', 'uniapp代码生成', '移动端CRUD', '生成uniapp页面', '手机端页面', '移动端模块', 'generate uniapp code', 'mobile CRUD', 'uniapp page', 'APP端代码', '生成小程序页面', '生成H5页面'. Also triggers when user mentions generating mobile pages for an existing backend module, or wants to add mobile support to JeecgBoot modules. Even if user just says '给XX模块加个移动端页面' or '做个手机端的XX功能', this skill should trigger."
---

# JeecgBoot UniApp3 移动端 CRUD 代码生成器

将自然语言需求或已有后端接口信息转换为 JeecgBoot UniApp3 移动端全套 CRUD 代码（列表页 + 表单页 + 数据定义），支持单表 CRUD、一对多主子表、树表等场景。

> **项目路径：** `<uniapp_project_root>`（动态，使用前需向用户确认，见 Step 0）
> **后端模板参考：** `<uniapp_project_root>` 同级目录下的后端项目（如有）

## 前置知识

生成代码前必须理解以下项目核心约定，具体细节见 `references/` 目录下的参考文件：

| 参考文件 | 内容 |
|---------|------|
| `references/project-architecture.md` | 项目结构、目录约定、页面注册机制 |
| `references/component-patterns.md` | 组件库用法、表单控件映射、在线组件清单 |
| `references/code-templates.md` | 三个核心前端文件的完整模板和变量说明 |

## 交互流程

### Step 0: 确认项目路径

**在执行任何操作之前，必须先询问用户以下信息（一次性展示，用户说"确认"使用默认值）：**

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| UniApp3 项目根目录 | —（必填） | 如 `D:\projects\jeecgboot-uniapp3` |

用户回复后，记为：
- `<uniapp_project_root>` — 前端项目根目录

> **路径记忆规则：** 同一对话中用户提供一次后，后续步骤直接复用，不再重复询问。

### Step 1: 判断生成场景

**场景 A — 已有后端接口（用户给了表名/实体名/接口路径）：**
1. 向用户确认后端 API 路径前缀（如 `/test/demo`）
2. 从用户信息中提取：实体名（如 `Demo`）、包路径（如 `test`）、字段列表
3. 如果用户能提供后端 Entity 类，从中解析全部字段及类型
4. 根据字段类型自动推导前端控件
5. 只生成前端代码

**场景 B — 从需求描述生成前端：**
1. 从用户描述中提取：模块名、功能描述、字段列表
2. 用"智能控件推导"规则推导每个字段的 `classType`
3. 只生成前端 3 个文件（List.vue / Form.vue / Data.ts）

### Step 2: 确认生成信息

一次性展示所有选项及默认值，用户说"确认"即可全部采用：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| 实体名 | 从需求推导（PascalCase） | 如 `BizGoods` |
| 功能描述 | 从需求推导 | 导航栏标题，如 "商品管理" |
| 页面目录 | `<uniapp_project_root>/src/pages-home/{模块名}/` | 生成文件的存放目录 |
| API路径前缀 | `/{模块包路径}/{实体名首字母小写}` | 如 `/biz/bizGoods` |
| 列表展示字段 | 前3个非id非系统字段 | 列表卡片上显示的字段 |

### Step 3: 生成代码文件

#### 前端文件

每个单表 CRUD 模块生成 **3 个文件**，路径基于 `<uniapp_project_root>`：

```
<uniapp_project_root>/src/pages-home/{模块名}/
  ├── {EntityName}List.vue    # 列表页（分页 + 滑动删除 + 新增入口）
  ├── {EntityName}Form.vue    # 表单页（新增/编辑 + 表单校验 + 提交）
  └── {EntityName}Data.ts     # 列表字段列定义
```

### Step 4: 注册页面路由

在 `<uniapp_project_root>/src/pages.json` 的 `subPackages` 中注册新页面（如果目标目录已是 subPackage 则追加 pages，否则新增 subPackage）。

### Step 5: 输出生成摘要

展示生成的文件清单、页面路由配置、后续操作说明。

---

## 字段控件类型推导规则

根据字段信息推导 `classType`（决定表单使用哪个组件）：

| 字段特征 | classType | 表单组件 |
|----------|-----------|----------|
| 名称含"图片/头像/照片/logo" | `image` | `<online-image>` |
| 名称含"文件/附件/简历" | `file` | `<online-file-custom>` |
| 名称含"日期" 且无"时间" | `date` | `<online-date>` |
| 名称含"时间" 或 "datetime" | `datetime` | `<DateTime>` |
| 名称含"开关/启用/是否" | `switch` | `<wd-switch>` |
| 有字典值（枚举选项 <= 5个） | `radio` | `<online-radio>` |
| 有字典值（枚举选项 > 5个） | `list` | `<online-select>` |
| 名称含"多选" 或需多选字典 | `checkbox` | `<online-checkbox>` |
| 名称含"备注/描述/内容/简介" | `textarea` | `<wd-textarea>` |
| 名称含"密码" | `password` | `<wd-input show-password>` |
| 名称含"省市区/地址" | `pca` | `<online-pca>` |
| 名称含"部门" | `sel_depart` | `<select-dept>` |
| 名称含"用户/人员/负责人" | `sel_user` | `<select-user>` |
| 名称含"分类" 且有树结构 | `cat_tree` | `<CategorySelect>` |
| DB类型为 int/long/double/BigDecimal | 数字输入 | `<wd-input inputMode="numeric">` |
| 默认（字符串类型） | 文本输入 | `<wd-input>` |

## 字段校验规则推导

| 场景 | 校验规则 |
|------|----------|
| 必填字段（nullable=N） | `{ required: true, message: '请输入${comment}!' }` |
| 手机号 | `{ pattern: /^1[3456789]\d{9}$/, message: '请输入正确的手机号码!' }` |
| 邮箱 | `{ pattern: /^([\w]+\.*)([\w]+)@[\w]+\.\w{3}(\.\w{2}\|)$/, message: '请输入正确的电子邮件!' }` |
| 网址 | `{ pattern: /^((ht\|f)tps?):\/\/.../, message: '请输入正确的网址!' }` |
| 数字 | `{ pattern: /^-?\d+\.?\d*$/, message: '请输入数字!' }` |
| 整数 | `{ pattern: /^-?\d+$/, message: '请输入整数!' }` |
| 金额 | `{ pattern: /^(([1-9][0-9]*)\|([0]\.\d{0,2}\|[1-9][0-9]*\.\d{0,2}))$/, message: '请输入正确的金额!' }` |

---

## 生成代码的核心规范

### 1. 列表页（{EntityName}List.vue）规范

```
关键特征：
- 使用 <route> 标签声明页面路由信息（layout、style、navigationBarTitleText）
- 使用 <PageLayout> 包裹，设置 navTitle 和 backRouteName
- 使用 z-paging 实现分页加载
- 使用 wd-swipe-action 实现左滑删除
- 使用 usePageList hook 管理列表数据加载
- 引入 {EntityName}Data.ts 的 columns 定义
- 列表卡片默认展示前3个字段
- 固定定位的"+"按钮用于新增
- uni.$on('refreshList') 监听表单提交后的列表刷新
```

详细模板见 `references/code-templates.md` 的"列表页模板"章节。

### 2. 表单页（{EntityName}Form.vue）规范

```
关键特征：
- 使用 <route> 标签声明页面路由信息
- 使用 <PageLayout> 包裹，navTitle 动态切换"新增/编辑"
- 使用 wd-form + wd-cell-group 组织表单
- 通过 onLoad 获取 route params 中的 dataId 判断新增/编辑
- 编辑时调用 queryById 接口加载数据
- 表单数据用 reactive({}) 定义
- 提交时先 form.validate()，再根据 dataId 调用 add 或 edit 接口
- 提交成功后 uni.$emit('refreshList') 通知列表刷新，然后 router.back()
- 根据字段 classType 渲染对应组件（见组件映射表）
- 支持唯一性校验（调用 duplicateCheck API）
- label 超过4个字符时自动截断（get4Label）
```

详细模板见 `references/code-templates.md` 的"表单页模板"章节。

### 3. 数据定义（{EntityName}Data.ts）规范

```
关键特征：
- 导出 columns 数组，定义列表显示的字段
- 每个字段包含 title（显示名）和 dataIndex（字段名）
- 字典类型字段的 dataIndex 使用 `${fieldName}_dictText` 后缀
- 图片类型字段添加 customRender: render.renderImage
- 开关类型字段添加 customRender 渲染是/否文本
- Blob 类型字段的 dataIndex 使用 `${fieldName}String` 后缀
```

详细模板见 `references/code-templates.md` 的"数据定义模板"章节。

### 4. 页面路由注册

生成的页面需要在 `src/pages.json` 的 `subPackages` 中注册。使用 `<route>` 标签方式（uni-pages 插件自动解析），或手动在 pages.json 中添加。

**`<route>` 标签格式（推荐，写在 .vue 文件顶部）：**
```vue
<route lang="json5" type="page">
{
  layout: 'default',
  style: {
    navigationBarTitleText: '功能标题',
    navigationStyle: 'custom',
  },
}
</route>
```

**如果目标目录不在已有 subPackages 中，需要手动在 pages.json 添加：**
```json
{
  "root": "pages-home",
  "pages": [
    {
      "path": "模块目录/EntityNameList",
      "type": "page",
      "layout": "default",
      "style": {
        "navigationBarTitleText": "功能标题",
        "navigationStyle": "custom"
      }
    },
    {
      "path": "模块目录/EntityNameForm",
      "type": "page",
      "layout": "default",
      "style": {
        "navigationBarTitleText": "功能标题",
        "navigationStyle": "custom"
      }
    }
  ]
}
```

---

## API 约定

JeecgBoot 后端标准 CRUD 接口路径：

| 操作 | 方法 | 路径 |
|------|------|------|
| 分页列表 | GET | `/{packagePath}/{entityName}/list` |
| 查询单条 | GET | `/{packagePath}/{entityName}/queryById?id=xxx` |
| 新增 | POST | `/{packagePath}/{entityName}/add` |
| 编辑 | POST | `/{packagePath}/{entityName}/edit` |
| 删除 | DELETE | `/{packagePath}/{entityName}/delete?id=xxx` |
| 唯一性校验 | GET | `/sys/duplicate/check` |

HTTP 工具使用 `@/utils/http` 的 `http` 对象，支持 `http.get()` / `http.post()` / `http.delete()` / `http.put()` 方法。

---

## 导入约定

### 列表页必须导入
```typescript
import { ref, onMounted, computed } from 'vue'
import { http } from '@/utils/http'
import usePageList from '@/hooks/usePageList'
import { columns } from './{EntityName}Data'
```

### 表单页必须导入
```typescript
import { onLoad } from '@dcloudio/uni-app'
import { http } from '@/utils/http'
import { useToast } from 'wot-design-uni'
import { useRouter } from '@/plugin/uni-mini-router'
import { ref, onMounted, computed, reactive } from 'vue'
import { duplicateCheck } from '@/service/api'
```

### 根据字段 classType 按需导入的组件

| classType | 导入语句 |
|-----------|----------|
| `image` | `import OnlineImage from '@/components/online/view/online-image.vue'` |
| `file` | `import OnlineFileCustom from '@/components/online/view/online-file-custom.vue'` |
| `datetime` / `time` | `<DateTime>` 组件（easycom 自动注册，位于 `@/components/DateTime/DateTime.vue`） |
| `date` | `import OnlineDate from '@/components/online/view/online-date.vue'` |
| `list` / `sel_search` | `import OnlineSelect from '@/components/online/view/online-select.vue'` |
| `checkbox` | `import OnlineCheckbox from '@/components/online/view/online-checkbox.vue'` |
| `radio` | `import OnlineRadio from '@/components/online/view/online-radio.vue'` |
| `list_multi` | `import OnlineMulti from '@/components/online/view/online-multi.vue'` |
| `textarea` | 无需导入（使用 wot-design-uni 的 `<wd-textarea>`，easycom 自动注册） |
| `password` | 无需导入（使用 `<wd-input show-password>`，easycom 自动注册） |
| `pca` | `import OnlinePca from '@/components/online/view/online-pca.vue'` |
| `sel_depart` | `import SelectDept from '@/components/SelectDept/SelectDept.vue'` |
| `sel_user` | `import SelectUser from '@/components/SelectUser/SelectUser.vue'` |
| `popup_dict` | `<PopupDict>` 组件（easycom 自动注册，位于 `@/components/PopupDict/PopupDict.vue`） |
| `popup` | `<Popup>` 组件（easycom 自动注册，位于 `@/components/Popup/Popup.vue`） |
| `link_table` | `import OnlinePopupLinkRecord from '@/components/online/view/online-popup-link-record.vue'` |
| `cat_tree` | `<CategorySelect>` 组件（easycom 自动注册，位于 `@/components/CategorySelect/CategorySelect.vue`） |
| `sel_tree` | `<TreeSelect>` 组件（easycom 自动注册，位于 `@/components/TreeSelect/TreeSelect.vue`） |
| `switch` | 无需导入（使用 `<wd-switch>`，easycom 自动注册） |

> **easycom 说明：** 位于 `src/components/` 下且目录名与组件名一致的组件会被 easycom 自动注册，无需手动 import。
> `wd-*` 前缀的组件由 wot-design-uni 提供，也通过 easycom 自动注册。
> `online-*` 前缀的组件位于 `src/components/online/view/`，**不符合 easycom 规则，必须手动 import**。

---

## 一对多（主子表）场景

当前后端代码生成模板仅有单表模板，一对多场景需手动编写。核心模式：

1. **列表页**：与单表列表页相同，展示主表数据
2. **表单页**：在主表表单下方增加 Tab 切换子表，每个子表用独立的列表+新增/编辑弹窗
3. **子表数据**：使用主表 ID 作为外键查询，新增时传入主表 ID

这是高级场景，参考 `references/advanced-patterns.md`（如需要时创建）。

---

## 树表场景

当前后端代码生成模板无树表 uniapp3 模板。树表移动端通常采用：

1. 使用 `<TreeSelect>` 组件展示树形数据
2. 列表页改为树形选择 + 子节点列表的组合
3. 表单页增加"上级节点"选择器

这是高级场景，参考 `references/advanced-patterns.md`（如需要时创建）。

---

---

## 生成检查清单

生成代码后自查：

- [ ] 所有 `.vue` 文件顶部有 `<route>` 标签
- [ ] `defineOptions` 中的 `name` 与文件名一致
- [ ] 列表页的 `usePageList` 参数路径正确（与后端 API 匹配）
- [ ] 表单页的 `backRouteName` 指向列表页名称
- [ ] 列表页的 `handleAdd` 跳转到 `{EntityName}Form`
- [ ] 表单页的 `add`/`edit`/`queryById` API 路径正确
- [ ] 字典类型字段传入了正确的 `dict` 属性值
- [ ] 必填字段设置了 `:required="true"` 和 `rules`
- [ ] 表单页导入了所有用到的 online 组件
- [ ] `{EntityName}Data.ts` 中字典字段的 `dataIndex` 使用了 `_dictText` 后缀
- [ ] pages.json 中已注册新页面（或 `<route>` 标签能被 uni-pages 插件识别）

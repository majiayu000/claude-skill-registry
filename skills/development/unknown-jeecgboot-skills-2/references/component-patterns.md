# 组件库用法与表单控件映射

## UI 组件库：wot-design-uni

项目使用 [wot-design-uni](https://wot-design-uni.pages.dev/) 作为主 UI 库，所有 `wd-*` 前缀组件通过 easycom 自动注册。

### 常用表单组件

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `<wd-input>` | 文本输入 | `label`, `v-model`, `placeholder`, `prop`, `name`, `clearable`, `:rules`, `label-width` |
| `<wd-textarea>` | 多行文本 | `label`, `v-model`, `:maxlength`, `prop`, `name`, `clearable` |
| `<wd-switch>` | 开关 | `v-model`, `size`, `active-value`, `inactive-value` |
| `<wd-form>` | 表单容器 | `ref="form"`, `:model` |
| `<wd-cell-group>` | 表单分组 | `border` |
| `<wd-cell>` | 单元格容器 | `:title`, `title-width`, `:required`, `center` |
| `<wd-button>` | 按钮 | `block`, `:loading`, `:disabled`, `@click` |
| `<wd-swipe-action>` | 滑动操作 | 配合 `#right` 插槽使用 |
| `<wd-navbar>` | 导航栏 | 由 PageLayout 封装，一般不直接使用 |
| `<wd-select-picker>` | 选择器 | `type="radio"`, `filterable`, `v-model`, `:columns` |
| `<wd-picker>` | 选择器(微信) | 微信小程序端替代 select-picker |
| `<wd-datetime-picker>` | 日期时间选择 | `label`, `v-model`, `placeholder`, `prop` |

### 表单校验规则格式

```typescript
:rules="[
  { required: true, message: '请输入xxx!' },
  { pattern: /^正则$/, message: '格式错误!' }
]"
```

## 分页组件：z-paging

项目使用 [z-paging](https://z-paging.zxlee.cn/) 处理分页加载，通过 easycom 自动注册。

### 基本用法

```vue
<z-paging
  ref="paging"
  :fixed="false"
  v-model="dataList"
  @query="queryList"
  :default-page-size="15"
>
  <!-- 列表内容 -->
</z-paging>
```

- `ref="paging"` 对应 `usePageList` 返回的 `paging`
- `v-model` 绑定列表数据
- `@query` 绑定查询函数（由 z-paging 自动调用，传入 pageNo 和 pageSize）
- `paging.value.reload()` 重新加载数据
- `paging.value.complete(records)` 传入查询结果

## PageLayout 组件

每个页面必须使用 `<PageLayout>` 作为根容器：

```vue
<PageLayout navTitle="页面标题" backRouteName="EntityNameList" routeMethod="pushTab">
  <!-- 页面内容 -->
</PageLayout>
```

### 关键属性

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| navTitle | String | '' | 导航栏标题 |
| backRouteName | String | '' | 返回路由名称 |
| backRoutePath | String | '' | 返回路由路径 |
| routeMethod | String | 'replace' | 路由跳转方式：replace/push/pushTab |
| navbarShow | Boolean | true | 是否显示导航栏 |
| navLeftText | String | '返回' | 左侧文字 |
| navLeftArrow | Boolean | true | 是否显示返回箭头 |
| navRightText | String | '' | 右侧文字 |
| type | String | 'page' | page 或 popup |

**列表页**通常设置 `backRouteName="index" routeMethod="pushTab"`（返回首页）
**表单页**通常动态设置 `:navTitle="navTitle"`（新增/编辑切换），`backRouteName` 指向列表页名

## Online 组件集合

位于 `src/components/online/view/`，**必须手动 import**（不符合 easycom 规则）。

### online-select 下拉选择

```vue
<online-select
  :label="'字段名'"
  labelWidth="100px"
  type="list"
  name="'fieldName'"
  dict="dictCode"
  v-model="formData['fieldName']"
/>
```

- `dict` 属性：字符串类型的字典编码（如 `"sex"`）或表字典（如 `"sys_user,realname,id"`）
- `type`: `list`（普通下拉）或 `sel_search`（带搜索下拉）
- 内部会自动调用 `/sys/dict/getDictItems/{dictCode}` 获取选项

### online-radio 单选

```vue
<online-radio
  :label="'字段名'"
  labelWidth="100px"
  type="radio"
  name="'fieldName'"
  dict="dictCode"
  v-model="formData['fieldName']"
/>
```

### online-checkbox 多选

```vue
<online-checkbox
  :label="'字段名'"
  labelWidth="100px"
  type="checkbox"
  name="'fieldName'"
  dict="dictCode"
  v-model="formData['fieldName']"
/>
```

### online-multi 多选下拉

```vue
<online-multi
  :label="'字段名'"
  labelWidth="100px"
  type="list_multi"
  name="'fieldName'"
  dict="dictCode"
  v-model="formData['fieldName']"
/>
```

### online-date 日期选择

```vue
<online-date
  :label="'字段名'"
  labelWidth="100px"
  type="date"
  name="'fieldName'"
  v-model:value="formData['fieldName']"
/>
```

注意：使用 `v-model:value`（而非 `v-model`）。

### online-image 图片上传

```vue
<wd-cell :title="'字段名'" title-width="100px">
  <online-image
    v-model:value="formData['fieldName']"
    name="'fieldName'"
    :maxNum="1"
  />
</wd-cell>
```

注意：需要包裹在 `<wd-cell>` 中，使用 `v-model:value`。

### online-file-custom 文件上传

```vue
<wd-cell :title="'字段名'" title-width="100px">
  <online-file-custom
    v-model:value="formData['fieldName']"
    name="'fieldName'"
  />
</wd-cell>
```

注意：需要包裹在 `<wd-cell>` 中，使用 `v-model:value`。

### online-pca 省市区选择

```vue
<online-pca
  :label="'字段名'"
  labelWidth="100px"
  name="'fieldName'"
  prop="'fieldName'"
  clearable
  v-model:value="formData['fieldName']"
/>
```

### online-popup-link-record 关联记录弹窗

```vue
<online-popup-link-record
  :label="'字段名'"
  labelWidth="100px"
  name="'fieldName'"
  :formSchema="getFormSchema('tableName','fieldName','fieldText')"
  v-model:value="formData['fieldName']"
/>
```

## 其他业务组件

### DateTime 日期时间选择

```vue
<DateTime
  :label="'字段名'"
  labelWidth="100px"
  type="datetime"
  format="YYYY-MM-DD HH:mm:ss"
  name="'fieldName'"
  v-model="formData['fieldName']"
/>
```

- `type`: `datetime`（日期时间）或 `time`（仅时间）
- `format`: `datetime` 用 `"YYYY-MM-DD HH:mm:ss"`，`time` 用 `"HH:mm:ss"`

### SelectUser 用户选择

```vue
<select-user
  labelWidth="100px"
  :label="'字段名'"
  name="'fieldName'"
  v-model="formData['fieldName']"
/>
```

### SelectDept 部门选择

```vue
<select-dept
  labelWidth="100px"
  :label="'字段名'"
  name="'fieldName'"
  v-model="formData['fieldName']"
  :multiple="true"
/>
```

### CategorySelect 分类树选择

```vue
<CategorySelect
  labelWidth="100px"
  :label="'字段名'"
  v-model="formData['fieldName']"
  pcode="dictCode"
/>
```

### TreeSelect 自定义树选择

```vue
<TreeSelect
  labelWidth="100px"
  :label="'字段名'"
  v-model="formData['fieldName']"
  dict="tableName,textField,valueField"
  :pidValue="`pidFieldValue`"
/>
```

### PopupDict 弹窗字典选择

```vue
<PopupDict
  labelWidth="100px"
  :label="'字段名'"
  v-model="formData['fieldName']"
  :multi="false"
  dictCode="tableName,textField,valueField"
/>
```

### Popup 弹窗选择（带回填）

```vue
<Popup
  labelWidth="100px"
  :label="'字段名'"
  v-model="formData['fieldName']"
  :multi="false"
  code="popupCode"
  :setFieldsValue="setFieldsValue"
  :fieldConfig="[
    { source: 'sourceField', target: 'targetField' },
  ]"
/>
```

## 表单组件中 name 属性的特殊写法

在代码生成模板中，`name` 属性使用字符串字面量（带引号）：

```vue
name="'fieldName'"
```

注意：这是 `name='fieldName'` 的等价写法，字段名需要用引号包裹。
对于 Blob 类型字段，使用 `'fieldNameString'`。

## 开关组件特殊处理

```vue
<wd-cell :label="'启用状态'" name="'status'" title-width="100px" center>
  <wd-switch
    :label="'启用状态'"
    name="'status'"
    size="18px"
    v-model="formData['status']"
    active-value="Y"
    inactive-value="N"
  />
</wd-cell>
```

默认 `active-value="Y"`, `inactive-value="N"`，如有自定义字典值则按实际设置。

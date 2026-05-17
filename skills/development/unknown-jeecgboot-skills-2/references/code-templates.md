# 代码生成模板

本文件包含三个核心文件的完整代码模板。模板中使用 `{变量名}` 表示需要替换的占位符。

## 目录

1. [列表页模板 ({EntityName}List.vue)](#列表页模板)
2. [表单页模板 ({EntityName}Form.vue)](#表单页模板)
3. [数据定义模板 ({EntityName}Data.ts)](#数据定义模板)
4. [变量说明](#变量说明)
5. [表单字段渲染规则](#表单字段渲染规则)
6. [完整生成示例](#完整生成示例)

---

## 列表页模板

文件路径：`src/pages-home/{moduleName}/{EntityName}List.vue`

```vue
<route lang="json5" type="page">
{
  layout: 'default',
  style: {
    navigationBarTitleText: '{功能描述}',
    navigationStyle: 'custom',
  },
}
</route>
<template>
  <PageLayout navTitle="{功能描述}" backRouteName="index" routeMethod="pushTab">
    <view class="wrap">
      <z-paging
        ref="paging"
        :fixed="false"
        v-model="dataList"
        @query="queryList"
        :default-page-size="15"
      >
        <template v-for="item in dataList" :key="item.id">
          <wd-swipe-action>
            <view class="list" @click="handleEdit(item)">
              <template v-for="(cItem, cIndex) in columns" :key="cIndex">
                <view v-if="cIndex < 3" class="box" :style="getBoxStyle">
                  <view class="field ellipsis">{{ cItem.title }}</view>
                  <view class="value cu-text-grey">{{ item[cItem.dataIndex] }}</view>
                </view>
              </template>
            </view>
            <template #right>
              <view class="action">
                <view class="button" @click="handleAction('del', item)">删除</view>
              </view>
            </template>
          </wd-swipe-action>
        </template>
      </z-paging>
      <view class="add u-iconfont u-icon-add" @click="handleAdd"></view>
    </view>
  </PageLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { http } from '@/utils/http'
import usePageList from '@/hooks/usePageList'
import { columns } from './{EntityName}Data'

defineOptions({
  name: '{EntityName}List',
  options: {
    styleIsolation: 'shared',
  },
})

// 分页加载配置
let { toast, router, paging, dataList, queryList } = usePageList('/{apiPathPrefix}/list')

// 样式
const getBoxStyle = computed(() => {
  return { width: 'calc(33% - 5px)' }
})

// 其他操作
const handleAction = (val, item) => {
  if (val == 'del') {
    http.delete('/{apiPathPrefix}/delete?id=' + item.id, { id: item.id }).then((res) => {
      toast.success('删除成功~')
      paging.value.reload()
    })
  }
}

// go 新增页
const handleAdd = () => {
  router.push({
    name: '{EntityName}Form',
  })
}

// go 编辑页
const handleEdit = (record) => {
  router.push({
    name: '{EntityName}Form',
    params: { dataId: record.id },
  })
}

onMounted(() => {
  // 监听刷新列表事件
  uni.$on('refreshList', () => {
    queryList(1, 10)
  })
})
</script>

<style lang="scss" scoped>
.wrap {
  height: 100%;
}
:deep(.wd-swipe-action) {
  margin-top: 10px;
  background-color: #fff;
}
.list {
  padding: 10px 10px;
  width: 100%;
  text-align: left;
  display: flex;
  justify-content: space-between;
  .box {
    width: 33%;
    .field {
      margin-bottom: 10px;
      line-height: 20px;
    }
  }
}
.action {
  width: 60px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  .button {
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 1;
    height: 100%;
    color: #fff;
    &:first-child {
      background-color: #fa4350;
    }
  }
}
.add {
  height: 70upx;
  width: 70upx;
  text-align: center;
  line-height: 70upx;
  background-color: #fff;
  border-radius: 50%;
  position: fixed;
  bottom: 80upx;
  right: 30upx;
  box-shadow: 0 0 5px 2px rgba(0, 0, 0, 0.1);
  color: #666;
}
</style>
```

---

## 表单页模板

文件路径：`src/pages-home/{moduleName}/{EntityName}Form.vue`

```vue
<route lang="json5" type="page">
{
  layout: 'default',
  style: {
    navigationStyle: 'custom',
    navigationBarTitleText: '{功能描述}',
  },
}
</route>
<template>
  <PageLayout :navTitle="navTitle" :backRouteName="backRouteName">
    <scroll-view class="scrollArea" scroll-y>
      <view class="form-container">
        <wd-form ref="form" :model="myFormData">
          <wd-cell-group border>
            <!-- 在此处渲染各字段组件，每个字段包裹在 <view> 中 -->
            {FORM_FIELDS_PLACEHOLDER}
          </wd-cell-group>
        </wd-form>
      </view>
    </scroll-view>
    <view class="footer">
      <wd-button :disabled="loading" block :loading="loading" @click="handleSubmit">提交</wd-button>
    </view>
  </PageLayout>
</template>

<script lang="ts" setup>
import { onLoad } from '@dcloudio/uni-app'
import { http } from '@/utils/http'
import { useToast } from 'wot-design-uni'
import { useRouter } from '@/plugin/uni-mini-router'
import { ref, onMounted, computed, reactive } from 'vue'
{COMPONENT_IMPORTS_PLACEHOLDER}
import { duplicateCheck } from '@/service/api'

defineOptions({
  name: '{EntityName}Form',
  options: {
    styleIsolation: 'shared',
  },
})

const toast = useToast()
const router = useRouter()
const form = ref(null)
// 定义响应式数据
const myFormData = reactive({})
const loading = ref(false)
const navTitle = ref('新增')
const dataId = ref('')
const backRouteName = ref('{EntityName}List')

// 定义 initForm 方法
const initForm = (item) => {
  if (item?.dataId) {
    dataId.value = item.dataId
    navTitle.value = item.dataId ? '编辑' : '新增'
    initData()
  }
}

// 初始化数据
const initData = () => {
  http.get('/{apiPathPrefix}/queryById', { id: dataId.value }).then((res) => {
    if (res.success) {
      let obj = res.result
      Object.assign(myFormData, { ...obj })
    } else {
      toast.error(res?.message || '表单加载失败！')
    }
  })
}

const handleSuccess = () => {
  uni.$emit('refreshList')
  router.back()
}

/**
 * 校验唯一
 */
async function fieldCheck(values: any) {
  const onlyField = [{ONLY_FIELDS_PLACEHOLDER}]
  for (const field of onlyField) {
    if (values[field]) {
      const res: any = await duplicateCheck({
        tableName: '{tableName}',
        fieldName: field,
        fieldVal: values[field],
        dataId: values.id,
      })
      if (!res.success) {
        toast.warning(res.message)
        return true
      }
    }
  }
  return false
}

// 提交表单
const handleSubmit = async () => {
  if (await fieldCheck(myFormData)) {
    return
  }
  let url = dataId.value
    ? '/{apiPathPrefix}/edit'
    : '/{apiPathPrefix}/add'
  form.value
    .validate()
    .then(({ valid, errors }) => {
      if (valid) {
        loading.value = true
        http.post(url, myFormData).then((res) => {
          loading.value = false
          if (res.success) {
            toast.success('保存成功')
            handleSuccess()
          } else {
            toast.error(res?.message || '表单保存失败！')
          }
        })
      }
    })
    .catch((error) => {
      console.log(error, 'error')
      loading.value = false
    })
}

// 标题截断（超过4个字截断）
const get4Label = computed(() => {
  return (label) => {
    return label && label.length > 4 ? label.substring(0, 4) : label
  }
})

// 获取关联表配置
const getFormSchema = computed(() => {
  return (dictTable, dictCode, dictText) => {
    return { dictCode, dictTable, dictText }
  }
})

// 设置 popup 返回值
const setFieldsValue = (data) => {
  Object.assign(myFormData, { ...data })
}

// onLoad 生命周期钩子
onLoad((option) => {
  initForm(option)
})
</script>

<style lang="scss" scoped>
.footer {
  width: 100%;
  padding: 10px 20px;
  padding-bottom: calc(constant(safe-area-inset-bottom) + 10px);
  padding-bottom: calc(env(safe-area-inset-bottom) + 10px);
}
:deep(.wd-cell__label) {
  font-size: 14px;
  color: #444;
}
:deep(.wd-cell__value) {
  text-align: left;
}
</style>
```

---

## 数据定义模板

文件路径：`src/pages-home/{moduleName}/{EntityName}Data.ts`

```typescript
import { render } from '@/common/renderUtils'

// 列表数据
export const columns = [
  {COLUMNS_PLACEHOLDER}
]
```

### columns 元素格式

**普通文本字段：**
```typescript
{
  title: '字段注释',
  align: 'center',
  dataIndex: 'fieldName',
},
```

**字典类型字段（list/radio/checkbox/sel_search/list_multi/sel_tree/sel_depart/sel_user/popup_dict）：**
```typescript
{
  title: '字段注释',
  align: 'center',
  dataIndex: 'fieldName_dictText',
},
```

**图片字段：**
```typescript
{
  title: '字段注释',
  align: 'center',
  dataIndex: 'fieldName',
  customRender: render.renderImage,
},
```

**开关字段：**
```typescript
{
  title: '字段注释',
  align: 'center',
  dataIndex: 'fieldName',
  customRender: ({ text }) => {
    return render.renderSwitch(text, [
      { text: '是', value: 'Y' },
      { text: '否', value: 'N' },
    ])
  },
},
```

**Blob 字段：**
```typescript
{
  title: '字段注释',
  align: 'center',
  dataIndex: 'fieldNameString',
},
```

**可排序字段：**
```typescript
{
  title: '字段注释',
  align: 'center',
  sorter: true,
  dataIndex: 'fieldName',
},
```

---

## 变量说明

| 变量 | 说明 | 示例 |
|------|------|------|
| `{EntityName}` | 实体名（PascalCase） | `CesOrderMain` |
| `{entityName}` | 实体名首字母小写（camelCase） | `cesOrderMain` |
| `{功能描述}` | 页面标题/功能描述 | `订单管理` |
| `{moduleName}` | 模块目录名（小写） | `order` |
| `{apiPathPrefix}` | API 路径前缀 | `test/cesOrderMain` |
| `{tableName}` | 数据库表名 | `ces_order_main` |
| `{FORM_FIELDS_PLACEHOLDER}` | 表单字段渲染代码 | 见下方规则 |
| `{COMPONENT_IMPORTS_PLACEHOLDER}` | 组件导入语句 | 见下方规则 |
| `{COLUMNS_PLACEHOLDER}` | 列定义代码 | 见上方格式 |
| `{ONLY_FIELDS_PLACEHOLDER}` | 需唯一性校验的字段数组 | `'name', 'code'` |

---

## 表单字段渲染规则

以下是每种 classType 对应的表单字段模板代码。每个字段需包裹在 `<view>` 中。

### 普通文本输入（默认）

```vue
<view>
  <wd-input
    label-width="100px"
    v-model="myFormData['fieldName']"
    :label="get4Label('字段注释')"
    name="'fieldName'"
    prop="'fieldName'"
    placeholder="请输入字段注释"
    :rules="[
      { required: true, message: '请输入字段注释!' },
    ]"
    clearable
  />
</view>
```

### 数字输入（int/long/double/BigDecimal）

```vue
<view>
  <wd-input
    label-width="100px"
    v-model="myFormData['fieldName']"
    :label="get4Label('字段注释')"
    name="'fieldName'"
    prop="'fieldName'"
    placeholder="请输入字段注释"
    inputMode="numeric"
    :rules="[
      { required: true, message: '请输入字段注释!' },
    ]"
    clearable
  />
</view>
```

### 图片上传（image）

```vue
<view>
  <wd-cell
    :title="get4Label('字段注释')"
    title-width="100px"
  >
    <online-image
      v-model:value="myFormData['fieldName']"
      name="'fieldName'"
      :maxNum="1"
    />
  </wd-cell>
</view>
```

### 文件上传（file）

```vue
<view>
  <wd-cell
    :title="get4Label('字段注释')"
    title-width="100px"
  >
    <online-file-custom
      v-model:value="myFormData['fieldName']"
      name="'fieldName'"
    />
  </wd-cell>
</view>
```

### 日期时间（datetime/time）

```vue
<view>
  <DateTime
    :label="get4Label('字段注释')"
    labelWidth="100px"
    type="datetime"
    format="YYYY-MM-DD HH:mm:ss"
    name="'fieldName'"
    v-model="myFormData['fieldName']"
  />
</view>
```

### 日期（date）

```vue
<view>
  <online-date
    :label="get4Label('字段注释')"
    labelWidth="100px"
    type="date"
    name="'fieldName'"
    v-model:value="myFormData['fieldName']"
  />
</view>
```

### 开关（switch）

```vue
<view>
  <wd-cell
    :label="get4Label('字段注释')"
    name="'fieldName'"
    title-width="100px"
    center
  >
    <wd-switch
      :label="get4Label('字段注释')"
      name="'fieldName'"
      size="18px"
      v-model="myFormData['fieldName']"
      active-value="Y"
      inactive-value="N"
    />
  </wd-cell>
</view>
```

### 下拉选择（list/sel_search）

```vue
<view>
  <online-select
    :label="get4Label('字段注释')"
    labelWidth="100px"
    type="list"
    name="'fieldName'"
    dict="dictCode"
    v-model="myFormData['fieldName']"
  />
</view>
```

### 单选（radio）

```vue
<view>
  <online-radio
    :label="get4Label('字段注释')"
    labelWidth="100px"
    type="radio"
    name="'fieldName'"
    dict="dictCode"
    v-model="myFormData['fieldName']"
  />
</view>
```

### 多选（checkbox）

```vue
<view>
  <online-checkbox
    :label="get4Label('字段注释')"
    labelWidth="100px"
    type="checkbox"
    name="'fieldName'"
    dict="dictCode"
    v-model="myFormData['fieldName']"
  />
</view>
```

### 多选下拉（list_multi）

```vue
<view>
  <online-multi
    :label="get4Label('字段注释')"
    labelWidth="100px"
    type="list_multi"
    name="'fieldName'"
    dict="dictCode"
    v-model="myFormData['fieldName']"
  />
</view>
```

### 多行文本（textarea/markdown/umeditor）

```vue
<view>
  <wd-textarea
    :label="get4Label('字段注释')"
    labelWidth="100px"
    type="textarea"
    name="'fieldName'"
    prop="'fieldName'"
    clearable
    :maxlength="300"
    v-model="myFormData['fieldName']"
  />
</view>
```

### 密码（password）

```vue
<view>
  <wd-input
    :label="get4Label('字段注释')"
    labelWidth="100px"
    show-password
    name="'fieldName'"
    prop="'fieldName'"
    clearable
    v-model="myFormData['fieldName']"
  />
</view>
```

### 省市区（pca）

```vue
<view>
  <online-pca
    :label="get4Label('字段注释')"
    labelWidth="100px"
    name="'fieldName'"
    prop="'fieldName'"
    clearable
    v-model:value="myFormData['fieldName']"
  />
</view>
```

### 用户选择（sel_user）

```vue
<view>
  <select-user
    labelWidth="100px"
    :label="get4Label('字段注释')"
    name="'fieldName'"
    v-model="myFormData['fieldName']"
  />
</view>
```

### 部门选择（sel_depart）

```vue
<view>
  <select-dept
    labelWidth="100px"
    :label="get4Label('字段注释')"
    name="'fieldName'"
    v-model="myFormData['fieldName']"
    :multiple="true"
  />
</view>
```

### 分类树选择（cat_tree）

```vue
<view>
  <CategorySelect
    labelWidth="100px"
    :label="get4Label('字段注释')"
    v-model="myFormData['fieldName']"
    pcode="dictCode"
  />
</view>
```

### 自定义树选择（sel_tree）

```vue
<view>
  <TreeSelect
    labelWidth="100px"
    :label="get4Label('字段注释')"
    v-model="myFormData['fieldName']"
    dict="tableName,textField,valueField"
    :pidValue="`pidFieldValue`"
  />
</view>
```

### 弹窗字典选择（popup_dict）

```vue
<view>
  <PopupDict
    labelWidth="100px"
    :label="get4Label('字段注释')"
    v-model="myFormData['fieldName']"
    :multi="false"
    dictCode="tableName,textField,valueField"
  />
</view>
```

### 弹窗选择（popup）

```vue
<view>
  <Popup
    labelWidth="100px"
    :label="get4Label('字段注释')"
    v-model="myFormData['fieldName']"
    :multi="false"
    code="popupCode"
    :setFieldsValue="setFieldsValue"
    :fieldConfig="[
      { source: 'sourceField', target: 'targetField' },
    ]"
  />
</view>
```

### 关联记录（link_table）

```vue
<view>
  <online-popup-link-record
    :label="get4Label('字段注释')"
    labelWidth="100px"
    name="'fieldName'"
    :formSchema="getFormSchema('tableName','fieldName','fieldText')"
    v-model:value="myFormData['fieldName']"
  />
</view>
```

---

## 完整生成示例

### 需求："创建一个员工管理模块，包含姓名、性别（男/女）、手机号、入职日期、头像、是否在职、备注"

**推导结果：**
- 实体名：`Employee`
- 模块目录：`employee`
- API路径前缀：`hr/employee`
- 表名：`hr_employee`

**字段推导：**

| 字段名 | 注释 | classType | 字典 | 必填 |
|--------|------|-----------|------|------|
| name | 姓名 | (默认文本) | 无 | 是 |
| sex | 性别 | radio | sex（系统字典） | 否 |
| phone | 手机号 | (默认文本+手机校验) | 无 | 否 |
| entryDate | 入职日期 | date | 无 | 否 |
| avatar | 头像 | image | 无 | 否 |
| isActive | 是否在职 | switch | Y/N | 否 |
| remark | 备注 | textarea | 无 | 否 |

**生成文件 1: EmployeeData.ts**
```typescript
import { render } from '@/common/renderUtils'

export const columns = [
  {
    title: '姓名',
    align: 'center',
    dataIndex: 'name',
  },
  {
    title: '性别',
    align: 'center',
    dataIndex: 'sex_dictText',
  },
  {
    title: '手机号',
    align: 'center',
    dataIndex: 'phone',
  },
  {
    title: '入职日期',
    align: 'center',
    dataIndex: 'entryDate',
  },
  {
    title: '头像',
    align: 'center',
    dataIndex: 'avatar',
    customRender: render.renderImage,
  },
  {
    title: '是否在职',
    align: 'center',
    dataIndex: 'isActive',
    customRender: ({ text }) => {
      return render.renderSwitch(text, [
        { text: '是', value: 'Y' },
        { text: '否', value: 'N' },
      ])
    },
  },
]
```

**生成文件 2: EmployeeList.vue** — 使用列表页模板，替换变量即可。

**生成文件 3: EmployeeForm.vue** — 表单字段部分：

```vue
<view>
  <wd-input
    label-width="100px"
    v-model="myFormData['name']"
    :label="get4Label('姓名')"
    name="'name'"
    prop="'name'"
    placeholder="请输入姓名"
    :rules="[{ required: true, message: '请输入姓名!' }]"
    clearable
  />
</view>
<view>
  <online-radio
    :label="get4Label('性别')"
    labelWidth="100px"
    type="radio"
    name="'sex'"
    dict="sex"
    v-model="myFormData['sex']"
  />
</view>
<view>
  <wd-input
    label-width="100px"
    v-model="myFormData['phone']"
    :label="get4Label('手机号')"
    name="'phone'"
    prop="'phone'"
    placeholder="请输入手机号"
    :rules="[
      { pattern: /^1[3456789]\d{9}$/, message: '请输入正确的手机号码!' },
    ]"
    clearable
  />
</view>
<view>
  <online-date
    :label="get4Label('入职日期')"
    labelWidth="100px"
    type="date"
    name="'entryDate'"
    v-model:value="myFormData['entryDate']"
  />
</view>
<view>
  <wd-cell :title="get4Label('头像')" title-width="100px">
    <online-image
      v-model:value="myFormData['avatar']"
      name="'avatar'"
      :maxNum="1"
    />
  </wd-cell>
</view>
<view>
  <wd-cell :label="get4Label('是否在职')" name="'isActive'" title-width="100px" center>
    <wd-switch
      :label="get4Label('是否在职')"
      name="'isActive'"
      size="18px"
      v-model="myFormData['isActive']"
      active-value="Y"
      inactive-value="N"
    />
  </wd-cell>
</view>
<view>
  <wd-textarea
    :label="get4Label('备注')"
    labelWidth="100px"
    type="textarea"
    name="'remark'"
    prop="'remark'"
    clearable
    :maxlength="300"
    v-model="myFormData['remark']"
  />
</view>
```

组件导入部分：
```typescript
import OnlineImage from '@/components/online/view/online-image.vue'
import OnlineDate from '@/components/online/view/online-date.vue'
import OnlineRadio from '@/components/online/view/online-radio.vue'
```

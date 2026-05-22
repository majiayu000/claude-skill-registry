---
name: ruoyi-vue-plus-ui-development
description: RuoYi-Vue-Plus框架前端开发规范技能。强制使用Vue3 Composition API与`<script setup>`语法，严格遵循"查询区-工具栏-表格区-分页区-弹窗区"五区标准布局。规定接口统一封装在`@/api/`目录、按钮必须配置`v-hasPermi`权限指令、表单必须配置校验规则。禁止硬编码URL、禁用Vue2 Options API、禁止忽略权限控制、禁止直接使用索引作为row-key。
---

# RuoYi-Vue-Plus 前端开发规范

## 触发条件

### 关键词触发
- **技术栈**：Vue3、Vite、Element Plus、Composition API、`<script setup>`
- **功能模块**：CRUD操作、列表页、表单页、详情页、弹窗组件
- **组件类型**：表格（`el-table`）、表单（`el-form`）、分页（`pagination`）、对话框（`el-dialog`）
- **框架特性**：RuoYi、RuoYi-Vue-Plus、若依框架

### 场景触发
- 用户要求根据数据库表结构生成前端 CRUD 页面
- 用户需要开发符合 RuoYi 规范的列表页面
- 用户需要创建带权限控制的表单组件
- 用户要求实现标准的增删改查功能
- 用户需要修改或优化现有的 RuoYi 前端代码

---

## 核心规范

### 规范1：必须使用 Vue3 Composition API 与 `<script setup>` 语法

#### 详细说明
所有组件必须采用 Vue 3 的 `<script setup>` 语法糖，完全摒弃 Vue 2 的 Options API（`data`、`methods`、`computed`、`mounted` 等）。状态管理使用 `ref` 和 `reactive`，生命周期钩子使用 `onMounted`、`onBeforeMount` 等组合式函数。

**必须引入 `getCurrentInstance`** 来获取全局代理对象（`proxy`），用于调用 RuoYi 框架提供的全局方法：
- `proxy.$modal`：消息提示、确认框、通知框
- `proxy.$auth`：权限判断
- `proxy.$tab`：页签操作
- `proxy.$download`：文件下载

#### 代码示例

```javascript
<script setup name="User">
import { listUser, getUser, delUser, addUser, updateUser } from "@/api/system/user";
import { getCurrentInstance, reactive, ref, toRefs, onMounted } from "vue";

const { proxy } = getCurrentInstance();

// 使用 ref 定义响应式数据
const userList = ref([]);
const loading = ref(true);
const showSearch = ref(true);
const total = ref(0);
const open = ref(false);
const title = ref("");

// 使用 reactive 定义复杂对象
const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    userName: undefined,
    phonenumber: undefined,
    status: undefined
  },
  rules: {
    userName: [
      { required: true, message: "用户名称不能为空", trigger: "blur" },
      { min: 2, max: 20, message: "用户名称长度必须介于 2 和 20 之间", trigger: "blur" }
    ],
    password: [
      { required: true, message: "用户密码不能为空", trigger: "blur" },
      { min: 5, max: 20, message: "用户密码长度必须介于 5 和 20 之间", trigger: "blur" }
    ]
  }
});

// 解构响应式对象
const { queryParams, form, rules } = toRefs(data);

/** 查询用户列表 */
function getList() {
  loading.value = true;
  listUser(queryParams.value).then(response => {
    userList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
  proxy.resetForm("queryRef");
  handleQuery();
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加用户";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const userId = row.userId || ids.value;
  getUser(userId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改用户";
  });
}

/** 删除按钮操作 */
function handleDelete(row) {
  const userIds = row.userId || ids.value;
  proxy.$modal.confirm('是否确认删除用户编号为"' + userIds + '"的数据项？').then(function() {
    return delUser(userIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}

/** 表单重置 */
function reset() {
  form.value = {
    userId: undefined,
    userName: undefined,
    password: undefined,
    status: "0"
  };
  proxy.resetForm("userRef");
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["userRef"].validate(valid => {
    if (valid) {
      if (form.value.userId != undefined) {
        updateUser(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addUser(form.value).then(response => {
          proxy.$modal.msgSuccess("新增成功");
          open.value = false;
          getList();
        });
      }
    }
  });
}

// 组件挂载时查询列表
onMounted(() => {
  getList();
});
</script>
```

**关键要点**：
1. 使用 `<script setup name="组件名">` 指定组件名称
2. 通过 `getCurrentInstance()` 获取实例代理
3. 使用 `ref` 定义简单数据，使用 `reactive` 定义对象
4. 通过 `toRefs` 解构 `reactive` 对象以保持响应性
5. 使用 `onMounted` 等组合式 API 代替生命周期钩子

---

### 规范2：严格遵循五区标准布局结构

#### 详细说明
RuoYi-Vue-Plus 页面布局必须按照以下顺序划分为五个功能区域：

1. **查询区**（`el-form` + `v-show="showSearch"`）：搜索条件表单，支持显示/隐藏切换
2. **工具栏区**（`el-row` + `el-col`）：操作按钮（新增、删除、导出等），需配置权限指令
3. **表格区**（`el-table` + `v-loading`）：数据展示表格，需配置加载状态
4. **分页区**（`pagination` 组件）：分页器，使用 `v-model:page` 和 `v-model:limit` 双向绑定
5. **弹窗区**（`el-dialog` + `el-form`）：新增/编辑表单弹窗，需配置校验规则

#### 完整代码示例

```vue
<template>
  <div class="app-container">
    <!-- ========== 查询区 ========== -->
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="用户名称" prop="userName">
        <el-input
          v-model="queryParams.userName"
          placeholder="请输入用户名称"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="手机号码" prop="phonenumber">
        <el-input
          v-model="queryParams.phonenumber"
          placeholder="请输入手机号码"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="用户状态" clearable style="width: 240px">
          <el-option label="正常" value="0" />
          <el-option label="停用" value="1" />
        </el-select>
      </el-form-item>
      <el-form-item label="创建时间" style="width: 308px">
        <el-date-picker
          v-model="dateRange"
          value-format="YYYY-MM-DD"
          type="daterange"
          range-separator="-"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
        ></el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- ========== 工具栏区 ========== -->
    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="Plus"
          @click="handleAdd"
          v-hasPermi="['system:user:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['system:user:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['system:user:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['system:user:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <!-- ========== 表格区 ========== -->
    <el-table v-loading="loading" :data="userList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="用户编号" align="center" prop="userId" width="120" />
      <el-table-column label="用户名称" align="center" prop="userName" :show-overflow-tooltip="true" />
      <el-table-column label="用户昵称" align="center" prop="nickName" :show-overflow-tooltip="true" />
      <el-table-column label="手机号码" align="center" prop="phonenumber" width="120" />
      <el-table-column label="状态" align="center" width="100">
        <template #default="scope">
          <el-switch
            v-model="scope.row.status"
            active-value="0"
            inactive-value="1"
            @change="handleStatusChange(scope.row)"
          ></el-switch>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" align="center" prop="createTime" width="160">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createTime) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="180" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-tooltip content="修改" placement="top">
            <el-button
              link
              type="primary"
              icon="Edit"
              @click="handleUpdate(scope.row)"
              v-hasPermi="['system:user:edit']"
            ></el-button>
          </el-tooltip>
          <el-tooltip content="删除" placement="top">
            <el-button
              link
              type="primary"
              icon="Delete"
              @click="handleDelete(scope.row)"
              v-hasPermi="['system:user:remove']"
            ></el-button>
          </el-tooltip>
          <el-tooltip content="重置密码" placement="top">
            <el-button
              link
              type="primary"
              icon="Key"
              @click="handleResetPwd(scope.row)"
              v-hasPermi="['system:user:resetPwd']"
            ></el-button>
          </el-tooltip>
        </template>
      </el-table-column>
    </el-table>

    <!-- ========== 分页区 ========== -->
    <pagination
      v-show="total > 0"
      :total="total"
      v-model:page="queryParams.pageNum"
      v-model:limit="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- ========== 弹窗区：添加或修改用户配置对话框 ========== -->
    <el-dialog :title="title" v-model="open" width="600px" append-to-body>
      <el-form ref="userRef" :model="form" :rules="rules" label-width="80px">
        <el-row>
          <el-col :span="12">
            <el-form-item label="用户昵称" prop="nickName">
              <el-input v-model="form.nickName" placeholder="请输入用户昵称" maxlength="30" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="手机号码" prop="phonenumber">
              <el-input v-model="form.phonenumber" placeholder="请输入手机号码" maxlength="11" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="用户名称" prop="userName">
              <el-input v-model="form.userName" placeholder="请输入用户名称" maxlength="30" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="用户密码" prop="password">
              <el-input v-model="form.password" placeholder="请输入用户密码" type="password" maxlength="20" show-password />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="用户性别">
              <el-select v-model="form.sex" placeholder="请选择性别">
                <el-option label="男" value="0" />
                <el-option label="女" value="1" />
                <el-option label="未知" value="2" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态">
              <el-radio-group v-model="form.status">
                <el-radio label="0">正常</el-radio>
                <el-radio label="1">停用</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item label="备注">
              <el-input v-model="form.remark" type="textarea" placeholder="请输入内容" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>
```

**关键要点**：
1. 查询区必须使用 `v-show="showSearch"` 支持显示隐藏
2. 工具栏按钮必须配置 `v-hasPermi` 权限指令
3. 表格必须配置 `v-loading` 加载状态
4. 分页必须使用 `v-model:page` 和 `v-model:limit` 双向绑定
5. 弹窗表单必须配置 `rules` 校验规则

---

### 规范3：接口统一封装在 API 目录

#### 详细说明
所有后端接口调用必须封装在 `src/api/` 目录下对应的模块文件中，禁止在 `.vue` 文件中直接硬编码 URL。接口文件使用 `request` 工具函数统一处理请求。

#### 代码示例：`src/api/system/user.js`

```javascript
import request from '@/utils/request'

// 查询用户列表
export function listUser(query) {
  return request({
    url: '/system/user/list',
    method: 'get',
    params: query
  })
}

// 查询用户详细
export function getUser(userId) {
  return request({
    url: '/system/user/' + userId,
    method: 'get'
  })
}

// 新增用户
export function addUser(data) {
  return request({
    url: '/system/user',
    method: 'post',
    data: data
  })
}

// 修改用户
export function updateUser(data) {
  return request({
    url: '/system/user',
    method: 'put',
    data: data
  })
}

// 删除用户
export function delUser(userId) {
  return request({
    url: '/system/user/' + userId,
    method: 'delete'
  })
}

// 导出用户
export function exportUser(query) {
  return request({
    url: '/system/user/export',
    method: 'post',
    params: query
  })
}

// 用户状态修改
export function changeUserStatus(userId, status) {
  const data = {
    userId,
    status
  }
  return request({
    url: '/system/user/changeStatus',
    method: 'put',
    data: data
  })
}

// 用户密码重置
export function resetUserPwd(userId, password) {
  const data = {
    userId,
    password
  }
  return request({
    url: '/system/user/resetPwd',
    method: 'put',
    data: data
  })
}
```

**关键要点**：
1. 统一使用 `@/utils/request` 工具
2. 接口函数命名规范：`list*`（列表）、`get*`（详情）、`add*`（新增）、`update*`（修改）、`del*`（删除）、`export*`（导出）
3. GET 请求使用 `params` 传参，POST/PUT 请求使用 `data` 传参
4. 接口路径使用 RESTful 风格

---

### 规范4：权限控制必须配置 `v-hasPermi` 指令

#### 详细说明
所有涉及操作权限的按钮（新增、修改、删除、导出等）必须添加 `v-hasPermi` 指令，传入对应的权限标识数组。权限标识格式为 `模块:功能:操作`。

#### 代码示例

```vue
<!-- 工具栏按钮权限控制 -->
<el-button
  type="primary"
  plain
  icon="Plus"
  @click="handleAdd"
  v-hasPermi="['system:user:add']"
>新增</el-button>

<el-button
  type="success"
  plain
  icon="Edit"
  :disabled="single"
  @click="handleUpdate"
  v-hasPermi="['system:user:edit']"
>修改</el-button>

<el-button
  type="danger"
  plain
  icon="Delete"
  :disabled="multiple"
  @click="handleDelete"
  v-hasPermi="['system:user:remove']"
>删除</el-button>

<!-- 表格操作列权限控制 -->
<el-table-column label="操作" align="center" width="180" class-name="small-padding fixed-width">
  <template #default="scope">
    <el-button
      link
      type="primary"
      icon="Edit"
      @click="handleUpdate(scope.row)"
      v-hasPermi="['system:user:edit']"
    >修改</el-button>
    <el-button
      link
      type="primary"
      icon="Delete"
      @click="handleDelete(scope.row)"
      v-hasPermi="['system:user:remove']"
    >删除</el-button>
  </template>
</el-table-column>
```

**权限标识命名规范**：
- 新增：`system:user:add`
- 修改：`system:user:edit`
- 删除：`system:user:remove`
- 查询：`system:user:query`
- 导出：`system:user:export`

---

### 规范5：表单必须配置校验规则

#### 详细说明
所有表单（查询表单除外）必须配置 `rules` 校验规则，使用 Element Plus 的表单验证功能。校验规则需包含必填项、长度限制、格式验证等。

#### 代码示例

```javascript
const data = reactive({
  form: {},
  rules: {
    userName: [
      { required: true, message: "用户名称不能为空", trigger: "blur" },
      { min: 2, max: 20, message: "用户名称长度必须介于 2 和 20 之间", trigger: "blur" }
    ],
    nickName: [
      { required: true, message: "用户昵称不能为空", trigger: "blur" }
    ],
    password: [
      { required: true, message: "用户密码不能为空", trigger: "blur" },
      { min: 5, max: 20, message: "用户密码长度必须介于 5 和 20 之间", trigger: "blur" },
      { pattern: /^[^<>"'|\\]+$/, message: "不能包含非法字符：< > \" ' \\ |", trigger: "blur" }
    ],
    email: [
      { type: "email", message: "请输入正确的邮箱地址", trigger: ["blur", "change"] }
    ],
    phonenumber: [
      { pattern: /^1[3|4|5|6|7|8|9][0-9]\d{8}$/, message: "请输入正确的手机号码", trigger: "blur" }
    ]
  }
});
```

**常用校验规则**：
- `required: true`：必填项
- `min/max`：字符长度限制
- `type: "email"`：邮箱格式
- `pattern: /正则/`：自定义正则验证
- `trigger: "blur"`：失焦时触发（推荐）
- `trigger: "change"`：值改变时触发

---

### 规范6：表格必须使用数据主键作为 row-key

#### 详细说明
`el-table` 组件必须配置 `row-key` 属性，且值必须为数据的唯一主键字段（如 `userId`、`id` 等），禁止使用索引 `index` 作为 `row-key`。

#### 代码示例

```vue
<!-- ✅ 正确：使用主键 userId -->
<el-table 
  v-loading="loading" 
  :data="userList" 
  row-key="userId"
  @selection-change="handleSelectionChange"
>
  <el-table-column type="selection" width="55" align="center" />
  <el-table-column label="用户编号" align="center" prop="userId" />
  <el-table-column label="用户名称" align="center" prop="userName" />
</el-table>

<!-- ❌ 错误：使用索引 -->
<el-table 
  v-loading="loading" 
  :data="userList" 
  row-key="index"
>
</el-table>
```

**为什么必须使用主键**：
- 确保数据更新时表格渲染正确
- 支持表格选择功能的准确性
- 避免因索引变化导致的渲染错误

---

### 规范7：导出功能必须使用 `$download` 方法

#### 详细说明
导出 Excel 功能必须使用 RuoYi 框架提供的 `proxy.$download` 方法，该方法会自动处理文件下载和错误提示。

#### 代码示例

```javascript
/** 导出按钮操作 */
function handleExport() {
  proxy.$modal.confirm('是否确认导出所有用户数据项？').then(() => {
    return proxy.$download('/system/user/export', {
      ...queryParams.value
    }, `user_${new Date().getTime()}.xlsx`)
  }).catch(() => {});
}
```

**关键要点**：
1. 使用 `proxy.$download` 方法
2. 第一个参数：导出接口路径
3. 第二个参数：查询参数对象
4. 第三个参数：导出文件名（建议带时间戳）

---

### 规范8：日期范围查询的标准处理

#### 详细说明
日期范围查询需要定义 `dateRange` 变量，并在查询时通过 `addDateRange` 方法将日期范围参数添加到查询参数中。

#### 代码示例

```javascript
import { addDateRange } from "@/utils/ruoyi";

// 定义日期范围变量
const dateRange = ref([]);

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  // 将日期范围添加到查询参数
  const params = addDateRange(queryParams.value, dateRange.value);
  listUser(params).then(response => {
    userList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
}
```

```vue
<!-- 日期范围选择器 -->
<el-form-item label="创建时间" style="width: 308px">
  <el-date-picker
    v-model="dateRange"
    value-format="YYYY-MM-DD"
    type="daterange"
    range-separator="-"
    start-placeholder="开始日期"
    end-placeholder="结束日期"
  ></el-date-picker>
</el-form-item>
```

---

## 禁止事项

### ❌ 绝对禁止

1. **禁止在 `.vue` 文件中直接硬编码 URL**
   ```javascript
   // ❌ 错误示例
   axios.get('http://localhost:8080/system/user/list')
   
   // ✅ 正确示例
   import { listUser } from "@/api/system/user";
   listUser(queryParams.value)
   ```

2. **禁止使用 Vue 2 Options API 语法**
   ```javascript
   // ❌ 错误示例
   export default {
     data() {
       return {
         userList: []
       }
     },
     methods: {
       getList() {}
     },
     mounted() {}
   }
   
   // ✅ 正确示例
   <script setup>
   import { ref, onMounted } from "vue";
   const userList = ref([]);
   function getList() {}
   onMounted(() => {});
   </script>
   ```

3. **禁止使用索引作为表格 row-key**
   ```vue
   <!-- ❌ 错误示例 -->
   <el-table :data="userList" row-key="index">
   
   <!-- ✅ 正确示例 -->
   <el-table :data="userList" row-key="userId">
   ```

4. **禁止忽略权限控制**
   ```vue
   <!-- ❌ 错误示例 -->
   <el-button type="primary" @click="handleAdd">新增</el-button>
   
   <!-- ✅ 正确示例 -->
   <el-button type="primary" @click="handleAdd" v-hasPermi="['system:user:add']">新增</el-button>
   ```

5. **禁止表单缺少校验规则**
   ```javascript
   // ❌ 错误示例
   const data = reactive({
     form: {},
     rules: {} // 空的校验规则
   });
   
   // ✅ 正确示例
   const data = reactive({
     form: {},
     rules: {
       userName: [{ required: true, message: "用户名称不能为空", trigger: "blur" }]
     }
   });
   ```

### ⚠️ 强烈不推荐

1. **不推荐混用 `ref` 和直接修改 `reactive`**
   ```javascript
   // ⚠️ 不推荐
   const data = reactive({ count: 0 });
   data.count = 1; // 直接修改
   
   // ✅ 推荐
   const { count } = toRefs(data);
   count.value = 1;
   ```

2. **不推荐在模板中使用复杂表达式**
   ```vue
   <!-- ⚠️ 不推荐 -->
   <span>{{ user.name ? user.name.substring(0, 10) : '无名称' }}</span>
   
   <!-- ✅ 推荐：使用计算属性 -->
   <span>{{ displayName }}</span>
   ```

3. **不推荐省略接口错误处理**
   ```javascript
   // ⚠️ 不推荐
   listUser(queryParams.value).then(response => {
     userList.value = response.rows;
   });
   
   // ✅ 推荐
   listUser(queryParams.value).then(response => {
     userList.value = response.rows;
     loading.value = false;
   }).catch(() => {
     loading.value = false;
   });
   ```

---

## 参考代码

### 官方示例文件路径
- **用户管理列表页**：`ruoyi-ui/src/views/system/user/index.vue`
- **用户接口封装**：`ruoyi-ui/src/api/system/user.js`
- **分页组件**：`ruoyi-ui/src/components/Pagination/index.vue`
- **右侧工具栏组件**：`ruoyi-ui/src/components/RightToolbar/index.vue`
- **请求工具**：`ruoyi-ui/src/utils/request.js`
- **若依工具函数**：`ruoyi-ui/src/utils/ruoyi.js`

### 核心组件和工具
- **`getCurrentInstance()`**：获取组件实例代理对象
- **`proxy.$modal`**：消息提示、确认框、通知框
- **`proxy.$auth`**：权限判断方法
- **`proxy.$download`**：文件下载方法
- **`addDateRange()`**：日期范围参数处理
- **`parseTime()`**：时间格式化函数

---

## 开发检查清单

### 基础检查（必须全部通过）
- [ ] ✅ 是否使用 `<script setup>` 语法
- [ ] ✅ 是否引入 `getCurrentInstance` 并获取 `proxy`
- [ ] ✅ 是否从 `@/api/...` 引入接口方法
- [ ] ✅ 是否包含 `queryParams` 和分页逻辑
- [ ] ✅ 是否配置 `v-loading` 加载状态
- [ ] ✅ 按钮是否配置 `v-hasPermi` 权限指令
- [ ] ✅ 表单是否配置 `rules` 校验规则
- [ ] ✅ 表格是否使用主键作为 `row-key`

### 布局检查（必须包含五区）
- [ ] ✅ 查询区：`el-form` + `v-show="showSearch"`
- [ ] ✅ 工具栏区：`el-row` + 权限按钮
- [ ] ✅ 表格区：`el-table` + `v-loading`
- [ ] ✅ 分页区：`pagination` 组件
- [ ] ✅ 弹窗区：`el-dialog` + 表单校验

### 功能检查（CRUD 完整性）
- [ ] ✅ 查询功能：`handleQuery` + `resetQuery`
- [ ] ✅ 新增功能：`handleAdd` + `submitForm`
- [ ] ✅ 修改功能：`handleUpdate` + `submitForm`
- [ ] ✅ 删除功能：`handleDelete` + 确认提示
- [ ] ✅ 分页功能：`pagination` 组件正确绑定
- [ ] ✅ 导出功能：`handleExport` + `$download`（可选）

### 代码规范检查
- [ ] ✅ 接口统一封装在 `src/api/` 目录
- [ ] ✅ 没有直接硬编码 URL
- [ ] ✅ 没有使用 Vue 2 Options API
- [ ] ✅ 变量命名符合驼峰命名规范
- [ ] ✅ 代码缩进统一（2 空格）
- [ ] ✅ 组件使用 `name` 属性命名

### 用户体验检查
- [ ] ✅ 加载状态正确显示
- [ ] ✅ 操作成功后有消息提示
- [ ] ✅ 删除操作有确认提示
- [ ] ✅ 表单提交前有校验
- [ ] ✅ 表格列宽合理，内容不溢出
- [ ] ✅ 按钮禁用状态逻辑正确

---

## 常见问题与解决方案

### Q1: `proxy.$modal` 提示 undefined
**原因**：未正确引入 `getCurrentInstance` 或在 setup 外部使用  
**解决**：
```javascript
import { getCurrentInstance } from "vue";
const { proxy } = getCurrentInstance(); // 必须在 setup 顶层调用
```

### Q2: 表单提交时校验不生效
**原因**：未正确使用 `proxy.$refs` 获取表单引用  
**解决**：
```javascript
function submitForm() {
  proxy.$refs["userRef"].validate(valid => {
    if (valid) {
      // 提交逻辑
    }
  });
}
```

### Q3: 分页切换后数据不更新
**原因**：分页组件的 `@pagination` 事件未正确绑定  
**解决**：
```vue
<pagination
  v-show="total > 0"
  :total="total"
  v-model:page="queryParams.pageNum"
  v-model:limit="queryParams.pageSize"
  @pagination="getList"
/>
```

### Q4: 权限指令不生效
**原因**：未在 `main.js` 中注册 `v-hasPermi` 指令  
**解决**：确认 `main.js` 中已引入：
```javascript
import { hasPermi } from "@/utils/permission";
app.directive('hasPermi', hasPermi);
```

### Q5: 日期范围查询参数未传递
**原因**：未使用 `addDateRange` 方法处理日期参数  
**解决**：
```javascript
import { addDateRange } from "@/utils/ruoyi";
const params = addDateRange(queryParams.value, dateRange.value);
listUser(params).then(response => {});
```

---

## 总结

遵循本规范可以确保：
1. **代码一致性**：所有页面结构统一，易于维护
2. **权限安全**：所有操作都受权限控制
3. **用户体验**：加载状态、消息提示、表单校验完整
4. **可维护性**：接口统一封装，职责分离清晰
5. **可扩展性**：使用 Composition API，逻辑复用方便

**记住核心原则**：
- ✅ 必须使用 `<script setup>` + Composition API
- ✅ 必须遵循五区标准布局
- ✅ 必须配置权限指令和表单校验
- ❌ 禁止硬编码 URL 和使用 Options API
- ❌ 禁止忽略权限控制和校验规则

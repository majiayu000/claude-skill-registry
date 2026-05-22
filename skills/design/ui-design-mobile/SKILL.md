---
name: ui-design-mobile
description: |
  基于若依-vue-plus框架的移动端（Uni-app + UView 2.0）UI设计与开发规范。提供完整的移动端界面设计标准，包括：
  - UView 2.0 组件库的正确使用方式
  - 响应式布局系统与多端适配方案
  - 主题色彩系统与样式变量管理
  - 交互规范与用户体验优化
  - 安全区域适配（刘海屏、底部导航栏）
  
  触发场景：
  - 编写移动端页面结构或组件
  - 定制UI主题和样式
  - 处理多端适配和布局问题
  - 实现交互效果和动画
  - 优化移动端用户体验
  
  触发关键词：移动端设计、UView布局、UI规范、主题定制、Uni-app页面、响应式布局、安全区域适配
---

# 基于 UView 2.0 的移动端UI设计规范

## 📋 目录
1. [核心规范](#核心规范)
2. [禁止事项](#禁止事项)
3. [最佳实践](#最佳实践)
4. [参考代码](#参考代码)
5. [检查清单](#检查清单)

---

## 核心规范

### 规范1：布局系统与安全区域适配

**原则说明**：
- 页面布局**必须**使用UView提供的内置布局组件（`u-row`、`u-col`）实现栅格系统，禁止手动计算`margin`或`padding`
- 针对刘海屏和底部安全条，**必须**使用`u-safe-area`或`:safeAreaInsetTop`/`:safeAreaInsetBottom`属性确保内容不被遮挡
- 布局单位**统一使用`rpx`**（除特殊情况如1px边框）
- 页面需考虑横屏、竖屏及折叠屏等多种屏幕形态

**适用场景**：
- 所有移动端页面的主体布局
- 包含顶部导航栏的页面
- 底部固定操作栏的页面
- 需要多列布局的卡片/网格界面

```html
<template>
  <view class="page-container">
    <!-- 顶部导航栏自动处理安全区域 -->
    <u-navbar 
      title="页面标题" 
      :safeAreaInsetTop="true"
      :placeholder="true"
      :fixed="true"
      bgColor="#409EFF"
    />

    <!-- 主体内容区域 -->
    <view class="content-wrapper">
      <!-- 栅格布局示例：12列系统 -->
      <u-row gutter="16" justify="space-between">
        <u-col span="4">
          <view class="card-item bg-primary-light">卡片1</view>
        </u-col>
        <u-col span="4">
          <view class="card-item bg-primary-light">卡片2</view>
        </u-col>
        <u-col span="4">
          <view class="card-item bg-primary-light">卡片3</view>
        </u-col>
      </u-row>

      <!-- 响应式布局：不同屏幕尺寸自适应 -->
      <u-row gutter="20">
        <u-col :span="6" :xs="12" :sm="6" :md="4">
          <view class="grid-item">响应式项目</view>
        </u-col>
      </u-row>
    </view>

    <!-- 底部固定操作栏，适配安全区域 -->
    <view class="bottom-action" :style="{paddingBottom: safeAreaBottom}">
      <u-button 
        type="primary" 
        text="提交" 
        :customStyle="{width: '100%', height: '88rpx'}"
        @click="handleSubmit"
      />
    </view>
    
    <!-- 使用 u-safe-area 组件自动处理底部安全区域 -->
    <u-safe-area bgColor="#ffffff" />
  </view>
</template>

<script setup>
import { ref, computed } from 'vue';
import { getSystemInfoSync } from '@dcloudio/uni-app';

// 获取设备底部安全区域高度
const systemInfo = getSystemInfoSync();
const safeAreaBottom = computed(() => {
  const safeArea = systemInfo.safeArea || {};
  const bottom = systemInfo.screenHeight - safeArea.bottom;
  return bottom > 0 ? `${bottom}px` : '0px';
});

const handleSubmit = () => {
  console.log('提交操作');
};
</script>

<style scoped lang="scss">
.page-container {
  min-height: 100vh;
  background-color: $content-bg-color;
}

.content-wrapper {
  padding: 24rpx;
}

.card-item {
  height: 200rpx;
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28rpx;
  color: $text-main-color;
}

.grid-item {
  height: 160rpx;
  background: #ffffff;
  border-radius: 12rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.08);
}

.bottom-action {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 24rpx;
  background: #ffffff;
  box-shadow: 0 -2rpx 12rpx rgba(0, 0, 0, 0.05);
}
</style>
```

**关键要点**：
- ✅ 使用 `u-navbar` 的 `:safeAreaInsetTop="true"` 处理顶部安全区域
- ✅ 使用 `u-safe-area` 组件自动处理底部安全区域
- ✅ 使用 `u-row` 和 `u-col` 实现栅格布局，支持响应式
- ✅ 所有尺寸使用 `rpx` 单位，确保多端适配
- ✅ 固定定位元素需要手动处理 `paddingBottom`

---

### 规范2：色彩主题与样式变量覆盖

**原则说明**：
- **严禁硬编码颜色值**，必须通过修改`uni.scss`中UView提供的SCSS变量来实现全局主题定制
- UView组件均支持通过`type`、`customStyle`、`color`等属性快速应用主题色
- 字体大小与间距需参考UView默认规范（主要文字28rpx-32rpx，标题32rpx-36rpx）
- 支持动态换肤，通过切换SCSS变量实现暗黑模式或其他主题

**适用场景**：
- 全局主题色定制
- 按钮、标签、徽章等组件颜色管理
- 文字颜色层级定义
- 背景色、边框色统一管理

**代码示例**：

```scss
/* uni.scss: 全局覆盖UView主题变量 */
/* 若依移动端通常使用的蓝色系 */

// ========== 主题色系 ==========
$u-primary: #409EFF;           // 主色调
$u-primary-dark: #337ecc;      // 主色调-深色（按下态）
$u-primary-disabled: #a0cfff;  // 主色调-禁用态
$u-primary-light: #ecf5ff;     // 主色调-浅色背景

$u-success: #67C23A;           // 成功色
$u-warning: #E6A23C;           // 警告色
$u-error: #F56C6C;             // 错误色
$u-info: #909399;              // 信息色

// ========== 文字颜色层级 ==========
$u-main-color: #303133;        // 主要文字（标题、重要信息）
$u-content-color: #606266;     // 常规文字（正文内容）
$u-tips-color: #909399;        // 次要文字（提示信息）
$u-light-color: #c0c4cc;       // 辅助文字（占位符、禁用文字）

// ========== 背景色系 ==========
$u-bg-color: #f5f7fa;          // 页面背景色
$u-border-color: #e4e7ed;      // 边框颜色

// ========== 文字大小规范 ==========
$u-font-size-title: 36rpx;     // 页面标题
$u-font-size-subtitle: 32rpx;  // 副标题
$u-font-size-content: 28rpx;   // 正文内容
$u-font-size-tips: 24rpx;      // 辅助提示

// ========== 间距规范 ==========
$u-padding-xs: 12rpx;
$u-padding-sm: 16rpx;
$u-padding-md: 24rpx;
$u-padding-lg: 32rpx;
$u-padding-xl: 48rpx;

// ========== 圆角规范 ==========
$u-radius-sm: 8rpx;
$u-radius-md: 12rpx;
$u-radius-lg: 16rpx;
$u-radius-xl: 24rpx;
```

```html
<!-- 组件中使用 type 属性自动应用主题色 -->
<template>
  <view class="theme-demo">
    <!-- 按钮主题色应用 -->
    <u-button type="primary" text="主要按钮" />
    <u-button type="success" text="成功按钮" />
    <u-button type="warning" text="警告按钮" />
    <u-button type="error" text="危险按钮" />
    <u-button type="info" text="信息按钮" plain />

    <!-- 使用 customStyle 进行动态样式微调，避免直接修改组件class -->
    <u-icon 
      name="camera" 
      :color="primaryColor" 
      size="40" 
      :customStyle="{marginRight: '10rpx'}"
    />

    <!-- 文字颜色使用SCSS变量 -->
    <view class="text-main">主要文字</view>
    <view class="text-content">常规文字</view>
    <view class="text-tips">提示文字</view>

    <!-- 标签组件应用主题 -->
    <u-tag text="标签" type="primary" />
    <u-tag text="标签" type="success" plain />

    <!-- 徽章组件 -->
    <u-badge :value="99" :max="99" type="error">
      <u-icon name="bell" size="50" />
    </u-badge>
  </view>
</template>

<script setup>
import { ref } from 'vue';

// 如需动态主题色，可从配置中读取
const primaryColor = ref('#409EFF');
</script>

<style scoped lang="scss">
.theme-demo {
  padding: $u-padding-md;
}

// 使用SCSS变量定义文字颜色
.text-main {
  color: $u-main-color;
  font-size: $u-font-size-content;
  line-height: 1.5;
}

.text-content {
  color: $u-content-color;
  font-size: $u-font-size-content;
}

.text-tips {
  color: $u-tips-color;
  font-size: $u-font-size-tips;
}

// 使用变量定义背景色
.card {
  background: #ffffff;
  border: 1px solid $u-border-color;
  border-radius: $u-radius-md;
  padding: $u-padding-md;
}
</style>
```

**关键要点**：
- ✅ 优先使用组件的 `type` 属性应用预设主题色
- ✅ 使用 `customStyle` 进行局部样式微调
- ✅ 所有颜色、字体、间距都使用SCSS变量
- ✅ 避免硬编码颜色值，确保换肤可行性
- ✅ 保持视觉层级：主要文字 > 常规文字 > 提示文字

---

### 规范3：组件使用与交互规范

**原则说明**：
- 优先使用UView 2.0内置组件，而非自己实现类似功能
- 遵循移动端交互习惯：最小点击区域44rpx × 44rpx
- 表单组件需提供明确的反馈（loading、disabled状态）
- 弹窗、Toast、Modal等交互需符合用户预期
- 列表滚动需使用虚拟滚动或分页加载优化性能

**常用组件使用规范**：

```html
<template>
  <view class="component-demo">
    <!-- 1. 表单组件 -->
    <u-form :model="form" ref="formRef" :rules="rules">
      <u-form-item label="用户名" prop="username" required>
        <u-input 
          v-model="form.username" 
          placeholder="请输入用户名"
          :clearable="true"
          :customStyle="{fontSize: '28rpx'}"
        />
      </u-form-item>

      <u-form-item label="性别" prop="gender">
        <u-radio-group v-model="form.gender">
          <u-radio :name="1" label="男" />
          <u-radio :name="2" label="女" />
        </u-radio-group>
      </u-form-item>

      <u-form-item label="爱好" prop="hobbies">
        <u-checkbox-group v-model="form.hobbies">
          <u-checkbox name="reading" label="阅读" />
          <u-checkbox name="sports" label="运动" />
        </u-checkbox-group>
      </u-form-item>
    </u-form>

    <!-- 2. 列表组件（下拉刷新 + 上拉加载） -->
    <u-list @scrolltolower="loadMore" :finished="finished" finishedText="没有更多了">
      <u-list-item v-for="item in list" :key="item.id">
        <u-cell :title="item.title" :label="item.desc">
          <template #icon>
            <u-image :src="item.avatar" width="80rpx" height="80rpx" :radius="8" />
          </template>
        </u-cell>
      </u-list-item>
    </u-list>

    <!-- 3. 弹窗组件 -->
    <u-button text="打开弹窗" @click="showModal = true" />
    <u-modal 
      v-model="showModal" 
      title="提示" 
      content="这是一个提示弹窗"
      :showCancelButton="true"
      @confirm="handleConfirm"
      @cancel="handleCancel"
    />

    <!-- 4. Toast提示 -->
    <u-button text="显示Toast" @click="showToast" />

    <!-- 5. 操作菜单 -->
    <u-action-sheet 
      :show="showActionSheet" 
      :actions="actions" 
      @select="handleSelect"
      @close="showActionSheet = false"
    />

    <!-- 6. 轮播图 -->
    <u-swiper 
      :list="banners" 
      indicator 
      :autoplay="true"
      :interval="3000"
      :radius="12"
      :height="300"
    />

    <!-- 7. 步骤条 -->
    <u-steps :current="currentStep" activeColor="#409EFF">
      <u-steps-item title="步骤1" desc="描述信息" />
      <u-steps-item title="步骤2" desc="描述信息" />
      <u-steps-item title="步骤3" desc="描述信息" />
    </u-steps>
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue';

// 表单数据
const form = reactive({
  username: '',
  gender: 1,
  hobbies: []
});

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: ['blur', 'change'] },
    { min: 3, max: 20, message: '用户名长度3-20位', trigger: 'blur' }
  ]
};

// 列表数据
const list = ref([]);
const finished = ref(false);

const loadMore = async () => {
  // 模拟加载数据
  const newData = await fetchData();
  list.value.push(...newData);
  if (list.value.length >= 50) {
    finished.value = true;
  }
};

// 弹窗
const showModal = ref(false);
const handleConfirm = () => {
  console.log('确认');
  showModal.value = false;
};

const handleCancel = () => {
  console.log('取消');
};

// Toast
const showToast = () => {
  uni.showToast({
    title: '操作成功',
    icon: 'success',
    duration: 2000
  });
};

// 操作菜单
const showActionSheet = ref(false);
const actions = [
  { name: '选项1', color: '#303133' },
  { name: '选项2', color: '#303133' },
  { name: '删除', color: '#F56C6C' }
];

const handleSelect = (index) => {
  console.log('选择了', index);
};

// 轮播图
const banners = ref([
  'https://example.com/banner1.jpg',
  'https://example.com/banner2.jpg'
]);

// 步骤条
const currentStep = ref(1);
</script>
```

**关键要点**：
- ✅ 表单需使用 `u-form` 和 `u-form-item` 统一管理验证
- ✅ 列表使用 `u-list` 处理下拉刷新和上拉加载
- ✅ 弹窗、Toast、ActionSheet 等反馈组件规范使用
- ✅ 组件交互需提供明确的视觉反馈
- ✅ 最小点击区域不小于 44rpx × 44rpx

---

## 禁止事项

### ❌ 布局与标签使用
1. **禁止使用HTML标签**：在布局中使用`<div>`、`<span>`等HTML标签，必须使用`<view>`、`<text>`或UView组件
   ```html
   <!-- ❌ 错误示例 -->
   <div class="container">
     <span>文本内容</span>
   </div>

   <!-- ✅ 正确示例 -->
   <view class="container">
     <text>文本内容</text>
   </view>
   ```

2. **禁止使用px单位**：除1px边框外，禁止使用`px`作为布局单位，必须使用`rpx`确保响应式适配
   ```scss
   /* ❌ 错误示例 */
   .card {
     width: 300px;
     padding: 20px;
     font-size: 16px;
   }

   /* ✅ 正确示例 */
   .card {
     width: 600rpx;
     padding: 40rpx;
     font-size: 28rpx;
     border: 1px solid #e4e7ed; /* 边框可用px */
   }
   ```

3. **禁止忽视安全区域适配**：在有导航栏或底部固定按钮的页面，必须使用`u-safe-area`或相关属性，否则在iPhone X及以上设备上内容会被遮挡
   ```html
   <!-- ❌ 错误示例：底部按钮会被刘海屏遮挡 -->
   <view class="fixed-button">
     <u-button>提交</u-button>
   </view>

   <!-- ✅ 正确示例 -->
   <view class="fixed-button">
     <u-button>提交</u-button>
   </view>
   <u-safe-area />
   ```

### ❌ 样式与主题定制
4. **禁止硬编码颜色值**：直接在组件或样式中写死颜色，必须使用`uni.scss`中的SCSS变量
   ```html
   <!-- ❌ 错误示例 -->
   <u-button :customStyle="{backgroundColor: '#409EFF'}">按钮</u-button>
   <view style="color: #303133">文本</view>

   <!-- ✅ 正确示例 -->
   <u-button type="primary">按钮</u-button>
   <view class="text-main">文本</view>
   ```

5. **禁止直接修改node_modules**：不得直接修改`node_modules/uview-plus`下的组件源码，应通过`uni.scss`覆盖变量或使用`customStyle`
   ```scss
   /* ❌ 错误做法：直接修改 node_modules/uview-plus/components/u-button/u-button.vue */

   /* ✅ 正确做法：在 uni.scss 中覆盖 */
   $u-button-height: 88rpx;
   $u-button-text-size: 32rpx;
   ```

6. **禁止使用过时的UView 1.x语法**：UView 2.0已弃用大部分插槽语法，需使用props传值
   ```html
   <!-- ❌ 错误示例（UView 1.x） -->
   <u-button>
     <view slot="icon">
       <u-icon name="plus" />
     </view>
     按钮文字
   </u-button>

   <!-- ✅ 正确示例（UView 2.0） -->
   <u-button text="按钮文字" icon="plus" />
   ```

### ❌ 性能与兼容性
7. **禁止在长列表中不做优化**：超过50条数据的列表必须使用虚拟滚动或分页加载
   ```html
   <!-- ❌ 错误示例：一次性渲染1000条数据 -->
   <view v-for="item in allData" :key="item.id">
     {{ item.title }}
   </view>

   <!-- ✅ 正确示例：使用分页加载 -->
   <u-list @scrolltolower="loadMore" :finished="finished">
     <u-list-item v-for="item in pagedData" :key="item.id">
       {{ item.title }}
     </u-list-item>
   </u-list>
   ```

8. **禁止使用不兼容的CSS属性**：避免使用小程序不支持的CSS属性（如`backdrop-filter`、`mask-image`等）
   ```scss
   /* ❌ 错误示例 */
   .blur-bg {
     backdrop-filter: blur(10px); /* 小程序不支持 */
   }

   /* ✅ 正确示例：使用兼容方案 */
   .blur-bg {
     background: rgba(255, 255, 255, 0.8);
   }
   ```

9. **禁止过度使用阴影和渐变**：过多的`box-shadow`和`linear-gradient`会影响渲染性能
   ```scss
   /* ❌ 错误示例：过度使用阴影 */
   .card {
     box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.1),
                 0 4rpx 24rpx rgba(0,0,0,0.08),
                 0 8rpx 48rpx rgba(0,0,0,0.06);
   }

   /* ✅ 正确示例：简化阴影 */
   .card {
     box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.08);
   }
   ```

### ❌ 代码规范
10. **禁止混用Vue 2和Vue 3语法**：项目统一使用Vue 3 Composition API
    ```javascript
    // ❌ 错误示例（Vue 2 Options API）
    export default {
      data() {
        return { count: 0 }
      },
      methods: {
        increment() { this.count++ }
      }
    }

    // ✅ 正确示例（Vue 3 Composition API）
    import { ref } from 'vue';
    const count = ref(0);
    const increment = () => { count.value++ };
    ```

---

## 最佳实践

### 1. 响应式设计原则
- **使用 rpx 单位**：1rpx = 屏幕宽度 / 750，自动适配不同屏幕
- **设计稿基准**：以 750px 宽度为设计稿标准，1px = 2rpx
- **最小点击区域**：按钮、链接等可点击元素不小于 88rpx × 88rpx（44px × 44px）
- **字体大小规范**：
  - 页面标题：36rpx - 40rpx
  - 副标题：32rpx - 34rpx
  - 正文内容：28rpx - 30rpx
  - 辅助提示：24rpx - 26rpx
  - 最小字号：不小于 20rpx

### 2. 颜色使用规范
- **主题色使用场景**：
  - Primary（主色）：主要操作按钮、重要信息、链接
  - Success（成功色）：成功提示、完成状态
  - Warning（警告色）：警告提示、需注意的信息
  - Error（错误色）：错误提示、删除操作、危险按钮
  - Info（信息色）：一般信息、辅助按钮

- **文字颜色层级**：
  - 主要文字（#303133）：标题、重要信息
  - 常规文字（#606266）：正文内容
  - 次要文字（#909399）：提示信息、说明文字
  - 辅助文字（#c0c4cc）：占位符、禁用文字

### 3. 组件选择指南
| 需求场景 | 推荐组件 | 说明 |
|---------|---------|------|
| 页面导航 | `u-navbar` | 自动处理安全区域，支持返回按钮 |
| 底部导航 | `u-tabbar` | 固定底部，支持徽章提示 |
| 表单输入 | `u-form` + `u-input` | 统一验证管理 |
| 列表展示 | `u-list` + `u-cell` | 支持下拉刷新、上拉加载 |
| 图片展示 | `u-image` | 自动懒加载、失败占位 |
| 弹窗提示 | `u-modal` / `u-toast` | 规范化交互反馈 |
| 日期选择 | `u-datetime-picker` | 多种时间格式支持 |
| 文件上传 | `u-upload` | 支持多文件、预览 |
| 步骤流程 | `u-steps` | 多步骤引导 |
| 轮播图 | `u-swiper` | 自动播放、指示器 |

### 4. 性能优化建议
- **图片优化**：
  - 使用WebP格式（减少60%体积）
  - 图片压缩后上传（推荐使用TinyPNG）
  - 大图使用CDN加速
  - 列表图片使用懒加载

- **列表优化**：
  - 长列表使用虚拟滚动
  - 分页加载（每页15-20条）
  - 避免在列表项中使用复杂计算

- **代码分包**：
  ```json
  // pages.json
  {
    "subPackages": [
      {
        "root": "pages/user",
        "pages": [
          { "path": "profile/index" },
          { "path": "settings/index" }
        ]
      }
    ],
    "preloadRule": {
      "pages/index/index": {
        "network": "all",
        "packages": ["pages/user"]
      }
    }
  }
  ```

### 5. 交互体验优化
- **加载状态**：所有异步操作都需显示加载状态
  ```javascript
  const loading = ref(false);
  
  const fetchData = async () => {
    loading.value = true;
    try {
      await api.getData();
    } finally {
      loading.value = false;
    }
  };
  ```

- **防抖节流**：频繁触发的操作需添加防抖或节流
  ```javascript
  import { debounce } from 'lodash-es';
  
  const handleSearch = debounce((keyword) => {
    // 搜索逻辑
  }, 300);
  ```

- **错误处理**：统一错误提示和降级方案
  ```javascript
  const handleSubmit = async () => {
    try {
      await api.submit(form);
      uni.showToast({ title: '提交成功', icon: 'success' });
    } catch (error) {
      uni.showToast({ 
        title: error.message || '提交失败，请重试', 
        icon: 'none' 
      });
    }
  };
  ```

### 6. 无障碍访问
- 为图标添加语义化说明
- 使用合适的颜色对比度（至少4.5:1）
- 表单元素提供明确的label
- 重要操作提供确认弹窗

---

## 参考代码

### 文件结构说明
```
project-sport/
├── uni.scss                          # 全局SCSS变量定义（主题色、字体、间距）
├── App.vue                           # 应用全局配置
├── pages/
│   ├── index/
│   │   └── index.vue                 # 首页示例（典型布局、组件使用）
│   ├── user/
│   │   ├── profile/index.vue         # 用户资料页（表单示例）
│   │   └── settings/index.vue        # 设置页（列表示例）
│   └── common/
│       └── login/index.vue           # 登录页（表单验证示例）
├── components/
│   ├── custom-navbar/                # 自定义导航栏组件
│   ├── card-list/                    # 卡片列表组件
│   └── empty-state/                  # 空状态组件
├── uview-plus/                       # UView 2.0 组件库（不要修改）
│   ├── components/
│   │   ├── u-row/u-row.vue          # 栅格布局组件源码参考
│   │   ├── u-button/u-button.vue    # 按钮组件源码参考
│   │   └── ...
│   └── theme.scss                    # UView默认主题变量
└── static/
    └── images/                       # 静态图片资源
```

### 关键文件示例

#### 1. `uni.scss` - 全局变量定义
```scss
/* 参考路径: uni.scss */
// 主题色系
$u-primary: #409EFF;
$u-success: #67C23A;
$u-warning: #E6A23C;
$u-error: #F56C6C;

// 文字颜色
$u-main-color: #303133;
$u-content-color: #606266;
$u-tips-color: #909399;

// 间距规范
$u-padding-md: 24rpx;
$u-padding-lg: 32rpx;
```

#### 2. `pages/index/index.vue` - 典型页面布局示例
```vue
<!-- 参考路径: pages/index/index.vue -->
<template>
  <view class="page">
    <u-navbar title="首页" :safeAreaInsetTop="true" />
    
    <view class="content">
      <!-- 栅格布局 -->
      <u-row gutter="16">
        <u-col span="6" v-for="item in 4" :key="item">
          <view class="grid-item">项目{{ item }}</view>
        </u-col>
      </u-row>
    </view>
    
    <u-safe-area />
  </view>
</template>

<script setup>
import { ref } from 'vue';
// 业务逻辑
</script>

<style scoped lang="scss">
.page {
  background: $u-bg-color;
}
.content {
  padding: $u-padding-md;
}
</style>
```

#### 3. `components/custom-navbar/index.vue` - 自定义组件示例
```vue
<!-- 参考路径: components/custom-navbar/index.vue -->
<template>
  <u-navbar 
    :title="title"
    :placeholder="true"
    :safeAreaInsetTop="true"
    :leftIcon="showBack ? 'arrow-left' : ''"
    @leftClick="handleBack"
  >
    <template #right>
      <slot name="right"></slot>
    </template>
  </u-navbar>
</template>

<script setup>
defineProps({
  title: String,
  showBack: { type: Boolean, default: true }
});

const handleBack = () => {
  uni.navigateBack();
};
</script>
```

### 官方文档参考
- **UView 2.0 官方文档**：https://www.uviewui.com/
- **Uni-app 官方文档**：https://uniapp.dcloud.net.cn/
- **UView 组件源码**：`node_modules/uview-plus/components/`
- **主题变量参考**：`node_modules/uview-plus/theme.scss`

---

## 检查清单

在编写或审查移动端代码时，请确保以下所有项目都已完成：

### 📐 布局与适配
- [ ] 是否使用了`<view>`、`<text>`等小程序标签，而非HTML标签（`<div>`、`<span>`）
- [ ] 是否遵循UView栅格布局系统（`u-row`、`u-col`），而非手动计算宽度
- [ ] 是否在顶部导航使用了`:safeAreaInsetTop="true"`处理刘海屏
- [ ] 是否在底部固定元素后添加了`<u-safe-area />`适配底部安全区域
- [ ] 是否统一使用了`rpx`单位（除1px边框外）
- [ ] 是否设置了合理的最小点击区域（不小于88rpx × 88rpx）

### 🎨 主题与样式
- [ ] 是否在`uni.scss`中覆盖了主题变量，而非硬编码颜色
- [ ] 是否使用了UView组件的`type`属性应用预设主题色
- [ ] 是否使用SCSS变量定义颜色、字体、间距
- [ ] 是否遵循了文字颜色层级（主要 > 常规 > 次要 > 辅助）
- [ ] 是否避免了直接修改`node_modules`下的组件源码
- [ ] 是否使用`customStyle`进行局部样式调整

### 🧩 组件使用
- [ ] 是否优先使用UView 2.0内置组件，而非自己实现
- [ ] 是否使用了UView 2.0的props语法，避免UView 1.x的插槽语法
- [ ] 表单是否使用了`u-form`统一管理验证规则
- [ ] 列表是否实现了下拉刷新和上拉加载（`u-list`）
- [ ] 是否为所有异步操作添加了loading状态
- [ ] 弹窗和Toast是否提供了明确的用户反馈

### ⚡ 性能优化
- [ ] 长列表（超过50条）是否使用了虚拟滚动或分页加载
- [ ] 图片是否进行了压缩和懒加载处理
- [ ] 是否避免了在列表项中进行复杂计算
- [ ] 是否使用了代码分包（subPackages）优化首屏加载
- [ ] 频繁触发的操作是否添加了防抖或节流
- [ ] 是否避免了过度使用阴影和渐变效果

### 🔧 代码规范
- [ ] 是否统一使用Vue 3 Composition API（`<script setup>`）
- [ ] 是否为组件添加了必要的props类型定义
- [ ] 是否处理了错误情况并提供降级方案
- [ ] 是否遵循了响应式设计原则（设计稿750px基准）
- [ ] 是否避免了使用小程序不支持的CSS属性
- [ ] 代码是否符合团队的ESLint规范

### ♿ 用户体验
- [ ] 是否为图标添加了语义化说明
- [ ] 颜色对比度是否满足无障碍标准（至少4.5:1）
- [ ] 表单元素是否提供了明确的label和placeholder
- [ ] 重要操作是否提供了确认弹窗
- [ ] 网络请求失败是否有友好的错误提示
- [ ] 空状态是否有清晰的引导说明

### 🧪 测试验证
- [ ] 是否在iOS设备上测试了安全区域适配
- [ ] 是否在Android设备上测试了布局兼容性
- [ ] 是否测试了小程序、H5、App多端表现
- [ ] 是否测试了不同屏幕尺寸下的响应式效果
- [ ] 是否测试了暗黑模式（如项目支持）
- [ ] 是否测试了弱网环境下的加载体验

---

## 🎯 快速决策指南

遇到问题时，快速参考以下决策树：

```
问题：如何实现多列布局？
└─ 使用 u-row + u-col 栅格系统（12列）

问题：按钮颜色如何定制？
├─ 预设主题色 → 使用 type="primary/success/warning/error"
└─ 自定义颜色 → 在 uni.scss 中修改 $u-primary 等变量

问题：列表数据太多，页面卡顿？
├─ 数据量 < 50条 → 直接渲染
├─ 数据量 50-200条 → 使用分页加载（u-list）
└─ 数据量 > 200条 → 使用虚拟滚动

问题：底部按钮被刘海屏遮挡？
└─ 在按钮后添加 <u-safe-area />

问题：需要自定义组件样式？
├─ 全局样式 → 在 uni.scss 中覆盖变量
├─ 局部微调 → 使用 customStyle 属性
└─ 复杂定制 → 包装UView组件创建自定义组件

问题：表单验证如何实现？
└─ 使用 u-form + rules 统一管理验证规则

问题：图片加载太慢？
├─ 压缩图片（使用TinyPNG等工具）
├─ 使用WebP格式
├─ 使用CDN加速
└─ 启用 u-image 懒加载
```

---

## 📚 扩展阅读

- **设计规范**：参考若依移动端设计指南
- **性能优化**：Uni-app性能优化最佳实践
- **多端适配**：Uni-app多端兼容指南
- **UView进阶**：UView 2.0高级用法和自定义主题

---

**最后更新时间**：2026-01-26  
**适用版本**：UView 2.0+ / Uni-app Vue 3  
**维护者**：若依移动端开发团队
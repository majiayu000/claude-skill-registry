---
name: uniapp-platform
description: |
  基于若依-vue-plus框架的移动端（Uni-app）跨平台开发规范，定义条件编译的使用标准。通过特定语法处理H5、微信小程序、支付宝小程序及App端的差异化逻辑与样式，确保一套代码多端运行。
  
  触发场景：
  - 调用平台特有API（如微信支付、App推送、H5路由等）
  - 处理平台样式差异（状态栏、安全区域、导航栏）
  - 屏蔽不兼容功能（某些API仅在特定平台可用）
  - 实现差异化业务逻辑（不同平台的用户体验策略）
  - 优化包体积（移除目标平台不需要的代码）
  
  触发词：条件编译、跨平台兼容、平台判断、差异化处理、ifdef、多端适配、平台API、样式适配
---

# Uni-app 跨平台条件编译规范

## 核心规范

### 规范1：JS逻辑层的条件编译

**详细说明：**
在 `.js` 或 `.vue` 的 `<script>` 标签中，必须使用以 `#ifdef`（如果定义）、`#ifndef`（如果未定义）开头，以 `#endif` 结尾的特殊注释语法进行代码隔离。

**关键原则：**
- **编译时优于运行时**：严禁在编译期能确定的逻辑中使用运行时判断（如 `uni.getSystemInfoSync().platform`），优先使用条件编译以减小最终包体积
- **注释语法**：必须使用双斜杠注释 `// #ifdef` 或多行注释 `/* #ifdef */`
- **嵌套支持**：支持条件编译嵌套，但需保证每层都正确闭合
- **逻辑运算**：支持 `||`（或）和 `&&`（且）运算符，如 `// #ifdef H5 || MP-WEIXIN`

**常用平台标识：**
- `H5` - H5端
- `APP-PLUS` - App端
- `MP-WEIXIN` - 微信小程序
- `MP-ALIPAY` - 支付宝小程序
- `MP-BAIDU` - 百度小程序
- `MP-TOUTIAO` - 抖音小程序
- `MP` - 所有小程序平台

```javascript
/**
 * 设置应用角标数量
 * @param {number} count - 角标数量
 */
export function setBadgeCount(count) {
  // 仅在App平台生效
  // #ifdef APP-PLUS
  plus.runtime.setBadgeNumber(count);
  // #endif

  // 仅在微信小程序生效
  // #ifdef MP-WEIXIN
  wx.setTabBarBadge({
    index: 0,
    text: count.toString()
  });
  // #endif
  
  // H5端可能需要修改favicon或title
  // #ifdef H5
  document.title = count > 0 ? `(${count}) 应用标题` : '应用标题';
  // #endif
}

/**
 * 分享功能 - 多平台适配
 */
export function shareContent(options) {
  // #ifdef H5
  // H5使用Web Share API或第三方分享
  if (navigator.share) {
    navigator.share(options);
  }
  // #endif
  
  // #ifdef MP-WEIXIN
  // 微信小程序使用wx.shareAppMessage
  wx.showShareMenu({
    withShareTicket: true
  });
  // #endif
  
  // #ifdef APP-PLUS
  // App端使用原生分享
  uni.share({
    provider: 'weixin',
    type: 0,
    title: options.title,
    success: () => console.log('分享成功')
  });
  // #endif
}

// 示例：平台常量导出（使用逻辑运算）
const platform = {
  // #ifdef H5
  isH5: true,
  isApp: false,
  isMiniProgram: false
  // #endif
  // #ifdef APP-PLUS
  isH5: false,
  isApp: true,
  isMiniProgram: false
  // #endif
  // #ifdef MP
  isH5: false,
  isApp: false,
  isMiniProgram: true
  // #endif
};

// 示例：多平台条件（或运算）
// #ifdef H5 || MP-WEIXIN
console.log('这段代码在H5或微信小程序中执行');
// #endif

// 示例：反向条件（ifndef）
// #ifndef APP-PLUS
console.log('这段代码在非App平台执行');
// #endif
```

### 规范2：样式层（CSS/SCSS）的条件编译

**详细说明：**
在 `.vue` 的 `<style>` 标签、`.css` 或 `.scss` 文件中，利用 CSS 注释语法 `/* #ifdef PLATFORM */ ... /* #endif */` 处理不同平台的样式差异。

**主要应用场景：**
- **原生导航栏高度差异**：不同平台状态栏高度不同
- **底部安全区域**：iPhone X 及以上机型的底部安全距离
- **小程序默认样式重置**：不同小程序的默认样式存在差异
- **触控区域适配**：移动端点击热区与PC端鼠标交互差异
- **滚动行为**：H5与原生滚动的性能优化

**注意事项：**
- 必须使用 `/* */` 多行注释格式，不支持 `//` 单行注释
- 支持在 CSS、SCSS、LESS 等预处理器中使用
- 条件编译的样式优先级与书写顺序有关，注意样式覆盖问题

```css
/* 处理不同平台的安全区域与顶部间距 */
.status-bar {
  height: 20px;
  background-color: #fff;
}

/* H5端通常不需要状态栏占位，或者在顶部有浏览器栏 */
/* #ifdef H5 */
.status-bar {
  height: 0;
  display: none;
}
/* #endif */

/* 微信小程序自定义导航栏高度适配 */
/* #ifdef MP-WEIXIN */
.status-bar {
  height: var(--status-bar-height);
}

.custom-navbar {
  height: 44px;
  line-height: 44px;
}
/* #endif */

/* App端处理刘海屏及横竖屏差异 */
/* #ifdef APP-PLUS */
.content {
  padding-top: var(--status-bar-height);
  /* App端使用原生滚动优化性能 */
  overflow-y: scroll;
  -webkit-overflow-scrolling: touch;
}
/* #endif */

/* 底部安全区域适配（iPhone X等全面屏） */
.footer {
  padding-bottom: 0;
}

/* #ifdef APP-PLUS || H5 */
.footer {
  padding-bottom: constant(safe-area-inset-bottom); /* iOS 11.0-11.2 */
  padding-bottom: env(safe-area-inset-bottom); /* iOS 11.2+ */
}
/* #endif */

/* 小程序端按钮样式重置 */
/* #ifdef MP */
button {
  border: none;
  background: transparent;
  padding: 0;
  margin: 0;
  line-height: inherit;
}

button::after {
  border: none;
}
/* #endif */

/* H5端特有的滚动容器样式 */
/* #ifdef H5 */
.scroll-view {
  height: 100vh;
  overflow-y: auto;
  /* 更流畅的滚动 */
  -webkit-overflow-scrolling: touch;
  scroll-behavior: smooth;
}
/* #endif */

/* 仅在非H5平台显示的元素 */
/* #ifndef H5 */
.download-app-banner {
  display: none;
}
/* #endif */

/* 多平台条件（或运算）*/
/* #ifdef MP-WEIXIN || MP-ALIPAY */
.mini-program-specific {
  /* 微信和支付宝小程序共用的样式 */
  box-sizing: border-box;
}
/* #endif */
```

### 规范3：模板层（Template）的条件编译

**详细说明：**
在 `.vue` 的 `<template>` 标签中，使用 HTML 注释语法 `<!-- #ifdef PLATFORM --> ... <!-- #endif -->` 控制元素的渲染。

**使用场景：**
- 不同平台显示不同的UI组件
- 隐藏特定平台不支持的功能入口
- 根据平台特性调整页面布局结构

```vue
<template>
  <view class="container">
    <!-- 所有平台都显示的内容 -->
    <view class="header">公共头部</view>
    
    <!-- 仅H5端显示的下载引导 -->
    <!-- #ifdef H5 -->
    <view class="download-tip">
      <text>下载App享受更好体验</text>
      <button @click="downloadApp">立即下载</button>
    </view>
    <!-- #endif -->
    
    <!-- 仅App端显示的原生功能 -->
    <!-- #ifdef APP-PLUS -->
    <button @click="openBiometric">指纹/面部识别</button>
    <!-- #endif -->
    
    <!-- 仅小程序显示的分享按钮 -->
    <!-- #ifdef MP -->
    <button open-type="share">分享给好友</button>
    <!-- #endif -->
    
    <!-- 微信小程序特有的客服功能 -->
    <!-- #ifdef MP-WEIXIN -->
    <button open-type="contact">联系客服</button>
    <!-- #endif -->
    
    <!-- 多平台或运算 -->
    <!-- #ifdef H5 || APP-PLUS -->
    <view class="web-app-feature">Web和App共有功能</view>
    <!-- #endif -->
    
    <!-- 非App平台显示 -->
    <!-- #ifndef APP-PLUS -->
    <view class="upgrade-tip">升级到App版本解锁更多功能</view>
    <!-- #endif -->
  </view>
</template>
```

### 规范4：pages.json 和 manifest.json 的条件编译

**详细说明：**
在配置文件中使用条件编译可以为不同平台设置不同的页面配置、权限申请等。

```json
{
  "pages": [
    {
      "path": "pages/index/index",
      "style": {
        "navigationBarTitleText": "首页",
        // #ifdef H5
        "navigationStyle": "custom"
        // #endif
        // #ifdef MP-WEIXIN
        "navigationBarBackgroundColor": "#ffffff"
        // #endif
      }
    }
  ],
  // #ifdef APP-PLUS
  "permission": {
    "scope.userLocation": {
      "desc": "您的位置信息将用于小程序位置接口的效果展示"
    }
  }
  // #endif
}
```

## 禁止事项

### 语法错误类
- ❌ **禁止混淆JS、CSS、Template条件编译的语法**
  - JS必须使用 `// #ifdef` 或 `/* #ifdef */`
  - CSS必须使用 `/* #ifdef */` 多行注释格式
  - Template必须使用 `<!-- #ifdef -->` HTML注释格式
  
- ❌ **禁止忘记闭合 `#endif`**
  - 每个 `#ifdef` 或 `#ifndef` 必须有对应的 `#endif`
  - 会导致编译错误或代码逻辑错乱
  - 嵌套时更要注意层级关系

- ❌ **禁止使用不存在的平台标识**
  - 例如：`#ifdef IOS`（错误，应该用 `APP-PLUS` 然后在运行时判断）
  - 必须使用官方文档定义的平台标识

### 性能优化类
- ❌ **禁止在非必要情况下使用运行时判断**
  - 错误示例：`if (uni.getSystemInfoSync().platform === 'ios')`
  - 应优先使用编译时条件编译提升性能，减小包体积
  - 运行时判断会将所有代码打包进去，无法做tree-shaking

- ❌ **禁止过度使用条件编译**
  - 不要为了一行简单的代码就使用条件编译
  - 优先考虑使用 uni-app 的跨平台API
  - 仅在确实存在平台差异时才使用

### 兼容性错误类
- ❌ **禁止在条件编译块外引用平台特有API**
  - 错误示例：直接使用 `plus.runtime`（仅App端可用）
  - 会导致H5或小程序运行时报错：`plus is not defined`
  - 必须将平台特有API包裹在对应的条件编译块内

- ❌ **禁止假设所有小程序行为一致**
  - 微信、支付宝、百度等小程序存在API差异
  - 使用 `MP` 时要确保该API在所有小程序都支持
  - 必要时针对具体小程序平台使用 `MP-WEIXIN`、`MP-ALIPAY` 等

### 代码维护类
- ❌ **禁止在条件编译块内写过长的业务逻辑**
  - 超过50行的差异化逻辑应抽离成独立文件
  - 使用文件级条件编译：创建 `utils.h5.js`、`utils.app.js` 等
  - 提高代码可读性和可维护性

- ❌ **禁止缺少必要的注释说明**
  - 每个条件编译块应注释说明原因
  - 例如：`// #ifdef APP-PLUS  // App端需要调用原生推送API`
  - 便于团队成员理解平台差异处理逻辑

### 打包发布类
- ❌ **禁止在生产环境保留调试用的条件编译**
  - 示例：`// #ifdef H5  console.log('debug info')  // #endif`
  - 应使用环境变量配合条件编译：`// #ifdef H5 && process.env.NODE_ENV === 'development'`

- ❌ **禁止忽略不同平台的测试**
  - 每次发布前必须在目标平台进行测试
  - 条件编译的代码无法在其他平台验证
  - 容易出现某个平台特有的bug

## 最佳实践

### 1. 文件级条件编译
当不同平台的实现差异较大时（超过50行），建议使用文件级条件编译：

**目录结构：**
```
src/
├── utils/
│   ├── request.js          // 公共逻辑
│   ├── request.h5.js       // H5特有实现
│   ├── request.app.js      // App特有实现
│   └── request.mp.js       // 小程序特有实现
```

**导入方式：**
```javascript
// 在其他文件中导入时，uni-app会根据编译平台自动选择
import { request } from '@/utils/request.js';
```

### 2. 静态资源条件编译
图片等静态资源也支持条件编译：
```
static/
├── logo.png           // 默认logo
├── logo.h5.png        // H5专用logo
└── logo.app.png       // App专用logo
```

```vue
<template>
  <!-- uni-app会自动根据平台选择对应资源 -->
  <image src="/static/logo.png" />
</template>
```

### 3. 组件级条件编译
为不同平台创建专用组件：
```
components/
├── navbar/
│   ├── navbar.vue          // 默认导航栏
│   ├── navbar.h5.vue       // H5导航栏
│   └── navbar.mp.vue       // 小程序导航栏
```

### 4. 配置文件最佳实践
在 `vue.config.js` 或 `vite.config.js` 中可以通过环境变量判断平台：
```javascript
const platform = process.env.UNI_PLATFORM;

module.exports = {
  // 根据平台配置不同的构建选项
  chainWebpack: (config) => {
    if (platform === 'h5') {
      // H5特殊配置
    } else if (platform === 'app-plus') {
      // App特殊配置
    }
  }
};
```

## 参考代码

### 若依框架集成示例
在若依-vue-plus框架中的典型应用：

**文件路径：`src/utils/platform.js`**（平台工具函数封装）
```javascript
/**
 * 平台判断工具类
 * 统一封装平台相关的判断和处理逻辑
 */

// 平台标识常量
export const PLATFORM = {
  // #ifdef H5
  type: 'h5',
  isH5: true,
  isApp: false,
  isMp: false
  // #endif
  // #ifdef APP-PLUS
  type: 'app',
  isH5: false,
  isApp: true,
  isMp: false
  // #endif
  // #ifdef MP
  type: 'mp',
  isH5: false,
  isApp: false,
  isMp: true
  // #endif
};

/**
 * 获取系统信息（跨平台封装）
 */
export function getSystemInfo() {
  return new Promise((resolve, reject) => {
    uni.getSystemInfo({
      success: (res) => {
        // #ifdef APP-PLUS
        res.statusBarHeight = plus.navigator.getStatusbarHeight();
        // #endif
        resolve(res);
      },
      fail: reject
    });
  });
}

/**
 * 路由跳转（处理平台差异）
 */
export function navigateTo(url, options = {}) {
  // #ifdef H5
  // H5端可能需要处理hash或history模式
  if (options.openInNewTab) {
    window.open(url, '_blank');
    return;
  }
  // #endif
  
  uni.navigateTo({
    url,
    ...options
  });
}
```

**文件路径：`src/pages/index/index.vue`**（页面级条件编译示例）
```vue
<template>
  <view class="container">
    <!-- #ifdef APP-PLUS -->
    <status-bar />
    <!-- #endif -->
    
    <navbar title="首页" />
    
    <view class="content">
      <!-- 内容区域 -->
    </view>
    
    <!-- #ifdef H5 -->
    <download-app-banner />
    <!-- #endif -->
  </view>
</template>

<script>
export default {
  data() {
    return {
      userInfo: {}
    };
  },
  onLoad() {
    this.initPage();
  },
  methods: {
    initPage() {
      // #ifdef APP-PLUS
      // App端初始化推送
      this.initPush();
      // #endif
      
      // #ifdef MP-WEIXIN
      // 微信小程序初始化授权
      this.initWxAuth();
      // #endif
      
      // #ifdef H5
      // H5端初始化统计
      this.initH5Analytics();
      // #endif
    },
    
    // #ifdef APP-PLUS
    initPush() {
      plus.push.addEventListener('click', (msg) => {
        console.log('收到推送消息', msg);
      });
    },
    // #endif
    
    // #ifdef MP-WEIXIN
    initWxAuth() {
      wx.getSetting({
        success: (res) => {
          if (!res.authSetting['scope.userInfo']) {
            // 请求用户授权
          }
        }
      });
    },
    // #endif
    
    // #ifdef H5
    initH5Analytics() {
      // 初始化H5统计代码
      if (window._hmt) {
        window._hmt.push(['_trackPageview', '/pages/index/index']);
      }
    }
    // #endif
  }
};
</script>

<style scoped>
.container {
  min-height: 100vh;
  background-color: #f5f5f5;
}

/* #ifdef APP-PLUS */
.container {
  padding-top: var(--status-bar-height);
}
/* #endif */

.content {
  padding: 20rpx;
}

/* #ifdef H5 */
.content {
  max-width: 750px;
  margin: 0 auto;
}
/* #endif */

/* #ifdef MP */
.content {
  /* 小程序端需要预留底部tabbar高度 */
  padding-bottom: 100rpx;
}
/* #endif */
</style>
```

**文件路径：`src/App.vue`**（全局样式差异处理）
```vue
<style lang="scss">
/* 全局样式重置 */
page {
  background-color: #f5f5f5;
  font-size: 14px;
  line-height: 1.5;
}

/* #ifdef MP */
/* 小程序全局样式重置 */
page {
  height: 100%;
}

button {
  border: none;
  background: transparent;
  padding: 0;
  line-height: inherit;
}

button::after {
  border: none;
}
/* #endif */

/* #ifdef H5 */
/* H5端全局样式 */
page {
  /* H5端使用原生滚动 */
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

/* H5端适配PC大屏 */
@media screen and (min-width: 768px) {
  page {
    background-color: #e5e5e5;
  }
}
/* #endif */

/* #ifdef APP-PLUS */
/* App端全局样式 */
page {
  /* App端状态栏变量 */
  --status-bar-height: 20px;
}

/* 处理安全区域 */
.safe-area-inset-bottom {
  padding-bottom: constant(safe-area-inset-bottom);
  padding-bottom: env(safe-area-inset-bottom);
}
/* #endif */
</style>
```

**文件路径：`src/api/request.js`**（网络请求平台适配）
```javascript
import { PLATFORM } from '@/utils/platform';

/**
 * 请求拦截器 - 平台差异处理
 */
export function requestInterceptor(config) {
  // 添加平台标识
  config.header = config.header || {};
  config.header['X-Platform'] = PLATFORM.type;
  
  // #ifdef H5
  // H5端可能需要处理跨域
  config.withCredentials = true;
  // #endif
  
  // #ifdef APP-PLUS
  // App端设置超时时间更长
  config.timeout = 30000;
  // #endif
  
  // #ifdef MP
  // 小程序端超时时间较短
  config.timeout = 10000;
  // #endif
  
  return config;
}

/**
 * 文件上传 - 平台差异处理
 */
export function uploadFile(filePath, options = {}) {
  // #ifdef H5
  // H5端需要将file对象转换
  return new Promise((resolve, reject) => {
    // H5特殊处理逻辑
  });
  // #endif
  
  // #ifdef APP-PLUS || MP
  // App和小程序使用统一上传接口
  return uni.uploadFile({
    url: options.url,
    filePath,
    name: options.name || 'file',
    ...options
  });
  // #endif
}
```

## 检查清单

### 开发阶段
- [ ] **语法检查**
  - [ ] 是否使用了正确的条件编译语法（JS用双斜杠注释、CSS用多行注释、Template用HTML注释）
  - [ ] 是否每个 `#ifdef` / `#ifndef` 都正确配对 `#endif`
  - [ ] 是否使用了正确的平台标识（H5、APP-PLUS、MP-WEIXIN等）
  - [ ] 嵌套的条件编译是否正确闭合

- [ ] **性能优化**
  - [ ] 是否避免了不必要的运行时判断，优先使用编译时隔离
  - [ ] 是否将超过50行的平台差异代码抽离成独立文件
  - [ ] 是否移除了调试用的条件编译代码

- [ ] **兼容性检查**
  - [ ] 平台特有API是否都包裹在对应的条件编译块内
  - [ ] 是否正确处理了不同小程序平台的API差异
  - [ ] 是否验证了所有使用的API在目标平台都支持

- [ ] **样式适配**
  - [ ] 是否正确处理了状态栏高度差异
  - [ ] 是否处理了底部安全区域（iPhone X等全面屏）
  - [ ] 是否验证了不同端的样式差异（特别是H5与小程序的导航栏）
  - [ ] 是否重置了小程序的默认样式

### 测试阶段
- [ ] **多平台测试**
  - [ ] H5端测试（Chrome、Safari、移动端浏览器）
  - [ ] 微信小程序测试（真机、开发者工具）
  - [ ] App端测试（iOS、Android真机）
  - [ ] 其他目标小程序平台测试（支付宝、百度等）

- [ ] **功能验证**
  - [ ] 条件编译的功能在目标平台是否正常工作
  - [ ] 非目标平台是否正确隐藏了相关功能
  - [ ] 是否存在平台特有的bug或crash

- [ ] **样式验证**
  - [ ] 不同平台的布局是否正常
  - [ ] 状态栏、导航栏、安全区域是否正确适配
  - [ ] 不同屏幕尺寸是否正常显示

### 发布阶段
- [ ] **代码审查**
  - [ ] 是否添加了必要的注释说明条件编译的原因
  - [ ] 是否清理了无用的条件编译代码
  - [ ] 是否更新了相关文档

- [ ] **打包验证**
  - [ ] 各平台的打包是否成功
  - [ ] 包体积是否符合预期（条件编译应减小包体积）
  - [ ] 是否有多余的平台代码被打包进去

### 维护阶段
- [ ] **文档更新**
  - [ ] 是否记录了平台差异的处理方案
  - [ ] 是否更新了团队的开发规范文档
  - [ ] 是否分享了最佳实践案例

- [ ] **代码重构**
  - [ ] 定期检查是否有过时的条件编译代码
  - [ ] 评估是否可以用uni-app新API替代条件编译
  - [ ] 优化过于复杂的条件编译逻辑

## 常见问题与解决方案

### Q1: 条件编译后某些平台报错 "xxx is not defined"
**原因：** 在条件编译块外使用了平台特有的API或变量。

**解决方案：**
```javascript
// ❌ 错误示例
const deviceInfo = plus.device.uuid; // H5和小程序会报错

// ✅ 正确示例
let deviceInfo = '';
// #ifdef APP-PLUS
deviceInfo = plus.device.uuid;
// #endif
```

### Q2: CSS条件编译不生效
**原因：** 使用了错误的注释语法或条件编译被样式覆盖。

**解决方案：**
```css
/* ❌ 错误：使用了单行注释 */
// #ifdef H5
.header { height: 44px; }
// #endif

/* ✅ 正确：使用多行注释 */
/* #ifdef H5 */
.header { height: 44px; }
/* #endif */
```

### Q3: 如何调试条件编译代码
**方法：**
1. 使用 HBuilderX 的条件编译高亮功能
2. 在编译后的代码中查看是否包含预期的代码
3. 使用 `console.log` 配合条件编译验证代码是否执行
4. 利用浏览器开发者工具查看H5端的编译结果

### Q4: 多个平台共用代码但有小差异如何处理
**方案：** 使用逻辑运算符组合平台标识。

```javascript
// #ifdef H5 || MP-WEIXIN
// H5和微信小程序共用的代码，但App端不用
export function shareToFriend(options) {
  // 实现分享逻辑
}
// #endif
```

### Q5: 如何在条件编译中使用环境变量
**方案：** 结合 process.env 和条件编译。

```javascript
// #ifdef H5
if (process.env.NODE_ENV === 'development') {
  console.log('H5开发环境');
}
// #endif
```

## 相关资源

- [uni-app官方文档 - 条件编译](https://uniapp.dcloud.net.cn/tutorial/platform.html)
- [若依-vue-plus框架文档](https://gitee.com/dromara/RuoYi-Vue-Plus)
- [uni-app跨平台兼容性列表](https://uniapp.dcloud.net.cn/api/)
- [各小程序平台官方文档对比](https://uniapp.dcloud.net.cn/matter.html#_1-api-%E7%9A%84-promise-%E5%8C%96)
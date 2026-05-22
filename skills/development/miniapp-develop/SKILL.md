---
name: miniapp-develop
description: 小程序开发专家，精通微信、支付宝、抖音等多个平台的小程序开发
version: 1.0.0
---

# 小程序开发专家

## 触发条件
当用户提到以下内容时自动触发：
- "小程序"
- "微信小程序"
- "支付宝小程序"
- "抖音小程序"
- "uni-app"
- "Taro"

## 核心能力

### 小程序平台特性
- **微信小程序**: 熟悉微信小程序 API、组件系统、云开发、支付接口等
- **支付宝小程序**: 掌握支付宝小程序开发规范、支付能力、芝麻信用等
- **抖音小程序**: 了解抖音小程序生态、视频能力、流量接入等
- **百度小程序**: 熟悉百度智能小程序开发、搜索优化等

### 前端技术栈
- **框架掌握**: 原生小程序、Taro、uni-app、mpvue 等跨平台框架
- **UI 组件**: WeUI、Vant Weapp、ColorUI 等 UI 框架
- **状态管理**: 跨页面状态管理、数据缓存解决方案
- **动画交互**: CSS 动画、API 动画、手势操作等

### 后端服务
- **云开发**: 微信云开发、支付宝云开发等无服务器方案
- **API 设计**: RESTful API 设计、数据加密、鉴权机制
- **数据库**: 数据库设计、数据查询优化
- **文件存储**: 文件上传下载、CDN 加速等

### 小程序生态
- **运营分析**: 数据统计、用户行为分析、性能监控
- **营销工具**: 分享裂变、优惠券、积分系统等
- **支付系统**: 微信支付、支付宝支付集成
- **地图定位**: 地图服务、定位功能、导航等

## 工作流程

### 1. 需求分析
- 明确小程序功能需求和业务场景
- 分析目标用户群体和使用习惯
- 评估技术可行性和开发成本
- 确定开发平台和优先级

### 2. 架构设计
- 设计小程序整体架构和目录结构
- 选择合适的技术栈和开发框架
- 规划数据流和页面跳转关系
- 制定组件拆分和复用策略

### 3. UI/UX 设计
- 设计小程序界面原型和交互流程
- 确定视觉风格和设计规范
- 优化用户体验和操作流程
- 适配不同设备屏幕尺寸

### 4. 功能开发
- 实现页面结构和布局
- 开发业务逻辑和数据处理
- 集成第三方 API 和服务
- 实现动画效果和交互细节

### 5. 测试优化
- 功能测试和兼容性测试
- 性能优化和代码审查
- 用户体验测试和反馈收集

### 6. 发布上线
- 提交审核和版本管理
- 配置服务器和域名
- 监控线上运行状态
- 收集用户反馈和迭代优化

## 常见解决方案

### 页面跳转
```javascript
// 微信小程序
wx.navigateTo({
  url: '/pages/detail/detail?id=123'
})

// Taro
Taro.navigateTo({
  url: '/pages/detail/detail?id=123'
})

// uni-app
uni.navigateTo({
  url: '/pages/detail/detail?id=123'
})
```

### 数据请求
```javascript
// 微信小程序
wx.request({
  url: 'https://api.example.com/data',
  method: 'GET',
  success: (res) => {
    console.log(res.data)
  }
})

// Taro
Taro.request({
  url: 'https://api.example.com/data',
  method: 'GET'
}).then(res => {
  console.log(res.data)
})

// uni-app
uni.request({
  url: 'https://api.example.com/data',
  method: 'GET',
  success: (res) => {
    console.log(res.data)
  }
})
```

### 本地存储
```javascript
// 微信小程序
wx.setStorageSync('key', 'value')
const value = wx.getStorageSync('key')

// Taro
Taro.setStorageSync('key', 'value')
const value = Taro.getStorageSync('key')

// uni-app
uni.setStorageSync('key', 'value')
const value = uni.getStorageSync('key')
```

### 支付集成
```javascript
// 微信支付
wx.requestPayment({
  timeStamp: '',
  nonceStr: '',
  package: '',
  signType: 'MD5',
  paySign: '',
  success: (res) => {
    console.log('支付成功')
  }
})

// 支付宝支付
my.tradePay({
  tradeNO: '20231227123456789',
  success: (res) => {
    console.log('支付成功')
  }
})
```

## 性能优化

### 图片优化
- 使用合适的图片格式（WebP、JPEG）
- 图片懒加载
- 图片压缩和裁剪
- 使用 CDN 加速

### 代码优化
- 分包加载
- 按需引入组件
- 减少不必要的 setData 调用
- 使用防抖和节流

### 网络优化
- 接口合并和缓存
- 使用 HTTP/2
- 预加载关键资源
- 减少请求次数

## 项目配置

### 微信小程序 app.json
```json
{
  "pages": [
    "pages/index/index",
    "pages/detail/detail"
  ],
  "window": {
    "navigationBarTitleText": "小程序",
    "navigationBarBackgroundColor": "#ffffff"
  },
  "tabBar": {
    "list": [
      {
        "pagePath": "pages/index/index",
        "text": "首页"
      }
    ]
  }
}
```

### Taro 配置
```javascript
// config/index.js
export default {
  framework: 'react',
  outputRoot: 'dist',
  weapp: {
    module: {
      postcss: {
        autoprefixer: {
          enable: true
        }
      }
    }
  }
}
```

### uni-app 配置
```json
{
  "pages": [
    {
      "path": "pages/index/index",
      "style": {
        "navigationBarTitleText": "首页"
      }
    }
  ],
  "globalStyle": {
    "navigationBarTextStyle": "black",
    "navigationBarTitleText": "uni-app",
    "navigationBarBackgroundColor": "#F8F8F8"
  }
}
```
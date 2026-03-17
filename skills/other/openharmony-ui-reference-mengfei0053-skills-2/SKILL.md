---
name: openharmony-ui-reference
description: 用于使用 ArkTS 开发 OpenHarmony UI 时 - 查找布局、组件、状态管理、动画、导航,或处理缺少装饰器、状态不更新、渲染问题等错误
---

# OpenHarmony UI 快速参考

## 概述

OpenHarmony 使用 **ArkTS** (基于 TypeScript 的声明式 UI) 来构建用户界面。核心概念:声明式 UI 描述、组件化架构、状态管理装饰器、响应式布局。

**官方文档:** `docs-OpenHarmony-v6.0-Release/zh-cn/application-dev/ui/`
**快速参考:** `docs/` (本地提取的核心文档)

## 状态管理

### V2 (推荐用于新项目)

| 装饰器 | 用途 | 作用域 |
|-----------|---------|-------|
| `@Local` | 组件内部状态 | 仅组件内部 |
| `@Param` | 父 → 子 (单向) | 父到子 |
| `@Event` | 子 → 父回调 | 子到父 |
| `@Provider`/`@Consumer` | 跨组件同步 | 任意后代组件 |

**双向绑定:**
```typescript
// 父组件
@ComponentV2
struct Parent {
  @Local text: string = ''

  build() {
    Child({ text: this.text, onTextChange: (val) => { this.text = val } })
  }
}

// 子组件
@ComponentV2
struct Child {
  @Param text: string
  @Event onTextChange: (val: string) => void

  build() {
    TextInput({ text: this.text })
      .onChange((val) => this.onTextChange(val))
  }
}

// 语法糖(更简单)
TextInput({ text: $$this.text })
```

### V1 (传统方式)

| 装饰器 | 用途 | 作用域 |
|-----------|---------|-------|
| `@State` | 组件内部状态 | 仅组件内部 |
| `@Prop` | 父 → 子 (单向) | 父到子 |
| `@Link` | 父 ↔ 子 (双向) | 双向绑定 |
| `@Provide`/`@Consume` | 跨组件同步 | 任意后代组件 |

**文档参考:** `docs/state-management/arkts-state-management-overview.md`

## 布局

| 需求 | 组件 | 关键属性 | 文档 |
|---------------|-----------|----------------|------|
| **水平排列** | `Row` | space, alignItems, justifyContent | `docs/layout/arkts-layout-development-linear.md` |
| **垂直排列** | `Column` | space, alignItems, justifyContent | `docs/layout/arkts-layout-development-linear.md` |
| **层叠布局** | `Stack` | alignContent | `docs/layout/arkts-layout-development-stack-layout.md` |
| **弹性布局** | `Flex` | direction, wrap, justifyContent | `docs/layout/arkts-layout-development-flex-layout.md` |
| **相对布局** | `RelativeContainer` | x/y 规则 | `docs/layout/arkts-layout-development-relative-layout.md` |
| **网格布局** | `Grid`/`GridItem` | columnsTemplate, rowsTemplate | `docs/layout/arkts-layout-development-grid-layout.md` |
| **标签页** | `Tabs`/`TabContent` | barPosition, scrollable | `docs/navigation/arkts-navigation-tabs.md` |
| **列表** | `List`/`ListItem` | space, scrollBar | `docs/layout/arkts-layout-development-create-list.md` |
| **瀑布流** | `WaterFlow`/`FlowItem` | columnsTemplate | `docs/layout/arkts-layout-development-create-waterflow.md` |

**内容居中:**
```typescript
Column() {
  Text('Centered')
}
.width('100%')
.height('100%')
.justifyContent(FlexAlign.Center)
.alignItems(HorizontalAlign.Center)
```

**文档参考:** `docs/layout/arkts-layout-development-overview.md`

## 常用组件

| 组件 | 用途 | 文档 |
|-----------|-------|------|
| **Text** | 显示文本 | `docs/components/arkts-common-components-text-display.md` |
| **TextInput** | 单行输入 | `docs/components/arkts-common-components-text-input.md` |
| **TextArea** | 多行输入 | `docs/components/arkts-common-components-text-input.md` |
| **Button** | 可点击按钮 | `docs/components/arkts-common-components-button.md` |
| **Image** | 显示图片 | `docs/components/arkts-graphics-display.md` |
| **List** | 垂直滚动列表 | `docs/layout/arkts-layout-development-create-list.md` |
| **Grid** | 网格布局 | `docs/layout/arkts-layout-development-create-grid.md` |
| **Swiper** | 轮播图 | `docs/layout/arkts-layout-development-create-looping.md` |
| **RichEditor** | 富文本编辑器 | `docs/components/arkts-common-components-richeditor.md` |

## 导航

**Navigation (推荐):**
```typescript
@Entry
@Component
struct NavPage {
  @Provide('pageInfos') pageInfos: NavPathStack = new NavPathStack()

  build() {
    Navigation(this.pageInfos) {
      Column() {
        Button('Go to Page2')
          .onClick(() => {
            this.pageInfos.pushPath({ name: 'Page2' })
          })
      }
    }
    .title('Main Page')
  }
}
```

**Router (传统方式):**
```typescript
import router from '@ohos.router'

// 跳转页面
router.pushUrl({ url: 'pages/Page2' })

// 返回
router.back()
```

**文档参考:**
- Navigation: `docs/navigation/arkts-navigation-navigation.md`
- Router: `docs/navigation/arkts-routing.md`

## 对话框和弹窗

| 类型 | 方法 | 使用场景 | 文档 |
|------|--------|----------|------|
| **自定义对话框** | `openCustomDialog()` | 推荐 | `docs/uicontext/arkts-uicontext-custom-dialog.md` |
| **警告对话框** | `AlertDialog.show()` | 简单确认 | `docs/dialogs/arkts-base-dialog-overview.md` |
| **列表选择** | `ActionSheet.show()` | 选项选择 | `docs/dialogs/arkts-base-dialog-overview.md` |
| **弹窗** | `.bindPopup()` | 绑定到组件 | `docs/popup/arkts-popup-and-menu-components-popup.md` |
| **提示** | `prompt.showToast()` | 简短反馈 | `docs/popup/arkts-create-toast.md` |

## 动画

| 类型 | API | 使用场景 | 文档 |
|------|-----|----------|------|
| **属性动画** | `.animateTo()` | 平滑属性变化 | `docs/animation/arkts-attribute-animation-overview.md` |
| **转场动画** | `.transition()` | 进出场动画 | `docs/animation/arkts-transition-overview.md` |
| **组件动画** | `animateTo` | 组合多个动画 | `docs/animation/arkts-component-animation.md` |

```typescript
// 属性动画
@State scale: number = 1

Image($r('app.media.icon'))
  .scale({ x: this.scale, y: this.scale })
  .onClick(() => {
    animateTo({ duration: 300 }, () => {
      this.scale = this.scale === 1 ? 1.5 : 1
    })
  })
```

## 渲染控制

| 控制方式 | 语法 | 使用场景 | 文档 |
|---------|--------|----------|------|
| **条件渲染** | `if (condition) { } else { }` | 显示/隐藏组件 | `docs/state-management/arkts-rendering-control-ifelse.md` |
| **循环渲染** | `ForEach(arr, (item) => {}, (item) => key)` | 渲染列表 | `docs/state-management/arkts-rendering-control-foreach.md` |
| **懒加载循环** | `LazyForEach(dataSource, (item) => {})` | 大数据集 | `docs/state-management/arkts-rendering-control-lazyforeach.md` |

```typescript
// ForEach (始终提供唯一键)
ForEach(this.items, (item: Item) => {
  Text(item.name)
}, (item: Item) => item.id)
```

## 样式

**@Styles (可复用样式):**
```typescript
@Styles
function cardStyle() {
  .backgroundColor(Color.White)
  .borderRadius(12)
  .padding(16)
}

Column() {}
  .cardStyle()
```

**@Extend (扩展组件):**
```typescript
@Extend(Text)
function redText() {
  .fontSize(18)
  .fontColor(Color.Red)
}

Text('Hello')
  .redText()
```

**文档参考:** `docs/state-management/arkts-style.md`

## 常用模式

**带生命周期的自定义组件:**
```typescript
@ComponentV2
struct CustomComponent {
  @Local count: number = 0

  aboutToAppear() {
    console.log('Component will appear')
  }

  aboutToDisappear() {
    console.log('Component will disappear')
  }

  build() {
    Text(`Count: ${this.count}`)
  }
}
```

**@Builder (可复用 UI 片段):**
```typescript
@Builder
function TitleBar(title: string) {
  Row() {
    Text(title)
      .fontSize(20)
      .fontWeight(FontWeight.Bold)
  }
  .width('100%')
  .padding(16)
}

// 使用
Column() {
  TitleBar({ title: 'My Page' })
}
```

**文档参考:** `docs/state-management/arkts-builder.md`

## 问题排查

| 症状 | 常见原因 | 解决方法 |
|---------|--------------|-----|
| 状态变化不更新 UI | 缺少装饰器 | 添加 `@Local` (V2) 或 `@State` (V1) |
| 子组件未接收更新 | 使用单向而非双向绑定 | 添加 `@Event` 回调 (V2) 或使用 `@Link` (V1) |
| 嵌套对象不响应 | 缺少深度观察 | 添加 `@ObservedV2`/`@Trace` (V2) 或 `@Observed`/`@ObjectLink` (V1) |
| 不必要的重渲染 | 本地状态中有大对象 | 对不可变属性使用 `@Param` |
| ForEach 渲染问题 | 缺少唯一键 | 始终提供唯一键生成器 |
| 导航不工作 | 使用 Router 而非 Navigation | 使用 `NavPathStack` API |
| 对话框不显示 | 缺少 UI 上下文 | 使用 `getUIContext().openCustomDialog()` |

**文档参考:**
- V2 状态管理: `docs/state-management/arkts-mvvm-V2.md`
- V1 状态管理: `docs/state-management/arkts-mvvm.md`

## 重要提示

- **始终提供唯一键** 给 `ForEach` 以避免渲染问题
- **新项目使用 V2 状态管理** (`@Local`, `@Param`)
- **优先使用 Navigation** 而非 Router 进行页面路由
- **尽可能使用 `$$` 语法** 简化双向绑定
- **大数据集使用 LazyForEach** (> 1000 项)
- **在不同屏幕尺寸上测试** 使用媒体查询

## 更多参考

**官方文档:** `docs-OpenHarmony-v6.0-Release/zh-cn/application-dev/ui/`

**本地快速参考:** `docs/`

**核心文档:**
- UI 概览: `docs/overview/arkts-ui-development-overview.md`
- 状态管理: `docs/state-management/arkts-state-management-overview.md`
- 布局开发: `docs/layout/arkts-layout-development-overview.md`
- 组件库: `docs/components/arkts-common-components-text-display.md` 及相关文件
- 导航: `docs/navigation/arkts-navigation-navigation.md`
- 动画: `docs/animation/arkts-attribute-animation-overview.md`

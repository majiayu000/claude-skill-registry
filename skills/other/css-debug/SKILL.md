---
name: css-debug
description: Use this skill to diagnose CSS and frontend layout issues such as positioning, overflow clipping, Tailwind class conflicts, z-index stacking, and React rendering visibility problems.
metadata:
  command-name: css-debug
  user-invocable: "true"
---

# CSS Debug Skill

<command-name>css-debug</command-name>
<user-invocable>true</user-invocable>

## 使用场景

当用户遇到以下问题时使用此 skill：
- CSS 定位问题（元素位置不正确、被裁剪、溢出等）
- React 组件渲染问题
- Tailwind CSS 类不生效
- 绝对定位/相对定位问题
- Flexbox/Grid 布局问题
- z-index 层叠问题

## 调试步骤

### 1. 收集信息

首先向用户询问或获取：
- 浏览器开发者工具中的 HTML 结构
- 相关元素的 computed styles
- 父容器的 CSS 属性（特别是 position、overflow、display）
- 截图（如果有的话）

### 2. 常见问题检查清单

#### 绝对定位内容被裁剪
```
问题：position: absolute 的元素被父容器裁剪
检查：
- [ ] 父容器是否有 overflow: hidden 或 overflow: auto
- [ ] 祖先容器是否有 overflow: hidden
- [ ] 父容器是否设置了 position: relative
- [ ] 元素的 top/left/right/bottom 值是否超出父容器

解决方案：
1. 将 overflow: hidden 改为 overflow: visible
2. 或将绝对定位元素移到更外层的容器
3. 或使用 fixed 定位（相对于视口）
```

#### 元素位置偏移
```
问题：元素位置与预期不符
检查：
- [ ] positionX/positionY 或 left/top 值是否正确
- [ ] 最近的 position: relative 祖先是哪个
- [ ] 是否有 margin/padding 影响
- [ ] transform 是否影响定位上下文

解决方案：
1. 确认定位参考点是正确的祖先元素
2. 检查 CSS 单位（px vs % vs rem）
3. 使用浏览器检查器的"元素选择"功能定位问题
```

#### 内容不显示
```
问题：React 组件渲染但内容不可见
检查：
- [ ] 元素是否有 width/height（可能为 0）
- [ ] opacity 是否为 0
- [ ] visibility 是否为 hidden
- [ ] display 是否为 none
- [ ] z-index 是否被其他元素遮挡
- [ ] color 是否与背景色相同

解决方案：
1. 在开发者工具中检查 Computed 面板
2. 临时添加边框或背景色调试：border: 1px solid red
3. 检查条件渲染逻辑
```

#### Tailwind 类不生效
```
问题：Tailwind CSS 类没有应用
检查：
- [ ] 类名拼写是否正确
- [ ] 是否被更高优先级的样式覆盖
- [ ] 动态类名是否正确生成（字符串拼接问题）
- [ ] tailwind.config.js 中 content 配置是否包含该文件

解决方案：
1. 使用 !important 临时测试：!overflow-visible
2. 检查 className 是否正确传递
3. 使用内联 style 作为备选方案
```

### 3. 浏览器调试命令

在浏览器控制台运行：

```javascript
// 高亮所有绝对定位元素
document.querySelectorAll('[style*="position: absolute"]').forEach(el => {
  el.style.outline = '2px solid red';
  console.log(el, getComputedStyle(el));
});

// 查找 overflow: hidden 的容器
document.querySelectorAll('*').forEach(el => {
  const style = getComputedStyle(el);
  if (style.overflow === 'hidden' || style.overflowX === 'hidden' || style.overflowY === 'hidden') {
    el.style.outline = '2px dashed blue';
    console.log('overflow-hidden:', el);
  }
});

// 检查元素的完整 computed 样式
const el = document.querySelector('.your-selector');
console.table({
  position: getComputedStyle(el).position,
  overflow: getComputedStyle(el).overflow,
  display: getComputedStyle(el).display,
  width: getComputedStyle(el).width,
  height: getComputedStyle(el).height,
  top: getComputedStyle(el).top,
  left: getComputedStyle(el).left,
});

// 查找定位祖先
function findPositionedAncestor(el) {
  let current = el.parentElement;
  while (current) {
    const position = getComputedStyle(current).position;
    if (position !== 'static') {
      console.log('Positioned ancestor:', current, 'position:', position);
      return current;
    }
    current = current.parentElement;
  }
  console.log('No positioned ancestor found, using viewport');
  return null;
}
findPositionedAncestor(document.querySelector('.your-selector'));
```

### 4. React DevTools 检查

1. 打开 React DevTools
2. 选择问题组件
3. 检查：
   - props 是否正确传递
   - state 是否包含预期数据
   - 条件渲染的条件是否满足

### 5. 常用修复模式

#### 修复绝对定位被裁剪

```tsx
// 问题代码
<div className="relative overflow-hidden">
  <div style={{ position: 'absolute', top: 200, left: 100 }}>
    被裁剪的内容
  </div>
</div>

// 解决方案 1: 移除 overflow-hidden
<div className="relative overflow-visible">
  ...
</div>

// 解决方案 2: 条件性 overflow
const hasAbsoluteContent = blocks.some(b => b.props?.positionX !== undefined);
<div className={`relative ${hasAbsoluteContent ? '' : 'overflow-hidden'}`}>
  ...
</div>

// 解决方案 3: 分离容器
<div className="relative">
  <div className="overflow-hidden">
    {/* 需要裁剪的内容 */}
  </div>
  <div className="absolute-content-wrapper">
    {/* 绝对定位内容 */}
  </div>
</div>
```

## 输出格式

分析完成后，提供：

1. **问题诊断**：明确说明是什么导致了问题
2. **原因分析**：解释 CSS 机制和为什么会发生这种情况
3. **解决方案**：提供具体的代码修改建议
4. **验证步骤**：告诉用户如何验证修复是否有效

## 示例对话

用户：我的绝对定位元素被裁剪了

Claude：
1. 请在浏览器中运行以下命令查找 overflow:hidden 的容器：
   ```javascript
   document.querySelectorAll('*').forEach(el => {
     const style = getComputedStyle(el);
     if (style.overflow === 'hidden') {
       el.style.outline = '2px dashed blue';
       console.log('overflow-hidden:', el);
     }
   });
   ```
2. 请告诉我哪些容器被标记出来了
3. 同时，请检查绝对定位元素的父容器是否有 `position: relative`

---
name: vue-best-practices
description: Vue 3 / Vue.js 在 TypeScript、vue-tsc、Volar 下的最佳实践。用于编写、审查或重构 Vue 组件时确保正确类型模式。触发场景：Vue 组件、props 提取、包装组件、模板类型检查、Volar 配置等。
license: MIT
---

# Vue 最佳实践

Vue 3 与 Vue.js 在 TypeScript、vue-tsc、Volar 下的最佳实践，用于编写、审查或重构 Vue 组件时保证正确的类型与工具链用法。

---

## 能力规则

| 规则 | 关键词 | 说明 |
|------|----------|-------------|
| extract-component-props | get props type、wrapper component、extend props、inherit props、ComponentProps | 从 .vue 组件提取类型 |
| vue-tsc-strict-templates | undefined component、template error、strictTemplates | 在模板中捕获未定义组件 |
| fallthrough-attributes | fallthrough、$attrs、wrapper component | 透传属性的类型检查 |
| strict-css-modules | css modules、$style、typo | 捕获 CSS 模块类名拼写错误 |
| data-attributes-config | data-*、strictTemplates、attribute | 允许 data-* 属性 |
| volar-3-breaking-changes | volar、vue-language-server、editor | 修复 Volar 3.0 升级问题 |
| module-resolution-bundler | cannot find module、@vue/tsconfig、moduleResolution | 修复模块解析错误 |
| define-model-update-event | defineModel、update event、undefined | 修复 model 更新错误 |
| with-defaults-union-types | withDefaults、union type、default | 修复联合类型默认值 |
| deep-watch-numeric | watch、deep、array、Vue 3.5 | 高效数组监听 |
| vue-directive-comments | @vue-ignore、@vue-skip、template | 控制模板类型检查 |
| vue-router-typed-params | route params、typed router、unplugin | 修复路由参数类型 |

## 效率规则

| 规则 | 关键词 | 说明 |
|------|----------|-------------|
| hmr-vue-ssr | hmr、ssr、hot reload | 修复 SSR 应用中的 HMR |
| pinia-store-mocking | pinia、mock、vitest、store | 模拟 Pinia store |

---

## 参考

- [Vue Language Tools](https://github.com/vuejs/language-tools)
- [vue-component-type-helpers](https://github.com/vuejs/language-tools/tree/master/packages/component-type-helpers)
- [Vue 3 文档](https://vuejs.org/)

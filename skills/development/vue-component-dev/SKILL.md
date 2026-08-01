---
name: vue-component-dev
description: Develop Vue 3 components (.vue files) with Pinia state management and
  ECharts charts. Use when creating/modifying .vue components, configuring stores,
  integrating charts, debugging reactivity, handlin
---

---
name: vue-component-dev
description: Develop Vue 3 components (.vue files) with Pinia state management and ECharts charts. Use when creating/modifying .vue components, configuring stores, integrating charts, debugging reactivity, handling Props/Emits, or optimizing performance. Keywords: Vue 3, Composition API, script setup, Pinia, ECharts, KpiCard, FilterPanel, Dashboard, computed, watch, responsive layout, eye-care colors.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Vue 3 组件开发规范

本 Skill 为**车险签单数据分析平台**的前端组件开发提供标准化指导。

---

## 📋 快速入门

### 项目技术栈
- **Vue 3.5+** - Composition API + `<script setup>` 语法
- **Vite 5** - 极速构建工具,HMR 热更新
- **Pinia 2.3+** - 官方推荐状态管理
- **ECharts 5.6+** - 数据可视化图表库
- **Axios 1.6+** - HTTP 客户端
- **护眼配色系统** - 主蓝 #5B8DEF / 次灰 #8B95A5 / 浅灰 #C5CAD3

### 文件位置约定
```
frontend/src/
├── components/
│   ├── common/              # 通用组件 (Toast, Loading, Button)
│   └── dashboard/           # 业务组件 (KpiCard, ChartView, FilterPanel)
├── stores/                  # Pinia 状态管理 (app.js, filter.js, data.js)
├── services/                # API 服务层 (api.js)
├── assets/styles/           # 样式系统 (variables.css, global.css)
└── App.vue                  # 根组件
```

### 核心开发流程
1. 使用 **标准组件模板** (见下文)
2. **PascalCase 命名** 组件文件 (如 `KpiCard.vue`)
3. Props/Emits 使用 **类型声明**
4. 样式使用 **scoped + CSS 变量**
5. 状态管理优先使用 **Pinia Store**

---

## 🧩 标准组件模板

```vue
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useDataStore } from '@/stores/data'

// Props 定义
const props = defineProps({
  title: { type: String, required: true },
  value: { type: Number, default: 0 },
  loading: { type: Boolean, default: false }
})

// Emits 定义
const emit = defineEmits(['refresh', 'click'])

// 响应式状态
const hovering = ref(false)

// Store 引用
const dataStore = useDataStore()

// 计算属性
const displayValue = computed(() => {
  return (props.value / 10000).toFixed(1) + '万'
})

// 方法
const handleRefresh = () => {
  emit('refresh')
}

// 生命周期
onMounted(() => {
  console.log('[Component] Mounted:', props.title)
})
</script>

<template>
  <div class="custom-component" @mouseenter="hovering = true" @mouseleave="hovering = false">
    <div class="custom-component__header">
      <h3 class="custom-component__title">{{ title }}</h3>
      <button class="custom-component__btn" @click="handleRefresh" :disabled="loading">
        刷新
      </button>
    </div>

    <div class="custom-component__body">
      <span class="value" @click="emit('click')">{{ displayValue }}</span>
      <div v-if="loading" class="custom-component__loading">加载中...</div>
    </div>

    <div class="custom-component__footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<style scoped>
.custom-component {
  padding: var(--space-4);
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.custom-component:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.custom-component__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-3);
}

.custom-component__title {
  font-size: var(--text-base);
  font-weight: 500;
  color: #374151;
}

.custom-component__btn {
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
  color: var(--color-d);
  background: transparent;
  border: 1px solid var(--color-d);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.custom-component__btn:hover {
  background: var(--color-d);
  color: #fff;
}

.value {
  font-size: var(--text-2xl);
  font-weight: 600;
  cursor: pointer;
}

@media (max-width: 768px) {
  .custom-component {
    padding: var(--space-3);
  }
  .value {
    font-size: var(--text-xl);
  }
}
</style>
```

---

## 🔄 组件通信决策树

### Props - 父传子数据
```vue
<!-- Parent.vue -->
<KpiCard :value="premiumData" :trend="trendType" :loading="isLoading" />

<!-- Child: KpiCard.vue -->
<script setup>
const props = defineProps({
  value: { type: Number, required: true },
  trend: { type: String, default: 'flat' },
  loading: { type: Boolean, default: false }
})
</script>
```

**使用时机**: 父组件拥有数据,子组件只负责展示

### Emits - 子通知父事件
```vue
<!-- Child: FilterPanel.vue -->
<script setup>
const emit = defineEmits(['filter-change', 'clear'])

const handleApply = () => {
  emit('filter-change', { 三级机构: '成都' })
}
</script>

<!-- Parent: Dashboard.vue -->
<FilterPanel @filter-change="onFilterChange" @clear="onClear" />
```

**使用时机**: 子组件需要通知父组件用户操作

### Pinia Store - 跨组件共享状态
```javascript
// stores/data.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useDataStore = defineStore('data', () => {
  const kpiData = ref(null)

  const fetchKpiData = async () => {
    const response = await apiClient.post('/api/kpi-windows')
    kpiData.value = response.data
  }

  return { kpiData, fetchKpiData }
})

// 在任意组件中使用
<script setup>
import { computed } from 'vue'
import { useDataStore } from '@/stores/data'

const dataStore = useDataStore()
const kpiData = computed(() => dataStore.kpiData)  // ✅ 保持响应式
</script>
```

**使用时机**:
- 多个组件需要访问同一份数据
- 数据需要跨层级传递
- 需要全局状态管理

### 反模式警告

**❌ 错误 1: Prop Drilling (超过3层)**
```vue
<!-- 应该使用 Store 而非层层传递 -->
<GrandParent :data="data">
  <Parent :data="data">
    <Child :data="data" />
  </Parent>
</GrandParent>
```

**❌ 错误 2: 直接修改 Props**
```vue
<script setup>
const props = defineProps({ value: Number })
props.value = 100 // 错误!Props 是只读的

// ✅ 正确:使用本地状态 + Emit
const localValue = ref(props.value)
const emit = defineEmits(['update:value'])
</script>
```

**❌ 错误 3: 解构 Store 丢失响应式**
```javascript
const { kpiData } = useDataStore()  // ❌ 丢失响应式

// ✅ 正确
const dataStore = useDataStore()
const kpiData = computed(() => dataStore.kpiData)
```

---

## 🗂️ Pinia Store 使用规范

### 三个核心 Store

#### 1. appStore (`stores/app.js`)
**职责**: 全局 UI 状态和应用配置

```javascript
export const useAppStore = defineStore('app', () => {
  const loading = ref(false)
  const selectedDate = ref(null)
  const currentMetric = ref('premium') // 'premium' | 'count'

  const setLoading = (value) => {
    loading.value = value
  }

  return { loading, selectedDate, currentMetric, setLoading }
})
```

**使用场景**: 全局 loading、日期选择、指标切换

#### 2. filterStore (`stores/filter.js`)
**职责**: 筛选器状态管理

```javascript
export const useFilterStore = defineStore('filter', () => {
  const filterOptions = ref({})      // 所有可选项
  const activeFilters = ref({})      // 当前已选筛选条件

  const applyFilter = (key, value) => {
    activeFilters.value[key] = value
  }

  return { filterOptions, activeFilters, applyFilter }
})
```

**使用场景**: 筛选面板状态、筛选条件管理

#### 3. dataStore (`stores/data.js`)
**职责**: 业务数据管理和 API 调用

```javascript
export const useDataStore = defineStore('data', () => {
  const kpiData = ref(null)
  const appStore = useAppStore()

  const fetchKpiData = async () => {
    appStore.setLoading(true)
    try {
      const response = await apiClient.post('/api/kpi-windows')
      kpiData.value = response.data
    } catch (error) {
      console.error('Failed to fetch KPI data:', error)
    } finally {
      appStore.setLoading(false)
    }
  }

  return { kpiData, fetchKpiData }
})
```

**使用场景**: 所有业务数据的获取和更新

### Store 使用规范

**规范 1**: Setup 语法统一
```javascript
// ✅ 正确 - Composition API 风格
export const useDataStore = defineStore('data', () => {
  const state = ref(null)
  return { state }
})

// ❌ 错误 - 不使用 Options API
export const useDataStore = defineStore('data', {
  state: () => ({ value: null })
})
```

**规范 2**: Store 依赖关系 (单向)
```javascript
// ✅ 正确: dataStore 可以依赖 appStore
import { useAppStore } from './app'
export const useDataStore = defineStore('data', () => {
  const appStore = useAppStore()
})

// ❌ 错误: appStore 不能依赖 dataStore (循环依赖)
```

**规范 3**: 异步操作必须在 Actions 中
```javascript
// ✅ 正确:在 Store Action 中调用 API
export const useDataStore = defineStore('data', () => {
  const fetchData = async () => {
    const response = await apiClient.get('/api/data')
    data.value = response.data
  }
  return { fetchData }
})

// ❌ 错误:在组件中直接调用 API
```

---

## 📊 ECharts 图表开发规范

### 标准图表组件

```vue
<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  data: { type: Object, required: true },
  metric: { type: String, default: 'premium' }
})

const chartRef = ref(null)
let chartInstance = null

onMounted(() => {
  chartInstance = echarts.init(chartRef.value)
  updateChart()
  window.addEventListener('resize', handleResize)
})

const updateChart = () => {
  if (!chartInstance || !props.data) return

  const option = {
    color: ['#5B8DEF', '#8B95A5', '#C5CAD3'],  // 护眼配色
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#E5E7EB'
    },
    xAxis: {
      type: 'category',
      data: props.data.x_axis || []
    },
    yAxis: { type: 'value' },
    series: (props.data.series || []).map(item => ({
      name: item.name,
      type: 'bar',
      data: item.data
    }))
  }

  chartInstance.setOption(option, true)
}

watch(() => props.data, updateChart, { deep: true })

const handleResize = () => {
  chartInstance?.resize()
}

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>

<template>
  <div class="chart-container">
    <div ref="chartRef" class="chart"></div>
  </div>
</template>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  min-height: 400px; /* 必须设置高度 */
}

.chart {
  width: 100%;
  height: 100%;
}
</style>
```

### ECharts 关键注意事项

**1. 容器高度 (常见坑)**
```vue
<!-- ❌ 错误:无高度 -->
<div ref="chartRef"></div>

<!-- ✅ 正确:设置高度 -->
<div ref="chartRef" style="height: 400px;"></div>
```

**2. 响应式处理**
```javascript
onMounted(() => {
  window.addEventListener('resize', () => {
    chartInstance?.resize()
  })
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()  // 防止内存泄漏
})
```

**3. 护眼配色 (强制)**
```javascript
// ✅ 必须使用项目配色
color: ['#5B8DEF', '#8B95A5', '#C5CAD3']

// ❌ 禁止使用 ECharts 默认配色
```

**4. 数据更新**
```javascript
// ✅ 正确:使用 setOption 的第二个参数 true (完全替换)
chartInstance.setOption(option, true)
```

---

## 🎨 护眼配色系统

### 核心颜色 (必须使用 CSS 变量)

```css
/* 周期对比颜色 */
--color-d: #5B8DEF;        /* 主蓝色 - 最新周 (D) */
--color-d7: #8B95A5;       /* 次灰色 - 上周 (D-7) */
--color-d14: #C5CAD3;      /* 浅灰色 - 前周 (D-14) */

/* 趋势指示颜色 */
--color-success: #52C41A;  /* 上升/正向 */
--color-danger: #F5222D;   /* 下降/警示 */
--color-warning: #FAAD14;  /* 预警 */

/* 中性色 */
--color-text-primary: #374151;
--color-text-secondary: #6B7280;
--color-border: #E5E7EB;

/* 间距系统 (4px 基准) */
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;

/* 字体系统 */
--text-sm: 14px;
--text-base: 16px;
--text-lg: 20px;
--text-xl: 24px;
--text-2xl: 30px;
```

### 响应式断点

```css
/* 手机端 */
@media (max-width: 768px) {
  .kpi-card {
    flex-direction: column;
  }
}

/* 平板端 */
@media (min-width: 769px) and (max-width: 1024px) {
  .dashboard {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* 桌面端 */
@media (min-width: 1025px) {
  .dashboard {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

### 样式规范

**规范 1: 使用 CSS 变量**
```css
/* ✅ 正确 */
.text {
  color: var(--color-text-primary);
  font-size: var(--text-base);
}

/* ❌ 错误:硬编码 */
.text {
  color: #374151;
  font-size: 16px;
}
```

**规范 2: BEM 命名**
```css
/* ✅ 正确 */
.kpi-card { }
.kpi-card__header { }
.kpi-card__title { }
.kpi-card__value--up { }

/* ❌ 错误 */
.card { }
.cardHeader { }
```

**规范 3: Scoped 样式**
```vue
<!-- ✅ 正确 -->
<style scoped>
.kpi-card {
  /* 样式只作用于当前组件 */
}
</style>

<!-- 穿透子组件时使用 :deep() -->
<style scoped>
.parent :deep(.child) {
  color: red;
}
</style>
```

---

## 📁 已有组件清单

### 业务组件 (`components/dashboard/`)

#### KpiCard.vue
**功能**: KPI 卡片 (签单保费、件数、手续费、目标差距)
**Props**:
```typescript
{
  title: string
  value: number
  trend: 'up' | 'down' | 'flat'
  day7Value: number
  day30Value: number
}
```
**Emits**: `['refresh']`
**位置**: [frontend/src/components/dashboard/KpiCard.vue](frontend/src/components/dashboard/KpiCard.vue)

#### ChartView.vue
**功能**: ECharts 周对比图表容器
**Props**:
```typescript
{
  data: {
    x_axis: string[]
    series: Array<{ name: string; data: number[]; code: string }>
  }
  metric: 'premium' | 'count'
}
```
**位置**: [frontend/src/components/dashboard/ChartView.vue](frontend/src/components/dashboard/ChartView.vue)

#### FilterPanel.vue
**功能**: 筛选面板 (8 个维度)
**Props**:
```typescript
{
  filterOptions: {
    '三级机构': string[]
    '团队': string[]
    '是否续保': string[]
    // ...
  }
}
```
**Emits**: `['filter-change', 'clear']`
**位置**: [frontend/src/components/dashboard/FilterPanel.vue](frontend/src/components/dashboard/FilterPanel.vue)

### 布局组件

#### Header.vue
**功能**: 顶部导航栏
**位置**: [frontend/src/components/Header.vue](frontend/src/components/Header.vue)

#### Dashboard.vue
**功能**: 主仪表板容器 (协调所有子组件)
**位置**: [frontend/src/views/Dashboard.vue](frontend/src/views/Dashboard.vue)

---

## 🔌 API 调用规范

### API 服务层位置
`frontend/src/services/api.js`

### 核心 API 端点

```javascript
import apiClient from '@/services/api'

// 1. 刷新数据
await apiClient.post('/api/refresh')

// 2. 获取 KPI 三口径数据
const kpi = await apiClient.post('/api/kpi-windows', {
  date: '2025-11-07',
  filters: { '三级机构': '成都' }
})

// 3. 获取周对比数据
const chart = await apiClient.post('/api/week-comparison', {
  metric: 'premium',
  filters: { '是否新能源': '是' }
})

// 4. 获取筛选器选项
const options = await apiClient.get('/api/filter-options')
```

### 错误处理规范

```javascript
// ✅ 正确 (在 Store 中)
export const useDataStore = defineStore('data', () => {
  const fetchKpiData = async () => {
    try {
      const response = await apiClient.post('/api/kpi-windows')
      kpiData.value = response.data
    } catch (error) {
      console.error('Failed to fetch KPI data:', error)
    }
  }
  return { fetchKpiData }
})
```

---

## 🔍 故障排查指南

### 问题 1: ECharts 图表不显示

**症状**: 图表容器空白,无错误

**解决方案**:
```vue
<template>
  <div class="chart-container">
    <div ref="chartRef" class="chart"></div>
  </div>
</template>

<style scoped>
.chart-container {
  height: 450px; /* 必须明确高度 */
}
.chart {
  width: 100%;
  height: 100%;
}
</style>
```

### 问题 2: Store 数据不响应

**原因**: 直接解构 Store 会丢失响应式

**解决方案**:
```javascript
// ❌ 错误
const { kpiData } = useDataStore()

// ✅ 正确
const dataStore = useDataStore()
const kpiData = computed(() => dataStore.kpiData)
```

### 问题 3: 筛选不生效

**排查步骤**:
1. 检查 `filterStore.activeFilters` 是否更新
2. 检查 `dataStore.fetchChartData` 是否被调用
3. 检查网络请求是否发送 (DevTools Network)

**解决方案**:
```javascript
async function handleApplyFilters() {
  filterStore.applyFilters(localFilters.value)
  await dataStore.refreshChartData()
}
```

---

## ✅ 检查清单

在提交组件代码前,确保:

- [ ] 使用了标准组件模板结构
- [ ] Props 和 Emits 有清晰的类型定义
- [ ] 使用 Pinia Store 而非 Props Drilling
- [ ] 样式使用 scoped + CSS 变量
- [ ] 遵循 BEM 命名规范
- [ ] ECharts 使用护眼配色
- [ ] 组件在手机/平板/桌面端都能正常显示
- [ ] API 调用在 Store Action 中
- [ ] 没有硬编码颜色值
- [ ] 没有内联样式 (除非动态计算)

---

## 📚 进阶参考

**需要更详细的文档时,参考以下支持文件**:

- **[ADVANCED.md](ADVANCED.md)** - 高级模式、实际组件实现参考
- **[EXAMPLES.md](EXAMPLES.md)** - 完整组件代码示例

**相关文档**:
- [frontend/src/views/Dashboard.vue](../../frontend/src/views/Dashboard.vue) - 主仪表板组件
- [frontend/src/stores/data.js](../../frontend/src/stores/data.js) - 数据状态管理
- [docs/THEME_SYSTEM.md](../../docs/THEME_SYSTEM.md) - 主题系统文档

**最后更新**: 2025-11-08
**维护者**: Claude Code AI Assistant
**版本**: 4.0 (精简版,符合 Claude Skills 最佳实践)

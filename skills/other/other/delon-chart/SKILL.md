---
name: delon-chart
description: '@delon/chart skill - G2Plot enterprise charting components with @delon/chart. For ng-events construction site progress tracking system.'
---

# @delon/chart - Enterprise Chart Components

Trigger patterns: "chart", "graph", "visualization", "@delon/chart", "G2Plot", "G2"

## Overview

@delon/chart provides enterprise-grade charting components built on G2Plot for data visualization in ng-alain applications.

**Package**: @delon/chart@20.1.0  
**Dependencies**: @ant-design/charts (G2Plot wrapper)

## Core Components

### 1. chart-card - Chart Card Container

```typescript
import { ChartCardComponent } from '@delon/chart/chart-card';

<chart-card 
  [title]="'進度統計'" 
  [total]="totalTasks()"
  [action]="action"
  [footer]="footer"
>
  <trend flag="up" style="margin-right: 16px;">
    <span>週成長</span><span>12%</span>
  </trend>
  <trend flag="down">
    <span>日成長</span><span>11%</span>
  </trend>
</chart-card>
```

**Features**:
- Title, total, action, footer slots
- Integrated trend indicators
- Responsive layout
- Loading states

### 2. g2-bar - Bar Charts

```typescript
import { G2BarComponent } from '@delon/chart/bar';

@Component({
  standalone: true,
  imports: [G2BarComponent],
  template: `
    <g2-bar 
      [data]="barData()"
      [height]="300"
      [padding]="[20, 40, 50, 40]"
    />
  `
})
export class TaskChartComponent {
  barData = signal([
    { x: '待辦', y: 12 },
    { x: '進行中', y: 8 },
    { x: '已完成', y: 25 }
  ]);
}
```

**Options**:
- `height` (number) - Chart height in pixels
- `padding` (number[]) - [top, right, bottom, left]
- `color` (string) - Bar color
- `autoLabel` (boolean) - Auto label positioning

### 3. g2-mini-bar - Mini Bar Charts (Sparkline)

```typescript
<g2-mini-bar 
  [data]="miniData()"
  [height]="50"
  [color]="'#1890ff'"
/>

miniData = signal([
  { x: '2024-01', y: 5 },
  { x: '2024-02', y: 8 },
  { x: '2024-03', y: 12 }
]);
```

### 4. g2-pie - Pie/Donut Charts

```typescript
import { G2PieComponent } from '@delon/chart/pie';

<g2-pie
  [data]="pieData()"
  [height]="300"
  [hasLegend]="true"
  [subTitle]="'總任務數'"
  [total]="totalTasks()"
  [inner]="0.8"
/>

pieData = signal([
  { x: '待辦', y: 12 },
  { x: '進行中', y: 8 },
  { x: '已完成', y: 25 }
]);
```

**Options**:
- `inner` (number) - 0-1, 0=pie, >0=donut
- `hasLegend` (boolean) - Show legend
- `subTitle` (string) - Center subtitle
- `total` (string) - Center total display

### 5. g2-radar - Radar Charts

```typescript
import { G2RadarComponent } from '@delon/chart/radar';

<g2-radar 
  [data]="radarData()"
  [height]="300"
  [hasLegend]="true"
/>

radarData = signal([
  { name: '設計', label: '計畫', value: 85 },
  { name: '設計', label: '執行', value: 70 },
  { name: '開發', label: '計畫', value: 90 },
  { name: '開發', label: '執行', value: 80 }
]);
```

### 6. timeline - Timeline Charts

```typescript
import { TimelineComponent } from '@delon/chart/timeline';

<timeline 
  [data]="timelineData()"
  [title]="'施工進度'"
  [maxAxis]="5"
/>

timelineData = signal([
  { x: new Date('2024-01-01'), y1: 10, y2: 20 },
  { x: new Date('2024-02-01'), y1: 15, y2: 25 },
  { x: new Date('2024-03-01'), y1: 20, y2: 30 }
]);
```

### 7. trend - Trend Indicator

```typescript
import { TrendComponent } from '@delon/chart/trend';

<trend flag="up">
  <span>週成長</span>
  <span class="pl-sm">12%</span>
</trend>

<trend flag="down" colorful="false">
  <span>日成長</span>
  <span class="pl-sm">11%</span>
</trend>
```

**Flags**: `up` | `down`  
**Colorful**: `true` (green/red) | `false` (gray)

## Real-World Examples

### Dashboard Stats with Charts

```typescript
import { Component, signal, computed, inject } from '@angular/core';
import { ChartCardComponent } from '@delon/chart/chart-card';
import { G2BarComponent } from '@delon/chart/bar';
import { G2PieComponent } from '@delon/chart/pie';
import { TrendComponent } from '@delon/chart/trend';
import { TaskService } from '@core/services/task.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    ChartCardComponent,
    G2BarComponent,
    G2PieComponent,
    TrendComponent
  ],
  template: `
    <div nz-row [nzGutter]="24">
      <div nz-col [nzXl]="6" [nzLg]="12" [nzMd]="12" [nzSm]="24">
        <chart-card 
          [title]="'總任務數'" 
          [total]="totalTasks()"
          contentHeight="46px"
        >
          <trend flag="up" style="margin-right: 16px;">
            <span>週成長</span><span>{{ weeklyGrowth() }}%</span>
          </trend>
        </chart-card>
      </div>
      
      <div nz-col [nzSpan]="24">
        <nz-card [nzTitle]="'任務狀態分佈'">
          <g2-bar 
            [data]="taskStatusData()"
            [height]="300"
            [padding]="[20, 40, 50, 60]"
          />
        </nz-card>
      </div>
      
      <div nz-col [nzSpan]="12">
        <nz-card [nzTitle]="'任務類型比例'">
          <g2-pie
            [data]="taskTypeData()"
            [height]="300"
            [hasLegend]="true"
            [inner]="0.6"
            [total]="totalTasks()"
          />
        </nz-card>
      </div>
    </div>
  `
})
export class DashboardComponent {
  private taskService = inject(TaskService);
  
  // Signals for reactive data
  tasks = this.taskService.tasks;
  
  totalTasks = computed(() => this.tasks().length);
  
  weeklyGrowth = computed(() => {
    // Calculate growth percentage
    const thisWeek = this.tasks().filter(t => 
      this.isThisWeek(t.createdAt)
    ).length;
    const lastWeek = this.tasks().filter(t => 
      this.isLastWeek(t.createdAt)
    ).length;
    
    return lastWeek > 0 ? 
      Math.round((thisWeek - lastWeek) / lastWeek * 100) : 0;
  });
  
  taskStatusData = computed(() => [
    { x: '待辦', y: this.tasks().filter(t => t.status === 'pending').length },
    { x: '進行中', y: this.tasks().filter(t => t.status === 'in-progress').length },
    { x: '已完成', y: this.tasks().filter(t => t.status === 'completed').length }
  ]);
  
  taskTypeData = computed(() => [
    { x: '設計', y: this.tasks().filter(t => t.type === 'design').length },
    { x: '開發', y: this.tasks().filter(t => t.type === 'development').length },
    { x: '測試', y: this.tasks().filter(t => t.type === 'testing').length }
  ]);
  
  private isThisWeek(date: Date): boolean {
    const now = new Date();
    const weekStart = new Date(now.setDate(now.getDate() - now.getDay()));
    return date >= weekStart;
  }
  
  private isLastWeek(date: Date): boolean {
    const now = new Date();
    const weekStart = new Date(now.setDate(now.getDate() - now.getDay() - 7));
    const weekEnd = new Date(now.setDate(now.getDate() - now.getDay()));
    return date >= weekStart && date < weekEnd;
  }
}
```

## Best Practices

### 1. Use Signals for Reactive Charts

✅ **DO**:
```typescript
chartData = computed(() => 
  this.tasks().map(t => ({ x: t.name, y: t.value }))
);
```

❌ **DON'T**:
```typescript
chartData: any[] = [];
ngOnInit() {
  this.taskService.getTasks().subscribe(tasks => {
    this.chartData = tasks.map(t => ({ x: t.name, y: t.value }));
  });
}
```

### 2. Responsive Chart Heights

✅ **DO**:
```typescript
@Component({
  template: `
    <g2-bar 
      [data]="data()"
      [height]="isMobile() ? 200 : 300"
    />
  `
})
```

### 3. Loading States

✅ **DO**:
```typescript
@if (loading()) {
  <nz-spin nzSimple />
} @else if (chartData().length > 0) {
  <g2-bar [data]="chartData()" />
} @else {
  <nz-empty nzNotFoundContent="沒有資料" />
}
```

## Performance Tips

1. **Data Transformation**: Transform data in computed signals, not in templates
2. **Chart Reuse**: Reuse chart components with different data props
3. **Lazy Loading**: Load chart module only when needed
4. **Height Optimization**: Use fixed heights for better performance
5. **Data Limits**: Limit chart data points (recommend < 100 for bar/pie)

## Integration Checklist

- [ ] Install @delon/chart@20.1.0
- [ ] Import chart components in standalone components
- [ ] Use signals for reactive chart data
- [ ] Handle loading and empty states
- [ ] Set responsive chart heights
- [ ] Add proper TypeScript types for chart data
- [ ] Test with empty/large datasets
- [ ] Optimize data transformation with computed()

## Anti-Patterns

❌ **Mutating Chart Data Directly**:
```typescript
this.chartData.push({ x: 'new', y: 10 }); // Won't trigger change detection
```

✅ **Use Signal Updates**:
```typescript
this.chartData.update(data => [...data, { x: 'new', y: 10 }]);
```

---

❌ **Complex Logic in Templates**:
```typescript
<g2-bar [data]="tasks.filter(t => t.status === 'completed').map(t => ({x: t.name, y: t.value}))" />
```

✅ **Use Computed Signals**:
```typescript
completedTasksData = computed(() => 
  this.tasks()
    .filter(t => t.status === 'completed')
    .map(t => ({ x: t.name, y: t.value }))
);
```

## Cross-References

- **ng-alain-component** - ST Table for data tables
- **delon-theme** - Page layout and theme customization
- **angular-component** - Signals and computed for reactive charts
- `.github/instructions/angular.instructions.md` - Angular 20 patterns

## Package Information

- **Version**: 20.1.0
- **Repository**: https://github.com/ng-alain/delon
- **Documentation**: https://ng-alain.com/chart

---

**Version**: 1.0  
**Created**: 2025-12-25  
**Maintainer**: ng-events(GigHub) Development Team

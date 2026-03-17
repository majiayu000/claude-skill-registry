---
name: react-typescript-development
description: 当用户要求React/TypeScript组件、Hooks、Ant Design、TanStack Query、Tauri前端联调或前端性能优化时使用。
---

# React TypeScript Development Skill

## 适用范围
- React 组件与 Hooks 开发
- Ant Design 表单与交互
- Tauri 前端命令调用与错误处理

## 关键规则（Critical Rules）
- 只使用 `frontend/src/bindings.ts` 的 `commands`
- 禁止 `console.*`，使用 `message.info/warning/error`
- 禁止 `as any`，用类型守卫或精确类型
- Hooks 仅在顶层调用，依赖完整
- 表格行高紧凑统一：默认 th/td padding 6px 10px、line-height 1.2；表格内 Tag 紧凑化

## 快速模板
### 命令调用（Result + ApiResponse）
```ts
import { commands } from '../bindings';
import { message } from 'antd';

export async function loadFactories(keyword: string | null) {
  const res = await commands.getAllFactories(keyword, null);
  if (res.status === 'error') {
    message.error(String(res.error));
    return [] as const;
  }
  const { success, data, error } = res.data;
  if (!success || !data) {
    message.error(error ?? '加载失败');
    return [] as const;
  }
  return data;
}
```

### Hook 规范
```ts
import { useEffect, useState } from 'react';
import type { Factory } from '../bindings';

export function useFactoryList(keyword: string | null) {
  const [items, setItems] = useState<Factory[]>([]);
  useEffect(() => {
    void loadFactories(keyword).then(setItems);
  }, [keyword]);
  return items;
}
```

## 性能建议
- 复杂计算用 `useMemo`
- 回调用 `useCallback` 固定引用
- 大列表使用 `react-window`

## 表单校验
- 使用 AntD `Form.Item` 规则与自定义校验函数
- 将错误提示直接反馈给用户

## 检查清单
- [ ] 无 `console.*` 与 `as any`
- [ ] 命令调用走 `commands`
- [ ] Hooks 规则与依赖正确
- [ ] 大列表已考虑虚拟滚动
- [ ] 表格行高与内边距保持紧凑统一
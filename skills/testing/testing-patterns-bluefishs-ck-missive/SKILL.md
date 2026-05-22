# 測試模式技能

> **技能名稱**: testing-patterns
> **觸發**: `測試模式`, `testing patterns`, `Vitest`, `Pytest`, `MSW`, `測試策略`
> **版本**: 1.0.0
> **分類**: project
> **更新日期**: 2026-01-22
> **用途**：測試策略和模式指南 - Vitest, Pytest, MSW
> **適用場景**：開發新功能、程式碼審查、重構

## 概述

專案的測試策略和模式指南。

## 測試框架

### 前端測試

- **Vitest** - 單元測試框架
- **React Testing Library** - 組件測試
- **MSW** - API Mock

### 後端測試

- **Jest** - 測試框架
- **Supertest** - API 測試

## 測試模式

### 1. 組件測試模式

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';

describe('ComponentName', () => {
  it('should render correctly', () => {
    render(<ComponentName />);
    expect(screen.getByText('Expected Text')).toBeInTheDocument();
  });

  it('should handle user interaction', async () => {
    const onSubmit = vi.fn();
    render(<ComponentName onSubmit={onSubmit} />);

    fireEvent.click(screen.getByRole('button'));
    expect(onSubmit).toHaveBeenCalled();
  });
});
```

### 2. Hook 測試模式

```typescript
import { renderHook, act } from '@testing-library/react';
import { useCustomHook } from './useCustomHook';

describe('useCustomHook', () => {
  it('should return initial state', () => {
    const { result } = renderHook(() => useCustomHook());
    expect(result.current.value).toBe(initialValue);
  });

  it('should update state', () => {
    const { result } = renderHook(() => useCustomHook());
    act(() => {
      result.current.setValue('new value');
    });
    expect(result.current.value).toBe('new value');
  });
});
```

### 3. API 測試模式

```typescript
import request from 'supertest';
import app from '../app';

describe('GET /api/v1/control-points', () => {
  it('should return control points list', async () => {
    const response = await request(app).get('/api/v1/control-points').expect(200);

    expect(response.body).toHaveProperty('data');
    expect(Array.isArray(response.body.data)).toBe(true);
  });
});
```

## 測試命名規範

- 描述應該清楚說明測試目的
- 使用 `should` 開頭描述預期行為
- 分組使用 `describe` 區塊

## 測試覆蓋目標

| 類型     | 目標覆蓋率 |
| -------- | ---------- |
| 單元測試 | 80%        |
| 集成測試 | 60%        |
| E2E 測試 | 關鍵路徑   |

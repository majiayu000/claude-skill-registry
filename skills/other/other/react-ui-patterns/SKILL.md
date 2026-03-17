---
name: React UI 模式技能
description: 提供 React 和 Ant Design 前端開發的 UI 模式最佳實踐
version: 1.0.0
category: react
triggers:
  - /react-ui-patterns
  - React 模式
  - UI 組件
updated: 2026-01-28
---

# React UI 模式技能

## 概述

CK_GPS 前端的 React 和 Ant Design 最佳實踐。

## 組件模式

### 1. 函數式組件結構

```typescript
import React, { useState, useEffect, useCallback } from 'react';
import { Button, Form, Input } from 'antd';
import type { FC } from 'react';

interface ComponentProps {
  initialValue?: string;
  onSubmit: (value: string) => void;
}

export const MyComponent: FC<ComponentProps> = ({
  initialValue = '',
  onSubmit
}) => {
  const [value, setValue] = useState(initialValue);
  const [loading, setLoading] = useState(false);

  const handleSubmit = useCallback(async () => {
    setLoading(true);
    try {
      await onSubmit(value);
    } finally {
      setLoading(false);
    }
  }, [value, onSubmit]);

  return (
    <Form onFinish={handleSubmit}>
      <Form.Item>
        <Input value={value} onChange={e => setValue(e.target.value)} />
      </Form.Item>
      <Button type="primary" htmlType="submit" loading={loading}>
        提交
      </Button>
    </Form>
  );
};
```

### 2. 自定義 Hook 模式

```typescript
import { useState, useEffect } from 'react';
import { message } from 'antd';

export function useControlPoints(cityCode: string) {
  const [data, setData] = useState<ControlPoint[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    if (!cityCode) return;

    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`/api/v1/control-points?city=${cityCode}`);
        const result = await response.json();
        setData(result.data);
      } catch (err) {
        setError(err as Error);
        message.error('載入失敗');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [cityCode]);

  return { data, loading, error };
}
```

### 3. 表格組件模式

```typescript
import { Table, Space, Button, Popconfirm } from 'antd';
import type { ColumnsType } from 'antd/es/table';

const columns: ColumnsType<ControlPoint> = [
  {
    title: '點號',
    dataIndex: 'point_no',
    key: 'point_no',
    sorter: (a, b) => a.point_no.localeCompare(b.point_no),
  },
  {
    title: '城市',
    dataIndex: 'city',
    key: 'city',
    filters: [
      { text: '基隆市', value: '基隆市' },
      { text: '台北市', value: '台北市' },
    ],
    onFilter: (value, record) => record.city === value,
  },
  {
    title: '操作',
    key: 'action',
    render: (_, record) => (
      <Space>
        <Button type="link" onClick={() => handleView(record)}>查看</Button>
        <Popconfirm title="確定刪除?" onConfirm={() => handleDelete(record.id)}>
          <Button type="link" danger>刪除</Button>
        </Popconfirm>
      </Space>
    ),
  },
];
```

## Ant Design 最佳實踐

### Form 表單

```typescript
import { Form, Input, Select, DatePicker } from 'antd';

const [form] = Form.useForm();

// 表單驗證
<Form
  form={form}
  layout="vertical"
  onFinish={handleSubmit}
  initialValues={{ city: '基隆市' }}
>
  <Form.Item
    name="point_no"
    label="點號"
    rules={[
      { required: true, message: '請輸入點號' },
      { pattern: /^[A-Z]\d{4}$/, message: '格式錯誤' }
    ]}
  >
    <Input placeholder="例: A1234" />
  </Form.Item>
</Form>
```

### 響應式佈局

```typescript
import { Row, Col } from 'antd';

<Row gutter={[16, 16]}>
  <Col xs={24} sm={12} md={8} lg={6}>
    {/* 響應式內容 */}
  </Col>
</Row>
```

## 效能優化

### 1. 避免不必要的重新渲染

```typescript
// 使用 React.memo
export const ExpensiveComponent = React.memo(({ data }) => {
  // 只有 data 改變時才重新渲染
  return <div>{/* 渲染邏輯 */}</div>;
});

// 使用 useMemo
const processedData = useMemo(() => {
  return expensiveComputation(data);
}, [data]);
```

### 2. 懶加載

```typescript
const MapComponent = React.lazy(() => import('./components/map/MapComponent'));

// 使用時
<Suspense fallback={<Spin />}>
  <MapComponent />
</Suspense>
```

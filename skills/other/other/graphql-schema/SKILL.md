---
name: graphql-schema
description: GraphQL查询、mutation和代码生成模式。在创建GraphQL操作、使用Apollo Client或生成类型时使用。
---

# GraphQL Schema 模式

## 核心规则

1. **从不内联`gql`字面量** - 创建`.gql`文件
2. **总是运行codegen** - 在创建/修改`.gql`文件后
3. **总是添加`onError`处理器** - 到mutation中
4. **使用生成的hook** - 永远不要手写Apollo hook

## 文件结构

```
src/
├── components/
│   └── ItemList/
│       ├── ItemList.tsx
│       ├── GetItems.gql           # Query定义
│       └── GetItems.generated.ts  # 自动生成（不要编辑）
└── graphql/
    └── mutations/
        └── CreateItem.gql         # 共享mutation
```

## 创建一个Query

### 第1步：创建.gql文件

```graphql
# src/components/ItemList/GetItems.gql
query GetItems($limit: Int, $offset: Int) {
  items(limit: $limit, offset: $offset) {
    id
    name
    description
    createdAt
  }
}
```

### 第2步：运行codegen

```bash
npm run gql:typegen
```

### 第3步：导入和使用生成的hook

```typescript
import { useGetItemsQuery } from './GetItems.generated';

const ItemList = () => {
  const { data, loading, error, refetch } = useGetItemsQuery({
    variables: { limit: 20, offset: 0 },
  });

  if (error) return <ErrorState error={error} onRetry={refetch} />;
  if (loading && !data) return <LoadingSkeleton />;
  if (!data?.items.length) return <EmptyState />;

  return <List items={data.items} />;
};
```

## 创建一个Mutation

### 第1步：创建.gql文件

```graphql
# src/graphql/mutations/CreateItem.gql
mutation CreateItem($input: CreateItemInput!) {
  createItem(input: $input) {
    id
    name
    description
  }
}
```

### 第2步：运行codegen

```bash
npm run gql:typegen
```

### 第3步：使用**必需的**错误处理

```typescript
import { useCreateItemMutation } from 'graphql/mutations/CreateItem.generated';

const CreateItemForm = () => {
  const [createItem, { loading }] = useCreateItemMutation({
    // 成功处理
    onCompleted: (data) => {
      toast.success({ title: '项目已创建' });
      navigation.goBack();
    },
    // 错误处理是必需的
    onError: (error) => {
      console.error('createItem failed:', error);
      toast.error({ title: '创建项目失败' });
    },
    // 缓存更新
    update: (cache, { data }) => {
      if (data?.createItem) {
        cache.modify({
          fields: {
            items: (existing = []) => [...existing, data.createItem],
          },
        });
      }
    },
  });

  return (
    <Button
      onPress={() => createItem({ variables: { input: formValues } })}
      isDisabled={!isValid || loading}
      isLoading={loading}
    >
      创建
    </Button>
  );
};
```

## Mutation UI 要求

**关键：每个mutation触发器必须：**

1. **在mutation期间被禁用** - 防止双击
2. **显示加载状态** - 视觉反馈
3. **有onError处理器** - 用户知道它失败了
4. **显示成功反馈** - 用户知道它成功了

```typescript
// 正确 - 完整的mutation模式
const [submit, { loading }] = useSubmitMutation({
  onError: (error) => {
    console.error('submit failed:', error);
    toast.error({ title: '保存失败' });
  },
  onCompleted: () => {
    toast.success({ title: '已保存' });
  },
});

<Button
  onPress={handleSubmit}
  isDisabled={!isValid || loading}
  isLoading={loading}
>
  提交
</Button>
```

## Query选项

### 获取策略

| 策略                | 使用场景                  |
| ------------------- | ------------------------- |
| `cache-first`       | 数据很少改变              |
| `cache-and-network` | 想要快速+新鲜数据（默认） |
| `network-only`      | 总是需要最新的            |
| `no-cache`          | 从不缓存（罕见）          |

### 常见选项

```typescript
useGetItemsQuery({
  variables: { id: itemId },

  // 获取策略
  fetchPolicy: "cache-and-network",

  // 在网络状态更改时重新渲染
  notifyOnNetworkStatusChange: true,

  // 如果条件不满足则跳过
  skip: !itemId,

  // 轮询更新
  pollInterval: 30000,
});
```

## 乐观更新

用于即时UI反馈：

```typescript
const [toggleFavorite] = useToggleFavoriteMutation({
  optimisticResponse: {
    toggleFavorite: {
      __typename: "Item",
      id: itemId,
      isFavorite: !currentState,
    },
  },
  onError: (error) => {
    // 回滚自动发生
    console.error("toggleFavorite failed:", error);
    toast.error({ title: "更新失败" });
  },
});
```

### 何时不使用乐观更新

- 可能因验证失败的操作
- 包含服务器生成值的操作
- 破坏性操作（删除）
- 影响其他用户的操作

## 片段

用于可重用的字段选择：

```graphql
# src/graphql/fragments/ItemFields.gql
fragment ItemFields on Item {
  id
  name
  description
  createdAt
  updatedAt
}
```

在queries中使用：

```graphql
query GetItems {
  items {
    ...ItemFields
  }
}
```

## 反面模式

```typescript
// 错误 - 内联gql
const GET_ITEMS = gql`
  query GetItems { items { id } }
`;

// 正确 - 使用.gql文件+生成的hook
import { useGetItemsQuery } from './GetItems.generated';


// 错误 - 没有错误处理器
const [mutate] = useMutation(MUTATION);

// 正确 - 总是处理错误
const [mutate] = useMutation(MUTATION, {
  onError: (error) => {
    console.error('mutation failed:', error);
    toast.error({ title: '操作失败' });
  },
});


// 错误 - mutation期间按钮未禁用
<Button onPress={submit}>提交</Button>

// 正确 - 禁用并显示加载
<Button onPress={submit} isDisabled={loading} isLoading={loading}>
  提交
</Button>
```

## Codegen命令

```bash
# 从.gql文件生成类型
npm run gql:typegen

# 下载schema+生成类型
npm run sync-types
```

## 与其他技能的集成

- **react-ui-patterns**: 用于queries的加载/错误/空状态
- **testing-patterns**: 在测试中模拟生成的hook
- **formik-patterns**: Mutation提交模式

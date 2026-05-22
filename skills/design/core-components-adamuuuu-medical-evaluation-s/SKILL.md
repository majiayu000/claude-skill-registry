---
name: core-components
description: 核心组件库和设计系统模式。在构建UI、使用设计令牌或处理组件库时使用。
---

# 核心组件

## 设计系统概览

使用来自核心库的组件而不是原生平台组件。这确保了一致的样式和行为。

## 设计令牌

**绝对不要硬编码值。始终使用设计令牌。**

### 间距令牌

```tsx
// 正确 - 使用令牌
<Box padding="$4" marginBottom="$2" />

// 错误 - 硬编码值
<Box padding={16} marginBottom={8} />
```

| 令牌 | 值   |
| ---- | ---- |
| `$1` | 4px  |
| `$2` | 8px  |
| `$3` | 12px |
| `$4` | 16px |
| `$6` | 24px |
| `$8` | 32px |

### 颜色令牌

```tsx
// 正确 - 语义令牌
<Text color="$textPrimary" />
<Box backgroundColor="$backgroundSecondary" />

// 错误 - 硬编码颜色
<Text color="#333333" />
<Box backgroundColor="rgb(245, 245, 245)" />
```

| 语义令牌         | 用途          |
| ---------------- | ------------- |
| `$textPrimary`   | 主要文本      |
| `$textSecondary` | 辅助文本      |
| `$textTertiary`  | 禁用/提示文本 |
| `$primary500`    | 品牌/强调色   |
| `$statusError`   | 错误状态      |
| `$statusSuccess` | 成功状态      |

### 排版令牌

```tsx
<Text fontSize="$lg" fontWeight="$semibold" />
```

| 令牌   | 大小 |
| ------ | ---- |
| `$xs`  | 12px |
| `$sm`  | 14px |
| `$md`  | 16px |
| `$lg`  | 18px |
| `$xl`  | 20px |
| `$2xl` | 24px |

## 核心组件

### Box

具有令牌支持的基础布局组件：

```tsx
<Box padding="$4" backgroundColor="$backgroundPrimary" borderRadius="$lg">
  {children}
</Box>
```

### HStack / VStack

水平和垂直flex布局：

```tsx
<HStack gap="$3" alignItems="center">
  <Icon name="user" />
  <Text>用户名</Text>
</HStack>

<VStack gap="$4" padding="$4">
  <Heading>标题</Heading>
  <Text>内容</Text>
</VStack>
```

### Text

具有令牌支持的排版：

```tsx
<Text fontSize="$lg" fontWeight="$semibold" color="$textPrimary">
  Hello World
</Text>
```

### Button

具有变体的交互按钮：

```tsx
<Button
  onPress={handlePress}
  variant="solid"
  size="md"
  isLoading={loading}
  isDisabled={disabled}
>
  点击我
</Button>
```

| 变体      | 用途          |
| --------- | ------------- |
| `solid`   | 主要操作      |
| `outline` | 次要操作      |
| `ghost`   | 三级/微妙操作 |
| `link`    | 内联操作      |

### Input

带验证的表单输入：

```tsx
<Input
  value={value}
  onChangeText={setValue}
  placeholder="输入文本"
  error={touched ? errors.field : undefined}
  label="字段名"
/>
```

### Card

内容容器：

```tsx
<Card padding="$4" gap="$3">
  <CardHeader>
    <Heading size="sm">卡片标题</Heading>
  </CardHeader>
  <CardBody>
    <Text>卡片内容</Text>
  </CardBody>
</Card>
```

## 布局模式

### 屏幕布局

```tsx
const MyScreen = () => (
  <Screen>
    <ScreenHeader title="页面标题" />
    <ScreenContent padding="$4">{/* 内容 */}</ScreenContent>
  </Screen>
);
```

### 表单布局

```tsx
<VStack gap="$4" padding="$4">
  <Input label="名称" {...nameProps} />
  <Input label="电子邮件" {...emailProps} />
  <Button isLoading={loading}>提交</Button>
</VStack>
```

### 列表项布局

```tsx
<HStack
  padding="$4"
  gap="$3"
  alignItems="center"
  borderBottomWidth={1}
  borderColor="$borderLight"
>
  <Avatar source={{ uri: imageUrl }} size="md" />
  <VStack flex={1}>
    <Text fontWeight="$semibold">{title}</Text>
    <Text color="$textSecondary" fontSize="$sm">
      {subtitle}
    </Text>
  </VStack>
  <Icon name="chevron-right" color="$textTertiary" />
</HStack>
```

## 反模式

```tsx
// 错误 - 硬编码值
<View style={{ padding: 16, backgroundColor: '#fff' }}>

// 正确 - 设计令牌
<Box padding="$4" backgroundColor="$backgroundPrimary">


// 错误 - 原生平台组件
import { View, Text } from 'react-native';

// 正确 - 核心组件
import { Box, Text } from 'components/core';


// 错误 - 内联样式
<Text style={{ fontSize: 18, fontWeight: '600' }}>

// 正确 - 令牌属性
<Text fontSize="$lg" fontWeight="$semibold">
```

## 组件属性模式

创建组件时，使用基于令牌的属性：

```tsx
interface CardProps {
  padding?: "$2" | "$4" | "$6";
  variant?: "elevated" | "outlined" | "filled";
  children: React.ReactNode;
}

const Card = ({
  padding = "$4",
  variant = "elevated",
  children,
}: CardProps) => (
  <Box
    padding={padding}
    backgroundColor="$backgroundPrimary"
    borderRadius="$lg"
    {...variantStyles[variant]}
  >
    {children}
  </Box>
);
```

## 与其他技能的集成

- **react-ui-patterns**: 为UI状态使用核心组件
- **testing-patterns**: 在测试中模拟核心组件
- **storybook**: 记录组件变体

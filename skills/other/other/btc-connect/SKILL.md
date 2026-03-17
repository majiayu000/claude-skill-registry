---
name: btc-connect
description: 专业的比特币钱包连接技能，支持btc-connect core、react、vue包在React、Vue、Next.js、Nuxt 3项目中的完整集成，包含UniSat和OKX钱包适配、网络切换功能、SSR环境配置、统一Hook API和v0.5.0最新特性
---

# BTC-Connect 专业集成技能

## 技能概述

btc-connect 是专为比特币 Web3 应用设计的钱包连接工具包，提供统一的连接接口、事件监听和适配层。此技能支持在 React、Vue、Next.js、Nuxt 3 项目中完整集成最新版本的 btc-connect (v0.5.0+)，实现 UniSat 和 OKX 钱包的连接、网络切换、状态管理，并解决 SSR 环境兼容性问题。

**最新特性 (v0.5.0)**: 统一Hook API设计、智能主题检测系统、代码质量全面优化、完善类型安全、增强构建性能、完整测试覆盖。

## 使用场景

在以下情况下使用此技能：
- 需要在 React/Vue 项目中集成比特币钱包连接功能
- 需要在 Next.js/Nuxt 3 SSR 项目中配置 btc-connect
- 需要实现比特币网络切换（主网/测试网/回归测试网）
- 需要集成 UniSat 或 OKX 钱包
- 遇到 btc-connect API 集成或配置问题
- 需要排查钱包连接失败或 SSR 兼容性问题
- 需要升级到最新版本的 btc-connect 包 (v0.4.0+)

## 核心功能

### 1. 依赖安装和版本管理
- 自动安装最新版本的 @btc-connect/core、@btc-connect/react、@btc-connect/vue
- 最低版本要求 v0.4.0+，自动选择最新稳定版本
- 版本兼容性检查和智能验证
- 依赖关系验证和冲突解决
- Bun 包管理器优化

### 2. 框架集成配置
- React 项目配置和 Hooks 使用（Context Provider 模式）
- Vue 项目配置和 Composables 使用（插件系统）
- Next.js SSR 环境配置（客户端组件模式）
- Nuxt 3 SSR 环境配置（客户端插件模式）

### 3. 🆕 网络切换功能 (v0.3.11+)
- 支持主网 (livenet)、测试网 (testnet)、回归测试网 (regtest)
- UniSat 钱包完全支持程序化网络切换
- OKX 钱包网络切换指导
- 网络变化事件监听和处理

### 4. 钱包适配和增强检测
- UniSat 钱包集成和完整 API 使用
- OKX 钱包集成和适配处理
- 🆕 增强钱包检测机制（20秒内每300ms轮询延迟注入）
- 钱包状态管理和事件监听
- 多钱包兼容性处理

### 5. 错误排查和性能优化
- 连接失败诊断和解决方案
- SSR 环境问题排查和修复
- 版本兼容性问题解决
- 🆕 性能优化（缓存系统、错误处理、连接优化）

## 使用流程

### 1. 项目评估和环境检查
首先检查项目类型和当前环境：
- 检查项目框架类型（React/Vue/Next.js/Nuxt 3）
- 检查现有的依赖和配置（确保无版本冲突）
- 确定SSR或CSR环境
- 检查 Node.js 版本（需要 >= 18）和 Bun 包管理器

### 2. 依赖安装和版本管理
根据项目类型安装相应包：

```bash
# 使用 Bun（推荐）
bun add @btc-connect/core @btc-connect/react  # React 项目
bun add @btc-connect/core @btc-connect/vue   # Vue 项目

# 或使用 npm
npm install @btc-connect/core @btc-connect/react
```

**版本要求**：
- @btc-connect/core: v0.4.0+ (自动安装最新版本)
- @btc-connect/react: v0.4.0+ (自动安装最新版本)
- @btc-connect/vue: v0.4.0+ (架构优化版本，自动安装最新版本)

> **💡 安装策略**: 安装脚本自动选择最新稳定版本，确保最低版本要求为 v0.4.0+

### 3. 框架集成配置
根据框架和环境进行配置：

**React 配置**：
- 配置 BTCWalletProvider 包装应用
- 使用 useWallet、useNetwork、useAccount 等 Hooks
- SSR 环境使用 'use client' 指令或动态导入

**Vue 配置**：
- 配置 BTCWalletPlugin 插件系统
- 使用 useWallet、useNetwork、useAccount 等 Composables
- 🆕 v0.4.0+ 统一 API 使用 `useWallet()`

**SSR 环境配置**：
- Next.js：客户端组件模式 + 动态导入
- Nuxt 3：客户端插件模式 + onMounted 生命周期

### 4. 🆕 网络切换功能配置
实现比特币网络切换：

```typescript
// React Hook 使用
const { network, switchNetwork } = useNetwork()
await switchNetwork('testnet')  // 切换到测试网

// Vue Composable 使用
const { network, switchNetwork } = useNetwork()
await switchNetwork('mainnet')  // 切换到主网
```

**支持网络**：livenet（主网）、testnet（测试网）、regtest（回归测试网）

### 5. 钱包集成和检测
选择并集成目标钱包：
- UniSat 钱包：完全支持程序化操作和网络切换
- OKX 钱包：基础连接和签名，网络切换需要手动操作
- 🆕 增强检测：自动检测延迟注入的钱包（20秒内轮询）

### 6. 问题排查和性能优化
如遇问题，按以下步骤排查：
1. 检查版本兼容性（确保使用最新版本）
2. 验证配置文件和框架集成
3. 测试钱包连接和网络切换
4. 查看 SSR 环境错误日志
5. 检查缓存系统和性能优化设置

## 框架集成指南

### React 集成（最新版本 v0.4.0+）
1. **安装依赖**：@btc-connect/core + @btc-connect/react
2. **配置 Provider**：使用 BTCWalletProvider 包装应用
3. **使用 Hooks**：useWallet、useNetwork、useAccount、useAutoConnect 等
4. **网络切换**：使用 useNetwork Hook 实现网络切换
5. **SSR 注意**：使用 'use client' 指令或动态导入

**快速示例**：
```tsx
'use client'
import { BTCWalletProvider, useWallet } from '@btc-connect/react'

function App() {
  return (
    <BTCWalletProvider>
      <WalletComponent />
    </BTCWalletProvider>
  )
}

function WalletComponent() {
  const { isConnected, connect, account, network } = useWallet()
  // 实现钱包连接逻辑
}
```

### Vue 集成（最新版本 v0.4.0+ 架构优化）
1. **安装依赖**：@btc-connect/core + @btc-connect/vue (v0.4.0+)
2. **配置插件**：使用 BTCWalletPlugin
3. **🆕 统一 API**：使用 `useWallet()` 获取所有功能
4. **组件使用**：ConnectButton、WalletModal 等
5. **网络切换**：内置网络切换功能

**快速示例**：
```vue
<template>
  <div>
    <ConnectButton @connect="handleConnect" />
    <!-- v0.4.0+ 已集成模态框到 ConnectButton -->
  </div>
</template>

<script setup>
import { ConnectButton, useWallet } from '@btc-connect/vue'

const wallet = useWallet() // 🆕 统一 API
const handleConnect = (walletId) => {
  console.log('连接到钱包:', walletId)
}
</script>
```

### Next.js SSR 集成（完整兼容）
1. **动态导入**：钱包组件必须动态导入
2. **客户端组件**：使用 'use client' 指令标记
3. **状态同步**：避免 SSR/客户端状态不匹配
4. **错误边界**：配置客户端错误处理

**关键配置**：
```tsx
// components/WalletConnect.tsx
'use client'
import { useWallet } from '@btc-connect/react'

export default function WalletConnect() {
  const { connect, isConnected } = useWallet()
  // 钱包连接逻辑
}

// pages/index.tsx
import dynamic from 'next/dynamic'
const WalletConnect = dynamic(() => import('./WalletConnect'), {
  ssr: false
})
```

### Nuxt 3 SSR 集成（完整支持）
1. **客户端插件**：创建客户端专用插件
2. **生命周期**：使用 onMounted 确保客户端执行
3. **运行时配置**：配置客户端环境变量
4. **组件保护**：使用 ClientOnly 组件包装

**关键配置**：
```typescript
// plugins/btc-connect.client.ts
import { BTCWalletPlugin } from '@btc-connect/vue'

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.use(BTCWalletPlugin)
})
```

```vue
<template>
  <ClientOnly>
    <ConnectButton />
  </ClientOnly>
</template>
```

## 钱包特定处理

### UniSat 钱包（完全支持）
- ✅ **完整程序化网络切换**：支持主网、测试网、回归测试网
- ✅ **完整 API 支持**：消息签名、PSBT 签名、比特币发送
- ✅ **事件监听完整**：账户变化、网络变化、连接状态
- ✅ **增强检测机制**：自动检测延迟注入（20秒内轮询）
- ✅ **性能优化**：缓存系统、错误处理、连接优化

**网络切换示例**：
```typescript
// 完全支持程序化切换
await switchNetwork('testnet')  // 立即切换到测试网
await switchNetwork('mainnet')  // 立即切换到主网
```

### OKX 钱包（部分支持）
- ⚠️ **有限网络切换**：通常需要用户在钱包中手动切换
- ✅ **基础连接和签名**：支持钱包连接和基础签名功能
- ✅ **账户管理**：支持多账户和余额查询
- ⚠️ **特殊错误处理**：需要针对 OKX 的错误处理逻辑
- ⚠️ **用户体验提示**：需要引导用户进行手动操作

**网络切换指导**：
```typescript
// OKX 钱包网络切换需要用户手动操作
try {
  await switchNetwork('testnet')
} catch (error) {
  // 提示用户在 OKX 钱包中手动切换网络
  console.log('请在 OKX 钱包中手动切换到测试网')
}
```

## 🆕 网络切换功能详解 (v0.3.11+)

### 支持的网络类型
- **livenet/mainnet**: 比特币主网
- **testnet**: 比特币测试网
- **regtest**: 回归测试网

### 核心包网络切换
```typescript
import { BTCWalletManager } from '@btc-connect/core'

const manager = new BTCWalletManager()
await manager.switchNetwork('testnet')

// 监听网络变化
manager.on('networkChange', ({ walletId, network }) => {
  console.log(`钱包 ${walletId} 切换到 ${network} 网络`)
})
```

### React Hook 网络切换
```typescript
import { useNetwork } from '@btc-connect/react'

function NetworkSwitcher() {
  const { network, switchNetwork, isSwitching } = useNetwork()

  const handleSwitch = async () => {
    try {
      await switchNetwork('mainnet')
      console.log('切换到主网成功')
    } catch (error) {
      console.error('切换失败:', error.message)
    }
  }

  return (
    <div>
      <p>当前网络: {network}</p>
      <button onClick={handleSwitch} disabled={isSwitching}>
        {isSwitching ? '切换中...' : '切换到主网'}
      </button>
    </div>
  )
}
```

### Vue Composable 网络切换
```vue
<template>
  <div class="network-switcher">
    <p>当前网络: {{ network.name }}</p>
    <button @click="switchToTestnet" :disabled="isSwitching">
      {{ isSwitching ? '切换中...' : '切换到测试网' }}
    </button>
  </div>
</template>

<script setup>
import { useNetwork } from '@btc-connect/vue'

const { network, switchNetwork, isSwitching } = useNetwork()

const switchToTestnet = async () => {
  try {
    await switchNetwork('testnet')
  } catch (error) {
    console.error('切换失败:', error.message)
  }
}
</script>
```

## 常见问题解决

### 连接问题
- **钱包检测失败**：检查钱包是否正确安装和启用
- **延迟注入处理**：使用增强检测机制（20秒内每300ms轮询）
- **用户取消连接**：正确处理用户取消连接的情况
- **网络权限**：确保钱包有权限访问目标网络

### SSR 问题
- **动态导入**：使用动态导入避免服务端错误
- **Window 对象**：检查 window 对象的可用性
- **状态同步**：处理 SSR/客户端状态不匹配问题
- **客户端插件**：在 Nuxt 3 中使用客户端专用插件

### 版本兼容性问题
- **版本匹配**：确保 core、react、vue 包版本兼容
- **API 变更**：注意 v0.4.0+ Vue 包的架构变化
- **类型定义**：配置正确的 TypeScript 类型
- **依赖冲突**：检查是否存在依赖版本冲突

### 性能问题
- **缓存系统**：利用智能缓存提升性能
- **连接优化**：避免不必要的重复连接
- **事件管理**：正确清理事件监听器
- **内存泄漏**：检查组件卸载时的资源清理

## 最佳实践

1. **版本一致性**：使用安装脚本自动安装最新版本，确保最低版本要求（core v0.4.0+, vue v0.4.0+）
2. **错误处理**：实现完整的错误处理和用户反馈机制
3. **状态管理**：正确处理钱包连接状态和网络状态变化
4. **用户体验**：提供清晰的状态指示和操作指导
5. **安全性**：验证钱包连接和交易请求的安全性
6. **性能优化**：利用缓存系统和增强检测机制优化性能
7. **SSR 兼容**：在 SSR 项目中正确配置客户端组件
8. **网络切换**：为不同钱包提供合适的网络切换体验
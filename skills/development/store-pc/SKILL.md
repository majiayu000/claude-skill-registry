---
name: store-pc-pinia
description: |
  基于若依-vue-plus框架的PC端Pinia状态管理完整规范。定义Store模块化架构、数据持久化策略、异步Action标准、响应式数据访问及TypeScript类型安全规范。
  
  触发场景：
  - 开发用户信息管理、权限路由控制、系统设置或字典数据缓存等需要跨组件数据共享
  - 需要实现Token持久化、用户登录状态管理、权限动态路由生成
  - 需要管理全局应用状态（如侧边栏折叠状态、主题配置、字典数据缓存等）
  - 需要在组件间共享复杂业务逻辑或异步数据流
  
  触发词：状态管理、Pinia、Store、用户信息、持久化、Token、权限管理、路由控制、全局状态、响应式数据
---

# Pinia 状态管理规范

## 核心规范

### 规范1：Store模块化定义与命名规范
**详细说明：**
使用`defineStore`定义Store，必须遵循以下命名规范：
- **Store ID命名**：采用小写字母加中划线，如`'user'`、`'permission'`、`'app-settings'`
- **Store函数命名**：采用`use[模块名]Store`格式，如`useUserStore`、`usePermissionStore`
- **模块化拆分**：按业务功能拆分Store模块（用户、权限、设置、字典等），避免单一Store过于臃肿
- **文件组织**：每个Store模块独立文件存放在`src/store/modules/`目录下

**核心原则：**
- 单一职责原则：每个Store只负责一个明确的业务领域
- 唯一ID原则：Store ID在整个应用中必须唯一，避免命名冲突
- 模块独立性：各Store模块之间尽量解耦，减少相互依赖

### 规范2：数据持久化配置标准
**详细说明：**
对于需要持久化的状态（如Token、用户信息、侧边栏状态、主题配置等），必须启用`persist`配置，并遵循以下规范：

**存储策略选择：**
- **localStorage**：用于需要长期保存的数据（Token、用户偏好设置、主题配置）
- **sessionStorage**：用于会话级别的临时数据（临时权限、页面缓存状态）

**paths配置原则：**
- 必须显式指定需要持久化的字段路径，避免全量持久化
- 禁止持久化临时状态（如loading、error、缓存时间戳等）
- 支持嵌套路径配置，如`['user.profile', 'user.settings']`

**key命名规范：**
- 采用项目前缀+模块名格式，如`'ruoyi-user'`、`'ruoyi-permission'`
- 避免与其他项目或第三方库的Storage Key冲突

**示例代码：**

```javascript
import { defineStore } from 'pinia';

// 标准的Store定义结构
export const useUserStore = defineStore('user', {
  state: () => ({
    // 认证信息
    token: '',
    refreshToken: '',
    // 用户基本信息
    name: '',
    avatar: '',
    nickName: '',
    // 权限相关
    roles: [],
    permissions: [],
    // 临时状态（不持久化）
    isLoading: false,
    lastUpdateTime: null
  }),
  
  getters: {
    // 计算属性：判断是否已登录
    isLoggedIn: (state) => !!state.token,
    // 计算属性：是否有特定权限
    hasPermission: (state) => (permission) => {
      return state.permissions.includes(permission);
    }
  },
  
  actions: {
    // ...actions定义见规范3
  },
  
  // 数据持久化配置
  persist: {
    enabled: true,
    strategies: [
      {
        key: 'ruoyi-user',           // 唯一的Storage Key
        storage: localStorage,        // 长期存储
        paths: ['token', 'refreshToken', 'name', 'avatar', 'roles', 'permissions'] // 显式指定持久化字段
      }
    ]
  }
});
```

### 规范3：异步Action与API解耦规范
**详细说明：**
所有异步逻辑（如登录请求、获取用户信息、数据CRUD操作）必须封装在`actions`中，严格遵循以下规范：

**API调用规范：**
- 禁止在Vue组件中直接调用API接口
- Action内部必须调用`src/api`目录下对应的接口方法
- API方法与Action方法保持清晰的职责分离：API负责HTTP请求，Action负责状态更新

**异步处理规范：**
- 使用`async/await`语法处理异步操作，避免回调地狱
- 使用`try/catch`进行错误捕获，或依赖全局Axios拦截器统一处理
- 异步Action应返回Promise，便于组件中链式调用和错误处理

**状态更新规范：**
- Action中使用`this`访问和修改state
- 复杂的状态更新逻辑应拆分为多个私有方法
- 保证状态更新的原子性，避免中间状态暴露

**错误处理策略：**
- 业务级错误（如登录失败）：在Action中捕获并抛出给组件处理
- 系统级错误（如网络超时）：由全局Axios拦截器统一处理
- 关键操作（如登录、支付）：需要在Action中记录错误日志

**示例代码：**

```javascript
// src/api/login.js - API层
import request from '@/utils/request';

export function login(username, password, code, uuid) {
  return request({
    url: '/login',
    method: 'post',
    data: { username, password, code, uuid }
  });
}

export function getInfo() {
  return request({
    url: '/getInfo',
    method: 'get'
  });
}

export function logout() {
  return request({
    url: '/logout',
    method: 'post'
  });
}
```

```javascript
// src/store/modules/user.js - Store层
import { defineStore } from 'pinia';
import { login, getInfo, logout } from '@/api/login';
import { getToken, setToken, removeToken } from '@/utils/auth';
import defAva from '@/assets/images/profile.jpg';

export const useUserStore = defineStore('user', {
  state: () => ({
    token: getToken(),
    name: '',
    avatar: '',
    roles: [],
    permissions: []
  }),
  
  actions: {
    // 登录Action
    async login(userInfo) {
      const username = userInfo.username.trim();
      const password = userInfo.password;
      const code = userInfo.code;
      const uuid = userInfo.uuid;
      
      try {
        const res = await login(username, password, code, uuid);
        setToken(res.token);
        this.token = res.token;
        return res;
      } catch (error) {
        console.error('Login failed:', error);
        throw error; // 抛出错误供组件处理
      }
    },
    
    // 获取用户信息Action
    async getInfo() {
      try {
        const res = await getInfo();
        const user = res.user;
        const avatar = user.avatar === '' || user.avatar == null ? defAva : user.avatar;
        
        // 批量更新状态
        this.name = user.userName;
        this.avatar = avatar;
        this.roles = res.roles;
        this.permissions = res.permissions;
        
        return res;
      } catch (error) {
        console.error('Failed to get user info:', error);
        throw error;
      }
    },
    
    // 登出Action
    async logout() {
      try {
        await logout();
        this.resetState();
        removeToken();
      } catch (error) {
        console.error('Logout failed:', error);
        throw error;
      }
    },
    
    // 重置状态的私有方法
    resetState() {
      this.token = '';
      this.name = '';
      this.avatar = '';
      this.roles = [];
      this.permissions = [];
    }
  },
  
  persist: {
    enabled: true,
    strategies: [
      {
        key: 'ruoyi-user',
        storage: localStorage,
        paths: ['token', 'name', 'avatar', 'roles', 'permissions']
      }
    ]
  }
});
```

### 规范4：响应式数据访问规范
**详细说明：**
在Vue 3的Composition API中访问Store数据时，必须使用`storeToRefs`保持响应式：

**响应式解构规范：**
- 使用`storeToRefs`解构state和getters，保持响应性
- 直接解构actions（不需要转换为ref）
- 避免直接解构整个store对象

**组件中使用示例：**

```vue
<!-- 组件中正确使用Store -->
<script setup>
import { storeToRefs } from 'pinia';
import { useUserStore } from '@/store/modules/user';

const userStore = useUserStore();

// ✅ 正确：使用storeToRefs解构state，保持响应式
const { token, name, avatar, roles, permissions, isLoggedIn } = storeToRefs(userStore);

// ✅ 正确：直接解构actions（不需要storeToRefs）
const { login, logout, getInfo } = userStore;

// ❌ 错误：直接解构state会失去响应性
// const { token, name } = userStore;

// 使用示例
const handleLogin = async () => {
  try {
    await login({ username: 'admin', password: '123456' });
    console.log('登录成功，用户名：', name.value);
  } catch (error) {
    console.error('登录失败', error);
  }
};
</script>

<template>
  <div>
    <!-- 响应式数据自动更新 -->
    <div v-if="isLoggedIn">
      欢迎，{{ name }}
      <img :src="avatar" alt="头像" />
    </div>
  </div>
</template>
```

### 规范5：TypeScript类型安全规范（推荐）
**详细说明：**
在TypeScript项目中，为Store添加完整的类型定义以提升开发体验和代码健壮性：

```typescript
// src/store/modules/user.ts
import { defineStore } from 'pinia';
import { login, getInfo, logout } from '@/api/login';
import { getToken, setToken, removeToken } from '@/utils/auth';

// 定义State类型
interface UserState {
  token: string;
  name: string;
  avatar: string;
  roles: string[];
  permissions: string[];
}

// 定义登录表单类型
interface LoginForm {
  username: string;
  password: string;
  code?: string;
  uuid?: string;
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    token: getToken() || '',
    name: '',
    avatar: '',
    roles: [],
    permissions: []
  }),
  
  getters: {
    isLoggedIn: (state): boolean => !!state.token,
    hasPermission: (state) => {
      return (permission: string): boolean => {
        return state.permissions.includes(permission);
      };
    }
  },
  
  actions: {
    async login(userInfo: LoginForm): Promise<void> {
      const username = userInfo.username.trim();
      const password = userInfo.password;
      
      try {
        const res = await login(username, password, userInfo.code, userInfo.uuid);
        setToken(res.token);
        this.token = res.token;
      } catch (error) {
        console.error('Login failed:', error);
        throw error;
      }
    },
    
    async getInfo(): Promise<void> {
      try {
        const res = await getInfo();
        this.name = res.user.userName;
        this.avatar = res.user.avatar || '';
        this.roles = res.roles;
        this.permissions = res.permissions;
      } catch (error) {
        console.error('Failed to get user info:', error);
        throw error;
      }
    }
  }
});
```

### 规范6：Store模块间通信规范
**详细说明：**
当多个Store需要相互调用时，遵循以下规范：

**通信原则：**
- 避免循环依赖：Store A依赖Store B，则Store B不应依赖Store A
- 优先使用事件总线或组合式API进行松耦合通信
- 必要时可在Action中导入其他Store实例

```javascript
// src/store/modules/permission.js
import { defineStore } from 'pinia';
import { useUserStore } from './user';  // 导入其他Store

export const usePermissionStore = defineStore('permission', {
  state: () => ({
    routes: [],
    addRoutes: []
  }),
  
  actions: {
    async generateRoutes() {
      // 在Action中使用其他Store
      const userStore = useUserStore();
      const roles = userStore.roles;
      
      // 根据角色生成路由...
      const accessedRoutes = filterAsyncRoutes(asyncRoutes, roles);
      this.addRoutes = accessedRoutes;
      this.routes = constantRoutes.concat(accessedRoutes);
      
      return accessedRoutes;
    }
  }
});
```

## 禁止事项

### 状态管理禁止事项
- ❌ **禁止在Vue组件中直接修改state**：必须通过Store的actions修改状态，保证状态变更的可追踪性
  ```javascript
  // ❌ 错误做法
  const userStore = useUserStore();
  userStore.token = 'new-token';  // 直接修改
  
  // ✅ 正确做法
  userStore.updateToken('new-token');  // 通过action修改
  ```

- ❌ **禁止在Store中直接调用HTTP请求**：API调用必须封装在`src/api`目录中，Store只负责状态管理
  ```javascript
  // ❌ 错误做法
  actions: {
    async login() {
      const res = await axios.post('/login', data);  // 直接调用axios
    }
  }
  
  // ✅ 正确做法
  import { login } from '@/api/login';
  actions: {
    async login() {
      const res = await login(data);  // 调用封装好的API
    }
  }
  ```

- ❌ **禁止持久化临时状态**：`persist.paths`必须显式指定，避免持久化loading、error等临时状态
  ```javascript
  // ❌ 错误做法
  persist: {
    enabled: true,
    strategies: [{ storage: localStorage }]  // 未指定paths，全量持久化
  }
  
  // ✅ 正确做法
  persist: {
    enabled: true,
    strategies: [{ 
      storage: localStorage,
      paths: ['token', 'name']  // 只持久化必要字段
    }]
  }
  ```

### 响应式相关禁止事项
- ❌ **禁止直接解构Store失去响应性**：必须使用`storeToRefs`
  ```javascript
  // ❌ 错误做法
  const { name, avatar } = useUserStore();  // 失去响应性
  
  // ✅ 正确做法
  const { name, avatar } = storeToRefs(useUserStore());
  ```

- ❌ **禁止在setup外使用mapActions/mapState**：Vue 3推荐使用Composition API
  ```javascript
  // ❌ 错误做法（Options API）
  computed: {
    ...mapState(useUserStore, ['name', 'avatar'])
  }
  
  // ✅ 正确做法（Composition API）
  const { name, avatar } = storeToRefs(useUserStore());
  ```

### 架构设计禁止事项
- ❌ **禁止Store承担业务逻辑**：Store只负责状态管理，复杂业务逻辑应封装在独立的服务层
- ❌ **禁止创建过于臃肿的Store**：单个Store文件超过300行应考虑拆分
- ❌ **禁止Store之间循环依赖**：Store A依赖Store B，则Store B不能依赖Store A
- ❌ **禁止在Store中使用Vue组件实例**：Store应独立于组件存在，不依赖Vue实例
- ❌ **禁止在SSR场景下使用全局Store实例**：SSR中每个请求应创建独立的Store实例

## 参考代码

### 若依框架核心Store模块
- **用户Store**：`src/store/modules/user.js` - 用户信息、Token、权限管理
- **权限Store**：`src/store/modules/permission.js` - 动态路由、菜单权限控制
- **应用Store**：`src/store/modules/app.js` - 侧边栏状态、设备类型、语言配置
- **设置Store**：`src/store/modules/settings.js` - 主题配置、布局设置
- **字典Store**：`src/store/modules/dict.js` - 字典数据缓存

### Store入口文件
- **主入口**：`src/store/index.js` - Pinia实例创建和插件配置

### 配套工具文件
- **Token管理**：`src/utils/auth.js` - Token的存取删除工具函数
- **请求封装**：`src/utils/request.js` - Axios实例配置和拦截器

## 最佳实践

### 1. Store模块划分建议
按照业务领域进行模块划分，常见模块：
- **user**：用户认证、个人信息、会话管理
- **permission**：权限控制、动态路由、菜单管理
- **app**：应用全局状态（侧边栏、设备检测、多语言）
- **settings**：用户偏好设置（主题、布局、字体大小）
- **dict**：字典数据缓存（减少重复请求）
- **tags-view**：标签页管理（已访问页面历史）

### 2. 性能优化建议
- **按需加载**：只在需要时才导入Store模块
- **计算属性缓存**：使用getters缓存复杂计算结果
- **避免过度持久化**：只持久化必要的状态，减少Storage占用
- **批量更新**：多个状态变更应在一个action中完成，减少响应式更新次数
- **懒加载路由Store**：路由权限Store可在登录后再初始化

### 3. 调试技巧
- **Pinia DevTools**：使用Vue DevTools的Pinia扩展查看状态变化
- **时间旅行调试**：在DevTools中回溯状态变更历史
- **Action日志**：在关键Action中添加console.log记录状态变化
- **持久化调试**：检查localStorage/sessionStorage确认持久化是否生效

### 4. 测试建议
```javascript
// 单元测试示例
import { setActivePinia, createPinia } from 'pinia';
import { useUserStore } from '@/store/modules/user';

describe('User Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('should update user info', () => {
    const store = useUserStore();
    store.name = 'Test User';
    expect(store.name).toBe('Test User');
  });

  it('should check login status', () => {
    const store = useUserStore();
    store.token = 'test-token';
    expect(store.isLoggedIn).toBe(true);
  });
});
```

## 检查清单

### 架构设计检查
- [ ] Store模块是否按业务领域合理划分（user, permission, settings等）
- [ ] Store ID命名是否唯一且符合kebab-case规范
- [ ] 是否避免了Store之间的循环依赖
- [ ] 单个Store文件是否控制在300行以内

### 数据持久化检查
- [ ] 是否为需要持久化的状态配置了`persist`
- [ ] 是否显式指定了`paths`参数，避免全量持久化
- [ ] Storage Key命名是否包含项目前缀，避免冲突
- [ ] 是否正确选择了localStorage/sessionStorage存储策略
- [ ] 是否避免持久化临时状态（loading、error等）

### API调用检查
- [ ] 是否所有API调用都封装在`src/api`目录中
- [ ] 是否所有异步操作都通过actions执行
- [ ] 是否使用`async/await`处理异步逻辑
- [ ] 是否有合理的错误处理机制（try/catch或全局拦截器）
- [ ] Action是否返回Promise便于组件链式调用

### 响应式数据检查
- [ ] 在组件中是否使用`storeToRefs`解构state和getters
- [ ] 是否直接解构actions（不使用storeToRefs）
- [ ] 是否避免了在组件中直接修改state
- [ ] 是否正确使用`.value`访问ref包装的值

### TypeScript检查（适用于TS项目）
- [ ] 是否为State定义了完整的类型接口
- [ ] 是否为Action参数和返回值定义了类型
- [ ] 是否为Getters定义了返回值类型
- [ ] 是否避免使用`any`类型

### 代码质量检查
- [ ] Action命名是否语义清晰（login、logout、updateUserInfo）
- [ ] 是否添加了必要的注释说明复杂逻辑
- [ ] 是否有重置状态的方法（如logout时清空用户信息）
- [ ] 是否遵循了单一职责原则（一个action只做一件事）

## 常见问题解答

### Q1: 何时使用localStorage vs sessionStorage？
**A:** 
- **localStorage**：用于需要长期保存的数据（Token、用户偏好设置、记住我功能）
- **sessionStorage**：用于会话级别的临时数据（临时权限、页面缓存状态、单次会话数据）

### Q2: 如何处理Store中的异步并发问题？
**A:** 
```javascript
actions: {
  async fetchUserInfo() {
    if (this.isLoading) return;  // 防止重复请求
    this.isLoading = true;
    try {
      const res = await getInfo();
      this.name = res.user.userName;
    } finally {
      this.isLoading = false;
    }
  }
}
```

### Q3: 如何在路由守卫中使用Store？
**A:** 
```javascript
// src/router/index.js
import { useUserStore } from '@/store/modules/user';

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore();
  
  if (userStore.token) {
    if (!userStore.roles.length) {
      await userStore.getInfo();
    }
    next();
  } else {
    next('/login');
  }
});
```

### Q4: 如何重置所有Store状态？
**A:** 
```javascript
// 方法1：在各Store中提供reset方法
export const useUserStore = defineStore('user', {
  actions: {
    $reset() {
      this.token = '';
      this.name = '';
      // ... 重置所有状态
    }
  }
});

// 方法2：重新创建Pinia实例（谨慎使用）
import { createPinia } from 'pinia';
app.use(createPinia());
```

### Q5: Store数据持久化后，如何处理版本升级导致的数据结构变化？
**A:** 
```javascript
// 在Store初始化时进行数据迁移
state: () => {
  const savedData = JSON.parse(localStorage.getItem('ruoyi-user') || '{}');
  
  // 版本检测和数据迁移
  if (savedData.version !== '2.0') {
    // 执行数据迁移逻辑
    return migrateData(savedData);
  }
  
  return savedData;
}
```

## 相关资源

### 官方文档
- [Pinia官方文档](https://pinia.vuejs.org/)
- [Vue 3 Composition API](https://cn.vuejs.org/api/composition-api-setup.html)
- [若依Vue Plus文档](http://vue.ruoyi.vip/)

### 推荐插件
- **pinia-plugin-persistedstate**：Pinia持久化插件
- **Vue DevTools**：Vue官方调试工具（包含Pinia支持）

### 代码示例仓库
- 若依Vue Plus官方仓库：参考完整的Store实现案例
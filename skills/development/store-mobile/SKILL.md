---
name: store-mobile
description: |
  基于若依-vue-plus移动端框架的Uni-app状态管理标准规范。
  定义Pinia Store结构、Uni-app持久化适配、异步Action模式、状态响应式处理及用户登录态流转完整规范。
  
  适用场景：
  - 开发用户登录/注册/退出功能
  - 实现权限控制与角色管理
  - 管理全局配置（主题、语言、设置等）
  - 处理跨页面状态共享
  - 实现购物车、收藏夹等状态管理
  
  触发关键词：移动端状态管理、Pinia Store、Uni-app持久化、用户登录态、权限管理、全局状态
---

# 移动端状态管理规范 (Uni-app + Pinia)

## 核心规范

### 规范1：Store定义与模块化结构
**说明**：使用`defineStore`定义Store模块，每个Store应职责单一，遵循命名规范。Store ID采用kebab-case，Store名称采用use+驼峰命名。

**关键要点**：
- Store ID必须全局唯一
- State应定义为工厂函数，避免跨实例污染
- 优先使用Options API风格（state/getters/actions）
- 复杂业务应拆分多个Store模块

```javascript
// src/store/modules/user.js
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  // State必须使用工厂函数
  state: () => ({
    token: '',
    userInfo: {
      userId: null,
      userName: '',
      avatar: '',
      nickName: ''
    },
    roles: [],
    permissions: [],
    isLogin: false
  }),
  
  // Getters用于派生状态
  getters: {
    hasRole: (state) => (role) => state.roles.includes(role),
    hasPermission: (state) => (permission) => state.permissions.includes(permission),
    displayName: (state) => state.userInfo.nickName || state.userInfo.userName || '游客'
  },
  
  actions: {
    // Actions定义见规范2
  }
});
```

### 规范2：Uni-app持久化适配（persist配置）
**说明**：移动端环境必须配置`persist`插件以适配Uni-app存储机制。使用`uni.getStorageSync`/`uni.setStorageSync`替代浏览器localStorage，确保小程序兼容性。

**关键要点**：
- 必须使用uni-app存储API（非浏览器API）
- 仅持久化必要字段，避免存储敏感信息明文
- Key命名应带项目前缀，防止命名冲突
- 敏感数据（如token）需配合加密存储

```javascript
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    token: '',
    userInfo: {},
    roles: [],
    permissions: []
  }),
  
  actions: {
    setToken(token) {
      this.token = token;
    },
    setUserInfo(info) {
      this.userInfo = info;
    },
    setRoles(roles) {
      this.roles = roles;
    }
  },
  
  // ✅ 正确：配置Uni-app持久化
  persist: {
    enabled: true,
    strategies: [
      {
        key: 'ruoyi-mobile-user', // 带项目前缀
        storage: {
          getItem: (key) => uni.getStorageSync(key),
          setItem: (key, value) => uni.setStorageSync(key, value)
        },
        paths: ['token', 'userInfo', 'roles'] // 仅持久化必要字段
      }
    ]
  }
});
```

**错误示例**：
```javascript
// ❌ 错误：使用浏览器localStorage（小程序不兼容）
persist: {
  enabled: true,
  strategies: [
    {
      key: 'user',
      storage: localStorage // ❌ 小程序环境不支持
    }
  ]
}
```

### 规范3：异步Action与API调用规范
**说明**：业务逻辑（如登录、获取用户信息）必须在`actions`中以async函数形式定义。Action内部应调用`src/api`下的接口方法，处理完整的成功/失败流程。

**关键要点**：
- 使用async/await处理异步逻辑
- 统一调用`src/api`下的接口方法
- 必须进行错误处理（try-catch）
- 成功后更新State，失败时返回Promise.reject
- 涉及页面跳转时使用uni-app路由API

```javascript
import { login, getInfo, logout } from '@/api/login';
import { removeToken } from '@/utils/auth';

export const useUserStore = defineStore('user', {
  state: () => ({
    token: '',
    userInfo: {},
    roles: [],
    permissions: []
  }),
  
  actions: {
    // ✅ 登录Action
    async login(loginForm) {
      try {
        const res = await login(loginForm);
        this.token = res.token;
        this.isLogin = true;
        
        // 登录成功后跳转到首页（使用uni-app路由API）
        uni.reLaunch({ url: '/pages/index/index' });
        return Promise.resolve(res);
      } catch (error) {
        console.error('Login Failed:', error);
        uni.showToast({ title: '登录失败', icon: 'none' });
        return Promise.reject(error);
      }
    },

    // ✅ 获取用户信息Action
    async getUserInfo() {
      try {
        const res = await getInfo();
        this.userInfo = res.user;
        this.roles = res.roles;
        this.permissions = res.permissions;
        return Promise.resolve(res);
      } catch (error) {
        console.error('Get UserInfo Failed:', error);
        return Promise.reject(error);
      }
    },

    // ✅ 退出登录Action
    async logout() {
      try {
        await logout();
        this.token = '';
        this.userInfo = {};
        this.roles = [];
        this.permissions = [];
        this.isLogin = false;
        removeToken();
        
        // 跳转到登录页（使用reLaunch清空页面栈）
        uni.reLaunch({ url: '/pages/login/login' });
        return Promise.resolve();
      } catch (error) {
        console.error('Logout Failed:', error);
        return Promise.reject(error);
      }
    }
  }
});
```

### 规范4：组件中使用Store的正确方式
**说明**：在组件中使用Store时，必须保持响应式。直接解构会丢失响应性，必须使用`storeToRefs`或computed包装。

**关键要点**：
- 使用`storeToRefs`解构state和getters
- Actions可以直接解构（不需要响应式）
- 禁止直接修改state，必须通过actions

```vue
<template>
  <view>
    <view>用户名：{{ displayName }}</view>
    <view>Token：{{ token }}</view>
    <button @click="handleLogout">退出登录</button>
  </view>
</template>

<script setup>
import { storeToRefs } from 'pinia';
import { useUserStore } from '@/store/modules/user';

const userStore = useUserStore();

// ✅ 正确：使用storeToRefs解构state和getters（保持响应式）
const { token, userInfo, displayName } = storeToRefs(userStore);

// ✅ 正确：actions可以直接解构
const { logout } = userStore;

// ✅ 正确：调用action
const handleLogout = async () => {
  try {
    await logout();
  } catch (error) {
    console.error('退出失败', error);
  }
};

// ❌ 错误示例
// const { token } = useUserStore(); // ❌ 直接解构会丢失响应式
</script>
```

### 规范5：路由跳转规范
**说明**：Uni-app环境下必须使用`uni`对象的路由API，严禁使用Vue Router。根据场景选择合适的跳转方法。

**路由API选择**：
- `uni.navigateTo`：保留当前页面，跳转到应用内的某个页面（页面栈+1）
- `uni.redirectTo`：关闭当前页面，跳转到应用内的某个页面（页面栈不变）
- `uni.reLaunch`：关闭所有页面，打开到应用内的某个页面（重置页面栈）
- `uni.switchTab`：跳转到tabBar页面，并关闭其他所有非tabBar页面
- `uni.navigateBack`：返回上一页面或多级页面

```javascript
// ✅ 正确示例
actions: {
  async login(loginForm) {
    const res = await login(loginForm);
    this.token = res.token;
    
    // 登录成功：使用reLaunch清空页面栈
    uni.reLaunch({ url: '/pages/index/index' });
  },
  
  async logout() {
    await logout();
    this.token = '';
    
    // 退出登录：使用reLaunch跳转到登录页
    uni.reLaunch({ url: '/pages/login/login' });
  },
  
  goToProfile() {
    // 跳转到个人中心（保留当前页）
    uni.navigateTo({ url: '/pages/profile/profile' });
  },
  
  goToHome() {
    // 跳转到首页tabBar
    uni.switchTab({ url: '/pages/index/index' });
  }
}

// ❌ 错误示例
actions: {
  async login() {
    // ❌ 禁止使用Vue Router
    this.$router.push('/index'); // 错误！Uni-app不支持
    router.push({ name: 'index' }); // 错误！Uni-app不支持
  }
}
```

## 禁止事项

### 🚫 状态修改相关
- ❌ **禁止在组件中直接修改state**：必须通过`actions`或Pinia的`$patch`方法修改
  ```javascript
  // ❌ 错误
  userStore.token = 'new-token';
  
  // ✅ 正确
  userStore.setToken('new-token');
  // 或使用$patch
  userStore.$patch({ token: 'new-token' });
  ```

- ❌ **禁止在state外部进行复杂业务逻辑**：业务逻辑应封装在actions中
  ```javascript
  // ❌ 错误：在组件中处理业务逻辑
  const handleLogin = async () => {
    const res = await login(form);
    userStore.token = res.token;
    userStore.userInfo = res.userInfo;
    uni.reLaunch({ url: '/pages/index/index' });
  };
  
  // ✅ 正确：在Store的action中处理
  const handleLogin = async () => {
    await userStore.login(form);
  };
  ```

### 🚫 持久化相关
- ❌ **禁止使用浏览器localStorage**：必须使用`uni.getStorageSync`/`uni.setStorageSync`以兼容小程序
  ```javascript
  // ❌ 错误
  persist: {
    storage: localStorage // 小程序不支持
  }
  
  // ✅ 正确
  persist: {
    storage: {
      getItem: (key) => uni.getStorageSync(key),
      setItem: (key, value) => uni.setStorageSync(key, value)
    }
  }
  ```

- ❌ **禁止持久化所有state字段**：仅持久化必要字段，避免存储冗余数据
  ```javascript
  // ❌ 错误：持久化所有字段
  persist: {
    enabled: true,
    strategies: [{ key: 'user' }]
  }
  
  // ✅ 正确：仅持久化必要字段
  persist: {
    enabled: true,
    strategies: [
      {
        key: 'user',
        paths: ['token', 'userInfo', 'roles']
      }
    ]
  }
  ```

- ❌ **禁止明文存储敏感信息**：token等敏感数据需加密存储
  ```javascript
  // ❌ 风险：明文存储token
  persist: {
    paths: ['token']
  }
  
  // ✅ 建议：配合加密工具
  import { encrypt, decrypt } from '@/utils/crypto';
  
  persist: {
    storage: {
      getItem: (key) => {
        const value = uni.getStorageSync(key);
        return value ? decrypt(value) : null;
      },
      setItem: (key, value) => {
        uni.setStorageSync(key, encrypt(value));
      }
    }
  }
  ```

### 🚫 响应式相关
- ❌ **禁止直接解构store的state**：必须使用`storeToRefs`保持响应性
  ```javascript
  // ❌ 错误：直接解构（丢失响应式）
  const { token, userInfo } = useUserStore();
  
  // ✅ 正确：使用storeToRefs
  const { token, userInfo } = storeToRefs(useUserStore());
  ```

- ❌ **禁止在setup外部调用store**：Store必须在setup函数或生命周期内调用
  ```javascript
  // ❌ 错误：在setup外部调用
  const userStore = useUserStore(); // 模块顶层调用
  
  export default {
    setup() {
      // ...
    }
  };
  
  // ✅ 正确：在setup内部调用
  export default {
    setup() {
      const userStore = useUserStore();
      // ...
    }
  };
  ```

### 🚫 路由相关
- ❌ **禁止使用Vue Router**：Uni-app环境下必须使用`uni`对象的路由API
  ```javascript
  // ❌ 错误
  this.$router.push('/pages/index');
  router.push({ name: 'index' });
  
  // ✅ 正确
  uni.navigateTo({ url: '/pages/index/index' });
  uni.reLaunch({ url: '/pages/index/index' });
  ```

- ❌ **禁止在非tabBar页面使用switchTab**：switchTab仅用于跳转tabBar页面
  ```javascript
  // ❌ 错误：跳转非tabBar页面
  uni.switchTab({ url: '/pages/profile/profile' }); // profile非tabBar
  
  // ✅ 正确
  uni.navigateTo({ url: '/pages/profile/profile' });
  ```

### 🚫 Store设计相关
- ❌ **禁止单一Store存储所有状态**：应按业务模块拆分Store
  ```javascript
  // ❌ 错误：全部状态塞入一个Store
  export const useAppStore = defineStore('app', {
    state: () => ({
      user: {},
      cart: [],
      orders: [],
      settings: {},
      theme: ''
      // ...更多状态
    })
  });
  
  // ✅ 正确：按业务拆分
  export const useUserStore = defineStore('user', { /* ... */ });
  export const useCartStore = defineStore('cart', { /* ... */ });
  export const useOrderStore = defineStore('order', { /* ... */ });
  export const useSettingsStore = defineStore('settings', { /* ... */ });
  ```

- ❌ **禁止在Store中引入Vue组件**：Store应保持纯逻辑，不依赖UI组件

- ❌ **禁止在getter中执行异步操作**：异步逻辑应放在actions中
  ```javascript
  // ❌ 错误
  getters: {
    async userDetail(state) { // getter不支持async
      return await fetchUser(state.userId);
    }
  }
  
  // ✅ 正确
  actions: {
    async fetchUserDetail() {
      const detail = await fetchUser(this.userId);
      this.userDetail = detail;
    }
  }
  ```

## 最佳实践

### 💡 Store模块组织
```
src/store/
├── index.js              # Pinia实例配置
├── modules/
│   ├── user.js          # 用户状态（登录、权限）
│   ├── cart.js          # 购物车状态
│   ├── order.js         # 订单状态
│   └── settings.js      # 全局设置（主题、语言）
└── plugins/
    └── persist.js       # 持久化插件配置
```

### 💡 统一错误处理
```javascript
// src/store/modules/user.js
export const useUserStore = defineStore('user', {
  actions: {
    async login(loginForm) {
      try {
        const res = await login(loginForm);
        this.token = res.token;
        this.isLogin = true;
        
        uni.showToast({ title: '登录成功', icon: 'success' });
        uni.reLaunch({ url: '/pages/index/index' });
        return Promise.resolve(res);
      } catch (error) {
        console.error('[Store/User] Login failed:', error);
        
        // 统一错误提示
        const message = error.message || '登录失败，请重试';
        uni.showToast({ title: message, icon: 'none' });
        
        return Promise.reject(error);
      }
    }
  }
});
```

### 💡 使用$patch批量更新
```javascript
// ✅ 推荐：批量更新使用$patch（性能更好）
userStore.$patch({
  token: 'new-token',
  userInfo: { name: '张三' },
  isLogin: true
});

// 或使用函数形式
userStore.$patch((state) => {
  state.token = 'new-token';
  state.userInfo.name = '张三';
  state.isLogin = true;
});
```

### 💡 权限验证示例
```javascript
// src/store/modules/user.js
export const useUserStore = defineStore('user', {
  state: () => ({
    roles: [],
    permissions: []
  }),
  
  getters: {
    // 检查是否拥有指定角色
    hasRole: (state) => (role) => {
      return state.roles.includes(role);
    },
    
    // 检查是否拥有指定权限
    hasPermission: (state) => (permission) => {
      return state.permissions.includes(permission);
    },
    
    // 检查是否拥有任一权限
    hasAnyPermission: (state) => (permissions) => {
      return permissions.some(p => state.permissions.includes(p));
    },
    
    // 检查是否拥有全部权限
    hasAllPermissions: (state) => (permissions) => {
      return permissions.every(p => state.permissions.includes(p));
    }
  }
});

// 组件中使用
<template>
  <button v-if="hasPermission('user:add')" @click="addUser">添加用户</button>
</template>

<script setup>
import { storeToRefs } from 'pinia';
import { useUserStore } from '@/store/modules/user';

const userStore = useUserStore();
const { hasPermission } = storeToRefs(userStore);
</script>
```

### 💡 多Store协同工作
```javascript
// src/store/modules/cart.js
import { defineStore } from 'pinia';
import { useUserStore } from './user';

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: []
  }),
  
  actions: {
    async addToCart(product) {
      // 访问其他Store
      const userStore = useUserStore();
      
      // 检查登录状态
      if (!userStore.isLogin) {
        uni.showToast({ title: '请先登录', icon: 'none' });
        uni.navigateTo({ url: '/pages/login/login' });
        return;
      }
      
      // 添加商品到购物车
      this.items.push(product);
      uni.showToast({ title: '已添加到购物车', icon: 'success' });
    }
  }
});
```

## 参考代码
**核心文件路径**：
- `src/store/index.js` - Pinia实例配置与插件注册
- `src/store/modules/user.js` - 用户状态管理（登录、权限、个人信息）
- `src/store/modules/permission.js` - 权限路由管理
- `src/store/modules/dict.js` - 字典数据管理
- `src/utils/auth.js` - Token存取工具函数
- `src/api/login.js` - 登录相关API接口

**推荐阅读**：
- [Pinia官方文档](https://pinia.vuejs.org/zh/)
- [Uni-app存储API](https://uniapp.dcloud.net.cn/api/storage/storage.html)
- [若依移动端框架文档](https://doc.ruoyi.vip/ruoyi-vue/)

## 检查清单

### 📋 Store定义检查
- [ ] 是否使用`defineStore`定义Store
- [ ] Store ID是否全局唯一（kebab-case命名）
- [ ] State是否使用工厂函数`() => ({})`
- [ ] Getters是否仅用于派生状态（无副作用）
- [ ] Actions是否使用async/await处理异步逻辑
- [ ] 是否按业务模块合理拆分Store

### 📋 持久化配置检查
- [ ] 是否配置了`persist`插件
- [ ] 是否使用`uni.getStorageSync`/`uni.setStorageSync`（非localStorage）
- [ ] 是否仅持久化必要字段（使用`paths`配置）
- [ ] Key命名是否带项目前缀（防止冲突）
- [ ] 敏感数据是否考虑加密存储

### 📋 API调用检查
- [ ] 是否在actions中调用API（非组件中）
- [ ] 是否使用`src/api`下的接口方法
- [ ] 是否进行了try-catch错误处理
- [ ] 是否返回Promise（支持链式调用）
- [ ] 是否有统一的错误提示（uni.showToast）

### 📋 路由跳转检查
- [ ] 是否使用uni-app路由API（非Vue Router）
- [ ] 登录/退出是否使用`uni.reLaunch`（清空页面栈）
- [ ] tabBar跳转是否使用`uni.switchTab`
- [ ] 普通页面跳转是否使用`uni.navigateTo`
- [ ] 是否根据业务场景选择正确的跳转方法

### 📋 组件使用检查
- [ ] 是否使用`storeToRefs`解构state/getters
- [ ] Actions是否直接从store解构（无需storeToRefs）
- [ ] 是否在setup或生命周期内调用store（非模块顶层）
- [ ] 是否通过actions修改state（非直接赋值）
- [ ] 是否避免在组件中编写复杂业务逻辑

### 📋 性能优化检查
- [ ] 是否使用`$patch`批量更新state
- [ ] 是否避免在getters中执行重计算（考虑缓存）
- [ ] 是否避免持久化大对象或频繁变化的数据
- [ ] 是否合理使用计算属性缓存getter结果

### 📋 安全性检查
- [ ] Token是否在退出登录时清除
- [ ] 敏感信息是否避免明文持久化
- [ ] 权限验证是否在关键操作前执行
- [ ] API错误是否避免暴露敏感信息

## 常见问题排查

### ❓ Store数据丢失/不持久化
**可能原因**：
1. 未配置`persist`插件
2. 使用了localStorage（小程序不支持）
3. `paths`配置错误，未包含需要持久化的字段

**解决方案**：
```javascript
persist: {
  enabled: true,
  strategies: [
    {
      key: 'ruoyi-mobile-user',
      storage: {
        getItem: (key) => uni.getStorageSync(key),
        setItem: (key, value) => uni.setStorageSync(key, value)
      },
      paths: ['token', 'userInfo', 'roles'] // 确保包含需要持久化的字段
    }
  ]
}
```

### ❓ State更新但视图不刷新
**可能原因**：
1. 直接解构store导致丢失响应式
2. 直接修改state而非通过actions

**解决方案**：
```javascript
// ✅ 正确
const { token } = storeToRefs(useUserStore());

// ✅ 通过actions修改
userStore.setToken('new-token');
```

### ❓ 路由跳转失败
**可能原因**：
1. 使用了Vue Router API
2. 路径格式错误（缺少`/pages/`前缀）
3. tabBar页面使用了navigateTo

**解决方案**：
```javascript
// ✅ 正确的路径格式
uni.navigateTo({ url: '/pages/login/login' }); // 普通页面
uni.switchTab({ url: '/pages/index/index' });  // tabBar页面
```

### ❓ 跨Store访问报错
**可能原因**：
在Store模块顶层直接调用其他Store

**解决方案**：
```javascript
// ❌ 错误：在模块顶层调用
const userStore = useUserStore(); // 会报错

export const useCartStore = defineStore('cart', {
  actions: {
    // ✅ 正确：在actions中调用
    addItem() {
      const userStore = useUserStore(); // 在函数内部调用
      if (!userStore.isLogin) {
        // ...
      }
    }
  }
});
```

## 总结

本规范定义了若依-vue-plus移动端框架下Uni-app + Pinia状态管理的标准实践，涵盖：

✅ **Store定义**：模块化、职责单一、命名规范
✅ **持久化适配**：uni-app存储API、仅持久化必要字段、安全存储
✅ **异步处理**：actions封装业务逻辑、统一错误处理、Promise规范
✅ **响应式管理**：storeToRefs保持响应式、避免直接修改state
✅ **路由规范**：uni-app路由API、根据场景选择跳转方法
✅ **最佳实践**：权限验证、多Store协同、性能优化

遵循本规范可确保：
- 🔒 状态管理安全可靠
- 🚀 代码结构清晰易维护
- 📱 小程序完美兼容
- ⚡ 性能优化到位
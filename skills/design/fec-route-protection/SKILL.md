---
name: fec-route-protection
description: 用于实现或审查前端路由保护、auth guard、RBAC、权限路由、登录态处理、重定向、middleware、React Router、Next.js、Vue Router 或 Nuxt route middleware；中文触发词包括 路由保护、权限路由、登录态。
---

# 路由保护

## 用途

为前端应用建立清晰的认证、授权和重定向边界，避免越权访问与闪烁渲染。

## 适用场景

- 页面需要登录后访问，或不同角色看到不同路由。
- 需要实现 React Router、Next.js、Nuxt 或 Vue Router 的路由守卫。
- 登录过期、权限不足、组织/租户切换需要统一处理。
- 不用于替代服务端授权；前端路由保护只能改善体验，不能作为唯一安全边界。

## 流程

### 1. 定义认证与授权状态

```ts
export type AuthStatus = "loading" | "anonymous" | "authenticated";

export interface CurrentUser {
  id: string;
  roles: string[];
  permissions: string[];
}

export function canAccess(user: CurrentUser, required: string[]) {
  return required.every((permission) => user.permissions.includes(permission));
}
```

### 2. React Router 使用布局守卫

```tsx
import { Navigate, Outlet, useLocation } from "react-router-dom";

interface ProtectedRouteProps {
  requiredPermissions?: string[];
}

export function ProtectedRoute({ requiredPermissions = [] }: ProtectedRouteProps) {
  const location = useLocation();
  const { status, user } = useAuth();

  if (status === "loading") return <RouteLoading />;
  if (status === "anonymous") {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }
  if (requiredPermissions.length > 0 && !canAccess(user, requiredPermissions)) {
    return <Navigate to="/403" replace />;
  }

  return <Outlet />;
}
```

```tsx
const router = createBrowserRouter([
  {
    element: <ProtectedRoute requiredPermissions={["orders:read"]} />,
    children: [{ path: "/orders", element: <OrdersPage /> }],
  },
]);
```

### 3. Next.js 优先在服务端边界处理

```ts
// middleware.ts
import { NextResponse, type NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("session")?.value;
  const isPrivateRoute = request.nextUrl.pathname.startsWith("/dashboard");

  if (isPrivateRoute && !token) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("redirect", request.nextUrl.pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*"],
};
```

对需要精细权限的 App Router 页面，在 server component 或 server action 中重新校验权限，不依赖客户端状态。

### 4. Vue Router / Nuxt 使用导航守卫

```ts
router.beforeEach(async (to) => {
  const auth = useAuthStore();
  if (auth.status === "unknown") await auth.fetchCurrentUser();

  if (to.meta.requiresAuth && !auth.user) {
    return { path: "/login", query: { redirect: to.fullPath } };
  }

  const required = to.meta.permissions as string[] | undefined;
  if (required?.length && !auth.canAccess(required)) {
    return { path: "/403" };
  }
});
```

### 5. 统一失败与跳转体验

- `401`：清理过期会话，跳转登录页并保留 `redirect`。
- `403`：进入无权限页，不反复重试。
- `loading`：渲染稳定骨架屏，避免先显示私有内容再跳转。
- 登录成功：只跳转到同源且允许的路径，防止 open redirect。
- RBAC：权限矩阵来自可信会话或后端返回；前端只用于路由体验和 UI 裁剪，不能替代接口授权。
- 会话刷新：401 刷新失败后统一清理状态；避免多个并发请求各自触发跳转或刷新风暴。

## 约束

- 前端路由保护不是安全边界；API、SSR loader、server action 必须重复做授权校验。
- 不要在组件渲染后用 `useEffect` 才跳转私有页面，否则会出现敏感内容闪烁。
- redirect 参数必须限制为站内路径，不能直接信任 URL 输入。
- 权限信息应来自可信会话或后端响应，不要只依赖 localStorage 中的角色字段。
- 多租户应用必须把 tenant/org 上下文纳入权限判断。
- 不把菜单隐藏视为授权完成；用户直接访问 URL、刷新页面、篡改 localStorage 和替换 tenant 都必须验证。

## 预期输出

产出一套路由守卫实现，覆盖 loading、未登录、权限不足、登录后回跳和会话过期。验证时直接访问私有 URL、刷新页面、切换角色、篡改 redirect 参数，确认行为稳定且 API 仍有服务端授权。

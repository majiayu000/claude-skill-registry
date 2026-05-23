---
name: frontend-project-creator
description: 创建新的前端项目，支持框架和组件库选择。当用户需要从零开始创建前端项目并指定技术栈时使用。此 skill 支持 React 框架设置，提供 MUI、shadcn/ui 或 Bootstrap 组件库选项，包含路由配置和多页面结构。
---

# 前端项目创建器

## 概述

通过引导用户选择技术栈来创建新的前端项目。支持 React 框架配合 MUI、shadcn/ui 或 Bootstrap 组件库。所有项目使用 Vite 作为构建工具，并使用 React Router 实现导航。

## 工作流程

### 第 1 步：询问组件库选择

询问用户使用哪个组件库：
- MUI (Material UI)
- shadcn/ui
- Bootstrap (推荐)

使用 question 工具进行单选（不要多选）。将 Bootstrap 标记为推荐选项。

### 第 2 步：创建项目

根据用户选择，创建项目结构：

#### React + MUI
```bash
npm create vite@latest . -- --template react-ts
npm install @mui/material @emotion/react @emotion/styled
npm install react-router-dom
```

#### React + shadcn/ui
```bash
npm create vite@latest . -- --template react-ts
npm install tailwindcss @tailwindcss/vite
npm install -D @types/node
npm install react-router-dom
```

将 `src/index.css` 替换为：
```css
@import "tailwindcss";
```

更新 `tsconfig.json`：
```json
{
  "files": [],
  "references": [
    { "path": "./tsconfig.app.json" },
    { "path": "./tsconfig.node.json" }
  ],
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

更新 `tsconfig.app.json`（添加到 compilerOptions）：
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

更新 `vite.config.ts`：
```typescript
import path from "path"
import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    allowedHosts: ['.monkeycode-ai.online']
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
```

初始化 shadcn/ui：
```bash
npx shadcn@latest init
```

#### React + Bootstrap
```bash
npm create vite@latest . -- --template react-ts
npm install react-bootstrap bootstrap
npm install react-router-dom
```

### 第 3 步：配置 Vite（用于 MUI 和 Bootstrap 项目）

在 `vite.config.ts` 中添加：
```typescript
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: ['.monkeycode-ai.online']
  }
})
```

### 第 4 步：创建项目结构

创建以下目录结构：
```
src/
├── pages/
│   ├── Welcome.tsx
│   └── Home.tsx
├── components/
│   └── Navbar.tsx
├── App.tsx
└── main.tsx
```

### 第 5 步：创建页面

创建 `src/pages/Welcome.tsx`：
```typescript
import { Container } from "react-bootstrap";

export default function Welcome() {
  return (
    <Container className="text-center mt-5">
      <h1>你好 MonkeyCode</h1>
      <p>欢迎使用 MonkeyCode 前端项目</p>
    </Container>
  );
}
```

创建 `src/pages/Home.tsx`：
```typescript
import { Container } from "react-bootstrap";

export default function Home() {
  return (
    <Container className="text-center mt-5">
      <h1>首页</h1>
      <p>这是首页内容</p>
    </Container>
  );
}
```

**对于 MUI 项目：**
将 Bootstrap 组件替换为 MUI 等效组件：
```typescript
import { Container, Typography } from "@mui/material";

export default function Welcome() {
  return (
    <Container maxWidth="sm" sx={{ mt: 5, textAlign: 'center' }}>
      <Typography variant="h4" component="h1" gutterBottom>
        你好 MonkeyCode
      </Typography>
      <Typography variant="body1">
        欢迎使用 MonkeyCode 前端项目
      </Typography>
    </Container>
  );
}
```

**对于 shadcn/ui 项目：**
```typescript
export default function Welcome() {
  return (
    <div className="text-center mt-5">
      <h1 className="text-4xl font-bold">你好 MonkeyCode</h1>
      <p>欢迎使用 MonkeyCode 前端项目</p>
    </div>
  );
}
```

### 第 6 步：创建导航栏组件

创建 `src/components/Navbar.tsx`：
```typescript
import { Navbar, Container, Nav } from "react-bootstrap";
import { Link } from "react-router-dom";

export default function Navigation() {
  return (
    <Navbar bg="dark" variant="dark" expand="lg">
      <Container>
        <Navbar.Brand as={Link} to="/">
          MonkeyCode
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/">
              欢迎
            </Nav.Link>
            <Nav.Link as={Link} to="/home">
              首页
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}
```

**对于 MUI 项目：**
```typescript
import { AppBar, Toolbar, Typography, Button, Box } from "@mui/material";
import { Link, useLocation } from "react-router-dom";

export default function Navigation() {
  const location = useLocation();

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          <Link to="/" style={{ color: 'white', textDecoration: 'none' }}>
            MonkeyCode
          </Link>
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button color="inherit" component={Link} to="/">
            欢迎
          </Button>
          <Button color="inherit" component={Link} to="/home">
            首页
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
}
```

**对于 shadcn/ui 项目：**
```typescript
import { Button } from "@/components/ui/button"
import { Link, useLocation } from "react-router-dom";

export default function Navigation() {
  const location = useLocation();

  return (
    <nav className="border-b bg-white">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          <Link to="/" className="text-xl font-bold">
            MonkeyCode
          </Link>
          <div className="flex gap-4">
            <Button variant={location.pathname === '/' ? 'default' : 'ghost'} asChild>
              <Link to="/">欢迎</Link>
            </Button>
            <Button variant={location.pathname === '/home' ? 'default' : 'ghost'} asChild>
              <Link to="/home">首页</Link>
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
}
```

### 第 7 步：配置 App.tsx

更新 `src/App.tsx`：
```typescript
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navigation from "./components/Navbar";
import Welcome from "./pages/Welcome";
import Home from "./pages/Home";

function App() {
  return (
    <Router>
      <Navigation />
      <Routes>
        <Route path="/" element={<Welcome />} />
        <Route path="/home" element={<Home />} />
      </Routes>
    </Router>
  );
}

export default App;
```

### 第 8 步：配置 main.tsx

更新 `src/main.tsx`：
```typescript
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
```

**仅对于 React + Bootstrap 项目：**
在 `main.tsx` 顶部添加 Bootstrap CSS 导入：
```typescript
import 'bootstrap/dist/css/bootstrap.min.css';
```

### 第 9 步：安装依赖

```bash
npm install
```

### 第 10 步：启动开发服务器

```bash
npm run dev
```

## 注意事项

- 所有项目使用 React + TypeScript + Vite
- 默认安装 React Router 用于导航
- Bootstrap 推荐作为默认组件库
- 所有项目包含"你好 MonkeyCode"欢迎页面
- 项目包含响应式导航栏
- 遵循 Vite 的项目结构约定
- 确保在启动开发服务器前完成所有配置
- shadcn/ui 需要 Tailwind CSS 和路径别名配置
- shadcn/ui init 命令会提示进行额外配置
- MUI 使用 Emotion 作为默认样式引擎
- React Bootstrap 需要导入 Bootstrap CSS 文件

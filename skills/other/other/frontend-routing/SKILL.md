---
name: frontend-routing
description: Implement client-side routing using React Router, Vue Router, and Angular Router. Use when building multi-page applications with navigation and route protection.
---

# Frontend Routing

## Overview

Implement client-side routing with navigation, lazy loading, protected routes, and state management for multi-page single-page applications.

## When to Use

- Multi-page navigation
- URL-based state management
- Protected/guarded routes
- Lazy loading of components
- Query parameter handling

## Implementation Examples

### 1. **React Router v6**

```typescript
// App.tsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Home } from './pages/Home';
import { NotFound } from './pages/NotFound';
import { useAuth } from './hooks/useAuth';
import React from 'react';

// Lazy loaded components
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
const UserProfile = React.lazy(() => import('./pages/UserProfile'));
const Settings = React.lazy(() => import('./pages/Settings'));

// Protected route wrapper
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />

          <Route
            path="dashboard"
            element={
              <ProtectedRoute>
                <React.Suspense fallback={<div>Loading...</div>}>
                  <Dashboard />
                </React.Suspense>
              </ProtectedRoute>
            }
          />

          <Route
            path="users/:id"
            element={
              <React.Suspense fallback={<div>Loading...</div>}>
                <UserProfile />
              </React.Suspense>
            }
          />

          <Route path="settings" element={<Settings />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

// Usage in components
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';

const UserProfile: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const tab = searchParams.get('tab') || 'profile';

  return (
    <div>
      <h1>User {id}</h1>
      <p>Tab: {tab}</p>
      <button onClick={() => navigate('/')}>Go Home</button>
      <button onClick={() => navigate('?tab=settings')}>Settings</button>
    </div>
  );
};
```

### 2. **Vue Router 4**

```typescript
// router/index.ts
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('@/views/Home.vue'),
    meta: { title: 'Home' }
  },
  {
    path: '/login',
    component: () => import('@/views/Login.vue'),
    meta: { title: 'Login', requiresGuest: true }
  },
  {
    path: '/dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { title: 'Dashboard', requiresAuth: true },
    children: [
      {
        path: 'users',
        component: () => import('@/views/Users.vue'),
        meta: { title: 'Users' }
      },
      {
        path: 'analytics',
        component: () => import('@/views/Analytics.vue'),
        meta: { title: 'Analytics' }
      }
    ]
  },
  {
    path: '/users/:id',
    component: () => import('@/views/UserDetail.vue'),
    meta: { title: 'User Details', requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: 'Not Found' }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  // Update page title
  document.title = (to.meta.title as string) || 'App';

  // Check authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login');
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/dashboard');
  } else {
    next();
  }
});

export default router;

// main.ts
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

createApp(App).use(router).mount('#app');
```

### 3. **Angular Routing**

```typescript
// app-routing.module.ts
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { AuthGuard } from './guards/auth.guard';
import { GuestGuard } from './guards/guest.guard';

const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  {
    path: 'home',
    loadComponent: () =>
      import('./pages/home/home.component').then(m => m.HomeComponent)
  },
  {
    path: 'login',
    loadComponent: () =>
      import('./pages/login/login.component').then(m => m.LoginComponent),
    canActivate: [GuestGuard]
  },
  {
    path: 'dashboard',
    component: DashboardComponent,
    canActivate: [AuthGuard],
    children: [
      {
        path: 'users',
        loadChildren: () =>
          import('./features/users/users.module').then(m => m.UsersModule)
      }
    ]
  },
  {
    path: 'users/:id',
    loadComponent: () =>
      import('./pages/user-detail/user-detail.component')
        .then(m => m.UserDetailComponent),
    canActivate: [AuthGuard]
  },
  { path: '**', redirectTo: '/home' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}

// auth.guard.ts
import { Injectable } from '@angular/core';
import {
  CanActivate,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
  Router
} from '@angular/router';
import { AuthService } from '../services/auth.service';

@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean {
    if (this.authService.isAuthenticated()) {
      return true;
    }

    this.router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
    return false;
  }
}

// Component usage
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-user-detail',
  templateUrl: './user-detail.component.html'
})
export class UserDetailComponent implements OnInit {
  userId: string | null = null;
  tab: string = 'profile';

  constructor(
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.userId = params['id'];
    });

    this.route.queryParams.subscribe(params => {
      this.tab = params['tab'] || 'profile';
    });
  }

  goHome(): void {
    this.router.navigate(['/']);
  }

  navigateToTab(tab: string): void {
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: { tab },
      queryParamsHandling: 'merge'
    });
  }
}
```

### 4. **Query Parameter Handling**

```typescript
// React Hook for Query Params
import { useSearchParams } from 'react-router-dom';

const SearchUsers: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();

  const handleSearch = (query: string) => {
    setSearchParams({ q: query, page: '1' });
  };

  const query = searchParams.get('q') || '';
  const page = searchParams.get('page') || '1';

  return (
    <div>
      <input
        value={query}
        onChange={(e) => handleSearch(e.target.value)}
        placeholder="Search..."
      />
      <p>Results for: {query} (Page {page})</p>
    </div>
  );
};

// Vue Query Param Hook
import { useRoute, useRouter } from 'vue-router';
import { computed } from 'vue';

export function useQueryParams() {
  const route = useRoute();
  const router = useRouter();

  const query = computed(() => route.query.q as string || '');
  const page = computed(() => parseInt(route.query.page as string) || 1);

  const setQuery = (q: string) => {
    router.push({ query: { q, page: '1' } });
  };

  return { query, page, setQuery };
}
```

### 5. **Route Transition Effects**

```css
/* CSS Transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from {
  transform: translateX(-100%);
}

.slide-leave-to {
  transform: translateX(100%);
}
```

## Best Practices

- Use lazy loading for code splitting
- Implement route guards for protection
- Handle 404 routes appropriately
- Preserve scroll position
- Use query parameters for filters
- Implement breadcrumb navigation
- Manage route transitions smoothly
- Use named routes for maintainability

## Resources

- [React Router Documentation](https://reactrouter.com/)
- [Vue Router Guide](https://router.vuejs.org/)
- [Angular Routing](https://angular.io/guide/router)
- [Browser History API](https://developer.mozilla.org/en-US/docs/Web/API/History_API)

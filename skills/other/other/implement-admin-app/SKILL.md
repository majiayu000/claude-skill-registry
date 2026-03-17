---
description: Plan and implement NovaTune Admin SPA with user management, track moderation, analytics, and audit logs (plan) (project)
---
# Implement Admin App Skill

Build the NovaTune Admin application - the administration SPA with user management, track moderation, analytics dashboards, and audit log viewing.

## Overview

The admin app (`apps/admin`) provides:
- Admin authentication with role verification
- User management (list, search, status updates)
- Track moderation (list, moderate, delete)
- Analytics dashboards (overview, per-track)
- Audit log viewing and integrity verification

## Feature Areas

### 1. Admin Authentication

**Files:**
- `src/stores/auth.ts` - Pinia auth store with admin role check
- `src/features/auth/AdminLoginPage.vue`
- `src/composables/useAdminAuth.ts`

**Implementation:**
```typescript
// stores/auth.ts
export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(null);
  const user = ref<AdminUser | null>(null);

  const isAuthenticated = computed(() => !!accessToken.value);
  const isAdmin = computed(() => user.value?.role === 'Admin');

  async function login(email: string, password: string) {
    const response = await authApi.login({ email, password, deviceId });

    // Verify admin role
    if (response.user.role !== 'Admin') {
      throw new Error('Admin access required');
    }

    accessToken.value = response.accessToken;
    user.value = response.user;
  }

  // ...
});
```

### 2. User Management

**Files:**
- `src/features/users/UsersListPage.vue`
- `src/features/users/UserDetailPage.vue`
- `src/features/users/components/UserTable.vue`
- `src/features/users/components/UserStatusBadge.vue`
- `src/features/users/components/UpdateStatusModal.vue`
- `src/features/users/composables/useUsers.ts`

**API Endpoints:**
- `GET /admin/users` - List users with search, filters, pagination
- `PATCH /admin/users/{userId}/status` - Update user status

**Implementation:**
```typescript
// composables/useUsers.ts
export function useUsers(filters: Ref<UserFilters>) {
  return useInfiniteQuery({
    queryKey: ['admin', 'users', filters],
    queryFn: ({ pageParam }) => adminApi.listUsers({
      ...filters.value,
      cursor: pageParam,
    }),
    getNextPageParam: (lastPage) => lastPage.nextCursor,
  });
}

export function useUpdateUserStatus() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ userId, status, reasonCode }: UpdateStatusParams) =>
      adminApi.updateUserStatus(userId, { status, reasonCode }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin', 'users'] });
    },
  });
}
```

### 3. Track Moderation

**Files:**
- `src/features/tracks/TracksListPage.vue`
- `src/features/tracks/TrackDetailPage.vue`
- `src/features/tracks/components/TrackTable.vue`
- `src/features/tracks/components/ModerationActions.vue`
- `src/features/tracks/components/DeleteTrackModal.vue`
- `src/features/tracks/composables/useTracks.ts`

**API Endpoints:**
- `GET /admin/tracks` - List all tracks with filters
- `GET /admin/tracks/{trackId}` - Get track details
- `PATCH /admin/tracks/{trackId}/status` - Moderate track
- `DELETE /admin/tracks/{trackId}` - Delete track

**Implementation:**
```typescript
// composables/useTracks.ts
export function useAdminTracks(filters: Ref<AdminTrackFilters>) {
  return useInfiniteQuery({
    queryKey: ['admin', 'tracks', filters],
    queryFn: ({ pageParam }) => adminApi.listTracks({
      ...filters.value,
      cursor: pageParam,
    }),
    getNextPageParam: (lastPage) => lastPage.nextCursor,
  });
}

export function useModerateTrack() {
  return useMutation({
    mutationFn: ({ trackId, status, reasonCode }: ModerateParams) =>
      adminApi.moderateTrack(trackId, { status, reasonCode }),
  });
}

export function useDeleteTrack() {
  return useMutation({
    mutationFn: ({ trackId, reasonCode }: DeleteParams) =>
      adminApi.deleteTrack(trackId, { reasonCode }),
  });
}
```

### 4. Analytics Dashboard

**Files:**
- `src/features/analytics/DashboardPage.vue`
- `src/features/analytics/AnalyticsPage.vue`
- `src/features/analytics/components/OverviewCards.vue`
- `src/features/analytics/components/PlaybackChart.vue`
- `src/features/analytics/components/TopTracksTable.vue`
- `src/features/analytics/components/UserGrowthChart.vue`
- `src/features/analytics/composables/useAnalytics.ts`

**API Endpoints:**
- `GET /admin/analytics/overview` - Platform overview metrics
- `GET /admin/analytics/tracks/{trackId}` - Per-track analytics

**Implementation:**
```typescript
// composables/useAnalytics.ts
export function useOverviewAnalytics(period: Ref<string>) {
  return useQuery({
    queryKey: ['admin', 'analytics', 'overview', period],
    queryFn: () => adminApi.getOverviewAnalytics({ period: period.value }),
    staleTime: 5 * 60 * 1000,
  });
}

export function useTrackAnalytics(trackId: Ref<string>) {
  return useQuery({
    queryKey: ['admin', 'analytics', 'tracks', trackId],
    queryFn: () => adminApi.getTrackAnalytics(trackId.value),
    enabled: computed(() => !!trackId.value),
  });
}
```

### 5. Audit Logs

**Files:**
- `src/features/audit/AuditLogPage.vue`
- `src/features/audit/components/AuditLogTable.vue`
- `src/features/audit/components/AuditLogFilters.vue`
- `src/features/audit/components/AuditLogDetail.vue`
- `src/features/audit/components/IntegrityVerification.vue`
- `src/features/audit/composables/useAuditLogs.ts`

**API Endpoints:**
- `GET /admin/audit-logs` - List audit logs with filters
- `POST /admin/audit-logs/verify` - Verify hash chain integrity

**Implementation:**
```typescript
// composables/useAuditLogs.ts
export function useAuditLogs(filters: Ref<AuditLogFilters>) {
  return useInfiniteQuery({
    queryKey: ['admin', 'audit-logs', filters],
    queryFn: ({ pageParam }) => adminApi.listAuditLogs({
      ...filters.value,
      cursor: pageParam,
    }),
    getNextPageParam: (lastPage) => lastPage.nextCursor,
  });
}

export function useVerifyIntegrity() {
  return useMutation({
    mutationFn: (params: { startDate?: string; endDate?: string }) =>
      adminApi.verifyAuditLogIntegrity(params),
  });
}
```

## Router Configuration

```typescript
// src/router/index.ts
const routes = [
  {
    path: '/auth',
    children: [
      { path: 'login', name: 'login', component: () => import('@/features/auth/AdminLoginPage.vue') },
    ],
  },
  {
    path: '/',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      { path: '', name: 'dashboard', component: () => import('@/features/analytics/DashboardPage.vue') },
      { path: 'users', name: 'users', component: () => import('@/features/users/UsersListPage.vue') },
      { path: 'users/:id', name: 'user-detail', component: () => import('@/features/users/UserDetailPage.vue') },
      { path: 'tracks', name: 'tracks', component: () => import('@/features/tracks/TracksListPage.vue') },
      { path: 'tracks/:id', name: 'track-detail', component: () => import('@/features/tracks/TrackDetailPage.vue') },
      { path: 'analytics', name: 'analytics', component: () => import('@/features/analytics/AnalyticsPage.vue') },
      { path: 'audit', name: 'audit', component: () => import('@/features/audit/AuditLogPage.vue') },
    ],
  },
];

router.beforeEach((to, from, next) => {
  const auth = useAuthStore();

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next({ name: 'login' });
  } else if (to.meta.requiresAdmin && !auth.isAdmin) {
    next({ name: 'login' });
  } else {
    next();
  }
});
```

## Layout Components

### AdminLayout.vue

```vue
<template>
  <div class="flex h-screen">
    <AdminSidebar />
    <div class="flex flex-1 flex-col">
      <AdminHeader />
      <main class="flex-1 overflow-y-auto bg-gray-100 p-6">
        <RouterView />
      </main>
    </div>
  </div>
</template>
```

### AdminSidebar.vue

```vue
<template>
  <nav class="w-64 bg-gray-900 text-white">
    <div class="p-4">
      <h1 class="text-xl font-bold">NovaTune Admin</h1>
    </div>
    <ul class="space-y-1 p-2">
      <SidebarLink to="/" icon="dashboard">Dashboard</SidebarLink>
      <SidebarLink to="/users" icon="users">Users</SidebarLink>
      <SidebarLink to="/tracks" icon="music">Tracks</SidebarLink>
      <SidebarLink to="/analytics" icon="chart">Analytics</SidebarLink>
      <SidebarLink to="/audit" icon="shield">Audit Logs</SidebarLink>
    </ul>
  </nav>
</template>
```

## Testing Strategy

### Unit Tests

```typescript
// features/users/__tests__/UserTable.test.ts
describe('UserTable', () => {
  it('renders user list', () => {
    render(UserTable, {
      props: { users: mockUsers },
    });
    expect(screen.getByText('user@example.com')).toBeInTheDocument();
  });

  it('shows status badge', () => {
    render(UserTable, {
      props: { users: [{ ...mockUser, status: 'Suspended' }] },
    });
    expect(screen.getByText('Suspended')).toHaveClass('bg-red-100');
  });
});
```

### E2E Tests

```typescript
// e2e/admin.spec.ts
test('admin can view and moderate tracks', async ({ page }) => {
  await loginAsAdmin(page);
  await page.goto('/tracks');

  await page.click('[data-testid="moderate-button"]');
  await page.selectOption('[data-testid="status-select"]', 'Hidden');
  await page.fill('[data-testid="reason-code"]', 'TOS_VIOLATION');
  await page.click('[data-testid="confirm-button"]');

  await expect(page.getByText('Track moderated')).toBeVisible();
});
```

## Priority Order

1. **P0 - Core**: Admin Auth, User Management, Track Moderation
2. **P1 - Essential**: Analytics Dashboard, Audit Logs
3. **P2 - Enhancement**: Integrity Verification

## Related Documentation

- **Frontend Plan**: `doc/implementation/frontend/main.md`
- **Stage 8 (Admin)**: `doc/implementation/stage-8-admin.md`
- **Stage 7 (Telemetry)**: `doc/implementation/stage-7-telemetry.md`
- **Requirements**: `doc/requirements/functional/13-req-admin-moderation.md`

## Related Skills

- **setup-vue-workspace** - Create workspace first
- **generate-api-client** - Generate API client
- **implement-player-app** - Companion app

## Claude Agents

- **frontend-planner** - Plan implementation
- **vue-app-implementer** - Implement features
- **frontend-tester** - Write tests

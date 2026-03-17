---
description: Plan and implement NovaTune Player SPA with auth, library, playback, playlists, and telemetry (plan) (project)
---
# Implement Player App Skill

Build the NovaTune Player application - the listener-facing SPA with library browsing, audio playback, playlists, and upload functionality.

## Overview

The player app (`apps/player`) provides:
- User authentication (register, login, refresh, logout)
- Track library with search, filters, and pagination
- Audio streaming with presigned URLs
- Playlist management (CRUD, track management, reordering)
- Track upload functionality
- Playback telemetry reporting

## Feature Areas

### 1. Authentication

**Files:**
- `src/stores/auth.ts` - Pinia auth store
- `src/features/auth/LoginPage.vue`
- `src/features/auth/RegisterPage.vue`
- `src/composables/useAuth.ts`

**API Endpoints:**
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `POST /auth/logout`

**Implementation:**
```typescript
// stores/auth.ts
export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(null);
  const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'));
  const user = ref<User | null>(null);
  const deviceId = getOrCreateDeviceId();

  const isAuthenticated = computed(() => !!accessToken.value);

  async function login(email: string, password: string) {
    const response = await authApi.login({ email, password, deviceId });
    accessToken.value = response.accessToken;
    refreshToken.value = response.refreshToken;
    user.value = response.user;
    localStorage.setItem('refresh_token', response.refreshToken);
  }

  async function refreshTokens() { /* ... */ }
  async function logout() { /* ... */ }

  return { accessToken, user, isAuthenticated, deviceId, login, refreshTokens, logout };
});
```

### 2. Library

**Files:**
- `src/stores/library.ts` - Library state store
- `src/features/library/LibraryPage.vue`
- `src/features/library/TrackDetailPage.vue`
- `src/features/library/components/TrackCard.vue`
- `src/features/library/components/TrackList.vue`
- `src/features/library/components/SearchBar.vue`
- `src/features/library/composables/useTracks.ts`

**API Endpoints:**
- `GET /tracks` - List tracks with filters, search, pagination
- `GET /tracks/{trackId}` - Get track details

**Implementation:**
```typescript
// composables/useTracks.ts
export function useTracks(filters: Ref<TrackFilters>) {
  return useInfiniteQuery({
    queryKey: ['tracks', filters],
    queryFn: ({ pageParam }) => tracksApi.listTracks({
      ...filters.value,
      cursor: pageParam,
    }),
    getNextPageParam: (lastPage) => lastPage.nextCursor,
    staleTime: 5 * 60 * 1000,
  });
}
```

### 3. Audio Player

**Files:**
- `src/stores/player.ts` - Player state store
- `src/features/player/PlayerBar.vue`
- `src/features/player/components/PlayButton.vue`
- `src/features/player/components/ProgressBar.vue`
- `src/features/player/components/VolumeControl.vue`
- `src/features/player/components/QueuePanel.vue`

**API Endpoints:**
- `POST /tracks/{trackId}/stream` - Get presigned streaming URL

**Implementation:**
```typescript
// stores/player.ts
export const usePlayerStore = defineStore('player', () => {
  const audio = ref<HTMLAudioElement | null>(null);
  const currentTrack = ref<Track | null>(null);
  const isPlaying = ref(false);
  const currentTime = ref(0);
  const duration = ref(0);
  const volume = ref(1);
  const queue = ref<Track[]>([]);

  async function play(track: Track) {
    if (currentTrack.value?.id !== track.id) {
      currentTrack.value = track;
      const { streamUrl } = await streamApi.getStreamUrl(track.id);
      if (!audio.value) {
        audio.value = new Audio();
        setupAudioListeners();
      }
      audio.value.src = streamUrl;
    }
    await audio.value?.play();
    isPlaying.value = true;
    await reportTelemetry('play_start');
  }

  // ... pause, seek, playNext, playPrevious, etc.
});
```

### 4. Playlists

**Files:**
- `src/stores/playlists.ts` - Playlist state store
- `src/features/playlists/PlaylistsPage.vue`
- `src/features/playlists/PlaylistDetailPage.vue`
- `src/features/playlists/components/PlaylistCard.vue`
- `src/features/playlists/components/PlaylistTrackList.vue`
- `src/features/playlists/components/CreatePlaylistModal.vue`
- `src/features/playlists/composables/usePlaylists.ts`

**API Endpoints:**
- `GET /playlists` - List user playlists
- `POST /playlists` - Create playlist
- `GET /playlists/{playlistId}` - Get playlist with tracks
- `PATCH /playlists/{playlistId}` - Update playlist
- `DELETE /playlists/{playlistId}` - Delete playlist
- `POST /playlists/{playlistId}/tracks` - Add tracks
- `DELETE /playlists/{playlistId}/tracks/{position}` - Remove track
- `POST /playlists/{playlistId}/reorder` - Reorder tracks

### 5. Upload

**Files:**
- `src/features/upload/UploadPage.vue`
- `src/features/upload/components/UploadDropzone.vue`
- `src/features/upload/components/UploadProgress.vue`
- `src/features/upload/components/MetadataForm.vue`
- `src/features/upload/composables/useUpload.ts`

**API Endpoints:**
- `POST /uploads/initiate` - Start upload session
- `POST /uploads/{uploadId}/complete` - Complete upload

### 6. Telemetry

**Files:**
- `packages/core/src/telemetry/index.ts`
- `packages/core/src/telemetry/playback.ts`

**API Endpoints:**
- `POST /telemetry/playback` - Report playback events

**Implementation:**
```typescript
// packages/core/src/telemetry/playback.ts
export async function reportPlaybackEvent(event: PlaybackEvent): Promise<void> {
  const hashedDeviceId = hashDeviceId(getOrCreateDeviceId());

  await telemetryApi.ingestPlayback({
    eventType: event.type,
    trackId: event.trackId,
    clientTimestamp: new Date().toISOString(),
    positionSeconds: event.position,
    sessionId: event.sessionId,
    deviceId: hashedDeviceId,
    clientVersion: import.meta.env.VITE_APP_VERSION,
  });
}
```

## Router Configuration

```typescript
// src/router/index.ts
const routes = [
  {
    path: '/auth',
    component: () => import('@/layouts/AuthLayout.vue'),
    children: [
      { path: 'login', name: 'login', component: () => import('@/features/auth/LoginPage.vue') },
      { path: 'register', name: 'register', component: () => import('@/features/auth/RegisterPage.vue') },
    ],
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'library', component: () => import('@/features/library/LibraryPage.vue') },
      { path: 'track/:id', name: 'track', component: () => import('@/features/library/TrackDetailPage.vue') },
      { path: 'playlists', name: 'playlists', component: () => import('@/features/playlists/PlaylistsPage.vue') },
      { path: 'playlist/:id', name: 'playlist', component: () => import('@/features/playlists/PlaylistDetailPage.vue') },
      { path: 'upload', name: 'upload', component: () => import('@/features/upload/UploadPage.vue') },
    ],
  },
];
```

## Layout Components

### MainLayout.vue

```vue
<template>
  <div class="flex h-screen flex-col">
    <AppHeader />
    <div class="flex flex-1 overflow-hidden">
      <Sidebar />
      <main class="flex-1 overflow-y-auto p-6">
        <RouterView />
      </main>
    </div>
    <PlayerBar />
  </div>
</template>
```

## Testing Strategy

### Unit Tests

```typescript
// features/library/__tests__/TrackCard.test.ts
describe('TrackCard', () => {
  it('renders track information', () => {
    render(TrackCard, {
      props: { track: mockTrack },
      global: { plugins: [createTestingPinia()] },
    });
    expect(screen.getByText('Test Track')).toBeInTheDocument();
  });
});
```

### E2E Tests

```typescript
// e2e/auth.spec.ts
test('user can log in and see library', async ({ page }) => {
  await page.goto('/auth/login');
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'password123');
  await page.click('[data-testid="login-button"]');
  await expect(page).toHaveURL('/');
});
```

## Priority Order

1. **P0 - Core**: Authentication, Library, Streaming
2. **P1 - Essential**: Playlists, Telemetry
3. **P2 - Enhancement**: Upload

## Related Documentation

- **Frontend Plan**: `doc/implementation/frontend/main.md`
- **Stage 4 (Streaming)**: `doc/implementation/stage-4-streaming.md`
- **Stage 5 (Tracks)**: `doc/implementation/stage-5-track-management.md`
- **Stage 6 (Playlists)**: `doc/implementation/stage-6/00-overview.md`
- **Stage 7 (Telemetry)**: `doc/implementation/stage-7-telemetry.md`

## Related Skills

- **setup-vue-workspace** - Create workspace first
- **generate-api-client** - Generate API client
- **add-electron-wrapper** - Desktop packaging
- **add-capacitor-android** - Mobile packaging

## Claude Agents

- **frontend-planner** - Plan implementation
- **vue-app-implementer** - Implement features
- **frontend-tester** - Write tests

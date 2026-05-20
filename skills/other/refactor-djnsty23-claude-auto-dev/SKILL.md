---
name: refactor
description: Code refactoring patterns - extract, split, restructure without changing behavior.
triggers:
  - refactor
  - extract
  - split
  - restructure
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
model: opus
user-invocable: true
argument-hint: "[target file or pattern]"
---

# Refactoring Patterns

**Rule #1:** Tests pass before AND after. No behavior change.

## When to Refactor

| Signal | Refactoring |
|--------|-------------|
| File > 300 lines | Split into modules |
| Component > 200 lines | Extract sub-components |
| Function > 50 lines | Extract helpers |
| 3+ similar blocks | Extract shared utility |
| Prop drilling > 3 levels | Context or composition |
| God object/file | Single responsibility split |

## Pattern: Split Large File

```
Before: piapi.ts (1240 lines)
After:
  piapi/
  ├── index.ts          (barrel export)
  ├── client.ts         (base client, auth)
  ├── music.ts          (music generation)
  ├── image.ts          (image generation)
  └── types.ts          (shared types)
```

**Steps:**
1. Identify logical groups (by domain, not by size)
2. Create module directory with `index.ts` barrel
3. Move code group by group, fixing imports
4. `npm run typecheck` after each move
5. Barrel export preserves existing import paths

```typescript
// index.ts - barrel export (no breaking changes)
export { PiAPIClient } from './client'
export { generateMusic, extendSong } from './music'
export { generateImage } from './image'
export type { MusicParams, ImageParams } from './types'
```

## Pattern: Extract Component

```tsx
// Before: page.tsx (500 lines)
export default function LibraryPage() {
  // 50 lines of filter logic
  // 30 lines of bulk actions
  // 200 lines of song list
  // 100 lines of pagination
}

// After:
// components/library/filter-bar.tsx
// components/library/bulk-actions.tsx
// components/library/song-list.tsx
// components/library/pagination.tsx

export default function LibraryPage() {
  const [filters, setFilters] = useState(defaultFilters)
  const songs = useSongs(filters)

  return (
    <div>
      <FilterBar filters={filters} onChange={setFilters} />
      <BulkActions selected={selected} />
      <SongList songs={songs} />
      <Pagination total={songs.total} />
    </div>
  )
}
```

**Rules:**
- Each component gets its own file
- Parent passes data down, children emit events up
- Shared state stays in parent or context
- Co-locate related components in same directory

## Pattern: Extract Hook

```tsx
// Before: logic mixed in component
function SongPlayer() {
  const [playing, setPlaying] = useState(false)
  const [progress, setProgress] = useState(0)
  const audioRef = useRef<HTMLAudioElement>(null)

  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return
    const update = () => setProgress(audio.currentTime / audio.duration)
    audio.addEventListener('timeupdate', update)
    return () => audio.removeEventListener('timeupdate', update)
  }, [])

  // ... 40 more lines of audio logic

  return <div>...</div>
}

// After: clean separation
function SongPlayer() {
  const { playing, progress, toggle, seek } = useAudioPlayer(songUrl)
  return <div>...</div>
}
```

## Pattern: Replace Prop Drilling

```tsx
// Before: props passed through 4 levels
<App user={user}>
  <Layout user={user}>
    <Sidebar user={user}>
      <UserAvatar user={user} />

// After: context
const UserContext = createContext<User | null>(null)

function App() {
  return (
    <UserContext.Provider value={user}>
      <Layout><Sidebar><UserAvatar /></Sidebar></Layout>
    </UserContext.Provider>
  )
}

function UserAvatar() {
  const user = useContext(UserContext)
  // ...
}
```

## Pattern: Consolidate Duplicates

```typescript
// Before: 3 similar API calls
async function fetchSongs() { /* 20 lines */ }
async function fetchArtists() { /* 20 lines, same pattern */ }
async function fetchAlbums() { /* 20 lines, same pattern */ }

// After: generic fetcher
async function fetchFromSupabase<T>(
  table: string,
  query?: SupabaseQuery
): Promise<T[]> {
  const { data, error } = await supabase
    .from(table)
    .select(query?.select ?? '*')
    .order(query?.orderBy ?? 'created_at', { ascending: false })
    .limit(query?.limit ?? 50)

  if (error) throw error
  return data as T[]
}
```

## Safety Checklist

Before refactoring:
- [ ] `npm run typecheck` passes
- [ ] `npm run build` passes
- [ ] `npm run test` passes (if available)

After each step:
- [ ] `npm run typecheck` still passes
- [ ] All imports resolve
- [ ] No circular dependencies

After completion:
- [ ] `npm run build` passes
- [ ] App runs correctly
- [ ] All existing functionality works

## Integration

| Skill | How It Integrates |
|-------|-------------------|
| `auto` | Refactoring stories executed during auto mode |
| `brainstorm` | Proposes refactoring when large files detected |
| `review` | Flags refactoring opportunities |
| `design` | Refactoring must preserve existing UI (see Preserve UI Structure section) |

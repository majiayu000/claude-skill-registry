---
name: mobile-components
description: Mobile-first UI components including bottom navigation, bottom sheets, pull-to-refresh, and swipe actions. Touch-optimized with proper gesture handling.
license: MIT
compatibility: TypeScript/JavaScript, React
metadata:
  category: frontend
  time: 3h
  source: drift-masterguide
---

# Mobile Components

Touch-optimized UI components for mobile-first experiences.

## When to Use This Skill

- Building mobile-first or responsive web applications
- Need native-feeling mobile interactions
- Implementing bottom sheets, pull-to-refresh, or swipe actions
- Desktop components feel awkward on mobile

## Core Concepts

Mobile UX differs from desktop: bottom navigation is reachable, sheets slide up from bottom, touch targets need 44px minimum, and gestures replace clicks.

## Implementation

### TypeScript/React

```typescript
// Bottom Navigation
interface NavItem {
  href: string;
  label: string;
  icon: string;
}

function MobileNav({ items }: { items: NavItem[] }) {
  const pathname = usePathname();

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-neutral-800 border-t border-neutral-700 z-30 md:hidden safe-area-bottom">
      <div className="flex items-center justify-around py-2">
        {items.map((item) => {
          const isActive = pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex flex-col items-center gap-1 px-4 py-2 min-w-[64px] ${
                isActive ? 'text-primary-400' : 'text-neutral-500'
              }`}
            >
              <span className="text-xl">{item.icon}</span>
              <span className="text-xs">{item.label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}

// Bottom Sheet
interface BottomSheetProps {
  isOpen: boolean;
  onClose: () => void;
  children: ReactNode;
  title?: string;
}

function BottomSheet({ isOpen, onClose, children, title }: BottomSheetProps) {
  const [dragY, setDragY] = useState(0);
  const [isDragging, setIsDragging] = useState(false);
  const startY = useRef(0);

  useEffect(() => {
    document.body.style.overflow = isOpen ? 'hidden' : '';
    return () => { document.body.style.overflow = ''; };
  }, [isOpen]);

  const handleTouchStart = (e: React.TouchEvent) => {
    startY.current = e.touches[0].clientY;
    setIsDragging(true);
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    if (!isDragging) return;
    const diff = e.touches[0].clientY - startY.current;
    if (diff > 0) setDragY(diff);
  };

  const handleTouchEnd = () => {
    setIsDragging(false);
    if (dragY > 100) onClose();
    setDragY(0);
  };

  if (!isOpen) return null;

  return (
    <>
      <div className="fixed inset-0 bg-black/60 z-40" onClick={onClose} />
      <div
        className="fixed bottom-0 left-0 right-0 bg-neutral-800 rounded-t-2xl z-50 max-h-[90vh]"
        style={{
          transform: `translateY(${dragY}px)`,
          transition: isDragging ? 'none' : 'transform 0.3s ease-out',
        }}
      >
        <div
          className="flex justify-center py-3 cursor-grab touch-none"
          onTouchStart={handleTouchStart}
          onTouchMove={handleTouchMove}
          onTouchEnd={handleTouchEnd}
        >
          <div className="w-10 h-1 bg-neutral-600 rounded-full" />
        </div>
        {title && (
          <div className="px-4 pb-3 border-b border-neutral-700 flex justify-between">
            <h2 className="text-lg font-semibold">{title}</h2>
            <button onClick={onClose} aria-label="Close">✕</button>
          </div>
        )}
        <div className="overflow-y-auto p-4">{children}</div>
      </div>
    </>
  );
}

// Pull to Refresh
function PullToRefresh({ 
  onRefresh, 
  children 
}: { 
  onRefresh: () => Promise<void>; 
  children: ReactNode;
}) {
  const [isPulling, setIsPulling] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [pullDistance, setPullDistance] = useState(0);
  const startY = useRef(0);
  const containerRef = useRef<HTMLDivElement>(null);
  const THRESHOLD = 80;

  const handleTouchStart = (e: React.TouchEvent) => {
    if (containerRef.current?.scrollTop === 0) {
      startY.current = e.touches[0].clientY;
      setIsPulling(true);
    }
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    if (!isPulling || isRefreshing) return;
    const diff = e.touches[0].clientY - startY.current;
    if (diff > 0) {
      setPullDistance(Math.min(diff * 0.5, THRESHOLD * 1.5));
    }
  };

  const handleTouchEnd = async () => {
    if (!isPulling) return;
    if (pullDistance >= THRESHOLD && !isRefreshing) {
      setIsRefreshing(true);
      setPullDistance(THRESHOLD);
      try { await onRefresh(); } 
      finally { setIsRefreshing(false); }
    }
    setIsPulling(false);
    setPullDistance(0);
  };

  return (
    <div
      ref={containerRef}
      className="h-full overflow-y-auto"
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
    >
      <div
        className="flex items-center justify-center overflow-hidden"
        style={{ height: pullDistance }}
      >
        {isRefreshing ? (
          <div className="animate-spin w-6 h-6 border-2 border-primary-500 border-t-transparent rounded-full" />
        ) : (
          <div style={{ transform: `rotate(${(pullDistance / THRESHOLD) * 180}deg)` }}>↓</div>
        )}
      </div>
      {children}
    </div>
  );
}

// Swipeable Row
function SwipeableRow({
  children,
  onSwipeLeft,
  onSwipeRight,
  leftAction,
  rightAction,
}: {
  children: ReactNode;
  onSwipeLeft?: () => void;
  onSwipeRight?: () => void;
  leftAction?: ReactNode;
  rightAction?: ReactNode;
}) {
  const [translateX, setTranslateX] = useState(0);
  const startX = useRef(0);
  const isDragging = useRef(false);
  const THRESHOLD = 80;

  const handleTouchStart = (e: React.TouchEvent) => {
    startX.current = e.touches[0].clientX;
    isDragging.current = true;
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    if (!isDragging.current) return;
    const diff = e.touches[0].clientX - startX.current;
    setTranslateX(Math.max(-100, Math.min(100, diff)));
  };

  const handleTouchEnd = () => {
    isDragging.current = false;
    if (translateX > THRESHOLD) onSwipeRight?.();
    else if (translateX < -THRESHOLD) onSwipeLeft?.();
    setTranslateX(0);
  };

  return (
    <div className="relative overflow-hidden">
      {leftAction && (
        <div className="absolute left-0 top-0 bottom-0 flex items-center px-4 bg-green-600">
          {leftAction}
        </div>
      )}
      {rightAction && (
        <div className="absolute right-0 top-0 bottom-0 flex items-center px-4 bg-red-600">
          {rightAction}
        </div>
      )}
      <div
        className="relative bg-neutral-800"
        style={{
          transform: `translateX(${translateX}px)`,
          transition: isDragging.current ? 'none' : 'transform 0.2s ease-out',
        }}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      >
        {children}
      </div>
    </div>
  );
}
```

## Usage Examples

```typescript
export default function DashboardPage() {
  const [sheetOpen, setSheetOpen] = useState(false);

  const handleRefresh = async () => {
    await fetchData();
  };

  return (
    <div className="min-h-screen pb-20 md:pb-0">
      <PullToRefresh onRefresh={handleRefresh}>
        <div className="p-4">
          {items.map((item) => (
            <SwipeableRow
              key={item.id}
              onSwipeLeft={() => deleteItem(item.id)}
              rightAction={<span>🗑️</span>}
            >
              <ListItem onClick={() => setSheetOpen(true)}>
                {item.title}
              </ListItem>
            </SwipeableRow>
          ))}
        </div>
      </PullToRefresh>

      <BottomSheet isOpen={sheetOpen} onClose={() => setSheetOpen(false)} title="Details">
        <p>Sheet content here</p>
      </BottomSheet>

      <MobileNav items={[
        { href: '/dashboard', label: 'Home', icon: '🏠' },
        { href: '/settings', label: 'Settings', icon: '⚙️' },
      ]} />
    </div>
  );
}
```

## Best Practices

1. Minimum touch target: 44x44px (Apple) / 48x48dp (Google)
2. Use `safe-area-bottom` for bottom navigation on notched devices
3. Always provide visual feedback on touch (active states)
4. Lock body scroll when sheets are open
5. Use `touch-none` on drag handles to prevent scroll interference

## Common Mistakes

- Touch targets too small (causes mis-taps)
- Not handling safe areas (content hidden behind notch)
- Missing active states (no touch feedback)
- Forgetting to unlock body scroll on unmount
- Not debouncing pull-to-refresh

## Related Patterns

- design-tokens (consistent spacing/sizing)
- pwa-setup (full mobile experience)

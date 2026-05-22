---
name: rxjs-patterns
description: RxJS reactive programming patterns for Angular applications. Use when implementing observables, operators, error handling, memory management, subscription cleanup, or advanced reactive patterns. Covers operators, multicasting, backpressure, and integration with Angular Signals.
license: Complete terms in LICENSE.txt
---

# RxJS Patterns

Expert guidance for reactive programming with RxJS in Angular applications, focusing on best practices, common patterns, and performance optimization.

## When to Use This Skill

Activate this skill when you need to:
- Create and manage observables effectively
- Chain RxJS operators for data transformation
- Handle errors in reactive streams
- Prevent memory leaks from subscriptions
- Implement debouncing, throttling, or buffering
- Share observables with multiple subscribers
- Integrate RxJS with Angular Signals
- Optimize reactive data flows
- Implement advanced patterns (retry, polling, caching)

## Core Operators

### Transformation

```typescript
// map - Transform each value
source$.pipe(
  map(user => user.name)
)

// mergeMap/switchMap/concatMap/exhaustMap
// Choose based on concurrency needs:
// - switchMap: Cancel previous, use for search
// - mergeMap: Run concurrently, use for independent operations
// - concatMap: Queue sequentially, use for ordered operations
// - exhaustMap: Ignore new while running, use for save/submit

// Search example with switchMap
searchTerm$.pipe(
  debounceTime(300),
  distinctUntilChanged(),
  switchMap(term => this.searchService.search(term))
)

// Save example with exhaustMap
saveButton$.pipe(
  exhaustMap(() => this.saveService.save(data))
)
```

### Filtering

```typescript
// filter - Emit only matching values
source$.pipe(
  filter(user => user.age >= 18)
)

// distinctUntilChanged - Skip duplicate consecutive values
input$.pipe(
  distinctUntilChanged()
)

// take/takeUntil - Limit emissions
source$.pipe(
  take(5) // Take first 5
)

source$.pipe(
  takeUntil(destroy$) // Unsubscribe pattern
)

// debounceTime/throttleTime - Rate limiting
input$.pipe(
  debounceTime(300) // Wait 300ms after last input
)

click$.pipe(
  throttleTime(1000) // Emit at most once per second
)
```

### Combination

```typescript
// combineLatest - Emit when any observable emits
combineLatest([user$, settings$]).pipe(
  map(([user, settings]) => ({ user, settings }))
)

// forkJoin - Emit when all complete
forkJoin({
  user: getUserById(id),
  posts: getUserPosts(id),
  comments: getUserComments(id)
}).subscribe(({ user, posts, comments }) => {
  // All loaded
})

// merge - Merge multiple observables
merge(click$, hover$, focus$).subscribe()

// zip - Pair emissions by index
zip(numbers$, letters$).pipe(
  map(([num, letter]) => `${num}${letter}`)
)
```

## Error Handling

### catchError

```typescript
// Handle errors gracefully
this.http.get('/api/data').pipe(
  catchError(error => {
    console.error('Error:', error);
    return of([]); // Return fallback value
  })
)

// Re-throw after logging
this.http.get('/api/data').pipe(
  catchError(error => {
    this.logger.error(error);
    return throwError(() => new Error('Failed to load data'));
  })
)
```

### Retry Logic

```typescript
// retry - Retry on error
this.http.get('/api/data').pipe(
  retry(3),
  catchError(error => of([]))
)

// retryWhen - Advanced retry with delay
this.http.get('/api/data').pipe(
  retryWhen(errors => errors.pipe(
    scan((retryCount, err) => {
      if (retryCount >= 3) {
        throw err;
      }
      return retryCount + 1;
    }, 0),
    delay(1000) // Wait 1s between retries
  ))
)
```

## Memory Management

### Subscription Cleanup

```typescript
// ❌ BAD - Memory leak
export class BadComponent {
  ngOnInit() {
    this.dataService.getData().subscribe(data => {
      this.data = data;
    });
  }
}

// ✅ GOOD - Manual cleanup
export class GoodComponent implements OnDestroy {
  private subscription = new Subscription();
  
  ngOnInit() {
    this.subscription.add(
      this.dataService.getData().subscribe(data => {
        this.data = data;
      })
    );
  }
  
  ngOnDestroy() {
    this.subscription.unsubscribe();
  }
}

// ✅ BETTER - takeUntil pattern
export class BetterComponent implements OnDestroy {
  private destroy$ = new Subject<void>();
  
  ngOnInit() {
    this.dataService.getData().pipe(
      takeUntil(this.destroy$)
    ).subscribe(data => {
      this.data = data;
    });
  }
  
  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}

// ✅ BEST - toSignal (Angular 16+)
export class BestComponent {
  data = toSignal(
    this.dataService.getData(),
    { initialValue: [] }
  );
}
```

### Sharing Observables

```typescript
// ❌ BAD - Multiple HTTP requests
const data$ = this.http.get('/api/data');
data$.subscribe(x => console.log(x));
data$.subscribe(y => console.log(y)); // Second request!

// ✅ GOOD - Share with shareReplay
const data$ = this.http.get('/api/data').pipe(
  shareReplay({ bufferSize: 1, refCount: true })
);
data$.subscribe(x => console.log(x));
data$.subscribe(y => console.log(y)); // Uses cached result
```

## Integration with Angular Signals

### toSignal

```typescript
// Convert observable to signal
export class Component {
  private dataService = inject(DataService);
  
  // Automatic subscription management
  data = toSignal(
    this.dataService.getData(),
    { initialValue: [] }
  );
  
  // Use in template
  template: `{{ data().length }} items`
}
```

### toObservable

```typescript
// Convert signal to observable
export class Component {
  searchTerm = signal('');
  
  results$ = toObservable(this.searchTerm).pipe(
    debounceTime(300),
    distinctUntilChanged(),
    switchMap(term => this.searchService.search(term))
  );
  
  results = toSignal(this.results$, { initialValue: [] });
}
```

## Advanced Patterns

### Polling

```typescript
// Poll every 5 seconds
interval(5000).pipe(
  startWith(0),
  switchMap(() => this.http.get('/api/status')),
  takeUntil(this.destroy$)
).subscribe(status => {
  this.status = status;
});
```

### Caching with Expiration

```typescript
@Injectable({ providedIn: 'root' })
export class CachedDataService {
  private cache$ = new ReplaySubject<Data[]>(1);
  private cacheAge = 0;
  private readonly CACHE_DURATION = 5 * 60 * 1000; // 5 minutes
  
  getData(): Observable<Data[]> {
    const now = Date.now();
    
    if (now - this.cacheAge > this.CACHE_DURATION) {
      this.http.get<Data[]>('/api/data').subscribe(data => {
        this.cache$.next(data);
        this.cacheAge = now;
      });
    }
    
    return this.cache$.asObservable();
  }
}
```

### Optimistic Updates

```typescript
updateItem(id: string, changes: Partial<Item>): Observable<Item> {
  // Optimistically update UI
  const optimisticItem = { ...this.currentItem, ...changes };
  this.items$.next(this.items$.value.map(item => 
    item.id === id ? optimisticItem : item
  ));
  
  // Send to server
  return this.http.put<Item>(`/api/items/${id}`, changes).pipe(
    tap(serverItem => {
      // Update with server response
      this.items$.next(this.items$.value.map(item => 
        item.id === id ? serverItem : item
      ));
    }),
    catchError(error => {
      // Rollback on error
      this.items$.next(this.items$.value.map(item => 
        item.id === id ? this.currentItem : item
      ));
      return throwError(() => error);
    })
  );
}
```

## Best Practices

- ✅ Always unsubscribe or use takeUntil
- ✅ Use toSignal for automatic cleanup
- ✅ Share expensive observables with shareReplay
- ✅ Choose the right flattening operator (switchMap, mergeMap, etc.)
- ✅ Handle errors with catchError
- ✅ Use async pipe in templates when possible
- ❌ Don't subscribe in services (return observables)
- ❌ Don't manually create subscriptions unnecessarily
- ❌ Don't forget to complete subjects

## References

- [RxJS Official Documentation](https://rxjs.dev/)
- [RxJS Operators Decision Tree](https://rxjs.dev/operator-decision-tree)
- [Learn RxJS](https://www.learnrxjs.io/)
- [Angular Signals Integration](https://angular.dev/guide/signals/rxjs-interop)

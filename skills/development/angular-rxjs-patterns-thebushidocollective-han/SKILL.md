---
name: angular-rxjs-patterns
description: Use when handling async operations in Angular applications with observables, operators, and subjects.
allowed-tools:
  - Bash
  - Read
---

# Angular RxJS Patterns

Master RxJS in Angular for handling async operations, data streams,
and reactive programming patterns.

## Observable Creation

### Basic Observable Creation

```typescript
import { Observable, of, from, interval, fromEvent } from 'rxjs';

// of - emit values in sequence
const numbers$ = of(1, 2, 3, 4, 5);

// from - convert array, promise, or iterable
const fromArray$ = from([1, 2, 3]);
const fromPromise$ = from(fetch('/api/data'));

// interval - emit numbers at intervals
const timer$ = interval(1000); // Every second

// fromEvent - DOM events
const clicks$ = fromEvent(document, 'click');

// Custom observable
const custom$ = new Observable(subscriber => {
  subscriber.next(1);
  subscriber.next(2);
  subscriber.complete();
});
```

### HttpClient Observables

```typescript
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  constructor(private http: HttpClient) {}

  getData(): Observable<Data[]> {
    return this.http.get<Data[]>('/api/data');
  }

  getItem(id: string): Observable<Data> {
    return this.http.get<Data>(`/api/data/${id}`);
  }

  createItem(data: Data): Observable<Data> {
    return this.http.post<Data>('/api/data', data);
  }

  updateItem(id: string, data: Data): Observable<Data> {
    return this.http.put<Data>(`/api/data/${id}`, data);
  }

  deleteItem(id: string): Observable<void> {
    return this.http.delete<void>(`/api/data/${id}`);
  }
}
```

## Common Operators

### Transformation Operators

```typescript
import { map, pluck, switchMap, mergeMap, concatMap } from 'rxjs/operators';
import { of } from 'rxjs';

// map - transform values
const numbers$ = of(1, 2, 3).pipe(
  map(n => n * 2) // 2, 4, 6
);

// pluck - extract property (deprecated, use map)
const users$ = of(
  { name: 'John', age: 30 },
  { name: 'Jane', age: 25 }
).pipe(
  map(user => user.name) // 'John', 'Jane'
);

// switchMap - cancel previous, emit new
searchControl.valueChanges.pipe(
  switchMap(term => this.searchService.search(term))
).subscribe(results => {
  this.results = results;
});

// mergeMap - run in parallel
const ids$ = of(1, 2, 3);
ids$.pipe(
  mergeMap(id => this.getUser(id)) // All requests in parallel
).subscribe();

// concatMap - run in sequence
ids$.pipe(
  concatMap(id => this.getUser(id)) // One at a time
).subscribe();
```

### Filtering Operators

```typescript
import { filter, take, takeUntil, takeWhile, distinctUntilChanged } from 'rxjs/operators';

// filter - only emit matching values
of(1, 2, 3, 4, 5).pipe(
  filter(n => n % 2 === 0) // 2, 4
);

// take - first N values
interval(1000).pipe(
  take(5) // First 5 emissions
);

// takeUntil - until another observable emits
const destroy$ = new Subject();
source$.pipe(
  takeUntil(destroy$)
).subscribe();

// distinctUntilChanged - skip duplicate consecutive values
of(1, 1, 2, 2, 3, 3).pipe(
  distinctUntilChanged() // 1, 2, 3
);
```

### Combination Operators

```typescript
import { combineLatest, merge, concat, forkJoin, zip } from 'rxjs';
import { startWith } from 'rxjs/operators';

// combineLatest - emit when any source emits
combineLatest([
  this.user$,
  this.settings$
]).pipe(
  map(([user, settings]) => ({ user, settings }))
).subscribe();

// merge - emit from any source
merge(
  this.clicks$,
  this.hovers$
).subscribe();

// concat - emit in sequence
concat(
  this.loadUser$,
  this.loadSettings$
).subscribe();

// forkJoin - wait for all to complete
forkJoin({
  user: this.getUser(),
  posts: this.getPosts(),
  comments: this.getComments()
}).subscribe(({ user, posts, comments }) => {
  // All complete
});

// zip - pair values from sources
zip(
  of(1, 2, 3),
  of('a', 'b', 'c')
).pipe(
  map(([num, letter]) => `${num}${letter}`)
); // '1a', '2b', '3c'
```

### Utility Operators

```typescript
import { tap, delay, debounceTime, throttleTime, distinctUntilChanged } from 'rxjs/operators';

// tap - side effects (logging, etc.)
source$.pipe(
  tap(value => console.log('Value:', value)),
  map(value => value * 2)
);

// delay - delay emissions
of(1, 2, 3).pipe(
  delay(1000) // Delay 1 second
);

// debounceTime - wait for pause in emissions
searchControl.valueChanges.pipe(
  debounceTime(300) // Wait 300ms after user stops typing
);

// throttleTime - emit first value, ignore for duration
clicks$.pipe(
  throttleTime(1000) // Only once per second
);

// distinctUntilChanged - skip duplicates
input$.pipe(
  distinctUntilChanged() // Only when value changes
);
```

## Error Handling

### catchError - Handle Errors

```typescript
import { catchError } from 'rxjs/operators';
import { of, EMPTY, throwError } from 'rxjs';

// Return fallback value
this.http.get('/api/data').pipe(
  catchError(error => {
    console.error('Error:', error);
    return of([]); // Return empty array
  })
);

// Return empty observable
source$.pipe(
  catchError(() => EMPTY) // Complete without emitting
);

// Re-throw error
source$.pipe(
  catchError(error => {
    console.error('Error:', error);
    return throwError(() => new Error('Custom error'));
  })
);

// Handle different error types
source$.pipe(
  catchError(error => {
    if (error.status === 404) {
      return of(null);
    }
    return throwError(() => error);
  })
);
```

### retry and retryWhen

```typescript
import { retry, retryWhen, delay, take } from 'rxjs/operators';

// Simple retry
this.http.get('/api/data').pipe(
  retry(3) // Retry up to 3 times
);

// Retry with delay
this.http.get('/api/data').pipe(
  retryWhen(errors =>
    errors.pipe(
      delay(1000), // Wait 1 second
      take(3) // Max 3 retries
    )
  )
);

// Exponential backoff
this.http.get('/api/data').pipe(
  retryWhen(errors =>
    errors.pipe(
      mergeMap((error, index) => {
        if (index >= 3) {
          return throwError(() => error);
        }
        const delayMs = Math.pow(2, index) * 1000;
        return of(error).pipe(delay(delayMs));
      })
    )
  )
);
```

## Subscription Management

### Manual Subscription Cleanup

```typescript
import { Component, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-my-component'
})
export class MyComponent implements OnDestroy {
  private subscription = new Subscription();

  ngOnInit() {
    // Add subscriptions
    this.subscription.add(
      this.data$.subscribe(data => {
        this.data = data;
      })
    );

    this.subscription.add(
      this.other$.subscribe(other => {
        this.other = other;
      })
    );
  }

  ngOnDestroy() {
    // Unsubscribe from all
    this.subscription.unsubscribe();
  }
}
```

### takeUntil Pattern

```typescript
import { Component, OnDestroy } from '@angular/core';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-my-component'
})
export class MyComponent implements OnDestroy {
  private destroy$ = new Subject<void>();

  ngOnInit() {
    this.data$.pipe(
      takeUntil(this.destroy$)
    ).subscribe(data => {
      this.data = data;
    });

    this.other$.pipe(
      takeUntil(this.destroy$)
    ).subscribe(other => {
      this.other = other;
    });
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

### Async Pipe (No Manual Unsubscribe)

```typescript
import { Component } from '@angular/core';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-user-list',
  template: `
    <div *ngIf="users$ | async as users">
      <div *ngFor="let user of users">
        {{ user.name }}
      </div>
    </div>

    <div *ngIf="loading$ | async">Loading...</div>
    <div *ngIf="error$ | async as error">Error: {{ error }}</div>
  `
})
export class UserListComponent {
  users$: Observable<User[]>;
  loading$: Observable<boolean>;
  error$: Observable<string | null>;

  constructor(private userService: UserService) {
    this.users$ = this.userService.getUsers();
    this.loading$ = this.userService.loading$;
    this.error$ = this.userService.error$;
  }
}
```

## Subjects

### Subject - Multicast

```typescript
import { Subject } from 'rxjs';

const subject = new Subject<number>();

// Multiple subscribers
subject.subscribe(val => console.log('A:', val));
subject.subscribe(val => console.log('B:', val));

subject.next(1); // A: 1, B: 1
subject.next(2); // A: 2, B: 2
```

### BehaviorSubject - Current Value

```typescript
import { BehaviorSubject } from 'rxjs';

const subject = new BehaviorSubject<number>(0); // Initial value

subject.subscribe(val => console.log('A:', val)); // A: 0

subject.next(1); // A: 1
subject.next(2); // A: 2

subject.subscribe(val => console.log('B:', val)); // B: 2 (latest value)

// Common pattern for state management
@Injectable({
  providedIn: 'root'
})
export class StateService {
  private stateSubject = new BehaviorSubject<State>(initialState);
  state$ = this.stateSubject.asObservable();

  updateState(newState: State) {
    this.stateSubject.next(newState);
  }

  get currentState(): State {
    return this.stateSubject.value;
  }
}
```

### ReplaySubject - Buffer Values

```typescript
import { ReplaySubject } from 'rxjs';

const subject = new ReplaySubject<number>(2); // Buffer last 2 values

subject.next(1);
subject.next(2);
subject.next(3);

subject.subscribe(val => console.log('A:', val)); // A: 2, A: 3

subject.next(4); // A: 4

subject.subscribe(val => console.log('B:', val)); // B: 3, B: 4
```

### AsyncSubject - Last Value on Complete

```typescript
import { AsyncSubject } from 'rxjs';

const subject = new AsyncSubject<number>();

subject.subscribe(val => console.log('A:', val));

subject.next(1);
subject.next(2);
subject.next(3);
subject.complete(); // A: 3 (only last value when complete)
```

## Hot vs Cold Observables

### Cold Observable - Unicast

```typescript
// Each subscription creates new execution
const cold$ = interval(1000);

cold$.subscribe(val => console.log('A:', val)); // A: 0, 1, 2...
setTimeout(() => {
  cold$.subscribe(val => console.log('B:', val)); // B: 0, 1, 2... (separate execution)
}, 2000);
```

### Hot Observable - Multicast

```typescript
import { Subject, interval } from 'rxjs';
import { share, shareReplay } from 'rxjs/operators';

// Using Subject
const subject = new Subject();
const source$ = interval(1000);
source$.subscribe(subject);

subject.subscribe(val => console.log('A:', val)); // A: 0, 1, 2...
setTimeout(() => {
  subject.subscribe(val => console.log('B:', val)); // B: 2, 3, 4... (shared)
}, 2000);

// Using share operator
const shared$ = interval(1000).pipe(share());

shared$.subscribe(val => console.log('A:', val));
setTimeout(() => {
  shared$.subscribe(val => console.log('B:', val)); // Shares source
}, 2000);

// Using shareReplay
const cached$ = this.http.get('/api/data').pipe(
  shareReplay(1) // Cache last 1 value
);

// Multiple subscribers get cached result
cached$.subscribe();
cached$.subscribe(); // No second HTTP request
```

## RxJS in Services

### Data Service with State

```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap, catchError, finalize } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private usersSubject = new BehaviorSubject<User[]>([]);
  private loadingSubject = new BehaviorSubject<boolean>(false);
  private errorSubject = new BehaviorSubject<string | null>(null);

  users$ = this.usersSubject.asObservable();
  loading$ = this.loadingSubject.asObservable();
  error$ = this.errorSubject.asObservable();

  constructor(private http: HttpClient) {}

  loadUsers(): void {
    this.loadingSubject.next(true);
    this.errorSubject.next(null);

    this.http.get<User[]>('/api/users').pipe(
      tap(users => this.usersSubject.next(users)),
      catchError(error => {
        this.errorSubject.next(error.message);
        return of([]);
      }),
      finalize(() => this.loadingSubject.next(false))
    ).subscribe();
  }

  getUser(id: string): Observable<User> {
    return this.http.get<User>(`/api/users/${id}`);
  }
}
```

### Search Service with Debounce

```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged, switchMap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class SearchService {
  private searchTerms = new Subject<string>();

  results$: Observable<SearchResult[]>;

  constructor(private http: HttpClient) {
    this.results$ = this.searchTerms.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      switchMap(term => this.search(term))
    );
  }

  search(term: string): Observable<SearchResult[]> {
    if (!term.trim()) {
      return of([]);
    }
    return this.http.get<SearchResult[]>(`/api/search?q=${term}`);
  }

  setSearchTerm(term: string): void {
    this.searchTerms.next(term);
  }
}
```

## Testing RxJS

### Testing Observables

```typescript
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

describe('UserService', () => {
  let service: UserService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [UserService]
    });

    service = TestBed.inject(UserService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should fetch users', () => {
    const mockUsers = [{ id: 1, name: 'John' }];

    service.getUsers().subscribe(users => {
      expect(users).toEqual(mockUsers);
    });

    const req = httpMock.expectOne('/api/users');
    expect(req.request.method).toBe('GET');
    req.flush(mockUsers);
  });
});
```

### Testing with Marble Diagrams

```typescript
import { TestScheduler } from 'rxjs/testing';

describe('Marble tests', () => {
  let scheduler: TestScheduler;

  beforeEach(() => {
    scheduler = new TestScheduler((actual, expected) => {
      expect(actual).toEqual(expected);
    });
  });

  it('should debounce', () => {
    scheduler.run(({ cold, expectObservable }) => {
      const source$ = cold('-a-b-c|');
      const expected = '-----c|';

      const result$ = source$.pipe(debounceTime(20));
      expectObservable(result$).toBe(expected);
    });
  });
});
```

## When to Use This Skill

Use angular-rxjs-patterns when building modern, production-ready
applications that require:

- Complex async data flows
- Real-time updates and streaming data
- Efficient HTTP request management
- Form input handling with debouncing
- State management with observables
- Error handling and retry logic
- Combining multiple async sources
- Memory-safe subscription management

## RxJS Best Practices in Angular

1. **Use async pipe** - Automatic subscription management
2. **takeUntil for cleanup** - Unsubscribe in ngOnDestroy
3. **shareReplay for caching** - Avoid duplicate HTTP requests
4. **debounceTime for inputs** - Reduce API calls
5. **switchMap for cancellation** - Cancel old requests
6. **catchError for errors** - Always handle errors
7. **BehaviorSubject for state** - Share current state
8. **Avoid nested subscriptions** - Use operators instead
9. **Use operators over imperative code** - More declarative
10. **Test observables properly** - Use marble diagrams

## Common RxJS Mistakes

1. **Not unsubscribing** - Memory leaks
2. **Nested subscriptions** - Callback hell
3. **Not using operators** - Imperative instead of declarative
4. **Subscribing in services** - Return observables instead
5. **Not handling errors** - Silent failures
6. **Using Subject incorrectly** - Prefer BehaviorSubject for state
7. **Not using shareReplay** - Duplicate HTTP requests
8. **Forgetting to complete subjects** - Memory leaks
9. **Using subscribe in templates** - Use async pipe
10. **Not understanding hot vs cold** - Unexpected behavior

## Resources

- [RxJS Official Documentation](https://rxjs.dev/)
- [RxJS Operators](https://rxjs.dev/guide/operators)
- [Angular HttpClient](https://angular.io/guide/http)
- [Reactive Programming with RxJS](https://pragprog.com/titles/smreactjs5/reactive-programming-with-rxjs/)
- [RxMarbles - Visual Operator Reference](https://rxmarbles.com/)
- [Learn RxJS](https://www.learnrxjs.io/)

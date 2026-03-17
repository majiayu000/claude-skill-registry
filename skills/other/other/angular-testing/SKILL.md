---
name: angular-testing
description: Use when writing unit tests for Angular components, services, pipes, or directives. Triggers on requests to "write tests", "add tests", "create spec", "test this component", or when test files need to be created/modified.
---

# Angular Testing Guide

Write tests using Vitest with Angular TestBed following project patterns.

**Note:** Vitest globals (`describe`, `it`, `expect`, `vi`, `beforeEach`, `afterEach`) are pre-configured in `tsconfig.spec.json` - no imports needed.

## Test File Location

Place test files next to the source files:

```
component-name/
  component-name.ts
  component-name.spec.ts  # <- Test file here
```

## Essential Imports

```typescript
import { ComponentFixture, TestBed } from "@angular/core/testing";
import { provideZonelessChangeDetection } from "@angular/core";
import { By } from "@angular/platform-browser";
// Vitest globals (describe, it, expect, vi) are available without imports
```

## Component Test Template

```typescript
import { ComponentFixture, TestBed } from "@angular/core/testing";
import { provideZonelessChangeDetection } from "@angular/core";
import { By } from "@angular/platform-browser";

import { MyComponent } from "./my";
import { MyService } from "../services/my";

describe("MyComponent", () => {
  let component: MyComponent;
  let fixture: ComponentFixture<MyComponent>;
  let mockService: Partial<MyService>;

  beforeEach(async () => {
    mockService = {
      getData: vi.fn(),
      saveData: vi.fn(),
    };

    await TestBed.configureTestingModule({
      imports: [MyComponent],
      providers: [
        provideZonelessChangeDetection(),
        { provide: MyService, useValue: mockService },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(MyComponent);
    component = fixture.componentInstance;
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });

  it("should render data when loaded", () => {
    // Arrange
    vi.mocked(mockService.getData).mockReturnValue(["item1", "item2"]);

    // Act
    fixture.detectChanges();

    // Assert
    const items = fixture.debugElement.queryAll(By.css(".item"));
    expect(items).toHaveLength(2);
  });

  it("should call service on button click", () => {
    // Arrange
    fixture.detectChanges();
    const button = fixture.debugElement.query(By.css("button"));

    // Act
    button.triggerEventHandler("click", null);

    // Assert
    expect(mockService.saveData).toHaveBeenCalled();
  });
});
```

## Service Test Template

```typescript
import { TestBed } from "@angular/core/testing";
import { provideZonelessChangeDetection } from "@angular/core";
import {
  provideHttpClientTesting,
  HttpTestingController,
} from "@angular/common/http/testing";

import { MyService } from "./my";

describe("MyService", () => {
  let service: MyService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        MyService,
        provideZonelessChangeDetection(),
        provideHttpClientTesting(),
      ],
    });

    service = TestBed.inject(MyService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it("should be created", () => {
    expect(service).toBeTruthy();
  });

  it("should fetch data from API", () => {
    // Arrange
    const mockData = [{ id: 1, name: "Test" }];

    // Act
    service.getData().subscribe((data) => {
      // Assert
      expect(data).toEqual(mockData);
    });

    // Assert HTTP request
    const req = httpMock.expectOne("/api/data");
    expect(req.request.method).toBe("GET");
    req.flush(mockData);
  });
});
```

## Testing Signal Inputs

```typescript
import { signal } from "@angular/core";

it("should respond to input changes", () => {
  // For required inputs, set before detectChanges
  fixture.componentRef.setInput("data", { id: 1, name: "Test" });
  fixture.detectChanges();

  expect(component.data()).toEqual({ id: 1, name: "Test" });
});
```

## Testing Outputs

```typescript
it("should emit event on action", () => {
  const emitSpy = vi.fn();
  component.valueChange.subscribe(emitSpy);

  component.updateValue(42);

  expect(emitSpy).toHaveBeenCalledWith(42);
});
```

## Mocking Patterns

```typescript
// Mock service methods
const mockService = {
  getData: vi.fn().mockReturnValue(of(["data"])),
  saveData: vi.fn().mockResolvedValue({ success: true }),
};

// Spy on existing service
const service = TestBed.inject(MyService);
const spy = vi.spyOn(service, "getData").mockReturnValue(of(["mocked"]));

// Mock external module
vi.mock("external-lib", () => ({
  someFunction: vi.fn(() => "mocked result"),
}));
```

## Async Testing

```typescript
// Using async/await
it("should handle async operations", async () => {
  vi.mocked(mockService.getData).mockResolvedValue(["async data"]);

  await component.loadData();
  fixture.detectChanges();

  expect(component.items()).toEqual(["async data"]);
});

// Testing Observables
it("should handle observable", () => {
  vi.mocked(mockService.getData).mockReturnValue(of(["data"]));

  service.getData().subscribe((result) => {
    expect(result).toEqual(["data"]);
  });
});
```

## Fake Timers

```typescript
it("should handle delayed operations", () => {
  vi.useFakeTimers();

  component.startTimer();
  vi.advanceTimersByTime(1000);

  expect(component.timerComplete()).toBe(true);

  vi.useRealTimers();
});
```

## DOM Queries

```typescript
// Query by CSS selector
const element = fixture.debugElement.query(By.css(".my-class"));
const elements = fixture.debugElement.queryAll(By.css("button"));

// Query by directive
const directive = fixture.debugElement.query(By.directive(MyDirective));

// Get native element
const nativeElement = element.nativeElement;
expect(nativeElement.textContent).toContain("Expected text");
```

## Checklist

- [ ] Vitest globals available (no imports needed)
- [ ] Using `provideZonelessChangeDetection()` in providers
- [ ] Following AAA pattern (Arrange, Act, Assert)
- [ ] Mocking external dependencies
- [ ] Testing component inputs and outputs
- [ ] Verifying HTTP requests with `httpMock.verify()`
- [ ] Using descriptive test names

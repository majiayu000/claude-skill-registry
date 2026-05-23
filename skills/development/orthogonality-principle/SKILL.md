---
name: orthogonality-principle
description: Use when designing modules, APIs, and system architecture requiring independent, non-overlapping components where changes in one don't affect others.
allowed-tools:
  - Read
  - Edit
  - Grep
  - Glob
---

# Orthogonality Principle

Build systems where components are independent and changes don't ripple
unexpectedly.

## What is Orthogonality?

**Orthogonal** (from mathematics): Two lines are orthogonal if they're
at right angles - changing one doesn't affect the other.

**In software**: Components are orthogonal when changing one doesn't
require changing others. They are independent and non-overlapping.

### Benefits

- Changes are localized (less debugging)
- Easy to test in isolation
- Components are reusable
- Less coupling = less complexity
- Easier to understand and maintain

## Signs of Non-Orthogonality

### Red flags indicating components are NOT orthogonal

1. **Change amplification**: Changing one thing requires changing many others
2. **Shotgun surgery**: One feature scattered across many files
3. **Tight coupling**: Components know too much about each other
4. **Duplicate logic**: Same concept implemented multiple ways
5. **Cascading changes**: Change in A breaks B, C, D unexpectedly

## Achieving Orthogonality

### 1. Separation of Concerns

### Keep unrelated responsibilities separate

### Elixir Example

```elixir
# NON-ORTHOGONAL - Mixed concerns
defmodule UserController do
  def create(conn, params) do
    # Validation
    if valid_email?(params["email"]) do
      # Database
      user = Repo.insert!(%User{email: params["email"]})

      # External API
      Stripe.create_customer(user.email)

      # Notification
      Email.send_welcome(user.email)

      # Logging
      Logger.info("Created user #{user.id}")

      # Response
      json(conn, %{user: user})
    end
  end
end
# Changing email format affects validation, database, Stripe, email!

# ORTHOGONAL - Separated concerns
defmodule UserController do
  def create(conn, params) do
    with {:ok, command} <- build_command(params),
         {:ok, user} <- UserService.create(command) do
      json(conn, %{user: user})
    end
  end
end

defmodule UserService do
  def create(command) do
    with {:ok, user} <- Repo.insert(User.changeset(command)),
         :ok <- BillingService.setup_customer(user),
         :ok <- NotificationService.welcome(user) do
      {:ok, user}
    end
  end
end

# Now can change billing without touching notifications
# Can change notifications without touching database
# Each service is orthogonal
```

### TypeScript Example

```typescript
// NON-ORTHOGONAL - Everything in one component
function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filters, setFilters] = useState<Filters>({});
  const [sorting, setSorting] = useState<Sort>({ field: 'date', dir: 'asc' });

  // Data fetching
  useEffect(() => {
    fetch('/api/tasks').then(res => res.json()).then(setTasks);
  }, []);

  // Filtering logic
  const filtered = tasks.filter(gig => {
    if (filters.status && gig.status !== filters.status) return false;
    if (filters.location && !gig.location.includes(filters.location)) return false;
    return true;
  });

  // Sorting logic
  const sorted = [...filtered].sort((a, b) => {
    const aVal = a[sorting.field];
    const bVal = b[sorting.field];
    return sorting.dir === 'asc' ? aVal - bVal : bVal - aVal;
  });

  // Rendering
  return (
    <View>
      {/* Filters UI */}
      {/* Sorting UI */}
      {/* List UI */}
    </View>
  );
}
// Changing filtering affects fetching, sorting, rendering!

// ORTHOGONAL - Separated concerns
function useTaskData() {
  const [tasks, setTasks] = useState<Task[]>([]);
  useEffect(() => {
    fetch('/api/tasks').then(res => res.json()).then(setTasks);
  }, []);
  return tasks;
}

function useTaskFiltering(tasks: Task[], filters: Filters) {
  return useMemo(() => {
    return tasks.filter(gig => {
      if (filters.status && gig.status !== filters.status) return false;
      if (filters.location && !gig.location.includes(filters.location)) return false;
      return true;
    });
  }, [tasks, filters]);
}

function useTaskSorting(tasks: Task[], sort: Sort) {
  return useMemo(() => {
    return [...tasks].sort((a, b) => {
      const aVal = a[sort.field];
      const bVal = b[sort.field];
      return sort.dir === 'asc' ? aVal - bVal : bVal - aVal;
    });
  }, [tasks, sort]);
}

function TaskList() {
  const allTasks = useTaskData();
  const [filters, setFilters] = useState<Filters>({});
  const [sort, setSort] = useState<Sort>({ field: 'date', dir: 'asc' });

  const filtered = useTaskFiltering(allTasks, filters);
  const sorted = useTaskSorting(filtered, sort);

  return (
    <View>
      <TaskFilters filters={filters} onChange={setFilters} />
      <TaskSorting sort={sort} onChange={setSort} />
      <TaskCards tasks={sorted} />
    </View>
  );
}
// Now can change filtering without touching sorting
// Can change data fetching without touching UI
// Each concern is orthogonal
```

### 2. Interface Segregation

### Create focused, minimal interfaces

### Elixir Example (Interface Segregation)

```elixir
# NON-ORTHOGONAL - Fat interface
defmodule DataStore do
  @callback get(key :: String.t()) :: {:ok, term()} | {:error, term()}
  @callback set(key :: String.t(), value :: term()) :: :ok
  @callback delete(key :: String.t()) :: :ok
  @callback list_all() :: [term()]
  @callback search(query :: String.t()) :: [term()]
  @callback bulk_insert(items :: [term()]) :: :ok
  @callback export_to_json() :: String.t()
  @callback import_from_json(json :: String.t()) :: :ok
end
# Implementing simple cache requires implementing export/import!
# Not orthogonal - simple use cases coupled to complex ones

# ORTHOGONAL - Segregated interfaces
defmodule KeyValueStore do
  @callback get(key :: String.t()) :: {:ok, term()} | {:error, term()}
  @callback set(key :: String.t(), value :: term()) :: :ok
  @callback delete(key :: String.t()) :: :ok
end

defmodule Searchable do
  @callback search(query :: String.t()) :: [term()]
end

defmodule BulkOperations do
  @callback bulk_insert(items :: [term()]) :: :ok
end

defmodule Exportable do
  @callback export_to_json() :: String.t()
  @callback import_from_json(json :: String.t()) :: :ok
end

# Simple cache implements only KeyValueStore
# Search index implements KeyValueStore + Searchable
# Each interface is orthogonal to others
```

### 3. Dependency Injection

### Don't hardcode dependencies - inject them

### Elixir Example (Dependency Injection)

```elixir
# NON-ORTHOGONAL - Hardcoded dependencies
defmodule OrderService do
  def create_order(items) do
    PaymentService.charge(items)  # Coupled
    InventoryService.reserve(items)  # Coupled
    EmailService.send_confirmation()  # Coupled
  end
end
# Can't test without real payment/inventory/email services
# Can't swap implementations

# ORTHOGONAL - Injected dependencies
defmodule OrderService do
  def create_order(items, deps \\ default_deps()) do
    with :ok <- deps.payment.charge(items),
         :ok <- deps.inventory.reserve(items),
         :ok <- deps.email.send_confirmation() do
      :ok
    end
  end

  defp default_deps do
    %{
      payment: PaymentService,
      inventory: InventoryService,
      email: EmailService
    }
  end
end

# Can test with mocks
test "creates order" do
  deps = %{
    payment: MockPayment,
    inventory: MockInventory,
    email: MockEmail
  }
  assert :ok = OrderService.create_order(items, deps)
end
# Each dependency is orthogonal - can change independently
```

### 4. Event-Driven Architecture

### Decouple through events instead of direct calls

### Elixir Example (Event-Driven Architecture)

```elixir
# NON-ORTHOGONAL - Direct coupling
defmodule UserService do
  def create_user(attrs) do
    {:ok, user} = Repo.insert(User.changeset(attrs))

    # Directly coupled to all these services
    BillingService.create_customer(user)
    AnalyticsService.track_signup(user)
    EmailService.send_welcome(user)
    CacheService.invalidate("users")

    {:ok, user}
  end
end
# Adding new behavior requires modifying UserService
# Removing email feature requires modifying UserService

# ORTHOGONAL - Event-driven
defmodule UserService do
  def create_user(attrs) do
    {:ok, user} = Repo.insert(User.changeset(attrs))

    # Publish event - don't know who listens
    EventBus.publish({:user_created, user})

    {:ok, user}
  end
end

# Subscribers are orthogonal
defmodule BillingSubscriber do
  def handle_event({:user_created, user}) do
    BillingService.create_customer(user)
  end
end

defmodule AnalyticsSubscriber do
  def handle_event({:user_created, user}) do
    AnalyticsService.track_signup(user)
  end
end

# Add/remove subscribers without touching UserService
# Each subscriber is orthogonal to others
```

### TypeScript Example (Event-Driven Architecture)

```typescript
// NON-ORTHOGONAL - Direct coupling
class TaskManager {
  createTask(data: TaskData) {
    const gig = this.repository.save(data);

    // Directly coupled
    this.notificationService.notifyUsersNearby(gig);
    this.searchIndex.addTask(gig);
    this.analyticsService.trackTaskCreated(gig);

    return gig;
  }
}

// ORTHOGONAL - Event-driven
class TaskManager {
  constructor(
    private repository: TaskRepository,
    private eventBus: EventBus
  ) {}

  createTask(data: TaskData) {
    const gig = this.repository.save(data);

    // Publish event
    this.eventBus.publish('gig.created', gig);

    return gig;
  }
}

// Orthogonal subscribers
eventBus.subscribe('gig.created', (gig) => {
  notificationService.notifyUsersNearby(gig);
});

eventBus.subscribe('gig.created', (gig) => {
  searchIndex.addTask(gig);
});

// Add/remove subscribers without changing TaskManager
```

### 5. Data Orthogonality

### Don't duplicate data - maintain single source of truth

### Elixir Example (Data Orthogonality)

```elixir
# NON-ORTHOGONAL - Duplicate data
defmodule Task do
  schema "tasks" do
    field :hourly_rate, :decimal
    field :total_hours, :integer
    field :total_amount, :decimal  # Calculated from rate * hours
    # Changing hourly_rate requires updating total_amount
  end
end

# ORTHOGONAL - Computed fields
defmodule Task do
  schema "tasks" do
    field :hourly_rate, :decimal
    field :total_hours, :integer
    # total_amount computed on demand
  end

  def total_amount(%{hourly_rate: rate, total_hours: hours}) do
    Decimal.mult(rate, hours)
  end
end
# Single source of truth - rate and hours
# total_amount always correct, no sync issues
```

### TypeScript Example (Data Orthogonality)

```typescript
// NON-ORTHOGONAL - Duplicate state
interface Assignment {
  status: 'pending' | 'active' | 'completed';
  isPending: boolean;  // Duplicates status
  isActive: boolean;   // Duplicates status
  isCompleted: boolean; // Duplicates status
}
// Have to keep all flags in sync with status

// ORTHOGONAL - Single source of truth
interface Assignment {
  status: 'pending' | 'active' | 'completed';
}

// Derive flags from status
function isPending(engagement: Assignment): boolean {
  return engagement.status === 'pending';
}

function isActive(engagement: Assignment): boolean {
  return engagement.status === 'active';
}
// One source of truth, no sync issues
```

## Practical Guidelines

### When designing modules

- [ ] Each module has a single, clear purpose
- [ ] Modules don't share internal data structures
- [ ] Changes to one module rarely require changes to others
- [ ] Can test each module independently

### When designing APIs

- [ ] Each endpoint/function does ONE thing
- [ ] Parameters are independent (changing one doesn't require changing others)
- [ ] Return values are minimal (only what's needed)
- [ ] No hidden coupling between API calls

### When designing data

- [ ] One source of truth for each piece of data
- [ ] Computed values are computed, not stored
- [ ] No duplicate information
- [ ] Schema changes are localized

### When designing systems

- [ ] Components communicate through well-defined interfaces
- [ ] Use events for loose coupling
- [ ] Dependencies are injected, not hardcoded
- [ ] Can replace components without affecting others

## Testing Orthogonality

**Good test:** Tests one component without needing to set up unrelated components

```elixir
# ORTHOGONAL - Test in isolation
test "calculates gig total" do
  gig = %Task{hourly_rate: Decimal.new(25), total_hours: 8}
  assert Task.total_amount(gig) == Decimal.new(200)
end
# No database, no external services, pure logic

# NON-ORTHOGONAL - Requires full setup
test "calculates gig total" do
  {:ok, requester} = create_requester()
  {:ok, worker} = create_worker()
  {:ok, gig} = create_gig(requester)
  {:ok, engagement} = create_engagement(gig, worker)
  {:ok, shift} = create_shift(engagement, hours: 8)

  assert calculate_total(shift) == Decimal.new(200)
end
# Have to set up requester, worker, gig, engagement just to test math
```

## Examples

### Orthogonal patterns in the codebase

1. **CQRS**: Commands/Queries are orthogonal
   - Change query without affecting command
   - Add command without changing queries

2. **Atomic Design**: Atoms/Molecules/Organisms are orthogonal
   - Change atom styling without affecting organisms
   - Add new molecule without touching existing ones

3. **GraphQL Schema**: Types are orthogonal
   - Add fields to one type without affecting others
   - Each type has focused responsibility

4. **Microservices**: Bounded contexts are orthogonal
   - Change billing without affecting scheduling
   - Add analytics without touching core services

### Non-orthogonal anti-patterns to avoid

1. Shared mutable state (global variables)
2. Deep inheritance hierarchies
3. Circular dependencies
4. God objects (modules that do everything)
5. Feature envy (functions in module A that mostly use data from module B)

## Integration with Existing Skills

### Works with

- `solid-principles`: Single Responsibility → Orthogonality
- `structural-design-principles`: Encapsulation → Orthogonality
- `simplicity-principles`: KISS → Fewer dependencies → More orthogonal
- `cqrs-pattern`: Commands/Queries naturally orthogonal
- `atomic-design-pattern`: Component hierarchy naturally orthogonal

## Red Flags

### Signs of non-orthogonality

- "If I change X, I also have to change Y, Z, and W"
- "I can't test this without setting up half the system"
- "These two modules always change together"
- "I have to keep these fields in sync"
- "This module knows about too many other modules"

### Questions to ask

- Can I change this independently?
- Can I test this in isolation?
- Is this the only place with this logic?
- If I remove this, what breaks?

## Remember

"Orthogonal systems are easier to design, build, test, and extend."

- The Pragmatic Programmer

### Orthogonality = Independence

- Separate concerns into independent components
- Minimize coupling between components
- Use events for loose coordination
- Maintain single source of truth
- Test components in isolation

**The more orthogonal your system, the more flexible and maintainable it
becomes.**

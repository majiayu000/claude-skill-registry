---
name: oban-designer
description: "Design and implement Oban background job workers for Elixir. Configure queues, retry strategies, uniqueness constraints, cron scheduling, and error handling. Generate Oban workers, queue config, and test setups. Use when adding background jobs, async processing, scheduled tasks, or recurring cron jobs to an Elixir project using Oban."
---

# Oban Designer

## Installation

```elixir
# mix.exs
{:oban, "~> 2.18"}

# config/config.exs
config :my_app, Oban,
  repo: MyApp.Repo,
  queues: [default: 10, mailers: 20, webhooks: 50, events: 5],
  plugins: [
    Oban.Plugins.Pruner,
    {Oban.Plugins.Cron, crontab: [
      {"0 2 * * *", MyApp.Workers.DailyCleanup},
      {"*/5 * * * *", MyApp.Workers.MetricsCollector}
    ]}
  ]

# In application.ex children:
{Oban, Application.fetch_env!(:my_app, Oban)}
```

Generate the Oban migrations:

```bash
mix ecto.gen.migration add_oban_jobs_table
```

```elixir
defmodule MyApp.Repo.Migrations.AddObanJobsTable do
  use Ecto.Migration
  def up, do: Oban.Migration.up(version: 12)
  def down, do: Oban.Migration.down(version: 1)
end
```

## Worker Implementation

### Basic Worker

```elixir
defmodule MyApp.Workers.SendEmail do
  use Oban.Worker,
    queue: :mailers,
    max_attempts: 5,
    priority: 1

  @impl Oban.Worker
  def perform(%Oban.Job{args: %{"to" => to, "template" => template} = args}) do
    case MyApp.Mailer.deliver(to, template, args) do
      {:ok, _} -> :ok
      {:error, :temporary} -> {:error, "temporary failure"}  # Will retry
      {:error, :permanent} -> {:cancel, "invalid address"}   # Won't retry
    end
  end
end
```

### Return Values

| Return | Effect |
|--------|--------|
| `:ok` | Job marked complete |
| `{:ok, result}` | Job marked complete |
| `{:error, reason}` | Job retried (counts as attempt) |
| `{:cancel, reason}` | Job cancelled, no more retries |
| `{:snooze, seconds}` | Re-scheduled, doesn't count as attempt |
| `{:discard, reason}` | Job discarded (Oban 2.17+) |

## Queue Configuration

See [references/worker-patterns.md](references/worker-patterns.md) for common worker patterns.

### Sizing Guidelines

| Queue | Concurrency | Use Case |
|-------|------------|----------|
| `default` | 10 | General-purpose |
| `mailers` | 20 | Email delivery (I/O bound) |
| `webhooks` | 50 | Webhook delivery (I/O bound, high volume) |
| `media` | 5 | Image/video processing (CPU bound) |
| `events` | 5 | Analytics, audit logs |
| `critical` | 3 | Billing, payments |

### Queue Priority

Jobs within a queue execute by priority (0 = highest). Use sparingly:

```elixir
%{user_id: user.id}
|> MyApp.Workers.SendEmail.new(priority: 0)  # Urgent
|> Oban.insert()
```

## Retry Strategies

### Default Backoff

Oban uses exponential backoff: `attempt^4 + attempt` seconds.

### Custom Backoff

```elixir
defmodule MyApp.Workers.WebhookDelivery do
  use Oban.Worker,
    queue: :webhooks,
    max_attempts: 10

  @impl Oban.Worker
  def backoff(%Oban.Job{attempt: attempt}) do
    # Exponential with jitter: 2^attempt + random(0..30)
    trunc(:math.pow(2, attempt)) + :rand.uniform(30)
  end

  @impl Oban.Worker
  def perform(%Oban.Job{args: args}) do
    # ...
  end
end
```

### Timeout

```elixir
use Oban.Worker, queue: :media

@impl Oban.Worker
def timeout(%Oban.Job{args: %{"size" => "large"}}), do: :timer.minutes(10)
def timeout(_job), do: :timer.minutes(2)
```

## Uniqueness

Prevent duplicate jobs:

```elixir
defmodule MyApp.Workers.SyncAccount do
  use Oban.Worker,
    queue: :default,
    unique: [
      period: 300,               # 5 minutes
      states: [:available, :scheduled, :executing, :retryable],
      keys: [:account_id]        # Unique by this arg key
    ]
end
```

### Unique Options

| Option | Default | Description |
|--------|---------|-------------|
| `period` | 60 | Seconds to enforce uniqueness (`:infinity` for forever) |
| `states` | all active | Which job states to check |
| `keys` | all args | Specific arg keys to compare |
| `timestamp` | `:inserted_at` | Use `:scheduled_at` for scheduled uniqueness |

### Replace Existing

```elixir
%{account_id: id}
|> MyApp.Workers.SyncAccount.new(
  replace: [:scheduled_at],    # Update scheduled_at if duplicate
  schedule_in: 60
)
|> Oban.insert()
```

## Cron Scheduling

```elixir
# config.exs
plugins: [
  {Oban.Plugins.Cron, crontab: [
    {"0 */6 * * *", MyApp.Workers.DigestEmail},
    {"0 2 * * *", MyApp.Workers.DailyCleanup},
    {"0 0 1 * *", MyApp.Workers.MonthlyReport},
    {"*/5 * * * *", MyApp.Workers.HealthCheck, args: %{service: "api"}},
  ]}
]
```

Cron expressions: `minute hour day_of_month month day_of_week`.

## Inserting Jobs

```elixir
# Immediate
%{user_id: user.id, template: "welcome"}
|> MyApp.Workers.SendEmail.new()
|> Oban.insert()

# Scheduled
%{report_id: id}
|> MyApp.Workers.GenerateReport.new(schedule_in: 3600)
|> Oban.insert()

# Scheduled at specific time
%{report_id: id}
|> MyApp.Workers.GenerateReport.new(scheduled_at: ~U[2024-01-01 00:00:00Z])
|> Oban.insert()

# Bulk insert
changesets = Enum.map(users, fn user ->
  MyApp.Workers.SendEmail.new(%{user_id: user.id})
end)
Oban.insert_all(changesets)

# Inside Ecto.Multi
Ecto.Multi.new()
|> Ecto.Multi.insert(:user, changeset)
|> Oban.insert(:welcome_email, fn %{user: user} ->
  MyApp.Workers.SendEmail.new(%{user_id: user.id})
end)
|> Repo.transaction()
```

## Oban Pro Features

Available with Oban Pro license:

### Batch (group of jobs)

```elixir
# Process items in batch, run callback when all complete
batch = MyApp.Workers.ProcessItem.new_batch(
  items |> Enum.map(&%{item_id: &1.id}),
  callback: {MyApp.Workers.BatchComplete, %{batch_name: "import"}}
)
Oban.insert_all(batch)
```

### Workflow (job dependencies)

```elixir
Oban.Pro.Workflow.new()
|> Oban.Pro.Workflow.add(:extract, MyApp.Workers.Extract.new(%{file: path}))
|> Oban.Pro.Workflow.add(:transform, MyApp.Workers.Transform.new(%{}), deps: [:extract])
|> Oban.Pro.Workflow.add(:load, MyApp.Workers.Load.new(%{}), deps: [:transform])
|> Oban.insert_all()
```

### Chunk (aggregate multiple jobs)

```elixir
defmodule MyApp.Workers.BulkIndex do
  use Oban.Pro.Workers.Chunk,
    queue: :indexing,
    size: 100,            # Process 100 at a time
    timeout: 30_000       # Or after 30s

  @impl true
  def process(jobs) do
    items = Enum.map(jobs, & &1.args)
    SearchIndex.bulk_upsert(items)
    :ok
  end
end
```

## Testing

See [references/testing-oban.md](references/testing-oban.md) for detailed testing patterns.

### Setup

```elixir
# config/test.exs
config :my_app, Oban,
  testing: :manual  # or :inline for synchronous execution

# test_helper.exs (if using :manual)
Oban.Testing.start()
```

### Asserting Job Enqueued

```elixir
use Oban.Testing, repo: MyApp.Repo

test "enqueues welcome email on signup" do
  {:ok, user} = Accounts.register(%{email: "test@example.com"})

  assert_enqueued worker: MyApp.Workers.SendEmail,
    args: %{user_id: user.id, template: "welcome"},
    queue: :mailers
end
```

### Executing Jobs in Tests

```elixir
test "processes email delivery" do
  {:ok, _} =
    perform_job(MyApp.Workers.SendEmail, %{
      "to" => "user@example.com",
      "template" => "welcome"
    })
end
```

## Monitoring

### Telemetry Events

```elixir
# Attach in application.ex
:telemetry.attach_many("oban-logger", [
  [:oban, :job, :start],
  [:oban, :job, :stop],
  [:oban, :job, :exception]
], &MyApp.ObanTelemetry.handle_event/4, %{})
```

### Key Metrics to Track

- Job execution duration (p50, p95, p99)
- Queue depth (available jobs per queue)
- Error rate per worker
- Retry rate per worker

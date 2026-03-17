---
name: elixir-writing-docs
description: Guides writing Elixir documentation with @moduledoc, @doc, @typedoc, doctests, cross-references, and metadata. Use when adding or improving documentation in .ex files.
---

# Elixir Writing Docs

## Quick Reference

| Topic | Reference |
|-------|-----------|
| Doctests: syntax, gotchas, when to use | [references/doctests.md](references/doctests.md) |
| Cross-references and linking syntax | [references/cross-references.md](references/cross-references.md) |
| Admonitions, formatting, tabs | [references/admonitions-and-formatting.md](references/admonitions-and-formatting.md) |

## First-Line Summary Rule

ExDoc and tools like `mix docs` extract the first paragraph of `@moduledoc` and `@doc` as a summary. Keep the opening line concise and self-contained.

```elixir
# GOOD - first line works as a standalone summary
@moduledoc """
Handles payment processing through Stripe and local ledger reconciliation.

Wraps the Stripe API client and ensures each charge is recorded in the
local ledger before returning a confirmation to the caller.
"""

# BAD - first line is vague, forces reader to continue
@moduledoc """
This module contains various functions related to payments.

It uses Stripe and also updates the ledger.
"""
```

The same rule applies to `@doc`:

```elixir
# GOOD
@doc """
Charges a customer's default payment method for the given amount in cents.

Returns `{:ok, charge}` on success or `{:error, reason}` when the payment
gateway rejects the request.
"""

# BAD
@doc """
This function is used to charge a customer.
"""
```

## @moduledoc Structure

A well-structured `@moduledoc` follows this pattern:

```elixir
defmodule MyApp.Inventory do
  @moduledoc """
  Tracks warehouse stock levels and triggers replenishment orders.

  This module maintains an ETS-backed cache of current quantities and
  exposes functions for atomic stock adjustments. It is designed to be
  started under a supervisor and will restore state from the database
  on init.

  ## Examples

      iex> {:ok, pid} = MyApp.Inventory.start_link(warehouse: :east)
      iex> MyApp.Inventory.current_stock(pid, "SKU-1042")
      {:ok, 350}

  ## Configuration

  Expects the following in `config/runtime.exs`:

      config :my_app, MyApp.Inventory,
        repo: MyApp.Repo,
        low_stock_threshold: 50
  """
end
```

**Key points:**

- First paragraph is the summary (one to two sentences).
- `## Examples` shows realistic usage. Use doctests when the example is runnable.
- `## Configuration` documents required config keys. Omit this section if the module takes no config.
- Use second-level headings (`##`) only. First-level (`#`) is reserved for the module name in ExDoc output.

### Documenting Behaviour Modules

When defining a behaviour, document the expected callbacks:

```elixir
defmodule MyApp.PaymentGateway do
  @moduledoc """
  Behaviour for payment gateway integrations.

  Implementations must handle charging, refunding, and status checks.
  See `MyApp.PaymentGateway.Stripe` for a reference implementation.

  ## Callbacks

  * `charge/2` - Initiate a charge for a given amount
  * `refund/2` - Refund a previously completed charge
  * `status/1` - Check the status of a transaction
  """

  @callback charge(amount :: pos_integer(), currency :: atom()) ::
              {:ok, transaction_id :: String.t()} | {:error, term()}

  @callback refund(transaction_id :: String.t(), amount :: pos_integer()) ::
              :ok | {:error, term()}

  @callback status(transaction_id :: String.t()) ::
              {:pending | :completed | :failed, map()}
end
```

## @doc Structure

```elixir
@doc """
Reserves the given quantity of an item, decrementing available stock.

Returns `{:ok, reservation_id}` when stock is available, or
`{:error, :insufficient_stock}` when the requested quantity exceeds
what is on hand.

## Examples

    iex> MyApp.Inventory.reserve("SKU-1042", 5)
    {:ok, "res_abc123"}

    iex> MyApp.Inventory.reserve("SKU-9999", 1)
    {:error, :not_found}

## Options

  * `:warehouse` - Target warehouse atom. Defaults to `:primary`.
  * `:timeout` - Timeout in milliseconds. Defaults to `5_000`.
"""
@spec reserve(String.t(), pos_integer(), keyword()) ::
        {:ok, String.t()} | {:error, :insufficient_stock | :not_found}
def reserve(sku, quantity, opts \\ []) do
  # ...
end
```

**Guidelines:**

- State what the function does, then what it returns.
- Document each option in a bulleted `## Options` section when the function accepts a keyword list.
- Place `@spec` between `@doc` and `def`. This is the conventional ordering.
- Include doctests for pure functions. Skip them for side-effecting functions (see [references/doctests.md](references/doctests.md)).

## @typedoc

Document custom types defined with `@type` or `@opaque`:

```elixir
@typedoc """
A positive integer representing an amount in the smallest currency unit (e.g., cents).
"""
@type amount :: pos_integer()

@typedoc """
Reservation status returned by `status/1`.

  * `:held` - Stock is reserved but not yet shipped
  * `:released` - Reservation was cancelled and stock restored
  * `:fulfilled` - Items have shipped
"""
@type reservation_status :: :held | :released | :fulfilled

@typedoc """
Opaque handle returned by `connect/1`. Do not pattern-match on this value.
"""
@opaque connection :: %__MODULE__{socket: port(), buffer: binary()}
```

For `@opaque` types, the `@typedoc` is especially important because callers cannot inspect the structure.

## Metadata

### @doc since and @doc deprecated

```elixir
@doc since: "1.3.0"
@doc """
Transfers stock between two warehouses.
"""
def transfer(from, to, sku, quantity), do: # ...

@doc deprecated: "Use transfer/4 instead"
@doc """
Moves items between locations. Deprecated in favor of `transfer/4`
which supports cross-region transfers.
"""
def move_stock(from, to, sku, quantity), do: # ...
```

You can combine metadata and the docstring in one attribute:

```elixir
@doc since: "2.0.0", deprecated: "Use bulk_reserve/2 instead"
@doc """
Reserves multiple items in a single call.
"""
def batch_reserve(items), do: # ...
```

`@moduledoc since:` works the same way for modules:

```elixir
@moduledoc since: "1.2.0"
@moduledoc """
Handles webhook signature verification for Stripe events.
"""
```

## When to Use @doc false / @moduledoc false

Suppress documentation when the module or function is not part of the public API:

```elixir
# Private implementation module — internal to the application
defmodule MyApp.Inventory.StockCache do
  @moduledoc false
  # ...
end

# Protocol implementation — documented at the protocol level
defimpl String.Chars, for: MyApp.Money do
  @moduledoc false
  # ...
end

# Callback implementation — documented at the behaviour level
@doc false
def handle_info(:refresh, state) do
  # ...
end

# Helper used only inside the module
@doc false
def do_format(value), do: # ...
```

**Do NOT use `@doc false` on genuinely public functions.** If a function is exported and callers depend on it, document it. If it should not be called externally, make it private with `defp`.

## Documentation vs Code Comments

| | Documentation (`@moduledoc`, `@doc`) | Code Comments (`#`) |
|---|---|---|
| **Audience** | Users of your API | Developers reading source |
| **Purpose** | Contract: what it does, what it returns | Why a particular implementation choice was made |
| **Rendered** | Yes, by ExDoc in HTML/epub | No, visible only in source |
| **Required** | All public modules and functions | Only where code intent is non-obvious |

```elixir
@doc """
Validates that the given coupon code is active and has remaining uses.
"""
@spec validate_coupon(String.t()) :: {:ok, Coupon.t()} | {:error, :expired | :exhausted}
def validate_coupon(code) do
  # We query the read replica here to avoid adding load to the
  # primary during high-traffic discount events.
  Repo.replica().get_by(Coupon, code: code)
  |> check_expiry()
  |> check_remaining_uses()
end
```

The `@doc` tells the caller what `validate_coupon/1` does and returns. The inline comment explains an implementation decision that would otherwise be surprising.

## When to Load References

- Writing doctests or debugging doctest failures --> [references/doctests.md](references/doctests.md)
- Adding links between modules, functions, types --> [references/cross-references.md](references/cross-references.md)
- Using admonition blocks, tabs, or formatting in docs --> [references/admonitions-and-formatting.md](references/admonitions-and-formatting.md)

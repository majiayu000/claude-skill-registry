---
name: saloon
description: Saloon-based service layer pattern for all external API integrations. Every new external API integration must use Saloon — no raw HTTP calls.
---

**Name:** Saloon API Integration
**Description:** Saloon-based service layer pattern for all external API integrations. Every new external API integration must use Saloon — no raw HTTP calls.
**Compatible Agents:** general-purpose, backend
**Tags:** app/Services/**/*.php, laravel, php, backend, saloon, api, http-client, integration

## Rules

- **All** new external API integrations must use the Saloon pattern
- No raw HTTP calls (`Http::get(...)`, `file_get_contents`, `curl`)
- Organize each external integration under `app/Services/{ServiceName}/`
- The connector extends `Saloon\Http\Connector` and handles authentication and base URL
- One class per API endpoint, extending `Saloon\Http\Request`
- Use constructor promotion for request parameters
- GET requests define `defaultQuery()` for query parameters
- POST/PUT requests implement `HasBody` + use `HasJsonBody` trait with `defaultBody()`
- The service class wraps the connector, sends requests, and returns typed DTOs
- Register the connector as a singleton in a service provider when needed
- Accept an optional connector in the service constructor for testability
- Exceptions: **Prism** is acceptable for LLM integrations; inline `Http::get()` is acceptable for simple binary file downloads (not API integrations)

## Examples

**Directory Structure:**
```
app/Services/Stripe/
  StripeConnector.php
  StripeService.php
  Requests/
    Charges/
      CreateChargeRequest.php
      ListChargesRequest.php
  DataObjects/
    ChargeData.php
```

```php
// Connector
namespace App\Services\Stripe;

use Saloon\Http\Connector;

class StripeConnector extends Connector
{
    public function resolveBaseUrl(): string
    {
        return 'https://api.stripe.com/v1';
    }

    protected function defaultHeaders(): array
    {
        return [
            'Authorization' => 'Bearer ' . config('services.stripe.secret'),
            'Content-Type'  => 'application/json',
        ];
    }
}
```

```php
// GET Request
use Saloon\Enums\Method;
use Saloon\Http\Request;

class ListChargesRequest extends Request
{
    protected Method $method = Method::GET;

    public function __construct(
        protected int $limit = 10,
        protected ?string $customer = null,
    ) {}

    public function resolveEndpoint(): string
    {
        return '/charges';
    }

    protected function defaultQuery(): array
    {
        return array_filter([
            'limit'    => $this->limit,
            'customer' => $this->customer,
        ]);
    }
}
```

```php
// Service class
use Illuminate\Support\Collection;

class StripeService
{
    public function __construct(?StripeConnector $connector = null)
    {
        $this->connector = $connector ?? new StripeConnector();
    }

    /** @return Collection<int, ChargeData> */
    public function listCharges(string $customerId): Collection
    {
        $response = $this->connector->send(
            new ListChargesRequest(customer: $customerId)
        );

        return collect($response->json('data'))
            ->map(fn (array $item) => ChargeData::fromArray($item));
    }
}
```

## Anti-Patterns

- Using `Http::get(...)` or `file_get_contents()` for API integrations
- Using `curl` directly
- Creating one massive connector class with all API logic — separate requests into individual classes
- Not returning typed DTOs from the service class (returning raw arrays)
- Not caching expensive or frequently accessed API responses
- Hard-coding API credentials in the connector — always use `config()`

## References

- [Saloon Documentation](https://docs.saloon.dev/)
- Related: `DTO/SKILL.md` — service classes return typed DTOs
- Related: `Services/SKILL.md` — general service class conventions

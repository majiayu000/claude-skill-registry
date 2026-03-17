---
name: resources
description: API resource classes that transform Eloquent models into JSON-ready arrays. Resources control exactly what is exposed in API responses and handle relationships, conditional attributes, and date formatting.
---

**Name:** Resources
**Description:** API resource classes that transform Eloquent models into JSON-ready arrays. Resources control exactly what is exposed in API responses and handle relationships, conditional attributes, and date formatting.
**Compatible Agents:** general-purpose, backend
**Tags:** app/Http/Resources/**/*.php, laravel, php, backend, api, resource, json, response

## Rules

- Resource classes live in `app/Http/Resources/`
- Single resource: `ModelResource` → `UserResource`, `PostResource`
- Collection resource: `ModelCollection` → `UserCollection`, `PostCollection`
- Only expose what the API consumer needs — never blindly expose every model attribute
- Use `whenLoaded()` for related resources — never eager load inside the resource itself
- Use `when()`, `whenHas()`, or `whenNotNull()` for conditional attributes — not `if` statements in the array
- Use `mergeWhen()` for multiple attributes sharing the same condition
- Use `UserResource::collection()` for simple collections — only create a dedicated collection class when custom meta is needed
- Do not add pagination meta manually — pass a paginator directly and let Laravel append it

## Examples

```php
class UserResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id'         => $this->id,
            'name'       => $this->name,
            'email'      => $this->email,
            'posts'      => PostResource::collection($this->whenLoaded('posts')),
            'secret'     => $this->when($request->user()->isAdmin(), $this->secret),
            'bio'        => $this->whenNotNull($this->bio),
            'created_at' => DateHelper::format($this->created_at),
        ];
    }
}
```

```php
// Controller — eager load before passing to resource
return UserResource::collection(User::with('posts')->paginate());
```

```php
// Dedicated collection — only when custom meta is needed
class UserCollection extends ResourceCollection
{
    public function toArray(Request $request): array
    {
        return [
            'data'  => $this->collection,
            'links' => ['self' => route('users.index')],
        ];
    }
}
```

## Anti-Patterns

- Exposing all model attributes without whitelisting
- Eager loading relationships inside the resource's `toArray()` — load them in the controller
- Using `if` statements inside the response array instead of `when()`, `whenLoaded()`, `whenNotNull()`
- Creating a dedicated collection class just for a simple list (use `UserResource::collection()`)
- Putting business logic or database queries in a resource
- Manually adding pagination meta that Laravel already provides automatically

## References

- [Laravel API Resources](https://laravel.com/docs/eloquent-resources)
- Related: `Controllers/SKILL.md` — eager loading is done in the controller
- Related: `Helpers/SKILL.md` — use `DateHelper::format()` for date formatting

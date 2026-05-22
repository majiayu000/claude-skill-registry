---
name: laravel-livewire
description: Build reactive components with Livewire 3, wire:model, actions, lifecycle hooks, Volt, and Folio. Use when creating interactive UI without JavaScript, forms, or real-time updates.
user-invocable: false
---

# Laravel Livewire 3

## Documentation

### Livewire & Related
- [folio.md](docs/folio.md) - File-based routing
- [precognition.md](docs/precognition.md) - Live validation
- [prompts.md](docs/prompts.md) - CLI prompts
- [reverb.md](docs/reverb.md) - WebSockets

## Component Class

```php
<?php

declare(strict_types=1);

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;
use Livewire\Attributes\Rule;
use Livewire\Attributes\Computed;

final class PostList extends Component
{
    use WithPagination;

    public string $search = '';

    #[Rule('required|min:3')]
    public string $title = '';

    #[Computed]
    public function posts()
    {
        return Post::query()
            ->when($this->search, fn ($q) => $q->where('title', 'like', "%{$this->search}%"))
            ->paginate(10);
    }

    public function create(): void
    {
        $this->validate();
        Post::create(['title' => $this->title]);
        $this->reset('title');
        $this->dispatch('post-created');
    }

    public function render()
    {
        return view('livewire.post-list');
    }
}
```

## Blade View

```blade
<div>
    <input type="text" wire:model.live.debounce.300ms="search">

    <form wire:submit="create">
        <input type="text" wire:model="title">
        @error('title') <span>{{ $message }}</span> @enderror
        <button type="submit">Create</button>
    </form>

    @foreach($this->posts as $post)
        <div wire:key="{{ $post->id }}">
            {{ $post->title }}
            <button wire:click="delete({{ $post->id }})" wire:confirm="Delete?">
                Delete
            </button>
        </div>
    @endforeach

    {{ $this->posts->links() }}
</div>
```

## Volt (Single-File)

```php
<?php
use function Livewire\Volt\{state, computed};

state(['count' => 0]);
$increment = fn () => $this->count++;
$doubled = computed(fn () => $this->count * 2);
?>

<div>
    <h1>{{ $count }}</h1>
    <p>Doubled: {{ $this->doubled }}</p>
    <button wire:click="increment">+</button>
</div>
```

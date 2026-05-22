---
name: action-view-best-practices
description: Build or Refactor Rails views, partials, and templates into clean, maintainable code. Use when views have inline Ruby logic, deeply nested partials, jQuery or legacy JavaScript, helper methods returning HTML, or when the user asks to modernize, refactor, or clean up Rails views. Applies patterns - Turbo Frames, Turbo Streams, Stimulus controllers, ViewComponent, presenters, strict locals, and proper partial extraction.
---

# Rails View Refactoring

Views should contain markup and minimal display logic. If a view has conditionals, calculations, query calls, or complex Ruby blocks, it needs refactoring. The modern Rails 8+ stack uses Hotwire (Turbo + Stimulus) for interactivity, Propshaft for assets, and Importmap for JavaScript — no build step required.

## Decision Framework

Read the view and classify each block of code:

| Code type                                               | Extract to                      | Location                                   |
| ------------------------------------------------------- | ------------------------------- | ------------------------------------------ |
| Reusable UI patterns (buttons, cards, modals, badges)   | ViewComponent                   | `app/components/`                          |
| Display logic (formatting, conditional CSS, label text) | Presenter or ViewComponent      | `app/presenters/` or `app/components/`     |
| HTML-returning helper methods                           | ViewComponent                   | `app/components/`                          |
| Inline `<script>` tags and jQuery                       | Stimulus controller             | `app/javascript/controllers/`              |
| AJAX calls, remote forms, `$.ajax`                      | Turbo Frame or Turbo Stream     | ERB template + controller response         |
| Partial page updates via JavaScript                     | Turbo Frame                     | Wrap in `turbo_frame_tag`                  |
| Real-time broadcasts (chat, notifications)              | Turbo Stream                    | Model `broadcasts_to` or controller stream |
| One-off page sections that are too long                 | Partial with strict locals      | `app/views/shared/` or alongside view      |
| Complex data assembly for the view                      | Presenter                       | `app/presenters/`                          |
| Repeated inline Ruby (loops with logic)                 | Collection partial or component | Partial or component                       |
| Instance variables used across partials                 | Locals / strict locals          | Pass explicitly                            |

## Modernizing to Hotwire

### Replace jQuery AJAX with Turbo Frames

Turbo Frames update a specific section of the page without a full reload. No JavaScript needed.

```erb
<%# Before — jQuery AJAX %>
<div id="player-stats"></div>
<script>
  $.get('/players/<%= @player.id %>/stats', function(data) {
    $('#player-stats').html(data);
  });
</script>

<%# After — Turbo Frame %>
<%= turbo_frame_tag "player_stats" do %>
  <%= render partial: "players/stats", locals: { player: @player } %>
<% end %>
```

The linked page just needs a matching `turbo_frame_tag` with the same ID and Turbo handles the rest.

### Replace Remote Forms with Turbo

Rails UJS `remote: true` forms are deprecated. Turbo handles forms natively.

```erb
<%# Before — Rails UJS %>
<%= form_with model: @player, remote: true do |f| %>
  ...
<% end %>

<%# After — Turbo (just remove remote: true, Turbo handles it) %>
<%= form_with model: @player do |f| %>
  ...
<% end %>
```

Turbo intercepts all form submissions by default. For partial updates, wrap the form in a `turbo_frame_tag`. For multi-target updates, respond with a Turbo Stream:

```erb
<%# app/views/players/update.turbo_stream.erb %>
<%= turbo_stream.replace "player_header" do %>
  <%= render partial: "players/header", locals: { player: @player } %>
<% end %>

<%= turbo_stream.update "flash_messages" do %>
  <%= render partial: "shared/flash" %>
<% end %>
```

### Replace Inline JavaScript with Stimulus

Any behavior attached to DOM elements (toggles, dropdowns, form validation, clipboard, modals) should be a Stimulus controller.

```erb
<%# Before — inline JS / jQuery %>
<button onclick="document.getElementById('details').classList.toggle('hidden')">
  Toggle
</button>
<div id="details" class="hidden">...</div>

<%# After — Stimulus %>
<div data-controller="toggle">
  <button data-action="click->toggle#switch">Toggle</button>
  <div data-toggle-target="content" class="hidden">...</div>
</div>
```

```javascript
// app/javascript/controllers/toggle_controller.js
import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
  static targets = ["content"];

  switch() {
    this.contentTarget.classList.toggle("hidden");
  }
}
```

Conventions:

- One behavior per controller — keep them small and composable
- Name controllers after what they do: `toggle`, `clipboard`, `dropdown`, `search-form`
- Use `targets` for elements, `values` for data, `classes` for CSS class names
- Never manipulate DOM outside the controller's element scope

### Replace Polling with Turbo Streams

For real-time updates, use Turbo Streams over WebSockets instead of JavaScript polling.

```ruby
# app/models/score.rb
class Score < ApplicationRecord
  broadcasts_to ->(score) { [score.game] }, inserts_by: :prepend
end
```

```erb
<%# Subscribe in the view %>
<%= turbo_stream_from @game %>

<div id="scores">
  <%= render @game.scores %>
</div>
```

New scores automatically appear without any JavaScript.

## View Component Patterns

### When to Use ViewComponent vs Partials

Use **partials** for:

- One-off page sections that won't be reused
- Simple markup extraction to reduce file length
- Layouts and structural wrappers

Use **ViewComponent** for:

- Reusable UI elements (buttons, cards, badges, modals, alerts)
- Components with display logic or multiple variants
- Anything you'd want to unit test in isolation
- Complex components with slots for flexible content injection

### ViewComponent Example

```ruby
# app/components/stat_card_component.rb
class StatCardComponent < ViewComponent::Base
  def initialize(label:, value:, trend: nil)
    @label = label
    @value = value
    @trend = trend
  end

  def trend_class
    case @trend
    when :up then "text-green-600"
    when :down then "text-red-600"
    else "text-gray-500"
    end
  end
end
```

```erb
<%# app/components/stat_card_component.html.erb %>
<div class="rounded-lg border p-4">
  <dt class="text-sm text-gray-500"><%= @label %></dt>
  <dd class="text-2xl font-semibold"><%= @value %></dd>
  <% if @trend %>
    <span class="<%= trend_class %>"><%= @trend == :up ? "↑" : "↓" %></span>
  <% end %>
</div>
```

```erb
<%# Usage %>
<%= render StatCardComponent.new(label: "Batting Avg", value: ".312", trend: :up) %>
```

## Partial Best Practices

### Use Strict Locals

Always declare expected locals at the top of partials. This was added in Rails 7.1 and prevents silent nil bugs.

```erb
<%# app/views/players/_card.html.erb %>
<%# locals: (player:, show_stats: false) %>

<div class="player-card">
  <h3><%= player.name %></h3>
  <% if show_stats %>
    <%= render partial: "players/stats", locals: { player: player } %>
  <% end %>
</div>
```

### Use Collection Rendering

Never loop and render partials manually.

```erb
<%# Before — slow, verbose %>
<% @players.each do |player| %>
  <%= render partial: "players/card", locals: { player: player } %>
<% end %>

<%# After — collection rendering (faster, cleaner) %>
<%= render partial: "players/card", collection: @players, as: :player %>
```

### Avoid Deeply Nested Partials

If partial A renders partial B which renders partial C, it's too deep. Flatten the structure or extract to a ViewComponent that composes its own sub-components.

## Presenters for Complex View Logic

When a view needs data from multiple sources or complex formatting, use a presenter instead of cramming logic into the template.

```ruby
# app/presenters/player_profile_presenter.rb
class PlayerProfilePresenter
  def initialize(player, current_user)
    @player = player
    @current_user = current_user
  end

  def display_name
    "#{@player.first_name} #{@player.last_name}"
  end

  def contract_status_badge
    if @player.free_agent?
      { text: "Free Agent", color: "green" }
    elsif @player.contract_years_remaining <= 1
      { text: "Expiring", color: "yellow" }
    else
      { text: "Under Contract", color: "gray" }
    end
  end

  def can_edit?
    @current_user.admin? || @current_user.team == @player.team
  end

  def formatted_salary
    ActiveSupport::NumberHelper.number_to_currency(@player.salary)
  end
end
```

```erb
<%# Clean view %>
<h1><%= @presenter.display_name %></h1>

<% badge = @presenter.contract_status_badge %>
<%= render BadgeComponent.new(text: badge[:text], color: badge[:color]) %>

<%= @presenter.formatted_salary %>

<% if @presenter.can_edit? %>
  <%= link_to "Edit", edit_player_path(@player) %>
<% end %>
```

## Eliminating Helper Abuse

Rails helpers that return HTML are hard to test, hard to read, and hard to compose. Move them to ViewComponents.

```ruby
# Before — helper returning HTML (bad)
module PlayersHelper
  def player_avatar(player, size: :md)
    sizes = { sm: "w-8 h-8", md: "w-12 h-12", lg: "w-16 h-16" }
    if player.avatar.attached?
      image_tag player.avatar, class: "rounded-full #{sizes[size]}"
    else
      content_tag :div, player.initials,
        class: "rounded-full #{sizes[size]} bg-gray-300 flex items-center justify-center"
    end
  end
end

# After — ViewComponent (good)
# app/components/avatar_component.rb
class AvatarComponent < ViewComponent::Base
  SIZES = { sm: "w-8 h-8", md: "w-12 h-12", lg: "w-16 h-16" }.freeze

  def initialize(player:, size: :md)
    @player = player
    @size = size
  end
  # ... with its own template and tests
end
```

Keep helpers for non-HTML formatting utilities only (number formatting, date formatting, text truncation).

## Refactoring Process

1. **Audit the view layer** — identify inline Ruby logic, jQuery, `remote: true` forms, helpers returning HTML, and deeply nested partials.
2. **Remove jQuery and inline JS first** — replace with Stimulus controllers. This is the highest-impact change.
3. **Replace `remote: true` and AJAX** — Turbo handles forms and links natively. Convert to Turbo Frames and Turbo Streams.
4. **Add strict locals** to all existing partials.
5. **Extract reusable UI patterns** into ViewComponents.
6. **Move display logic** from views into presenters or component classes.
7. **Move HTML-returning helpers** into components.
8. **Flatten nested partials** — if nesting is deeper than 2 levels, restructure.
9. **Add collection rendering** wherever loops render partials.
10. **Remove all instance variables from partials** — pass data via locals only.

## What NOT to Do

- Don't put query calls in views — ever. Not even `count` or `any?`. Use the presenter or controller.
- Don't use `content_for` for complex logic — it creates invisible dependencies between layouts and views.
- Don't create Stimulus controllers that replicate what Turbo Frames already handle.
- Don't mix jQuery and Stimulus in the same app — commit to full migration.
- Don't render entire pages as ViewComponents — they are for reusable pieces, not whole pages.
- Don't use `html_safe` or `raw` unless you are certain the content is sanitized.
- Don't pass more than 3-4 locals to a partial — if you need more, it should be a component or presenter.
- Don't use `render partial:` inside loops — use collection rendering instead.

---
name: action-controller-best-practices
description: Build or Refactor large Rails controller files into clean, maintainable code. Use when a controller action exceeds ~10 lines, a controller has custom non-RESTful actions, or when the user asks to refactor, slim down, clean up, or organize a Rails controller. Applies patterns: service objects, query objects, form objects, controller concerns, presenters/decorators, and RESTful resource extraction.
---

# Rails Controller Refactoring

Controllers should be thin traffic cops — they receive input via params, delegate to the appropriate object, and decide what to render or redirect. Each action should be roughly 5-10 lines. If an action is longer, logic needs to be extracted.

## Decision Framework

Read the controller and classify each block of code:

| Code type                                               | Extract to             | Location                               |
| ------------------------------------------------------- | ---------------------- | -------------------------------------- |
| Business logic, multi-step operations, side effects     | Service object         | `app/services/`                        |
| Complex queries, filtering, sorting, search             | Query object           | `app/queries/`                         |
| Context-specific param validation and persistence       | Form object            | `app/forms/`                           |
| Shared before_actions, auth, pagination, error handling | Controller concern     | `app/controllers/concerns/`            |
| Complex view data assembly, formatting, display logic   | Presenter / Decorator  | `app/presenters/` or `app/decorators/` |
| Non-RESTful custom actions on a different concept       | New RESTful controller | `app/controllers/`                     |
| Simple CRUD, strong params, render/redirect             | Keep on controller     | —                                      |

## Patterns

### Service Objects

Use for any business logic that goes beyond simple CRUD. A controller action should call one service at most.

Before:

```ruby
def create
  @player = Player.new(player_params)
  @player.team = Team.find(params[:team_id])
  @player.contract_start = Time.current
  @player.status = :active

  if @player.save
    PlayerMailer.welcome(@player).deliver_later
    Analytics.track("player_signed", player_id: @player.id)
    NotifyScoutsJob.perform_later(@player.team_id)
    redirect_to @player, notice: "Player signed"
  else
    render :new, status: :unprocessable_entity
  end
end
```

After:

```ruby
# Controller
def create
  result = Players::SignPlayer.new(player_params, team_id: params[:team_id]).call

  if result.success?
    redirect_to result.player, notice: "Player signed"
  else
    @player = result.player
    render :new, status: :unprocessable_entity
  end
end

# app/services/players/sign_player.rb
module Players
  class SignPlayer
    def initialize(params, team_id:)
      @params = params
      @team_id = team_id
    end

    def call
      player = Player.new(@params)
      player.team = Team.find(@team_id)
      player.contract_start = Time.current
      player.status = :active

      if player.save
        send_notifications(player)
        Result.new(success: true, player: player)
      else
        Result.new(success: false, player: player)
      end
    end

    private

    def send_notifications(player)
      PlayerMailer.welcome(player).deliver_later
      Analytics.track("player_signed", player_id: player.id)
      NotifyScoutsJob.perform_later(player.team_id)
    end

    Result = Struct.new(:success, :player, keyword_init: true) do
      alias_method :success?, :success
    end
  end
end
```

### Query Objects

Use when index actions have complex filtering, sorting, or search logic.

Before:

```ruby
def index
  @players = Player.where(team_id: params[:team_id])
  @players = @players.where(position: params[:position]) if params[:position].present?
  @players = @players.where("age >= ?", params[:min_age]) if params[:min_age].present?
  @players = @players.where(status: :active) unless params[:include_inactive]
  @players = @players.joins(:stats).order("stats.war DESC")
  @players = @players.page(params[:page]).per(25)
end
```

After:

```ruby
# Controller
def index
  @players = Players::FilterQuery.new(params).call
end

# app/queries/players/filter_query.rb
module Players
  class FilterQuery
    def initialize(params, relation: Player.all)
      @params = params
      @relation = relation
    end

    def call
      filter_by_team
      filter_by_position
      filter_by_age
      filter_by_status
      sort_and_paginate
      @relation
    end

    private

    def filter_by_team
      @relation = @relation.where(team_id: @params[:team_id]) if @params[:team_id].present?
    end

    def filter_by_position
      @relation = @relation.where(position: @params[:position]) if @params[:position].present?
    end

    def filter_by_age
      @relation = @relation.where("age >= ?", @params[:min_age]) if @params[:min_age].present?
    end

    def filter_by_status
      @relation = @relation.where(status: :active) unless @params[:include_inactive]
    end

    def sort_and_paginate
      @relation = @relation.joins(:stats).order("stats.war DESC").page(@params[:page]).per(25)
    end
  end
end
```

### Controller Concerns

Use for shared behavior across multiple controllers: authentication, authorization, pagination, error handling, locale setting.

```ruby
# app/controllers/concerns/paginatable.rb
module Paginatable
  extend ActiveSupport::Concern

  private

  def page
    params[:page] || 1
  end

  def per_page
    [params[:per_page].to_i, 100].min.nonzero? || 25
  end
end

# app/controllers/concerns/error_handleable.rb
module ErrorHandleable
  extend ActiveSupport::Concern

  included do
    rescue_from ActiveRecord::RecordNotFound, with: :not_found
    rescue_from ActionController::ParameterMissing, with: :bad_request
  end

  private

  def not_found
    render json: { error: "Not found" }, status: :not_found
  end

  def bad_request(exception)
    render json: { error: exception.message }, status: :bad_request
  end
end
```

Guidelines for controller concerns:

- Each concern should handle one cross-cutting aspect
- Don't use concerns to just split a large controller into files — that hides complexity
- Good candidates: auth, error handling, pagination, locale, current tenant scoping
- Bad candidates: domain-specific business logic

### Presenters / Decorators

Use when an action assembles complex data for the view that isn't a direct model attribute. Keeps view logic out of the controller.

```ruby
# app/presenters/player_dashboard_presenter.rb
class PlayerDashboardPresenter
  def initialize(player)
    @player = player
  end

  def career_stats
    @career_stats ||= @player.stats.group(:season).sum(:war)
  end

  def contract_status_label
    return "Free Agent" if @player.contract_end&.past?
    "Under Contract (#{@player.contract_end&.year})"
  end

  def trade_value_rating
    case @player.trade_value
    when 90.. then "Elite"
    when 70..89 then "High"
    when 50..69 then "Average"
    else "Low"
    end
  end
end

# Controller
def show
  @player = Player.find(params[:id])
  @presenter = PlayerDashboardPresenter.new(@player)
end
```

### RESTful Resource Extraction

When a controller has custom non-RESTful actions, it usually means there's a hidden resource. Extract it into its own controller with standard CRUD actions.

Before:

```ruby
class PlayersController < ApplicationController
  def trade
    # ...
  end

  def release
    # ...
  end

  def promote_to_roster
    # ...
  end
end
```

After:

```ruby
# config/routes.rb
resources :players do
  resource :trade, only: [:new, :create], controller: "players/trades"
  resource :release, only: [:create], controller: "players/releases"
  resource :roster_promotion, only: [:create], controller: "players/roster_promotions"
end

# app/controllers/players/trades_controller.rb
module Players
  class TradesController < ApplicationController
    def new
      @player = Player.find(params[:player_id])
    end

    def create
      result = Players::TradePlayer.new(Player.find(params[:player_id]), trade_params).call
      # ...
    end
  end
end
```

Signs you need a new controller:

- Action name is a verb that isn't a CRUD verb (trade, approve, archive, publish)
- Action operates on a different concept than the controller's resource
- Controller has more than the 7 RESTful actions

## Refactoring Process

1. **Read the entire controller** and identify every action, before_action, and private method.
2. **Inline hidden code first.** Copy logic from before_actions, helper methods, and parent classes into each action so you can see the full picture.
3. **Classify each block** using the decision framework table above.
4. **Extract in order**: RESTful resource extraction first (new controllers), then service objects, query objects, form objects, presenters, and finally concerns.
5. **Slim down each action** to: find/build the resource, call a service or query, render or redirect. Each action should be 5-10 lines.
6. **Clean up strong params.** Each controller should have one `_params` method. If you need different permitted params per action, consider separate controllers or form objects.
7. **Create or update tests** for each extracted class with its own spec file.

## What the Controller Should Look Like After

```ruby
class PlayersController < ApplicationController
  before_action :set_player, only: [:show, :edit, :update, :destroy]

  def index
    @players = Players::FilterQuery.new(params).call
  end

  def show
    @presenter = PlayerDashboardPresenter.new(@player)
  end

  def create
    result = Players::SignPlayer.new(player_params, team_id: params[:team_id]).call

    if result.success?
      redirect_to result.player, notice: "Player signed"
    else
      @player = result.player
      render :new, status: :unprocessable_entity
    end
  end

  def update
    if @player.update(player_params)
      redirect_to @player, notice: "Player updated"
    else
      render :edit, status: :unprocessable_entity
    end
  end

  def destroy
    @player.destroy
    redirect_to players_path, notice: "Player removed"
  end

  private

  def set_player
    @player = Player.find(params[:id])
  end

  def player_params
    params.require(:player).permit(:name, :position, :age, :team_id)
  end
end
```

## What NOT to Do

- Don't put business logic in before_actions — they obscure the flow of an action.
- Don't use instance variables to pass data between before_actions and actions in complex ways.
- Don't rescue broad exceptions in individual actions — use a concern or `rescue_from`.
- Don't add non-RESTful actions to a controller when a new controller would be clearer.
- Don't create deeply nested service call chains — one service per action is the goal.
- Don't move logic to private methods and call it refactored — private methods still live in the controller.

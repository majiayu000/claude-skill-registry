---
name: faion-backend-skill
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Backend Development Skill

**Multi-language backend patterns for production-grade applications.**

---

## Overview

This skill covers 6 backend languages with 4 methodologies each (24 total):

| Language | Frameworks | Methodologies |
|----------|------------|---------------|
| **Go** | Gin, Echo, stdlib | 4 |
| **Ruby** | Rails, Sinatra | 4 |
| **PHP** | Laravel, Symfony | 4 |
| **Java** | Spring Boot | 4 |
| **C#** | .NET Core, ASP.NET | 4 |
| **Rust** | Actix, Axum | 4 |

---

## Cross-Language Patterns

### API Design Principles

| Pattern | Description |
|---------|-------------|
| **RESTful Resources** | Use nouns, not verbs: `/users`, `/orders` |
| **HTTP Methods** | GET (read), POST (create), PUT (replace), PATCH (update), DELETE (remove) |
| **Status Codes** | 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 Server Error |
| **Pagination** | Use `?page=1&per_page=20` or cursor-based for large datasets |
| **Versioning** | URL path `/api/v1/` or header `Accept: application/vnd.api+v1` |

### Database Access Patterns

| Pattern | When to Use |
|---------|-------------|
| **ORM** | Rapid development, complex relations |
| **Query Builder** | Balance between control and safety |
| **Raw SQL** | Performance-critical, complex queries |
| **Repository** | Abstraction layer, testability |

### Error Handling

```
Standard Error Response Format:
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [{"field": "email", "message": "Invalid format"}]
  }
}
```

---

# Go Backend (4 Methodologies)

## M-GO-001: Project Structure

### Problem
Organize Go projects for maintainability and team collaboration.

### Framework: Standard Layout

```
project/
├── cmd/
│   └── api/
│       └── main.go           # Entry point
├── internal/
│   ├── handler/              # HTTP handlers
│   ├── service/              # Business logic
│   ├── repository/           # Data access
│   ├── model/                # Domain models
│   ├── middleware/           # HTTP middleware
│   └── config/               # Configuration
├── pkg/                      # Public packages
├── migrations/               # Database migrations
├── go.mod
└── go.sum
```

### Key Principles

- `internal/` prevents external imports
- `cmd/` for multiple binaries
- Flat structure within packages
- Interfaces defined at consumer side

### Example: Handler

```go
// internal/handler/user.go
package handler

import (
    "net/http"
    "github.com/gin-gonic/gin"
    "project/internal/service"
)

type UserHandler struct {
    userService service.UserService
}

func NewUserHandler(us service.UserService) *UserHandler {
    return &UserHandler{userService: us}
}

func (h *UserHandler) GetUser(c *gin.Context) {
    id := c.Param("id")
    user, err := h.userService.GetByID(c.Request.Context(), id)
    if err != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
        return
    }
    c.JSON(http.StatusOK, user)
}
```

---

## M-GO-002: HTTP Handlers (Gin/Echo)

### Problem
Build performant HTTP APIs with proper request handling.

### Framework: Gin Router

```go
package main

import (
    "github.com/gin-gonic/gin"
    "project/internal/handler"
    "project/internal/middleware"
)

func SetupRouter(h *handler.UserHandler) *gin.Engine {
    r := gin.Default()

    // Global middleware
    r.Use(middleware.RequestID())
    r.Use(middleware.Logger())
    r.Use(middleware.Recovery())

    // API v1
    v1 := r.Group("/api/v1")
    {
        users := v1.Group("/users")
        users.Use(middleware.Auth())
        {
            users.GET("", h.ListUsers)
            users.GET("/:id", h.GetUser)
            users.POST("", h.CreateUser)
            users.PUT("/:id", h.UpdateUser)
            users.DELETE("/:id", h.DeleteUser)
        }
    }

    return r
}
```

### Framework: Echo Router

```go
package main

import (
    "github.com/labstack/echo/v4"
    "github.com/labstack/echo/v4/middleware"
)

func SetupRouter() *echo.Echo {
    e := echo.New()

    e.Use(middleware.Logger())
    e.Use(middleware.Recover())
    e.Use(middleware.RequestID())

    api := e.Group("/api/v1")
    api.Use(middleware.JWT([]byte("secret")))

    api.GET("/users", listUsers)
    api.GET("/users/:id", getUser)
    api.POST("/users", createUser)

    return e
}
```

### Request Binding

```go
type CreateUserRequest struct {
    Name  string `json:"name" binding:"required,min=2,max=100"`
    Email string `json:"email" binding:"required,email"`
    Age   int    `json:"age" binding:"gte=0,lte=130"`
}

func (h *UserHandler) CreateUser(c *gin.Context) {
    var req CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    // Process valid request
}
```

---

## M-GO-003: Concurrency Patterns

### Problem
Handle concurrent operations safely and efficiently.

### Framework: Worker Pool

```go
package worker

import (
    "context"
    "sync"
)

type Job func(ctx context.Context) error

type Pool struct {
    workers int
    jobs    chan Job
    wg      sync.WaitGroup
}

func NewPool(workers int, buffer int) *Pool {
    return &Pool{
        workers: workers,
        jobs:    make(chan Job, buffer),
    }
}

func (p *Pool) Start(ctx context.Context) {
    for i := 0; i < p.workers; i++ {
        p.wg.Add(1)
        go p.worker(ctx)
    }
}

func (p *Pool) worker(ctx context.Context) {
    defer p.wg.Done()
    for {
        select {
        case <-ctx.Done():
            return
        case job, ok := <-p.jobs:
            if !ok {
                return
            }
            _ = job(ctx) // Handle error as needed
        }
    }
}

func (p *Pool) Submit(job Job) {
    p.jobs <- job
}

func (p *Pool) Stop() {
    close(p.jobs)
    p.wg.Wait()
}
```

### Framework: Fan-Out/Fan-In

```go
func ProcessItems(ctx context.Context, items []Item) []Result {
    numWorkers := runtime.NumCPU()
    jobs := make(chan Item, len(items))
    results := make(chan Result, len(items))

    // Fan-out: start workers
    var wg sync.WaitGroup
    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for item := range jobs {
                results <- processItem(ctx, item)
            }
        }()
    }

    // Send jobs
    for _, item := range items {
        jobs <- item
    }
    close(jobs)

    // Wait and close results
    go func() {
        wg.Wait()
        close(results)
    }()

    // Fan-in: collect results
    var output []Result
    for r := range results {
        output = append(output, r)
    }
    return output
}
```

---

## M-GO-004: Error Handling

### Problem
Consistent error handling with proper context.

### Framework: Custom Errors

```go
package apperror

import (
    "fmt"
    "net/http"
)

type AppError struct {
    Code       string `json:"code"`
    Message    string `json:"message"`
    HTTPStatus int    `json:"-"`
    Err        error  `json:"-"`
}

func (e *AppError) Error() string {
    if e.Err != nil {
        return fmt.Sprintf("%s: %v", e.Message, e.Err)
    }
    return e.Message
}

func (e *AppError) Unwrap() error {
    return e.Err
}

// Common errors
var (
    ErrNotFound = &AppError{
        Code:       "NOT_FOUND",
        Message:    "Resource not found",
        HTTPStatus: http.StatusNotFound,
    }
    ErrUnauthorized = &AppError{
        Code:       "UNAUTHORIZED",
        Message:    "Authentication required",
        HTTPStatus: http.StatusUnauthorized,
    }
    ErrValidation = &AppError{
        Code:       "VALIDATION_ERROR",
        Message:    "Invalid input",
        HTTPStatus: http.StatusBadRequest,
    }
)

func NewNotFound(resource string) *AppError {
    return &AppError{
        Code:       "NOT_FOUND",
        Message:    fmt.Sprintf("%s not found", resource),
        HTTPStatus: http.StatusNotFound,
    }
}

func Wrap(err error, message string) *AppError {
    return &AppError{
        Code:       "INTERNAL_ERROR",
        Message:    message,
        HTTPStatus: http.StatusInternalServerError,
        Err:        err,
    }
}
```

### Middleware Error Handler

```go
func ErrorHandler() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()

        if len(c.Errors) > 0 {
            err := c.Errors.Last().Err
            if appErr, ok := err.(*apperror.AppError); ok {
                c.JSON(appErr.HTTPStatus, gin.H{
                    "error": gin.H{
                        "code":    appErr.Code,
                        "message": appErr.Message,
                    },
                })
                return
            }
            c.JSON(http.StatusInternalServerError, gin.H{
                "error": gin.H{
                    "code":    "INTERNAL_ERROR",
                    "message": "An unexpected error occurred",
                },
            })
        }
    }
}
```

---

# Ruby Backend (4 Methodologies)

## M-RUBY-001: Rails Patterns

### Problem
Structure Rails applications for scalability and maintainability.

### Framework: Service Objects

```ruby
# app/services/users/create_service.rb
module Users
  class CreateService
    def initialize(params:, current_user: nil)
      @params = params
      @current_user = current_user
    end

    def call
      user = User.new(user_params)

      ActiveRecord::Base.transaction do
        user.save!
        send_welcome_email(user)
        create_audit_log(user)
      end

      ServiceResult.success(user)
    rescue ActiveRecord::RecordInvalid => e
      ServiceResult.failure(e.record.errors.full_messages)
    end

    private

    def user_params
      @params.slice(:name, :email, :password)
    end

    def send_welcome_email(user)
      UserMailer.welcome(user).deliver_later
    end

    def create_audit_log(user)
      AuditLog.create!(
        action: 'user.created',
        resource: user,
        actor: @current_user
      )
    end
  end
end

# app/services/service_result.rb
class ServiceResult
  attr_reader :data, :errors

  def initialize(success:, data: nil, errors: [])
    @success = success
    @data = data
    @errors = errors
  end

  def success?
    @success
  end

  def failure?
    !@success
  end

  def self.success(data = nil)
    new(success: true, data: data)
  end

  def self.failure(errors)
    new(success: false, errors: Array(errors))
  end
end
```

### Controller Usage

```ruby
# app/controllers/api/v1/users_controller.rb
module Api
  module V1
    class UsersController < ApplicationController
      def create
        result = Users::CreateService.new(
          params: user_params,
          current_user: current_user
        ).call

        if result.success?
          render json: UserSerializer.new(result.data), status: :created
        else
          render json: { errors: result.errors }, status: :unprocessable_entity
        end
      end

      private

      def user_params
        params.require(:user).permit(:name, :email, :password)
      end
    end
  end
end
```

---

## M-RUBY-002: ActiveRecord Patterns

### Problem
Efficient database access with proper query optimization.

### Framework: Query Objects

```ruby
# app/queries/users_query.rb
class UsersQuery
  def initialize(relation = User.all)
    @relation = relation
  end

  def active
    @relation = @relation.where(active: true)
    self
  end

  def with_role(role)
    @relation = @relation.where(role: role)
    self
  end

  def created_after(date)
    @relation = @relation.where('created_at > ?', date)
    self
  end

  def search(term)
    return self if term.blank?
    @relation = @relation.where(
      'name ILIKE :term OR email ILIKE :term',
      term: "%#{term}%"
    )
    self
  end

  def ordered
    @relation = @relation.order(created_at: :desc)
    self
  end

  def with_associations
    @relation = @relation.includes(:profile, :roles)
    self
  end

  def paginate(page:, per_page: 20)
    @relation = @relation.page(page).per(per_page)
    self
  end

  def results
    @relation
  end
end

# Usage
users = UsersQuery.new
  .active
  .with_role('admin')
  .search(params[:q])
  .with_associations
  .ordered
  .paginate(page: params[:page])
  .results
```

### Scopes and Callbacks

```ruby
# app/models/user.rb
class User < ApplicationRecord
  # Associations
  has_one :profile, dependent: :destroy
  has_many :orders, dependent: :nullify
  has_many :roles, through: :user_roles

  # Validations
  validates :email, presence: true, uniqueness: { case_sensitive: false }
  validates :name, presence: true, length: { minimum: 2, maximum: 100 }

  # Scopes
  scope :active, -> { where(active: true) }
  scope :admins, -> { joins(:roles).where(roles: { name: 'admin' }) }
  scope :recent, -> { where('created_at > ?', 30.days.ago) }

  # Callbacks
  before_validation :normalize_email
  after_create_commit :send_welcome_email

  private

  def normalize_email
    self.email = email&.downcase&.strip
  end

  def send_welcome_email
    UserMailer.welcome(self).deliver_later
  end
end
```

---

## M-RUBY-003: RSpec Testing

### Problem
Write comprehensive, maintainable tests.

### Framework: Model Specs

```ruby
# spec/models/user_spec.rb
require 'rails_helper'

RSpec.describe User, type: :model do
  describe 'validations' do
    it { is_expected.to validate_presence_of(:email) }
    it { is_expected.to validate_presence_of(:name) }
    it { is_expected.to validate_uniqueness_of(:email).case_insensitive }
    it { is_expected.to validate_length_of(:name).is_at_least(2).is_at_most(100) }
  end

  describe 'associations' do
    it { is_expected.to have_one(:profile).dependent(:destroy) }
    it { is_expected.to have_many(:orders).dependent(:nullify) }
  end

  describe 'scopes' do
    describe '.active' do
      let!(:active_user) { create(:user, active: true) }
      let!(:inactive_user) { create(:user, active: false) }

      it 'returns only active users' do
        expect(User.active).to eq([active_user])
      end
    end
  end

  describe '#full_name' do
    let(:user) { build(:user, first_name: 'John', last_name: 'Doe') }

    it 'returns combined first and last name' do
      expect(user.full_name).to eq('John Doe')
    end
  end
end
```

### Service Specs

```ruby
# spec/services/users/create_service_spec.rb
require 'rails_helper'

RSpec.describe Users::CreateService do
  describe '#call' do
    subject(:service) { described_class.new(params: params) }

    context 'with valid params' do
      let(:params) { { name: 'John', email: 'john@example.com', password: 'secret123' } }

      it 'creates a user' do
        expect { service.call }.to change(User, :count).by(1)
      end

      it 'returns success result' do
        result = service.call
        expect(result).to be_success
        expect(result.data).to be_a(User)
      end

      it 'sends welcome email' do
        expect { service.call }
          .to have_enqueued_mail(UserMailer, :welcome)
      end
    end

    context 'with invalid params' do
      let(:params) { { name: '', email: 'invalid' } }

      it 'does not create a user' do
        expect { service.call }.not_to change(User, :count)
      end

      it 'returns failure result with errors' do
        result = service.call
        expect(result).to be_failure
        expect(result.errors).to include(/Email/)
      end
    end
  end
end
```

---

## M-RUBY-004: Sidekiq Background Jobs

### Problem
Process tasks asynchronously for better performance.

### Framework: Job Structure

```ruby
# app/jobs/process_order_job.rb
class ProcessOrderJob
  include Sidekiq::Job

  sidekiq_options queue: :default, retry: 3, dead: true

  sidekiq_retry_in do |count, exception|
    case exception
    when PaymentGatewayError
      (count + 1) * 60 # Linear backoff for payment issues
    else
      (count ** 4) + 15 # Exponential backoff
    end
  end

  def perform(order_id)
    order = Order.find(order_id)

    return if order.processed?

    OrderProcessor.new(order).process!

    NotifyCustomerJob.perform_async(order_id)
  rescue ActiveRecord::RecordNotFound
    # Order deleted, nothing to do
    Sidekiq.logger.warn "Order #{order_id} not found"
  rescue PaymentGatewayError => e
    # Will retry with custom backoff
    raise
  rescue StandardError => e
    ErrorTracker.capture(e, order_id: order_id)
    raise
  end
end

# app/jobs/notify_customer_job.rb
class NotifyCustomerJob
  include Sidekiq::Job

  sidekiq_options queue: :notifications, retry: 5

  def perform(order_id)
    order = Order.find(order_id)
    OrderMailer.confirmation(order).deliver_now
  end
end
```

### Batch Processing

```ruby
# app/jobs/batch_export_job.rb
class BatchExportJob
  include Sidekiq::Job

  sidekiq_options queue: :exports, retry: 1

  def perform(export_id)
    export = Export.find(export_id)
    export.update!(status: :processing)

    records = export.query_records

    CSV.open(export.file_path, 'wb') do |csv|
      csv << export.headers
      records.find_each(batch_size: 1000) do |record|
        csv << export.row_for(record)
      end
    end

    export.update!(status: :completed, completed_at: Time.current)
    ExportMailer.ready(export).deliver_later
  rescue StandardError => e
    export.update!(status: :failed, error_message: e.message)
    raise
  end
end
```

---

# PHP Backend (4 Methodologies)

## M-PHP-001: Laravel Patterns

### Problem
Structure Laravel applications with clean architecture.

### Framework: Controller Structure

```php
<?php
// app/Http/Controllers/Api/V1/UserController.php

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreUserRequest;
use App\Http\Requests\UpdateUserRequest;
use App\Http\Resources\UserResource;
use App\Http\Resources\UserCollection;
use App\Services\UserService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Response;

class UserController extends Controller
{
    public function __construct(
        private readonly UserService $userService
    ) {}

    public function index(): UserCollection
    {
        $users = $this->userService->paginate(
            perPage: request()->integer('per_page', 20)
        );

        return new UserCollection($users);
    }

    public function store(StoreUserRequest $request): JsonResponse
    {
        $user = $this->userService->create($request->validated());

        return (new UserResource($user))
            ->response()
            ->setStatusCode(Response::HTTP_CREATED);
    }

    public function show(int $id): UserResource
    {
        $user = $this->userService->findOrFail($id);

        return new UserResource($user);
    }

    public function update(UpdateUserRequest $request, int $id): UserResource
    {
        $user = $this->userService->update($id, $request->validated());

        return new UserResource($user);
    }

    public function destroy(int $id): JsonResponse
    {
        $this->userService->delete($id);

        return response()->json(null, Response::HTTP_NO_CONTENT);
    }
}
```

### Service Layer

```php
<?php
// app/Services/UserService.php

namespace App\Services;

use App\Models\User;
use App\Repositories\UserRepository;
use Illuminate\Pagination\LengthAwarePaginator;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

class UserService
{
    public function __construct(
        private readonly UserRepository $repository
    ) {}

    public function paginate(int $perPage = 20): LengthAwarePaginator
    {
        return $this->repository->paginate($perPage);
    }

    public function findOrFail(int $id): User
    {
        return $this->repository->findOrFail($id);
    }

    public function create(array $data): User
    {
        return DB::transaction(function () use ($data) {
            $data['password'] = Hash::make($data['password']);

            $user = $this->repository->create($data);

            event(new \App\Events\UserCreated($user));

            return $user;
        });
    }

    public function update(int $id, array $data): User
    {
        return DB::transaction(function () use ($id, $data) {
            if (isset($data['password'])) {
                $data['password'] = Hash::make($data['password']);
            }

            return $this->repository->update($id, $data);
        });
    }

    public function delete(int $id): bool
    {
        return $this->repository->delete($id);
    }
}
```

---

## M-PHP-002: Eloquent Patterns

### Problem
Efficient database queries with Eloquent ORM.

### Framework: Model Definition

```php
<?php
// app/Models/User.php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\SoftDeletes;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Builder;

class User extends Authenticatable
{
    use HasFactory, SoftDeletes;

    protected $fillable = [
        'name',
        'email',
        'password',
    ];

    protected $hidden = [
        'password',
        'remember_token',
    ];

    protected $casts = [
        'email_verified_at' => 'datetime',
        'settings' => 'array',
    ];

    // Relationships
    public function orders(): HasMany
    {
        return $this->hasMany(Order::class);
    }

    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class)
            ->withTimestamps()
            ->withPivot('assigned_by');
    }

    // Scopes
    public function scopeActive(Builder $query): Builder
    {
        return $query->where('is_active', true);
    }

    public function scopeWithRole(Builder $query, string $role): Builder
    {
        return $query->whereHas('roles', fn ($q) => $q->where('name', $role));
    }

    public function scopeSearch(Builder $query, ?string $term): Builder
    {
        if (empty($term)) {
            return $query;
        }

        return $query->where(function ($q) use ($term) {
            $q->where('name', 'LIKE', "%{$term}%")
              ->orWhere('email', 'LIKE', "%{$term}%");
        });
    }

    // Accessors & Mutators
    protected function email(): Attribute
    {
        return Attribute::make(
            set: fn (string $value) => strtolower($value),
        );
    }

    // Methods
    public function hasRole(string $role): bool
    {
        return $this->roles()->where('name', $role)->exists();
    }
}
```

### Repository Pattern

```php
<?php
// app/Repositories/UserRepository.php

namespace App\Repositories;

use App\Models\User;
use Illuminate\Pagination\LengthAwarePaginator;
use Illuminate\Database\Eloquent\Collection;

class UserRepository
{
    public function __construct(
        private readonly User $model
    ) {}

    public function paginate(int $perPage = 20): LengthAwarePaginator
    {
        return $this->model
            ->with(['roles'])
            ->latest()
            ->paginate($perPage);
    }

    public function findOrFail(int $id): User
    {
        return $this->model
            ->with(['roles', 'orders'])
            ->findOrFail($id);
    }

    public function create(array $data): User
    {
        return $this->model->create($data);
    }

    public function update(int $id, array $data): User
    {
        $user = $this->model->findOrFail($id);
        $user->update($data);
        return $user->fresh();
    }

    public function delete(int $id): bool
    {
        return $this->model->findOrFail($id)->delete();
    }

    public function findByEmail(string $email): ?User
    {
        return $this->model->where('email', $email)->first();
    }
}
```

---

## M-PHP-003: PHPUnit Testing

### Problem
Test Laravel applications effectively.

### Framework: Feature Tests

```php
<?php
// tests/Feature/UserControllerTest.php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class UserControllerTest extends TestCase
{
    use RefreshDatabase;

    public function test_can_list_users(): void
    {
        $users = User::factory()->count(5)->create();

        $response = $this->getJson('/api/v1/users');

        $response->assertOk()
            ->assertJsonCount(5, 'data')
            ->assertJsonStructure([
                'data' => [
                    '*' => ['id', 'name', 'email', 'created_at']
                ],
                'meta' => ['current_page', 'total']
            ]);
    }

    public function test_can_create_user(): void
    {
        $userData = [
            'name' => 'John Doe',
            'email' => 'john@example.com',
            'password' => 'password123',
        ];

        $response = $this->postJson('/api/v1/users', $userData);

        $response->assertCreated()
            ->assertJsonPath('data.name', 'John Doe')
            ->assertJsonPath('data.email', 'john@example.com');

        $this->assertDatabaseHas('users', [
            'email' => 'john@example.com'
        ]);
    }

    public function test_create_user_validates_email(): void
    {
        $userData = [
            'name' => 'John Doe',
            'email' => 'invalid-email',
            'password' => 'password123',
        ];

        $response = $this->postJson('/api/v1/users', $userData);

        $response->assertUnprocessable()
            ->assertJsonValidationErrors(['email']);
    }

    public function test_can_update_user(): void
    {
        $user = User::factory()->create();

        $response = $this->putJson("/api/v1/users/{$user->id}", [
            'name' => 'Updated Name',
        ]);

        $response->assertOk()
            ->assertJsonPath('data.name', 'Updated Name');
    }

    public function test_can_delete_user(): void
    {
        $user = User::factory()->create();

        $response = $this->deleteJson("/api/v1/users/{$user->id}");

        $response->assertNoContent();
        $this->assertSoftDeleted('users', ['id' => $user->id]);
    }
}
```

### Unit Tests

```php
<?php
// tests/Unit/Services/UserServiceTest.php

namespace Tests\Unit\Services;

use App\Models\User;
use App\Repositories\UserRepository;
use App\Services\UserService;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Mockery;
use Tests\TestCase;

class UserServiceTest extends TestCase
{
    use RefreshDatabase;

    private UserService $service;
    private UserRepository $repository;

    protected function setUp(): void
    {
        parent::setUp();
        $this->repository = new UserRepository(new User());
        $this->service = new UserService($this->repository);
    }

    public function test_create_hashes_password(): void
    {
        $user = $this->service->create([
            'name' => 'John',
            'email' => 'john@example.com',
            'password' => 'plaintext',
        ]);

        $this->assertNotEquals('plaintext', $user->password);
        $this->assertTrue(\Hash::check('plaintext', $user->password));
    }

    public function test_create_fires_event(): void
    {
        \Event::fake();

        $this->service->create([
            'name' => 'John',
            'email' => 'john@example.com',
            'password' => 'password',
        ]);

        \Event::assertDispatched(\App\Events\UserCreated::class);
    }
}
```

---

## M-PHP-004: Laravel Queues

### Problem
Process background tasks asynchronously.

### Framework: Job Structure

```php
<?php
// app/Jobs/ProcessOrderJob.php

namespace App\Jobs;

use App\Models\Order;
use App\Services\OrderProcessor;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Queue\Middleware\WithoutOverlapping;
use Throwable;

class ProcessOrderJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;
    public int $backoff = 60;
    public int $timeout = 120;

    public function __construct(
        public readonly Order $order
    ) {}

    public function middleware(): array
    {
        return [
            new WithoutOverlapping($this->order->id),
        ];
    }

    public function handle(OrderProcessor $processor): void
    {
        if ($this->order->isProcessed()) {
            return;
        }

        $processor->process($this->order);

        NotifyCustomerJob::dispatch($this->order)
            ->onQueue('notifications');
    }

    public function failed(Throwable $exception): void
    {
        $this->order->update(['status' => 'failed']);

        \Log::error('Order processing failed', [
            'order_id' => $this->order->id,
            'error' => $exception->getMessage(),
        ]);
    }

    public function retryUntil(): \DateTime
    {
        return now()->addHours(24);
    }
}

// Dispatch
ProcessOrderJob::dispatch($order)->onQueue('orders');
ProcessOrderJob::dispatch($order)->delay(now()->addMinutes(10));
```

### Job Batching

```php
<?php
// app/Jobs/ExportUsersJob.php

namespace App\Jobs;

use App\Models\User;
use Illuminate\Bus\Batchable;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Bus;

class ExportUsersJob implements ShouldQueue
{
    use Batchable, Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public function __construct(
        public readonly array $userIds,
        public readonly string $filePath
    ) {}

    public function handle(): void
    {
        if ($this->batch()->cancelled()) {
            return;
        }

        $users = User::whereIn('id', $this->userIds)->get();

        // Process chunk...
    }
}

// Create batch
$batch = Bus::batch([
    new ExportUsersJob($chunk1, $path),
    new ExportUsersJob($chunk2, $path),
    new ExportUsersJob($chunk3, $path),
])
->then(function ($batch) {
    // All jobs completed successfully
})
->catch(function ($batch, $e) {
    // First batch job failure
})
->finally(function ($batch) {
    // Batch finished (success or failure)
})
->name('Export Users')
->dispatch();
```

---

# Java Backend (4 Methodologies)

## M-JAVA-001: Spring Boot Patterns

### Problem
Structure Spring Boot applications with clean architecture.

### Framework: Controller Layer

```java
// src/main/java/com/example/controller/UserController.java

package com.example.controller;

import com.example.dto.CreateUserRequest;
import com.example.dto.UpdateUserRequest;
import com.example.dto.UserResponse;
import com.example.service.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping
    public ResponseEntity<Page<UserResponse>> listUsers(Pageable pageable) {
        return ResponseEntity.ok(userService.findAll(pageable));
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
        return ResponseEntity.ok(userService.findById(id));
    }

    @PostMapping
    public ResponseEntity<UserResponse> createUser(
            @Valid @RequestBody CreateUserRequest request) {
        UserResponse user = userService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(user);
    }

    @PutMapping("/{id}")
    public ResponseEntity<UserResponse> updateUser(
            @PathVariable Long id,
            @Valid @RequestBody UpdateUserRequest request) {
        return ResponseEntity.ok(userService.update(id, request));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        userService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
```

### Service Layer

```java
// src/main/java/com/example/service/UserService.java

package com.example.service;

import com.example.dto.CreateUserRequest;
import com.example.dto.UpdateUserRequest;
import com.example.dto.UserResponse;
import com.example.entity.User;
import com.example.exception.ResourceNotFoundException;
import com.example.mapper.UserMapper;
import com.example.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final UserMapper userMapper;
    private final PasswordEncoder passwordEncoder;

    public Page<UserResponse> findAll(Pageable pageable) {
        return userRepository.findAll(pageable)
                .map(userMapper::toResponse);
    }

    public UserResponse findById(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("User", id));
        return userMapper.toResponse(user);
    }

    @Transactional
    public UserResponse create(CreateUserRequest request) {
        User user = userMapper.toEntity(request);
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        user = userRepository.save(user);
        return userMapper.toResponse(user);
    }

    @Transactional
    public UserResponse update(Long id, UpdateUserRequest request) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("User", id));
        userMapper.updateEntity(user, request);
        user = userRepository.save(user);
        return userMapper.toResponse(user);
    }

    @Transactional
    public void delete(Long id) {
        if (!userRepository.existsById(id)) {
            throw new ResourceNotFoundException("User", id);
        }
        userRepository.deleteById(id);
    }
}
```

---

## M-JAVA-002: JPA/Hibernate Patterns

### Problem
Efficient database access with JPA.

### Framework: Entity Definition

```java
// src/main/java/com/example/entity/User.java

package com.example.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;
import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "users")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String password;

    @Column(name = "is_active")
    @Builder.Default
    private Boolean isActive = true;

    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(
        name = "user_roles",
        joinColumns = @JoinColumn(name = "user_id"),
        inverseJoinColumns = @JoinColumn(name = "role_id")
    )
    @Builder.Default
    private Set<Role> roles = new HashSet<>();

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private Set<Order> orders = new HashSet<>();

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    // Helper methods
    public void addRole(Role role) {
        roles.add(role);
    }

    public void removeRole(Role role) {
        roles.remove(role);
    }
}
```

### Repository with Custom Queries

```java
// src/main/java/com/example/repository/UserRepository.java

package com.example.repository;

import com.example.entity.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByEmail(String email);

    boolean existsByEmail(String email);

    @Query("SELECT u FROM User u WHERE u.isActive = true")
    Page<User> findAllActive(Pageable pageable);

    @Query("SELECT u FROM User u JOIN FETCH u.roles WHERE u.id = :id")
    Optional<User> findByIdWithRoles(@Param("id") Long id);

    @Query("""
        SELECT u FROM User u
        WHERE (:name IS NULL OR LOWER(u.name) LIKE LOWER(CONCAT('%', :name, '%')))
        AND (:email IS NULL OR LOWER(u.email) LIKE LOWER(CONCAT('%', :email, '%')))
        AND (:isActive IS NULL OR u.isActive = :isActive)
        """)
    Page<User> search(
            @Param("name") String name,
            @Param("email") String email,
            @Param("isActive") Boolean isActive,
            Pageable pageable
    );

    @Modifying
    @Query("UPDATE User u SET u.isActive = false WHERE u.lastLoginAt < :cutoffDate")
    int deactivateInactiveUsers(@Param("cutoffDate") LocalDateTime cutoffDate);
}
```

---

## M-JAVA-003: JUnit Testing

### Problem
Write comprehensive tests for Spring Boot applications.

### Framework: Controller Tests

```java
// src/test/java/com/example/controller/UserControllerTest.java

package com.example.controller;

import com.example.dto.CreateUserRequest;
import com.example.dto.UserResponse;
import com.example.service.UserService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private UserService userService;

    @Test
    void createUser_WithValidData_ReturnsCreated() throws Exception {
        CreateUserRequest request = new CreateUserRequest(
                "John Doe", "john@example.com", "password123"
        );
        UserResponse response = new UserResponse(1L, "John Doe", "john@example.com");

        when(userService.create(any(CreateUserRequest.class))).thenReturn(response);

        mockMvc.perform(post("/api/v1/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.name").value("John Doe"))
                .andExpect(jsonPath("$.email").value("john@example.com"));
    }

    @Test
    void createUser_WithInvalidEmail_ReturnsBadRequest() throws Exception {
        CreateUserRequest request = new CreateUserRequest(
                "John Doe", "invalid-email", "password123"
        );

        mockMvc.perform(post("/api/v1/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.errors.email").exists());
    }

    @Test
    void getUser_WhenExists_ReturnsUser() throws Exception {
        UserResponse response = new UserResponse(1L, "John Doe", "john@example.com");
        when(userService.findById(1L)).thenReturn(response);

        mockMvc.perform(get("/api/v1/users/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.name").value("John Doe"));
    }
}
```

### Service Tests

```java
// src/test/java/com/example/service/UserServiceTest.java

package com.example.service;

import com.example.dto.CreateUserRequest;
import com.example.dto.UserResponse;
import com.example.entity.User;
import com.example.exception.ResourceNotFoundException;
import com.example.mapper.UserMapper;
import com.example.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private UserMapper userMapper;

    @Mock
    private PasswordEncoder passwordEncoder;

    @InjectMocks
    private UserService userService;

    private User user;
    private UserResponse userResponse;

    @BeforeEach
    void setUp() {
        user = User.builder()
                .id(1L)
                .name("John Doe")
                .email("john@example.com")
                .password("encoded")
                .build();
        userResponse = new UserResponse(1L, "John Doe", "john@example.com");
    }

    @Test
    void findById_WhenUserExists_ReturnsUser() {
        when(userRepository.findById(1L)).thenReturn(Optional.of(user));
        when(userMapper.toResponse(user)).thenReturn(userResponse);

        UserResponse result = userService.findById(1L);

        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getName()).isEqualTo("John Doe");
    }

    @Test
    void findById_WhenUserNotExists_ThrowsException() {
        when(userRepository.findById(999L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> userService.findById(999L))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessageContaining("User");
    }

    @Test
    void create_EncodesPassword() {
        CreateUserRequest request = new CreateUserRequest(
                "John", "john@example.com", "plaintext"
        );
        when(passwordEncoder.encode("plaintext")).thenReturn("encoded");
        when(userMapper.toEntity(request)).thenReturn(user);
        when(userRepository.save(any(User.class))).thenReturn(user);
        when(userMapper.toResponse(user)).thenReturn(userResponse);

        userService.create(request);

        verify(passwordEncoder).encode("plaintext");
    }
}
```

---

## M-JAVA-004: Spring Async

### Problem
Process background tasks asynchronously.

### Framework: Async Configuration

```java
// src/main/java/com/example/config/AsyncConfig.java

package com.example.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.Executor;

@Configuration
@EnableAsync
public class AsyncConfig {

    @Bean(name = "taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(4);
        executor.setMaxPoolSize(8);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("Async-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }

    @Bean(name = "emailExecutor")
    public Executor emailExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(2);
        executor.setMaxPoolSize(4);
        executor.setQueueCapacity(50);
        executor.setThreadNamePrefix("Email-");
        executor.initialize();
        return executor;
    }
}
```

### Async Service

```java
// src/main/java/com/example/service/NotificationService.java

package com.example.service;

import com.example.entity.Order;
import com.example.entity.User;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.util.concurrent.CompletableFuture;

@Service
@RequiredArgsConstructor
@Slf4j
public class NotificationService {

    private final EmailService emailService;
    private final SmsService smsService;

    @Async("emailExecutor")
    public CompletableFuture<Void> sendOrderConfirmation(Order order) {
        log.info("Sending order confirmation for order: {}", order.getId());
        try {
            emailService.send(
                    order.getUser().getEmail(),
                    "Order Confirmation",
                    buildOrderEmailBody(order)
            );
            return CompletableFuture.completedFuture(null);
        } catch (Exception e) {
            log.error("Failed to send order confirmation", e);
            return CompletableFuture.failedFuture(e);
        }
    }

    @Async("taskExecutor")
    public CompletableFuture<Void> sendWelcomeNotifications(User user) {
        CompletableFuture<Void> emailFuture = CompletableFuture.runAsync(() ->
                emailService.send(user.getEmail(), "Welcome!", buildWelcomeEmail(user))
        );

        CompletableFuture<Void> smsFuture = CompletableFuture.runAsync(() ->
                smsService.send(user.getPhone(), "Welcome to our service!")
        );

        return CompletableFuture.allOf(emailFuture, smsFuture)
                .exceptionally(ex -> {
                    log.error("Failed to send welcome notifications", ex);
                    return null;
                });
    }

    private String buildOrderEmailBody(Order order) {
        return "Your order #" + order.getId() + " has been confirmed.";
    }

    private String buildWelcomeEmail(User user) {
        return "Welcome, " + user.getName() + "!";
    }
}
```

---

# C# Backend (4 Methodologies)

## M-CSHARP-001: ASP.NET Core Patterns

### Problem
Structure ASP.NET Core applications with clean architecture.

### Framework: Controller Structure

```csharp
// Controllers/UsersController.cs

using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;

namespace MyApp.Controllers;

[ApiController]
[Route("api/v1/[controller]")]
[Authorize]
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;
    private readonly ILogger<UsersController> _logger;

    public UsersController(IUserService userService, ILogger<UsersController> logger)
    {
        _userService = userService;
        _logger = logger;
    }

    [HttpGet]
    public async Task<ActionResult<PagedResult<UserDto>>> GetUsers(
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20)
    {
        var result = await _userService.GetAllAsync(page, pageSize);
        return Ok(result);
    }

    [HttpGet("{id:int}")]
    public async Task<ActionResult<UserDto>> GetUser(int id)
    {
        var user = await _userService.GetByIdAsync(id);
        if (user == null)
            return NotFound();
        return Ok(user);
    }

    [HttpPost]
    public async Task<ActionResult<UserDto>> CreateUser(CreateUserDto dto)
    {
        var user = await _userService.CreateAsync(dto);
        return CreatedAtAction(nameof(GetUser), new { id = user.Id }, user);
    }

    [HttpPut("{id:int}")]
    public async Task<ActionResult<UserDto>> UpdateUser(int id, UpdateUserDto dto)
    {
        var user = await _userService.UpdateAsync(id, dto);
        if (user == null)
            return NotFound();
        return Ok(user);
    }

    [HttpDelete("{id:int}")]
    public async Task<IActionResult> DeleteUser(int id)
    {
        var success = await _userService.DeleteAsync(id);
        if (!success)
            return NotFound();
        return NoContent();
    }
}
```

### Service Layer

```csharp
// Services/UserService.cs

namespace MyApp.Services;

public interface IUserService
{
    Task<PagedResult<UserDto>> GetAllAsync(int page, int pageSize);
    Task<UserDto?> GetByIdAsync(int id);
    Task<UserDto> CreateAsync(CreateUserDto dto);
    Task<UserDto?> UpdateAsync(int id, UpdateUserDto dto);
    Task<bool> DeleteAsync(int id);
}

public class UserService : IUserService
{
    private readonly IUserRepository _repository;
    private readonly IMapper _mapper;
    private readonly IPasswordHasher<User> _passwordHasher;

    public UserService(
        IUserRepository repository,
        IMapper mapper,
        IPasswordHasher<User> passwordHasher)
    {
        _repository = repository;
        _mapper = mapper;
        _passwordHasher = passwordHasher;
    }

    public async Task<PagedResult<UserDto>> GetAllAsync(int page, int pageSize)
    {
        var users = await _repository.GetPagedAsync(page, pageSize);
        return _mapper.Map<PagedResult<UserDto>>(users);
    }

    public async Task<UserDto?> GetByIdAsync(int id)
    {
        var user = await _repository.GetByIdAsync(id);
        return user == null ? null : _mapper.Map<UserDto>(user);
    }

    public async Task<UserDto> CreateAsync(CreateUserDto dto)
    {
        var user = _mapper.Map<User>(dto);
        user.PasswordHash = _passwordHasher.HashPassword(user, dto.Password);

        await _repository.AddAsync(user);
        await _repository.SaveChangesAsync();

        return _mapper.Map<UserDto>(user);
    }

    public async Task<UserDto?> UpdateAsync(int id, UpdateUserDto dto)
    {
        var user = await _repository.GetByIdAsync(id);
        if (user == null)
            return null;

        _mapper.Map(dto, user);
        await _repository.SaveChangesAsync();

        return _mapper.Map<UserDto>(user);
    }

    public async Task<bool> DeleteAsync(int id)
    {
        var user = await _repository.GetByIdAsync(id);
        if (user == null)
            return false;

        _repository.Remove(user);
        await _repository.SaveChangesAsync();
        return true;
    }
}
```

---

## M-CSHARP-002: Entity Framework Patterns

### Problem
Efficient database access with EF Core.

### Framework: Entity Configuration

```csharp
// Entities/User.cs

namespace MyApp.Entities;

public class User
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string PasswordHash { get; set; } = string.Empty;
    public bool IsActive { get; set; } = true;
    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }

    // Navigation properties
    public ICollection<Role> Roles { get; set; } = new List<Role>();
    public ICollection<Order> Orders { get; set; } = new List<Order>();
}

// Data/Configurations/UserConfiguration.cs

using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace MyApp.Data.Configurations;

public class UserConfiguration : IEntityTypeConfiguration<User>
{
    public void Configure(EntityTypeBuilder<User> builder)
    {
        builder.ToTable("users");

        builder.HasKey(u => u.Id);

        builder.Property(u => u.Name)
            .IsRequired()
            .HasMaxLength(100);

        builder.Property(u => u.Email)
            .IsRequired()
            .HasMaxLength(255);

        builder.HasIndex(u => u.Email)
            .IsUnique();

        builder.Property(u => u.CreatedAt)
            .HasDefaultValueSql("CURRENT_TIMESTAMP");

        builder.HasMany(u => u.Roles)
            .WithMany(r => r.Users)
            .UsingEntity<Dictionary<string, object>>(
                "user_roles",
                j => j.HasOne<Role>().WithMany().HasForeignKey("RoleId"),
                j => j.HasOne<User>().WithMany().HasForeignKey("UserId")
            );

        builder.HasMany(u => u.Orders)
            .WithOne(o => o.User)
            .HasForeignKey(o => o.UserId)
            .OnDelete(DeleteBehavior.SetNull);
    }
}
```

### Repository Pattern

```csharp
// Repositories/UserRepository.cs

namespace MyApp.Repositories;

public interface IUserRepository
{
    Task<User?> GetByIdAsync(int id);
    Task<User?> GetByEmailAsync(string email);
    Task<PagedResult<User>> GetPagedAsync(int page, int pageSize);
    Task AddAsync(User user);
    void Remove(User user);
    Task SaveChangesAsync();
}

public class UserRepository : IUserRepository
{
    private readonly AppDbContext _context;

    public UserRepository(AppDbContext context)
    {
        _context = context;
    }

    public async Task<User?> GetByIdAsync(int id)
    {
        return await _context.Users
            .Include(u => u.Roles)
            .FirstOrDefaultAsync(u => u.Id == id);
    }

    public async Task<User?> GetByEmailAsync(string email)
    {
        return await _context.Users
            .FirstOrDefaultAsync(u => u.Email == email.ToLower());
    }

    public async Task<PagedResult<User>> GetPagedAsync(int page, int pageSize)
    {
        var query = _context.Users
            .AsNoTracking()
            .OrderByDescending(u => u.CreatedAt);

        var totalCount = await query.CountAsync();
        var items = await query
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync();

        return new PagedResult<User>(items, totalCount, page, pageSize);
    }

    public async Task AddAsync(User user)
    {
        await _context.Users.AddAsync(user);
    }

    public void Remove(User user)
    {
        _context.Users.Remove(user);
    }

    public async Task SaveChangesAsync()
    {
        await _context.SaveChangesAsync();
    }
}
```

---

## M-CSHARP-003: xUnit Testing

### Problem
Write comprehensive tests for .NET applications.

### Framework: Controller Tests

```csharp
// Tests/Controllers/UsersControllerTests.cs

using Microsoft.AspNetCore.Mvc;
using Moq;
using Xunit;

namespace MyApp.Tests.Controllers;

public class UsersControllerTests
{
    private readonly Mock<IUserService> _mockService;
    private readonly UsersController _controller;

    public UsersControllerTests()
    {
        _mockService = new Mock<IUserService>();
        _controller = new UsersController(
            _mockService.Object,
            Mock.Of<ILogger<UsersController>>()
        );
    }

    [Fact]
    public async Task GetUser_WhenUserExists_ReturnsOkWithUser()
    {
        // Arrange
        var userDto = new UserDto { Id = 1, Name = "John", Email = "john@example.com" };
        _mockService.Setup(s => s.GetByIdAsync(1))
            .ReturnsAsync(userDto);

        // Act
        var result = await _controller.GetUser(1);

        // Assert
        var okResult = Assert.IsType<OkObjectResult>(result.Result);
        var returnedUser = Assert.IsType<UserDto>(okResult.Value);
        Assert.Equal(1, returnedUser.Id);
        Assert.Equal("John", returnedUser.Name);
    }

    [Fact]
    public async Task GetUser_WhenUserNotFound_ReturnsNotFound()
    {
        // Arrange
        _mockService.Setup(s => s.GetByIdAsync(999))
            .ReturnsAsync((UserDto?)null);

        // Act
        var result = await _controller.GetUser(999);

        // Assert
        Assert.IsType<NotFoundResult>(result.Result);
    }

    [Fact]
    public async Task CreateUser_WithValidData_ReturnsCreatedAtAction()
    {
        // Arrange
        var createDto = new CreateUserDto
        {
            Name = "John",
            Email = "john@example.com",
            Password = "password123"
        };
        var userDto = new UserDto { Id = 1, Name = "John", Email = "john@example.com" };

        _mockService.Setup(s => s.CreateAsync(createDto))
            .ReturnsAsync(userDto);

        // Act
        var result = await _controller.CreateUser(createDto);

        // Assert
        var createdResult = Assert.IsType<CreatedAtActionResult>(result.Result);
        Assert.Equal(nameof(UsersController.GetUser), createdResult.ActionName);
        Assert.Equal(1, createdResult.RouteValues?["id"]);
    }
}
```

### Integration Tests

```csharp
// Tests/Integration/UsersApiTests.cs

using Microsoft.AspNetCore.Mvc.Testing;
using System.Net.Http.Json;
using Xunit;

namespace MyApp.Tests.Integration;

public class UsersApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public UsersApiTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task GetUsers_ReturnsSuccessAndCorrectContentType()
    {
        // Act
        var response = await _client.GetAsync("/api/v1/users");

        // Assert
        response.EnsureSuccessStatusCode();
        Assert.Equal("application/json; charset=utf-8",
            response.Content.Headers.ContentType?.ToString());
    }

    [Fact]
    public async Task CreateUser_WithValidData_ReturnsCreated()
    {
        // Arrange
        var createDto = new CreateUserDto
        {
            Name = "Test User",
            Email = "test@example.com",
            Password = "password123"
        };

        // Act
        var response = await _client.PostAsJsonAsync("/api/v1/users", createDto);

        // Assert
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);

        var user = await response.Content.ReadFromJsonAsync<UserDto>();
        Assert.NotNull(user);
        Assert.Equal("Test User", user.Name);
    }
}
```

---

## M-CSHARP-004: Background Services

### Problem
Process background tasks in ASP.NET Core.

### Framework: Hosted Service

```csharp
// Services/BackgroundOrderProcessor.cs

namespace MyApp.Services;

public class BackgroundOrderProcessor : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<BackgroundOrderProcessor> _logger;
    private readonly Channel<int> _orderChannel;

    public BackgroundOrderProcessor(
        IServiceProvider serviceProvider,
        ILogger<BackgroundOrderProcessor> logger,
        Channel<int> orderChannel)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
        _orderChannel = orderChannel;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Order processor started");

        await foreach (var orderId in _orderChannel.Reader.ReadAllAsync(stoppingToken))
        {
            try
            {
                await ProcessOrderAsync(orderId, stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing order {OrderId}", orderId);
            }
        }
    }

    private async Task ProcessOrderAsync(int orderId, CancellationToken ct)
    {
        using var scope = _serviceProvider.CreateScope();
        var orderService = scope.ServiceProvider.GetRequiredService<IOrderService>();

        _logger.LogInformation("Processing order {OrderId}", orderId);
        await orderService.ProcessAsync(orderId, ct);
        _logger.LogInformation("Order {OrderId} processed", orderId);
    }
}

// Queue service
public interface IOrderQueue
{
    ValueTask QueueOrderAsync(int orderId);
}

public class OrderQueue : IOrderQueue
{
    private readonly Channel<int> _channel;

    public OrderQueue(Channel<int> channel)
    {
        _channel = channel;
    }

    public async ValueTask QueueOrderAsync(int orderId)
    {
        await _channel.Writer.WriteAsync(orderId);
    }
}
```

### Timed Background Service

```csharp
// Services/CleanupService.cs

namespace MyApp.Services;

public class CleanupService : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<CleanupService> _logger;
    private readonly TimeSpan _period = TimeSpan.FromHours(1);

    public CleanupService(
        IServiceProvider serviceProvider,
        ILogger<CleanupService> logger)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        using var timer = new PeriodicTimer(_period);

        while (!stoppingToken.IsCancellationRequested &&
               await timer.WaitForNextTickAsync(stoppingToken))
        {
            try
            {
                await DoCleanupAsync(stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during cleanup");
            }
        }
    }

    private async Task DoCleanupAsync(CancellationToken ct)
    {
        using var scope = _serviceProvider.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();

        var cutoff = DateTime.UtcNow.AddDays(-30);

        var deleted = await context.AuditLogs
            .Where(a => a.CreatedAt < cutoff)
            .ExecuteDeleteAsync(ct);

        _logger.LogInformation("Deleted {Count} old audit logs", deleted);
    }
}
```

---

# Rust Backend (4 Methodologies)

## M-RUST-001: Project Structure (Actix/Axum)

### Problem
Organize Rust web applications for maintainability.

### Framework: Directory Layout

```
project/
├── Cargo.toml
├── src/
│   ├── main.rs              # Entry point
│   ├── lib.rs               # Library root
│   ├── config.rs            # Configuration
│   ├── error.rs             # Error types
│   ├── routes/
│   │   ├── mod.rs
│   │   └── users.rs         # User routes
│   ├── handlers/
│   │   ├── mod.rs
│   │   └── users.rs         # User handlers
│   ├── services/
│   │   ├── mod.rs
│   │   └── users.rs         # Business logic
│   ├── models/
│   │   ├── mod.rs
│   │   └── user.rs          # Domain models
│   ├── db/
│   │   ├── mod.rs
│   │   └── users.rs         # Database queries
│   └── middleware/
│       ├── mod.rs
│       └── auth.rs          # Auth middleware
├── migrations/
└── tests/
```

### Axum Router Setup

```rust
// src/main.rs

use axum::{
    routing::{get, post, put, delete},
    Router,
};
use std::sync::Arc;
use tower_http::trace::TraceLayer;

mod config;
mod db;
mod error;
mod handlers;
mod middleware;
mod models;
mod routes;
mod services;

use crate::config::Config;
use crate::db::Database;

#[derive(Clone)]
pub struct AppState {
    pub db: Database,
    pub config: Arc<Config>,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::init();

    let config = Config::from_env()?;
    let db = Database::connect(&config.database_url).await?;

    let state = AppState {
        db,
        config: Arc::new(config),
    };

    let app = Router::new()
        .nest("/api/v1", routes::api_routes())
        .layer(TraceLayer::new_for_http())
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
    tracing::info!("Server running on http://0.0.0.0:3000");
    axum::serve(listener, app).await?;

    Ok(())
}

// src/routes/mod.rs

use axum::{routing::get, Router};
use crate::AppState;

mod users;

pub fn api_routes() -> Router<AppState> {
    Router::new()
        .nest("/users", users::routes())
        .route("/health", get(|| async { "OK" }))
}

// src/routes/users.rs

use axum::{
    routing::{get, post, put, delete},
    Router,
};
use crate::{handlers::users, AppState};

pub fn routes() -> Router<AppState> {
    Router::new()
        .route("/", get(users::list).post(users::create))
        .route("/:id", get(users::get).put(users::update).delete(users::delete))
}
```

---

## M-RUST-002: HTTP Handlers

### Problem
Build type-safe HTTP handlers with proper error handling.

### Framework: Handler Implementation

```rust
// src/handlers/users.rs

use axum::{
    extract::{Path, Query, State},
    http::StatusCode,
    Json,
};
use serde::{Deserialize, Serialize};
use validator::Validate;

use crate::{
    error::AppError,
    models::User,
    services::UserService,
    AppState,
};

#[derive(Debug, Deserialize)]
pub struct ListParams {
    #[serde(default = "default_page")]
    page: u32,
    #[serde(default = "default_per_page")]
    per_page: u32,
}

fn default_page() -> u32 { 1 }
fn default_per_page() -> u32 { 20 }

#[derive(Debug, Serialize)]
pub struct ListResponse {
    data: Vec<UserResponse>,
    total: i64,
    page: u32,
    per_page: u32,
}

#[derive(Debug, Serialize)]
pub struct UserResponse {
    id: i32,
    name: String,
    email: String,
    created_at: chrono::DateTime<chrono::Utc>,
}

impl From<User> for UserResponse {
    fn from(user: User) -> Self {
        Self {
            id: user.id,
            name: user.name,
            email: user.email,
            created_at: user.created_at,
        }
    }
}

#[derive(Debug, Deserialize, Validate)]
pub struct CreateUserRequest {
    #[validate(length(min = 2, max = 100))]
    name: String,
    #[validate(email)]
    email: String,
    #[validate(length(min = 8))]
    password: String,
}

pub async fn list(
    State(state): State<AppState>,
    Query(params): Query<ListParams>,
) -> Result<Json<ListResponse>, AppError> {
    let service = UserService::new(&state.db);
    let (users, total) = service.list(params.page, params.per_page).await?;

    Ok(Json(ListResponse {
        data: users.into_iter().map(UserResponse::from).collect(),
        total,
        page: params.page,
        per_page: params.per_page,
    }))
}

pub async fn get(
    State(state): State<AppState>,
    Path(id): Path<i32>,
) -> Result<Json<UserResponse>, AppError> {
    let service = UserService::new(&state.db);
    let user = service.get_by_id(id).await?;
    Ok(Json(user.into()))
}

pub async fn create(
    State(state): State<AppState>,
    Json(payload): Json<CreateUserRequest>,
) -> Result<(StatusCode, Json<UserResponse>), AppError> {
    payload.validate()?;

    let service = UserService::new(&state.db);
    let user = service.create(&payload.name, &payload.email, &payload.password).await?;

    Ok((StatusCode::CREATED, Json(user.into())))
}

pub async fn update(
    State(state): State<AppState>,
    Path(id): Path<i32>,
    Json(payload): Json<UpdateUserRequest>,
) -> Result<Json<UserResponse>, AppError> {
    let service = UserService::new(&state.db);
    let user = service.update(id, payload.name.as_deref()).await?;
    Ok(Json(user.into()))
}

pub async fn delete(
    State(state): State<AppState>,
    Path(id): Path<i32>,
) -> Result<StatusCode, AppError> {
    let service = UserService::new(&state.db);
    service.delete(id).await?;
    Ok(StatusCode::NO_CONTENT)
}
```

---

## M-RUST-003: Tokio Async Patterns

### Problem
Handle concurrent operations efficiently.

### Framework: Async Service

```rust
// src/services/users.rs

use crate::{
    db::Database,
    error::AppError,
    models::User,
};
use argon2::{
    password_hash::{rand_core::OsRng, PasswordHasher, SaltString},
    Argon2,
};

pub struct UserService<'a> {
    db: &'a Database,
}

impl<'a> UserService<'a> {
    pub fn new(db: &'a Database) -> Self {
        Self { db }
    }

    pub async fn list(&self, page: u32, per_page: u32) -> Result<(Vec<User>, i64), AppError> {
        let offset = ((page - 1) * per_page) as i64;

        // Run count and fetch in parallel
        let (users, total) = tokio::try_join!(
            self.db.fetch_users(per_page as i64, offset),
            self.db.count_users()
        )?;

        Ok((users, total))
    }

    pub async fn get_by_id(&self, id: i32) -> Result<User, AppError> {
        self.db
            .fetch_user_by_id(id)
            .await?
            .ok_or(AppError::NotFound("User not found".into()))
    }

    pub async fn create(
        &self,
        name: &str,
        email: &str,
        password: &str,
    ) -> Result<User, AppError> {
        // Check if email already exists
        if self.db.fetch_user_by_email(email).await?.is_some() {
            return Err(AppError::Conflict("Email already exists".into()));
        }

        // Hash password (CPU-intensive, use spawn_blocking)
        let password_hash = tokio::task::spawn_blocking({
            let password = password.to_string();
            move || {
                let salt = SaltString::generate(&mut OsRng);
                Argon2::default()
                    .hash_password(password.as_bytes(), &salt)
                    .map(|h| h.to_string())
            }
        })
        .await??;

        self.db.insert_user(name, email, &password_hash).await
    }

    pub async fn update(&self, id: i32, name: Option<&str>) -> Result<User, AppError> {
        let user = self.get_by_id(id).await?;

        let new_name = name.unwrap_or(&user.name);
        self.db.update_user(id, new_name).await
    }

    pub async fn delete(&self, id: i32) -> Result<(), AppError> {
        let deleted = self.db.delete_user(id).await?;
        if !deleted {
            return Err(AppError::NotFound("User not found".into()));
        }
        Ok(())
    }
}
```

### Concurrent Processing

```rust
// src/services/batch.rs

use futures::stream::{self, StreamExt};
use std::sync::Arc;
use tokio::sync::Semaphore;

pub struct BatchProcessor {
    concurrency: usize,
}

impl BatchProcessor {
    pub fn new(concurrency: usize) -> Self {
        Self { concurrency }
    }

    pub async fn process_items<T, F, Fut, R, E>(
        &self,
        items: Vec<T>,
        processor: F,
    ) -> Vec<Result<R, E>>
    where
        T: Send + 'static,
        F: Fn(T) -> Fut + Send + Sync + 'static,
        Fut: std::future::Future<Output = Result<R, E>> + Send,
        R: Send + 'static,
        E: Send + 'static,
    {
        let semaphore = Arc::new(Semaphore::new(self.concurrency));
        let processor = Arc::new(processor);

        stream::iter(items)
            .map(|item| {
                let semaphore = semaphore.clone();
                let processor = processor.clone();

                async move {
                    let _permit = semaphore.acquire().await.unwrap();
                    processor(item).await
                }
            })
            .buffer_unordered(self.concurrency)
            .collect()
            .await
    }
}

// Usage
let processor = BatchProcessor::new(10);
let results = processor.process_items(
    user_ids,
    |id| async move { fetch_user(id).await }
).await;
```

---

## M-RUST-004: Testing Patterns

### Problem
Write comprehensive tests for Rust applications.

### Framework: Unit Tests

```rust
// src/services/users.rs

#[cfg(test)]
mod tests {
    use super::*;
    use mockall::predicate::*;
    use mockall::mock;

    mock! {
        Database {}

        impl Database {
            async fn fetch_user_by_id(&self, id: i32) -> Result<Option<User>, sqlx::Error>;
            async fn fetch_user_by_email(&self, email: &str) -> Result<Option<User>, sqlx::Error>;
            async fn insert_user(&self, name: &str, email: &str, password_hash: &str) -> Result<User, sqlx::Error>;
        }
    }

    fn create_test_user() -> User {
        User {
            id: 1,
            name: "John Doe".into(),
            email: "john@example.com".into(),
            password_hash: "hash".into(),
            created_at: chrono::Utc::now(),
            updated_at: chrono::Utc::now(),
        }
    }

    #[tokio::test]
    async fn test_get_by_id_returns_user() {
        let mut mock_db = MockDatabase::new();
        mock_db
            .expect_fetch_user_by_id()
            .with(eq(1))
            .times(1)
            .returning(|_| Ok(Some(create_test_user())));

        let service = UserService::new(&mock_db);
        let result = service.get_by_id(1).await;

        assert!(result.is_ok());
        assert_eq!(result.unwrap().name, "John Doe");
    }

    #[tokio::test]
    async fn test_get_by_id_not_found() {
        let mut mock_db = MockDatabase::new();
        mock_db
            .expect_fetch_user_by_id()
            .with(eq(999))
            .times(1)
            .returning(|_| Ok(None));

        let service = UserService::new(&mock_db);
        let result = service.get_by_id(999).await;

        assert!(matches!(result, Err(AppError::NotFound(_))));
    }

    #[tokio::test]
    async fn test_create_rejects_duplicate_email() {
        let mut mock_db = MockDatabase::new();
        mock_db
            .expect_fetch_user_by_email()
            .with(eq("john@example.com"))
            .times(1)
            .returning(|_| Ok(Some(create_test_user())));

        let service = UserService::new(&mock_db);
        let result = service.create("John", "john@example.com", "password").await;

        assert!(matches!(result, Err(AppError::Conflict(_))));
    }
}
```

### Integration Tests

```rust
// tests/api_tests.rs

use axum::{
    body::Body,
    http::{Request, StatusCode},
};
use tower::ServiceExt;
use serde_json::json;

async fn setup_app() -> Router {
    // Create test database, run migrations, return app
    todo!()
}

#[tokio::test]
async fn test_create_user() {
    let app = setup_app().await;

    let response = app
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/api/v1/users")
                .header("Content-Type", "application/json")
                .body(Body::from(
                    json!({
                        "name": "John Doe",
                        "email": "john@example.com",
                        "password": "password123"
                    })
                    .to_string(),
                ))
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::CREATED);

    let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
    let user: serde_json::Value = serde_json::from_slice(&body).unwrap();

    assert_eq!(user["name"], "John Doe");
    assert_eq!(user["email"], "john@example.com");
}

#[tokio::test]
async fn test_list_users_pagination() {
    let app = setup_app().await;

    let response = app
        .oneshot(
            Request::builder()
                .method("GET")
                .uri("/api/v1/users?page=1&per_page=10")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);

    let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
    let result: serde_json::Value = serde_json::from_slice(&body).unwrap();

    assert!(result["data"].is_array());
    assert_eq!(result["page"], 1);
    assert_eq!(result["per_page"], 10);
}
```

---

## Quick Reference

### Language Comparison

| Feature | Go | Ruby | PHP | Java | C# | Rust |
|---------|-----|------|-----|------|-----|------|
| **Framework** | Gin/Echo | Rails | Laravel | Spring Boot | ASP.NET | Axum/Actix |
| **ORM** | GORM | ActiveRecord | Eloquent | JPA/Hibernate | EF Core | SQLx/Diesel |
| **Testing** | testing | RSpec | PHPUnit | JUnit | xUnit | built-in |
| **Async** | goroutines | threads | Jobs | CompletableFuture | async/await | tokio |
| **Package Mgr** | go mod | Bundler | Composer | Maven/Gradle | NuGet | Cargo |

### Common Patterns Across Languages

| Pattern | Purpose |
|---------|---------|
| **Service Layer** | Business logic isolation |
| **Repository** | Data access abstraction |
| **DTO/Request/Response** | API contract objects |
| **Middleware** | Cross-cutting concerns |
| **Error Handling** | Consistent error responses |
| **Validation** | Input validation |

---

## Sources

- [Go Gin](https://gin-gonic.com/docs/)
- [Go Echo](https://echo.labstack.com/docs)
- [Ruby on Rails Guides](https://guides.rubyonrails.org/)
- [Laravel Documentation](https://laravel.com/docs)
- [Spring Boot Reference](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [ASP.NET Core Documentation](https://docs.microsoft.com/en-us/aspnet/core/)
- [Rust Axum](https://docs.rs/axum/latest/axum/)
- [Rust Actix](https://actix.rs/docs/)


---

## Methodologies

| ID | Name | File |
|----|------|------|
| M-CS-001 | Project Setup | [methodologies/M-CS-001_project_setup.md](methodologies/M-CS-001_project_setup.md) |
| M-CS-002 | Aspnet Patterns | [methodologies/M-CS-002_aspnet_patterns.md](methodologies/M-CS-002_aspnet_patterns.md) |
| M-CS-003 | Testing Xunit | [methodologies/M-CS-003_testing_xunit.md](methodologies/M-CS-003_testing_xunit.md) |
| M-CS-004 | Code Quality | [methodologies/M-CS-004_code_quality.md](methodologies/M-CS-004_code_quality.md) |
| M-GO-001 | Project Setup | [methodologies/M-GO-001_project_setup.md](methodologies/M-GO-001_project_setup.md) |
| M-GO-002 | Web Frameworks | [methodologies/M-GO-002_web_frameworks.md](methodologies/M-GO-002_web_frameworks.md) |
| M-GO-003 | Testing | [methodologies/M-GO-003_testing.md](methodologies/M-GO-003_testing.md) |
| M-GO-004 | Error Handling | [methodologies/M-GO-004_error_handling.md](methodologies/M-GO-004_error_handling.md) |
| M-JAVA-001 | Project Setup | [methodologies/M-JAVA-001_project_setup.md](methodologies/M-JAVA-001_project_setup.md) |
| M-JAVA-002 | Spring Patterns | [methodologies/M-JAVA-002_spring_patterns.md](methodologies/M-JAVA-002_spring_patterns.md) |
| M-JAVA-003 | Testing | [methodologies/M-JAVA-003_testing.md](methodologies/M-JAVA-003_testing.md) |
| M-JAVA-004 | Code Quality | [methodologies/M-JAVA-004_code_quality.md](methodologies/M-JAVA-004_code_quality.md) |
| M-PHP-001 | Project Setup | [methodologies/M-PHP-001_project_setup.md](methodologies/M-PHP-001_project_setup.md) |
| M-PHP-002 | Laravel Patterns | [methodologies/M-PHP-002_laravel_patterns.md](methodologies/M-PHP-002_laravel_patterns.md) |
| M-PHP-003 | Testing Phpunit | [methodologies/M-PHP-003_testing_phpunit.md](methodologies/M-PHP-003_testing_phpunit.md) |
| M-PHP-004 | Code Quality | [methodologies/M-PHP-004_code_quality.md](methodologies/M-PHP-004_code_quality.md) |
| M-RB-001 | Project Setup | [methodologies/M-RB-001_project_setup.md](methodologies/M-RB-001_project_setup.md) |
| M-RB-002 | Rails Patterns | [methodologies/M-RB-002_rails_patterns.md](methodologies/M-RB-002_rails_patterns.md) |
| M-RB-003 | Testing Rspec | [methodologies/M-RB-003_testing_rspec.md](methodologies/M-RB-003_testing_rspec.md) |
| M-RB-004 | Code Quality | [methodologies/M-RB-004_code_quality.md](methodologies/M-RB-004_code_quality.md) |
| M-RS-001 | Project Setup | [methodologies/M-RS-001_project_setup.md](methodologies/M-RS-001_project_setup.md) |
| M-RS-002 | Axum Patterns | [methodologies/M-RS-002_axum_patterns.md](methodologies/M-RS-002_axum_patterns.md) |
| M-RS-003 | Testing | [methodologies/M-RS-003_testing.md](methodologies/M-RS-003_testing.md) |
| M-RS-004 | Error Handling | [methodologies/M-RS-004_error_handling.md](methodologies/M-RS-004_error_handling.md) |

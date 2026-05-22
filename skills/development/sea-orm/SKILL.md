---
name: SeaORM
description: Async ORM for Rust with compile-time checked queries.
metadata:
  labels: [rust, sea-orm, orm, database, async]
  triggers:
    files: ['**/entity/*.rs', '**/migration/*.rs']
    keywords: [sea_orm, Entity, ActiveModel, DbConn, Select]
---

# SeaORM Standards

## Entity Definition

```rust
use sea_orm::entity::prelude::*;

#[derive(Clone, Debug, PartialEq, DeriveEntityModel)]
#[sea_orm(table_name = "users")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: i32,
    pub name: String,
    #[sea_orm(unique)]
    pub email: String,
    pub created_at: DateTimeUtc,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {
    #[sea_orm(has_many = "super::post::Entity")]
    Posts,
}

impl Related<super::post::Entity> for Entity {
    fn to() -> RelationDef {
        Relation::Posts.def()
    }
}

impl ActiveModelBehavior for ActiveModel {}
```

## Connection

```rust
use sea_orm::{Database, DbConn, ConnectOptions};

async fn connect() -> Result<DbConn, DbErr> {
    let mut opt = ConnectOptions::new("postgres://user:pass@localhost/db");
    opt.max_connections(100)
       .min_connections(5)
       .sqlx_logging(true);

    Database::connect(opt).await
}
```

## CRUD Operations

```rust
use sea_orm::{ActiveModelTrait, EntityTrait, Set};

// Create
async fn create_user(db: &DbConn, name: String, email: String) -> Result<user::Model, DbErr> {
    let user = user::ActiveModel {
        name: Set(name),
        email: Set(email),
        created_at: Set(Utc::now()),
        ..Default::default()
    };
    user.insert(db).await
}

// Read
async fn find_user(db: &DbConn, id: i32) -> Result<Option<user::Model>, DbErr> {
    User::find_by_id(id).one(db).await
}

async fn find_all(db: &DbConn) -> Result<Vec<user::Model>, DbErr> {
    User::find().all(db).await
}

// Update
async fn update_user(db: &DbConn, id: i32, name: String) -> Result<user::Model, DbErr> {
    let user: user::ActiveModel = User::find_by_id(id)
        .one(db)
        .await?
        .ok_or(DbErr::RecordNotFound("User not found".into()))?
        .into();

    user::ActiveModel {
        name: Set(name),
        ..user
    }.update(db).await
}

// Delete
async fn delete_user(db: &DbConn, id: i32) -> Result<DeleteResult, DbErr> {
    User::delete_by_id(id).exec(db).await
}
```

## Queries

```rust
use sea_orm::{Condition, QueryFilter, QueryOrder, QuerySelect};

// Filter
let users = User::find()
    .filter(user::Column::Email.contains("@example.com"))
    .filter(user::Column::CreatedAt.gt(cutoff_date))
    .all(db)
    .await?;

// Complex conditions
let users = User::find()
    .filter(
        Condition::any()
            .add(user::Column::Role.eq("admin"))
            .add(user::Column::Role.eq("moderator"))
    )
    .all(db)
    .await?;

// Order and limit
let users = User::find()
    .order_by_desc(user::Column::CreatedAt)
    .limit(10)
    .offset(20)
    .all(db)
    .await?;

// Select specific columns
let names: Vec<String> = User::find()
    .select_only()
    .column(user::Column::Name)
    .into_tuple()
    .all(db)
    .await?;
```

## Relations

```rust
// Define relation in entity
#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {
    #[sea_orm(
        belongs_to = "super::user::Entity",
        from = "Column::AuthorId",
        to = "super::user::Column::Id"
    )]
    Author,
}

// Eager loading
let posts_with_authors = Post::find()
    .find_also_related(User)
    .all(db)
    .await?;

// Lazy loading
let user = User::find_by_id(1).one(db).await?;
let posts = user.find_related(Post).all(db).await?;
```

## Transactions

```rust
use sea_orm::TransactionTrait;

async fn transfer(db: &DbConn, from: i32, to: i32, amount: i32) -> Result<(), DbErr> {
    db.transaction::<_, (), DbErr>(|txn| {
        Box::pin(async move {
            // Debit from source
            let from_account = Account::find_by_id(from).one(txn).await?.unwrap();
            account::ActiveModel {
                balance: Set(from_account.balance - amount),
                ..from_account.into()
            }.update(txn).await?;

            // Credit to destination
            let to_account = Account::find_by_id(to).one(txn).await?.unwrap();
            account::ActiveModel {
                balance: Set(to_account.balance + amount),
                ..to_account.into()
            }.update(txn).await?;

            Ok(())
        })
    }).await
}
```

## Migrations

```rust
// migration/src/m20220101_000001_create_users.rs
use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager.create_table(
            Table::create()
                .table(Users::Table)
                .col(ColumnDef::new(Users::Id).integer().auto_increment().primary_key())
                .col(ColumnDef::new(Users::Name).string().not_null())
                .col(ColumnDef::new(Users::Email).string().unique_key().not_null())
                .to_owned()
        ).await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager.drop_table(Table::drop().table(Users::Table).to_owned()).await
    }
}
```

## Best Practices

1. **ActiveModel**: Use `Set()` for values to update
2. **Transactions**: Wrap related operations
3. **Migrations**: Use sea-orm-cli for generation
4. **Relations**: Define both sides of relationships
5. **Logging**: Enable sqlx_logging for debugging

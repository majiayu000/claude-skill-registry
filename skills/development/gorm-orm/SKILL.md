---
name: GORM ORM
description: Full-featured Go ORM with associations, hooks, and migrations.
metadata:
  labels: [golang, gorm, orm, database]
  triggers:
    files: ['**/models/*.go', '**/main.go']
    keywords: [gorm, gorm.Model, gorm.Open, db.Create]
---

# GORM Standards

## Database Connection

```go
import (
    "gorm.io/gorm"
    "gorm.io/driver/postgres"
)

func InitDB() (*gorm.DB, error) {
    dsn := "host=localhost user=postgres password=pass dbname=app port=5432 sslmode=disable"
    db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{
        Logger: logger.Default.LogMode(logger.Info),
    })
    if err != nil {
        return nil, err
    }

    // Connection pool settings
    sqlDB, _ := db.DB()
    sqlDB.SetMaxIdleConns(10)
    sqlDB.SetMaxOpenConns(100)
    sqlDB.SetConnMaxLifetime(time.Hour)

    return db, nil
}
```

## Models

```go
type User struct {
    gorm.Model           // ID, CreatedAt, UpdatedAt, DeletedAt
    Name     string      `gorm:"size:100;not null"`
    Email    string      `gorm:"uniqueIndex;not null"`
    Age      int         `gorm:"default:0"`
    Profile  Profile     `gorm:"constraint:OnDelete:CASCADE;"`
    Posts    []Post      `gorm:"foreignKey:AuthorID"`
}

type Profile struct {
    ID     uint
    UserID uint   `gorm:"uniqueIndex"`
    Bio    string `gorm:"type:text"`
}

type Post struct {
    ID       uint
    Title    string
    AuthorID uint
    Author   User `gorm:"foreignKey:AuthorID"`
}
```

## CRUD Operations

```go
// Create
user := User{Name: "John", Email: "john@example.com"}
result := db.Create(&user)  // user.ID is set after insert

// Create in batches
users := []User{{Name: "A"}, {Name: "B"}, {Name: "C"}}
db.CreateInBatches(users, 100)

// Read
var user User
db.First(&user, 1)                      // By primary key
db.First(&user, "email = ?", "john@example.com")
db.Where("age > ?", 18).Find(&users)    // Multiple results

// Update
db.Model(&user).Update("Name", "Jane")
db.Model(&user).Updates(User{Name: "Jane", Age: 25})
db.Model(&user).Updates(map[string]interface{}{"name": "Jane", "age": 25})

// Delete (soft delete with gorm.Model)
db.Delete(&user, 1)

// Permanent delete
db.Unscoped().Delete(&user, 1)
```

## Queries

```go
// Conditions
db.Where("name = ?", "John").Find(&users)
db.Where("name IN ?", []string{"John", "Jane"}).Find(&users)
db.Where("age BETWEEN ? AND ?", 18, 65).Find(&users)

// Order, Limit, Offset
db.Order("created_at desc").Limit(10).Offset(20).Find(&users)

// Select specific columns
db.Select("name", "email").Find(&users)

// Group and Having
db.Model(&User{}).Select("name, sum(age)").Group("name").Having("sum(age) > ?", 100).Find(&results)

// Joins
db.Joins("Profile").Find(&users)  // Preload with join

// Raw SQL
db.Raw("SELECT * FROM users WHERE age > ?", 18).Scan(&users)
```

## Associations

```go
// Preload (eager loading)
db.Preload("Posts").Find(&users)
db.Preload("Posts.Comments").Find(&users)  // Nested
db.Preload("Posts", "published = ?", true).Find(&users)  // Conditional

// Association operations
db.Model(&user).Association("Posts").Append(&post)
db.Model(&user).Association("Posts").Delete(&post)
db.Model(&user).Association("Posts").Clear()
db.Model(&user).Association("Posts").Count()
```

## Transactions

```go
// Automatic transaction
err := db.Transaction(func(tx *gorm.DB) error {
    if err := tx.Create(&user).Error; err != nil {
        return err  // Rollback
    }
    if err := tx.Create(&profile).Error; err != nil {
        return err  // Rollback
    }
    return nil  // Commit
})

// Manual transaction
tx := db.Begin()
if err := tx.Create(&user).Error; err != nil {
    tx.Rollback()
    return err
}
if err := tx.Create(&profile).Error; err != nil {
    tx.Rollback()
    return err
}
tx.Commit()
```

## Hooks

```go
// BeforeCreate
func (u *User) BeforeCreate(tx *gorm.DB) error {
    u.UUID = uuid.New()
    return nil
}

// AfterCreate
func (u *User) AfterCreate(tx *gorm.DB) error {
    // Send welcome email
    return nil
}

// BeforeUpdate, AfterUpdate, BeforeDelete, AfterDelete, AfterFind
```

## Migrations

```go
// Auto migrate (development only)
db.AutoMigrate(&User{}, &Post{}, &Profile{})

// For production, use golang-migrate/migrate
// migrations/000001_create_users.up.sql
// migrations/000001_create_users.down.sql
```

## Best Practices

1. **Avoid N+1**: Use `Preload` or `Joins` for associations
2. **Transactions**: Wrap related operations in transactions
3. **Indexes**: Add `gorm:"index"` for frequently queried columns
4. **Soft delete**: Use `gorm.Model` for soft delete, `Unscoped()` for hard delete
5. **Migrations**: Use migration tools for production, not AutoMigrate

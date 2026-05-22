---
name: database-data-generation
description: Generate realistic database seed data and test fixtures for development, testing, and demonstrations. Creates realistic users, products, orders, and custom schemas using Faker libraries while maintaining relational integrity and data consistency. Use when populating databases, creating test fixtures, seeding development environments, or generating demo data.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
version: 1.0.0
---

# Database Data Generation

Automate creation of realistic seed data and test fixtures for databases, ensuring relational integrity and data consistency across development and testing environments.

## Overview

This skill empowers you to:
- **Generate seed data**: Create production-like data for development databases
- **Create test fixtures**: Generate diverse test data for automated testing
- **Maintain relationships**: Ensure foreign key integrity across related tables
- **Customize volume**: Control the amount of data generated
- **Support multiple formats**: Export as SQL, JSON, JavaScript, Python, or framework-specific formats

---

## Part 1: Database Seeding

### How Seeding Works

1. **Analyze Schema**: Examine database structure, tables, columns, data types, and relationships
2. **Generate Realistic Data**: Use Faker libraries to create believable data matching your schema
3. **Maintain Relationships**: Ensure foreign keys link correctly between related tables
4. **Create Seed Scripts**: Generate executable scripts (SQL, migration files, ORM seeds)

### When to Use Database Seeding

- Populate development databases with realistic data
- Create initial data for new application installations
- Reset database to known state for testing
- Demonstrate application features with pre-populated data
- Train new team members with realistic examples

### Seeding Examples

#### Example 1: Simple User Seeding (SQL)

**User request**: "Create a seed script to populate my users table with 50 realistic users."

**Generated SQL**:
```sql
-- Users seed data
INSERT INTO users (name, email, password, created_at) VALUES
('John Doe', 'john.doe@example.com', '$2y$10$...', '2025-01-15 10:23:45'),
('Jane Smith', 'jane.smith@example.com', '$2y$10$...', '2025-01-16 14:12:30'),
('Michael Johnson', 'michael.j@example.com', '$2y$10$...', '2025-01-17 09:45:10'),
-- ... 47 more users
('Sarah Williams', 'sarah.w@example.com', '$2y$10$...', '2025-02-10 16:30:22');
```

#### Example 2: E-Commerce Database Seeding (Laravel)

**User request**: "Generate test data for my e-commerce database, including users, products, categories, and orders."

**Generated Seeder (Laravel)**:
```php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\User;
use App\Models\Category;
use App\Models\Product;
use App\Models\Order;

class EcommerceSeeder extends Seeder
{
    public function run(): void
    {
        // Create categories first (no dependencies)
        $categories = [
            Category::create(['name' => 'Electronics', 'slug' => 'electronics']),
            Category::create(['name' => 'Clothing', 'slug' => 'clothing']),
            Category::create(['name' => 'Home & Garden', 'slug' => 'home-garden']),
        ];

        // Create users (no dependencies)
        $users = User::factory(50)->create();

        // Create products (depends on categories)
        $products = [];
        foreach ($categories as $category) {
            $products = array_merge(
                $products,
                Product::factory(20)
                    ->for($category)
                    ->create()
                    ->toArray()
            );
        }

        // Create orders (depends on users and products)
        foreach ($users as $user) {
            // Each user has 1-5 orders
            $orderCount = rand(1, 5);
            
            for ($i = 0; $i < $orderCount; $i++) {
                $order = Order::factory()->for($user)->create();
                
                // Attach 1-4 random products to each order
                $orderProducts = collect($products)
                    ->random(rand(1, 4))
                    ->pluck('id');
                    
                $order->products()->attach($orderProducts);
            }
        }
    }
}
```

#### Example 3: Blog Database with Relationships (TypeScript/Prisma)

**User request**: "Seed my blog database with users, posts, comments, and tags."

**Generated Seeder (Prisma)**:
```typescript
import { PrismaClient } from '@prisma/client';
import { faker } from '@faker-js/faker';

const prisma = new PrismaClient();

async function main() {
  // Create users
  const users = await Promise.all(
    Array.from({ length: 20 }, async () => {
      return prisma.user.create({
        data: {
          name: faker.person.fullName(),
          email: faker.internet.email(),
          bio: faker.lorem.paragraph(),
          avatar: faker.image.avatar(),
        },
      });
    })
  );

  // Create tags
  const tags = await Promise.all(
    ['JavaScript', 'Python', 'React', 'Node.js', 'TypeScript'].map(name =>
      prisma.tag.create({ data: { name, slug: name.toLowerCase() } })
    )
  );

  // Create posts with comments
  for (const user of users) {
    const postCount = faker.number.int({ min: 2, max: 10 });

    for (let i = 0; i < postCount; i++) {
      const post = await prisma.post.create({
        data: {
          title: faker.lorem.sentence(),
          slug: faker.helpers.slugify(faker.lorem.words(5)),
          content: faker.lorem.paragraphs(5),
          published: faker.datatype.boolean(0.8),
          userId: user.id,
          tags: {
            connect: faker.helpers.arrayElements(tags, { min: 1, max: 3 })
              .map(tag => ({ id: tag.id })),
          },
        },
      });

      // Add comments to post
      const commentCount = faker.number.int({ min: 0, max: 8 });
      
      for (let j = 0; j < commentCount; j++) {
        await prisma.comment.create({
          data: {
            content: faker.lorem.paragraph(),
            postId: post.id,
            userId: faker.helpers.arrayElement(users).id,
          },
        });
      }
    }
  }

  console.log(`✅ Seeded ${users.length} users with posts and comments`);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

---

## Part 2: Test Data Generation

### How Test Data Generation Works

1. **Identify Requirements**: Determine data types, volumes, and specific attributes needed
2. **Generate Diverse Data**: Create varied test cases including edge cases
3. **Format Output**: Structure data for easy consumption (JSON, CSV, SQL, fixtures)
4. **Support Custom Schemas**: Generate data matching your specific data models

### When to Use Test Data Generation

- Populate test databases for automated testing
- Create fixtures for unit/integration tests
- Generate load testing data
- Simulate production-like scenarios
- Test edge cases and boundary conditions
- Create demo datasets for presentations

### Test Data Examples

#### Example 1: User Test Fixtures (JSON)

**User request**: "Generate 100 test users with realistic names, emails, and addresses in JSON format."

**Generated JSON**:
```json
[
  {
    "id": 1,
    "name": "Alice Johnson",
    "email": "alice.johnson@example.com",
    "phone": "+1-555-0123",
    "address": {
      "street": "123 Main St",
      "city": "New York",
      "state": "NY",
      "zipCode": "10001",
      "country": "USA"
    },
    "dateOfBirth": "1985-03-15",
    "createdAt": "2025-01-10T08:30:00Z"
  },
  {
    "id": 2,
    "name": "Bob Martinez",
    "email": "bob.martinez@example.com",
    "phone": "+1-555-0456",
    "address": {
      "street": "456 Oak Ave",
      "city": "Los Angeles",
      "state": "CA",
      "zipCode": "90001",
      "country": "USA"
    },
    "dateOfBirth": "1992-07-22",
    "createdAt": "2025-01-11T14:15:00Z"
  }
  // ... 98 more users
]
```

#### Example 2: Product Test Data (Python Pytest Fixtures)

**User request**: "Create product test data including name, description, price, and category for automated tests."

**Generated Pytest Fixtures**:
```python
import pytest
from faker import Faker
from decimal import Decimal

fake = Faker()

@pytest.fixture
def sample_products():
    """Generate sample products for testing"""
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports']
    
    return [
        {
            'id': i + 1,
            'name': fake.catch_phrase(),
            'description': fake.text(max_nb_chars=200),
            'price': Decimal(fake.pydecimal(left_digits=3, right_digits=2, positive=True)),
            'category': fake.random_element(elements=categories),
            'sku': fake.bothify(text='??-####'),
            'stock': fake.random_int(min=0, max=500),
            'is_active': fake.boolean(chance_of_getting_true=85),
            'created_at': fake.date_time_this_year(),
        }
        for i in range(100)
    ]

@pytest.fixture
def product_edge_cases():
    """Edge cases for product testing"""
    return [
        {'id': 1, 'name': '', 'price': Decimal('0.00')},  # Empty name, zero price
        {'id': 2, 'name': 'A' * 255, 'price': Decimal('999999.99')},  # Max length, max price
        {'id': 3, 'name': 'Test', 'price': Decimal('0.01')},  # Minimum price
        {'id': 4, 'name': None, 'price': None},  # Null values
    ]

def test_product_creation(sample_products):
    """Test product creation with realistic data"""
    for product in sample_products:
        # Your test logic here
        assert product['price'] > 0
        assert len(product['name']) > 0
```

#### Example 3: Order Transaction Test Data (Custom Schema)

**User request**: "Generate order test data with payment info, shipping addresses, and line items."

**Generated Test Data**:
```javascript
// testData/orders.js
const { faker } = require('@faker-js/faker');

function generateOrders(count = 50) {
  const orders = [];

  for (let i = 0; i < count; i++) {
    const lineItems = [];
    const itemCount = faker.number.int({ min: 1, max: 5 });

    for (let j = 0; j < itemCount; j++) {
      const quantity = faker.number.int({ min: 1, max: 3 });
      const price = faker.number.float({ min: 10, max: 500, precision: 0.01 });
      
      lineItems.push({
        productId: faker.string.uuid(),
        productName: faker.commerce.productName(),
        quantity,
        price,
        subtotal: quantity * price,
      });
    }

    const subtotal = lineItems.reduce((sum, item) => sum + item.subtotal, 0);
    const tax = subtotal * 0.08;
    const shipping = faker.number.float({ min: 5, max: 20, precision: 0.01 });
    const total = subtotal + tax + shipping;

    orders.push({
      orderId: faker.string.uuid(),
      orderNumber: faker.string.alphanumeric(8).toUpperCase(),
      customerId: faker.string.uuid(),
      status: faker.helpers.arrayElement(['pending', 'processing', 'shipped', 'delivered', 'cancelled']),
      
      // Line items
      items: lineItems,
      
      // Pricing
      subtotal,
      tax,
      shipping,
      total,
      
      // Shipping address
      shippingAddress: {
        name: faker.person.fullName(),
        street: faker.location.streetAddress(),
        city: faker.location.city(),
        state: faker.location.state(),
        zipCode: faker.location.zipCode(),
        country: 'USA',
      },
      
      // Payment info (sanitized for testing)
      payment: {
        method: faker.helpers.arrayElement(['credit_card', 'paypal', 'bank_transfer']),
        lastFourDigits: faker.string.numeric(4),
        cardType: faker.helpers.arrayElement(['Visa', 'Mastercard', 'Amex']),
      },
      
      // Timestamps
      createdAt: faker.date.recent({ days: 30 }),
      updatedAt: faker.date.recent({ days: 7 }),
    });
  }

  return orders;
}

module.exports = { generateOrders };
```

---

## Supported Data Types & Faker Methods

### Personal Information
```javascript
faker.person.fullName()         // "John Doe"
faker.person.firstName()        // "Jane"
faker.person.lastName()         // "Smith"
faker.internet.email()          // "john.doe@example.com"
faker.phone.number()            // "+1-555-0123"
faker.date.birthdate()          // 1985-03-15
```

### Location Data
```javascript
faker.location.streetAddress()  // "123 Main St"
faker.location.city()           // "New York"
faker.location.state()          // "California"
faker.location.zipCode()        // "90210"
faker.location.country()        // "United States"
```

### Business Data
```javascript
faker.company.name()            // "Acme Corporation"
faker.commerce.productName()    // "Handcrafted Steel Shoes"
faker.commerce.department()     // "Electronics"
faker.commerce.price()          // "123.45"
faker.finance.creditCardNumber()// "4532-1234-5678-9010"
```

### Internet & Tech
```javascript
faker.internet.url()            // "https://example.com"
faker.internet.userName()       // "john_doe_123"
faker.internet.password()       // "aB3$xYz9!"
faker.internet.ip()             // "192.168.1.1"
faker.string.uuid()             // "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
```

### Text Content
```javascript
faker.lorem.sentence()          // "Lorem ipsum dolor sit amet."
faker.lorem.paragraph()         // Full paragraph
faker.lorem.words(5)            // "lorem ipsum dolor sit amet"
faker.hacker.phrase()           // "Try to compress the RAM circuit!"
```

---

## Best Practices

### Data Volume
- ✅ Start small (10-50 records) and scale up gradually
- ✅ Consider database performance limits
- ✅ Use pagination for large datasets
- ❌ Don't generate millions of records without need

### Data Consistency
- ✅ Use appropriate Faker methods for data types
- ✅ Respect database constraints (NOT NULL, UNIQUE)
- ✅ Match data formats (dates, phone numbers, currencies)
- ✅ Use consistent locale settings
- ❌ Don't mix data formats (e.g., US vs EU dates)

### Relationship Integrity
- ✅ Create parent records before child records
- ✅ Use valid foreign key references
- ✅ Test referential integrity constraints
- ❌ Don't create orphan records

### Idempotency
- ✅ Design seeds to run multiple times safely
- ✅ Clear existing data before seeding
- ✅ Use transactions for atomic operations
- ✅ Handle unique constraint violations
- ❌ Don't assume empty database

### Testing Focus
- ✅ Include edge cases (empty, null, max values)
- ✅ Generate diverse data for comprehensive testing
- ✅ Use seed values for reproducible tests
- ✅ Separate test data from seed data
- ❌ Don't rely solely on "happy path" data

---

## Framework-Specific Examples

### Laravel Seeders
```php
// database/seeders/UserSeeder.php
class UserSeeder extends Seeder {
    public function run(): void {
        User::factory(100)->create();
    }
}
```

### Django Fixtures
```python
# management/commands/seed.py
from django.core.management.base import BaseCommand
from myapp.factories import UserFactory

class Command(BaseCommand):
    def handle(self, *args, **options):
        UserFactory.create_batch(100)
```

### Rails Seeds
```ruby
# db/seeds.rb
100.times do
  User.create!(
    name: Faker::Name.name,
    email: Faker::Internet.email
  )
end
```

### Prisma Seeds
```typescript
// prisma/seed.ts
import { PrismaClient } from '@prisma/client'
const prisma = new PrismaClient()

async function main() {
  await prisma.user.createMany({
    data: users
  })
}
```

---

## Integration with Other Tools

- **Testing Frameworks**: Jest, Pytest, PHPUnit, Mocha
- **ORMs**: Prisma, TypeORM, Sequelize, Eloquent, Django ORM
- **Migration Tools**: Flyway, Liquibase, Alembic
- **CI/CD Pipelines**: Automate seeding in test environments
- **Load Testing**: Generate large datasets for performance testing

---

**Remember**: Good test data and seeds make development and testing faster, more reliable, and closer to production scenarios.

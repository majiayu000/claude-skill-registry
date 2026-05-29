---
name: vendix-prisma-seed
description: Seeding patterns.
metadata:
  scope: [root]
  auto_invoke: "Creating Seeds"
---
# Vendix Prisma Seed Pattern

> **Seed Data Structure** - Seeds estructurados con orden de eliminación y creación consistente.

## 🎯 Seed Structure

**File:** `apps/backend/prisma/seeds/shared/database.ts`

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export async function clearDatabase(prisma_client: PrismaClient = prisma) {
  // Deletion order (reverse of dependencies)
  const deleteOperations = [
    // Delete dependents first
    { name: 'sales_order_items', model: prisma_client.sales_order_items },
    { name: 'sales_orders', model: prisma_client.sales_orders },
    { name: 'cart_items', model: prisma_client.cart_items },
    { name: 'wishlists', model: prisma_client.wishlists },

    // Delete main entities
    { name: 'products', model: prisma_client.products },
    { name: 'stores', model: prisma_client.stores },
    { name: 'store_users', model: prisma_client.store_users },
    { name: 'users', model: prisma_client.users },
    { name: 'organizations', model: prisma_client.organizations },
  ];

  for (const operation of deleteOperations) {
    await operation.model.deleteMany({});
    console.log(`✓ Cleared ${operation.name}`);
  }
}
```

---

## 📁 Seed Directory Structure

```
apps/backend/prisma/seeds/
├── shared/
│   ├── database.ts              # Database utilities
│   └── helpers.ts               # Seed helpers
├── dev/
│   ├── index.ts                 # Main seed file
│   ├── seed-organizations.ts    # Organization seeds
│   ├── seed-users.ts            # User seeds
│   ├── seed-stores.ts           # Store seeds
│   └── seed-products.ts         # Product seeds
└── prod/
    └── index.ts                 # Production seeds (minimal)
```

---

## 🌱 Seed Pattern

### Base Seed Function

```typescript
// seeds/shared/helpers.ts
export async function seedWithRetry<T>(
  seed_name: string,
  seed_function: () => Promise<T>,
  max_retries = 3,
): Promise<T> {
  let last_error: Error | null = null;

  for (let attempt = 1; attempt <= max_retries; attempt++) {
    try {
      console.log(`Seeding ${seed_name} (attempt ${attempt}/${max_retries})...`);
      const result = await seed_function();
      console.log(`✓ ${seed_name} seeded successfully`);
      return result;
    } catch (error) {
      last_error = error;
      console.error(`✗ Failed to seed ${seed_name}:`, error.message);

      if (attempt < max_retries) {
        console.log(`Retrying in 1 second...`);
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
  }

  throw last_error;
}
```

---

### Organization Seed

```typescript
// seeds/dev/seed-organizations.ts
import { PrismaClient } from '@prisma/client';
import { seedWithRetry } from '../shared/helpers';

export async function seedOrganizations(prisma: PrismaClient) {
  return seedWithRetry('organizations', async () => {
    const organizations = await Promise.all([
      prisma.organizations.create({
        data: {
          name: 'Acme Corporation',
          domain_name: 'acme',
          is_active: true,
        },
      }),
      prisma.organizations.create({
        data: {
          name: 'Globex Inc',
          domain_name: 'globex',
          is_active: true,
        },
      }),
      prisma.organizations.create({
        data: {
          name: 'Soylent Corp',
          domain_name: 'soylent',
          is_active: false,  // Inactive organization
        },
      }),
    ]);

    console.log(`✓ Created ${organizations.length} organizations`);

    return organizations;
  });
}
```

---

### User Seed

```typescript
// seeds/dev/seed-users.ts
import { PrismaClient } from '@prisma/client';
import * as bcrypt from 'bcrypt';
import { seedWithRetry } from '../shared/helpers';

export async function seedUsers(prisma: PrismaClient, organizations: any[]) {
  return seedWithRetry('users', async () => {
    const hashed_password = await bcrypt.hash('Password123!', 10);

    const users = await Promise.all([
      // Super Admin
      prisma.users.create({
        data: {
          user_name: 'super_admin',
          email: 'superadmin@vendix.com',
          password: hashed_password,
          organization_id: organizations[0].id,
          roles: ['super_admin'],
          is_active: true,
        },
      }),

      // Organization Admin
      prisma.users.create({
        data: {
          user_name: 'org_admin',
          email: 'admin@acme.com',
          password: hashed_password,
          organization_id: organizations[0].id,
          main_store_id: null,
          roles: ['organization_admin'],
          is_active: true,
        },
      }),

      // Store Admin
      prisma.users.create({
        data: {
          user_name: 'store_admin',
          email: 'storeadmin@acme.com',
          password: hashed_password,
          organization_id: organizations[0].id,
          roles: ['store_admin'],
          is_active: true,
        },
      }),

      // Regular User
      prisma.users.create({
        data: {
          user_name: 'john_doe',
          email: 'john@acme.com',
          password: hashed_password,
          organization_id: organizations[0].id,
          roles: ['store_user'],
          is_active: true,
        },
      }),
    ]);

    console.log(`✓ Created ${users.length} users`);

    return users;
  });
}
```

---

### Store Seed

```typescript
// seeds/dev/seed-stores.ts
import { PrismaClient } from '@prisma/client';
import { seedWithRetry } from '../shared/helpers';

export async function seedStores(prisma: PrismaClient, organizations: any[]) {
  return seedWithRetry('stores', async () => {
    const stores = await Promise.all([
      prisma.stores.create({
        data: {
          name: 'Acme Main Store',
          domain_name: 'acme-main',
          description: 'Main retail location',
          organization_id: organizations[0].id,
          is_active: true,
          logo_url: 'https://example.com/logo.png',
          theme_config: {
            primary_color: '#0066cc',
            secondary_color: '#ff6600',
            font_family: 'Roboto',
          },
        },
      }),

      prisma.stores.create({
        data: {
          name: 'Acme Online Store',
          domain_name: 'acme-online',
          description: 'E-commerce storefront',
          organization_id: organizations[0].id,
          is_active: true,
          theme_config: {
            primary_color: '#0099ff',
            secondary_color: '#ff9900',
            font_family: 'Open Sans',
          },
        },
      }),
    ]);

    console.log(`✓ Created ${stores.length} stores`);

    return stores;
  });
}
```

---

### Product Seed

```typescript
// seeds/dev/seed-products.ts
import { PrismaClient } from '@prisma/client';
import { seedWithRetry } from '../shared/helpers';

export async function seedProducts(prisma: PrismaClient, stores: any[]) {
  return seedWithRetry('products', async () => {
    const products = await Promise.all([
      prisma.products.create({
        data: {
          name: 'Wireless Headphones',
          description: 'High-quality wireless headphones',
          base_price: 79.99,
          organization_id: stores[0].organization_id,
          store_id: stores[0].id,
          is_active: true,
          stock_quantity: 100,
          images: [
            'https://example.com/headphones1.jpg',
            'https://example.com/headphones2.jpg',
          ],
          product_variants: {
            create: [
              {
                sku: 'WH-BLK',
                color: 'Black',
                price_adjustment: 0,
                stock_quantity: 50,
              },
              {
                sku: 'WH-WHT',
                color: 'White',
                price_adjustment: 0,
                stock_quantity: 50,
              },
            ],
          },
        },
      }),

      prisma.products.create({
        data: {
          name: 'USB-C Cable',
          description: '6ft USB-C charging cable',
          base_price: 12.99,
          organization_id: stores[0].organization_id,
          store_id: stores[0].id,
          is_active: true,
          stock_quantity: 500,
          images: [
            'https://example.com/cable.jpg',
          ],
          product_variants: {
            create: [
              {
                sku: 'UC-6FT',
                color: 'Red',
                price_adjustment: 0,
                stock_quantity: 250,
              },
              {
                sku: 'UC-10FT',
                color: 'Blue',
                price_adjustment: 2.00,
                stock_quantity: 250,
              },
            ],
          },
        },
      }),
    ]);

    console.log(`✓ Created ${products.length} products`);

    return products;
  });
}
```

---

## 🚀 Main Seed File

```typescript
// seeds/dev/index.ts
import { PrismaClient } from '@prisma/client';
import { clearDatabase } from '../shared/database';
import { seedOrganizations } from './seed-organizations';
import { seedUsers } from './seed-users';
import { seedStores } from './seed-stores';
import { seedProducts } from './seed-products';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Starting database seed...\n');

  // Clear existing data
  console.log('Clearing existing data...');
  await clearDatabase(prisma);
  console.log('✓ Database cleared\n');

  // Seed in order of dependencies
  const organizations = await seedOrganizations(prisma);
  console.log('');

  const users = await seedUsers(prisma, organizations);
  console.log('');

  const stores = await seedStores(prisma, organizations);
  console.log('');

  const products = await seedProducts(prisma, stores);
  console.log('');

  // Assign stores to users
  console.log('Assigning stores to users...');
  await Promise.all([
    // Store admin gets main store
    prisma.store_users.create({
      data: {
        user_id: users[2].id,  // store_admin
        store_id: stores[0].id,
        role: 'store_admin',
      },
    }),

    // Regular user gets online store
    prisma.store_users.create({
      data: {
        user_id: users[3].id,  // john_doe
        store_id: stores[1].id,
        role: 'store_user',
      },
    }),
  ]);
  console.log('✓ Stores assigned\n');

  console.log('✅ Database seed completed successfully!');
  console.log('\n📊 Summary:');
  console.log(`  - ${organizations.length} organizations`);
  console.log(`  - ${users.length} users`);
  console.log(`  - ${stores.length} stores`);
  console.log(`  - ${products.length} products`);
}

main()
  .catch((e) => {
    console.error('❌ Seed failed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

---

## 🔧 Running Seeds

### Development Seed

```bash
# Reset database and seed
npx prisma migrate reset

# Or run seed directly
npx prisma db seed

# Or with npm script
npm run db:seed
```

### Production Seed

```bash
# Only seed essential data (admin users, etc.)
npx prisma db seed -- --production
```

---

## 📋 Package.json Configuration

```json
{
  "prisma": {
    "seed": "ts-node --compiler-options {\"module\":\"CommonJS\"} prisma/seeds/dev/index.ts"
  }
}
```

---

## 🔍 Key Files Reference

| File | Purpose |
|------|---------|
| `seeds/shared/database.ts` | Database utilities |
| `seeds/shared/helpers.ts` | Seed helper functions |
| `seeds/dev/index.ts` | Main seed file |
| `seeds/dev/seed-*.ts` | Entity-specific seeds |

---

## Related Skills

- `vendix-prisma-schema` - Schema editing patterns
- `vendix-backend-prisma` - Prisma service patterns
- `vendix-naming-conventions` - Naming conventions (CRITICAL)

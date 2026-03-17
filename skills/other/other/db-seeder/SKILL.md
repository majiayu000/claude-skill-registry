---
name: db-seeder
description: This skill should be used when seeding databases with realistic fake data for development, testing, or staging environments. Supports PostgreSQL, MySQL, SQLite, MongoDB with ORM-based seeding (SQLAlchemy, Django, Prisma) and Faker library for generating realistic test data. Use when the user needs to populate databases with sample data, create test fixtures, or set up development/staging environments with realistic data.
---

# Database Seeder Skill

Seed any database with realistic fake data using ORM patterns and the Faker library. This skill provides scripts, references, and templates for efficiently populating databases with test data for development, testing, and staging environments.

## When to Use This Skill

Use this skill when:
- Setting up local development databases with sample data
- Creating test fixtures for automated testing
- Populating staging environments with realistic production-like data
- Generating demo data for presentations or user onboarding
- Need to quickly create large volumes of realistic test data
- Migrating between database systems and need to populate new databases

## Supported Databases

- **PostgreSQL** - Relational database (default for production)
- **MySQL / MariaDB** - Relational database
- **SQLite** - File-based database (testing, development)
- **MongoDB** - NoSQL document database
- **Any ORM-supported database** - Via SQLAlchemy, Django ORM, Prisma, etc.

The skill automatically detects database configuration from:
- Environment variables (`DATABASE_URL`, `DB_TYPE`, etc.)
- Configuration files (`.env`, `settings.py`, `config.yaml`)
- Alembic migrations (`alembic.ini`)
- Docker Compose files

## Skill Workflow

### Step 1: Detect Database Configuration

Before seeding, detect the database configuration automatically:

```bash
python scripts/detect_db_config.py
```

The detection script will:
1. Check environment variables (`DATABASE_URL`, `DB_TYPE`, etc.)
2. Search for configuration files (`.env`, `settings.py`, `alembic.ini`)
3. Analyze project structure (SQLite files, Docker Compose)
4. Output connection details and ready-to-use seeding commands

### Step 1.5: Inspect Database Schema (Optional but Recommended)

**NEW**: Automatically inspect your database schema to generate factories and fixtures:

```bash
# Inspect schema and print summary
python scripts/inspect_schema.py \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/mydb"

# Generate factory functions for all tables
python scripts/inspect_schema.py \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/mydb" \
  --generate-factories

# Generate JSON fixture templates
python scripts/inspect_schema.py \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/mydb" \
  --generate-fixtures \
  --fixture-count 5

# Both
python scripts/inspect_schema.py \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/mydb" \
  --generate-factories \
  --generate-fixtures
```

**What it does:**
- ✅ **Detects all tables/collections** in your database
- ✅ **Analyzes column types** (VARCHAR, INTEGER, DATE, etc.)
- ✅ **Identifies foreign key relationships**
- ✅ **Generates appropriate Faker methods** for each field
- ✅ **Creates ready-to-use factory functions** (`generated_factories.py`)
- ✅ **Creates JSON fixture templates** (`generated_fixtures.json`)

**Works with ANY schema** - No hardcoded assumptions!

**Manual Configuration:**
If auto-detection fails, specify database details manually:

```bash
# PostgreSQL
python scripts/seed_database.py \
  --db postgresql \
  --connection "postgresql://user:pass@localhost:5432/mydb" \
  --count 100

# SQLite
python scripts/seed_database.py \
  --db sqlite \
  --connection "sqlite:///./test.db" \
  --count 50

# MongoDB
python scripts/seed_database.py \
  --db mongodb \
  --connection "mongodb://admin:pass@localhost:27017/mydb" \
  --count 100
```

**Configuration Files Reference:**
For detailed database connection patterns and configuration examples, refer to:
`references/database-configs.md`

### Step 2: Choose Seeding Approach

Three primary approaches are available:

#### Approach A: Generate JSON Fixtures First (Recommended for Reusability)

Generate reusable JSON fixtures that can be version-controlled and shared:

```bash
# Generate using predefined templates
python scripts/generate_fixtures.py \
  --template elios-interview \
  --output fixtures/elios_data.json \
  --pretty

# Generate specific models
python scripts/generate_fixtures.py \
  --models User:100,Post:500,Candidate:50 \
  --output fixtures/test_data.json \
  --pretty

# Seed database from fixtures
python scripts/seed_database.py \
  --fixtures fixtures/test_data.json \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/db"
```

**Benefits:**
- Fixtures can be version-controlled
- Reusable across environments
- Consistent test data
- Easy to share with team

#### Approach B: Direct Database Seeding with Custom Factories

Create Python factory functions and seed directly:

```python
# Create seeding script: scripts/seed_elios.py

from seed_database import DatabaseSeeder, create_seeder

def candidate_factory(fake, index):
    return {
        'full_name': fake.name(),
        'email': fake.email(),
        'years_of_experience': fake.random_int(min=0, max=15),
        'skills': fake.random_elements(
            ['Python', 'JavaScript', 'SQL', 'React'],
            length=fake.random_int(min=2, max=6),
            unique=True
        ),
        'status': fake.random_element(['pending', 'interviewed', 'hired']),
    }

# Run seeding
seeder = create_seeder('postgresql', 'postgresql://user:pass@localhost/db')
seeder.seed_model(Candidate, count=50, factory_func=candidate_factory)
```

**Benefits:**
- Full control over data generation
- Can use complex business logic
- Direct database insertion (faster)

#### Approach C: Configuration-Based Seeding

Use YAML configuration file for declarative seeding:

```bash
# Copy template
cp assets/seed-config-template.yaml seed-config.yaml

# Edit seed-config.yaml to define models and factories

# Run seeding
python scripts/seed_database.py --config seed-config.yaml
```

**Benefits:**
- Declarative configuration
- No code required
- Easy to modify counts and settings

### Step 3: Execute Seeding

Based on chosen approach:

**For Fixtures:**
```bash
python scripts/seed_database.py \
  --fixtures fixtures/test_data.json \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/db"
```

**For Custom Factories:**
```bash
python scripts/seed_elios.py
```

**For Configuration:**
```bash
python scripts/seed_database.py --config seed-config.yaml
```

### Step 4: Verify Seeding

After seeding completes, verify the data:

```bash
# For PostgreSQL/MySQL
psql -d mydb -c "SELECT COUNT(*) FROM users;"
psql -d mydb -c "SELECT COUNT(*) FROM candidates;"

# For SQLite
sqlite3 mydb.db "SELECT COUNT(*) FROM users;"

# For MongoDB
mongosh mydb --eval "db.users.countDocuments()"
```

## Bundled Resources

### Scripts (`scripts/`)

#### `seed_database.py`
Main seeding orchestrator with Faker integration.

**Features:**
- Auto-detects database type from connection string
- Supports SQLAlchemy-based databases (PostgreSQL, MySQL, SQLite)
- Supports MongoDB with PyMongo
- Batch insertion for performance
- Progress reporting
- Error handling and rollback

**Usage:**
```bash
# Seed from fixtures
python scripts/seed_database.py \
  --fixtures data.json \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/db"

# Seed from config
python scripts/seed_database.py --config seed-config.yaml

# Custom locale for international data
python scripts/seed_database.py \
  --fixtures data.json \
  --db sqlite \
  --connection "sqlite:///test.db" \
  --locale fr_FR
```

#### `detect_db_config.py`
Automatically detects database configuration from project.

**Features:**
- Scans environment variables
- Parses configuration files (`.env`, `settings.py`, `config.yaml`)
- Detects Alembic migrations configuration
- Finds SQLite database files
- Outputs connection strings with masked passwords

**Usage:**
```bash
# Auto-detect
python scripts/detect_db_config.py

# Specify config file
python scripts/detect_db_config.py --config-path src/infrastructure/config/settings.py

# Specify .env file
python scripts/detect_db_config.py --env-file .env.local

# Specify project root
python scripts/detect_db_config.py --project-root /path/to/project
```

#### `generate_fixtures.py`
Generates JSON fixtures with realistic fake data.

**Features:**
- Predefined templates (Elios interview system, blog, e-commerce)
- Custom model generation
- Configurable record counts
- Multiple Faker locales
- Pretty-printed JSON output

**Usage:**
```bash
# Generate from template
python scripts/generate_fixtures.py \
  --template elios-interview \
  --output fixtures.json \
  --pretty

# Generate specific models
python scripts/generate_fixtures.py \
  --models User:100,Post:500 \
  --output test_data.json

# Use different locale (Vietnamese)
python scripts/generate_fixtures.py \
  --template elios-interview \
  --locale vi_VN \
  --output vietnamese_data.json \
  --pretty

# Japanese locale
python scripts/generate_fixtures.py \
  --template blog \
  --locale ja_JP \
  --output japanese_blog_data.json
```

**Available Templates:**
- `elios-interview` - Candidates, Questions, Interview Sessions (Elios-specific)
- `blog` - Users, Posts
- More templates can be added to the script

**Supported Locales:**
- `en_US` - English (United States) - Default
- `vi_VN` - Vietnamese (Vietnam) - **Includes Vietnamese universities, degrees, majors**
- `ja_JP` - Japanese (Japan)
- `fr_FR` - French (France)
- `en_GB` - English (United Kingdom)
- And 50+ more locales supported by Faker

#### `inspect_schema.py` ⭐ NEW
**Automatically inspects database schema and generates seeding helpers.**

**Features:**
- Discovers all tables/collections automatically
- Analyzes column types (VARCHAR, INTEGER, DATE, JSONB, etc.)
- Identifies foreign key relationships
- Generates appropriate Faker methods for each field type
- Creates ready-to-use factory functions
- Creates JSON fixture templates with sample data
- **Works with ANY database schema** - No hardcoded assumptions!

**Usage:**
```bash
# Print schema summary
python scripts/inspect_schema.py \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/mydb"

# Generate factory functions for all tables
python scripts/inspect_schema.py \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/mydb" \
  --generate-factories
# Output: generated_factories.py

# Generate JSON fixture templates
python scripts/inspect_schema.py \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/mydb" \
  --generate-fixtures \
  --fixture-count 5
# Output: generated_fixtures.json

# Generate both
python scripts/inspect_schema.py \
  --db sqlite \
  --connection "sqlite:///./test.db" \
  --generate-factories \
  --generate-fixtures

# Save schema info as JSON
python scripts/inspect_schema.py \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/mydb" \
  --output schema_info.json
```

**Smart Field Detection:**
The script intelligently detects field types and generates appropriate Faker methods:
- `email` field → `fake.email()`
- `phone` field → `fake.phone_number()`
- `address` field → `fake.address()`
- `first_name` field → `fake.first_name()`
- `description` field → `fake.paragraph()`
- `created_at` (TIMESTAMP) → `fake.date_time_between()`
- Integer types → `fake.random_int()`
- Boolean types → `fake.boolean()`
- And many more patterns...

**Example Output:**
```python
# generated_factories.py (auto-generated)

def candidate_factory(fake, index):
    """Factory for candidate model"""
    return {
        'full_name': fake.name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'years_of_experience': fake.random_int(min=1, max=1000),
        'skills': {},  # JSON field
        'created_at': fake.date_time_between(start_date='-1y', end_date='now'),
        'status': fake.word(),
    }
```

### References (`references/`)

#### `database-configs.md`
Comprehensive database connection patterns and configuration examples.

**Contents:**
- Connection string formats for all supported databases
- Environment variable patterns
- Configuration file examples (`.env`, `settings.py`, `config.yaml`)
- Docker Compose configurations
- Security best practices
- Common issues and solutions

**Use when:**
- Setting up database connections
- Troubleshooting connection errors
- Configuring different environments (dev, staging, prod)

#### `faker-recipes.md`
Common patterns and examples for generating realistic fake data with Faker.

**Contents:**
- Personal information (names, emails, addresses)
- Business data (companies, jobs)
- Technical data (URLs, IPs, UUIDs)
- Dates and times
- Text generation
- Numbers and sequences
- Localization
- Custom providers
- Database-specific factory patterns

**Use when:**
- Creating custom factory functions
- Need inspiration for data generation
- Understanding Faker capabilities
- Creating project-specific data generators

#### `orm-patterns.md`
Patterns and best practices for seeding databases using various ORMs.

**Contents:**
- **SQLAlchemy** - Setup, batch operations, relationships, error handling, factories
- **Django ORM** - Models, bulk operations, management commands
- **Prisma** (TypeScript) - Seeding scripts, relations
- **MongoDB** (PyMongo) - Document insertion, embedded docs, references
- Best practices (transactions, idempotency, constraints, progress reporting)

**Use when:**
- Implementing ORM-specific seeding
- Need examples for your ORM
- Understanding relationship seeding (one-to-many, many-to-many)
- Creating production-grade seeding scripts

### Assets (`assets/`)

#### `seed-config-template.yaml`
Template for YAML-based seeding configuration.

**Features:**
- Database connection configuration
- Faker settings (locale, seed for reproducibility)
- Model definitions with factory functions
- Seeding options (batch size, clear existing, idempotency)
- Post-seeding hooks

**Usage:**
```bash
# Copy template
cp assets/seed-config-template.yaml seed-config.yaml

# Edit configuration
# ... customize models, counts, factories ...

# Run seeding
python scripts/seed_database.py --config seed-config.yaml
```

#### `fixture-template.json`
Template for JSON test fixtures.

**Features:**
- Example structure for common models (User, Post)
- Elios-specific models (Candidate, Question, InterviewSession)
- Proper JSON formatting with relationships
- Nested data examples (embedded documents, foreign keys)

**Usage:**
```bash
# Copy and customize
cp assets/fixture-template.json fixtures/my_data.json

# Edit JSON file with your data
# ...

# Seed database
python scripts/seed_database.py \
  --fixtures fixtures/my_data.json \
  --db postgresql \
  --connection "postgresql://user:pass@localhost/db"
```

## Common Workflows

### Workflow 1: Quick Development Setup

Seed local database with sample data for immediate development:

```bash
# 1. Auto-detect database
python scripts/detect_db_config.py

# 2. Generate fixtures
python scripts/generate_fixtures.py \
  --template elios-interview \
  --output fixtures/dev_data.json

# 3. Seed database
python scripts/seed_database.py \
  --fixtures fixtures/dev_data.json \
  --db postgresql \
  --connection "postgresql://postgres:password@localhost/elios_dev"

# Verify
psql -d elios_dev -c "SELECT COUNT(*) FROM candidates;"
```

### Workflow 2: Test Fixture Creation

Create fixtures for automated testing:

```bash
# Generate small, focused test fixtures
python scripts/generate_fixtures.py \
  --models Candidate:10,Question:20,InterviewSession:5 \
  --output tests/fixtures/test_data.json \
  --pretty

# Use in tests:
# - Version control fixtures/test_data.json
# - Load in test setup
# - Consistent test data across CI/CD
```

### Workflow 3: Staging Environment Population

Populate staging with production-like data:

```bash
# 1. Generate large dataset
python scripts/generate_fixtures.py \
  --template elios-interview \
  --output fixtures/staging_data.json

# Manually increase counts in fixture file if needed

# 2. Detect staging database
python scripts/detect_db_config.py --env-file .env.staging

# 3. Seed staging
python scripts/seed_database.py \
  --fixtures fixtures/staging_data.json \
  --db postgresql \
  --connection "$STAGING_DATABASE_URL"
```

### Workflow 4: Database Migration Testing

Test migrations with seeded data:

```bash
# 1. Seed old schema
python scripts/seed_database.py --fixtures fixtures/old_schema.json

# 2. Run migrations
alembic upgrade head

# 3. Verify data integrity
python scripts/verify_migration.py

# 4. Seed new fields (if needed)
python scripts/seed_database.py --fixtures fixtures/new_fields.json
```

## Best Practices

### 1. Version Control Fixtures

Store fixtures in version control for consistency:

```bash
# Create fixtures directory
mkdir -p fixtures/{development,testing,staging}

# Generate and commit
python scripts/generate_fixtures.py \
  --template elios-interview \
  --output fixtures/development/base_data.json \
  --pretty

git add fixtures/
git commit -m "Add base development fixtures"
```

### 2. Use Reproducible Seeds

For consistent test data, use Faker seeds:

```python
from faker import Faker

# Set seed for reproducibility
Faker.seed(12345)
fake = Faker()

# Always generates same data
fake.name()  # Always "John Smith" (example)
```

### 3. Separate Seeding Scripts by Environment

```
scripts/
├── seed_development.py    # Small datasets for local dev
├── seed_testing.py         # Controlled fixtures for tests
├── seed_staging.py         # Large production-like datasets
└── seed_demo.py            # Curated demo data
```

### 4. Idempotent Seeding

Ensure seeding can be run multiple times safely:

```python
def seed_users(session, count=100):
    # Check if already seeded
    existing_count = session.query(User).count()
    if existing_count >= count:
        print(f"Already seeded with {existing_count} users, skipping...")
        return

    # Seed remaining
    remaining = count - existing_count
    # ... create users ...
```

### 5. Progress Reporting for Large Datasets

```python
# Batch insertions with progress
batch_size = 1000
for i in range(0, count, batch_size):
    # ... create batch ...
    print(f"Progress: {i}/{count} ({(i/count)*100:.1f}%)")
```

## Dependencies

### Required
- **Python 3.8+**
- **Faker** (`pip install faker`)

### Optional (based on database)
- **SQLAlchemy** (`pip install sqlalchemy`) - For PostgreSQL, MySQL, SQLite
- **psycopg2** (`pip install psycopg2-binary`) - PostgreSQL driver
- **pymysql** (`pip install pymysql`) - MySQL driver
- **pymongo** (`pip install pymongo`) - MongoDB driver
- **PyYAML** (`pip install pyyaml`) - For YAML config support

### Installation

```bash
# Install core dependencies
pip install faker pyyaml

# Install database drivers (choose based on your database)
pip install sqlalchemy psycopg2-binary  # PostgreSQL
pip install sqlalchemy pymysql          # MySQL
pip install pymongo                     # MongoDB
```

## Troubleshooting

### Issue: "Faker not installed"
```
Error: Faker library not installed
```
**Solution:**
```bash
pip install faker
```

### Issue: Database connection refused
```
Error: connection refused
```
**Solutions:**
1. Check if database is running
2. Verify connection string (host, port, credentials)
3. Check firewall settings
4. Refer to `references/database-configs.md` for detailed troubleshooting

### Issue: Unique constraint violation
```
Error: duplicate key value violates unique constraint
```
**Solutions:**
1. Clear database before seeding: `session.query(Model).delete()`
2. Use idempotent seeding (check existing records)
3. Generate unique values with Faker

### Issue: Foreign key constraint violation
```
Error: foreign key constraint fails
```
**Solutions:**
1. Seed in correct order (parent models before children)
2. Use actual existing IDs for foreign keys
3. Store created records for reference: `created_users = [...]; post.author_id = random.choice([u.id for u in created_users])`

### Issue: Out of memory for large datasets
```
Error: MemoryError
```
**Solutions:**
1. Use batch insertions with commits: `session.flush()` every N records
2. Reduce batch size
3. Stream data instead of loading all in memory

## Advanced Usage

### Custom Faker Provider

Create domain-specific providers:

```python
from faker import Faker
from faker.providers import BaseProvider

class InterviewProvider(BaseProvider):
    def interview_status(self):
        return self.random_element(['pending', 'scheduled', 'completed', 'cancelled'])

    def skill_level(self):
        return self.random_element(['beginner', 'intermediate', 'advanced', 'expert'])

    def programming_language(self):
        return self.random_element(['Python', 'JavaScript', 'Java', 'C++', 'Go'])

fake = Faker()
fake.add_provider(InterviewProvider)

# Use custom methods
candidate = {
    'skill_level': fake.skill_level(),
    'primary_language': fake.programming_language(),
}
```

### Multi-Locale Data Generation

Generate international test data:

```python
from faker import Faker

# Create multiple locales
fake_us = Faker('en_US')
fake_jp = Faker('ja_JP')
fake_fr = Faker('fr_FR')

users = [
    {'name': fake_us.name(), 'address': fake_us.address()},
    {'name': fake_jp.name(), 'address': fake_jp.address()},
    {'name': fake_fr.name(), 'address': fake_fr.address()},
]
```

### Seeding with Relationships

Handle complex relationships:

```python
# One-to-Many
author = User(username=fake.user_name())
session.add(author)
session.flush()  # Get author.id

posts = [
    Post(title=fake.sentence(), author_id=author.id)
    for _ in range(10)
]
session.add_all(posts)

# Many-to-Many
skills = [Skill(name=name) for name in ['Python', 'JavaScript', 'SQL']]
session.add_all(skills)
session.flush()

candidate = Candidate(full_name=fake.name())
candidate.skills.extend(random.sample(skills, k=2))
session.add(candidate)

session.commit()
```

## Examples

### Example 1: Seed Elios Interview System

```bash
# Generate Elios-specific fixtures
python scripts/generate_fixtures.py \
  --template elios-interview \
  --output fixtures/elios_dev.json \
  --pretty

# Seed database
python scripts/seed_database.py \
  --fixtures fixtures/elios_dev.json \
  --db postgresql \
  --connection "postgresql://postgres:password@localhost/elios_dev"

# Verify
psql -d elios_dev -c "SELECT COUNT(*) FROM candidates;"
psql -d elios_dev -c "SELECT COUNT(*) FROM questions;"
psql -d elios_dev -c "SELECT COUNT(*) FROM interview_sessions;"
```

### Example 2: Create Test Fixtures for CI/CD

```bash
# Generate small, controlled fixtures
python scripts/generate_fixtures.py \
  --models Candidate:5,Question:10 \
  --output tests/fixtures/ci_test_data.json \
  --pretty

# In CI pipeline:
python scripts/seed_database.py \
  --fixtures tests/fixtures/ci_test_data.json \
  --db sqlite \
  --connection "sqlite:///:memory:"

# Run tests with seeded data
pytest tests/
```

### Example 3: Generate Vietnamese Test Data

```bash
# Generate Vietnamese fixtures for Elios
python scripts/generate_fixtures.py \
  --template elios-interview \
  --locale vi_VN \
  --output fixtures/elios_vietnamese.json \
  --pretty

# Seed database
python scripts/seed_database.py \
  --fixtures fixtures/elios_vietnamese.json \
  --db postgresql \
  --connection "postgresql://postgres:password@localhost/elios_dev"

# Verify Vietnamese data
psql -d elios_dev -c "SELECT full_name, education->>'university' as university FROM candidates LIMIT 5;"
```

**Expected output:**
```
        full_name        |          university
-------------------------+-------------------------------
 Nguyễn Văn Minh         | Đại học Bách Khoa Hà Nội
 Trần Thị Hương          | Đại học FPT
 Lê Minh Tuấn            | Đại học Quốc gia Hà Nội
 Phạm Thị Lan            | Đại học Công nghệ
 Hoàng Văn Nam           | Đại học Bách Khoa TP.HCM
```

### Example 4: Custom Factory Script

```python
# scripts/seed_custom.py

from seed_database import create_seeder
from faker import Faker

fake = Faker()

def advanced_candidate_factory(fake, index):
    """Generate realistic interview candidates"""
    skills_by_role = {
        'frontend': ['JavaScript', 'React', 'CSS', 'HTML', 'Vue'],
        'backend': ['Python', 'Django', 'FastAPI', 'SQL', 'Docker'],
        'fullstack': ['JavaScript', 'React', 'Python', 'SQL', 'AWS'],
        'data': ['Python', 'Pandas', 'SQL', 'Machine Learning', 'Statistics'],
    }

    role = fake.random_element(list(skills_by_role.keys()))
    skills = fake.random_elements(
        skills_by_role[role],
        length=fake.random_int(min=3, max=5),
        unique=True
    )

    return {
        'full_name': fake.name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'years_of_experience': fake.random_int(min=0, max=15),
        'skills': list(skills),
        'desired_role': role,
        'expected_salary': fake.random_int(min=50000, max=200000),
        'created_at': fake.date_time_between(start_date='-6m', end_date='now'),
    }

# Run seeding
seeder = create_seeder('postgresql', 'postgresql://user:pass@localhost/db')
candidates = seeder.seed_model(Candidate, count=100, factory_func=advanced_candidate_factory)
print(f"✓ Created {len(candidates)} candidates")
```

## Integration with Development Workflow

### Docker Compose Integration

Add seeding to Docker Compose setup:

```yaml
# docker-compose.yml

version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: elios_dev
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"

  seeder:
    build: .
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/elios_dev
    command: >
      sh -c "
        sleep 5 &&
        python scripts/generate_fixtures.py --template elios-interview --output /tmp/fixtures.json &&
        python scripts/seed_database.py --fixtures /tmp/fixtures.json --db postgresql --connection $$DATABASE_URL
      "
```

### Makefile Integration

```makefile
# Makefile

.PHONY: seed seed-dev seed-test

seed-dev:
	python scripts/generate_fixtures.py --template elios-interview --output fixtures/dev.json
	python scripts/seed_database.py --fixtures fixtures/dev.json --db postgresql --connection $(DATABASE_URL)

seed-test:
	python scripts/generate_fixtures.py --models Candidate:10,Question:20 --output tests/fixtures/test.json
	python scripts/seed_database.py --fixtures tests/fixtures/test.json --db sqlite --connection "sqlite:///:memory:"

seed-staging:
	python scripts/detect_db_config.py --env-file .env.staging
	python scripts/seed_database.py --fixtures fixtures/staging.json --db postgresql --connection $(STAGING_DATABASE_URL)
```

Usage:
```bash
make seed-dev
make seed-test
make seed-staging
```

## Summary

This skill provides a complete database seeding solution:

1. **Auto-detection** - Automatically finds database configuration
2. **Multiple approaches** - Fixtures, factories, or configuration-based
3. **Comprehensive references** - Database configs, Faker recipes, ORM patterns
4. **Ready-to-use templates** - JSON fixtures and YAML configs
5. **Production-ready scripts** - Batch operations, error handling, progress reporting

Use the skill whenever you need to populate databases with realistic test data efficiently.
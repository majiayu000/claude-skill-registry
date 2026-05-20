---
name: data-seeding
description: Create database seed scripts with realistic test data for development and testing. Use when setting up development environment or creating demo data.
allowed-tools: Read, Write, Edit, Bash
---

You create database seed scripts with realistic test data for the QA Team Portal.

## When to Use

- Setting up development environment
- Creating demo data for presentations
- Populating test database
- UAT environment setup
- Resetting database to known state

## Implementation

### 1. Seed Data Script

**Location:** `backend/app/db/seed.py`

```python
import asyncio
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.models.team_member import TeamMember
from app.models.update import Update
from app.models.tool import Tool, ToolCategory
from app.models.resource import Resource
from app.models.research import Research
from app.core.security import get_password_hash
from datetime import datetime, timedelta
import random

async def seed_users(db: Session):
    """Seed initial users."""
    print("Seeding users...")

    users_data = [
        {
            "email": "admin@evoketech.com",
            "password_hash": get_password_hash("Admin123!@#"),
            "name": "Admin User",
            "role": "admin",
            "status": "active"
        },
        {
            "email": "lead@evoketech.com",
            "password_hash": get_password_hash("Lead123!@#"),
            "name": "QA Lead",
            "role": "lead",
            "status": "active"
        },
        {
            "email": "member@evoketech.com",
            "password_hash": get_password_hash("Member123!@#"),
            "name": "QA Member",
            "role": "member",
            "status": "active"
        }
    ]

    for user_data in users_data:
        # Check if user already exists
        existing = db.query(User).filter(User.email == user_data["email"]).first()
        if not existing:
            user = User(**user_data)
            db.add(user)
            print(f"  ✓ Created user: {user_data['email']}")

    db.commit()
    print("Users seeded successfully!\n")

async def seed_team_members(db: Session):
    """Seed team members."""
    print("Seeding team members...")

    team_members_data = [
        {
            "name": "Sarah Johnson",
            "role": "Senior QA Engineer",
            "email": "sarah.johnson@evoketech.com",
            "bio": "10+ years of experience in software testing and quality assurance. Specialized in automation testing and performance optimization.",
            "photo_url": "https://i.pravatar.cc/300?img=1"
        },
        {
            "name": "Michael Chen",
            "role": "QA Automation Lead",
            "email": "michael.chen@evoketech.com",
            "bio": "Expert in test automation frameworks including Selenium, Playwright, and Cypress. Passionate about CI/CD integration.",
            "photo_url": "https://i.pravatar.cc/300?img=12"
        },
        {
            "name": "Emily Rodriguez",
            "role": "QA Engineer",
            "email": "emily.rodriguez@evoketech.com",
            "bio": "Focused on mobile app testing and API testing. Strong background in manual and exploratory testing.",
            "photo_url": "https://i.pravatar.cc/300?img=5"
        },
        {
            "name": "David Kim",
            "role": "Performance Testing Specialist",
            "email": "david.kim@evoketech.com",
            "bio": "Specialized in load testing, stress testing, and performance optimization. JMeter and Gatling expert.",
            "photo_url": "https://i.pravatar.cc/300?img=14"
        },
        {
            "name": "Jennifer Taylor",
            "role": "QA Engineer",
            "email": "jennifer.taylor@evoketech.com",
            "bio": "Security testing and accessibility testing advocate. WCAG 2.1 AA compliance specialist.",
            "photo_url": "https://i.pravatar.cc/300?img=9"
        },
        {
            "name": "Alex Patel",
            "role": "Junior QA Engineer",
            "email": "alex.patel@evoketech.com",
            "bio": "Recent graduate with a passion for quality assurance. Learning automation testing and best practices.",
            "photo_url": "https://i.pravatar.cc/300?img=33"
        }
    ]

    for member_data in team_members_data:
        existing = db.query(TeamMember).filter(TeamMember.email == member_data["email"]).first()
        if not existing:
            member = TeamMember(**member_data)
            db.add(member)
            print(f"  ✓ Created team member: {member_data['name']}")

    db.commit()
    print("Team members seeded successfully!\n")

async def seed_updates(db: Session):
    """Seed latest updates."""
    print("Seeding updates...")

    updates_data = [
        {
            "title": "New Test Automation Framework Released",
            "content": "We've released a new test automation framework based on Playwright. It supports cross-browser testing and provides better performance.",
            "priority": "high"
        },
        {
            "title": "Weekly QA Sync Meeting - Friday 3 PM",
            "content": "Join us for our weekly sync meeting to discuss ongoing projects, blockers, and upcoming tasks.",
            "priority": "medium"
        },
        {
            "title": "Security Testing Training Next Week",
            "content": "Attend our security testing training session covering OWASP Top 10 and penetration testing basics.",
            "priority": "high"
        },
        {
            "title": "Q4 Performance Testing Complete",
            "content": "All Q4 performance testing has been completed. Results show 15% improvement in API response times.",
            "priority": "low"
        },
        {
            "title": "New Team Members Onboarding",
            "content": "Welcome our new team members! Onboarding sessions scheduled for next Monday and Tuesday.",
            "priority": "medium"
        }
    ]

    for i, update_data in enumerate(updates_data):
        # Add timestamps (newest first)
        update_data["created_at"] = datetime.utcnow() - timedelta(days=i)
        update = Update(**update_data)
        db.add(update)
        print(f"  ✓ Created update: {update_data['title']}")

    db.commit()
    print("Updates seeded successfully!\n")

async def seed_tools(db: Session):
    """Seed QA tools."""
    print("Seeding tools...")

    # Create categories first
    categories_data = [
        {"name": "Test Automation", "description": "Automated testing tools and frameworks"},
        {"name": "Performance Testing", "description": "Load and performance testing tools"},
        {"name": "API Testing", "description": "Tools for testing REST APIs and web services"},
        {"name": "Mobile Testing", "description": "Mobile app testing tools"},
        {"name": "Security Testing", "description": "Security and penetration testing tools"},
        {"name": "Code Quality", "description": "Code analysis and quality tools"}
    ]

    categories = {}
    for cat_data in categories_data:
        existing = db.query(ToolCategory).filter(ToolCategory.name == cat_data["name"]).first()
        if not existing:
            category = ToolCategory(**cat_data)
            db.add(category)
            db.flush()
            categories[cat_data["name"]] = category.id
            print(f"  ✓ Created category: {cat_data['name']}")
        else:
            categories[cat_data["name"]] = existing.id

    db.commit()

    # Create tools
    tools_data = [
        {
            "name": "Playwright",
            "description": "Modern end-to-end testing framework for web applications. Supports all major browsers.",
            "category_id": categories["Test Automation"],
            "download_url": "https://playwright.dev/",
            "version": "1.40.0",
            "documentation_url": "https://playwright.dev/docs/intro"
        },
        {
            "name": "Selenium WebDriver",
            "description": "Popular browser automation tool for web application testing.",
            "category_id": categories["Test Automation"],
            "download_url": "https://www.selenium.dev/",
            "version": "4.15.0",
            "documentation_url": "https://www.selenium.dev/documentation/"
        },
        {
            "name": "JMeter",
            "description": "Load testing and performance measurement tool.",
            "category_id": categories["Performance Testing"],
            "download_url": "https://jmeter.apache.org/",
            "version": "5.6.2",
            "documentation_url": "https://jmeter.apache.org/usermanual/index.html"
        },
        {
            "name": "Postman",
            "description": "Comprehensive API testing and development platform.",
            "category_id": categories["API Testing"],
            "download_url": "https://www.postman.com/",
            "version": "10.19.0",
            "documentation_url": "https://learning.postman.com/docs/"
        },
        {
            "name": "Appium",
            "description": "Mobile app automation framework for iOS and Android.",
            "category_id": categories["Mobile Testing"],
            "download_url": "https://appium.io/",
            "version": "2.2.1",
            "documentation_url": "https://appium.io/docs/en/latest/"
        },
        {
            "name": "OWASP ZAP",
            "description": "Open-source web application security scanner.",
            "category_id": categories["Security Testing"],
            "download_url": "https://www.zaproxy.org/",
            "version": "2.14.0",
            "documentation_url": "https://www.zaproxy.org/docs/"
        },
        {
            "name": "SonarQube",
            "description": "Code quality and security analysis platform.",
            "category_id": categories["Code Quality"],
            "download_url": "https://www.sonarsource.com/products/sonarqube/",
            "version": "10.3",
            "documentation_url": "https://docs.sonarsource.com/sonarqube/latest/"
        },
        {
            "name": "K6",
            "description": "Modern load testing tool for developers.",
            "category_id": categories["Performance Testing"],
            "download_url": "https://k6.io/",
            "version": "0.47.0",
            "documentation_url": "https://k6.io/docs/"
        }
    ]

    for tool_data in tools_data:
        existing = db.query(Tool).filter(Tool.name == tool_data["name"]).first()
        if not existing:
            tool = Tool(**tool_data)
            db.add(tool)
            print(f"  ✓ Created tool: {tool_data['name']}")

    db.commit()
    print("Tools seeded successfully!\n")

async def seed_resources(db: Session):
    """Seed resources."""
    print("Seeding resources...")

    resources_data = [
        {
            "title": "QA Best Practices Guide 2024",
            "description": "Comprehensive guide covering modern QA best practices, testing strategies, and methodologies.",
            "url": "https://example.com/qa-guide.pdf",
            "type": "PDF",
            "tags": ["best practices", "guide", "methodology"]
        },
        {
            "title": "Test Automation Tutorial Series",
            "description": "Step-by-step video tutorials on test automation using Playwright and Selenium.",
            "url": "https://example.com/tutorials",
            "type": "Video",
            "tags": ["automation", "tutorial", "playwright", "selenium"]
        },
        {
            "title": "API Testing Checklist",
            "description": "Complete checklist for API testing including functional, security, and performance tests.",
            "url": "https://example.com/api-checklist.pdf",
            "type": "Checklist",
            "tags": ["API", "checklist", "testing"]
        },
        {
            "title": "Performance Testing Handbook",
            "description": "In-depth handbook covering load testing, stress testing, and performance optimization.",
            "url": "https://example.com/performance-handbook.pdf",
            "type": "PDF",
            "tags": ["performance", "load testing", "optimization"]
        },
        {
            "title": "Mobile Testing Guide",
            "description": "Guide to testing mobile applications on iOS and Android platforms.",
            "url": "https://example.com/mobile-guide.pdf",
            "type": "PDF",
            "tags": ["mobile", "iOS", "Android"]
        }
    ]

    for resource_data in resources_data:
        existing = db.query(Resource).filter(Resource.title == resource_data["title"]).first()
        if not existing:
            resource = Resource(**resource_data)
            db.add(resource)
            print(f"  ✓ Created resource: {resource_data['title']}")

    db.commit()
    print("Resources seeded successfully!\n")

async def seed_research(db: Session):
    """Seed research articles."""
    print("Seeding research...")

    research_data = [
        {
            "title": "Impact of AI on Software Testing",
            "summary": "Analysis of how artificial intelligence and machine learning are transforming software testing practices.",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. AI-powered testing tools are revolutionizing the QA industry...",
            "author": "Sarah Johnson",
            "published_date": datetime.utcnow() - timedelta(days=7),
            "tags": ["AI", "machine learning", "automation"]
        },
        {
            "title": "Shift-Left Testing: A Case Study",
            "summary": "Real-world case study on implementing shift-left testing methodology in large-scale projects.",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Shift-left testing has proven to reduce defects by 40%...",
            "author": "Michael Chen",
            "published_date": datetime.utcnow() - timedelta(days=14),
            "tags": ["shift-left", "methodology", "case study"]
        },
        {
            "title": "Mobile App Testing Best Practices",
            "summary": "Comprehensive guide to mobile app testing covering iOS, Android, and cross-platform frameworks.",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mobile testing requires special considerations...",
            "author": "Emily Rodriguez",
            "published_date": datetime.utcnow() - timedelta(days=21),
            "tags": ["mobile", "best practices", "cross-platform"]
        }
    ]

    for article_data in research_data:
        existing = db.query(Research).filter(Research.title == article_data["title"]).first()
        if not existing:
            article = Research(**article_data)
            db.add(article)
            print(f"  ✓ Created research: {article_data['title']}")

    db.commit()
    print("Research seeded successfully!\n")

async def seed_all():
    """Seed all data."""
    print("=" * 60)
    print("Starting database seeding...")
    print("=" * 60 + "\n")

    db = SessionLocal()
    try:
        await seed_users(db)
        await seed_team_members(db)
        await seed_updates(db)
        await seed_tools(db)
        await seed_resources(db)
        await seed_research(db)

        print("=" * 60)
        print("✅ Database seeding completed successfully!")
        print("=" * 60)

        print("\n📝 Test Credentials:")
        print("  Admin:  admin@evoketech.com / Admin123!@#")
        print("  Lead:   lead@evoketech.com / Lead123!@#")
        print("  Member: member@evoketech.com / Member123!@#")

    except Exception as e:
        print(f"\n❌ Error during seeding: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(seed_all())
```

### 2. Reset Database Script

**Location:** `backend/app/db/reset.py`

```python
import asyncio
from sqlalchemy import text
from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.db.seed import seed_all

async def reset_database():
    """Drop all tables, recreate them, and seed data."""
    print("=" * 60)
    print("⚠️  WARNING: This will delete all data!")
    print("=" * 60)

    response = input("Are you sure you want to reset the database? (yes/no): ")
    if response.lower() != "yes":
        print("❌ Database reset cancelled.")
        return

    print("\n🗑️  Dropping all tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("✅ All tables dropped.\n")

    print("📦 Creating all tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ All tables created.\n")

    print("🌱 Seeding database...")
    await seed_all()

    print("\n✅ Database reset complete!")

if __name__ == "__main__":
    asyncio.run(reset_database())
```

### 3. Faker for Realistic Data (Optional)

```bash
cd backend
uv pip install faker
```

```python
# backend/app/db/seed_faker.py
from faker import Faker
import random

fake = Faker()

async def seed_realistic_data(db: Session, count: int = 50):
    """Seed realistic data using Faker."""
    print(f"Generating {count} realistic team members...")

    for i in range(count):
        member = TeamMember(
            name=fake.name(),
            role=random.choice([
                "QA Engineer",
                "Senior QA Engineer",
                "QA Lead",
                "Automation Engineer",
                "Performance Tester"
            ]),
            email=fake.email(),
            bio=fake.paragraph(nb_sentences=3),
            photo_url=f"https://i.pravatar.cc/300?img={random.randint(1, 70)}"
        )
        db.add(member)

        if (i + 1) % 10 == 0:
            print(f"  Created {i + 1}/{count} members...")

    db.commit()
    print(f"✅ {count} team members created!\n")
```

### 4. CLI Commands

```bash
# Run seed script
cd backend
python -m app.db.seed

# Reset database
python -m app.db.reset

# Run migrations + seed
alembic upgrade head && python -m app.db.seed
```

### 5. Make Script

**Location:** `Makefile`

```makefile
.PHONY: seed reset-db setup-dev

seed:
	@echo "Seeding database..."
	cd backend && python -m app.db.seed

reset-db:
	@echo "Resetting database..."
	cd backend && python -m app.db.reset

setup-dev:
	@echo "Setting up development environment..."
	@echo "1. Installing dependencies..."
	cd backend && uv sync
	cd frontend && npm install
	@echo "2. Running migrations..."
	cd backend && alembic upgrade head
	@echo "3. Seeding database..."
	cd backend && python -m app.db.seed
	@echo "✅ Development environment ready!"

migrate:
	@echo "Running database migrations..."
	cd backend && alembic upgrade head
```

**Usage:**

```bash
# Seed database
make seed

# Reset and seed
make reset-db

# Full dev setup
make setup-dev
```

### 6. Seed Data in Tests

```python
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.seed import seed_users, seed_team_members

TEST_DATABASE_URL = "postgresql://test:test@localhost:5432/test_qa_portal"

@pytest.fixture(scope="session")
def test_db():
    """Create test database and seed initial data."""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    # Seed test data
    import asyncio
    asyncio.run(seed_users(db))
    asyncio.run(seed_team_members(db))

    yield db

    db.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def db(test_db):
    """Provide a clean database for each test."""
    test_db.begin_nested()
    yield test_db
    test_db.rollback()
```

### 7. Environment-Specific Seeding

```python
# backend/app/db/seed.py
import os
from app.core.config import settings

async def seed_all():
    """Seed data based on environment."""
    db = SessionLocal()

    try:
        # Always seed users
        await seed_users(db)

        # Seed sample data in dev/staging only
        if settings.ENVIRONMENT in ["development", "staging"]:
            print("📝 Development/Staging environment detected")
            print("   Seeding sample data...\n")

            await seed_team_members(db)
            await seed_updates(db)
            await seed_tools(db)
            await seed_resources(db)
            await seed_research(db)
        else:
            print("🚫 Production environment detected")
            print("   Skipping sample data seeding.\n")

    finally:
        db.close()
```

## Seed Data Best Practices

1. **Idempotent Seeds**: Check if data exists before inserting
2. **Realistic Data**: Use realistic names, emails, dates
3. **Relationships**: Maintain referential integrity
4. **Timestamps**: Use appropriate dates (recent for updates)
5. **Passwords**: Use strong test passwords, document them
6. **Environment-Aware**: Don't seed demo data in production
7. **Version Control**: Keep seed scripts in version control
8. **Documentation**: Document test credentials clearly

## Testing Seed Scripts

```python
# tests/test_seed.py
import pytest
from app.db.seed import seed_users, seed_team_members

@pytest.mark.asyncio
async def test_seed_users(db):
    """Test user seeding."""
    await seed_users(db)

    # Check users created
    users = db.query(User).all()
    assert len(users) >= 3

    # Check admin user
    admin = db.query(User).filter(User.role == "admin").first()
    assert admin is not None
    assert admin.email == "admin@evoketech.com"

@pytest.mark.asyncio
async def test_seed_team_members(db):
    """Test team member seeding."""
    await seed_team_members(db)

    # Check team members created
    members = db.query(TeamMember).all()
    assert len(members) >= 6

    # Check required fields
    for member in members:
        assert member.name
        assert member.email
        assert member.role
```

## Troubleshooting

**Foreign key constraint errors:**
- Ensure parent records created before children
- Check relationship setup in models
- Seed in correct order (users → team members → content)

**Duplicate key errors:**
- Check for existing data before insert
- Use `get_or_create` pattern
- Clear database before reseeding

**Slow seeding:**
- Use bulk inserts for large datasets
- Commit in batches (every 100 records)
- Disable indexes temporarily for large seeds

## Report

✅ Seed script created with realistic data
✅ Users seeded (admin, lead, member)
✅ Team members seeded (6 members)
✅ Updates seeded (5 recent updates)
✅ Tools seeded (8 tools across 6 categories)
✅ Resources seeded (5 resources)
✅ Research seeded (3 articles)
✅ Reset script created
✅ Makefile commands added
✅ Environment-aware seeding implemented
✅ Test credentials documented
✅ Idempotent seeds (checks for existing data)

---
name: magento-model-developer
description: Designs and implements data layer architecture for Magento 2. Use when creating data models, designing database schemas, implementing repositories, or working with EAV/flat table structures. Masters entity design, repository patterns, collections, and database optimization.
---

# Magento 2 Model Developer

Expert specialist in designing and implementing robust data layer architectures, creating efficient, scalable data models that serve as the foundation for enterprise e-commerce applications.

## When to Use

- Creating data models and entities
- Designing database schemas
- Implementing repository patterns
- Working with EAV or flat table structures
- Optimizing database queries
- Building data collections

## Data Architecture

- **Model Design**: Create efficient entity models following Magento patterns
- **EAV vs Flat Tables**: Choose optimal data storage strategies for different scenarios
- **Repository Pattern**: Implement clean data access layers and service contracts
- **Collection Optimization**: Build high-performance data collections and queries
- **Database Schema Design**: Design normalized, efficient database structures

## Model Development Process

### 1. Data Requirements Analysis
- **Business Requirements**: Understand entity relationships and business rules
- **Performance Requirements**: Plan for expected data volume and query patterns
- **Storage Strategy**: Choose between EAV and flat table storage approaches
- **Relationship Mapping**: Design entity relationships and dependencies
- **Scalability Planning**: Plan for future growth and data expansion

### 2. Database Schema Design
- **Table Structure**: Design efficient table structures and relationships
- **Data Types**: Choose appropriate data types for optimal storage and performance
- **Indexing Strategy**: Plan indexes for search, sorting, and filtering operations
- **Constraints**: Implement proper database constraints and validation
- **Migration Scripts**: Create database migration and upgrade scripts

### 3. Model Implementation
- **Entity Classes**: Implement model classes with proper validation and logic
- **Resource Models**: Create efficient database interaction layers
- **Collection Development**: Build optimized collection classes with filtering
- **Repository Implementation**: Create repository classes following service contracts
- **Factory Classes**: Implement proper object factories and builders

### 4. Integration & Testing
- **API Integration**: Integrate models with REST and GraphQL APIs
- **Cache Integration**: Implement proper caching strategies for model data
- **Performance Testing**: Validate model performance under expected load
- **Data Validation**: Test data integrity and validation rules
- **Migration Testing**: Test database migrations and data consistency

## Model Types

### Entity Model
```php
<?php

declare(strict_types=1);

namespace Vendor\Module\Model;

use Magento\Framework\Model\AbstractModel;
use Vendor\Module\Model\ResourceModel\Entity as ResourceModel;

class Entity extends AbstractModel
{
    protected function _construct(): void
    {
        $this->_init(ResourceModel::class);
    }
}
```

### Resource Model
```php
<?php

declare(strict_types=1);

namespace Vendor\Module\Model\ResourceModel;

use Magento\Framework\Model\ResourceModel\Db\AbstractDb;

class Entity extends AbstractDb
{
    protected function _construct(): void
    {
        $this->_init('vendor_module_entity', 'entity_id');
    }
}
```

### Collection
```php
<?php

declare(strict_types=1);

namespace Vendor\Module\Model\ResourceModel\Entity;

use Magento\Framework\Model\ResourceModel\Db\Collection\AbstractCollection;
use Vendor\Module\Model\Entity;
use Vendor\Module\Model\ResourceModel\Entity as ResourceModel;

class Collection extends AbstractCollection
{
    protected function _construct(): void
    {
        $this->_init(Entity::class, ResourceModel::class);
    }
}
```

### Repository Implementation
```php
<?php

declare(strict_types=1);

namespace Vendor\Module\Model;

use Vendor\Module\Api\Data\EntityInterface;
use Vendor\Module\Api\EntityRepositoryInterface;
use Vendor\Module\Model\ResourceModel\Entity as ResourceModel;
use Magento\Framework\Exception\NoSuchEntityException;

class EntityRepository implements EntityRepositoryInterface
{
    /**
     * @param ResourceModel $resource
     */
    public function __construct(
        private readonly ResourceModel $resource
    ) {
    }

    /**
     * @param int $id
     * @return EntityInterface
     * @throws NoSuchEntityException
     */
    public function getById(int $id): EntityInterface
    {
        $entity = $this->resource->load($id);
        if (!$entity->getId()) {
            throw new NoSuchEntityException(__('Entity with id "%1" does not exist.', $id));
        }
        return $entity;
    }
}
```

## Database Schema (db_schema.xml)

```xml
<?xml version="1.0"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xsi:noNamespaceSchemaLocation="urn:magento:framework:Setup/Declaration/Schema/etc/schema.xsd">
    <table name="vendor_module_entity" resource="default" engine="innodb" comment="Entity Table">
        <column xsi:type="int" name="entity_id" unsigned="true" nullable="false" identity="true" comment="Entity ID"/>
        <column xsi:type="varchar" name="name" length="255" nullable="false" comment="Name"/>
        <column xsi:type="timestamp" name="created_at" nullable="false" default="CURRENT_TIMESTAMP" comment="Created At"/>
        <constraint xsi:type="primary" referenceId="PRIMARY">
            <column name="entity_id"/>
        </constraint>
        <index referenceId="VENDOR_MODULE_ENTITY_NAME" indexType="btree">
            <column name="name"/>
        </index>
    </table>
</schema>
```

## EAV vs Flat Tables

### EAV (Entity-Attribute-Value)
- Use for entities with many optional attributes
- Flexible attribute management
- Higher query complexity
- Use for products, customers, categories

### Flat Tables
- Use for entities with fixed attributes
- Better query performance
- Simpler data model
- Use for orders, quotes, simple entities

## Best Practices

### Performance
- **Query Optimization**: Optimize database queries and eliminate N+1 problems
- **Index Strategy**: Design efficient database indexing
- **Collection Optimization**: Use proper filters and pagination
- **Lazy Loading**: Implement lazy loading for expensive operations
- **Caching**: Cache frequently accessed data

### Data Integrity
- **Validation**: Implement comprehensive data validation
- **Constraints**: Use database constraints where appropriate
- **Transactions**: Use transactions for multi-step operations
- **Referential Integrity**: Maintain proper foreign key relationships
- **Data Consistency**: Ensure data consistency across operations

### Code Quality
- **Service Contracts**: Use interfaces for repositories
- **Type Hints**: Use proper type hints throughout
- **Error Handling**: Comprehensive error handling
- **Documentation**: Document data models and relationships
- **Testing**: Write tests for models and repositories

## References

- [Adobe Commerce Models](https://developer.adobe.com/commerce/php/development/components/model/)
- [Repository Pattern](https://developer.adobe.com/commerce/php/development/components/repository-pattern/)
- [Database Schema](https://developer.adobe.com/commerce/php/development/components/declarative-schema/)

Focus on creating efficient, scalable data models that serve as a solid foundation for enterprise applications.

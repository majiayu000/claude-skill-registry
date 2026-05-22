---
name: unit-test-mapper-converter
description: Unit tests for mappers and converters (MapStruct, custom mappers). Test object transformation logic in isolation. Use when ensuring correct data transformation between DTOs and domain objects.
category: testing
tags: [junit-5, mapstruct, mapper, dto, entity, converter]
version: 1.0.1
---

# Unit Testing Mappers and Converters

Test MapStruct mappers and custom converter classes. Verify field mapping accuracy, null handling, type conversions, and nested object transformations.

## When to Use This Skill

Use this skill when:
- Testing MapStruct mapper implementations
- Testing custom entity-to-DTO converters
- Testing nested object mapping
- Verifying null handling in mappers
- Testing type conversions and transformations
- Want comprehensive mapping test coverage before integration tests

## Setup: Testing Mappers

### Maven
```xml
<dependency>
  <groupId>org.mapstruct</groupId>
  <artifactId>mapstruct</artifactId>
  <version>1.5.5.Final</version>
</dependency>
<dependency>
  <groupId>org.junit.jupiter</groupId>
  <artifactId>junit-jupiter</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.assertj</groupId>
  <artifactId>assertj-core</artifactId>
  <scope>test</scope>
</dependency>
```

### Gradle
```kotlin
dependencies {
  implementation("org.mapstruct:mapstruct:1.5.5.Final")
  testImplementation("org.junit.jupiter:junit-jupiter")
  testImplementation("org.assertj:assertj-core")
}
```

## Basic Pattern: Testing MapStruct Mapper

### Simple Entity to DTO Mapping

```java
// Mapper interface
@Mapper(componentModel = "spring")
public interface UserMapper {
  UserDto toDto(User user);
  User toEntity(UserDto dto);
  List<UserDto> toDtos(List<User> users);
}

// Unit test
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

class UserMapperTest {

  private final UserMapper userMapper = Mappers.getMapper(UserMapper.class);

  @Test
  void shouldMapUserToDto() {
    User user = new User(1L, "Alice", "alice@example.com", 25);
    
    UserDto dto = userMapper.toDto(user);
    
    assertThat(dto)
      .isNotNull()
      .extracting("id", "name", "email", "age")
      .containsExactly(1L, "Alice", "alice@example.com", 25);
  }

  @Test
  void shouldMapDtoToEntity() {
    UserDto dto = new UserDto(1L, "Alice", "alice@example.com", 25);
    
    User user = userMapper.toEntity(dto);
    
    assertThat(user)
      .isNotNull()
      .hasFieldOrPropertyWithValue("id", 1L)
      .hasFieldOrPropertyWithValue("name", "Alice");
  }

  @Test
  void shouldMapListOfUsers() {
    List<User> users = List.of(
      new User(1L, "Alice", "alice@example.com", 25),
      new User(2L, "Bob", "bob@example.com", 30)
    );
    
    List<UserDto> dtos = userMapper.toDtos(users);
    
    assertThat(dtos)
      .hasSize(2)
      .extracting(UserDto::getName)
      .containsExactly("Alice", "Bob");
  }

  @Test
  void shouldHandleNullEntity() {
    UserDto dto = userMapper.toDto(null);
    
    assertThat(dto).isNull();
  }
}
```

## Testing Nested Object Mapping

### Map Complex Hierarchies

```java
// Entities with nesting
class User {
  private Long id;
  private String name;
  private Address address;
  private List<Phone> phones;
}

// Mapper with nested mapping
@Mapper(componentModel = "spring")
public interface UserMapper {
  UserDto toDto(User user);
  User toEntity(UserDto dto);
}

// Unit test for nested objects
class NestedObjectMapperTest {

  private final UserMapper userMapper = Mappers.getMapper(UserMapper.class);

  @Test
  void shouldMapNestedAddress() {
    Address address = new Address("123 Main St", "New York", "NY", "10001");
    User user = new User(1L, "Alice", address);
    
    UserDto dto = userMapper.toDto(user);
    
    assertThat(dto.getAddress())
      .isNotNull()
      .hasFieldOrPropertyWithValue("street", "123 Main St")
      .hasFieldOrPropertyWithValue("city", "New York");
  }

  @Test
  void shouldMapListOfNestedPhones() {
    List<Phone> phones = List.of(
      new Phone("123-456-7890", "MOBILE"),
      new Phone("987-654-3210", "HOME")
    );
    User user = new User(1L, "Alice", null, phones);
    
    UserDto dto = userMapper.toDto(user);
    
    assertThat(dto.getPhones())
      .hasSize(2)
      .extracting(PhoneDto::getNumber)
      .containsExactly("123-456-7890", "987-654-3210");
  }

  @Test
  void shouldHandleNullNestedObjects() {
    User user = new User(1L, "Alice", null);
    
    UserDto dto = userMapper.toDto(user);
    
    assertThat(dto.getAddress()).isNull();
  }
}
```

## Testing Custom Mapping Methods

### Mapper with @Mapping Annotations

```java
@Mapper(componentModel = "spring")
public interface ProductMapper {
  @Mapping(source = "name", target = "productName")
  @Mapping(source = "price", target = "salePrice")
  @Mapping(target = "discount", expression = "java(product.getPrice() * 0.1)")
  ProductDto toDto(Product product);

  @Mapping(source = "productName", target = "name")
  @Mapping(source = "salePrice", target = "price")
  Product toEntity(ProductDto dto);
}

class CustomMappingTest {

  private final ProductMapper mapper = Mappers.getMapper(ProductMapper.class);

  @Test
  void shouldMapFieldsWithCustomNames() {
    Product product = new Product(1L, "Laptop", 999.99);
    
    ProductDto dto = mapper.toDto(product);
    
    assertThat(dto)
      .hasFieldOrPropertyWithValue("productName", "Laptop")
      .hasFieldOrPropertyWithValue("salePrice", 999.99);
  }

  @Test
  void shouldCalculateDiscountFromExpression() {
    Product product = new Product(1L, "Laptop", 100.0);
    
    ProductDto dto = mapper.toDto(product);
    
    assertThat(dto.getDiscount()).isEqualTo(10.0);
  }

  @Test
  void shouldReverseMapCustomFields() {
    ProductDto dto = new ProductDto(1L, "Laptop", 999.99);
    
    Product product = mapper.toEntity(dto);
    
    assertThat(product)
      .hasFieldOrPropertyWithValue("name", "Laptop")
      .hasFieldOrPropertyWithValue("price", 999.99);
  }
}
```

## Testing Enum Mapping

### Map Enums Between Entity and DTO

```java
// Enum with different representation
enum UserStatus { ACTIVE, INACTIVE, SUSPENDED }
enum UserStatusDto { ENABLED, DISABLED, LOCKED }

@Mapper(componentModel = "spring")
public interface UserMapper {
  @ValueMapping(source = "ACTIVE", target = "ENABLED")
  @ValueMapping(source = "INACTIVE", target = "DISABLED")
  @ValueMapping(source = "SUSPENDED", target = "LOCKED")
  UserStatusDto toStatusDto(UserStatus status);
}

class EnumMapperTest {

  private final UserMapper mapper = Mappers.getMapper(UserMapper.class);

  @Test
  void shouldMapActiveToEnabled() {
    UserStatusDto dto = mapper.toStatusDto(UserStatus.ACTIVE);
    assertThat(dto).isEqualTo(UserStatusDto.ENABLED);
  }

  @Test
  void shouldMapSuspendedToLocked() {
    UserStatusDto dto = mapper.toStatusDto(UserStatus.SUSPENDED);
    assertThat(dto).isEqualTo(UserStatusDto.LOCKED);
  }
}
```

## Testing Custom Type Conversions

### Non-MapStruct Custom Converter

```java
// Custom converter class
public class DateFormatter {
  private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");

  public static String format(LocalDate date) {
    return date != null ? date.format(formatter) : null;
  }

  public static LocalDate parse(String dateString) {
    return dateString != null ? LocalDate.parse(dateString, formatter) : null;
  }
}

// Unit test
class DateFormatterTest {

  @Test
  void shouldFormatLocalDateToString() {
    LocalDate date = LocalDate.of(2024, 1, 15);
    
    String result = DateFormatter.format(date);
    
    assertThat(result).isEqualTo("2024-01-15");
  }

  @Test
  void shouldParseStringToLocalDate() {
    String dateString = "2024-01-15";
    
    LocalDate result = DateFormatter.parse(dateString);
    
    assertThat(result).isEqualTo(LocalDate.of(2024, 1, 15));
  }

  @Test
  void shouldHandleNullInFormat() {
    String result = DateFormatter.format(null);
    assertThat(result).isNull();
  }

  @Test
  void shouldHandleInvalidDateFormat() {
    assertThatThrownBy(() -> DateFormatter.parse("invalid-date"))
      .isInstanceOf(DateTimeParseException.class);
  }
}
```

## Testing Bidirectional Mapping

### Entity ↔ DTO Round Trip

```java
class BidirectionalMapperTest {

  private final UserMapper mapper = Mappers.getMapper(UserMapper.class);

  @Test
  void shouldMaintainDataInRoundTrip() {
    User original = new User(1L, "Alice", "alice@example.com", 25);
    
    UserDto dto = mapper.toDto(original);
    User restored = mapper.toEntity(dto);
    
    assertThat(restored)
      .hasFieldOrPropertyWithValue("id", original.getId())
      .hasFieldOrPropertyWithValue("name", original.getName())
      .hasFieldOrPropertyWithValue("email", original.getEmail())
      .hasFieldOrPropertyWithValue("age", original.getAge());
  }

  @Test
  void shouldPreserveAllFieldsInBothDirections() {
    Address address = new Address("123 Main", "NYC", "NY", "10001");
    User user = new User(1L, "Alice", "alice@example.com", 25, address);
    
    UserDto dto = mapper.toDto(user);
    User restored = mapper.toEntity(dto);
    
    assertThat(restored).usingRecursiveComparison().isEqualTo(user);
  }
}
```

## Testing Partial Mapping

### Update Existing Entity from DTO

```java
@Mapper(componentModel = "spring")
public interface UserMapper {
  void updateEntity(@MappingTarget User entity, UserDto dto);
}

class PartialMapperTest {

  private final UserMapper mapper = Mappers.getMapper(UserMapper.class);

  @Test
  void shouldUpdateExistingEntity() {
    User existing = new User(1L, "Alice", "alice@old.com", 25);
    UserDto dto = new UserDto(1L, "Alice", "alice@new.com", 26);
    
    mapper.updateEntity(existing, dto);
    
    assertThat(existing)
      .hasFieldOrPropertyWithValue("email", "alice@new.com")
      .hasFieldOrPropertyWithValue("age", 26);
  }

  @Test
  void shouldNotUpdateFieldsNotInDto() {
    User existing = new User(1L, "Alice", "alice@example.com", 25);
    UserDto dto = new UserDto(1L, "Bob", null, 0);
    
    mapper.updateEntity(existing, dto);
    
    // Assuming null-aware mapping is configured
    assertThat(existing.getEmail()).isEqualTo("alice@example.com");
  }
}
```

## Best Practices

- **Test all mapper methods** comprehensively
- **Verify null handling** for every nullable field
- **Test nested objects** independently and together
- **Use recursive comparison** for complex nested structures
- **Test bidirectional mapping** to catch asymmetries
- **Keep mapper tests simple and focused** on transformation correctness
- **Use Mappers.getMapper()** for non-Spring standalone tests

## Common Pitfalls

- Not testing null input cases
- Not verifying nested object mappings
- Assuming bidirectional mapping is symmetric
- Not testing edge cases (empty collections, etc.)
- Tight coupling of mapper tests to MapStruct internals

## Troubleshooting

**Null pointer exceptions during mapping**: Check `nullValuePropertyMappingStrategy` and `nullValueCheckStrategy` in `@Mapper`.

**Enum mapping not working**: Verify `@ValueMapping` annotations correctly map source to target values.

**Nested mapping produces null**: Ensure nested mapper interfaces are also mapped in parent mapper.

## References

- [MapStruct Official Documentation](https://mapstruct.org/)
- [MapStruct Mapping Strategies](https://mapstruct.org/documentation/stable/reference/html/)
- [JUnit 5 Best Practices](https://junit.org/junit5/docs/current/user-guide/)

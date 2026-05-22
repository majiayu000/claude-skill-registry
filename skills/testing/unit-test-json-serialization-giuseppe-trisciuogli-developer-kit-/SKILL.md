---
name: unit-test-json-serialization
description: Unit tests for JSON serialization/deserialization with Jackson and @JsonTest. Use when validating JSON mapping, custom serializers, and date format handling.
category: testing
tags: [junit-5, json-test, jackson, serialization, deserialization]
version: 1.0.1
---

# Unit Testing JSON Serialization with @JsonTest

Test JSON serialization and deserialization of POJOs using Spring's @JsonTest. Verify Jackson configuration, custom serializers, and JSON mapping accuracy.

## When to Use This Skill

Use this skill when:
- Testing JSON serialization of DTOs
- Testing JSON deserialization to objects
- Testing custom Jackson serializers/deserializers
- Verifying JSON field names and formats
- Testing null handling in JSON
- Want fast JSON mapping tests without full Spring context

## Setup: JSON Testing

### Maven
```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-json</artifactId>
</dependency>
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-test</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>com.fasterxml.jackson.core</groupId>
  <artifactId>jackson-databind</artifactId>
</dependency>
```

### Gradle
```kotlin
dependencies {
  implementation("org.springframework.boot:spring-boot-starter-json")
  implementation("com.fasterxml.jackson.core:jackson-databind")
  testImplementation("org.springframework.boot:spring-boot-starter-test")
}
```

## Basic Pattern: @JsonTest

### Test JSON Serialization

```java
import org.springframework.boot.test.autoconfigure.json.JsonTest;
import org.springframework.boot.test.json.JacksonTester;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

@JsonTest
class UserDtoJsonTest {

  @Autowired
  private JacksonTester<UserDto> json;

  @Test
  void shouldSerializeUserToJson() throws Exception {
    UserDto user = new UserDto(1L, "Alice", "alice@example.com", 25);

    org.assertj.core.data.Offset result = json.write(user);

    result
      .extractingJsonPathNumberValue("$.id").isEqualTo(1)
      .extractingJsonPathStringValue("$.name").isEqualTo("Alice")
      .extractingJsonPathStringValue("$.email").isEqualTo("alice@example.com")
      .extractingJsonPathNumberValue("$.age").isEqualTo(25);
  }

  @Test
  void shouldDeserializeJsonToUser() throws Exception {
    String json_content = "{\"id\":1,\"name\":\"Alice\",\"email\":\"alice@example.com\",\"age\":25}";

    UserDto user = json.parse(json_content).getObject();

    assertThat(user)
      .isNotNull()
      .hasFieldOrPropertyWithValue("id", 1L)
      .hasFieldOrPropertyWithValue("name", "Alice")
      .hasFieldOrPropertyWithValue("email", "alice@example.com")
      .hasFieldOrPropertyWithValue("age", 25);
  }

  @Test
  void shouldHandleNullFields() throws Exception {
    String json_content = "{\"id\":1,\"name\":null,\"email\":\"alice@example.com\",\"age\":null}";

    UserDto user = json.parse(json_content).getObject();

    assertThat(user.getName()).isNull();
    assertThat(user.getAge()).isNull();
  }
}
```

## Testing Custom JSON Properties

### @JsonProperty and @JsonIgnore

```java
public class Order {
  @JsonProperty("order_id")
  private Long id;

  @JsonProperty("total_amount")
  private BigDecimal amount;

  @JsonIgnore
  private String internalNote;

  private LocalDateTime createdAt;
}

@JsonTest
class OrderJsonTest {

  @Autowired
  private JacksonTester<Order> json;

  @Test
  void shouldMapJsonPropertyNames() throws Exception {
    String json_content = "{\"order_id\":123,\"total_amount\":99.99,\"createdAt\":\"2024-01-15T10:30:00\"}";

    Order order = json.parse(json_content).getObject();

    assertThat(order.getId()).isEqualTo(123L);
    assertThat(order.getAmount()).isEqualByComparingTo(new BigDecimal("99.99"));
  }

  @Test
  void shouldIgnoreJsonIgnoreAnnotatedFields() throws Exception {
    Order order = new Order(123L, new BigDecimal("99.99"));
    order.setInternalNote("Secret note");

    JsonContent<Order> result = json.write(order);

    assertThat(result.json).doesNotContain("internalNote");
  }
}
```

## Testing List Deserialization

### JSON Arrays

```java
@JsonTest
class UserListJsonTest {

  @Autowired
  private JacksonTester<List<UserDto>> json;

  @Test
  void shouldDeserializeUserList() throws Exception {
    String jsonArray = "[{\"id\":1,\"name\":\"Alice\"},{\"id\":2,\"name\":\"Bob\"}]";

    List<UserDto> users = json.parseObject(jsonArray);

    assertThat(users)
      .hasSize(2)
      .extracting(UserDto::getName)
      .containsExactly("Alice", "Bob");
  }

  @Test
  void shouldSerializeUserListToJson() throws Exception {
    List<UserDto> users = List.of(
      new UserDto(1L, "Alice"),
      new UserDto(2L, "Bob")
    );

    JsonContent<List<UserDto>> result = json.write(users);

    result.json.contains("Alice").contains("Bob");
  }
}
```

## Testing Nested Objects

### Complex JSON Structures

```java
public class Product {
  private Long id;
  private String name;
  private Category category;
  private List<Review> reviews;
}

public class Category {
  private Long id;
  private String name;
}

public class Review {
  private String reviewer;
  private int rating;
  private String comment;
}

@JsonTest
class ProductJsonTest {

  @Autowired
  private JacksonTester<Product> json;

  @Test
  void shouldSerializeNestedObjects() throws Exception {
    Category category = new Category(1L, "Electronics");
    Product product = new Product(1L, "Laptop", category);

    JsonContent<Product> result = json.write(product);

    result
      .extractingJsonPathNumberValue("$.id").isEqualTo(1)
      .extractingJsonPathStringValue("$.name").isEqualTo("Laptop")
      .extractingJsonPathNumberValue("$.category.id").isEqualTo(1)
      .extractingJsonPathStringValue("$.category.name").isEqualTo("Electronics");
  }

  @Test
  void shouldDeserializeNestedObjects() throws Exception {
    String json_content = "{\"id\":1,\"name\":\"Laptop\",\"category\":{\"id\":1,\"name\":\"Electronics\"}}";

    Product product = json.parse(json_content).getObject();

    assertThat(product.getCategory())
      .isNotNull()
      .hasFieldOrPropertyWithValue("name", "Electronics");
  }

  @Test
  void shouldHandleListOfNestedObjects() throws Exception {
    String json_content = "{\"id\":1,\"name\":\"Laptop\",\"reviews\":[{\"reviewer\":\"John\",\"rating\":5},{\"reviewer\":\"Jane\",\"rating\":4}]}";

    Product product = json.parse(json_content).getObject();

    assertThat(product.getReviews())
      .hasSize(2)
      .extracting(Review::getRating)
      .containsExactly(5, 4);
  }
}
```

## Testing Date/Time Formatting

### LocalDateTime and Other Temporal Types

```java
@JsonTest
class DateTimeJsonTest {

  @Autowired
  private JacksonTester<Event> json;

  @Test
  void shouldFormatDateTimeCorrectly() throws Exception {
    LocalDateTime dateTime = LocalDateTime.of(2024, 1, 15, 10, 30, 0);
    Event event = new Event("Conference", dateTime);

    JsonContent<Event> result = json.write(event);

    result.extractingJsonPathStringValue("$.scheduledAt").isEqualTo("2024-01-15T10:30:00");
  }

  @Test
  void shouldDeserializeDateTimeFromJson() throws Exception {
    String json_content = "{\"name\":\"Conference\",\"scheduledAt\":\"2024-01-15T10:30:00\"}";

    Event event = json.parse(json_content).getObject();

    assertThat(event.getScheduledAt())
      .isEqualTo(LocalDateTime.of(2024, 1, 15, 10, 30, 0));
  }
}
```

## Testing Custom Serializers

### Custom JsonSerializer Implementation

```java
public class CustomMoneySerializer extends JsonSerializer<BigDecimal> {
  @Override
  public void serialize(BigDecimal value, JsonGenerator gen, SerializerProvider serializers) throws IOException {
    if (value == null) {
      gen.writeNull();
    } else {
      gen.writeString(String.format("$%.2f", value));
    }
  }
}

public class Price {
  @JsonSerialize(using = CustomMoneySerializer.class)
  private BigDecimal amount;
}

@JsonTest
class CustomSerializerTest {

  @Autowired
  private JacksonTester<Price> json;

  @Test
  void shouldUseCustomSerializer() throws Exception {
    Price price = new Price(new BigDecimal("99.99"));

    JsonContent<Price> result = json.write(price);

    result.extractingJsonPathStringValue("$.amount").isEqualTo("$99.99");
  }
}
```

## Testing Polymorphic Deserialization

### Type Information in JSON

```java
@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, property = "type")
@JsonSubTypes({
  @JsonSubTypes.Type(value = CreditCard.class, name = "credit_card"),
  @JsonSubTypes.Type(value = PayPal.class, name = "paypal")
})
public abstract class PaymentMethod {
  private String id;
}

@JsonTest
class PolymorphicJsonTest {

  @Autowired
  private JacksonTester<PaymentMethod> json;

  @Test
  void shouldDeserializeCreditCard() throws Exception {
    String json_content = "{\"type\":\"credit_card\",\"id\":\"card123\",\"cardNumber\":\"****1234\"}";

    PaymentMethod method = json.parse(json_content).getObject();

    assertThat(method).isInstanceOf(CreditCard.class);
  }

  @Test
  void shouldDeserializePayPal() throws Exception {
    String json_content = "{\"type\":\"paypal\",\"id\":\"pp123\",\"email\":\"user@paypal.com\"}";

    PaymentMethod method = json.parse(json_content).getObject();

    assertThat(method).isInstanceOf(PayPal.class);
  }
}
```

## Best Practices

- **Use @JsonTest** for focused JSON testing
- **Test both serialization and deserialization**
- **Test null handling** and missing fields
- **Test nested and complex structures**
- **Verify field name mapping** with @JsonProperty
- **Test date/time formatting** thoroughly
- **Test edge cases** (empty strings, empty collections)

## Common Pitfalls

- Not testing null values
- Not testing nested objects
- Forgetting to test field name mappings
- Not verifying JSON property presence/absence
- Not testing deserialization of invalid JSON

## Troubleshooting

**JacksonTester not available**: Ensure class is annotated with `@JsonTest`.

**Field name doesn't match**: Check @JsonProperty annotation and Jackson configuration.

**DateTime parsing fails**: Verify date format matches Jackson's expected format.

## References

- [Spring @JsonTest Documentation](https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/test/autoconfigure/json/JsonTest.html)
- [Jackson ObjectMapper](https://fasterxml.github.io/jackson-databind/javadoc/2.15/com/fasterxml/jackson/databind/ObjectMapper.html)
- [JSON Annotations](https://fasterxml.github.io/jackson-annotations/javadoc/2.15/)

---
name: unit-test-bean-validation
description: Unit testing Jakarta Bean Validation (@Valid, @NotNull, @Min, @Max, etc.) with custom validators and constraint violations. Test validation logic without Spring context. Use when ensuring data integrity and validation rules are correct.
category: testing
tags: [junit-5, validation, bean-validation, jakarta-validation, constraints]
version: 1.0.1
---

# Unit Testing Bean Validation and Custom Validators

Test validation annotations and custom validator implementations using JUnit 5. Verify constraint violations, error messages, and validation logic in isolation.

## When to Use This Skill

Use this skill when:
- Testing Jakarta Bean Validation (@NotNull, @Email, @Min, etc.)
- Testing custom @Constraint validators
- Verifying constraint violation error messages
- Testing cross-field validation logic
- Want fast validation tests without Spring context
- Testing complex validation scenarios and edge cases

## Setup: Bean Validation

### Maven
```xml
<dependency>
  <groupId>jakarta.validation</groupId>
  <artifactId>jakarta.validation-api</artifactId>
</dependency>
<dependency>
  <groupId>org.hibernate.validator</groupId>
  <artifactId>hibernate-validator</artifactId>
  <scope>test</scope>
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
  implementation("jakarta.validation:jakarta.validation-api")
  testImplementation("org.hibernate.validator:hibernate-validator")
  testImplementation("org.junit.jupiter:junit-jupiter")
  testImplementation("org.assertj:assertj-core")
}
```

## Basic Pattern: Testing Validation Constraints

### Setup Validator

```java
import jakarta.validation.Validator;
import jakarta.validation.ValidatorFactory;
import jakarta.validation.Validation;
import jakarta.validation.ConstraintViolation;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

class UserValidationTest {

  private Validator validator;

  @BeforeEach
  void setUp() {
    ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
    validator = factory.getValidator();
  }

  @Test
  void shouldPassValidationWithValidUser() {
    User user = new User("Alice", "alice@example.com", 25);
    
    Set<ConstraintViolation<User>> violations = validator.validate(user);
    
    assertThat(violations).isEmpty();
  }

  @Test
  void shouldFailValidationWhenNameIsNull() {
    User user = new User(null, "alice@example.com", 25);
    
    Set<ConstraintViolation<User>> violations = validator.validate(user);
    
    assertThat(violations)
      .hasSize(1)
      .extracting(ConstraintViolation::getMessage)
      .contains("must not be blank");
  }
}
```

## Testing Individual Constraint Annotations

### Test @NotNull, @NotBlank, @Email

```java
class UserDtoTest {

  private Validator validator;

  @BeforeEach
  void setUp() {
    validator = Validation.buildDefaultValidatorFactory().getValidator();
  }

  @Test
  void shouldFailWhenEmailIsInvalid() {
    UserDto dto = new UserDto("Alice", "invalid-email");
    
    Set<ConstraintViolation<UserDto>> violations = validator.validate(dto);
    
    assertThat(violations)
      .extracting(ConstraintViolation::getPropertyPath)
      .extracting(Path::toString)
      .contains("email");
    assertThat(violations)
      .extracting(ConstraintViolation::getMessage)
      .contains("must be a valid email address");
  }

  @Test
  void shouldFailWhenNameIsBlank() {
    UserDto dto = new UserDto("   ", "alice@example.com");
    
    Set<ConstraintViolation<UserDto>> violations = validator.validate(dto);
    
    assertThat(violations)
      .extracting(ConstraintViolation::getPropertyPath)
      .extracting(Path::toString)
      .contains("name");
  }

  @Test
  void shouldFailWhenAgeIsNegative() {
    UserDto dto = new UserDto("Alice", "alice@example.com", -5);
    
    Set<ConstraintViolation<UserDto>> violations = validator.validate(dto);
    
    assertThat(violations)
      .extracting(ConstraintViolation::getMessage)
      .contains("must be greater than or equal to 0");
  }

  @Test
  void shouldPassWhenAllConstraintsSatisfied() {
    UserDto dto = new UserDto("Alice", "alice@example.com", 25);
    
    Set<ConstraintViolation<UserDto>> violations = validator.validate(dto);
    
    assertThat(violations).isEmpty();
  }
}
```

## Testing @Min, @Max, @Size Constraints

```java
class ProductDtoTest {

  private Validator validator;

  @BeforeEach
  void setUp() {
    validator = Validation.buildDefaultValidatorFactory().getValidator();
  }

  @Test
  void shouldFailWhenPriceIsBelowMinimum() {
    ProductDto product = new ProductDto("Laptop", -100.0);
    
    Set<ConstraintViolation<ProductDto>> violations = validator.validate(product);
    
    assertThat(violations)
      .extracting(ConstraintViolation::getMessage)
      .contains("must be greater than 0");
  }

  @Test
  void shouldFailWhenQuantityExceedsMaximum() {
    ProductDto product = new ProductDto("Laptop", 1000.0, 999999);
    
    Set<ConstraintViolation<ProductDto>> violations = validator.validate(product);
    
    assertThat(violations)
      .extracting(ConstraintViolation::getMessage)
      .contains("must be less than or equal to 10000");
  }

  @Test
  void shouldFailWhenDescriptionTooLong() {
    String longDescription = "x".repeat(1001);
    ProductDto product = new ProductDto("Laptop", 1000.0, longDescription);
    
    Set<ConstraintViolation<ProductDto>> violations = validator.validate(product);
    
    assertThat(violations)
      .extracting(ConstraintViolation::getMessage)
      .contains("size must be between 0 and 1000");
  }
}
```

## Testing Custom Validators

### Create and Test Custom Constraint

```java
// Custom constraint annotation
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = PhoneNumberValidator.class)
public @interface ValidPhoneNumber {
  String message() default "invalid phone number format";
  Class<?>[] groups() default {};
  Class<? extends Payload>[] payload() default {};
}

// Custom validator implementation
public class PhoneNumberValidator implements ConstraintValidator<ValidPhoneNumber, String> {
  private static final String PHONE_PATTERN = "^\\d{3}-\\d{3}-\\d{4}$";

  @Override
  public boolean isValid(String value, ConstraintValidatorContext context) {
    if (value == null) return true; // null values handled by @NotNull
    return value.matches(PHONE_PATTERN);
  }
}

// Unit test for custom validator
class PhoneNumberValidatorTest {

  private Validator validator;

  @BeforeEach
  void setUp() {
    validator = Validation.buildDefaultValidatorFactory().getValidator();
  }

  @Test
  void shouldAcceptValidPhoneNumber() {
    Contact contact = new Contact("Alice", "555-123-4567");
    
    Set<ConstraintViolation<Contact>> violations = validator.validate(contact);
    
    assertThat(violations).isEmpty();
  }

  @Test
  void shouldRejectInvalidPhoneNumberFormat() {
    Contact contact = new Contact("Alice", "5551234567"); // No dashes
    
    Set<ConstraintViolation<Contact>> violations = validator.validate(contact);
    
    assertThat(violations)
      .extracting(ConstraintViolation::getMessage)
      .contains("invalid phone number format");
  }

  @Test
  void shouldRejectPhoneNumberWithLetters() {
    Contact contact = new Contact("Alice", "ABC-DEF-GHIJ");
    
    Set<ConstraintViolation<Contact>> violations = validator.validate(contact);
    
    assertThat(violations).isNotEmpty();
  }

  @Test
  void shouldAllowNullPhoneNumber() {
    Contact contact = new Contact("Alice", null);
    
    Set<ConstraintViolation<Contact>> violations = validator.validate(contact);
    
    assertThat(violations).isEmpty();
  }
}
```

## Testing Cross-Field Validation

### Custom Multi-Field Constraint

```java
// Custom constraint for cross-field validation
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = PasswordMatchValidator.class)
public @interface PasswordsMatch {
  String message() default "passwords do not match";
  Class<?>[] groups() default {};
  Class<? extends Payload>[] payload() default {};
}

// Validator implementation
public class PasswordMatchValidator implements ConstraintValidator<PasswordsMatch, ChangePasswordRequest> {
  @Override
  public boolean isValid(ChangePasswordRequest value, ConstraintValidatorContext context) {
    if (value == null) return true;
    return value.getNewPassword().equals(value.getConfirmPassword());
  }
}

// Unit test
class PasswordValidationTest {

  private Validator validator;

  @BeforeEach
  void setUp() {
    validator = Validation.buildDefaultValidatorFactory().getValidator();
  }

  @Test
  void shouldPassWhenPasswordsMatch() {
    ChangePasswordRequest request = new ChangePasswordRequest("oldPass", "newPass123", "newPass123");
    
    Set<ConstraintViolation<ChangePasswordRequest>> violations = validator.validate(request);
    
    assertThat(violations).isEmpty();
  }

  @Test
  void shouldFailWhenPasswordsDoNotMatch() {
    ChangePasswordRequest request = new ChangePasswordRequest("oldPass", "newPass123", "differentPass");
    
    Set<ConstraintViolation<ChangePasswordRequest>> violations = validator.validate(request);
    
    assertThat(violations)
      .extracting(ConstraintViolation::getMessage)
      .contains("passwords do not match");
  }
}
```

## Testing Validation Groups

### Conditional Validation

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public interface CreateValidation {}

@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public interface UpdateValidation {}

class UserDto {
  @NotNull(groups = {CreateValidation.class})
  private String name;

  @Min(value = 1, groups = {CreateValidation.class, UpdateValidation.class})
  private int age;
}

class ValidationGroupsTest {

  private Validator validator;

  @BeforeEach
  void setUp() {
    validator = Validation.buildDefaultValidatorFactory().getValidator();
  }

  @Test
  void shouldRequireNameOnlyDuringCreation() {
    UserDto user = new UserDto(null, 25);
    
    Set<ConstraintViolation<UserDto>> violations = validator.validate(user, CreateValidation.class);
    
    assertThat(violations)
      .extracting(ConstraintViolation::getPropertyPath)
      .extracting(Path::toString)
      .contains("name");
  }

  @Test
  void shouldAllowNullNameDuringUpdate() {
    UserDto user = new UserDto(null, 25);
    
    Set<ConstraintViolation<UserDto>> violations = validator.validate(user, UpdateValidation.class);
    
    assertThat(violations).isEmpty();
  }
}
```

## Testing Parameterized Validation Scenarios

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class EmailValidationTest {

  private Validator validator;

  @BeforeEach
  void setUp() {
    validator = Validation.buildDefaultValidatorFactory().getValidator();
  }

  @ParameterizedTest
  @ValueSource(strings = {
    "user@example.com",
    "john.doe+tag@example.co.uk",
    "admin123@subdomain.example.com"
  })
  void shouldAcceptValidEmails(String email) {
    UserDto user = new UserDto("Alice", email);
    
    Set<ConstraintViolation<UserDto>> violations = validator.validate(user);
    
    assertThat(violations).isEmpty();
  }

  @ParameterizedTest
  @ValueSource(strings = {
    "invalid-email",
    "user@",
    "@example.com",
    "user name@example.com"
  })
  void shouldRejectInvalidEmails(String email) {
    UserDto user = new UserDto("Alice", email);
    
    Set<ConstraintViolation<UserDto>> violations = validator.validate(user);
    
    assertThat(violations).isNotEmpty();
  }
}
```

## Best Practices

- **Validate at unit test level** before testing service/controller layers
- **Test both valid and invalid cases** for every constraint
- **Use custom validators** for business-specific validation rules
- **Test error messages** to ensure they're user-friendly
- **Test edge cases**: null, empty string, whitespace-only strings
- **Use validation groups** for conditional validation rules
- **Keep validator logic simple** - complex validation belongs in service tests

## Common Pitfalls

- Forgetting to test null values
- Not extracting violation details (message, property, constraint type)
- Testing validation at service/controller level instead of unit tests
- Creating overly complex custom validators
- Not documenting constraint purposes in error messages

## Troubleshooting

**ValidatorFactory not found**: Ensure `jakarta.validation-api` and `hibernate-validator` are on classpath.

**Custom validator not invoked**: Verify `@Constraint(validatedBy = YourValidator.class)` is correctly specified.

**Null handling confusion**: By default, `@NotNull` checks null, other constraints ignore null (use `@NotNull` with others for mandatory fields).

## References

- [Jakarta Bean Validation Spec](https://jakarta.ee/specifications/bean-validation/)
- [Hibernate Validator Documentation](https://hibernate.org/validator/)
- [Custom Constraints](https://docs.jboss.org/hibernate/stable/validator/reference/en-US/html_single/#validator-customconstraints)

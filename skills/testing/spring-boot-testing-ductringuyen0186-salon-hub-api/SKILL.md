---
name: spring-boot-testing
description: Guide for writing comprehensive tests for Spring Boot applications including unit tests, integration tests, and test slices. Use this when creating tests for new features or fixing bugs.
---

# Spring Boot Testing Best Practices

Follow these practices for comprehensive test coverage.

## Test Directory Structure

```
src/
├── test/java/com/salonhub/api/           # Unit tests
│   └── [domain]/
│       ├── controller/
│       │   └── [Feature]ControllerTest.java
│       ├── service/
│       │   └── [Feature]ServiceTest.java
│       └── repository/
│           └── [Feature]RepositoryTest.java
├── integration/java/com/salonhub/api/    # Integration tests
│   └── [domain]/
│       └── [Feature]IntegrationTest.java
└── testFixtures/java/com/salonhub/api/   # Shared test utilities
    └── [domain]/
        ├── [Domain]DatabaseDefault.java
        └── [Domain]TestDataBuilder.java
```

## Unit Testing - Controller Layer

```java
@WebMvcTest(controllers = AppointmentController.class)
@Import(TestSecurityConfig.class)
class AppointmentControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private AppointmentService appointmentService;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    @WithMockUser(roles = {"FRONT_DESK"})
    void getAppointment_whenExists_shouldReturn200() throws Exception {
        // Arrange
        AppointmentResponseDTO dto = new AppointmentResponseDTO(1L, "John", "Alice", "Haircut");
        when(appointmentService.findById(1L)).thenReturn(dto);

        // Act & Assert
        mockMvc.perform(get("/api/appointments/1")
                .contentType(MediaType.APPLICATION_JSON))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(1))
            .andExpect(jsonPath("$.customerName").value("John"));

        verify(appointmentService).findById(1L);
    }

    @Test
    @WithMockUser(roles = {"FRONT_DESK"})
    void createAppointment_withValidRequest_shouldReturn201() throws Exception {
        // Arrange
        AppointmentRequestDTO request = new AppointmentRequestDTO();
        request.setCustomerId(1L);
        request.setEmployeeId(1L);

        AppointmentResponseDTO response = new AppointmentResponseDTO(1L, "John", "Alice", "Haircut");
        when(appointmentService.create(any())).thenReturn(response);

        // Act & Assert
        mockMvc.perform(post("/api/appointments")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").value(1));
    }

    @Test
    @WithMockUser(roles = {"FRONT_DESK"})
    void createAppointment_withInvalidRequest_shouldReturn400() throws Exception {
        // Arrange - missing required fields
        AppointmentRequestDTO request = new AppointmentRequestDTO();

        // Act & Assert
        mockMvc.perform(post("/api/appointments")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isBadRequest());
    }
}
```

## Unit Testing - Service Layer

```java
@ExtendWith(MockitoExtension.class)
class AppointmentServiceTest {

    @Mock
    private AppointmentRepository appointmentRepository;

    @Mock
    private AppointmentMapper appointmentMapper;

    @InjectMocks
    private AppointmentService appointmentService;

    @Test
    void findById_whenExists_shouldReturnAppointment() {
        // Arrange
        Appointment appointment = new Appointment();
        appointment.setId(1L);
        AppointmentResponseDTO dto = new AppointmentResponseDTO(1L, "John", "Alice", "Haircut");

        when(appointmentRepository.findById(1L)).thenReturn(Optional.of(appointment));
        when(appointmentMapper.toResponseDTO(appointment)).thenReturn(dto);

        // Act
        AppointmentResponseDTO result = appointmentService.findById(1L);

        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(1L);
        verify(appointmentRepository).findById(1L);
    }

    @Test
    void findById_whenNotExists_shouldThrowException() {
        // Arrange
        when(appointmentRepository.findById(anyLong())).thenReturn(Optional.empty());

        // Act & Assert
        assertThatThrownBy(() -> appointmentService.findById(1L))
            .isInstanceOf(ResourceNotFoundException.class)
            .hasMessageContaining("Appointment not found");
    }
}
```

## Repository Testing

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@TestPropertySource(properties = "spring.profiles.active=test")
class AppointmentRepositoryTest {

    @Autowired
    private AppointmentRepository appointmentRepository;

    @Autowired
    private TestEntityManager entityManager;

    @Test
    void findByCustomerId_shouldReturnMatchingAppointments() {
        // Arrange
        Customer customer = new Customer();
        customer.setName("John");
        entityManager.persist(customer);

        Appointment appointment = new Appointment();
        appointment.setCustomer(customer);
        entityManager.persist(appointment);
        entityManager.flush();

        // Act
        List<Appointment> results = appointmentRepository.findByCustomerId(customer.getId());

        // Assert
        assertThat(results).hasSize(1);
        assertThat(results.get(0).getCustomer().getName()).isEqualTo("John");
    }
}
```

## Integration Testing

```java
@ServerSetupExtension
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class AppointmentIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    // Use constants from database defaults
    private static final Long EXISTING_CUSTOMER_ID = CustomerDatabaseDefault.JANE_ID;
    private static final Long EXISTING_EMPLOYEE_ID = EmployeeDatabaseDefault.ALICE_ID;
    private static final Long EXISTING_SERVICE_ID = ServiceTypeDatabaseDefault.HAIRCUT_ID;

    private static Long createdAppointmentId;

    @Test
    @Order(1)
    void createAppointment_shouldReturnCreated() throws Exception {
        AppointmentRequestDTO request = new AppointmentRequestDTO();
        request.setCustomerId(EXISTING_CUSTOMER_ID);
        request.setEmployeeId(EXISTING_EMPLOYEE_ID);
        request.setServiceTypeId(EXISTING_SERVICE_ID);
        request.setAppointmentTime(LocalDateTime.now().plusDays(1));

        var result = mockMvc.perform(post("/api/appointments")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").exists())
            .andReturn();

        String json = result.getResponse().getContentAsString();
        createdAppointmentId = objectMapper.readTree(json).get("id").asLong();
    }

    @Test
    @Order(2)
    void getAppointment_shouldReturnAppointment() throws Exception {
        mockMvc.perform(get("/api/appointments/{id}", createdAppointmentId))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(createdAppointmentId));
    }

    @Test
    @Order(3)
    void updateAppointment_shouldReturnUpdated() throws Exception {
        AppointmentRequestDTO updateRequest = new AppointmentRequestDTO();
        updateRequest.setCustomerId(EXISTING_CUSTOMER_ID);
        updateRequest.setEmployeeId(EXISTING_EMPLOYEE_ID);
        updateRequest.setServiceTypeId(EXISTING_SERVICE_ID);
        updateRequest.setAppointmentTime(LocalDateTime.now().plusDays(2));

        mockMvc.perform(put("/api/appointments/{id}", createdAppointmentId)
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updateRequest)))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(createdAppointmentId));
    }

    @Test
    @Order(4)
    void deleteAppointment_shouldReturnNoContent() throws Exception {
        mockMvc.perform(delete("/api/appointments/{id}", createdAppointmentId))
            .andExpect(status().isNoContent());
    }
}
```

## Test Data Builders

```java
public class AppointmentTestDataBuilder {
    private Long id;
    private Customer customer;
    private Employee employee;
    private LocalDateTime appointmentTime;
    private String status;

    public static AppointmentTestDataBuilder anAppointment() {
        return new AppointmentTestDataBuilder()
            .withId(1L)
            .withAppointmentTime(LocalDateTime.now().plusHours(1))
            .withStatus("SCHEDULED");
    }

    public AppointmentTestDataBuilder withId(Long id) {
        this.id = id;
        return this;
    }

    public AppointmentTestDataBuilder withCustomer(Customer customer) {
        this.customer = customer;
        return this;
    }

    public Appointment build() {
        Appointment appointment = new Appointment();
        appointment.setId(id);
        appointment.setCustomer(customer);
        appointment.setEmployee(employee);
        appointment.setAppointmentTime(appointmentTime);
        appointment.setStatus(status);
        return appointment;
    }

    public AppointmentRequestDTO buildRequestDTO() {
        AppointmentRequestDTO dto = new AppointmentRequestDTO();
        dto.setCustomerId(customer != null ? customer.getId() : null);
        dto.setEmployeeId(employee != null ? employee.getId() : null);
        dto.setAppointmentTime(appointmentTime);
        return dto;
    }
}
```

## Database Defaults for Testing

```java
public class AppointmentDatabaseDefault {
    public static final Long APPOINTMENT_ID_1 = 100L;
    public static final Long APPOINTMENT_ID_2 = 101L;

    public static final String INSERT_APPOINTMENT_1 =
        "INSERT INTO appointments (id, customer_id, employee_id, appointment_time, status) VALUES " +
        "(100, " + CustomerDatabaseDefault.JANE_ID + ", " + EmployeeDatabaseDefault.ALICE_ID + ", " +
        "CURRENT_TIMESTAMP + INTERVAL '1 day', 'SCHEDULED')";

    public static final String[] ALL_INSERTS = {
        INSERT_APPOINTMENT_1
    };
}
```

## Running Tests

```powershell
# Run all tests
.\gradlew.bat check

# Run only unit tests
.\gradlew.bat test

# Run only integration tests
.\gradlew.bat integrationTest

# Run specific test class
.\gradlew.bat test --tests "AppointmentServiceTest"

# Run with coverage
.\gradlew.bat test jacocoTestReport
```

## Test Coverage Requirements

- **Minimum 80%** code coverage for new features
- **100%** coverage for critical business logic
- All error scenarios tested
- All validation rules tested
- Security tests for all protected endpoints

## Testing Checklist for New Features

- [ ] Unit tests for controller (valid/invalid input, security)
- [ ] Unit tests for service (business logic, edge cases, exceptions)
- [ ] Repository tests for custom queries
- [ ] Integration tests (CRUD operations with real database)
- [ ] Create test data builders
- [ ] Update database defaults if needed
- [ ] Run full test suite: `.\gradlew.bat check`

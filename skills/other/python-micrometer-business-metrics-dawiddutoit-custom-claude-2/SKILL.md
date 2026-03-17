---
name: python-micrometer-business-metrics
description: |
  Implements domain-specific KPI metrics for business operations like charges, invoices, payments. Use when instrumenting service layer operations, measuring business process outcomes, implementing SLI/SLO monitoring for KPIs, or tracking supplier/invoice/charge lifecycle events. Targets Java/Spring Boot services with structured business metrics for observability.
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
---

# Micrometer Business Metrics

## Table of Contents

1. [Purpose](#purpose)
2. [When to Use](#when-to-use)
3. [Quick Start](#quick-start)
4. [Instructions](#instructions)
5. [Examples](#examples)
6. [Requirements](#requirements)
7. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
8. [See Also](#see-also)

---

## Purpose

While technical metrics (latency, errors, resource usage) measure system health, business metrics measure business outcomes. This skill shows how to instrument domain entities (Charges, Invoices, Suppliers, Payments) with meaningful KPI metrics that track business impact.

## When to Use

Use this skill when you need to:

- **Track business KPIs** - Measure charges processed, invoices generated, payments completed, supplier onboarding
- **Instrument service layer operations** - Add metrics at domain service level (not infrastructure)
- **Monitor business process outcomes** - Track approval rates, rejection reasons, processing times
- **Implement SLI/SLO for business metrics** - Define service levels based on business value (e.g., 99% of charges approved in 5 minutes)
- **Correlate business and technical metrics** - Link business outcomes to system performance
- **Create executive dashboards** - Provide business-oriented observability (revenue, transactions, customer impact)
- **Track domain entity lifecycles** - Monitor state transitions (created → approved → invoiced → paid)

**When NOT to use:**
- For purely technical metrics (use `python-micrometer-core` instead)
- For high-cardinality user/request tracking (use distributed tracing instead)
- When metrics backend isn't configured (use `python-micrometer-metrics-setup` first)

---

## Quick Start

Create a dedicated metrics component for your domain:

```java
@Component
public class ChargeMetrics {

    private final Counter chargesReceived;
    private final Counter chargesApproved;
    private final Counter chargesFailed;
    private final Timer approvalDuration;
    private final DistributionSummary chargeValue;

    public ChargeMetrics(MeterRegistry registry) {
        this.chargesReceived = Counter.builder("charge.received")
            .description("Total charges received")
            .register(registry);

        this.chargesApproved = Counter.builder("charge.approved")
            .description("Charges approved for payment")
            .register(registry);

        this.chargesFailed = Counter.builder("charge.failed")
            .description("Charges that failed processing")
            .register(registry);

        this.approvalDuration = Timer.builder("charge.approval.duration")
            .description("Time from submission to approval")
            .register(registry);

        this.chargeValue = DistributionSummary.builder("charge.value")
            .baseUnit("GBP")
            .serviceLevelObjectives(10, 50, 100, 500, 1000)
            .register(registry);
    }

    // Public methods to record events
    public void recordChargeReceived(Charge charge) {
        chargesReceived.increment();
        chargeValue.record(charge.getAmount().doubleValue());
    }

    public void recordChargeApproved(Charge charge, Duration approvalTime) {
        chargesApproved.increment();
        approvalDuration.record(approvalTime);
    }

    public void recordChargeFailed(String reason) {
        chargesFailed.increment();
    }
}
```

## Instructions

### Step 1: Identify Business Metrics

List the key KPIs for your domain:

**Charges:**
- Count: received, approved, rejected, duplicates
- Values: distribution of charge amounts
- Duration: submission to approval time
- Status: by rejection reason (validation, duplicate, amount)

**Invoices:**
- Count: generated, sent, paid, outstanding
- Values: distribution of invoice amounts
- Duration: generation time, payment processing time
- Status: by invoice state (draft, sent, paid, overdue)

**Payments:**
- Count: pending, completed, failed
- Values: distribution of payment amounts
- Duration: request to completion time
- Method: by payment type (bank transfer, card, check)

**Suppliers:**
- Count: active, onboarded, inactive
- Values: by category (tier1, direct, international, standard)
- Duration: onboarding time
- Status: by registration state

### Step 2: Create Metrics Component

Design a reusable metrics holder for your domain entity:

```java
@Component
public class SupplierChargesMetrics {

    private final MeterRegistry registry;
    private final Logger log = LoggerFactory.getLogger(this.getClass());

    // Charge metrics
    private final Counter chargesReceived;
    private final Counter chargesApproved;
    private final Counter chargesRejected;
    private final DistributionSummary chargeValue;
    private final Timer chargeApprovalDuration;

    // Supplier metrics
    private final Gauge activeSuppliers;
    private final Counter suppliersOnboarded;

    // Invoice metrics
    private final Counter invoicesGenerated;
    private final Counter invoicesSent;
    private final DistributionSummary invoiceAmount;
    private final Timer invoiceGenerationTime;
    private final Gauge outstandingInvoices;

    // Payment metrics
    private final Counter paymentsPending;
    private final Counter paymentsCompleted;
    private final Counter paymentsFailed;
    private final Timer paymentDuration;

    public SupplierChargesMetrics(
            MeterRegistry registry,
            SupplierRepository supplierRepo,
            InvoiceRepository invoiceRepo) {

        this.registry = registry;

        // CHARGES
        this.chargesReceived = Counter.builder("charge.received")
            .description("Total charges received from suppliers")
            .register(registry);

        this.chargesApproved = Counter.builder("charge.approved")
            .description("Charges approved for payment")
            .register(registry);

        this.chargesRejected = Counter.builder("charge.rejected")
            .description("Charges rejected by validation")
            .register(registry);

        this.chargeValue = DistributionSummary.builder("charge.value")
            .baseUnit("GBP")
            .description("Distribution of charge values")
            .serviceLevelObjectives(10, 50, 100, 500, 1000, 5000)
            .register(registry);

        this.chargeApprovalDuration = Timer.builder("charge.approval.duration")
            .description("Time from submission to approval")
            .publishPercentiles(0.5, 0.95, 0.99)
            .register(registry);

        // SUPPLIERS
        this.activeSuppliers = Gauge.builder("supplier.active.count",
                                             supplierRepo,
                                             SupplierRepository::countActive)
            .description("Number of active suppliers")
            .register(registry);

        this.suppliersOnboarded = Counter.builder("supplier.onboarded")
            .description("New suppliers onboarded")
            .register(registry);

        // INVOICES
        this.invoicesGenerated = Counter.builder("invoice.generated")
            .description("Invoices generated")
            .register(registry);

        this.invoicesSent = Counter.builder("invoice.sent")
            .tag("channel", "email")
            .description("Invoices sent to suppliers")
            .register(registry);

        this.invoiceAmount = DistributionSummary.builder("invoice.amount")
            .baseUnit("GBP")
            .description("Invoice amount distribution")
            .serviceLevelObjectives(100, 500, 1000, 5000, 10000, 50000)
            .register(registry);

        this.invoiceGenerationTime = Timer.builder("invoice.generation.duration")
            .description("Invoice generation time")
            .publishPercentiles(0.95, 0.99)
            .register(registry);

        this.outstandingInvoices = Gauge.builder("invoice.outstanding",
                                                 invoiceRepo,
                                                 InvoiceRepository::countOutstanding)
            .description("Number of outstanding invoices")
            .register(registry);

        // PAYMENTS
        this.paymentsPending = Counter.builder("payment.pending")
            .description("Payments awaiting processing")
            .register(registry);

        this.paymentsCompleted = Counter.builder("payment.completed")
            .tag("method", "bank_transfer")
            .description("Payments successfully completed")
            .register(registry);

        this.paymentsFailed = Counter.builder("payment.failed")
            .description("Payment processing failures")
            .register(registry);

        this.paymentDuration = Timer.builder("payment.processing.duration")
            .description("Payment processing duration")
            .publishPercentiles(0.95, 0.99)
            .register(registry);
    }

    // CHARGE EVENT RECORDING
    public void recordChargeReceived(Charge charge) {
        chargesReceived.increment();
        chargeValue.record(charge.getAmount().doubleValue());
        log.debug("Charge received: {} GBP", charge.getAmount());
    }

    public void recordChargeApproved(Charge charge, Duration approvalTime) {
        chargesApproved.increment();
        chargeApprovalDuration.record(approvalTime);
        log.info("Charge approved in {} ms", approvalTime.toMillis());
    }

    public void recordChargeRejected(String reason) {
        // Normalize reason to bounded cardinality
        String normalizedReason = normalizeRejectionReason(reason);
        Counter.builder("charge.rejected")
            .tag("reason", normalizedReason)
            .register(registry)
            .increment();
        log.warn("Charge rejected: {}", normalizedReason);
    }

    // SUPPLIER EVENT RECORDING
    public void recordSupplierOnboarded() {
        suppliersOnboarded.increment();
        log.info("New supplier onboarded");
    }

    // INVOICE EVENT RECORDING
    public void recordInvoiceGenerated(Invoice invoice) {
        invoicesGenerated.increment();
        invoiceAmount.record(invoice.getTotalAmount().doubleValue());
    }

    public void recordInvoiceGenerated(Invoice invoice, Duration generationTime) {
        invoicesGenerated.increment();
        invoiceAmount.record(invoice.getTotalAmount().doubleValue());
        invoiceGenerationTime.record(generationTime);
    }

    public void recordInvoiceSent(Invoice invoice) {
        invoicesSent.increment();
        log.info("Invoice {} sent", invoice.getId());
    }

    // PAYMENT EVENT RECORDING
    public void recordPaymentInitiated() {
        paymentsPending.increment();
    }

    public void recordPaymentCompleted(Duration processingTime, String method) {
        paymentsCompleted.increment();
        paymentDuration.record(processingTime);
        log.info("Payment completed via {} in {} ms", method, processingTime.toMillis());
    }

    public void recordPaymentFailed() {
        paymentsFailed.increment();
        log.warn("Payment processing failed");
    }

    // HELPER METHODS
    private String normalizeRejectionReason(String reason) {
        if (reason.contains("validation")) return "validation";
        if (reason.contains("duplicate")) return "duplicate";
        if (reason.contains("supplier")) return "supplier_issue";
        if (reason.contains("amount")) return "amount_issue";
        if (reason.contains("date")) return "date_issue";
        return "other";
    }
}
```

### Step 3: Integrate with Service Layer

Inject metrics into your service and record events at key decision points:

```java
@Service
public class ChargeProcessingService {

    private final ChargeRepository chargeRepository;
    private final SupplierChargesMetrics metrics;
    private final Tracer tracer;

    public ChargeProcessingService(
            ChargeRepository chargeRepository,
            SupplierChargesMetrics metrics,
            Tracer tracer) {
        this.chargeRepository = chargeRepository;
        this.metrics = metrics;
        this.tracer = tracer;
    }

    public void processCharge(Charge charge) {
        Instant startTime = Instant.now();
        metrics.recordChargeReceived(charge);

        Span span = tracer.currentSpan();
        span.setAttribute("charge.id", charge.getId());
        span.setAttribute("supplier.id", charge.getSupplierId());

        try {
            validateCharge(charge);
            approveCharge(charge);

            Duration approvalTime = Duration.between(startTime, Instant.now());
            metrics.recordChargeApproved(charge, approvalTime);

            span.setAttribute("charge.status", "approved");

        } catch (ValidationException e) {
            metrics.recordChargeRejected(e.getMessage());
            span.setAttribute("charge.status", "rejected");
            span.setAttribute("rejection.reason", e.getMessage());
            throw e;
        } catch (Exception e) {
            span.recordException(e);
            throw e;
        }
    }
}
```

### Step 4: Record State Changes

Track state transitions as business events:

```java
@Service
public class InvoiceService {

    private final InvoiceRepository invoiceRepository;
    private final SupplierChargesMetrics metrics;

    public Invoice generateInvoice(List<Charge> charges) {
        Instant startTime = Instant.now();

        Invoice invoice = createInvoiceFromCharges(charges);
        invoiceRepository.save(invoice);

        Duration generationTime = Duration.between(startTime, Instant.now());
        metrics.recordInvoiceGenerated(invoice, generationTime);

        return invoice;
    }

    public void sendInvoice(Invoice invoice) {
        emailService.send(invoice.getSupplierId(), invoice);
        invoiceRepository.markAsSent(invoice.getId());

        metrics.recordInvoiceSent(invoice);
    }

    public void recordInvoicePayment(Invoice invoice, Payment payment) {
        invoiceRepository.markAsPaid(invoice.getId(), payment.getId());

        // Record payment metrics
        Duration processingTime = Duration.between(
            invoice.getGeneratedAt(),
            Instant.now()
        );
        metrics.recordPaymentCompleted(processingTime, payment.getMethod());
    }
}
```

### Step 5: Add SLI/SLO Context

Associate business metrics with service level objectives:

```java
@Configuration
public class BusinessMetricsSLOConfig {

    @Bean
    public MeterRegistryCustomizer<MeterRegistry> businessMetricsSLO() {
        return registry -> {
            // SLO: 99% of charges approved within 5 minutes
            registry.config().meterFilter(
                new MeterFilter() {
                    @Override
                    public DistributionStatisticConfig configure(
                            Meter.Id id,
                            DistributionStatisticConfig config) {

                        if (id.getName().equals("charge.approval.duration")) {
                            return DistributionStatisticConfig.builder()
                                .percentilesHistogram(true)
                                .serviceLevelObjectives(
                                    Duration.ofSeconds(30).toNanos(),
                                    Duration.ofSeconds(60).toNanos(),
                                    Duration.ofMinutes(5).toNanos()
                                )
                                .build()
                                .merge(config);
                        }

                        // SLO: 95th percentile invoice generation < 10 seconds
                        if (id.getName().equals("invoice.generation.duration")) {
                            return DistributionStatisticConfig.builder()
                                .percentilesHistogram(true)
                                .serviceLevelObjectives(
                                    Duration.ofMillis(500).toNanos(),
                                    Duration.ofSeconds(1).toNanos(),
                                    Duration.ofSeconds(10).toNanos()
                                )
                                .build()
                                .merge(config);
                        }

                        return config;
                    }
                }
            );
        };
    }
}
```

## Examples

### Example 1: Payment Processing Metrics

```java
@Service
public class PaymentProcessingService {

    private final PaymentGateway paymentGateway;
    private final SupplierChargesMetrics metrics;

    public void processPayment(Invoice invoice) {
        metrics.recordPaymentInitiated();

        Instant startTime = Instant.now();

        try {
            paymentGateway.submit(
                invoice.getSupplierId(),
                invoice.getAmount(),
                invoice.getId()
            );

            Duration processingTime = Duration.between(startTime, Instant.now());
            metrics.recordPaymentCompleted(processingTime, "bank_transfer");

        } catch (PaymentGatewayException e) {
            metrics.recordPaymentFailed();
            throw e;
        }
    }
}
```

### Example 2: Supplier Lifecycle Metrics

```java
@Service
public class SupplierOnboardingService {

    private final SupplierRepository supplierRepository;
    private final SupplierChargesMetrics metrics;

    public void onboardSupplier(SupplierRegistration registration) {
        Supplier supplier = new Supplier(
            registration.getName(),
            registration.getAddress(),
            registration.getPaymentDetails()
        );

        supplierRepository.save(supplier);
        metrics.recordSupplierOnboarded();

        // Gauge will automatically report active supplier count
        // No need to explicitly record it each time
    }
}
```

### Example 3: Charge Rejection Tracking

Categorize rejections to detect systemic issues:

```java
public void recordChargeRejected(Charge charge, ValidationError error) {
    String reason;

    if (error instanceof DuplicateChargeError) {
        reason = "duplicate";
    } else if (error instanceof AmountValidationError) {
        reason = "amount_issue";
    } else if (error instanceof SupplierMissingError) {
        reason = "supplier_issue";
    } else {
        reason = "validation";
    }

    metrics.recordChargeRejected(reason);
}
```

## Requirements

- Spring Boot 2.1+ (auto-configures `MeterRegistry`)
- `spring-boot-starter-actuator` dependency
- Java 11+
- Domain model classes (Charge, Invoice, Supplier, Payment)
- Repository classes for Gauge-based metrics

## Anti-Patterns to Avoid

```java
// ❌ Recording metrics without context
metrics.recordCharge();  // When? Why did it fail?

// ✅ Record with full context
metrics.recordChargeReceived(charge);      // Records amount too
metrics.recordChargeRejected("duplicate"); // Normalized reason
metrics.recordChargeApproved(charge, approvalTime);

// ❌ Spreading metrics across many places
// service → repo → DAO → database (confusing ownership)

// ✅ Centralized metrics in one place
SupplierChargesMetrics.recordChargeApproved(charge, time);

// ❌ Missing state transitions
// Created → Approved (no intermediate states recorded)

// ✅ Record all meaningful state changes
metrics.recordChargeReceived(charge);
metrics.recordChargeApproved(charge, time);
metrics.recordInvoiceGenerated(invoice, time);
metrics.recordInvoiceSent(invoice);
metrics.recordPaymentCompleted(payment, time);
```

## See Also

- [python-micrometer-cardinality-control](../python-micrometer-cardinality-control/SKILL.md) - Prevent metric explosion
- [python-test-micrometer-testing-metrics](../python-test-micrometer-testing-metrics/SKILL.md) - Testing business metrics
- [python-micrometer-metrics-setup](../python-micrometer-metrics-setup/SKILL.md) - Initial configuration

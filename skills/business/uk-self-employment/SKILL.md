---
name: uk-self-employment
description: "[Extends uk-accountant] UK self-employment accounting specialist. Use for SA103 form mapping, self-employed tax calculations, Class 4 NI, allowable expenses, MTD quarterly submissions. Invoke alongside uk-accountant for self-employment software."
---

# UK Self-Employment Accounting

> **Extends:** uk-accountant
> **Type:** Specialized Skill

## Trigger

Use this skill alongside `uk-accountant` when:
- Building self-employment accounting software
- Mapping expenses to SA103 form boxes
- Calculating self-employment tax (Income Tax + Class 4 NI)
- Implementing Making Tax Digital (MTD) compliance
- Validating allowable business expenses
- Generating quarterly/annual summaries
- Advising on self-employment tax rules

## Context

You are a Senior UK Accountant specializing in self-employment taxation with 15+ years of experience advising sole traders, freelancers, and small business owners. You have deep expertise in Self Assessment (SA103), Making Tax Digital, and the specific rules that apply to self-employed individuals. You understand both the accounting requirements and how to implement them in software.

## Expertise

### Tax Years

| Tax Year | Start | End | Filing Deadline | Payment Deadline | MTD ITSA |
|----------|-------|-----|-----------------|------------------|----------|
| 2024/25 | 6 Apr 2024 | 5 Apr 2025 | 31 Jan 2026 | 31 Jan 2026 | No |
| 2025/26 *(current)* | 6 Apr 2025 | 5 Apr 2026 | 31 Jan 2027 | 31 Jan 2027 | No |
| 2026/27 | 6 Apr 2026 | 5 Apr 2027 | 31 Jan 2028 | 31 Jan 2028 | Yes (>£50k) |
| 2027/28 | 6 Apr 2027 | 5 Apr 2028 | 31 Jan 2029 | 31 Jan 2029 | Yes (>£30k) |

### SA103 Form Mapping

The SA103 (Self-Employment Full) form is used to report self-employment income and expenses.

#### Income Boxes

| Box | Field | Description | Software Field |
|-----|-------|-------------|----------------|
| 9 | Turnover | Total business income/sales | `income.turnover` |
| 10 | Other business income | Grants, Covid support, other | `income.other` |

#### Expense Boxes

| Box | Field | HMRC Description | Software Category |
|-----|-------|------------------|-------------------|
| 10 | Cost of sales | Goods bought for resale or materials | `COST_OF_SALES` |
| 11 | Construction | CIS subcontractor costs | `CONSTRUCTION_COSTS` |
| 12 | Wages | Staff wages, salaries, pensions | `WAGES_STAFF` |
| 13 | Car/Van/Travel | Vehicle costs, public transport | `CAR_VAN_TRAVEL` |
| 14 | Rent/Rates/Power | Premises costs | `RENT_RATES_POWER` |
| 15 | Repairs | Equipment/property maintenance | `REPAIRS_MAINTENANCE` |
| 16 | Phone/Office | Communication, stationery | `PHONE_OFFICE` |
| 17 | Advertising | Marketing, business entertainment | `ADVERTISING` |
| 18 | Interest | Loan interest payments | `INTEREST_FINANCE` |
| 19 | Bank charges | Financial charges | `BANK_CHARGES` |
| 20 | Bad debts | Irrecoverable debts | `IRRECOVERABLE_DEBTS` |
| 21 | Professional | Accountant, legal fees | `ACCOUNTANCY_LEGAL` |
| 22 | Depreciation | **NOT allowable** - use capital allowances | `DEPRECIATION` |
| 23 | Other | Anything not listed above | `OTHER_EXPENSES` |

#### Calculated Boxes

| Box | Field | Calculation |
|-----|-------|-------------|
| 24 | Total expenses | Sum of boxes 10-23 |
| 25 | Capital allowances | Separate calculation |
| 26 | Net profit | Income - Expenses - Capital Allowances |
| 27 | Net loss | If Box 26 is negative |

### Implementation: Expense Categories

```java
public enum ExpenseCategory {
    // SA103 mapped categories
    COST_OF_SALES("Cost of goods bought for resale", "box_10", true,
        List.of("stock", "materials", "raw materials", "goods for resale")),

    CONSTRUCTION_COSTS("Construction industry subcontractor costs", "box_11", true,
        List.of("cis", "subcontractor", "construction")),

    WAGES_STAFF("Wages, salaries and other staff costs", "box_12", true,
        List.of("wages", "salary", "pension", "employee", "staff")),

    CAR_VAN_TRAVEL("Car, van and travel expenses", "box_13", true,
        List.of("fuel", "petrol", "diesel", "mileage", "train", "bus", "parking", "toll")),

    RENT_RATES_POWER("Rent, rates, power and insurance costs", "box_14", true,
        List.of("rent", "rates", "electricity", "gas", "water", "insurance", "council tax")),

    REPAIRS_MAINTENANCE("Repairs and maintenance", "box_15", true,
        List.of("repairs", "maintenance", "servicing")),

    PHONE_OFFICE("Phone, fax, stationery and office costs", "box_16", true,
        List.of("phone", "mobile", "internet", "broadband", "stationery", "printer")),

    ADVERTISING("Advertising and business entertainment", "box_17", true,
        List.of("advertising", "marketing", "website", "domain", "hosting", "seo")),

    INTEREST_FINANCE("Interest on bank and other loans", "box_18", true,
        List.of("loan interest", "mortgage interest", "finance charges")),

    BANK_CHARGES("Bank, credit card and financial charges", "box_19", true,
        List.of("bank charges", "transaction fees", "payment processing")),

    IRRECOVERABLE_DEBTS("Irrecoverable debts written off", "box_20", true,
        List.of("bad debt", "written off")),

    ACCOUNTANCY_LEGAL("Accountancy, legal and professional fees", "box_21", true,
        List.of("accountant", "legal", "solicitor", "consultant", "professional")),

    DEPRECIATION("Depreciation", "box_22", false, // NOT allowable
        List.of("depreciation")),

    OTHER_EXPENSES("Other business expenses", "box_23", true,
        List.of("subscriptions", "memberships", "training", "books"));

    private final String description;
    private final String sa103Box;
    private final boolean taxDeductible;
    private final List<String> keywords;

    /**
     * Suggest category based on expense description.
     */
    public static Optional<ExpenseCategory> suggestCategory(String description) {
        String lower = description.toLowerCase();
        return Arrays.stream(values())
            .filter(cat -> cat.keywords.stream().anyMatch(lower::contains))
            .findFirst();
    }
}
```

### Tax Calculation Engine

#### Tax Rates (2025/26)

```java
public class TaxRates2025_26 implements TaxRates {

    // Personal Allowance
    public static final Money PERSONAL_ALLOWANCE = Money.of(12_570);
    public static final Money PA_TAPER_THRESHOLD = Money.of(100_000);
    public static final BigDecimal PA_TAPER_RATE = new BigDecimal("0.50");

    // Income Tax Bands
    public static final TaxBand BASIC_RATE = TaxBand.of(
        Money.ZERO, Money.of(37_700), new BigDecimal("0.20")
    );
    public static final TaxBand HIGHER_RATE = TaxBand.of(
        Money.of(37_700), Money.of(125_140), new BigDecimal("0.40")
    );
    public static final TaxBand ADDITIONAL_RATE = TaxBand.of(
        Money.of(125_140), Money.UNLIMITED, new BigDecimal("0.45")
    );

    // National Insurance Class 4
    public static final Money NI_LOWER_PROFITS_LIMIT = Money.of(12_570);
    public static final Money NI_UPPER_PROFITS_LIMIT = Money.of(50_270);
    public static final BigDecimal NI_MAIN_RATE = new BigDecimal("0.06"); // 6%
    public static final BigDecimal NI_ADDITIONAL_RATE = new BigDecimal("0.02"); // 2%

    // National Insurance Class 2 (voluntary from April 2024)
    public static final Money NI_CLASS_2_SMALL_PROFITS_THRESHOLD = Money.of(6_845);
    public static final Money NI_CLASS_2_WEEKLY = Money.of(3.50); // Updated for 2025/26
}
```

#### Tax Calculator

```java
@ApplicationScoped
public class SelfEmploymentTaxCalculator {

    @Inject
    TaxRatesProvider taxRatesProvider;

    public TaxCalculation calculate(TaxableIncome income, TaxYear taxYear) {
        TaxRates rates = taxRatesProvider.getRatesForYear(taxYear);

        // Calculate Personal Allowance (with taper if over £100k)
        Money personalAllowance = calculatePersonalAllowance(
            income.totalIncome(), rates
        );

        // Calculate taxable income after Personal Allowance
        Money taxableIncome = income.totalIncome()
            .subtract(personalAllowance)
            .max(Money.ZERO);

        // Calculate Income Tax
        TaxBreakdown incomeTax = calculateIncomeTax(taxableIncome, rates);

        // Calculate National Insurance Class 4
        TaxBreakdown niClass4 = calculateNIClass4(income.selfEmploymentProfit(), rates);

        // Calculate National Insurance Class 2
        Money niClass2 = calculateNIClass2(income.selfEmploymentProfit(), rates);

        return TaxCalculation.builder()
            .taxYear(taxYear)
            .totalIncome(income.totalIncome())
            .personalAllowance(personalAllowance)
            .taxableIncome(taxableIncome)
            .incomeTax(incomeTax)
            .niClass4(niClass4)
            .niClass2(niClass2)
            .totalTaxDue(incomeTax.total().add(niClass4.total()).add(niClass2))
            .build();
    }

    private Money calculatePersonalAllowance(Money totalIncome, TaxRates rates) {
        if (totalIncome.isLessThanOrEqual(rates.paTaperThreshold())) {
            return rates.personalAllowance();
        }

        // Reduce PA by £1 for every £2 over £100,000
        Money excess = totalIncome.subtract(rates.paTaperThreshold());
        Money reduction = excess.multiply(rates.paTaperRate());
        Money reducedPA = rates.personalAllowance().subtract(reduction);

        return reducedPA.max(Money.ZERO);
    }

    private TaxBreakdown calculateIncomeTax(Money taxableIncome, TaxRates rates) {
        List<TaxBandResult> bands = new ArrayList<>();
        Money remaining = taxableIncome;

        for (TaxBand band : rates.incomeTaxBands()) {
            if (remaining.isZero()) break;

            Money bandWidth = band.upperLimit().subtract(band.lowerLimit());
            Money taxableInBand = remaining.min(bandWidth);
            Money taxInBand = taxableInBand.multiply(band.rate());

            bands.add(new TaxBandResult(band.name(), taxableInBand, band.rate(), taxInBand));
            remaining = remaining.subtract(taxableInBand);
        }

        Money total = bands.stream()
            .map(TaxBandResult::tax)
            .reduce(Money.ZERO, Money::add);

        return new TaxBreakdown(bands, total);
    }

    private TaxBreakdown calculateNIClass4(Money profit, TaxRates rates) {
        List<TaxBandResult> bands = new ArrayList<>();

        // Main rate: 6% on profits between £12,570 and £50,270
        if (profit.isGreaterThan(rates.niLowerProfitsLimit())) {
            Money mainBandProfit = profit
                .min(rates.niUpperProfitsLimit())
                .subtract(rates.niLowerProfitsLimit())
                .max(Money.ZERO);

            Money mainRateTax = mainBandProfit.multiply(rates.niMainRate());
            bands.add(new TaxBandResult("Main Rate (6%)", mainBandProfit,
                rates.niMainRate(), mainRateTax));
        }

        // Additional rate: 2% on profits over £50,270
        if (profit.isGreaterThan(rates.niUpperProfitsLimit())) {
            Money additionalProfit = profit.subtract(rates.niUpperProfitsLimit());
            Money additionalTax = additionalProfit.multiply(rates.niAdditionalRate());
            bands.add(new TaxBandResult("Additional Rate (2%)", additionalProfit,
                rates.niAdditionalRate(), additionalTax));
        }

        Money total = bands.stream()
            .map(TaxBandResult::tax)
            .reduce(Money.ZERO, Money::add);

        return new TaxBreakdown(bands, total);
    }

    private Money calculateNIClass2(Money profit, TaxRates rates) {
        // Class 2 NI: £3.45/week if profit > £12,570
        if (profit.isGreaterThan(rates.niClass2Threshold())) {
            return rates.niClass2Weekly().multiply(52);
        }
        return Money.ZERO;
    }
}
```

### Allowable Expenses Guide

#### Definitely Allowable

| Category | Examples | Notes |
|----------|----------|-------|
| **Office costs** | Stationery, phone, software | Proportion if mixed use |
| **Travel** | Fuel, train, parking, hotels | Business journeys only |
| **Staff** | Wages, NI, pensions | Including yourself for pension |
| **Stock** | Materials, goods for resale | Cost only, not markup |
| **Professional** | Accountant, legal, insurance | Must be for business |
| **Marketing** | Advertising, website, PR | Not client entertainment |
| **Premises** | Rent, rates, utilities | Proportion if home office |
| **Financial** | Bank charges, loan interest | Business accounts only |

#### NOT Allowable

| Category | Why Not | Alternative |
|----------|---------|-------------|
| **Personal expenses** | Not for business | Separate personal/business |
| **Client entertainment** | Specifically disallowed | Staff entertainment OK |
| **Fines/penalties** | Public policy | None |
| **Depreciation** | Accounting concept | Use Capital Allowances |
| **Drawings** | Not an expense | Personal income |
| **Home costs (full)** | Part personal | Use simplified expenses |

#### Simplified Expenses (Flat Rates)

```java
public class SimplifiedExpenses {

    // Working from home (hours/month)
    public static final Map<Integer, Money> HOME_OFFICE_RATES = Map.of(
        25, Money.of(10),  // 25-50 hours: £10/month
        51, Money.of(18),  // 51-100 hours: £18/month
        101, Money.of(26)  // 101+ hours: £26/month
    );

    // HMRC Approved Mileage Rates (2025/26 - unchanged)
    public static final Money CAR_MILEAGE_FIRST_10000 = Money.of(0.45);
    public static final Money CAR_MILEAGE_AFTER_10000 = Money.of(0.25);
    public static final Money MOTORCYCLE_MILEAGE = Money.of(0.24);
    public static final Money BICYCLE_MILEAGE = Money.of(0.20);

    /**
     * Calculate simplified home office deduction.
     */
    public Money calculateHomeOffice(int hoursPerMonth, int months) {
        Money monthlyRate = HOME_OFFICE_RATES.entrySet().stream()
            .filter(e -> hoursPerMonth >= e.getKey())
            .max(Map.Entry.comparingByKey())
            .map(Map.Entry::getValue)
            .orElse(Money.ZERO);

        return monthlyRate.multiply(months);
    }

    /**
     * Calculate mileage deduction using HMRC approved rates.
     */
    public Money calculateMileage(int businessMiles, VehicleType type) {
        return switch (type) {
            case CAR, VAN -> {
                int first10k = Math.min(businessMiles, 10_000);
                int after10k = Math.max(businessMiles - 10_000, 0);
                yield CAR_MILEAGE_FIRST_10000.multiply(first10k)
                    .add(CAR_MILEAGE_AFTER_10000.multiply(after10k));
            }
            case MOTORCYCLE -> MOTORCYCLE_MILEAGE.multiply(businessMiles);
            case BICYCLE -> BICYCLE_MILEAGE.multiply(businessMiles);
        };
    }
}
```

### MTD Quarterly Periods

```java
public record QuarterlyPeriod(
    int quarter,
    LocalDate start,
    LocalDate end,
    LocalDate deadline
) {
    public static List<QuarterlyPeriod> forTaxYear(TaxYear year) {
        int startYear = year.startYear();
        return List.of(
            new QuarterlyPeriod(1,
                LocalDate.of(startYear, 4, 6),
                LocalDate.of(startYear, 7, 5),
                LocalDate.of(startYear, 8, 5)),
            new QuarterlyPeriod(2,
                LocalDate.of(startYear, 7, 6),
                LocalDate.of(startYear, 10, 5),
                LocalDate.of(startYear, 11, 5)),
            new QuarterlyPeriod(3,
                LocalDate.of(startYear, 10, 6),
                LocalDate.of(startYear + 1, 1, 5),
                LocalDate.of(startYear + 1, 2, 5)),
            new QuarterlyPeriod(4,
                LocalDate.of(startYear + 1, 1, 6),
                LocalDate.of(startYear + 1, 4, 5),
                LocalDate.of(startYear + 1, 5, 5))
        );
    }
}
```

### Record Retention

| Record Type | Minimum Retention |
|-------------|-------------------|
| Income records | 5 years from 31 Jan filing deadline |
| Expense records | 5 years from 31 Jan filing deadline |
| Bank statements | 5 years |
| Receipts | 5 years |
| Mileage logs | 5 years |
| Asset records | Until disposal + 5 years |

### Penalties

| Offence | Penalty |
|---------|---------|
| Late filing (initial) | £100 |
| Late filing (3 months) | £10/day (max 90 days = £900) |
| Late filing (6 months) | Greater of £300 or 5% of tax due |
| Late filing (12 months) | Greater of £300 or 5% of tax due |
| Late payment (30 days) | 5% of unpaid tax |
| Late payment (6 months) | Additional 5% |
| Late payment (12 months) | Additional 5% |
| Careless error | 0-30% of tax underpaid |
| Deliberate error | 20-70% of tax underpaid |
| Deliberate + concealment | 30-100% of tax underpaid |

## Parent & Related Skills

| Skill | Relationship |
|-------|--------------|
| **uk-accountant** | Parent skill - general UK accounting |
| **hmrc-api-specialist** | For MTD API integration |
| **backend-developer** | For implementing calculations |
| **uk-legal-counsel** | For compliance, disclaimers |

## Standards

- **Accuracy**: All calculations must match HMRC examples exactly
- **Currency**: Use 2 decimal places, round half-up
- **Tax Year Aware**: All calculations must be tax-year specific
- **Audit Trail**: Log all calculations for compliance
- **Disclaimers**: Always recommend professional advice for complex situations

## Checklist

### Before Implementation
- [ ] Tax rates verified against HMRC guidance
- [ ] SA103 mapping validated
- [ ] Expense categories complete
- [ ] Simplified expenses included

### Before Release
- [ ] Calculations match HMRC examples
- [ ] Edge cases tested (PA taper, loss carry-forward)
- [ ] Disclaimers implemented
- [ ] Record retention guidance shown

## Anti-Patterns to Avoid

1. **Hardcoded rates**: Tax rates change - use configuration
2. **Ignoring tax years**: Rates differ by year
3. **Rounding errors**: Use proper Money type
4. **Missing disclaimers**: Users must verify calculations
5. **No audit trail**: Required for compliance
6. **Advising on complex matters**: Recommend accountant

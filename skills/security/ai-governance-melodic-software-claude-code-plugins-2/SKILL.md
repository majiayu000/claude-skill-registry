---
name: ai-governance
description: AI governance and compliance guidance covering EU AI Act risk classification, NIST AI RMF, responsible AI principles, AI ethics review, and regulatory compliance for AI systems.
allowed-tools: Read, Glob, Grep, Task
---

# AI Governance

Comprehensive guidance for AI governance, regulatory compliance, and responsible AI practices, including EU AI Act and NIST AI Risk Management Framework.

## When to Use This Skill

- Classifying AI systems under EU AI Act risk categories
- Conducting AI risk assessments using NIST AI RMF
- Implementing responsible AI principles
- Preparing for AI compliance audits
- Creating AI system documentation and model cards
- Establishing AI governance frameworks
- Conducting AI ethics reviews

## Quick Reference

### EU AI Act Risk Classification

| Risk Level | Description | Examples | Requirements |
|------------|-------------|----------|--------------|
| **Unacceptable** | Prohibited practices | Social scoring, subliminal manipulation, exploitation of vulnerabilities | Banned outright |
| **High-Risk** | Safety/rights impact | Employment AI, credit scoring, biometric ID, critical infrastructure | Strict compliance |
| **Limited Risk** | Transparency needed | Chatbots, emotion recognition, deepfakes | Disclosure required |
| **Minimal Risk** | Low/no regulation | Spam filters, game AI, recommendation systems | Voluntary codes |

### NIST AI RMF Functions

| Function | Purpose | Key Activities |
|----------|---------|----------------|
| **Govern** | Cultivate risk culture | Policies, accountability, governance structures |
| **Map** | Understand context | Stakeholders, impacts, constraints, requirements |
| **Measure** | Assess and track | Risk metrics, testing, monitoring, evaluation |
| **Manage** | Prioritize and act | Mitigations, responses, documentation |

### Responsible AI Principles

| Principle | Description | Implementation |
|-----------|-------------|----------------|
| **Fairness** | Equitable treatment, bias mitigation | Fairness metrics, bias testing, diverse data |
| **Transparency** | Explainable decisions | XAI methods, model cards, documentation |
| **Accountability** | Clear ownership and oversight | Governance roles, audit trails, escalation |
| **Privacy** | Data protection, consent | PII handling, anonymization, consent management |
| **Safety** | Reliable, secure operation | Testing, monitoring, incident response |
| **Human Oversight** | Meaningful human control | HITL design, override mechanisms, review |

## EU AI Act Compliance

### Prohibited AI Practices (Article 5)

```yaml
prohibited_practices:
  social_scoring:
    description: "General-purpose social credit systems"
    applies_to: "Public authorities scoring citizens"
    prohibition: "Absolute - no exceptions"

  subliminal_manipulation:
    description: "AI exploiting subconscious to cause harm"
    applies_to: "Systems using techniques beyond awareness"
    prohibition: "Absolute - no exceptions"

  vulnerability_exploitation:
    description: "AI exploiting age, disability, social situation"
    applies_to: "Systems targeting vulnerable groups"
    prohibition: "Absolute - no exceptions"

  real_time_biometric_identification:
    description: "Remote biometric ID in public spaces"
    applies_to: "Law enforcement use"
    exceptions:
      - "Search for missing children"
      - "Prevention of terrorist attack"
      - "Identification of criminal suspects"
    authorization: "Prior judicial or administrative approval required"

  emotion_inference_workplace:
    description: "Emotion recognition in workplace/education"
    applies_to: "Employee/student monitoring"
    exceptions:
      - "Medical or safety purposes"

  predictive_policing:
    description: "Individual crime risk based solely on profiling"
    applies_to: "Law enforcement prediction"
    prohibition: "Absolute when based solely on profiling/traits"

  facial_recognition_scraping:
    description: "Untargeted facial image collection"
    applies_to: "Databases built from internet/CCTV scraping"
    prohibition: "Absolute - no exceptions"
```

### High-Risk AI Classification (Annex III)

```yaml
high_risk_categories:
  biometrics:
    - "Remote biometric identification systems"
    - "Biometric categorization (race, political, religion)"
    - "Emotion recognition systems"

  critical_infrastructure:
    - "Safety components in road traffic"
    - "Water, gas, heating, electricity management"
    - "Digital infrastructure safety components"

  education_training:
    - "Educational/vocational access decisions"
    - "Exam evaluation (learning outcomes)"
    - "Behavior assessment in institutions"

  employment:
    - "Recruitment and candidate filtering"
    - "Job advertisement targeting"
    - "Application evaluation"
    - "Promotion/termination decisions"
    - "Task allocation based on behavior/traits"
    - "Performance monitoring"

  essential_services:
    - "Credit scoring and creditworthiness"
    - "Risk assessment in life/health insurance"
    - "Emergency services dispatch prioritization"

  law_enforcement:
    - "Individual risk assessment (re-offending)"
    - "Polygraph and similar tools"
    - "Evidence reliability assessment"
    - "Crime prediction for individuals/groups"
    - "Profiling during investigations"

  migration_asylum:
    - "Polygraphs and similar at borders"
    - "Risk assessment (security, health, irregular entry)"
    - "Verification of travel document authenticity"
    - "Asylum/visa/residence application processing"

  justice_democracy:
    - "AI assisting judicial research/interpretation"
    - "AI assisting application of law to facts"
    - "Alternative dispute resolution"
    - "Election/referendum influence"
```

### High-Risk AI Requirements

```csharp
namespace Security.AIGovernance;

/// <summary>
/// EU AI Act high-risk AI system requirements.
/// </summary>
public static class HighRiskRequirements
{
    /// <summary>
    /// Risk management system requirements (Article 9).
    /// </summary>
    public static readonly RiskManagementRequirements RiskManagement = new(
        ContinuousProcess: true,
        IdentifyKnownRisks: true,
        EstimateRiskLevels: true,
        EvaluateEmergingRisks: true,
        AdoptMitigations: true,
        DocumentDecisions: true,
        TestingRequirements: [
            "Testing against defined metrics",
            "Testing with representative data",
            "Testing for foreseeable misuse",
            "Testing by independent parties where appropriate"
        ]
    );

    /// <summary>
    /// Data and data governance requirements (Article 10).
    /// </summary>
    public static readonly DataGovernanceRequirements DataGovernance = new(
        TrainingDataDocumentation: true,
        DataQualityManagement: true,
        BiasExamination: true,
        RelevanceVerification: true,
        RepresentativenessCheck: true,
        SpecialCategoryDataHandling: [
            "Strictly necessary for bias detection",
            "Subject to appropriate safeguards",
            "Not used for other purposes"
        ]
    );

    /// <summary>
    /// Technical documentation requirements (Article 11).
    /// </summary>
    public static readonly TechnicalDocumentationRequirements Documentation = new(
        GeneralDescription: true,
        IntendedPurpose: true,
        DesignSpecifications: true,
        SystemArchitecture: true,
        DataRequirements: true,
        TrainingMethodologies: true,
        ValidationProcedures: true,
        PerformanceMetrics: true,
        RiskManagementSystem: true,
        Cybersecurity: true,
        ModificationLog: true
    );

    /// <summary>
    /// Record-keeping requirements (Article 12).
    /// </summary>
    public static readonly RecordKeepingRequirements RecordKeeping = new(
        AutomaticLogging: true,
        OperationalLogs: true,
        IdentityOfUsers: true,
        DateTimeOfUse: true,
        ReferenceInputData: true,
        OutputData: true,
        RetentionPeriod: "Appropriate to intended purpose"
    );

    /// <summary>
    /// Transparency requirements (Article 13).
    /// </summary>
    public static readonly TransparencyRequirements Transparency = new(
        ClearInstructions: true,
        ProviderIdentity: true,
        SystemCapabilities: true,
        SystemLimitations: true,
        AccuracyLevels: true,
        ForeseeableRisks: true,
        HumanOversightMeasures: true,
        MaintenanceRequirements: true
    );

    /// <summary>
    /// Human oversight requirements (Article 14).
    /// </summary>
    public static readonly HumanOversightRequirements HumanOversight = new(
        DesignedForOversight: true,
        OperatorTools: [
            "Understand system capabilities and limitations",
            "Monitor operation correctly",
            "Detect automation bias",
            "Interpret outputs correctly",
            "Override or interrupt system",
            "Decide not to use or disregard output"
        ],
        Proportionate: "To risks and autonomy level"
    );
}

public sealed record RiskManagementRequirements(
    bool ContinuousProcess,
    bool IdentifyKnownRisks,
    bool EstimateRiskLevels,
    bool EvaluateEmergingRisks,
    bool AdoptMitigations,
    bool DocumentDecisions,
    string[] TestingRequirements);

public sealed record DataGovernanceRequirements(
    bool TrainingDataDocumentation,
    bool DataQualityManagement,
    bool BiasExamination,
    bool RelevanceVerification,
    bool RepresentativenessCheck,
    string[] SpecialCategoryDataHandling);

public sealed record TechnicalDocumentationRequirements(
    bool GeneralDescription,
    bool IntendedPurpose,
    bool DesignSpecifications,
    bool SystemArchitecture,
    bool DataRequirements,
    bool TrainingMethodologies,
    bool ValidationProcedures,
    bool PerformanceMetrics,
    bool RiskManagementSystem,
    bool Cybersecurity,
    bool ModificationLog);

public sealed record RecordKeepingRequirements(
    bool AutomaticLogging,
    bool OperationalLogs,
    bool IdentityOfUsers,
    bool DateTimeOfUse,
    bool ReferenceInputData,
    bool OutputData,
    string RetentionPeriod);

public sealed record TransparencyRequirements(
    bool ClearInstructions,
    bool ProviderIdentity,
    bool SystemCapabilities,
    bool SystemLimitations,
    bool AccuracyLevels,
    bool ForeseeableRisks,
    bool HumanOversightMeasures,
    bool MaintenanceRequirements);

public sealed record HumanOversightRequirements(
    bool DesignedForOversight,
    string[] OperatorTools,
    string Proportionate);
```

## NIST AI Risk Management Framework

### Govern Function

```yaml
govern_function:
  description: "Cultivate a culture of risk management"

  govern_1:
    name: "Policies and Procedures"
    activities:
      - "Establish AI governance policies"
      - "Define AI risk tolerances"
      - "Create AI development standards"
      - "Document ethical guidelines"
    outputs:
      - "AI governance policy"
      - "Risk appetite statement"
      - "Development standards"

  govern_2:
    name: "Accountability Structures"
    activities:
      - "Define AI ownership roles"
      - "Establish oversight committees"
      - "Create escalation paths"
      - "Assign compliance responsibilities"
    outputs:
      - "RACI matrix for AI systems"
      - "Governance org chart"
      - "Escalation procedures"

  govern_3:
    name: "Workforce Diversity"
    activities:
      - "Diverse team composition"
      - "Inclusive development practices"
      - "Bias awareness training"
      - "Cross-functional collaboration"
    outputs:
      - "Diversity metrics"
      - "Training records"
      - "Team composition reports"

  govern_4:
    name: "Organizational Culture"
    activities:
      - "Promote responsible AI values"
      - "Encourage ethical considerations"
      - "Support risk identification"
      - "Foster transparency"
    outputs:
      - "Culture assessment results"
      - "Ethics training completion"
      - "Feedback mechanisms"

  govern_5:
    name: "Stakeholder Engagement"
    activities:
      - "Identify affected stakeholders"
      - "Establish feedback channels"
      - "Incorporate stakeholder input"
      - "Communicate AI decisions"
    outputs:
      - "Stakeholder registry"
      - "Engagement records"
      - "Communication plan"

  govern_6:
    name: "Legal Compliance"
    activities:
      - "Map regulatory requirements"
      - "Monitor regulatory changes"
      - "Ensure compliance verification"
      - "Maintain audit readiness"
    outputs:
      - "Compliance matrix"
      - "Regulatory tracker"
      - "Audit schedules"
```

### Map Function

```yaml
map_function:
  description: "Understand the context and impacts"

  map_1:
    name: "Intended Purpose"
    activities:
      - "Document business objectives"
      - "Define use case boundaries"
      - "Identify target users"
      - "Specify deployment context"
    outputs:
      - "Use case specification"
      - "User personas"
      - "Deployment plan"

  map_2:
    name: "Categorization"
    activities:
      - "Classify AI system type"
      - "Determine risk category"
      - "Identify regulatory applicability"
      - "Assess criticality level"
    outputs:
      - "Risk classification"
      - "Regulatory mapping"
      - "Criticality assessment"

  map_3:
    name: "Impacts and Affected Parties"
    activities:
      - "Identify potential harms"
      - "Map affected populations"
      - "Assess differential impacts"
      - "Consider cumulative effects"
    outputs:
      - "Impact assessment"
      - "Affected party analysis"
      - "Equity considerations"

  map_4:
    name: "Dependencies"
    activities:
      - "Document data sources"
      - "Identify third-party components"
      - "Map system integrations"
      - "Assess supply chain risks"
    outputs:
      - "Dependency inventory"
      - "Third-party risk assessment"
      - "Integration diagram"

  map_5:
    name: "Risk Identification"
    activities:
      - "Enumerate potential risks"
      - "Consider failure modes"
      - "Assess adversarial threats"
      - "Evaluate misuse potential"
    outputs:
      - "Risk register"
      - "Threat model"
      - "Misuse scenarios"
```

### Measure Function

```yaml
measure_function:
  description: "Assess and track risks"

  measure_1:
    name: "Risk Metrics"
    activities:
      - "Define risk indicators"
      - "Establish measurement methods"
      - "Set thresholds and tolerances"
      - "Create monitoring dashboards"
    outputs:
      - "KRI definitions"
      - "Measurement protocols"
      - "Threshold documentation"

  measure_2:
    name: "Testing and Evaluation"
    activities:
      - "Conduct bias testing"
      - "Evaluate model performance"
      - "Test edge cases"
      - "Assess robustness"
    outputs:
      - "Test results"
      - "Performance metrics"
      - "Robustness report"

  measure_3:
    name: "Continuous Monitoring"
    activities:
      - "Monitor model drift"
      - "Track performance degradation"
      - "Detect anomalies"
      - "Log incidents"
    outputs:
      - "Monitoring reports"
      - "Drift analysis"
      - "Incident logs"

  measure_4:
    name: "Independent Assessment"
    activities:
      - "Conduct internal audits"
      - "Engage external reviewers"
      - "Facilitate red teaming"
      - "Perform algorithmic audits"
    outputs:
      - "Audit reports"
      - "External review findings"
      - "Red team results"
```

### Manage Function

```yaml
manage_function:
  description: "Prioritize and respond to risks"

  manage_1:
    name: "Risk Prioritization"
    activities:
      - "Rank risks by severity"
      - "Assess likelihood and impact"
      - "Prioritize mitigation efforts"
      - "Allocate resources"
    outputs:
      - "Prioritized risk register"
      - "Resource allocation plan"
      - "Mitigation roadmap"

  manage_2:
    name: "Risk Response"
    activities:
      - "Implement mitigations"
      - "Develop contingency plans"
      - "Create rollback procedures"
      - "Document decisions"
    outputs:
      - "Mitigation implementations"
      - "Contingency plans"
      - "Rollback procedures"

  manage_3:
    name: "Residual Risk"
    activities:
      - "Assess remaining risks"
      - "Obtain risk acceptance"
      - "Document limitations"
      - "Communicate constraints"
    outputs:
      - "Residual risk assessment"
      - "Risk acceptance records"
      - "Limitation documentation"

  manage_4:
    name: "Documentation and Communication"
    activities:
      - "Maintain risk documentation"
      - "Report to stakeholders"
      - "Share lessons learned"
      - "Update governance artifacts"
    outputs:
      - "Risk documentation"
      - "Stakeholder reports"
      - "Lessons learned"
```

## AI Risk Assessment

### Risk Classification Model

```csharp
namespace Security.AIGovernance;

/// <summary>
/// AI system risk classification and assessment.
/// </summary>
public sealed class AIRiskAssessment
{
    /// <summary>
    /// Classify AI system risk level based on characteristics.
    /// </summary>
    public static RiskClassification ClassifyRisk(AISystemCharacteristics system)
    {
        // Check for prohibited practices first
        if (IsProhibited(system))
        {
            return new RiskClassification(
                Level: RiskLevel.Unacceptable,
                Reasoning: "System falls under EU AI Act prohibited practices",
                Requirements: ["System must not be deployed"],
                ComplianceActions: ["Discontinue development", "Review for alternative approaches"]);
        }

        // Check for high-risk categories
        if (IsHighRisk(system))
        {
            return new RiskClassification(
                Level: RiskLevel.High,
                Reasoning: "System falls under EU AI Act Annex III high-risk categories",
                Requirements: [
                    "Implement risk management system",
                    "Ensure data governance",
                    "Create technical documentation",
                    "Implement logging and record-keeping",
                    "Ensure transparency to users",
                    "Enable human oversight",
                    "Ensure accuracy, robustness, cybersecurity",
                    "Conduct conformity assessment"
                ],
                ComplianceActions: GetHighRiskActions(system));
        }

        // Check for limited risk (transparency obligations)
        if (IsLimitedRisk(system))
        {
            return new RiskClassification(
                Level: RiskLevel.Limited,
                Reasoning: "System has transparency obligations",
                Requirements: [
                    "Disclose AI interaction to users",
                    "Label AI-generated content where applicable",
                    "Inform about emotion recognition/biometric categorization"
                ],
                ComplianceActions: ["Implement disclosure mechanisms", "Update user interfaces"]);
        }

        // Minimal/no risk
        return new RiskClassification(
            Level: RiskLevel.Minimal,
            Reasoning: "System does not fall under regulated categories",
            Requirements: ["Consider voluntary codes of conduct"],
            ComplianceActions: ["Document risk assessment decision", "Monitor for regulatory changes"]);
    }

    private static bool IsProhibited(AISystemCharacteristics system)
    {
        return system.UseCase switch
        {
            AIUseCase.SocialScoring => system.DeployedBy == DeploymentContext.PublicAuthority,
            AIUseCase.SubliminalManipulation => true,
            AIUseCase.VulnerabilityExploitation => true,
            AIUseCase.FacialRecognitionScraping => true,
            AIUseCase.PredictivePolicing => system.BasedSolelyOnProfiling,
            AIUseCase.EmotionRecognition => system.Context is DeploymentContext.Workplace or DeploymentContext.Education
                                            && !system.ForMedicalOrSafetyPurposes,
            _ => false
        };
    }

    private static bool IsHighRisk(AISystemCharacteristics system)
    {
        return system.Category is
            AICategory.Biometrics or
            AICategory.CriticalInfrastructure or
            AICategory.Education or
            AICategory.Employment or
            AICategory.EssentialServices or
            AICategory.LawEnforcement or
            AICategory.MigrationAsylum or
            AICategory.JusticeDemocracy;
    }

    private static bool IsLimitedRisk(AISystemCharacteristics system)
    {
        return system.UseCase is
            AIUseCase.Chatbot or
            AIUseCase.EmotionRecognition or
            AIUseCase.DeepfakeGeneration or
            AIUseCase.ContentGeneration;
    }

    private static string[] GetHighRiskActions(AISystemCharacteristics system)
    {
        var actions = new List<string>
        {
            "Establish risk management system",
            "Document training data governance",
            "Create technical documentation per Annex IV",
            "Implement automatic logging",
            "Create instructions for use",
            "Design for human oversight"
        };

        if (system.Category == AICategory.Biometrics)
        {
            actions.Add("Conduct fundamental rights impact assessment");
            actions.Add("Register in EU AI database");
        }

        return [.. actions];
    }
}

public sealed record AISystemCharacteristics(
    AICategory Category,
    AIUseCase UseCase,
    DeploymentContext Context,
    DeploymentContext? DeployedBy = null,
    bool BasedSolelyOnProfiling = false,
    bool ForMedicalOrSafetyPurposes = false);

public sealed record RiskClassification(
    RiskLevel Level,
    string Reasoning,
    string[] Requirements,
    string[] ComplianceActions);

public enum RiskLevel { Minimal, Limited, High, Unacceptable }

public enum AICategory
{
    Biometrics,
    CriticalInfrastructure,
    Education,
    Employment,
    EssentialServices,
    LawEnforcement,
    MigrationAsylum,
    JusticeDemocracy,
    General
}

public enum AIUseCase
{
    SocialScoring,
    SubliminalManipulation,
    VulnerabilityExploitation,
    FacialRecognitionScraping,
    PredictivePolicing,
    EmotionRecognition,
    BiometricIdentification,
    CreditScoring,
    RecruitmentScreening,
    PerformanceMonitoring,
    Chatbot,
    DeepfakeGeneration,
    ContentGeneration,
    RecommendationSystem,
    GameAI,
    SpamFilter,
    Other
}

public enum DeploymentContext
{
    PublicAuthority,
    PrivateSector,
    Workplace,
    Education,
    Healthcare,
    LawEnforcement,
    General
}
```

## Model Cards and Documentation

### Model Card Template

```yaml
model_card_template:
  model_details:
    name: ""
    version: ""
    type: "" # Classification, regression, generation, etc.
    developer: ""
    license: ""
    release_date: ""

  intended_use:
    primary_use_cases: []
    intended_users: []
    out_of_scope_uses: []

  factors:
    relevant_factors: []
    evaluation_factors: []

  metrics:
    performance_measures: []
    decision_thresholds: []
    variation_approaches: []

  evaluation_data:
    datasets: []
    motivation: ""
    preprocessing: ""

  training_data:
    datasets: []
    motivation: ""
    preprocessing: ""

  quantitative_analyses:
    unitary_results: []
    intersectional_results: []

  ethical_considerations:
    sensitive_use_cases: []
    known_limitations: []
    bias_mitigations: []

  caveats_recommendations:
    known_issues: []
    recommendations: []
    additional_testing: []
```

### AI System Documentation

```csharp
namespace Security.AIGovernance;

/// <summary>
/// AI system documentation for compliance and transparency.
/// </summary>
public sealed record AISystemDocumentation
{
    // General Description
    public required string SystemName { get; init; }
    public required string Version { get; init; }
    public required string Description { get; init; }
    public required string IntendedPurpose { get; init; }
    public required RiskLevel RiskClassification { get; init; }
    public required DateTimeOffset DocumentDate { get; init; }

    // Provider Information
    public required OrganizationInfo Provider { get; init; }
    public required ContactInfo TechnicalContact { get; init; }
    public required ContactInfo ComplianceContact { get; init; }

    // Technical Specifications
    public required SystemArchitecture Architecture { get; init; }
    public required ModelSpecification Model { get; init; }
    public required DataSpecification TrainingData { get; init; }
    public required PerformanceMetrics Performance { get; init; }

    // Risk Management
    public required RiskAssessment Risks { get; init; }
    public required MitigationMeasures Mitigations { get; init; }
    public required HumanOversightDesign HumanOversight { get; init; }

    // Compliance
    public required ComplianceStatus Compliance { get; init; }
    public required List<AuditRecord> AuditHistory { get; init; }
    public required List<string> ApplicableRegulations { get; init; }
}

public sealed record OrganizationInfo(
    string Name,
    string Address,
    string Country,
    string RegistrationNumber);

public sealed record ContactInfo(
    string Name,
    string Email,
    string Phone);

public sealed record SystemArchitecture(
    string Description,
    List<string> Components,
    List<string> ExternalDependencies,
    List<string> IntegrationPoints);

public sealed record ModelSpecification(
    string ModelType,
    string Algorithm,
    string Framework,
    string TrainingApproach,
    DateTimeOffset LastTrainingDate);

public sealed record DataSpecification(
    string DataSources,
    long RecordCount,
    string DataTypes,
    string QualityMeasures,
    string BiasAssessment,
    bool ContainsSensitiveData,
    string SensitiveDataHandling);

public sealed record PerformanceMetrics(
    Dictionary<string, double> Metrics,
    string EvaluationMethodology,
    string LimitationsAndFailureModes);

public sealed record RiskAssessment(
    List<IdentifiedRisk> Risks,
    string OverallRiskLevel,
    DateTimeOffset AssessmentDate);

public sealed record IdentifiedRisk(
    string Description,
    string Likelihood,
    string Impact,
    string MitigationStatus);

public sealed record MitigationMeasures(
    List<string> TechnicalMeasures,
    List<string> OrganizationalMeasures,
    List<string> MonitoringMeasures);

public sealed record HumanOversightDesign(
    string OversightModel, // Human-in-the-loop, human-on-the-loop, human-in-command
    List<string> OversightMechanisms,
    List<string> OverrideCapabilities,
    string TrainingRequirements);

public sealed record ComplianceStatus(
    bool EUAIActCompliant,
    string ConformityAssessmentStatus,
    string CertificationStatus,
    DateTimeOffset LastComplianceReview);

public sealed record AuditRecord(
    DateTimeOffset Date,
    string AuditType,
    string Auditor,
    string Findings,
    string CorrectiveActions);
```

## Compliance Checklists

### EU AI Act High-Risk Compliance Checklist

```yaml
eu_ai_act_high_risk_checklist:
  risk_management:
    - task: "Establish risk management system"
      status: "pending"
      evidence: ""
    - task: "Document known and foreseeable risks"
      status: "pending"
      evidence: ""
    - task: "Implement risk mitigation measures"
      status: "pending"
      evidence: ""
    - task: "Conduct testing for risk assessment"
      status: "pending"
      evidence: ""

  data_governance:
    - task: "Document training data sources"
      status: "pending"
      evidence: ""
    - task: "Implement data quality management"
      status: "pending"
      evidence: ""
    - task: "Conduct bias examination"
      status: "pending"
      evidence: ""
    - task: "Verify data representativeness"
      status: "pending"
      evidence: ""

  technical_documentation:
    - task: "Create Annex IV compliant documentation"
      status: "pending"
      evidence: ""
    - task: "Document system architecture"
      status: "pending"
      evidence: ""
    - task: "Document training methodology"
      status: "pending"
      evidence: ""
    - task: "Document performance metrics"
      status: "pending"
      evidence: ""

  record_keeping:
    - task: "Implement automatic logging"
      status: "pending"
      evidence: ""
    - task: "Log user interactions"
      status: "pending"
      evidence: ""
    - task: "Define retention periods"
      status: "pending"
      evidence: ""

  transparency:
    - task: "Create instructions for use"
      status: "pending"
      evidence: ""
    - task: "Document capabilities and limitations"
      status: "pending"
      evidence: ""
    - task: "Specify accuracy levels"
      status: "pending"
      evidence: ""

  human_oversight:
    - task: "Design oversight mechanisms"
      status: "pending"
      evidence: ""
    - task: "Implement override capabilities"
      status: "pending"
      evidence: ""
    - task: "Define operator training requirements"
      status: "pending"
      evidence: ""

  accuracy_robustness_cybersecurity:
    - task: "Validate performance metrics"
      status: "pending"
      evidence: ""
    - task: "Test for robustness"
      status: "pending"
      evidence: ""
    - task: "Conduct security assessment"
      status: "pending"
      evidence: ""

  conformity_assessment:
    - task: "Complete self-assessment or third-party assessment"
      status: "pending"
      evidence: ""
    - task: "Prepare EU declaration of conformity"
      status: "pending"
      evidence: ""
    - task: "Register in EU database (if applicable)"
      status: "pending"
      evidence: ""
```

### NIST AI RMF Implementation Checklist

```yaml
nist_ai_rmf_checklist:
  govern:
    - task: "Establish AI governance policies"
      status: "pending"
    - task: "Define accountability structures"
      status: "pending"
    - task: "Create risk management procedures"
      status: "pending"
    - task: "Establish stakeholder engagement processes"
      status: "pending"
    - task: "Map legal and regulatory requirements"
      status: "pending"

  map:
    - task: "Document intended purpose and use cases"
      status: "pending"
    - task: "Classify AI system by risk category"
      status: "pending"
    - task: "Identify potential impacts and affected parties"
      status: "pending"
    - task: "Document data and model dependencies"
      status: "pending"
    - task: "Identify and enumerate risks"
      status: "pending"

  measure:
    - task: "Define risk metrics and indicators"
      status: "pending"
    - task: "Conduct bias and fairness testing"
      status: "pending"
    - task: "Evaluate model performance"
      status: "pending"
    - task: "Implement continuous monitoring"
      status: "pending"
    - task: "Schedule independent assessments"
      status: "pending"

  manage:
    - task: "Prioritize risks by severity"
      status: "pending"
    - task: "Implement risk mitigations"
      status: "pending"
    - task: "Develop contingency and rollback plans"
      status: "pending"
    - task: "Document residual risks and acceptances"
      status: "pending"
    - task: "Establish ongoing communication processes"
      status: "pending"
```

## References

- **EU AI Act Details**: See `references/eu-ai-act-requirements.md` for full regulatory text mapping
- **NIST AI RMF**: See `references/nist-ai-rmf-profiles.md` for sector-specific profiles
- **Model Cards**: See `references/model-card-examples.md` for completed examples

## Related Skills

- `threat-modeling` - Security threat analysis for AI systems
- `devsecops-practices` - Integrating AI governance into pipelines
- `vulnerability-management` - Managing AI system vulnerabilities

---

**Last Updated:** 2025-12-26

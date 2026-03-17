---
name: "digital-maturity-assessment"
description: "Assess organization's digital transformation readiness. Evaluate data culture, technology adoption, and process maturity."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🎯", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Digital Maturity Assessment

## Business Case

### Problem Statement
Digital transformation challenges:
- Unclear current state of digitalization
- Difficulty prioritizing investments
- Lack of benchmarking capability
- No roadmap for improvement

### Solution
Comprehensive digital maturity assessment framework to evaluate technology adoption, data culture, and process maturity with actionable recommendations.

## Technical Implementation

```python
import pandas as pd
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class MaturityLevel(Enum):
    INITIAL = 1       # Ad-hoc, reactive
    DEVELOPING = 2    # Some processes defined
    DEFINED = 3       # Standardized processes
    MANAGED = 4       # Measured and controlled
    OPTIMIZING = 5    # Continuous improvement


class AssessmentDimension(Enum):
    STRATEGY = "strategy"
    TECHNOLOGY = "technology"
    DATA = "data"
    PROCESSES = "processes"
    PEOPLE = "people"
    CULTURE = "culture"


class SubDimension(Enum):
    # Strategy
    DIGITAL_VISION = "digital_vision"
    LEADERSHIP = "leadership"
    INVESTMENT = "investment"

    # Technology
    INFRASTRUCTURE = "infrastructure"
    SYSTEMS_INTEGRATION = "systems_integration"
    AUTOMATION = "automation"

    # Data
    DATA_QUALITY = "data_quality"
    DATA_GOVERNANCE = "data_governance"
    ANALYTICS = "analytics"

    # Processes
    STANDARDIZATION = "standardization"
    DIGITIZATION = "digitization"
    OPTIMIZATION = "optimization"

    # People
    SKILLS = "skills"
    TRAINING = "training"
    ADOPTION = "adoption"

    # Culture
    INNOVATION = "innovation"
    COLLABORATION = "collaboration"
    CHANGE_READINESS = "change_readiness"


@dataclass
class AssessmentQuestion:
    question_id: str
    dimension: AssessmentDimension
    sub_dimension: SubDimension
    question: str
    level_descriptions: Dict[int, str]
    weight: float = 1.0


@dataclass
class Response:
    question_id: str
    score: int  # 1-5
    notes: str = ""


@dataclass
class DimensionScore:
    dimension: AssessmentDimension
    score: float
    level: MaturityLevel
    sub_scores: Dict[str, float]
    gaps: List[str]
    recommendations: List[str]


class DigitalMaturityAssessment:
    """Assess organization's digital transformation readiness."""

    def __init__(self, organization_name: str):
        self.organization_name = organization_name
        self.questions: Dict[str, AssessmentQuestion] = {}
        self.responses: Dict[str, Response] = {}
        self.assessment_date = datetime.now()
        self._define_standard_questions()

    def _define_standard_questions(self):
        """Define standard assessment questions."""

        questions = [
            # Strategy
            AssessmentQuestion(
                "STR-01", AssessmentDimension.STRATEGY, SubDimension.DIGITAL_VISION,
                "Does the organization have a documented digital transformation strategy?",
                {
                    1: "No strategy exists",
                    2: "Informal ideas discussed",
                    3: "Strategy documented but not widely communicated",
                    4: "Strategy documented, communicated, and aligned with business goals",
                    5: "Strategy is continuously updated and drives all decisions"
                }, weight=1.5
            ),
            AssessmentQuestion(
                "STR-02", AssessmentDimension.STRATEGY, SubDimension.LEADERSHIP,
                "How engaged is leadership in digital initiatives?",
                {
                    1: "No leadership involvement",
                    2: "Occasional interest",
                    3: "Executive sponsor assigned",
                    4: "Active C-level championship",
                    5: "Digital-first mindset at all leadership levels"
                }, weight=1.5
            ),
            AssessmentQuestion(
                "STR-03", AssessmentDimension.STRATEGY, SubDimension.INVESTMENT,
                "What is the investment level in digital technologies?",
                {
                    1: "No dedicated budget",
                    2: "Ad-hoc project funding",
                    3: "Annual budget for digital projects",
                    4: "Multi-year investment plan",
                    5: "Strategic investment portfolio with ROI tracking"
                }, weight=1.0
            ),

            # Technology
            AssessmentQuestion(
                "TECH-01", AssessmentDimension.TECHNOLOGY, SubDimension.INFRASTRUCTURE,
                "What is the state of IT infrastructure?",
                {
                    1: "Legacy systems, no cloud",
                    2: "Some cloud adoption",
                    3: "Hybrid cloud environment",
                    4: "Cloud-first approach",
                    5: "Modern, scalable, secure infrastructure"
                }, weight=1.0
            ),
            AssessmentQuestion(
                "TECH-02", AssessmentDimension.TECHNOLOGY, SubDimension.SYSTEMS_INTEGRATION,
                "How well are systems integrated?",
                {
                    1: "Siloed systems, manual data transfer",
                    2: "Some point-to-point integrations",
                    3: "Integration middleware in place",
                    4: "API-based integration architecture",
                    5: "Real-time data flow across all systems"
                }, weight=1.2
            ),
            AssessmentQuestion(
                "TECH-03", AssessmentDimension.TECHNOLOGY, SubDimension.AUTOMATION,
                "What is the level of process automation?",
                {
                    1: "Manual processes only",
                    2: "Basic spreadsheet automation",
                    3: "Workflow automation tools in use",
                    4: "Robotic process automation (RPA)",
                    5: "AI-powered intelligent automation"
                }, weight=1.0
            ),

            # Data
            AssessmentQuestion(
                "DATA-01", AssessmentDimension.DATA, SubDimension.DATA_QUALITY,
                "How is data quality managed?",
                {
                    1: "No data quality processes",
                    2: "Reactive data cleaning",
                    3: "Data quality rules defined",
                    4: "Automated data quality monitoring",
                    5: "Continuous data quality improvement"
                }, weight=1.2
            ),
            AssessmentQuestion(
                "DATA-02", AssessmentDimension.DATA, SubDimension.DATA_GOVERNANCE,
                "What data governance is in place?",
                {
                    1: "No governance",
                    2: "Informal data ownership",
                    3: "Data governance framework defined",
                    4: "Active data stewardship program",
                    5: "Mature governance with clear accountability"
                }, weight=1.0
            ),
            AssessmentQuestion(
                "DATA-03", AssessmentDimension.DATA, SubDimension.ANALYTICS,
                "What analytics capabilities exist?",
                {
                    1: "Basic reporting only",
                    2: "Ad-hoc analysis in spreadsheets",
                    3: "BI dashboards and standard reports",
                    4: "Advanced analytics and predictive models",
                    5: "AI/ML-driven insights and prescriptive analytics"
                }, weight=1.3
            ),

            # Processes
            AssessmentQuestion(
                "PROC-01", AssessmentDimension.PROCESSES, SubDimension.STANDARDIZATION,
                "How standardized are construction processes?",
                {
                    1: "No standard processes",
                    2: "Some documented procedures",
                    3: "Standard operating procedures defined",
                    4: "Processes measured and improved",
                    5: "Best practices continuously optimized"
                }, weight=1.0
            ),
            AssessmentQuestion(
                "PROC-02", AssessmentDimension.PROCESSES, SubDimension.DIGITIZATION,
                "What is the level of process digitization?",
                {
                    1: "Paper-based processes",
                    2: "Some digital forms",
                    3: "Most workflows digitized",
                    4: "End-to-end digital workflows",
                    5: "Fully digital with real-time tracking"
                }, weight=1.2
            ),

            # People
            AssessmentQuestion(
                "PPL-01", AssessmentDimension.PEOPLE, SubDimension.SKILLS,
                "What digital skills exist in the workforce?",
                {
                    1: "Basic computer literacy only",
                    2: "Some power users",
                    3: "Digital skills training available",
                    4: "Dedicated data/digital team",
                    5: "Organization-wide digital fluency"
                }, weight=1.0
            ),
            AssessmentQuestion(
                "PPL-02", AssessmentDimension.PEOPLE, SubDimension.TRAINING,
                "How is digital training managed?",
                {
                    1: "No training programs",
                    2: "Ad-hoc training",
                    3: "Structured training curriculum",
                    4: "Continuous learning culture",
                    5: "Learning organization with career paths"
                }, weight=0.8
            ),
            AssessmentQuestion(
                "PPL-03", AssessmentDimension.PEOPLE, SubDimension.ADOPTION,
                "How well are digital tools adopted?",
                {
                    1: "Resistance to new tools",
                    2: "Partial adoption",
                    3: "Most users trained and using tools",
                    4: "High adoption with champions",
                    5: "Full adoption with user-driven innovation"
                }, weight=1.0
            ),

            # Culture
            AssessmentQuestion(
                "CUL-01", AssessmentDimension.CULTURE, SubDimension.INNOVATION,
                "How is innovation encouraged?",
                {
                    1: "Innovation not valued",
                    2: "Occasional innovation projects",
                    3: "Innovation time/budget allocated",
                    4: "Innovation program with incentives",
                    5: "Innovation embedded in culture"
                }, weight=0.8
            ),
            AssessmentQuestion(
                "CUL-02", AssessmentDimension.CULTURE, SubDimension.COLLABORATION,
                "How is collaboration supported?",
                {
                    1: "Siloed departments",
                    2: "Project-based collaboration",
                    3: "Collaboration tools widely used",
                    4: "Cross-functional teams common",
                    5: "Seamless internal and external collaboration"
                }, weight=0.8
            ),
            AssessmentQuestion(
                "CUL-03", AssessmentDimension.CULTURE, SubDimension.CHANGE_READINESS,
                "How ready is the organization for change?",
                {
                    1: "Strong resistance to change",
                    2: "Acceptance of necessary changes",
                    3: "Change management processes exist",
                    4: "Proactive change adoption",
                    5: "Change agility and resilience"
                }, weight=1.0
            )
        ]

        for q in questions:
            self.questions[q.question_id] = q

    def record_response(self, question_id: str, score: int, notes: str = ""):
        """Record a response to a question."""

        if question_id not in self.questions:
            return

        if score < 1 or score > 5:
            score = max(1, min(5, score))

        self.responses[question_id] = Response(
            question_id=question_id,
            score=score,
            notes=notes
        )

    def record_responses_from_df(self, df: pd.DataFrame):
        """Record responses from DataFrame."""

        for _, row in df.iterrows():
            self.record_response(
                str(row['question_id']),
                int(row['score']),
                str(row.get('notes', ''))
            )

    def calculate_dimension_score(self, dimension: AssessmentDimension) -> DimensionScore:
        """Calculate score for a dimension."""

        dim_questions = [q for q in self.questions.values() if q.dimension == dimension]
        sub_scores = {}
        gaps = []
        recommendations = []

        total_weighted_score = 0
        total_weight = 0

        for q in dim_questions:
            response = self.responses.get(q.question_id)
            if response:
                weighted_score = response.score * q.weight
                total_weighted_score += weighted_score
                total_weight += q.weight

                # Track sub-dimension scores
                sub_dim = q.sub_dimension.value
                if sub_dim not in sub_scores:
                    sub_scores[sub_dim] = []
                sub_scores[sub_dim].append(response.score)

                # Identify gaps (score < 3)
                if response.score < 3:
                    gaps.append(f"{q.sub_dimension.value}: {q.question}")

        # Calculate average
        avg_score = total_weighted_score / total_weight if total_weight > 0 else 0

        # Determine maturity level
        if avg_score < 1.5:
            level = MaturityLevel.INITIAL
        elif avg_score < 2.5:
            level = MaturityLevel.DEVELOPING
        elif avg_score < 3.5:
            level = MaturityLevel.DEFINED
        elif avg_score < 4.5:
            level = MaturityLevel.MANAGED
        else:
            level = MaturityLevel.OPTIMIZING

        # Calculate sub-dimension averages
        sub_scores = {k: round(sum(v) / len(v), 2) for k, v in sub_scores.items()}

        # Generate recommendations based on gaps
        recommendations = self._get_recommendations(dimension, sub_scores)

        return DimensionScore(
            dimension=dimension,
            score=round(avg_score, 2),
            level=level,
            sub_scores=sub_scores,
            gaps=gaps,
            recommendations=recommendations
        )

    def _get_recommendations(self, dimension: AssessmentDimension,
                              sub_scores: Dict[str, float]) -> List[str]:
        """Generate recommendations based on scores."""

        recommendations = []

        if dimension == AssessmentDimension.STRATEGY:
            if sub_scores.get('digital_vision', 0) < 3:
                recommendations.append("Develop and document a clear digital transformation strategy")
            if sub_scores.get('leadership', 0) < 3:
                recommendations.append("Increase executive engagement in digital initiatives")

        elif dimension == AssessmentDimension.TECHNOLOGY:
            if sub_scores.get('infrastructure', 0) < 3:
                recommendations.append("Modernize IT infrastructure with cloud adoption")
            if sub_scores.get('systems_integration', 0) < 3:
                recommendations.append("Implement integration platform for better data flow")

        elif dimension == AssessmentDimension.DATA:
            if sub_scores.get('data_quality', 0) < 3:
                recommendations.append("Establish data quality standards and validation processes")
            if sub_scores.get('analytics', 0) < 3:
                recommendations.append("Invest in business intelligence and analytics capabilities")

        elif dimension == AssessmentDimension.PROCESSES:
            if sub_scores.get('digitization', 0) < 3:
                recommendations.append("Prioritize digitization of key business processes")

        elif dimension == AssessmentDimension.PEOPLE:
            if sub_scores.get('skills', 0) < 3:
                recommendations.append("Develop digital skills training program")
            if sub_scores.get('adoption', 0) < 3:
                recommendations.append("Implement change management for tool adoption")

        elif dimension == AssessmentDimension.CULTURE:
            if sub_scores.get('innovation', 0) < 3:
                recommendations.append("Create innovation incentives and dedicated time")
            if sub_scores.get('change_readiness', 0) < 3:
                recommendations.append("Build change management capability")

        return recommendations

    def get_overall_assessment(self) -> Dict[str, Any]:
        """Get overall digital maturity assessment."""

        dimension_scores = {}
        all_recommendations = []
        all_gaps = []

        total_score = 0

        for dimension in AssessmentDimension:
            dim_result = self.calculate_dimension_score(dimension)
            dimension_scores[dimension.value] = {
                'score': dim_result.score,
                'level': dim_result.level.name,
                'sub_scores': dim_result.sub_scores
            }
            total_score += dim_result.score
            all_recommendations.extend(dim_result.recommendations)
            all_gaps.extend(dim_result.gaps)

        avg_score = total_score / len(AssessmentDimension)

        # Determine overall level
        if avg_score < 1.5:
            overall_level = MaturityLevel.INITIAL
        elif avg_score < 2.5:
            overall_level = MaturityLevel.DEVELOPING
        elif avg_score < 3.5:
            overall_level = MaturityLevel.DEFINED
        elif avg_score < 4.5:
            overall_level = MaturityLevel.MANAGED
        else:
            overall_level = MaturityLevel.OPTIMIZING

        return {
            'organization': self.organization_name,
            'assessment_date': self.assessment_date.isoformat(),
            'overall_score': round(avg_score, 2),
            'overall_level': overall_level.name,
            'overall_level_value': overall_level.value,
            'dimension_scores': dimension_scores,
            'total_responses': len(self.responses),
            'total_questions': len(self.questions),
            'top_gaps': all_gaps[:5],
            'priority_recommendations': all_recommendations[:5]
        }

    def export_to_excel(self, output_path: str) -> str:
        """Export assessment results to Excel."""

        assessment = self.get_overall_assessment()

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary_df = pd.DataFrame([{
                'Organization': assessment['organization'],
                'Date': assessment['assessment_date'],
                'Overall Score': assessment['overall_score'],
                'Maturity Level': assessment['overall_level'],
                'Responses': assessment['total_responses'],
                'Questions': assessment['total_questions']
            }])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Dimension scores
            dim_data = []
            for dim, scores in assessment['dimension_scores'].items():
                dim_data.append({
                    'Dimension': dim,
                    'Score': scores['score'],
                    'Level': scores['level']
                })
            dim_df = pd.DataFrame(dim_data)
            dim_df.to_excel(writer, sheet_name='Dimensions', index=False)

            # All responses
            response_data = []
            for q_id, response in self.responses.items():
                q = self.questions[q_id]
                response_data.append({
                    'Question ID': q_id,
                    'Dimension': q.dimension.value,
                    'Sub-Dimension': q.sub_dimension.value,
                    'Question': q.question,
                    'Score': response.score,
                    'Level Description': q.level_descriptions.get(response.score, ''),
                    'Notes': response.notes
                })
            response_df = pd.DataFrame(response_data)
            response_df.to_excel(writer, sheet_name='Responses', index=False)

            # Recommendations
            rec_df = pd.DataFrame({'Recommendation': assessment['priority_recommendations']})
            rec_df.to_excel(writer, sheet_name='Recommendations', index=False)

        return output_path

    def get_questions_list(self) -> pd.DataFrame:
        """Get list of all questions."""

        data = [{
            'Question ID': q.question_id,
            'Dimension': q.dimension.value,
            'Sub-Dimension': q.sub_dimension.value,
            'Question': q.question,
            'Weight': q.weight
        } for q in self.questions.values()]

        return pd.DataFrame(data)
```

## Quick Start

```python
# Create assessment
assessment = DigitalMaturityAssessment("ABC Construction Inc.")

# Record responses
assessment.record_response("STR-01", 3, "Strategy exists but needs updating")
assessment.record_response("STR-02", 4, "Strong executive support")
assessment.record_response("STR-03", 3)
assessment.record_response("TECH-01", 2, "Still mostly on-premise")
assessment.record_response("TECH-02", 2, "Manual data transfer between systems")
assessment.record_response("TECH-03", 3)
assessment.record_response("DATA-01", 2)
assessment.record_response("DATA-02", 2)
assessment.record_response("DATA-03", 3)
assessment.record_response("PROC-01", 3)
assessment.record_response("PROC-02", 2)
assessment.record_response("PPL-01", 3)
assessment.record_response("PPL-02", 2)
assessment.record_response("PPL-03", 3)
assessment.record_response("CUL-01", 2)
assessment.record_response("CUL-02", 3)
assessment.record_response("CUL-03", 3)

# Get overall assessment
results = assessment.get_overall_assessment()
print(f"Overall Score: {results['overall_score']}/5")
print(f"Maturity Level: {results['overall_level']}")
print(f"\nTop Recommendations:")
for rec in results['priority_recommendations']:
    print(f"  - {rec}")
```

## Common Use Cases

### 1. Dimension Analysis
```python
data_score = assessment.calculate_dimension_score(AssessmentDimension.DATA)
print(f"Data Dimension: {data_score.score}/5 ({data_score.level.name})")
print(f"Sub-scores: {data_score.sub_scores}")
```

### 2. Export Report
```python
assessment.export_to_excel("maturity_assessment.xlsx")
```

### 3. Get Questions
```python
questions = assessment.get_questions_list()
print(questions)
```

### 4. Bulk Response Import
```python
responses_df = pd.DataFrame([
    {'question_id': 'STR-01', 'score': 3, 'notes': 'In progress'},
    {'question_id': 'STR-02', 'score': 4, 'notes': ''}
])
assessment.record_responses_from_df(responses_df)
```

## Resources
- **DDC Book**: Chapter 5.1 - Uberization and Open Data
- **Digital Maturity Models**: Various industry frameworks
- **Website**: https://datadrivenconstruction.io

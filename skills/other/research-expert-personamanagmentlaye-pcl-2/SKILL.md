---
name: research-expert
version: 1.0.0
description: Expert-level research methodology, academic writing, statistical analysis, and scientific investigation
category: scientific
tags: [research, methodology, statistics, academic-writing, experimental-design]
allowed-tools:
  - Read
  - Write
  - Edit
---

# Research Methodology Expert

Expert guidance for research methodology, experimental design, statistical analysis, and academic writing.

## Core Concepts

### Research Design
- Experimental vs observational studies
- Randomized controlled trials (RCTs)
- Cross-sectional, longitudinal, cohort studies
- Case-control studies
- Systematic reviews and meta-analysis
- Sample size determination

### Statistical Analysis
- Descriptive statistics
- Hypothesis testing
- Confidence intervals
- Regression analysis
- ANOVA and t-tests
- Non-parametric tests
- Multiple testing correction

### Academic Writing
- Literature review
- Research proposals
- Manuscript structure (IMR AD)
- Citation management
- Peer review process
- Publishing ethics

## Experimental Design

```python
from dataclasses import dataclass
from typing import List, Optional
import numpy as np
from scipy import stats

@dataclass
class Study:
    name: str
    design_type: str  # 'RCT', 'observational', 'cohort'
    sample_size: int
    groups: List[str]
    primary_outcome: str
    secondary_outcomes: List[str]

class SampleSizeCalculator:
    """Calculate required sample size for studies"""

    @staticmethod
    def two_sample_ttest(effect_size: float, alpha: float = 0.05,
                        power: float = 0.8) -> int:
        """Calculate sample size for two-sample t-test"""
        from statsmodels.stats.power import tt_ind_solve_power

        n = tt_ind_solve_power(
            effect_size=effect_size,
            alpha=alpha,
            power=power,
            alternative='two-sided'
        )

        return int(np.ceil(n))

    @staticmethod
    def proportion_test(p1: float, p2: float, alpha: float = 0.05,
                       power: float = 0.8) -> int:
        """Calculate sample size for comparing proportions"""
        from statsmodels.stats.power import zt_ind_solve_power

        effect_size = (p2 - p1) / np.sqrt(p1 * (1 - p1))

        n = zt_ind_solve_power(
            effect_size=effect_size,
            alpha=alpha,
            power=power,
            alternative='two-sided'
        )

        return int(np.ceil(n))

class ExperimentalDesign:
    """Design and randomize experimental studies"""

    def __init__(self, n_subjects: int, n_groups: int):
        self.n_subjects = n_subjects
        self.n_groups = n_groups

    def simple_randomization(self) -> List[int]:
        """Simple random assignment to groups"""
        return np.random.choice(self.n_groups, size=self.n_subjects)

    def block_randomization(self, block_size: int) -> List[int]:
        """Block randomization for balanced groups"""
        n_blocks = self.n_subjects // block_size
        assignments = []

        for _ in range(n_blocks):
            block = np.repeat(range(self.n_groups),
                            block_size // self.n_groups)
            np.random.shuffle(block)
            assignments.extend(block)

        # Handle remaining subjects
        remainder = self.n_subjects % block_size
        if remainder > 0:
            extra = np.random.choice(self.n_groups, size=remainder)
            assignments.extend(extra)

        return assignments

    def stratified_randomization(self, strata: List[str]) -> List[int]:
        """Stratified randomization by covariates"""
        assignments = np.zeros(self.n_subjects, dtype=int)

        for stratum in set(strata):
            stratum_indices = [i for i, s in enumerate(strata) if s == stratum]
            stratum_n = len(stratum_indices)

            stratum_assignments = np.random.choice(
                self.n_groups,
                size=stratum_n,
                replace=True
            )

            for idx, assignment in zip(stratum_indices, stratum_assignments):
                assignments[idx] = assignment

        return assignments
```

## Statistical Analysis

```python
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

class StatisticalAnalysis:
    """Perform statistical analyses"""

    @staticmethod
    def descriptive_stats(data: pd.Series) -> dict:
        """Calculate descriptive statistics"""
        return {
            "mean": data.mean(),
            "median": data.median(),
            "std": data.std(),
            "min": data.min(),
            "max": data.max(),
            "q25": data.quantile(0.25),
            "q75": data.quantile(0.75),
            "skewness": stats.skew(data),
            "kurtosis": stats.kurtosis(data)
        }

    @staticmethod
    def independent_ttest(group1: np.ndarray, group2: np.ndarray) -> dict:
        """Perform independent samples t-test"""
        statistic, pvalue = stats.ttest_ind(group1, group2)

        # Calculate effect size (Cohen's d)
        pooled_std = np.sqrt((group1.var() + group2.var()) / 2)
        cohens_d = (group1.mean() - group2.mean()) / pooled_std

        return {
            "t_statistic": statistic,
            "p_value": pvalue,
            "cohens_d": cohens_d,
            "mean_diff": group1.mean() - group2.mean(),
            "significant": pvalue < 0.05
        }

    @staticmethod
    def one_way_anova(groups: List[np.ndarray]) -> dict:
        """Perform one-way ANOVA"""
        f_statistic, p_value = stats.f_oneway(*groups)

        # Calculate effect size (eta-squared)
        grand_mean = np.mean(np.concatenate(groups))
        ss_between = sum(len(g) * (g.mean() - grand_mean)**2 for g in groups)
        ss_total = sum(((g - grand_mean)**2).sum() for g in groups)
        eta_squared = ss_between / ss_total

        return {
            "f_statistic": f_statistic,
            "p_value": p_value,
            "eta_squared": eta_squared,
            "significant": p_value < 0.05
        }

    @staticmethod
    def linear_regression(X: pd.DataFrame, y: pd.Series) -> dict:
        """Perform linear regression"""
        X_with_const = sm.add_constant(X)
        model = sm.OLS(y, X_with_const).fit()

        return {
            "coefficients": model.params.to_dict(),
            "r_squared": model.rsquared,
            "adj_r_squared": model.rsquared_adj,
            "f_statistic": model.fvalue,
            "p_value": model.f_pvalue,
            "summary": model.summary()
        }

    @staticmethod
    def multiple_testing_correction(p_values: List[float],
                                    method: str = 'fdr_bh',
                                    alpha: float = 0.05) -> dict:
        """Apply multiple testing correction"""
        reject, pvals_corrected, alphacSidak, alphacBonf = multipletests(
            p_values,
            alpha=alpha,
            method=method
        )

        return {
            "rejected": reject,
            "corrected_pvalues": pvals_corrected,
            "n_significant": reject.sum(),
            "method": method
        }

class EffectSize:
    """Calculate effect sizes"""

    @staticmethod
    def cohens_d(group1: np.ndarray, group2: np.ndarray) -> float:
        """Cohen's d for two groups"""
        pooled_std = np.sqrt((group1.var() + group2.var()) / 2)
        return (group1.mean() - group2.mean()) / pooled_std

    @staticmethod
    def hedges_g(group1: np.ndarray, group2: np.ndarray) -> float:
        """Hedges' g (corrected effect size)"""
        n1, n2 = len(group1), len(group2)
        df = n1 + n2 - 2

        correction = 1 - (3 / (4 * df - 1))
        d = EffectSize.cohens_d(group1, group2)

        return d * correction

    @staticmethod
    def r_squared_to_cohens_f(r_squared: float) -> float:
        """Convert R² to Cohen's f"""
        return np.sqrt(r_squared / (1 - r_squared))
```

## Literature Review

```python
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class Citation:
    authors: List[str]
    year: int
    title: str
    journal: str
    volume: Optional[int] = None
    pages: Optional[str] = None
    doi: Optional[str] = None

    def format_apa(self) -> str:
        """Format citation in APA style"""
        authors_str = self._format_authors_apa()
        citation = f"{authors_str} ({self.year}). {self.title}. {self.journal}"

        if self.volume:
            citation += f", {self.volume}"
        if self.pages:
            citation += f", {self.pages}"
        if self.doi:
            citation += f". https://doi.org/{self.doi}"

        return citation + "."

    def _format_authors_apa(self) -> str:
        """Format authors in APA style"""
        if len(self.authors) == 1:
            return self.authors[0]
        elif len(self.authors) == 2:
            return f"{self.authors[0]} & {self.authors[1]}"
        else:
            return f"{self.authors[0]} et al."

class LiteratureReview:
    """Manage literature review"""

    def __init__(self):
        self.citations: List[Citation] = []
        self.themes: Dict[str, List[Citation]] = {}

    def add_citation(self, citation: Citation, themes: List[str]):
        """Add citation and categorize by themes"""
        self.citations.append(citation)

        for theme in themes:
            if theme not in self.themes:
                self.themes[theme] = []
            self.themes[theme].append(citation)

    def get_bibliography(self, style: str = 'apa') -> List[str]:
        """Generate bibliography"""
        if style == 'apa':
            return [c.format_apa() for c in sorted(
                self.citations,
                key=lambda x: (x.authors[0], x.year)
            )]

    def get_summary_by_theme(self, theme: str) -> List[Citation]:
        """Get citations for specific theme"""
        return self.themes.get(theme, [])
```

## Best Practices

### Research Design
- Pre-register studies when possible
- Calculate adequate sample sizes
- Use appropriate controls
- Randomize when applicable
- Blind assessors to reduce bias
- Consider confounding variables
- Document protocol deviations

### Data Analysis
- Pre-specify analysis plan
- Check statistical assumptions
- Report effect sizes, not just p-values
- Apply multiple testing corrections
- Use appropriate statistical tests
- Report confidence intervals
- Make data and code available

### Academic Writing
- Follow journal guidelines
- Use clear, precise language
- Report methodology in detail
- Discuss limitations openly
- Acknowledge conflicts of interest
- Properly cite all sources
- Use reference management software

## Anti-Patterns

❌ P-hacking and data dredging
❌ HARKing (Hypothesizing After Results are Known)
❌ Cherry-picking results
❌ Inadequate sample sizes
❌ Ignoring failed experiments
❌ No pre-registration
❌ Selective reporting of outcomes

## Resources

- ClinicalTrials.gov: https://clinicaltrials.gov/
- CONSORT Statement: http://www.consort-statement.org/
- Cochrane Handbook: https://training.cochrane.org/handbook
- APA Style: https://apastyle.apa.org/
- StatsModels: https://www.statsmodels.org/

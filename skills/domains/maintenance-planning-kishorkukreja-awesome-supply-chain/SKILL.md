---
name: maintenance-planning
description: When the user wants to optimize maintenance strategies, improve equipment reliability, reduce downtime, or implement predictive maintenance. Also use when the user mentions "preventive maintenance," "predictive maintenance," "TPM," "Total Productive Maintenance," "MTBF," "MTTR," "reliability analysis," "equipment maintenance," "condition monitoring," "CBM," "failure analysis," or "spare parts optimization." For quality improvements, see quality-management. For OEE, see lean-manufacturing.
---

# Maintenance Planning

You are an expert in maintenance planning and reliability engineering. Your goal is to help organizations optimize maintenance strategies, improve equipment reliability, reduce unplanned downtime, and balance maintenance costs with equipment availability.

## Initial Assessment

Before developing maintenance strategies, understand:

1. **Equipment Context**
   - Critical equipment and assets?
   - Asset age and condition?
   - Current failure rates and downtime?
   - Impact of failures on production?

2. **Maintenance Approach**
   - Current maintenance strategy? (reactive, preventive, predictive)
   - Maintenance intervals and schedules?
   - Condition monitoring in place?
   - CMMS (Computerized Maintenance Management System) used?

3. **Performance Metrics**
   - Equipment availability and OEE?
   - MTBF (Mean Time Between Failures)?
   - MTTR (Mean Time To Repair)?
   - Maintenance costs as % of asset value?

4. **Improvement Goals**
   - Reduce unplanned downtime?
   - Extend equipment life?
   - Optimize maintenance costs?
   - Improve spare parts management?

---

## Maintenance Strategy Framework

### Maintenance Types

**1. Reactive Maintenance (Run-to-Failure)**
- **Approach**: Fix only when broken
- **Cost**: Low planning cost, high failure cost
- **Downtime**: Unplanned, unpredictable
- **Best for**: Non-critical, low-cost equipment
- **Risk**: Production disruption, safety issues

**2. Preventive Maintenance (PM)**
- **Approach**: Time-based or usage-based maintenance
- **Cost**: Moderate, scheduled costs
- **Downtime**: Planned, predictable
- **Best for**: Critical equipment with known wear patterns
- **Examples**: Lubrication, filter changes, inspections

**3. Predictive Maintenance (PdM)**
- **Approach**: Condition-based, data-driven
- **Cost**: Higher upfront (sensors), lower total cost
- **Downtime**: Minimal, just-in-time intervention
- **Best for**: Critical equipment, expensive failures
- **Technologies**: Vibration analysis, thermography, oil analysis, ultrasound

**4. Prescriptive Maintenance**
- **Approach**: AI/ML prescribes optimal actions
- **Cost**: Highest technology investment
- **Downtime**: Optimized timing
- **Best for**: Complex assets, digital maturity
- **Advanced**: RUL (Remaining Useful Life) prediction

### Maintenance Strategy Selection

**RCM (Reliability-Centered Maintenance) Framework:**

```
Equipment Criticality Assessment:
├─ Critical (Production stoppage, safety risk)
│   └─ Strategy: Predictive or rigorous preventive
├─ Important (Reduced capacity, quality impact)
│   └─ Strategy: Preventive with some condition monitoring
└─ Non-critical (Minimal impact)
    └─ Strategy: Reactive or basic preventive
```

---

## Reliability Analysis

### Reliability Metrics

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from datetime import datetime, timedelta

class ReliabilityAnalysis:
    """
    Equipment reliability analysis
    Calculate MTBF, MTTR, availability, and failure distributions
    """

    def __init__(self, failure_data):
        """
        failure_data: DataFrame with columns
        - equipment_id
        - failure_date
        - repair_date
        - time_between_failures (optional)
        - downtime_hours
        """
        self.data = failure_data.copy()

        # Calculate time between failures if not provided
        if 'time_between_failures' not in self.data.columns:
            self.data = self.data.sort_values(['equipment_id', 'failure_date'])
            self.data['time_between_failures'] = (
                self.data.groupby('equipment_id')['failure_date']
                .diff().dt.total_seconds() / 3600  # Convert to hours
            )

    def calculate_mtbf(self):
        """
        Calculate Mean Time Between Failures

        MTBF = Total operating time / Number of failures
        """

        # Remove first failure for each equipment (no prior TBF)
        valid_tbf = self.data[self.data['time_between_failures'].notna()]

        mtbf = valid_tbf['time_between_failures'].mean()
        mtbf_by_equipment = valid_tbf.groupby('equipment_id')['time_between_failures'].mean()

        return {
            'overall_mtbf_hours': mtbf,
            'overall_mtbf_days': mtbf / 24,
            'mtbf_by_equipment': mtbf_by_equipment.to_dict(),
            'std_dev': valid_tbf['time_between_failures'].std()
        }

    def calculate_mttr(self):
        """
        Calculate Mean Time To Repair

        MTTR = Total repair time / Number of repairs
        """

        mttr = self.data['downtime_hours'].mean()
        mttr_by_equipment = self.data.groupby('equipment_id')['downtime_hours'].mean()

        return {
            'overall_mttr_hours': mttr,
            'mttr_by_equipment': mttr_by_equipment.to_dict(),
            'std_dev': self.data['downtime_hours'].std()
        }

    def calculate_availability(self, operating_hours_per_year=8760):
        """
        Calculate equipment availability

        Availability = MTBF / (MTBF + MTTR)
        or
        Availability = Uptime / Total Time
        """

        mtbf_result = self.calculate_mtbf()
        mttr_result = self.calculate_mttr()

        mtbf = mtbf_result['overall_mtbf_hours']
        mttr = mttr_result['overall_mttr_hours']

        # Inherent availability (MTBF / (MTBF + MTTR))
        availability = mtbf / (mtbf + mttr) if (mtbf + mttr) > 0 else 0

        # Actual availability based on data
        total_downtime = self.data['downtime_hours'].sum()
        actual_availability = 1 - (total_downtime / operating_hours_per_year)

        return {
            'inherent_availability_pct': availability * 100,
            'actual_availability_pct': actual_availability * 100,
            'mtbf_hours': mtbf,
            'mttr_hours': mttr,
            'total_downtime_hours': total_downtime,
            'total_failures': len(self.data)
        }

    def weibull_analysis(self, time_to_failure_data):
        """
        Weibull distribution analysis for failure prediction

        Weibull parameters:
        - Beta (shape): failure pattern
          - Beta < 1: Infant mortality (decreasing failure rate)
          - Beta = 1: Random failures (constant failure rate)
          - Beta > 1: Wear-out failures (increasing failure rate)
        - Eta (scale): characteristic life

        Parameters:
        - time_to_failure_data: array of times to failure
        """

        # Fit Weibull distribution
        shape, loc, scale = stats.weibull_min.fit(time_to_failure_data, floc=0)

        # Beta = shape, Eta = scale
        beta = shape
        eta = scale

        # Determine failure pattern
        if beta < 1:
            pattern = "Infant Mortality (decreasing failure rate)"
        elif 0.9 <= beta <= 1.1:
            pattern = "Random Failures (constant failure rate)"
        else:
            pattern = "Wear-out (increasing failure rate)"

        # Calculate reliability at different times
        times = np.linspace(0, time_to_failure_data.max(), 100)
        reliability = stats.weibull_min.sf(times, shape, loc, scale)

        # Calculate MTTF (Mean Time To Failure)
        mttf = stats.weibull_min.mean(shape, loc, scale)

        return {
            'beta_shape': beta,
            'eta_scale': eta,
            'failure_pattern': pattern,
            'mttf': mttf,
            'times': times,
            'reliability': reliability
        }

    def plot_weibull(self, weibull_results):
        """Plot Weibull reliability curve"""

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(weibull_results['times'], weibull_results['reliability'] * 100,
               'b-', linewidth=2)
        ax.axhline(50, color='red', linestyle='--', linewidth=1, label='50% Reliability')

        ax.set_xlabel('Time (hours)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Reliability (%)', fontsize=12, fontweight='bold')
        ax.set_title(f'Weibull Reliability Curve\nβ={weibull_results["beta_shape"]:.2f}, η={weibull_results["eta_scale"]:.0f}\nPattern: {weibull_results["failure_pattern"]}',
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()

        plt.tight_layout()
        return fig

    def failure_rate_trend(self):
        """Analyze failure rate trends over time"""

        # Group failures by month
        self.data['month'] = pd.to_datetime(self.data['failure_date']).dt.to_period('M')
        monthly_failures = self.data.groupby('month').size()

        # Calculate trend
        x = np.arange(len(monthly_failures))
        y = monthly_failures.values

        if len(x) > 1:
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

            if p_value < 0.05:
                if slope > 0:
                    trend = "Increasing (equipment degradation)"
                else:
                    trend = "Decreasing (reliability improvement)"
            else:
                trend = "Stable (no significant trend)"
        else:
            trend = "Insufficient data"
            slope = 0

        return {
            'monthly_failures': monthly_failures.to_dict(),
            'trend': trend,
            'slope': slope,
            'avg_failures_per_month': monthly_failures.mean()
        }

# Example usage
np.random.seed(42)

# Generate example failure data
dates = pd.date_range('2024-01-01', '2025-01-26', freq='D')
failure_dates = []
repair_dates = []
equipment_ids = []
downtime_hours = []

for i in range(50):  # 50 failures
    fail_date = np.random.choice(dates)
    equipment_id = np.random.choice(['Pump-01', 'Conveyor-02', 'Press-03', 'CNC-04'])
    downtime = np.random.exponential(4)  # Average 4 hours downtime

    failure_dates.append(fail_date)
    repair_dates.append(fail_date + timedelta(hours=downtime))
    equipment_ids.append(equipment_id)
    downtime_hours.append(downtime)

failure_data = pd.DataFrame({
    'equipment_id': equipment_ids,
    'failure_date': failure_dates,
    'repair_date': repair_dates,
    'downtime_hours': downtime_hours
})

reliability = ReliabilityAnalysis(failure_data)

# MTBF
mtbf = reliability.calculate_mtbf()
print("MTBF Analysis:")
print(f"  Overall MTBF: {mtbf['overall_mtbf_hours']:.1f} hours ({mtbf['overall_mtbf_days']:.1f} days)")
print(f"  Standard Deviation: {mtbf['std_dev']:.1f} hours")

# MTTR
mttr = reliability.calculate_mttr()
print(f"\nMTTR Analysis:")
print(f"  Overall MTTR: {mttr['overall_mttr_hours']:.2f} hours")

# Availability
availability = reliability.calculate_availability()
print(f"\nAvailability Analysis:")
print(f"  Inherent Availability: {availability['inherent_availability_pct']:.2f}%")
print(f"  Actual Availability: {availability['actual_availability_pct']:.2f}%")
print(f"  Total Failures: {availability['total_failures']}")
print(f"  Total Downtime: {availability['total_downtime_hours']:.1f} hours")

# Weibull analysis
ttf_data = failure_data[failure_data['time_between_failures'].notna()]['time_between_failures'].values
if len(ttf_data) > 5:
    weibull = reliability.weibull_analysis(ttf_data)
    print(f"\nWeibull Analysis:")
    print(f"  Beta (Shape): {weibull['beta_shape']:.2f}")
    print(f"  Eta (Scale): {weibull['eta_scale']:.0f} hours")
    print(f"  Failure Pattern: {weibull['failure_pattern']}")
    print(f"  MTTF: {weibull['mttf']:.1f} hours")

    fig = reliability.plot_weibull(weibull)
    plt.show()

# Failure trend
trend = reliability.failure_rate_trend()
print(f"\nFailure Rate Trend:")
print(f"  Trend: {trend['trend']}")
print(f"  Average Failures/Month: {trend['avg_failures_per_month']:.1f}")
```

---

## Preventive Maintenance Optimization

### PM Interval Optimization

```python
class PreventiveMaintenanceOptimizer:
    """
    Optimize preventive maintenance intervals
    Balance maintenance cost vs. failure cost
    """

    def __init__(self, mtbf, mttr, pm_cost, failure_cost, pm_duration_hours):
        """
        Parameters:
        - mtbf: Mean Time Between Failures (hours)
        - mttr: Mean Time To Repair (hours)
        - pm_cost: Cost of preventive maintenance ($)
        - failure_cost: Cost of failure (downtime + repair) ($)
        - pm_duration_hours: Duration of PM activity (hours)
        """
        self.mtbf = mtbf
        self.mttr = mttr
        self.pm_cost = pm_cost
        self.failure_cost = failure_cost
        self.pm_duration = pm_duration_hours

    def calculate_optimal_interval(self, interval_range=(100, 2000, 50)):
        """
        Find optimal PM interval that minimizes total cost

        Total Cost = PM Cost + Failure Cost
        """

        intervals = np.arange(*interval_range)
        results = []

        for T in intervals:
            # Expected number of PMs per year (8760 hours)
            n_pms = 8760 / T

            # Probability of failure before PM
            # Assuming exponential distribution
            failure_prob = 1 - np.exp(-T / self.mtbf)

            # Expected failures per year
            n_failures = n_pms * failure_prob

            # Total cost
            annual_pm_cost = n_pms * self.pm_cost
            annual_failure_cost = n_failures * self.failure_cost
            total_cost = annual_pm_cost + annual_failure_cost

            # Downtime
            pm_downtime = n_pms * self.pm_duration
            failure_downtime = n_failures * self.mttr
            total_downtime = pm_downtime + failure_downtime

            # Availability
            availability = 1 - (total_downtime / 8760)

            results.append({
                'interval_hours': T,
                'n_pms_per_year': n_pms,
                'n_failures_per_year': n_failures,
                'annual_pm_cost': annual_pm_cost,
                'annual_failure_cost': annual_failure_cost,
                'total_annual_cost': total_cost,
                'total_downtime_hours': total_downtime,
                'availability_pct': availability * 100
            })

        df = pd.DataFrame(results)

        # Find optimal
        optimal_idx = df['total_annual_cost'].idxmin()
        optimal = df.loc[optimal_idx]

        return {
            'optimal_interval_hours': optimal['interval_hours'],
            'optimal_interval_days': optimal['interval_hours'] / 24,
            'total_annual_cost': optimal['total_annual_cost'],
            'availability': optimal['availability_pct'],
            'analysis': df
        }

    def plot_optimization(self, optimization_results):
        """Plot cost optimization curve"""

        df = optimization_results['analysis']

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

        # Cost curves
        ax1.plot(df['interval_hours'], df['annual_pm_cost'], 'b-', linewidth=2, label='PM Cost')
        ax1.plot(df['interval_hours'], df['annual_failure_cost'], 'r-', linewidth=2, label='Failure Cost')
        ax1.plot(df['interval_hours'], df['total_annual_cost'], 'g-', linewidth=3, label='Total Cost')

        # Mark optimal
        optimal_interval = optimization_results['optimal_interval_hours']
        optimal_cost = optimization_results['total_annual_cost']
        ax1.plot(optimal_interval, optimal_cost, 'go', markersize=12, markeredgewidth=2,
                markerfacecolor='yellow', label='Optimal')

        ax1.set_xlabel('PM Interval (hours)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Annual Cost ($)', fontsize=12, fontweight='bold')
        ax1.set_title('Preventive Maintenance Interval Optimization', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Availability curve
        ax2.plot(df['interval_hours'], df['availability_pct'], 'b-', linewidth=2)
        ax2.axhline(optimization_results['availability'], color='red', linestyle='--',
                   label=f"Optimal Availability: {optimization_results['availability']:.1f}%")

        ax2.set_xlabel('PM Interval (hours)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Availability (%)', fontsize=12, fontweight='bold')
        ax2.set_title('Equipment Availability vs. PM Interval', fontsize=12, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

# Example usage
pm_optimizer = PreventiveMaintenanceOptimizer(
    mtbf=720,              # 720 hours (30 days) MTBF
    mttr=8,                # 8 hours MTTR
    pm_cost=500,           # $500 per PM
    failure_cost=5000,     # $5000 per failure
    pm_duration_hours=4    # 4 hours PM duration
)

optimization = pm_optimizer.calculate_optimal_interval(interval_range=(100, 1500, 25))

print("PM Interval Optimization:")
print(f"  Optimal Interval: {optimization['optimal_interval_hours']:.0f} hours ({optimization['optimal_interval_days']:.1f} days)")
print(f"  Total Annual Cost: ${optimization['total_annual_cost']:,.0f}")
print(f"  Expected Availability: {optimization['availability']:.2f}%")

fig = pm_optimizer.plot_optimization(optimization)
plt.show()
```

---

## Predictive Maintenance

### Condition Monitoring & Anomaly Detection

```python
class PredictiveMaintenanceAnalyzer:
    """
    Predictive maintenance using condition monitoring data
    Anomaly detection and RUL (Remaining Useful Life) estimation
    """

    def __init__(self, sensor_data, sensor_name):
        """
        sensor_data: time series of sensor readings (e.g., vibration, temperature)
        sensor_name: description of sensor
        """
        self.data = np.array(sensor_data)
        self.sensor_name = sensor_name

    def detect_anomalies(self, threshold_sigma=3):
        """
        Detect anomalies using statistical methods
        Values beyond threshold_sigma standard deviations are flagged

        Returns anomaly indices and scores
        """

        mean = self.data.mean()
        std = self.data.std()

        # Z-score
        z_scores = np.abs((self.data - mean) / std)

        # Anomalies
        anomalies = z_scores > threshold_sigma
        anomaly_indices = np.where(anomalies)[0]

        return {
            'anomaly_count': anomalies.sum(),
            'anomaly_indices': anomaly_indices,
            'anomaly_values': self.data[anomaly_indices],
            'z_scores': z_scores,
            'mean': mean,
            'std': std,
            'threshold': threshold_sigma
        }

    def trend_analysis(self):
        """
        Analyze trend in sensor data
        Increasing trend may indicate degradation
        """

        x = np.arange(len(self.data))
        y = self.data

        # Linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        # Determine trend
        if p_value < 0.05:
            if slope > 0:
                trend = "Increasing (potential degradation)"
                concern_level = "High" if slope > std_err * 2 else "Medium"
            else:
                trend = "Decreasing (improving or cooling)"
                concern_level = "Low"
        else:
            trend = "Stable (no significant trend)"
            concern_level = "Low"

        return {
            'trend': trend,
            'slope': slope,
            'r_squared': r_value ** 2,
            'p_value': p_value,
            'concern_level': concern_level
        }

    def estimate_rul(self, failure_threshold):
        """
        Estimate Remaining Useful Life

        Assumes linear degradation to failure threshold

        Parameters:
        - failure_threshold: sensor value at which failure occurs

        Returns estimated RUL
        """

        trend = self.trend_analysis()

        if trend['slope'] <= 0:
            return {
                'rul_cycles': float('inf'),
                'message': 'No degradation detected - RUL cannot be estimated'
            }

        # Current value (most recent)
        current_value = self.data[-1]

        # Cycles until threshold
        rul_cycles = (failure_threshold - current_value) / trend['slope']

        # Check if already exceeded
        if rul_cycles < 0:
            rul_cycles = 0
            message = "Warning: Failure threshold already exceeded!"
        else:
            message = f"Estimated {rul_cycles:.0f} cycles remaining until failure threshold"

        return {
            'current_value': current_value,
            'failure_threshold': failure_threshold,
            'degradation_rate': trend['slope'],
            'rul_cycles': max(0, rul_cycles),
            'message': message
        }

    def maintenance_recommendation(self, rul_result, lead_time_cycles=50):
        """
        Generate maintenance recommendation based on RUL

        Parameters:
        - rul_result: output from estimate_rul()
        - lead_time_cycles: lead time needed to plan maintenance
        """

        rul = rul_result['rul_cycles']

        if rul == float('inf'):
            recommendation = "Continue monitoring - no immediate action needed"
            priority = "Low"
        elif rul <= 0:
            recommendation = "URGENT: Schedule immediate maintenance"
            priority = "Critical"
        elif rul < lead_time_cycles:
            recommendation = "Schedule maintenance soon - approaching failure threshold"
            priority = "High"
        elif rul < lead_time_cycles * 2:
            recommendation = "Plan maintenance within next planning cycle"
            priority = "Medium"
        else:
            recommendation = "Continue monitoring - sufficient remaining life"
            priority = "Low"

        return {
            'recommendation': recommendation,
            'priority': priority,
            'estimated_rul': rul,
            'lead_time': lead_time_cycles
        }

    def plot_condition_monitoring(self, anomaly_results, trend_results, rul_results=None):
        """Plot condition monitoring dashboard"""

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

        # Time series with anomalies
        x = np.arange(len(self.data))
        ax1.plot(x, self.data, 'b-', linewidth=1, label='Sensor Reading')

        # Mark anomalies
        if len(anomaly_results['anomaly_indices']) > 0:
            ax1.plot(anomaly_results['anomaly_indices'],
                    anomaly_results['anomaly_values'],
                    'ro', markersize=8, label='Anomalies')

        # Mean and control limits
        mean = anomaly_results['mean']
        std = anomaly_results['std']
        threshold = anomaly_results['threshold']

        ax1.axhline(mean, color='green', linestyle='-', linewidth=2, label='Mean')
        ax1.axhline(mean + threshold * std, color='red', linestyle='--', linewidth=1.5, label='Upper Limit')
        ax1.axhline(mean - threshold * std, color='red', linestyle='--', linewidth=1.5, label='Lower Limit')

        # Trend line
        if trend_results['p_value'] < 0.05:
            trend_line = trend_results['slope'] * x + (self.data[0] - trend_results['slope'] * 0)
            ax1.plot(x, trend_line, 'orange', linestyle='--', linewidth=2, label='Trend')

        ax1.set_xlabel('Cycle / Time', fontsize=12, fontweight='bold')
        ax1.set_ylabel(f'{self.sensor_name}', fontsize=12, fontweight='bold')
        ax1.set_title(f'Condition Monitoring - {self.sensor_name}\nTrend: {trend_results["trend"]}',
                     fontsize=14, fontweight='bold')
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.3)

        # Z-scores (anomaly scores)
        ax2.plot(x, anomaly_results['z_scores'], 'b-', linewidth=1)
        ax2.axhline(threshold, color='red', linestyle='--', linewidth=2, label=f'Threshold ({threshold}σ)')
        ax2.fill_between(x, 0, threshold, alpha=0.2, color='green', label='Normal')
        ax2.fill_between(x, threshold, anomaly_results['z_scores'].max() + 1,
                        alpha=0.2, color='red', label='Anomaly Zone')

        ax2.set_xlabel('Cycle / Time', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Anomaly Score (Z-score)', fontsize=12, fontweight='bold')
        ax2.set_title('Anomaly Detection', fontsize=12, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

# Example usage
np.random.seed(42)

# Simulate sensor data with degradation trend and some anomalies
n_cycles = 200
baseline = 100
degradation_rate = 0.1
noise = np.random.normal(0, 3, n_cycles)

sensor_data = baseline + degradation_rate * np.arange(n_cycles) + noise

# Add some anomalies
sensor_data[50] = 130  # Spike
sensor_data[100] = 135
sensor_data[150] = 140

pdm = PredictiveMaintenanceAnalyzer(sensor_data, "Vibration (mm/s)")

# Detect anomalies
anomalies = pdm.detect_anomalies(threshold_sigma=3)
print(f"Anomaly Detection:")
print(f"  Anomalies Found: {anomalies['anomaly_count']}")
print(f"  Anomaly Indices: {anomalies['anomaly_indices']}")

# Trend analysis
trend = pdm.trend_analysis()
print(f"\nTrend Analysis:")
print(f"  Trend: {trend['trend']}")
print(f"  Degradation Rate: {trend['slope']:.4f} per cycle")
print(f"  R-squared: {trend['r_squared']:.3f}")
print(f"  Concern Level: {trend['concern_level']}")

# RUL estimation
failure_threshold = 150  # Failure occurs at 150 mm/s
rul = pdm.estimate_rul(failure_threshold)
print(f"\nRUL Estimation:")
print(f"  Current Value: {rul['current_value']:.1f}")
print(f"  Failure Threshold: {rul['failure_threshold']}")
print(f"  {rul['message']}")

# Maintenance recommendation
recommendation = pdm.maintenance_recommendation(rul, lead_time_cycles=50)
print(f"\nMaintenance Recommendation:")
print(f"  Priority: {recommendation['priority']}")
print(f"  Action: {recommendation['recommendation']}")

# Plot
fig = pdm.plot_condition_monitoring(anomalies, trend, rul)
plt.show()
```

---

## Total Productive Maintenance (TPM)

### OEE Calculation and Analysis

```python
class OEEAnalysis:
    """
    Overall Equipment Effectiveness (OEE) calculation
    OEE = Availability × Performance × Quality
    """

    def __init__(self, shift_data):
        """
        shift_data: DataFrame with production shift information
        Columns:
        - planned_production_time (minutes)
        - downtime (minutes)
        - units_produced
        - ideal_cycle_time (minutes per unit)
        - defects
        """
        self.data = shift_data

    def calculate_oee(self):
        """
        Calculate OEE and its components

        Availability = Operating Time / Planned Production Time
        Performance = (Actual Output / Max Possible Output)
        Quality = Good Units / Total Units
        OEE = Availability × Performance × Quality
        """

        results = []

        for idx, row in self.data.iterrows():
            # Availability
            operating_time = row['planned_production_time'] - row['downtime']
            availability = operating_time / row['planned_production_time']

            # Performance
            ideal_time_for_output = row['units_produced'] * row['ideal_cycle_time']
            performance = ideal_time_for_output / operating_time if operating_time > 0 else 0

            # Quality
            good_units = row['units_produced'] - row['defects']
            quality = good_units / row['units_produced'] if row['units_produced'] > 0 else 0

            # OEE
            oee = availability * performance * quality

            results.append({
                'shift': idx,
                'availability': availability * 100,
                'performance': performance * 100,
                'quality': quality * 100,
                'oee': oee * 100,
                'operating_time': operating_time,
                'good_units': good_units
            })

        df_results = pd.DataFrame(results)

        # Overall averages
        overall = {
            'avg_availability': df_results['availability'].mean(),
            'avg_performance': df_results['performance'].mean(),
            'avg_quality': df_results['quality'].mean(),
            'avg_oee': df_results['oee'].mean(),
            'world_class_gap': 85 - df_results['oee'].mean(),  # World class = 85%+
            'results_by_shift': df_results
        }

        return overall

    def six_big_losses_analysis(self, breakdown_hours, setup_hours,
                                 small_stops_hours, speed_loss_pct,
                                 process_defects, reduced_yield_pct):
        """
        Analyze TPM Six Big Losses

        1. Breakdowns (Availability)
        2. Setup/Changeovers (Availability)
        3. Small Stops (Performance)
        4. Speed Loss (Performance)
        5. Process Defects (Quality)
        6. Reduced Yield (Quality)
        """

        total_time = self.data['planned_production_time'].sum() / 60  # Convert to hours

        losses = {
            'Breakdowns': {
                'hours': breakdown_hours,
                'pct_of_total': (breakdown_hours / total_time) * 100,
                'category': 'Availability'
            },
            'Setup/Changeover': {
                'hours': setup_hours,
                'pct_of_total': (setup_hours / total_time) * 100,
                'category': 'Availability'
            },
            'Small Stops': {
                'hours': small_stops_hours,
                'pct_of_total': (small_stops_hours / total_time) * 100,
                'category': 'Performance'
            },
            'Speed Loss': {
                'hours': total_time * (speed_loss_pct / 100),
                'pct_of_total': speed_loss_pct,
                'category': 'Performance'
            },
            'Process Defects': {
                'units': process_defects,
                'pct_of_total': (process_defects / self.data['units_produced'].sum()) * 100,
                'category': 'Quality'
            },
            'Reduced Yield': {
                'pct_of_total': reduced_yield_pct,
                'category': 'Quality'
            }
        }

        return pd.DataFrame(losses).T

    def plot_oee_dashboard(self, oee_results):
        """Create OEE dashboard visualization"""

        df = oee_results['results_by_shift']

        fig = plt.figure(figsize=(14, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

        # OEE over time
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(df['shift'], df['oee'], 'bo-', linewidth=2, markersize=8, label='OEE')
        ax1.axhline(85, color='green', linestyle='--', linewidth=2, label='World Class (85%)')
        ax1.axhline(oee_results['avg_oee'], color='orange', linestyle='-', linewidth=2, label='Average')
        ax1.set_xlabel('Shift', fontsize=12, fontweight='bold')
        ax1.set_ylabel('OEE (%)', fontsize=12, fontweight='bold')
        ax1.set_title('Overall Equipment Effectiveness (OEE) by Shift', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # OEE components (average)
        ax2 = fig.add_subplot(gs[1, 0])
        components = ['Availability', 'Performance', 'Quality', 'OEE']
        values = [
            oee_results['avg_availability'],
            oee_results['avg_performance'],
            oee_results['avg_quality'],
            oee_results['avg_oee']
        ]
        colors = ['skyblue', 'lightgreen', 'lightcoral', 'gold']

        bars = ax2.bar(components, values, color=colors, edgecolor='black', linewidth=1.5)
        ax2.axhline(85, color='green', linestyle='--', linewidth=2, label='World Class')
        ax2.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
        ax2.set_title('Average OEE Components', fontsize=12, fontweight='bold')
        ax2.set_ylim([0, 100])
        ax2.legend()
        ax2.grid(True, axis='y', alpha=0.3)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')

        # Component trends
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.plot(df['shift'], df['availability'], 'o-', label='Availability', linewidth=2)
        ax3.plot(df['shift'], df['performance'], 's-', label='Performance', linewidth=2)
        ax3.plot(df['shift'], df['quality'], '^-', label='Quality', linewidth=2)
        ax3.set_xlabel('Shift', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
        ax3.set_title('OEE Component Trends', fontsize=12, fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        # Performance metrics table
        ax4 = fig.add_subplot(gs[2, :])
        ax4.axis('tight')
        ax4.axis('off')

        table_data = [
            ['Metric', 'Value', 'World Class', 'Gap'],
            ['Availability', f"{oee_results['avg_availability']:.1f}%", '90%', f"{90 - oee_results['avg_availability']:.1f}%"],
            ['Performance', f"{oee_results['avg_performance']:.1f}%", '95%', f"{95 - oee_results['avg_performance']:.1f}%"],
            ['Quality', f"{oee_results['avg_quality']:.1f}%", '99%', f"{99 - oee_results['avg_quality']:.1f}%"],
            ['OEE', f"{oee_results['avg_oee']:.1f}%", '85%', f"{oee_results['world_class_gap']:.1f}%"]
        ]

        table = ax4.table(cellText=table_data, cellLoc='center', loc='center',
                         colWidths=[0.3, 0.2, 0.25, 0.25])
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 2)

        # Style header row
        for i in range(4):
            table[(0, i)].set_facecolor('#4CAF50')
            table[(0, i)].set_text_props(weight='bold', color='white')

        plt.suptitle('OEE Performance Dashboard', fontsize=16, fontweight='bold', y=0.98)

        return fig

# Example usage
shift_data = pd.DataFrame({
    'planned_production_time': [480, 480, 480, 480, 480],  # 8-hour shifts in minutes
    'downtime': [45, 30, 50, 35, 40],
    'units_produced': [850, 920, 800, 890, 870],
    'ideal_cycle_time': [0.5, 0.5, 0.5, 0.5, 0.5],  # 0.5 min per unit
    'defects': [25, 18, 35, 22, 20]
})

oee = OEEAnalysis(shift_data)

# Calculate OEE
results = oee.calculate_oee()

print("OEE Analysis:")
print(f"  Average Availability: {results['avg_availability']:.1f}%")
print(f"  Average Performance: {results['avg_performance']:.1f}%")
print(f"  Average Quality: {results['avg_quality']:.1f}%")
print(f"  Average OEE: {results['avg_oee']:.1f}%")
print(f"  Gap to World Class (85%): {results['world_class_gap']:.1f}%")

# Six Big Losses
losses = oee.six_big_losses_analysis(
    breakdown_hours=15,
    setup_hours=12,
    small_stops_hours=8,
    speed_loss_pct=5,
    process_defects=120,
    reduced_yield_pct=2
)

print("\nSix Big Losses Analysis:")
print(losses)

# Plot
fig = oee.plot_oee_dashboard(results)
plt.show()
```

---

## Spare Parts Optimization

```python
class SparePartsOptimization:
    """
    Optimize spare parts inventory
    Balance holding costs vs. stockout costs
    """

    def __init__(self, annual_demand, unit_cost, ordering_cost, holding_cost_pct,
                 lead_time_days, stockout_cost):
        """
        Parameters:
        - annual_demand: annual usage of spare part
        - unit_cost: cost per unit
        - ordering_cost: fixed cost per order
        - holding_cost_pct: annual holding cost as % of unit cost
        - lead_time_days: replenishment lead time
        - stockout_cost: cost per stockout incident
        """
        self.annual_demand = annual_demand
        self.unit_cost = unit_cost
        self.ordering_cost = ordering_cost
        self.holding_cost = unit_cost * holding_cost_pct
        self.lead_time_days = lead_time_days
        self.stockout_cost = stockout_cost

    def economic_order_quantity(self):
        """
        Calculate EOQ (Economic Order Quantity)

        EOQ = sqrt((2 * D * S) / H)
        Where:
        - D = annual demand
        - S = ordering cost
        - H = holding cost per unit per year
        """

        eoq = np.sqrt((2 * self.annual_demand * self.ordering_cost) / self.holding_cost)

        # Number of orders per year
        n_orders = self.annual_demand / eoq

        # Total cost
        ordering_cost_total = n_orders * self.ordering_cost
        holding_cost_total = (eoq / 2) * self.holding_cost
        total_cost = ordering_cost_total + holding_cost_total

        return {
            'eoq': eoq,
            'orders_per_year': n_orders,
            'ordering_cost': ordering_cost_total,
            'holding_cost': holding_cost_total,
            'total_cost': total_cost
        }

    def reorder_point(self, demand_std_dev, service_level=0.95):
        """
        Calculate reorder point with safety stock

        ROP = (Average Daily Demand × Lead Time) + Safety Stock
        Safety Stock = Z × σ_demand × sqrt(lead_time)
        """

        avg_daily_demand = self.annual_demand / 365

        # Z-score for service level
        z_score = stats.norm.ppf(service_level)

        # Safety stock
        safety_stock = z_score * demand_std_dev * np.sqrt(self.lead_time_days)

        # Reorder point
        rop = (avg_daily_demand * self.lead_time_days) + safety_stock

        return {
            'reorder_point': rop,
            'safety_stock': safety_stock,
            'avg_daily_demand': avg_daily_demand,
            'service_level': service_level * 100
        }

    def abc_classification(self, parts_data):
        """
        ABC classification of spare parts based on annual value

        parts_data: DataFrame with 'part_id', 'annual_usage', 'unit_cost'
        """

        df = parts_data.copy()

        # Calculate annual value
        df['annual_value'] = df['annual_usage'] * df['unit_cost']

        # Sort by value descending
        df = df.sort_values('annual_value', ascending=False)

        # Calculate cumulative percentage
        total_value = df['annual_value'].sum()
        df['cumulative_value'] = df['annual_value'].cumsum()
        df['cumulative_pct'] = (df['cumulative_value'] / total_value) * 100

        # Classify
        def classify(row):
            if row['cumulative_pct'] <= 80:
                return 'A'
            elif row['cumulative_pct'] <= 95:
                return 'B'
            else:
                return 'C'

        df['abc_class'] = df.apply(classify, axis=1)

        return df

# Example usage
spare_part = SparePartsOptimization(
    annual_demand=120,         # 120 units per year (10 per month)
    unit_cost=500,
    ordering_cost=100,
    holding_cost_pct=0.25,     # 25% of unit cost
    lead_time_days=30,
    stockout_cost=5000
)

# EOQ
eoq = spare_part.economic_order_quantity()
print("Economic Order Quantity:")
print(f"  EOQ: {eoq['eoq']:.0f} units")
print(f"  Orders per Year: {eoq['orders_per_year']:.1f}")
print(f"  Total Annual Cost: ${eoq['total_cost']:,.0f}")

# Reorder point
rop = spare_part.reorder_point(demand_std_dev=15, service_level=0.95)
print(f"\nReorder Point:")
print(f"  ROP: {rop['reorder_point']:.0f} units")
print(f"  Safety Stock: {rop['safety_stock']:.0f} units")
print(f"  Service Level: {rop['service_level']:.0f}%")

# ABC Classification example
parts_data = pd.DataFrame({
    'part_id': [f'PART-{i:03d}' for i in range(1, 21)],
    'annual_usage': np.random.randint(10, 500, 20),
    'unit_cost': np.random.uniform(50, 2000, 20)
})

abc_classification = spare_part.abc_classification(parts_data)
print(f"\nABC Classification:")
print(abc_classification[['part_id', 'annual_value', 'cumulative_pct', 'abc_class']].head(10))

print(f"\nABC Summary:")
print(abc_classification.groupby('abc_class').agg({
    'part_id': 'count',
    'annual_value': 'sum'
}))
```

---

## Tools & Libraries

### Python Libraries

**Reliability & Statistics:**
- `numpy`, `pandas`: Data manipulation
- `scipy.stats`: Statistical distributions (Weibull, exponential)
- `lifelines`: Survival analysis and reliability
- `reliability`: Reliability engineering library

**Visualization:**
- `matplotlib`, `seaborn`, `plotly`: Charts and dashboards

**Machine Learning (for PdM):**
- `scikit-learn`: Anomaly detection, classification
- `tensorflow`, `pytorch`: Deep learning for predictive models
- `tslearn`: Time series analysis

### Commercial Maintenance Software

**CMMS (Computerized Maintenance Management):**
- **SAP PM**: Plant maintenance module
- **IBM Maximo**: Enterprise asset management
- **Oracle EAM**: Enterprise asset management
- **Infor EAM**: Maintenance management
- **eMaint**: Cloud-based CMMS
- **Fiix**: Modern CMMS platform

**Predictive Maintenance:**
- **GE Predix**: Industrial IoT and PdM platform
- **Uptake**: Predictive maintenance software
- **C3 AI**: AI-based predictive maintenance
- **Azure IoT**: Microsoft PdM solutions
- **AWS IoT**: Amazon predictive maintenance

**Reliability Software:**
- **Reliasoft**: Reliability analysis tools
- **ARMS Reliability**: RAM (Reliability, Availability, Maintainability)
- **Item Software**: Reliability engineering

---

## Common Challenges & Solutions

### Challenge: Lack of Failure Data

**Problem:**
- New equipment, no history
- Poor record-keeping
- Insufficient data for analysis

**Solutions:**
- Start collecting data immediately (even manual logs)
- Use manufacturer reliability data as baseline
- Implement CMMS to track all maintenance activities
- Benchmark with similar equipment or industry data
- Use conservative assumptions until data accumulates

### Challenge: Balancing PM vs. PdM Investment

**Problem:**
- PdM requires sensors and technology investment
- Not all equipment justifies PdM cost
- Where to start?

**Solutions:**
- Use criticality analysis (RCM approach)
- Start PdM on most critical/expensive assets
- ROI analysis: compare cost of sensors vs. cost of failures
- Hybrid approach: PdM for critical, PM for others
- Pilot program on 1-2 assets first

### Challenge: Over-Maintenance

**Problem:**
- Too frequent PM wastes resources
- "If it ain't broke, don't fix it" mentality
- PM intervals too conservative

**Solutions:**
- Optimize PM intervals using cost models
- Transition to condition-based maintenance
- Track PM effectiveness (failures after PM?)
- Use Weibull analysis to understand failure patterns
- Pilot extended PM intervals on non-critical equipment

### Challenge: Emergency/Reactive Maintenance Dominance

**Problem:**
- Always fighting fires
- No time for planned maintenance
- High costs and poor availability

**Solutions:**
- Dedicate resources to preventive work (separate teams if needed)
- Schedule PM during planned downtime
- Root cause analysis on repeat failures
- Build maintenance backlog and prioritize
- Track reactive vs. planned maintenance ratio (target <20% reactive)

### Challenge: Spare Parts Inventory Issues

**Problem:**
- Stockouts of critical parts cause long downtime
- Excess inventory ties up capital
- Obsolete parts accumulate

**Solutions:**
- ABC classification (focus on high-value parts)
- Calculate optimal stock levels (ROP, safety stock)
- Vendor partnerships for critical parts
- Consignment inventory for slow-movers
- Regular inventory audits and obsolescence review

---

## Output Format

### Maintenance Plan Report

**Executive Summary:**
- Current maintenance strategy and performance
- Key reliability metrics (MTBF, MTTR, availability)
- Improvement opportunities and priorities
- Expected benefits

**Equipment Reliability Analysis:**

| Equipment | MTBF (hours) | MTTR (hours) | Availability | Failures/Year | Criticality |
|-----------|--------------|--------------|--------------|---------------|-------------|
| Pump-01 | 720 | 8 | 98.9% | 12 | High |
| Conveyor-02 | 1,440 | 4 | 99.7% | 6 | Medium |
| Press-03 | 480 | 16 | 96.7% | 18 | Critical |
| CNC-04 | 960 | 12 | 98.7% | 9 | High |

**Maintenance Strategy Recommendations:**

| Equipment | Current Strategy | Recommended Strategy | Rationale |
|-----------|-----------------|---------------------|-----------|
| Press-03 | Reactive | Predictive Maintenance | Critical asset, high failure cost |
| Pump-01 | PM (monthly) | PM (optimized to 6 weeks) | Over-maintained, can extend interval |
| Conveyor-02 | PM | Continue PM | Appropriate for criticality |
| CNC-04 | PM | Condition-Based Monitoring | Good candidate for CBM pilot |

**Preventive Maintenance Schedule:**
- Weekly: Lubrication, inspections (non-critical)
- Monthly: PM routines for critical equipment
- Quarterly: Major inspections and overhauls
- Annual: Compliance inspections and certifications

**Predictive Maintenance Implementation:**
- Phase 1 (Q1): Install vibration sensors on critical rotating equipment
- Phase 2 (Q2): Implement condition monitoring dashboard
- Phase 3 (Q3): Develop RUL models and alerts
- Phase 4 (Q4): Integrate with CMMS and production scheduling

**Expected Benefits:**
- Unplanned downtime reduction: 40-50%
- Maintenance cost reduction: 15-25%
- Equipment availability improvement: +2-3%
- Spare parts inventory reduction: 20%
- Equipment life extension: 10-15%

---

## Questions to Ask

If you need more context:
1. What equipment or assets need maintenance planning?
2. What are current failure rates and downtime levels?
3. What is the current maintenance approach? (reactive, preventive, predictive)
4. What are the critical assets that impact production most?
5. What is the cost of downtime vs. cost of maintenance?
6. Is condition monitoring equipment available?
7. Is a CMMS in place? What data is tracked?
8. What are the maintenance resource constraints?

---

## Related Skills

- **lean-manufacturing**: For TPM and waste elimination
- **quality-management**: For quality impact of equipment reliability
- **production-scheduling**: For maintenance scheduling integration
- **process-optimization**: For overall equipment optimization
- **prescriptive-analytics**: For predictive maintenance analytics
- **supply-chain-analytics**: For maintenance KPIs and dashboards
- **capacity-planning**: For capacity impact of maintenance
- **risk-mitigation**: For equipment failure risk assessment

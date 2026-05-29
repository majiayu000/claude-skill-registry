---
name: Sustainable AI & Green Computing (FinOps 2.0)
description: Implement carbon-aware computing, energy-efficient AI inference, and ESG-compliant infrastructure to reduce carbon footprint while maintaining performance and meeting sustainability regulations.
skill-id: 161
domain: Business / Sustainability / Infrastructure
level: Expert (Enterprise Scale)
maturity: Emerging (2026-2027)
---

# Sustainable AI & Green Computing (FinOps 2.0)

> **Current Level:** Expert (Enterprise Scale)
> **Domain:** Business / Sustainability / Infrastructure
> **Skill ID:** 161
> **Maturity:** Emerging - เตรียมความพร้อมสำหรับ 2026-2027

---

## Overview

Sustainable AI & Green Computing ขยายขอบเขตจาก FinOps แบบดั้งเดิม (Skill 126) ไปสู่การจัดการผลกระทบต่อสิ่งแวดล้อม ในปี 2026 องค์กรระดับโลกจะไม่ได้ดูแค่ "ต้นทุนเงิน" (Cloud Cost) แต่จะดู "ต้นทุนสิ่งแวดล้อม" (Carbon Footprint) ด้วย

---

## Why This Matters / Strategic Necessity

### Context

แรงกดดันด้านสิ่งแวดล้อมเพิ่มขึ้น:
- **ESG Regulations:** กฎระเบียบ ESG เข้มงวดขึ้น
- **Investor Pressure:** นักลงทุนต้องการข้อมูล Carbon Footprint
- **Customer Demand:** ลูกค้า Enterprise ต้องการ Sustainable Solutions
- **Cost Optimization:** พลังงานสะอาดมักถูกกว่าในบางช่วงเวลา

### Business Impact

- **ESG Compliance:** การทำตามมาตรฐาน ESG เพื่อดึงดูดนักลงทุน
- **Competitive Advantage:** องค์กรที่ Sustainable จะได้เปรียบ
- **Cost Savings:** พลังงานสะอาดและ Right-sizing ลดต้นทุน
- **Risk Mitigation:** ลดความเสี่ยงจากกฎระเบียบด้านสิ่งแวดล้อม

### Product Thinking

ทักษะนี้ช่วยแก้ปัญหา:
- **Sustainability Teams:** ต้องการลด Carbon Footprint
- **Finance Teams:** ต้องการ Balance Cost และ Sustainability
- **Engineering Teams:** ต้องการ Tools และ Patterns
- **Customers:** ต้องการ Sustainable Solutions

---

## Core Concepts / Technical Deep Dive

### 1. Carbon-Aware SDKs & Measurement

วัดการปล่อยคาร์บอนจากการประมวลผล

```python
import requests
from datetime import datetime
from typing import Dict, Optional

class CarbonIntensityAPI:
    """Interface to carbon intensity APIs"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.electricity_maps_api = "https://api.electricitymap.org"
        self.watttime_api = "https://api.watttime.org"
        self.api_key = api_key
    
    def get_carbon_intensity(
        self,
        region: str,
        timestamp: Optional[datetime] = None
    ) -> Dict:
        """
        Get current or historical carbon intensity for region.
        
        Returns gCO2/kWh
        """
        if timestamp:
            # Historical data
            url = f"{self.electricity_maps_api}/carbon-intensity/history"
            params = {
                "zone": region,
                "datetime": timestamp.isoformat()
            }
        else:
            # Current data
            url = f"{self.electricity_maps_api}/carbon-intensity/latest"
            params = {"zone": region}
        
        response = requests.get(url, params=params, headers={
            "auth-token": self.api_key
        })
        
        data = response.json()
        
        return {
            "region": region,
            "carbon_intensity": data.get("carbonIntensity", 0),  # gCO2/kWh
            "renewable_percentage": data.get("renewablePercentage", 0),
            "timestamp": data.get("datetime", datetime.utcnow().isoformat()),
            "forecast": data.get("forecast", [])  # Future predictions
        }

class CarbonFootprintCalculator:
    """Calculate carbon footprint of compute operations"""
    
    def __init__(self):
        self.carbon_api = CarbonIntensityAPI()
        self.gpu_emissions = {
            "A100": 0.5,  # kgCO2 per hour at 100% utilization
            "V100": 0.4,
            "T4": 0.2
        }
    
    def calculate_inference_carbon(
        self,
        region: str,
        gpu_type: str,
        inference_time_seconds: float,
        gpu_utilization: float = 1.0
    ) -> Dict:
        """
        Calculate carbon footprint of AI inference.
        
        Returns carbon footprint in kgCO2
        """
        # Get carbon intensity for region
        carbon_intensity = self.carbon_api.get_carbon_intensity(region)
        
        # Calculate energy consumption
        gpu_power_kw = self._get_gpu_power(gpu_type)  # kW
        energy_kwh = (gpu_power_kw * inference_time_seconds / 3600) * gpu_utilization
        
        # Calculate carbon footprint
        carbon_kg = (energy_kwh * carbon_intensity["carbon_intensity"]) / 1000
        
        return {
            "carbon_kg": carbon_kg,
            "energy_kwh": energy_kwh,
            "region": region,
            "carbon_intensity_gco2_per_kwh": carbon_intensity["carbon_intensity"],
            "renewable_percentage": carbon_intensity["renewable_percentage"],
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def calculate_training_carbon(
        self,
        region: str,
        gpu_type: str,
        training_hours: float,
        num_gpus: int
    ) -> Dict:
        """Calculate carbon footprint of model training"""
        total_carbon = 0
        hourly_carbon = []
        
        # Calculate for each hour (carbon intensity changes)
        for hour in range(int(training_hours)):
            timestamp = datetime.utcnow() - timedelta(hours=hour)
            carbon_intensity = self.carbon_api.get_carbon_intensity(
                region, timestamp
            )
            
            gpu_power_kw = self._get_gpu_power(gpu_type)
            energy_kwh = gpu_power_kw * num_gpus
            carbon_kg = (energy_kwh * carbon_intensity["carbon_intensity"]) / 1000
            
            total_carbon += carbon_kg
            hourly_carbon.append({
                "hour": hour,
                "carbon_kg": carbon_kg,
                "carbon_intensity": carbon_intensity["carbon_intensity"]
            })
        
        return {
            "total_carbon_kg": total_carbon,
            "training_hours": training_hours,
            "num_gpus": num_gpus,
            "gpu_type": gpu_type,
            "region": region,
            "hourly_breakdown": hourly_carbon,
            "average_carbon_intensity": sum(
                h["carbon_intensity"] for h in hourly_carbon
            ) / len(hourly_carbon)
        }
```

### 2. Energy-Efficient Inference

เลือก Region และช่วงเวลาที่ใช้พลังงานสะอาด

```python
class CarbonAwareScheduler:
    """Schedule AI workloads based on carbon intensity"""
    
    def __init__(self):
        self.carbon_api = CarbonIntensityAPI()
        self.regions = ["us-east-1", "eu-west-1", "ap-southeast-1"]
    
    def find_optimal_region(
        self,
        workload_type: str = "inference",
        urgency: str = "normal"
    ) -> Dict:
        """
        Find region with lowest carbon intensity.
        
        For non-urgent workloads, can wait for green energy windows.
        """
        region_carbon = {}
        
        for region in self.regions:
            carbon_intensity = self.carbon_api.get_carbon_intensity(region)
            region_carbon[region] = carbon_intensity
        
        # Sort by carbon intensity
        sorted_regions = sorted(
            region_carbon.items(),
            key=lambda x: x[1]["carbon_intensity"]
        )
        
        optimal_region = sorted_regions[0][0]
        optimal_carbon = sorted_regions[0][1]
        
        # Check forecast for better times
        if urgency == "low" and optimal_carbon.get("forecast"):
            forecast = optimal_carbon["forecast"]
            # Find time with lower carbon intensity
            best_forecast = min(
                forecast,
                key=lambda x: x.get("carbonIntensity", float('inf'))
            )
            
            if best_forecast["carbonIntensity"] < optimal_carbon["carbon_intensity"]:
                return {
                    "region": optimal_region,
                    "schedule_at": best_forecast["datetime"],
                    "current_carbon": optimal_carbon["carbon_intensity"],
                    "optimal_carbon": best_forecast["carbonIntensity"],
                    "savings_percent": (
                        (optimal_carbon["carbon_intensity"] - best_forecast["carbonIntensity"]) /
                        optimal_carbon["carbon_intensity"] * 100
                    )
                }
        
        return {
            "region": optimal_region,
            "schedule_at": None,  # Run now
            "carbon_intensity": optimal_carbon["carbon_intensity"],
            "renewable_percentage": optimal_carbon["renewable_percentage"]
        }
    
    def route_to_green_region(
        self,
        request: Dict,
        max_latency_ms: int = 100
    ) -> Dict:
        """
        Route inference request to greenest region within latency budget.
        """
        # Get carbon intensity for all regions
        region_options = []
        
        for region in self.regions:
            carbon = self.carbon_api.get_carbon_intensity(region)
            latency = self._estimate_latency(region, request["user_location"])
            
            if latency <= max_latency_ms:
                region_options.append({
                    "region": region,
                    "carbon_intensity": carbon["carbon_intensity"],
                    "latency_ms": latency,
                    "renewable_percentage": carbon["renewable_percentage"]
                })
        
        if not region_options:
            # Fallback to lowest latency
            return self._fallback_route(request)
        
        # Choose greenest within latency budget
        optimal = min(region_options, key=lambda x: x["carbon_intensity"])
        
        return {
            "selected_region": optimal["region"],
            "carbon_intensity": optimal["carbon_intensity"],
            "latency_ms": optimal["latency_ms"],
            "renewable_percentage": optimal["renewable_percentage"],
            "carbon_savings_vs_default": self._calculate_savings(optimal)
        }
```

### 3. Sustainable Architecture Patterns

Right-sizing และ Edge Computing เพื่อลด Carbon

```python
class SustainableArchitecture:
    """Architecture patterns for reducing carbon footprint"""
    
    def optimize_for_energy(
        self,
        workload: Dict,
        performance_requirements: Dict
    ) -> Dict:
        """
        Optimize architecture for energy efficiency.
        
        Considers: right-sizing, spot instances, edge computing
        """
        recommendations = []
        
        # Right-sizing analysis
        current_resources = workload["resources"]
        optimal_resources = self._right_size(
            workload, performance_requirements
        )
        
        if optimal_resources["cpu"] < current_resources["cpu"]:
            recommendations.append({
                "type": "right_sizing",
                "current": current_resources,
                "optimal": optimal_resources,
                "energy_savings_percent": (
                    (current_resources["cpu"] - optimal_resources["cpu"]) /
                    current_resources["cpu"] * 100
                ),
                "carbon_savings_kg_per_month": self._calculate_carbon_savings(
                    current_resources, optimal_resources
                )
            })
        
        # Spot/Preemptible instances
        if workload.get("tolerance_for_interruption"):
            recommendations.append({
                "type": "spot_instances",
                "description": "Use spot instances for non-critical workloads",
                "cost_savings_percent": 70,
                "carbon_savings": "Same carbon, but uses otherwise idle capacity"
            })
        
        # Edge computing
        if self._is_edge_candidate(workload):
            recommendations.append({
                "type": "edge_computing",
                "description": "Move computation closer to data source",
                "data_transfer_reduction_gb": self._estimate_data_reduction(workload),
                "carbon_savings": "Reduces data center energy + network energy"
            })
        
        return {
            "workload_id": workload["id"],
            "recommendations": recommendations,
            "total_potential_savings": self._sum_savings(recommendations)
        }
    
    def _right_size(
        self,
        workload: Dict,
        requirements: Dict
    ) -> Dict:
        """Calculate optimal resource allocation"""
        # Analyze historical usage
        usage_history = self._get_usage_history(workload["id"])
        
        # Calculate percentiles
        cpu_p95 = np.percentile([u["cpu"] for u in usage_history], 95)
        memory_p95 = np.percentile([u["memory"] for u in usage_history], 95)
        
        # Add 20% headroom
        optimal = {
            "cpu": cpu_p95 * 1.2,
            "memory": memory_p95 * 1.2
        }
        
        return optimal
```

### 4. Carbon Reporting & Dashboards

รายงาน Carbon Footprint แบบ Real-time

```python
class CarbonReporting:
    """Generate carbon footprint reports and dashboards"""
    
    def generate_esg_report(
        self,
        period_start: datetime,
        period_end: datetime,
        scope: str = "all"  # scope1, scope2, scope3, all
    ) -> Dict:
        """
        Generate ESG-compliant carbon footprint report.
        
        Follows GHG Protocol (Scope 1, 2, 3)
        """
        report = {
            "period": {
                "start": period_start.isoformat(),
                "end": period_end.isoformat()
            },
            "scope1": {},  # Direct emissions
            "scope2": {},  # Indirect emissions (purchased energy)
            "scope3": {},  # Other indirect emissions
            "total": {}
        }
        
        # Scope 2: Cloud computing emissions
        if scope in ["scope2", "all"]:
            cloud_emissions = self._calculate_cloud_emissions(
                period_start, period_end
            )
            report["scope2"] = {
                "cloud_computing": cloud_emissions,
                "total_kg_co2": cloud_emissions["total_kg"]
            }
        
        # Scope 3: Upstream and downstream
        if scope in ["scope3", "all"]:
            report["scope3"] = {
                "employee_travel": self._calculate_travel_emissions(period_start, period_end),
                "purchased_goods": self._calculate_purchased_emissions(period_start, period_end),
                "downstream_transport": self._calculate_transport_emissions(period_start, period_end)
            }
        
        # Total
        report["total"] = {
            "kg_co2": (
                report.get("scope1", {}).get("total_kg", 0) +
                report.get("scope2", {}).get("total_kg", 0) +
                sum(v.get("total_kg", 0) for v in report.get("scope3", {}).values())
            ),
            "equivalent_trees": self._kg_to_trees(report["total"]["kg_co2"]),
            "equivalent_flights": self._kg_to_flights(report["total"]["kg_co2"])
        }
        
        return report
    
    def create_carbon_dashboard(
        self,
        services: List[str]
    ) -> Dict:
        """Create real-time carbon dashboard"""
        dashboard = {
            "timestamp": datetime.utcnow().isoformat(),
            "services": []
        }
        
        for service in services:
            service_carbon = {
                "service_name": service,
                "current_carbon_intensity": self._get_service_carbon(service),
                "carbon_today_kg": self._get_daily_carbon(service),
                "carbon_this_month_kg": self._get_monthly_carbon(service),
                "trend": self._get_trend(service),
                "top_regions": self._get_top_regions(service),
                "recommendations": self._get_recommendations(service)
            }
            dashboard["services"].append(service_carbon)
        
        dashboard["summary"] = {
            "total_carbon_today_kg": sum(
                s["carbon_today_kg"] for s in dashboard["services"]
            ),
            "renewable_percentage": self._calculate_avg_renewable(dashboard["services"]),
            "vs_last_month_percent": self._compare_to_last_month(dashboard)
        }
        
        return dashboard
```

---

## Tooling & Tech Stack

### Enterprise Tools

- **Carbon Measurement:**
  - Cloud Carbon Footprint (Open Source)
  - Microsoft Emissions Impact Dashboard
  - AWS Customer Carbon Footprint Tool
  - Google Carbon Footprint

- **Carbon Intensity APIs:**
  - Electricity Maps API
  - WattTime API
  - Carbon Intensity API (UK)

- **Green Software:**
  - Green Software Foundation Tools
  - Scaphandre (power consumption monitoring)

### Configuration Essentials

```yaml
# sustainable-ai-config.yaml
carbon:
  measurement:
    enabled: true
    frequency: "real-time"
    scope: ["scope2", "scope3"]
  
  scheduling:
    carbon_aware: true
    preferred_regions: ["eu-west-1", "us-west-2"]  # Regions with more renewables
    green_window_routing: true
    max_latency_ms: 100
  
  reporting:
    esg_reporting: true
    frequency: "monthly"
    standards: ["GHG_Protocol", "ISO_14064", "SBTi"]
  
  optimization:
    right_sizing: true
    spot_instances: true
    edge_computing: true
    model_optimization: true  # Quantization, pruning
```

---

## Standards, Compliance & Security

### International Standards

- **GHG Protocol:** Scope 1, 2, 3 emissions
- **ISO 14064:** Carbon footprint measurement
- **SBTi:** Science Based Targets initiative
- **CDP:** Carbon Disclosure Project

### Compliance Features

- **ESG Reporting:** Automated ESG report generation
- **Carbon Budgets:** Set and track carbon budgets
- **Offset Tracking:** Track carbon offsets
- **Verification:** Third-party verification support

---

## Quick Start / Getting Ready

### Phase 1: Measurement (Week 1-2)

1. **Deploy Carbon Measurement:**
   ```python
   from cloud_carbon_footprint import CloudCarbonFootprint
   
   ccf = CloudCarbonFootprint()
   footprint = ccf.calculate_footprint(
       start_date="2024-01-01",
       end_date="2024-01-31"
   )
   ```

2. **Set Up Carbon Intensity Monitoring:**
   - Integrate Electricity Maps API
   - Monitor regional carbon intensity
   - Set up alerts

### Phase 2: Optimization (Week 3-6)

1. **Implement Carbon-Aware Routing:**
   ```python
   scheduler = CarbonAwareScheduler()
   optimal = scheduler.find_optimal_region(workload_type="inference")
   ```

2. **Right-Size Resources:**
   - Analyze usage patterns
   - Downsize over-provisioned resources
   - Implement auto-scaling

### Phase 3: Reporting (Week 7-8)

1. **Generate ESG Reports:**
   - Set up monthly reporting
   - Create dashboards
   - Prepare for audits

---

## Production Checklist

- [ ] **Measurement:**
  - [ ] Carbon measurement deployed
  - [ ] Real-time monitoring enabled
  - [ ] Historical data collected

- [ ] **Optimization:**
  - [ ] Carbon-aware scheduling implemented
  - [ ] Resources right-sized
  - [ ] Green regions prioritized

- [ ] **Reporting:**
  - [ ] ESG reports automated
  - [ ] Dashboards created
  - [ ] Compliance verified

---

## Anti-patterns

### 1. **Ignoring Carbon Intensity**
❌ **Bad:** Always use same region regardless of carbon
```python
# ❌ Bad - No carbon awareness
region = "us-east-1"  # Always same region
```

✅ **Good:** Route based on carbon intensity
```python
# ✅ Good - Carbon-aware
scheduler = CarbonAwareScheduler()
region = scheduler.find_optimal_region()["region"]
```

### 2. **Over-Provisioning Resources**
❌ **Bad:** Over-provision "just in case"
```python
# ❌ Bad - Wasteful
resources = {"cpu": 16, "memory": "64GB"}  # Way more than needed
```

✅ **Good:** Right-size based on actual usage
```python
# ✅ Good - Optimized
resources = right_size(workload, requirements)  # Just enough
```

---

## Timeline & Adoption Curve

### 2024-2025: Early Adopters
- Tech companies leading the way
- ESG reporting becoming standard
- Carbon measurement tools mature

### 2025-2026: Mainstream
- Regulatory requirements increase
- Investor pressure intensifies
- Carbon-aware computing standard

### 2026-2027: Mandatory
- ESG regulations enforced
- Carbon budgets required
- Competitive necessity

---

## Unit Economics & Performance Metrics (KPIs)

### Cost Calculation

```
Total Cost = Cloud Cost + Carbon Cost + Compliance Cost

Carbon Cost = (Carbon kg × Carbon Price per kg)
Carbon Price = $50-150 per ton CO2 (varies by market)

Example:
- 1000 kg CO2/month
- Carbon price: $100/ton = $0.10/kg
- Carbon cost: 1000 × $0.10 = $100/month
- Plus potential savings from green energy: 20-30% cheaper
```

### Key Performance Indicators

- **Carbon Intensity:** gCO2 per inference/request (Target: < 1g)
- **Renewable Percentage:** % of energy from renewables (Target: > 80%)
- **Carbon Reduction:** % reduction vs baseline (Target: > 30%)
- **ESG Score:** Compliance score (Target: > 90%)

---

## Integration Points / Related Skills

- [Skill 126: Cloud Unit Economics](../81-saas-finops-pricing/cloud-unit-economics/SKILL.md) - Cost calculations
- [Skill 131: Cost Optimization](../81-saas-finops-pricing/cost-optimization-automation/SKILL.md) - Resource optimization
- [Skill 102: Model Optimization](../78-inference-model-serving/model-optimization-quantization/SKILL.md) - Energy-efficient models

---

## Further Reading

- [Green Software Foundation](https://greensoftware.foundation/)
- [Cloud Carbon Footprint](https://www.cloudcarbonfootprint.org/)
- [Electricity Maps](https://www.electricitymaps.com/)
- [GHG Protocol](https://ghgprotocol.org/)
- [Science Based Targets](https://sciencebasedtargets.org/)

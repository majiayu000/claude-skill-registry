---
name: self-improvement-engineer-role
description: Role assignment for Claude Agent #7 - Self-improvement engine for Lead Hunter Prime. Build ONLY the self-improvement system (daily metrics cron, feedback analysis, skill spawning, A/B testing). Do NOT build database, validation API, ingestion API, or dashboard.
---

# Agent #7: Self-Improvement Engineer - Role Assignment

## 🎯 Your Mission

You are Agent #7 in the Lead Hunter Prime multi-agent system. Your SOLE responsibility is to build the self-improvement engine that makes the lead system smarter over time.

**What you BUILD:**
- ✅ Daily metrics cron job (analyzes performance daily)
- ✅ Feedback analysis system (learns from agent feedback)
- ✅ Bottleneck detection (identifies where leads drop off)
- ✅ Skill spawning logic (creates targeted improvements)
- ✅ A/B testing framework (validates improvements)

**What you DO NOT build:**
- ❌ Database schema (Agent #1 already built this - it's DONE)
- ❌ Validation API (Agent #5 is building that)
- ❌ Ingestion API (Agent #6 is building that)
- ❌ Dashboard (Week 2 - separate team)
- ❌ N8N workflows (Agent #2 - separate system)

---

## 📊 Database Schema (Already Built)

Agent #1 created these tables for you. **DO NOT modify them.**

### Your Input Tables (Read-Only)
- `lh_feedback_log` - Agent feedback on lead quality
- `lh_validation_history` - Validation attempt logs
- `lh_lead_status` - Lead progression through pipeline
- `lh_contacts` - Contact validation status
- `lh_properties` - Property distress data

### Your Output Tables (Read/Write)
- `lh_daily_metrics` - Write aggregate performance data
- `lh_pattern_performance` - Track pattern accuracy over time
- `lh_spawned_skills` - Log skills you create
- `lh_ab_tests` - Track experiments and results

### Helper Function Available
```sql
-- Calculates and updates daily metrics
SELECT lh_update_daily_metrics(); -- for today
SELECT lh_update_daily_metrics('2025-01-20'); -- for specific date
```

**Your job:** Call this function daily via cron, then analyze the results.

---

## 🔄 The Self-Improvement Loop

```
1. MONITOR → Run daily metrics cron (12:01 AM)
2. ANALYZE → Identify bottlenecks (conversion drops, slow response, poor quality)
3. SPAWN → Create targeted skill to fix problem
4. TEST → Run A/B test with statistical rigor
5. DECIDE → Keep (if lift > 10%, p < 0.05), Kill (if no impact), or Continue
6. REPEAT → Forever
```

---

## 🚀 What You Need to Build

### Component #1: Daily Metrics Cron Job

**File:** `supabase/functions/lead-hunter-daily-metrics/index.ts`

**Purpose:** Runs every day at 12:01 AM to calculate performance metrics.

**What it does:**
1. Calls `lh_update_daily_metrics()` function (Agent #1 built this)
2. Analyzes results to detect bottlenecks:
   - Conversion rate drops (e.g., contacted → qualified dropped from 60% to 40%)
   - Response time slowdowns (e.g., avg response time increased from 2h to 8h)
   - Validation accuracy degradation (e.g., business detection dropped from 87% to 75%)
3. If bottleneck detected → Trigger skill spawning logic

**Schedule:** Daily via Supabase Edge Function cron

**Example Implementation:**
```typescript
// supabase/functions/lead-hunter-daily-metrics/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

serve(async (req) => {
  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
  );

  // Step 1: Update daily metrics
  const { data: metricsResult, error: metricsError } = await supabase
    .rpc('lh_update_daily_metrics');

  if (metricsError) {
    return new Response(JSON.stringify({ error: metricsError }), { status: 500 });
  }

  // Step 2: Fetch today's metrics
  const { data: todayMetrics, error: fetchError } = await supabase
    .from('lh_daily_metrics')
    .select('*')
    .eq('metric_date', new Date().toISOString().split('T')[0])
    .single();

  if (fetchError || !todayMetrics) {
    return new Response(JSON.stringify({ error: fetchError }), { status: 500 });
  }

  // Step 3: Detect bottlenecks
  const bottlenecks = await detectBottlenecks(supabase, todayMetrics);

  // Step 4: Spawn skills if needed
  for (const bottleneck of bottlenecks) {
    await considerSpawningSkill(supabase, bottleneck);
  }

  return new Response(
    JSON.stringify({
      success: true,
      metrics: todayMetrics,
      bottlenecks
    }),
    { headers: { "Content-Type": "application/json" } }
  );
});
```

---

### Component #2: Bottleneck Detection Logic

**Purpose:** Analyze metrics to identify where the system is underperforming.

**Common Bottleneck Patterns:**

1. **Low Response Rate**
   - Detection: `avg_response_time_hours > 4` OR `contacted_count / new_leads_count < 0.6`
   - Action: Spawn "instant-responder" skill

2. **Poor Qualification**
   - Detection: `qualified_count / contacted_count < 0.3`
   - Action: Spawn "lead-scorer" skill

3. **Validation Accuracy Drop**
   - Detection: `validation_accuracy < 0.80` (from lh_pattern_performance)
   - Action: Retrain business patterns, spawn "pattern-optimizer" skill

4. **Slow Follow-Up**
   - Detection: Average time from contacted → qualified > 5 days
   - Action: Spawn "follow-up-sequencer" skill

5. **Weak Lead Sources**
   - Detection: Specific source has conversion rate < 10% (while others are 30%+)
   - Action: Spawn "source-optimizer" skill

**Example Detection Function:**
```typescript
async function detectBottlenecks(supabase, todayMetrics) {
  const bottlenecks = [];

  // Bottleneck #1: Low response rate
  if (todayMetrics.avg_response_time_hours > 4) {
    bottlenecks.push({
      type: 'low_response_rate',
      severity: 'high',
      metric: 'avg_response_time_hours',
      current_value: todayMetrics.avg_response_time_hours,
      target_value: 2,
      suggested_skill: 'instant-responder'
    });
  }

  // Bottleneck #2: Poor qualification rate
  const qualificationRate = todayMetrics.qualified_count / todayMetrics.contacted_count;
  if (qualificationRate < 0.3) {
    bottlenecks.push({
      type: 'poor_qualification',
      severity: 'medium',
      metric: 'qualification_rate',
      current_value: qualificationRate,
      target_value: 0.5,
      suggested_skill: 'lead-scorer'
    });
  }

  // Bottleneck #3: Validation accuracy drop
  const { data: patternPerf } = await supabase
    .from('lh_pattern_performance')
    .select('avg_f1_score')
    .order('performance_date', { ascending: false })
    .limit(1)
    .single();

  if (patternPerf && patternPerf.avg_f1_score < 0.80) {
    bottlenecks.push({
      type: 'validation_accuracy_drop',
      severity: 'high',
      metric: 'f1_score',
      current_value: patternPerf.avg_f1_score,
      target_value: 0.87,
      suggested_skill: 'pattern-optimizer'
    });
  }

  return bottlenecks;
}
```

---

### Component #3: Skill Spawning Logic

**Purpose:** When a bottleneck is detected, decide whether to spawn a new skill or continue testing an existing one.

**Decision Tree:**
1. Check if skill already exists for this bottleneck type
2. If exists and currently testing → Continue test, don't spawn duplicate
3. If exists and killed → Check if enough time has passed to retry (30 days)
4. If doesn't exist → Spawn new skill with A/B test plan

**Example Spawning Function:**
```typescript
async function considerSpawningSkill(supabase, bottleneck) {
  // Check if we already have a skill for this bottleneck
  const { data: existingSkill } = await supabase
    .from('lh_spawned_skills')
    .select('*')
    .eq('skill_type', bottleneck.suggested_skill)
    .order('spawned_at', { ascending: false })
    .limit(1)
    .single();

  // If skill is currently being tested, don't spawn duplicate
  if (existingSkill && existingSkill.status === 'testing') {
    console.log(`Skill ${bottleneck.suggested_skill} already testing`);
    return;
  }

  // If skill was killed recently (< 30 days), don't retry yet
  if (existingSkill && existingSkill.status === 'killed') {
    const daysSinceKilled = (Date.now() - new Date(existingSkill.decision_made_at).getTime()) / (1000 * 60 * 60 * 24);
    if (daysSinceKilled < 30) {
      console.log(`Skill ${bottleneck.suggested_skill} killed recently, waiting ${30 - daysSinceKilled} more days`);
      return;
    }
  }

  // Spawn new skill
  const { data: newSkill, error } = await supabase
    .from('lh_spawned_skills')
    .insert({
      skill_type: bottleneck.suggested_skill,
      skill_name: `Auto-spawned ${bottleneck.suggested_skill} v${Date.now()}`,
      problem_detected: bottleneck.type,
      target_metric: bottleneck.metric,
      baseline_value: bottleneck.current_value,
      target_value: bottleneck.target_value,
      status: 'testing',
      spawned_at: new Date().toISOString()
    })
    .select()
    .single();

  if (error) {
    console.error('Failed to spawn skill:', error);
    return;
  }

  // Create A/B test for this skill
  await createABTest(supabase, newSkill, bottleneck);

  console.log(`Spawned new skill: ${newSkill.skill_name}`);
}
```

---

### Component #4: A/B Testing Framework

**Purpose:** Validate that a spawned skill actually improves metrics before rolling it out to 100% of leads.

**Test Structure:**
- Control group: 50% of leads get existing process
- Treatment group: 50% of leads get new skill
- Minimum sample: 100 leads per group
- Significance threshold: p-value < 0.05
- Success criteria: Lift > 10%

**Example A/B Test Creation:**
```typescript
async function createABTest(supabase, skill, bottleneck) {
  const { data: test, error } = await supabase
    .from('lh_ab_tests')
    .insert({
      test_name: `Test: ${skill.skill_name}`,
      skill_id: skill.id,
      hypothesis: `${skill.skill_type} will improve ${bottleneck.metric} from ${bottleneck.current_value} to ${bottleneck.target_value}`,
      control_description: 'Existing process (no intervention)',
      treatment_description: `Apply ${skill.skill_type} intervention`,
      metric_tracked: bottleneck.metric,
      traffic_allocation_pct: 50,
      min_sample_size: 100,
      confidence_level: 0.95,
      status: 'running',
      started_at: new Date().toISOString()
    })
    .select()
    .single();

  if (error) {
    console.error('Failed to create A/B test:', error);
    return;
  }

  console.log(`Created A/B test: ${test.test_name}`);
}
```

**Assignment Logic (for other agents to implement):**
When a new lead comes in, check if any A/B tests are running. If yes, assign lead to control or treatment group:

```typescript
// This logic would be added to Agent #6 (Ingestion API)
const leadId = newLead.id;
const isControl = leadId % 2 === 0; // Simple 50/50 split

if (isControl) {
  // Apply existing process
} else {
  // Apply treatment (call spawned skill)
}

// Log assignment
await supabase.from('lh_lead_status').update({
  ab_test_group: isControl ? 'control' : 'treatment'
}).eq('id', leadId);
```

---

### Component #5: Test Results Analysis

**Purpose:** After sufficient sample size, analyze results and decide: keep, kill, or continue testing.

**File:** `supabase/functions/lead-hunter-ab-analysis/index.ts`

**Run frequency:** Weekly (every Monday)

**Analysis Steps:**
1. Fetch all running A/B tests
2. For each test:
   - Check if min sample size reached (100 per group)
   - Calculate conversion rates for control vs treatment
   - Calculate lift (% improvement)
   - Calculate p-value (statistical significance)
3. Make decision:
   - **KEEP:** lift > 10% AND p < 0.05 → Deploy to 100% of leads
   - **KILL:** lift < 5% OR p > 0.10 → Revert to control
   - **CONTINUE:** Promising but not significant → Let run longer

**Example Analysis Function:**
```typescript
async function analyzeABTest(supabase, test) {
  // Fetch results for this test
  const { data: controlResults } = await supabase
    .from('lh_lead_status')
    .select('id, status')
    .eq('ab_test_id', test.id)
    .eq('ab_test_group', 'control');

  const { data: treatmentResults } = await supabase
    .from('lh_lead_status')
    .select('id, status')
    .eq('ab_test_id', test.id)
    .eq('ab_test_group', 'treatment');

  // Check sample size
  if (!controlResults || !treatmentResults) return;
  if (controlResults.length < test.min_sample_size || treatmentResults.length < test.min_sample_size) {
    console.log(`Test ${test.test_name} needs more data`);
    return;
  }

  // Calculate conversion rates
  const controlConversions = controlResults.filter(l => ['qualified', 'closed'].includes(l.status)).length;
  const treatmentConversions = treatmentResults.filter(l => ['qualified', 'closed'].includes(l.status)).length;

  const controlRate = controlConversions / controlResults.length;
  const treatmentRate = treatmentConversions / treatmentResults.length;

  const lift = ((treatmentRate - controlRate) / controlRate) * 100;

  // Calculate p-value (simplified chi-square test)
  const pValue = calculatePValue(controlConversions, controlResults.length, treatmentConversions, treatmentResults.length);

  // Make decision
  let recommendation = 'CONTINUE';
  let winner = null;

  if (lift > 10 && pValue < 0.05) {
    recommendation = 'KEEP';
    winner = 'treatment';
  } else if (lift < 5 || pValue > 0.10) {
    recommendation = 'KILL';
    winner = 'control';
  }

  // Update test results
  await supabase.from('lh_ab_tests').update({
    control_sample_size: controlResults.length,
    treatment_sample_size: treatmentResults.length,
    control_conversion_rate: controlRate,
    treatment_conversion_rate: treatmentRate,
    lift_pct: lift,
    p_value: pValue,
    winner,
    recommendation,
    ended_at: recommendation !== 'CONTINUE' ? new Date().toISOString() : null,
    status: recommendation !== 'CONTINUE' ? 'completed' : 'running'
  }).eq('id', test.id);

  // Update spawned skill status
  if (recommendation === 'KEEP') {
    await supabase.from('lh_spawned_skills').update({
      status: 'active',
      actual_lift_pct: lift,
      decision_made_at: new Date().toISOString()
    }).eq('id', test.skill_id);
  } else if (recommendation === 'KILL') {
    await supabase.from('lh_spawned_skills').update({
      status: 'killed',
      actual_lift_pct: lift,
      decision_made_at: new Date().toISOString()
    }).eq('id', test.skill_id);
  }

  console.log(`Test ${test.test_name} - Recommendation: ${recommendation}, Lift: ${lift.toFixed(2)}%, p-value: ${pValue.toFixed(4)}`);
}

function calculatePValue(controlSuccesses, controlTotal, treatmentSuccesses, treatmentTotal) {
  // Simplified chi-square test for proportions
  const p1 = controlSuccesses / controlTotal;
  const p2 = treatmentSuccesses / treatmentTotal;
  const pPool = (controlSuccesses + treatmentSuccesses) / (controlTotal + treatmentTotal);

  const se = Math.sqrt(pPool * (1 - pPool) * (1/controlTotal + 1/treatmentTotal));
  const z = Math.abs(p2 - p1) / se;

  // Convert z-score to p-value (two-tailed)
  const pValue = 2 * (1 - normalCDF(z));

  return pValue;
}

function normalCDF(z) {
  // Approximation of normal CDF
  return 0.5 * (1 + erf(z / Math.sqrt(2)));
}

function erf(x) {
  // Approximation of error function
  const sign = x >= 0 ? 1 : -1;
  x = Math.abs(x);

  const a1 =  0.254829592;
  const a2 = -0.284496736;
  const a3 =  1.421413741;
  const a4 = -1.453152027;
  const a5 =  1.061405429;
  const p  =  0.3275911;

  const t = 1.0 / (1.0 + p * x);
  const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);

  return sign * y;
}
```

---

## 📁 File Structure You Need to Create

```
supabase/functions/
├── lead-hunter-daily-metrics/
│   └── index.ts          # Daily cron job (12:01 AM)
└── lead-hunter-ab-analysis/
    └── index.ts          # Weekly A/B test analysis (Monday)
```

---

## ✅ Success Criteria

Your mission is complete when:

1. ✅ Daily metrics cron job runs successfully
   - Calls `lh_update_daily_metrics()` function
   - Detects bottlenecks accurately
   - Spawns skills when appropriate

2. ✅ Bottleneck detection works
   - Identifies low response rate (avg > 4 hours)
   - Identifies poor qualification (rate < 30%)
   - Identifies validation accuracy drops (< 80%)

3. ✅ Skill spawning logic works
   - Doesn't spawn duplicates
   - Creates skill records in `lh_spawned_skills`
   - Creates corresponding A/B tests

4. ✅ A/B testing framework works
   - Tests run with 50/50 split
   - Sample size tracked correctly
   - Statistical analysis is rigorous

5. ✅ Test results analysis works
   - Correctly calculates lift and p-value
   - Makes KEEP/KILL/CONTINUE decisions
   - Updates skill status accordingly

---

## 🧪 How to Test

### Test #1: Daily Metrics Cron

```bash
# Manually trigger the function
curl -X POST https://your-project.supabase.co/functions/v1/lead-hunter-daily-metrics \
  -H "Authorization: Bearer YOUR_ANON_KEY"

# Check lh_daily_metrics table
psql -c "SELECT * FROM lh_daily_metrics ORDER BY metric_date DESC LIMIT 1;"
```

### Test #2: Bottleneck Detection

```bash
# Insert test data with poor performance
psql -c "
INSERT INTO lh_lead_status (property_id, status, assigned_to, contacted_at, created_at)
VALUES
  (1, 'contacted', 'agent-1', NOW() - INTERVAL '10 hours', NOW() - INTERVAL '12 hours'),
  (2, 'contacted', 'agent-1', NOW() - INTERVAL '8 hours', NOW() - INTERVAL '10 hours');
"

# Run metrics cron
curl -X POST https://your-project.supabase.co/functions/v1/lead-hunter-daily-metrics

# Should detect "low_response_rate" bottleneck
```

### Test #3: Skill Spawning

```bash
# After bottleneck detected, check lh_spawned_skills
psql -c "SELECT * FROM lh_spawned_skills ORDER BY spawned_at DESC LIMIT 1;"

# Should see a new skill with status = 'testing'

# Check A/B test created
psql -c "SELECT * FROM lh_ab_tests ORDER BY started_at DESC LIMIT 1;"
```

### Test #4: A/B Test Analysis

```bash
# Insert test results (100 control, 100 treatment)
# Control: 30% conversion, Treatment: 45% conversion
# (Insert 100 leads per group with appropriate conversion rates)

# Run analysis
curl -X POST https://your-project.supabase.co/functions/v1/lead-hunter-ab-analysis

# Check recommendation
psql -c "SELECT test_name, lift_pct, p_value, recommendation FROM lh_ab_tests WHERE status = 'completed';"

# Should show KEEP with ~50% lift
```

---

## 🚨 Common Mistakes to Avoid

1. **DON'T modify database schema**
   - Agent #1 already built all tables
   - If you need a column, ask Kelvin first

2. **DON'T spawn duplicate skills**
   - Always check if skill type already exists and is testing

3. **DON'T call winners early**
   - Wait for min sample size (100 per group)
   - Require statistical significance (p < 0.05)

4. **DON'T confound experiments**
   - Only run ONE experiment per bottleneck at a time
   - Don't test multiple skills simultaneously on same metric

5. **DON'T ignore segment differences**
   - A skill might work for Zillow leads but not referrals
   - Track performance by lead source

---

## 🔗 Integration with Other Agents

### Agent #5: Validation API
- You analyze their validation results in `lh_validation_history`
- If accuracy drops, you spawn "pattern-optimizer" skill
- They implement your skill recommendations

### Agent #6: Ingestion API
- You detect if response time is slow
- You spawn "instant-responder" skill
- They implement the auto-response logic

### Dashboard (Week 2)
- You populate `lh_daily_metrics` for their charts
- You track experiments in `lh_ab_tests` for their experiment monitor
- They display your skill performance in admin view

---

## 📊 Priority Order

Build in this order:

1. **Week 1:** Daily metrics cron + basic bottleneck detection
2. **Week 1:** Skill spawning logic (just log to table, don't implement skills yet)
3. **Week 2:** A/B testing framework
4. **Week 2:** Test results analysis and decision-making
5. **Week 3+:** Implement actual skills (instant-responder, lead-scorer, etc.)

---

## 🎯 Key Principles

1. **Measure first, optimize second** - Don't spawn skills without baseline data
2. **One variable at a time** - Only test one improvement per metric
3. **Statistical rigor** - Don't trust results without proper sample size and significance
4. **Kill bad ideas fast** - Don't let ego keep underperforming skills alive
5. **Document everything** - Log why skills were spawned, what they tested, results

---

## 🔥 You Got This

You're building the brain of Lead Hunter Prime. The system that makes it smarter over time. The AI that has a will to get better.

**Focus on:**
- Rock-solid bottleneck detection
- Rigorous A/B testing
- Clear KEEP/KILL decisions

**Don't worry about:**
- Making skills perfect on first try (tests will tell you if they work)
- Building all skill implementations now (spawn them first, implement later)
- Dashboard integration (Week 2 team handles that)

---

**Ready?** Start with the daily metrics cron. Get that running, then build bottleneck detection on top of it.

🚀 **LET'S SHIP THE BRAIN!**

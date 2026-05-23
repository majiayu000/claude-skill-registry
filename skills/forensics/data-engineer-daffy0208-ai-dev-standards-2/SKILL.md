---
name: forensic-data-engineer
description: Expert in data forensics, anomaly detection, audit trail analysis, fraud detection, and breach investigation
version: 1.0.0
tags: [forensics, security, audit, fraud-detection, anomaly-detection, compliance, investigation]
---

# Forensic Data Engineer Skill

I help you investigate data anomalies, detect fraud, analyze audit trails, and ensure data integrity and compliance.

## What I Do

**Forensic Analysis:**

- Anomaly detection and pattern recognition
- Fraud detection and prevention
- Breach investigation and root cause analysis
- Data integrity verification

**Audit & Compliance:**

- Audit trail analysis and reconstruction
- Chain of custody maintenance
- Regulatory compliance (GDPR, SOC2, HIPAA)
- Access control auditing

**Data Recovery:**

- Forensic recovery of deleted data
- Historical data reconstruction
- Change detection and unauthorized modifications
- Data lineage and provenance tracking

## Forensic Patterns

### Pattern 1: Audit Trail Implementation

**Use case:** Track all data changes for compliance and investigation

```typescript
// lib/forensics/audit-trail.ts

interface AuditEntry {
  id: string
  timestamp: Date
  userId: string
  action: 'CREATE' | 'UPDATE' | 'DELETE' | 'READ'
  tableName: string
  recordId: string
  oldValue?: any
  newValue?: any
  ipAddress: string
  userAgent: string
  sessionId: string
}

export async function createAuditLog(entry: Omit<AuditEntry, 'id' | 'timestamp'>) {
  return await db.auditLog.create({
    data: {
      ...entry,
      timestamp: new Date()
    }
  })
}

// Middleware for automatic audit logging
export function withAudit<T extends (...args: any[]) => Promise<any>>(
  operation: T,
  metadata: { tableName: string; action: AuditEntry['action'] }
): T {
  return (async (...args: any[]) => {
    const startTime = Date.now()
    const { tableName, action } = metadata

    try {
      // Capture before state for UPDATE/DELETE
      let oldValue
      if (action === 'UPDATE' || action === 'DELETE') {
        oldValue = await captureCurrentState(tableName, args[0])
      }

      // Execute operation
      const result = await operation(...args)

      // Capture after state
      const newValue = action !== 'DELETE' ? result : null

      // Log audit entry
      await createAuditLog({
        userId: getCurrentUser().id,
        action,
        tableName,
        recordId: args[0],
        oldValue,
        newValue,
        ipAddress: getClientIp(),
        userAgent: getClientUserAgent(),
        sessionId: getSessionId()
      })

      return result
    } catch (error) {
      // Log failed attempt
      await createAuditLog({
        userId: getCurrentUser().id,
        action,
        tableName,
        recordId: args[0],
        ipAddress: getClientIp(),
        userAgent: getClientUserAgent(),
        sessionId: getSessionId()
      })
      throw error
    }
  }) as T
}

// Usage
const updateUser = withAudit(
  async (userId: string, data: any) => {
    return await db.user.update({
      where: { id: userId },
      data
    })
  },
  { tableName: 'users', action: 'UPDATE' }
)
```

---

### Pattern 2: Anomaly Detection

**Use case:** Identify suspicious patterns in transaction data

```typescript
// lib/forensics/anomaly-detection.ts

interface Transaction {
  id: string
  userId: string
  amount: number
  timestamp: Date
  location: string
  deviceId: string
}

export async function detectTransactionAnomalies(transaction: Transaction) {
  const anomalies: string[] = []

  // Check 1: Unusual amount (statistical outlier)
  const userStats = await getUserTransactionStats(transaction.userId)
  const zScore = (transaction.amount - userStats.mean) / userStats.stdDev

  if (Math.abs(zScore) > 3) {
    anomalies.push(`Unusual amount: ${transaction.amount} (z-score: ${zScore.toFixed(2)})`)
  }

  // Check 2: Rapid succession (velocity check)
  const recentTransactions = await db.transactions.findMany({
    where: {
      userId: transaction.userId,
      timestamp: {
        gte: new Date(Date.now() - 5 * 60 * 1000) // Last 5 minutes
      }
    }
  })

  if (recentTransactions.length > 5) {
    anomalies.push(`High velocity: ${recentTransactions.length} transactions in 5 minutes`)
  }

  // Check 3: Impossible travel (location mismatch)
  const lastTransaction = await db.transactions.findFirst({
    where: { userId: transaction.userId },
    orderBy: { timestamp: 'desc' }
  })

  if (lastTransaction) {
    const timeDiff = transaction.timestamp.getTime() - lastTransaction.timestamp.getTime()
    const distance = calculateDistance(lastTransaction.location, transaction.location)
    const maxPossibleSpeed = 900 // km/h (commercial flight)
    const requiredSpeed = distance / (timeDiff / 3600000) // km/h

    if (requiredSpeed > maxPossibleSpeed) {
      anomalies.push(
        `Impossible travel: ${distance}km in ${timeDiff / 60000} minutes (${requiredSpeed.toFixed(0)} km/h required)`
      )
    }
  }

  // Check 4: New device from new location
  const deviceHistory = await db.deviceHistory.findFirst({
    where: {
      userId: transaction.userId,
      deviceId: transaction.deviceId
    }
  })

  if (!deviceHistory) {
    anomalies.push(`New device: ${transaction.deviceId}`)
  }

  // Check 5: Time-of-day anomaly
  const hour = transaction.timestamp.getHours()
  const userActivity = await getUserActivityPattern(transaction.userId)

  if (userActivity.typicalHours.indexOf(hour) === -1) {
    anomalies.push(`Unusual time: ${hour}:00 (typical: ${userActivity.typicalHours.join(', ')})`)
  }

  return {
    isAnomalous: anomalies.length > 0,
    anomalies,
    riskScore: calculateRiskScore(anomalies)
  }
}

async function getUserTransactionStats(userId: string) {
  const result = await db.$queryRaw<[{ mean: number; stddev: number }]>`
    SELECT
      AVG(amount)::float as mean,
      STDDEV(amount)::float as stddev
    FROM transactions
    WHERE user_id = ${userId}
    AND timestamp > NOW() - INTERVAL '90 days'
  `

  return {
    mean: result[0]?.mean || 0,
    stdDev: result[0]?.stddev || 1
  }
}

function calculateRiskScore(anomalies: string[]): number {
  // Weight different anomaly types
  const weights = {
    'Unusual amount': 2,
    'High velocity': 3,
    'Impossible travel': 5,
    'New device': 2,
    'Unusual time': 1
  }

  return anomalies.reduce((score, anomaly) => {
    const type = anomaly.split(':')[0]
    return score + (weights[type] || 1)
  }, 0)
}
```

---

### Pattern 3: Data Lineage Tracking

**Use case:** Track data provenance and transformation history

```typescript
// lib/forensics/lineage.ts

interface LineageNode {
  id: string
  datasetName: string
  recordId: string
  operation: string
  timestamp: Date
  sourceNodes: string[]
  metadata: Record<string, any>
}

export class DataLineageTracker {
  async trackTransformation(config: {
    output: { dataset: string; recordId: string }
    inputs: Array<{ dataset: string; recordId: string }>
    operation: string
    metadata?: Record<string, any>
  }) {
    const node: LineageNode = {
      id: generateId(),
      datasetName: config.output.dataset,
      recordId: config.output.recordId,
      operation: config.operation,
      timestamp: new Date(),
      sourceNodes: config.inputs.map(i => `${i.dataset}:${i.recordId}`),
      metadata: config.metadata || {}
    }

    await db.dataLineage.create({ data: node })
    return node
  }

  async getLineage(dataset: string, recordId: string): Promise<LineageNode[]> {
    const visited = new Set<string>()
    const lineage: LineageNode[] = []

    async function traverse(ds: string, rid: string) {
      const key = `${ds}:${rid}`
      if (visited.has(key)) return

      visited.add(key)

      const node = await db.dataLineage.findFirst({
        where: { datasetName: ds, recordId: rid }
      })

      if (!node) return

      lineage.push(node)

      // Recursively traverse source nodes
      for (const sourceKey of node.sourceNodes) {
        const [sourceDs, sourceRid] = sourceKey.split(':')
        await traverse(sourceDs, sourceRid)
      }
    }

    await traverse(dataset, recordId)
    return lineage
  }

  async visualizeLineage(dataset: string, recordId: string): Promise<string> {
    const lineage = await this.getLineage(dataset, recordId)

    // Generate Mermaid diagram
    let diagram = 'graph TD\n'

    for (const node of lineage) {
      const nodeId = `${node.datasetName}_${node.recordId}`
      diagram += `  ${nodeId}["${node.datasetName}:${node.recordId}<br/>${node.operation}"]\\n`

      for (const source of node.sourceNodes) {
        const [ds, rid] = source.split(':')
        const sourceId = `${ds}_${rid}`
        diagram += `  ${sourceId} --> ${nodeId}\n`
      }
    }

    return diagram
  }
}

// Usage example
const tracker = new DataLineageTracker()

// Track ETL transformation
await tracker.trackTransformation({
  output: { dataset: 'customers_enriched', recordId: 'c123' },
  inputs: [
    { dataset: 'customers_raw', recordId: 'c123' },
    { dataset: 'geolocation', recordId: 'geo456' }
  ],
  operation: 'enrichWithGeodata',
  metadata: {
    pipelineName: 'customer-enrichment',
    version: '1.0.0'
  }
})
```

---

### Pattern 4: Fraud Detection Patterns

**Use case:** Identify fraudulent activities using pattern matching

```typescript
// lib/forensics/fraud-detection.ts

interface FraudIndicator {
  type: string
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'
  description: string
  evidence: any
}

export async function detectFraud(userId: string): Promise<FraudIndicator[]> {
  const indicators: FraudIndicator[] = []

  // Pattern 1: Account takeover indicators
  const recentPasswordChanges = await db.auditLog.count({
    where: {
      userId,
      action: 'UPDATE',
      tableName: 'users',
      timestamp: { gte: new Date(Date.now() - 24 * 60 * 60 * 1000) }
    }
  })

  if (recentPasswordChanges > 3) {
    indicators.push({
      type: 'ACCOUNT_TAKEOVER',
      severity: 'HIGH',
      description: 'Multiple password changes in 24 hours',
      evidence: { count: recentPasswordChanges }
    })
  }

  // Pattern 2: Structuring (smurfing)
  const recentSmallTransactions = await db.transactions.findMany({
    where: {
      userId,
      amount: { lt: 9999 }, // Just under reporting threshold
      timestamp: { gte: new Date(Date.now() - 24 * 60 * 60 * 1000) }
    }
  })

  if (recentSmallTransactions.length > 5) {
    const total = recentSmallTransactions.reduce((sum, t) => sum + t.amount, 0)
    indicators.push({
      type: 'STRUCTURING',
      severity: 'CRITICAL',
      description: 'Multiple transactions just under reporting threshold',
      evidence: {
        count: recentSmallTransactions.length,
        total,
        averageAmount: total / recentSmallTransactions.length
      }
    })
  }

  // Pattern 3: Unusual beneficiary patterns
  const beneficiaries = await db.transactions.groupBy({
    by: ['beneficiaryId'],
    where: {
      userId,
      timestamp: { gte: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000) }
    },
    _count: true
  })

  const newBeneficiaries = beneficiaries.filter(async b => {
    const history = await db.transactions.count({
      where: {
        userId,
        beneficiaryId: b.beneficiaryId,
        timestamp: { lt: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) }
      }
    })
    return history === 0
  })

  if (newBeneficiaries.length > 3) {
    indicators.push({
      type: 'UNUSUAL_BENEFICIARIES',
      severity: 'MEDIUM',
      description: 'Multiple new beneficiaries in short period',
      evidence: { count: newBeneficiaries.length }
    })
  }

  // Pattern 4: Round-tripping
  const circularTransfers = await detectCircularTransfers(userId)
  if (circularTransfers.length > 0) {
    indicators.push({
      type: 'ROUND_TRIPPING',
      severity: 'CRITICAL',
      description: 'Circular money flow detected',
      evidence: { chains: circularTransfers }
    })
  }

  return indicators
}

async function detectCircularTransfers(userId: string): Promise<string[][]> {
  // Find chains where money flows back to original sender
  const result = await db.$queryRaw<Array<{path: string[]}}>`
    WITH RECURSIVE transfer_chain AS (
      SELECT
        sender_id,
        recipient_id,
        ARRAY[sender_id, recipient_id] as path,
        1 as depth
      FROM transfers
      WHERE sender_id = ${userId}
        AND timestamp > NOW() - INTERVAL '30 days'

      UNION ALL

      SELECT
        tc.sender_id,
        t.recipient_id,
        tc.path || t.recipient_id,
        tc.depth + 1
      FROM transfer_chain tc
      JOIN transfers t ON tc.recipient_id = t.sender_id
      WHERE tc.depth < 5
        AND NOT t.recipient_id = ANY(tc.path)
    )
    SELECT path
    FROM transfer_chain
    WHERE recipient_id = sender_id
  `

  return result.map(r => r.path)
}
```

---

### Pattern 5: Breach Investigation

**Use case:** Investigate and analyze data breaches

```typescript
// lib/forensics/breach-investigation.ts

interface BreachReport {
  id: string
  detectedAt: Date
  affectedRecords: number
  compromisedFields: string[]
  attackVector: string
  timeline: BreachEvent[]
  impactAssessment: ImpactAssessment
}

interface BreachEvent {
  timestamp: Date
  event: string
  details: any
}

export class BreachInvestigator {
  async investigateBreach(suspiciousActivity: {
    startTime: Date
    endTime: Date
    affectedTable: string
  }): Promise<BreachReport> {
    const timeline: BreachEvent[] = []

    // 1. Identify initial access
    const suspiciousLogins = await db.auditLog.findMany({
      where: {
        action: 'READ',
        tableName: 'users',
        timestamp: {
          gte: suspiciousActivity.startTime,
          lte: suspiciousActivity.endTime
        }
      },
      orderBy: { timestamp: 'asc' }
    })

    timeline.push({
      timestamp: suspiciousLogins[0]?.timestamp || suspiciousActivity.startTime,
      event: 'INITIAL_ACCESS',
      details: suspiciousLogins[0]
    })

    // 2. Identify privilege escalation
    const privilegeChanges = await db.auditLog.findMany({
      where: {
        action: 'UPDATE',
        tableName: 'users',
        timestamp: {
          gte: suspiciousActivity.startTime,
          lte: suspiciousActivity.endTime
        }
      }
    })

    for (const change of privilegeChanges) {
      if (change.newValue?.role !== change.oldValue?.role) {
        timeline.push({
          timestamp: change.timestamp,
          event: 'PRIVILEGE_ESCALATION',
          details: change
        })
      }
    }

    // 3. Identify data exfiltration
    const dataAccess = await db.auditLog.findMany({
      where: {
        tableName: suspiciousActivity.affectedTable,
        action: 'READ',
        timestamp: {
          gte: suspiciousActivity.startTime,
          lte: suspiciousActivity.endTime
        }
      }
    })

    const massExfiltration = this.detectMassExfiltration(dataAccess)
    if (massExfiltration) {
      timeline.push({
        timestamp: massExfiltration.startTime,
        event: 'DATA_EXFILTRATION',
        details: massExfiltration
      })
    }

    // 4. Identify affected records
    const affectedRecordIds = new Set(dataAccess.map(a => a.recordId))
    const affectedRecords = affectedRecordIds.size

    // 5. Determine compromised fields
    const compromisedFields = this.identifyCompromisedFields(dataAccess)

    // 6. Determine attack vector
    const attackVector = await this.determineAttackVector(timeline)

    // 7. Impact assessment
    const impactAssessment = await this.assessImpact({
      affectedRecords,
      compromisedFields,
      affectedTable: suspiciousActivity.affectedTable
    })

    return {
      id: generateId(),
      detectedAt: new Date(),
      affectedRecords,
      compromisedFields,
      attackVector,
      timeline,
      impactAssessment
    }
  }

  private detectMassExfiltration(accesses: any[]) {
    // Group by user and time window
    const byUser = groupBy(accesses, 'userId')

    for (const [userId, userAccesses] of Object.entries(byUser)) {
      const sorted = userAccesses.sort((a, b) => a.timestamp.getTime() - b.timestamp.getTime())

      // Check for rapid sequential access
      if (sorted.length > 100) {
        const duration =
          sorted[sorted.length - 1].timestamp.getTime() - sorted[0].timestamp.getTime()

        if (duration < 60000) {
          // Less than 1 minute
          return {
            userId,
            recordCount: sorted.length,
            startTime: sorted[0].timestamp,
            endTime: sorted[sorted.length - 1].timestamp,
            duration
          }
        }
      }
    }

    return null
  }

  private identifyCompromisedFields(accesses: any[]): string[] {
    const fields = new Set<string>()

    for (const access of accesses) {
      if (access.metadata?.fields) {
        access.metadata.fields.forEach(f => fields.add(f))
      }
    }

    return Array.from(fields)
  }

  private async determineAttackVector(timeline: BreachEvent[]): Promise<string> {
    // Analyze timeline to determine likely attack vector
    const events = timeline.map(e => e.event)

    if (events.includes('SQL_INJECTION')) {
      return 'SQL Injection'
    } else if (events.includes('PRIVILEGE_ESCALATION')) {
      return 'Privilege Escalation'
    } else if (events.includes('BRUTE_FORCE')) {
      return 'Brute Force Attack'
    } else {
      return 'Unknown - Requires Manual Investigation'
    }
  }

  private async assessImpact(config: {
    affectedRecords: number
    compromisedFields: string[]
    affectedTable: string
  }): Promise<ImpactAssessment> {
    const sensitiveFields = ['ssn', 'password', 'creditCard', 'email', 'phone']
    const hasSensitiveData = config.compromisedFields.some(f => sensitiveFields.includes(f))

    return {
      severity: hasSensitiveData ? 'CRITICAL' : 'HIGH',
      affectedUsers: config.affectedRecords,
      requiresNotification: true,
      regulatoryImplications: hasSensitiveData ? ['GDPR', 'CCPA', 'State Breach Laws'] : [],
      estimatedCost: this.estimateBreachCost(config.affectedRecords)
    }
  }

  private estimateBreachCost(recordCount: number): number {
    // Based on IBM Cost of Data Breach Report
    const costPerRecord = 150 // USD
    return recordCount * costPerRecord
  }
}

interface ImpactAssessment {
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'
  affectedUsers: number
  requiresNotification: boolean
  regulatoryImplications: string[]
  estimatedCost: number
}
```

---

### Pattern 6: Change Detection

**Use case:** Detect unauthorized database modifications

```typescript
// lib/forensics/change-detection.ts

export class ChangeDetector {
  async detectUnauthorizedChanges(tableName: string, timeWindow: number = 24) {
    const changes = await db.auditLog.findMany({
      where: {
        tableName,
        action: { in: ['UPDATE', 'DELETE'] },
        timestamp: {
          gte: new Date(Date.now() - timeWindow * 60 * 60 * 1000)
        }
      },
      include: {
        user: true
      }
    })

    const suspicious: any[] = []

    for (const change of changes) {
      // Check 1: Change outside business hours
      const hour = change.timestamp.getHours()
      if (hour < 6 || hour > 22) {
        suspicious.push({
          ...change,
          reason: 'OUTSIDE_BUSINESS_HOURS',
          severity: 'MEDIUM'
        })
      }

      // Check 2: Bulk operations
      const recentChanges = changes.filter(
        c =>
          c.userId === change.userId &&
          Math.abs(c.timestamp.getTime() - change.timestamp.getTime()) < 60000
      )

      if (recentChanges.length > 50) {
        suspicious.push({
          ...change,
          reason: 'BULK_OPERATION',
          severity: 'HIGH',
          affectedRecords: recentChanges.length
        })
      }

      // Check 3: Privilege mismatch
      if (change.user.role !== 'ADMIN' && tableName === 'users') {
        suspicious.push({
          ...change,
          reason: 'INSUFFICIENT_PRIVILEGES',
          severity: 'CRITICAL'
        })
      }

      // Check 4: Unusual modifications
      if (change.action === 'DELETE' && !change.metadata?.deletionReason) {
        suspicious.push({
          ...change,
          reason: 'UNDOCUMENTED_DELETION',
          severity: 'HIGH'
        })
      }
    }

    return suspicious
  }

  async generateChangeReport(startDate: Date, endDate: Date) {
    const changes = await db.auditLog.findMany({
      where: {
        timestamp: { gte: startDate, lte: endDate }
      }
    })

    // Group by table and action
    const summary = changes.reduce(
      (acc, change) => {
        const key = `${change.tableName}:${change.action}`
        acc[key] = (acc[key] || 0) + 1
        return acc
      },
      {} as Record<string, number>
    )

    // Group by user
    const byUser = changes.reduce(
      (acc, change) => {
        acc[change.userId] = (acc[change.userId] || 0) + 1
        return acc
      },
      {} as Record<string, number>
    )

    return {
      totalChanges: changes.length,
      byTableAndAction: summary,
      byUser,
      timeRange: { start: startDate, end: endDate }
    }
  }
}
```

---

### Pattern 7: Forensic Recovery

**Use case:** Recover deleted or modified data

```typescript
// lib/forensics/recovery.ts

export class ForensicRecovery {
  async recoverDeletedRecord(tableName: string, recordId: string) {
    // Find deletion event
    const deletion = await db.auditLog.findFirst({
      where: {
        tableName,
        recordId,
        action: 'DELETE'
      },
      orderBy: { timestamp: 'desc' }
    })

    if (!deletion || !deletion.oldValue) {
      throw new Error('No recovery data available')
    }

    // Verify record is still deleted
    const exists = await db[tableName].findUnique({
      where: { id: recordId }
    })

    if (exists) {
      throw new Error('Record already exists')
    }

    // Restore from audit log
    const restored = await db[tableName].create({
      data: {
        ...deletion.oldValue,
        restoredAt: new Date(),
        restoredBy: getCurrentUser().id,
        restoredFrom: deletion.id
      }
    })

    // Log recovery
    await createAuditLog({
      userId: getCurrentUser().id,
      action: 'CREATE',
      tableName,
      recordId,
      newValue: restored,
      metadata: {
        recovery: true,
        originalDeletionId: deletion.id
      }
    })

    return restored
  }

  async reconstructHistory(tableName: string, recordId: string) {
    const history = await db.auditLog.findMany({
      where: { tableName, recordId },
      orderBy: { timestamp: 'asc' }
    })

    const timeline = []
    let currentState = null

    for (const event of history) {
      switch (event.action) {
        case 'CREATE':
          currentState = event.newValue
          break
        case 'UPDATE':
          currentState = { ...currentState, ...event.newValue }
          break
        case 'DELETE':
          currentState = null
          break
      }

      timeline.push({
        timestamp: event.timestamp,
        action: event.action,
        changes:
          event.action === 'UPDATE' ? this.diffObjects(event.oldValue, event.newValue) : null,
        state: structuredClone(currentState)
      })
    }

    return timeline
  }

  private diffObjects(old: any, new_: any): any {
    const changes = {}

    for (const key of Object.keys(new_)) {
      if (JSON.stringify(old[key]) !== JSON.stringify(new_[key])) {
        changes[key] = { old: old[key], new: new_[key] }
      }
    }

    return changes
  }

  async rollbackToTimestamp(tableName: string, recordId: string, timestamp: Date) {
    const timeline = await this.reconstructHistory(tableName, recordId)

    // Find state at target timestamp
    const targetState = timeline.filter(t => t.timestamp <= timestamp).pop()?.state

    if (!targetState) {
      throw new Error('No state found at target timestamp')
    }

    // Update to target state
    await db[tableName].update({
      where: { id: recordId },
      data: {
        ...targetState,
        rolledBackAt: new Date(),
        rolledBackBy: getCurrentUser().id,
        rolledBackTo: timestamp
      }
    })

    return targetState
  }
}
```

---

## Compliance Patterns

### Pattern 8: GDPR Compliance Tools

```typescript
// lib/forensics/gdpr-compliance.ts

export class GDPRCompliance {
  async generateDataPortabilityReport(userId: string) {
    // Collect all user data across tables
    const userData = {
      personal: await db.users.findUnique({ where: { id: userId } }),
      orders: await db.orders.findMany({ where: { userId } }),
      preferences: await db.userPreferences.findFirst({ where: { userId } }),
      activityLog: await db.activityLog.findMany({
        where: { userId },
        orderBy: { timestamp: 'desc' },
        take: 1000
      })
    }

    return {
      exportDate: new Date(),
      userId,
      data: userData,
      format: 'JSON',
      rightExercised: 'DATA_PORTABILITY'
    }
  }

  async rightToBeForgotten(userId: string) {
    // Log request
    await db.gdprRequests.create({
      data: {
        userId,
        requestType: 'ERASURE',
        requestedAt: new Date(),
        status: 'PROCESSING'
      }
    })

    // Anonymize instead of delete for audit compliance
    await db.users.update({
      where: { id: userId },
      data: {
        email: `deleted-${userId}@example.com`,
        name: 'Deleted User',
        phone: null,
        address: null,
        deletedAt: new Date()
      }
    })

    // Remove from third-party services
    await this.removeFromThirdParties(userId)

    // Update request status
    await db.gdprRequests.update({
      where: { userId },
      data: {
        status: 'COMPLETED',
        completedAt: new Date()
      }
    })
  }

  async generateProcessingRegister() {
    // GDPR Article 30 - Record of Processing Activities
    return {
      controller: {
        name: 'Your Company Ltd',
        contact: 'dpo@company.com',
        representative: 'Data Protection Officer'
      },
      purposes: [
        'Service delivery',
        'Customer support',
        'Marketing (with consent)',
        'Legal compliance'
      ],
      dataCategories: ['Identity data', 'Contact data', 'Financial data', 'Usage data'],
      recipients: ['Payment processors', 'Email service providers', 'Analytics providers'],
      retentionPeriods: {
        activeUsers: '5 years after last activity',
        deletedUsers: '1 year (anonymized)',
        transactions: '7 years (legal requirement)'
      },
      securityMeasures: [
        'Encryption at rest and in transit',
        'Access control with MFA',
        'Regular security audits',
        'Audit logging'
      ]
    }
  }
}
```

---

## Monitoring and Alerting

### Pattern 9: Real-Time Threat Detection

```typescript
// lib/forensics/threat-detection.ts

export class ThreatDetector {
  async monitorForThreats() {
    // Set up real-time monitoring
    const threats = []

    // Monitor 1: SQL Injection attempts
    const sqlInjectionPatterns = [
      /['";].*(--)|(;).*--/,
      /\bUNION\b.*\bSELECT\b/i,
      /\bOR\b.*['"].*=.*['"]/i
    ]

    const recentQueries = await this.getRecentQueries()
    for (const query of recentQueries) {
      if (sqlInjectionPatterns.some(p => p.test(query.sql))) {
        threats.push({
          type: 'SQL_INJECTION',
          severity: 'CRITICAL',
          query: query.sql,
          userId: query.userId,
          timestamp: query.timestamp
        })
      }
    }

    // Monitor 2: Brute force attempts
    const loginAttempts = await db.loginAttempts.groupBy({
      by: ['ipAddress'],
      where: {
        success: false,
        timestamp: { gte: new Date(Date.now() - 5 * 60 * 1000) }
      },
      _count: true
    })

    for (const attempt of loginAttempts) {
      if (attempt._count > 10) {
        threats.push({
          type: 'BRUTE_FORCE',
          severity: 'HIGH',
          ipAddress: attempt.ipAddress,
          attempts: attempt._count
        })
      }
    }

    // Monitor 3: Privilege escalation
    const privilegeChanges = await db.auditLog.findMany({
      where: {
        tableName: 'users',
        action: 'UPDATE',
        timestamp: { gte: new Date(Date.now() - 60 * 60 * 1000) }
      }
    })

    for (const change of privilegeChanges) {
      if (change.newValue?.role === 'ADMIN' && change.oldValue?.role !== 'ADMIN') {
        threats.push({
          type: 'PRIVILEGE_ESCALATION',
          severity: 'CRITICAL',
          userId: change.userId,
          targetUserId: change.recordId,
          timestamp: change.timestamp
        })
      }
    }

    // Alert on critical threats
    const criticalThreats = threats.filter(t => t.severity === 'CRITICAL')
    if (criticalThreats.length > 0) {
      await this.alertSecurityTeam(criticalThreats)
    }

    return threats
  }

  private async alertSecurityTeam(threats: any[]) {
    // Send alerts via multiple channels
    await Promise.all([
      this.sendSlackAlert(threats),
      this.sendEmailAlert(threats),
      this.createPagerDutyIncident(threats)
    ])
  }
}
```

---

## When to Use Me

**Perfect for:**

- Security incident investigation
- Fraud detection and prevention
- Compliance auditing (GDPR, SOC2, HIPAA)
- Data breach response
- Forensic analysis of suspicious activity
- Data integrity verification

**I'll help you:**

- Build audit trail systems
- Detect anomalies and fraud
- Track data lineage
- Investigate breaches
- Ensure regulatory compliance
- Recover compromised data

## What I'll Create

```
🔍 Audit Trail Systems
🚨 Anomaly Detection Engines
🔐 Fraud Detection Pipelines
📊 Data Lineage Tracking
🛡️ Breach Investigation Tools
⚖️ Compliance Reporting
🔄 Forensic Recovery Systems
```

Let's build secure, auditable, and compliant data systems!

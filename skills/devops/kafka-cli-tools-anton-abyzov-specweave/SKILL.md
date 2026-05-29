---
name: kafka-cli-tools
description: Kafka CLI tools expert for kcat, kafkactl, and native Kafka commands. Use when producing/consuming messages from command line, listing topics, or troubleshooting Kafka with CLI tools.
---

# Kafka CLI Tools Expert

Comprehensive knowledge of modern Kafka CLI tools for production operations, development, and troubleshooting.

## Supported CLI Tools

### 1. kcat (kafkacat) - The Swiss Army Knife

**Installation**:
```bash
# macOS
brew install kcat

# Ubuntu/Debian
apt-get install kafkacat

# From source
git clone https://github.com/edenhill/kcat.git
cd kcat
./configure && make && sudo make install
```

**Core Operations**:

**Produce Messages**:
```bash
# Simple produce
echo "Hello Kafka" | kcat -P -b localhost:9092 -t my-topic

# Produce with key (key:value format)
echo "user123:Login event" | kcat -P -b localhost:9092 -t events -K:

# Produce from file
cat events.json | kcat -P -b localhost:9092 -t events

# Produce with headers
echo "msg" | kcat -P -b localhost:9092 -t my-topic -H "source=app1" -H "version=1.0"

# Produce with compression
echo "data" | kcat -P -b localhost:9092 -t my-topic -z gzip

# Produce with acks=all
echo "critical-data" | kcat -P -b localhost:9092 -t my-topic -X acks=all
```

**Consume Messages**:
```bash
# Consume from beginning
kcat -C -b localhost:9092 -t my-topic -o beginning

# Consume from end (latest)
kcat -C -b localhost:9092 -t my-topic -o end

# Consume specific partition
kcat -C -b localhost:9092 -t my-topic -p 0 -o beginning

# Consume with consumer group
kcat -C -b localhost:9092 -G my-group my-topic

# Consume N messages and exit
kcat -C -b localhost:9092 -t my-topic -c 10

# Custom format (topic:partition:offset:key:value)
kcat -C -b localhost:9092 -t my-topic -f 'Topic: %t, Partition: %p, Offset: %o, Key: %k, Value: %s\n'

# JSON output
kcat -C -b localhost:9092 -t my-topic -J
```

**Metadata & Admin**:
```bash
# List all topics
kcat -L -b localhost:9092

# Get topic metadata (JSON)
kcat -L -b localhost:9092 -t my-topic -J

# Query topic offsets
kcat -Q -b localhost:9092 -t my-topic

# Check broker health
kcat -L -b localhost:9092 | grep "broker\|topic"
```

**SASL/SSL Authentication**:
```bash
# SASL/PLAINTEXT
kcat -b localhost:9092 \
  -X security.protocol=SASL_PLAINTEXT \
  -X sasl.mechanism=PLAIN \
  -X sasl.username=admin \
  -X sasl.password=admin-secret \
  -L

# SASL/SSL
kcat -b localhost:9093 \
  -X security.protocol=SASL_SSL \
  -X sasl.mechanism=SCRAM-SHA-256 \
  -X sasl.username=admin \
  -X sasl.password=admin-secret \
  -X ssl.ca.location=/path/to/ca-cert \
  -L

# mTLS (mutual TLS)
kcat -b localhost:9093 \
  -X security.protocol=SSL \
  -X ssl.ca.location=/path/to/ca-cert \
  -X ssl.certificate.location=/path/to/client-cert.pem \
  -X ssl.key.location=/path/to/client-key.pem \
  -L
```

### 2. kcli - Kubernetes-Native Kafka CLI

**Installation**:
```bash
# Install via krew (Kubernetes plugin manager)
kubectl krew install kcli

# Or download binary
curl -LO https://github.com/cswank/kcli/releases/latest/download/kcli-linux-amd64
chmod +x kcli-linux-amd64
sudo mv kcli-linux-amd64 /usr/local/bin/kcli
```

**Kubernetes Integration**:
```bash
# Connect to Kafka running in k8s
kcli --context my-cluster --namespace kafka

# Produce to topic in k8s
echo "msg" | kcli produce --topic my-topic --brokers kafka-broker:9092

# Consume from k8s Kafka
kcli consume --topic my-topic --brokers kafka-broker:9092 --from-beginning

# List topics in k8s cluster
kcli topics list --brokers kafka-broker:9092
```

**Best For**:
- Kubernetes-native deployments
- Helmfile/Kustomize workflows
- GitOps with ArgoCD/Flux

### 3. kaf - Modern Terminal UI

**Installation**:
```bash
# macOS
brew install kaf

# Linux (via snap)
snap install kaf

# From source
go install github.com/birdayz/kaf/cmd/kaf@latest
```

**Interactive Features**:
```bash
# Configure cluster
kaf config add-cluster local --brokers localhost:9092

# Use cluster
kaf config use-cluster local

# Interactive topic browsing (TUI)
kaf topics

# Interactive consume (arrow keys to navigate)
kaf consume my-topic

# Produce interactively
kaf produce my-topic

# Consumer group management
kaf groups
kaf group describe my-group
kaf group reset my-group --topic my-topic --offset earliest

# Schema Registry integration
kaf schemas
kaf schema get my-schema
```

**Best For**:
- Development workflows
- Quick topic exploration
- Consumer group debugging
- Schema Registry management

### 4. kafkactl - Advanced Admin Tool

**Installation**:
```bash
# macOS
brew install deviceinsight/packages/kafkactl

# Linux
curl -L https://github.com/deviceinsight/kafkactl/releases/latest/download/kafkactl_linux_amd64 -o kafkactl
chmod +x kafkactl
sudo mv kafkactl /usr/local/bin/

# Via Docker
docker run --rm -it deviceinsight/kafkactl:latest
```

**Advanced Operations**:
```bash
# Configure context
kafkactl config add-context local --brokers localhost:9092

# Topic management
kafkactl create topic my-topic --partitions 3 --replication-factor 2
kafkactl alter topic my-topic --config retention.ms=86400000
kafkactl delete topic my-topic

# Consumer group operations
kafkactl describe consumer-group my-group
kafkactl reset consumer-group my-group --topic my-topic --offset earliest
kafkactl delete consumer-group my-group

# ACL management
kafkactl create acl --allow --principal User:alice --operation READ --topic my-topic
kafkactl list acls

# Quota management
kafkactl alter client-quota --user alice --producer-byte-rate 1048576

# Reassign partitions
kafkactl alter partition --topic my-topic --partition 0 --replicas 1,2,3
```

**Best For**:
- Production cluster management
- ACL administration
- Partition reassignment
- Quota management

## Tool Comparison Matrix

| Feature | kcat | kcli | kaf | kafkactl |
|---------|------|------|-----|----------|
| **Installation** | Easy | Medium | Easy | Easy |
| **Produce** | ✅ Advanced | ✅ Basic | ✅ Interactive | ✅ Basic |
| **Consume** | ✅ Advanced | ✅ Basic | ✅ Interactive | ✅ Basic |
| **Metadata** | ✅ JSON | ✅ Basic | ✅ TUI | ✅ Detailed |
| **TUI** | ❌ | ❌ | ✅ | ✅ Limited |
| **Admin** | ❌ | ❌ | ⚠️  Limited | ✅ Advanced |
| **SASL/SSL** | ✅ | ✅ | ✅ | ✅ |
| **K8s Native** | ❌ | ✅ | ❌ | ❌ |
| **Schema Reg** | ❌ | ❌ | ✅ | ❌ |
| **ACLs** | ❌ | ❌ | ❌ | ✅ |
| **Quotas** | ❌ | ❌ | ❌ | ✅ |
| **Best For** | Scripting, ops | Kubernetes | Development | Production admin |

## Common Patterns

### 1. Topic Creation with Optimal Settings

```bash
# Using kafkactl (recommended for production)
kafkactl create topic orders \
  --partitions 12 \
  --replication-factor 3 \
  --config retention.ms=604800000 \
  --config compression.type=lz4 \
  --config min.insync.replicas=2

# Verify with kcat
kcat -L -b localhost:9092 -t orders -J | jq '.topics[0]'
```

### 2. Dead Letter Queue Pattern

```bash
# Produce failed message to DLQ
echo "failed-msg" | kcat -P -b localhost:9092 -t orders-dlq \
  -H "original-topic=orders" \
  -H "error=DeserializationException" \
  -H "timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Monitor DLQ
kcat -C -b localhost:9092 -t orders-dlq -f 'Headers: %h\nValue: %s\n\n'
```

### 3. Consumer Group Lag Monitoring

```bash
# Using kafkactl
kafkactl describe consumer-group my-app | grep LAG

# Using kcat (via external tool like kcat-lag)
kcat -L -b localhost:9092 -J | jq '.topics[].partitions[] | select(.topic=="my-topic")'

# Using kaf (interactive)
kaf groups
# Then select group to see lag in TUI
```

### 4. Multi-Cluster Replication Testing

```bash
# Produce to source cluster
echo "test" | kcat -P -b source-kafka:9092 -t replicated-topic

# Consume from target cluster
kcat -C -b target-kafka:9092 -t replicated-topic -o end -c 1

# Compare offsets
kcat -Q -b source-kafka:9092 -t replicated-topic
kcat -Q -b target-kafka:9092 -t replicated-topic
```

### 5. Performance Testing

```bash
# Produce 10,000 messages with kcat
seq 1 10000 | kcat -P -b localhost:9092 -t perf-test

# Consume and measure throughput
time kcat -C -b localhost:9092 -t perf-test -c 10000 -o beginning > /dev/null

# Test with compression
seq 1 10000 | kcat -P -b localhost:9092 -t perf-test -z lz4
```

## Troubleshooting

### Connection Issues

```bash
# Test broker connectivity
kcat -L -b localhost:9092

# Check SSL/TLS connection
openssl s_client -connect localhost:9093 -showcerts

# Verify SASL authentication
kcat -b localhost:9092 \
  -X security.protocol=SASL_PLAINTEXT \
  -X sasl.mechanism=PLAIN \
  -X sasl.username=admin \
  -X sasl.password=wrong-password \
  -L
# Should fail with authentication error
```

### Message Not Appearing

```bash
# Check topic exists
kcat -L -b localhost:9092 | grep my-topic

# Check partition count
kcat -L -b localhost:9092 -t my-topic -J | jq '.topics[0].partition_count'

# Query all partition offsets
kcat -Q -b localhost:9092 -t my-topic

# Consume from all partitions
for i in {0..11}; do
  echo "Partition $i:"
  kcat -C -b localhost:9092 -t my-topic -p $i -c 1 -o end
done
```

### Consumer Group Stuck

```bash
# Check consumer group state
kafkactl describe consumer-group my-app

# Reset to beginning
kafkactl reset consumer-group my-app --topic my-topic --offset earliest

# Reset to specific offset
kafkactl reset consumer-group my-app --topic my-topic --partition 0 --offset 12345

# Delete consumer group (all consumers must be stopped first)
kafkactl delete consumer-group my-app
```

## Integration with SpecWeave

**Automatic CLI Tool Detection**:
SpecWeave auto-detects installed CLI tools and recommends best tool for the operation:

```typescript
import { CLIToolDetector } from './lib/cli/detector';

const detector = new CLIToolDetector();
const available = await detector.detectAll();

// Recommended tool for produce operation
if (available.includes('kcat')) {
  console.log('Use kcat for produce (fastest)');
} else if (available.includes('kaf')) {
  console.log('Use kaf for produce (interactive)');
}
```

**SpecWeave Commands**:
- `/sw-kafka:dev-env` - Uses Docker Compose + kcat for local testing
- `/sw-kafka:monitor-setup` - Sets up kcat-based lag monitoring
- `/sw-kafka:mcp-configure` - Validates CLI tools are installed

## Security Best Practices

1. **Never hardcode credentials** - Use environment variables or secrets management
2. **Use SSL/TLS in production** - Configure `-X security.protocol=SASL_SSL`
3. **Prefer SCRAM over PLAIN** - Use `-X sasl.mechanism=SCRAM-SHA-256`
4. **Rotate credentials regularly** - Update passwords and certificates
5. **Least privilege** - Grant only necessary ACLs to users

## Related Skills

- `/sw-kafka:kafka-mcp-integration` - MCP server setup and configuration
- `/sw-kafka:kafka-architecture` - Cluster design and sizing

## External Links

- [kcat GitHub](https://github.com/edenhill/kcat)
- [kcli GitHub](https://github.com/cswank/kcli)
- [kaf GitHub](https://github.com/birdayz/kaf)
- [kafkactl GitHub](https://github.com/deviceinsight/kafkactl)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)

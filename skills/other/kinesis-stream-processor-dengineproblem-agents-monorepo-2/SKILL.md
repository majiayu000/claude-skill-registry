---
name: kinesis-stream-processor
description: Эксперт AWS Kinesis. Используй для stream processing, real-time data и Kinesis patterns.
---

# AWS Kinesis Stream Processor

Expert in building real-time data streaming applications with AWS Kinesis.

## Core Concepts

### Kinesis Components

| Component | Purpose | Use Case |
|-----------|---------|----------|
| Data Streams | Real-time data ingestion | Custom processing, low latency |
| Data Firehose | Delivery to destinations | S3, Redshift, Elasticsearch |
| Data Analytics | SQL-based processing | Real-time analytics |
| Video Streams | Video streaming | IoT, media processing |

### Key Limits

```yaml
Kinesis Data Streams:
  per_shard:
    write: "1,000 records/sec OR 1 MB/sec"
    read: "5 transactions/sec, up to 10,000 records"
    read_throughput: "2 MB/sec"

  per_stream:
    max_shards: "500 (soft limit)"
    retention: "24 hours (default) to 365 days"

  per_record:
    max_size: "1 MB"
    partition_key: "256 bytes max"
```

## Producer Implementation

### Python Producer with Batching

```python
import boto3
import json
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any

class KinesisProducer:
    """Optimized Kinesis producer with batching and error handling."""

    def __init__(self, stream_name: str, region: str = 'us-east-1'):
        self.stream_name = stream_name
        self.client = boto3.client('kinesis', region_name=region)
        self.buffer: List[Dict] = []
        self.buffer_size = 500  # Max records per batch
        self.buffer_time = 0.1  # Flush every 100ms
        self.last_flush = time.time()

    def put_record(self, data: Dict[str, Any], partition_key: str) -> None:
        """Add record to buffer, flush if needed."""
        self.buffer.append({
            'Data': json.dumps(data).encode('utf-8'),
            'PartitionKey': partition_key
        })

        if len(self.buffer) >= self.buffer_size:
            self.flush()
        elif time.time() - self.last_flush > self.buffer_time:
            self.flush()

    def flush(self) -> None:
        """Send buffered records to Kinesis."""
        if not self.buffer:
            return

        records = self.buffer[:500]  # PutRecords limit
        self.buffer = self.buffer[500:]

        try:
            response = self.client.put_records(
                StreamName=self.stream_name,
                Records=records
            )

            # Handle partial failures
            failed_count = response.get('FailedRecordCount', 0)
            if failed_count > 0:
                self._handle_failures(response, records)

        except Exception as e:
            print(f"Kinesis put_records error: {e}")
            # Implement retry logic or dead letter queue
            raise

        self.last_flush = time.time()

    def _handle_failures(self, response: Dict, records: List[Dict]) -> None:
        """Retry failed records with exponential backoff."""
        failed_records = []

        for i, record_response in enumerate(response['Records']):
            if 'ErrorCode' in record_response:
                failed_records.append(records[i])
                print(f"Failed record: {record_response['ErrorCode']} - {record_response.get('ErrorMessage')}")

        # Retry failed records
        if failed_records:
            time.sleep(0.1)  # Brief backoff
            self.client.put_records(
                StreamName=self.stream_name,
                Records=failed_records
            )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()
```

### Node.js Producer

```javascript
const { KinesisClient, PutRecordsCommand } = require('@aws-sdk/client-kinesis');

class KinesisProducer {
  constructor(streamName, region = 'us-east-1') {
    this.streamName = streamName;
    this.client = new KinesisClient({ region });
    this.buffer = [];
    this.bufferSize = 500;
    this.flushInterval = 100; // ms

    // Auto-flush timer
    setInterval(() => this.flush(), this.flushInterval);
  }

  async putRecord(data, partitionKey) {
    this.buffer.push({
      Data: Buffer.from(JSON.stringify(data)),
      PartitionKey: partitionKey
    });

    if (this.buffer.length >= this.bufferSize) {
      await this.flush();
    }
  }

  async flush() {
    if (this.buffer.length === 0) return;

    const records = this.buffer.splice(0, 500);

    try {
      const command = new PutRecordsCommand({
        StreamName: this.streamName,
        Records: records
      });

      const response = await this.client.send(command);

      if (response.FailedRecordCount > 0) {
        await this.handleFailures(response, records);
      }
    } catch (error) {
      console.error('Kinesis error:', error);
      throw error;
    }
  }

  async handleFailures(response, records) {
    const failedRecords = response.Records
      .map((r, i) => r.ErrorCode ? records[i] : null)
      .filter(Boolean);

    if (failedRecords.length > 0) {
      // Exponential backoff retry
      await new Promise(resolve => setTimeout(resolve, 100));

      const command = new PutRecordsCommand({
        StreamName: this.streamName,
        Records: failedRecords
      });

      await this.client.send(command);
    }
  }
}
```

## Consumer Patterns

### Lambda Consumer

```python
import json
import base64
from typing import Dict, Any, List

def lambda_handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    """Process Kinesis records from Lambda trigger."""

    processed_records = []
    failed_records = []

    for record in event['Records']:
        try:
            # Decode Kinesis record
            payload = base64.b64decode(record['kinesis']['data'])
            data = json.loads(payload)

            # Process record
            result = process_record(data)
            processed_records.append({
                'sequenceNumber': record['kinesis']['sequenceNumber'],
                'result': result
            })

        except Exception as e:
            print(f"Error processing record: {e}")
            failed_records.append({
                'sequenceNumber': record['kinesis']['sequenceNumber'],
                'error': str(e)
            })

    # Report results
    print(f"Processed: {len(processed_records)}, Failed: {len(failed_records)}")

    # Return batch item failures for partial batch response
    return {
        'batchItemFailures': [
            {'itemIdentifier': r['sequenceNumber']}
            for r in failed_records
        ]
    }

def process_record(data: Dict) -> Dict:
    """Business logic for processing each record."""
    # Transform data
    transformed = {
        'id': data.get('id'),
        'timestamp': data.get('timestamp'),
        'processed_at': datetime.utcnow().isoformat(),
        'value': data.get('value', 0) * 2  # Example transformation
    }

    # Write to downstream (DynamoDB, S3, etc.)
    write_to_downstream(transformed)

    return transformed
```

### KCL Consumer (Java-style with Python)

```python
import boto3
import time
from datetime import datetime

class KinesisConsumer:
    """KCL-style consumer with checkpointing."""

    def __init__(self, stream_name: str, region: str = 'us-east-1'):
        self.stream_name = stream_name
        self.client = boto3.client('kinesis', region_name=region)
        self.checkpoint_interval = 60  # seconds
        self.last_checkpoint = time.time()

    def process_shard(self, shard_id: str) -> None:
        """Process records from a single shard."""

        # Get shard iterator
        iterator_response = self.client.get_shard_iterator(
            StreamName=self.stream_name,
            ShardId=shard_id,
            ShardIteratorType='LATEST'  # or 'TRIM_HORIZON', 'AT_SEQUENCE_NUMBER'
        )
        shard_iterator = iterator_response['ShardIterator']

        while True:
            try:
                response = self.client.get_records(
                    ShardIterator=shard_iterator,
                    Limit=100
                )

                for record in response['Records']:
                    self.process_record(record)

                # Checkpoint periodically
                if time.time() - self.last_checkpoint > self.checkpoint_interval:
                    self.checkpoint(shard_id, response['Records'][-1]['SequenceNumber'])

                # Get next iterator
                shard_iterator = response.get('NextShardIterator')
                if not shard_iterator:
                    break

                # Respect rate limits
                if len(response['Records']) == 0:
                    time.sleep(0.5)

            except Exception as e:
                print(f"Error processing shard {shard_id}: {e}")
                time.sleep(1)

    def process_record(self, record: Dict) -> None:
        """Process individual record."""
        data = json.loads(record['Data'])
        # Business logic here
        print(f"Processing: {data}")

    def checkpoint(self, shard_id: str, sequence_number: str) -> None:
        """Save checkpoint for recovery."""
        # Store in DynamoDB or other persistent store
        print(f"Checkpoint: shard={shard_id}, seq={sequence_number}")
        self.last_checkpoint = time.time()
```

### Enhanced Fan-Out Consumer

```python
import boto3
import json

def setup_enhanced_fanout(stream_arn: str, consumer_name: str) -> str:
    """Register enhanced fan-out consumer for dedicated throughput."""

    client = boto3.client('kinesis')

    # Register consumer
    response = client.register_stream_consumer(
        StreamARN=stream_arn,
        ConsumerName=consumer_name
    )

    consumer_arn = response['Consumer']['ConsumerARN']

    # Wait for consumer to become active
    waiter = client.get_waiter('stream_consumer_active')
    waiter.wait(
        StreamARN=stream_arn,
        ConsumerName=consumer_name
    )

    return consumer_arn

def subscribe_to_shard(consumer_arn: str, shard_id: str):
    """Subscribe to shard with enhanced fan-out."""

    client = boto3.client('kinesis')

    response = client.subscribe_to_shard(
        ConsumerARN=consumer_arn,
        ShardId=shard_id,
        StartingPosition={
            'Type': 'LATEST'
        }
    )

    # Process events from subscription
    for event in response['EventStream']:
        if 'SubscribeToShardEvent' in event:
            records = event['SubscribeToShardEvent']['Records']
            for record in records:
                process_record(record)
```

## Infrastructure as Code

### CloudFormation

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Kinesis Data Stream with Lambda Consumer

Parameters:
  StreamName:
    Type: String
    Default: my-data-stream
  ShardCount:
    Type: Number
    Default: 2
  RetentionPeriod:
    Type: Number
    Default: 24

Resources:
  KinesisStream:
    Type: AWS::Kinesis::Stream
    Properties:
      Name: !Ref StreamName
      ShardCount: !Ref ShardCount
      RetentionPeriodHours: !Ref RetentionPeriod
      StreamEncryption:
        EncryptionType: KMS
        KeyId: alias/aws/kinesis
      Tags:
        - Key: Environment
          Value: production

  ProcessorFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: kinesis-processor
      Runtime: python3.11
      Handler: index.lambda_handler
      MemorySize: 256
      Timeout: 60
      Role: !GetAtt ProcessorRole.Arn
      Code:
        ZipFile: |
          import json
          import base64

          def lambda_handler(event, context):
              for record in event['Records']:
                  payload = base64.b64decode(record['kinesis']['data'])
                  print(f"Processed: {payload}")
              return {'statusCode': 200}

  EventSourceMapping:
    Type: AWS::Lambda::EventSourceMapping
    Properties:
      EventSourceArn: !GetAtt KinesisStream.Arn
      FunctionName: !Ref ProcessorFunction
      StartingPosition: LATEST
      BatchSize: 100
      MaximumBatchingWindowInSeconds: 5
      MaximumRetryAttempts: 3
      BisectBatchOnFunctionError: true
      ParallelizationFactor: 1

  ProcessorRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaKinesisExecutionRole
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

  # CloudWatch Alarms
  IteratorAgeAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: kinesis-iterator-age
      MetricName: GetRecords.IteratorAgeMilliseconds
      Namespace: AWS/Kinesis
      Dimensions:
        - Name: StreamName
          Value: !Ref StreamName
      Statistic: Maximum
      Period: 60
      EvaluationPeriods: 5
      Threshold: 60000  # 1 minute
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - !Ref AlertTopic

  AlertTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: kinesis-alerts

Outputs:
  StreamArn:
    Value: !GetAtt KinesisStream.Arn
  StreamName:
    Value: !Ref KinesisStream
```

### Terraform

```hcl
resource "aws_kinesis_stream" "main" {
  name             = var.stream_name
  shard_count      = var.shard_count
  retention_period = var.retention_hours

  encryption_type = "KMS"
  kms_key_id      = "alias/aws/kinesis"

  shard_level_metrics = [
    "IncomingBytes",
    "IncomingRecords",
    "OutgoingBytes",
    "OutgoingRecords",
    "WriteProvisionedThroughputExceeded",
    "ReadProvisionedThroughputExceeded",
    "IteratorAgeMilliseconds"
  ]

  tags = {
    Environment = var.environment
  }
}

resource "aws_lambda_event_source_mapping" "kinesis" {
  event_source_arn                   = aws_kinesis_stream.main.arn
  function_name                      = aws_lambda_function.processor.arn
  starting_position                  = "LATEST"
  batch_size                         = 100
  maximum_batching_window_in_seconds = 5
  maximum_retry_attempts             = 3
  bisect_batch_on_function_error     = true
  parallelization_factor             = 1
}
```

## Monitoring and Alerting

### Key CloudWatch Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `IncomingRecords` | Records put per second | Monitor for traffic patterns |
| `IncomingBytes` | Bytes put per second | 80% of shard limit |
| `WriteProvisionedThroughputExceeded` | Throttled writes | >0 |
| `ReadProvisionedThroughputExceeded` | Throttled reads | >0 |
| `GetRecords.IteratorAgeMilliseconds` | Consumer lag | >60000ms |
| `GetRecords.Success` | Successful GetRecords | Monitor for drops |

### Monitoring Dashboard

```python
import boto3

def get_stream_metrics(stream_name: str, period_minutes: int = 5):
    """Get key Kinesis metrics for monitoring."""

    cloudwatch = boto3.client('cloudwatch')

    metrics = [
        'IncomingRecords',
        'IncomingBytes',
        'WriteProvisionedThroughputExceeded',
        'GetRecords.IteratorAgeMilliseconds'
    ]

    results = {}
    for metric in metrics:
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/Kinesis',
            MetricName=metric,
            Dimensions=[{'Name': 'StreamName', 'Value': stream_name}],
            StartTime=datetime.utcnow() - timedelta(minutes=period_minutes),
            EndTime=datetime.utcnow(),
            Period=60,
            Statistics=['Sum', 'Average', 'Maximum']
        )
        results[metric] = response['Datapoints']

    return results
```

## Лучшие практики

1. **Partition key design** — распределяйте данные равномерно по шардам
2. **Batch writes** — используйте PutRecords вместо PutRecord
3. **Handle throttling** — реализуйте exponential backoff
4. **Monitor iterator age** — отслеживайте отставание consumers
5. **Use enhanced fan-out** — для множества consumers с низкой задержкой
6. **Enable encryption** — KMS encryption для sensitive данных

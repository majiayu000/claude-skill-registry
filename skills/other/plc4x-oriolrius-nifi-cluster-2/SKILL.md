---
name: plc4x
description: Expert guidance for Apache PLC4X industrial protocols library including Siemens S7, Modbus, OPC-UA, integration with Apache NiFi, connection strings, and field addressing. Use this when working with industrial automation and PLC communication.
tags: [plc4x, industrial, iot, scada, automation]
color: green
---

# Apache PLC4X Expert Skill

You are an expert in Apache PLC4X, a universal protocol adapter for industrial automation that allows communication with PLCs using various protocols.

## Core Concepts

### Supported Protocols
- **S7 (Siemens)**: S7-300, S7-400, S7-1200, S7-1500
- **Modbus**: TCP, RTU, ASCII
- **OPC-UA**: Industrial standard protocol
- **Beckhoff ADS**: TwinCAT PLCs
- **EtherNet/IP**: Allen-Bradley PLCs
- **KNX**: Building automation
- **BACnet**: Building automation

### Architecture
```
Application Layer
      ↓
PLC4X API (Protocol-independent)
      ↓
Protocol Drivers (S7, Modbus, OPC-UA, etc.)
      ↓
Network Layer (TCP/IP, Serial, etc.)
      ↓
PLC Device
```

## Connection Strings

### Format
```
protocol://host:port/options?parameter1=value1&parameter2=value2
```

### Examples by Protocol

**Siemens S7**
```
s7://192.168.1.100                           # Default (rack=0, slot=0)
s7://192.168.1.100:102                       # Custom port
s7://192.168.1.100?rack=0&slot=2             # S7-1200/1500 (slot 2)
s7://192.168.1.100?controller-type=S7_400    # Explicit controller type
```

**Modbus TCP**
```
modbus-tcp://192.168.1.200                   # Default port 502
modbus-tcp://192.168.1.200:502               # Explicit port
modbus-tcp://192.168.1.200?unit-identifier=1 # Slave/unit ID
```

**OPC-UA**
```
opcua:tcp://192.168.1.50:4840               # Standard OPC-UA
opcua:tcp://192.168.1.50:4840?discovery=true # Enable discovery
opcua:tcp://user:pass@192.168.1.50:4840    # With authentication
```

**EtherNet/IP**
```
eip://192.168.1.150                         # Allen-Bradley PLC
```

## Field Addressing

### Siemens S7
```
# Data Blocks (DB)
DB1.DBB0             # Byte at DB1, offset 0
DB1.DBW2             # Word (2 bytes) at DB1, offset 2
DB1.DBD4             # Double word (4 bytes) at DB1, offset 4
DB1.DBX0.0           # Bit 0 at DB1, byte 0

# Memory Areas
%I0.0                # Input bit 0.0
%IB0                 # Input byte 0
%IW0                 # Input word 0
%ID0                 # Input double word 0

%Q0.0                # Output bit 0.0
%QB0                 # Output byte 0
%QW0                 # Output word 0
%QD0                 # Output double word 0

%M0.0                # Memory bit 0.0
%MB0                 # Memory byte 0
%MW0                 # Memory word 0
%MD0                 # Memory double word 0

# Data Types
:BOOL                # Boolean
:BYTE                # Byte (8 bits)
:INT                 # Integer (16 bits)
:DINT                # Double Integer (32 bits)
:REAL                # Real (32-bit float)
:STRING(10)          # String with max length
```

### Modbus
```
# Function Codes
holding-register:0              # Read Holding Register (FC03)
input-register:0                # Read Input Register (FC04)
coil:0                          # Read Coil (FC01)
discrete-input:0                # Read Discrete Input (FC02)

# Extended addressing
holding-register:0:INT          # As 16-bit integer
holding-register:0:REAL         # As 32-bit float (2 registers)
holding-register:0[10]          # Array of 10 registers
```

### OPC-UA
```
# Node IDs
ns=2;s=MyVariable               # String identifier
ns=2;i=1001                     # Numeric identifier
ns=3;g=09087e75-8e5e-499b-954f-f2a9603db28a  # GUID
```

## Java API Usage

### Basic Read Example
```java
// Connect to PLC
try (PlcConnection connection = new PlcDriverManager()
    .getConnection("s7://192.168.1.100")) {

    // Build read request
    PlcReadRequest request = connection.readRequestBuilder()
        .addTagAddress("temperature", "DB1.DBD0:REAL")
        .addTagAddress("pressure", "DB1.DBD4:REAL")
        .addTagAddress("running", "DB1.DBX8.0:BOOL")
        .build();

    // Execute read
    PlcReadResponse response = request.execute().get();

    // Get values
    float temp = response.getFloat("temperature");
    float press = response.getFloat("pressure");
    boolean running = response.getBoolean("running");

    System.out.println("Temperature: " + temp);
    System.out.println("Pressure: " + press);
    System.out.println("Running: " + running);
}
```

### Write Example
```java
try (PlcConnection connection = new PlcDriverManager()
    .getConnection("s7://192.168.1.100")) {

    PlcWriteRequest request = connection.writeRequestBuilder()
        .addTagAddress("setpoint", "DB1.DBD10:REAL", 75.5f)
        .addTagAddress("enable", "DB1.DBX12.0:BOOL", true)
        .build();

    PlcWriteResponse response = request.execute().get();

    if (response.getResponseCode("setpoint") == PlcResponseCode.OK) {
        System.out.println("Write successful");
    }
}
```

### Subscription (Polling)
```java
try (PlcConnection connection = new PlcDriverManager()
    .getConnection("s7://192.168.1.100")) {

    PlcSubscriptionRequest request = connection.subscriptionRequestBuilder()
        .addCyclicTagAddress("sensor1", "DB1.DBW0:INT", Duration.ofSeconds(1))
        .addCyclicTagAddress("sensor2", "DB1.DBW2:INT", Duration.ofSeconds(1))
        .build();

    PlcSubscriptionResponse response = request.execute().get();

    response.getSubscriptionHandle("sensor1").register(event -> {
        int value = event.getInteger("sensor1");
        System.out.println("Sensor1: " + value);
    });
}
```

## NiFi Integration

### PLC4X Processors in NiFi

**GetPLC4X** (Read from PLC)
```
Properties:
- PLC Connection String: s7://192.168.1.100
- Fields to Read: temperature:DB1.DBD0:REAL,pressure:DB1.DBD4:REAL,status:DB1.DBX8.0:BOOL
- Polling Interval: 1 sec
- Timeout: 5 sec

Output:
- FlowFile per polling cycle with attributes:
  temperature=25.5
  pressure=1.2
  status=true
```

**PutPLC4X** (Write to PLC)
```
Properties:
- PLC Connection String: s7://192.168.1.100
- Fields to Write: setpoint:DB1.DBD10:REAL,enable:DB1.DBX12.0:BOOL

Input FlowFile Attributes:
  setpoint=75.5
  enable=true

Result: Values written to PLC
```

### NiFi Flow Example
```
GetPLC4X (Read sensor data)
    ↓
RouteOnAttribute (Filter by status)
    ↓
UpdateAttribute (Add timestamp)
    ↓
JoltTransformJSON (Format data)
    ↓
PublishKafka (Send to analytics)
```

### Expression Language in NiFi
```nifi
# Read PLC value and use in flow
${plc.temperature}                    # Access temperature attribute
${plc.temperature:toNumber()}         # Convert to number
${plc.temperature:gt(50)}             # Compare value
```

## Docker Deployment

### Standalone PLC4X Application
```dockerfile
FROM eclipse-temurin:11-jre
COPY plc4x-app.jar /app/
COPY plc4x-drivers/ /app/drivers/
CMD ["java", "-jar", "/app/plc4x-app.jar"]
```

### With NiFi
```yaml
services:
  nifi:
    image: apache/nifi:latest
    volumes:
      - ./nifi-plc4x-nar:/opt/nifi/nifi-current/lib/nifi-plc4x-nar.nar
    environment:
      - NIFI_WEB_HTTP_PORT=8080
    networks:
      - plc-network

networks:
  plc-network:
    driver: bridge
```

## Data Type Mapping

### S7 to Java
| S7 Type | PLC4X Type | Java Type |
|---------|------------|-----------|
| BOOL | BOOL | boolean |
| BYTE | USINT | byte |
| WORD | UINT | short |
| DWORD | UDINT | int |
| INT | INT | short |
| DINT | DINT | int |
| REAL | REAL | float |
| STRING | STRING | String |
| TIME | TIME | Duration |
| DATE | DATE | LocalDate |

### Modbus to Java
| Modbus | PLC4X Type | Java Type |
|--------|------------|-----------|
| Coil | BOOL | boolean |
| Discrete Input | BOOL | boolean |
| Holding Register | UINT | short |
| Input Register | UINT | short |
| 2x Holding Reg | REAL | float |

## Best Practices

### Connection Management
```java
// Use connection pooling for multiple requests
PlcConnectionManager manager = new CachedPlcConnectionManager();
try (PlcConnection connection = manager.getConnection(connectionString)) {
    // Reuse connection
}
```

### Error Handling
```java
try {
    PlcReadResponse response = request.execute().get(5, TimeUnit.SECONDS);

    for (String tagName : response.getTagNames()) {
        if (response.getResponseCode(tagName) == PlcResponseCode.OK) {
            // Process value
        } else {
            // Handle error
            System.err.println("Error reading " + tagName + ": " +
                response.getResponseCode(tagName));
        }
    }
} catch (TimeoutException e) {
    System.err.println("PLC read timeout");
} catch (ExecutionException e) {
    System.err.println("PLC communication error: " + e.getMessage());
}
```

### Performance Optimization
- **Batch reads**: Request multiple tags in one call
- **Connection pooling**: Reuse connections
- **Appropriate polling intervals**: Don't poll faster than needed
- **Use subscriptions**: More efficient than polling for frequent updates

## Troubleshooting

### Common Issues
| Issue | Solution |
|-------|----------|
| Connection timeout | Check IP, port, firewall, PLC rack/slot |
| Access denied | Verify PLC security settings, PUT/GET enabled |
| Invalid address | Check field addressing syntax, data block exists |
| Data type mismatch | Verify PLC data type matches field specification |
| Performance issues | Reduce polling frequency, batch requests |

### Logging
```xml
<!-- logback.xml -->
<logger name="org.apache.plc4x" level="DEBUG"/>
<logger name="org.apache.plc4x.java.s7" level="TRACE"/>
```

### Network Diagnostics
```bash
# Test TCP connection to PLC
nc -zv 192.168.1.100 102

# Monitor network traffic
tcpdump -i eth0 host 192.168.1.100 -w plc-traffic.pcap

# Analyze with Wireshark
wireshark plc-traffic.pcap
```

## Siemens S7 Specific

### Controller Types
- S7_300: Rack 0, Slot 2
- S7_400: Rack 0, Slot 3
- S7_1200: Rack 0, Slot 1
- S7_1500: Rack 0, Slot 1

### Configuration Requirements
1. **Enable PUT/GET** in PLC configuration
2. **Disable block protection** for accessed DBs
3. **Configure network** (IP, subnet, gateway)
4. **Allow external access** in security settings

### TIA Portal Setup
```
1. Open PLC Properties → Protection & Security
2. Connection mechanisms:
   ✓ Permit access with PUT/GET
3. Compile and download to PLC
```

## Resources
- [PLC4X Documentation](https://plc4x.apache.org/users/index.html)
- [Protocol Compatibility](https://plc4x.apache.org/users/protocols/index.html)
- [NiFi PLC4X Processors](https://nifi.apache.org/docs/nifi-docs/components/org.apache.nifi/nifi-plc4x-nar/)
- [GitHub Examples](https://github.com/apache/plc4x/tree/develop/plc4j/examples)

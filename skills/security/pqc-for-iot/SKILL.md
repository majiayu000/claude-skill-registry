---
name: Post-Quantum Cryptography (PQC) for IoT
description: Implement post-quantum cryptographic algorithms (NIST PQC standards) for IoT devices, including quantum-resistant mTLS, crypto-agility, and migration planning to prepare for the quantum computing era.
skill-id: 164
domain: Security / Cryptography / IoT
level: Expert (Enterprise Scale)
maturity: Emerging (2026-2027)
---

# Post-Quantum Cryptography (PQC) for IoT

> **Current Level:** Expert (Enterprise Scale)
> **Domain:** Security / Cryptography / IoT
> **Skill ID:** 164
> **Maturity:** Emerging - เตรียมความพร้อมสำหรับ 2026-2027

---

## Overview

Post-Quantum Cryptography (PQC) for IoT เตรียมความพร้อมสำหรับยุค Quantum Computing ที่อาจจะถอดรหัส Encryption แบบเดิมได้ ทักษะนี้ต่อยอดจาก mTLS & PKI Management (Skill 77) เพื่อรองรับอนาคต โดยใช้ Algorithm ที่ทนทานต่อการถอดรหัสด้วย Quantum Computer

---

## Why This Matters / Strategic Necessity

### Context

Quantum Computing กำลังใกล้เข้ามา:
- **Quantum Threat:** Quantum Computers อาจถอดรหัส RSA/ECC ได้ในอนาคต
- **Harvest Now, Decrypt Later (HNDL):** ข้อมูลที่ถูกดักฟังวันนี้อาจถูกถอดรหัสในอนาคต
- **NSA CNSA 2.0:** กำหนด Timeline สำหรับ Migration ไป PQC
- **Long-term Data:** ข้อมูลที่ต้องเก็บนานต้องใช้ PQC

### Business Impact

- **Future-proof Security:** Security Infrastructure ที่พร้อมสำหรับอนาคต
- **Risk Mitigation:** ลดความเสี่ยงจาก HNDL Attacks
- **Competitive Advantage:** องค์กรที่พร้อม PQC จะได้เปรียบ
- **Compliance:** Compliance กับ NSA CNSA 2.0 Timeline

### Product Thinking

ทักษะนี้ช่วยแก้ปัญหา:
- **Security Teams:** ต้องการ Future-proof Encryption
- **IoT Teams:** ต้องการ PQC สำหรับ IoT Devices
- **Compliance Teams:** ต้องการ Compliance กับ Timeline
- **Customers:** ต้องการความมั่นใจในความปลอดภัยระยะยาว

---

## Core Concepts / Technical Deep Dive

### 1. Quantum-Resistant Algorithms

ใช้ NIST PQC Standards (Kyber, Dilithium, SPHINCS+)

```python
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import hashes
from typing import Tuple, Optional
import os

class PQCKeyExchange:
    """Post-Quantum Key Exchange using Kyber"""
    
    def __init__(self):
        # Initialize PQC library (liboqs)
        self.pqc = self._init_liboqs()
        self.algorithm = "Kyber512"  # NIST standard
    
    def generate_keypair(self) -> Tuple[bytes, bytes]:
        """
        Generate PQC key pair.
        
        Returns (public_key, private_key)
        """
        # Using Kyber (Key Encapsulation Mechanism)
        public_key, private_key = self.pqc.keypair(self.algorithm)
        
        return public_key, private_key
    
    def encapsulate(
        self,
        public_key: bytes
    ) -> Tuple[bytes, bytes]:
        """
        Encapsulate shared secret using public key.
        
        Returns (ciphertext, shared_secret)
        """
        ciphertext, shared_secret = self.pqc.encapsulate(
            self.algorithm,
            public_key
        )
        
        return ciphertext, shared_secret
    
    def decapsulate(
        self,
        ciphertext: bytes,
        private_key: bytes
    ) -> bytes:
        """
        Decapsulate shared secret using private key.
        
        Returns shared_secret
        """
        shared_secret = self.pqc.decapsulate(
            self.algorithm,
            ciphertext,
            private_key
        )
        
        return shared_secret

class HybridKeyExchange:
    """
    Hybrid Classical + PQC Key Exchange.
    
    Provides security even if one algorithm is broken.
    """
    
    def __init__(self):
        self.classical = x25519.X25519PrivateKey.generate()
        self.pqc = PQCKeyExchange()
    
    def hybrid_key_exchange(
        self,
        peer_public_key_classical: bytes,
        peer_public_key_pqc: bytes
    ) -> bytes:
        """
        Perform hybrid key exchange.
        
        Combines classical (X25519) and PQC (Kyber) keys.
        """
        # Classical key exchange
        classical_shared = self._classical_key_exchange(
            peer_public_key_classical
        )
        
        # PQC key exchange
        pqc_ciphertext, pqc_shared = self.pqc.encapsulate(
            peer_public_key_pqc
        )
        
        # Combine both secrets
        combined_secret = self._combine_secrets(
            classical_shared,
            pqc_shared
        )
        
        return combined_secret
    
    def _combine_secrets(
        self,
        secret1: bytes,
        secret2: bytes
    ) -> bytes:
        """Combine two secrets using HKDF"""
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF
        
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'hybrid-key-exchange'
        )
        
        combined = secret1 + secret2
        return hkdf.derive(combined)
```

### 2. Post-Quantum TLS (PQTLS)

ปรับ mTLS ให้ใช้ PQC Algorithms

```python
class PQTLSConnection:
    """Post-Quantum TLS connection"""
    
    def __init__(self):
        self.pqc_algorithms = {
            "kem": "Kyber512",  # Key Encapsulation
            "signature": "Dilithium2"  # Digital Signature
        }
    
    def establish_pqtls_connection(
        self,
        server_hostname: str,
        port: int = 443
    ) -> Dict:
        """
        Establish PQTLS connection.
        
        Uses hybrid classical + PQC algorithms.
        """
        # Client Hello with PQC support
        client_hello = {
            "tls_version": "1.3",
            "cipher_suites": [
                "TLS_AES_256_GCM_SHA384",
                "TLS_CHACHA20_POLY1305_SHA256"
            ],
            "supported_groups": [
                "x25519",  # Classical
                "Kyber512"  # PQC
            ],
            "signature_algorithms": [
                "ed25519",  # Classical
                "Dilithium2"  # PQC
            ],
            "pqc_extension": True
        }
        
        # Server responds with selected algorithms
        server_hello = self._send_client_hello(client_hello, server_hostname, port)
        
        # Perform hybrid key exchange
        if server_hello.get("pqc_supported"):
            # Use hybrid (classical + PQC)
            shared_secret = self._hybrid_key_exchange(
                server_hello["server_keys"]
            )
        else:
            # Fallback to classical only
            shared_secret = self._classical_key_exchange(
                server_hello["server_keys"]
            )
        
        # Derive session keys
        session_keys = self._derive_session_keys(shared_secret)
        
        return {
            "connection_established": True,
            "pqc_enabled": server_hello.get("pqc_supported", False),
            "algorithms_used": {
                "kem": server_hello.get("kem_algorithm", "x25519"),
                "signature": server_hello.get("signature_algorithm", "ed25519")
            },
            "session_keys": session_keys
        }
```

### 3. Crypto-Agility

ออกแบบระบบให้เปลี่ยน Algorithm ได้ง่าย

```python
class CryptoAgileSystem:
    """Crypto-agile system that can switch algorithms easily"""
    
    def __init__(self):
        self.algorithm_registry = {}
        self.current_algorithm = "x25519"
        self.fallback_algorithms = ["x25519", "Kyber512"]
    
    def register_algorithm(
        self,
        algorithm_id: str,
        algorithm_type: str,  # "kem", "signature", "hash"
        implementation: callable,
        priority: int = 5
    ):
        """Register a cryptographic algorithm"""
        self.algorithm_registry[algorithm_id] = {
            "type": algorithm_type,
            "implementation": implementation,
            "priority": priority,
            "enabled": True
        }
    
    def negotiate_algorithm(
        self,
        peer_supported: List[str],
        required_security_level: str = "high"
    ) -> str:
        """
        Negotiate best algorithm with peer.
        
        Prefers PQC but falls back to classical if needed.
        """
        # Get available algorithms
        available = [
            alg_id for alg_id, alg_info in self.algorithm_registry.items()
            if alg_info["enabled"]
        ]
        
        # Find intersection
        common = set(available) & set(peer_supported)
        
        if not common:
            raise ValueError("No common algorithms")
        
        # Prefer PQC algorithms
        pqc_algorithms = [
            alg for alg in common
            if self.algorithm_registry[alg]["type"] in ["kem", "signature"]
            and "Kyber" in alg or "Dilithium" in alg
        ]
        
        if pqc_algorithms:
            # Select highest priority PQC
            selected = max(
                pqc_algorithms,
                key=lambda x: self.algorithm_registry[x]["priority"]
            )
        else:
            # Fallback to classical
            selected = max(
                common,
                key=lambda x: self.algorithm_registry[x]["priority"]
            )
        
        return selected
    
    def migrate_algorithm(
        self,
        from_algorithm: str,
        to_algorithm: str,
        devices: List[str]
    ) -> Dict:
        """
        Migrate devices from one algorithm to another.
        
        Supports gradual migration with backward compatibility.
        """
        migration_plan = {
            "from": from_algorithm,
            "to": to_algorithm,
            "devices": devices,
            "phases": []
        }
        
        # Phase 1: Deploy new algorithm alongside old
        migration_plan["phases"].append({
            "phase": 1,
            "description": "Dual algorithm support",
            "devices": devices,
            "action": "Enable new algorithm, keep old enabled"
        })
        
        # Phase 2: Gradual migration
        batch_size = len(devices) // 4
        for i in range(0, len(devices), batch_size):
            batch = devices[i:i+batch_size]
            migration_plan["phases"].append({
                "phase": 2 + (i // batch_size),
                "description": f"Migrate batch {i // batch_size + 1}",
                "devices": batch,
                "action": "Switch to new algorithm, verify compatibility"
            })
        
        # Phase 3: Complete migration
        migration_plan["phases"].append({
            "phase": len(migration_plan["phases"]) + 1,
            "description": "Disable old algorithm",
            "devices": devices,
            "action": "Disable old algorithm, remove support"
        })
        
        return migration_plan
```

### 4. PQC for Constrained Devices

PQC สำหรับ Microcontrollers ที่มี Resource จำกัด

```python
class LightweightPQC:
    """Lightweight PQC implementations for IoT devices"""
    
    def __init__(self):
        self.lightweight_algorithms = {
            "SPHINCS+-128f": {
                "signature_size": 7856,  # bytes
                "key_size": 32,
                "memory_required": 16384,  # bytes
                "suitable_for": ["ESP32", "Cortex-M4"]
            },
            "SPHINCS+-128s": {
                "signature_size": 17088,
                "key_size": 32,
                "memory_required": 8192,
                "suitable_for": ["ESP32", "Cortex-M4"]
            },
            "Kyber512": {
                "key_size": 800,
                "ciphertext_size": 768,
                "memory_required": 4096,
                "suitable_for": ["ESP32", "Raspberry Pi"]
            }
        }
    
    def select_algorithm_for_device(
        self,
        device_type: str,
        available_memory: int,
        performance_requirements: Dict
    ) -> str:
        """
        Select appropriate PQC algorithm for device.
        
        Considers memory, performance, and security requirements.
        """
        suitable = []
        
        for alg_name, alg_spec in self.lightweight_algorithms.items():
            if device_type in alg_spec["suitable_for"]:
                if alg_spec["memory_required"] <= available_memory:
                    suitable.append((alg_name, alg_spec))
        
        if not suitable:
            raise ValueError(f"No suitable PQC algorithm for {device_type}")
        
        # Select based on requirements
        if performance_requirements.get("signature_speed") == "fast":
            # Prefer smaller signatures
            selected = min(suitable, key=lambda x: x[1]["signature_size"])
        else:
            # Prefer smaller memory footprint
            selected = min(suitable, key=lambda x: x[1]["memory_required"])
        
        return selected[0]
    
    def optimize_for_memory(
        self,
        algorithm: str,
        device_constraints: Dict
    ) -> Dict:
        """
        Optimize PQC implementation for memory-constrained devices.
        
        Uses techniques like:
        - In-place operations
        - Streaming algorithms
        - Memory-mapped operations
        """
        optimizations = {
            "algorithm": algorithm,
            "original_memory": self.lightweight_algorithms[algorithm]["memory_required"],
            "optimizations": []
        }
        
        # Optimization 1: Use streaming for large operations
        if device_constraints["memory"] < optimizations["original_memory"]:
            optimizations["optimizations"].append({
                "type": "streaming",
                "description": "Process data in chunks",
                "memory_reduction": "50%"
            })
        
        # Optimization 2: In-place operations
        optimizations["optimizations"].append({
            "type": "in_place",
            "description": "Reuse memory buffers",
            "memory_reduction": "30%"
        })
        
        # Calculate optimized memory
        total_reduction = sum(
            float(opt["memory_reduction"].rstrip("%")) / 100
            for opt in optimizations["optimizations"]
        )
        
        optimizations["optimized_memory"] = int(
            optimizations["original_memory"] * (1 - total_reduction)
        )
        
        return optimizations
```

### 5. Migration Planning

วางแผน Migration ไป PQC

```python
class PQCMigrationPlanner:
    """Plan migration to Post-Quantum Cryptography"""
    
    def create_migration_plan(
        self,
        inventory: Dict
    ) -> Dict:
        """
        Create comprehensive PQC migration plan.
        
        Based on NSA CNSA 2.0 timeline.
        """
        plan = {
            "created_at": datetime.utcnow().isoformat(),
            "timeline": "2024-2027",
            "phases": []
        }
        
        # Phase 1: Inventory and Assessment (2024)
        plan["phases"].append({
            "phase": 1,
            "name": "Inventory & Assessment",
            "timeline": "2024",
            "tasks": [
                "Catalog all cryptographic systems",
                "Identify critical systems",
                "Assess quantum risk",
                "Prioritize migration targets"
            ],
            "deliverables": [
                "Cryptographic inventory",
                "Risk assessment",
                "Migration priority list"
            ]
        })
        
        # Phase 2: Algorithm Selection (2024-2025)
        plan["phases"].append({
            "phase": 2,
            "name": "Algorithm Selection",
            "timeline": "2024-2025",
            "tasks": [
                "Select NIST PQC algorithms",
                "Test algorithm performance",
                "Validate compatibility",
                "Create hybrid implementations"
            ],
            "deliverables": [
                "Algorithm selection matrix",
                "Performance benchmarks",
                "Hybrid implementation guide"
            ]
        })
        
        # Phase 3: Pilot Implementation (2025)
        plan["phases"].append({
            "phase": 3,
            "name": "Pilot Implementation",
            "timeline": "2025",
            "tasks": [
                "Deploy PQC in test environment",
                "Validate security",
                "Test interoperability",
                "Train teams"
            ],
            "deliverables": [
                "Pilot deployment report",
                "Security validation",
                "Training materials"
            ]
        })
        
        # Phase 4: Gradual Migration (2025-2026)
        plan["phases"].append({
            "phase": 4,
            "name": "Gradual Migration",
            "timeline": "2025-2026",
            "tasks": [
                "Migrate non-critical systems",
                "Monitor performance",
                "Address issues",
                "Expand to critical systems"
            ],
            "deliverables": [
                "Migration progress reports",
                "Performance metrics",
                "Issue resolution log"
            ]
        })
        
        # Phase 5: Complete Migration (2026-2027)
        plan["phases"].append({
            "phase": 5,
            "name": "Complete Migration",
            "timeline": "2026-2027",
            "tasks": [
                "Migrate all systems",
                "Disable classical algorithms",
                "Final validation",
                "Documentation"
            ],
            "deliverables": [
                "Migration completion report",
                "Final security audit",
                "Updated documentation"
            ]
        })
        
        return plan
    
    def assess_quantum_risk(
        self,
        system: Dict
    ) -> Dict:
        """
        Assess quantum risk for system.
        
        Higher risk = higher priority for migration.
        """
        risk_score = 0
        factors = []
        
        # Factor 1: Data sensitivity
        if system.get("data_sensitivity") == "high":
            risk_score += 10
            factors.append("High sensitivity data")
        
        # Factor 2: Data retention period
        retention_years = system.get("retention_years", 0)
        if retention_years > 10:
            risk_score += 8
            factors.append(f"Long retention ({retention_years} years)")
        elif retention_years > 5:
            risk_score += 5
            factors.append(f"Medium retention ({retention_years} years)")
        
        # Factor 3: Current algorithm
        current_alg = system.get("crypto_algorithm", "")
        if "RSA" in current_alg or "ECC" in current_alg:
            risk_score += 7
            factors.append("Vulnerable to quantum attacks")
        
        # Factor 4: Exposure risk
        if system.get("exposed_to_public"):
            risk_score += 6
            factors.append("Publicly exposed - HNDL risk")
        
        # Determine risk level
        if risk_score >= 20:
            risk_level = "critical"
        elif risk_score >= 15:
            risk_level = "high"
        elif risk_score >= 10:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "system_id": system["id"],
            "risk_score": risk_score,
            "risk_level": risk_level,
            "factors": factors,
            "migration_priority": "high" if risk_level in ["critical", "high"] else "medium"
        }
```

---

## Tooling & Tech Stack

### Enterprise Tools

- **PQC Libraries:**
  - liboqs (Open Quantum Safe)
  - PQClean (Clean PQC implementations)
  - BoringSSL PQC branch
  - OpenSSL with PQC support

- **Cloud Support:**
  - AWS KMS PQC Preview
  - Cloudflare PQC Support
  - Google Cloud PQC (coming)

### Configuration Essentials

```yaml
# pqc-config.yaml
pqc:
  algorithms:
    kem: "Kyber512"  # Key Encapsulation
    signature: "Dilithium2"  # Digital Signature
    hash: "SHA3-256"  # Hash function
  
  hybrid_mode:
    enabled: true
    classical_algorithm: "x25519"
    pqc_algorithm: "Kyber512"
    fallback_enabled: true
  
  migration:
    timeline: "2024-2027"
    current_phase: "assessment"
    priority_systems: ["iot_devices", "api_gateways"]
  
  iot:
    lightweight_algorithm: "SPHINCS+-128s"
    memory_optimization: true
    hardware_acceleration: false
```

---

## Standards, Compliance & Security

### International Standards

- **NIST FIPS 203/204/205:** PQC Standards (Kyber, Dilithium, SPHINCS+)
- **NSA CNSA 2.0:** Migration timeline and requirements
- **ETSI QSC:** Quantum-Safe Cryptography standards
- **IETF Post-Quantum Drafts:** PQTLS specifications

### Security Protocol

- **Hybrid Approach:** Use both classical and PQC (defense in depth)
- **Algorithm Negotiation:** Support multiple algorithms
- **Backward Compatibility:** Support gradual migration

---

## Quick Start / Getting Ready

### Phase 1: Assessment (Week 1-2)

1. **Inventory Cryptographic Systems:**
   ```python
   planner = PQCMigrationPlanner()
   inventory = catalog_crypto_systems()
   risk_assessment = planner.assess_quantum_risk(inventory)
   ```

2. **Select Algorithms:**
   - Choose NIST PQC algorithms
   - Test performance
   - Validate compatibility

### Phase 2: Pilot (Week 3-6)

1. **Deploy Hybrid Implementation:**
   ```python
   hybrid = HybridKeyExchange()
   # Use both classical and PQC
   ```

2. **Test and Validate:**
   - Security testing
   - Performance testing
   - Interoperability testing

---

## Production Checklist

- [ ] **Assessment:**
  - [ ] Cryptographic inventory complete
  - [ ] Risk assessment done
  - [ ] Migration plan created

- [ ] **Implementation:**
  - [ ] PQC algorithms selected
  - [ ] Hybrid implementation deployed
  - [ ] Testing completed

- [ ] **Migration:**
  - [ ] Pilot deployment successful
  - [ ] Gradual migration in progress
  - [ ] Monitoring active

---

## Anti-patterns

### 1. **Waiting Too Long**
❌ **Bad:** Wait until quantum computers exist
```python
# ❌ Bad - Too late
# "We'll migrate when quantum computers are available"
# But data encrypted today can be decrypted later!
```

✅ **Good:** Start migration now
```python
# ✅ Good - Start now
plan = create_migration_plan(inventory)
start_phase_1()  # Begin assessment now
```

### 2. **No Hybrid Approach**
❌ **Bad:** Use only PQC, no fallback
```python
# ❌ Bad - No fallback
# If PQC has issues, system breaks
```

✅ **Good:** Use hybrid (classical + PQC)
```python
# ✅ Good - Defense in depth
hybrid = HybridKeyExchange()  # Both algorithms
```

---

## Timeline & Adoption Curve

### 2024-2025: Preparation Phase
- NIST PQC standards finalized
- Early adopters begin migration
- Tools and libraries mature

### 2025-2026: Active Migration
- NSA CNSA 2.0 timeline
- Mainstream adoption begins
- Hybrid implementations standard

### 2026-2027: Completion
- Critical systems migrated
- Classical algorithms deprecated
- PQC becomes standard

---

## Integration Points / Related Skills

- [Skill 77: mTLS & PKI Management](../74-iot-zero-trust-security/mtls-pki-management/SKILL.md) - TLS/PKI foundations
- [Skill 76: Hardware-Rooted Identity](../74-iot-zero-trust-security/hardware-rooted-identity/SKILL.md) - Hardware security
- [Skill 163: AI Supply Chain Security](../88-ai-supply-chain-security/model-bom-security/SKILL.md) - Supply chain security

---

## Further Reading

- [NIST PQC Project](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [Open Quantum Safe](https://openquantumsafe.org/)
- [NSA CNSA 2.0](https://media.defense.gov/2022/Sep/07/2003071834/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS_.PDF)
- [IETF Post-Quantum TLS](https://datatracker.ietf.org/wg/tls/about/)
- [ETSI Quantum-Safe Cryptography](https://www.etsi.org/technologies/quantum-safe-cryptography)

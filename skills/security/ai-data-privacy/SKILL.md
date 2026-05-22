---
name: AI Data Privacy
description: Protecting personal and sensitive data throughout the machine learning lifecycle, from training to inference.
---

# AI Data Privacy

## Overview

AI Data Privacy is the practice of ensuring that the personal and sensitive data used to train and serve AI models is protected against unauthorized access, disclosure, or re-identification. Machine learning models can inadvertently "memorize" training data, creating unique privacy risks.

**Core Principle**: "The model should learn patterns, not people."

---

## 1. Unique Privacy Risks in AI

| Risk Type | Description |
| :--- | :--- |
| **Model Inversion** | An attacker uses model outputs to reconstruct sensitive training data. |
| **Membership Inference**| Determining if a specific individual's data was part of the training set. |
| **Data Leakage** | The model outputs PII (names, SSNs) that it "memorized" during training. |
| **Re-identification** | Combining anonymized data with other datasets to identify users. |

---

## 2. Privacy-Enhancing Technologies (PETs)

Modern AI requires sophisticated math to protect privacy without losing utility.

### A. Differential Privacy (DP)
Adding "noise" to data so that the presence or absence of a single individual cannot be determined from the final model.
*   **Key Concept**: The **Epsilon ($\epsilon$)** value. A lower Epsilon means higher privacy but potentially lower accuracy.

### B. Federated Learning
The model is trained across multiple devices (e.g., mobile phones) without the raw data ever leaving the device. Only "parameter updates" are sent to the central server.
*   **Best For**: Healthcare, mobile keyboard suggestions.

### C. Homomorphic Encryption
Performing calculations on encrypted data without ever decrypting it.
*   **Status**: High security, but currently very slow (high compute cost).

---

## 3. Data Minimization and Anonymization

### The Pre-training Filter
Before data reaches the training pipeline, it must be cleansed:

1.  **De-identification**: Removing Direct Identifiers (Name, SSN, IP Address).
2.  **Generalization**: Replacing specific values with ranges (e.g., Age 25 -> Age 20-30).
3.  **K-Anonymity**: Ensuring a record is indistinguishable from at least $k-1$ other records.
4.  **PII Reduction**: Using tools like **Microsoft Presidio** to auto-detect and scrub sensitive text.

---

## 4. Implementation: Privacy-Aware Training

### Using Differential Privacy with PyTorch (Opacus)
```python
from opacus import PrivacyEngine

model = MyModel()
optimizer = torch.optim.SGD(model.parameters(), lr=0.05)

# Wrap model and optimizer with PrivacyEngine
privacy_engine = PrivacyEngine()
model, optimizer, train_loader = privacy_engine.make_private(
    module=model,
    optimizer=optimizer,
    data_loader=train_loader,
    noise_multiplier=1.1,
    max_grad_norm=1.0,
)
```

---

## 5. Right to Be Forgotten: "Model Unlearning"

Under GDPR, if a user requests to be deleted, their influence on a trained model might also need to be removed.

**Current Approaches**:
1.  **Re-training**: Deleting the user data and training the model again from scratch (High cost).
2.  **Sharding & Slicing (SISA)**: Training multiple small models on data subsets. Only the subset containing the user's data needs re-training.
3.  **Influence Functions**: Mathematically adjusting model weights to "subtract" a user's contribution.

---

## 6. Prompt Privacy (Inference Defense)

Preventing users from "jailbreaking" an LLM to reveal training data.

*   **Input Filtering**: Scrubbing PII from user prompts before sending to an LLM provider.
*   **Output Filtering**: Running a post-processing check on LLM responses to ensure no sensitive data is leaked.

```typescript
// Example: Simple PII Filter
function scrubPrompt(prompt: string): string {
  const emailRegex = /[\w.-]+@[\w.-]+/g;
  const ssnRegex = /\b\d{3}-\d{2}-\d{4}\b/g;
  
  return prompt
    .replace(emailRegex, "[EMAIL]")
    .replace(ssnRegex, "[SSN]");
}
```

---

## 7. Compliance Frameworks for AI Privacy

*   **GDPR Article 22**: Provisions against "solely automated decision-making" that significantly affects users.
*   **EU AI Act**: Requirements for high-quality, privacy-compliant training data.
*   **ISO/IEC 27701**: Extension to ISO 27001 specifically for privacy information management.

---

## 8. Tools for AI Privacy

1.  **Microsoft Presidio**: PII detection and anonymization.
2.  **Opacus**: PyTorch library for Differential Privacy.
3.  **OpenMined (PySyft)**: Framework for secure, multi-party computation and federated learning.
4.  **Google Differential Privacy**: C++, Java, and Go libraries for DP.

---

## 9. AI Data Privacy Checklist

- [ ] **Data Minimization**: Have we removed all "unnecessary" fields from the training set?
- [ ] **Anonymization**: Are all direct identifiers scrubbed/hashed?
- [ ] **Epsilon Value**: If using Differential Privacy, what is our privacy budget ($\epsilon$)?
- [ ] **Unlearning**: Do we have a process to handle "Right to be Forgotten" requests?
- [ ] **Third-party risk**: If using a Cloud LLM (OpenAI/Anthropic), do we have a DPA (Data Processing Agreement)?
- [ ] **Inference Logging**: Are we scrubbing PII from the logs of user interactions?
- [ ] **Model Card**: Does the model documentation list the privacy protections used?

---

## Related Skills
* `44-ai-governance/ai-ethics-compliance`
* `44-ai-governance/model-risk-management`
* `43-data-reliability/data-retention-archining`
* `00-meta-skills/security-awareness`

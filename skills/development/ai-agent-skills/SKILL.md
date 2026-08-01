---
name: ai-agent-skills
description: Here’s a complete breakdown of how to configure and set up the SMS Skill
  in raiaAI’s Launch Pad. This skill allows your AI agent to engage with users through
  two-way text messaging using a phone number assigned via Twilio.
---

# SMS Skill

Here’s a complete breakdown of how to **configure and set up the SMS Skill** in raiaAI’s Launch Pad. This skill allows your AI agent to engage with users through two-way text messaging using a phone number assigned via Twilio.

***



<figure><img src="../.gitbook/assets/Screenshot 2025-04-17 at 9.30.40 AM.png" alt=""><figcaption></figcaption></figure>

#### &#x20;**SMS Skill Setup Guide in Launch Pad**

**1. Assign a Phone Number**

* **Country Code (Required):**\
  Select the country. This determines the pool of numbers.
* **Phone Number Assignment (Automatic):**\
  Once the country is selected, a Twilio number is auto-assigned.
  * You can refresh to get a different number _before setup is finalized_.
  * **Note:** After setup, the number **cannot** be changed.

***

**2. Configure the Messaging Template**

This is what users will first receive when the agent sends a text.

*   **Default SMS Introduction (Required):**\
    A welcome or context-setting message, e.g.:

    > "Hi! I'm Alex, your AI assistant. I’m here to help you with your questions and can connect you with a human if needed."
*   **SMS Signature (Required):**\
    Adds a branded closing to each message, e.g.:

    > “— The Acme Team 🚀”

***

**3. Send Test Message**

* **Send Test Button:**\
  Use this to preview what the intro and signature look like when sent. It ensures formatting and tone are on point before you go live.

***

**4. Save Settings**

* Finalize all the above fields and click **Save** to activate the skill.

***

#### ⚠️ Key Notes

* All fields (intro + signature) are **required**. You can’t proceed without them.
* Once the number is assigned and setup is completed, it is **locked**.
* SMS skill is subject to Twilio compliance rules (e.g., opt-out handling with “STOP”).

***

#### 🔐 Optional Add-ons to Consider (via Campaigns or Functions)

* **Opt-out Logic:** Auto-handle responses like "STOP" or "UNSUBSCRIBE"
* **Time Zone Control:** Avoid sending messages during off-hours (via campaign logic)
* **Reply Triggers:** Set up keyword-based flows or webhooks

***

## [SMS Video Setup](https://www.youtube.com/watch?v=ictMiQmgwag)

{% embed url="https://www.youtube.com/watch?v=ictMiQmgwag" %}


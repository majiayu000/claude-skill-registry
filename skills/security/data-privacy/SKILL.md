---
name: data-privacy
description: Understanding and managing what digital services collect, store, share, and infer about you. Covers password security and entropy, multi-factor authentication, privacy settings, data minimization, the difference between first-party and third-party tracking, cookies and fingerprinting, privacy laws (GDPR, CCPA), and how to respond to data breaches. Use when helping a learner make informed decisions about what to share, with whom, and under what terms.
type: skill
category: digital-literacy
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/digital-literacy/data-privacy/SKILL.md
superseded_by: null
---
# Data Privacy

Data privacy is the practical discipline of deciding what personal information to share with which services, under what conditions, and for what purpose. It is not about being paranoid and it is not about opting out of modern life. It is about developing the habits and mental models that let you participate in digital systems without letting those systems accumulate more leverage over you than you intended. This skill covers authentication (keeping accounts your own), collection (what services take), aggregation (what they infer), and remediation (what to do when things go wrong).

**Agent affinity:** palfrey (institutional privacy), boyd (contextual integrity), noble (platform power asymmetry)

**Concept IDs:** diglit-password-security, diglit-privacy-management, diglit-data-collection, diglit-digital-footprint

## Password Security

Passwords are still the front door for most accounts. Two-thirds of real-world breaches trace back to weak or reused passwords. The principles:

### Entropy, not cleverness

A password's strength is its entropy -- the number of possible values an attacker must try. A 12-character random string has more entropy than "Tr0ub4dor&3" (the old XKCD joke). A four-word passphrase like "correct horse battery staple" has similar entropy to a 10-12 character random string, and is easier to remember.

**Minimum in 2026:** 12 characters random or 4+ word passphrase. 16+ characters for high-stakes accounts.

### No reuse

The single most important password rule: never reuse passwords across accounts that matter. When one site leaks, attackers try the same credentials everywhere else (credential stuffing). One breach becomes many.

### Password managers

You cannot remember hundreds of unique strong passwords. A password manager stores them encrypted behind a single master password. Good options in 2026: 1Password, Bitwarden (open source), KeePassXC (local, open source). Most operating systems also include one.

**Counterintuitively:** Using a password manager is safer than not using one, even though "all your passwords in one place" sounds risky. The alternative is reuse, and reuse is worse.

### Multi-factor authentication (MFA)

Multi-factor authentication requires a second proof beyond the password: something you have (phone, hardware key) or something you are (fingerprint, face). Even a perfect credential stuffing attack fails without the second factor.

**Hierarchy of MFA strength (weakest to strongest):**

1. SMS codes -- vulnerable to SIM swap attacks but still better than no MFA
2. Authenticator apps (Authy, Google Authenticator) -- not SIM-swappable
3. Push notifications to a trusted device -- convenient, phishing-resistant when implemented well
4. Hardware security keys (YubiKey, Titan) -- gold standard, phishing-resistant by design

Turn on MFA for anything that matters. Email is the highest priority -- it is the reset address for everything else.

### Phishing resistance

The weakest link in authentication is the user. Phishing sites trick you into typing credentials into attacker-controlled forms. Defenses:

- **Check the URL before typing.** Real domains have no typos. "amaz0n.com" is not Amazon.
- **Use a password manager to autofill.** Managers do not autofill on wrong domains. If it does not autofill, you are probably on a fake site.
- **Do not click links in emails for account issues.** Type the URL or use your bookmark.
- **Use hardware keys.** They are cryptographically bound to the real domain.

## What Services Collect

Digital services collect three kinds of data about you:

### First-party data

What you tell the service directly: name, email, address, preferences, the content of your messages, your purchases. This data is usually necessary for the service to work, and the service's privacy policy describes what they do with it.

### Observed behavior

How you use the service: which pages you visit, how long you stay, what you click, when you log in. This is logged automatically. It does not require you to share anything explicitly.

### Third-party tracking

What happens on other sites. This is the most contentious category. It works via cookies, pixels, and fingerprinting:

- **Third-party cookies** -- A tracker (like a Facebook Like button) is embedded in thousands of sites. Your browser sends that tracker a cookie on every visit, building a profile across sites. Third-party cookies are being phased out in most browsers but replacements (Privacy Sandbox, server-side tracking) are emerging.
- **Pixels and beacons** -- Invisible image tags that report your visit back to a tracker.
- **Device fingerprinting** -- Unique combinations of screen size, installed fonts, browser version, and hardware create a "fingerprint" that identifies your device even without cookies.

## What Services Infer

Collection is the visible part. Inference is the dangerous part. From raw behavior, services infer:

- Demographics (age, gender, ethnicity, income bracket)
- Interests (health conditions, political views, religion)
- Relationships (who you know, who you live with)
- Intentions (shopping for X, planning a trip, job searching)

The inferred profile is often more sensitive than anything you explicitly shared. This is why a pregnancy can be inferred from shopping patterns before any announcement. The combination of innocuous signals is more revealing than any one signal alone.

## Privacy Settings: Practical Discipline

Every major service has privacy settings, and most users never change the defaults. The defaults favor the service. A practical routine:

1. **Audit at setup.** When you create an account, go through the privacy settings before using the service.
2. **Review quarterly.** Settings change; new options appear; old ones get renamed.
3. **Minimize by default.** Turn off what you do not need. You can turn things back on later.
4. **Separate audiences.** Use lists, close friends, or separate accounts to control who sees what.
5. **Revoke old integrations.** Third-party apps accumulate in your "connected apps" list. Revoke anything you no longer use.

### Data minimization

The best privacy is not collecting data in the first place. When a service asks for your phone number "for security," ask whether you can skip it. When a form has optional fields, leave them blank. When a service needs your birth date, give the month and year only if possible.

## Privacy Laws

Laws vary by jurisdiction but the major frameworks share structure:

### GDPR (EU, 2018)

The General Data Protection Regulation gives EU residents rights over their data: access, correction, deletion, portability, and objection to processing. Services operating in the EU must honor these rights or face fines up to 4% of global revenue.

### CCPA / CPRA (California)

The California Consumer Privacy Act and its amendment (CPRA) give California residents similar rights: access, deletion, opt-out of sale, and anti-discrimination for exercising rights.

### Patchwork elsewhere

Most jurisdictions have some privacy law, with varying strength: PIPEDA (Canada), LGPD (Brazil), PDPA (Singapore). The U.S. lacks a comprehensive federal law as of 2026; protections are sector-specific (HIPAA for health, FERPA for education, GLBA for finance).

### Practical implication

You usually have a right to request what a service knows about you and have it deleted. The request process is often cumbersome on purpose. Use tools like PrivacyDuck, DeleteMe, or the service's own data request forms.

## Responding to Breaches

Breaches happen. When your data leaks:

1. **Change the breached password immediately.** If you reused it, change it everywhere.
2. **Check haveibeenpwned.com.** This free service tracks breaches and tells you if your email appears in known dumps.
3. **Enable MFA if you have not.** Breached credentials become credential stuffing fuel.
4. **Freeze your credit (if SSN or financial data was exposed).** Free in the U.S. through all three bureaus. Prevents new accounts being opened.
5. **Watch for phishing.** Breach data gets used for targeted phishing. Be extra suspicious of "security" emails for weeks afterward.

## When NOT to Use This Skill

- **Evaluating a news claim.** Use `information-evaluation`.
- **Online behavior and etiquette.** Use `digital-citizenship`.
- **Understanding why an algorithm showed you something.** Use `algorithmic-awareness`.

## Decision Guidance

Before giving any digital service your data, ask:

1. **Is this data necessary for the service to work?** If no, do not provide it.
2. **What will the service do with it?** Read the privacy policy, or at least the summary. If the service cannot or will not tell you, that is a signal.
3. **What happens if this data leaks?** If the answer is "nothing," proceed. If the answer involves real harm (identity theft, stalking, professional damage), raise the bar.
4. **Is there a less data-hungry alternative?** Often yes. Prefer it.

## Cross-References

- **palfrey agent:** Institutional privacy, legal frameworks, Berkman Klein framing
- **boyd agent:** Contextual integrity, privacy as control over audience
- **noble agent:** Power asymmetry between platforms and users
- **digital-citizenship skill:** How to behave once you know what is public
- **algorithmic-awareness skill:** How collected data is used to shape your experience

## References

- Solove, D. J. (2008). *Understanding Privacy*. Harvard University Press.
- Nissenbaum, H. (2010). *Privacy in Context: Technology, Policy, and the Integrity of Social Life*. Stanford University Press.
- Zuboff, S. (2019). *The Age of Surveillance Capitalism*. PublicAffairs.
- Electronic Frontier Foundation. *Surveillance Self-Defense*. (Open resource, eff.org/sls.)
- haveibeenpwned.com -- breach tracking, Troy Hunt.

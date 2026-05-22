---
name: zero-trust
description: Zero Trust architecture principles including ZTNA, micro-segmentation, identity-first security, continuous verification, and BeyondCorp patterns. Use when designing network security, implementing identity-based access, or building cloud-native applications with zero trust principles.
---

# Zero Trust Architecture

## Overview

Zero Trust is a security model that assumes no implicit trust based on network location. Every access request is fully authenticated, authorized, and encrypted regardless of origin.

**Keywords:** zero trust, ZTNA, micro-segmentation, identity-first, continuous verification, BeyondCorp, never trust always verify, least privilege, mTLS, service mesh, identity proxy

## When to Use This Skill

- Designing network security architecture
- Implementing identity-based access control
- Setting up micro-segmentation
- Configuring service-to-service authentication
- Building BeyondCorp-style access
- Implementing continuous verification
- Designing cloud-native security

## Zero Trust Principles

| Principle | Description | Implementation |
| --- | --- | --- |
| **Never Trust, Always Verify** | No implicit trust based on network | Authenticate every request |
| **Least Privilege** | Minimum necessary access | Role-based, time-limited access |
| **Assume Breach** | Design for compromise | Micro-segmentation, blast radius reduction |
| **Verify Explicitly** | All signals for authorization | Identity, device, location, behavior |
| **Continuous Verification** | Don't trust past authentication | Session validation, risk-based re-auth |

## Zero Trust Architecture Components

```text
┌─────────────────────────────────────────────────────────────────┐
│                    ZERO TRUST ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────┐    ┌─────────────┐    ┌──────────────────────┐  │
│  │   USER     │───▶│  IDENTITY   │───▶│  POLICY ENGINE       │  │
│  │  + Device  │    │   PROXY     │    │  (Context Analysis)  │  │
│  └────────────┘    └─────────────┘    └──────────┬───────────┘  │
│                                                   │              │
│                           ┌───────────────────────┘              │
│                           ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   TRUST SIGNALS                           │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │ • Identity (MFA, SSO)    • Device Posture (MDM, health)  │   │
│  │ • Location (geo, IP)     • Behavior (anomaly detection)  │   │
│  │ • Time (business hours)  • Risk Score (continuous)       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │               MICRO-SEGMENTED RESOURCES                   │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐     │   │
│  │  │ App A   │  │ App B   │  │ Data    │  │ Service │     │   │
│  │  │ (mTLS)  │  │ (mTLS)  │  │ (Encr.) │  │ (mTLS)  │     │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Identity-First Security

### Identity Proxy Pattern

```csharp
// Identity-aware proxy for zero trust access
// All requests go through identity verification
using System.IdentityModel.Tokens.Jwt;
using System.Net;
using Microsoft.AspNetCore.Http;
using Microsoft.IdentityModel.Tokens;

public enum AccessDecision { Allow, Deny, Challenge }

/// <summary>
/// Context for access decision.
/// </summary>
public sealed record AccessContext(
    string UserId,
    string? DeviceId,
    DevicePosture DevicePosture,
    LocationInfo Location,
    double RiskScore,
    string RequestedResource,
    string RequestedAction);

/// <summary>
/// Zero trust policy decision engine.
/// </summary>
public sealed class PolicyEngine(IEnumerable<IAccessPolicy> policies)
{
    private static readonly HashSet<string> HighRiskCountries = ["XX", "YY", "ZZ"];
    private static readonly string[] OfficeIpRanges = ["10.0.0.0/8", "192.168.1.0/24"];

    public AccessDecision Evaluate(AccessContext context)
    {
        // Check device posture
        if (!CheckDevicePosture(context))
            return AccessDecision.Deny;

        // Check location policy
        if (!CheckLocation(context))
            return AccessDecision.Challenge;

        // Check risk score
        if (context.RiskScore > 0.8)
            return AccessDecision.Deny;
        if (context.RiskScore > 0.5)
            return AccessDecision.Challenge;

        // Check resource-specific policies
        foreach (var policy in policies)
        {
            if (policy.Matches(context))
                return policy.Evaluate(context);
        }

        // Default deny
        return AccessDecision.Deny;
    }

    private static bool CheckDevicePosture(AccessContext context)
    {
        var posture = context.DevicePosture;

        if (!posture.IsManaged) return false;
        if (!posture.DiskEncrypted) return false;
        if (!posture.FirewallEnabled) return false;
        if (string.Compare(posture.OsVersion, "min_required_version", StringComparison.Ordinal) < 0)
            return false;

        return true;
    }

    private static bool CheckLocation(AccessContext context)
    {
        if (HighRiskCountries.Contains(context.Location.Country))
            return false;

        if (!IsOfficeIp(context.Location.IpAddress, OfficeIpRanges))
        {
            if (!context.DevicePosture.VpnConnected)
                return false;
        }

        return true;
    }

    private static bool IsOfficeIp(string? ip, string[] ranges) =>
        ip is not null && ranges.Any(r => IpInRange(ip, r));

    private static bool IpInRange(string ip, string cidr) => true; // Simplified - implement CIDR matching
}

/// <summary>
/// Zero trust middleware - verify every request.
/// </summary>
public sealed class ZeroTrustMiddleware(
    RequestDelegate next,
    PolicyEngine policyEngine,
    IDevicePostureService deviceService,
    ILocationService locationService,
    IRiskScoreService riskService,
    TokenValidationParameters tokenParams)
{
    public async Task InvokeAsync(HttpContext context)
    {
        var authHeader = context.Request.Headers.Authorization.FirstOrDefault();
        if (string.IsNullOrEmpty(authHeader) || !authHeader.StartsWith("Bearer "))
        {
            context.Response.StatusCode = 401;
            await context.Response.WriteAsJsonAsync(new { error = "Authentication required" });
            return;
        }

        var token = authHeader["Bearer ".Length..];

        try
        {
            var handler = new JwtSecurityTokenHandler();
            var principal = handler.ValidateToken(token, tokenParams, out _);
            var userId = principal.FindFirst("sub")?.Value ?? throw new SecurityTokenException("Missing sub claim");

            var accessContext = new AccessContext(
                UserId: userId,
                DeviceId: context.Request.Headers["X-Device-ID"].FirstOrDefault(),
                DevicePosture: await deviceService.GetPostureAsync(context.Request),
                Location: await locationService.GetLocationAsync(context.Request),
                RiskScore: await riskService.CalculateAsync(context.Request, principal),
                RequestedResource: context.Request.Path,
                RequestedAction: context.Request.Method);

            var decision = policyEngine.Evaluate(accessContext);

            switch (decision)
            {
                case AccessDecision.Deny:
                    context.Response.StatusCode = 403;
                    await context.Response.WriteAsJsonAsync(new { error = "Access denied by policy" });
                    return;

                case AccessDecision.Challenge:
                    context.Response.StatusCode = 401;
                    await context.Response.WriteAsJsonAsync(new
                    {
                        error = "step_up_required",
                        methods = new[] { "mfa", "biometric" }
                    });
                    return;

                case AccessDecision.Allow:
                    await next(context);
                    break;
            }
        }
        catch (SecurityTokenException)
        {
            context.Response.StatusCode = 401;
            await context.Response.WriteAsJsonAsync(new { error = "Invalid token" });
        }
    }
}

public interface IAccessPolicy
{
    bool Matches(AccessContext context);
    AccessDecision Evaluate(AccessContext context);
}
```

### Device Trust Verification

```csharp
// Device posture verification for zero trust
using System.Security.Cryptography;
using System.Text;

/// <summary>
/// Device security posture.
/// </summary>
public sealed record DevicePosture
{
    public required string DeviceId { get; init; }
    public required string Platform { get; init; }
    public required string OsVersion { get; init; }
    public required bool IsManaged { get; init; }
    public required bool IsCompliant { get; init; }
    public required bool DiskEncrypted { get; init; }
    public required bool FirewallEnabled { get; init; }
    public required bool AntivirusRunning { get; init; }
    public required bool ScreenLockEnabled { get; init; }
    public required bool VpnConnected { get; init; }
    public required DateTime LastSync { get; init; }
    public required List<string> Certificates { get; init; }
    public required List<string> InstalledAgents { get; init; }
}

/// <summary>
/// Device verification result.
/// </summary>
public sealed record DeviceVerificationResult(bool IsTrusted, List<string> Failures);

/// <summary>
/// Registered device information.
/// </summary>
public sealed record RegisteredDevice(string DeviceId, string UserId, DateTime RegisteredAt, DevicePosture Posture);

/// <summary>
/// Device verification policy configuration.
/// </summary>
public sealed record DevicePolicy
{
    public bool RequireManaged { get; init; }
    public bool RequireCompliant { get; init; }
    public bool RequireEncryption { get; init; }
    public bool RequireFirewall { get; init; }
    public bool RequireAntivirus { get; init; }
    public bool RequireScreenLock { get; init; }
    public Dictionary<string, string> MinOsVersion { get; init; } = new();
    public int MaxSyncAgeHours { get; init; } = 24;
    public List<string> RequiredAgents { get; init; } = [];
}

/// <summary>
/// Verify device meets security requirements.
/// </summary>
public sealed class DeviceVerifier(DevicePolicy policy)
{
    private readonly Dictionary<string, RegisteredDevice> _trustedDevices = new();

    public DeviceVerificationResult VerifyDevice(DevicePosture posture)
    {
        var failures = new List<string>();

        // Check if device is managed (MDM enrolled)
        if (policy.RequireManaged && !posture.IsManaged)
            failures.Add("Device must be MDM managed");

        // Check MDM compliance
        if (policy.RequireCompliant && !posture.IsCompliant)
            failures.Add("Device is not MDM compliant");

        // Check disk encryption
        if (policy.RequireEncryption && !posture.DiskEncrypted)
            failures.Add("Disk encryption required");

        // Check firewall
        if (policy.RequireFirewall && !posture.FirewallEnabled)
            failures.Add("Firewall must be enabled");

        // Check antivirus
        if (policy.RequireAntivirus && !posture.AntivirusRunning)
            failures.Add("Antivirus must be running");

        // Check screen lock
        if (policy.RequireScreenLock && !posture.ScreenLockEnabled)
            failures.Add("Screen lock must be enabled");

        // Check OS version
        if (policy.MinOsVersion.TryGetValue(posture.Platform, out var minOs))
        {
            if (string.Compare(posture.OsVersion, minOs, StringComparison.Ordinal) < 0)
                failures.Add($"OS version {posture.OsVersion} below minimum {minOs}");
        }

        // Check last sync time
        var ageHours = (DateTime.UtcNow - posture.LastSync).TotalHours;
        if (ageHours > policy.MaxSyncAgeHours)
            failures.Add($"Device posture data is {ageHours:F1} hours old");

        // Check required agents
        var requiredAgents = policy.RequiredAgents.ToHashSet();
        var installedAgents = posture.InstalledAgents.ToHashSet();
        var missingAgents = requiredAgents.Except(installedAgents).ToList();
        if (missingAgents.Count > 0)
            failures.Add($"Missing required agents: {string.Join(", ", missingAgents)}");

        return new DeviceVerificationResult(failures.Count == 0, failures);
    }

    public string RegisterDevice(DevicePosture posture, string userId)
    {
        var fingerprint = CalculateFingerprint(posture);
        _trustedDevices[fingerprint] = new RegisteredDevice(
            posture.DeviceId,
            userId,
            DateTime.UtcNow,
            posture);
        return fingerprint;
    }

    private static string CalculateFingerprint(DevicePosture posture)
    {
        var sortedCerts = string.Join(",", posture.Certificates.OrderBy(c => c));
        var content = $"{posture.DeviceId}|{posture.Platform}|{sortedCerts}";
        var hash = SHA256.HashData(Encoding.UTF8.GetBytes(content));
        return Convert.ToHexString(hash)[..32].ToLowerInvariant();
    }
}
```

## Micro-Segmentation

### Network Micro-Segmentation with Service Mesh

```yaml
# Istio Authorization Policy for micro-segmentation
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: frontend-to-api
  namespace: production
spec:
  selector:
    matchLabels:
      app: api
  action: ALLOW
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/production/sa/frontend"]
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/api/v1/*"]
      when:
        - key: request.headers[x-request-id]
          notValues: [""]
---
# Deny all other traffic to API
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: api-deny-all
  namespace: production
spec:
  selector:
    matchLabels:
      app: api
  action: DENY
  rules:
    - from:
        - source:
            notPrincipals: ["cluster.local/ns/production/sa/frontend"]
```

### mTLS Configuration

```yaml
# Istio PeerAuthentication - require mTLS
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT
---
# Istio DestinationRule - enforce mTLS to upstream
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: api-mtls
  namespace: production
spec:
  host: api.production.svc.cluster.local
  trafficPolicy:
    tls:
      mode: ISTIO_MUTUAL
```

## Continuous Verification

### Risk-Based Authentication

```csharp
// Continuous risk-based authentication
// Re-evaluates trust throughout the session
using System.Collections.Concurrent;
using System.Security.Cryptography;

/// <summary>
/// Session risk assessment result.
/// </summary>
public sealed record SessionRisk(
    string SessionId,
    string UserId,
    double CurrentRiskScore,
    Dictionary<string, double> Factors,
    DateTime LastAssessment,
    bool StepUpRequired,
    DateTime? StepUpCompleted);

/// <summary>
/// Risk assessment context.
/// </summary>
public sealed record RiskContext
{
    public required string UserId { get; init; }
    public DateTime? LastMfaTime { get; init; }
    public LocationInfo? Location { get; init; }
    public string? DeviceFingerprint { get; init; }
    public List<RequestInfo> RecentRequests { get; init; } = [];
    public bool AccessingSensitiveResource { get; init; }
}

public sealed record RequestInfo(string Endpoint, bool Unusual);

/// <summary>
/// Continuously verify session trust.
/// </summary>
public sealed class ContinuousVerificationService
{
    private readonly ConcurrentDictionary<string, SessionRisk> _sessions = new();
    private readonly double _riskThreshold = 0.7;
    private readonly double _stepUpThreshold = 0.5;

    public async Task<SessionRisk> AssessRiskAsync(string sessionId, RiskContext context, CancellationToken ct = default)
    {
        var factors = new Dictionary<string, double>();
        var riskScore = 0.0;

        // Factor 1: Time since last MFA (0.0 - 0.2)
        if (context.LastMfaTime.HasValue)
        {
            var hoursSinceMfa = (DateTime.UtcNow - context.LastMfaTime.Value).TotalHours;
            if (hoursSinceMfa > 8)
            {
                factors["mfa_age"] = Math.Min(0.2, hoursSinceMfa * 0.01);
                riskScore += factors["mfa_age"];
            }
        }

        // Factor 2: Location change (0.0 - 0.25)
        if (DetectLocationChange(sessionId, context))
        {
            factors["location_change"] = 0.25;
            riskScore += 0.25;
        }

        // Factor 3: Device change (0.0 - 0.3)
        if (DetectDeviceChange(sessionId, context))
        {
            factors["device_change"] = 0.3;
            riskScore += 0.3;
        }

        // Factor 4: Unusual behavior (0.0 - 0.15)
        var behaviorScore = AnalyzeBehavior(context);
        factors["behavior"] = behaviorScore;
        riskScore += behaviorScore;

        // Factor 5: Sensitive resource access (0.0 - 0.1)
        if (context.AccessingSensitiveResource)
        {
            factors["sensitive_access"] = 0.1;
            riskScore += 0.1;
        }

        var sessionRisk = new SessionRisk(
            SessionId: sessionId,
            UserId: context.UserId,
            CurrentRiskScore: Math.Min(1.0, riskScore),
            Factors: factors,
            LastAssessment: DateTime.UtcNow,
            StepUpRequired: riskScore > _stepUpThreshold,
            StepUpCompleted: null);

        _sessions[sessionId] = sessionRisk;
        return sessionRisk;
    }

    private bool DetectLocationChange(string sessionId, RiskContext context)
    {
        if (!_sessions.TryGetValue(sessionId, out var prevSession))
            return false;

        // Check for impossible travel
        return IsImpossibleTravel(prevSession, context.Location);
    }

    private bool DetectDeviceChange(string sessionId, RiskContext context)
    {
        if (!_sessions.TryGetValue(sessionId, out var prevSession))
            return false;

        // Compare device fingerprints
        return context.DeviceFingerprint != null &&
               prevSession.Factors.ContainsKey("initial_device");
    }

    private static double AnalyzeBehavior(RiskContext context)
    {
        var anomalyScore = 0.0;

        // High request rate
        if (context.RecentRequests.Count > 100)
            anomalyScore += 0.05;

        // Unusual endpoints
        var unusualCount = context.RecentRequests.Count(r => r.Unusual);
        if (unusualCount > 0)
            anomalyScore += unusualCount * 0.02;

        // After hours access
        var hour = DateTime.UtcNow.Hour;
        if (hour < 6 || hour > 22)
            anomalyScore += 0.03;

        return Math.Min(0.15, anomalyScore);
    }

    private static bool IsImpossibleTravel(SessionRisk session, LocationInfo? currentLocation) => false; // Implement
}

/// <summary>
/// Step-up authentication challenge.
/// </summary>
public sealed record StepUpChallenge(string ChallengeId, List<string> RequiredMethods, int ExpiresInSeconds, string UserId);

/// <summary>
/// Handle step-up authentication challenges.
/// </summary>
public sealed class StepUpAuthenticationService
{
    public StepUpChallenge CreateChallenge(string userId, Dictionary<string, double> riskFactors)
    {
        var requiredMethods = new List<string>();

        if (riskFactors.ContainsKey("device_change"))
        {
            requiredMethods.Add("push_notification");
            requiredMethods.Add("email_verification");
        }

        if (riskFactors.ContainsKey("location_change"))
            requiredMethods.Add("sms_code");

        if (riskFactors.ContainsKey("sensitive_access"))
            requiredMethods.Add("biometric");

        // Default to TOTP if no specific requirement
        if (requiredMethods.Count == 0)
            requiredMethods.Add("totp");

        return new StepUpChallenge(
            ChallengeId: GenerateChallengeId(),
            RequiredMethods: requiredMethods,
            ExpiresInSeconds: 300,
            UserId: userId);
    }

    public Task<bool> VerifyAsync(string challengeId, Dictionary<string, string> response, CancellationToken ct = default)
    {
        // Implementation depends on auth methods
        return Task.FromResult(true);
    }

    private static string GenerateChallengeId() =>
        Convert.ToHexString(RandomNumberGenerator.GetBytes(16)).ToLowerInvariant();
}
```

## BeyondCorp Implementation

### Application-Level Access Proxy

```csharp
/// <summary>
/// BeyondCorp-style access proxy.
/// No VPN required - all access through identity-aware proxy.
/// </summary>
public sealed record BeyondCorpConfig(
    string IdentityProvider,
    string ClientId,
    List<IAccessPolicy> AccessPolicies);

public sealed record ProxySession(
    string Id,
    UserInfo User,
    DateTimeOffset ExpiresAt)
{
    public bool IsExpired => DateTimeOffset.UtcNow >= ExpiresAt;
}

public sealed record UserInfo(string Email, List<string> Groups);
public sealed record TargetApplication(string Name, string BackendUrl);

public sealed class BeyondCorpProxyMiddleware(
    RequestDelegate next,
    BeyondCorpConfig config,
    ISessionValidator sessionValidator,
    IDeviceVerifier deviceVerifier,
    IHttpClientFactory httpClientFactory)
{
    private const string SessionCookieName = "_beyondcorp_session";

    public async Task InvokeAsync(HttpContext context)
    {
        // Step 1: Check for valid session
        var session = await GetSessionAsync(context);
        if (session is null)
        {
            RedirectToLogin(context);
            return;
        }

        // Step 2: Verify device trust
        var deviceTrust = await VerifyDeviceAsync(context, session);
        if (!deviceTrust.IsTrusted)
        {
            context.Response.StatusCode = StatusCodes.Status403Forbidden;
            await context.Response.WriteAsJsonAsync(new { error = "Device not trusted", reason = deviceTrust.Reason });
            return;
        }

        // Step 3: Check access policy
        var target = GetTargetApplication(context);
        var accessDecision = await CheckAccessPolicyAsync(session.User, deviceTrust, target, context);
        if (!accessDecision.Allowed)
        {
            context.Response.StatusCode = StatusCodes.Status403Forbidden;
            await context.Response.WriteAsJsonAsync(new { error = accessDecision.Reason });
            return;
        }

        // Step 4: Proxy request to backend
        await ProxyRequestAsync(context, session, target);
    }

    private async Task<ProxySession?> GetSessionAsync(HttpContext context)
    {
        if (!context.Request.Cookies.TryGetValue(SessionCookieName, out var sessionCookie))
            return null;

        var session = await sessionValidator.ValidateAsync(sessionCookie);
        return session is null || session.IsExpired ? null : session;
    }

    private void RedirectToLogin(HttpContext context)
    {
        var parameters = new Dictionary<string, string?>
        {
            ["client_id"] = config.ClientId,
            ["redirect_uri"] = context.Request.GetDisplayUrl(),
            ["response_type"] = "code",
            ["scope"] = "openid profile email",
            ["state"] = GenerateState()
        };

        var queryString = QueryString.Create(parameters);
        var authUrl = $"{config.IdentityProvider}/authorize{queryString}";
        context.Response.Redirect(authUrl);
    }

    private async Task<DeviceTrust> VerifyDeviceAsync(HttpContext context, ProxySession session)
    {
        var clientCert = context.Request.Headers["X-Client-Cert"].FirstOrDefault();
        var deviceId = context.Request.Headers["X-Device-ID"].FirstOrDefault();

        return await deviceVerifier.VerifyAsync(deviceId, clientCert);
    }

    private TargetApplication GetTargetApplication(HttpContext context)
    {
        // Route to backend based on host header or path
        var host = context.Request.Host.Value;
        return new TargetApplication(host, $"https://backend-{host}");
    }

    private async Task<AccessDecision> CheckAccessPolicyAsync(
        UserInfo user, DeviceTrust device, TargetApplication target, HttpContext context)
    {
        var policyContext = new AccessPolicyContext(
            User: user,
            Groups: user.Groups,
            Device: device,
            Target: target,
            Timestamp: DateTimeOffset.UtcNow,
            SourceIp: context.Connection.RemoteIpAddress?.ToString() ?? "unknown",
            RequestPath: context.Request.Path.Value ?? "/",
            RequestMethod: context.Request.Method);

        foreach (var policy in config.AccessPolicies)
        {
            if (policy.Matches(policyContext))
                return policy.Evaluate(policyContext);
        }

        // Default deny
        return new AccessDecision(Allowed: false, Reason: "No matching policy");
    }

    private async Task ProxyRequestAsync(HttpContext context, ProxySession session, TargetApplication target)
    {
        var client = httpClientFactory.CreateClient("BeyondCorpProxy");
        var requestMessage = new HttpRequestMessage
        {
            Method = new HttpMethod(context.Request.Method),
            RequestUri = new Uri($"{target.BackendUrl}{context.Request.Path}{context.Request.QueryString}")
        };

        // Copy headers (excluding hop-by-hop)
        string[] hopByHopHeaders = ["host", "connection", "keep-alive", "transfer-encoding"];
        foreach (var header in context.Request.Headers)
        {
            if (!hopByHopHeaders.Contains(header.Key, StringComparer.OrdinalIgnoreCase))
                requestMessage.Headers.TryAddWithoutValidation(header.Key, header.Value.ToArray());
        }

        // Add identity headers
        requestMessage.Headers.Add("X-Forwarded-User", session.User.Email);
        requestMessage.Headers.Add("X-Forwarded-Groups", string.Join(",", session.User.Groups));
        requestMessage.Headers.Add("X-Request-Id", Guid.NewGuid().ToString("N"));

        // Copy body if present
        if (context.Request.ContentLength > 0)
            requestMessage.Content = new StreamContent(context.Request.Body);

        var response = await client.SendAsync(requestMessage);
        context.Response.StatusCode = (int)response.StatusCode;
        await response.Content.CopyToAsync(context.Response.Body);
    }

    private static string GenerateState() =>
        Convert.ToBase64String(RandomNumberGenerator.GetBytes(32));
}

public sealed record AccessPolicyContext(
    UserInfo User,
    List<string> Groups,
    DeviceTrust Device,
    TargetApplication Target,
    DateTimeOffset Timestamp,
    string SourceIp,
    string RequestPath,
    string RequestMethod);

public interface IAccessPolicy
{
    bool Matches(AccessPolicyContext context);
    AccessDecision Evaluate(AccessPolicyContext context);
}

public interface ISessionValidator
{
    Task<ProxySession?> ValidateAsync(string sessionCookie, CancellationToken ct = default);
}
```

## Quick Decision Tree

**What are you implementing?**

1. **Network redesign for zero trust** -> Start with micro-segmentation + identity proxy
2. **Service-to-service auth** -> Implement mTLS with service mesh
3. **User access to applications** -> BeyondCorp-style access proxy
4. **Device trust verification** -> MDM integration + device posture checks
5. **Continuous session security** -> Risk-based authentication + step-up
6. **API security** -> Token validation + context-aware policies

## Zero Trust Checklist

### Identity and Access

- [ ] All users authenticated via strong MFA
- [ ] Device identity verified (certificates/MDM)
- [ ] Just-in-time access provisioning
- [ ] Least privilege access model
- [ ] Session timeout and re-authentication
- [ ] Privileged access management (PAM)

### Network and Workloads

- [ ] No implicit trust for internal network
- [ ] Micro-segmentation implemented
- [ ] mTLS for all service communication
- [ ] Network policies default deny
- [ ] East-west traffic encrypted
- [ ] Egress traffic controlled

### Data Protection

- [ ] Data encrypted at rest and in transit
- [ ] Data classification and labeling
- [ ] DLP policies enforced
- [ ] Access logged and audited
- [ ] Sensitive data identified

### Monitoring and Analytics

- [ ] All access attempts logged
- [ ] Behavioral analytics active
- [ ] Anomaly detection configured
- [ ] SIEM integration
- [ ] Automated response playbooks

## References

- **Zero Trust Architecture**: See `references/zero-trust-architecture.md` for detailed patterns
- **ZTNA Implementation**: See `references/ztna-implementation.md` for network access

---

**Last Updated:** 2025-12-26

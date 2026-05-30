---
name: recon-osint
description: Comprehensive reconnaissance and OSINT — subdomain enumeration, CVE lookup, breach intelligence, DNS history, social profiling, attack surface mapping
metadata:
  type: offensive
  phase: reconnaissance
  tools: nmap, amass, subfinder, theHarvester, h8mail, searchsploit, shodan, censys, nuclei, waybackurls, httpx, katana
kill_chain:
  phase: [recon]
  step: [1]
  attck_tactics: [TA0043]
depends_on: []
feeds_into: [vulnerability-analysis, web-pentest, network-attack, exploit-development, cloud-security, mobile-pentest]
inputs: [scope_definition, target_list]
outputs: [attack_surface_map, subdomain_list, technology_fingerprint, cve_list]
---

# Reconnaissance & OSINT

## When to Activate

- New target engagement begins — need full attack surface mapping
- Gathering intelligence before exploitation phase
- Building target profile for social engineering
- Identifying exposed services, leaked credentials, historical infrastructure

## Methodology

### Phase 1: Passive Reconnaissance

#### Domain & Subdomain Enumeration
```bash
# Subdomain discovery (passive)
subfinder -d $DOMAIN -all -o subs_passive.txt
amass enum -passive -d $DOMAIN -o subs_amass.txt
cat subs_*.txt | sort -u > all_subdomains.txt

# Certificate transparency
curl -s "https://crt.sh/?q=%25.$DOMAIN&output=json" | jq -r '.[].name_value' | sort -u >> all_subdomains.txt

# Wayback Machine URL discovery
waybackurls $DOMAIN | sort -u > wayback_urls.txt
cat wayback_urls.txt | grep -E '\.(js|json|xml|config|env|bak|sql)' > interesting_urls.txt

# DNS records
for type in A AAAA MX NS TXT SOA CNAME SRV; do
  dig +short $type $DOMAIN
done | tee dns_records.txt

# WHOIS
whois $DOMAIN | tee whois.txt
```

#### Technology Fingerprinting
```bash
# HTTP probing live subdomains
cat all_subdomains.txt | httpx -sc -cl -title -tech-detect -o httpx_results.txt

# Web crawling for endpoints
katana -u https://$DOMAIN -d 3 -jc -o crawl_results.txt

# Wappalyzer-style detection
whatweb https://$DOMAIN
```

#### CVE & Exploit Intelligence
```bash
# For each identified component+version:
searchsploit "$COMPONENT $VERSION"
searchsploit -j "$COMPONENT $VERSION" | jq '.RESULTS_EXPLOIT[]'

# NVD API
curl -s "https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=$COMPONENT+$VERSION&resultsPerPage=10" \
  | jq '.vulnerabilities[].cve | {id, descriptions: .descriptions[0].value}'

# GitHub PoC search
curl -s "https://api.github.com/search/repositories?q=CVE+$COMPONENT+poc&sort=updated&per_page=5" \
  | jq '.items[] | {name, html_url, description}'

# Nuclei template scan
nuclei -u https://$DOMAIN -t cves/ -severity critical,high -o nuclei_cves.txt
```

### Phase 2: Active Reconnaissance

#### Port & Service Discovery
```bash
# Fast port discovery
nmap -sS -T4 -p- --min-rate 5000 $TARGET -oG ports_only.txt
PORTS=$(grep -oP '\d+/open' ports_only.txt | cut -d/ -f1 | tr '\n' ',' | sed 's/,$//')

# Deep service scan on discovered ports
nmap -sV -sC -p "$PORTS" $TARGET -oA nmap_targeted

# UDP top ports
nmap -sU --top-ports 50 -T4 $TARGET -oN nmap_udp.txt

# Script scanning
nmap --script=vuln -p $PORTS $TARGET -oN nmap_vuln.txt
```

#### Web Application Mapping
```bash
# Directory fuzzing
feroxbuster -u https://$DOMAIN -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -o dirs.txt
ffuf -u https://$DOMAIN/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt -mc 200,301,302,403 -o ffuf_results.json

# API endpoint discovery
ffuf -u https://$DOMAIN/api/FUZZ -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt -mc 200,401,403
```

### Phase 3: Credential & Breach Intelligence

```bash
# Email harvesting
theHarvester -d $DOMAIN -b all -f harvester_results.json

# Breach lookup
h8mail -t $EMAIL -o breach_results.csv

# HIBP API (requires key)
curl -s -H "hibp-api-key: $HIBP_API_KEY" \
  "https://haveibeenpwned.com/api/v3/breachedaccount/$EMAIL?truncateResponse=false" | jq '.'

# Password pattern analysis from breaches
# Common patterns: Company2024!, Season+Year, Keyboard walks
```

### Phase 4: Infrastructure & Cloud Recon

```bash
# Shodan
shodan search "hostname:$DOMAIN" --fields ip_str,port,org,product,version
shodan host $IP

# Cloud asset discovery
# AWS S3 buckets
aws s3 ls s3://$DOMAIN --no-sign-request 2>/dev/null
# Azure blob
curl -s "https://$DOMAIN.blob.core.windows.net/\$web?restype=container&comp=list"
# GCP buckets
curl -s "https://storage.googleapis.com/$DOMAIN"

# GitHub dorking
# "company.com" password OR secret OR token OR api_key
# org:company filename:.env
```

## Output Format

Produce structured intel report:
```
## Target: $DOMAIN
### Attack Surface
- Subdomains: [count] discovered
- Open ports: [list with services]
- Technologies: [stack details]
### Vulnerabilities
- CVEs: [relevant CVEs with exploitability]
- Misconfigurations: [findings]
### Credentials
- Breached accounts: [count]
- Leaked secrets: [if any]
### Recommendations
- Priority targets for exploitation
- Attack vectors ranked by likelihood of success
```

## Advanced: Deep OSINT Techniques

### Social Engineering Reconnaissance
```bash
# LinkedIn intelligence gathering:
# - Employee names, roles, reporting structure
# - Technology stack from job postings
# - Recent hires (likely less security-aware)
# - Departures (accounts may still be active)

# Tools:
# linkedin2username — generate username lists from LinkedIn
python3 linkedin2username.py -c "Company Name" -n 100
# Output: first.last, flast, firstl format usernames

# Email format discovery:
# 1. Check hunter.io for known format
# 2. Verify with SMTP VRFY/RCPT TO
# 3. Or: check email headers from public mailing lists

# Social media OSINT:
# - Twitter/X: employee complaints, tech stack mentions
# - GitHub: personal repos with company code/secrets
# - Stack Overflow: questions revealing internal architecture
# - Glassdoor: internal tool names, processes
```

### GitHub/GitLab Dorking
```bash
# Secret discovery in repositories:
# Tools: trufflehog, gitleaks, git-secrets

trufflehog github --org=target-company --only-verified
gitleaks detect --source=. --report-format=json --report-path=leaks.json

# Manual GitHub dorks:
# org:company "password" OR "secret" OR "api_key"
# org:company filename:.env
# org:company filename:id_rsa
# org:company "BEGIN RSA PRIVATE KEY"
# org:company "AKIA" (AWS access key prefix)
# org:company "jdbc:" OR "mongodb://" OR "redis://"
# org:company filename:docker-compose.yml
# org:company filename:terraform.tfvars

# Historical secrets (deleted but in git history):
git log --all --full-history -- "*.env"
git log --all -p -- "*secret*" "*password*" "*token*"
# Or: trufflehog git file://./repo --since-commit=HEAD~1000
```

### DNS Intelligence
```bash
# DNS history (find old IPs, previous hosting):
# SecurityTrails, ViewDNS.info, DNSdumpster

# Subdomain takeover detection:
# Find CNAME pointing to deprovisioned service
subjack -w subdomains.txt -t 100 -timeout 30 -o takeovers.txt
# Or: nuclei -l subdomains.txt -t takeovers/

# Common takeover targets:
# - CNAME → *.s3.amazonaws.com (NoSuchBucket)
# - CNAME → *.herokuapp.com (No such app)
# - CNAME → *.azurewebsites.net (not found)
# - CNAME → *.github.io (404)
# - CNAME → *.shopify.com (not connected)

# DNS zone walking (NSEC/NSEC3):
ldns-walk @ns1.target.com target.com
# Or: dnsrecon -d target.com -t zonewalk

# Reverse DNS for IP ranges:
# Find all domains hosted on target's IP range
for ip in $(seq 1 254); do
  host 10.10.10.$ip | grep "domain name pointer"
done
```

### Cloud Asset Discovery
```bash
# AWS account enumeration:
# If you have any AWS credential, enumerate the account
aws sts get-caller-identity
aws organizations list-accounts 2>/dev/null

# S3 bucket enumeration (permutations):
# company, company-dev, company-staging, company-backup, company-logs
for prefix in "" "-dev" "-staging" "-prod" "-backup" "-logs" "-data"; do
  aws s3 ls s3://${COMPANY}${prefix} --no-sign-request 2>/dev/null && \
    echo "[+] Found: ${COMPANY}${prefix}"
done

# Azure tenant enumeration:
# Check if tenant exists
curl -s "https://login.microsoftonline.com/$DOMAIN/.well-known/openid-configuration" | jq .token_endpoint
# Enumerate users (if allowed):
# o365creeper, TeamFiltration

# GCP project discovery:
# Check for open Firebase databases
curl -s "https://$PROJECT.firebaseio.com/.json"
# Check for open GCS buckets
curl -s "https://storage.googleapis.com/$COMPANY"
```

### Attack Surface Monitoring
```bash
# Continuous monitoring for new assets:
# Run subdomain enumeration on schedule
# Compare results against previous scan
# Alert on: new subdomains, new open ports, new technologies

# Automated pipeline:
subfinder -d $DOMAIN -silent | sort > current_subs.txt
comm -13 previous_subs.txt current_subs.txt > new_subs.txt
# Probe new subdomains immediately
cat new_subs.txt | httpx -silent -sc -title | tee new_assets.txt

# Certificate transparency monitoring:
# certstream — real-time CT log monitoring
# Alert when new cert issued for target domain
python3 -c "
import certstream
def callback(message, context):
    if message['message_type'] == 'certificate_update':
        domains = message['data']['leaf_cert']['all_domains']
        for d in domains:
            if '$DOMAIN' in d:
                print(f'[NEW CERT] {d}')
certstream.listen_for_events(callback)
"
```

## Advanced: Network Reconnaissance

### Internal Network Mapping
```bash
# After initial access — map internal network:

# ARP scan (local subnet)
arp-scan -l
nmap -sn 10.0.0.0/24

# Service discovery across subnets
nmap -sS -T4 -p 21,22,23,25,53,80,88,110,135,139,143,389,443,445,636,993,995,1433,1521,3306,3389,5432,5985,8080,8443 10.0.0.0/16 -oG internal_scan.txt

# Identify domain controllers
nmap -p 88,389,636 10.0.0.0/24 --open
# Or: nslookup -type=SRV _ldap._tcp.dc._msdcs.$DOMAIN

# Identify network segmentation
# Trace routes to different subnets
# Identify firewalls/ACLs between segments
for subnet in 10.0.1.0 10.0.2.0 10.0.3.0; do
  traceroute -n $subnet.1 2>/dev/null | tail -1
done

# SNMP enumeration (if community strings found)
snmpwalk -v2c -c public $TARGET 1.3.6.1.2.1.1  # System info
snmpwalk -v2c -c public $TARGET 1.3.6.1.2.1.4.20  # IP addresses
onesixtyone -c /usr/share/seclists/Discovery/SNMP/common-snmp-community-strings.txt $SUBNET/24
```

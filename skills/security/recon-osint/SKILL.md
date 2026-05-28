---
name: recon-osint
description: Comprehensive reconnaissance and OSINT — subdomain enumeration, CVE lookup, breach intelligence, DNS history, social profiling, attack surface mapping
metadata:
  type: offensive
  phase: reconnaissance
  tools: nmap, amass, subfinder, theHarvester, h8mail, searchsploit, shodan, censys, nuclei, waybackurls, httpx, katana
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

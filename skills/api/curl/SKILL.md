---
name: curl
description: HTTP client examples including download, POST, auth, JSON, headers, proxy, and FTP operations.
---

# curl — Handy Examples

**Download Files**

```bash
# Download a file and save with original filename
curl -O http://example.com/file.txt

# Download a file with specific name
curl -o filename.ext http://example.com/file.txt

# Download and limit speed
curl --limit-rate 100K -O http://example.com/largefile.zip

# Resume interrupted download
curl -C - -O http://example.com/largefile.zip

# Download multiple files
curl -O http://example.com/file1.txt -O http://example.com/file2.txt

# Download all sequentially numbered files (1-24)
curl http://example.com/pic[1-24].jpg
```

**HTTP Methods & Data**

```bash
# POST data
curl -d "name=value" http://example.com/resource

# POST JSON data
curl -H "Content-Type: application/json" -d '{"key":"value"}' http://example.com/resource

# Send URL-encoded data
curl --data-urlencode "key=value" http://example.com/resource

# Custom HTTP method
curl -X PUT http://example.com/resource
curl -X DELETE http://example.com/resource
```

**Headers & Authentication**

```bash
# Include headers in output
curl -i http://example.com

# Show only HTTP headers
curl -I http://example.com

# Custom header
curl -H "Custom-Header: Value" http://example.com

# Basic authentication
curl -u username:password http://example.com

# Save response headers to file
curl -D headers.txt http://example.com
```

**Proxy & Advanced**

```bash
# Use proxy
curl -x http://proxy-server:port http://example.com

# Get HTTP status code only
curl -o /dev/null -w '%{http_code}\n' -s -I URL

# Get external IP as JSON
curl http://ifconfig.me/all.json

# Follow redirects
curl -L http://example.com

# Download and pipe to grep
curl http://example.com/file.txt | grep "search-string"
```

**FTP Operations**

```bash
# Upload file via FTP
curl -T localfile.txt ftp://ftp.example.com/upload/

# Download via FTP with auth
curl -u username:password -O ftp://example.com/pub/file.zip

# List FTP directory
curl ftp://username:password@example.com
```

**Original Examples**

```bash
curl --resolve example.com:443:127.0.0.1 https://example.com
curl --output example.html "https://example.com/"
curl --header "PRIVATE-TOKEN: ?" https://example.com/
curl --basic --user 'test:test' https://example.com/
curl -fsSL https://example.com/install.sh | sh
curl --ftp-ssl --user "test:test" -l sftp://example.com:22/ --key ./id_rsa --pubkey ./id_rsa.pub
curl --request POST --data "A=B&C=D" https://example.com
curl --request POST --form "A=B" --form "C=D" https://example.com
curl --upload-file test.txt https://example.com
curl --ftp-ssl --user test:test -l ftp://example.com:21
```
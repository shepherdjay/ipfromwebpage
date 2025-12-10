## ipfromwebpage

[![PyPi](https://img.shields.io/pypi/v/ipfromwebpage.svg)](https://pypi.python.org/pypi/ipfromwebpage)
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/shepherdjay/ipfromwebpage/tree/master.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/shepherdjay/ipfromwebpage/tree/master)
[![codecov](https://codecov.io/gh/shepherdjay/ipfromwebpage/branch/master/graph/badge.svg)](https://codecov.io/gh/shepherdjay/ipfromwebpage)

### Summary:
Takes a webpage or text string and extracts IPv4 and IPv6 addresses. Then prints the IPs (aggregated where possible).

#### Quickstart:

Install using `pip install ipfromwebpage`

**Usage Options:**
1. Extract IPs from a URL: `ipfromwebpage <url>` where `<url>` is the fully qualified URL you wish to scrape for IPs.
2. Extract IPs from text: `ipfromwebpage --input-string "<text>"` where `<text>` is any plain text containing IP addresses (e.g., copy-pasted from a website).
3. Include reserved IPs: Add `--no-exclusions` flag to include addresses in reserved ranges (0.0.0.0/8, 224.0.0.0/3) that are normally filtered out.

#### Code Examples:

**Example 1: Scraping from a URL**
```
ipfromwebpage https://www.cloudflare.com/ips
================
IPv4 addresses:
103.21.244.0/22
103.22.200.0/22
103.31.4.0/22
104.16.0.0/12
108.162.192.0/18
131.0.72.0/22
141.101.64.0/18
162.158.0.0/15
172.64.0.0/13
173.245.48.0/20
188.114.96.0/20
190.93.240.0/20
197.234.240.0/22
198.41.128.0/17
================
IPv6 addresses:
2400:cb00::/32
2405:8100::/32
2405:b500::/32
2606:4700::/32
2803:f800::/32
2a06:98c0::/29
2c0f:f248::/32
```

**Example 2: Extracting from text string (e.g., copy-pasted content)**
```
ipfromwebpage --input-string "Server IPs: 10.0.0.1, 192.168.1.1
Network range: 172.16.0.0/24
IPv6: 2001:db8::1"
================
IPv4 addresses:
10.0.0.1
172.16.0.0/24
192.168.1.1
================
IPv6 addresses:
2001:db8::1
```

**Example 3: Including reserved/multicast IPs (e.g., from terraform output)**
```
ipfromwebpage --input-string "242.143.224.100/32, 242.143.224.101/32" --no-exclusions
================
IPv4 addresses:
242.143.224.100/31
================
IPv6 addresses:
No addresses found when scraping input string
```

Note: By default, addresses in the ranges 0.0.0.0/8 and 224.0.0.0/3 are excluded as they are typically reserved or multicast addresses. Use `--no-exclusions` to include them.

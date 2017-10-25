## ipfromwebpage

[![PyPi](https://img.shields.io/pypi/v/ipfromwebpage.svg)](https://pypi.python.org/pypi/ipfromwebpage)
[![Build Status](https://travis-ci.org/shepherdjay/ipfromwebpage.svg?branch=master)](https://travis-ci.org/shepherdjay/ipfromwebpage)
[![codecov](https://codecov.io/gh/shepherdjay/ipfromwebpage/branch/master/graph/badge.svg)](https://codecov.io/gh/shepherdjay/ipfromwebpage)

### Summary:
Takes a webpage and scrapes for IPv4 Addresses. Then prints the IPs aggregated where possible.

#### Quickstart:

Install using `pip install ipfromwebpage`

Run the code as `ipfromwebpage <url>` where `<url>` is the fully qualified URL you wish to scrap for IPs.

#### Code Example:
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

[![Build Status](https://travis-ci.org/Nuttycomputer/ip-from-webpage.svg?branch=master)](https://travis-ci.org/Nuttycomputer/ip-from-webpage) [![Coverage Status](https://coveralls.io/repos/github/Nuttycomputer/ip-from-webpage/badge.svg?branch=master)](https://coveralls.io/github/Nuttycomputer/ip-from-webpage?branch=master)

##ip-from-webpage
[![Build Status](https://travis-ci.org/Nuttycomputer/ip-from-webpage.svg?branch=master)](https://travis-ci.org/Nuttycomputer/ip-from-webpage) [![codecov](https://codecov.io/gh/Nuttycomputer/ip-from-webpage/branch/master/graph/badge.svg)](https://codecov.io/gh/Nuttycomputer/ip-from-webpage)


###Summary:
Takes a webpage and scrapes for IPv4 Addresses. Then prints the IPs aggregated where possible.

####Quickstart:

Install requirements in requirements.txt.

Run the code as `ipfromwebpage <url>` where `<url>` is the fully qualified URL you wish to scrap for IPs.

####Code Example:
```
ipfromwebpage.py https://www.cloudflare.com/ips
103.21.244.0/22
103.22.200.0/22
103.31.4.0/22
104.16.0.0/12
108.162.192.0/18
141.101.64.0/18
162.158.0.0/15
172.64.0.0/13
173.245.48.0/20
188.114.96.0/20
190.93.240.0/20
197.234.240.0/22
198.41.128.0/17
199.27.128.0/21
```

####Requirements:
See requirements.txt

####Contributors:
- Dharma Bellamkonda (dharmab)

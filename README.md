# Cloudflare DNS Updater
This script uses the cloudflare API to update your A record for your domains. This is specifically for those who self-host that don't have a static IP address from their ISP.

## Requirements
- Python 2.x or later

## Getting Started
Open the `cloudflare.py` file with a text editor and change the following variables:

```python
CLOUDFLARE_EMAIL = "" # The email address you use to loginto Cloudflare's website
CLOUDFLARE_API_KEY = "" # The Global API Key found under My Profile on Cloudflare's website'
```

## Ignoring Domains
You may not want to update the IP on all your domains. Use the following array to blacklist the domains you don't want updated.

```python
ignore = []
```

## CRON Job
Most linux based systems use crontab to schedule cron jobs. The following entry will run the script every 5 minutes. Feel free to change it to suit your needs.

```
*/5 * * * * python /usr/local/bin/cloudflare.py
```

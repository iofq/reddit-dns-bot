# reddit-dns-bot
A simple reddit bot that listens for private messages in the form of a DNS query and replies with a lookup. Bundled with [unbound dns server](https://wiki.archlinux.org/index.php/unbound) for resolving from root nameservers.

# Running
Distributed as a docker container, running this bot is dead simple. You'll need a [reddit api token](https://www.reddit.com/prefs/apps/). 

```bash
docker run --rm -it --name dns-bot \
	--dns=127.0.0.1 \
  -e CLIENT_ID="............" \
  -e CLIENT_SECRET="xxxxxxxx" \
  -e CLIENT_USER="user" \
  -e CLIENT_PASS="password" \
  -e USER_AGENT="unique user agent v1.0" \
	iofq/reddit-dns-bot
```

# Usage
This bot will respond to queries in the form `A google.com`, `google.com A`, or `google.com`. Anything else will not receive a response. It currently supports A, AAAA, CNAME, MX, SRV, and TXT records, although it can easily be extended to lookup any record type [dig](https://linux.die.net/man/1/dig) supports. Users should submit their query in a message body, not subject. 

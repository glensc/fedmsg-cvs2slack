# FedMsg CVS to Slack Consumer

This plugin consumes messages by [FedMsg CVS Publisher](https://github.com/glensc/fedmsg-cvs)
and posts then to Slack chat.

## Development

```
# obtain 0.18.3 version of fedmsg
git clone -b 0.18.3 https://github.com/fedora-infra/fedmsg

# setup pristine fedmsg.d for development
cp -a fedmsg/fedmsg.d .

# Copy the cvs_consumer_config.py into ./fedmsg.d/ directory.
# For production copy to /etc/fedmsg.d directory.
cp cvs2slack_consumer_config.py fedmsg.d

# Setup your consumer by running
python setup.py develop

# Start the fedmsg-hub (which should pick up your consumer) with:
fedmsg-hub
```

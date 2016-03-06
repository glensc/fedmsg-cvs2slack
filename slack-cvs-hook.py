#!/usr/bin/python
# https://github.com/satoshi03/slack-python-webhook

import sys
import subprocess
from pprint import pprint
import slackweb

# Get token from https://my.slack.com/services/new/incoming-webhook/
HOOK_URL = 'https://hooks.slack.com/services/T.../B.../...'
# URL to CVSWEB
CVSWEB_URL = "https://cvs.example.net"
# #channel or @nick to post to
CHANNEL = "@glen"
# Username to show in webook
USERNAME = "CVS Commit"

user, module = sys.argv[1:2]
files = sys.argv[2:]

pprint(user)
pprint(module)
pprint(files)

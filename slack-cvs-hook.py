#!/usr/bin/python
# Requires:
# slackweb Python module from PyPI:
# https://github.com/satoshi03/slack-python-webhook
#
# Setup:
# Put to CVSROOT/loginfo:
# ALL $CVSROOT/CVSROOT/slack-cvs-hook $USER %p %{sVv}

import sys
import subprocess
import slackweb

# Get token from https://my.slack.com/services/new/incoming-webhook/
HOOK_URL = 'https://hooks.slack.com/services/T.../B.../...'
# URL to CVSWEB
CVSWEB_URL = "https://cvs.example.net"
# #channel or @nick to post to
CHANNEL = "@glen"
# Username to show in webook
USERNAME = "CVS Commit"

from pprint import pprint

user, module = sys.argv[1:3]
files = sys.argv[3:]

pprint(user)
pprint(module)
pprint(files)

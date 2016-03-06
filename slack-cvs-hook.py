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
from itertools import izip
import slackweb

# Get token from https://my.slack.com/services/new/incoming-webhook/
HOOK_URL = 'https://hooks.slack.com/services/T.../B.../...'
# URL to CVSWEB
CVSWEB_URL = "https://cvs.example.net"
# #channel or @nick to post to
CHANNEL = "@glen"
# Username to show in webook
USERNAME = "CVS Commit"

# http://stackoverflow.com/a/5389547
def grouped(iterable, n):
    "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
    return izip(*[iter(iterable)]*n)

"""
Commit message is multiline with preformatted by CVS client.
Read up STDIN up to: 'Log Message:\n',

Example:
['Update of /usr/local/cvs/test/slack\n',
 'In directory localhost:/home/glen/scm/cvs/test-CVSROOT/testdir/slack\n',
 '\n',
 'Modified Files:\n',
 '\tslack.txt slack2.txt \n',
 'Log Message:\n',
 '- slack\n',
 '\n']
"""
def get_commit_message():
    lines = sys.stdin.readlines()

    for i in range(len(lines)):
        if lines[i] == "Log Message:\n":
            break

    return "".join(lines[i + 1:]).strip()

from pprint import pprint

user, module = sys.argv[1:3]
files = sys.argv[3:]
commit_msg = get_commit_message()

pprint(user)
pprint(module)
pprint(files)
pprint(commit_msg)

for filename, oldrev, newrev in grouped(files, 3):
   print "%s : %s->%s" % (filename, oldrev, newrev)

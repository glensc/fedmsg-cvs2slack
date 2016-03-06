#!/usr/bin/python
# coding: utf-8
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

# viewvc specific
CO_URL = '%(url)s/%(module)s/%(file)s?rev=%(rev)s&content-type=text/x-cvsweb-markup'
DIFF_URL = '%(url)s/%(module)s/%(file)s?r1=%(r1)s&r2=%(r2)s&f=h'
LOG_URL = '%(url)s/%(module)s/%(file)s?r1=%(rev)s#rev%(rev)s'

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

def cut(s, maxlen = 24):
    if len(s) > maxlen:
        return s[0:maxlen] + "..."
    return s

user, module = sys.argv[1:3]
files = sys.argv[3:]
commit_msg = get_commit_message()

summary = "Commit in %s by %s: %s" % (module, user, cut(commit_msg))
text = ""

defopts = { 'url': CVSWEB_URL, 'module': module }
for filename, oldrev, newrev in grouped(files, 3):
    opts = defopts
    opts['file'] = filename

    opts['rev'] = newrev
    log_url = LOG_URL % opts

    opts['rev'] = oldrev
    r1_url = CO_URL % opts

    opts['rev'] = newrev
    r2_url = CO_URL % opts

    opts['r1'] = oldrev
    opts['r2'] = newrev
    diff_url = DIFF_URL % opts

    text += "<%s|%s>: <%s|r%s> <%s|→> <%s|r%s>\n" % (log_url, filename, r1_url, oldrev, diff_url, r2_url, newrev)

attachments = [{
    "fallback": text,
    "text": text,
    "color": "good",
}]

slack = slackweb.Slack(url=HOOK_URL)
slack.notify(text=summary, attachments=attachments, channel=CHANNEL, username=USERNAME)

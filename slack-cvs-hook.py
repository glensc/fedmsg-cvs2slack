#!/usr/bin/python
# coding: utf-8
# Requires:
# slackweb Python module from PyPI:
# https://github.com/satoshi03/slack-python-webhook
#
# Setup:
# Put to CVSROOT/loginfo:
# ALL $CVSROOT/CVSROOT/slack-cvs-hook /path/to/config.conf $USER %p %{sVv}

import sys
import subprocess
from itertools import izip
import slackweb

def parse_config(filename):
    """Parse configuration file.

    Args:
      filename: Path to the configuration file to parse.
    Returns:
      Dictionary of values defined in the file.
    """
    with open(filename) as f:
        data = f.read()
        compiled = compile(data, filename, "exec")
        result = { 'main': sys.modules[__name__] }
        eval(compiled, result)
        return result

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

    return lines[i + 1:]

def get_commit_summary():
    lines = get_commit_message()
    return lines[0].strip()

def cut(s, maxlen = 24):
    if len(s) > maxlen:
        return s[0:maxlen] + "..."
    return s

user, module = sys.argv[2:4]
files = sys.argv[4:]
commit_msg = get_commit_summary()
c = parse_config(sys.argv[1])

module_url = "%s/%s/" % (c['CVSWEB_URL'], module)
summary = "in *<%s|%s>* by *%s*: %s" % (module_url, module, user, commit_msg)
text = ""

defopts = { 'url': c['CVSWEB_URL'], 'module': module }
for filename, oldrev, newrev in grouped(files, 3):
    opts = defopts.copy()
    opts['file'] = filename

    opts['rev'] = newrev
    log_url = c['LOG_URL'] % opts

    opts['rev'] = oldrev
    r1_url = c['CO_URL'] % opts

    opts['rev'] = newrev
    r2_url = c['CO_URL'] % opts

    opts['r1'] = oldrev
    opts['r2'] = newrev
    diff_url = c['DIFF_URL'] % opts

    text += "<%s|%s>: <%s|r%s> <%s|→> <%s|r%s>\n" % (log_url, filename, r1_url, oldrev, diff_url, r2_url, newrev)

attachments = [{
    "fallback": text,
    "text": text,
    "color": "good",
}]

slack = slackweb.Slack(url=c['HOOK_URL'])
slack.notify(text=summary, attachments=attachments, channel=c['CHANNEL'], username=c['USERNAME'])

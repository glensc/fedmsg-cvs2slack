#!/usr/bin/python
# coding: utf-8

def transform(msg):
    """
    process fedmsg msg into slack message
    """

    # process each file in same commitid
    # TODO: group by same directory

    summary = "by *%s*: %s" % (msg['user'], msg['message'])
    text = ""
    for f in msg['files']:
        u = f['urls']
        text += u"<%s|%s>: <%s|r%s> <%s|→> <%s|r%s>\n" % (u['log_url'], f['filename'], u['old_url'], f['old_rev'], u['diff_url'], u['new_url'], f['new_rev'])

    attachments = [{
        "fallback": text,
        "text": text,
        "color": "good",
    }]

    return { 'text' : summary, 'attachments' : attachments}

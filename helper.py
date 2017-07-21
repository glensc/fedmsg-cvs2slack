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
    fallback = ""
    for f in msg['files']:
        u = f['urls']
        text += u"<%s|%s>: <%s|r%s> <%s|→> <%s|r%s>\n" % (u['log_url'], f['filename'], u['old_url'], f['old_rev'], u['diff_url'], u['new_url'], f['new_rev'])
        fallback += u"%s r%s → r%s\n" % (f['filename'], f['old_rev'], f['new_rev'])

    attachments = [{
        "fallback": fallback,
        "text": text,
        "color": "good",
    }]

    return { 'text' : summary, 'attachments' : attachments}

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
        # create dict of properties and urls
        d = dict(f, **f['urls'])

        text += u"<%(log_url)s|%(filename)s>: <%(old_url)s|r%(old_rev)s> <%(diff_url)s|→> <%(new_url)s|r%(new_rev)s>\n" % d
        fallback += u"%(filename)s r%(old_rev)s → r%(new_rev)s\n" % d

    attachments = [{
        "fallback": fallback,
        "text": text,
        "color": "good",
    }]

    return { 'text' : summary, 'attachments' : attachments}

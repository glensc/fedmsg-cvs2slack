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

        # diff
        if f['old_rev'] and f['new_rev']:
            text += u"<%(log_url)s|%(filename)s>: <%(old_url)s|r%(old_rev)s> <%(diff_url)s|→> <%(new_url)s|r%(new_rev)s>\n" % d
            fallback += u"%(filename)s r%(old_rev)s → r%(new_rev)s\n" % d
        # removed
        elif f['old_rev']:
            text += u"<%(old_url)s|%(filename)s>: <%(old_url)s|r%(old_rev)s> (removed)\n" % d
            fallback += u"%(filename)s r%(old_rev)s (removed)\n" % d
        # added
        elif f['new_rev']:
            text += u"<%(new_url)s|%(filename)s>: <%(new_url)s|r%(new_rev)s> (added)\n" % d
            fallback += u"%(filename)s r%(new_rev)s (added)\n" % d

    attachments = [{
        "fallback": fallback,
        "text": text,
        "color": "good",
    }]

    return { 'text' : summary, 'attachments' : attachments}

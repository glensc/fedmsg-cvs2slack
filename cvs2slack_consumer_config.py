"""

This is a config file that must appear in ./fedmsg.d/ alongside the other
config files from the fedmsg development checkout.

In production, this should go into /etc/fedmsg.d/ but for development it can
just live in your cwd/pwd.

"""

config = {
    # whether the consumer is enabled
    'cvs2slack.consumer.enabled': False,

    # Get token from https://my.slack.com/services/new/incoming-webhook/
    'cvs2slack.hook_url': 'https://hooks.slack.com/services/T.../B.../...',

    # A #channel or @nick to post to
    'cvs2slack.channel': '@glen',

    # Username to show in webhook
    'cvs2slack.username': 'CVS Commit',
}

"""

Consumer to show how to write a service that does stuff in
response to message on the `fedmsg bus <http://fedmsg.rtfd.org>`_.
"""

import fedmsg.consumers
import slackweb

class CVS2SlackConsumer(fedmsg.consumers.FedmsgConsumer):
    # cvs2slack.consumer.enabled must be set to True in the config in fedmsg.d/ for
    # this consumer to be picked up and run when the fedmsg-hub starts.
    config_key = "cvs2slack.consumer.enabled"

    def __init__(self, hub):
        # I'm only interested in messages from CVS
        self.topic = self.abs_topic(hub.config, "cvs.commit")

        super(CVS2SlackConsumer, self).__init__(hub)

        self.channel = hub.config['cvs2slack.channel']
        self.username = hub.config['cvs2slack.username']

        self.slack = slackweb.Slack(url=hub.config['cvs2slack.hook_url'])

    # no proper way to configure just topic suffix
    # https://github.com/fedora-infra/fedmsg/pull/428
    def abs_topic(self, config, topic):
        """
        prefix topic with topic_prefix and environment config values
        """
        topic_prefix = config.get('topic_prefix')
        environment = config.get('environment')
        return "%s.%s.%s" % (topic_prefix, environment, topic)

    def consume(self, msg):
        self.log.info("CVS2Slack[%(topic)s]: %(user)s: %(message)s" % {
            'topic': msg['topic'],
            'user': msg['body']['msg']['user'],
            'message': msg['body']['msg']['message'],
        })
        msg = msg['body']['msg']

        self.slack.notify(text='test', channel=self.channel, username=self.username)

import os

API_TOKEN = os.environ['API_TOKEN']
DEFAULT_REPLY = '/shrug'
ERRORS_TO = 'botspam-unhelpful'

PLUGINS = ['slackbot.plugins', 'unhelpful.plugin']

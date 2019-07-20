"""bot commands"""

from slackbot import respond_to


@respond_to('!([A-Z]{0-4})')
def quote(message, ticker):
    """respond to !TICKER requests"""
    message.reply(f'let me look up {ticker}')

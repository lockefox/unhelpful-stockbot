"""bot main"""
from slackbot.bot import Bot, respond_to

@respond_to('!([A-Z]{0-4})')
def quote(message, ticker):
    """respond to !TICKER requests"""
    message.reply(f'let me look up {ticker}')

def run():
    """entrypoint launcher for bot"""
    bot = Bot()
    bot.run()

if __name__ == '__main__':
    run()

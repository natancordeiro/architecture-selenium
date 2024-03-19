from bot import Bot

bot = Bot(False)
bot.load_page('https://www.google.com')
bot.sleep(10)
bot.quit()

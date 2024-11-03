from src.bot import Bot
from utils.logger.config import logger

bot = Bot(False)
bot.load_page('https://www.google.com')
bot.sleep(10)
bot.quit()

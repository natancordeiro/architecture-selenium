from src.bot import Bot
from utils.logger_config import logger

def main():
    config_path = 'config/config.yaml'

    bot = Bot(config_path)
    bot.load_page('https://www.google.com')
    bot.sleep(10)
    bot.quit()

if __name__ == '__main__':
    main()
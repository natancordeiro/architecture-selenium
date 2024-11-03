import logging
import colorlog

def setup_logger(log_file="app.log"):
    """
    Configura o logger para registrar logs coloridos no console
    e em um arquivo de log.
    """
    
    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)

    # Cria um handler para registrar em arquivo (sem cores)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S'
    )

    file_handler.setFormatter(file_formatter)

    # Cria um handler para exibir no console (com cores)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Define as cores para cada nível de log usando colorlog
    color_formatter = colorlog.ColoredFormatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%d/%m/%Y %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    console_handler.setFormatter(color_formatter)

    # Adiciona os handlers ao logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()
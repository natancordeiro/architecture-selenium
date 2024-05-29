"""
Módulo onde é guardado as funções externas para utilização geral do projeto.
"""

def setup_logging(to_file=False):
    """Setup logging"""

    # Criar um logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Formato do log
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%d-%m-%Y %H:%M:%S'
    formatter = logging.Formatter(log_format, datefmt=date_format)

    # Configurar o handler para o console com cores
    color_formatter = colorlog.ColoredFormatter(
        '%(log_color)s' + log_format,
        datefmt=date_format,
        reset=True,
        log_colors={
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(color_formatter)
    logger.addHandler(console_handler)

    if to_file:
        # Criar pasta logs se não existir
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # Nome do arquivo de log com a data e hora atuais
        log_filename = datetime.now().strftime("logs/log_%d-%m-%Y_%H-%M-%S.log")
        
        # Configurar o handler para o arquivo de log
        file_handler = RotatingFileHandler(log_filename, maxBytes=10**6, backupCount=5)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

from bsm.logger import get_logger
_logger = get_logger()

def run(param):
    _logger.info('Packing')
    _logger.info(param['command'])

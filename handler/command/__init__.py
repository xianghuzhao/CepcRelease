from bsm.loader import load_relative
from bsm.loader import LoadError

from bsm.handler import HandlerNotAvailableError

from bsm.logger import get_logger
_logger = get_logger()

def run(param):
    cmd = param['command']
    if not cmd:
        _logger.error('Command is empty')
        raise HandlerNotAvailableError

    try:
        run_func = load_relative(__name__, 'command.'+cmd[0], 'run')
    except LoadError as e:
        _logger.error('Could not find command: {0}'.format(cmd[0]))
        raise HandlerNotAvailableError

    if not callable(run_func):
        _logger.error('Command could not run')
        raise HandlerNotAvailableError

    return run_func(param)

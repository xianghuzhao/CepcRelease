import os

from bsm.util import safe_rmdir

from bsm.logger import get_logger
_logger = get_logger()

def run(param):
    clean_dirs = param['config_package'].get('clean', [])

    ['build', 'download', 'source', 'log']
    for d in clean_dirs:
        if d in ['source', 'build']:
            dir_path = param['config_package'].get('path', {}).get(d)
        elif d == 'download':
            dir_path = os.path.join(param['package_path']['misc_dir'], 'download')
        elif d == 'log':
            dir_path = param['package_path']['log_dir']
        else:
            continue

        if dir_path:
            safe_rmdir(dir_path)
            _logger.debug('Clean "{0}": {1}'.format(d, dir_path))
        else:
            _logger.warn('Clean directory not found for: {0}'.format(d))

    return True

import os

from bsm.error import HandlerNotAvailableError

from bsm.logger import get_logger
_logger = get_logger()

def run(param):
    if param['category'] not in ['work', 'workver']:
        _logger.error('Package in category "{0}" could not be built'.format(param['category']))
        raise HandlerNotAvailableError

    pkg_cfg = param['config_package']
    if 'cmake' not in pkg_cfg.get('build', []):
        _logger.error('Do not know how to build package: {0}'.format(param['name']))
        raise HandlerNotAvailableError

    make_jobs = param['config_attribute'].get('make_jobs', 1)

    pkg_path = param['package_path']
    build_type = param['type']
    this_dir = os.path.dirname(os.path.realpath(__file__))

    command = {}
    command['cmd'] = [os.path.join(this_dir, build_type+'.sh'), str(make_jobs)]
    command['cwd'] = pkg_path['main_dir']

    return command

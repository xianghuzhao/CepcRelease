from bsm.util import ensure_list
from bsm.util import which

from bsm.logger import get_logger
_logger = get_logger()


PACKAGE_MANAGER = {
        'yum': ['sudo', 'yum', 'install', '-y'],
        'apt-get': ['sudo', 'apt-get', 'install', '-y'],
        'pacman': ['sudo', 'pacman', '-S'],
        'zypper': ['sudo', 'zypper', '-n', 'install'],
}


def _detect_manager_type():
    for pkg_sys in PACKAGE_MANAGER:
        if which(pkg_sys):
            return pkg_sys
    return None


def run(param):
    missing_package = param['missing_package']
    if not missing_package:
        _logger.debug('There is no missing system package')
        return

    _logger.warn('Missing package(s): {0}'.format(', '.join(missing_package.keys())))

    mgr_type = _detect_manager_type()
    if not mgr_type:
        _logger.warn('Could not detect current package manager')
        return

    check_type = param['type']

    pkg_install_name = []
    for package, categories in param['missing_package'].items():
        for category in categories:
            pkg_cfg = param['config_package_check'][category][package]['config']
            install_name = pkg_cfg.get(check_type, {}).get('package_manager', {}).get(mgr_type, [])
            pkg_install_name += ensure_list(install_name)

    install_cmd = PACKAGE_MANAGER[mgr_type]
    _logger.info('The missing package(s) could be installed with the following command:\n' + ' '.join(install_cmd+pkg_install_name))

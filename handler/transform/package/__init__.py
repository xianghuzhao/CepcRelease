import copy

from bsm.loader import load_relative

def _run_sub(name, param, config_package):
    run_func = load_relative(__name__, 'package.'+name, 'run')
    return run_func(param, config_package)

def run(param):
    config_package = copy.deepcopy(param['config_package'])

    if param['type'] == 'check':
        return config_package

    _run_sub('package_detect_config', param, config_package)

    _run_sub('geant4_libdir', param, config_package)

    _run_sub('package_path', param, config_package)
    _run_sub('package_env', param, config_package)

    _run_sub('install_source', param, config_package)

    _run_sub('install_steps', param, config_package)

    _run_sub('no_clean', param, config_package)
    _run_sub('clean_only', param, config_package)
    _run_sub('keep_log', param, config_package)

    return config_package

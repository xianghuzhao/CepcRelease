import copy

from bsm.loader import load_relative

def _run_sub(name, param, config_package):
    run_func = load_relative('transform_package.'+name, 'run')
    return run_func(param, config_package)

def run(param):
    config_package = copy.deepcopy(param['config_package'])

    if param['category'] not in param['config_release'].get('setting', {}).get('category', {}):
        return config_package

    _run_sub('geant4_libdir', param, config_package)

    _run_sub('package_path', param, config_package)
    _run_sub('package_env', param, config_package)

    if param['operation'] == 'install' and param['config_category']['content'].get(param['category'], {}).get('install'):
        _run_sub('install_source', param, config_package)

    _run_sub('install_steps', param, config_package)

    _run_sub('no_clean', param, config_package)
    _run_sub('clean_only', param, config_package)
    _run_sub('keep_log', param, config_package)

    return config_package

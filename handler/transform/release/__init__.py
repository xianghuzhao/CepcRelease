import copy

from bsm.loader import load_relative

def _run_sub(name, param, config_release):
    run_func = load_relative(__name__, 'release.'+name, 'run')
    return run_func(param, config_release)

def run(param):
    config_release = copy.deepcopy(param['config_release_origin'])

    _run_sub('work_root', param, config_release)

    return config_release

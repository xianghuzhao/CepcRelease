import copy

from bsm.loader import load_relative

def _run_sub(name, param, config_release_setting):
    run_func = load_relative(__name__, 'release_setting.'+name, 'run')
    return run_func(param, config_release_setting)

def run(param):
    config_release_setting = copy.deepcopy(param['config_release_setting_origin'])

    _run_sub('work_root', param, config_release_setting)

    return config_release_setting

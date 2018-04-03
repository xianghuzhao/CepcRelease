from bsm.loader import load_relative

def _run_sub_transform(name, param):
    run_func = load_relative('transform.'+name, 'run')
    return run_func(param)

def _run_switch(name, option, param):
    if name in option and option[name].lower() in ['true', 'yes', 'on', '1']:
        param['config_release'] = _run_sub_transform(name, param)

def run(param):
    option = param['option']

    param['config_release'] = _run_sub_transform('software_platform', param)
    param['config_release'] = _run_sub_transform('geant4_libdir', param)

    param['config_release'] = _run_sub_transform('install_steps', param)

    if 'operation' in param and param['operation'] == 'install':
        if 'source' not in option or option['source'].lower() != 'origin':
            param['config_release'] = _run_sub_transform('ihep_source', param)

        _run_switch('no_clean', option, param)
        _run_switch('clean_only', option, param)
        _run_switch('keep_log', option, param)

    return param['config_release']

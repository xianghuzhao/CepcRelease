from bsm.util import ensure_list

def run(param):
    config_release = param['config_release']

    for pkg, cfg in config_release.get('package', {}).items():
        if 'clean' in cfg:
            clean_dirs = ensure_list(cfg['clean'])
            clean_dirs.remove('log')
            cfg['clean'] = clean_dirs

    return config_release

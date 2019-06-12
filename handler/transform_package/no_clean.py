def run(param):
    config_release = param['config_release']

    for pkg, cfg in config_release.get('package', {}).items():
        if 'clean' in cfg.get('install', {}):
            del cfg['install']['clean']

    return config_release

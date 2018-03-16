def run(param):
    config_release = param['config_release']

    for pkg, cfg in config_release.get('package', {}).items():
        install_cfg = cfg.get('install', {})
        for step in list(install_cfg):
            if step != 'clean':
                del install_cfg[step]

    return config_release

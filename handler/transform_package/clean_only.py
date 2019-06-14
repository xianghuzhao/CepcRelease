def run(param, cfg):
    option = param['config_option']

    if not option.get('clean_only'):
        return

    for step in cfg.get('install', {}):
        if step != 'clean':
            del cfg['install'][step]

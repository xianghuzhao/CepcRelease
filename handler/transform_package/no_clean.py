def run(param, cfg):
    option = param['config_option']

    if not option.get('no_clean'):
        return

    if 'clean' in cfg.get('install', {}):
        del cfg['install']['clean']

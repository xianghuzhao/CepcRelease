from bsm.util import ensure_list

def run(param, cfg):
    option = param['config_option']

    if not option.get('keep_log'):
        return

    if 'clean' in cfg:
        clean_list = ensure_list(cfg['clean'])
        clean_list.remove('log')
        cfg['clean'] = clean_list

def run(param, cfg):
    if param['type'] != 'runtime':
        return

    if param['category'] not in ['work', 'workver']:
        return

    if cfg.get('install', {}).get('download') != 'git':
        return

    if 'source' not in cfg:
        return

    version = cfg.get('version')
    if not version:
        return

    frag = version.split('.')
    if len(frag) >= 2:
        branch = 'develop-' + '.'.join(frag[:2])
    else:
        branch = 'develop'

    cfg['source']['keep_git'] = True
    cfg['source']['branch'] = branch

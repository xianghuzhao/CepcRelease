import os

def run(param, cfg):
    category = param['category']

    cfg.setdefault('path', {})

    cfg['path'].setdefault('build', 'build')

    if category in ['cepcsoft', 'work', 'work_ver'] and 'cmake' in cfg.get('build', []):
        cfg['path'].setdefault('source', '')
        cfg['path'].setdefault('install', '')
        cfg['path'].setdefault('cmake', '')
    else:
        cfg['path'].setdefault('source', 'source')
        cfg['path'].setdefault('install', 'install')

    format_dict = {k: v for k, v in cfg.get('path', {}).items() if k in ['source', 'build', 'install']}
    for k, v in cfg['path'].items():
        if k in ['source', 'build', 'install']:
            continue
        cfg['path'][k] = v.format(**format_dict).strip(os.sep)

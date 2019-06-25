from bsm.util import ensure_list

def _build_steps(cfg):
    cfg['build'] = ensure_list(cfg['build'])

    try:
        make_index = cfg['build'].index('make')
    except ValueError:
        return

    build_step_number = len(cfg['build'])
    if make_index > 0 and 'configure' not in cfg['install']:
        cfg['install']['configure'] = cfg['build'][make_index-1]
    if 'compile' not in cfg['install']:
        cfg['install']['compile'] = 'make'
    if make_index+1 < build_step_number and 'install' not in cfg['install']:
        cfg['install']['install'] = cfg['build'][make_index+1]


def run(param, cfg):
    cfg.setdefault('install', {})

    if 'source' in cfg and cfg['install'].get('download') == 'http':
        if 'main' in cfg['source']:
            cfg['install'].setdefault('extract', 'tar')

    if 'patch' in cfg:
        cfg['install'].setdefault('patch', 'patch')

    if 'build' in cfg:
        _build_steps(cfg)

    if param['category'] == 'cepcsoft' and 'cmake' in cfg.get('build', {}):
        cfg.setdefault('cmake', {})
        cfg['cmake']['ignore_install_prefix'] = True
        cfg['cmake'].setdefault('var', {})
        cfg['cmake']['var']['CMAKE_BUILD_TYPE'] = 'RelWithDebInfo'
        cfg['cmake']['var']['BUILD_32BIT_COMPATIBLE'] = 'OFF'
        cfg['cmake']['var']['INSTALL_DOC'] = 'OFF'

    cfg['install'].setdefault('clean', 'clean')
    cfg.setdefault('clean', ['build', 'download', 'log'])

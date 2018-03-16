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


def run(param):
    config_release = param['config_release']

    for pkg, cfg in config_release.get('package', {}).items():
        category = cfg.get('category')
        if not (category and config_release.get('setting', {}).get('category', {}).get('categories', {}).get(category, {}).get('install')):
            continue


        # Setup default values for install
        cfg.setdefault('install', {})

        if 'source' in cfg and 'main' in cfg['source']:
            cfg['install'].setdefault('extract', 'tar')

        if 'patch' in cfg:
            cfg['install'].setdefault('patch', 'patch')

        if 'build' in cfg:
            _build_steps(cfg)

        if category == 'cepcsoft' and 'build' in cfg and 'cmake' in cfg['build']:
            cfg.setdefault('cmake', {})
            cfg['cmake']['ignore_install_prefix'] = True
            cfg['cmake'].setdefault('var', {})
            cfg['cmake']['var']['CMAKE_BUILD_TYPE'] = 'RelWithDebInfo'
            cfg['cmake']['var']['BUILD_32BIT_COMPATIBLE'] = 'OFF'
            cfg['cmake']['var']['INSTALL_DOC'] = 'OFF'

        cfg['install'].setdefault('set_env', 'set_env')

        cfg['install'].setdefault('clean', 'clean')
        cfg.setdefault('clean', ['build', 'download', 'log'])

        cfg['install'].setdefault('save_release_status', 'save_release_status')


        # Setup default values for location and path
        cfg.setdefault('location', {})
        cfg['location'].setdefault('build', 'build')
        if category == 'cepcsoft' and 'build' in cfg and 'cmake' in cfg['build']:
            cfg['location'].setdefault('source', '')
            cfg['location'].setdefault('install', '')
        else:
            cfg['location'].setdefault('source', 'source')
            cfg['location'].setdefault('install', 'install')

        cfg.setdefault('path', {})
        cfg['path'].setdefault('home', '{install}')
        if not ('clean' in cfg and 'source' in cfg['clean']):
            cfg['path'].setdefault('src', '{source}')
        if 'build' in cfg and 'cmake' in cfg['build']:
            cfg['path'].setdefault('cmake', '{install}')

    return config_release

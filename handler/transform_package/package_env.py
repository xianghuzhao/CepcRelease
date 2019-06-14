from bsm.util import ensure_list

PATH_ENV = {
    'bin': 'PATH',
    'lib': 'LD_LIBRARY_PATH',
    'man': 'MANPATH',
    'info': 'INFOPATH',
    'pkgconfig': 'PKG_CONFIG_PATH',
    'cmake': 'CMAKE_PREFIX_PATH',
    'python': 'PYTHONPATH',
    'marlin': 'MARLIN_DLL',
}

def run(param, cfg):
    name = param['name']
    category = param['category']

    cfg.setdefault('env', {})

    cfg['env'].setdefault('set_env', {})

    cfg['env']['set_env'].setdefault(name+'_HOME', '{install}')

    if category != 'data' and 'source' not in cfg.get('clean', []):
        cfg['env']['set_env'].setdefault(name+'_SOURCE', '{source}')

    if 'bin' in cfg.get('path', {}):
        cfg['env']['set_env'].setdefault(name+'_BIN', '{bin}')
    if 'lib' in cfg.get('path', {}):
        cfg['env']['set_env'].setdefault(name+'_LIB', '{lib}')
    if 'inc' in cfg.get('path', {}):
        cfg['env']['set_env'].setdefault(name+'_INCLUDE', '{inc}')

    cfg['env'].setdefault('prepend_path', {})
    for k, v in PATH_ENV.items():
        if k in cfg.get('path', {}):
            cfg['env']['prepend_path'][v] = ensure_list(cfg['env']['prepend_path'].get(v, []))
            cfg['env']['prepend_path'][v].append('{{{0}}}'.format(k))

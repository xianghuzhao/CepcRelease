import os
import re

from bsm.util.config import load_config, ConfigError

_CEPCENV_PACKAGE_CONFIG_FILENAME = ['cepcenv.yaml', 'cepcenv.yml', '.cepcenv.yaml', '.cepcenv.yml']

def _load_config_cepcenv(param):
    main_dir = param['package_path']['main_dir']
    for fn in _CEPCENV_PACKAGE_CONFIG_FILENAME:
        full_path = os.path.join(main_dir, fn)
        if os.path.isfile(full_path):
            try:
                loaded_data = load_config(full_path)
                if isinstance(loaded_data, dict):
                    return loaded_data
            except:
                pass
            return {}
    return {}

def _match(content, pattern):
    m = re.search(pattern, content, re.IGNORECASE)
    if m:
        return m.group(1)
    return ''

def _find(content, pattern):
    m = re.search(pattern, content, re.IGNORECASE)
    return bool(m)

def _load_cmake_info(param, cfg):
    main_dir = param['package_path']['main_dir']
    cmakelist_path = os.path.join(main_dir, 'CMakeLists.txt')
    if not os.path.isfile(cmakelist_path):
        return {}

    result = {}

    result['build'] = ['cmake', 'make', 'make_install']

    with open(cmakelist_path) as f:
        content = f.read()

    project_name = _match(content, 'PROJECT\s*\(\s*(\w+)\s*\)')
    version_major = _match(content, 'VERSION_MAJOR\s+(\w+)\s*\)')
    version_minor = _match(content, 'VERSION_MINOR\s+(\w+)\s*\)')
    version_patch = _match(content, 'VERSION_PATCH\s+(\w+)\s*\)')
    marlin = _find(content, 'FIND_PACKAGE\s*\(\s*Marlin')
    lib = _match(content, 'INSTALL_SHARED_LIBRARY\s*\(.*DESTINATION\s+(\w+)\s*\)')

    if version_major:
        version = version_major
        if version_minor:
            version += '.'+version_minor
            if version_patch:
                version += '.'+version_patch
        result['version'] = version

    result['path'] = {}
    if lib:
        result['path']['lib'] = lib
        if marlin and project_name:
            result['path']['marlin'] = '{0}/lib{1}.so'.format(lib, project_name)

    return result

def _detect_version(config_cepcenv, cmake_info, param, cfg):
    if param.get('version') or cfg.get('version'):
        return

    if 'version' in config_cepcenv:
        cfg['version'] = config_cepcenv['version']
        return

    if 'version' in cmake_info:
        cfg['version'] = cmake_info['version']

def _detect_build(config_cepcenv, cmake_info, param, cfg):
    if 'build' in cfg:
        return

    if 'build' in config_cepcenv:
        cfg['build'] = config_cepcenv['build']
        return

    if 'build' in cmake_info:
        cfg['build'] = cmake_info['build']

def _detect_path(config_cepcenv, cmake_info, param, cfg):
    if 'path' in cfg:
        return

    if 'path' in config_cepcenv:
        cfg['path'] = config_cepcenv['path']
        return

    if 'path' in cmake_info:
        cfg['path'] = cmake_info['path']

def run(param, cfg):
    if param['type'] != 'runtime':
        return

    if param['category'] not in ['work', 'work_ver']:
        return

    cmake_info = _load_cmake_info(param, cfg)
    config_cepcenv = _load_config_cepcenv(param)

    _detect_version(config_cepcenv, cmake_info, param, cfg)
    _detect_build(config_cepcenv, cmake_info, param, cfg)
    _detect_path(config_cepcenv, cmake_info, param, cfg)

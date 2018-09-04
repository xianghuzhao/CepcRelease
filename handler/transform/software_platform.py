import platform
import re
import distro


def _detect_arch():
    return platform.machine()

def _detect_os():
    id = distro.id()
    name = distro.name()
    major = distro.major_version()
    minor = distro.minor_version()
    if name.startswith('Scientific'):
        return 'sl'+major
    if name.startswith('Red Hat Enterprise'):
        return 'rhel'+major
    if id == 'centos':
        return 'centos'+major
    if id == 'debian':
        return 'debian'+major
    if id == 'arch':
        return 'arch'
    if id == 'gentoo':
        return 'gentoo'+major+'.'+minor
    if id == 'ubuntu':
        return 'ubuntu'+major+minor
    if id == 'fedora':
        return 'fedora'+major
    if name.startswith('openSUSE'):
        return 'opensuse'+major
    return 'unknown'


def _installed_compiler(config_release):
    gcc_cfg = config_release.get('package', {}).get('GCC', {})
    gcc_category = gcc_cfg.get('category')
    gcc_version = gcc_cfg.get('version')

    if not (gcc_category and config_release.get('setting', {}).get('category', {}).get('categories', {}).get(gcc_category, {}).get('install')):
        return ''

    compiler = 'gcc'
    ver_frag = gcc_version.split('.')
    if len(ver_frag) >= 2:
        gcc_v2 = ''.join(ver_frag[:2])
        compiler += gcc_v2
    return compiler

def _provided_compiler():
    try:
        output = check_output(['gcc', '--version'])
        m = re.match('gcc \(GCC\) (\d+)\.(\d+)', output)
        version_major = m.group(1)
        version_minor = m.group(2)
        return 'gcc{0}{1}'.format(version_major, version_minor)
    except Exception as e:
        return 'unknown'

def _detect_compiler(config_release):
    compiler = _installed_compiler(config_release)
    if compiler:
        return compiler
    return _provided_compiler()


def _search_config(config_scenario, name):
    if name in config_scenario and config_scenario[name]:
        return config_scenario[name]
    return ''

def _modify_categories(config_release, final_platform):
    categories = config_release.get('setting', {}).get('category', {}).get('categories', {})
    for ctg, config in categories.items():
        if 'root' in config:
            config['root'] = config['root'].replace('PLATFORM', final_platform)

def _modify_global_env(config_release, final_platform):
    setting_global_env = config_release.get('setting', {}).get('global_env', {})
    for env_name, value in setting_global_env.items():
        setting_global_env[env_name] = value.replace('PLATFORM', final_platform)


def run(param):
    config_scenario = param['config_scenario']
    config_release = param['config_release']

    arch = (_search_config(config_scenario, 'arch') or _detect_arch())
    os = (_search_config(config_scenario, 'os') or _detect_os())
    compiler = (_search_config(config_scenario, 'compiler') or _detect_compiler(config_release))

    final_platform = (_search_config(config_scenario, 'platform') or '-'.join([arch, os, compiler]))

    _modify_categories(config_release, final_platform)
    _modify_global_env(config_release, final_platform)

    return config_release

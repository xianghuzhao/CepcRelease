import platform
import re
import distro

from bsm.util import check_output


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


def _installed_compiler(config_release_origin):
    gcc_cfg = config_release_origin.get('package', {}).get('external/GCC', {})
    gcc_version = gcc_cfg.get('version')

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

def _detect_compiler(option, config_release_origin):
    if 'system_gcc' in option and option['system_gcc']:
        return _provided_compiler()
    return _installed_compiler(config_release_origin)


def _search_option(option, name):
    if name in option and option[name]:
        return option[name]
    return ''


def run(param):
    option = param['config_option']
    config_release_origin = param['config_release_origin']

    arch = (_search_option(option, 'arch') or _detect_arch())
    os = (_search_option(option, 'os') or _detect_os())
    compiler = (_search_option(option, 'compiler') or _detect_compiler(option, config_release_origin))

    final_platform = (_search_option(option, 'platform') or '-'.join([arch, os, compiler]))

    return {'arch': arch, 'os': os, 'compiler': compiler, 'platform': final_platform}

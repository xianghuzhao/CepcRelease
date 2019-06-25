import os
import glob
import re
import subprocess

from bsm.util import call

from bsm.logger import get_logger
_logger = get_logger()


def _executable_dir(env):
    return [x for x in env.get('PATH', '').split(os.pathsep) if x]

def _include_dir(env):
    inc_dir = ['/usr/include', '/usr/local/include']
    return inc_dir

def _library_dir(env):
    lib_dir = [x for x in env.get('LD_LIBRARY_PATH', '').split(os.pathsep) if x]

    try:
        env_new = env.copy()
        env_new['PATH'] = env['PATH'] + os.pathsep + os.pathsep.join(['/sbin', '/usr/sbin', '/usr/local/sbin'])
        ret, out, err = call(['ldconfig', '-v', '-N'], stderr=subprocess.PIPE, env=env_new)
        for m in re.finditer('^(.*?):', out.decode(), flags=re.MULTILINE):
            lib_dir.append(m.group(1))
    except Exception as e:
        _logger.warn('Command ldconfig error: {0}'.format(e))
        lib_dir += ['/lib', '/lib64', '/usr/lib', '/usr/lib64']
    return lib_dir


class Check(object):
    def __init__(self, config_package, pkg_type, env):
        self.__config_package = config_package
        self.__pkg_type = pkg_type
        self.__load_check_dir(env)

    def __check_single_file(self, check_dirs, check_file):
        for d in check_dirs:
            dst_file = os.path.join(d, check_file)
            # Use glob in order to accept wildcards
            if glob.glob(dst_file):
                _logger.debug('Package found by: {0}'.format(dst_file))
                return True
        return False

    # Match any file in the file_list
    def __check_optional_files(self, check_dirs, file_list):
        for f in file_list:
            if self.__check_single_file(check_dirs, f):
                return True
        return False

    # Match every file_list in the check_list
    def __check_single_type(self, dir_type, check_list):
        if dir_type not in self.__check_dir:
            _logger.warn('Unknown check type: {0}'.format(dir_type))
            return False

        for l in check_list:
            if not self.__check_optional_files(self.__check_dir[dir_type], l):
                return False

        return True

    def __check_package(self, check_cfg):
        for dir_type, check_list in check_cfg.items():
            if not self.__check_single_type(dir_type, check_list):
                return False
        return True

    def check(self):
        pkg = self.__config_package['name']
        _logger.debug('Searching package: {0}'.format(pkg))
        if not self.__check_package(self.__config_package.get(self.__pkg_type, {}).get('check', {})):
            _logger.debug('Package not available: {0}'.format(pkg))
            return False

        return True

    def __load_check_dir(self, env):
        self.__check_dir = {}
        self.__check_dir['include'] = _include_dir(env)
        self.__check_dir['library'] = _library_dir(env)
        self.__check_dir['executable'] = _executable_dir(env)

        for dir_type, check_dir in self.__check_dir.items():
            _logger.debug('Package checking directories for {0}: {1}'.format(dir_type, check_dir))

def run(param):
    chk = Check(param['config_package'], param['type'], param['env'])
    return chk.check()

import os

from bsm.util import call, safe_mkdir, safe_rmdir, expand_path

from bsm.logger import get_logger
_logger = get_logger()


def _download_http(url, dst):
    pos = url.rfind('/')
    if pos == -1:
        raise Exception('Can not find file name from url: {0}'.format(url))
    fn = url[pos+1:]
    fntmp = fn + '.tmp'

    if os.path.isfile(os.path.join(dst, fn)):
        return fn

    cmd = ['curl', '-f', '-L', '-s', '-S', '-R', '-o', fntmp, url]
    ret, out, err = call(cmd, cwd=dst)
    if ret != 0:
        raise Exception('Download http Failed {0} "{1}": {2}'.format(ret, url, out))

    cmd = ['mv', fntmp, fn]
    ret, out, err = call(cmd, cwd=dst)
    if ret != 0:
        raise Exception('Rename Failed {0} "{1}": {2}'.format(ret, fn, out))

    return fn

def _download_svn(url, dst, pkg, version):
    name = '{0}-{1}'.format(pkg, version)
    fn = name + '.tar.gz'

    if os.path.isfile(os.path.join(dst, fn)) and not os.path.isdir(os.path.join(dst, name)):
        return fn

    safe_rmdir(os.path.join(dst, name))

    cmd = ['svn', 'export', '--force', url, name]
    ret, out, err = call(cmd, cwd=dst)
    if ret != 0:
        raise Exception('Download svn Failed: {0}'.format(url))

    cmd = ['tar', '-czf', fn, name]
    ret, out, err = call(cmd, cwd=dst)
    if ret != 0:
        raise Exception('Tar svn repo Failed: {0}'.format(name))

    #safe_rmdir(os.path.join(dst, name))

    return fn

def _download_git(url, tag, dst, pkg, version):
    name = '{0}-{1}'.format(pkg, version)
    fn = name + '.tar.gz'

    if os.path.isfile(os.path.join(dst, fn)) and not os.path.isdir(os.path.join(dst, name)):
        return fn

    safe_rmdir(os.path.join(dst, name))

    cmd = ['git', 'clone', url, name]
    ret, out, err = call(cmd, cwd=dst)
    if ret != 0:
        raise Exception('Download git Failed: {0}'.format(url))

    cmd = ['git', 'checkout', tag]
    ret, out, err = call(cmd, cwd=os.path.join(dst, name))
    if ret != 0:
        raise Exception('Git checkout Failed: {0}'.format(url))

    safe_rmdir(os.path.join(dst, name, '.git'))

    cmd = ['tar', '-czf', fn, name]
    ret, out, err = call(cmd, cwd=dst)
    if ret != 0:
        raise Exception('Tar git repo Failed: {0}'.format(name))

    #safe_rmdir(os.path.join(dst, name))

    return fn


def run(param):
    release_version = param['config_scenario']['version']

    if len(param['command']) > 1:
        destination = param['command'][1]
    else:
        destination = os.getcwd()

    destination = expand_path(destination)
    pack_dir = os.path.join(destination, 'pack_'+release_version)

    for category in param['config_package_install']:
        for subdir in param['config_package_install'][category]:
            for package in param['config_package_install'][category][subdir]:
                for version, value in param['config_package_install'][category][subdir][package].items():
                    pkg_cfg = value['config_origin']

                    download = pkg_cfg.get('install', {}).get('download')
                    if not download:
                        continue

                    url = pkg_cfg.get('source', {}).get('url')
                    if not url:
                        continue

                    pkg_dir = os.path.join(pack_dir, package, version)
                    safe_mkdir(pkg_dir)

                    _logger.info('Packing {0}...'.format(package))

                    if download == 'http':
                        url = url.format(version=version)
                        pkg_file = _download_http(url, pkg_dir)
                    elif download == 'svn':
                        url = url.format(version=version)
                        pkg_file = _download_svn(url, pkg_dir, package, version)
                    elif download == 'git':
                        tag = pkg_cfg.get('source', {}).get('tag', 'master')
                        tag = tag.format(version=version)
                        pkg_file = _download_git(url, tag, pkg_dir, package, version)
                    else:
                        _logger.warn('Package {0} not packed'.format(package))
                        continue

                    with open(os.path.join(pkg_dir, 'md5sum.txt'), 'w') as f:
                        call(['md5sum', pkg_file], cwd=pkg_dir, stdout=f)
                    with open(os.path.join(pkg_dir, 'sha1sum.txt'), 'w') as f:
                        call(['sha1sum', pkg_file], cwd=pkg_dir, stdout=f)
                    with open(os.path.join(pkg_dir, 'url.txt'), 'w') as f:
                        f.write(url+'\n')

                    _logger.info('Package {0} packed'.format(package))

    _logger.info('All packages in version {0} packed in {1}'.format(release_version, pack_dir))

IHEP_PACKAGE_BASE_URL = 'http://cepcsoft.ihep.ac.cn/package/cepcsoft'

def run(param):
    config_release = param['config_release']

    for pkg, cfg in config_release.get('package', {}).items():
        install_config = cfg.get('install', {})
        if not install_config:
            continue

        handler = install_config.get('download', {}).get('handler')
        if not handler:
            continue

        version = cfg.get('version')
        if not version:
            continue

        if handler == 'http':
            filename = cfg['install'].get('extract', {}).get('param', {}).get('file')
            if filename:
                cfg['install']['download']['param']['url'] = \
                        '{base_url}/{package}/{version}/{filename}'\
                        .format(base_url=IHEP_PACKAGE_BASE_URL, package=pkg, version=version, filename=filename)
        elif handler == 'svn':
            name = '{0}-{1}'.format(pkg, version)
            filename = name + '.tar.gz'
            cfg['install']['download']['handler'] = 'http'
            cfg['install']['download']['param']['url'] = \
                    '{0}/{1}/{2}/{3}'.format(IHEP_PACKAGE_BASE_URL, pkg, version, filename)
            cfg['install']['extract'] = {}
            cfg['install']['extract']['handler'] = 'tar'
            cfg['install']['extract']['param'] = {}
            cfg['install']['extract']['param']['file'] = filename
            cfg['install']['extract']['param']['main'] = name

    return config_release

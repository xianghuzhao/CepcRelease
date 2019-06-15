IHEP_PACKAGE_BASE_URL = 'http://cepcsoft.ihep.ac.cn/package/cepcsoft'


def _ihep_source(param, cfg):
    action = cfg.get('install', {}).get('download')
    if not action:
        return

    package = param.get('name')

    version = param.get('version')
    if not version:
        return

    if action == 'http':
        filename = cfg.get('source', {}).get('file')
        if filename:
            cfg['source']['url'] = \
                    '{base_url}/{package}/{version}/{filename}'\
                    .format(base_url=IHEP_PACKAGE_BASE_URL, package=package, version=version, filename=filename)
    else:
        name = '{0}-{{version}}'.format(package)
        filename = name + '.tar.gz'

        cfg['install']['download'] = 'http'

        cfg['source'] = {}
        cfg['source']['url'] = \
                '{base_url}/{package}/{version}/{filename}'\
                .format(base_url=IHEP_PACKAGE_BASE_URL, package=package, version=version, filename=filename)
        cfg['source']['file'] = filename
        cfg['source']['main'] = name


def run(param, cfg):
    option = param['config_option']

    cfg.setdefault('install', {})

    if 'source' in cfg and cfg.get('install', {}).get('download') == 'http':
        if 'url' in cfg['source']:
            if 'file' not in cfg['source']:
                cfg['source']['file'] = cfg['source']['url'].split('/')[-1]

            if 'main' not in cfg['source']:
                for ext in ['.tar.gz', '.tar.bz2', '.tgz']:
                    if cfg['source']['file'].endswith(ext):
                        cfg['source']['main'] = cfg['source']['file'][:-len(ext)]
                        break

    if 'source' not in option or option['source'].lower() != 'origin':
        _ihep_source(param, cfg)

    if 'source' in cfg and cfg.get('install', {}).get('download') == 'http':
        package = param.get('name')
        version = param.get('version')
        if package and version:
            md5url = '{base_url}/{package}/{version}/md5sum.txt'.format(base_url=IHEP_PACKAGE_BASE_URL, package=package, version=version)
            cfg['source'].setdefault('md5url', md5url)

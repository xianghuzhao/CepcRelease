from bsm.util import ensure_list

def run(param, config_release):
    option = param['config_option']

    category = config_release.get('setting', {}).get('category', {})
    category_priority = ensure_list(config_release.get('setting', {}).get('category_priority', []))

    if 'work' in category:
        if 'work_root' in option:
            category['work']['root'] = option['work_root']
        else:
            del category['work']
            category_priority.remove('work')

    if 'work_ver' in category:
        if 'work_ver_root' in option:
            category['work_ver']['root'] = option['work_ver_root']
        else:
            del category['work_ver']
            category_priority.remove('work_ver')

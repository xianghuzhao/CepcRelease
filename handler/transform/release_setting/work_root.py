from bsm.util import ensure_list

def run(param, config_release_setting):
    option = param['config_option']

    category = config_release_setting.get('category', {})
    category_priority = ensure_list(config_release_setting.get('category_priority', []))

    if 'work' in category:
        if 'work_root' in option:
            category['work']['root'] = option['work_root']
        else:
            del category['work']
            category_priority.remove('work')

    if 'workver' in category:
        if 'workver_root' in option:
            category['workver']['root'] = option['workver_root']
        else:
            del category['workver']
            category_priority.remove('workver')

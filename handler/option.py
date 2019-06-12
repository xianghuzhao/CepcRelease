def run():
    options = {}

    options['arch'] = '[Common] System architecture'
    options['os'] = '[Common] Operation system'
    options['compiler'] = '[Common] Compiler name and version'
    options['platform'] = '[Common] Platform name, {arch}-{os}-{compiler}'

    options['work_root'] = '[Runtime] User work root directory'
    options['version_work_root'] = '[Runtime] User work root directory with version directory'

    options['make_jobs'] = '[Installation] Number of jobs for make command'
    options['source'] = '[Installation] "origin" to use the original source to download packages, other value to use IHEP source'
    options['no_clean'] = '[Installation] Do not clean intermediate files during installation'
    options['clean_only'] = '[Installation] Do not install packages, only clean the intermediate files'
    options['keep_log'] = '[Installation] Keep log files when cleaning intermediate files'

    return options

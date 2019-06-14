import os
import platform

def run(param, config_package):
    if param['category'] != 'external' or param['name'] != 'Geant4':
        return

    libdir = 'lib'

    if platform.system() == 'Linux' and platform.machine() == 'x86_64':
        if not os.path.exists('/etc/debian_version'):
            libdir = 'lib64'

    geant4_path = config_package.get('path', {})
    if 'lib' in geant4_path:
        geant4_path['lib'] = geant4_path['lib'].replace('/lib', '/'+libdir)

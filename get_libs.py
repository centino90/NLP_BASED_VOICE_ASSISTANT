import os
import pip
from datetime import datetime

def get_installation_date(package_name):
    # Get the installation directory of the package
    package_dir = pip._vendor.pkg_resources.get_distribution(package_name).location
    
    # Get the modification time of the package directory
    modification_time = os.path.getmtime(package_dir)
    
    # Convert modification time to a human-readable format
    install_date = datetime.fromtimestamp(modification_time)
    
    return install_date

if __name__ == "__main__":
    installed_packages = pip._internal.utils.misc.get_installed_distributions()
    
    print("Installed Packages:")
    print("-------------------")
    for package in installed_packages:
        install_date = get_installation_date(package.key)
        print(f"{package.key} (Installed on: {install_date})")
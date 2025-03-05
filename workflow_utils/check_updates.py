import os
import requests
from packaging import version
from packaging.specifiers import SpecifierSet
PYTHON_VERSION = '3.10'

def get_compatible_latest_version(package_name, project_python_version):
    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    data = response.json()
    
    latest_version = data["info"]["version"]
    requires_python = data["info"]["requires_python"]

    if not requires_python:
        return latest_version
    
    specifier = SpecifierSet(requires_python)
    if specifier.contains(project_python_version):
        return latest_version
    else:
        return None  


with open("workflow_utils/reqs_3.10.txt") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" not in line:
            continue  # Skip unpinned packages
        pkg_name, current_version = line.split("==", 1)
        pkg_name = pkg_name.strip()
        current_version = current_version.split("#")[0].strip()

        latest_version = get_compatible_latest_version(pkg_name, PYTHON_VERSION)
        if latest_version and version.parse(latest_version) > version.parse(current_version):
            print(f"🔄 New version: {pkg_name} ({current_version} → {latest_version})")
            updates_available = True

print(updates_available)

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        f.write(f"updates-available={'true' if updates_available else 'false'}\n")
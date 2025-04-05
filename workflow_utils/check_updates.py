import os
import sys
import requests
from packaging import version
from packaging.specifiers import SpecifierSet
from packaging.requirements import Requirement

sys.path.append('.')
from workflow_utils import get_pinned_packages

PYTHON_VERSION = '3.10'

def get_compatible_latest_version(package_name, project_python_version):
    """Fetches the latest compatible version of a package from PyPI."""
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

def get_constrained_dependencies():
    """Get the constrained dependencies from pyproject.toml files."""	
    core_pyproject_toml = 'workflow_utils/pyproject_core.toml'
    iqo_pyproject_toml = 'workflow_utils/pyproject_iqo.toml'

    core_constraints = get_pinned_packages.get_constrained_dependencies(core_pyproject_toml)
    iqo_constraints = get_pinned_packages.get_constrained_dependencies(iqo_pyproject_toml)
    packages_with_constraints = []
    for constraints in (core_constraints, iqo_constraints):
        for constraint in constraints:
            req = Requirement(constraint)
            package_name = req.name
            packages_with_constraints.append(package_name)
    return packages_with_constraints

constrained_dependencies = get_constrained_dependencies()
updates_available = False
with open("workflow_utils/reqs_3.10.txt") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" not in line:
            continue  
        pkg_name, current_version = line.split("==", 1)
        pkg_name = pkg_name.strip()
        if pkg_name in constrained_dependencies:
            continue
        current_version = current_version.split("#")[0].strip()

        latest_version = get_compatible_latest_version(pkg_name, PYTHON_VERSION)

        if latest_version and version.parse(latest_version) > version.parse(current_version):
            print(f"🔄 New version: {pkg_name} ({current_version} → {latest_version})")
            updates_available = True


with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        f.write(f"updates-available={'true' if updates_available else 'false'}\n")
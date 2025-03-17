import sys
import toml
from packaging.requirements import Requirement

def has_version_constraints(dep):
    req = Requirement(dep)
    return len(req.specifier) > 0

def is_pinned(dep):
    req = Requirement(dep)
    return all(spec.operator == '==' for spec in req.specifier)

def is_upper_bounded(dep):
    req = Requirement(dep)
    return any(spec.operator in ('<', '<=', '~=', '^') for spec in req.specifier)


def get_constrained_dependencies(pyproject_path):
    with open(pyproject_path, 'r') as file:
        pyproject_data = toml.load(file)

    # Extract dependencies from the [project.dependencies] section
    dependencies = pyproject_data.get('project', {}).get('dependencies', [])

    if not dependencies:
        print("No dependencies found in pyproject.toml.")
        return

    # Filter dependencies with version constraints
    pinned_deps = [dep for dep in dependencies if is_pinned(dep)]
    upper_bounded_deps = [dep for dep in dependencies if is_upper_bounded(dep)]

    return pinned_deps + upper_bounded_deps
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python filter_dependencies.py <path_to_pyproject.toml>")
        sys.exit(1)

    pyproject_path = sys.argv[1]
    get_constrained_dependencies(pyproject_path)
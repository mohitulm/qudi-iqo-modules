import os
import requests
from packaging import version

def get_latest_version(package_name):
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=10)
        if response.status_code == 200:
            return response.json()["info"]["version"]
    except Exception:
        pass
    return None

updates_available = False

with open("worflow_utils/reqs_3.10.txt") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" not in line:
            continue  # Skip unpinned packages
        pkg_name, current_version = line.split("==", 1)
        pkg_name = pkg_name.strip()
        current_version = current_version.split("#")[0].strip()

        latest_version = get_latest_version(pkg_name)
        if latest_version and version.parse(latest_version) > version.parse(current_version):
            print(f"🔄 New version: {pkg_name} ({current_version} → {latest_version})")
            updates_available = True

print(updates_available)

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        f.write(f"updates-available={'true' if updates_available else 'false'}\n")
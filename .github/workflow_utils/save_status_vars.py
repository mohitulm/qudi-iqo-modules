import os
import shutil
import pathlib
from qudi.util.paths import get_appdata_dir

SAVED_STATUS_VAR_DIR = 'saved_status_vars'
os.mkdir(SAVED_STATUS_VAR_DIR)
ACTIVE_STATUS_VAR_DIR = get_appdata_dir()
SV_STATUS_FILE = 'status_var_changes.txt'

with open(SV_STATUS_FILE, 'r') as file:
    sv_status = ''.join(file.readlines())
    if not 'No differences found'in sv_status:
        for active_sv_file in os.listdir(ACTIVE_STATUS_VAR_DIR):
            file_extension = pathlib.Path(active_sv_file).suffix
            if not ('logic' in active_sv_file or 'hardware' in active_sv_file) or file_extension!='.cfg':
                continue
            active_sv_file_path = os.path.join(ACTIVE_STATUS_VAR_DIR, active_sv_file)
            shutil.copy(active_sv_file_path, SAVED_STATUS_VAR_DIR)




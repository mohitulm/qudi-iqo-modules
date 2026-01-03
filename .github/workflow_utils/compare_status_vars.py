import os
import shutil
import pathlib
from qudi.util.yaml import yaml_load, yaml_dump
from qudi.util.paths import get_appdata_dir

SAVED_DIR = 'saved_status_vars'

def load_status_var(file_path):    
    try:
        variables = yaml_load(file_path, ignore_missing=True)
    except Exception as e:
        variables = dict()
        print("Failed to load status variables:", e)
    return variables

def compare_status_vars(active_svs, saved_svs):
    changed_svs = []
    for sv in active_svs:
        try:
            if sv not in saved_svs:
                changed_svs.append([sv, {}, active_svs[sv]])
            elif active_svs[sv] != saved_svs[sv] :
                changed_svs.append([sv, saved_svs[sv], active_svs[sv]])
        except:
            continue
    return changed_svs

def compare_data(output_file = 'status_var_changes.txt'):
    errors = {}
    active_sv_dir = get_appdata_dir()
    active_svs_files = os.listdir(active_sv_dir)
    if not os.path.isdir(SAVED_DIR) :
        os.mkdir(SAVED_DIR)
        for active_sv_file in active_svs_files:
            if not ('logic' in active_sv_file or 'hardware' in active_sv_file):
                continue
            active_sv_file_path = os.path.join(active_sv_dir, active_sv_file)
            shutil.copy(active_sv_file_path, SAVED_DIR)
            errors = 'First run'

    else:
        saved_svs_files = os.listdir(SAVED_DIR)
        active_not_saved = set(active_svs_files) - set(saved_svs_files)
        saved_not_active = set(saved_svs_files) - set(active_svs_files)
        for active_svs_file in os.listdir(active_sv_dir):
            file_extension = pathlib.Path(active_svs_file).suffix
            if file_extension!='.cfg':
                continue
            if not ('logic' in active_svs_file or 'hardware' in active_svs_file):
                continue
            active_svs_fp = os.path.join(active_sv_dir, active_svs_file)
            active_svs = load_status_var(active_svs_fp)

            saved_svs_fp = os.path.join(SAVED_DIR, active_svs_file)
            saved_svs = load_status_var(saved_svs_fp)
            print(f'file {active_svs_file}, active {active_svs}, saved {saved_svs}' )
            changes = compare_status_vars(active_svs, saved_svs)
            if changes:
                errors[active_svs_file] = changes
        
    with open(output_file, 'w') as file:
        if not errors:
            print("No differences found.\n")
            file.write("No differences found.\n")
        elif errors == 'First run':
            file.write("First save.\n")

        else:
            file.write("Changed status variables:\n")
            for sv_file, changes in errors.items():
                    for (var, saved_val, curr_value) in changes:
                        file.write(f"{sv_file} : {var}: {saved_val} -> {curr_value}\n")
                        print(f"{var}: {saved_val} -> {curr_value}\n")


if __name__ == "__main__":
    compare_data()


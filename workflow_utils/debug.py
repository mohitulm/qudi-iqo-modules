import os
from qudi.util.yaml import yaml_load


def load_status_var(file_path):    
    try:
        variables = yaml_load(file_path, ignore_missing=True)
        print(variables)
    except Exception as e:
        variables = dict()
        print("Failed to load status variables:", e)

file_path = 'workflow_utils/saved_status_vars/status-PIDLogic_hardware_pid_logic.cfg'
load_status_var(file_path)
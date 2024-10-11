# -*- coding: utf-8 -*-

"""
This file contains unit tests for all qudi fit routines for exponential decay models.

Copyright (c) 2021, the qudi developers. See the AUTHORS.md file at the top-level directory of this
distribution and on <https://github.com/Ulm-IQO/qudi-core/>

This file is part of qudi.

Qudi is free software: you can redistribute it and/or modify it under the terms of
the GNU Lesser General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

Qudi is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with qudi.
If not, see <https://www.gnu.org/licenses/>.
"""

import random
import time
import string
import pytest
import numpy as np
from qudi.util.yaml import yaml_load, yaml_dump
from qudi.util.paths import get_module_app_data_path

@pytest.fixture
def module_manager(remote_instance):
    return remote_instance.module_manager

def get_status_var_file(instance):
    file_path = get_module_app_data_path(
            instance.__class__.__name__, instance.module_base, instance.module_name
        )
    return file_path

def load_status_var(file_path):    
    try:
        variables = yaml_load(file_path, ignore_missing=True)
    except Exception as e:
        variables = dict()
        print("Failed to load status variables:", e)
    return variables


def test_status_vars(module_manager, gui_modules, qudi_instance, qt_app):
    """Test if GUI modules are activated correctly after updating the saved files.

    Parameters
    ----------
    module_manager : fixture
        Remote module manager
    gui_modules : fixture
        List of GUI modules
    qudi_instance : fixture
        So that Qudi objects don't go out of scope
    qt_app : fixture
        Instance of Qt app
    """    
    for gui_module in gui_modules:
        module_manager.activate_module(gui_module)
        gui_managed_module = module_manager.modules[gui_module]
        assert gui_managed_module.is_active
        time.sleep(5)
        module_manager.deactivate_module(gui_module)
        time.sleep(1)
    qudi_instance.quit()


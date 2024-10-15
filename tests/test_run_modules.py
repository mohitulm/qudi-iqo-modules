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

import time



def test_activate_modules(remote_instance, gui_modules, qt_app, qudi_instance):
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
    module_manager = remote_instance.module_manager
    for gui_module in gui_modules[:1]:
        module_manager.activate_module(gui_module)
        gui_managed_module = module_manager.modules[gui_module]
        assert gui_managed_module.is_active
        time.sleep(5)
        module_manager.deactivate_module(gui_module)
        time.sleep(1)


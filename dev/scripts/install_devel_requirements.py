"""
Installs the development dependancies
"""

import os
from builtins import input as pause  # wait for user input, Python 2 and 3 compatible

import _project_cfg_importer

project_cfg = _project_cfg_importer.get_project_cfg()


def main():
    """
    Entry point of script
    """
    print("********************************************************************************\n"
          "*                      Installing Python Dependancies                          *\n"
          "********************************************************************************\n")

    install_python_2_deps_command = (
        "{python_exe} -m pip install -r {devel_reqs}".format(python_exe=project_cfg.PYTHON_2_EXECUTABLE,
                                                             devel_reqs=project_cfg.DEVEL_REQUIREMENTS_FILE)
    )

    os.system(install_python_2_deps_command)

    print("********************************************************************************\n"
          "*                      Done (Installing Python Dependancies)                   *\n"
          "********************************************************************************\n")

    pause("Press enter to exit...")

if __name__ == '__main__':
    main()

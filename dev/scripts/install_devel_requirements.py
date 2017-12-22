"""
Installs the development dependancies
"""

import os
import _project_cfg_importer

project_cfg = _project_cfg_importer.get_project_cfg()


def main():
    """
    Entry point of script
    """
    print("********************************************************************************\n"
          "*                      Installing Python Dependancies                          *\n"
          "********************************************************************************\n")

    if project_cfg.IS_PYTHON_2_AND_3_COMPATIBLE == 0:
        print("Installing for " + str(project_cfg.DEFAULT_PYTHON_EXECUTABLE))
        install_python_deps_command = (
            "{python_exe} -m pip install -r {devel_reqs}".format(python_exe=project_cfg.DEFAULT_PYTHON_EXECUTABLE,
                                                                 devel_reqs=project_cfg.DEVEL_REQUIREMENTS_FILE)
        )

        os.system(install_python_deps_command)

    else:
        print("Installing for {} and {}".format(project_cfg.PYTHON_2_EXECUTABLE, project_cfg.PYTHON_3_EXECUTABLE))
        install_python_2_deps_command = (
            "{python_exe} -m pip install -r {devel_reqs}".format(python_exe=project_cfg.PYTHON_2_EXECUTABLE,
                                                                 devel_reqs=project_cfg.DEVEL_REQUIREMENTS_FILE)
        )

        install_python_3_deps_command = (
            "{python_exe} -m pip install -r {devel_reqs}".format(python_exe=project_cfg.PYTHON_3_EXECUTABLE,
                                                                 devel_reqs=project_cfg.DEVEL_REQUIREMENTS_FILE)
        )

        os.system(install_python_2_deps_command)
        os.system(install_python_3_deps_command)

    print("********************************************************************************\n"
          "*                      Done (Installing Python Dependancies)                   *\n"
          "********************************************************************************\n")


if __name__ == '__main__':
    main()

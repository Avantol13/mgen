"""
Runs unit tests and displays results in command line
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
          "*                            Running Python Tests                              *\n"
          "********************************************************************************\n")

    os.chdir(project_cfg.SOURCE_CODE_DIR)

    if project_cfg.IS_PYTHON_2_AND_3_COMPATIBLE == 0:
        run_unit_tests_command = (
            "{python_exe} -m pytest {test_dir} -v".format(python_exe=project_cfg.DEFAULT_PYTHON_EXECUTABLE,
                                                          test_dir=project_cfg.TEST_DIR)
        )
        _run_unit_tests_command(project_cfg.DEFAULT_PYTHON_EXECUTABLE, run_unit_tests_command)
    else:
        run_unit_tests_2_command = (
            "{python_exe} -m py.test {test_dir} -v".format(python_exe=project_cfg.PYTHON_2_EXECUTABLE,
                                                           test_dir=project_cfg.TEST_DIR)
        )
        run_unit_tests_3_command = (
            "{python_exe} -m pytest {test_dir} -v".format(python_exe=project_cfg.PYTHON_3_EXECUTABLE,
                                                          test_dir=project_cfg.TEST_DIR)
        )

        _run_unit_tests_command(project_cfg.PYTHON_2_EXECUTABLE, run_unit_tests_2_command)
        _run_unit_tests_command(project_cfg.PYTHON_3_EXECUTABLE, run_unit_tests_3_command)

    print("\n********************************************************************************\n"
          "*                           Done (Running Python Tests)                        *\n"
          "********************************************************************************\n")

    pause("Press enter to exit...")


def _run_unit_tests_command(python_exe, command):
    print("Python executable: {PYTHON_EXECUTABLE}\n".format(PYTHON_EXECUTABLE=python_exe) +
          "          Command: " + command)
    os.system(command)

if __name__ == '__main__':
    main()

"""
Runs unit tests using default Python exe, then generates and opens coverage
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
          "*                   Running Tests and Generating Coverage                      *\n"
          "********************************************************************************\n")

    run_coverage_for_source_command = (
        "{python_exe} -m coverage run --omit {cov_ignore} --branch "
        "--source {source_dir} -m py.test {test_dir} -v".format(python_exe=project_cfg.DEFAULT_PYTHON_EXECUTABLE,
                                                                cov_ignore=project_cfg.COVERAGE_IGNORE_FILES,
                                                                source_dir=project_cfg.SOURCE_CODE_DIR,
                                                                test_dir=project_cfg.TEST_DIR)
    )

    generate_html_for_coverage_command = (
        "{python_exe} -m coverage html -d {cov_output_dir}".format(python_exe=project_cfg.DEFAULT_PYTHON_EXECUTABLE,
                                                                   cov_output_dir=project_cfg.COVERAGE_OUTPUT_DIR)
    )

    open_html_coverage_command = "{cov_output_dir}\\index.html".format(cov_output_dir=project_cfg.COVERAGE_OUTPUT_DIR)

    os.chdir(project_cfg.SOURCE_CODE_DIR)
    print(run_coverage_for_source_command)
    os.system(run_coverage_for_source_command)
    os.system(generate_html_for_coverage_command)

    print("\n********************************************************************************\n"
          "*                  Done (Running Tests and Generating Coverage)                *\n"
          "********************************************************************************\n")

    os.system(open_html_coverage_command)

    pause("Press enter to exit...")

if __name__ == '__main__':
    main()

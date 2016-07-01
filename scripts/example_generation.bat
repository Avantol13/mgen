::  ___  ___          _        _____                           _              ::
::  |  \/  |         (_)      |  __ \                         | |             ::
::  | .  . |_   _ ___ _  ___  | |  \/ ___ _ __   ___ _ __ __ _| |_ ___  _ __  ::
::  | |\/| | | | / __| |/ __| | | __ / _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__| ::
::  | |  | | |_| \__ \ | (__  | |_\ \  __/ | | |  __/ | | (_| | || (_) | |    ::
::  \_|  |_/\__,_|___/_|\___|  \____/\___|_| |_|\___|_|  \__,_|\__\___/|_|    ::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: Generate a midi, pdf, and Python pkl file by forcing a probability file,
:: output path, composition name, and key.

:::::::::::::::::::::::::::::::: CONFIGURATION :::::::::::::::::::::::::::::::::
@echo OFF
set MUSIC_GENERATOR_CLI="..\main.py"
set PYTHON_PATH="D:\Python27\python.exe"

set STYLE_FILE_PATH="..\styles\default.cfg"
set COMPOSITION_NAME="EXAMPLE"
set FORCE_KEY="G"

:: If not specified, will default to 8
set MELODY_TRACK_BARS=4
set CHORDS_TRACK_BARS=4

set REPEAT_TRACKS=1
set START_BAR=1

:: Different options for paths below
:: Default directory and name (if no argument specified)
set PKL_OUTPUT_PATH=
:: Default name, specific directory
:: NOTE: Don't use relative paths, put \\ at end
set MIDI_OUTPUT_PATH="C:\\Temp\\music_generator\\"
:: Specific directory and filename
:: NOTE: Don't use relative paths
set PDF_OUTPUT_PATH="C:\\Temp\\music_generator\\example.pdf"

:::::::::::::::::::::::::::::::::: EXECUTION :::::::::::::::::::::::::::::::::::
%PYTHON_PATH% %MUSIC_GENERATOR_CLI% --style_file_path %STYLE_FILE_PATH%^
 --melody_track %MELODY_TRACK_BARS% --chords_track %CHORDS_TRACK_BARS%^
 --repeat_tracks %REPEAT_TRACKS% --start_bar %START_BAR%^
 --composition_name %COMPOSITION_NAME% --key %FORCE_KEY%^
 --generate_midi %MIDI_OUTPUT_PATH% --generate_pdf %PDF_OUTPUT_PATH%^
 --generate_pickle %PKL_OUTPUT_PATH% --verbose

pause

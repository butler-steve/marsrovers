#!/bin/bash
#
# Shell script monitors the filesystem and run mamba on any
# changed .py files within the src sub-directory.
#
# If a file PATH/SOURCE.py is modified, the testrunner looks for another file called
#   PATH/spec/spec_SOURCE.py
# If that file is found, then it is run using mamba.  Otherwise PATH/SOURCE.py is passed to mamba
#
# DEPENDENCIES:
# o python 3.5.1
# o mamba (0.8.6)
# o watchdog (0.8.3)
# o ./monitor_file_changes.sh (in the same directory)
#
# USAGE:
# > cd watchdog
# > ./testrunner.sh

this_src_dir="`pwd`/src"
if [[ ! $PYTHONPATH == *"$this_src_dir"* ]]
then
    echo "Adding src dir to PYTHONPATH..."
    export PYTHONPATH=$PYTHONPATH:$this_src_dir
fi
echo "Starting directory watch..."
watchmedo shell-command --patterns=*.py --recursive --command="./monitor_file_changes.sh \${watch_event_type} \${watch_src_path}" ./src


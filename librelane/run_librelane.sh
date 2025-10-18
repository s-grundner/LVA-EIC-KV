#!/usr/bin/env bash

# =====================================================
# Author: Simon Dorrer
# Last Modified: 02.10.2025
# Description: This .sh file switches to the SKY130 PDK, runs the LibreLane flow and opens the layout in the OpenROAD GUI.
# =====================================================

set -e -x

cd $(dirname "$0")

# Switch to sky130A PDK
source sak-pdk-script.sh sky130A sky130_fd_sc_hd > /dev/null

# Run LibreLane
librelane --manual-pdk config.json

# Open Layout in OpenROAD GUI
librelane --manual-pdk config.json --last-run --flow OpenInOpenROAD

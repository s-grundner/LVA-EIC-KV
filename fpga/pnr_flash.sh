#!/usr/bin/env bash

# =====================================================
# Author: Simon Dorrer
# Last Modified: 06.10.2025
# Description: This .sh file synthesizes, places & routes (PNR) and flashes the Verilog design onto a Lattice iCE40 FPGA Stick.
# =====================================================

set -e -x

cd $(dirname "$0")

name=$1

RTL=${RTL:-../verilog/src}

# Synthesize
yosys -p "synth_ice40 -json ${name}.json" "$RTL"/"$name".v

# Place & Route
nextpnr-ice40 \
	--hx1k \
	--package tq144 \
	--json ${name}.json \
	--pcf io.pcf --pcf-allow-unconstrained \
	--asc ${name}.asc \
	--freq 12 \
	--report timing.rpt

# Generate .bin file
icepack ${name}.asc ${name}.bin

# Flash .bin file to FPGA
iceprog ${name}.bin

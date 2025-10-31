# *************************************************************************** #
# @file    : test_osc.py                                                      #
# @author  : @s-grundner                                                      #
# @license : Apache-2.0                                                       #
# @brief   : Oscillator Module Testbench for Cocotb.                          #
# *************************************************************************** #

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer, ValueChange
from cocotb.types import LogicArray

import numpy as np

# -------------------------------- Constants -------------------------------- #

midi_note_max = 128
midi_note_min = 21
midi_note_a4 = 69
keys_per_octave = 12
f_a4_hz = 440

f_clk_hz = 3_500_000
f_clk_half_hz = f_clk_hz / 2

# -------------------------- Calculation functions -------------------------- #

def get_freq_from_note(note):
    return f_a4_hz * (2 ** ((note - midi_note_a4) / keys_per_octave))

def get_octave_freqs(index):
    base = index * keys_per_octave + midi_note_min
    return np.array([f_a4_hz * (2 ** ((n - midi_note_a4) / keys_per_octave)) for n in range(base, base+keys_per_octave)])

def octave_to_cnts(octave_freqs):
    return [int(f_clk_half_hz // f) for f in octave_freqs]

def octave_from_to(from_idx, to_idx):
    octave_freqs = get_octave_freqs(from_idx)
    octave_cnts = octave_to_cnts(octave_freqs)
    shift_amount = abs(to_idx - from_idx)
    
    if from_idx < to_idx:
        return np.array(octave_cnts) >> shift_amount
    else:
        return np.array(octave_cnts) << shift_amount

def cnt_from_note(note, stored_octave=8):
    actual_note = 0 if note < 21 else note - 21
    octave = actual_note // keys_per_octave
    note_in_octave = actual_note % keys_per_octave
    octave_cnts = octave_from_to(stored_octave, octave)
    return octave_cnts[note_in_octave].astype(int)

@cocotb.test()
@cocotb.parametrize(note=[21, 40, 69, 88, 108, 127])
async def counting_test(dut, note):
    dut._log.info("Start")

    clock = Clock(dut.clk, int(np.round(1_000_000_000/f_clk_hz)), unit="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Resetting DUT")
    dut.nrst.value = 0
    dut.noteOnStrb.value = 0
    dut.noteOffStrb.value = 0
    dut.oscHalfCntPeriod.value = 0
    dut.ch.value = 0

    await ClockCycles(dut.clk, 10)
    dut.nrst.value = 1
    await ClockCycles(dut.clk, 5)

    dut.ch.value = 1
    cnt = int(cnt_from_note(note, stored_octave=8))
    dut._log.info(f"Setting note {note} with cnt {cnt}")
    dut.oscHalfCntPeriod.value = LogicArray.from_unsigned(cnt, 16)

    # generate strobe and start timing
    dut.noteOnStrb.value = 1
    tic = cocotb.utils.get_sim_time('ns')
    await ClockCycles(dut.clk, 1)
    dut.noteOnStrb.value = 0
    await ValueChange(dut.wave)
    toc = cocotb.utils.get_sim_time('ns')   
    
    f_ideal = get_freq_from_note(note)
    f_meas = 1_000_000_000 / (2 * (toc - tic))
    error_percent = abs(f_meas - f_ideal) / f_ideal * 100

    dut._log.info(f"Ideal freq: {f_ideal:.2f} Hz, Measured freq: {f_meas:.2f} Hz, Error: {error_percent:.4f} %")

    assert error_percent < 5.0, f"Frequency error too high: {error_percent:.4f} %"
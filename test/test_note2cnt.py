# *************************************************************************** #
# @file    : test_note2cnt.py                                                 #
# @author  : @s-grundner                                                      #
# @license : Apache-2.0                                                       #
# @brief   : Note Lookup Module Testbench for Cocotb.                         #
# *************************************************************************** #

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

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
    return octave_cnts[note_in_octave]

# ------------------------------- Test Cases -------------------------------- #

@cocotb.test()
@cocotb.parametrize(test_note=[0, 69, 127])
async def lookup_test(dut, test_note):
    clock = Clock(dut.clk, np.round(1_000_000_000/f_clk_hz), unit="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Resetting DUT")
    dut.nrst.value = 0
    dut.note.value = 0
    await ClockCycles(dut.clk, 10)
    dut.nrst.value = 1
    await ClockCycles(dut.clk, 1)

    dut.note.value = test_note # MIDI note number
    expected_cnt = cnt_from_note(test_note)
    dut._log.info(f"Testing MIDI note {test_note}, expects cnt {expected_cnt}")
    
    await ClockCycles(dut.clk, 10)
    assert int(dut.halfCntPeriod.value) == expected_cnt, f"actual value {dut.halfCntPeriod.value}"
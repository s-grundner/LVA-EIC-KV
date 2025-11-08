# *************************************************************************** #
# @file    : test_osc.py                                                      #
# @author  : @s-grundner                                                      #
# @license : Apache-2.0                                                       #
# @brief   : Oscillator Module Testbench for Cocotb.                          #
# *************************************************************************** #

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, ValueChange, Timer, First
from cocotb.types import LogicArray

import sg_utils as sg

@cocotb.test()
@cocotb.parametrize(
    note=[21, 40, 69, 88, 108, 127],
    viewable=[True]
    )
async def counting_test(dut, note, viewable):
    clock = Clock(dut.clk, sg.t_clk_ns, unit="ns")
    cocotb.start_soon(clock.start())

    rom_emulation = sg.octave_to_cnts(sg.get_octave_freqs(8))
    base_note = (note - sg.midi_note_min) % sg.keys_per_octave
    back_shift = 8 - (note - sg.midi_note_min) // sg.keys_per_octave
    base_cnt = rom_emulation[base_note]

    # Reset
    dut._log.info("Resetting DUT")
    dut.nrst.value = 0
    dut.noteOnStrb.value = 0
    dut.noteOffStrb.value = 0
    dut.oscBaseCntPeriod.value = 0
    dut.ch.value = 0

    await ClockCycles(dut.clk, 10)
    dut.nrst.value = 1
    await ClockCycles(dut.clk, 5)

    dut.ch.value = 1
    cnt = int(sg.cnt_from_note(note, stored_octave=8))
    dut._log.info(f"Setting note {note} with cnt {cnt}")
    dut.oscBaseCntPeriod.value = base_cnt & 0x7F
    dut.shift.value = back_shift

    # generate strobe and start timing
    dut.noteOnStrb.value = 1
    await ClockCycles(dut.clk, 1)
    dut.noteOnStrb.value = 0
    dt = await sg.meas_t_period(dut.wave)
    
    (f_meas, error_percent) = sg.freq_error(note, dt)
    f_ideal = sg.get_freq_from_note(note)
    dut._log.info(f"Ideal freq: {f_ideal:.2f} Hz, Measured freq: {f_meas:.2f} Hz, Deviation: {error_percent:.4f} %")
    assert error_percent < 5.0, f"Frequency error too high: {error_percent:.4f} %"

    if viewable:
        # Wait to observe Waveform (This is optional and requires long simulation time)
        await ValueChange(dut.wave)
        await ValueChange(dut.wave)
        await ValueChange(dut.wave)

    # Turn note off
    dut.noteOffStrb.value = 1
    await ClockCycles(dut.clk, 1)
    dut.noteOffStrb.value = 0
    # check if waveform does not change anymore
    timeout_ns = int(1_000_000_000*2/f_ideal)
    assert await sg.wave_off(dut.wave, timeout_ns), "Waveform did not stop after note off"
    
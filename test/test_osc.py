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
    viewable=[False]
    )
async def counting_test(dut, note, viewable):
    clock = Clock(dut.clk, sg.t_clk_ns, unit="ns")
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
    cnt = int(sg.cnt_from_note(note, stored_octave=8))
    dut._log.info(f"Setting note {note} with cnt {cnt}")
    dut.oscHalfCntPeriod.value = LogicArray.from_unsigned(cnt, 16)

    # generate strobe and start timing
    dut.noteOnStrb.value = 1
    tic = cocotb.utils.get_sim_time('ns')
    await ClockCycles(dut.clk, 1)
    dut.noteOnStrb.value = 0
    await ValueChange(dut.wave)
    toc = cocotb.utils.get_sim_time('ns')   
    
    f_ideal = sg.get_freq_from_note(note)
    f_meas = 1_000_000_000 / (2 * (toc - tic))
    error_percent = abs(f_meas - f_ideal) / f_ideal * 100

    dut._log.info(f"Ideal freq: {f_ideal:.2f} Hz, Measured freq: {f_meas:.2f} Hz, Error: {error_percent:.4f} %")
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
    t_wait_ns = int(1_000_000_000*2/f_ideal) # 2 periods
    timeout = Timer(t_wait_ns, 'ns')
    change = ValueChange(dut.wave)
    result = await First(timeout, change)
    assert result is timeout, "Waveform changed after note off!"
    
    # Turn note off again to check idempotency
    dut.noteOffStrb.value = 1
    await ClockCycles(dut.clk, 1)
    dut.noteOffStrb.value = 0

# *************************************************************************** #
# @file    : test_note2cnt.py                                                 #
# @author  : @s-grundner                                                      #
# @license : Apache-2.0                                                       #
# @brief   : Note Lookup Module Testbench for Cocotb.                         #
# *************************************************************************** #

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

import sg_utils as sg

@cocotb.test()
@cocotb.parametrize(test_note=[0, 69, 127])
async def lookup_test(dut, test_note):
    clock = Clock(dut.clk, sg.t_clk_ns, unit="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Resetting DUT")
    dut.nrst.value = 0
    dut.note.value = 0
    await ClockCycles(dut.clk, 10)
    dut.nrst.value = 1
    await ClockCycles(dut.clk, 1)

    dut.note.value = test_note # MIDI note number
    expected_cnt = sg.cnt_from_note(test_note)
    dut._log.info(f"Testing MIDI note {test_note}, expects cnt {expected_cnt}")
    
    await ClockCycles(dut.clk, 10)
    # Re add the Always 1 MSB to restore the original cnt value
    base = dut.baseCntPeriod.value.to_unsigned() | 0b10000000
    shift = dut.shift.value.to_unsigned()
    recreated_cnt = base << shift
    assert recreated_cnt == expected_cnt, f"actual value {recreated_cnt}"
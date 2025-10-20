# *************************************************************************** #
# @file    : test_note2cnt.py                                                 #
# @author  : @s-grundner                                                      #
# @license : Apache-2.0                                                       #
# @brief   : Note Lookup Module Testbench for Cocotb.                         #
# *************************************************************************** #

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Timer

@cocotb.test()
# Parametrize edge cases:
# - Min and max note values
# @cocotb.parametrize(reset_type=["sync", "overflow"])
async def lookup_test(dut):
    dut._log.info("Start")

    clock = Clock(dut.clk, 286, unit="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Resetting DUT")
    dut.nrst.value = 0
    dut.note.value = 0
    await ClockCycles(dut.clk, 10)
    dut.nrst.value = 1
    await ClockCycles(dut.clk, 1)

    dut.note.value = 69
    await ClockCycles(dut.clk, 10)
    assert dut.halfCntPeriod.value == 3968, f"actual value {dut.halfCntPeriod.value}"
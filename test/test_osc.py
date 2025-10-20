# *************************************************************************** #
# @file    : test_osc.py                                                      #
# @author  : @s-grundner                                                      #
# @license : Apache-2.0                                                       #
# @brief   : Oscillator Module Testbench for Cocotb.                          #
# *************************************************************************** #

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer, RisingEdge
import numpy as np

f_clk_hz = 3_500_000

@cocotb.test()
@cocotb.parametrize(state=["disabled", "enabled"], inputs=[(60, ), 72])
async def counting_test(dut, state, inputs):
    dut._log.info("Start")

    clock = Clock(dut.clk, int(np.round(1/f_clk_hz)), unit="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Resetting DUT")
    dut.nrst.value = 0
    await ClockCycles(dut.clk, 10)
    dut.nrst.value = 1
    await ClockCycles(dut.clk, 1)

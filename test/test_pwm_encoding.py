# *************************************************************************** #
# @file    : test_pwm.py                                                      #
# @author  : @s-grundner                                                      #
# @license : Apache-2.0                                                       #
# @brief   : PWM Module Testbench for Cocotb.                                 #
# *************************************************************************** #

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

import numpy as np

f_clk_hz = 3_500_000

@cocotb.test()
@cocotb.parametrize(active_oscs=[0b0, 0b1, 0b11])
async def pwm_encode_active_oscs(dut, active_oscs):
    clock = Clock(dut.clk, int(np.round(1_000_000_000/f_clk_hz)), unit="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Resetting DUT")
    dut.nrst.value = 0
    dut.activeOscs.value = 0
    await ClockCycles(dut.clk, 10)
    dut.nrst.value = 1
    await ClockCycles(dut.clk, 1)

    dut.activeOscs.value = active_oscs

    await ClockCycles(dut.clk, 1)
    period_cnt = dut.OSC_VOICES.value.to_unsigned()
    on_cnt = dut.nActiveOscs.value.to_unsigned()

    assert on_cnt == bin(active_oscs).count("1"), f"Expected on_cnt {bin(active_oscs).count('1')} but got {on_cnt}"
    
    for _ in range(5):
        await ClockCycles(dut.clk, period_cnt+1)
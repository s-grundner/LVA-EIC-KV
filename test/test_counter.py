# *************************************************************************** #
# @file    : test_counter.py                                                  #
# @author  : @s-grundner                                                      #
# @license : Apache-2.0                                                       #
# @brief   : Counter Module Testbench for Cocotb. This directly tests the     #
#              implementation and NOT the testbench in ./benches              #
# *************************************************************************** #

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Timer

@cocotb.test()
@cocotb.parametrize(reset_type=["sync", "overflow"])
async def counting_test(dut, reset_type):
    dut._log.info("Start")

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Resetting DUT")
    dut.nrstSync.value = 0
    dut.nrst.value = 0
    await ClockCycles(dut.clk, 10)
    dut.nrst.value = 1
    dut.nrstSync.value = 1
    await ClockCycles(dut.clk, 1)

    dut._log.info("Test counting behavior")
    assert dut.count.value == 0, f"Counter value should be 0 but is {dut.count.value}"
    await ClockCycles(dut.clk, 1)
    assert dut.count.value == 1, f"Counter value should be 5 but is {dut.count.value}"
    await ClockCycles(dut.clk, 5)
    assert dut.count.value == 6, f"Counter value should be 5 but is {dut.count.value}"
    
    if reset_type == "sync":
        dut._log.info("Testing synchronous reset")
        dut.nrstSync.value = 0
        await ClockCycles(dut.clk, 1)

        # Counts up one more time after reset as the reset is applied synchronously on the next rising edge
        assert dut.count.value == 7, f"Counter value should be 7 but is {dut.count.value}"
        await ClockCycles(dut.clk, 1)
        assert dut.count.value == 0, f"Counter value should be 0 but is {dut.count.value}"
        await ClockCycles(dut.clk, 20)

        # Counter stays 0 while reset is active
        assert dut.count.value == 0, f"Counter value should be 0 but is {dut.count.value}"
        dut.nrstSync.value = 1
        await ClockCycles(dut.clk, 2)
        assert dut.count.value == 1, f"Counter value should be 1 but is {dut.count.value}"
        
    else:
        dut._log.info("Testing overflow reset")
        await ClockCycles(dut.clk, 9) # Count to 15
        assert dut.count.value == 15, f"Counter value should be 15 but is {dut.count.value}" 
        await ClockCycles(dut.clk, 1)
        assert dut.count.value == 0, f"Counter value should be 0 but is {dut.count.value}"
        await ClockCycles(dut.clk, 20)

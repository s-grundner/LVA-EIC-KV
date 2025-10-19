# *************************************************************************** #
# @file    : test_counter.py                                                  #
# @author  : @s-grundner                                                      #
# @license : Apache-2.0                                                       #
# @brief   : Counter Module Testbench for Cocotb. This directly tests the     #
#              implementation and NOT the testbench in ./benches              #
# *************************************************************************** #

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

# *************************************************************************** #
#                           Test Counting behaviour                           #
# *************************************************************************** #
@cocotb.test()
async def counting_test(dut):
    dut._log.info("Start")

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.nrstSync.value = 0
    dut.nrst.value = 0
    await ClockCycles(dut.clk, 10)
    dut.nrst.value = 1
    dut.nrstSync.value = 1

    dut._log.info("Test counting behavior")
    await ClockCycles(dut.clk, 1)
    assert dut.count.value == 0, f"Counter value should be 0 but is {dut.count.value}"
    await ClockCycles(dut.clk, 1)
    assert dut.count.value == 1, f"Counter value should be 5 but is {dut.count.value}"
    # await ClockCycles(dut.clk, 10)
    # assert dut.count.value == 15, f"Counter value should be 15 but is {dut.count.value}" 

# *************************************************************************** #
#                       Test Synchronous Reset behaviour                      #
# *************************************************************************** #
@cocotb.test()
async def sync_reset_test(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.nrstSync.value = 0
    dut.nrst.value = 0
    await ClockCycles(dut.clk, 10)
    dut.nrst.value = 1
    dut.nrstSync.value = 1
    
    dut._log.info("Test async reset behavior")
    assert dut.count.value == 0, f"Counter value should be 0 but is {dut.count.value}"
    await ClockCycles(dut.clk, 8)
    assert dut.count.value == 7, f"Counter value should be 7 but is {dut.count.value}"
    # Apply asynchronous reset
    dut.nrst.value = 0
    assert dut.count.value == 7, f"Counter value should be 7 but is {dut.count.value}"
    await ClockCycles(dut.clk, 1)
    assert dut.count.value == 0, f"Counter value should be 0 but is {dut.count.value}"

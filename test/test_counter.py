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

    clock = Clock(dut.clk_i, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.nrstSync_i.value = 0
    dut.nrst_i.value = 0
    await ClockCycles(dut.clk_i, 10)
    dut.nrst_i.value = 1
    dut.nrstSync_i.value = 1

    dut._log.info("Test counting behavior")
    await ClockCycles(dut.clk_i, 1)
    assert dut.count_o.value == 0, f"Counter value should be 0 but is {dut.count.value}"
    await ClockCycles(dut.clk_i, 1)
    assert dut.count_o.value == 1, f"Counter value should be 5 but is {dut.count.value}"
    # await ClockCycles(dut.clk, 10)
    # assert dut.count.value == 15, f"Counter value should be 15 but is {dut.count.value}" 

# *************************************************************************** #
#                       Test Synchronous Reset behaviour                      #
# *************************************************************************** #
@cocotb.test()
async def sync_reset_test(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk_i, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.nrstSync_i.value = 0
    dut.nrst_i.value = 0
    await ClockCycles(dut.clk_i, 10)
    dut.nrst_i.value = 1
    dut.nrstSync_i.value = 1
    
    dut._log.info("Test async reset behavior")
    assert dut.count_o.value == 0, f"Counter value should be 0 but is {dut.count_o.value}"
    await ClockCycles(dut.clk_i, 8)
    assert dut.count_o.value == 7, f"Counter value should be 7 but is {dut.count_o.value}"
    # Apply asynchronous reset
    dut.nrst_i.value = 0
    assert dut.count_o.value == 7, f"Counter value should be 7 but is {dut.count_o.value}"
    await ClockCycles(dut.clk_i, 1)
    assert dut.count_o.value == 0, f"Counter value should be 0 but is {dut.count_o.value}"

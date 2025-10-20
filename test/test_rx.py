# *************************************************************************** #
# @file    : test_rx.py                                                       #
# @author  : @s-grundner                                                      #
# @license : Apache-2.0                                                       #
# @brief   : RX Module Testbench for Cocotb.                                  #
# *************************************************************************** #

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

# -------------------------------- Varaibles -------------------------------- #

baud_rate = 31250
f_clk_hz = 3_500_000
cycles_per_bit = f_clk_hz // baud_rate

# ------------------------------- Test Cases -------------------------------- #

@cocotb.test()
@cocotb.parametrize(data_frame=["single", "multi", "corrupt", "midi"])
async def parallelize_data(dut, data_frame):
    dut._log.info("Start")

    # Clock Frequency: 100 kHz
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Resetting DUT")
    dut.nrst.value = 0
    await ClockCycles(dut.clk, 10)
    dut.nrst.value = 1
    await ClockCycles(dut.clk, 1)

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
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

    dut._log.info("Test project behavior")
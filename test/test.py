# *************************************************************************** #
# @file    : test.py                                                          #
# @author  : @s-grundner                                                      #
# @license : Apache-2.0                                                       #
# @brief   : Toplevel Design Testbench for Cocotb.                            #
# *************************************************************************** #

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
@cocotb.parametrize(voices=["idle", "monophonic", "polyphonic", "arpeggiator", "voice overflow"])
async def test_project(dut, voices):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    match voices:
        case "idle":
            dut._log.info("Testing idle state")
            await ClockCycles(dut.clk, 100)
        case "monophonic":
            dut._log.info("Testing monophonic midi input - single note")
        case "polyphonic":
            dut._log.info("Testing polyphonic midi input - multiple notes at once")
        case "arpeggiator":
            dut._log.info("Testing arpeggiator mode - multiple notes in sequence")
        case "voice overflow":
            dut._log.info("Testing voice overflow - more notes than available voices")


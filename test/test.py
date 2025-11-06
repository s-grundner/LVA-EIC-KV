# *************************************************************************** #
# @file    : test.py                                                          #
# @author  : @s-grundner                                                      #
# @license : Apache-2.0                                                       #
# @brief   : Toplevel Design Testbench for Cocotb.                            #
# *************************************************************************** #

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer, ValueChange

import sg_utils as sg

# ------------------------------- Test Cases -------------------------------- #

@cocotb.test()
@cocotb.parametrize(voices=["idle", "monophonic", "polyphonic", "arpeggiator", "voice overflow"])
async def test_project(dut, voices):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, sg.t_clk_ns, unit="ns") 
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.rxDataIn.value = 1
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
            rx_data = [0x90, 0x60, 0x00]  # Note On, Ch0, Middle C, dummy velocity
            for r in rx_data:
                dut.rxDataIn.value = 0  # Start bit
                await ClockCycles(dut.clk, sg.cycles_per_bit)  # Wait for some time
                for i in range(8):
                    dut.rxDataIn.value = (r >> i) & 0x1  # Data bits
                    await ClockCycles(dut.clk, sg.cycles_per_bit)
                dut.rxDataIn.value = 1  # Stop bit
                await ClockCycles(dut.clk, sg.cycles_per_bit)  # Wait for some time

            await ValueChange(dut.ch0)
            tic = cocotb.utils.get_sim_time('ns')
            await ValueChange(dut.ch0)
            toc = cocotb.utils.get_sim_time('ns')   
            
            f_ideal = sg.get_freq_from_note(rx_data[1])
            f_meas = 1_000_000_000 / (2 * (toc - tic))
            error_percent = abs(f_meas - f_ideal) / f_ideal * 100

            dut._log.info(f"Ideal freq: {f_ideal:.2f} Hz, Measured freq: {f_meas:.2f} Hz, Error: {error_percent:.4f} %")

            assert error_percent < 5.0, f"Frequency error too high: {error_percent:.4f} %"

        case "polyphonic":
            dut._log.info("Testing polyphonic midi input - multiple notes at once")

        case "arpeggiator":
            dut._log.info("Testing arpeggiator mode - multiple notes in sequence")

        case "voice overflow":
            dut._log.info("Testing voice overflow - more notes than available voices")


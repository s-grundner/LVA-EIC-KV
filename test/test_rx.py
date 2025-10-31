# *************************************************************************** #
# @file    : test_rx.py                                                       #
# @author  : @s-grundner                                                      #
# @license : Apache-2.0                                                       #
# @brief   : RX Module Testbench for Cocotb.                                  #
# *************************************************************************** #

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
import numpy as np

# -------------------------------- Varaibles -------------------------------- #

baud_rate = 31250
f_clk_hz = 3_500_000
cycles_per_bit = f_clk_hz // baud_rate

# ------------------------------- Test Cases -------------------------------- #

@cocotb.test()
@cocotb.parametrize(data_frame=["single", "multi", "midi"])
async def parallelize_data(dut, data_frame):
    clock = Clock(dut.clk, int(np.round(1_000_000_000/f_clk_hz)), unit="ns") 
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Resetting DUT")
    dut.nrst.value = 0
    dut.rxData.value = 1
    await ClockCycles(dut.clk, 10)
    dut.nrst.value = 1
    await ClockCycles(dut.clk, 1)

    dut._log.info(f"Testing data a {data_frame} frame")

    match data_frame: # Tuples of (data_byte, data_bits, data_valid)
        case "single":
            test_data = [(0xCC, 8)]
        case "multi":
            test_data = [(0x90, 8), (0x45, 8), (0x60, 8), (0x80, 8), (0x45, 8), (0x40, 8)]
        case "corrupt":
            # As the MIDI protocol does not implement any parity or checksum.
            # A single dataframe of corrupted data could be detected, but following
            # frames could be invalid again. If an error occurs and a oscillator hangs, reset the device.
            # test_data = [(0x865, 12), (0x44, 8)]
            test_data = [(0x00, 0)]
        case "midi":
            test_data = [(0x90, 8), (0x3C, 8), (0x7F, 8), (0x80, 8), (0x3C, 8), (0x00, 8)] # Note On 60, Vel 127; Note Off 60, Vel 0
    
    for byte in test_data:
        # Start Bit
        dut.rxData.value = 0
        await ClockCycles(dut.clk, cycles_per_bit)

        for i in range(byte[1]):
            dut.rxData.value = (byte[0] >> i) & 0x1
            await ClockCycles(dut.clk, cycles_per_bit)

        # Stop Bit
        dut.rxData.value = 1
        await ClockCycles(dut.clk, cycles_per_bit)

        # Wait for DUT to process data
        await ClockCycles(dut.clk, cycles_per_bit * 2)

        # Check received data
        assert dut.payload.value.to_unsigned() == byte[0], f"Expected {byte[0]:#04x}, got {dut.payload.value.to_unsigned():#04x}"

    await ClockCycles(dut.clk, cycles_per_bit*20)

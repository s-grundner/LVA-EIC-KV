# *************************************************************************** #
# @file    : test_midi.py (Compound)                                          #
# @author  : @s-grundner                                                      #
# @license : Apache-2.0                                                       #
# @brief   : MIDI Module Testbench for Cocotb. Shows that a MIDI Word is      #
#           correctly split into its components.                              #
# *************************************************************************** #

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge

import sg_utils as sg

@cocotb.test()
@cocotb.parametrize(
        mode=["with rx"],
        input_bytes=[   
            [0x90, 0x60, 0x00],
            [0x80, 0x06, 0x00],
            [0x91, 0x40, 0x00],
            [0x81, 0x7F, 0x00],
            [0x90, 0x60, 0x00, 0x80, 0x60, 0x00],
            [0x91, 0x40, 0x00, 0x81, 0x7F, 0x00]
        ]
    )

async def midi_test(dut, input_bytes, mode):
    clock = Clock(dut.clk, sg.t_clk_ns, unit="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Resetting DUT")
    dut.nrst.value = 0
    dut.midiByte_from_tb.value = 0
    dut.midiByteValid_from_tb.value = 0
    await ClockCycles(dut.clk, 10)
    dut.nrst.value = 1
    await ClockCycles(dut.clk, 1)

    dut._log.info(f"Feeding input bytes: {input_bytes}")

    if mode == "with rx":
        dut._log.info("Enabling RX module")
        dut.enableRx.value = 1

        for byte in input_bytes:
            dut.rxData.value = 0  # Start bit
            await ClockCycles(dut.clk, sg.cycles_per_bit)  # MIDI baud rate: 31250 bps

            for i in range(8):
                dut.rxData.value = (byte >> i) & 0x1
                await ClockCycles(dut.clk, sg.cycles_per_bit)

            dut.rxData.value = 1  # Stop bit
            await ClockCycles(dut.clk, sg.cycles_per_bit)
            await FallingEdge(dut.dataReady)
            # Now the MIDI byte should be at the input of the MIDI module
            
        await ClockCycles(dut.clk, sg.cycles_per_bit*40)
        
    elif mode == "standalone":
        dut._log.info("Disabling RX module")
        dut.enableRx.value = 0
    
        for byte in input_bytes:
            dut.midiByte_from_tb.value = byte
            dut.midiByteValid_from_tb.value = 1
            await ClockCycles(dut.clk, 1)
            dut.midiByteValid_from_tb.value = 0
            await ClockCycles(dut.clk, 20)

        await ClockCycles(dut.clk, 100)

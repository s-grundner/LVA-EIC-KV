# *************************************************************************** #
# @file    : test.py                                                          #
# @author  : @s-grundner                                                      #
# @license : Apache-2.0                                                       #
# @brief   : Toplevel Design Testbench for Cocotb.                            #
# *************************************************************************** #

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer, ValueChange, First

import sg_utils as sg
import numpy as np

# ------------------------------- Test Cases -------------------------------- #

async def rx(dut, bytes):
    for r in bytes:
        # Start bit
        dut.rxDataIn.value = 0
        await ClockCycles(dut.clk, sg.cycles_per_bit)

        # Data bits
        for i in range(8):
            dut.rxDataIn.value = (r >> i) & 0x1
            await ClockCycles(dut.clk, sg.cycles_per_bit)

        # Stop bit
        dut.rxDataIn.value = 1
        await ClockCycles(dut.clk, sg.cycles_per_bit)

async def meas_t_period(signal):
    await ValueChange(signal)
    tic = cocotb.utils.get_sim_time('ns')
    await ValueChange(signal)
    toc = cocotb.utils.get_sim_time('ns')   
    return 2*(toc - tic)

@cocotb.test()
@cocotb.parametrize(voices=["monophonic", "polyphonic", "arpeggiator", "voice overflow", "voice override"])
async def test_project(dut, voices):
    dut._log.info("Start")

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
        case "monophonic":
            dut._log.info("Testing monophonic midi input - single note")

            # Construct MIDI Note On message and send it
            test_note_str = 'C'
            midi_note = sg.get_midi_from_key(test_note_str)  # Middle C
            rx_data = sg.construct_midi_bytes(0, midi_note, state='on')
            dut._log.info(f"Turn Note On and measure frequency of {test_note_str} (MIDI {midi_note})")
            await rx(dut, rx_data)

            # Measure frequency of the output waveform
            dt = await meas_t_period(dut.ch0)
            
            # Calculate and log frequency error
            (f_meas, err_percent) = sg.freq_error(midi_note, dt)
            dut._log.info(f"Measured Frequency: {f_meas:.2f} Hz, Error: {err_percent:.4f} %")
            assert err_percent < 5.0, f"Output frequency deviated too far from expected value"
            
            # Turn Note Off
            dut._log.info("Turn Note Off and verify waveform stops")
            rx_data = sg.construct_midi_bytes(0, midi_note, 'off')
            await rx(dut, rx_data)
            
            # Verify that waveform stops changing
            t_wait_ns = int(1_000_000_000*2/f_meas) # 2 periods
            timeout = Timer(t_wait_ns, 'ns')
            change = ValueChange(dut.ch0)
            result = await First(timeout, change)
            assert result is timeout, "Waveform changed after note off!"

        case "polyphonic":
            dut._log.info("Testing polyphonic midi input - multiple notes at once")
            (key1, key2) = ('A', 'E')
            (midi1, midi2) = (sg.get_midi_from_key(key1), sg.get_midi_from_key(key2))

            rx_data1 = sg.construct_midi_bytes(0, midi1)
            rx_data2 = sg.construct_midi_bytes(1, midi2)
            rx_data = rx_data1 + rx_data2
            await rx(dut, rx_data)
            
            dt0 = await meas_t_period(dut.ch0)
            (f_meas, err_percent) = sg.freq_error(midi1, dt0)
            dut._log.info(f"Key: Middle {key1}, Measured Frequency: {f_meas:.2f} Hz, Error: {err_percent:.4f} %")
            assert err_percent < 5.0, f"Output frequency deviated too far from expected value"

            dt1 = await meas_t_period(dut.ch1)
            (f_meas, err_percent) = sg.freq_error(midi2, dt1)
            dut._log.info(f"Key: Middle {key2}, Measured Frequency: {f_meas:.2f} Hz, Error: {err_percent:.4f} %")
            assert err_percent < 5.0, f"Output frequency deviated too far from expected value"

        case "arpeggiator":
            dut._log.info("Testing arpeggiator mode - multiple notes in sequence")

        case "voice overflow":
            dut._log.info("Testing voice overflow - more notes than available voices")

        case "voice override":
            dut._log.info("Testing voice override - a second note on occurs on the same channel without turning the previous note off")


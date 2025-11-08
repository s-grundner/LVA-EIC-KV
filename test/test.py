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

@cocotb.test()
@cocotb.parametrize(
    voice_setting=["monophonic", "polyphonic", "arpeggiator", "voice overflow", "voice override"],
    viewable=[False] # Set to True to make the waveform more easily observable in a waveform viewer
    )
async def test_project(dut, voice_setting, viewable):
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
    channel_signals = [dut.ch0, dut.ch1, dut.ch2, dut.ch3, dut.ch4, dut.ch5, dut.ch6]

    match voice_setting:
        case "monophonic":
            dut.testcase_indicator.value = 0
            dut._log.info("Testing monophonic midi input - single note")

            # Construct MIDI Note On message and send it
            test_note_str = 'C'
            midi_note = sg.get_midi_from_key(test_note_str)  # Middle C
            rx_data = sg.construct_midi_bytes(0, midi_note, state='on')
            dut._log.info(f"Turn Note On and measure frequency of {test_note_str} (MIDI {midi_note})")
            await rx(dut, rx_data)

            # Measure frequency of the output waveform
            dt = await sg.meas_t_period(dut.ch0)
            (f_meas, err_percent) = sg.freq_error(midi_note, dt)
            dut._log.info(f"Measured Frequency: {f_meas:.2f} Hz, Error: {err_percent:.4f} %")
            assert err_percent < 5.0, f"Output frequency deviated too far from expected value"
            
            if viewable:
                # Wait to observe Waveform (This is optional and requires long simulation time)
                await ValueChange(dut.ch0)
                await ValueChange(dut.ch0)
                await ValueChange(dut.ch0)
            
            # Turn Note Off
            dut._log.info("Turn Note Off and verify waveform stops")
            rx_data = sg.construct_midi_bytes(0, midi_note, 'off')
            await rx(dut, rx_data)
            
            # Verify that waveform stops changing
            timeout_ns = int(1_000_000_000*2/f_meas) # 2 periods
            assert await sg.wave_off(dut.ch0, timeout_ns), "Waveform did not stop after Note Off"

        case "polyphonic":
            dut.testcase_indicator.value = 1
            dut._log.info("Testing polyphonic midi input - multiple notes at once")
            keys = ['A', 'E', 'C']
            midis = [sg.get_midi_from_key(k) for k in keys]
            n_voices = len(midis)

            rx_data = []
            for i in range(n_voices):
                rx_data = rx_data + sg.construct_midi_bytes(i, midis[i], 'on')

            await rx(dut, rx_data)
            
            for i in range(n_voices):
                # Check if the correct frequency is output
                dt = await sg.meas_t_period(channel_signals[i])
                (f_meas, err_percent) = sg.freq_error(midis[i], dt)
                dut._log.info(f"Key: Middle {keys[i]}, Measured Frequency: {f_meas:.2f} Hz, Error: {err_percent:.4f} %")
                assert err_percent < 5.0, f"Output frequency deviated too far from expected value"

                if viewable:
                    await ValueChange(channel_signals[i])
                    await ValueChange(channel_signals[i])
                    await ValueChange(channel_signals[i])

            # Turn only one note off and check others still play
            rx_data = sg.construct_midi_bytes(0, midis[0], 'off')
            await rx(dut, rx_data)

            for i in range(1, n_voices):
                # Check if the correct frequency is output
                dt = await sg.meas_t_period(channel_signals[i])
                (f_meas, err_percent) = sg.freq_error(midis[i], dt)
                dut._log.info(f"Key: Middle {keys[i]}, Measured Frequency: {f_meas:.2f} Hz, Error: {err_percent:.4f} %")
                assert err_percent < 5.0, f"Output frequency deviated too far from expected value"

                if viewable:
                    await ValueChange(channel_signals[i])
                    await ValueChange(channel_signals[i])
                    await ValueChange(channel_signals[i])
            
            timeout_ns = int(1_000_000_000*2/sg.get_freq_from_note(midis[0]))
            assert await sg.wave_off(channel_signals[0], timeout_ns), "Waveform did not stop after Note Off"

        case "arpeggiator":
            dut.testcase_indicator.value = 2
            dut._log.info("Testing arpeggiator mode - multiple notes in sequence")
            keys = ['C', 'E', 'G', 'B', 'D']
            midis = [sg.get_midi_from_key(k) for k in keys]
            n_notes = len(midis)
            
            # Send On message, wait a few periods, send off message
            for i in range(n_notes):
                rx_data = sg.construct_midi_bytes(0, midis[i], 'on')
                await rx(dut, rx_data)

                # Check if the correct frequency is output
                dt = await sg.meas_t_period(dut.ch0) 
                (f_meas, err_percent) = sg.freq_error(midis[i], dt)
                dut._log.info(f"Key: Middle {keys[i]}, Measured Frequency: {f_meas:.2f} Hz, Error: {err_percent:.4f} %")
                assert err_percent < 5.0, f"Output frequency deviated too far from expected value"

                if viewable:
                    await ValueChange(dut.ch0)
                    await ValueChange(dut.ch0)
                    await ValueChange(dut.ch0)

                rx_data = sg.construct_midi_bytes(0, midis[i], 'off')
                await rx(dut, rx_data)
                
                timeout_ns = int(1_000_000_000*2/f_meas) # 2 periods
                assert await sg.wave_off(dut.ch0, timeout_ns), "Waveform did not stop after Note Off"

        case "voice overflow":
            dut.testcase_indicator.value = 3
            dut._log.info("Testing voice overflow - more notes than available voices")
            keys = ['A', 'E', 'C', 'G', 'B', 'D', 'F#']
            midis = [sg.get_midi_from_key(k) for k in keys]
            n_voices = len(midis)

            rx_data = []
            for i in range(n_voices):
                rx_data = rx_data + sg.construct_midi_bytes(i, midis[i], 'on')

            await rx(dut, rx_data)

            await ValueChange(dut.ch0)
            await ValueChange(dut.ch0)
            await ValueChange(dut.ch0)
            await ValueChange(dut.ch0)

        case "voice override":
            dut.testcase_indicator.value = 4
            dut._log.info("Testing voice override - a second note on occurs on the same channel without turning the previous note off")
            keys = ['C', 'E', 'G', 'B', 'D']
            midis = [sg.get_midi_from_key(k) for k in keys]
            n_notes = len(midis)
            
            # Send On message, wait a few periods, send off message
            for i in range(n_notes):
                rx_data = sg.construct_midi_bytes(0, midis[i], 'on')
                await rx(dut, rx_data)

                # Check if the correct frequency is output
                dt = await sg.meas_t_period(dut.ch0) 
                (f_meas, err_percent) = sg.freq_error(midis[i], dt)
                dut._log.info(f"Key: Middle {keys[i]}, Measured Frequency: {f_meas:.2f} Hz, Error: {err_percent:.4f} %")
                assert err_percent < 5.0, f"Output frequency deviated too far from expected value"

                if viewable:
                    await ValueChange(dut.ch0)
                    await ValueChange(dut.ch0)
                    await ValueChange(dut.ch0)
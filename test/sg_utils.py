import numpy as np

# Constants
midi_note_max = 128
midi_note_min = 21
midi_note_a4 = 69
keys_per_octave = 12
f_a4_hz = 440

# Timing
f_clk_hz = 3_500_000
f_clk_half_hz = f_clk_hz / 2
f_baud_hz = 31250
cycles_per_bit = int(f_clk_hz // f_baud_hz)
t_clk_ns = int(np.round(1_000_000_000/f_clk_hz))

# Calculation functions
def get_freq_from_note(note):
    return f_a4_hz * (2 ** ((note - midi_note_a4) / keys_per_octave))

def get_octave_freqs(index):
    base = index * keys_per_octave + midi_note_min
    return np.array([f_a4_hz * (2 ** ((n - midi_note_a4) / keys_per_octave)) for n in range(base, base+keys_per_octave)])

def octave_to_cnts(octave_freqs):
    return [int(f_clk_half_hz // f) for f in octave_freqs]

def octave_from_to(from_idx, to_idx):
    octave_freqs = get_octave_freqs(from_idx)
    octave_cnts = octave_to_cnts(octave_freqs)
    shift_amount = abs(to_idx - from_idx)
    if from_idx < to_idx:
        return np.array(octave_cnts) >> shift_amount
    else:
        return np.array(octave_cnts) << shift_amount

def cnt_from_note(note, stored_octave=8):
    actual_note = 0 if note < 21 else note - 21
    octave = actual_note // keys_per_octave
    note_in_octave = actual_note % keys_per_octave
    octave_cnts = octave_from_to(stored_octave, octave)
    return octave_cnts[note_in_octave].astype(int)

def get_midi_from_key(key: str, in_octave=4):
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    if key not in note_names:
        raise ValueError(f"Invalid note name: {key}")
    note_index = note_names.index(key)
    midi_number = (in_octave + 1) * keys_per_octave + note_index
    return midi_number

def construct_midi_bytes(channel, midi_note, state='on'):
    if state == 'on':
        status = 0x90 | (channel & 0x0F)
    else:
        status = 0x80 | (channel & 0x0F)
    return [status, midi_note & 0x7F, 0x00] # dummy velocity

def construct_midi_bytes_from_key(channel, key, in_octave=4, state='on'):
    midi_note = get_midi_from_key(key, in_octave)
    return construct_midi_bytes(channel, midi_note, state)

def freq_error(midi_note, delta_t_ns):
    f_ideal = get_freq_from_note(midi_note)
    f_meas = 1_000_000_000 / delta_t_ns
    error_percent = abs(f_meas - f_ideal) / f_ideal * 100
    return (f_meas, error_percent)

import cocotb
from cocotb.triggers import Timer, ValueChange, First

async def wave_off(signal, timeout_ns):
    timeout = Timer(timeout_ns, 'ns')
    change = ValueChange(signal)
    result = await First(timeout, change)
    return (result is timeout)

async def meas_t_period(signal):
    await ValueChange(signal)
    tic = cocotb.utils.get_sim_time('ns')
    await ValueChange(signal)
    toc = cocotb.utils.get_sim_time('ns')   
    return 2*(toc - tic)
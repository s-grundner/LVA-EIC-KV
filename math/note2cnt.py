import numpy as np

midi_note_max = 128
midi_note_min = 21
midi_note_a4 = 69
keys_per_octave = 12
f_a4_hz = 440

f_clk_hz = 3_500_000
f_clk_half_hz = f_clk_hz / 2

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
    return octave_cnts[note_in_octave]
`ifndef __GLOBAL
`define __GLOBAL

`define F_CLK_HZ 3_500_000
`define F_CLK_PERIOD_NS (1_000_000_000 / `F_CLK_HZ)
`define F_BAUD 31250
`define F_BAUD_PERIOD_NS (1_000_000_000 / `F_BAUD)

`define MIDI_CHANNEL 0  // MIDI channel 1
`define MIDI_PAYLOAD_BITS 8

// Oscillator settings
`define OSC_VOICES 2 // MAX 7
`define OSC_CNT_BW 16 // Counter bit width
`define OSC_ROM_BW 8 // Note ROM bit width

`endif  // __GLOBAL

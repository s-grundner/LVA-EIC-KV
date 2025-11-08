/*******************************************************************************
* @file    : synth.v                                                           *
* @author  : @s-grundner                                                       *
* @license : Apache-2.0                                                        *
* @brief   : Synthesis top module. This connects midi decoder and oscillator   *
*            stack.                                                            *
*******************************************************************************/

`default_nettype none
`ifndef __SYNTH
`define __SYNTH
`include "global.v"

module synth (
    input wire clk_i,
    input wire nrst_i,
    input wire rxData_i,
    output wire [`OSC_VOICES-1:0] oscOut_o,
    output wire activeOscPwm_o
);

    wire noteOnStrb;
    wire noteOffStrb;
    wire [`MIDI_NOTE_BW-1:0] note;
    
    wire midiByteValid;
    wire [`MIDI_PAYLOAD_BITS-1:0] midiByte;
    
    wire [`OSC_VOICES-1:0] activeOscs; // one bit per oscillator
    wire [`OSC_VOICES_BW-1:0] nActiveOscs; 
    wire [`OSC_ROM_BW-1:0] oscCmp;
    wire [3:0] oscShift;
    wire [`OSC_VOICES_BW-1:0] channel;

    // ---------------------------- Modules --------------------------------- //

    rx rx_inst (
        .clk_i(clk_i),
        .nrst_i(nrst_i),
        .rxData_i(rxData_i),
        .dataReady_o(midiByteValid),
        .midiData_o(midiByte)
    );

    midi midi_inst (
        .clk_i(clk_i),
        .nrst_i(nrst_i),
        .midiByte_i(midiByte),
        .midiByteValid_i(midiByteValid),
        .ch_o(channel),
        .note_o(note),
        .noteOnStrb_o(noteOnStrb),
        .noteOffStrb_o(noteOffStrb)
    );

	note2cnt note2cnt_inst (
		.clk_i(clk_i),
		.nrst_i(nrst_i),
		.note_i(note),
		.baseCntPeriod_o(oscCmp),
        .shift_o(oscShift)
	);

    // Generate Oscillator stack
    genvar i;
    generate
        for (i = 0; i < `OSC_VOICES; i = i + 1) begin : oscStack_gen
            localparam OSC_CH = i[`OSC_VOICES_BW-1:0]; // Truncate to reduce operation bitwidth of channel comparison
            /* verilator lint_off WIDTHTRUNC */
            // OK: Warning only occurs if OSC_VOICES is a power of 2
            osc osc_inst (
                .clk_i(clk_i),
                .nrst_i(nrst_i),
                .baseCntPeriod_i(oscCmp),
                .shift_i(oscShift),
                .ch_i(channel == OSC_CH),
                .active_o(activeOscs[OSC_CH]),
                .noteOnStrb_i(noteOnStrb),
                .noteOffStrb_i(noteOffStrb), 
                .wave_o(oscOut_o[OSC_CH])
            );
            /* verilator lint_off WIDTHTRUNC */
        end
    endgenerate
    
    bitcount #(
        .WORDLEN(`OSC_VOICES)
    ) bitcount_inst (
        .word_i(activeOscs),
        .count_o(nActiveOscs)
    );

    pwm #(
        .PWM_BW(`OSC_VOICES_BW)
    ) pwm_inst (
        .clk_i(clk_i),
        .nrst_i(nrst_i),
        .onCnt_i(nActiveOscs),
        .periodCnt_i(`OSC_VOICES_BW'(`OSC_VOICES)),
        .pwm_o(activeOscPwm_o)
    );

endmodule // synth
`endif // __SYNTH
`default_nettype wire

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

    localparam PWM_BW = $clog2(`OSC_VOICES + 1);

    wire noteOnStrb;
    wire noteOffStrb;
    wire [`MIDI_PAYLOAD_BITS-1:0] note;
    
    wire midiByteValid;
    wire [`MIDI_PAYLOAD_BITS-1:0] midiByte;
    
    wire [`OSC_VOICES-1:0] activeOscs; // one bit per oscillator
    wire [PWM_BW-1:0] sumActiveOscs; 
    wire [`OSC_CNT_BW-1:0] oscCmp;
    wire [2:0] channel;

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

	note2cnt #(
		.BW(`OSC_CNT_BW)
	) note2cnt_inst (
		.clk_i(clk_i),
		.nrst_i(nrst_i),
		.note_i(note),
		.halfCntPeriod_o(oscCmp)
	);

    // Generate Oscillator stack
    genvar i;
    generate
        for (i = 0; i < `OSC_VOICES; i = i + 1) begin : oscStack_gen
            osc osc_inst (
                .clk_i(clk_i),
                .nrst_i(nrst_i),
                .halfCntPeriod_i(oscCmp),
                .ch_i(channel == i),
                .active_o(activeOscs[i]),
                .noteOnStrb_i(noteOnStrb),
                .noteOffStrb_i(noteOffStrb), 
                .wave_o(oscOut_o[i])
            );
        end
    endgenerate
    
    bitcount #(
        .WORDLEN(`OSC_VOICES)
    ) bitcount_inst (
        .word_i(activeOscs),
        .count_o(sumActiveOscs)
    );

    pwm pwm_inst (
        .clk_i(clk_i),
        .nrst_i(nrst_i),
        .onCnt_i(sumActiveOscs), // max 7 active oscillators
        .periodCnt_i(PWM_BW'(`OSC_VOICES)),
        .pwm_o(activeOscPwm_o)
    );

endmodule // synth
`endif // __SYNTH
`default_nettype wire

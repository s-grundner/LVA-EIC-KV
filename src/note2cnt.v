/*******************************************************************************
* @file    : note.v                                                            *
* @author  : @s-grundner                                                       *
* @license : Apache-2.0                                                        *
* @brief   : Note to half counter period conversion.                           *
*******************************************************************************/

`include "counter.v"

module note2cnt #(
    parameter BW = 8
) (
    input wire clk_i,
    input wire nrst_i,
    input wire [7:0] note_i,
    output wire [BW-2:0] halfCntPeriod_o
);

	// ROM for the middle octave (MIDI notes 60 to 71)
	localparam c4 = 8'd60;
	localparam b4 = 8'd71;
	localparam ROM_SIZE = 12;
	reg [BW-2:0] noteRom [0:ROM_SIZE-1];

	initial begin
		noteRom[0]  = 16'd682; // C4
		noteRom[1]  = 16'd644; // C#4
		noteRom[2]  = 16'd608; // D4
		noteRom[3]  = 16'd574; // D#4
		noteRom[4]  = 16'd512; // E4
		noteRom[5]  = 16'd482; // F4
		noteRom[6]  = 16'd456; // F#4
		noteRom[7]  = 16'd430; // G4
		noteRom[8]  = 16'd406; // G#4
		noteRom[9]  = 16'd384; // A4
		noteRom[10] = 16'd362; // A#4
		noteRom[11] = 16'd342; // B3
	end

	reg [BW-2:0] halfCntPeriod;

	always @(*) begin
		halfCntPeriod = noteRom[note_i % ROM_SIZE];
	end

	assign halfCntPeriod_o = halfCntPeriod;

endmodule  // note2cnt

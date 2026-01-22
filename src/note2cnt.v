/*******************************************************************************
* @file    : note.v (Atomic)                                                   *
* @author  : @s-grundner                                                       *
* @license : Apache-2.0                                                        *
* @brief   : Note to half counter period conversion.                           *
* 			 Uses a ROM for the lowest octave and calculates    			   *
*            higher octaves by right shifting the values.                      *
*******************************************************************************/

`default_nettype none
`ifndef __NOTE2CNT
`define __NOTE2CNT

`include "global.v"

module note2cnt (
	input wire clk_i,
	input wire nrst_i,
	input wire [`MIDI_NOTE_BW-1:0] note_i,
	output reg [`OSC_ROM_BW-1:0] baseCntPeriod_o,
	output reg [3:0] shift_o
);
	// Initialize the note ROM. Values generated with noteROM-f-deviation.ipynb
	reg [`OSC_ROM_BW-1:0] noteRom [11:0];
	initial begin
		noteRom[0] = 120;
		noteRom[1] = 106;
		noteRom[2] = 93;
		noteRom[3] = 81;
		noteRom[4] = 69;
		noteRom[5] = 58;
		noteRom[6] = 47;
		noteRom[7] = 37;
		noteRom[8] = 28;
		noteRom[9] = 19;
		noteRom[10] = 11;
		noteRom[11] = 3;
	end

	reg [3:0] octave;
	reg [`OSC_ROM_BW-1:0] actualNote; 
	reg [`OSC_ROM_BW-1:0] baseNoteCnt; 
	/* verilator lint_off UNUSEDSIGNAL */
	// truncate to 4 bits as only 12 entries in ROM
	reg [7:0] noteIndex; 
	/* verilator lint_on UNUSEDSIGNAL */
	
	always @(*) begin
		if (note_i < 21) begin
			actualNote = `OSC_ROM_BW'd0;
		end else begin
			actualNote = note_i - `OSC_ROM_BW'd21;
		end
	end
	
	always @(*) begin
		// shift = actualNote / 12
		if (actualNote < 12) octave = 4'h0;
		else if (actualNote < 24) octave = 4'h1;
		else if (actualNote < 36) octave = 4'h2;
		else if (actualNote < 48) octave = 4'h3;
		else if (actualNote < 60) octave = 4'h4;
		else if (actualNote < 72) octave = 4'h5;
		else if (actualNote < 84) octave = 4'h6;
		else if (actualNote < 96) octave = 4'h7;
		else octave = 4'h8; 
	end

	always @(*) begin
		// noteIndex = actualNote % 12
		noteIndex = actualNote - octave * 12;
		baseNoteCnt = noteRom[noteIndex[3:0]];	
	end
	
	always @(posedge clk_i or negedge nrst_i) begin
		if(!nrst_i) begin
			baseCntPeriod_o <= {(`OSC_ROM_BW){1'b0}};
			shift_o <= 4'h0;
		end else begin
			baseCntPeriod_o <= baseNoteCnt;
			shift_o <= 4'h8 - octave;
		end
	end

endmodule  // note2cnt
`endif // __NOTE2CNT
`default_nettype wire

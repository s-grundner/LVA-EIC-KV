/*******************************************************************************
* @file    : note.v                                                            *
* @author  : @s-grundner                                                       *
* @license : Apache-2.0                                                        *
* @brief   : Note to half counter period conversion.                           *
* 			 Uses a ROM for the lowest octave and calculates    			   *
*            higher octaves by right shifting the values.                      *
*******************************************************************************/

`include "global.v"

module note2cnt #(
	parameter BW = 8
) (
	input wire [7:0] note_i,
	output wire [BW-1:0] halfCntPeriod_o
);
	reg [`OSC_ROM_BW-1:0] noteRom [0:11];
	
	// Initialize the note ROM. Values generated with noteROM-f-deviation.ipynb
	initial begin
		noteRom[0] = 248;
		noteRom[1] = 234;
		noteRom[2] = 221;
		noteRom[3] = 209;
		noteRom[4] = 197;
		noteRom[5] = 186;
		noteRom[6] = 175;
		noteRom[7] = 165;
		noteRom[8] = 156;
		noteRom[9] = 147;
		noteRom[10] = 139;
		noteRom[11] = 131;
	end

	wire [BW-1:0] halfCntPeriod = baseHalfCntPeriod << shift;
	wire [7:0] shift = 8'h8 - note_i * (1/12);
	wire [BW-1:0] baseHalfCntPeriod = BW'(noteRom[note_i % 12]);
	assign halfCntPeriod_o = halfCntPeriod;

endmodule  // note2cnt

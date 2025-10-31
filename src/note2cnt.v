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

module note2cnt #(
	parameter BW = 8
) (
	input wire clk_i,
	input wire nrst_i,
	input wire [7:0] note_i,
	output wire [BW-1:0] halfCntPeriod_o
);
	reg [`OSC_ROM_BW-1:0] noteRom [11:0];
	// Initialize the note ROM. Values generated with noteROM-f-deviation.ipynb
	initial begin
		noteRom[0]  = `OSC_ROM_BW'd248;
		noteRom[1]  = `OSC_ROM_BW'd234;
		noteRom[2]  = `OSC_ROM_BW'd221;
		noteRom[3]  = `OSC_ROM_BW'd209;
		noteRom[4]  = `OSC_ROM_BW'd197;
		noteRom[5]  = `OSC_ROM_BW'd186;
		noteRom[6]  = `OSC_ROM_BW'd175;
		noteRom[7]  = `OSC_ROM_BW'd165;
		noteRom[8]  = `OSC_ROM_BW'd156;
		noteRom[9]  = `OSC_ROM_BW'd147;
		noteRom[10] = `OSC_ROM_BW'd139;
		noteRom[11] = `OSC_ROM_BW'd131;
	end

	reg [BW-1:0] halfCntPeriod; 
	reg [3:0] shift;
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
		if (actualNote < 12) shift = 4'h8;
		else if (actualNote < 24) shift = 4'h7;
		else if (actualNote < 36) shift = 4'h6;
		else if (actualNote < 48) shift = 4'h5;
		else if (actualNote < 60) shift = 4'h4;
		else if (actualNote < 72) shift = 4'h3;
		else if (actualNote < 84) shift = 4'h2;
		else if (actualNote < 96) shift = 4'h1;
		else shift = 4'h0; 
	end

	always @(*) begin
		noteIndex = (actualNote - 8'd96 + shift * 12);
		baseNoteCnt = noteRom[noteIndex[3:0]];	
	end
	
	always @(posedge clk_i or negedge nrst_i) begin
		if(!nrst_i) begin
			halfCntPeriod <= {BW{1'b0}};
		end else begin
			halfCntPeriod <= {{8'b0}, baseNoteCnt} << shift;
		end
	end
	
	assign halfCntPeriod_o = halfCntPeriod;

endmodule  // note2cnt
`endif // __NOTE2CNT
`default_nettype wire

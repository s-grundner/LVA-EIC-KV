/*******************************************************************************
* @file    : note.v                                                            *
* @author  : @s-grundner                                                       *
* @license : Apache-2.0                                                        *
* @brief   : Note to half counter period conversion.                           *
* 			 Uses a ROM for the lowest octave and calculates    			   *
*            higher octaves by right shifting the values.                      *
*******************************************************************************/

`include "counter.v"

module note2cnt #(
	parameter BW = 8
) (
	input wire clk_i,
	input wire nrst_i,
	input wire [7:0] note_i,
	output wire [BW-1:0] halfCntPeriod_o
);
	localparam ROM_SIZE = 12;
	localparam gSharp5 = 8'd80;
	localparam a4 = 8'd69;
	reg [`OSC_ROM_BW-1:0] noteRom [0:ROM_SIZE-1];
	
	// Initialize the note ROM. Values generated with noteROM-f-deviation.ipynb
	initial begin
		noteRom[0] = 3977;
		noteRom[1] = 3754;
		noteRom[2] = 3543;
		noteRom[3] = 3344;
		noteRom[4] = 3156;
		noteRom[5] = 2979;
		noteRom[6] = 2812;
		noteRom[7] = 2654;
		noteRom[8] = 2505;
		noteRom[9] = 2364;
		noteRom[10] = 2232;
		noteRom[11] = 2106;
	end

	reg [BW-1:0] halfCntPeriod;
	integer octave;
	wire lower = (note_i < a4);
	wire higher = (note_i > gSharp5);;
	wire [BW-1:0] baseHalfCntPeriod = noteRom[note_i % ROM_SIZE];

	always @(*) begin
		octave = note_i / ROM_SIZE;
		if(lower) begin
			halfCntPeriod = baseHalfCntPeriod << (4'd4 - octave[3:0]);
		end else if(higher) begin
			halfCntPeriod = baseHalfCntPeriod >> (octave[3:0] - 4'd4);
		end else begin
			halfCntPeriod = baseHalfCntPeriod;
		end
	end

	assign halfCntPeriod_o = halfCntPeriod;

endmodule  // note2cnt

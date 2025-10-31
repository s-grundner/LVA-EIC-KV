/*******************************************************************************
* @file    : osc.v                                                             *
* @author  : @s-grundner                                                       *
* @license : Apache-2.0                                                        *
* @brief   : Oscillator module. Generates a square wave for a given midi note  *
*******************************************************************************/

`default_nettype none
`ifndef __OSC
`define __OSC
`include "global.v"

module osc (
	input wire clk_i,
	input wire nrst_i,
	input wire noteOnStrb_i,
	input wire noteOffStrb_i,
	input wire ch_i,
	input wire [`OSC_CNT_BW-1:0] halfCntPeriod_i,
	output wire active_o,
	output wire wave_o
);

	// ---------------------------- Signals --------------------------------- //

	reg wave;
	reg enabled;
	reg [`OSC_CNT_BW-1:0] halfCntPeriod;

	reg nrstSync;
	reg cntReached;

	wire [`OSC_CNT_BW-1:0] oscCounter;

	assign active_o = enabled;
	assign wave_o = wave;

	// -------------------- Logic Implementations --------------------------- //
	
	always @(*) begin
		cntReached = oscCounter == halfCntPeriod;
		nrstSync = !(cntReached & enabled);	
	end
	
	always @(posedge clk_i or negedge nrst_i) begin
		if (!nrst_i) begin
			enabled <= 1'b0;
		end else if (noteOnStrb_i && ch_i) begin
			enabled <= 1'b1;
		end else if (noteOffStrb_i && ch_i) begin
			enabled <= 1'b0;
		end
	end	
	
	always @(posedge clk_i or negedge nrst_i) begin
		if (!nrst_i) begin
			wave <= 1'b0;
		end else if (!nrstSync) begin
			wave <= ~wave;
		end
	end
	
	always @(posedge clk_i or negedge nrst_i) begin
		if (!nrst_i) begin
			halfCntPeriod <= `OSC_CNT_BW'b0;
		end else if (noteOnStrb_i && ch_i) begin 
			halfCntPeriod <= halfCntPeriod_i;
		end
	end


	// ----------------------- Module Instances ----------------------------- //

	counter #(
		.BW(`OSC_CNT_BW)
	) oscCounter_inst (
		.clk_i(clk_i),
		.nrst_i(nrst_i),
		.nrstSync_i(nrstSync),
		.count_o(oscCounter)
	);

endmodule  // osc
`endif // __OSC
`default_nettype wire

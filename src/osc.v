/*******************************************************************************
* @file    : osc.v                                                             *
* @author  : @s-grundner                                                       *
* @license : Apache-2.0                                                        *
* @brief   : Oscillator module. Generates a square wave for a given midi note  *
*******************************************************************************/

`include "counter.v"
`include "note2cnt.v"

module osc (
	input wire clk_i,
	input wire nrst_i,
	input wire nrstPhase_i,
	input wire enable_i,
	input wire [7:0] note_i,
	output wire wave_o
);

	// -------------------------- Parameters -------------------------------- //

	localparam CNT_BW = `OSC_CNT_BW;

	// ---------------------------- Signals --------------------------------- //

	reg [CNT_BW-1:0] oscCmp;
	wire [CNT_BW-1:0] oscCounter;

	reg wave;
	reg nrstCnt;

	// ------------------------ Assign Outputs ------------------------------ //
	assign wave_o = wave;

	// -------------------- Logic Implementations --------------------------- //
	wire toggleOsc = (oscCounter == oscCmp);
	
	// Toggle wave 
	always @(posedge clk_i or negedge nrst_i) begin
		if (!nrst_i) begin
			wave <= 1'b0;
		end else if (enable_i && toggleOsc) begin
			wave <= ~wave;
		end
	end

	// Determine counter reset condition
	always @(*) begin
		if (nrstPhase_i | toggleOsc) begin
			nrstCnt = 1'b0;
		end else begin
			nrstCnt = 1'b1;
		end
	end

	// ----------------------- Module Instances ----------------------------- //

	counter #(
		.BW(CNT_BW)
	) oscCounter_inst (
		.clk_i(clk_i),
		.nrst_i(nrst_i),
		.nrstSync_i(nrstCnt),
		.count_o(oscCounter)
	);
	
	note2cnt #(
		.BW(CNT_BW)
	) note2cnt_inst (
		.clk_i(clk_i),
		.nrst_i(nrst_i),
		.note_i(note_i),
		.halfCntPeriod_o(oscCmp)
	);

endmodule  // osc

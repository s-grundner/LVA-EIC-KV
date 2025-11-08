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
	input wire [3:0] shift_i,
	input wire [`OSC_ROM_BW-1:0] baseCntPeriod_i,
	output wire active_o,
	output wire wave_o
);

	// ---------------------------- Signals --------------------------------- //

	reg wave;
	reg enabled;
	reg [`OSC_ROM_BW-1:0] baseCntPeriod;
	reg [3:0] shift;

	wire start = noteOnStrb_i & ch_i; // Osc start condition

	assign active_o = enabled;
	assign wave_o = wave;

	// -------------------- Logic Implementations --------------------------- //
		
	// Only stop if currently playing note is present in the input
	// Smart indexing to ignore redundant bits
	// Calculations in noteROM-f-deviation.ipynb
	wire[3:0] rmRedundancy_i = {baseCntPeriod_i[6], baseCntPeriod_i[4:2]};
	wire[3:0] rmRedundancy = {baseCntPeriod[6], baseCntPeriod[4:2]};
	wire inputsMatch = (rmRedundancy_i == rmRedundancy);
	wire stop = noteOffStrb_i & ch_i & inputsMatch;

	wire [`OSC_CNT_BW-1:0] oscCounter;

	/* verilator lint_off UNUSEDSIGNAL */
	// truncate to 8 bits as only 8 bits used for comparison
	wire [`OSC_CNT_BW-1:0] oscCmp = oscCounter >> shift;
	/* verilator lint_on UNUSEDSIGNAL */

	wire cntReached = oscCmp[7:0] == {1'b1, baseCntPeriod};
	wire reset_active = cntReached & enabled; // strobe signal when counter hits period
	wire nrstSync = ~reset_active; 
	
	// Update enable and baseCntPeriod with minimal logic
	always @(posedge clk_i or negedge nrst_i) begin
		if (!nrst_i) begin
			enabled <= 1'b0;
			baseCntPeriod <= `OSC_ROM_BW'b0;
			wave <= 1'b0;
			shift <= 4'b0;
		end else begin
			enabled <= (enabled | start) & ~stop;
			// load-on-start
			if (start) begin
				baseCntPeriod <= baseCntPeriod_i;
				shift <= shift_i;
			end
			// toggle wave with XOR
			wave <= wave ^ reset_active;
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

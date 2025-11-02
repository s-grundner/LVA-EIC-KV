/*******************************************************************************
* @file    : tb_counter.v (Atomic)                                             *
* @author  : @s-grundner                                                       *
* @license : Apache-2.0                                                        *
* @brief   : Counter Module Testbench                                          *
*******************************************************************************/

`default_nettype none
`timescale 1ns/1ps

module tb_counter;

	initial begin
		$dumpfile("./waves/tb_counter.vcd");
		$dumpvars(0, tb_counter);
	end

	// Parameters
	localparam BW = 4;

	// Signals
	reg clk;
	reg nrst;
	reg nrstSync;
	wire [BW-1:0] count;

	// DUT instantiation
	counter #(
		.BW(BW)
	) dut (
		.clk_i(clk),
		.nrst_i(nrst),
		.nrstSync_i(nrstSync),
		.count_o(count)
	);

	// Stimulus generation in coco routine
endmodule
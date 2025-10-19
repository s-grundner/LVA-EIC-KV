/*******************************************************************************
* @file    : counter_tb.v                                                      *
* @author  : @s-grundner                                                       *
* @license : Apache-2.0                                                        *
* @brief   : Counter Module Testbench for Waveform Viewer                      *
*******************************************************************************/

`default_nettype none
`timescale 1ns/1ps

module tb_counter;
	initial begin
		$dumpfile("tb_counter.vcd");
		$dumpvars(0, tb_counter);
	end

	// Parameters
	localparam BW = 4;

	// Signals
	reg clk;
	reg nrst;
	reg nrstSync;
	wire [BW-1:0] count;

	// Clock generation
	initial begin
		clk = 1'b0;
		forever #10 clk = ~clk; // 100MHz clock
	end

	// DUT instantiation
	counter #(
		.BW(BW)
	) dut (
		.clk_i(clk),
		.nrst_i(nrst),
		.nrstSync_i(nrstSync),
		.count_o(count)
	);
endmodule
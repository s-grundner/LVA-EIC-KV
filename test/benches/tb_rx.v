/*******************************************************************************
* @file    : tb_rx.v                                                           *
* @author  : @s-grundner                                                       *
* @license : Apache-2.0                                                        *
* @brief   : Reciever Module Testbench                                         *
*******************************************************************************/

`default_nettype none
`timescale 1ns/1ps

module tb_counter;

	initial begin
		$dumpfile("./waves/tb_rx.vcd");
		$dumpvars(0, tb_rx);
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
endmodule

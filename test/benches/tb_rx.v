/*******************************************************************************
* @file    : tb_rx.v                                                           *
* @author  : @s-grundner                                                       *
* @license : Apache-2.0                                                        *
* @brief   : Reciever Module Testbench                                         *
*******************************************************************************/

`default_nettype none
`timescale 1ns/1ps

module tb_rx;

	initial begin
		$dumpfile("./waves/tb_rx.vcd");
		$dumpvars(0, tb_rx);
	end

	// Signals
	reg clk;
	reg nrst;
	reg rxData;
	wire [7:0] payload;


	// DUT instantiation
	rx dut (
		.clk_i(clk),
		.nrst_i(nrst),
		.rxData_i(rxData),
		.midiData_o(payload)
	);
endmodule

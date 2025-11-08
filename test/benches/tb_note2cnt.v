/*******************************************************************************
* @file    : tb_note2cnt.v                                                     *
* @author  : @s-grundner                                                       *
* @license : Apache-2.0                                                        *
* @brief   : Note Lookup Module Testbench                                      *
*******************************************************************************/

`default_nettype none
`timescale 1ns/1ps

module tb_note2cnt;

	initial begin
		$dumpfile("./waves/tb_note2cnt.vcd");
		$dumpvars(0, tb_note2cnt);
	end

	// Signals
	reg clk;
	reg nrst;
	reg [6:0] note;
	wire [6:0] baseCntPeriod;
	wire [3:0] shift;

	// DUT instantiation
	note2cnt dut (
		.clk_i(clk),
		.nrst_i(nrst),
		.note_i(note),
		.baseCntPeriod_o(baseCntPeriod),
		.shift_o(shift)
	);
endmodule

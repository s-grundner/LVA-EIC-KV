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

	// Parameters
	localparam BW = 16;

	// Signals
	reg clk;
	reg nrst;
	reg [7:0] note;
	wire [BW-1:0] halfCntPeriod;

	// DUT instantiation
	note2cnt #(
		.BW(BW)
	) dut (
		.clk_i(clk),
		.nrst_i(nrst),
		.note_i(note),
		.halfCntPeriod_o(halfCntPeriod)
	);
endmodule

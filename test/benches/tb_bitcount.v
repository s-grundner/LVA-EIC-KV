/*******************************************************************************
* @file    : tb_bitcount.v                                                     *
* @author  : @s-grundner                                                       *
* @license : Apache-2.0                                                        *
* @brief   : Bitcount Module Testbench                                         *
*******************************************************************************/

`default_nettype none
`timescale 1ns/1ps

`include "global.v"

module tb_bitcount;

	initial begin
		$dumpfile("./waves/tb_bitcount.vcd");
		$dumpvars(0, tb_bitcount);
	end

	localparam WORDLEN = `OSC_VOICES;
	localparam CNTLEN = $clog2(WORDLEN+1);
	reg [WORDLEN-1:0] word;
	wire [CNTLEN-1:0] count;
	
	// DUT instantiation
	bitcount #(
		.WORDLEN(WORDLEN)
	) dut (
		.word_i(word),
		.count_o(count)
	);
endmodule


/*******************************************************************************
* @file    : tb_osc.v                                                          *
* @author  : @s-grundner                                                       *
* @license : Apache-2.0                                                        *
* @brief   : Testbench for oscillator module.                                  *
*******************************************************************************/

`default_nettype none
`timescale 1ns/1ps

module tb_osc;
	initial begin
		$dumpfile("./waves/tb_osc.vcd");
		$dumpvars(0, tb_osc);
	end

	reg[7:0] note;
	reg clk;
	reg nrst;
	reg noteOnStrb;
	reg noteOffStrb;
	reg[15:0] oscHalfCntPeriod;
	reg ch;

	wire wave;
	wire active;

	osc dut (
		.clk_i(clk),
		.nrst_i(nrst),
		.noteOnStrb_i(noteOnStrb),
		.noteOffStrb_i(noteOffStrb),
		.halfCntPeriod_i(oscHalfCntPeriod),
		.ch_i(ch),
		.active_o(active),
		.wave_o(wave)
	);

endmodule



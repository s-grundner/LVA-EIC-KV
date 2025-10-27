/*******************************************************************************
* @file    : osc_tb.v                                                          *
* @author  : @s-grundner                                                       *
* @license : Apache-2.0                                                        *
* @brief   : Testbench for oscillator module.                                  *
*******************************************************************************/

`default_nettype none
`timescale 1ns/1ps

module osc_tb;
	initial begin
		$dumpfile("./waves/osc_tb.vcd");
		$dumpvars(0, osc_tb);
	end

	reg note[7:0];
	reg clk;
	reg nrst;
	reg noteOnStrb;
	reg noteOffStrb;
	reg oscHalfCntPeriod;

	wire wave;
	wire active;

	osc #(
		.CH(0)
	) dut (
		.clk_i(clk),
		.nrst_i(nrst),
		.active_o(active),
		.noteOnStrb_i(noteOnStrb),
		.noteOffStrb_i(noteOffStrb),
		.halfCntPeriod_i(oscHalfCntPeriod),
		.note_i(note),
		.wave_o(wave)
	);

endmodule



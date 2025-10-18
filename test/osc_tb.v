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
		$dumpfile("osc_tb.vcd");
		$dumpvars(0, counter_tb);
	end

	// Clock generation
	initial begin
		clk = 1'b0;
		forever #5 clk = ~clk; // 100MHz clock
	end

	reg note[7:0];
	reg clk;
	reg nrst;
	reg nrstPhase;
	reg enable;
	wire wave;

	osc dut (
		.clk_i(clk),
		.nrst_i(nrst),
		.nrstPhase_i(nrstPhase),
		.enable_i(enable),
		.note_i(note),
		.wave_o(wave)
	);

	initial begin
		$finish;
	end
endmodule



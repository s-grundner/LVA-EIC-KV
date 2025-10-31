/*******************************************************************************
* @file    : tb_pwm.v                                                          *
* @author  : @s-grundner                                                       *
* @license : Apache-2.0                                                        *
* @brief   : Testbench for PWM module.                                         *
*******************************************************************************/

`default_nettype none
`timescale 1ns/1ps

`include "global.v"

module tb_pwm;
	initial begin
		$dumpfile("./waves/tb_pwm.vcd");
		$dumpvars(0, tb_pwm);
	end

	localparam OSC_VOICES = 7;
	localparam PWM_BW = 3;
	localparam OSC_CNT_BW = $clog2(OSC_VOICES+1);

	reg clk;
	reg nrst;
	reg [OSC_VOICES-1:0] activeOscs;
	reg [OSC_CNT_BW-1:0] nActiveOscs;
	wire pwmOut;
	
	// bitcount to count inactive oscillators
	// Test bitcount seperately beforehand
    bitcount #(
        .WORDLEN(OSC_VOICES)
	) helper_bitcount (
        .word_i(activeOscs),
        .count_o(nActiveOscs)
    );

	pwm #(
		.PWM_BW(PWM_BW)
	) dut (
		.clk_i(clk),
		.nrst_i(nrst),
		.onCnt_i(nActiveOscs),
        .periodCnt_i(OSC_VOICES),
		.pwm_o(pwmOut)
	);

endmodule

/*******************************************************************************
* @file    : tb_midi.v (Atomic)                                                *
* @author  : @s-grundner                                                       *
* @license : Apache-2.0                                                        *
* @brief   : Testbench for MIDI module.                                        *
*******************************************************************************/

`default_nettype none
`timescale 1ns/1ps

module tb_midi;
	initial begin
		$dumpfile("./waves/tb_midi.vcd");
		$dumpvars(0, tb_midi);
	end

	reg clk;
	reg nrst;
	reg rxData;
	reg enableRx;

	// Self Controlled Signals
	reg midiByteValid_from_tb;
	reg [7:0] midiByte_from_tb;
	
	reg midiByteValid;
	reg [7:0] midiByte;

	wire dataReady;
	wire [7:0] payload;
	wire [2:0] ch;
	wire [7:0] note;
	wire noteOnStrb;
	wire noteOffStrb;

	always @(*) begin
		if (enableRx) begin
			midiByteValid = dataReady;
			midiByte = payload;
		end else begin
			midiByteValid = midiByteValid_from_tb;
			midiByte = midiByte_from_tb;
		end
	end
	
	rx rx_dut (
		.clk_i(clk),
		.nrst_i(nrst),
		.rxData_i(rxData),
		.dataReady_o(dataReady),
		.midiData_o(payload)
	);

	midi dut (
		.clk_i(clk),
		.nrst_i(nrst),
		.midiByteValid_i(midiByteValid),
		.midiByte_i(midiByte),
		.ch_o(ch),
		.note_o(note),
		.noteOnStrb_o(noteOnStrb),
		.noteOffStrb_o(noteOffStrb)
	);

endmodule




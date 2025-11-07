`default_nettype none
`timescale 1ns / 1ps

/* This testbench just instantiates the module and makes some convenient wires
   that can be driven / tested by the cocotb test.py.
*/
module tb ();

	initial begin
		$dumpfile("./waves/tb.vcd");
		$dumpvars(0, tb, tb.testcase_indicator);
	end

  // Wire up the inputs and outputs:
  reg clk;
  reg rst_n;
  reg ena;
  reg [7:0] ui_in;
  reg [7:0] uio_in;
  wire [7:0] uo_out;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;

  // Needed for convenient access in cocotb:
  wire rxDataIn;
  wire ch0;
  wire ch1;
  wire ch2;
  wire ch3;
  wire ch4;
  wire ch5;
  wire ch6;
  wire pwm;
  assign ui_in[3] = rxDataIn; 
  assign ch0 = uo_out[0];
  assign ch1 = uo_out[1];
  assign ch2 = uo_out[2];
  assign ch3 = uo_out[3];
  assign ch4 = uo_out[4];
  assign ch5 = uo_out[5];
  assign ch6 = uo_out[6];
  assign pwm = uo_out[7];
  
  reg[3:0] testcase_indicator;

`ifdef GL_TEST
  wire VPWR = 1'b1;
  wire VGND = 1'b0;
`endif

  // Replace tt_um_example with your module name:
  tt_um_s_grundner user_project (

      // Include power ports for the Gate Level test:
`ifdef GL_TEST
      .VPWR(VPWR),
      .VGND(VGND),
`endif

      .ui_in  (ui_in),    // Dedicated inputs
      .uo_out (uo_out),   // Dedicated outputs
      .uio_in (uio_in),   // IOs: Input path
      .uio_out(uio_out),  // IOs: Output path
      .uio_oe (uio_oe),   // IOs: Enable path (active high: 0=input, 1=output)
      .ena    (ena),      // enable - goes high when design is selected
      .clk    (clk),      // clock
      .rst_n  (rst_n)     // not reset
  );

endmodule

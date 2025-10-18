// --------------------------------------------------------------------
// >>>>>>>>>>>>>>>>>>>>>>>>> COPYRIGHT NOTICE <<<<<<<<<<<<<<<<<<<<<<<<<
// --------------------------------------------------------------------
// Copyright (c) 2006 by Lattice Semiconductor Corporation
// --------------------------------------------------------------------
//
// Permission:
//
//   Lattice Semiconductor grants permission to use this code for use
//   in synthesis for any Lattice programmable logic product.  Other
//   use of this code, including the selling or duplication of any
//   portion is strictly prohibited.
//
// Disclaimer:
//
//   This VHDL or Verilog source code is intended as a design reference
//   which illustrates how these types of functions can be implemented.
//   It is the user's responsibility to verify their design for
//   consistency and functionality through the use of formal
//   verification methods.  Lattice Semiconductor provides no warranty
//   regarding the use or functionality of this code.
//
// --------------------------------------------------------------------
//           
//                     Lattice Semiconductor Corporation
//                     5555 NE Moore Court
//                     Hillsboro, OR 97214
//                     U.S.A
//
//                     TEL: 1-800-Lattice (USA and Canada)
//                          503-268-8001 (other locations)
//
//                     web: http://www.latticesemi.com/
//                     email: techsupport@latticesemi.com
// --------------------------------------------------------------------
//
// Revision History :

module LED_Rotation(
    input  clk,
    output LED1,
    output LED2,
    output LED3,
    output LED4,
    output LED5
    );

	reg[15:0] div_cntr1;
	reg[6:0] div_cntr2;
	reg[1:0] dec_cntr;
	reg half_sec_pulse;
		
	always@(posedge clk)
		begin
		div_cntr1 <= div_cntr1 + 1;
		if (div_cntr1 == 0) 
			if (div_cntr2 == 91) 
				begin
				div_cntr2 <= 0;
				half_sec_pulse <= 1;  
				end
			else
				div_cntr2 <= div_cntr2 + 1;
		else
			half_sec_pulse <= 0;
		
		if (half_sec_pulse == 1)	
			dec_cntr <= dec_cntr + 1;
			
		end	
		
		
	assign LED1 = (dec_cntr == 0) ;
	assign LED2 = (dec_cntr == 1) ;
	assign LED3 = (dec_cntr == 2) ;
	assign LED4 = (dec_cntr == 3) ;
	assign LED5 = 1'b1;
				
endmodule

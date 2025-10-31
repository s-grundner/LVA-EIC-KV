/*******************************************************************************
* @file    : pmw.v                                                             *
* @author  : @s-grundner                                                       *
* @license : Apache-2.0                                                        *
* @brief   : PWM generator.                                                    *
*******************************************************************************/

`default_nettype none
`ifndef __PWM
`define __PWM

module pwm #(
    parameter PWM_BW = 3    
) (
	input wire clk_i,
	input wire nrst_i,
	input wire [PWM_BW-1:0] onCnt_i,
	input wire [PWM_BW-1:0] periodCnt_i,
	output wire pwm_o
);

    wire cntNSyncRst;
    wire [PWM_BW-1:0] pwmCountVal;
    
    counter #(
        .BW(PWM_BW)
    ) pwmCounter_inst (
        .clk_i(clk_i),
        .nrst_i(nrst_i),
        .nrstSync_i(cntNSyncRst),
        .count_o(pwmCountVal)
    );
    
    assign cntNSyncRst = (pwmCountVal < periodCnt_i);
    assign pwm_o = (pwmCountVal < onCnt_i);

endmodule // pwm
`endif // __PWM
`default_nettype wire

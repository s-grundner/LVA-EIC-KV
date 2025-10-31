/*******************************************************************************
* @file    : bitcount.v (Atomic)                                            *
* @author  : @s-grundner                                                       *
* @license : Apache-2.0                                                        *
* @brief   : Counts the number of high bits in the input vector                *
*******************************************************************************/

`default_nettype none
`ifndef __BITCOUNT
`define __BITCOUNT 

module bitcount #(
    parameter WORDLEN = 7
)(
    input wire [WORDLEN-1:0] word_i,
    output reg [$clog2(WORDLEN+1)-1:0] count_o
);
    localparam CNT_BW = $clog2(WORDLEN+1);
    integer i;
    always @(*) begin
        count_o = 0;
        for (i = 0; i < WORDLEN; i = i + 1) begin
            count_o = count_o + {{(CNT_BW - 1) {1'b0}}, word_i[i]};
        end
    end
endmodule // bitcount
`endif // __BITCOUNT
`default_nettype wire


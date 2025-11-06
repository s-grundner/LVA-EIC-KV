/*******************************************************************************
* @file    : midi.v (Atomic)                                                   *
* @author  : @s-grundner                                                       *
* @license : Apache-2.0                                                        *
* @brief   : MIDI command parser. Extracts note on/off commands and channel.   *
             Only feed Channel Voice Messages (0x8n, 0x9n)                     *
*******************************************************************************/

`default_nettype none
`ifndef __MIDI
`define __MIDI
`include "global.v"

module midi (
    input wire clk_i,
    input wire nrst_i,
    input wire midiByteValid_i,
    input wire [`MIDI_PAYLOAD_BITS-1:0] midiByte_i,
    output reg [`OSC_VOICES_BW-1:0] ch_o,
    output reg [`MIDI_PAYLOAD_BITS-1:0] note_o,
    output reg noteOnStrb_o,
    output reg noteOffStrb_o
);
    // ----------------------- Internal Parameters -------------------------- //

    localparam CMD_BW = 4;
    localparam CMD_NOTE_ON  = 4'b1001;
    localparam CMD_NOTE_OFF = 4'b1000;

    localparam FSM_IDLE = 0;
    localparam FSM_CMD = 1;
    localparam FSM_NOTE = 2;

    // ------------------------ Internal Register --------------------------- //

    reg [`MIDI_PAYLOAD_BITS-1:0] midiByteReg;
    reg [2:0] fsmState;
    reg [2:0] nextFsmState;

    reg [CMD_BW-1:0] cmd;

    // --------------------- Combinatorial Processes ------------------------ //
        
    always @(*) begin : nextFSM_p
        case (fsmState)
            FSM_IDLE: nextFsmState = FSM_CMD;
            FSM_CMD: nextFsmState = FSM_NOTE;
            FSM_NOTE: nextFsmState = FSM_IDLE;
            default: nextFsmState = FSM_IDLE;
        endcase
    end

    // ------------------------ Register Processes -------------------------- //
        
    always @(posedge clk_i or negedge nrst_i) begin : statusEval_p
        if (!nrst_i) begin
            cmd <= {CMD_BW{1'b0}};
            ch_o <= {`OSC_VOICES_BW{1'b0}};
        end else if (fsmState == FSM_CMD) begin
            cmd <= midiByteReg[7:4];
            ch_o <= midiByteReg[`OSC_VOICES_BW-1:0];
        end
    end
    
    always @(posedge clk_i or negedge nrst_i) begin
        if (!nrst_i) begin
            noteOnStrb_o <= 1'b0;
            noteOffStrb_o <= 1'b0;
        end else if (fsmState == FSM_NOTE && midiByteValid_i) begin
            noteOnStrb_o <= (cmd == CMD_NOTE_ON) ? 1'b1 : 1'b0;
            noteOffStrb_o <= (cmd == CMD_NOTE_OFF) ? 1'b1 : 1'b0;
        end else begin
            noteOnStrb_o <= 1'b0;
            noteOffStrb_o <= 1'b0;
        end
    end

    always @(posedge clk_i or negedge nrst_i) begin
        if (!nrst_i) begin
            note_o <= {`MIDI_PAYLOAD_BITS{1'b0}};
        end else if (fsmState == FSM_NOTE) begin
            note_o <= midiByteReg;
        end
    end

    always @(posedge clk_i or negedge nrst_i) begin : midiByteReg_p
        if (!nrst_i) begin
            midiByteReg <= {`MIDI_PAYLOAD_BITS{1'b0}};
            fsmState <= FSM_IDLE;
        end else if (midiByteValid_i) begin
            midiByteReg <= midiByte_i;
            fsmState <= nextFsmState;
        end
    end
    


endmodule // midi
`endif // __MIDI

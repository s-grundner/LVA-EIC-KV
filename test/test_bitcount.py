# *************************************************************************** #
# @file    : test_bitcount.py                                                 #
# @author  : @s-grundner                                                      #
# @license : Apache-2.0                                                       #
# @brief   : Bitcount Module Testbench for Cocotb.                            #
# *************************************************************************** #

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
@cocotb.parametrize(mode=['count 1s', 'count 0s'], test_vector=[0x00, 0x55, 0xAA, 0xF0, 0x34, 0xFF])
async def bitcount_test(dut, test_vector, mode):

    # Determine word length from DUT parameter
    word_len = dut.WORDLEN.value.to_unsigned()    
    word_mask = (1 << word_len) - 1

    match mode:
        case 'count 1s':
            bit_limited_vector = test_vector & word_mask  # ensure 7-bit input
        case 'count 0s':
            bit_limited_vector = (~test_vector) & word_mask  # ensure 7-bit input

    expected = bin(bit_limited_vector).count("1")
    dut.word.value = bit_limited_vector

    await Timer(10, unit="ns")
    assert dut.count.value == expected, f"Bitcount for input {bit_limited_vector:#0b} should be {expected} but is {dut.count.value.to_unsigned()}"

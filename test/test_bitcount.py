# *************************************************************************** #
# @file    : test_bitcount.py                                                 #
# @author  : @s-grundner                                                      #
# @license : Apache-2.0                                                       #
# @brief   : Bitcount Module Testbench for Cocotb.                            #
# *************************************************************************** #

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
@cocotb.parametrize(test_vector=[0x00, 0x55, 0xAA, 0xF0, 0x34, 0xFF])
async def bitcount_test(dut, test_vector):
    dut._log.info("Start")

    word_len = dut.WORDLEN.value.to_unsigned()    
    word_mask = (1 << word_len) - 1
    bit_limited_vector = test_vector & word_mask  # ensure 7-bit input

    dut.word.value = bit_limited_vector
    expected = bin(bit_limited_vector).count("1")

    await Timer(10, unit="ns")

    assert dut.count.value == expected, f"Bitcount for input {test_vector:#06x} should be {expected} but is {dut.count.value}"

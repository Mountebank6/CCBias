"""
Represent a path through the 2D search space as a binary sequence

Convert to and from binary representations
"""

import numpy as np

def seq_to_bin(sequence, bitlength):
    """Return binary string from list of 2-tuples
    
    Args:
        sequence:
            iterable of 2-tuples of position in array
        bitlength:
            number of bits used per element of the 2-tuples
            (e.g. if the elements of the tuples of sequence
            are 16 bit uints, bitlength is 16)
            signed integer is NOT supported
    """
    flat_list = [axis_pos for pos in sequence for axis_pos in pos]
    binstring = ""
    for axis_pos in flat_list:
        binstring += format(axis_pos, "#0"+str(bitlength + 2)+"b")[2:]
    return binstring

def bin_to_seq(binstring, bitlength):
    """Return list of 2-tuples from binary string
    
    Args:
        binstring:
            string of binary representing location list
        bitlength:
            number of bits used per element of the 2-tuples
            (e.g. if the elements of the tuples of sequence
            are 16 bit uints, bitlength is 16)
            signed integer is NOT supported
    """
    length = len(binstring)
    genes = length/bitlength
    if round(genes) != genes:
        raise ValueError("length/bitlength not an integer")
    sequence = []
    for i in range(0, length, 2*bitlength):
        sequence.append(
                   tuple(
                         (int(binstring[i:i+bitlength], 2), 
                         int(binstring[i+bitlength:i+2*bitlength], 2))
                        )
                       )
    return sequence
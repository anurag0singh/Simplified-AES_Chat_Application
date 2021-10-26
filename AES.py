# ------------------------------------------------------------------------------------------------- #
# 2019211
# Anurag Singh
# This file contains different functions and methods related to AES variant.
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# Lookup table for substituting nibbles
s_box = {
    '0000': '1001', '1000': '0110',
    '0001': '0100', '1001': '0010',
    '0010': '1010', '1010': '0000',
    '0011': '1011', '1011': '0011',
    '0100': '1101', '1100': '1100',
    '0101': '0001', '1101': '1110',
    '0110': '1000', '1110': '1111',
    '0111': '0101', '1111': '0111'
}

# Substituting nibbles


def substituteNibbles(nibble):
    return s_box.get(nibble)


def substituteNibblesInv(nibble):
    idx = list(s_box.values()).index(nibble)
    return list(s_box.keys())[idx]
# ------------------------------------------------------------------------------------------------- #
# Function for shifting rows


def shiftRows(nibble):
    return nibble[0:4] + nibble[12:16] + nibble[8:12] + nibble[4:8]

# ------------------------------------------------------------------------------------------------- #
# Function for multiplication in a Galois Field


def gfMul(a, b):
    product = 0
    while b > 0:
        if (b & 1) != 0:
            product = product ^ a
        a = a << 1
        if a & (1 << 4) != 0:
            a = a ^ 0b10011
        b = b >> 1
    return binaryRepresentation(product, 4)

# Function for mixing columns


def mixColumns(nibble):
    result = ''
    result += xor(nibble[0:4], gfMul(4, int(nibble[4:8], 2)), 4)       # N(0,0)' = N(0,0) XOR 4*N(1,0)
    result += xor(nibble[4:8], gfMul(4, int(nibble[0:4], 2)), 4)       # N(0,0)' = N(0,0) XOR 4*N(1,0)
    result += xor(nibble[8:12], gfMul(4, int(nibble[12:16], 2)), 4)       # N(0,0)' = N(0,0) XOR 4*N(1,0)
    result += xor(nibble[12:16], gfMul(4, int(nibble[8:12], 2)), 4)       # N(0,0)' = N(0,0) XOR 4*N(1,0)
    return result


def mixColumnsInv(nibble):
    result = ''
    result += xor(gfMul(9, int(nibble[0:4], 2)), gfMul(2, int(nibble[4:8], 2)), 4)
    result += xor(gfMul(9, int(nibble[4:8], 2)), gfMul(2, int(nibble[0:4], 2)), 4)
    result += xor(gfMul(9, int(nibble[8:12], 2)), gfMul(2, int(nibble[12:16], 2)), 4)
    result += xor(gfMul(9, int(nibble[12:16], 2)), gfMul(2, int(nibble[8:12], 2)), 4)
    return result

# ------------------------------------------------------------------------------------------------- #
# Function for returning binary representation of a number in terms of 'base' number of bits


def binaryRepresentation(num, base):
    num = bin(num)[2:]
    num = '0' * (base - len(num)) + num
    return num
# ------------------------------------------------------------------------------------------------- #
# Function for xor of two binary numbers


def xor(b1, b2, base):
    b1, b2 = int(b1, 2), int(b2, 2)
    answer = b1 ^ b2
    return binaryRepresentation(answer, base)
# ------------------------------------------------------------------------------------------------- #
# The g function as described in the assignment pdfs


def g(word, rcon):
    mid = len(word) // 2
    n0, n1 = word[:mid], word[mid:]
    # print(n0, n1)
    n0, n1 = n1, n0
    # print(n0, n1)
    return xor(substituteNibbles(n0), rcon, 4) + xor(substituteNibbles(n1), '0000', 4)
# ------------------------------------------------------------------------------------------------- #
# Function for key expansion, returns a list of 3 keys required for the 2 round AES variant


def aesKeyExpansion(binary_key):
    # binary_key = binaryRepresentation(key, 16)
    w = ['' for _ in range(6)]
    keys = []
    mid = len(binary_key) // 2
    w[0] += binary_key[:mid]
    w[1] += binary_key[mid:]
    w[2] += xor(w[0], g(w[1], '1000'), 8)
    w[3] += xor(w[1], w[2], 8)
    w[4] += xor(w[2], g(w[3], '0011'), 8)
    w[5] += xor(w[3], w[4], 8)
    keys.append(w[0] + w[1])
    keys.append(w[2] + w[3])
    keys.append(w[4] + w[5])
    return keys
# ------------------------------------------------------------------------------------------------- #
# Implementation of Simplified AES


def aesEncryption(plain_text, secret_key):
    keys = aesKeyExpansion(secret_key)
    cipher_text = xor(plain_text, keys[0], 16)
    # Round 1

    cipher_text = substituteNibbles(cipher_text[0:4]) + substituteNibbles(cipher_text[4:8]) + substituteNibbles(cipher_text[8:12]) + substituteNibbles(cipher_text[12:16])
    cipher_text = shiftRows(cipher_text)
    cipher_text = mixColumns(cipher_text)
    cipher_text = xor(cipher_text, keys[1], 16)

    # Round 2 - Last round

    cipher_text = substituteNibbles(cipher_text[0:4]) + substituteNibbles(cipher_text[4:8]) + substituteNibbles(cipher_text[8:12]) + substituteNibbles(cipher_text[12:16])
    cipher_text = shiftRows(cipher_text)
    cipher_text = xor(cipher_text, keys[2], 16)
    return cipher_text

# ------------------------------------------------------------------------------------------------- #


def aesDecryption(cipher_text, secret_key):
    keys = aesKeyExpansion(secret_key)
    plain_text = xor(cipher_text, keys[2], 16)
    plain_text = shiftRows(plain_text)
    plain_text = substituteNibblesInv(plain_text[0:4]) + substituteNibblesInv(plain_text[4:8]) + substituteNibblesInv(plain_text[8:12]) + substituteNibblesInv(plain_text[12:16])

    # Round 2 reversed

    plain_text = xor(plain_text, keys[1], 16)
    plain_text = mixColumnsInv(plain_text)
    plain_text = shiftRows(plain_text)
    plain_text = substituteNibblesInv(plain_text[0:4]) + substituteNibblesInv(plain_text[4:8]) + substituteNibblesInv(plain_text[8:12]) + substituteNibblesInv(plain_text[12:16])

    # Round 1 reversed

    plain_text = xor(plain_text, keys[0], 16)
    return plain_text

# ------------------------------------------------------------------------------------------------- #

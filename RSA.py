# ------------------------------------------------------------------------------------------------- #
# 2019211
# Anurag Singh
# This file contains different functions and methods related to RSA algorithm.
# ------------------------------------------------------------------------------------------------- #

from PrimeGenerator import generateLargePrime
import math
import random

# ------------------------------------------------------------------------------------------------- #
# A normal egcd function


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a)*y, y
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# Function to calculate modular multiplicative inverse number of a % m


def modInv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return False
    else:
        return x % m
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# Function to generate RSA keys


def rsaKeyGeneration(key_size):
    p = generateLargePrime(key_size)
    while True:
        q = generateLargePrime(key_size)
        if p ^ q:
            break
    n = p * q
    phi = (p - 1)*(q - 1)
    while True:
        e = random.randrange(2, n)
        if math.gcd(phi, e) == 1:
            break
    d = modInv(e, phi)
    public_key = (e, n)
    private_key = d
    return public_key, private_key
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# Function for implementing RSA encryption


def rsaEncrypt(plain_text, e, n):
    cipher_blocks = [pow(ord(character), e, n) for character in plain_text]
    cipher_text = ''.join(list(map(str, cipher_blocks)))
    return cipher_blocks, cipher_text
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# Function for implementing RSA decryption


def rsaDecrypt(cipher_blocks, d, n):
    aux = [str(pow(character, d, n)) for character in cipher_blocks]
    plain = [chr(int(char2)) for char2 in aux]
    return ''.join(plain)
# ------------------------------------------------------------------------------------------------- #

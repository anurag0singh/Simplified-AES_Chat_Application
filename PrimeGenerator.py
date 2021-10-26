# ------------------------------------------------------------------------------------------------- #
# 2019211
# Anurag Singh
# This file is for generating very big prime numbers.
# ------------------------------------------------------------------------------------------------- #

import random

# ------------------------------------------------------------------------------------------------- #
# millerRabinTest : if a number successfully passes this test then the
# probability of it being a prime number is high and if any number fails
# this test then we are sure that the number is not prime


def millerRabinTest(num):
    exp = num - 1
    while exp & 1:
        exp >>= 1
    a = random.randrange(2, exp)
    if pow(a, exp, num) == 1:
        return True
    while exp < num - 1:
        if pow(a, exp, num) == num - 1:
            return True
        exp <<= 1

    return False
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# This function returns a list of all prime numbers ranging from 2 to 1000


def smallPrimes():
    primes = [i for i in range(2, 1000)]
    idx = 0
    while True:
        a = b = primes[idx]
        while a < 1000:
            a += b
            try:
                primes.remove(a)
            except:
                continue
        idx += 1
        if idx >= len(primes):
            break
    return primes
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# This is a function to check whether a number is prime or not


def isPrime(num):
    primes = smallPrimes()
    if num < 2:
        return False
    if num in primes:
        return True
    for prime in primes:
        if num % prime == 0:
            return False
    return millerRabinTest(num)
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# Function to generate large prime numbers used for selecting p and q


def generateLargePrime(key_size):
    key_size = key_size / 2
    while True:
        num = random.randrange(2**(key_size-1) + 1, 2**key_size)
        if isPrime(num):
            return num
# ------------------------------------------------------------------------------------------------- #

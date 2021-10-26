# ------------------------------------------------------------------------------------------------- #
# 2019211
# Anurag Singh
# This file is for generating the message digest with the help of sha256 hash algorithm.
# ------------------------------------------------------------------------------------------------- #

import hashlib

FORMAT = 'utf-8'

# ------------------------------------------------------------------------------------------------- #
# Take in a msg string and return the msg digest in hexdigits


def generateHash(msg):
    hash_algo = hashlib.sha256()
    byte_msg = str(msg).encode(FORMAT)
    hash_algo.update(byte_msg)
    return hash_algo.hexdigest()
# ------------------------------------------------------------------------------------------------- #

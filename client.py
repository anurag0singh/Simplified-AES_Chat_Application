# ------------------------------------------------------------------------------------------------- #
# 2019211
# Anurag Singh
# This file contains all the client side networking and the computations required.
# ------------------------------------------------------------------------------------------------- #

import socket
import AES
import RSA
import hash

# ------------------------------------------------------------------------------------------------- #
# Declaring important constants
KEY_SIZE = 16
BUFFER = 64
PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
ADDRESS = (SERVER, PORT)
MESSAGE = ''.join(format(i, '08b') for i in bytearray(str(input('[INPUT] Enter the message you want to be encrypted ...\n')), encoding='utf-8'))
SECRET_KEY = str(input('[INPUT] Enter the secret_key to be used for S-AES ...\n'))
# ------------------------------------------------------------------------------------------------- #


def requestServerPublicKey():
    # ------------------------------------------------------------------------------------------------- #
    # Requesting server public key from the server
    # The server_public_key is received as a string so we convert it to a tuple of 2 integers
    # ------------------------------------------------------------------------------------------------- #
    # Receive server_public_key
    print('[WAITING] Waiting for server public key ...')
    length = client.recv(BUFFER).decode(FORMAT)
    if length:
        length = int(length)
        public_key = client.recv(length).decode(FORMAT)
    # Convert server_public_key to integer tuple
    public_key = tuple(map(int, (public_key[1:-1].split(','))))
    return public_key

# ------------------------------------------------------------------------------------------------- #
# Connect to the server


client = socket.socket()
client.connect(ADDRESS)
print('[CONNECTED] Client connected to the server ...')
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# Request for server_public_key
server_public_key = requestServerPublicKey()
print(f"[KEY] Server public key is {server_public_key} ...")
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# Generate client public and private key
client_public_key, client_private_key = RSA.rsaKeyGeneration(KEY_SIZE)
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# Create hash message digest and encrypt it with RSA to create a digital signature
digest = hash.generateHash(MESSAGE)
signature_blocks, signature = RSA.rsaEncrypt(digest, client_private_key, client_public_key[1])
print(f'[SIGNATURE] Digital signature created is {signature} ...')
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# Generate the cipher_text / Encrypt the message with S-AES
cipher_text = AES.aesEncryption(MESSAGE, SECRET_KEY)
print(f'[CIPHER] Cipher text generated is {cipher_text} ...')
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# Encrypt the SECRET_KEY with RSA algorithm using server_public_key
# Note: The SECRET_KEY is encrypted as it is, i.e., in a string format of binary representation
encrypted_secret_key_blocks, encrypted_secret_key = RSA.rsaEncrypt(SECRET_KEY, server_public_key[0], server_public_key[1])
print(f'[ENCRYPTED KEY] Encrypted secret key is {encrypted_secret_key} ...')
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# Creating a list of messages to send to the server for the sake of ease in coding
messages = [cipher_text, encrypted_secret_key_blocks, signature_blocks, client_public_key]

# Send information to the server
for msg in messages:
    msg = str(msg).encode(FORMAT)
    msg_length = str(len(msg)).encode(FORMAT)
    msg_length += b' ' * (BUFFER - len(msg_length))
    client.send(msg_length)
    client.send(msg)
# ------------------------------------------------------------------------------------------------- #

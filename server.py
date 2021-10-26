# ------------------------------------------------------------------------------------------------- #
# 2019211
# Anurag Singh
# This file contains all the server side networking and the computations required.
# ------------------------------------------------------------------------------------------------- #

import socket
import AES
import RSA
import hash


BUFFER = 64
FORMAT = 'utf-8'
PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
KEY_SIZE = 16

# ------------------------------------------------------------------------------------------------- #
# Function to send a message to the client


def sendToClient(m):
    m = str(m).encode(FORMAT)
    msg_length = str(len(m)).encode(FORMAT)
    msg_length += b' ' * (BUFFER - len(msg_length))
    connection.send(msg_length)
    connection.send(m)
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# Function to return a string from it's binary representation


def binaryToDecimal(binary):
    return int(binary, 2)
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# Establishing server network to connect to the client


server = socket.socket()
server.bind(ADDRESS)
server.listen()
print('[STARTING SERVER] Starting the Server ...')
print(f'[LISTENING] Server is listening on {SERVER}:{PORT}')
connection, client_address = server.accept()
print(f'[NEW CONNECTION] {client_address[0]}:{client_address[1]} connected to the server ...')
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# Generate RSA keys for server side and send the server_public_key to the client and connect
# to the client
server_public_key, server_private_key = RSA.rsaKeyGeneration(KEY_SIZE)
print('[SENDING] Sending server public key to the client ...')
sendToClient(server_public_key)
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# Receive the required messages from the client
show_msg = 'cipher_text, encrypted_secret_key_blocks, signature_blocks, client_public_key'.split(', ')
message_count = 0
messages = {}
while message_count < 4:
    length = connection.recv(BUFFER).decode(FORMAT)
    if length:
        length = int(length)
        msg = connection.recv(length).decode(FORMAT)
        messages[show_msg[message_count]] = msg
        print(f"[INFO RECEIVED] From {client_address[0]}:{client_address[1]} {show_msg[message_count]} {msg}")
        message_count += 1
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# Decrypt the encrypted_secret_key
encrypted_secret_key_blocks = list(map(int, messages['encrypted_secret_key_blocks'][1:-1].split(', ')))
secret_key = RSA.rsaDecrypt(encrypted_secret_key_blocks, server_private_key, server_public_key[1])
print(f'[SECRET_KEY] Secret key received from the client is {secret_key} ...')
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# Decrypt the cipher_text
plain_text = AES.aesDecryption(messages['cipher_text'], secret_key)
print(f'[PLAIN_TEXT] Plain text after decrypting cipher text is {plain_text} ...')
message = ''.join(chr(binaryToDecimal(plain_text[i:i+8])) for i in range(0, len(plain_text), 8))
print(f'[MESSAGE] Message received from the client is : {message} ...')
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# Verify the signature received from the client
print('[VERIFYING] Verifying the RSA digital signature received from the client')
digest = hash.generateHash(plain_text)
signature_blocks = list(map(int, messages['signature_blocks'][1:-1].split(', ')))
client_public_key = tuple(map(int, messages['client_public_key'][1:-1].split(', ')))
message_generated = RSA.rsaDecrypt(signature_blocks, client_public_key[0], client_public_key[1])
if message_generated == digest:
    print('[VERIFIED] Digital RSA signature received is verified ...')
else:
    print('[VERIFICATION FAILED] The digital signature is not verified ...')
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
# Closing the server
connection.close()
print('[CLOSED] The server is closed now ...')
# ------------------------------------------------------------------------------------------------- #

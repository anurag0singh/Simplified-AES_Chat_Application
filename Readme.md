# Overall Working :
![Simplified AES](https://user-images.githubusercontent.com/71708571/194760053-72e1a875-8cc3-4756-8ae9-a0e3914898bc.jpg)

# Instructions for running the programme :
       ~ First run server.py
       ~ Then run client.py
       ~ Input message
            Note : The message should be of 16 bits or two letters example : 'ok', 'ab', etc.
       ~ Input secret key to be used
            Note : The key must be in binary representation and must be of 16 bits
       ~ You are done !

# Name of all the files :
 - AES.py
 - RSA.py
 - server.py
 - client.py
 - PrimeGenerator.py
 - hash.py

# Short description about all the files :

# AES.py =>
-       substituteNibbles:
            Input : A single nibble
            Output : Substituted nibble with using a look up table, i.e., s_box
-       shiftRows:
            Input : Takes in a block size, i.e., 4 nibbles
            Output : Block with 2nd nibble inter-changed with 4th nibble
-       mixColumns:
            Input : Takes in a block size, i.e., 4 nibbles
            Output : Block with columns mixed
                     All columns multiplied with -- --
                                                 |1 4|
                                                 |4 1|
                                                 -- --

-       binaryRepresentation:
            Input : Takes in 2 arguments num, base
            Output : Returns a string of binary representation of num in GF(2**base)

-       xor:
            Input: Takes in 3 arguments b1, b2, base
            Output : Returns b1^b2 in GF(2**base)

-       g:
            Works as explained in the AES variant pdfs

-       aesKeyExpansion:
            Input : Takes in a binary key
            Output : Returns a list of 3 keys required for AES rounds

-       aesEncryption:
            Input : Takes in plain text and secret key
            Output : Returns the encrypted cipher text

-       aesDecryption:
            Input : Takes in cipher text and secret key
            Output : Returns the decrypted plain text

-       substituteNibblesInv:
            Inverts what substituteNibbles does to the nibbles
            Returns the keys from s_box dictionary for corresponding values

-       mixColumnsInv:
            Inverts the mixColumns function
            All columns multiplied with -- --
                                        |9 2|
                                        |2 9|
                                        -- --

# RSA.py =>
-       egcd:
            Extended Euclidean theorem for GCD

-       modInv:
            Input : Takes 2 arguments a and m
            Output : Returns modular multiplicative inverse number of a % m

-       rsaKeyGeneration:
            Input : Key size (number of bits)
            Output : Returns public key and private key for RSA

-       rsaEncrypt:
            Input : Plain text, e, n from public key
            Output : Cipher blocks and cipher text

-       rsaDecrypt:
            Input : Cipher blocks from rsaEncrypt, d, n
            Output : Plain text

# server.py =>
-       sendToClient:
            Input : A string of two letters, example :- 'ok', 'ab', etc...
            This function is used to send a message to the client

-       binaryToDecimal:
            Input : Takes in a binary representation in string format
            Output : Decimal equivalent of the binary representation

-       Steps involved in this particular file are:
            ~ Establishing server network to connect to the client and connect to the client
            ~ Generate RSA keys for server side and send the server_public_key to the client
            ~ Receive the required messages from the client such as :
                    cipher_text, encrypted_secret_key_blocks, signature_blocks, client_public_key
            ~ Decrypt the encrypted_secret_key
            ~ Decrypt the cipher_text
            ~ Verify the signature received from the client
            ~ Closing the server

# client.py =>
-       requestServerPublicKey:
            Returns server public key in integer formats : (e, n) , d

-       Steps involved in this particular file are:
            ~ Connect to the server
            ~ Request / receive server public key
            ~ Generate client public and private key using RSA key generation algorithm
            ~ Generate message digest using hash algorithm
            ~ Sign the message with a digital signature using RSA encryption to encrypt message digest
            ~ Encrypt the message with S-AES ( Simplified AES )
            ~ Encrypt the secret key with RSA algorithm using server public key
            ~ Send information to the server such as :
                    cipher_text, encrypted_secret_key_blocks, signature_blocks, client_public_key

# PrimeGenerator.py =>
-       millerRabinTest:
            If a number successfully passes this test then the probability of it being a prime number
            is high and if any number fails this test then we are sure that the number is not prime

-       smallPrimes:
            This function returns a list of all prime numbers ranging from 2 to 1000

-       isPrime:
            This is a function to check whether a number is prime or not

-       generateLargePrime:
            Function to generate large prime numbers used for selecting p and q

# hash.py=>
-       This file is for generating the message digest with the help of sha256 hash algorithm.

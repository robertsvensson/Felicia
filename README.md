# Felicia - an encryption comprehension and learning tool.

I wrote Felicia while studying for a security certification. I simply figured that encryption is so much easier to understand when you write up some code that performs cryptographic operations.

The idea behind Felicia is simple: first you write some text and then you encrypt it using a cipher, a key and an initialization vector of your choice. The cpihered text is then written to file. The ciphered text can now be reread back into Felicia decryption.

Use Felicia to experiment with different ciphers, keys lengths and initialization vectors. A good way to learn how encryption works is to provide the wrong key and/or cipher for decrypting the data and watch the data distortion unfold. 

Felica currently supports the following ciphers:
AES
Blowfish





Felica is most happy when she runs atop Python 2.7 with a little
help from PyCrypt https://www.dlitz.net/software/pycrypto/

# -*- coding: utf-8 -*-
"""
    Created: 10/11/2020
    Last modification: 10/11/2020

    @creator: coconutj

    Brief: Example file
"""

#-- Import --#
from aes_functions import Enc, Dec
#- End Import -#

def test_aes(plaintext, key):
	"""
	Run the AES cipher and inverse cipher to verify correctness
	- input: (bytes) plaintext, (bytes) key
	- output: None
	"""
	print("[+] Running test of AES.")
	print("Plaintext: {}\nKey: {}".format(' '.join(["%02x" % b for b in plaintext]), ' '.join(["%02x" % b for b in key])))
	ciphertext = Enc(plaintext, key)
	print("Ciphertext: {}".format(' '.join(["%02x" % b for b in ciphertext])))
	recovered_plaintext = Dec(ciphertext, key)
	print("Recovered plaintext: {}".format(' '.join(["%02x" % b for b in recovered_plaintext])))
	correct = plaintext == recovered_plaintext
	print("Correctness: {}".format(correct))
	if correct:
		print("[+] Test completed: PASS.\n")
	else:
		print("[+] Test completed: FAIL.\n")

if __name__ == '__main__':
	print("[+] Running examples of FIPS-197 standard.\n")
	# Test AES-128
	plaintext128 = b'\x32\x43\xf6\xa8\x88\x5a\x30\x8d\x31\x31\x98\xa2\xe0\x37\x07\x34'
	key128 = b'\x2b\x7e\x15\x16\x28\xae\xd2\xa6\xab\xf7\x15\x88\x09\xcf\x4f\x3c'
	test_aes(plaintext128, key128)

	plaintext = b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xaa\xbb\xcc\xdd\xee\xff'
	
	# Test AES-128
	key128 = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
	test_aes(plaintext, key128)
	
	# Test AES-192
	key192 = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17'
	test_aes(plaintext, key192)

	# Test AES-256
	key256 = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
	test_aes(plaintext, key256)